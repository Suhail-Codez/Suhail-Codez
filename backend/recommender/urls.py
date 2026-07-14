from django.urls import path
from . import views, admin_views
from .decorators import api_login_required, api_admin_required

# NOTE on protection: every endpoint below requires an authenticated session
# EXCEPT `health/`, which the sign-in and register pages call *before* the
# user is authenticated purely to prime the CSRF cookie (see signin.html /
# register.html -> ensureCSRF()). Protecting it too would break login itself.
#
# Endpoints under admin/* additionally require profile.role == 'admin' via
# `api_admin_required` -- a Patient account gets a 403 JSON response, never
# the underlying data, even if they call the URL directly.
urlpatterns = [
    path('health/',             views.health),  # intentionally public -- used to bootstrap CSRF pre-login

    path('conditions/',         api_login_required(views.conditions_list)),
    path('predict/',            api_login_required(views.predict)),
    path('recommend/',          api_login_required(views.recommend)),
    path('recommend/all/',      api_login_required(views.recommend_all)),
    path('sentiment/',          api_login_required(views.sentiment)),
    path('compare/',            api_login_required(views.compare_drugs)),
    path('dashboard/',          api_login_required(views.dashboard)),
    path('reviews/',            api_login_required(views.recent_reviews)),
    path('predictions/',        api_login_required(views.recent_predictions)),
    path('drug/',               api_login_required(views.drug_detail)),

    # Drug Search & Drug Report module
    path('drug/report/',        api_login_required(views.drug_report)),
    path('drug/report/pdf/',    api_login_required(views.drug_report_pdf)),
    path('drug/search/',        api_login_required(views.drug_search)),
    path('drug/buy/',           api_login_required(views.where_to_buy)),

    path('interactions/',       api_login_required(views.check_interactions)),
    path('disease/',            api_login_required(views.disease_info)),
    path('smart-recommend/',    api_login_required(views.symptom_recommend)),

    # Disease Diagnosis Report module
    path('diagnosis/report/',                      api_login_required(views.diagnosis_report_create)),
    path('diagnosis/reports/',                      api_login_required(views.diagnosis_report_list)),
    path('diagnosis/report/<int:report_id>/',       api_login_required(views.diagnosis_report_detail)),
    path('diagnosis/report/<int:report_id>/pdf/',   api_login_required(views.diagnosis_report_pdf)),

    # ── Admin-only: User Management ──────────────────────────────
    path('admin/users/',                    api_admin_required(admin_views.admin_users_list)),
    path('admin/users/<int:user_id>/role/', api_admin_required(admin_views.admin_user_set_role)),
    path('admin/users/<int:user_id>/toggle-active/', api_admin_required(admin_views.admin_user_toggle_active)),
    path('admin/users/<int:user_id>/',      api_admin_required(admin_views.admin_user_delete)),

    # ── Admin-only: Drug Database Management ─────────────────────
    path('admin/drugs/',                    api_admin_required(admin_views.admin_drugs_list_create)),
    path('admin/drugs/<int:drug_id>/',      api_admin_required(admin_views.admin_drug_detail)),

    # ── Admin-only: Audit Logs ────────────────────────────────────
    path('admin/audit-logs/',               api_admin_required(admin_views.admin_audit_logs)),

    # ── Admin-only: System Settings ───────────────────────────────
    path('admin/settings/',                 api_admin_required(admin_views.admin_system_settings)),

    # ── Admin-only: Extended Analytics ────────────────────────────
    path('admin/analytics/',                api_admin_required(admin_views.admin_analytics)),
]
