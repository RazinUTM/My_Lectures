/* SPDX-License-Identifier: MIT · Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
   Engine of the NURBS–meshfree primer pages (rz-tnl-app-template): views and hash routes, settings buttons
   (rz-settings-buttons), description fold, search, progress, notes reading, quick checks, recall and can-do,
   stepwise examples, seeded exercises, slides, Explorer milestones, glossary filter, the scripted guide in
   Dr RJ's panel and the screen guide (ⓘ). Reads window.COURSE (written by web/build.py) and EX.specs.
   Exposes window.RZ = {show, goTo, goSlide, current, lang} and window.RZ_AVS for the rz-tutor panel glue.
   Every storage access is in try/catch: the page works with localStorage blocked (state then lives in memory). */
(function () {
  "use strict";
  var C = window.COURSE || {}, D = document, html = D.documentElement;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || D).querySelectorAll(s)); };
  var MEM = {};
  function ld(k, dflt) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : dflt; } catch (e) { return MEM[k] || dflt; } }
  function sv(k, v) { MEM[k] = v; try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function bi(en, ms) { return '<span class="en">' + en + '</span><span class="ms">' + ms + '</span>'; }
  function L2(en, ms) { return PR.lang === "ms" ? ms : en; }
  function el(tag, attrs, inner) { var e = D.createElement(tag); for (var k in (attrs || {})) e.setAttribute(k, attrs[k]); if (inner !== undefined) e.innerHTML = inner; return e; }

  /* ---------------------------------------------------------------- preferences (rz-settings-buttons) */
  var FONT_STEPS = [0.9, 1, 1.15, 1.3];
  function fontStep(f) { var k = 0; FONT_STEPS.forEach(function (v, i) { if (Math.abs(v - f) < Math.abs(FONT_STEPS[k] - f)) k = i; }); return k; }
  function nextFont(f, dir) {
    if (dir > 0) { for (var i = 0; i < FONT_STEPS.length; i++) if (FONT_STEPS[i] > f + 1e-6) return FONT_STEPS[i]; return FONT_STEPS[0]; }
    for (var j = FONT_STEPS.length - 1; j >= 0; j--) if (FONT_STEPS[j] < f - 1e-6) return FONT_STEPS[j]; return FONT_STEPS[FONT_STEPS.length - 1];
  }
  var SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';
  var p0 = ld(C.prefs, {}), dark = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  var PR = { lang: p0.lang || "ms", theme: p0.theme || (dark ? "dark" : "light"), font: +p0.font || 1, fold: !!p0.fold, seen: !!p0.seen };
  function savePrefs() { sv(C.prefs, { lang: PR.lang, theme: PR.theme, font: PR.font, fold: PR.fold, seen: PR.seen }); }
  function applyPrefs() {
    html.setAttribute("data-theme", PR.theme); html.setAttribute("data-lang", PR.lang); html.lang = PR.lang === "ms" ? "ms" : "en";
    html.style.setProperty("--font-scale", String(PR.font)); html.style.setProperty("--ts", String(PR.font));
    var tb = $("#btn-theme"); if (tb) { tb.innerHTML = PR.theme === "dark" ? SUN : MOON; tb.title = PR.theme === "dark" ? L2("Light theme", "Tema cerah") : L2("Dark theme", "Tema gelap"); tb.setAttribute("aria-label", tb.title); }
    var lb = $("#btn-lang"); if (lb) { lb.textContent = PR.lang === "ms" ? "EN" : "BM"; lb.title = PR.lang === "ms" ? "Language" : "Bahasa"; lb.setAttribute("aria-label", lb.title); }
    var fb = $("#btn-font"); if (fb) { var k = fontStep(PR.font); $$(".lvl i", fb).forEach(function (d, i) { d.classList.toggle("on", i <= k); });
      fb.title = L2("Text size ", "Saiz teks ") + Math.round(PR.font * 100) + "% (" + L2("click: ", "klik: ") + Math.round(nextFont(PR.font, 1) * 100) + "%)"; fb.setAttribute("aria-label", fb.title); }
    var ib = $("#btn-info"); if (ib) { ib.title = L2("About this screen", "Tentang skrin ini"); ib.setAttribute("aria-label", ib.title); }
    var fd = $("#foldbtn"); if (fd) { $(".sub") && $(".sub").classList.toggle("folded", PR.fold); fd.setAttribute("aria-expanded", String(!PR.fold)); }
    var q = $("#q"); if (q) q.placeholder = L2("Search this part", "Cari dalam bahagian ini");
    var sf = $(".sframe"); if (sf) sf.setAttribute("aria-label", L2("Slides: use the arrow keys", "Slides: guna kekunci anak panah"));
    pushPrefs();
  }
  function wirePrefs() {
    var t = $("#btn-theme"), l = $("#btn-lang"), f = $("#btn-font"), i = $("#btn-info"), fd = $("#foldbtn");
    if (t) t.addEventListener("click", function () { PR.theme = PR.theme === "dark" ? "light" : "dark"; savePrefs(); applyPrefs(); });
    if (l) l.addEventListener("click", function () { PR.lang = PR.lang === "ms" ? "en" : "ms"; savePrefs(); applyPrefs(); refreshAll(); });
    if (f) f.addEventListener("click", function (e) { PR.font = nextFont(PR.font, e.shiftKey ? -1 : 1); /* an old stored value (A−/A+) moves to the next step above it */ savePrefs(); applyPrefs(); fitSlides(); });
    if (i) { i.addEventListener("click", openGuide); if (!PR.seen) i.classList.add("hint"); }
    if (fd) fd.addEventListener("click", function () { PR.fold = !PR.fold; savePrefs(); applyPrefs(); });
  }

  /* ---------------------------------------------------------------- progress state */
  function fresh() { return { v: 1, visit: {}, read: {}, qc: {}, recall: {}, cando: {}, slides: {}, xm: {}, xs: {}, ex: { seed: {}, val: {}, ok: {}, hint: {}, sol: {} }, ms: {}, guide: { skip: {} } }; }
  var ST = ld(C.key, null);
  if (!ST || ST.v !== 1) ST = fresh();
  var F = fresh(); for (var k0 in F) if (!(k0 in ST)) ST[k0] = F[k0]; for (var k1 in F.ex) if (!(k1 in ST.ex)) ST.ex[k1] = F.ex[k1];
  function save() { sv(C.key, ST); }
  function cnt(o) { var n = 0; for (var k in o) if (o[k]) n++; return n; }
  var NOTES = C.notes || [], NSL = C.slides || 0, EXS = C.examples || [], EXR = C.exercises || [], MSS = (C.lab && C.lab.milestones) || [], NCAN = C.cando || 0;
  function counts() {
    var r = NOTES.filter(function (n) { return ST.read[n]; }).length, s = Math.min(cnt(ST.slides), NSL), x = EXS.filter(function (n) { return ST.xm[n]; }).length,
      e = EXR.filter(function (n) { return ST.ex.ok[n]; }).length, m = MSS.filter(function (n) { return ST.ms[n]; }).length, c = cnt(ST.cando);
    return { notes: [r, NOTES.length], slides: [s, NSL], examples: [x, EXS.length], exercises: [e, EXR.length], lab: [m, MSS.length], cando: [Math.min(c, NCAN), NCAN] };
  }
  function isDone(cond) {
    var c = counts(), p = cond.split(":"), a = p[0], b = p[1];
    if (a === "visit") return !!ST.visit[b];
    if (a === "read") return !!ST.read[b];
    if (a === "qc") return !!ST.qc[b];
    if (a === "recall") return !!ST.recall[b];
    if (a === "xm") return !!ST.xm[b];
    if (a === "ex") return !!ST.ex.ok[b];
    if (a === "ms") return !!ST.ms[b];
    if (c[a]) return c[a][0] >= c[a][1] && c[a][1] > 0;
    return false;
  }
  function updateProgress() {
    var c = counts(), parts = ["notes", "slides", "examples", "exercises", "lab", "cando"], sum = 0, n = 0;
    parts.forEach(function (k) { if (c[k][1]) { sum += c[k][0] / c[k][1]; n++; } });
    var pct = n ? Math.round(100 * sum / n) : 0, bar = $("#pbar");
    if (bar) { bar.setAttribute("aria-valuenow", pct); $("i", bar).style.width = pct + "%"; }
    var pp = $("#ppct"); if (pp) pp.textContent = pct + " %";
    if (ST.pct !== pct) { ST.pct = pct; save(); } /* the primer home reads this to show the part's progress */
    $$(".tab .bd[data-bd]").forEach(function (b) { var k = b.getAttribute("data-bd"); if (!c[k]) return; b.textContent = c[k][0] + "/" + c[k][1]; b.classList.toggle("full", c[k][0] >= c[k][1] && c[k][1] > 0); });
    $$("[data-stage-item]").forEach(function (li) { li.classList.toggle("done", isDone(li.getAttribute("data-stage-item"))); });
    $$(".stage").forEach(function (st) { var it = $$("[data-stage-item]", st), d = it.filter(function (x) { return x.classList.contains("done"); }).length, s = $(".st", st); if (s && it.length) s.textContent = d + " / " + it.length; });
    var nx = $$("[data-stage-item]").filter(function (li) { return !li.classList.contains("done"); })[0], cb = $("#contbtn");
    if (cb) { var a = nx && $("a", nx); cb.setAttribute("data-goto", a ? a.getAttribute("data-goto") : "start/cando"); cb.innerHTML = nx ? bi("Continue", "Teruskan") + " → " + (a ? a.innerHTML : "") : bi("All done — review anything", "Semua selesai — ulang kaji apa-apa"); }
    guideRefresh();
  }

  /* ---------------------------------------------------------------- views and routes */
  var VIEWS = $$("section.view").map(function (s) { return s.getAttribute("data-view"); }), current = "start";
  function flash(t) { t.classList.remove("coach"); void t.offsetWidth; t.classList.add("coach"); setTimeout(function () { t.classList.remove("coach"); }, 4600); }
  function show(v, opts) {
    opts = opts || {}; if (VIEWS.indexOf(v) < 0) v = "start"; current = v;
    $$("section.view").forEach(function (s) { s.hidden = s.getAttribute("data-view") !== v; });
    $$(".tab[data-view]").forEach(function (t) { var on = t.getAttribute("data-view") === v; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1; });
    var h = "#" + v + (opts.anchor ? "-" + opts.anchor : "");
    try { if (location.hash !== h) history.replaceState(null, "", h); } catch (e) {}
    ST.visit[v] = true; save();
    if (v === "slides") { fitSlides(); markSlide(); }
    if (opts.anchor) { var t = D.getElementById(opts.anchor); if (v === "slides") goSlide(parseInt(opts.anchor, 10) - 1); else if (t) setTimeout(function () { if (t.tagName === "DETAILS") t.open = true; t.scrollIntoView({ behavior: opts.instant ? "auto" : "smooth", block: "start" }); flash(t); }, 60); }
    else if (!opts.keep) window.scrollTo({ top: 0, behavior: "auto" });
    updateProgress();
  }
  function goTo(view, anchor) { show(view, { anchor: anchor }); }
  function fromHash(instant) { var h = decodeURIComponent((location.hash || "").slice(1)); if (!h) return show("start", { keep: true }); var i = h.indexOf("-"), v = i < 0 ? h : h.slice(0, i), a = i < 0 ? "" : h.slice(i + 1); show(v, { anchor: a, instant: instant }); }
  D.addEventListener("click", function (e) {
    var g = e.target.closest("[data-goto]"); if (!g) return; e.preventDefault();
    var p = g.getAttribute("data-goto").split("/"); show(p[0], { anchor: p[1] || "" });
  });
  $$(".tab[data-view]").forEach(function (t) { t.addEventListener("click", function (e) { show(t.getAttribute("data-view"));
    /* a mouse or touch click on Slides hands the arrow keys to the slides (keyboard users keep the tab pattern) */
    if (e.detail > 0 && t.getAttribute("data-view") === "slides") { var fr = $(".sframe"); if (fr) fr.focus({ preventScroll: true }); } }); });
  var tabsEl = $("nav.tabs"); if (tabsEl) tabsEl.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return; var i = VIEWS.indexOf(current) + (e.key === "ArrowRight" ? 1 : -1);
    i = (i + VIEWS.length) % VIEWS.length; show(VIEWS[i]); var t = $('.tab[data-view="' + VIEWS[i] + '"]'); if (t) t.focus();
  });
  window.addEventListener("hashchange", function () { fromHash(false); });

  /* ---------------------------------------------------------------- notes */
  function syncRead() {
    $$("section.nsec").forEach(function (s) { var on = !!ST.read[s.id], ck = $(".readck input", s); s.classList.toggle("isread", on); if (ck) ck.checked = on; });
    $$(".toc a[data-toc]").forEach(function (a) { a.classList.toggle("isread", !!ST.read[a.getAttribute("data-toc")]); });
  }
  $$("section.nsec .readck input").forEach(function (ck) { ck.addEventListener("change", function () { var s = ck.closest("section.nsec"); ST.read[s.id] = ck.checked; save(); syncRead(); updateProgress(); }); });
  var kpb = $("#kpmode"); if (kpb) kpb.addEventListener("click", function () { var a = $(".article"), on = !a.classList.contains("kponly"); a.classList.toggle("kponly", on); kpb.setAttribute("aria-pressed", String(on)); $$("details.kp", a).forEach(function (d) { d.open = on || d.open; }); });

  /* ---------------------------------------------------------------- quick checks (one try, not graded) */
  function paintQc(q) {
    var id = q.getAttribute("data-qc"), ans = q.getAttribute("data-ans"), got = ST.qc[id];
    $$(".opt", q).forEach(function (o) { var k = o.getAttribute("data-k"); o.disabled = !!got;
      o.setAttribute("data-state", got ? (k === ans ? "right" : (k === got ? "wrong" : "other")) : ""); o.setAttribute("aria-pressed", String(k === got)); });
    var fb = $(".fb", q); if (fb) { fb.hidden = !got; fb.setAttribute("data-ok", String(got === ans)); }
  }
  $$(".qc").forEach(function (q) { paintQc(q); $$(".opt", q).forEach(function (o) { o.addEventListener("click", function () { if (ST.qc[q.getAttribute("data-qc")]) return; ST.qc[q.getAttribute("data-qc")] = o.getAttribute("data-k"); save(); paintQc(q); updateProgress(); }); }); });

  /* ---------------------------------------------------------------- start: recall, can-do, files */
  $$("details[data-recall]").forEach(function (d) { var id = d.getAttribute("data-recall"); if (ST.recall[id]) d.classList.add("seen");
    d.addEventListener("toggle", function () { if (d.open) { ST.recall[id] = true; d.classList.add("seen"); save(); updateProgress(); } }); });
  $$(".cando [data-cd]").forEach(function (row) { var i = row.getAttribute("data-cd");
    function paint() { $$("button[data-lv]", row).forEach(function (b) { b.setAttribute("aria-pressed", String(ST.cando[i] === b.getAttribute("data-lv"))); }); }
    $$("button[data-lv]", row).forEach(function (b) { b.addEventListener("click", function () { ST.cando[i] = b.getAttribute("data-lv"); save(); paint(); updateProgress(); }); }); paint(); });
  var exb = $("#exportbtn"), imf = $("#importfile"), rsb = $("#resetbtn");
  if (exb) exb.addEventListener("click", function () {
    var blob = new Blob([JSON.stringify({ key: C.key, saved: new Date().toISOString(), progress: ST, prefs: ld(C.prefs, {}) }, null, 1)], { type: "application/json" });
    var a = el("a", { href: URL.createObjectURL(blob), download: C.key + "-progress.json" }); D.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  });
  if (imf) imf.addEventListener("change", function () { var f = imf.files[0]; if (!f) return; var r = new FileReader(); r.onload = function () {
    var msg = $("#filemsg"); try { var j = JSON.parse(r.result); if (j.key !== C.key || !j.progress || j.progress.v !== 1) throw new Error("key");
      ST = j.progress; save(); location.reload(); } catch (e) { if (msg) msg.innerHTML = bi("That file is not a progress file of this part.", "Fail itu bukan fail kemajuan bagi bahagian ini."); } }; r.readAsText(f); });
  if (rsb) rsb.addEventListener("click", function () { if (rsb.getAttribute("data-arm") !== "1") { rsb.setAttribute("data-arm", "1"); rsb.innerHTML = bi("Click again to erase your progress", "Klik sekali lagi untuk memadam kemajuan"); setTimeout(function () { rsb.removeAttribute("data-arm"); rsb.innerHTML = bi("Reset progress", "Set semula kemajuan"); }, 4000); return; }
    ST = fresh(); save(); location.hash = ""; location.reload(); });

  /* ---------------------------------------------------------------- examples: reveal step by step */
  $$("section.xsec").forEach(function (x) {
    var id = x.id, steps = $$(".xstep", x), btn = $(".xnext", x), all = $(".xall", x);
    function paint() { var n = Math.min(ST.xs[id] || 0, steps.length); steps.forEach(function (s, i) { s.hidden = i >= n; });
      if (btn) { btn.hidden = n >= steps.length; btn.innerHTML = bi("Show step ", "Tunjuk langkah ") + (n + 1) + " / " + steps.length; }
      if (all) all.hidden = n >= steps.length; var dn = $(".xdone", x); if (dn) dn.hidden = n < steps.length; }
    function setN(n) { ST.xs[id] = n; if (n >= steps.length) ST.xm[id] = true; save(); paint(); updateProgress(); }
    if (btn) btn.addEventListener("click", function () { setN((ST.xs[id] || 0) + 1); var s = steps[(ST.xs[id] || 1) - 1]; if (s) s.scrollIntoView({ behavior: "smooth", block: "nearest" }); });
    if (all) all.addEventListener("click", function () { setN(steps.length); });
    paint();
  });

  /* ---------------------------------------------------------------- exercises: seeded numbers, hints, solution, check */
  var EX = window.EX || { specs: {} };
  function rng(seed) { var a = seed >>> 0; return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function parseNum(s) { s = String(s || "").trim().replace(/\s/g, "").replace(/,/g, ".").replace(/−/g, "-"); return s === "" ? NaN : Number(s); }
  function renderEx(id) {
    var art = D.getElementById(id), s = EX.specs[id]; if (!art || !s) return; var body = $(".exrun", art);
    if (!ST.ex.seed[id]) ST.ex.seed[id] = 1 + Math.floor(Math.random() * 1e9);
    var P = s.gen(rng(ST.ex.seed[id])), flds = s.fields.filter(function (f) { return !f.show || f.show(P); }), solShown = !!ST.ex.sol[id];
    body.innerHTML = "";
    body.appendChild(el("p", { class: "given" }, "<b>" + bi("Given", "Diberi") + "</b> " + s.given(P)));
    var fw = el("div", { class: "fields" });
    flds.forEach(function (f) { var key = id + "." + f.id, w = el("label", { class: "fld" }, '<span class="fl">' + f.label + ' =</span>');
      var inp = el("input", { class: "ans", type: "text", inputmode: "decimal", autocomplete: "off", "aria-label": f.label.replace(/<[^>]+>/g, "") });
      inp.value = ST.ex.val[key] || ""; inp.disabled = solShown; inp.addEventListener("input", function () { ST.ex.val[key] = inp.value; save(); }); w.appendChild(inp); w.appendChild(el("span", { class: "fmark" })); fw.appendChild(w); });
    body.appendChild(fw);
    var bar = el("div", { class: "exbar" }), chk = el("button", { class: "btn", type: "button" }, bi("Check", "Semak")), hb = el("button", { class: "btn ghost", type: "button" }),
      sb = el("button", { class: "btn ghost", type: "button" }, bi("Show solution", "Tunjuk penyelesaian")), nb = el("button", { class: "btn ghost", type: "button" }, bi("New numbers", "Nombor baharu"));
    bar.appendChild(chk); bar.appendChild(hb); bar.appendChild(sb); bar.appendChild(nb); body.appendChild(bar);
    var verdict = el("p", { class: "verdict", role: "status" }); body.appendChild(verdict);
    var hints = el("div", { class: "hints" }); body.appendChild(hints); var sol = el("div", { class: "sol" }); body.appendChild(sol);
    function paintHints() { var n = ST.ex.hint[id] || 0; hints.innerHTML = ""; for (var i = 0; i < n && i < s.hints.length; i++) hints.appendChild(el("div", { class: "hintbox" }, "<b>" + bi("Hint", "Petunjuk") + " " + (i + 1) + "/" + s.hints.length + "</b> " + s.hints[i](P)));
      hb.innerHTML = bi("Hint", "Petunjuk") + " " + Math.min(n + 1, s.hints.length) + "/" + s.hints.length; hb.disabled = n >= s.hints.length || solShown; }
    function paintSol() { sol.hidden = !solShown; sol.innerHTML = solShown ? "<b>" + bi("Solution", "Penyelesaian") + "</b> " + s.solution(P) + '<p class="muted">' + bi("Checking is off for these numbers. Press New numbers to try a fresh set.", "Semakan ditutup untuk nombor ini. Tekan Nombor baharu untuk mencuba set yang baharu.") + "</p>" : ""; chk.disabled = solShown; sb.disabled = solShown; }
    function check(silent) { var all = true, any = false; $$(".fld", fw).forEach(function (w, i) { var f = flds[i], v = parseNum($("input", w).value), m = $(".fmark", w), ok = isFinite(v) && Math.abs(v - f.ans(P)) <= f.tol;
        any = any || isFinite(v); all = all && ok; $("input", w).setAttribute("data-state", isFinite(v) ? (ok ? "right" : "wrong") : ""); m.textContent = isFinite(v) ? (ok ? "✓" : "✗") : ""; });
      if (silent) return; if (!any) { verdict.innerHTML = bi("Enter your answers first.", "Masukkan jawapan anda dahulu."); return; }
      if (all) { ST.ex.ok[id] = true; verdict.className = "verdict v-ok"; verdict.innerHTML = bi("✓ Correct.", "✓ Betul."); } else { verdict.className = "verdict"; verdict.innerHTML = bi("✗ Not yet. Fix the fields marked ✗: try again, open a hint, or show the solution.", "✗ Belum tepat. Betulkan ruang bertanda ✗: cuba lagi, buka petunjuk, atau tunjuk penyelesaian."); }
      save(); updateProgress(); }
    chk.addEventListener("click", function () { check(false); });
    hb.addEventListener("click", function () { ST.ex.hint[id] = Math.min((ST.ex.hint[id] || 0) + 1, s.hints.length); save(); paintHints(); });
    sb.addEventListener("click", function () { ST.ex.sol[id] = true; save(); renderEx(id); });
    nb.addEventListener("click", function () { ST.ex.seed[id] = 1 + Math.floor(Math.random() * 1e9); ST.ex.hint[id] = 0; delete ST.ex.sol[id]; flds.forEach(function (f) { delete ST.ex.val[id + "." + f.id]; }); save(); renderEx(id); });
    paintHints(); paintSol(); if (ST.ex.ok[id] && !solShown) { verdict.className = "verdict v-ok"; verdict.innerHTML = bi("✓ Solved earlier. New numbers give a fresh set.", "✓ Sudah diselesaikan. Nombor baharu memberi set yang baharu."); }
  }
  EXR.forEach(renderEx);
  $$("div.q").forEach(function (q) { var b = $("button", q), a = $(".qa", q); if (b && a) b.addEventListener("click", function () { a.hidden = !a.hidden; b.setAttribute("aria-expanded", String(!a.hidden)); }); });

  /* ---------------------------------------------------------------- slides */
  var SL = $$("#v-slides section.slide"), si = 0, stage = $(".stage16"), frame = $(".sframe");
  function fitSlides() { if (!stage || !frame) return; var w = frame.clientWidth || 800; stage.style.transform = "scale(" + (w / 1600) + ")"; frame.style.height = (900 * w / 1600) + "px"; }
  function markSlide() { if (current !== "slides" || !SL.length) return; ST.slides[si + 1] = true; save(); updateProgress(); }
  function goSlide(i) { if (!SL.length) return; si = Math.max(0, Math.min(SL.length - 1, i)); SL.forEach(function (s, j) { s.classList.toggle("on", j === si); s.setAttribute("aria-hidden", String(j !== si)); });
    var cn = $("#scount"); if (cn) cn.textContent = (si + 1) + " / " + SL.length; var rg = $("#srange"); if (rg) rg.value = String(si + 1);
    try { if (current === "slides") history.replaceState(null, "", "#slides-" + (si + 1)); } catch (e) {} markSlide(); }
  var sb0 = { first: function () { goSlide(0); }, prev: function () { goSlide(si - 1); }, next: function () { goSlide(si + 1); }, last: function () { goSlide(SL.length - 1); } };
  $$("[data-sl]").forEach(function (b) { b.addEventListener("click", function () { sb0[b.getAttribute("data-sl")](); }); });
  var rg0 = $("#srange"); if (rg0) { rg0.max = String(SL.length); rg0.addEventListener("input", function () { goSlide(parseInt(rg0.value, 10) - 1); }); }
  var fsb = $("#sfull"); if (fsb) fsb.addEventListener("click", function () { var sv0 = $(".sv"); try { if (D.fullscreenElement) D.exitFullscreen(); else sv0.requestFullscreen(); } catch (e) {} });
  D.addEventListener("fullscreenchange", fitSlides);
  D.addEventListener("keydown", function (e) { if (current !== "slides" || /INPUT|TEXTAREA|SELECT/.test((e.target || {}).tagName || "")) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") { goSlide(si + 1); e.preventDefault(); } if (e.key === "ArrowLeft" || e.key === "PageUp") { goSlide(si - 1); e.preventDefault(); } });
  if (frame) { var x0 = null; frame.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    frame.addEventListener("touchend", function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) goSlide(si + (dx < 0 ? 1 : -1)); x0 = null; });
    frame.addEventListener("wheel", function (e) { if (Math.abs(e.deltaY) < 30) return; e.preventDefault(); goSlide(si + (e.deltaY > 0 ? 1 : -1)); }, { passive: false }); }
  window.addEventListener("resize", fitSlides);

  /* ---------------------------------------------------------------- Explorer milestones (postMessage from the lab, or its localStorage) */
  function syncLab() { var lab = ld(C.lab && C.lab.key, {}) || {}; MSS.forEach(function (m) { if (lab[m]) ST.ms[m] = true; }); paintTasks(); }
  function paintTasks() { $$(".tk[data-ms]").forEach(function (t) { var m = t.getAttribute("data-ms"), on = !!ST.ms[m], ck = $("input.tkck", t); t.classList.toggle("done", on); if (ck) ck.checked = on; }); }
  window.addEventListener("message", function (e) { var d = e.data || {}, lf = $("#labframe");
    if (!lf || e.source !== lf.contentWindow) return; /* only the embedded lab may tick a milestone */
    if (d.type === "nmf-lab" && MSS.indexOf(d.ms) >= 0 && !ST.ms[d.ms]) { ST.ms[d.ms] = true; save(); paintTasks(); updateProgress(); }
    if (d.type === "nmf-lab-ready") pushPrefs();
    if (d.type === "nmf-lab-height" && +d.h > 0) { lf.classList.add("autoh"); lf.style.height = Math.min(2600, Math.max(420, Math.ceil(+d.h) + 2)) + "px"; } });
  /* the lab follows this page's language, theme and text size; a message works even when storage is blocked */
  function pushPrefs() { var lf = $("#labframe"); if (!lf || !lf.contentWindow) return;
    try { lf.contentWindow.postMessage({ type: "nmf-prefs", lang: PR.lang, theme: PR.theme, font: PR.font }, location.protocol === "file:" ? "*" : location.origin); } catch (e) {} }
  var lfr = $("#labframe"); if (lfr) lfr.addEventListener("load", pushPrefs);
  window.addEventListener("storage", function (e) { if (C.lab && e.key === C.lab.key) { syncLab(); updateProgress(); } });
  window.addEventListener("focus", function () { syncLab(); updateProgress(); });
  $$(".tk[data-ms] input.tkck").forEach(function (ck) { ck.addEventListener("change", function () { ST.ms[ck.closest(".tk").getAttribute("data-ms")] = ck.checked; save(); paintTasks(); updateProgress(); }); });

  /* ---------------------------------------------------------------- glossary filter */
  var gf = $("#gfilter"); if (gf) gf.addEventListener("input", function () { var q = gf.value.trim().toLowerCase(); $$("table.gloss tr").forEach(function (tr) { tr.hidden = q && tr.textContent.toLowerCase().indexOf(q) < 0; }); });

  /* ---------------------------------------------------------------- search over the generated index */
  var qi = $("#q"), qr = $("#qres"), SIDX = C.sections || [];
  function norm(s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function search() {
    var q = norm(qi.value.trim()); if (q.length < 2) { qr.hidden = true; qr.innerHTML = ""; return; }
    var words = q.split(/\s+/), hits = SIDX.filter(function (s) { var t = norm(s.en + " " + s.ms + " " + (s.k || "")); return words.every(function (w) { return t.indexOf(w) >= 0; }); }).slice(0, 8);
    qr.innerHTML = hits.length ? hits.map(function (h, i) { return '<a href="#' + h.view + (h.anchor ? "-" + h.anchor : "") + '" data-goto="' + h.view + (h.anchor ? "/" + h.anchor : "") + '" role="option" data-i="' + i + '">' + bi(h.en, h.ms) + "</a>"; }).join("")
      : '<p class="none">' + bi("Nothing found. Try a shorter word.", "Tiada hasil. Cuba perkataan yang lebih pendek.") + "</p>";
    qr.hidden = false;
  }
  if (qi && qr) {
    qi.addEventListener("input", search);
    qi.addEventListener("keydown", function (e) { if (e.key === "Escape") { qi.value = ""; search(); } if (e.key === "Enter") { var a = $("a", qr); if (a) { a.click(); qr.hidden = true; qi.blur(); } } if (e.key === "ArrowDown") { var f = $("a", qr); if (f) { f.focus(); e.preventDefault(); } } });
    qr.addEventListener("keydown", function (e) { var a = D.activeElement; if (e.key === "ArrowDown" && a.nextElementSibling) { a.nextElementSibling.focus(); e.preventDefault(); } if (e.key === "ArrowUp") { (a.previousElementSibling || qi).focus(); e.preventDefault(); } if (e.key === "Escape") { qr.hidden = true; qi.focus(); } });
    qr.addEventListener("click", function () { qr.hidden = true; });
    D.addEventListener("click", function (e) { if (!e.target.closest(".search")) qr.hidden = true; });
  }

  /* ---------------------------------------------------------------- avatars and the tutor hooks */
  var AV = C.avatar || "../shared/avatar/";
  var AVS = {}; ["welcome", "wave", "explain", "think", "present", "tablet", "ok", "thumbs-up", "cheer", "arms-crossed", "head"].forEach(function (p) { AVS[p] = AV + p + ".webp"; });
  AVS.offer = AVS.welcome; AVS.badge = AVS.head;
  window.RZ_AVS = AVS;
  window.RZ = { show: function (v) { show(v); }, goTo: goTo, goSlide: function (i) { show("slides", { keep: true }); goSlide(i); }, current: function () { return current; }, lang: function () { return PR.lang; } };
  $$("img[data-avsrc]").forEach(function (im) { var k = im.getAttribute("data-avsrc"); if (AVS[k] && !im.getAttribute("src")) im.src = AVS[k]; });
  var CORNER = { welcome: "welcome", think: "think", explain: "present", present: "ok", ok: "ok", "arms-crossed": "arms-crossed", wave: "wave", cheer: "cheer", "thumbs-up": "thumbs-up", tablet: "tablet" };
  function pose(p) { var img = $("#rjav"), k = CORNER[p] || p; if (!img || !AVS[k] || img.getAttribute("data-pose") === k) return; img.setAttribute("data-pose", k); img.classList.add("swap"); setTimeout(function () { img.src = AVS[k]; img.classList.remove("swap"); }, 110); }

  /* ---------------------------------------------------------------- scripted guide in Dr RJ's panel */
  var G = C.guide || [], gbox = null, lastStep = null;
  function guideMount() {
    var bubble = $("#rzguide .bubble"), say = $("#rjsay"); if (!bubble || !G.length) return;
    gbox = el("div", { class: "rzact", id: "rzact", "aria-live": "polite" },
      '<div class="rzact-h"><b>' + bi("Activity", "Aktiviti") + '</b> <span class="rzact-n"></span><span class="rzact-dots" aria-hidden="true"></span></div>' +
      '<p class="rzact-t"></p><p class="rzact-hint" hidden></p><div class="rzact-b"><button type="button" class="rzbtn go">' + bi("Go to", "Pergi") + '</button>' +
      '<button type="button" class="rzbtn hint">' + bi("Hint", "Petunjuk") + '</button><button type="button" class="rzbtn skip">' + bi("Skip", "Langkau") + "</button></div>");
    if (say && say.nextSibling) bubble.insertBefore(gbox, say.nextSibling); else bubble.appendChild(gbox);
    $(".go", gbox).addEventListener("click", function () { var s = curStep(); if (!s) return; var p = s.goto.split("/"); show(p[0], { anchor: p[1] || "" }); pose("present"); });
    $(".hint", gbox).addEventListener("click", function () { var s = curStep(), h = $(".rzact-hint", gbox); if (!s) return; h.innerHTML = bi(s.hen, s.hms); h.hidden = !h.hidden; pose("think"); });
    $(".skip", gbox).addEventListener("click", function () { var s = curStep(); if (!s) return; ST.guide.skip[s.id] = true; save(); guideRefresh(); });
  }
  function curStep() { for (var i = 0; i < G.length; i++) if (!isDone(G[i].done) && !ST.guide.skip[G[i].id]) return G[i]; return null; }
  function guideRefresh() {
    if (!gbox) return; var s = curStep(), i = s ? G.indexOf(s) : G.length;
    $(".rzact-n", gbox).innerHTML = s ? bi("step ", "langkah ") + (i + 1) + "/" + G.length : bi("all steps done", "semua langkah selesai");
    $(".rzact-dots", gbox).innerHTML = G.map(function (g) { return '<i class="' + (isDone(g.done) ? "d" : ST.guide.skip[g.id] ? "s" : g === s ? "c" : "") + '"></i>'; }).join("");
    $(".rzact-t", gbox).innerHTML = s ? bi(s.en, s.ms) : bi("You have done every step of this part. Go back to anything that felt shaky, or try the exercises with new numbers.", "Awak telah selesai setiap langkah bahagian ini. Kembali kepada apa-apa yang masih goyah, atau cuba latihan dengan nombor baharu.");
    $$(".rzbtn", gbox).forEach(function (b) { b.disabled = !s; });
    var changed = lastStep !== (s && s.id);
    if (changed) { $(".rzact-hint", gbox).hidden = true;
      if (lastStep !== null) { gbox.classList.remove("new"); gbox.classList.add("ok"); pose(s ? "thumbs-up" : "cheer"); setTimeout(function () { gbox.classList.remove("ok"); if (s) { gbox.classList.add("new"); pose(s.pose || "wave"); } }, 1300); }
      else if (s) { gbox.classList.add("new"); }
      lastStep = s ? s.id : ""; }
  }

  /* ---------------------------------------------------------------- screen guide (ⓘ) */
  var REG = [
    [".crumbs", "Where you are: the primer home and this part.", "Di mana awak berada: laman primer dan bahagian ini."],
    ["header h1", "The part's title; the line under it folds away (▴).", "Tajuk bahagian; baris di bawahnya boleh dilipat (▴)."],
    [".search", "Search every section, example, exercise, slide and glossary term of this part.", "Cari setiap seksyen, contoh, latihan, slide dan istilah glosari dalam bahagian ini."],
    [".prefs", "Language (BM / EN), light or dark theme, text size (AA: four sizes in turn), and this guide (ⓘ).", "Bahasa (BM / EN), tema cerah atau gelap, saiz teks (AA: empat saiz bergilir), dan panduan ini (ⓘ)."],
    [".navwrap", "Tabs with their counts, and your progress across the six counted parts.", "Tab dengan kiraannya, dan kemajuan awak merentasi enam bahagian yang dikira."],
    ["main", "The content of the tab you chose.", "Kandungan tab yang awak pilih."],
    ["#rzguide", "Dr RJ: the next step of your plan (Go to · Hint · Skip) and a box for questions about this page.", "Dr RJ: langkah seterusnya dalam pelan awak (Pergi · Petunjuk · Langkau) dan ruang untuk soalan tentang page ini."],
    ["footer.foot", "Course, lecturer and licence.", "Kursus, pensyarah dan lesen."]
  ];
  var sgEl = null, sgi = 0;
  function spot(sel) { $$(".sgspot").forEach(function (x) { x.classList.remove("sgspot"); }); var t = $(sel); if (t) { t.classList.add("sgspot"); t.scrollIntoView({ behavior: "smooth", block: "center" }); } }
  function openGuide() {
    PR.seen = true; savePrefs(); var ib = $("#btn-info"); if (ib) ib.classList.remove("hint");
    if (!sgEl) { sgEl = el("div", { class: "sg", role: "dialog", "aria-modal": "false", "aria-label": "Screen guide" });
      sgEl.innerHTML = '<div class="sgcard"><div class="sghead"><b>' + bi("Screen guide", "Panduan skrin") + '</b><button type="button" class="sgx" aria-label="Close">×</button></div><ol class="sglist">' +
        REG.map(function (r, i) { return '<li><button type="button" data-sg="' + i + '">' + bi(r[1], r[2]) + "</button></li>"; }).join("") + '</ol><p class="sgkeys">' +
        bi("Keys: ← → step through the areas · Esc closes · in Slides, ← → change slide.", "Kekunci: ← → melangkah antara kawasan · Esc menutup · dalam Slides, ← → menukar slide.") + "</p></div>";
      D.body.appendChild(sgEl);
      $(".sgx", sgEl).addEventListener("click", closeGuide);
      $$("[data-sg]", sgEl).forEach(function (b) { b.addEventListener("click", function () { sgi = +b.getAttribute("data-sg"); paintSg(); }); });
    }
    sgEl.hidden = false; sgi = 0; paintSg(); $(".sgx", sgEl).focus();
  }
  function paintSg() { $$("[data-sg]", sgEl).forEach(function (b, i) { b.setAttribute("aria-current", String(i === sgi)); }); spot(REG[sgi][0]); }
  function closeGuide() { if (sgEl) sgEl.hidden = true; $$(".sgspot").forEach(function (x) { x.classList.remove("sgspot"); }); var ib = $("#btn-info"); if (ib) ib.focus(); }
  D.addEventListener("keydown", function (e) { if (!sgEl || sgEl.hidden) return; if (e.key === "Escape") closeGuide(); if (e.key === "ArrowRight") { sgi = (sgi + 1) % REG.length; paintSg(); } if (e.key === "ArrowLeft") { sgi = (sgi - 1 + REG.length) % REG.length; paintSg(); } });

  /* ---------------------------------------------------------------- start-up */
  function refreshAll() { updateProgress(); if (window.__rzt && window.__rzt.refresh) try { window.__rzt.refresh(); } catch (e) {} }
  applyPrefs(); wirePrefs(); syncRead(); syncLab(); guideMount(); goSlide(0);
  fromHash(true); updateProgress(); fitSlides();
})();
