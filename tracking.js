/* =============================================================
   CANDIDALIB — Suivi de trafic & consentement RGPD
   -------------------------------------------------------------
   Ce fichier gère :
     1. Le bandeau de consentement cookies (obligatoire en France)
     2. Le chargement de Google Analytics 4, Microsoft Clarity et
        Meta Pixel UNIQUEMENT après accord du visiteur
     3. Le suivi automatique des clics sur "Appeler" (liens tel:)
     4. Une fonction candidalibTrack() pour suivre les conversions
        (formulaire "Être rappelé", boutons importants, etc.)

   >>> À FAIRE : remplace les 3 identifiants ci-dessous par les
       tiens. Tant qu'ils contiennent "XXXX", l'outil concerné
       reste désactivé (aucune erreur, le site fonctionne).
   ============================================================= */

const CANDIDALIB_TRACKING = {
  GA4_ID:        "G-P1VV14CR0E",   // Google Analytics 4  (https://analytics.google.com)
  CLARITY_ID:    "xcyzchjdx6",     // Microsoft Clarity   (https://clarity.microsoft.com)
  META_PIXEL_ID: "XXXXXXXXXX"      // Meta Pixel          (Business Manager)
};

/* ------------------------------------------------------------- */

(function () {
  "use strict";

  const CONSENT_KEY = "candidalib_consent"; // valeurs : "accepte" | "refuse"

  function estConfigure(id) {
    return id && id.indexOf("XXXX") === -1;
  }

  /* ---------- Chargement des outils (après consentement) ---------- */

  function chargerGA4(id) {
    if (!estConfigure(id)) return;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", id, { anonymize_ip: true });
  }

  function chargerClarity(id) {
    if (!estConfigure(id)) return;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", id);
  }

  function chargerMetaPixel(id) {
    if (!estConfigure(id)) return;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0";
      n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", id);
    window.fbq("track", "PageView");
  }

  function activerTraqueurs() {
    chargerGA4(CANDIDALIB_TRACKING.GA4_ID);
    chargerClarity(CANDIDALIB_TRACKING.CLARITY_ID);
    chargerMetaPixel(CANDIDALIB_TRACKING.META_PIXEL_ID);
  }

  /* ---------- Suivi des conversions ---------- */

  // Utilisable partout : candidalibTrack("Appel") ou candidalibTrack("Rappel", {...})
  window.candidalibTrack = function (nom, params) {
    params = params || {};
    if (window.gtag) window.gtag("event", nom, params);
    if (window.fbq) window.fbq("track", "Lead", Object.assign({ content_name: nom }, params));
    if (window.clarity) window.clarity("event", nom);
    console.info("[Candidalib] conversion suivie :", nom, params);
  };

  // Suit automatiquement TOUS les clics sur un lien "Appeler" (tel:)
  function activerSuiviAppels() {
    document.addEventListener("click", function (e) {
      const lien = e.target.closest('a[href^="tel:"]');
      if (lien) window.candidalibTrack("Appel", { numero: lien.getAttribute("href").replace("tel:", "") });
    });
  }

  /* ---------- Bandeau de consentement ---------- */

  function appliquerConsentement(valeur) {
    try { localStorage.setItem(CONSENT_KEY, valeur); } catch (err) {}
    if (valeur === "accepte") activerTraqueurs();
  }

  function afficherBandeau() {
    const barre = document.createElement("div");
    barre.setAttribute("role", "dialog");
    barre.setAttribute("aria-label", "Consentement aux cookies");
    barre.style.cssText =
      "position:fixed;bottom:20px;left:20px;right:20px;z-index:9999;margin:0 auto;max-width:680px;" +
      "background:#ffffff;color:#404040;border:1px solid rgba(0,0,0,.06);border-radius:16px;" +
      "padding:18px 22px;font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.5;" +
      "display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;" +
      "box-shadow:0 20px 25px -5px rgba(0,0,0,.1),0 10px 10px -5px rgba(0,0,0,.04);";

    const texte = document.createElement("span");
    texte.style.cssText = "flex:1;min-width:240px;";
    texte.innerHTML =
      'Nous utilisons des cookies de mesure d\'audience pour améliorer votre expérience. ' +
      '<a href="confidentialite.html" style="color:#2563eb;text-decoration:underline;">En savoir plus</a>.';

    const actions = document.createElement("div");
    actions.style.cssText = "display:flex;gap:10px;align-items:center;margin-left:auto;";

    const btnRefus = document.createElement("button");
    btnRefus.textContent = "Refuser";
    btnRefus.style.cssText =
      "background:transparent;color:#525252;border:none;" +
      "border-radius:10px;padding:11px 16px;font-weight:500;cursor:pointer;font-size:14px;font-family:inherit;";

    const btnAccept = document.createElement("button");
    btnAccept.textContent = "Accepter";
    btnAccept.style.cssText =
      "background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;border:none;border-radius:10px;" +
      "padding:11px 24px;font-weight:600;cursor:pointer;font-size:14px;font-family:inherit;" +
      "box-shadow:0 4px 6px -1px rgba(37,99,235,.3);";

    function fermer() { if (barre.parentNode) barre.parentNode.removeChild(barre); }
    btnAccept.addEventListener("click", function () { appliquerConsentement("accepte"); fermer(); });
    btnRefus.addEventListener("click", function () { appliquerConsentement("refuse"); fermer(); });

    actions.appendChild(btnRefus);
    actions.appendChild(btnAccept);
    barre.appendChild(texte);
    barre.appendChild(actions);
    document.body.appendChild(barre);
  }

  /* ---------- Démarrage ---------- */

  function init() {
    activerSuiviAppels();
    let choix = null;
    try { choix = localStorage.getItem(CONSENT_KEY); } catch (err) {}

    if (choix === "accepte") {
      activerTraqueurs();
    } else if (choix !== "refuse") {
      afficherBandeau();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
