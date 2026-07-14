"""
Vercel serverless entrypoint for the IDPDR Django app.

Vercel's Python runtime expects a WSGI/ASGI callable named `app` (or a
Flask-style `handler`) in this file. We simply point it at Django's
existing WSGI application -- no view/business logic is duplicated here.

IMPORTANT (see DEPLOYMENT_GUIDE.md "Vercel" section):
Vercel functions run on an ephemeral, read-only filesystem, so the bundled
db.sqlite3 file cannot be written to in production. Set a DATABASE_URL
env var pointing at a managed Postgres (Vercel Postgres, Neon, Supabase,
Railway Postgres, etc.) before deploying, or the app will error on any
write (registration, login history, predictions, etc).
"""
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
