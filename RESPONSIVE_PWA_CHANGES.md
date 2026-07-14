# Responsive Redesign + PWA Conversion — Change Log

This document explains every change made to convert IDPDR into a
responsive, installable PWA. **No business logic, view, model, URL
route, or API behavior was modified or removed** — every change below is
additive (new files) or purely presentational (CSS/meta tags/markup for
navigation chrome).

## New files added

| File | Purpose |
|---|---|
| `backend/static/css/responsive.css` | Mobile-first responsive layer: fluid typography, 44×44px touch targets, table→scroll/stack handling, grid stacking at 1024/768/480px, off-canvas sidebar, safe-area padding for notched phones, focus-visible rings, reduced-motion support, install-banner styling. Loaded *after* each page's own `<style>` block so it can override without editing existing rules. |
| `backend/static/js/pwa-register.js` | Registers the service worker; shows an "Install app" banner on Android/Chrome/Edge (via `beforeinstallprompt`) and an "Add to Home Screen" hint on iOS Safari (which has no install-prompt API). |
| `backend/static/service-worker.js` | Caches the app shell (CSS/JS/icons/manifest) for offline use; network-first for `/api/*` GET requests with cache fallback; never intercepts POST/PUT/DELETE so data writes always hit the server. |
| `backend/static/manifest.json` | Web App Manifest — app name, icons, `theme_color`/`background_color`, `display: standalone`, so the app installs with its own icon and splash screen. |
| `backend/static/offline.html` | Fallback page shown by the service worker when a page navigation fails with no network. |
| `backend/static/icons/*.png` + `generate_icons.py` | 192px/512px/maskable/apple-touch/favicon icons generated from the app's existing brand gradient (`--primary` → `--purple`), plus the script that generated them (re-run any time to regenerate). |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment instructions for Render, Railway, Vercel, Netlify. |
| `Procfile`, `runtime.txt`, `render.yaml`, `railway.json`, `vercel.json`, `api/index.py`, `netlify.toml`, `netlify/functions/app.py`, `netlify/requirements-netlify.txt`, `.env.example`, `.gitignore` | Production/deployment configuration for the four requested hosts. |

## Changes to existing files

### `backend/templates/index.html` (Patient Dashboard)
- Added `{% load static %}`, `viewport-fit=cover` (for notched phones),
  manifest link, theme-color/apple PWA meta tags, favicon/apple-touch-icon
  links.
- Linked `responsive.css` right before `</head>` and `pwa-register.js`
  right before `</body>`.
- No CSS rules, JS functions, or markup structure were deleted — the
  page already had a working hamburger/drawer pattern (`openSidebar()` /
  `closeSidebar()` / `.sidebar-overlay`), which the new stylesheet builds
  on rather than replaces.

### `backend/templates/admin_dashboard.html` (Admin Dashboard)
- Same head additions as above.
- **This page previously had no mobile navigation at all** (no hamburger
  button, no drawer, no `@media` queries). Added:
  - a `.hamburger` button in the topbar and a `.sidebar-overlay` div
    (mirroring the pattern already used in `index.html`),
  - `openSidebar()` / `closeSidebar()` JS functions,
  - a call to `closeSidebar()` inside the existing `showPage()` function
    so the drawer auto-closes after choosing a section on mobile.
- Wrapped the two data tables that weren't already inside a
  `.table-wrap` scroll container (`#users-table`, `#preds-table`) so they
  scroll horizontally instead of overflowing the viewport.

### `backend/templates/signin.html`, `register.html`, `forgot_password.html`, `reset_password.html`
- Same head additions (manifest, PWA meta, `responsive.css`,
  `pwa-register.js`). These pages were already reasonably responsive
  (centered, `max-width` card layout) — the shared stylesheet adds fluid
  type, 44px touch targets, and 16px input font-size (prevents iOS
  Safari's auto-zoom-on-focus).

### `backend/config/settings.py`
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` now read from environment
  variables, **falling back to the exact original hard-coded values** if
  unset — local `runserver` behavior is unchanged.
- Added `whitenoise.middleware.WhiteNoiseMiddleware` so static files
  (CSS/JS/manifest/icons) are served correctly in production without a
  separate CDN/nginx step.
- Added `STORAGES['staticfiles']` using WhiteNoise's compressed-manifest
  storage (required for `collectstatic` on all four hosting platforms).
- `DATABASES` now uses `DATABASE_URL` (via `dj_database_url`) when
  present, otherwise falls back to the original `db.sqlite3` file —
  unchanged for local development.
- Added `DJANGO_EXTRA_ORIGINS` env var to extend
  `CSRF_TRUSTED_ORIGINS`/`CORS_ALLOWED_ORIGINS` with your deployed HTTPS
  domain, plus `SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE` when
  `DEBUG=False`.

### `backend/config/urls.py`
- Added three routes — `/service-worker.js`, `/manifest.json`,
  `/offline.html` — served from `backend/static/` at the site **root**
  (rather than under `/static/`) so the service worker's default scope
  is `/` and it can control every page. No existing routes were changed,
  reordered in a breaking way, or removed.

### `backend/requirements.txt`
- Added `gunicorn` (production WSGI server), `whitenoise` (static file
  serving), `dj-database-url` (Postgres URL parsing). All existing
  packages/pins are untouched.

## What was intentionally left alone

- All Django views, models, serializers, migrations, the ML
  pipeline (`recommender/drug_data.py`, `models_pkl/*`), and REST API
  endpoints are byte-for-byte unchanged.
- `db.sqlite3` and its schema are untouched (production deployments that
  need persistence use `DATABASE_URL` instead of modifying this file).
- Existing inline `<style>` blocks in every template are still intact;
  the new `responsive.css` file only adds overriding rules loaded after
  them.
