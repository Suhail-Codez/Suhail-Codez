# MediRec v4.0 — RBAC, Navigation, and Theme System

## 1. Authentication & Roles
- `UserProfile.role` renamed from `'user'` → `'patient'` (data-migrated, no data loss) alongside `'admin'`.
- **Sign Up** (`/register/`) always creates a **Patient**. Admin accounts are only created via `seed_admin` or by an existing admin promoting a user in User Management — never through public self-service, to keep privilege escalation out of reach of the public form.
- **Forgot Password**: `/forgot-password/` → emails a tokenized reset link (Django's `default_token_generator`) through the console email backend (no real SMTP server in this environment — the link is printed to the server log; swap `EMAIL_BACKEND` in `settings.py` for real delivery). Always returns a generic "if this account exists…" message to prevent account enumeration.
- **Reset Password**: `/reset-password/<uidb64>/<token>/` validates the token server-side before showing the form; invalid/used/expired links show a clear error with a link to request a new one.
- **Change Password** and **Profile Management** (name, email, phone, age, gender, bio, notification preference) via `/api/auth/change-password/` and `/api/auth/profile/update/`.
- Every login/logout/register/password-change/profile-update writes an **AuditLog** row.

## 2. Role-Based Access Control
- New `api_admin_required` decorator (alongside the existing `api_login_required`) — every `/api/admin/*` endpoint 403s for a Patient even if they call the URL directly; nothing is client-trust-based.
- `/admin-dashboard/` re-checks `profile.role == 'admin'` on every request; a signed-in Patient hitting the URL is bounced back to `/` — never shown any admin markup.
- Login now returns a `redirect` field (`/` for Patients, `/admin-dashboard/` for Admins) and the sign-in page follows it, so **Patients land on the Patient Dashboard and Admins land on the Admin Dashboard** automatically after login.
- Removed the **Analytics** and **API Reference** links from the Patient sidebar entirely (previously visible to every signed-in user, patient or admin — a real gap). That functionality now lives only inside the Admin Dashboard.
- New Admin Dashboard sections, all backed by real, role-gated CRUD APIs:
  - **User Management** — search, promote/demote role, activate/deactivate, delete.
  - **Drug Database Management** — full CRUD on a new `Drug` model; active entries are merged into the Patient Dashboard's Drug Search/Drug Report alongside the built-in knowledge base (an admin can add a drug and a patient can immediately find it).
  - **Audit Logs** — filterable table of the security events above.
  - **System Settings** — toggle new-registration and maintenance-mode, edit site name/support email; both toggles have real effect (verified: registration returns 403 when disabled; non-admin login returns 503 during maintenance while admin login still succeeds).
  - **Analytics Dashboard** — user/role/sentiment/condition charts (Chart.js).
  - **API Reference** — full endpoint documentation, split into patient-facing and admin-only sections.

## 3. Navigation — Profile Dropdown
Replaced the old plain avatar-and-signout row (in both the Patient and Admin apps) with a proper dropdown menu: avatar, name, role badge, **My Profile**, **Account Settings**, **Notifications**, **Appearance** (with an inline Light/Dark/System submenu), **Help & Support**, and **Sign Out** — with hover states, a chevron that rotates on open, and slide/fade-in animation on the panel itself. Clicking outside closes it.

## 4. Theme System
Replaced the old binary dark/light toggle with **Light / Dark / System**, persisted in `localStorage`, applied instantly with a smooth `.25s` color transition across the whole page. "System" listens for OS-level `prefers-color-scheme` changes live. Implemented identically in both the Patient app and the (previously dark-only) Admin Dashboard, which now also supports light mode.

## 5. Dashboard Experience
- Patient login → `/` (Patient Dashboard: diagnosis, drug search/report, recommendations, comparisons, interactions, sentiment, profile).
- Admin login → `/admin-dashboard/` (Admin Dashboard: overview, analytics, user/drug management, audit logs, settings, API reference).
- Sidebar/nav contents differ correctly per role; nothing admin-only is ever rendered into a Patient's page.

## New backend files
`recommender/admin_views.py`, `recommender/audit.py`, `templates/forgot_password.html`, `templates/reset_password.html`.

## New models / migration
`Drug`, `AuditLog`, `SystemSettings`, plus `UserProfile.bio` / `email_notifications`. One new migration (`0003_...py`) — additive, plus the `user`→`patient` role rename via `RunPython` (reversible, no rows deleted). Verified all 9,000+ existing reviews and the admin account survive `migrate` unchanged.

## Testing performed
Full endpoint smoke test (all patient + all new admin endpoints), role-escalation attempts (patient hitting `/admin-dashboard/` and `/api/admin/*` directly — blocked), maintenance-mode and registration-toggle enforcement, forgot/reset/change-password round trip, drug CRUD → immediately searchable by a patient, JS syntax-checked with Node, HTML structure validated with BeautifulSoup, and the real dev server booted and hit with curl.

## Assumptions
- Password reset uses Django's console email backend (no real mail server available here); the reset link appears in the server log. Point `EMAIL_BACKEND` at a real SMTP/API provider for production use.
- "Admin Login (or role-based login)" was implemented as a single login form with role-based post-login redirect, rather than a second login page, to avoid duplicating auth logic — the spec explicitly allowed this option.
- Managed `Drug` entries are additive/override records merged with the existing code-based drug knowledge base at query time, rather than migrating the entire built-in catalogue into the database — this keeps the fast, already-tested lookup path intact while still giving admins real CRUD control.
