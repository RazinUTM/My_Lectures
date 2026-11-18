/* SEAA 4333 Unit 3 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method (the RC Design app's frame model):
   Table 3.15: v = beta n l_x, l_x the short side of the panel; beta_vx (interpolated in l_y/l_x) on a long side, beta_vy on a short side;
   G_k = sum(beta g_k l_x) + b_b (h_b - h_s) gamma_c, Q_k = sum(beta q_k l_x); w_max = 1.35 G_k + 1.5 Q_k, w_min = 1.35 G_k;
   continuous beam: K = I/L, 3/4 K for an end span with its far end pinned, F = K/sum K, FEM = wL^2/12, balance -F sum M, carry 1/2;
   two spans pinned at both ends: M_B = (w1 L1^3 + w2 L2^3)/(8 (L1 + L2)) (one balance after releasing the pins gives it exactly);
   span statics with hogging magnitudes: V_L = wL/2 + (M_L - M_R)/L, V_R = wL - V_L, M_span = V_L^2/(2w) - M_L;
   one-free-joint sub-frame: dFEM = max(FEM_max,1 - FEM_min,2, FEM_max,2 - FEM_min,1) (end column: FEM_max of its span),
   M_c = dFEM K_c / (K_cu + K_cl + 1/2 K_b,L + 1/2 K_b,R); at an end support the beam carries M_cu + M_cl. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function f2(v) { return fmt(v, 2); }
  var RAT = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.75, 2.0];
  var VX = { 1: [0.33, 0.36, 0.39, 0.41, 0.43, 0.45, 0.48, 0.50], 2: [0.36, 0.39, 0.42, 0.44, 0.45, 0.47, 0.50, 0.52] }, VY = { 1: 0.33, 2: 0.36 };
  function interp(x, ys) { if (x <= RAT[0]) return ys[0]; if (x >= RAT[RAT.length - 1]) return ys[ys.length - 1]; for (var i = 1; i < RAT.length; i++) if (x <= RAT[i]) { var t = (x - RAT[i - 1]) / (RAT[i] - RAT[i - 1]); return ys[i - 1] + t * (ys[i] - ys[i - 1]); } return ys[ys.length - 1]; }
  function panel(L, Ly, cs) { var lx = Math.min(L, Ly), ly = Math.max(L, Ly), rt = ly / lx, long = L >= Ly; return { lx: lx, ly: ly, rt: rt, long: long, beta: long ? interp(rt, VX[cs]) : VY[cs] }; }
  function caseName(cs) { return cs === 1 ? bi("an interior bay (case 1)", "bay dalaman (kes 1)") : bi("an end bay with one short edge outside (case 2)", "bay hujung dengan satu tepi pendek di luar (kes 2)"); }

  /* ---------- B1 the load on a beam from two slab panels ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.L = pick(r, [5, 5.5, 6, 6.5, 7, 7.5, 8]); P.Ly1 = pick(r, [3.5, 4, 4.5, 5]); P.Ly2 = pick(r, [4, 4.5, 5, 5.5, 6, 7]); P.cs = pick(r, [1, 2]);
      P.hs = pick(r, [125, 150, 175]); P.fin = pick(r, [1.0, 1.25, 1.5, 2.0]); P.qi = pick(r, [2.5, 3.0, 4.0, 5.0]); P.qp = pick(r, [0, 0.5, 1.0]);
      P.bb = pick(r, [250, 300]); P.hb = pick(r, [450, 500, 550, 600]);
      P.gk = P.hs / 1000 * 25 + P.fin; P.qk = P.qi + P.qp; P.rib = P.bb / 1000 * (P.hb - P.hs) / 1000 * 25;
      P.a = panel(P.L, P.Ly1, P.cs); P.b = panel(P.L, P.Ly2, P.cs);
      P.Gk = P.a.beta * P.gk * P.a.lx + P.b.beta * P.gk * P.b.lx + P.rib; P.Qk = P.a.beta * P.qk * P.a.lx + P.b.beta * P.qk * P.b.lx;
      P.wmax = 1.35 * P.Gk + 1.5 * P.Qk;
      return P;
    },
    text: function (P) {
      return bi("An interior frame beam spans " + num(P.L) + " m in " + caseName(P.cs) + ". The slab panels on its two sides are " + num(P.Ly1) + " m and " + num(P.Ly2) + " m wide, and the beam is a continuous edge of both. Slab " + num(P.hs) + " mm, finishes " + num(P.fin) + " kN/m², imposed load " + num(P.qi) + " and partitions " + num(P.qp) + " kN/m²; beam " + num(P.bb + " × " + P.hb) + "; concrete 25 kN/m³. Find G<sub>k</sub>, Q<sub>k</sub> and w<sub>max</sub> per metre of beam (RDF Table 3.15).",
                "Satu beam frame dalaman merentang " + num(P.L) + " m dalam " + caseName(P.cs) + ". Panel slab di kedua-dua sisinya selebar " + num(P.Ly1) + " m dan " + num(P.Ly2) + " m, dan beam ialah tepi continuous bagi kedua-duanya. Slab " + num(P.hs) + " mm, kemasan " + num(P.fin) + " kN/m², imposed load " + num(P.qi) + " dan partition " + num(P.qp) + " kN/m²; beam " + num(P.bb + " × " + P.hb) + "; konkrit 25 kN/m³. Cari G<sub>k</sub>, Q<sub>k</sub> dan w<sub>max</sub> per meter beam (RDF Table 3.15).");
    },
    fields: [{ id: "g", label: ["G<sub>k</sub>", "G<sub>k</sub>"], unit: "kN/m", fn: function (P) { return P.Gk; }, rtol: 0.015 },
             { id: "q", label: ["Q<sub>k</sub>", "Q<sub>k</sub>"], unit: "kN/m", fn: function (P) { return P.Qk; }, rtol: 0.015 },
             { id: "w", label: ["w<sub>max</sub>", "w<sub>max</sub>"], unit: "kN/m", fn: function (P) { return P.wmax; }, rtol: 0.015 }],
    hints: [function () { return bi("For each panel: l<sub>x</sub> is its short side. Is the beam on a long side (it is at least as long as the panel is wide) or on a short side?", "Bagi setiap panel: l<sub>x</sub> ialah sisi pendeknya. Adakah beam pada sisi panjang (sekurang-kurangnya sepanjang lebar panel) atau pada sisi pendek?"); },
            function () { return bi("A long side takes β<sub>vx</sub>, interpolated in l<sub>y</sub>/l<sub>x</sub>; a short side takes β<sub>vy</sub>, one value for the case (0.33 in case 1, 0.36 in case 2).", "Sisi panjang mengambil β<sub>vx</sub>, diinterpolasi mengikut l<sub>y</sub>/l<sub>x</sub>; sisi pendek mengambil β<sub>vy</sub>, satu nilai bagi kes itu (0.33 dalam kes 1, 0.36 dalam kes 2)."); },
            function () { return bi("G<sub>k</sub> = Σβ g<sub>k</sub> l<sub>x</sub> + b<sub>b</sub>(h<sub>b</sub> − h<sub>s</sub>) × 25; Q<sub>k</sub> = Σβ q<sub>k</sub> l<sub>x</sub>; w<sub>max</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>.", "G<sub>k</sub> = Σβ g<sub>k</sub> l<sub>x</sub> + b<sub>b</sub>(h<sub>b</sub> − h<sub>s</sub>) × 25; Q<sub>k</sub> = Σβ q<sub>k</sub> l<sub>x</sub>; w<sub>max</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>."); }],
    solution: function (P) {
      function pl(p, Ly) { return Ly + " × " + P.L + " m: l<sub>x</sub> = " + p.lx + ", l<sub>y</sub>/l<sub>x</sub> = " + fmt(p.rt, 3) + ", " + (p.long ? bi("long side, β<sub>vx</sub> = ", "sisi panjang, β<sub>vx</sub> = ") : bi("short side, β<sub>vy</sub> = ", "sisi pendek, β<sub>vy</sub> = ")) + fmt(p.beta, 3); }
      return sol(["g<sub>k</sub> = 25 × " + fmt(P.hs / 1000, 3) + " + " + P.fin + " = " + f2(P.gk) + " kN/m²; q<sub>k</sub> = " + P.qi + " + " + P.qp + " = " + f2(P.qk) + " kN/m²; " + bi("rib", "rib") + " = " + fmt(P.bb / 1000, 2) + " × " + fmt((P.hb - P.hs) / 1000, 3) + " × 25 = " + f2(P.rib) + " kN/m",
        pl(P.a, P.Ly1) + "; " + pl(P.b, P.Ly2),
        "G<sub>k</sub> = " + fmt(P.a.beta, 3) + " × " + f2(P.gk) + " × " + P.a.lx + " + " + fmt(P.b.beta, 3) + " × " + f2(P.gk) + " × " + P.b.lx + " + " + f2(P.rib) + " = " + f2(P.Gk) + " kN/m",
        "Q<sub>k</sub> = " + fmt(P.a.beta, 3) + " × " + f2(P.qk) + " × " + P.a.lx + " + " + fmt(P.b.beta, 3) + " × " + f2(P.qk) + " × " + P.b.lx + " = " + f2(P.Qk) + " kN/m",
        "w<sub>max</sub> = 1.35 × " + f2(P.Gk) + " + 1.5 × " + f2(P.Qk) + " = " + f2(P.wmax) + " kN/m; w<sub>min</sub> = " + f2(1.35 * P.Gk) + " kN/m"]);
    }
  });

  /* ---------- B2 distribution factors and the first balance ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [4, 4.5, 5, 5.5, 6, 6.5, 7]); P.L2 = pick(r, [4, 4.5, 5, 5.5, 6, 6.5, 7, 8]); P.w1 = step(r, 30, 65, 0.5); P.w2 = step(r, 30, 65, 0.5);
      P.k1 = 0.75 / P.L1; P.k2 = 1 / P.L2; P.F1 = P.k1 / (P.k1 + P.k2); P.F2 = 1 - P.F1;
      P.f1 = P.w1 * P.L1 * P.L1 / 12; P.f2 = P.w2 * P.L2 * P.L2 / 12;
      P.A1 = P.f1 / 2;                      /* the release of A carried to B */
      P.U = P.f1 - P.f2; P.b1 = -P.U * P.F1;
      return P;
    },
    text: function (P) {
      return bi("The beams of one floor are analysed as a continuous beam. AB is an end span of " + num(P.L1) + " m, pinned at A, carrying " + num(fmt(P.w1, 1)) + " kN/m; BC is an interior span of " + num(P.L2) + " m carrying " + num(fmt(P.w2, 1)) + " kN/m. All beams have the same section. Find the distribution factor F<sub>BA</sub>, the out-of-balance moment at B in the first row (the fixed-end moments only), and the balancing moment given to BA, with its sign (clockwise positive).",
                "Beam satu lantai dianalisis sebagai continuous beam. AB ialah span hujung " + num(P.L1) + " m, pin di A, memikul " + num(fmt(P.w1, 1)) + " kN/m; BC ialah span dalaman " + num(P.L2) + " m memikul " + num(fmt(P.w2, 1)) + " kN/m. Semua beam mempunyai section yang sama. Cari distribution factor F<sub>BA</sub>, moment tidak seimbang di B dalam baris pertama (fixed-end moment sahaja), dan balancing moment yang diberi kepada BA, dengan tandanya (positif mengikut arah jam).");
    },
    fields: [{ id: "f", label: ["F<sub>BA</sub>", "F<sub>BA</sub>"], unit: "", fn: function (P) { return P.F1; }, rtol: 0.01 },
             { id: "u", label: ["ΣM at B", "ΣM di B"], unit: "kN m", fn: function (P) { return P.U; }, rtol: 0.01, atol: 0.2 },
             { id: "b", label: ["balance at BA", "imbangan di BA"], unit: "kN m", fn: function (P) { return P.b1; }, rtol: 0.015, atol: 0.2 }],
    hints: [function () { return bi("K ∝ I/L; the same section, so K ∝ 1/L. AB has a pinned far end: use ¾ of its K.", "K ∝ I/L; section yang sama, jadi K ∝ 1/L. AB mempunyai hujung jauh pin: gunakan ¾ daripada K-nya."); },
            function () { return bi("At B: FEM<sub>BA</sub> = +w<sub>1</sub>L<sub>1</sub>²/12 (right end of AB), FEM<sub>BC</sub> = −w<sub>2</sub>L<sub>2</sub>²/12 (left end of BC); ΣM is their sum.", "Di B: FEM<sub>BA</sub> = +w<sub>1</sub>L<sub>1</sub>²/12 (hujung kanan AB), FEM<sub>BC</sub> = −w<sub>2</sub>L<sub>2</sub>²/12 (hujung kiri BC); ΣM ialah jumlahnya."); },
            function () { return bi("The balancing moment at BA is −ΣM × F<sub>BA</sub>: it has the opposite sign to the out-of-balance moment.", "Balancing moment di BA ialah −ΣM × F<sub>BA</sub>: tandanya bertentangan dengan moment tidak seimbang."); }],
    solution: function (P) {
      return sol(["K′<sub>AB</sub> ∝ ¾/" + P.L1 + " = " + fmt(P.k1, 4) + "; K<sub>BC</sub> ∝ 1/" + P.L2 + " = " + fmt(P.k2, 4),
        "F<sub>BA</sub> = " + fmt(P.k1, 4) + "/(" + fmt(P.k1, 4) + " + " + fmt(P.k2, 4) + ") = " + fmt(P.F1, 3) + "; F<sub>BC</sub> = " + fmt(P.F2, 3),
        "FEM<sub>BA</sub> = " + fmt(P.w1, 1) + " × " + P.L1 + "²/12 = +" + f2(P.f1) + "; FEM<sub>BC</sub> = −" + fmt(P.w2, 1) + " × " + P.L2 + "²/12 = −" + f2(P.f2) + " kN m",
        "ΣM = " + f2(P.f1) + " − " + f2(P.f2) + " = " + f2(P.U) + " kN m; " + bi("balance at BA", "imbangan di BA") + " = −(" + f2(P.U) + ") × " + fmt(P.F1, 3) + " = " + f2(P.b1) + " kN m",
        bi("In the same row A is released (+" + f2(P.f1) + " at AB); half of it, " + f2(P.A1) + " kN m, is carried to B in the next row, and nothing ever goes back to A (Notes §4).", "Dalam baris yang sama A dilepaskan (+" + f2(P.f1) + " di AB); separuh daripadanya, " + f2(P.A1) + " kN m, dibawa ke B dalam baris seterusnya, dan tiada apa yang kembali ke A (Nota §4).")]);
    }
  });

  /* ---------- B3 two spans: the support moment ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [4, 4.5, 5, 5.5, 6, 6.5, 7]); P.L2 = pick(r, [4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5]); P.w1 = step(r, 40, 65, 0.5); P.w2 = step(r, 22, 38, 0.5);
      P.MB = (P.w1 * Math.pow(P.L1, 3) + P.w2 * Math.pow(P.L2, 3)) / (8 * (P.L1 + P.L2));
      P.VA = P.w1 * P.L1 / 2 - P.MB / P.L1; P.Ms = P.VA * P.VA / (2 * P.w1);
      return P;
    },
    text: function (P) {
      return bi("A two-span beam ABC rests on knife-edge supports, pinned at A and C. AB = " + num(P.L1) + " m carries w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m and BC = " + num(P.L2) + " m carries w<sub>min</sub> = " + num(fmt(P.w2, 1)) + " kN/m; the section is the same throughout. Find the hogging moment at B, the reaction at A and the largest sagging moment in AB.",
                "Satu beam dua span ABC bertumpu pada knife-edge support, pin di A dan C. AB = " + num(P.L1) + " m memikul w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m dan BC = " + num(P.L2) + " m memikul w<sub>min</sub> = " + num(fmt(P.w2, 1)) + " kN/m; section sama di sepanjangnya. Cari hogging moment di B, reaction di A dan sagging moment terbesar dalam AB.");
    },
    fields: [{ id: "m", label: ["M<sub>B</sub>", "M<sub>B</sub>"], unit: "kN m", fn: function (P) { return P.MB; }, rtol: 0.01 },
             { id: "v", label: ["V<sub>A</sub>", "V<sub>A</sub>"], unit: "kN", fn: function (P) { return P.VA; }, rtol: 0.01 },
             { id: "s", label: ["M<sub>span,AB</sub>", "M<sub>span,AB</sub>"], unit: "kN m", fn: function (P) { return P.Ms; }, rtol: 0.015 }],
    hints: [function () { return bi("Both spans have a pinned far end: ¾K each, and the pins are released at once. Releasing A turns the FEM at BA into w<sub>1</sub>L<sub>1</sub>²/8 (the propped cantilever); likewise BC at B, −w<sub>2</sub>L<sub>2</sub>²/8.", "Kedua-dua span mempunyai hujung jauh pin: ¾K setiap satu, dan pin dilepaskan serta-merta. Melepaskan A menjadikan FEM di BA w<sub>1</sub>L<sub>1</sub>²/8 (propped cantilever); begitu juga BC di B, −w<sub>2</sub>L<sub>2</sub>²/8."); },
            function () { return bi("F<sub>BA</sub> = (¾/L<sub>1</sub>)/(¾/L<sub>1</sub> + ¾/L<sub>2</sub>) = L<sub>2</sub>/(L<sub>1</sub> + L<sub>2</sub>). Balance B once: nothing is carried back to the pins, so one balance is exact.", "F<sub>BA</sub> = (¾/L<sub>1</sub>)/(¾/L<sub>1</sub> + ¾/L<sub>2</sub>) = L<sub>2</sub>/(L<sub>1</sub> + L<sub>2</sub>). Imbangi B sekali: tiada apa yang dibawa kembali ke pin, jadi satu imbangan sudah tepat."); },
            function () { return bi("Then V<sub>A</sub> = w<sub>1</sub>L<sub>1</sub>/2 − M<sub>B</sub>/L<sub>1</sub> and M<sub>span</sub> = V<sub>A</sub>²/(2w<sub>1</sub>).", "Kemudian V<sub>A</sub> = w<sub>1</sub>L<sub>1</sub>/2 − M<sub>B</sub>/L<sub>1</sub> dan M<sub>span</sub> = V<sub>A</sub>²/(2w<sub>1</sub>)."); }],
    solution: function (P) {
      var a = P.w1 * P.L1 * P.L1 / 8, b = P.w2 * P.L2 * P.L2 / 8, F = P.L2 / (P.L1 + P.L2);
      return sol([bi("After releasing A and C: ", "Selepas melepaskan A dan C: ") + "M<sub>BA</sub> = " + fmt(P.w1, 1) + " × " + P.L1 + "²/8 = " + f2(a) + ", M<sub>BC</sub> = −" + fmt(P.w2, 1) + " × " + P.L2 + "²/8 = −" + f2(b) + " kN m",
        "F<sub>BA</sub> = " + P.L2 + "/(" + P.L1 + " + " + P.L2 + ") = " + fmt(F, 3) + "; M<sub>B</sub> = " + f2(a) + " − " + fmt(F, 3) + " × (" + f2(a) + " − " + f2(b) + ") = " + f2(P.MB) + " kN m",
        bi("Check: (w<sub>1</sub>L<sub>1</sub>³ + w<sub>2</sub>L<sub>2</sub>³)/(8(L<sub>1</sub> + L<sub>2</sub>)) = ", "Semak: (w<sub>1</sub>L<sub>1</sub>³ + w<sub>2</sub>L<sub>2</sub>³)/(8(L<sub>1</sub> + L<sub>2</sub>)) = ") + f2(P.MB) + " kN m",
        "V<sub>A</sub> = " + fmt(P.w1, 1) + " × " + P.L1 + "/2 − " + f2(P.MB) + "/" + P.L1 + " = " + f2(P.VA) + " kN; x₀ = " + fmt(P.VA / P.w1, 2) + " m; M<sub>span</sub> = " + f2(P.VA) + "²/(2 × " + fmt(P.w1, 1) + ") = " + f2(P.Ms) + " kN m"]);
    }
  });

  /* ---------- B4 shears and the span moment ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = {};
      P.L = pick(r, [4, 4.5, 5, 5.5, 6, 6.5, 7, 8]); P.w = step(r, 25, 65, 0.5);
      var cap = 0.14 * P.w * P.L * P.L; P.ML = Math.round(cap * step(r, 0, 1, 0.05)); P.MR = Math.round(cap * step(r, 0.2, 1, 0.05));
      P.VL = P.w * P.L / 2 + (P.ML - P.MR) / P.L; P.VR = P.w * P.L - P.VL; P.x0 = P.VL / P.w; P.Ms = P.VL * P.VL / (2 * P.w) - P.ML;
      return P;
    },
    text: function (P) {
      return bi("After the moment distribution, a span of " + num(P.L) + " m carrying " + num(fmt(P.w, 1)) + " kN/m has hogging moments of " + num(P.ML) + " kN m at its left end and " + num(P.MR) + " kN m at its right end. Find the shear at each end and the largest sagging moment in the span.",
                "Selepas moment distribution, satu span " + num(P.L) + " m yang memikul " + num(fmt(P.w, 1)) + " kN/m mempunyai hogging moment " + num(P.ML) + " kN m di hujung kiri dan " + num(P.MR) + " kN m di hujung kanan. Cari shear di setiap hujung dan sagging moment terbesar dalam span.");
    },
    fields: [{ id: "l", label: ["V<sub>L</sub>", "V<sub>L</sub>"], unit: "kN", fn: function (P) { return P.VL; }, rtol: 0.005 },
             { id: "r", label: ["V<sub>R</sub>", "V<sub>R</sub>"], unit: "kN", fn: function (P) { return P.VR; }, rtol: 0.005 },
             { id: "m", label: ["M<sub>span</sub>", "M<sub>span</sub>"], unit: "kN m", fn: function (P) { return P.Ms; }, rtol: 0.01, atol: 0.3 }],
    hints: [function () { return bi("Moments about the right end: V<sub>L</sub>L = wL²/2 + M<sub>L</sub> − M<sub>R</sub> (hogging magnitudes).", "Moment pada hujung kanan: V<sub>L</sub>L = wL²/2 + M<sub>L</sub> − M<sub>R</sub> (magnitud hogging)."); },
            function () { return bi("V<sub>R</sub> = wL − V<sub>L</sub>. The shear is zero at x₀ = V<sub>L</sub>/w from the left end.", "V<sub>R</sub> = wL − V<sub>L</sub>. Shear sifar pada x₀ = V<sub>L</sub>/w dari hujung kiri."); },
            function () { return bi("M<sub>span</sub> = V<sub>L</sub>x₀ − wx₀²/2 − M<sub>L</sub> = V<sub>L</sub>²/(2w) − M<sub>L</sub>. It can come out negative: the span then hogs throughout.", "M<sub>span</sub> = V<sub>L</sub>x₀ − wx₀²/2 − M<sub>L</sub> = V<sub>L</sub>²/(2w) − M<sub>L</sub>. Ia boleh menjadi negatif: span itu kemudian hogging di sepanjangnya."); }],
    solution: function (P) {
      return sol(["V<sub>L</sub> = " + fmt(P.w, 1) + " × " + P.L + "/2 + (" + P.ML + " − " + P.MR + ")/" + P.L + " = " + f2(P.w * P.L / 2) + " + (" + f2((P.ML - P.MR) / P.L) + ") = " + f2(P.VL) + " kN",
        "V<sub>R</sub> = " + fmt(P.w, 1) + " × " + P.L + " − " + f2(P.VL) + " = " + f2(P.VR) + " kN; " + bi("check", "semak") + " V<sub>L</sub> + V<sub>R</sub> = wL ✓",
        "x₀ = " + f2(P.VL) + "/" + fmt(P.w, 1) + " = " + fmt(P.x0, 3) + " m; M<sub>span</sub> = " + f2(P.VL) + "²/(2 × " + fmt(P.w, 1) + ") − " + P.ML + " = " + f2(P.Ms) + " kN m",
        P.Ms < 0 ? bi("Negative: the span hogs along its whole length and needs top bars across it (Notes §5).", "Negatif: span hogging di sepanjang panjangnya dan memerlukan bar atas merentasinya (Nota §5).")
                 : bi("Compare the free moment wL²/8 = " + f2(P.w * P.L * P.L / 8) + " kN m: the end moments take " + f2(P.w * P.L * P.L / 8 - P.Ms) + " kN m off it, a little less than their mean when they differ.", "Bandingkan free moment wL²/8 = " + f2(P.w * P.L * P.L / 8) + " kN m: moment hujung mengurangkannya sebanyak " + f2(P.w * P.L * P.L / 8 - P.Ms) + " kN m, sedikit kurang daripada puratanya apabila kedua-duanya berbeza.")]);
    }
  });

  /* ---------- B5 an interior column: the one-free-joint sub-frame ---------- */
  function colData(r, P) {
    P.bb = pick(r, [250, 300]); P.hb = pick(r, [500, 550, 600, 650]); P.bc = pick(r, [300, 350, 400]); P.hc = pick(r, [300, 400, 450, 500]);
    P.hu = pick(r, [3.0, 3.5, 4.0]); P.hl = pick(r, [3.5, 4.0, 4.5]);
    P.Ib = P.bb * Math.pow(P.hb, 3) / 12e9; P.Ic = P.bc * Math.pow(P.hc, 3) / 12e9; P.Kcu = 10 * P.Ic / P.hu; P.Kcl = 10 * P.Ic / P.hl;
  }
  EX.define("b5", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [5, 5.5, 6, 6.5, 7, 7.5, 8]); P.L2 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 8]);
      P.w1 = step(r, 45, 65, 0.5); P.n1 = step(r, 25, 36, 0.5); P.w2 = step(r, 45, 65, 0.5); P.n2 = step(r, 25, 36, 0.5);
      colData(r, P);
      P.K1 = 10 * P.Ib / P.L1; P.K2 = 10 * P.Ib / P.L2;
      P.fx1 = P.w1 * P.L1 * P.L1 / 12; P.fn1 = P.n1 * P.L1 * P.L1 / 12; P.fx2 = P.w2 * P.L2 * P.L2 / 12; P.fn2 = P.n2 * P.L2 * P.L2 / 12;
      P.da = P.fx1 - P.fn2; P.db = P.fx2 - P.fn1; P.D = Math.max(P.da, P.db);
      P.S = P.Kcu + P.Kcl + 0.5 * P.K1 + 0.5 * P.K2; P.Mu = P.D * P.Kcu / P.S; P.Ml = P.D * P.Kcl / P.S;
      return P;
    },
    text: function (P) {
      return bi("At the interior column B of a braced frame, the beam AB spans " + num(P.L1) + " m (w<sub>max</sub> = " + num(fmt(P.w1, 1)) + ", w<sub>min</sub> = " + num(fmt(P.n1, 1)) + " kN/m) and BC spans " + num(P.L2) + " m (w<sub>max</sub> = " + num(fmt(P.w2, 1)) + ", w<sub>min</sub> = " + num(fmt(P.n2, 1)) + " kN/m). Beams " + num(P.bb + " × " + P.hb) + "; column " + num(P.bc + " × " + P.hc) + " (" + P.hc + " in the plane of the frame), " + num(P.hu) + " m high above the floor and " + num(P.hl) + " m below. By the one-free-joint sub-frame, find ΔFEM and the moments in the upper and lower columns.",
                "Di column dalaman B sebuah braced frame, beam AB merentang " + num(P.L1) + " m (w<sub>max</sub> = " + num(fmt(P.w1, 1)) + ", w<sub>min</sub> = " + num(fmt(P.n1, 1)) + " kN/m) dan BC merentang " + num(P.L2) + " m (w<sub>max</sub> = " + num(fmt(P.w2, 1)) + ", w<sub>min</sub> = " + num(fmt(P.n2, 1)) + " kN/m). Beam " + num(P.bb + " × " + P.hb) + "; column " + num(P.bc + " × " + P.hc) + " (" + P.hc + " dalam satah frame), setinggi " + num(P.hu) + " m di atas lantai dan " + num(P.hl) + " m di bawah. Melalui one-free-joint sub-frame, cari ΔFEM dan moment dalam column atas dan bawah.");
    },
    fields: [{ id: "d", label: ["ΔFEM", "ΔFEM"], unit: "kN m", fn: function (P) { return P.D; }, rtol: 0.01 },
             { id: "u", label: ["M<sub>c,u</sub>", "M<sub>c,u</sub>"], unit: "kN m", fn: function (P) { return P.Mu; }, rtol: 0.015 },
             { id: "l", label: ["M<sub>c,l</sub>", "M<sub>c,l</sub>"], unit: "kN m", fn: function (P) { return P.Ml; }, rtol: 0.015 }],
    hints: [function () { return bi("w<sub>max</sub> on one side, w<sub>min</sub> on the other: work out both arrangements and keep the larger ΔFEM = FEM(w<sub>max</sub> side) − FEM(w<sub>min</sub> side).", "w<sub>max</sub> pada satu sisi, w<sub>min</sub> pada sisi lain: kira kedua-dua susunan dan kekalkan ΔFEM yang lebih besar = FEM(sisi w<sub>max</sub>) − FEM(sisi w<sub>min</sub>)."); },
            function () { return bi("K = 10I/L with I = bh³/12 in 10⁹ mm⁴ and L in m; the upper column with the storey above, the lower with the storey below.", "K = 10I/L dengan I = bh³/12 dalam 10⁹ mm⁴ dan L dalam m; column atas dengan tingkat di atas, column bawah dengan tingkat di bawah."); },
            function () { return bi("ΣK = K<sub>c,u</sub> + K<sub>c,l</sub> + ½K<sub>AB</sub> + ½K<sub>BC</sub> (full I/L, halved; not ¾); M<sub>c</sub> = ΔFEM × K<sub>c</sub>/ΣK.", "ΣK = K<sub>c,u</sub> + K<sub>c,l</sub> + ½K<sub>AB</sub> + ½K<sub>BC</sub> (I/L penuh, dibahagi dua; bukan ¾); M<sub>c</sub> = ΔFEM × K<sub>c</sub>/ΣK."); }],
    solution: function (P) {
      return sol(["FEM: AB " + f2(P.fx1) + " / " + f2(P.fn1) + ", BC " + f2(P.fx2) + " / " + f2(P.fn2) + " kN m (w<sub>max</sub> / w<sub>min</sub>)",
        "ΔFEM = max(" + f2(P.fx1) + " − " + f2(P.fn2) + ", " + f2(P.fx2) + " − " + f2(P.fn1) + ") = max(" + f2(P.da) + ", " + f2(P.db) + ") = " + f2(P.D) + " kN m (" + (P.da >= P.db ? bi("AB loaded, BC light", "AB dibebani, BC ringan") : bi("BC loaded, AB light", "BC dibebani, AB ringan")) + ")",
        "I<sub>b</sub> = " + fmt(P.Ib, 3) + ", I<sub>c</sub> = " + fmt(P.Ic, 3) + " × 10⁹ mm⁴; K<sub>AB</sub> = " + f2(P.K1) + ", K<sub>BC</sub> = " + f2(P.K2) + ", K<sub>c,u</sub> = " + f2(P.Kcu) + ", K<sub>c,l</sub> = " + f2(P.Kcl),
        "ΣK = " + f2(P.Kcu) + " + " + f2(P.Kcl) + " + ½ × " + f2(P.K1) + " + ½ × " + f2(P.K2) + " = " + f2(P.S),
        "M<sub>c,u</sub> = " + f2(P.D) + " × " + f2(P.Kcu) + "/" + f2(P.S) + " = " + f2(P.Mu) + " kN m; M<sub>c,l</sub> = " + f2(P.D) + " × " + f2(P.Kcl) + "/" + f2(P.S) + " = " + f2(P.Ml) + " kN m"]);
    }
  });

  /* ---------- B6 an end column and the beam at the end support ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [5, 5.5, 6, 6.5, 7, 7.5, 8]); P.w1 = step(r, 45, 65, 0.5);
      colData(r, P);
      P.K1 = 10 * P.Ib / P.L1; P.D = P.w1 * P.L1 * P.L1 / 12; P.S = P.Kcu + P.Kcl + 0.5 * P.K1;
      P.Mu = P.D * P.Kcu / P.S; P.Ml = P.D * P.Kcl / P.S; P.Me = P.Mu + P.Ml;
      return P;
    },
    text: function (P) {
      return bi("At the end column A of a braced frame, the end span AB is " + num(P.L1) + " m long and carries w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m. Beam " + num(P.bb + " × " + P.hb) + "; column " + num(P.bc + " × " + P.hc) + " (" + P.hc + " in the plane of the frame), " + num(P.hu) + " m high above the floor and " + num(P.hl) + " m below. Find the column moments by the one-free-joint sub-frame, and the hogging moment the beam carries at A.",
                "Di column hujung A sebuah braced frame, span hujung AB sepanjang " + num(P.L1) + " m dan memikul w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m. Beam " + num(P.bb + " × " + P.hb) + "; column " + num(P.bc + " × " + P.hc) + " (" + P.hc + " dalam satah frame), setinggi " + num(P.hu) + " m di atas lantai dan " + num(P.hl) + " m di bawah. Cari moment column melalui one-free-joint sub-frame, dan hogging moment yang dipikul beam di A.");
    },
    fields: [{ id: "u", label: ["M<sub>c,u</sub>", "M<sub>c,u</sub>"], unit: "kN m", fn: function (P) { return P.Mu; }, rtol: 0.015 },
             { id: "l", label: ["M<sub>c,l</sub>", "M<sub>c,l</sub>"], unit: "kN m", fn: function (P) { return P.Ml; }, rtol: 0.015 },
             { id: "e", label: ["beam at A", "beam di A"], unit: "kN m", fn: function (P) { return P.Me; }, rtol: 0.015 }],
    hints: [function () { return bi("An end column has one beam only: the whole fixed-end moment of AB at w<sub>max</sub> is out of balance.", "Column hujung hanya mempunyai satu beam: seluruh fixed-end moment AB pada w<sub>max</sub> tidak seimbang."); },
            function () { return bi("ΣK = K<sub>c,u</sub> + K<sub>c,l</sub> + ½K<sub>AB</sub>, with K = 10I/L.", "ΣK = K<sub>c,u</sub> + K<sub>c,l</sub> + ½K<sub>AB</sub>, dengan K = 10I/L."); },
            function () { return bi("By equilibrium of the joint the beam end carries the sum of the two column moments.", "Melalui keseimbangan joint, hujung beam memikul jumlah dua moment column."); }],
    solution: function (P) {
      return sol(["ΔFEM = " + fmt(P.w1, 1) + " × " + P.L1 + "²/12 = " + f2(P.D) + " kN m",
        "K<sub>AB</sub> = 10 × " + fmt(P.Ib, 3) + "/" + P.L1 + " = " + f2(P.K1) + "; K<sub>c,u</sub> = 10 × " + fmt(P.Ic, 3) + "/" + P.hu + " = " + f2(P.Kcu) + "; K<sub>c,l</sub> = 10 × " + fmt(P.Ic, 3) + "/" + P.hl + " = " + f2(P.Kcl),
        "ΣK = " + f2(P.Kcu) + " + " + f2(P.Kcl) + " + ½ × " + f2(P.K1) + " = " + f2(P.S) + "; M<sub>c,u</sub> = " + f2(P.Mu) + ", M<sub>c,l</sub> = " + f2(P.Ml) + " kN m",
        bi("Beam at A: " + f2(P.Mu) + " + " + f2(P.Ml) + " = " + f2(P.Me) + " kN m of hogging. The continuous beam showed zero here; the top bars at A must take this moment (Notes §6).", "Beam di A: " + f2(P.Mu) + " + " + f2(P.Ml) + " = " + f2(P.Me) + " kN m hogging. Continuous beam menunjukkan sifar di sini; bar atas di A mesti memikul moment ini (Nota §6).")]);
    }
  });
  EX.ready();
})();
