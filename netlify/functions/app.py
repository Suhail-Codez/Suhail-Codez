"""
Netlify Function entrypoint for the IDPDR Django app.
Wraps Django's WSGI application using `serverless-wsgi` so Netlify's
Lambda-style function invocation can call into Django unmodified.

Same caveat as the Vercel entrypoint: Netlify's filesystem is ephemeral,
so db.sqlite3 writes will NOT persist between invocations. Set DATABASE_URL
to a managed Postgres instance before using this in real deployments.
"""
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import serverless_wsgi  # noqa: E402
from django.core.wsgi import get_wsgi_application  # noqa: E402

django_app = get_wsgi_application()

def handler(event, context):
    return serverless_wsgi.handle_request(django_app, event, context)
