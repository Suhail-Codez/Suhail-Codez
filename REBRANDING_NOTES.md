# Rebranding Notes — "MediRec" → Project Title

The product name **"MediRec" / "MediRec AI"** has been replaced throughout
the application with the project's official title:

> **AN INTELLIGENT DISEASE PREDICTION AND DRUG RECOMMENDATION PROTOTYPE BY
> USING MULTIPLE APPROACHES OF MACHINE LEARNING ALGORITHMS**

## How the (long) title was applied

The full title is used verbatim wherever there's room for it:
- Browser tab `<title>` on every page (Patient app, Admin Dashboard, Sign In,
  Register, Forgot/Reset Password).
- The Patient Dashboard welcome banner and the Admin Overview page header.
- The password-reset email subject/body.
- README.md's main heading.

For places where the full ~120-character title physically cannot fit —
the small top-left logo mark in the sidebar/navbar, in-app breadcrumbs, chip
badges — a short acronym, **IDPDR** (Intelligent Disease Prediction & Drug
Recommendation), is used instead, generally paired with a short subtitle
("Disease & Drug ML Prototype") so the shorthand is still self-explanatory.
Both forms refer to the same project; IDPDR is simply the compact form of
the title for tight UI real estate.

## What else changed

- All "MediRec AI"/"MediRec" mentions in code comments, docstrings, PDF
  report titles, UI copy, disclaimers, the Django app's `verbose_name`, the
  default System Settings (`site_name`, `support_email`), the password-reset
  email templates, and `DEFAULT_FROM_EMAIL` were updated to match.
- The `medirec-theme` localStorage key was renamed to `idpdr-theme` in both
  the Patient app and Admin Dashboard (kept identical between the two so
  the Light/Dark/System preference still stays in sync).
- The placeholder support/admin email addresses (`support@medirec.ai`,
  `admin@medirec.ai`) were updated to `@idpdr.ai` equivalents, including the
  **already-existing** database rows (the seeded admin user's email and the
  System Settings singleton row) — not just the code defaults, since Django
  defaults only apply to newly-created rows.
- The Django `SECRET_KEY` string (which happened to contain the word
  "medirec" as a memorable prefix) was also updated, for completeness. This
  invalidates any currently-active server sessions on restart, which is
  expected/harmless for a prototype.

## What was intentionally left unchanged

- **The two changelogs from earlier rounds of work**, `CHANGES_V3.1.md` and
  `CHANGES_V4.0.md`, still refer to "MediRec" — they're a historical record
  of what was built and named at the time, and rewriting them would make
  them inaccurate as a change history.
- **One existing AuditLog entry** (from earlier testing) still contains the
  literal JSON string `{"site_name": "MediRec AI"}` in its `detail` field.
  Audit logs are an immutable record of what actually happened, so this
  entry was left as-is rather than edited after the fact — new settings
  updates will correctly log `"IDPDR"` going forward.
- **Folder/zip-name references** in `README.md` and `SETUP.md` (e.g.
  `medirec_enhanced/`, `unzip MediRec_v3.zip`) were left alone because they
  describe the actual on-disk folder and file names, which were not
  renamed. Renaming the Python package (`recommender`), the project
  directory (`medirec_enhanced`), or the SQLite filename (`db.sqlite3`)
  was out of scope for a branding change and would carry real risk of
  breaking imports/paths for no user-visible benefit — say the word if
  you'd like those renamed too.
- **`data/generate_and_train.py`** still contains old absolute file paths
  (`/home/claude/medirec_v2/...`) in a couple of comments describing where
  the shipped `.pkl` model files were originally generated — this is a
  historical reproducibility note, not part of the running application.
