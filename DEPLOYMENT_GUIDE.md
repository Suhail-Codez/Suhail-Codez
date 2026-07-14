# IDPDR — Deployment Guide

This guide explains how to publish IDPDR so it's reachable from any
phone, tablet, or desktop at a single public HTTPS URL, and how to
install it as an app from that URL.

## 0. Which platform should I actually use?

IDPDR is a **Django** app (server-rendered templates + a SQLite database +
scikit-learn model files loaded from disk). That matters for hosting:

| Platform | Fit | Why |
|---|---|---|
| **Render** | ✅ Best fit | Native long-running Python web service, persistent disk option, free Postgres, `render.yaml` included — one click. |
| **Railway** | ✅ Best fit | Same as Render: native Python process, easy Postgres add-on, `railway.json` included. |
| **Vercel** | ⚠️ Works with caveats | Vercel runs Python as short-lived serverless functions with a **read-only, ephemeral filesystem** — `db.sqlite3` cannot be written to. You must attach a managed Postgres (Vercel Postgres/Neon/Supabase) via `DATABASE_URL`. Cold starts also mean the first request after idle reloads the scikit-learn model files, which can take a few seconds. |
| **Netlify** | ⚠️ Works, not ideal | Same serverless/ephemeral-filesystem limitation as Vercel, via a `serverless-wsgi` shim. Netlify's Python function support is less mature than Vercel's. Use this only if your organization already standardizes on Netlify. |

**Recommendation:** deploy to **Render or Railway** for the real/primary
public URL. The Vercel and Netlify configs are included and functional,
but budget extra setup time for the Postgres requirement.

All four configs are already in the repo root:
`render.yaml`, `railway.json`, `vercel.json` + `api/index.py`,
`netlify.toml` + `netlify/functions/app.py`.

---

## 1. Render (recommended)

1. Push this project to a GitHub repository.
2. In the Render dashboard: **New → Blueprint**, pick the repo. Render
   reads `render.yaml` automatically and provisions:
   - a **Web Service** (Python, root dir `backend/`)
   - a free **Postgres** database, wired up via `DATABASE_URL`
3. Render auto-generates `DJANGO_SECRET_KEY` and sets `DJANGO_DEBUG=False`.
   After the first deploy, open the service's **Environment** tab and set
   `DJANGO_EXTRA_ORIGINS` to your actual `https://<your-service>.onrender.com`
   URL (the placeholder in `render.yaml` won't match your generated name).
4. Click **Deploy**. Render runs `collectstatic` + `migrate` automatically
   (see `buildCommand` in `render.yaml`), then starts Gunicorn.
5. Your public URL is `https://<your-service-name>.onrender.com`.

**Manual (no Blueprint) alternative:** New → Web Service → connect repo →
set **Root Directory** to `backend` → Build Command
`pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
→ Start Command `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.

---

## 2. Railway (recommended)

1. Push the project to GitHub.
2. In Railway: **New Project → Deploy from GitHub repo**. Railway detects
   `railway.json` and uses its build/start commands automatically.
3. Add a **Postgres** plugin (New → Database → PostgreSQL). Railway
   injects `DATABASE_URL` into your service automatically.
4. In the service's **Variables** tab, add:
   - `DJANGO_SECRET_KEY` (generate with
     `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=.up.railway.app`
   - `DJANGO_EXTRA_ORIGINS=https://<your-generated-subdomain>.up.railway.app`
5. Under **Settings → Networking**, click **Generate Domain** to get your
   public `https://xxxx.up.railway.app` URL.

---

## 3. Vercel

1. Push the project to GitHub, import it in Vercel.
2. Attach a managed Postgres (Vercel Postgres, or an external one like
   Neon/Supabase) and copy its connection string.
3. In **Project Settings → Environment Variables**, set:
   - `DATABASE_URL` = the Postgres connection string (**required** — see
     the fit table above)
   - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=.vercel.app`
   - `DJANGO_EXTRA_ORIGINS=https://<your-project>.vercel.app`
4. Vercel reads `vercel.json`, which routes all traffic to
   `api/index.py` (a thin wrapper around Django's WSGI app) and serves
   `/static/*` from the pre-built `backend/staticfiles/` directory.
5. Before the first deploy, run `python backend/manage.py collectstatic
   --noinput` locally (or via a Vercel build step) so `staticfiles/`
   exists in the deployed bundle, and run `python backend/manage.py
   migrate` once against the Postgres database (e.g. from your machine
   with `DATABASE_URL` exported).
6. Your public URL is `https://<your-project>.vercel.app`.

---

## 4. Netlify

1. Push to GitHub, import the site in Netlify.
2. Netlify reads `netlify.toml`: it builds from `backend/`, runs
   `collectstatic`, and routes all non-static requests to the
   `netlify/functions/app.py` function (a `serverless-wsgi` wrapper
   around the same Django app, no logic duplicated).
3. Attach a managed Postgres exactly as in the Vercel section — same
   ephemeral-filesystem limitation applies — and set the same
   `DATABASE_URL`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`,
   `DJANGO_ALLOWED_HOSTS=.netlify.app`, `DJANGO_EXTRA_ORIGINS` variables
   in **Site settings → Environment variables**.
4. Run `migrate` once against the Postgres DB from your machine before
   the first real request.
5. Your public URL is `https://<your-site-name>.netlify.app`.

---

## 5. After any deployment — smoke test checklist

- [ ] Visit the public URL on a phone, tablet, and desktop browser.
- [ ] Sign in, register, and reset-password pages load without
      horizontal scrolling.
- [ ] Sidebar collapses into a hamburger menu below ~1024px width.
- [ ] Chrome/Edge (Android) shows an "Install app" prompt or the
      in-page install banner; on iPhone Safari, Share → **Add to Home
      Screen** installs it with the IDPDR icon and splash color.
- [ ] Turning on airplane mode and reopening the installed app shows the
      offline fallback page instead of a browser error.

## 6. Installing the PWA (what to tell your users)

- **Android (Chrome/Edge/Samsung Internet):** open the site → tap the
  "Install" banner at the bottom, or menu (⋮) → **Add to Home screen** /
  **Install app**.
- **iPhone/iPad (Safari):** open the site → tap the **Share** icon →
  **Add to Home Screen**. (Safari does not support the automatic install
  prompt other browsers use — this is an Apple/WebKit limitation, not a
  bug in this app.)
- Once installed, IDPDR opens full-screen with its own icon, splash
  screen, and theme color, and works offline for previously visited
  static content.
