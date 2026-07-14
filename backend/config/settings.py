from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Deployment additions -------------------------------------------------
# Everything below reads from environment variables with the ORIGINAL
# hard-coded values kept as the fallback default, so local `python manage.py
# runserver` behaves exactly as before if no env vars are set. Business
# logic, models, views, and URLs are untouched.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'idpdr-mca-final-year-secure-key-2024-xk9pQ!v#mL')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'recommender',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static/ (css, js, manifest, icons) in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'config.wsgi.application'

# Defaults to the original sqlite3 file for local dev; if a managed host
# (Render/Railway/Vercel-Postgres/etc.) provides DATABASE_URL, that's used
# instead. Note: platforms with an ephemeral/read-only filesystem (e.g.
# Vercel serverless) cannot persist a sqlite file between requests, so a
# DATABASE_URL-backed Postgres is required there -- see DEPLOYMENT_GUIDE.md.
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Compressed + hashed filenames with a manifest, served efficiently by
# WhiteNoise -- required for `collectstatic` to work on Render/Railway/
# Vercel/Netlify. Falls back gracefully to plain serving if a referenced
# file is missing (avoids 500s from stale manifest entries in dev).
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

MODELS_DIR = os.path.join(BASE_DIR.parent, 'models_pkl')
SESSION_COOKIE_AGE = 86400 * 7  # used only when "Remember Me" is checked at login
LOGIN_URL = '/signin/'
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Password-reset emails are printed to the server console/log instead of
# requiring a real SMTP server -- swap EMAIL_BACKEND for a real SMTP backend
# in production.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'IDPDR <no-reply@idpdr.ai>'

# CSRF & Session fixes for local dev
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # JS must be able to read it
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

# --- Deployment additions -------------------------------------------------
# Add your deployed HTTPS domain(s) here via env var, e.g.
#   DJANGO_EXTRA_ORIGINS=https://myproject.vercel.app,https://myproject.onrender.com
# Django 4+ requires the scheme (https://) in CSRF_TRUSTED_ORIGINS.
_extra_origins = [o for o in os.environ.get('DJANGO_EXTRA_ORIGINS', '').split(',') if o]
CSRF_TRUSTED_ORIGINS += _extra_origins
CORS_ALLOWED_ORIGINS += _extra_origins
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
# ---------------------------------------------------------------------------
