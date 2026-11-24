/* lab_ui.js — shared UI helpers for the SEAA 4243 FE labs */
var UI = (function () {
  "use strict";
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function mode() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t === "dark" || t === "light") return t;
    return mq && mq.matches ? "dark" : "light";
  }
  function onTheme(cb) {
    if (mq && mq.addEventListener) mq.addEventListener("change", cb);
    new MutationObserver(cb).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  }
  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) { if (k === "class") e.className = attrs[k]; else e.setAttribute(k, attrs[k]); }
    if (text != null) e.textContent = text;
    return e;
  }
  function fmt(x, d) {
    if (x == null || !isFinite(x)) return "—";
    var s = Math.abs(x) >= 1e5 || (Math.abs(x) < 1e-3 && x !== 0) ? x.toExponential(Math.max(1, d - 1)) : x.toFixed(d);
    return s.replace("-", "−");
  }
  function fmtSig(x, sig) {
    if (x == null || !isFinite(x)) return "—";
    if (x === 0) return "0";
    var d = Math.max(0, sig - 1 - Math.floor(Math.log10(Math.abs(x))));
    return fmt(x, Math.min(d, 6));
  }
  function group(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function pct(x) { return (x >= 0 ? "+" : "−") + Math.abs(x).toFixed(Math.abs(x) < 1 ? 2 : 1) + "%"; }
  /* size a canvas to its container width with a given aspect; returns {ctx, w, h, dpr} in CSS pixels */
  function fitCanvas(canvas, aspect, maxH) {
    var w = Math.max(240, Math.floor(canvas.parentElement.clientWidth));
    var h = Math.round(w / aspect); if (maxH && h > maxH) { h = maxH; }
    var dpr = Math.min(3, window.devicePixelRatio || 1);
    canvas.style.height = h + "px"; canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    var ctx = canvas.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h, dpr: dpr };
  }
  /* world -> screen transform fitting box [x0,x1]x[y0,y1] into w x h with padding */
  function view(box, w, h, pad) {
    var sx = (w - 2 * pad) / (box[1] - box[0]), sy = (h - 2 * pad) / (box[3] - box[2]), s = Math.min(sx, sy);
    var ox = pad + ((w - 2 * pad) - s * (box[1] - box[0])) / 2 - s * box[0];
    var oy = h - pad - ((h - 2 * pad) - s * (box[3] - box[2])) / 2 + s * box[2];
    return { s: s, X: function (x) { return ox + s * x; }, Y: function (y) { return oy - s * y; }, inv: function (px, py) { return [(px - ox) / s, (oy - py) / s]; } };
  }
  /* fill the screen rectangle covering world box with a scalar field; val(x, y) returns a number or NaN */
  function paintField(ctx, V, box, dpr, val, lo, hi, lutArr) {
    var px0 = Math.floor(V.X(box[0]) * dpr), px1 = Math.ceil(V.X(box[1]) * dpr), py0 = Math.floor(V.Y(box[3]) * dpr), py1 = Math.ceil(V.Y(box[2]) * dpr);
    var W = Math.max(1, px1 - px0), H = Math.max(1, py1 - py0), img = ctx.createImageData(W, H), d = img.data, span = hi - lo || 1;
    for (var j = 0; j < H; j++) {
      var wy = (V.Y(0) * dpr - (py0 + j + 0.5)) / (V.s * dpr);
      if (wy < box[2] || wy > box[3]) continue;
      for (var i = 0; i < W; i++) {
        var wx = ((px0 + i + 0.5) / dpr - V.X(0)) / V.s;
        if (wx < box[0] || wx > box[1]) continue;
        var v = val(wx, wy); if (!(v === v)) continue;
        var k = Math.max(0, Math.min(255, Math.round((v - lo) / span * 255))) * 3, o = (j * W + i) * 4;
        d[o] = lutArr[k]; d[o + 1] = lutArr[k + 1]; d[o + 2] = lutArr[k + 2]; d[o + 3] = 255;
      }
    }
    var tmp = document.createElement("canvas"); tmp.width = W; tmp.height = H; tmp.getContext("2d").putImageData(img, 0, 0);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(tmp, px0, py0); ctx.restore();
  }
  /* marching squares on a sampled grid; returns array of segments [x1,y1,x2,y2] in world coordinates */
  function contours(val, box, nx, ny, level) {
    var segs = [], dx = (box[1] - box[0]) / nx, dy = (box[3] - box[2]) / ny, g = [], i, j;
    for (j = 0; j <= ny; j++) { g.push([]); for (i = 0; i <= nx; i++) g[j].push(val(box[0] + i * dx, box[2] + j * dy) - level); }
    function lerp(x1, y1, v1, x2, y2, v2) { var t = v1 / (v1 - v2); return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]; }
    for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) {
      var x = box[0] + i * dx, y = box[2] + j * dy, a = g[j][i], b = g[j][i + 1], c = g[j + 1][i + 1], d = g[j + 1][i], pts = [];
      if ((a > 0) !== (b > 0)) pts.push(lerp(x, y, a, x + dx, y, b));
      if ((b > 0) !== (c > 0)) pts.push(lerp(x + dx, y, b, x + dx, y + dy, c));
      if ((c > 0) !== (d > 0)) pts.push(lerp(x + dx, y + dy, c, x, y + dy, d));
      if ((d > 0) !== (a > 0)) pts.push(lerp(x, y + dy, d, x, y, a));
      if (pts.length >= 2) segs.push([pts[0][0], pts[0][1], pts[1][0], pts[1][1]]);
      if (pts.length === 4) segs.push([pts[2][0], pts[2][1], pts[3][0], pts[3][1]]);
    }
    return segs;
  }
  function legend(host, ramp, lo, hi, caption, n) {
    host.innerHTML = "";
    var bar = el("div", { class: "bar" }); bar.style.background = FE.cssGradient(ramp, mode());
    var ticks = el("div", { class: "ticks" }); n = n || 5;
    for (var i = 0; i < n; i++) ticks.appendChild(el("span", null, fmtSig(lo + (hi - lo) * i / (n - 1), 3)));
    host.appendChild(el("div", { class: "cap" }, caption)); host.appendChild(bar); host.appendChild(ticks);
  }
  /* bind a radio-group "seg" control */
  function seg(host, name, options, value, onChange) {
    host.innerHTML = ""; host.classList.add("seg"); host.setAttribute("role", "radiogroup");
    options.forEach(function (o, k) {
      var id = name + "-" + k, inp = el("input", { type: "radio", name: name, id: id, value: String(o.value) });
      if (String(o.value) === String(value)) inp.checked = true;
      inp.addEventListener("change", function () { if (inp.checked) onChange(o.value); });
      var lab = el("label", { for: id }); lab.innerHTML = o.label;
      host.appendChild(inp); host.appendChild(lab);
    });
  }
  /* SVG line chart. series: [{name, color, points: [{x, y}]}]; opt: {xlog, xlabel, ylabel, ref: {y, label}, yfmt, xfmt, height} */
  function lineChart(host, series, opt) {
    host.innerHTML = ""; opt = opt || {};
    var W = Math.max(280, host.clientWidth), H = opt.height || 260, m = { l: 62, r: 16, t: 14, b: 44 };
    var all = []; series.forEach(function (s) { s.points.forEach(function (p) { all.push(p); }); });
    if (!all.length) return;
    var xs = all.map(function (p) { return p.x; }), ys = all.map(function (p) { return p.y; });
    if (opt.ref) ys.push(opt.ref.y);
    var fx = opt.xlog ? function (v) { return Math.log10(v); } : function (v) { return v; };
    var x0 = Math.min.apply(null, xs.map(fx)), x1 = Math.max.apply(null, xs.map(fx)); if (x1 === x0) { x0 -= 0.5; x1 += 0.5; }
    var padx = (x1 - x0) * 0.06; x0 -= padx; x1 += padx;
    var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys), pady = (y1 - y0) * 0.12 || Math.abs(y1) * 0.1 || 1; y0 -= pady; y1 += pady;
    var SX = function (v) { return m.l + (fx(v) - x0) / (x1 - x0) * (W - m.l - m.r); }, SY = function (v) { return H - m.b - (v - y0) / (y1 - y0) * (H - m.t - m.b); };
    var NS = "http://www.w3.org/2000/svg", svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("role", "img"); svg.setAttribute("aria-label", opt.aria || "Convergence chart");
    function add(tag, at, parent) { var e = document.createElementNS(NS, tag); for (var k in at) e.setAttribute(k, at[k]); (parent || svg).appendChild(e); return e; }
    function txt(x, y, s, at) { var e = add("text", Object.assign({ x: x, y: y, fill: css("--muted"), "font-size": 12, "font-family": "IBM Plex Sans, system-ui, sans-serif" }, at || {})); e.textContent = s; return e; }
    var step = niceStep((y1 - y0) / 4), yt = Math.ceil(y0 / step) * step;
    for (; yt <= y1 + 1e-12; yt += step) {
      add("line", { x1: m.l, x2: W - m.r, y1: SY(yt), y2: SY(yt), stroke: css("--grid"), "stroke-width": 1 });
      txt(m.l - 8, SY(yt) + 4, (opt.yfmt || function (v) { return fmtSig(v, 3); })(yt), { "text-anchor": "end" });
    }
    var xticks = (opt.xticks || xs.filter(function (v, k) { return xs.indexOf(v) === k; })).filter(function (v) { var u = fx(v); return u >= x0 && u <= x1; });
    xticks.forEach(function (v) { txt(SX(v), H - m.b + 18, (opt.xfmt || String)(v), { "text-anchor": "middle" }); });
    add("line", { x1: m.l, x2: W - m.r, y1: H - m.b, y2: H - m.b, stroke: css("--axis"), "stroke-width": 1 });
    if (opt.xlabel) txt((m.l + W - m.r) / 2, H - 6, opt.xlabel, { "text-anchor": "middle" });
    if (opt.ylabel) txt(14, (m.t + H - m.b) / 2, opt.ylabel, { "text-anchor": "middle", transform: "rotate(-90 14 " + ((m.t + H - m.b) / 2) + ")" });
    if (opt.ref) {
      add("line", { x1: m.l, x2: W - m.r, y1: SY(opt.ref.y), y2: SY(opt.ref.y), stroke: css("--ref"), "stroke-width": 1.5 });
      var above = all.filter(function (p) { return p.y > opt.ref.y; }).length, below = all.length - above;
      txt(W - m.r, SY(opt.ref.y) + (above > below ? 16 : -7), opt.ref.label, { "text-anchor": "end", fill: css("--body") });
    }
    series.forEach(function (s) {
      if (!s.points.length) return;
      var d = s.points.map(function (p, k) { return (k ? "L" : "M") + SX(p.x).toFixed(1) + " " + SY(p.y).toFixed(1); }).join(" ");
      add("path", { d: d, fill: "none", stroke: s.color, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" });
      s.points.forEach(function (p) { add("circle", { cx: SX(p.x), cy: SY(p.y), r: 4.5, fill: s.color, stroke: css("--surface"), "stroke-width": 2 }); });
    });
    var cross = add("line", { y1: m.t, y2: H - m.b, stroke: css("--axis"), "stroke-width": 1, visibility: "hidden" });
    host.appendChild(svg);
    if (series.length > 1) {
      var lg = el("div", { class: "chart-legend" });
      series.forEach(function (s) { var sp = el("span"); var i = el("i"); i.style.background = s.color; sp.appendChild(i); sp.appendChild(document.createTextNode(s.name)); lg.appendChild(sp); });
      host.insertBefore(lg, svg);
    }
    var tip = el("div", { class: "tip" }); tip.hidden = true; host.appendChild(tip);
    function show(evt) {
      var r = svg.getBoundingClientRect(), px = (evt.clientX - r.left) * W / r.width, best = null, bd = Infinity;
      xs.forEach(function (v) { var dd = Math.abs(SX(v) - px); if (dd < bd) { bd = dd; best = v; } });
      if (best == null || bd > 40) { hide(); return; }
      cross.setAttribute("x1", SX(best)); cross.setAttribute("x2", SX(best)); cross.setAttribute("visibility", "visible");
      tip.innerHTML = ""; tip.appendChild(el("div", null, (opt.xname || "x") + " " + (opt.xfmt || String)(best)));
      series.forEach(function (s) {
        var p = s.points.filter(function (q) { return q.x === best; })[0]; if (!p) return;
        var row = el("div", { class: "r" }), left = el("span"), key = el("i"); key.style.background = s.color;
        left.appendChild(key); left.appendChild(document.createTextNode(" " + (p.label || s.name)));
        var b = el("b", null, (opt.yfmt || function (v) { return fmtSig(v, 4); })(p.y)); row.appendChild(b); row.appendChild(left); tip.appendChild(row);
      });
      tip.hidden = false;
      var tx = SX(best) / W * r.width + 12; if (tx > r.width - 170) tx = SX(best) / W * r.width - 170;
      tip.style.left = Math.max(0, tx) + "px"; tip.style.top = (svg.offsetTop + 8) + "px";
    }
    function hide() { tip.hidden = true; cross.setAttribute("visibility", "hidden"); }
    svg.addEventListener("pointermove", show); svg.addEventListener("pointerdown", show); svg.addEventListener("pointerleave", hide);
  }
  function niceStep(raw) { var p = Math.pow(10, Math.floor(Math.log10(Math.abs(raw) || 1))), f = raw / p; return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p; }
  function table(host, head, rows) {
    host.innerHTML = ""; var wrap = el("div", { class: "table-wrap" }), t = el("table"), tr = el("tr");
    head.forEach(function (h) { tr.appendChild(el("th", { scope: "col" }, h)); }); t.appendChild(tr);
    rows.forEach(function (r) { var row = el("tr"); r.forEach(function (c) { row.appendChild(el("td", null, c)); }); t.appendChild(row); });
    wrap.appendChild(t); host.appendChild(wrap);
  }
  function debounce(fn, ms) { var t; return function () { var a = arguments; clearTimeout(t); t = setTimeout(function () { fn.apply(null, a); }, ms); }; }
  function halo(ctx, s, x, y, color, align, size, weight) {
    ctx.font = (weight || 600) + " " + (size || 13) + "px IBM Plex Sans, system-ui, sans-serif"; ctx.textAlign = align || "center"; ctx.textBaseline = "middle";
    ctx.lineWidth = 3.5; ctx.strokeStyle = css("--surface"); ctx.lineJoin = "round"; ctx.strokeText(s, x, y); ctx.fillStyle = color; ctx.fillText(s, x, y);
  }
  /* Milestones: a task the lab can see completed from its own state. Recorded in this browser
     (so a part page opened later can read it) and posted to a parent page if there is one. */
  var _ms = {};
  function milestone(lab, id) {
    if (_ms[id]) return; _ms[id] = true;
    var key = "seaa4243-lab-" + lab, rec = {};
    try { rec = JSON.parse(localStorage.getItem(key) || "{}") || {}; } catch (e) { rec = {}; }
    rec[id] = Date.now(); try { localStorage.setItem(key, JSON.stringify(rec)); } catch (e) {}
    try { if (window.parent && window.parent !== window) window.parent.postMessage({ type: "seaa4243-lab", lab: lab, id: id }, "*"); } catch (e) {}
  }
  return { mode: mode, onTheme: onTheme, css: css, $: $, $$: $$, el: el, fmt: fmt, fmtSig: fmtSig, group: group, pct: pct, fitCanvas: fitCanvas, view: view,
           paintField: paintField, contours: contours, legend: legend, seg: seg, lineChart: lineChart, table: table, debounce: debounce, halo: halo, milestone: milestone };
})();
