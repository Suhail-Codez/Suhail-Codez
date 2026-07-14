# IDPDR (formerly MediRec) — Bug Fixes & Improvements Log

## Bugs Fixed

### 1. Drug Comparison Module
**Problem:** The frontend sent a `POST` request with JSON body to `/api/compare/`,
but the backend view was decorated `@api_view(["GET"])` and read parameters from
`request.GET` (query string). This caused a 405 Method Not Allowed error.

**Fix (two-part):**
- `views.py`: Changed decorator to `@api_view(["GET", "POST"])` and added dynamic
  data source: `data = request.data if request.method == "POST" else request.GET`
- `index.html`: Frontend now sends a `GET` request with URLSearchParams:
  ```js
  const params = new URLSearchParams({condition, drug_a: da, drug_b: db});
  const res = await fetch(`${API}/api/compare/?${params}`);
  ```

### 2. Drug Diagnosis → Quick Recommend
**Problem:** `quickRecommend(condition)` navigated to the Recommend page and called
`loadRecommendations()`, but the `<select>` options were hardcoded with fixed strings
that didn't always match the ML model's predicted condition string (e.g. capitalisation
differences). This caused no data to load.

**Fix:** `quickRecommend()` now iterates all `<option>` elements with a
case-insensitive match, and dynamically adds the condition as a new option if not
found, guaranteeing the value is set before `loadRecommendations()` is called.

## UI/UX Overhaul

- Complete redesign with Inter + Syne type pairing for a clean medical aesthetic
- Dark / Light mode toggle (persisted to localStorage)
- Responsive layout: hamburger menu on mobile, fluid grid breakpoints
- Toast notification system for all async actions (success / error)
- Loading skeletons on the dashboard stat cards
- Animated confidence bars, strength bars, and sentiment bars
- Modern card system with accent borders and hover elevations
- Recent Reviews table on the Sentiment page
- Prediction Log table on the Analytics page
- Accessible colour palette with sufficient contrast in both themes
- Chart.js charts rebuilt with theme-aware colours
