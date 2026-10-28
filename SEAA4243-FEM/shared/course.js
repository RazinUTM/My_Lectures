/* SEAA 4243 course pages — shared engine (no dependencies).
   Preferences (language, theme) are course-wide; progress is per part. Everything lives in
   this browser's localStorage: it is the student's own record, not a gradebook. */
(function () {
  "use strict";
  var C = window.COURSE || {};
  var PREFS = C.prefs || "seaa4243-prefs", KEY = C.key || "seaa4243-p0-v1";
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

  /* ---------- preferences: language and theme ---------- */
  var P = ld(PREFS, { lang: "en", theme: "auto", ts: 1 });
  function savePrefs() { sv(PREFS, P); }
  function applyLang() {
    document.documentElement.setAttribute("data-lang", P.lang); document.documentElement.setAttribute("lang", P.lang === "ms" ? "ms" : "en");
    $$("[data-setlang]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-setlang") === P.lang)); });
  }
  var ICON = {
    auto: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10" cy="10" r="7"/><path d="M10 3v14" /><path d="M10 3a7 7 0 0 1 0 14z" fill="currentColor" stroke="none"/></svg>',
    light: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="10" r="3.6"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.3 4.3l1.4 1.4M14.3 14.3l1.4 1.4M4.3 15.7l1.4-1.4M14.3 5.7l1.4-1.4"/></svg>',
    dark: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M15.5 12.5A6.5 6.5 0 0 1 7.5 4.5a6.5 6.5 0 1 0 8 8z"/></svg>'
  };
  function applyTheme() {
    var r = document.documentElement; if (P.theme === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", P.theme);
    var b = $("#themebtn"); if (b) { b.innerHTML = ICON[P.theme]; b.setAttribute("aria-label", "Theme: " + P.theme); b.title = "Theme: " + P.theme; }
    window.dispatchEvent(new Event("themechange"));
  }
  /* text size: one scale factor for every font size (CSS var --ts); equations zoom with it */
  var TS = [0.9, 1, 1.12, 1.25, 1.4];
  function applyTs() {
    var t = TS.indexOf(+P.ts) >= 0 ? +P.ts : 1; P.ts = t; document.documentElement.style.setProperty("--ts", String(t));
    $$("[data-ts]").forEach(function (b) { var up = +b.getAttribute("data-ts") > 0, i = TS.indexOf(t);
      b.disabled = up ? i === TS.length - 1 : i === 0;
      b.title = (up ? "Larger text" : "Smaller text") + " · " + Math.round(t * 100) + " %"; });
    window.dispatchEvent(new Event("resize"));
  }
  $$("[data-ts]").forEach(function (b) { b.addEventListener("click", function () { var i = TS.indexOf(+P.ts); if (i < 0) i = 1;
    P.ts = TS[clamp(i + (+b.getAttribute("data-ts")), 0, TS.length - 1)]; savePrefs(); applyTs(); }); });
  applyTs();
  $$("[data-setlang]").forEach(function (b) { b.addEventListener("click", function () { P.lang = b.getAttribute("data-setlang"); savePrefs(); applyLang(); }); });
  var tb = $("#themebtn"); if (tb) tb.addEventListener("click", function () { P.theme = P.theme === "auto" ? "light" : P.theme === "light" ? "dark" : "auto"; savePrefs(); applyTheme(); });
  applyLang(); applyTheme();

  /* ---------- part state ---------- */
  function fresh() {
    return { view: "start", nmode: "full", read: {}, qc: {}, seen: {}, slide: 0,
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
  var VIEWS = $$(".view").map(function (v) { return v.getAttribute("data-view"); }), current = null;
  function show(v, opts) {
    if (!VIEWS.length) return;
    opts = opts || {}; if (VIEWS.indexOf(v) < 0) v = VIEWS[0]; current = v; ST.view = v; save();
    $$(".view").forEach(function (s) { s.hidden = s.getAttribute("data-view") !== v; });
    $$(".tab").forEach(function (t) { t.setAttribute("aria-selected", String(t.getAttribute("data-view") === v)); });
    if (!opts.keepHash) { try { history.replaceState(null, "", "#" + v + (opts.anchor ? "-" + opts.anchor : "")); } catch (e) {} }
    if (opts.anchor) { var a = document.getElementById(opts.anchor); if (a) setTimeout(function () { a.scrollIntoView({ block: "start", behavior: "smooth" }); }, 30); }
    else if (!opts.noscroll) window.scrollTo({ top: 0 });
    if (v === "start") renderStart();
    if (v === "slides") fitSlides();
    if (v === "exercises") renderStats();
    if (v === "lab") armLab();
    if (typeof eqSoon === "function") eqSoon();
    updatePill();
  }
  $$(".tab").forEach(function (t) { t.addEventListener("click", function () { show(t.getAttribute("data-view")); }); });
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
    if (w) { w.textContent = ST.last ? (P.lang === "ms" ? "Terakhir dibuka: " : "Last opened: ") + new Date(ST.last).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }) : ""; }
  }
  function nextStep() {
    for (var i = 0; i < NOTES.length; i++) if (!ST.read[NOTES[i]]) { var h = $("#" + NOTES[i] + " h2"); return { en: "Continue: Notes §" + (i + 1), ms: "Sambung: Nota §" + (i + 1), go: "notes/" + NOTES[i] }; }
    if (NSLIDES && cnt(ST.seen) < NSLIDES) return { en: "Continue: Slides " + (ST.slide + 1) + "/" + NSLIDES, ms: "Sambung: Slides " + (ST.slide + 1) + "/" + NSLIDES, go: "slides" };
    for (var x = 0; x < XS.length; x++) if (!ST.read[XS[x]]) return { en: "Continue: Example " + (x + 1), ms: "Sambung: Contoh " + (x + 1), go: "examples/" + XS[x] };
    for (var j = 0; j < EXIDS.length; j++) if (!ST.ex.chk[EXIDS[j]]) return { en: "Continue: Exercises", ms: "Sambung: Latihan", go: "exercises/" + EXIDS[j] };
    if (MS.length && MS.some(function (m) { return !ST.lab[m.id]; })) return { en: "Continue: Explorer", ms: "Sambung: Explorer", go: "lab" };
    for (var k = 1; k <= NCANDO; k++) if ((ST.cando["c" + k] || 0) < 2) return { en: "Continue: Checklist", ms: "Sambung: Senarai semak", go: "start/cando" };
    return { en: "Everything in this part is done", ms: "Semua dalam bahagian ini selesai", go: "start" };
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

  /* ---------- slides viewer (the deck fragment is fetched when the tab is first shown) ---------- */
  var cv = $("#svcv"), slides = [], frame = $("#svframe"), svInit = false, svLoading = false;
  function fitSlides() { if (!frame || !cv) return; var w = frame.clientWidth; cv.style.transform = "scale(" + (w / 1920) + ")"; loadSlides(); }
  function loadSlides() {
    if (svInit || svLoading || !cv) return; svLoading = true;
    fetch(cv.getAttribute("data-src")).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }).then(function (t) { cv.innerHTML = t; var l = $("#svload"); if (l) l.remove(); initSlides(); })
      .catch(function (e) { svLoading = false; var l = $("#svload"); if (l) l.innerHTML = bi("The slides could not be loaded (" + e.message + "). Use the PDF.", "Slides tidak dapat dimuatkan (" + e.message + "). Guna PDF."); });
  }
  function goSlide(i) {
    if (!slides.length) return; i = clamp(i, 0, slides.length - 1); ST.slide = i; ST.seen["s" + i] = true;
    slides.forEach(function (s, k) { s.classList.toggle("on", k === i); });
    var c = $("#svcount"); if (c) c.textContent = (i + 1) + " / " + slides.length;
    var pr = $("#sprog"); if (pr) pr.firstElementChild.style.width = ((i + 1) / slides.length * 100) + "%";
    $$(".thumbs button").forEach(function (b, k) { b.setAttribute("aria-current", String(k === i)); b.classList.toggle("seen", !!ST.seen["s" + k]); });
    var pv = $("#svprev"), nx = $("#svnext"); if (pv) pv.disabled = i === 0; if (nx) nx.disabled = i === slides.length - 1;
    updateProgress();
  }
  function initSlides() {
    slides = $$(".sl", cv); svInit = true; if (!slides.length) return;
    var th = $("#thumbs");
    if (th) { th.innerHTML = ""; slides.forEach(function (s, k) { var b = el("button", { type: "button" }, '<span class="n">' + (k + 1) + '</span><span>' + (s.getAttribute("data-title") || "") + '</span>'); b.addEventListener("click", function () { goSlide(k); }); th.appendChild(b); }); }
    goSlide(ST.slide || 0);
  }
  if (frame) {
    var pv = $("#svprev"), nx = $("#svnext"), fs = $("#svfull");
    if (pv) pv.addEventListener("click", function () { goSlide(ST.slide - 1); });
    if (nx) nx.addEventListener("click", function () { goSlide(ST.slide + 1); });
    if (fs) fs.addEventListener("click", function () { var st = $("#svstage"); if (!document.fullscreenElement) { if (st.requestFullscreen) st.requestFullscreen(); } else document.exitFullscreen(); });
    document.addEventListener("fullscreenchange", function () { setTimeout(fitSlides, 50); });
    frame.addEventListener("click", function (ev) { if (ev.target.closest("a")) return; var r = frame.getBoundingClientRect(); goSlide(ST.slide + ((ev.clientX - r.left) > r.width / 2 ? 1 : -1)); });
    document.addEventListener("keydown", function (ev) { if (current !== "slides" || ev.target.matches("input,textarea,select")) return;
      if (ev.key === "ArrowRight" || ev.key === "PageDown" || ev.key === " ") { ev.preventDefault(); goSlide(ST.slide + 1); }
      else if (ev.key === "ArrowLeft" || ev.key === "PageUp") { ev.preventDefault(); goSlide(ST.slide - 1); }
      else if (ev.key === "Home") goSlide(0); else if (ev.key === "End") goSlide(slides.length - 1); });
    if (window.ResizeObserver) new ResizeObserver(function () { var w = frame.clientWidth; if (cv) cv.style.transform = "scale(" + (w / 1920) + ")"; }).observe(frame); else window.addEventListener("resize", fitSlides);
    var c0 = $("#svcount"); if (c0) c0.textContent = ((ST.slide || 0) + 1) + " / " + NSLIDES;
  }

  /* ---------- exercises ---------- */
  var L = { check: ["Check", "Semak"], newnum: ["New numbers", "Nombor baharu"], hint: ["Hint", "Petunjuk"], sol: ["Show solution", "Tunjuk penyelesaian"],
    sure: ["Sure", "Yakin"], unsure: ["Not sure", "Tak pasti"], confq: ["Before you check:", "Sebelum semak:"],
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
        var tol = Math.max(fd.atol != null ? fd.atol : 0, (fd.rtol != null ? fd.rtol : 0.01) * Math.abs(ref)); var ok = isFinite(x) && Math.abs(x - ref) <= tol; f[fd.id] = ok; if (!ok) all = false; });
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
    EXIDS.push(id);
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
    var tt = 0; ids.forEach(function (i) { if (ST.ex.t[i]) tt += ST.ex.t[i]; });
    var tgt = C.targetMin || 0;
    var h = '<div class="kv"><div><b>' + done.length + '/' + ids.length + '</b><span>' + bi("answered", "dijawab") + '</span></div>' +
      '<div><b>' + firstOk.length + '/' + done.length + '</b><span>' + bi("right first time", "betul cubaan pertama") + '</span></div>' +
      '<div><b>' + mmss(exElapsed()) + '</b><span>' + bi("on the timer", "pada timer") + (tgt ? ' · ' + bi("target", "sasaran") + ' ' + tgt + ' min' : "") + '</span></div></div>';
    var names = function (arr) { return arr.length ? arr.map(function (i) { return '<a href="#exercises-' + i + '" data-exlink="' + i + '">' + i.toUpperCase() + '</a>'; }).join(", ") : "—"; };
    h += '<div class="tbl"><table class="cal"><tr><th class="l">' + bi("Your confidence", "Keyakinan anda") + '</th><th>' + bi("Right", "Betul") + '</th><th>' + bi("Wrong", "Salah") + '</th></tr>' +
      '<tr><td class="l">' + bi("Sure", "Yakin") + '</td><td>' + cal.sr.length + '</td><td>' + cal.sw.length + '</td></tr>' +
      '<tr><td class="l">' + bi("Not sure", "Tak pasti") + '</td><td>' + cal.ur.length + '</td><td>' + cal.uw.length + '</td></tr></table></div>';
    h += '<p class="muted" style="font-size:13.5px;margin:8px 0 0">' + bi("Sure and wrong: ", "Yakin tetapi salah: ") + names(cal.sw) + '. ' + bi("Not sure and right: ", "Tak pasti tetapi betul: ") + names(cal.ur) + '.</p>';
    box.innerHTML = h;
    $$("[data-exlink]", box).forEach(function (a) { a.addEventListener("click", function (ev) { ev.preventDefault(); show("exercises", { anchor: a.getAttribute("data-exlink") }); }); });
  }
  $$(".q[data-q]").forEach(initChoice);
  $$("article.qx[data-ex]").forEach(function (a) { EXIDS.push(a.getAttribute("data-ex")); });
  Object.keys(EX.specs).forEach(renderEx);
  EX.ready = function () { Object.keys(EX.specs).forEach(renderEx); updateProgress(); };

  /* ---------- lab milestones (postMessage from the lab, or its localStorage record) ---------- */
  function labKey() { return C.lab ? "seaa4243-lab-" + C.lab.id : null; }
  function syncLab() { var k = labKey(); if (!k) return; var rec = ld(k, {}); var changed = false; MS.forEach(function (m) { if (rec[m.id] && !ST.lab[m.id]) { ST.lab[m.id] = true; changed = true; } });
    MS.forEach(function (m) { var t = $('.tk[data-ms="' + m.id + '"]'); if (t) t.classList.toggle("done", !!ST.lab[m.id]); }); if (changed) { save(); } updateProgress(); }
  window.addEventListener("message", function (ev) { var d = ev.data; if (!d || d.type !== "seaa4243-lab" || !C.lab || d.lab !== C.lab.id) return; if (!ST.lab[d.id]) { ST.lab[d.id] = true; save(); } syncLab(); });
  window.addEventListener("focus", syncLab); document.addEventListener("visibilitychange", function () { if (!document.hidden) syncLab(); });
  /* the iframe is lazy and sits in a hidden tab, so the "did not load" note is armed only when the
     Explorer tab is first shown, and removed if the Explorer loads after all */
  var lf = $("#labframe"), labLoaded = false, labArmed = false, labNote = null;
  if (lf) lf.addEventListener("load", function () { labLoaded = true; if (labNote) { labNote.remove(); labNote = null; } });
  function armLab() { if (!lf || labArmed) return; labArmed = true;
    setTimeout(function () { if (!labLoaded && !labNote) { labNote = el("p", { class: "note" }, bi("The Explorer did not load inside this page. Open it in its own tab with the link below; tasks done there are still recorded here.", "Explorer tidak dimuatkan di dalam halaman ini. Buka dalam tab sendiri melalui pautan di bawah; tugasan yang selesai di situ tetap direkod di sini.")); lf.parentNode.insertBefore(labNote, lf); } }, 8000); }
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
  if (rs) rs.addEventListener("click", function () { if (!armed) { armed = true; tx(rs, "Tap again to erase this part’s progress", "Tekan sekali lagi untuk memadam kemajuan bahagian ini"); setTimeout(function () { armed = false; tx(rs, "Reset this part’s progress", "Set semula kemajuan bahagian ini"); }, 4000); return; }
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
      if (FRAMED) { blocked(); return; }      /* a host page that frames this one without the capability blocks page downloads */
      anchorSave(blob, name, href, say);
    }).catch(function (e) { say("Could not get " + name + " (" + e.message + ").", "Tidak dapat mendapatkan " + name + " (" + e.message + ")."); })
      .then(function () { if (btn) btn.disabled = false; });
    function blocked() {
      var home = document.querySelector(".homelink") ? ' <a href="../index.html">⌂ Course home</a>' : "";
      var homeMs = document.querySelector(".homelink") ? ' <a href="../index.html">⌂ Laman kursus</a>' : "";
      var dir = href ? ' <a href="' + href + '" target="_blank" rel="noopener">' : "";
      say("This view does not allow downloads." + (home ? " Download from" + home + "," : "") + (href ? dir + " open the file directly</a>," : "") + " or use “Show the code” and Copy where offered.",
          "Paparan ini tidak membenarkan muat turun." + (homeMs ? " Muat turun dari" + homeMs + "," : "") + (href ? dir + " buka fail terus</a>," : "") + " atau guna “Tunjuk kod” dan Salin jika ada.");
    }
  }
  /* zip (store method) built in the browser from files the site serves as text */
  var CRC = (function () { var t = new Uint32Array(256); for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  function crc32(u) { var c = 0xFFFFFFFF; for (var i = 0; i < u.length; i++) c = CRC[(c ^ u[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  function makeZip(entries) {
    var enc = new TextEncoder(), parts = [], central = [], off = 0, DATE = ((2026 - 1980) << 9) | (10 << 5) | 1, TIME = 0;
    function hdr(n) { return new DataView(new ArrayBuffer(n)); }
    entries.forEach(function (e) {
      var name = enc.encode(e.name), data = e.data, crc = crc32(data), h = hdr(30);
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0, true); h.setUint16(8, 0, true); h.setUint16(10, TIME, true); h.setUint16(12, DATE, true);
      h.setUint32(14, crc, true); h.setUint32(18, data.length, true); h.setUint32(22, data.length, true); h.setUint16(26, name.length, true); h.setUint16(28, 0, true);
      parts.push(h.buffer, name, data);
      var c = hdr(46); c.setUint32(0, 0x02014b50, true); c.setUint16(4, 0x0314, true); c.setUint16(6, 20, true); c.setUint16(8, 0, true); c.setUint16(10, 0, true);
      c.setUint16(12, TIME, true); c.setUint16(14, DATE, true); c.setUint32(16, crc, true); c.setUint32(20, data.length, true); c.setUint32(24, data.length, true);
      c.setUint16(28, name.length, true); c.setUint32(38, 0o100644 << 16 >>> 0, true); c.setUint32(42, off, true);
      central.push(c.buffer, name); off += 30 + name.length + data.length;
    });
    var csize = central.reduce(function (s, b) { return s + (b.byteLength); }, 0), z = hdr(22);
    z.setUint32(0, 0x06054b50, true); z.setUint16(8, entries.length, true); z.setUint16(10, entries.length, true); z.setUint32(12, csize, true); z.setUint32(16, off, true);
    return new Blob(parts.concat(central, [z.buffer]), { type: "application/zip" });
  }
  function getBytes(u) { return fetch(u).then(function (r) { if (!r.ok) throw new Error(u.split("/").pop() + ": HTTP " + r.status); return r.arrayBuffer(); }).then(function (b) { return new Uint8Array(b); }); }
  $$("[data-zip]").forEach(function (b) { b.addEventListener("click", function () {
    var box = b.closest(".recbar, .cardacts") || b.parentNode, m = box ? $(".savemsg", box) : null;
    var stem = b.getAttribute("data-zip"), base = b.getAttribute("data-base") || "", files = b.getAttribute("data-files").split(",");
    var names = ["README.txt"].concat(files), urls = [base + b.getAttribute("data-readme")].concat(files.map(function (f) { return base + f; }));
    saveFile(function () { return Promise.all(urls.map(getBytes)).then(function (arr) { return makeZip(arr.map(function (d, i) { return { name: stem + "/" + names[i], data: d }; })); }); }, stem + ".zip", m, b);
  }); });
  dlCap();
  $$("[data-save]").forEach(function (b) { b.addEventListener("click", function () {
    var box = b.closest(".recbar, .cardacts, .slidebar") || b.parentNode, m = box ? $(".savemsg", box) : null;
    saveFile(b.getAttribute("data-save"), b.getAttribute("data-name"), m, b); }); });
  /* copy a code block (clipboard writes are allowed inside the click) */
  $$("[data-copy]").forEach(function (b) { b.addEventListener("click", function () {
    var pre = document.getElementById(b.getAttribute("data-copy")), m = b.parentNode.querySelector(".copymsg"), t = pre ? pre.textContent : "";
    function ok() { if (m) m.innerHTML = bi("Copied.", "Disalin."); }
    function manual() { try { var r = document.createRange(); r.selectNodeContents(pre); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); if (document.execCommand && document.execCommand("copy")) { ok(); return; } } catch (e) {}
      if (m) m.innerHTML = bi("Selected: press Ctrl+C (⌘C) to copy.", "Dipilih: tekan Ctrl+C (⌘C) untuk menyalin."); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(ok, manual); else manual(); }); });

  /* ---------- wide equations scroll sideways on a narrow screen: fade the edge while there is more ---------- */
  function eqHints() { $$(".eqwrap").forEach(function (w) { var more = w.scrollWidth > w.clientWidth + 2 && w.scrollLeft + w.clientWidth < w.scrollWidth - 2; w.classList.toggle("more", more); }); }
  var eqT = null; function eqSoon() { clearTimeout(eqT); eqT = setTimeout(eqHints, 120); }
  window.addEventListener("resize", eqSoon); document.addEventListener("scroll", function (ev) { if (ev.target && ev.target.classList && ev.target.classList.contains("eqwrap")) eqSoon(); }, true);
  document.addEventListener("toggle", eqSoon, true);

  /* ---------- run Python in the browser: Pyodide (CPython compiled to WebAssembly) in a Web Worker ----------
     A worker keeps the page responsive and lets Stop end a runaway script. Pyodide is loaded only where the
     page comes from GitHub Pages or a local server; elsewhere (a preview) the panel points to the website. */
  var PYURL = window.SEAA_PYURL || "https://cdn.jsdelivr.net/pyodide/v0.29.5/full/";
  var PYHOST = !!window.SEAA_PYURL || /(^|\.)github\.io$|^localhost$|^127\.0\.0\.1$/.test(location.hostname);
  var PYPRE = [
    "import os, sys, io, base64, warnings",
    "os.environ['MPLBACKEND'] = 'Agg'",
    "warnings.filterwarnings('ignore', message='.*non-interactive.*')",
    "os.makedirs('/home/pyodide/run', exist_ok=True)",
    "os.chdir('/home/pyodide/run')",
    "sys.path.insert(0, '/home/pyodide/run')",
    "_SEAA_NP = None",
    "_SEAA_IMG = {'png': 'image/png', 'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg'}",
    "def _seaa_run(code):",
    "    global _SEAA_NP",
    "    for f in os.listdir('.'):",
    "        if f.rsplit('.', 1)[-1].lower() in _SEAA_IMG:",
    "            os.remove(f)",
    "    for m in [m for m in sys.modules if m.startswith('fe_')]:",
    "        del sys.modules[m]",
    "    try:",
    "        import numpy",
    "        if _SEAA_NP is None:",
    "            _SEAA_NP = numpy.get_printoptions()",
    "        numpy.set_printoptions(**_SEAA_NP)",
    "    except ImportError:",
    "        pass",
    "    ok = True",
    "    try:",
    "        exec(compile(code, 'script', 'exec'), {'__name__': '__main__'})",
    "    except SystemExit:",
    "        pass",
    "    except BaseException:",
    "        import traceback",
    "        et, ev, tb = sys.exc_info()",
    "        traceback.print_exception(et, ev, tb.tb_next)",
    "        ok = False",
    "    figs = []",
    "    plt = sys.modules.get('matplotlib.pyplot')",
    "    if plt is not None:",
    "        for n in plt.get_fignums():",
    "            b = io.BytesIO()",
    "            plt.figure(n).savefig(b, format='png', dpi=110, bbox_inches='tight')",
    "            figs.append(['Figure %d' % n, 'image/png', base64.b64encode(b.getvalue()).decode()])",
    "        plt.close('all')",
    "    for f in sorted(os.listdir('.')):",
    "        ext = f.rsplit('.', 1)[-1].lower()",
    "        if ext in _SEAA_IMG:",
    "            with open(f, 'rb') as h:",
    "                figs.append([f, _SEAA_IMG[ext], base64.b64encode(h.read()).decode()])",
    "    sys.stdout.flush()",
    "    sys.stderr.flush()",
    "    return ok, figs"
  ].join("\n");
  var PYW = [
    "var py = null, boot = null, PRE = " + JSON.stringify(PYPRE) + ";",
    "function post(m) { self.postMessage(m); }",
    "async function start(url) {",
    "  importScripts(url + 'pyodide.js');",
    "  py = await loadPyodide({ indexURL: url });",
    "  py.setStdout({ batched: function (s) { post({ t: 'out', s: s + '\\n' }); } });",
    "  py.setStderr({ batched: function (s) { post({ t: 'err', s: s + '\\n' }); } });",
    "  py.runPython(PRE);",
    "}",
    "self.onmessage = async function (e) {",
    "  var m = e.data;",
    "  try { if (!boot) boot = start(m.url); await boot; }",
    "  catch (err) { post({ t: 'fail', s: String(err && err.message || err) }); return; }",
    "  try {",
    "    Object.keys(m.files).forEach(function (f) { py.FS.writeFile('/home/pyodide/run/' + f, m.files[f]); });",
    "    var said = false, cb = { messageCallback: function (s) { if (!said && /^Loading/.test(s)) { said = true; post({ t: 'status', k: 'pkgs' }); } }, errorCallback: function () {} };",
    "    var need = ['numpy']; if (/plot|matplotlib|runpy/.test(m.code)) need.push('matplotlib');",
    "    await py.loadPackage(need, cb);",
    "    await py.loadPackagesFromImports(m.code, cb);",
    "    post({ t: 'status', k: 'run' });",
    "    var t0 = performance.now(), r = py.globals.get('_seaa_run')(m.code), a = r.toJs(); r.destroy();",
    "    post({ t: 'done', ok: a[0], figs: a[1], ms: performance.now() - t0 });",
    "  } catch (err) { post({ t: 'done', ok: false, figs: [], err: String(err && err.message || err), ms: 0 }); }",
    "};"
  ].join("\n");
  var pyEver = false;   /* Python has started once on this page: later starts come from the browser cache */
  function pyPanel(card) {
    var srcs = JSON.parse($(".pysrc", card).textContent), ed = $(".pyedit", card), out = $(".pyout", card), figs = $(".pyfigs", card), stat = $(".pystat", card);
    var runB = $("[data-pyrun]", card), stopB = $("[data-pystop]", card), resetB = $("[data-pyreset]", card), segs = $$("[data-py]", card);
    var key = "seaa4243-py-" + card.getAttribute("data-part"), edits = ld(key, {}), cur = 0, files = null, W = null, busy = false, phase = "", tick = null, t0 = 0, nout = 0, MAXOUT = 200000;
    if (!edits || typeof edits !== "object") edits = {};
    function say(en, ms, cls) { stat.innerHTML = bi(en, ms); stat.className = "pystat" + (cls ? " " + cls : ""); }
    function fit() { ed.rows = clamp(ed.value.split("\n").length + 1, 6, 28); }
    function pick(i) {
      cur = i; ed.value = edits[i] != null ? edits[i] : srcs[i]; fit(); resetB.disabled = edits[i] == null;
      segs.forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-py") === i)); });
    }
    segs.forEach(function (b) { b.addEventListener("click", function () { pick(+b.getAttribute("data-py")); }); });
    ed.addEventListener("input", function () { if (ed.value === srcs[cur]) delete edits[cur]; else edits[cur] = ed.value; sv(key, edits); resetB.disabled = edits[cur] == null; fit(); });
    ed.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); run(); return; }
      if (ev.key === "Enter" && !ev.shiftKey && !ev.altKey && !ev.isComposing) {   /* keep the indentation of the line above; one level more after a colon */
        var s = ed.selectionStart, v = ed.value, line = v.slice(v.lastIndexOf("\n", s - 1) + 1, s), ind = /^[ \t]*/.exec(line)[0];
        if (/:\s*(#.*)?$/.test(line)) ind += "    ";
        if (!ind) return;
        ev.preventDefault();
        var done = false; try { done = document.execCommand && document.execCommand("insertText", false, "\n" + ind); } catch (e) {}
        if (!done) { ed.setRangeText("\n" + ind, s, ed.selectionEnd, "end"); ed.dispatchEvent(new Event("input")); }
      }
    });
    resetB.addEventListener("click", function () { delete edits[cur]; sv(key, edits); pick(cur); ed.focus(); });
    function show(t, err) {
      if (nout >= MAXOUT) return;
      out.hidden = false; var sp = document.createElement("span"); if (err) sp.className = "e"; sp.textContent = t; out.appendChild(sp); nout += t.length;
      if (nout >= MAXOUT) out.appendChild(document.createTextNode("\n… output cut at 200 000 characters\n"));
      out.scrollTop = out.scrollHeight;
    }
    function getFiles() {
      if (files) return Promise.resolve(files);
      var base = card.getAttribute("data-base"), names = card.getAttribute("data-files").split(",");
      return Promise.all(names.map(function (n) { return fetch(base + n).then(function (r) { if (!r.ok) throw new Error(n + ": HTTP " + r.status); return r.text(); }); }))
        .then(function (arr) { files = {}; names.forEach(function (n, i) { files[n] = arr[i]; }); return files; });
    }
    function secs() { return Math.round((Date.now() - t0) / 1000) + " s"; }
    function status() {
      if (phase === "boot") { if (pyEver) say("Starting Python… " + secs(), "Memulakan Python… " + secs()); else say("Loading Python (first time: about 9 MB)… " + secs(), "Memuatkan Python (kali pertama: lebih kurang 9 MB)… " + secs()); }
      else if (phase === "pkgs") say("Loading numpy / matplotlib… " + secs(), "Memuatkan numpy / matplotlib… " + secs());
      else if (phase === "run") say("Running… " + secs(), "Sedang berjalan… " + secs());
    }
    function finish() { busy = false; phase = ""; clearInterval(tick); runB.disabled = false; stopB.hidden = true; }
    function failed(why) {
      finish(); if (W) W.terminate(); W = null;
      say("Python could not be loaded here (" + why + "). Offline, or a network that blocks cdn.jsdelivr.net? Download the code above and run it on your computer.",
          "Python tidak dapat dimuatkan di sini (" + why + "). Luar talian, atau rangkaian menyekat cdn.jsdelivr.net? Muat turun kod di atas dan jalankan di komputer anda.", "pybad");
    }
    function worker() {
      var w = new Worker(URL.createObjectURL(new Blob([PYW], { type: "text/javascript" })));
      w.onmessage = function (e) {
        var m = e.data;
        if (m.t === "out") show(m.s, false);
        else if (m.t === "err") { if (!/font cache/i.test(m.s)) show(m.s, true); }
        else if (m.t === "status") { pyEver = true; phase = m.k; status(); }
        else if (m.t === "fail") failed(m.s);
        else if (m.t === "done") {
          finish(); if (m.err) show(m.err + "\n", true);
          (m.figs || []).forEach(function (f) { var fig = el("figure"), cap = el("figcaption"); fig.appendChild(el("img", { src: "data:" + f[1] + ";base64," + f[2], alt: f[0] })); cap.textContent = f[0]; fig.appendChild(cap); figs.appendChild(fig); });
          var s = (m.ms / 1000).toFixed(m.ms < 10000 ? 1 : 0), quiet = !nout && !(m.figs || []).length;
          if (m.ok) say("Done in " + s + " s." + (quiet ? " The script printed nothing." : ""), "Siap dalam " + s + " s." + (quiet ? " Skrip tidak mencetak apa-apa." : ""), "pyok");
          else say("Stopped at an error: the last lines below give the line of the script and the reason.", "Terhenti kerana ralat: baris terakhir di bawah memberi baris skrip dan sebabnya.", "pybad");
        }
      };
      w.onerror = function (e) { if (e && e.preventDefault) e.preventDefault(); failed((e && e.message) || "worker error"); };
      return w;
    }
    function run() {
      if (busy || !PYHOST) return;
      busy = true; runB.disabled = true; stopB.hidden = false; out.textContent = ""; out.hidden = true; nout = 0; figs.innerHTML = "";
      t0 = Date.now(); phase = "boot"; status(); tick = setInterval(status, 1000);
      getFiles().then(function (f) {
        if (!busy) return;
        try { if (!W) W = worker(); W.postMessage({ url: PYURL, code: ed.value, files: f }); } catch (e) { failed(e.message); }
      }, function (e) { finish(); say("Could not fetch the course code (" + e.message + ").", "Tidak dapat mendapatkan kod kursus (" + e.message + ").", "pybad"); });
    }
    runB.addEventListener("click", run);
    stopB.addEventListener("click", function () {
      if (W) W.terminate(); W = null; finish();
      say("Stopped. Python starts again on the next run (a few seconds).", "Dihentikan. Python dimulakan semula pada larian seterusnya (beberapa saat).");
    });
    pick(0);
    if (!PYHOST) {
      runB.disabled = true; var a = ' <a href="' + card.getAttribute("data-pages") + '" target="_blank" rel="noopener">';
      say("Running needs the course website:" + a + "open this part there</a>. Here you can read, edit and copy the scripts.",
          "Larian memerlukan laman web kursus:" + a + "buka bahagian ini di sana</a>. Di sini anda boleh membaca, mengubah dan menyalin skrip.");
    }
  }
  $$(".pyrun").forEach(pyPanel);

  /* ---------- go ---------- */
  syncRead(); applyNmode(); syncLab(); if (VIEWS.length) { updateProgress(); fromHash(); }
  window.COURSE_API = { show: show, state: ST, save: save, fmt: fmt, bi: bi, saveFile: saveFile, makeZip: makeZip };
})();
