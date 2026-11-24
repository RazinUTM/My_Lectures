/* Annotation toolbar: write on the screen while teaching. T&L app template, version 1.2 (24 Nov 2026).
   Source of record: My_Lectures/SEAA4243-FEM/shared/annotate.js. The other courses carry a copy of this file;
   change it here first, then copy it.

   One self-contained file with no dependencies. It adds its own styles, a small floating toolbar (bottom
   right, draggable) and, while annotation is on, a transparent canvas over the page. It needs nothing from
   the page's engine and changes nothing in it; the colours come from the page's CSS variables when they
   exist (--panel, --fg, --line, --accent), so the toolbar follows the light and dark themes.

   Annotation off: the canvas is hidden and the page works as usual; only the pencil button shows.
   Annotation on:  the canvas takes every mouse, touch and pen input, so the page cannot be clicked or
                   scrolled (wheel, touch and keys); Esc or the pencil button turns it off.

   The ink is kept in memory while the page is open and is never stored or sent. A stroke is recorded in
   page coordinates, so it stays on what it was written on when the page has been scrolled in between, and
   each view of a part page (and each slide, and the full-screen slide viewer) keeps its own ink.
   The eraser works by object: touching a line removes the whole line. "Clear all" clears the ink of the view
   on screen. Ctrl/Cmd+Z takes back the last thing done (a line, an erasure, a Clear all).

   The second slider puts a blank page behind the ink, from 0% (the page shows through) to 100% (a clean page
   to write on): white on the light theme, dark on the dark theme. It starts at 0% each time the page is opened.

   Only the pen (slot, size) and the toolbar's place are remembered, in localStorage under "rz-annotate".

   Two highlighters, magenta and cyan, are see-through and have one thickness, for marking what matters on the
   page; the thickness slider is for the pens.

   1.1: a green pen; the eraser removes whole lines (it rubbed out pixels in 1.0); the blank page behind the ink;
        Ctrl/Cmd+Z also takes back an erasure and a Clear all.
   1.2: the magenta and cyan highlighters.

   SPDX-License-Identifier: MIT
   Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia */
(function () {
  "use strict";
  var D = document, H = D.documentElement;
  if (window.RZAnnotate || !D.body || !window.PointerEvent) return;
  var cv = D.createElement("canvas"), ctx = cv.getContext && cv.getContext("2d");
  if (!ctx) return;

  var STORE = "rz-annotate";
  var INK = { red: "#e0202c", blue: "#1463d6", green: "#12964a", yellow: "#f6c400", magenta: "#ff1fc0", cyan: "#00c2ee" };   /* the slot "ink" follows the theme: black or white */
  var SLOTS = ["red", "blue", "green", "ink", "yellow", "magenta", "cyan"];
  var HL = { magenta: 1, cyan: 1 }, HL_W = 20, HL_A = 0.4;               /* the highlighters: one thickness, see-through */
  var on = false, tool = "pen", slot = "red", size = 4, pos = null;      /* pos: {r, b} from the right and bottom edges, null = the default corner */
  var layers = {}, hists = {}, layer = [], hist = [], cur = null, penAt = 0, dpr = 1, dragEnd = 0;
  var cover = 0;                                       /* the blank page behind the ink, 0 to 100 %; not remembered */

  try { var saved = JSON.parse(localStorage.getItem(STORE) || "null") || {};
    if (SLOTS.indexOf(saved.c) >= 0) slot = saved.c;
    if (saved.w >= 1 && saved.w <= 24) size = Math.round(saved.w);
    if (isFinite(saved.r) && isFinite(saved.b) && saved.r !== null && saved.b !== null) pos = { r: +saved.r, b: +saved.b };
  } catch (e) {}
  function save() { try { localStorage.setItem(STORE, JSON.stringify({ c: slot, w: size, r: pos ? Math.round(pos.r) : null, b: pos ? Math.round(pos.b) : null })); } catch (e) {} }

  function isMs() { return H.getAttribute("data-lang") === "ms" || /^ms/i.test(H.getAttribute("lang") || ""); }
  function L(en, ms) { return isMs() ? ms : en; }
  function isDark() { var t = H.getAttribute("data-theme"); return t ? t === "dark" : !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches); }
  function inkOf(s) { return INK[s] || (isDark() ? "#ffffff" : "#111111"); }
  function rgba(hex, a) { var n = parseInt(hex.slice(1), 16); return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")"; }
  function fsEl() { return D.fullscreenElement || D.webkitFullscreenElement || null; }

  /* ---------- styles and markup ---------- */
  var css = D.createElement("style");
  css.textContent =
    ".rzan-cv{position:fixed;left:0;top:0;width:100%;height:100%;z-index:2147483000;touch-action:none;cursor:crosshair;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}" +
    ".rzan-cv[data-tool=eraser]{cursor:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='12' r='9' fill='%23ffffff' fill-opacity='.45' stroke='%23444444' stroke-width='1.5'/%3E%3C/svg%3E\") 12 12,cell}" +
    ".rzan-cv[hidden],.rzan-tools[hidden]{display:none}" +
    ".rzan-bar{position:fixed;z-index:2147483001;display:flex;flex-direction:row-reverse;flex-wrap:wrap-reverse;align-items:center;gap:5px;box-sizing:border-box;max-width:calc(100vw - 28px);padding:4px;" +
      "border:1px solid var(--line,#cfcfcf);border-radius:12px;background:var(--panel,Canvas);color:var(--fg,CanvasText);box-shadow:0 4px 14px rgba(0,0,0,.2);" +
      "font:600 12px/1 var(--font-ui,system-ui,sans-serif);touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-tap-highlight-color:transparent}" +
    ".rzan-tools{display:flex;flex-wrap:wrap;justify-content:flex-end;align-items:center;gap:5px}" +
    ".rzan-bar button{font:inherit;margin:0;-webkit-appearance:none;appearance:none}" +
    ".rzan-b{display:inline-grid;place-items:center;width:36px;height:36px;padding:0;border:1px solid var(--line,#cfcfcf);border-radius:8px;background:var(--panel2,var(--panel,Canvas));color:inherit;cursor:pointer}" +
    ".rzan-b:hover{border-color:var(--accent,#830f3e);color:var(--accent,#830f3e)}" +
    ".rzan-b[aria-pressed=true],.rzan-b[aria-pressed=true]:hover{background:var(--accent,#830f3e);border-color:var(--accent,#830f3e);color:var(--accent-fg,#fff)}" +
    ".rzan-b svg,.rzan-grip svg{display:block;width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;pointer-events:none}" +
    ".rzan-grip{display:inline-grid;place-items:center;width:14px;height:36px;color:var(--muted,GrayText);cursor:grab}.rzan-grip svg{width:14px;fill:currentColor;stroke:none}" +
    ".rzan-c{display:inline-grid;place-items:center;width:28px;height:36px;padding:0;border:0;background:none;cursor:pointer}" +
    ".rzan-c i{display:block;width:20px;height:20px;border-radius:50%;box-shadow:0 0 0 1px rgba(128,128,128,.6);pointer-events:none}" +
    ".rzan-c[aria-pressed=true] i{box-shadow:0 0 0 2px var(--panel,Canvas),0 0 0 4px var(--accent,#830f3e)}" +
    ".rzan-c[data-hl] i{width:22px;height:13px;border-radius:3px}" +
    ".rzan-size input:disabled{opacity:.4;cursor:default}" +
    ".rzan-size{display:inline-flex;align-items:center;gap:4px;height:36px;padding:0 2px}" +
    ".rzan-dot{display:inline-grid;place-items:center;width:24px;height:24px}.rzan-dot i{display:block;border-radius:50%;box-shadow:0 0 0 1px rgba(128,128,128,.45)}" +
    ".rzan-size input{width:68px;height:28px;margin:0;padding:0;accent-color:var(--accent,#830f3e);cursor:pointer;touch-action:none}" +
    ".rzan-pg{display:inline-grid;place-items:center;width:24px;height:24px}.rzan-pg i{display:block;width:14px;height:18px;border-radius:2px;box-shadow:0 0 0 1.5px currentColor}" +
    ".rzan-bar button:focus-visible,.rzan-bar input:focus-visible{outline:2px solid var(--accent,#830f3e);outline-offset:2px}" +
    "@media print{.rzan{display:none!important}}";
  D.head.appendChild(css);

  var SVG = '<svg viewBox="0 0 24 24" aria-hidden="true">';
  var IC = {
    pen: SVG + '<path d="M4 20l1.2-4.6L16.6 4a2 2 0 0 1 2.9 0l.5.5a2 2 0 0 1 0 2.9L8.6 18.8 4 20z"/><path d="M14.6 6l3.4 3.4"/></svg>',
    eraser: SVG + '<path d="M8.6 19.5l-4.7-4.7a1.6 1.6 0 0 1 0-2.3l8.6-8.6a1.6 1.6 0 0 1 2.3 0l5.3 5.3a1.6 1.6 0 0 1 0 2.3l-8 8"/><path d="M5.5 19.5H20"/><path d="M8.2 8.8l7 7"/></svg>',
    clear: SVG + '<path d="M4 7h16"/><path d="M9.5 7V4.5h5V7"/><path d="M6.5 7l.9 12.5h9.2L17.5 7"/><path d="M10 10.8v5.4M14 10.8v5.4"/></svg>',
    grip: SVG + '<circle cx="8" cy="5" r="1.7"/><circle cx="16" cy="5" r="1.7"/><circle cx="8" cy="12" r="1.7"/><circle cx="16" cy="12" r="1.7"/><circle cx="8" cy="19" r="1.7"/><circle cx="16" cy="19" r="1.7"/></svg>'
  };
  function el(tag, cls, html) { var x = D.createElement(tag); if (cls) x.className = cls; if (html) x.innerHTML = html; return x; }
  function btn(cls, act, html) { var b = el("button", cls, html); b.type = "button"; b.setAttribute("data-act", act); return b; }

  var root = el("div", "rzan"), bar = el("div", "rzan-bar"), tools = el("div", "rzan-tools");
  cv.className = "rzan-cv"; cv.hidden = true; cv.setAttribute("aria-hidden", "true");
  bar.setAttribute("role", "toolbar"); tools.hidden = true;
  var grip = el("span", "rzan-grip", IC.grip), swatch = {};
  tools.appendChild(grip);
  SLOTS.forEach(function (s) { var b = btn("rzan-c", "colour", "<i></i>"); b.setAttribute("data-c", s); if (HL[s]) b.setAttribute("data-hl", "1"); swatch[s] = b; tools.appendChild(b); });
  var sizeBox = el("span", "rzan-size", '<span class="rzan-dot" aria-hidden="true"><i></i></span>'), dot = sizeBox.querySelector("i");
  var range = el("input"); range.type = "range"; range.min = "1"; range.max = "24"; range.step = "1"; range.value = String(size); sizeBox.appendChild(range);
  var bErase = btn("rzan-b", "eraser", IC.eraser), bClear = btn("rzan-b", "clear", IC.clear), bToggle = btn("rzan-b rzan-toggle", "toggle", IC.pen);
  var coverBox = el("span", "rzan-size", '<span class="rzan-pg" aria-hidden="true"><i></i></span>'), page = coverBox.querySelector("i");
  var veil = el("input"); veil.type = "range"; veil.min = "0"; veil.max = "100"; veil.step = "5"; veil.value = "0"; coverBox.appendChild(veil);
  tools.appendChild(sizeBox); tools.appendChild(bErase); tools.appendChild(bClear); tools.appendChild(coverBox);
  bar.appendChild(bToggle); bar.appendChild(tools);          /* the pencil first in the tab order, last on screen (row-reverse): the bar grows left and up from it */
  root.appendChild(cv); root.appendChild(bar);

  function tip(x, t) { x.title = t; x.setAttribute("aria-label", t); }
  function sync() {                                   /* labels, pressed states, swatches: language, theme and tool */
    var names = { red: L("Red pen", "Pen merah"), blue: L("Blue pen", "Pen biru"), green: L("Green pen", "Pen hijau"), yellow: L("Yellow pen", "Pen kuning"),
      magenta: L("Magenta highlighter", "Penyerlah magenta"), cyan: L("Cyan highlighter", "Penyerlah sian"),
      ink: isDark() ? L("White pen", "Pen putih") : L("Black pen", "Pen hitam") };
    bar.setAttribute("aria-label", L("Annotation tools", "Alat anotasi"));
    tip(bToggle, on ? L("Stop writing on the screen (Esc)", "Henti menulis pada skrin (Esc)") : L("Write on the screen", "Tulis pada skrin"));
    bToggle.setAttribute("aria-pressed", String(on));
    SLOTS.forEach(function (s) { var b = swatch[s]; b.firstChild.style.background = HL[s] ? rgba(INK[s], 0.6) : inkOf(s); tip(b, names[s]); b.setAttribute("aria-pressed", String(tool === "pen" && slot === s)); });
    tip(bErase, L("Eraser: touch a line to remove the whole line", "Pemadam: sentuh satu garisan untuk memadam seluruh garisan itu")); bErase.setAttribute("aria-pressed", String(tool === "eraser"));
    cv.setAttribute("data-tool", tool);
    tip(bClear, L("Clear all the writing on this screen", "Padam semua tulisan pada skrin ini"));
    var hl = tool === "pen" && !!HL[slot];
    range.disabled = hl;                               /* the highlighters have one thickness */
    tip(range, hl ? L("Line thickness: fixed for the highlighters", "Ketebalan garisan: tetap bagi penyerlah") : L("Line thickness", "Ketebalan garisan"));
    grip.title = L("Drag to move the toolbar", "Seret untuk mengalih bar alat");
    var d = Math.max(3, Math.min(22, hl ? HL_W : size)); dot.style.width = dot.style.height = d + "px";
    dot.style.background = tool === "eraser" ? "transparent" : hl ? rgba(INK[slot], 0.6) : inkOf(slot);
    /* the blank page behind the ink: the canvas's own background, so the ink and the eraser never touch it */
    var rgb = isDark() ? "22,24,28" : "255,255,255", paper = cover ? "rgba(" + rgb + "," + cover / 100 + ")" : "";
    cv.style.backgroundColor = paper; page.style.background = paper;
    tip(veil, L("Blank page behind the writing (0% shows the page, 100% covers it)", "Halaman kosong di belakang tulisan (0% menunjukkan halaman, 100% menutupnya)") + ": " + cover + "%");
    veil.setAttribute("aria-valuetext", cover + "%");
  }

  /* ---------- where the toolbar sits ---------- */
  function shown(x) { return !!x && !x.hidden && x.getClientRects().length > 0; }
  function place() {
    var vw = H.clientWidth || innerWidth, vh = H.clientHeight || innerHeight, r, b;
    if (pos) { r = pos.r; b = pos.b; }
    else {                                             /* the default corner, above whatever already sits there: the Dr RJ button, the exercise timer */
      r = 14; b = 14;
      if (!fsEl()) [".rjfab", ".tpill"].forEach(function (q) { var x = D.querySelector(q); if (shown(x)) b = Math.max(b, vh - x.getBoundingClientRect().top + 10); });
    }
    var w = bar.offsetWidth, h = bar.offsetHeight;
    r = Math.max(4, Math.min(r, vw - w - 4)); b = Math.max(4, Math.min(b, vh - h - 4));
    bar.style.right = "calc(" + r + "px + env(safe-area-inset-right, 0px))"; bar.style.bottom = "calc(" + b + "px + env(safe-area-inset-bottom, 0px))";
  }

  /* ---------- the ink ---------- */
  function ctxKey() {                                  /* which screen the ink belongs to: the view, the slide, full screen or not */
    var v = D.querySelector(".view:not([hidden])"), k = "";
    if (v) { k = v.getAttribute("data-view") || v.id || ""; var s = v.querySelector(".sl.on, .slide.on"); if (s) k += "/" + Array.prototype.indexOf.call(s.parentNode.children, s); }
    return k + (fsEl() ? "|fs" : "");
  }
  function useLayer() { var k = ctxKey(); layer = layers[k] || (layers[k] = []); hist = hists[k] || (hists[k] = []); }
  function did(act) { hist.push(act); if (hist.length > 300) hist.shift(); }                  /* what Ctrl/Cmd+Z takes back, newest last */
  function origin() { return fsEl() ? { x: 0, y: 0 } : { x: window.pageXOffset || 0, y: window.pageYOffset || 0 }; }
  function fit() {
    var rc = cv.getBoundingClientRect(); dpr = Math.min(3, window.devicePixelRatio || 1);
    var w = Math.max(1, Math.round(rc.width * dpr)), h = Math.max(1, Math.round(rc.height * dpr));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
  }
  function style(s) { ctx.globalAlpha = s.a || 1; ctx.strokeStyle = ctx.fillStyle = s.c; ctx.lineWidth = s.w; ctx.lineCap = ctx.lineJoin = "round"; }
  function paint(s) {                                  /* a whole stroke, smoothed through the midpoints */
    var p = s.p, n = p.length / 2, i; style(s); ctx.beginPath();
    if (n === 1) { ctx.arc(p[0], p[1], s.w / 2, 0, 6.2832); ctx.fill(); return; }
    ctx.moveTo(p[0], p[1]);
    for (i = 1; i < n - 1; i++) ctx.quadraticCurveTo(p[2 * i], p[2 * i + 1], (p[2 * i] + p[2 * i + 2]) / 2, (p[2 * i + 1] + p[2 * i + 3]) / 2);
    ctx.lineTo(p[2 * n - 2], p[2 * n - 1]); ctx.stroke();
  }
  function redraw() {
    if (!on) return; var o = origin();
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.setTransform(dpr, 0, 0, dpr, -o.x * dpr, -o.y * dpr);
    for (var i = 0; i < layer.length; i++) paint(layer[i]);
    ctx.globalAlpha = 1;
  }
  /* a see-through line in hand is drawn whole each time, over a picture of the canvas kept when it began: pieces laid
     one on another, as for the pens, would show a darker spot at every joint */
  var snap = null;
  function keep() {
    if (!snap) snap = D.createElement("canvas");
    if (snap.width !== cv.width || snap.height !== cv.height) { snap.width = cv.width; snap.height = cv.height; }
    var c = snap.getContext("2d"); c.clearRect(0, 0, snap.width, snap.height); c.drawImage(cv, 0, 0);
  }
  function live() {
    var o = origin(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.clearRect(0, 0, cv.width, cv.height); ctx.drawImage(snap, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, -o.x * dpr, -o.y * dpr); paint(cur.s); ctx.globalAlpha = 1;
  }
  function point(e) { var rc = cv.getBoundingClientRect(), o = origin(); return [e.clientX - rc.left + o.x, e.clientY - rc.top + o.y]; }
  function extend(x, y) {                              /* the newest piece of the stroke in hand; a pen's piece is drawn at once */
    var s = cur.s, p = s.p, n = p.length, dx = x - p[n - 2], dy = y - p[n - 1];
    if (dx * dx + dy * dy < 0.6) return false;
    if (!s.a) { style(s); ctx.beginPath(); ctx.moveTo(p[n - 2], p[n - 1]); ctx.lineTo(x, y); ctx.stroke(); }
    p.push(x, y); if (x < s.x0) s.x0 = x; if (x > s.x1) s.x1 = x; if (y < s.y0) s.y0 = y; if (y > s.y1) s.y1 = y;
    return true;
  }

  /* the eraser works by object: a line that the eraser touches goes as a whole */
  function near(s, x, y, r) {                          /* is (x, y) within r of the line s (r is added to half its thickness)? */
    var p = s.p, n = p.length / 2, rr = r + s.w / 2, i, ax, ay, bx, by, t, dx, dy;
    if (x < s.x0 - rr || x > s.x1 + rr || y < s.y0 - rr || y > s.y1 + rr) return false;
    if (n === 1) { dx = x - p[0]; dy = y - p[1]; return dx * dx + dy * dy <= rr * rr; }
    for (i = 0; i < n - 1; i++) {
      ax = p[2 * i]; ay = p[2 * i + 1]; bx = p[2 * i + 2] - ax; by = p[2 * i + 3] - ay;
      t = bx || by ? ((x - ax) * bx + (y - ay) * by) / (bx * bx + by * by) : 0; t = t < 0 ? 0 : t > 1 ? 1 : t;
      dx = x - ax - t * bx; dy = y - ay - t * by; if (dx * dx + dy * dy <= rr * rr) return true;
    }
    return false;
  }
  function eraseAt(x, y) {                             /* newest line first; each removal remembers its place for the undo */
    var hitAny = false, i;
    for (i = layer.length - 1; i >= 0; i--) if (near(layer[i], x, y, cur.r)) { cur.gone.push({ s: layer[i], i: i }); layer.splice(i, 1); hitAny = true; }
    return hitAny;
  }
  function eraseTo(x, y) {                             /* along the eraser's path, so a quick sweep misses nothing */
    var dx = x - cur.x, dy = y - cur.y, n = Math.max(1, Math.ceil(Math.sqrt(dx * dx + dy * dy) / 5)), k, hitAny = false;
    for (k = 1; k <= n; k++) if (eraseAt(cur.x + dx * k / n, cur.y + dy * k / n)) hitAny = true;
    cur.x = x; cur.y = y; if (hitAny) redraw();
  }
  function putBack(gone) { for (var i = gone.length - 1; i >= 0; i--) layer.splice(Math.min(gone[i].i, layer.length), 0, gone[i].s); }

  function drop() {                                    /* what the pointer in hand has done is undone: a palm that came before the pen */
    if (!cur) return;
    if (cur.gone) putBack(cur.gone); else { var i = layer.indexOf(cur.s); if (i >= 0) layer.splice(i, 1); hist.pop(); }
    try { cv.releasePointerCapture(cur.id); } catch (e) {} cur = null; redraw();
  }
  function finish(e) {
    if (!cur || (e && e.pointerId !== cur.id)) return;
    if (cur.type === "pen") penAt = Date.now();
    if (cur.gone && cur.gone.length) did({ a: "erase", gone: cur.gone });
    cur = null; redraw();
  }

  cv.addEventListener("pointerdown", function (e) {
    if (!on) return; var now = Date.now();
    if (e.pointerType === "mouse" && e.button !== 0) return;
    if (e.pointerType === "pen") { penAt = now; if (cur && cur.type === "touch") drop(); }       /* a resting palm came first: the pen wins */
    else if (e.pointerType === "touch" && now - penAt < 700) return;                              /* a palm beside the pen */
    if (cur) return;
    e.preventDefault(); try { cv.setPointerCapture(e.pointerId); } catch (err) {}
    var pt = point(e);
    if (tool === "eraser") {
      cur = { id: e.pointerId, type: e.pointerType, gone: [], x: pt[0], y: pt[1], r: e.pointerType === "mouse" ? 8 : 12 };
      if (eraseAt(pt[0], pt[1])) redraw();
      return;
    }
    var hl = !!HL[slot], s = { c: inkOf(slot), w: hl ? HL_W : size, p: pt, x0: pt[0], y0: pt[1], x1: pt[0], y1: pt[1] };
    if (hl) { s.a = HL_A; keep(); }                     /* the picture is kept before the new line is on it */
    cur = { id: e.pointerId, type: e.pointerType, s: s }; layer.push(s); did({ a: "add", s: s });
    if (hl) live(); else { style(s); ctx.beginPath(); ctx.arc(pt[0], pt[1], s.w / 2, 0, 6.2832); ctx.fill(); }
  });
  cv.addEventListener("pointermove", function (e) {
    if (e.pointerType === "pen") penAt = Date.now();
    if (!cur || e.pointerId !== cur.id) return;
    var evs = e.getCoalescedEvents ? e.getCoalescedEvents() : null, i, pt;
    if (!evs || !evs.length) evs = [e];
    var grown = false;
    for (i = 0; i < evs.length; i++) { pt = point(evs[i]); if (cur.gone) eraseTo(pt[0], pt[1]); else if (extend(pt[0], pt[1])) grown = true; }
    if (grown && cur.s.a) live();
  });
  ["pointerup", "pointercancel", "lostpointercapture"].forEach(function (t) { cv.addEventListener(t, finish); });
  cv.addEventListener("contextmenu", function (e) { e.preventDefault(); });
  root.addEventListener("wheel", function (e) { if (on) e.preventDefault(); }, { passive: false });
  root.addEventListener("touchmove", function (e) { if (on && e.target !== range && e.target !== veil) e.preventDefault(); }, { passive: false });
  /* what happens on the toolbar and the canvas stays here: the page's own handlers (a slide viewer that pages on a
     click, a swipe or the wheel; menus that close on a click elsewhere) never see it */
  ["pointerdown", "pointerup", "pointermove", "pointercancel", "mousedown", "mouseup", "mousemove", "click", "dblclick", "contextmenu", "touchstart", "touchmove", "touchend", "touchcancel", "wheel"]
    .forEach(function (t) { root.addEventListener(t, function (e) { e.stopPropagation(); }); });

  /* ---------- on and off ---------- */
  function setOn(v) {
    v = !!v; if (v === on) return;
    if (!v && cur) finish();
    on = v; cv.hidden = !on; tools.hidden = !on;
    if (on) { var a = D.activeElement; if (a && a !== D.body && !root.contains(a) && a.blur) try { a.blur(); } catch (e) {} useLayer(); fit(); redraw(); }
    sync(); place();
  }
  function clearAll() { if (cur) finish(); if (layer.length) did({ a: "clear", all: layer.slice() }); layer.length = 0; redraw(); }
  function undo() {
    if (cur) return; var act = hist.pop(), i; if (!act) return;
    if (act.a === "add") { i = layer.indexOf(act.s); if (i >= 0) layer.splice(i, 1); }
    else if (act.a === "erase") putBack(act.gone);
    else if (act.a === "clear") Array.prototype.unshift.apply(layer, act.all);
    redraw();
  }

  bar.addEventListener("click", function (e) {
    if (Date.now() - dragEnd < 350) { e.preventDefault(); e.stopPropagation(); return; }           /* the end of a drag is not a click */
    var b = e.target.closest ? e.target.closest("button[data-act]") : null; if (!b) return;
    var act = b.getAttribute("data-act");
    if (act === "toggle") setOn(!on);
    else if (act === "colour") { slot = b.getAttribute("data-c"); tool = "pen"; save(); sync(); }
    else if (act === "eraser") { tool = tool === "eraser" ? "pen" : "eraser"; sync(); }
    else if (act === "clear") clearAll();
  });
  range.addEventListener("input", function () { size = Math.max(1, Math.min(24, Math.round(+range.value) || 4)); save(); sync(); });
  veil.addEventListener("input", function () { cover = Math.max(0, Math.min(100, Math.round(+veil.value) || 0)); sync(); });

  /* dragging the toolbar: by any part of it except the slider; a small movement is still a click */
  var drag = null, DRAG = ["pointermove", "pointerup", "pointercancel", "dragstart", "selectstart"];
  function dragOn(t) { return t === "pointermove" ? dragMove : t === "dragstart" || t === "selectstart" ? dragNo : dragStop; }
  /* once the toolbar has moved, a link or a picture of the page may lie where the press began, and the browser would
     start dragging that instead (and cancel the pointer): no native drag or text selection while the toolbar is held */
  function dragNo(e) { e.preventDefault(); }
  function dragMove(e) {                               /* on the window, so a quick pull that leaves the small button is still followed */
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.moved) { if (dx * dx + dy * dy < 36) return; drag.moved = true; try { bar.setPointerCapture(e.pointerId); } catch (err) {} }
    pos = { r: drag.r - dx, b: drag.b - dy }; place(); e.preventDefault();
  }
  function dragStop(e) {
    if (!drag || e.pointerId !== drag.id) return;
    DRAG.forEach(function (t) { window.removeEventListener(t, dragOn(t), true); });
    if (drag.moved) { dragEnd = Date.now(); var rc = bar.getBoundingClientRect(); pos = { r: (H.clientWidth || innerWidth) - rc.right, b: (H.clientHeight || innerHeight) - rc.bottom }; save(); }
    drag = null;
  }
  bar.addEventListener("pointerdown", function (e) {
    if (e.target === range || e.target === veil || (e.pointerType === "mouse" && e.button !== 0) || drag) return;
    var rc = bar.getBoundingClientRect(), vw = H.clientWidth || innerWidth, vh = H.clientHeight || innerHeight;
    drag = { id: e.pointerId, x: e.clientX, y: e.clientY, r: vw - rc.right, b: vh - rc.bottom, moved: false };
    DRAG.forEach(function (t) { window.addEventListener(t, dragOn(t), true); });
  });

  /* while annotation is on the page gets no keys either; the browser's own shortcuts and the toolbar keep theirs */
  window.addEventListener("keydown", function (e) {
    if (!on) return;
    function stop() { e.preventDefault(); e.stopImmediatePropagation(); }
    if (e.key === "Escape") { stop(); setOn(false); return; }
    if ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === "z" || e.key === "Z")) { stop(); undo(); return; }
    if (e.ctrlKey || e.metaKey || e.altKey || /^F\d+$/.test(e.key) || e.key === "Tab") return;
    /* the toolbar keeps the keys its controls need: Enter and Space on a button, every key on a slider */
    if (e.target && e.target.nodeType === 1 && root.contains(e.target) && (e.target === range || e.target === veil || e.key === "Enter" || e.key === " " || e.key === "Spacebar")) return;
    stop();
  }, true);

  /* the page moved, turned, changed theme or language, or went full screen */
  var raf = 0;
  function settle() { raf = 0; if (on) { fit(); redraw(); } place(); }
  function later() { if (!raf) raf = window.requestAnimationFrame ? requestAnimationFrame(settle) : setTimeout(settle, 16); }
  window.addEventListener("scroll", function () { if (on) redraw(); }, { passive: true });
  window.addEventListener("resize", later); window.addEventListener("orientationchange", later);
  function rehost() {                                  /* full screen shows only its own element: move in with it, and back */
    var f = fsEl(), h = f && f.nodeType === 1 && !/^(IFRAME|VIDEO|IMG|CANVAS|OBJECT|EMBED)$/.test(f.tagName) ? f : D.body;
    if (cur) finish();
    if (root.parentNode !== h) h.appendChild(root);
    if (on) { useLayer(); fit(); redraw(); }
    place();
  }
  D.addEventListener("fullscreenchange", rehost); D.addEventListener("webkitfullscreenchange", rehost);
  if (window.MutationObserver) {
    new MutationObserver(sync).observe(H, { attributes: true, attributeFilter: ["data-lang", "lang", "data-theme"] });
    var tp = D.querySelector(".tpill"); if (tp) new MutationObserver(function () { if (!pos) place(); }).observe(tp, { attributes: true, attributeFilter: ["hidden", "class", "style"] });
  }
  if (window.matchMedia) { var mq = matchMedia("(prefers-color-scheme: dark)"); if (mq.addEventListener) mq.addEventListener("change", sync); else if (mq.addListener) mq.addListener(sync); }

  D.body.appendChild(root); sync(); place();
  window.RZAnnotate = { version: "1.2", on: function () { setOn(true); }, off: function () { setOn(false); }, toggle: function () { setOn(!on); },
    clear: clearAll, undo: undo, isOn: function () { return on; } };
})();
