"""
IDPDR Auth Views v1.0
Handles sign-in, register, sign-out, forgot/reset password, profile
management, and the page-level gate for the Patient Dashboard vs. Admin
Dashboard.

Role model: every user has a UserProfile.role of either 'patient' or
'admin'. There is a single login form; the role returned by /api/auth/login/
determines which dashboard the frontend redirects to, and every admin-only
page/endpoint independently re-checks profile.role == 'admin' server-side
(never trusts the client), so a patient can never reach an admin page even
by guessing the URL.

Security hardening carried over from v3.1:
- All protected/auth-adjacent pages use @never_cache so the Back/Forward
  button can't resurrect a cached copy after logout.
- Login/register/profile endpoints are NOT @csrf_exempt.
- "Remember Me" is honored explicitly (persistent vs. browser-session cookie).
- Logout fully flushes the session.
New in v4.0:
- Forgot Password / Reset Password flow (token-based, no real SMTP needed --
  uses Django's console email backend so the reset link is visible in the
  server log for this environment; see settings.py).
- Change Password (while logged in) and Profile view/update endpoints.
- AuditLog entries written for login, logout, register, password changes,
  and profile updates.
- Admin Dashboard page now also verifies profile.role == 'admin' (previously
  only checked login), so a signed-in patient hitting /admin-dashboard/
  directly is redirected back to their own dashboard instead of ever seeing
  admin markup.
"""
import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.db.models import Count

from .models import UserProfile, SavedDiagnosis, DrugReview, Prediction, DrugComparison, SystemSettings
from .audit import log_action


def _is_admin(user):
    profile = getattr(user, 'profile', None)
    return bool(profile and profile.role == 'admin')


# ── Page views ──────────────────────────────────────────────────
@never_cache
def signin_page(request):
    if request.user.is_authenticated:
        return redirect('/admin-dashboard/' if _is_admin(request.user) else '/')
    return render(request, 'signin.html')


@never_cache
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/admin-dashboard/' if _is_admin(request.user) else '/')
    return render(request, 'register.html')


@never_cache
def forgot_password_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'forgot_password.html')


@never_cache
def reset_password_page(request, uidb64, token):
    """Validates the reset link before rendering the 'set new password' form
    so an expired/invalid link shows a clear error instead of a broken form."""
    valid = False
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        valid = default_token_generator.check_token(user, token)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        valid = False
    return render(request, 'reset_password.html', {'valid': valid, 'uidb64': uidb64, 'token': token})


@never_cache
def signout_view(request):
    """Fully destroy the session so Back-button navigation cannot restore
    access to protected pages after logout."""
    if request.user.is_authenticated:
        log_action(request, 'logout')
    logout(request)          # rotates the session key and clears request.session
    request.session.flush()  # explicitly deletes the session store + cookie data
    response = redirect('/signin/')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@never_cache
def home_page(request):
    """The Patient Dashboard (application root). Always requires
    authentication -- if the session isn't valid, the user is redirected
    straight to the Login page instead of the dashboard ever being rendered
    for a guest. Admins can still open this to use the diagnosis/drug tools,
    but the moment they log in they land on the Admin Dashboard instead
    (see api_login's `redirect` field)."""
    if not request.user.is_authenticated:
        return redirect(f"/signin/?next={request.path}")
    return render(request, 'index.html')


@never_cache
def admin_dashboard_page(request):
    """Admin-only. A signed-in patient hitting this URL directly is bounced
    back to their own dashboard -- role is re-verified server-side on every
    request, never trusted from the client."""
    if not request.user.is_authenticated:
        return redirect(f"/signin/?next={request.path}")
    if not _is_admin(request.user):
        return redirect('/')
    return render(request, 'admin_dashboard.html')


# ── API endpoints ───────────────────────────────────────────────
# NOTE: these are intentionally NOT @csrf_exempt. The frontend primes the
# CSRF cookie via GET /api/health/ before rendering the form and sends the
# token back as the X-CSRFToken header (see signin.html / register.html),
# so genuine CSRF protection is enforced end-to-end.
@require_http_methods(["POST"])
def api_register(request):
    try:
        settings_row = SystemSettings.load()
        if not settings_row.allow_registration:
            return JsonResponse({'error': 'New account registration is currently disabled by the administrator.'}, status=403)

        data = json.loads(request.body)
        username   = data.get('username', '').strip()
        email      = data.get('email', '').strip()
        password   = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name  = data.get('last_name', '').strip()

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        if len(password) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)
        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # All self-service signups are Patients. Admin accounts are only
        # created by an existing admin (via User Management) or the
        # `seed_admin` management command -- never through public registration.
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        UserProfile.objects.create(user=user, role='patient')
        login(request, user)
        log_action(request, 'register', detail=f"New patient account: {username}", user=user)
        return JsonResponse({
            'success': True,
            'message': f'Welcome, {first_name or username}!',
            'username': username,
            'role': 'patient',
            'redirect': '/',
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_login(request):
    try:
        data       = json.loads(request.body)
        username   = data.get('username', '').strip()
        password   = data.get('password', '')
        remember   = bool(data.get('remember') or data.get('remember_me'))

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        if not user.is_active:
            return JsonResponse({'error': 'This account has been deactivated. Contact an administrator.'}, status=403)

        profile = getattr(user, 'profile', None)
        role = profile.role if profile else 'patient'

        settings_row = SystemSettings.load()
        if settings_row.maintenance_mode and role != 'admin':
            return JsonResponse({'error': 'The system is currently under maintenance. Please try again later.'}, status=503)

        login(request, user)

        # "Remember Me" must be opted into explicitly. If it isn't checked,
        # the session cookie expires when the browser closes; only a
        # deliberate opt-in grants a persistent (SESSION_COOKIE_AGE) session.
        if remember:
            request.session.set_expiry(None)  # uses SESSION_COOKIE_AGE from settings
        else:
            request.session.set_expiry(0)  # expire at browser close

        log_action(request, 'login', detail=f"role={role}, remember={remember}")

        return JsonResponse({
            'success': True,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'role': role,
            'message': f'Welcome back, {user.first_name or user.username}!',
            'redirect': '/admin-dashboard/' if role == 'admin' else '/',
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False})
    profile = getattr(request.user, 'profile', None)
    return JsonResponse({
        'authenticated': True,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'role': profile.role if profile else 'patient',
        'phone': profile.phone if profile else '',
        'age': profile.age if profile else None,
        'gender': profile.gender if profile else '',
        'bio': profile.bio if profile else '',
        'email_notifications': profile.email_notifications if profile else True,
        'date_joined': request.user.date_joined.strftime('%Y-%m-%d'),
    })


# ── Forgot / Reset Password ─────────────────────────────────────
@require_http_methods(["POST"])
def api_forgot_password(request):
    """
    Accepts a username or email. Always returns a generic success message
    regardless of whether the account exists (prevents account enumeration).
    The reset email is sent through Django's configured EMAIL_BACKEND -- in
    this project that's the console backend, so for local/demo use the
    reset link is printed to the server log/console instead of requiring a
    real SMTP server.
    """
    try:
        data = json.loads(request.body)
        identifier = (data.get('username') or data.get('email') or '').strip()
        generic_response = JsonResponse({
            'success': True,
            'message': "If an account matches that username/email, a password reset link has been sent."
        })
        if not identifier:
            return JsonResponse({'error': 'Username or email is required'}, status=400)

        user = User.objects.filter(username=identifier).first() or User.objects.filter(email__iexact=identifier).first()
        if not user:
            return generic_response

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(f"/reset-password/{uidb64}/{token}/")

        send_mail(
            subject="IDPDR — Password Reset Request",
            message=(
                f"Hello {user.first_name or user.username},\n\n"
                f"We received a request to reset your IDPDR password. "
                f"Click the link below to choose a new password:\n\n{reset_link}\n\n"
                f"This link will expire after it's used once or after Django's "
                f"default token timeout. If you didn't request this, you can "
                f"safely ignore this email.\n\n— IDPDR"
            ),
            from_email=None,
            recipient_list=[user.email] if user.email else [f"{user.username}@example.invalid"],
            fail_silently=True,
        )
        log_action(request, 'password_reset', detail=f"Reset link requested for {user.username}", user=user)
        return generic_response
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_reset_password(request):
    """Consumes a {uidb64, token, new_password} payload from the Reset
    Password page and sets the new password if the token is valid."""
    try:
        data = json.loads(request.body)
        uidb64 = data.get('uidb64', '')
        token = data.get('token', '')
        new_password = data.get('new_password', '')

        if not (uidb64 and token and new_password):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        if len(new_password) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return JsonResponse({'error': 'Invalid or expired reset link'}, status=400)

        if not default_token_generator.check_token(user, token):
            return JsonResponse({'error': 'Invalid or expired reset link'}, status=400)

        user.set_password(new_password)
        user.save()
        log_action(request, 'password_reset', detail=f"Password reset completed for {user.username}", user=user)
        return JsonResponse({'success': True, 'message': 'Password reset successful. You can now sign in.'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_change_password(request):
    """Change password while logged in (requires current password)."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        if not authenticate(request, username=request.user.username, password=current_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        if len(new_password) < 6:
            return JsonResponse({'error': 'New password must be at least 6 characters'}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # keep the current session valid
        log_action(request, 'password_change')
        return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ── Profile management ──────────────────────────────────────────
@require_http_methods(["POST"])
def api_update_profile(request):
    """Update the signed-in user's own profile (My Profile / Account Settings)."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'patient'})

        if 'first_name' in data: user.first_name = data.get('first_name', '').strip()
        if 'last_name' in data: user.last_name = data.get('last_name', '').strip()
        if 'email' in data:
            new_email = data.get('email', '').strip()
            if new_email and User.objects.filter(email__iexact=new_email).exclude(pk=user.pk).exists():
                return JsonResponse({'error': 'That email is already in use by another account'}, status=400)
            user.email = new_email
        user.save()

        if 'phone' in data: profile.phone = data.get('phone', '').strip()
        if 'age' in data:
            try:
                profile.age = int(data['age']) if data['age'] not in (None, '') else None
            except (TypeError, ValueError):
                pass
        if 'gender' in data: profile.gender = data.get('gender', '').strip()
        if 'bio' in data: profile.bio = data.get('bio', '').strip()[:300]
        if 'email_notifications' in data: profile.email_notifications = bool(data.get('email_notifications'))
        profile.save()

        log_action(request, 'profile_update')
        return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_save_diagnosis(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        SavedDiagnosis.objects.create(
            user=request.user,
            symptoms=data.get('symptoms', ''),
            condition=data.get('condition', ''),
            top_drug=data.get('top_drug', ''),
        )
        return JsonResponse({'success': True, 'message': 'Diagnosis saved!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_my_diagnoses(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    diagnoses = SavedDiagnosis.objects.filter(user=request.user).order_by('-created_at')[:20]
    return JsonResponse({'diagnoses': [
        {'id': d.id, 'condition': d.condition, 'top_drug': d.top_drug,
         'symptoms': d.symptoms[:80], 'date': d.created_at.strftime('%b %d, %Y')}
        for d in diagnoses
    ]})


def api_admin_stats(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'admin':
        return JsonResponse({'error': 'Admin access required'}, status=403)

    return JsonResponse({
        'total_users':       User.objects.count(),
        'total_reviews':     DrugReview.objects.count(),
        'total_predictions': Prediction.objects.count(),
        'total_comparisons': DrugComparison.objects.count(),
        'total_diagnoses':   SavedDiagnosis.objects.count(),
        'top_conditions': list(
            Prediction.objects.values('predicted_condition')
            .annotate(count=Count('id')).order_by('-count')[:5]
        ),
        'recent_users': [
            {'username': u.username, 'email': u.email, 'joined': u.date_joined.strftime('%b %d, %Y'),
             'role': getattr(u, 'profile', None).role if hasattr(u, 'profile') else 'patient'}
            for u in User.objects.order_by('-date_joined')[:5]
        ],
    })
