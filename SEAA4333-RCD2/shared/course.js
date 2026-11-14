/* SEAA 4333 course pages — shared engine (no dependencies).
   Derived from the SEAA 4243 engine (views, progress, notes, slides, exercises, Explorer milestones) and
   brought to the T&L app template: the standard settings buttons (rz-settings-buttons: BM/EN · theme · AA · ⓘ),
   a foldable description, a search box over this page, a screen guide with a tour, examples revealed one step
   at a time, and the two hooks the Dr RJ guide panel needs (window.RZ, window.RZ_AVS).
   Preferences are course-wide; progress is per Unit. Everything lives in this browser's localStorage: it is
   the student's own record, not a gradebook. */
(function () {
  "use strict";
  var C = window.COURSE || {};
  var PFX = C.prefix || "seaa4333";
  var PREFS = C.prefs || PFX + "-prefs", KEY = C.key || PFX + "-u0-v1";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function ld(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function sv(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function el(tag, attrs, html) { var e = document.createElement(tag); if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); }); if (html != null) e.innerHTML = html; return e; }
  function bi(en, ms) { return '<span class="en">' + en + '</span><span class="ms">' + ms + '</span>'; }
  function tx(node, en, ms) { if (node) node.innerHTML = bi(en, ms); }
  function mmss(s) { s = Math.max(0, Math.round(s)); var m = Math.floor(s / 60); return m + ":" + (s % 60 < 10 ? "0" : "") + (s % 60); }
  function fmt(v, d) { if (!isFinite(v)) return "—"; var s = Math.abs(v) < 1e-12 ? 0 : v; return s.toFixed(d).replace("-", "−"); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var reduced = (function () { try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } })();

  /* ---------- the lecturer's avatar: one file per pose; the Dr RJ panel reads window.RZ_AVS ---------- */
  var AVB = C.avatarBase || "../shared/avatar/";
  var AVS = {};
  ["welcome", "wave", "explain", "think", "present", "tablet", "ok", "cheer", "arms-crossed", "thumbs-up", "head"].forEach(function (p) { AVS[p] = AVB + p + ".webp"; });
  AVS.offer = AVS.welcome; AVS.badge = AVS.head; AVS.crossed = AVS["arms-crossed"]; AVS.thumbs = AVS["thumbs-up"];
  window.RZ_AVS = AVS;
  $$("img[data-avsrc]").forEach(function (im) { var k = im.getAttribute("data-avsrc"); if (AVS[k]) im.src = AVS[k]; });
  /* inside an embedding frame (claude.ai preview), open the links that leave the page in a new tab */
  (function () { var framed = true; try { framed = window.top !== window.self; } catch (e) {}
    if (framed) $$(".crumbs a, .contact a, a.homeicon").forEach(function (l) { l.target = "_blank"; l.rel = "noopener"; }); })();

  /* ---------- preferences: language · theme · text size · folded description (rz-settings-buttons) ---------- */
  var FONT_STEPS = [0.9, 1, 1.15, 1.3];
  var P = (function () {
    var p = ld(PREFS, null); if (!p || typeof p !== "object") p = {};
    return { lang: p.lang === "en" || p.lang === "ms" ? p.lang : (C.lang || "ms"),
      theme: p.theme === "light" || p.theme === "dark" ? p.theme : "",
      font: +p.font || +p.ts || 1, fold: !!p.fold, guided: !!p.guided };
  })();
  function savePrefs() { sv(PREFS, { lang: P.lang, theme: P.theme, font: P.font, fold: P.fold, guided: P.guided }); }
  function L2(en, ms) { return P.lang === "ms" ? ms : en; }
  var langHooks = [];
  function applyLang() {
    var r = document.documentElement; r.setAttribute("data-lang", P.lang); r.setAttribute("lang", P.lang === "ms" ? "ms" : "en");
    var lb = $("#btn-lang");
    if (lb) { lb.textContent = P.lang === "ms" ? "EN" : "BM"; lb.title = P.lang === "ms" ? "Language" : "Bahasa"; lb.setAttribute("aria-label", P.lang === "ms" ? "Language: English" : "Bahasa: Melayu"); }
    $$("[data-ph-en]").forEach(function (e) { e.placeholder = L2(e.getAttribute("data-ph-en"), e.getAttribute("data-ph-ms")); });
    $$("[data-tt-en]").forEach(function (e) { var t = L2(e.getAttribute("data-tt-en"), e.getAttribute("data-tt-ms")); e.title = t; e.setAttribute("aria-label", t); });
    langHooks.forEach(function (f) { try { f(); } catch (e) {} });
  }
  var SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';
  var mq = null; try { mq = window.matchMedia("(prefers-color-scheme: dark)"); } catch (e) {}
  function effTheme() { return P.theme || (mq && mq.matches ? "dark" : "light"); }
  function applyTheme() {
    var r = document.documentElement; if (P.theme) r.setAttribute("data-theme", P.theme); else r.removeAttribute("data-theme");
    var b = $("#btn-theme"), dk = effTheme() === "dark", t = dk ? L2("Light theme", "Tema cerah") : L2("Dark theme", "Tema gelap");
    if (b) { b.innerHTML = dk ? SUN : MOON; b.title = t; b.setAttribute("aria-label", t); }
    window.dispatchEvent(new Event("themechange"));
  }
  if (mq) { var mqf = function () { if (!P.theme) applyTheme(); }; if (mq.addEventListener) mq.addEventListener("change", mqf); else if (mq.addListener) mq.addListener(mqf); }
  function fontStep(f) { var k = 0; FONT_STEPS.forEach(function (v, i) { if (Math.abs(v - f) < Math.abs(FONT_STEPS[k] - f)) k = i; }); return k; }
  function nextFont(f, dir) {
    var i; if (dir > 0) { for (i = 0; i < FONT_STEPS.length; i++) if (FONT_STEPS[i] > f + 1e-6) return FONT_STEPS[i]; return FONT_STEPS[0]; }
    for (i = FONT_STEPS.length - 1; i >= 0; i--) if (FONT_STEPS[i] < f - 1e-6) return FONT_STEPS[i]; return FONT_STEPS[FONT_STEPS.length - 1];
  }
  function applyFont() {
    var r = document.documentElement; r.style.setProperty("--font-scale", String(P.font)); r.style.setProperty("--ts", String(P.font));
    var fb = $("#btn-font");
    if (fb) { var k = fontStep(P.font); $$(".lvl i", fb).forEach(function (d, i) { d.classList.toggle("on", i <= k); });
      var pct = Math.round(P.font * 100), nx = Math.round(nextFont(P.font, 1) * 100), t = L2("Text size " + pct + "% (click: " + nx + "%)", "Saiz teks " + pct + "% (klik: " + nx + "%)");
      fb.title = t; fb.setAttribute("aria-label", t); }
    window.dispatchEvent(new Event("resize"));
  }
  function applyFold() {
    document.documentElement.classList.toggle("subfold", !!P.fold);
    var b = $("#foldbtn"); if (!b) return; b.setAttribute("aria-expanded", String(!P.fold));
    var t = P.fold ? L2("Show description", "Tunjuk penerangan") : L2("Hide description", "Sembunyi penerangan"), s = $(".vh", b);
    if (s) s.textContent = t; b.title = t;
  }
  langHooks.push(applyTheme, applyFont, applyFold);
  var lbtn = $("#btn-lang"); if (lbtn) lbtn.addEventListener("click", function () { P.lang = P.lang === "ms" ? "en" : "ms"; savePrefs(); applyLang(); });
  var tbtn = $("#btn-theme"); if (tbtn) tbtn.addEventListener("click", function () { P.theme = effTheme() === "dark" ? "light" : "dark"; savePrefs(); applyTheme(); });
  var fbtn = $("#btn-font"); if (fbtn) fbtn.addEventListener("click", function (e) { P.font = nextFont(P.font, e.shiftKey ? -1 : 1); savePrefs(); applyFont(); });
  var fold = $("#foldbtn"); if (fold) fold.addEventListener("click", function () { P.fold = !P.fold; savePrefs(); applyFold(); });
  /* another tab of the course (or its Explorer) changed the preferences: follow them */
  window.addEventListener("storage", function (e) {
    if (e.key !== PREFS) return; var p = ld(PREFS, {}) || {};
    if (p.lang === "en" || p.lang === "ms") P.lang = p.lang; P.theme = p.theme === "light" || p.theme === "dark" ? p.theme : ""; if (+p.font) P.font = +p.font; P.fold = !!p.fold;
    applyLang();
  });
  applyLang();

  /* ---------- part state ---------- */
  function fresh() {
    return { view: "start", nmode: "full", read: {}, qc: {}, seen: {}, slide: 0, xrev: {},
      ex: { seed: {}, v: {}, chk: {}, first: {}, att: {}, hint: {}, conf: {}, sol: {}, t: {}, timer: { el: 0, run: false, t0: 0 } },
      lab: {}, cando: {}, last: 0, opened: 0 };
  }
  var ST = (function () { var d = fresh(), s = ld(KEY, null); if (!s || typeof s !== "object") return d;
    Object.keys(d).forEach(function (k) { if (s[k] === undefined) s[k] = d[k]; else if (d[k] && typeof d[k] === "object" && !Array.isArray(d[k])) { Object.keys(d[k]).forEach(function (j) { if (s[k][j] === undefined) s[k][j] = d[k][j]; }); } }); return s; })();
  var saveT = null; function save() { clearTimeout(saveT); saveT = setTimeout(function () { ST.last = Date.now(); sv(KEY, ST); }, 120); }
  function saveNow() { clearTimeout(saveT); ST.last = Date.now(); sv(KEY, ST); }
  if (!ST.opened) ST.opened = Date.now();
  window.addEventListener("pagehide", saveNow);

  /* ---------- views (tabs) ---------- */
  var VIEWS = $$(".view").map(function (v) { return v.getAttribute("data-view"); }), current = null, pendingSlide = null;
  function show(v, opts) {
    if (!VIEWS.length) return;
    opts = opts || {}; if (VIEWS.indexOf(v) < 0) v = VIEWS[0]; current = v; ST.view = v; save();
    $$(".view").forEach(function (s) { s.hidden = s.getAttribute("data-view") !== v; });
    $$(".tab").forEach(function (t) { var on = t.getAttribute("data-view") === v; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1; });
    /* on a phone the tab bar scrolls sideways: bring the current tab into view */
    var at = $('.tab[aria-selected="true"]'), nav = at && at.parentNode;
    if (nav && nav.scrollWidth > nav.clientWidth) { var nr = nav.getBoundingClientRect(), tr = at.getBoundingClientRect();
      if (tr.left < nr.left) nav.scrollLeft += tr.left - nr.left - 8; else if (tr.right > nr.right) nav.scrollLeft += tr.right - nr.right + 8; }
    if (!opts.keepHash) { try { history.replaceState(null, "", "#" + v + (opts.anchor ? "-" + opts.anchor : "")); } catch (e) {} }
    var slideNo = v === "slides" && opts.anchor && /^\d+$/.test(opts.anchor);
    if (slideNo) { pendingSlide = +opts.anchor - 1; if (svInit) goSlide(pendingSlide); }
    if (opts.anchor && !slideNo) { var a = document.getElementById(opts.anchor); if (a) setTimeout(function () { var d = a.closest && a.closest("details:not([open])"); if (d) d.open = true; a.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" }); }, 30); }
    else if (!opts.noscroll) window.scrollTo({ top: 0 });
    if (v === "start") renderStart();
    if (v === "slides") fitSlides();
    if (v === "exercises") renderStats();
    if (v === "lab") armLab();
    if (typeof eqSoon === "function") eqSoon();
    updatePill();
  }
  $$(".tab").forEach(function (t, i, all) {
    t.addEventListener("click", function () { show(t.getAttribute("data-view")); });
    t.addEventListener("keydown", function (e) { if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return; var n = all[(i + (e.key === "ArrowRight" ? 1 : all.length - 1)) % all.length]; n.focus(); show(n.getAttribute("data-view")); e.preventDefault(); });
  });
  $$("[data-goto]").forEach(function (b) { if (b.id === "contbtn") return; b.addEventListener("click", function (ev) { ev.preventDefault(); var p = b.getAttribute("data-goto").split("/"); show(p[0], { anchor: p[1] }); }); });
  window.addEventListener("hashchange", function () { fromHash(); });
  function fromHash() { var h = decodeURIComponent(location.hash.replace("#", "")), m = /^([a-z]+)(?:[-\/](.+))?$/.exec(h);
    if (m && VIEWS.indexOf(m[1]) >= 0) show(m[1], { anchor: m[2], keepHash: true }); else show(ST.view || VIEWS[0], { keepHash: true }); }

  /* ---------- progress ---------- */
  function cnt(o) { return Object.keys(o).filter(function (k) { return o[k]; }).length; }
  var NOTES = C.notes || [], NSLIDES = C.slides || 0, MS = (C.lab && C.lab.milestones) || [], NCANDO = C.cando || 0, XS = C.examples || [];
  var EXIDS = []; // filled by exercise init
  function parts() {
    var p = {};
    if (NOTES.length) p.notes = [NOTES.filter(function (s) { return ST.read[s]; }).length, NOTES.length];
    if (NSLIDES) p.slides = [Math.min(cnt(ST.seen), NSLIDES), NSLIDES];
    if (XS.length) p.examples = [XS.filter(function (s) { return ST.read[s]; }).length, XS.length];
    if (EXIDS.length) p.exercises = [EXIDS.filter(function (id) { return ST.ex.chk[id]; }).length, EXIDS.length];
    if (MS.length) p.lab = [MS.filter(function (m) { return ST.lab[m.id]; }).length, MS.length];
    if (NCANDO) { var s = 0; for (var i = 1; i <= NCANDO; i++) s += (ST.cando["c" + i] || 0); p.checklist = [s / 2, NCANDO]; }
    return p;
  }
  function updateProgress() {
    var p = parts(), sum = 0, n = 0;
    Object.keys(p).forEach(function (k) { var b = $('[data-bd="' + k + '"]'); var f = p[k][1] ? p[k][0] / p[k][1] : 0; sum += f; n++;
      if (b) { b.textContent = (k === "checklist" ? Math.round(p[k][0] * 10) / 10 : p[k][0]) + "/" + p[k][1]; b.classList.toggle("full", p[k][0] >= p[k][1]); } });
    var pct = n ? Math.round(sum / n * 100) : 0, bar = $("#pbar");
    if (bar) { bar.firstElementChild.style.width = pct + "%"; bar.setAttribute("aria-valuenow", String(pct)); }
    var pp = $("#ppct"); if (pp) pp.textContent = pct + " %";
    ST.pct = pct; save();
    if (current === "start") renderStart();
  }

  /* ---------- start view ---------- */
  function renderStart() {
    var p = parts();
    $$("[data-stage-item]").forEach(function (li) {
      var k = li.getAttribute("data-stage-item"), done = false, m;
      if ((m = /^read:(.+)$/.exec(k))) done = !!ST.read[m[1]];
      else if ((m = /^qc:(.+)$/.exec(k))) done = !!ST.qc[m[1]];
      else if ((m = /^ex:(.+)$/.exec(k))) done = !!ST.ex.chk[m[1]];
      else if (k === "notes") done = p.notes && p.notes[0] >= p.notes[1];
      else if (k === "slides") done = p.slides && p.slides[0] >= p.slides[1];
      else if (k === "examples") done = p.examples && p.examples[0] >= p.examples[1];
      else if (k === "exercises") done = p.exercises && p.exercises[0] >= p.exercises[1];
      else if (k === "lab") done = p.lab && p.lab[0] >= p.lab[1];
      else if (k === "checklist") done = p.checklist && p.checklist[0] >= p.checklist[1];
      else if ((m = /^ms:(.+)$/.exec(k))) done = !!ST.lab[m[1]];
      li.classList.toggle("done", !!done);
    });
    $$("[data-stage]").forEach(function (st) { var items = $$("[data-stage-item]", st), d = items.filter(function (i) { return i.classList.contains("done"); }).length; var s = $(".st", st); if (s) s.textContent = d + "/" + items.length; });
    var c = $("#contbtn"), w = $("#contwhen");
    if (c) { var nx = nextStep(); tx(c, nx.en, nx.ms); c.setAttribute("data-goto", nx.go); }
    if (w) { w.textContent = ST.last ? L2("Last opened: ", "Terakhir dibuka: ") + new Date(ST.last).toLocaleDateString(P.lang === "ms" ? "ms-MY" : "en-GB", { day: "numeric", month: "short", year: "numeric" }) : ""; }
  }
  function nextStep() {
    for (var i = 0; i < NOTES.length; i++) if (!ST.read[NOTES[i]]) return { en: "Continue: Notes §" + (i + 1), ms: "Sambung: Nota §" + (i + 1), go: "notes/" + NOTES[i] };
    if (NSLIDES && cnt(ST.seen) < NSLIDES) return { en: "Continue: Slides " + (ST.slide + 1) + "/" + NSLIDES, ms: "Sambung: Slides " + (ST.slide + 1) + "/" + NSLIDES, go: "slides" };
    for (var x = 0; x < XS.length; x++) if (!ST.read[XS[x]]) return { en: "Continue: Example " + (x + 1), ms: "Sambung: Contoh " + (x + 1), go: "examples/" + XS[x] };
    for (var j = 0; j < EXIDS.length; j++) if (!ST.ex.chk[EXIDS[j]]) return { en: "Continue: Exercises", ms: "Sambung: Latihan", go: "exercises/" + EXIDS[j] };
    if (MS.length && MS.some(function (m) { return !ST.lab[m.id]; })) return { en: "Continue: Explorer", ms: "Sambung: Explorer", go: "lab" };
    for (var k = 1; k <= NCANDO; k++) if ((ST.cando["c" + k] || 0) < 2) return { en: "Continue: Checklist", ms: "Sambung: Senarai semak", go: "start/cando" };
    return { en: "Everything in this Unit is done", ms: "Semua dalam Unit ini selesai", go: "start" };
  }
  var cb = $("#contbtn"); if (cb) cb.addEventListener("click", function () { var p = cb.getAttribute("data-goto").split("/"); show(p[0], { anchor: p[1] }); });

  /* ---------- answer marking, the same everywhere: ✓ on the right option, ✗ on a wrong pick, a verdict line ---------- */
  var VERD = { ok: ["✓ Correct.", "✓ Betul."], no: ["✗ Not quite. The correct answer is marked ✓.", "✗ Belum tepat. Jawapan betul ditanda ✓."] };
  function markOpts(opts, ans, pick) {
    opts.forEach(function (o) { var k = o.getAttribute("data-k"), st = k === ans ? "right" : k === pick ? "wrong" : "other"; o.disabled = true; o.setAttribute("data-state", st);
      if (st !== "other" && !$(".mark", o)) o.appendChild(el("span", { class: "mark", "aria-hidden": "true" }, st === "right" ? "✓" : "✗"));
      if (k === pick && !$(".yours", o)) o.appendChild(el("span", { class: "yours" }, bi("your answer", "jawapan anda"))); });
  }
  function verdict(ok) { var v = VERD[ok ? "ok" : "no"]; return '<b class="verdict ' + (ok ? "v-ok" : "v-no") + '">' + bi(v[0], v[1]) + '</b>'; }

  /* ---------- notes: read marks, key-points mode, quick checks ---------- */
  function syncRead() {
    NOTES.concat(XS).forEach(function (id) { var sec = document.getElementById(id); if (!sec) return; var on = !!ST.read[id]; sec.classList.toggle("isread", on);
      var ck = $(".readck input", sec); if (ck) ck.checked = on; var a = $('.toc a[data-toc="' + id + '"]'); if (a) a.classList.toggle("isread", on); });
  }
  $$(".readck input").forEach(function (ck) { ck.addEventListener("change", function () { var sec = ck.closest(".nsec, .xsec"); ST.read[sec.id] = ck.checked; syncRead(); updateProgress(); }); });
  $$("[data-nmode]").forEach(function (b) { b.addEventListener("click", function () { ST.nmode = b.getAttribute("data-nmode"); applyNmode(); save(); }); });
  function applyNmode() { var art = $(".article"); if (!art) return; art.classList.toggle("keyonly", ST.nmode === "key"); $$("[data-nmode]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-nmode") === ST.nmode)); }); $$("details.kp").forEach(function (d) { if (ST.nmode === "key") d.open = true; }); }
  $$(".qc").forEach(function (q) {
    var id = q.getAttribute("data-qc"), ans = q.getAttribute("data-ans"), opts = $$(".opt", q), fb = $(".fb", q);
    function paint() { var r = ST.qc[id]; if (!r) return; markOpts(opts, ans, r.pick); q.setAttribute("data-done", r.ok ? "ok" : "no");
      if (fb) { fb.hidden = false; fb.setAttribute("data-ok", String(!!r.ok)); var vv = $(".verdict", fb); if (vv) vv.remove(); fb.insertAdjacentHTML("afterbegin", verdict(r.ok) + " "); } }
    opts.forEach(function (o) { o.addEventListener("click", function () { if (ST.qc[id]) return; ST.qc[id] = { pick: o.getAttribute("data-k"), ok: o.getAttribute("data-k") === ans, at: Date.now() }; paint(); updateProgress(); }); });
    if (fb) fb.hidden = !ST.qc[id]; paint();
  });

  /* ---------- examples: the steps of a model answer appear one at a time; the last one completes the example ---------- */
  $$(".xsec").forEach(function (sec) {
    var steps = $$(".xstep", sec), id = sec.id; if (!steps.length) return;
    var bar = el("div", { class: "xbar" }), nb = el("button", { class: "btn", type: "button" }), ab = el("button", { class: "btn ghost", type: "button" }, bi("Show all steps", "Tunjuk semua langkah")),
      hb = el("button", { class: "linkbtn", type: "button" }, bi("Hide the steps again", "Sembunyikan semula langkah")), after = $(".xafter", sec);
    function paint() {
      var n = Math.min(ST.xrev[id] || 0, steps.length);
      steps.forEach(function (s, i) { s.hidden = i >= n; });
      nb.hidden = ab.hidden = n >= steps.length; hb.hidden = n === 0;
      nb.innerHTML = bi("Show step " + (n + 1) + " of " + steps.length, "Tunjuk langkah " + (n + 1) + " daripada " + steps.length);
      if (after) after.hidden = n < steps.length;
    }
    function done() { if (!ST.read[id]) { ST.read[id] = true; syncRead(); updateProgress(); } }
    nb.addEventListener("click", function () { ST.xrev[id] = Math.min((ST.xrev[id] || 0) + 1, steps.length); save(); paint(); var s = steps[ST.xrev[id] - 1]; if (s) s.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" }); if (ST.xrev[id] >= steps.length) done(); });
    ab.addEventListener("click", function () { ST.xrev[id] = steps.length; save(); paint(); done(); });
    hb.addEventListener("click", function () { ST.xrev[id] = 0; save(); paint(); });
    bar.appendChild(nb); bar.appendChild(ab); bar.appendChild(hb);
    var last = steps[steps.length - 1]; last.parentNode.insertBefore(bar, last.nextSibling);
    paint();
  });

  /* ---------- slides viewer (the deck fragment is fetched when the tab is first shown) ---------- */
  var cv = $("#svcv"), slides = [], frame = $("#svframe"), svInit = false, svLoading = false;
  function fitSlides() { if (!frame || !cv) return; var w = frame.clientWidth; cv.style.transform = "scale(" + (w / 1920) + ")"; loadSlides(); }
  function loadSlides() {
    if (svInit || svLoading || !cv) return; svLoading = true;
    fetch(cv.getAttribute("data-src")).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }).then(function (t) { cv.innerHTML = t; var l = $("#svload"); if (l) l.remove(); initSlides(); })
      .catch(function (e) { svLoading = false; var l = $("#svload"); if (l) l.innerHTML = bi("The slides could not be loaded (" + e.message + "). Use the PDF.", "Slides tidak dapat dimuatkan (" + e.message + "). Guna PDF."); });
  }
  function goSlide(i) {
    if (!slides.length || !isFinite(i)) { if (isFinite(i)) pendingSlide = i; return; }
    i = clamp(Math.round(i), 0, slides.length - 1); ST.slide = i; ST.seen["s" + i] = true; pendingSlide = null;
    slides.forEach(function (s, k) { s.classList.toggle("on", k === i); });
    var c = $("#svcount"); if (c) c.textContent = (i + 1) + " / " + slides.length;
    $$(".thumbs button").forEach(function (b, k) { b.setAttribute("aria-current", String(k === i)); b.classList.toggle("seen", !!ST.seen["s" + k]); });
    var pv = $("#svprev"), nx = $("#svnext"), f0 = $("#svfirst"), fn = $("#svlast"), at0 = i === 0, atN = i === slides.length - 1;
    if (pv) pv.disabled = at0; if (f0) f0.disabled = at0; if (nx) nx.disabled = atN; if (fn) fn.disabled = atN;
    var sc = $("#svscrub"); if (sc) { sc.max = slides.length; sc.value = i + 1; scrubFill(); }
    updateProgress();
  }
  function initSlides() {
    slides = $$(".sl", cv); svInit = true; if (!slides.length) return;
    var th = $("#thumbs");
    if (th) { th.innerHTML = ""; slides.forEach(function (s, k) { var b = el("button", { type: "button" }, '<span class="n">' + (k + 1) + '</span><span>' + (s.getAttribute("data-title") || "") + '</span>'); b.addEventListener("click", function () { goSlide(k); }); th.appendChild(b); }); }
    goSlide(pendingSlide != null ? pendingSlide : (ST.slide || 0));
  }
  /* the bar under the slide is a slider: drag it (or click it) to any page; the tip shows the slide's title */
  function scrubFill() { var sc = $("#svscrub"); if (!sc) return; var f = sc.max > 1 ? (sc.value - 1) / (sc.max - 1) : 1; sc.style.setProperty("--fill", (f * 100) + "%"); }
  if (frame) {
    var scrub = $("#svscrub"), tip = $("#svtip"), tipT = null;
    if (scrub) {
      scrub.addEventListener("input", function () {
        var k = +scrub.value - 1; scrubFill();
        if (tip) { var t = slides[k] ? (slides[k].getAttribute("data-title") || "") : ""; tip.textContent = (k + 1) + (t ? " · " + t : ""); tip.style.left = (scrub.max > 1 ? (k / (scrub.max - 1)) * 100 : 0) + "%"; tip.classList.add("on"); clearTimeout(tipT); tipT = setTimeout(function () { tip.classList.remove("on"); }, 900); }
        goSlide(k);
      });
    }
    /* the mouse wheel or a two-finger scroll over the slide turns pages: one page per gesture */
    var wheelSum = 0, wheelLock = false, wheelT = null;
    frame.addEventListener("wheel", function (ev) {
      if (!slides.length || ev.ctrlKey) return;
      var d = Math.abs(ev.deltaY) >= Math.abs(ev.deltaX) ? ev.deltaY : ev.deltaX;
      if ((d < 0 && ST.slide === 0) || (d > 0 && ST.slide === slides.length - 1)) return;   /* past either end the page scrolls as usual */
      ev.preventDefault();
      clearTimeout(wheelT); wheelT = setTimeout(function () { wheelLock = false; wheelSum = 0; }, 220);
      if (wheelLock) return;
      wheelSum += d;
      if (Math.abs(wheelSum) >= 40) { wheelLock = true; goSlide(ST.slide + (wheelSum > 0 ? 1 : -1)); }
    }, { passive: false });
    /* a horizontal swipe on a phone */
    var tx0 = null, ty0 = null, swiped = 0;
    frame.addEventListener("touchstart", function (ev) { if (ev.touches.length === 1) { tx0 = ev.touches[0].clientX; ty0 = ev.touches[0].clientY; } }, { passive: true });
    frame.addEventListener("touchend", function (ev) {
      if (tx0 == null) return; var t = ev.changedTouches[0], dx = t.clientX - tx0, dy = t.clientY - ty0; tx0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) { swiped = Date.now(); goSlide(ST.slide + (dx < 0 ? 1 : -1)); }
    }, { passive: true });
    var f0 = $("#svfirst"), fn = $("#svlast");
    if (f0) f0.addEventListener("click", function () { goSlide(0); });
    if (fn) fn.addEventListener("click", function () { goSlide(slides.length - 1); });
    var pv = $("#svprev"), nx = $("#svnext"), fs = $("#svfull");
    if (pv) pv.addEventListener("click", function () { goSlide(ST.slide - 1); });
    if (nx) nx.addEventListener("click", function () { goSlide(ST.slide + 1); });
    if (fs) fs.addEventListener("click", function () { var st = $("#svstage"); if (!document.fullscreenElement) { if (st.requestFullscreen) st.requestFullscreen(); } else document.exitFullscreen(); });
    document.addEventListener("fullscreenchange", function () { setTimeout(fitSlides, 50); });
    frame.addEventListener("click", function (ev) { if (ev.target.closest("a") || Date.now() - swiped < 400) return; var r = frame.getBoundingClientRect(); goSlide(ST.slide + ((ev.clientX - r.left) > r.width / 2 ? 1 : -1)); });
    document.addEventListener("keydown", function (ev) { if (current !== "slides" || ev.target.matches("input,textarea,select")) return;
      if (ev.key === "ArrowRight" || ev.key === "PageDown" || ev.key === " ") { ev.preventDefault(); goSlide(ST.slide + 1); }
      else if (ev.key === "ArrowLeft" || ev.key === "PageUp") { ev.preventDefault(); goSlide(ST.slide - 1); }
      else if (ev.key === "Home") goSlide(0); else if (ev.key === "End") goSlide(slides.length - 1); });
    if (window.ResizeObserver) new ResizeObserver(function () { var w = frame.clientWidth; if (cv) cv.style.transform = "scale(" + (w / 1920) + ")"; }).observe(frame); else window.addEventListener("resize", fitSlides);
    var c0 = $("#svcount"); if (c0) c0.textContent = ((ST.slide || 0) + 1) + " / " + NSLIDES;
  }

  /* ---------- exercises ---------- */
  var L = { check: ["Check", "Semak"], newnum: ["New numbers", "Nombor baharu"], hint: ["Hint", "Petunjuk"], sol: ["Show solution", "Tunjuk penyelesaian"],
    sure: ["Sure", "Yakin"], unsure: ["Not sure", "Tidak pasti"], confq: ["Before you check:", "Sebelum semak:"],
    right: ["✓ Correct.", "✓ Betul."], wrong: ["✗ Not yet. Fix the fields marked ✗: try again, open a hint, or show the solution.", "✗ Belum tepat. Betulkan ruang bertanda ✗: cuba lagi, buka petunjuk, atau tunjuk penyelesaian."],
    partial: ["✗ {n} of {m} correct. Fix the fields marked ✗.", "✗ {n} daripada {m} betul. Betulkan ruang bertanda ✗."], viewed: ["Solution shown: counted as answered, not as right.", "Penyelesaian dipaparkan: dikira sebagai dijawab, bukan betul."], youwere: ["you were", "anda"],
    attempt: ["attempt", "cubaan"], within: ["within tolerance", "dalam toleransi"], hintused: ["hints used", "petunjuk digunakan"] };
  function T(k, sub) { var a = L[k][0], b = L[k][1]; if (sub) Object.keys(sub).forEach(function (s) { a = a.replace("{" + s + "}", sub[s]); b = b.replace("{" + s + "}", sub[s]); }); return bi(a, b); }
  function rng(seed) { var t = seed >>> 0; return function () { t += 0x6D2B79F5; var r = Math.imul(t ^ (t >>> 15), 1 | t); r ^= r + Math.imul(r ^ (r >>> 7), 61 | r); return ((r ^ (r >>> 14)) >>> 0) / 4294967296; }; }
  var EX = window.EX = { specs: {} };
  EX.define = function (id, spec) { EX.specs[id] = spec; };
  function exSeed(id) { if (!ST.ex.seed[id]) { ST.ex.seed[id] = (Date.now() % 100000) + Math.floor(Math.random() * 1000); save(); } return ST.ex.seed[id]; }
  function exParams(id) { var s = EX.specs[id]; return s.gen(rng(exSeed(id))); }
  function renderEx(id) {
    var art = $('article.qx[data-ex="' + id + '"]'), s = EX.specs[id]; if (!art || !s) return;
    var Pm = exParams(id), body = $(".exbody", art); body.innerHTML = "";
    body.appendChild(el("div", { class: "given" }, s.text(Pm)));
    var fl = el("div", { class: "fields" });
    s.fields.forEach(function (f) { var lab = el("label", { class: "fld" }, '<span>' + bi(f.label[0], f.label[1]) + (f.unit ? ' <span class="u">(' + f.unit + ')</span>' : "") + '</span>');
      var inp = el("input", { class: "ans", type: "text", inputmode: "decimal", autocomplete: "off", "data-f": f.id }); var v = ST.ex.v[id + "." + f.id]; if (v != null) inp.value = v;
      var fm = el("span", { class: "fmark", "aria-hidden": "true" }), iw = el("span", { class: "inwrap" }); iw.appendChild(inp); iw.appendChild(fm);
      inp.addEventListener("input", function () { ST.ex.v[id + "." + f.id] = inp.value; inp.removeAttribute("data-state"); fm.textContent = ""; fm.removeAttribute("data-state"); save(); }); lab.appendChild(iw); fl.appendChild(lab); });
    body.appendChild(fl);
    var conf = el("div", { class: "conf" }, '<span>' + T("confq") + '</span>');
    ["sure", "unsure"].forEach(function (c) { var b = el("button", { type: "button", "data-c": c }, T(c)); b.setAttribute("aria-pressed", String(ST.ex.conf[id] === c)); b.addEventListener("click", function () { ST.ex.conf[id] = c; $$("button", conf).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); save(); }); conf.appendChild(b); });
    body.appendChild(conf);
    var bar = el("div", { class: "qbar" }), chk = el("button", { class: "btn", type: "button" }, T("check")), nn = el("button", { class: "btn ghost", type: "button" }, T("newnum")), res = el("div", { class: "resline", role: "status" });
    var hb = el("button", { class: "btn ghost", type: "button" }), sb = el("button", { class: "btn ghost", type: "button" }, T("sol"));
    bar.appendChild(chk); bar.appendChild(hb); bar.appendChild(sb); bar.appendChild(nn); body.appendChild(bar); body.appendChild(res);
    var hints = el("div"); body.appendChild(hints); var sol = el("div"); body.appendChild(sol);
    function paintHints() { var n = ST.ex.hint[id] || 0; hints.innerHTML = ""; for (var i = 0; i < n && i < s.hints.length; i++) hints.appendChild(el("div", { class: "hintbox" }, '<b>' + T("hint") + ' ' + (i + 1) + '/' + s.hints.length + '</b>' + s.hints[i](Pm)));
      hb.innerHTML = T("hint") + " " + Math.min(n + 1, s.hints.length) + "/" + s.hints.length; hb.disabled = n >= s.hints.length; }
    function paintSol() { sol.innerHTML = ""; if (ST.ex.sol[id]) { sol.appendChild(el("div", { class: "sol" }, s.solution(Pm))); sb.disabled = true; } else sb.disabled = false; }
    function paintRes() { var r = ST.ex.chk[id]; res.removeAttribute("data-ok"); if (!r) { res.innerHTML = ""; return; }
      if (r.viewed && !ST.ex.att[id]) { res.innerHTML = T("viewed"); res.setAttribute("data-ok", "viewed"); return; }
      $$("input.ans", body).forEach(function (inp) { var st = r.f[inp.getAttribute("data-f")], fm = inp.nextElementSibling; if (st == null) return; inp.setAttribute("data-state", st ? "right" : "wrong");
        if (fm) { fm.textContent = st ? "✓" : "✗"; fm.setAttribute("data-state", st ? "right" : "wrong"); } });
      var n = Object.keys(r.f).filter(function (k) { return r.f[k]; }).length, m = s.fields.length;
      res.setAttribute("data-ok", String(n === m));
      res.innerHTML = '<b class="verdict ' + (n === m ? "v-ok" : "v-no") + '">' + (n === m ? T("right") : n === 0 ? T("wrong") : T("partial", { n: n, m: m })) + '</b> <span class="qmeta">· ' + T("attempt") + ' ' + (ST.ex.att[id] || 1) + (ST.ex.t[id] ? ' · ' + mmss(ST.ex.t[id]) : "") + '</span>'; }
    chk.addEventListener("click", function () {
      var f = {}, all = true;
      s.fields.forEach(function (fd) { var inp = $('input.ans[data-f="' + fd.id + '"]', body), x = parseFloat(String(inp.value).replace(/[−–]/g, "-").replace(",", ".")), ref = fd.fn(Pm);
        var tol = Math.max(fd.atol != null ? fd.atol : 0, (fd.rtol != null ? fd.rtol : 0.01) * Math.abs(ref)); var ok = isFinite(x) && Math.abs(x - ref) <= tol + 1e-9; f[fd.id] = ok; if (!ok) all = false; });
      ST.ex.att[id] = (ST.ex.att[id] || 0) + 1; if (!ST.ex.first[id]) ST.ex.first[id] = { ok: all, conf: ST.ex.conf[id] || null, at: Date.now(), hints: ST.ex.hint[id] || 0 };
      if (!ST.ex.t[id]) ST.ex.t[id] = exElapsed() - (ST.ex.t0 && ST.ex.t0[id] || 0);
      ST.ex.chk[id] = { f: f, ok: all, at: Date.now() }; save(); paintRes(); updateProgress(); renderStats();
    });
    nn.addEventListener("click", function () { ST.ex.seed[id] = (ST.ex.seed[id] || 1) + 7919; delete ST.ex.chk[id]; delete ST.ex.sol[id]; ST.ex.hint[id] = 0; s.fields.forEach(function (fd) { delete ST.ex.v[id + "." + fd.id]; }); ST.ex.t0 = ST.ex.t0 || {}; ST.ex.t0[id] = exElapsed(); delete ST.ex.t[id]; save(); renderEx(id); updateProgress(); });
    hb.addEventListener("click", function () { ST.ex.hint[id] = Math.min((ST.ex.hint[id] || 0) + 1, s.hints.length); save(); paintHints(); });
    sb.addEventListener("click", function () { ST.ex.sol[id] = true; if (!ST.ex.chk[id]) { ST.ex.chk[id] = { f: {}, ok: false, viewed: true, at: Date.now() }; } save(); paintSol(); paintRes(); updateProgress(); renderStats(); });
    paintHints(); paintSol(); paintRes();
    if (!ST.ex.t0 || ST.ex.t0[id] == null) { ST.ex.t0 = ST.ex.t0 || {}; ST.ex.t0[id] = exElapsed(); save(); }
  }
  /* multiple choice (also used for error-spotting lines) */
  function initChoice(q) {
    var id = q.getAttribute("data-q"), ans = q.getAttribute("data-ans"), opts = $$("[data-k]", q), fb = $(".fb", q), conf = $(".conf", q);
    function paint() { var r = ST.ex.chk[id]; if (!r) return; markOpts(opts, ans, r.pick); q.setAttribute("data-done", r.ok ? "ok" : "no");
      if (fb) { fb.hidden = false; fb.setAttribute("data-ok", String(!!r.ok)); var m = $(".meta", fb); if (m) m.innerHTML = verdict(r.ok) + (r.conf ? ' <span class="qmeta">· ' + T("youwere") + " " + T(r.conf).toLowerCase() + '</span>' : ""); }
      if (conf) $$("button", conf).forEach(function (b) { b.disabled = true; b.setAttribute("aria-pressed", String(b.getAttribute("data-c") === r.conf)); }); }
    if (conf) $$("button", conf).forEach(function (b) { b.addEventListener("click", function () { if (ST.ex.chk[id]) return; ST.ex.conf[id] = b.getAttribute("data-c"); $$("button", conf).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); save(); }); b.setAttribute("aria-pressed", String(ST.ex.conf[id] === b.getAttribute("data-c"))); });
    opts.forEach(function (o) { o.addEventListener("click", function () { if (ST.ex.chk[id]) return; var ok = o.getAttribute("data-k") === ans;
      ST.ex.chk[id] = { pick: o.getAttribute("data-k"), ok: ok, conf: ST.ex.conf[id] || null, at: Date.now() }; ST.ex.first[id] = { ok: ok, conf: ST.ex.conf[id] || null, at: Date.now() }; ST.ex.t[id] = exElapsed(); save(); paint(); updateProgress(); renderStats(); }); });
    if (fb) fb.hidden = !ST.ex.chk[id]; paint();
  }
  /* timer */
  var tmr = ST.ex.timer, tEl = $("#tmr"), pill = $("#tpill");
  function exElapsed() { return tmr.el + (tmr.run ? (Date.now() - tmr.t0) / 1000 : 0); }
  function tick() { if (tEl) tEl.textContent = mmss(exElapsed()); updatePill(); }
  function startTimer() { if (!tmr.run) { tmr.run = true; tmr.t0 = Date.now(); save(); } paintTimer(); }
  function pauseTimer() { if (tmr.run) { tmr.el = exElapsed(); tmr.run = false; save(); } paintTimer(); }
  function paintTimer() { var s = $("#tstart"), p = $("#tpause"); if (s) s.hidden = tmr.run; if (p) p.hidden = !tmr.run; tick(); }
  function updatePill() { if (!pill) return; pill.hidden = !(tmr.run && current !== "exercises"); if (!pill.hidden) pill.textContent = mmss(exElapsed()); }
  var ts = $("#tstart"), tp = $("#tpause"), tr = $("#treset");
  if (ts) ts.addEventListener("click", startTimer); if (tp) tp.addEventListener("click", pauseTimer);
  if (tr) tr.addEventListener("click", function () { tmr.el = 0; tmr.run = false; tmr.t0 = 0; save(); paintTimer(); });
  if (pill) pill.addEventListener("click", function () { show("exercises"); });
  setInterval(tick, 1000); paintTimer();
  /* summary statistics and calibration */
  function renderStats() {
    var box = $("#exstats"); if (!box) return;
    var ids = EXIDS, done = ids.filter(function (i) { return ST.ex.chk[i]; }), firstOk = ids.filter(function (i) { return ST.ex.first[i] && ST.ex.first[i].ok; });
    var cal = { sr: [], sw: [], ur: [], uw: [] };
    ids.forEach(function (i) { var f = ST.ex.first[i]; if (!f || !f.conf) return; cal[(f.conf === "sure" ? "s" : "u") + (f.ok ? "r" : "w")].push(i); });
    var tgt = C.targetMin || 0;
    var h = '<div class="kv"><div><b>' + done.length + '/' + ids.length + '</b><span>' + bi("answered", "dijawab") + '</span></div>' +
      '<div><b>' + firstOk.length + '/' + done.length + '</b><span>' + bi("right first time", "betul pada cubaan pertama") + '</span></div>' +
      '<div><b>' + mmss(exElapsed()) + '</b><span>' + bi("on the timer", "pada pemasa") + (tgt ? ' · ' + bi("target", "sasaran") + ' ' + tgt + ' min' : "") + '</span></div></div>';
    var names = function (arr) { return arr.length ? arr.map(function (i) { return '<a href="#exercises-' + i + '" data-exlink="' + i + '">' + i.toUpperCase() + '</a>'; }).join(", ") : "—"; };
    h += '<div class="tbl"><table class="cal"><tr><th class="l">' + bi("Your confidence", "Keyakinan anda") + '</th><th>' + bi("Right", "Betul") + '</th><th>' + bi("Wrong", "Salah") + '</th></tr>' +
      '<tr><td class="l">' + bi("Sure", "Yakin") + '</td><td>' + cal.sr.length + '</td><td>' + cal.sw.length + '</td></tr>' +
      '<tr><td class="l">' + bi("Not sure", "Tidak pasti") + '</td><td>' + cal.ur.length + '</td><td>' + cal.uw.length + '</td></tr></table></div>';
    h += '<p class="muted" style="font-size:13.5px;margin:8px 0 0">' + bi("Sure and wrong: ", "Yakin tetapi salah: ") + names(cal.sw) + '. ' + bi("Not sure and right: ", "Tidak pasti tetapi betul: ") + names(cal.ur) + '.</p>';
    box.innerHTML = h;
    $$("[data-exlink]", box).forEach(function (a) { a.addEventListener("click", function (ev) { ev.preventDefault(); show("exercises", { anchor: a.getAttribute("data-exlink") }); }); });
  }
  /* every exercise, in page order (Part A, B, C), so that "Continue" goes to the first one not done */
  $$(".q[data-q], article.qx[data-ex]").forEach(function (q) { EXIDS.push(q.getAttribute("data-q") || q.getAttribute("data-ex")); });
  $$(".q[data-q]").forEach(initChoice);
  Object.keys(EX.specs).forEach(renderEx);
  EX.ready = function () { Object.keys(EX.specs).forEach(renderEx); updateProgress(); };

  /* ---------- Explorer milestones (postMessage from the Explorer, or its localStorage record) ---------- */
  function labKey() { return C.lab ? PFX + "-lab-" + C.lab.id : null; }
  function syncLab() { var k = labKey(); if (!k) return; var rec = ld(k, {}) || {}; var changed = false; MS.forEach(function (m) { if (rec[m.id] && !ST.lab[m.id]) { ST.lab[m.id] = true; changed = true; } });
    MS.forEach(function (m) { var t = $('.tk[data-ms="' + m.id + '"]'); if (t) t.classList.toggle("done", !!ST.lab[m.id]); }); if (changed) { save(); } updateProgress(); }
  window.addEventListener("message", function (ev) { var d = ev.data; if (!d || d.type !== PFX + "-lab" || !C.lab || d.lab !== C.lab.id) return; if (!ST.lab[d.id]) { ST.lab[d.id] = true; save(); } syncLab(); });
  window.addEventListener("focus", syncLab); document.addEventListener("visibilitychange", function () { if (!document.hidden) syncLab(); });
  window.addEventListener("storage", function (e) { if (e.key === labKey()) syncLab(); });
  /* the iframe is lazy and sits in a hidden tab, so the "did not load" note is armed only when the
     Explorer tab is first shown, and removed if the Explorer loads after all */
  var lf = $("#labframe"), labLoaded = false, labArmed = false, labNote = null;
  if (lf) lf.addEventListener("load", function () { labLoaded = true; if (labNote) { labNote.remove(); labNote = null; } });
  function armLab() { if (!lf || labArmed) return; labArmed = true;
    setTimeout(function () { if (!labLoaded && !labNote) { labNote = el("p", { class: "note" }, bi("The Explorer did not load inside this page. Open it in its own tab with the link below; tasks done there are still recorded here.", "Explorer tidak dimuatkan di dalam halaman ini. Buka dalam tab sendiri melalui pautan di bawah; tugasan yang selesai di situ tetap direkodkan di sini.")); lf.parentNode.insertBefore(labNote, lf); } }, 8000); }
  $$(".tk[data-ms] .tkself").forEach(function (b) { b.addEventListener("click", function () { var t = b.closest(".tk"); ST.lab[t.getAttribute("data-ms")] = true; save(); syncLab(); }); });

  /* ---------- can-do checklist ---------- */
  $$(".cando .row").forEach(function (r) { var id = r.getAttribute("data-c"); $$("button", r).forEach(function (b) { var v = +b.getAttribute("data-v");
    b.setAttribute("aria-pressed", String((ST.cando[id] || 0) === v)); b.addEventListener("click", function () { ST.cando[id] = v; $$("button", r).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); save(); updateProgress(); }); }); });

  /* ---------- glossary filter ---------- */
  var gf = $("#gfilter"); if (gf) gf.addEventListener("input", function () { var q = gf.value.trim().toLowerCase(); $$(".gloss tbody tr").forEach(function (tr) { tr.hidden = q && tr.textContent.toLowerCase().indexOf(q) < 0; }); });

  /* ---------- drawer ---------- */
  var dr = $("#drawer"), sc = $("#scrim"), sn = $("#snbtn");
  function openDrawer() { if (!dr) return; dr.classList.add("open"); sc.hidden = false; sn.setAttribute("aria-expanded", "true"); }
  function closeDrawer() { if (!dr) return; dr.classList.remove("open"); sc.hidden = true; sn.setAttribute("aria-expanded", "false"); }
  if (sn) sn.addEventListener("click", function () { dr.classList.contains("open") ? closeDrawer() : openDrawer(); });
  if (sc) sc.addEventListener("click", closeDrawer); var dc = $("#drclose"); if (dc) dc.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closeDrawer(); });

  /* ---------- reset (double-tap) ---------- */
  var rs = $("#resetbtn"), armed = false;
  if (rs) rs.addEventListener("click", function () { if (!armed) { armed = true; tx(rs, "Tap again to erase this Unit’s progress", "Tekan sekali lagi untuk memadam kemajuan Unit ini"); setTimeout(function () { armed = false; tx(rs, "Reset this Unit’s progress", "Set semula kemajuan Unit ini"); }, 4000); return; }
    var f = fresh(); Object.keys(f).forEach(function (k) { ST[k] = f[k]; }); try { var k = labKey(); if (k) localStorage.removeItem(k); } catch (e) {} saveNow(); location.reload(); });

  /* ---------- downloads: the viewer's downloads capability where it exists (claude.ai), a plain download elsewhere ---------- */
  var DLP = null;
  function dlCap() {
    if (!DLP) { try { DLP = (window.claude && typeof window.claude.use === "function") ? Promise.resolve(window.claude.use("downloads")).catch(function () { return null; }) : Promise.resolve(null); } catch (e) { DLP = Promise.resolve(null); } }
    return DLP;
  }
  function anchorSave(blob, name, href, say) {
    var u = URL.createObjectURL(blob), a = document.createElement("a"); a.href = u; a.download = name; a.rel = "noopener"; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(u); }, 60000);
    var direct = href ? ' <a href="' + href + '" target="_blank" rel="noopener">' : "";
    say("Download started: " + name + "." + (href ? " Nothing arrived?" + direct + "Open the file directly</a>." : ""), "Muat turun bermula: " + name + "." + (href ? " Tiada fail?" + direct + "Buka fail terus</a>." : ""));
  }
  var FRAMED = (function () { try { return window.self !== window.top; } catch (e) { return true; } })();
  function saveFile(src, name, msgEl, btn) {
    function say(en, ms) { if (msgEl) msgEl.innerHTML = bi(en, ms); }
    var href = typeof src === "string" ? src : null;
    if (btn) btn.disabled = true; say("Preparing " + name + "…", "Menyediakan " + name + "…");
    var blobP = href ? fetch(href).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.blob(); }) : Promise.resolve(typeof src === "function" ? src() : src);
    return Promise.all([dlCap(), blobP]).then(function (a) {
      var d = a[0], blob = a[1];
      if (d && typeof d.save === "function") return d.save({ filename: name, data: blob }).then(function () { say("Saved: " + name, "Disimpan: " + name); }, function (e) {
        var c = e && e.code;
        if (c === "declined") say("Download cancelled.", "Muat turun dibatalkan.");
        else if (c === "rate_limited") say("Another download is waiting for your answer; try again in a moment.", "Satu lagi muat turun menunggu jawapan anda; cuba sebentar lagi.");
        else blocked();
      });
      if (FRAMED) { blocked(); return; }
      anchorSave(blob, name, href, say);
    }).catch(function (e) { say("Could not get " + name + " (" + e.message + ").", "Tidak dapat mendapatkan " + name + " (" + e.message + ")."); })
      .then(function () { if (btn) btn.disabled = false; });
    function blocked() {
      var dir = href ? ' <a href="' + href + '" target="_blank" rel="noopener">' : "";
      say("This view does not allow downloads." + (href ? dir + " Open the file directly</a>." : ""), "Paparan ini tidak membenarkan muat turun." + (href ? dir + " Buka fail terus</a>." : ""));
    }
  }
  dlCap();
  $$("[data-save]").forEach(function (b) { b.addEventListener("click", function () {
    var box = b.closest(".recbar, .cardacts, .slidebar") || b.parentNode, m = box ? $(".savemsg", box) : null;
    saveFile(b.getAttribute("data-save"), b.getAttribute("data-name"), m, b); }); });

  /* ---------- wide equations scroll sideways on a narrow screen: fade the edge while there is more ---------- */
  function eqHints() { $$(".eqwrap").forEach(function (w) { var more = w.scrollWidth > w.clientWidth + 2 && w.scrollLeft + w.clientWidth < w.scrollWidth - 2; w.classList.toggle("more", more); }); }
  var eqT = null; function eqSoon() { clearTimeout(eqT); eqT = setTimeout(eqHints, 120); }
  window.addEventListener("resize", eqSoon); document.addEventListener("scroll", function (ev) { if (ev.target && ev.target.classList && ev.target.classList.contains("eqwrap")) eqSoon(); }, true);
  document.addEventListener("toggle", eqSoon, true);

  /* ---------- header search: client-side, over this page only (no network) ---------- */
  function biText(node, lang) { if (!node) return ""; var c = node.cloneNode(true);
    $$((lang === "ms" ? ".en" : ".ms") + ",script,style,svg,.vh,.tkok,.mk,.tkn,.mk-badge,.xbar,.readck,.conf", c).forEach(function (x) { x.remove(); });
    $$("p,li,div,h2,h3,h4,td,th,tr,br,dt,dd", c).forEach(function (x) { x.appendChild(document.createTextNode(" ")); });
    return c.textContent.replace(/\s+/g, " ").trim(); }
  function nrm(s) { return (s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function goEl(view, node, anchor) { show(view, { noscroll: true, anchor: anchor }); setTimeout(function () { var d = node.closest && node.closest("details:not([open])"); if (d) d.open = true;
    if (node.hidden && node.classList.contains("xstep")) { var sec = node.closest(".xsec"); if (sec) { ST.xrev[sec.id] = 999; save(); $$(".xstep", sec).forEach(function (s) { s.hidden = false; }); } }
    node.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" }); node.classList.add("hflash"); setTimeout(function () { node.classList.remove("hflash"); }, 1800); }, 80); }
  var SIDX = null;
  function sEntry(tag, node, titleNode, bodyNode, go, prefix) { var e = { tag: tag, go: go, t: {}, b: {} };
    ["en", "ms"].forEach(function (l) { e.t[l] = (prefix ? prefix[l === "ms" ? 1 : 0] + " · " : "") + biText(titleNode, l); e.b[l] = biText(bodyNode || node, l); });
    e.n = { en: nrm(e.t.en), ms: nrm(e.t.ms) }; e.nb = { en: nrm(e.b.en), ms: nrm(e.b.ms) }; return e; }
  function buildIndex() {
    var X = [], TG = { start: ["Start", "Mula"], notes: ["Notes", "Nota"], slides: ["Slides", "Slides"], examples: ["Examples", "Contoh"], exercises: ["Exercises", "Latihan"], lab: ["Explorer", "Explorer"], glossary: ["Glossary", "Glosari"] };
    $$("#v-start .card > h2").forEach(function (h) { X.push(sEntry(TG.start, h.parentNode, h, null, function () { goEl("start", h.parentNode); })); });
    $$("#v-notes section.nsec").forEach(function (s) { X.push(sEntry(TG.notes, s, $("h2", s), null, function () { show("notes", { anchor: s.id }); })); });
    (C.slideTitles || []).forEach(function (t, i) { var e = { tag: TG.slides, go: function () { show("slides", { anchor: String(i + 1) }); }, t: { en: "Slide " + (i + 1) + " · " + t, ms: "Slide " + (i + 1) + " · " + t }, b: { en: "", ms: "" } };
      e.n = { en: nrm(e.t.en), ms: nrm(e.t.ms) }; e.nb = { en: "", ms: "" }; X.push(e); });
    $$("#v-examples section.xsec").forEach(function (s) { X.push(sEntry(TG.examples, s, $("h2", s), null, function () { show("examples", { anchor: s.id }); })); });
    $$("#v-exercises .q[data-q], #v-exercises article.qx").forEach(function (q) { var h = $("h4", q) || $("p", q); X.push(sEntry(TG.exercises, q, h, null, function () { goEl("exercises", q, q.id); })); });
    $$("#v-lab .tk").forEach(function (t) { X.push(sEntry(TG.lab, t, $("h4", t), null, function () { goEl("lab", t); })); });
    $$("#v-glossary table.gloss tr").forEach(function (r) { var c = $$("td", r); if (c.length < 2) return; X.push(sEntry(TG.glossary, r, c[0], c[1], function () { goEl("glossary", r); })); });
    return X;
  }
  var hq = $("#hq"), hres = $("#hres"), hsel = -1, hhits = [];
  function markUp(s, toks) { var h = esc(s), n = nrm(h); if (n.length !== h.length) return h; var spans = [];
    toks.forEach(function (t) { var i = n.indexOf(t); while (i >= 0 && t) { spans.push([i, i + t.length]); i = n.indexOf(t, i + t.length); } });
    if (!spans.length) return h; spans.sort(function (a, b) { return a[0] - b[0]; }); var out = "", p = 0;
    spans.forEach(function (sp) { if (sp[0] < p) return; out += h.slice(p, sp[0]) + "<mark>" + h.slice(sp[0], sp[1]) + "</mark>"; p = sp[1]; }); return out + h.slice(p); }
  function snippet(b, nb, t) { var i = nb.indexOf(t); if (i < 0) return b.length > 90 ? b.slice(0, 88) + "…" : b; var a = Math.max(0, i - 30); return (a ? "…" : "") + b.slice(a, a + 90) + (a + 90 < b.length ? "…" : ""); }
  function runSearch() {
    var q = nrm(hq.value).trim(), toks = q.split(/\s+/).filter(Boolean), l = P.lang === "ms" ? "ms" : "en";
    if (!toks.length) { closeRes(); return; } if (!SIDX) SIDX = buildIndex();
    hhits = SIDX.map(function (e) { var tt = e.n[l], tb = e.nb[l], scr = 0;
      for (var i = 0; i < toks.length; i++) { var k = toks[i]; if (tt.indexOf(k) >= 0) scr += 3; else if (tb.indexOf(k) >= 0) scr += 1; else return null; }
      if (tt.indexOf(q) === 0) scr += 2; return { e: e, s: scr }; }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
    hsel = hhits.length ? 0 : -1;
    hres.innerHTML = hhits.length ? hhits.map(function (h, i) { var e = h.e; return '<button type="button" role="option" id="hr' + i + '" aria-selected="' + (i === hsel) + '"><span class="tg">' + esc(e.tag[l === "ms" ? 1 : 0]) + '</span><span>' + markUp(e.t[l], toks) + '</span><span class="sn">' + markUp(snippet(e.b[l], e.nb[l], toks[0]), toks) + '</span></button>'; }).join("")
      : '<div class="none">' + esc(L2("Nothing on this page matches. Try a shorter word, e.g. waist or kink.", "Tiada padanan dalam halaman ini. Cuba perkataan yang lebih pendek, contohnya waist atau kink.")) + '</div>';
    hres.hidden = false; hq.setAttribute("aria-expanded", "true");
    $$("button", hres).forEach(function (b, i) { b.addEventListener("click", function () { pickRes(i); }); });
  }
  function closeRes() { if (!hres) return; hres.hidden = true; hq.setAttribute("aria-expanded", "false"); hsel = -1; }
  function pickRes(i) { var h = hhits[i]; if (!h) return; closeRes(); hq.blur(); h.e.go(); }
  function markSel() { $$("button", hres).forEach(function (b, i) { b.setAttribute("aria-selected", String(i === hsel)); if (i === hsel) b.scrollIntoView({ block: "nearest" }); }); }
  if (hq && hres) {
    hq.addEventListener("input", runSearch);
    hq.addEventListener("focus", function () { if (hq.value.trim()) runSearch(); });
    hq.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" && hhits.length) { hsel = (hsel + 1) % hhits.length; markSel(); e.preventDefault(); }
      else if (e.key === "ArrowUp" && hhits.length) { hsel = (hsel - 1 + hhits.length) % hhits.length; markSel(); e.preventDefault(); }
      else if (e.key === "Enter") { if (hsel >= 0) { pickRes(hsel); e.preventDefault(); } }
      else if (e.key === "Escape") { if (!hres.hidden) { closeRes(); e.stopPropagation(); } else hq.blur(); } });
    document.addEventListener("pointerdown", function (e) { if (!hres.hidden && !e.target.closest("#hsearch")) closeRes(); });
    langHooks.push(function () { if (!hres.hidden) runSearch(); });
    document.addEventListener("keydown", function (e) { var sg = $("#sguide"); if (e.key === "/" && !e.ctrlKey && !e.metaKey && !(e.target.closest && e.target.closest("input,textarea,select,[contenteditable]")) && (!sg || sg.hidden)) { e.preventDefault(); hq.focus(); } });
  }

  /* ---------- screen guide (ⓘ) and a short tour of the screen ---------- */
  var REGIONS = C.regions || [];
  var sguide = $("#sguide"), sgscrim = $("#sgscrim"), binfo = $("#btn-info"), ring = $("#tourring"), tcard = $("#tourcard"), tourI = -1, tourList = [];
  function visRegions() { return REGIONS.filter(function (r) { var n = $(r[0]); return n && n.getClientRects().length; }); }
  function renderGuide() { var l = P.lang === "ms" ? 1 : 0; tourList = visRegions();
    $("#sglist").innerHTML = tourList.map(function (r, i) { return '<li><button type="button" data-ti="' + i + '"><b>' + esc(r[1 + l]) + '</b><span class="d">' + esc(r[3 + l]) + '</span></button></li>'; }).join("");
    $$("#sglist button").forEach(function (b) { b.addEventListener("click", function () { closeGuide(true); startTour(+b.getAttribute("data-ti")); }); }); }
  function openGuide() { endTour(true); renderGuide(); sguide.hidden = false; sgscrim.hidden = false; binfo.setAttribute("aria-expanded", "true"); binfo.classList.remove("hint");
    if (!P.guided) { P.guided = true; savePrefs(); } var f = $("#sglist button", sguide); if (f) f.focus(); }
  function closeGuide(keepFocus) { sguide.hidden = true; sgscrim.hidden = true; binfo.setAttribute("aria-expanded", "false"); if (!keepFocus) binfo.focus(); }
  function startTour(i) { tourList = visRegions(); if (!tourList.length) return; tourI = clamp(i, 0, tourList.length - 1); ring.hidden = false; tcard.hidden = false;
    var n = $(tourList[tourI][0]), r = n.getBoundingClientRect(), tall = r.height > innerHeight * 0.6;
    n.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: tall ? "start" : "center" });
    placeTour(); setTimeout(placeTour, 350); setTimeout(placeTour, 700); $("#tcnext").focus({ preventScroll: true }); }
  function placeTour() { if (tourI < 0) return; var rg = tourList[tourI], l = P.lang === "ms" ? 1 : 0, n = $(rg[0]); if (!n) { endTour(); return; }
    var r = n.getBoundingClientRect(), p = 6, top = Math.max(4, r.top - p), bot = Math.min(innerHeight - 4, r.bottom + p), left = Math.max(4, r.left - p), right = Math.min(innerWidth - 4, r.right + p);
    ring.style.top = top + "px"; ring.style.left = left + "px"; ring.style.width = Math.max(0, right - left) + "px"; ring.style.height = Math.max(0, bot - top) + "px";
    $("#tctitle").textContent = rg[1 + l]; $("#tctext").textContent = rg[3 + l]; $("#tcn").textContent = (tourI + 1) + " / " + tourList.length;
    $("#tcprev").disabled = tourI === 0;
    tx($("#tcnext"), tourI === tourList.length - 1 ? "Finish" : "Next", tourI === tourList.length - 1 ? "Selesai" : "Seterusnya");
    var cw = tcard.offsetWidth, ch = tcard.offsetHeight, cx = Math.min(Math.max(8, left), innerWidth - cw - 8), cy;
    if (bot + 12 + ch < innerHeight) cy = bot + 12; else if (top - 12 - ch > 0) cy = top - 12 - ch; else cy = innerHeight - ch - 12;
    tcard.style.left = cx + "px"; tcard.style.top = cy + "px"; }
  function endTour(silent) { if (tourI < 0) return; tourI = -1; ring.hidden = true; tcard.hidden = true; if (!silent && binfo) binfo.focus(); }
  if (sguide && binfo) {
    binfo.addEventListener("click", function () { sguide.hidden ? openGuide() : closeGuide(); });
    $("#sgclose").addEventListener("click", function () { closeGuide(); });
    sgscrim.addEventListener("click", function () { closeGuide(); });
    $("#sgtour").addEventListener("click", function () { closeGuide(true); startTour(0); });
    $("#tcnext").addEventListener("click", function () { if (tourI >= tourList.length - 1) endTour(); else startTour(tourI + 1); });
    $("#tcprev").addEventListener("click", function () { startTour(tourI - 1); });
    $("#tcclose").addEventListener("click", function () { endTour(); });
    langHooks.push(function () { if (!sguide.hidden) renderGuide(); if (tourI >= 0) placeTour(); $("#sgclose").setAttribute("aria-label", L2("Close", "Tutup")); });
    if (!P.guided) binfo.classList.add("hint");
    window.addEventListener("scroll", function () { if (tourI >= 0) placeTour(); }, { passive: true });
    window.addEventListener("resize", function () { if (tourI >= 0) placeTour(); });
    document.addEventListener("keydown", function (e) {
      if (tourI >= 0) { if (e.key === "Escape") endTour(); else if (e.key === "ArrowRight") { if (tourI < tourList.length - 1) startTour(tourI + 1); else endTour(); } else if (e.key === "ArrowLeft") startTour(tourI - 1); else return;
        e.preventDefault(); e.stopImmediatePropagation(); return; }
      if (!sguide.hidden && e.key === "Escape") { closeGuide(); e.preventDefault(); e.stopImmediatePropagation(); } }, true);
  }

  /* ---------- go ---------- */
  syncRead(); applyNmode(); syncLab(); applyLang();
  /* the Dr RJ guide panel navigates through these, exactly like a "Go to" button (rz-tutor-worker panel-mount.js) */
  window.RZ = { show: function (v) { show(v); }, goTo: function (v, a) { show(v, { anchor: a }); },
    goSlide: function (i) { if (current !== "slides") show("slides"); goSlide(i); }, current: function () { return current; }, lang: function () { return P.lang; } };
  if (VIEWS.length) { updateProgress(); fromHash(); }
  window.COURSE_API = { show: show, state: ST, save: save, fmt: fmt, bi: bi, saveFile: saveFile, lang: function () { return P.lang; } };
})();
