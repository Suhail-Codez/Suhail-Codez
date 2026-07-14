/* ==========================================================================
   IDPDR — Service Worker
   --------------------------------------------------------------------------
   Strategy:
     - App shell (static CSS/JS/icons + the auth pages) -> cache-first, so
       the app still opens offline / on flaky mobile data.
     - /api/* calls -> network-first, falling back to cache only for GET
       requests, so live data (predictions, drug data) is never served
       stale when a connection exists. Writes (POST/PUT/DELETE) always hit
       the network — offline mutation is intentionally NOT supported to
       avoid silently losing patient/admin data.
   This file must be served from the site root ("/service-worker.js") so
   its default scope is "/" — see config/urls.py.
   ========================================================================== */

const CACHE_VERSION = "idpdr-v1";
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

// Core assets always worth having offline. Paths are relative to site root.
const APP_SHELL = [
  "/static/css/responsive.css",
  "/static/js/pwa-register.js",
  "/static/manifest.json",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/offline.html",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith("idpdr-") && key !== STATIC_CACHE && key !== RUNTIME_CACHE)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return; // never intercept writes

  const url = new URL(request.url);

  // API calls: network-first, cache as a fallback for read-only endpoints.
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(RUNTIME_CACHE).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // Static assets & pages: cache-first, then network, then offline page.
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request)
        .then((response) => {
          if (response.ok && (url.pathname.startsWith("/static/") || url.pathname.startsWith("/staticfiles/"))) {
            const copy = response.clone();
            caches.open(STATIC_CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => {
          if (request.mode === "navigate") {
            return caches.match("/offline.html");
          }
        });
    })
  );
});
