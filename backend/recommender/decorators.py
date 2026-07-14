"""
decorators — auth helpers for API views.

DRF's @api_view functions don't play well with Django's default
login_required (which redirects to LOGIN_URL and returns HTML). For a JSON
API we want a clean 401/403 JSON response instead, so the frontend can react
to it (e.g. redirect to /signin/) rather than trying to render an HTML login
page inside a fetch() call.
"""
from functools import wraps

from django.http import JsonResponse


def api_login_required(view_func):
    """Wrap a DRF view so it returns 401 JSON if the session isn't authenticated.

    Uses django.http.JsonResponse (not DRF's Response) for the 401 case
    because this decorator wraps the already-@api_view-decorated function
    from the outside, in urls.py -- a DRF Response short-circuited before
    reaching APIView.dispatch() never gets a renderer attached and would
    raise "accepted_renderer not set". JsonResponse needs no such setup.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication required. Please sign in.", "authenticated": False},
                status=401,
            )
        return view_func(request, *args, **kwargs)
    return _wrapped


def api_admin_required(view_func):
    """Like api_login_required, but additionally requires profile.role == 'admin'.
    Used for every admin-only API endpoint (user management, drug management,
    audit logs, system settings, admin analytics). RBAC is enforced here --
    server-side, on every request -- so a Patient account can never reach
    these endpoints no matter what the client sends."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication required. Please sign in.", "authenticated": False},
                status=401,
            )
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != "admin":
            return JsonResponse(
                {"error": "Admin access required.", "authenticated": True},
                status=403,
            )
        return view_func(request, *args, **kwargs)
    return _wrapped
