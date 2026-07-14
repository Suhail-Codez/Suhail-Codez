"""
IDPDR Admin Views v1.0
Every view in this module is wrapped in `api_admin_required` at the URL
level (see urls.py) -- none of it is reachable by a Patient account, even
if they know the endpoint path, because the decorator re-checks
`profile.role == 'admin'` from the database on every request.

Covers the Admin Dashboard's:
  - User Management (list/search, change role, activate/deactivate, delete)
  - Drug Database Management (CRUD on the `Drug` model, merged into patient
    Drug Search/Drug Report alongside the built-in curated knowledge base)
  - Audit Logs (view/filter security-relevant events)
  - System Settings (registration toggle, maintenance mode, site branding)
  - Analytics (extended platform-wide statistics)
"""
import json

from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (DrugReview, Prediction, DrugComparison, SavedDiagnosis, DiagnosisReport,
                      UserProfile, Drug, AuditLog, SystemSettings, SearchLog)
from .audit import log_action


# ── User Management ─────────────────────────────────────────────
@api_view(["GET"])
def admin_users_list(request):
    """List all users with role/status, optionally filtered by a search query."""
    q = request.GET.get("q", "").strip()
    users = User.objects.select_related("profile").order_by("-date_joined")
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q) |
                              Q(first_name__icontains=q) | Q(last_name__icontains=q))
    data = []
    for u in users[:200]:
        profile = getattr(u, "profile", None)
        data.append({
            "id": u.id, "username": u.username, "email": u.email,
            "first_name": u.first_name, "last_name": u.last_name,
            "role": profile.role if profile else "patient",
            "is_active": u.is_active,
            "date_joined": u.date_joined.strftime("%b %d, %Y"),
            "last_login": u.last_login.strftime("%b %d, %Y %I:%M %p") if u.last_login else "Never",
        })
    return Response({"users": data, "total": users.count()})


@api_view(["POST"])
def admin_user_set_role(request, user_id):
    """Promote/demote a user between 'patient' and 'admin'."""
    new_role = request.data.get("role")
    if new_role not in ("patient", "admin"):
        return Response({"error": "role must be 'patient' or 'admin'"}, status=400)
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found"}, status=404)
    if user.id == request.user.id and new_role != "admin":
        return Response({"error": "You cannot remove your own admin role"}, status=400)

    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"role": "patient"})
    old_role = profile.role
    profile.role = new_role
    profile.save()
    log_action(request, "role_change", detail=f"{user.username}: {old_role} -> {new_role}")
    return Response({"success": True, "message": f"{user.username} is now {'an Administrator' if new_role=='admin' else 'a Patient'}."})


@api_view(["POST"])
def admin_user_toggle_active(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found"}, status=404)
    if user.id == request.user.id:
        return Response({"error": "You cannot deactivate your own account"}, status=400)
    user.is_active = not user.is_active
    user.save()
    log_action(request, "user_activated" if user.is_active else "user_deactivated", detail=user.username)
    return Response({"success": True, "is_active": user.is_active,
                      "message": f"{user.username} {'activated' if user.is_active else 'deactivated'}."})


@api_view(["DELETE"])
def admin_user_delete(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found"}, status=404)
    if user.id == request.user.id:
        return Response({"error": "You cannot delete your own account"}, status=400)
    username = user.username
    user.delete()
    log_action(request, "user_deleted", detail=username)
    return Response({"success": True, "message": f"User {username} deleted."})


# ── Drug Database Management ────────────────────────────────────
def _serialize_drug(d):
    return {
        "id": d.id, "name": d.name, "generic_name": d.generic_name,
        "brand_names": d.brand_names, "drug_class": d.drug_class,
        "condition": d.condition, "description": d.description, "dosage": d.dosage,
        "side_effects": d.side_effects, "contraindications": d.contraindications,
        "price_inr": d.price_inr, "prescription_required": d.prescription_required,
        "is_active": d.is_active,
        "created_by": d.created_by.username if d.created_by else None,
        "created_at": d.created_at.strftime("%b %d, %Y"),
    }


@api_view(["GET", "POST"])
def admin_drugs_list_create(request):
    if request.method == "GET":
        q = request.GET.get("q", "").strip()
        drugs = Drug.objects.all()
        if q:
            drugs = drugs.filter(Q(name__icontains=q) | Q(generic_name__icontains=q) | Q(condition__icontains=q))
        return Response({"drugs": [_serialize_drug(d) for d in drugs], "total": drugs.count()})

    # POST -- create
    name = (request.data.get("name") or "").strip()
    if not name:
        return Response({"error": "Drug name is required"}, status=400)
    if Drug.objects.filter(name__iexact=name).exists():
        return Response({"error": f"A managed drug named '{name}' already exists"}, status=400)

    drug = Drug.objects.create(
        name=name,
        generic_name=(request.data.get("generic_name") or "").strip(),
        brand_names=(request.data.get("brand_names") or "").strip(),
        drug_class=(request.data.get("drug_class") or "").strip(),
        condition=(request.data.get("condition") or "").strip(),
        description=(request.data.get("description") or "").strip(),
        dosage=(request.data.get("dosage") or "").strip(),
        side_effects=(request.data.get("side_effects") or "").strip(),
        contraindications=(request.data.get("contraindications") or "").strip(),
        price_inr=(request.data.get("price_inr") or "").strip(),
        prescription_required=bool(request.data.get("prescription_required", True)),
        created_by=request.user,
    )
    log_action(request, "drug_created", detail=drug.name)
    return Response({"success": True, "drug": _serialize_drug(drug)}, status=201)


@api_view(["GET", "PUT", "DELETE"])
def admin_drug_detail(request, drug_id):
    drug = Drug.objects.filter(id=drug_id).first()
    if not drug:
        return Response({"error": "Drug not found"}, status=404)

    if request.method == "GET":
        return Response(_serialize_drug(drug))

    if request.method == "DELETE":
        name = drug.name
        drug.delete()
        log_action(request, "drug_deleted", detail=name)
        return Response({"success": True, "message": f"Drug '{name}' deleted."})

    # PUT -- update
    for field in ["name", "generic_name", "brand_names", "drug_class", "condition",
                  "description", "dosage", "side_effects", "contraindications", "price_inr"]:
        if field in request.data:
            setattr(drug, field, (request.data.get(field) or "").strip())
    if "prescription_required" in request.data:
        drug.prescription_required = bool(request.data.get("prescription_required"))
    if "is_active" in request.data:
        drug.is_active = bool(request.data.get("is_active"))
    drug.save()
    log_action(request, "drug_updated", detail=drug.name)
    return Response({"success": True, "drug": _serialize_drug(drug)})


# ── Audit Logs ───────────────────────────────────────────────────
@api_view(["GET"])
def admin_audit_logs(request):
    action_filter = request.GET.get("action", "").strip()
    q = request.GET.get("q", "").strip()
    logs = AuditLog.objects.all()
    if action_filter:
        logs = logs.filter(action=action_filter)
    if q:
        logs = logs.filter(Q(username_snapshot__icontains=q) | Q(detail__icontains=q))
    logs = logs[:300]
    return Response({
        "logs": [{
            "id": l.id, "action": l.action, "action_display": l.get_action_display(),
            "username": l.username_snapshot, "detail": l.detail, "ip_address": l.ip_address,
            "created_at": l.created_at.strftime("%b %d, %Y %I:%M %p"),
        } for l in logs],
        "total": AuditLog.objects.count(),
        "action_choices": [{"value": v, "label": lbl} for v, lbl in AuditLog.ACTION_CHOICES],
    })


# ── System Settings ─────────────────────────────────────────────
@api_view(["GET", "POST"])
def admin_system_settings(request):
    settings_row = SystemSettings.load()
    if request.method == "GET":
        return Response({
            "allow_registration": settings_row.allow_registration,
            "maintenance_mode": settings_row.maintenance_mode,
            "site_name": settings_row.site_name,
            "support_email": settings_row.support_email,
            "updated_at": settings_row.updated_at.strftime("%b %d, %Y %I:%M %p"),
        })

    if "allow_registration" in request.data:
        settings_row.allow_registration = bool(request.data.get("allow_registration"))
    if "maintenance_mode" in request.data:
        settings_row.maintenance_mode = bool(request.data.get("maintenance_mode"))
    if "site_name" in request.data:
        settings_row.site_name = (request.data.get("site_name") or "IDPDR").strip()
    if "support_email" in request.data:
        settings_row.support_email = (request.data.get("support_email") or "").strip()
    settings_row.save()
    log_action(request, "settings_updated", detail=json.dumps(request.data))
    return Response({"success": True, "message": "System settings updated."})


# ── Analytics (extended admin-only stats) ───────────────────────
@api_view(["GET"])
def admin_analytics(request):
    return Response({
        "total_users": User.objects.count(),
        "total_patients": UserProfile.objects.filter(role="patient").count(),
        "total_admins": UserProfile.objects.filter(role="admin").count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "inactive_users": User.objects.filter(is_active=False).count(),
        "total_reviews": DrugReview.objects.count(),
        "total_predictions": Prediction.objects.count(),
        "total_diagnosis_reports": DiagnosisReport.objects.count(),
        "total_managed_drugs": Drug.objects.count(),
        "total_searches": SearchLog.objects.count(),
        "sentiment_breakdown": list(
            DrugReview.objects.values("sentiment").annotate(count=Count("id")).order_by("-count")
        ),
        "top_conditions": list(
            Prediction.objects.values("predicted_condition")
            .annotate(count=Count("id")).order_by("-count")[:8]
        ),
        "avg_rating_by_condition": list(
            DrugReview.objects.values("condition")
            .annotate(avg_rating=Avg("rating"), count=Count("id"))
            .order_by("-count")[:8]
        ),
        "recent_registrations": [
            {"username": u.username, "joined": u.date_joined.strftime("%b %d, %Y")}
            for u in User.objects.order_by("-date_joined")[:8]
        ],
    })
