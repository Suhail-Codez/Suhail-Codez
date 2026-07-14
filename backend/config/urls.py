from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve as static_serve
from recommender import auth_views

urlpatterns = [
    path('admin/',              admin.site.urls),
    path('api/',                include('recommender.urls')),

    # PWA: service worker must be served from the site root (not /static/)
    # so its default scope is "/" and it can control every page. manifest.json
    # and offline.html are exposed at the root for the same reason /
    # convenience -- they still live physically under backend/static/.
    path('service-worker.js', static_serve, {'path': 'service-worker.js', 'document_root': settings.BASE_DIR / 'static'}),
    path('manifest.json',     static_serve, {'path': 'manifest.json',     'document_root': settings.BASE_DIR / 'static'}),
    path('offline.html',      static_serve, {'path': 'offline.html',      'document_root': settings.BASE_DIR / 'static'}),

    # Auth pages
    path('signin/',                          auth_views.signin_page,             name='signin'),
    path('register/',                        auth_views.register_page,           name='register'),
    path('signout/',                         auth_views.signout_view,            name='signout'),
    path('forgot-password/',                 auth_views.forgot_password_page,    name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', auth_views.reset_password_page,     name='reset_password'),
    path('admin-dashboard/',                 auth_views.admin_dashboard_page,    name='admin_dash'),

    # Auth API
    path('api/auth/register/',          auth_views.api_register),
    path('api/auth/login/',             auth_views.api_login),
    path('api/auth/me/',                auth_views.api_me),
    path('api/auth/forgot-password/',   auth_views.api_forgot_password),
    path('api/auth/reset-password/',    auth_views.api_reset_password),
    path('api/auth/change-password/',   auth_views.api_change_password),
    path('api/auth/profile/update/',    auth_views.api_update_profile),
    path('api/auth/save-diagnosis/',    auth_views.api_save_diagnosis),
    path('api/auth/my-diagnoses/',      auth_views.api_my_diagnoses),
    path('api/auth/admin-stats/',       auth_views.api_admin_stats),

    # Main SPA (Patient Dashboard) — gated behind login. Unauthenticated
    # visitors are redirected to /signin/ instead of the dashboard ever
    # being rendered for a guest.
    path('',                    auth_views.home_page, name='home'),
]
