# MediRec v3.1 — Change Log & Deliverables

This document describes everything that was changed in this pass, why, and how
to run the updated project. It complements (does not replace) `FIXES.md`,
which covered the prior "AuthFixed" round.

---

## 1. Drug Search Module

**Root cause found:** the app had TWO separate drug-data files. `views.py`
had a 10-drug `DRUG_DATABASE`; a second, richer 12-drug file
(`recommender/drug_data.py`) existed but was **never imported anywhere** —
completely dead code. Meanwhile the ML model/review dataset
(`data/drug_reviews.csv`, `models_pkl/recommendations.json`) references 57
distinct drugs. Only the 10 in `DRUG_DATABASE` had full detail; everything
else fell back to a mostly-blank response, and search only checked the top
5 recommended drugs per condition.

**What changed:**
- New file `backend/recommender/drug_database.py` — a single, consolidated,
  57+ drug knowledge base (merges the old 10 + 12, plus complete new
  entries for every remaining drug used by the model/dataset). Every entry
  has the same schema (generic name, brand names, class, uses, dosage,
  side effects, contraindications, interactions, pregnancy/breastfeeding,
  kidney/liver warnings, storage, overdose, missed dose, alternatives,
  price, prescription requirement, manufacturer, availability, condition).
- `drug_search` (`/api/drug/search/`) rewritten:
  - Case-insensitive partial matching on drug name, **generic name**, and
    **brand name** (previously brand-name matches existed but only for the
    10-drug subset).
  - Empty query now returns **every** drug ("browse all") instead of
    requiring text.
  - Result cap raised from a hard-coded 10 to a configurable `limit`
    (default 50, max 200).
- `drug_report` (`/api/drug/report/`) rewritten to look up the new
  consolidated database and to build a **complete fallback profile**
  (never a blank/partial report) for any drug name it doesn't recognize,
  via `build_fallback_profile()`.
- Search Drug UI (`templates/index.html`): added a **"Browse All Drugs"**
  button; search now works with an empty query too.

## 2. Drug Report Module

- Every one of the 58 drugs in the consolidated database now returns a
  fully populated report — no blank sections.
- Added `/api/drug/report/pdf/` — renders the same report as a downloadable
  / printable PDF (see PDF section below). A **Download PDF** button was
  added next to the existing Print button in the UI.

## 3. Disease Diagnosis Report — root cause + fix

**Root cause found:** the trained model / symptom map covers **12**
conditions, but the hand-written `DISEASE_DATABASE` in `views.py` only had
entries for **6** of them (Diabetes Type 2, Hypertension, Depression,
Asthma, Migraine, GERD). Whenever the ML ensemble predicted one of the
other 6 conditions (**Anxiety, Hypothyroidism, Insomnia, Pain, Infection,
High Cholesterol**), `disease_summary` in the `/api/predict/` response came
back empty, and there was no report-generation endpoint at all — the
frontend only showed inline prediction results with no report to view,
save, download, or print.

**What changed:**
- `DISEASE_DATABASE` extended to all 12 conditions with full descriptions,
  causes, risk factors, diagnosis, treatment, lifestyle, prevention, and
  emergency-sign fields.
- New `DiagnosisReport` model (`recommender/models.py`) persists a full
  report snapshot: patient name/age/gender, symptoms, predicted disease,
  confidence score, recommended drugs (with dosage), recommended tests,
  precautions, lifestyle recommendations, doctor/system notes, and
  timestamp. Kept the old lightweight `SavedDiagnosis` model untouched for
  backward compatibility.
- New endpoints:
  - `POST /api/diagnosis/report/` — generate + persist a report from either
    a `prediction_id` (from a prior `/api/predict/` call) or raw
    `symptoms`+`condition`. Accepts optional patient info and notes.
  - `GET /api/diagnosis/reports/` — list the signed-in user's past reports.
  - `GET /api/diagnosis/report/<id>/` — view a saved report as JSON.
  - `GET /api/diagnosis/report/<id>/pdf/` — download/print as PDF.
- Frontend: the Diagnose page now shows a **"Generate Diagnosis Report"**
  button after a prediction. It opens a small patient-info form (name, age,
  gender, notes) and renders the finished report inline with **Print** and
  **Download PDF** buttons.
- PDF generation is real: built with ReportLab (added to `requirements.txt`)
  via a shared `pdf_utils.build_pdf()` helper used by both the drug report
  and the diagnosis report.

## 4. Authentication — root cause + fix

**Root cause found:** the root URL (`/`) was a plain `TemplateView` that
rendered `index.html` unconditionally — it never checked whether the
visitor was logged in. The page's own JavaScript only used the session to
decide what to *display* ("Guest" vs. a name), but every dashboard page and
every API endpoint was fully reachable without ever signing in. That is
the "automatically logs in" behavior you saw: there was no login gate at
all, not an actual auto-login.

**What changed:**
- `/` is now `auth_views.home_page`: if the session isn't authenticated,
  it redirects to `/signin/?next=/` instead of ever rendering the
  dashboard. Same fix applied to `/admin-dashboard/`.
- Every route in `recommender/urls.py` (all `/api/...` endpoints except
  `/api/health/`, which only returns `{"status":"ok"}` and is needed to
  prime the CSRF cookie before login) is wrapped in a new
  `api_login_required` decorator (`recommender/decorators.py`) that
  returns a clean `401 {"error": "..."}` JSON response instead of Django's
  default HTML-redirect behavior (which doesn't make sense for a JSON API).
- **Logout** (`/signout/`) now calls both `logout(request)` **and**
  `request.session.flush()`, and the redirect response carries
  `Cache-Control: no-cache, no-store, must-revalidate` headers.
- **Back-button protection:** `home_page`, `admin_dashboard_page`,
  `signin_page`, and `register_page` are all decorated with Django's
  `@never_cache`, so the browser can't serve a cached copy of a protected
  page after logout — every visit re-checks the session server-side.
- **Remember Me:** added a real checkbox to the sign-in form. If checked,
  `request.session.set_expiry(None)` is called (uses `SESSION_COOKIE_AGE`,
  7 days). If left unchecked, `request.session.set_expiry(0)` — the session
  cookie expires when the browser closes. Previously every login silently
  got a persistent 7-day session regardless of user intent.

## 5. Security Improvements

- **CSRF:** `api_login`, `api_register`, and `api_save_diagnosis` were
  previously `@csrf_exempt`. That's no longer necessary or safe — the
  frontend already primes the CSRF cookie (`GET /api/health/`) and sends
  `X-CSRFToken` on every POST (verified in `signin.html`, `register.html`,
  and `index.html`'s shared `apiFetch()` helper), so the exemptions were
  removed and real CSRF validation now applies to these endpoints too.
- **Authentication middleware:** Django's standard
  `AuthenticationMiddleware` was already present and correctly configured;
  the gap was that nothing *used* `request.user.is_authenticated` to gate
  access. That's fixed by the changes in section 4.
- **Session management:** `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`,
  and `SESSION_COOKIE_AGE` were already set sensibly; expiry is now also
  driven by the Remember Me choice (see section 4).
- **Login required / protected endpoints:** implemented via
  `api_login_required` in `recommender/urls.py` (see section 4) rather than
  scattering decorators across every view function in `views.py` — keeps
  the change minimal and centrally auditable.
- **Unauthorized access handling:** unauthenticated page requests → 302
  redirect to `/signin/?next=<page>`; unauthenticated API requests → 401
  JSON `{"error": "Authentication required. Please sign in."}`.

## 6. Database — migrations

- One new migration: `recommender/migrations/0002_alter_druginteractioncheck_options_and_more.py`.
  - Adds the new `DiagnosisReport` table (additive only).
  - Also includes a handful of pre-existing schema-drift fixups that
    Django's `makemigrations` detected between `models.py` and the
    original `0001_initial` migration (upgrading a few `id` columns from
    `AutoField` to `BigAutoField`, and syncing `Meta.ordering` on
    `Prediction`/`DrugInteractionCheck` to match the models). These were
    **not** introduced by this change — they were latent drift already
    present in the delivered project — but Django bundled them into the
    same migration. They are non-destructive; all existing data (9,000
    reviews after reseeding, the existing admin user, etc.) was verified
    intact after running `migrate`.
- New management command **`seed_reviews`** (`python manage.py seed_reviews`)
  — see section 8 (root cause) for why this was necessary. Idempotent by
  default; pass `--force` to wipe and reload.
- No existing data was deleted at any point. `db.sqlite3` from the upload
  is reused as-is; only additive schema changes were applied.

## 7. Testing performed

- `python manage.py check` — clean, 0 issues.
- Full endpoint smoke test via Django's test client covering every module:
  auth (login/logout/remember-me/register), conditions, predict,
  recommend, recommend/all, sentiment, compare, dashboard, reviews,
  predictions, drug detail/report/report-pdf/search/buy, interactions,
  disease info, symptom-recommend, diagnosis report create/list/detail/pdf,
  admin stats — all return 200/201 as expected.
- Verified unauthenticated requests are blocked (401 for API, 302 redirect
  for pages) and that authenticated requests succeed.
- Verified logout destroys the session and that the root page becomes
  inaccessible again immediately afterward (no back-button bypass).
- Rendered both the Drug Report PDF and the Disease Diagnosis Report PDF
  and visually inspected the output — correctly formatted, all sections
  populated.
- Booted the real dev server (`manage.py runserver`) and confirmed it
  starts cleanly and serves `/`, `/signin/`, and `/api/health/`.
- **Bug found and fixed during testing:** `check_interactions()` (the drug
  interaction checker) referenced a name, `DRUG_INTERACTIONS`, that was
  never imported anywhere in `views.py` — every call to
  `POST /api/interactions/` raised a `NameError` and returned HTTP 500.
  Fixed by importing `DRUG_INTERACTIONS` from `drug_data.py`. This was a
  pre-existing bug in the delivered project, not something introduced by
  this round of changes.
- `python -m pyflakes` run over all modified files — no undefined names;
  a few pre-existing unused imports remain (harmless, not runtime errors).

---

## 8. Files changed / added

| File | Change |
|---|---|
| `backend/recommender/drug_database.py` | **New.** Consolidated 58-drug knowledge base + lookup/fallback helpers. |
| `backend/recommender/pdf_utils.py` | **New.** Shared ReportLab PDF renderer. |
| `backend/recommender/decorators.py` | **New.** `api_login_required` — JSON-friendly auth gate for API views. |
| `backend/recommender/management/commands/seed_reviews.py` | **New.** Loads `data/drug_reviews.csv` into the DB (was never being loaded — see below). |
| `backend/recommender/models.py` | Added `DiagnosisReport` model. |
| `backend/recommender/migrations/0002_...py` | **New.** Adds `DiagnosisReport` table (+ minor pre-existing drift fixes). |
| `backend/recommender/views.py` | Imports the new drug database; rewrote `drug_search`/`drug_report`; extended `DISEASE_DATABASE` to 12 conditions; added `diagnosis_report_create/list/detail/pdf` and `drug_report_pdf`; fixed the `DRUG_INTERACTIONS` NameError bug. |
| `backend/recommender/urls.py` | Every endpoint (except `/health/`) now wrapped in `api_login_required`; added diagnosis-report routes. |
| `backend/recommender/auth_views.py` | `home_page` added (root now requires login); `@never_cache` on all auth-adjacent pages; removed unnecessary `@csrf_exempt`; Remember Me session-expiry logic; logout now flushes the session. |
| `backend/recommender/admin.py` | Registered `DiagnosisReport` in Django admin. |
| `backend/config/urls.py` | Root path now points at `auth_views.home_page` instead of an ungated `TemplateView`. |
| `backend/config/settings.py` | Added `LOGIN_URL`; tidied session/cookie settings. |
| `backend/templates/signin.html` | Added "Remember me" checkbox, wired into the login request. |
| `backend/templates/index.html` | Added "Browse All Drugs" button + empty-query search support; added Download-PDF button to Drug Report; added the full Diagnosis Report generation UI (patient info form, report view with Print/Download PDF). |
| `backend/requirements.txt` | Added `reportlab` (PDF generation); pinned `scikit-learn==1.8.0` to match the shipped trained models (see Assumptions). |

---

## 9. How to run the project

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# One-time: load the 9,000 drug reviews into the database
# (this was missing before — the table was empty even though the ML
# models were trained on this data)
python manage.py seed_reviews

# Apply the new migration (adds the DiagnosisReport table; no data is deleted)
python manage.py migrate

python manage.py runserver
```

Then open `http://127.0.0.1:8000/` — you'll land on the Login page. The
default seeded admin account is `admin` / `admin123` (from the existing
`seed_admin` command / fixture — unchanged).

## 10. New dependency

- **reportlab** (`>=4.0`) — used to render the Drug Report and Disease
  Diagnosis Report as PDF. Added to `requirements.txt`.

## 11. Assumptions made

- Real, standard patient-information-leaflet-level detail (uses, typical
  adult dosing, common side effects, key contraindications/interactions,
  pregnancy/breastfeeding notes) was written for every drug now in
  `drug_database.py`, at the same level of specificity as the 10 drugs
  already curated in the original project. This is general reference
  information, not a substitute for a package insert or clinical
  judgement — the existing disclaimer wording was kept on every report.
- `scikit-learn` was pinned to `1.8.0` in `requirements.txt` because the
  shipped `.pkl` models in `models_pkl/` were trained on that version;
  installing a newer scikit-learn (this sandbox had 1.9.0 available)
  still works but prints an `InconsistentVersionWarning` on every model
  load. Pinning removes the warning; it is not required for correctness.
- Ranitidine is included in the drug database (it's part of the trained
  dataset/recommendations) with a note that its regulatory status varies
  by region due to past contamination-related withdrawals in some
  markets — flagged in its "availability" field rather than omitted.
- "Remember Me" persistence uses the existing `SESSION_COOKIE_AGE` (7
  days) when checked, and browser-session-only (expires on browser close)
  when unchecked — no explicit duration was specified in the request, so
  the existing 7-day constant was reused as the "remembered" duration.
- Diagnosis reports are tied to the signed-in user (`request.user`) when
  generated while logged in; since every route now requires
  authentication, guest/anonymous diagnosis reports are no longer a
  realistic path, but the model still supports a null `user` for
  robustness.
