/* ==========================================================================
   IDPDR — PWA bootstrap
   --------------------------------------------------------------------------
   Registers the service worker and wires up the "Add to Home Screen"
   banner. Loaded on every page (see <script src="{% static 'js/pwa-register.js' %}">
   near the end of <body> in each template). Does not touch any existing
   app logic — it only adds install/offline behaviour.
   ========================================================================== */
(function () {
  "use strict";

  // 1. Service worker registration (scope = "/" so it can control every
  //    route, not just /static/). Falls back silently on unsupported
  //    browsers (older Safari, some in-app browsers).
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker
        .register("/service-worker.js", { scope: "/" })
        .then(function (reg) {
          console.log("[IDPDR PWA] service worker registered:", reg.scope);
        })
        .catch(function (err) {
          console.warn("[IDPDR PWA] service worker registration failed:", err);
        });
    });
  }

  // 2. "Add to Home Screen" banner for Android/Chrome/Edge/Samsung
  //    Internet (they fire beforeinstallprompt). iOS Safari does not
  //    support this event — users install via Share -> Add to Home
  //    Screen, so we show a one-time hint instead (see below).
  var deferredPrompt = null;

  function ensureBanner() {
    var banner = document.getElementById("pwa-install-banner");
    if (banner) return banner;

    banner = document.createElement("div");
    banner.id = "pwa-install-banner";
    banner.className = "pwa-install-banner";
    banner.innerHTML =
      '<span style="flex:1;font-size:.85rem;">Install IDPDR on your device for quick, offline-ready access.</span>' +
      '<button type="button" class="pwa-install-cta">Install</button>' +
      '<button type="button" class="pwa-install-dismiss" aria-label="Dismiss">✕</button>';
    document.body.appendChild(banner);

    banner.querySelector(".pwa-install-dismiss").addEventListener("click", function () {
      banner.classList.remove("show");
      try { localStorage.setItem("idpdr_pwa_dismissed", "1"); } catch (e) {}
    });
    banner.querySelector(".pwa-install-cta").addEventListener("click", function () {
      banner.classList.remove("show");
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.finally(function () { deferredPrompt = null; });
      }
    });
    return banner;
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    var dismissed = false;
    try { dismissed = localStorage.getItem("idpdr_pwa_dismissed") === "1"; } catch (err) {}
    if (!dismissed) ensureBanner().classList.add("show");
  });

  window.addEventListener("appinstalled", function () {
    var banner = document.getElementById("pwa-install-banner");
    if (banner) banner.classList.remove("show");
  });

  // 3. iOS Safari hint (no beforeinstallprompt support there). Only shown
  //    once, only in Safari on iOS, and only when not already installed.
  function isIos() {
    return /iphone|ipad|ipod/i.test(window.navigator.userAgent);
  }
  function isInStandaloneMode() {
    return "standalone" in window.navigator && window.navigator.standalone;
  }
  if (isIos() && !isInStandaloneMode()) {
    var dismissedIos = false;
    try { dismissedIos = localStorage.getItem("idpdr_pwa_ios_hint_dismissed") === "1"; } catch (e) {}
    if (!dismissedIos) {
      var b = ensureBanner();
      b.querySelector("span").textContent =
        "Install IDPDR: tap Share, then \u201cAdd to Home Screen\u201d.";
      b.querySelector(".pwa-install-cta").style.display = "none";
      b.classList.add("show");
      b.querySelector(".pwa-install-dismiss").addEventListener("click", function () {
        try { localStorage.setItem("idpdr_pwa_ios_hint_dismissed", "1"); } catch (e) {}
      });
    }
  }
})();
