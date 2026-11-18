/* SPDX-License-Identifier: MIT · Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
   Page-side glue between the guide panel and the tutor widget. The page exposes two hooks:
     window.RZ     = { show(view), goTo(view, anchor), goSlide(i), current(), lang() }   (its engine)
     window.RZ_AVS = { pose: dataURL | path }                                            (its avatar map)
   tools/add_panel.py fills __APP__ and __PART__; a page (or the demo) may instead set window.RZ_TUTOR =
   { app, part, manifest } before this script. The endpoint comes from <meta name="rz-tutor" content="…">
   or ?endpoint=http://127.0.0.1:…/v1/chat for local tests (loopback addresses only); without one the widget
   answers in offline mode, makes no request and shows no AI notice. */
(function () {
  "use strict";
  var C = window.RZ_TUTOR || {};
  var APP = C.app || "__APP__", PART = C.part || "__PART__", MANIFEST = C.manifest || "tutor/manifest.json";
  var meta = document.querySelector('meta[name="rz-tutor"]');
  // ?endpoint= is for local tests only: a link that points the page at someone else's server must not carry students' questions there.
  var asked = new URLSearchParams(location.search).get("endpoint") || "";
  var local = /^http:\/\/(127\.0\.0\.1|localhost|\[::1\])(:\d+)?\//.test(asked);
  var endpoint = (local ? asked : "") || (meta && meta.getAttribute("content")) || "";
  /* corner stage: poses that face the chat once mirrored; the two-armed "explain" is too wide for the corner.
     Each semantic pose lists the page's own file names in order of preference (S2 names first, SEAA 4243 second). */
  var CORNER = { welcome: ["offer", "welcome"], think: ["think"], explain: ["present"], present: ["ok"], ok: ["ok"],
    "arms-crossed": ["crossed", "arms-crossed"], wave: ["wave"], cheer: ["cheer"], "thumbs-up": ["thumbs", "thumbs-up"], tablet: ["tablet"] };
  function pose(p) {
    var img = document.getElementById("rjav"), m = window.RZ_AVS || {}, list = CORNER[p] || [p], k = null;
    for (var i = 0; i < list.length; i++) if (m[list[i]]) { k = list[i]; break; }
    if (!img || !k || img.getAttribute("data-pose") === k) return;
    img.setAttribute("data-pose", k); img.classList.add("swap");
    setTimeout(function () { img.src = m[k]; img.classList.remove("swap"); }, 110);
  }
  function spotlight(el) { el.classList.remove("coach"); void el.offsetWidth; el.classList.add("coach"); setTimeout(function () { el.classList.remove("coach"); }, 4600); }
  function goto(t) {
    if (t.url) { window.open(t.url, "_blank", "noopener"); return; }      // supplementary material by the same lecturer (e.g. an rz-tools page)
    var RZ = window.RZ; if (!RZ) return;
    if (t.view === "slides" && t.anchor) { RZ.show("slides"); if (RZ.goSlide) RZ.goSlide(parseInt(t.anchor, 10) - 1); return; }
    var el = (t.anchor && document.getElementById(t.anchor)) || (t.selector && document.querySelector(t.selector));
    if (t.anchor && RZ.goTo) RZ.goTo(t.view, t.anchor); else RZ.show(t.view);
    if (el) setTimeout(function () { if (!t.anchor) el.scrollIntoView({ block: "center", behavior: "smooth" }); spotlight(el); }, 140);
  }
  function mount(manifest) {
    if (!window.RzTutor || !document.getElementById("tutor")) return;
    window.__rzt = RzTutor.mount({
      root: "#tutor", endpoint: endpoint, app: APP, part: PART, manifest: manifest, name: "Dr RJ", storageKey: APP + "-" + PART + "-tutor",
      lang: function () { return (window.RZ && RZ.lang && RZ.lang()) || (document.documentElement.lang === "ms" ? "ms" : "en"); },
      where: function () { return { view: (window.RZ && RZ.current && RZ.current()) || "", anchor: "" }; },
      goto: goto, pose: pose,
      onAnswer: function (el) { if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([el]).catch(function () {}); },
    });
    pose("welcome");
  }
  // Is the AI switched on for this app? Off (the owner's switch in the Worker, or no key) means offline mode by
  // design: no notice, no request. Unknown (Worker down, an older Worker) means try; the widget then says the
  // server is not reachable if it is down.
  function aiStatus() {
    if (!endpoint) return Promise.resolve(false);
    var url = endpoint.replace(/\/v1\/chat(\?.*)?$/, "/v1/health") + "?app=" + encodeURIComponent(APP);
    var ctl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctl) ctl.abort(); }, 3000);
    return fetch(url, ctl ? { signal: ctl.signal } : {}).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { clearTimeout(timer); return !(j && j.ai === false); })
      .catch(function () { clearTimeout(timer); return true; });
  }
  Promise.all([
    fetch(MANIFEST).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
    aiStatus(),
  ]).then(function (v) { if (!v[1]) endpoint = ""; mount(v[0]); });
  var fab = document.getElementById("rjfab"), guide = document.getElementById("rzguide");
  if (fab) fab.addEventListener("click", function () { if (guide) guide.scrollIntoView({ behavior: "smooth", block: "start" }); var i = document.querySelector("#tutor .rzt-in"); if (i) setTimeout(function () { try { i.focus({ preventScroll: true }); } catch (e) { i.focus(); } }, 600); });
  if (fab && guide && "IntersectionObserver" in window) new IntersectionObserver(function (es) { fab.classList.toggle("rj-near", es[0].isIntersecting); }, { threshold: 0.15 }).observe(guide);
  new MutationObserver(function () { if (window.__rzt) window.__rzt.refresh(); }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
})();
