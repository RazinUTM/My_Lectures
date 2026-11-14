/* SEAA 4333 Unit 7 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes: clear height l = storey height − beam depth in the plane;
   k = (I/l)col / Σ2(I/l)beam ≥ 0.1 (fixed base k1 = 0.1); braced l0 by EC2 Eq. 5.15, unbraced by Eq. 5.16;
   λ = l0/i with i = h/√12; λlim = 20ABC/√n with A = 0.7, B = 1.1, n = NEd/(Ac fcd), fcd = 0.85fck/1.5;
   C = 1.7 − rm, rm negative in double curvature, rm = 1 when unbraced, without end moments, or when
   |M02| ≤ NEd l0/400 (braced, imperfections dominate). */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return a + s * Math.floor(r() * (n + 1)); }
  function r2(x) { return Math.round(x * 100) / 100; }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }

  /* ---------- the course method ---------- */
  function fB(k) { return 1 + k / (0.45 + k); }                       // bracket of Eq. 5.15
  function l0Braced(l, k1, k2) { return 0.5 * l * Math.sqrt(fB(k1) * fB(k2)); }
  function unbTerms(k1, k2) { return { a: Math.sqrt(1 + 10 * k1 * k2 / (k1 + k2)), b: (1 + k1 / (1 + k1)) * (1 + k2 / (1 + k2)) }; }
  function l0Unbraced(l, k1, k2) { var t = unbTerms(k1, k2); return l * Math.max(t.a, t.b); }
  function fcdOf(fck) { return 0.85 * fck / 1.5; }
  var CLS = { 25: "C25/30", 30: "C30/37", 35: "C35/45" };
  function limit(c) {                                                 // c: {braced, N, Ac, fck, Mt, Mb, dbl, l0}
    var fcd = fcdOf(c.fck), n = c.N * 1e3 / (c.Ac * fcd), Mx = Math.max(Math.abs(c.Mt), Math.abs(c.Mb)), Mn = Math.min(Math.abs(c.Mt), Math.abs(c.Mb));
    var Mi = c.N * c.l0 / 400 / 1e3, why = "", rm;
    if (!c.braced) { rm = 1; why = "unbraced"; }
    else if (Mx === 0) { rm = 1; why = "none"; }
    else if (Mx <= Mi) { rm = 1; why = "imp"; }
    else rm = (c.dbl ? -1 : 1) * Mn / Mx;
    var C = 1.7 - rm;
    return { fcd: fcd, n: n, Mi: Mi, rm: rm, C: C, why: why, Mx: Mx, Mn: Mn, lim: 20 * 0.7 * 1.1 * C / Math.sqrt(n) };
  }
  function kTxt(k1, fixed) { return fixed ? bi("k<sub>1</sub> = " + num("0.1") + " at the bottom (a base fixed into a footing designed for the moment)", "k<sub>1</sub> = " + num("0.1") + " di bawah (base yang fixed ke dalam footing yang di-design untuk moment)")
                                         : bi("k<sub>1</sub> = " + num(fmt(k1, 2)) + " at the bottom", "k<sub>1</sub> = " + num(fmt(k1, 2)) + " di bawah"); }
  function curvTxt(dbl) { return dbl ? bi("tension on opposite faces (double curvature)", "tegangan pada muka bertentangan (double curvature)") : bi("tension on the same face (single curvature)", "tegangan pada muka yang sama (single curvature)"); }
  function rmLines(c, L) {
    if (L.why === "unbraced") return [bi("Unbraced: r<sub>m</sub> = 1, C = 0.7, whatever the end moments", "Unbraced: r<sub>m</sub> = 1, C = 0.7, walau apa pun end moment-nya")];
    if (L.why === "none") return [bi("No end moments: the first-order moment is the imperfection only, r<sub>m</sub> = 1, C = 0.7", "Tiada end moment: first-order moment hanyalah imperfection, r<sub>m</sub> = 1, C = 0.7")];
    var imp = "N<sub>Ed</sub>l<sub>0</sub>/400 = " + c.N + " × " + fmt(c.l0 / 1000, 3) + "/400 = " + fmt(L.Mi, 2) + " kN m";
    if (L.why === "imp") return [imp + " ≥ " + fmt(L.Mx, 1) + bi(": imperfections dominate, r<sub>m</sub> = 1, C = 0.7", ": imperfection mendominasi, r<sub>m</sub> = 1, C = 0.7")];
    return [imp + " &lt; " + fmt(L.Mx, 1) + "; r<sub>m</sub> = " + (c.dbl ? "−" : "") + fmt(L.Mn, 1) + "/" + fmt(L.Mx, 1) + " = " + fmt(L.rm, 3) + " → C = 1.7 − (" + fmt(L.rm, 3) + ") = " + fmt(L.C, 3)];
  }

  /* ---------- B1 stiffnesses and k ---------- */
  EX.define("b1", {
    gen: function (r) {
      var b = pick(r, [250, 300]), h = pick(r, b === 250 ? [300, 350, 400, 450] : [300, 350, 400, 450, 500]), ax = r() < 0.5 ? "z" : "y";
      var H = step(r, 3000, 4500, 100), bw = pick(r, [200, 250, 300]), hb = pick(r, [450, 500, 550, 600]);
      var L1 = step(r, 4000, 8000, 500), two = r() < 0.75, L2 = two ? step(r, 4000, 8000, 500) : 0;
      var l = H - hb, I = ax === "z" ? b * Math.pow(h, 3) / 12 : h * Math.pow(b, 3) / 12, Kc = I / l, Ib = bw * Math.pow(hb, 3) / 12;
      var SKb = Ib / L1 + (two ? Ib / L2 : 0), kr = Kc / (2 * SKb);
      return { b: b, h: h, ax: ax, H: H, bw: bw, hb: hb, L1: L1, L2: L2, two: two, l: l, I: I, Kc: Kc, Ib: Ib, SKb: SKb, kr: kr, k: Math.max(0.1, kr) };
    },
    text: function (P) {
      var beams = P.two ? bi("two beams " + num(P.bw + " × " + P.hb) + " spanning " + num(fmt(P.L1 / 1000, 1)) + " m and " + num(fmt(P.L2 / 1000, 1)) + " m frame in, one on each side", "dua beam " + num(P.bw + " × " + P.hb) + " dengan span " + num(fmt(P.L1 / 1000, 1)) + " m dan " + num(fmt(P.L2 / 1000, 1)) + " m masuk, satu pada setiap sisi")
                        : bi("one beam " + num(P.bw + " × " + P.hb) + " spanning " + num(fmt(P.L1 / 1000, 1)) + " m frames in from one side (an edge column)", "satu beam " + num(P.bw + " × " + P.hb) + " dengan span " + num(fmt(P.L1 / 1000, 1)) + " m masuk dari satu sisi (edge column)");
      return bi("A column " + num(P.b + " × " + P.h) + " (h = " + P.h + " mm in the plane of bending about z) runs between floors " + num(P.H) + " mm apart. At the end considered, in the plane of bending about " + P.ax + ", " + beams + ". Find K<sub>c</sub> = I/l of the column and ΣK<sub>b</sub> of the beams, both in units of 10⁵ mm³, and the relative flexibility k at this end.",
                "Satu column " + num(P.b + " × " + P.h) + " (h = " + P.h + " mm dalam satah lenturan pada paksi z) berada di antara lantai yang berjarak " + num(P.H) + " mm. Di hujung yang dipertimbangkan, dalam satah lenturan pada paksi " + P.ax + ", " + beams + ". Cari K<sub>c</sub> = I/l bagi column dan ΣK<sub>b</sub> bagi beam, kedua-duanya dalam unit 10⁵ mm³, dan relative flexibility k di hujung ini.");
    },
    fields: [{ id: "kc", label: ["K<sub>c</sub>", "K<sub>c</sub>"], unit: "10⁵ mm³", fn: function (P) { return P.Kc / 1e5; }, rtol: 0.01 },
             { id: "kb", label: ["ΣK<sub>b</sub>", "ΣK<sub>b</sub>"], unit: "10⁵ mm³", fn: function (P) { return P.SKb / 1e5; }, rtol: 0.01 },
             { id: "k", label: ["k", "k"], fn: function (P) { return P.k; }, atol: 0.003, rtol: 0.02 }],
    hints: [function (P) { return bi("Clear height l = storey height − beam depth = " + P.H + " − " + P.hb + ". About " + P.ax + " the column’s I is " + (P.ax === "z" ? "bh³/12, with h = " + P.h : "hb³/12, with b = " + P.b + " now the side in the plane of bending") + ".",
                                     "Clear height l = ketinggian tingkat − kedalaman beam = " + P.H + " − " + P.hb + ". Pada paksi " + P.ax + ", I column ialah " + (P.ax === "z" ? "bh³/12, dengan h = " + P.h : "hb³/12, dengan b = " + P.b + " kini sisi dalam satah lenturan") + "."); },
            function () { return bi("K = I/l for the column; each beam gives (b<sub>w</sub>h<sub>b</sub>³/12)/L with its own span.", "K = I/l bagi column; setiap beam memberi (b<sub>w</sub>h<sub>b</sub>³/12)/L dengan span-nya sendiri."); },
            function () { return bi("k = K<sub>c</sub>/(2ΣK<sub>b</sub>), and never less than 0.1 (EC2 5.8.3.2(3) note).", "k = K<sub>c</sub>/(2ΣK<sub>b</sub>), dan tidak pernah kurang daripada 0.1 (nota EC2 5.8.3.2(3))."); }],
    solution: function (P) {
      var Iexp = P.ax === "z" ? P.b + " × " + P.h + "³/12" : P.h + " × " + P.b + "³/12";
      var kb = P.two ? fmt(P.Ib / 1e9, 3) + " × 10⁹/" + P.L1 + " + " + fmt(P.Ib / 1e9, 3) + " × 10⁹/" + P.L2 : fmt(P.Ib / 1e9, 3) + " × 10⁹/" + P.L1;
      return sol(["l = " + P.H + " − " + P.hb + " = " + P.l + " mm",
        "I = " + Iexp + " = " + fmt(P.I / 1e9, 4) + " × 10⁹ mm⁴; K<sub>c</sub> = " + fmt(P.I / 1e9, 4) + " × 10⁹/" + P.l + " = " + fmt(P.Kc / 1e5, 3) + " × 10⁵ mm³",
        "I<sub>b</sub> = " + P.bw + " × " + P.hb + "³/12 = " + fmt(P.Ib / 1e9, 3) + " × 10⁹ mm⁴; ΣK<sub>b</sub> = " + kb + " = " + fmt(P.SKb / 1e5, 3) + " × 10⁵ mm³",
        "k = " + fmt(P.Kc / 1e5, 3) + "/(2 × " + fmt(P.SKb / 1e5, 3) + ") = " + fmt(P.kr, 4) + (P.kr < 0.1 ? bi(" &lt; 0.1, so k = 0.1", " &lt; 0.1, jadi k = 0.1") : "")]);
    }
  });

  /* ---------- B2 braced l0 ---------- */
  EX.define("b2", {
    gen: function (r) { var l = step(r, 2600, 4600, 100), fixed = r() < 0.35, k1 = fixed ? 0.1 : step(r, 0.1, 0.8, 0.05), k2 = step(r, 0.1, 0.9, 0.05);
      k1 = r2(k1); k2 = r2(k2); return { l: l, fixed: fixed, k1: k1, k2: k2, f1: fB(k1), f2: fB(k2), l0: l0Braced(l, k1, k2) }; },
    text: function (P) { return bi("A braced column has a clear height l = " + num(P.l) + " mm, with " + kTxt(P.k1, P.fixed) + " and k<sub>2</sub> = " + num(fmt(P.k2, 2)) + " at the top. Find the two brackets of Eq. (7.2), 1 + k<sub>1</sub>/(0.45 + k<sub>1</sub>) and 1 + k<sub>2</sub>/(0.45 + k<sub>2</sub>), and the effective length l<sub>0</sub>.",
                                     "Satu column braced mempunyai clear height l = " + num(P.l) + " mm, dengan " + kTxt(P.k1, P.fixed) + " dan k<sub>2</sub> = " + num(fmt(P.k2, 2)) + " di atas. Cari dua kurungan dalam Eq. (7.2), 1 + k<sub>1</sub>/(0.45 + k<sub>1</sub>) dan 1 + k<sub>2</sub>/(0.45 + k<sub>2</sub>), dan effective length l<sub>0</sub>."); },
    fields: [{ id: "f1", label: ["Bracket 1", "Kurungan 1"], fn: function (P) { return P.f1; }, rtol: 0.004 },
             { id: "f2", label: ["Bracket 2", "Kurungan 2"], fn: function (P) { return P.f2; }, rtol: 0.004 },
             { id: "l0", label: ["l<sub>0</sub>", "l<sub>0</sub>"], unit: "mm", fn: function (P) { return P.l0; }, rtol: 0.008 }],
    hints: [function () { return bi("Eq. (7.2): l<sub>0</sub> = 0.5l√[(1 + k<sub>1</sub>/(0.45 + k<sub>1</sub>))(1 + k<sub>2</sub>/(0.45 + k<sub>2</sub>))].", "Eq. (7.2): l<sub>0</sub> = 0.5l√[(1 + k<sub>1</sub>/(0.45 + k<sub>1</sub>))(1 + k<sub>2</sub>/(0.45 + k<sub>2</sub>))]."); },
            function () { return bi("Each bracket lies between 1 (k = 0, rigid) and 2 (k = ∞, pinned). With k = 0.1 it is 1.182.", "Setiap kurungan terletak antara 1 (k = 0, tegar) dan 2 (k = ∞, pinned). Dengan k = 0.1 nilainya 1.182."); },
            function (P) { return bi("Check: a braced column has 0.59l ≤ l<sub>0</sub> ≤ l when k ≥ 0.1, here " + fmt(0.591 * P.l, 0) + " to " + P.l + " mm.", "Semak: column braced mempunyai 0.59l ≤ l<sub>0</sub> ≤ l apabila k ≥ 0.1, di sini " + fmt(0.591 * P.l, 0) + " hingga " + P.l + " mm."); }],
    solution: function (P) { return sol(["1 + " + fmt(P.k1, 2) + "/(0.45 + " + fmt(P.k1, 2) + ") = " + fmt(P.f1, 4), "1 + " + fmt(P.k2, 2) + "/(0.45 + " + fmt(P.k2, 2) + ") = " + fmt(P.f2, 4),
      "l<sub>0</sub> = 0.5 × " + P.l + " × √(" + fmt(P.f1, 4) + " × " + fmt(P.f2, 4) + ") = 0.5 × " + P.l + " × " + fmt(Math.sqrt(P.f1 * P.f2), 4) + " = " + fmt(P.l0, 0) + " mm (" + fmt(P.l0 / P.l, 3) + "l)"]); }
  });

  /* ---------- B3 unbraced l0 ---------- */
  EX.define("b3", {
    gen: function (r) { var l = step(r, 2600, 4600, 100), fixed = r() < 0.5, k1 = fixed ? 0.1 : r2(step(r, 0.15, 0.8, 0.05)), k2 = r2(step(r, 0.15, 1.2, 0.05)), t = unbTerms(k1, k2);
      return { l: l, fixed: fixed, k1: k1, k2: k2, a: t.a, b: t.b, l0: l * Math.max(t.a, t.b) }; },
    text: function (P) { return bi("An unbraced column has a clear height l = " + num(P.l) + " mm, with " + kTxt(P.k1, P.fixed) + " and k<sub>2</sub> = " + num(fmt(P.k2, 2)) + " at the top. Find the two terms of Eq. (7.3), √(1 + 10k<sub>1</sub>k<sub>2</sub>/(k<sub>1</sub> + k<sub>2</sub>)) and (1 + k<sub>1</sub>/(1 + k<sub>1</sub>))(1 + k<sub>2</sub>/(1 + k<sub>2</sub>)), and the effective length l<sub>0</sub>.",
                                     "Satu column unbraced mempunyai clear height l = " + num(P.l) + " mm, dengan " + kTxt(P.k1, P.fixed) + " dan k<sub>2</sub> = " + num(fmt(P.k2, 2)) + " di atas. Cari dua sebutan dalam Eq. (7.3), √(1 + 10k<sub>1</sub>k<sub>2</sub>/(k<sub>1</sub> + k<sub>2</sub>)) dan (1 + k<sub>1</sub>/(1 + k<sub>1</sub>))(1 + k<sub>2</sub>/(1 + k<sub>2</sub>)), dan effective length l<sub>0</sub>."); },
    fields: [{ id: "ta", label: ["Square-root term", "Sebutan punca kuasa dua"], fn: function (P) { return P.a; }, rtol: 0.004 },
             { id: "tb", label: ["Product term", "Sebutan hasil darab"], fn: function (P) { return P.b; }, rtol: 0.004 },
             { id: "l0", label: ["l<sub>0</sub>", "l<sub>0</sub>"], unit: "mm", fn: function (P) { return P.l0; }, rtol: 0.008 }],
    hints: [function () { return bi("Eq. (7.3): l<sub>0</sub> = l × the larger of the two terms.", "Eq. (7.3): l<sub>0</sub> = l × yang lebih besar antara dua sebutan."); },
            function (P) { return bi("10k<sub>1</sub>k<sub>2</sub>/(k<sub>1</sub> + k<sub>2</sub>) = 10 × " + fmt(P.k1, 2) + " × " + fmt(P.k2, 2) + "/" + fmt(P.k1 + P.k2, 2) + ". Either term can govern: work out both.", "10k<sub>1</sub>k<sub>2</sub>/(k<sub>1</sub> + k<sub>2</sub>) = 10 × " + fmt(P.k1, 2) + " × " + fmt(P.k2, 2) + "/" + fmt(P.k1 + P.k2, 2) + ". Mana-mana sebutan boleh menentukan: kira kedua-duanya."); },
            function () { return bi("Check: an unbraced column always has l<sub>0</sub> ≥ l, and at least 1.22l when k ≥ 0.1.", "Semak: column unbraced sentiasa mempunyai l<sub>0</sub> ≥ l, dan sekurang-kurangnya 1.22l apabila k ≥ 0.1."); }],
    solution: function (P) { var x = 10 * P.k1 * P.k2 / (P.k1 + P.k2);
      return sol(["√(1 + 10 × " + fmt(P.k1, 2) + " × " + fmt(P.k2, 2) + "/" + fmt(P.k1 + P.k2, 2) + ") = √(1 + " + fmt(x, 4) + ") = " + fmt(P.a, 4),
        "(1 + " + fmt(P.k1, 2) + "/" + fmt(1 + P.k1, 2) + ")(1 + " + fmt(P.k2, 2) + "/" + fmt(1 + P.k2, 2) + ") = " + fmt(1 + P.k1 / (1 + P.k1), 4) + " × " + fmt(1 + P.k2 / (1 + P.k2), 4) + " = " + fmt(P.b, 4),
        "l<sub>0</sub> = " + P.l + " × " + fmt(Math.max(P.a, P.b), 4) + " = " + fmt(P.l0, 0) + " mm (" + (P.a >= P.b ? bi("square-root term governs", "sebutan punca kuasa dua menentukan") : bi("product term governs", "sebutan hasil darab menentukan")) + ")"]); }
  });

  /* ---------- B4 slenderness ratios ---------- */
  EX.define("b4", {
    gen: function (r) { var b = pick(r, [250, 300, 350]), h = step(r, b + 50, 600, 50), l0z = step(r, 1800, 4500, 10), l0y = Math.round(l0z * (0.85 + 0.3 * r()) / 10) * 10;
      return { b: b, h: h, l0z: l0z, l0y: l0y, iz: h / Math.sqrt(12), iy: b / Math.sqrt(12) }; },
    text: function (P) { return bi("A column " + num(P.b + " × " + P.h) + " has effective lengths l<sub>0,z</sub> = " + num(P.l0z) + " mm (bending about z, with h = " + P.h + " mm in that plane) and l<sub>0,y</sub> = " + num(P.l0y) + " mm. Find the radius of gyration i<sub>y</sub> and the slenderness ratios λ<sub>z</sub> and λ<sub>y</sub>.",
                                     "Satu column " + num(P.b + " × " + P.h) + " mempunyai effective length l<sub>0,z</sub> = " + num(P.l0z) + " mm (lenturan pada paksi z, dengan h = " + P.h + " mm dalam satah itu) dan l<sub>0,y</sub> = " + num(P.l0y) + " mm. Cari radius of gyration i<sub>y</sub> dan slenderness ratio λ<sub>z</sub> dan λ<sub>y</sub>."); },
    fields: [{ id: "iy", label: ["i<sub>y</sub>", "i<sub>y</sub>"], unit: "mm", fn: function (P) { return P.iy; }, rtol: 0.005 },
             { id: "lz", label: ["λ<sub>z</sub>", "λ<sub>z</sub>"], fn: function (P) { return P.l0z / P.iz; }, rtol: 0.008 },
             { id: "ly", label: ["λ<sub>y</sub>", "λ<sub>y</sub>"], fn: function (P) { return P.l0y / P.iy; }, rtol: 0.008 }],
    hints: [function () { return bi("i = √(I/A); for a rectangle i = (side in the plane of bending)/√12.", "i = √(I/A); bagi segi empat tepat i = (sisi dalam satah lenturan)/√12."); },
            function (P) { return bi("About z the side in the plane of bending is h = " + P.h + " mm; about y it is b = " + P.b + " mm.", "Pada paksi z sisi dalam satah lenturan ialah h = " + P.h + " mm; pada paksi y ialah b = " + P.b + " mm."); },
            function () { return bi("λ = l<sub>0</sub>/i about each axis, each with its own l<sub>0</sub>.", "λ = l<sub>0</sub>/i pada setiap paksi, masing-masing dengan l<sub>0</sub> sendiri."); }],
    solution: function (P) { return sol(["i<sub>z</sub> = " + P.h + "/√12 = " + fmt(P.iz, 1) + " mm; λ<sub>z</sub> = " + P.l0z + "/" + fmt(P.iz, 1) + " = " + fmt(P.l0z / P.iz, 1),
      "i<sub>y</sub> = " + P.b + "/√12 = " + fmt(P.iy, 1) + " mm; λ<sub>y</sub> = " + P.l0y + "/" + fmt(P.iy, 1) + " = " + fmt(P.l0y / P.iy, 1),
      (P.l0y / P.iy > P.l0z / P.iz ? bi("The minor axis (y) has the larger λ.", "Minor axis (y) mempunyai λ yang lebih besar.") : bi("Here the major axis (z) has the larger λ, because its l<sub>0</sub> is longer.", "Di sini major axis (z) mempunyai λ yang lebih besar, kerana l<sub>0</sub>-nya lebih panjang."))]); }
  });

  /* ---------- B5 slenderness limit ---------- */
  function genMoments(r, braced, Mi) {
    var t = braced ? pick(r, ["dbl", "dbl", "sgl", "imp"]) : pick(r, ["dbl", "sgl"]);
    if (t === "imp") { var M = Math.max(1, Math.floor(Mi * (0.3 + 0.6 * r()))); return { Mt: M, Mb: Math.round(M * (0.3 + 0.5 * r())), dbl: r() < 0.5 }; }
    var Mx = Math.max(Math.ceil(Mi * 1.6 / 5) * 5, step(r, 20, 120, 5)), Mn = Math.round(Mx * (0.2 + 0.7 * r()) / 5) * 5;
    return { Mt: Mx, Mb: Mn, dbl: t === "dbl" };
  }
  EX.define("b5", {
    gen: function (r) {
      var braced = r() < 0.75, b = pick(r, [250, 300, 350]), h = step(r, b, 500, 50), fck = pick(r, [25, 30, 35]), Ac = b * h;
      var N = Math.round((0.3 + 0.7 * r()) * Ac * fcdOf(fck) / 1e3 / 10) * 10, l0 = step(r, 1800, 4200, 10), Mi = N * l0 / 400 / 1e3, m = genMoments(r, braced, Mi);
      var c = { braced: braced, b: b, h: h, fck: fck, Ac: Ac, N: N, l0: l0, Mt: m.Mt, Mb: m.Mb, dbl: m.dbl }; c.L = limit(c); return c;
    },
    text: function (P) { var cc = CLS[P.fck];
      return bi((P.braced ? "A braced" : "An unbraced") + " column " + num(P.b + " × " + P.h) + ", " + cc + ", carries N<sub>Ed</sub> = " + num(P.N) + " kN. About the axis considered, l<sub>0</sub> = " + num(P.l0) + " mm and the first-order end moments are " + num(P.Mt) + " kN m at the top and " + num(P.Mb) + " kN m at the bottom, " + curvTxt(P.dbl) + ". With A = 0.7 and B = 1.1, find n, C and λ<sub>lim</sub>.",
                "Satu column " + (P.braced ? "braced" : "unbraced") + " " + num(P.b + " × " + P.h) + ", " + cc + ", membawa N<sub>Ed</sub> = " + num(P.N) + " kN. Pada paksi yang dipertimbangkan, l<sub>0</sub> = " + num(P.l0) + " mm dan first-order end moment ialah " + num(P.Mt) + " kN m di atas dan " + num(P.Mb) + " kN m di bawah, " + curvTxt(P.dbl) + ". Dengan A = 0.7 dan B = 1.1, cari n, C dan λ<sub>lim</sub>."); },
    fields: [{ id: "n", label: ["n", "n"], fn: function (P) { return P.L.n; }, rtol: 0.01 },
             { id: "C", label: ["C", "C"], fn: function (P) { return P.L.C; }, atol: 0.011, rtol: 0 },
             { id: "lim", label: ["λ<sub>lim</sub>", "λ<sub>lim</sub>"], fn: function (P) { return P.L.lim; }, rtol: 0.01 }],
    hints: [function (P) { return bi("f<sub>cd</sub> = 0.85f<sub>ck</sub>/1.5 = " + fmt(P.L.fcd, 2) + " N/mm²; n = N<sub>Ed</sub>/(A<sub>c</sub>f<sub>cd</sub>).", "f<sub>cd</sub> = 0.85f<sub>ck</sub>/1.5 = " + fmt(P.L.fcd, 2) + " N/mm²; n = N<sub>Ed</sub>/(A<sub>c</sub>f<sub>cd</sub>)."); },
            function () { return bi("Unbraced: C = 0.7. Braced: compare the larger end moment with N<sub>Ed</sub>l<sub>0</sub>/400 first; if it is not larger, r<sub>m</sub> = 1 and C = 0.7.", "Unbraced: C = 0.7. Braced: bandingkan end moment yang lebih besar dengan N<sub>Ed</sub>l<sub>0</sub>/400 dahulu; jika ia tidak lebih besar, r<sub>m</sub> = 1 dan C = 0.7."); },
            function () { return bi("Otherwise r<sub>m</sub> = M<sub>01</sub>/M<sub>02</sub> with |M<sub>02</sub>| ≥ |M<sub>01</sub>|: positive in single curvature, negative in double curvature. C = 1.7 − r<sub>m</sub>; λ<sub>lim</sub> = 20 × 0.7 × 1.1 × C/√n.", "Jika tidak, r<sub>m</sub> = M<sub>01</sub>/M<sub>02</sub> dengan |M<sub>02</sub>| ≥ |M<sub>01</sub>|: positif dalam single curvature, negatif dalam double curvature. C = 1.7 − r<sub>m</sub>; λ<sub>lim</sub> = 20 × 0.7 × 1.1 × C/√n."); }],
    solution: function (P) { var L = P.L;
      return sol(["n = " + P.N + " × 10³/(" + P.b + " × " + P.h + " × " + fmt(L.fcd, 2) + ") = " + fmt(L.n, 3)].concat(rmLines(P, L), ["λ<sub>lim</sub> = 20 × 0.7 × 1.1 × " + fmt(L.C, 3) + "/√" + fmt(L.n, 3) + " = " + fmt(L.lim, 1)])); }
  });

  /* ---------- B6 classify ---------- */
  EX.define("b6", {
    gen: function (r) {
      var c, tries = 0;
      do {
        var b = pick(r, [250, 300, 350]), h = step(r, b, 500, 50), ax = r() < 0.5 ? "z" : "y", d = ax === "z" ? h : b, fck = pick(r, [25, 30, 35]), Ac = b * h;
        var l = step(r, 2700, 4500, 100), k1 = r() < 0.4 ? 0.1 : r2(step(r, 0.1, 0.6, 0.05)), k2 = r2(step(r, 0.1, 0.6, 0.05)), l0 = l0Braced(l, k1, k2);
        var N = Math.round((0.35 + 0.65 * r()) * Ac * fcdOf(fck) / 1e3 / 10) * 10, Mi = N * l0 / 400 / 1e3, m = genMoments(r, true, Mi);
        c = { braced: true, b: b, h: h, ax: ax, d: d, fck: fck, Ac: Ac, l: l, k1: k1, k2: k2, l0: l0, N: N, Mt: m.Mt, Mb: m.Mb, dbl: m.dbl };
        c.i = d / Math.sqrt(12); c.lam = l0 / c.i; c.L = limit(c); tries++;
      } while (Math.abs(c.lam - c.L.lim) < 1.5 && tries < 25);
      return c;
    },
    text: function (P) { var cc = CLS[P.fck];
      return bi("A braced column " + num(P.b + " × " + P.h) + ", " + cc + ", bends about " + P.ax + " (the side of " + P.d + " mm lies in that plane). Clear height l = " + num(P.l) + " mm; k<sub>1</sub> = " + num(fmt(P.k1, 2)) + ", k<sub>2</sub> = " + num(fmt(P.k2, 2)) + "; N<sub>Ed</sub> = " + num(P.N) + " kN; end moments " + num(P.Mt) + " and " + num(P.Mb) + " kN m, " + curvTxt(P.dbl) + ". With A = 0.7 and B = 1.1, find λ and λ<sub>lim</sub>, and say whether the column is slender about this axis: type 1 for slender, 0 for non-slender.",
                "Satu column braced " + num(P.b + " × " + P.h) + ", " + cc + ", melentur pada paksi " + P.ax + " (sisi " + P.d + " mm terletak dalam satah itu). Clear height l = " + num(P.l) + " mm; k<sub>1</sub> = " + num(fmt(P.k1, 2)) + ", k<sub>2</sub> = " + num(fmt(P.k2, 2)) + "; N<sub>Ed</sub> = " + num(P.N) + " kN; end moment " + num(P.Mt) + " dan " + num(P.Mb) + " kN m, " + curvTxt(P.dbl) + ". Dengan A = 0.7 dan B = 1.1, cari λ dan λ<sub>lim</sub>, dan nyatakan sama ada column itu slender pada paksi ini: taip 1 untuk slender, 0 untuk non-slender."); },
    fields: [{ id: "lam", label: ["λ", "λ"], fn: function (P) { return P.lam; }, rtol: 0.01 },
             { id: "lim", label: ["λ<sub>lim</sub>", "λ<sub>lim</sub>"], fn: function (P) { return P.L.lim; }, rtol: 0.012 },
             { id: "sl", label: ["Slender? (1 = yes, 0 = no)", "Slender? (1 = ya, 0 = tidak)"], fn: function (P) { return P.lam > P.L.lim ? 1 : 0; }, atol: 0, rtol: 0 }],
    hints: [function () { return bi("l<sub>0</sub> by Eq. (7.2); i = (side in the plane of bending)/√12; λ = l<sub>0</sub>/i.", "l<sub>0</sub> dengan Eq. (7.2); i = (sisi dalam satah lenturan)/√12; λ = l<sub>0</sub>/i."); },
            function (P) { return bi("Imperfection check: N<sub>Ed</sub>l<sub>0</sub>/400 = " + fmt(P.L.Mi, 2) + " kN m against the larger end moment.", "Semakan imperfection: N<sub>Ed</sub>l<sub>0</sub>/400 = " + fmt(P.L.Mi, 2) + " kN m berbanding end moment yang lebih besar."); },
            function () { return bi("Slender when λ &gt; λ<sub>lim</sub>.", "Slender apabila λ &gt; λ<sub>lim</sub>."); }],
    solution: function (P) { var L = P.L;
      return sol(["l<sub>0</sub> = 0.5 × " + P.l + " × √[(1 + " + fmt(P.k1, 2) + "/" + fmt(0.45 + P.k1, 2) + ")(1 + " + fmt(P.k2, 2) + "/" + fmt(0.45 + P.k2, 2) + ")] = " + fmt(P.l0, 0) + " mm",
        "i = " + P.d + "/√12 = " + fmt(P.i, 1) + " mm; λ = " + fmt(P.l0, 0) + "/" + fmt(P.i, 1) + " = " + fmt(P.lam, 1),
        "n = " + P.N + " × 10³/(" + P.b + " × " + P.h + " × " + fmt(L.fcd, 2) + ") = " + fmt(L.n, 3)].concat(rmLines(P, L), [
        "λ<sub>lim</sub> = 20 × 0.7 × 1.1 × " + fmt(L.C, 3) + "/√" + fmt(L.n, 3) + " = " + fmt(L.lim, 1),
        fmt(P.lam, 1) + (P.lam > L.lim ? " &gt; " : " ≤ ") + fmt(L.lim, 1) + (P.lam > L.lim ? bi(": slender (1)", ": slender (1)") : bi(": non-slender (0)", ": non-slender (0)"))])); }
  });

  EX.ready();
})();
