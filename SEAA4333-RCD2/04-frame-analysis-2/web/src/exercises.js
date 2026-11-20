/* SEAA 4333 Unit 4 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method (the RC Design app's frame model, sub-frames of RDF §11.0):
   K = I/L written 10I/L (I in 10^9 mm^4, L or h in m); one-level sub-frame: full K for every beam, the columns in sum K;
   F = K / (K_b,L + K_b,R + K_c,u + K_c,l); balance -F U at every free joint, columns included; carry 1/2 along the beams;
   two-free-joint sub-frame of beam AB: the neighbour BC at 1/2 K with its far end fixed, nothing carried to fixed ends;
   column moments from the final beam moments: M_c = -(M_L + M_R) K_c / (K_c,u + K_c,l); far end of a column 1/2 M_c;
   span statics with hogging magnitudes: V_L = wL/2 + (M_L - M_R)/L, x0 = V_L/w, M_span = V_L^2/(2w) - M_L. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function f2(v) { return fmt(v, 2); }
  function f3(v) { return fmt(v, 3); }
  function sg(v) { return (v >= 0 ? "+" : "") + f2(v); }
  function colData(r, P) {
    P.bb = pick(r, [250, 300]); P.hb = pick(r, [500, 550, 600, 650]); P.bc = pick(r, [300, 350, 400]); P.hc = pick(r, [300, 400, 450, 500]);
    P.hu = pick(r, [3.0, 3.5, 4.0]); P.hl = pick(r, [3.5, 4.0, 4.5]);
    P.Ib = P.bb * Math.pow(P.hb, 3) / 12e9; P.Ic = P.bc * Math.pow(P.hc, 3) / 12e9; P.Kcu = 10 * P.Ic / P.hu; P.Kcl = 10 * P.Ic / P.hl;
  }
  function secText(P) {
    return bi("Beams " + num(P.bb + " × " + P.hb) + "; columns " + num(P.bc + " × " + P.hc) + " (" + P.hc + " in the plane of the frame), " + num(P.hu) + " m high above the floor and " + num(P.hl) + " m below, their far ends fixed.",
              "Beam " + num(P.bb + " × " + P.hb) + "; column " + num(P.bc + " × " + P.hc) + " (" + P.hc + " dalam satah frame), setinggi " + num(P.hu) + " m di atas lantai dan " + num(P.hl) + " m di bawah, dengan hujung jauh fixed.");
  }
  function kLine(P, beams) {
    return "I<sub>b</sub> = " + P.bb + " × " + P.hb + "³/12 = " + f3(P.Ib) + ", I<sub>c</sub> = " + P.bc + " × " + P.hc + "³/12 = " + f3(P.Ic) + " × 10⁹ mm⁴; " + beams +
      "K<sub>c,u</sub> = 10 × " + f3(P.Ic) + "/" + P.hu + " = " + f3(P.Kcu) + ", K<sub>c,l</sub> = 10 × " + f3(P.Ic) + "/" + P.hl + " = " + f3(P.Kcl);
  }

  /* ---------- B1 distribution factors at an interior joint of a one-level sub-frame ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]); P.L2 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]);
      colData(r, P);
      P.K1 = 10 * P.Ib / P.L1; P.K2 = 10 * P.Ib / P.L2; P.S = P.K1 + P.K2 + P.Kcu + P.Kcl;
      P.F1 = P.K1 / P.S; P.F2 = P.K2 / P.S; P.Fu = P.Kcu / P.S; P.Fl = P.Kcl / P.S;
      return P;
    },
    text: function (P) {
      return bi("In the one-level sub-frame of a braced frame, the interior joint B joins the beam AB of " + num(P.L1) + " m, the beam BC of " + num(P.L2) + " m and the columns above and below. ",
                "Dalam one-level sub-frame sebuah braced frame, joint dalaman B menyambungkan beam AB sepanjang " + num(P.L1) + " m, beam BC sepanjang " + num(P.L2) + " m dan column di atas dan di bawah. ") + secText(P) +
        bi(" Find the distribution factors F<sub>BA</sub>, F<sub>BC</sub> and F<sub>c,u</sub> at B.", " Cari distribution factor F<sub>BA</sub>, F<sub>BC</sub> dan F<sub>c,u</sub> di B.");
    },
    fields: [{ id: "a", label: ["F<sub>BA</sub>", "F<sub>BA</sub>"], unit: "", fn: function (P) { return P.F1; }, rtol: 0.01 },
             { id: "c", label: ["F<sub>BC</sub>", "F<sub>BC</sub>"], unit: "", fn: function (P) { return P.F2; }, rtol: 0.01 },
             { id: "u", label: ["F<sub>c,u</sub>", "F<sub>c,u</sub>"], unit: "", fn: function (P) { return P.Fu; }, rtol: 0.01 }],
    hints: [function () { return bi("K = 10I/L for every member, with I = bh³/12 in 10⁹ mm⁴: the beams with their spans, the columns with their storey heights.", "K = 10I/L bagi setiap member, dengan I = bh³/12 dalam 10⁹ mm⁴: beam dengan span-nya, column dengan ketinggian tingkatnya."); },
            function () { return bi("In the one-level sub-frame every beam keeps its full K (no ¾, no ½), and the two columns are members of the joint.", "Dalam one-level sub-frame setiap beam mengekalkan K penuhnya (tiada ¾, tiada ½), dan dua column ialah member joint."); },
            function () { return bi("F = K/ΣK with ΣK = K<sub>AB</sub> + K<sub>BC</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; the four factors add up to 1.", "F = K/ΣK dengan ΣK = K<sub>AB</sub> + K<sub>BC</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; empat faktor berjumlah 1."); }],
    solution: function (P) {
      return sol([kLine(P, "K<sub>AB</sub> = 10 × " + f3(P.Ib) + "/" + P.L1 + " = " + f3(P.K1) + ", K<sub>BC</sub> = 10 × " + f3(P.Ib) + "/" + P.L2 + " = " + f3(P.K2) + ", "),
        "ΣK = " + f3(P.K1) + " + " + f3(P.K2) + " + " + f3(P.Kcu) + " + " + f3(P.Kcl) + " = " + f3(P.S),
        "F<sub>BA</sub> = " + f3(P.F1) + ", F<sub>BC</sub> = " + f3(P.F2) + ", F<sub>c,u</sub> = " + f3(P.Fu) + ", F<sub>c,l</sub> = " + f3(P.Fl) + bi("; check: they add up to 1.", "; semak: jumlahnya 1.")]);
    }
  });

  /* ---------- B2 the first balance at an end joint of a one-level sub-frame ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.L = pick(r, [5, 5.5, 6, 6.5, 7, 7.5, 8]); P.w = step(r, 40, 65, 0.5);
      colData(r, P);
      P.K = 10 * P.Ib / P.L; P.S = P.K + P.Kcu + P.Kcl; P.F = P.K / P.S; P.Fu = P.Kcu / P.S;
      P.fem = P.w * P.L * P.L / 12; P.bA = P.fem * P.F; P.bu = P.fem * P.Fu; P.co = P.bA / 2;
      return P;
    },
    text: function (P) {
      return bi("In the one-level sub-frame of a braced frame, the end span AB is " + num(P.L) + " m long and carries " + num(fmt(P.w, 1)) + " kN/m in this load case. At the end joint A it meets a column above and a column below. ",
                "Dalam one-level sub-frame sebuah braced frame, span hujung AB sepanjang " + num(P.L) + " m dan memikul " + num(fmt(P.w, 1)) + " kN/m dalam kes load ini. Di joint hujung A ia bertemu column di atas dan column di bawah. ") + secText(P) +
        bi(" In the first row of the distribution, find F<sub>AB</sub>, the balancing moment at AB and the balancing moment in the upper column at A (clockwise positive).", " Dalam baris pertama distribution, cari F<sub>AB</sub>, balancing moment di AB dan balancing moment dalam column atas di A (positif mengikut arah jam).");
    },
    fields: [{ id: "f", label: ["F<sub>AB</sub>", "F<sub>AB</sub>"], unit: "", fn: function (P) { return P.F; }, rtol: 0.01 },
             { id: "b", label: ["balance at AB", "imbangan di AB"], unit: "kN m", fn: function (P) { return P.bA; }, rtol: 0.015, atol: 0.2 },
             { id: "u", label: ["balance in the upper column", "imbangan dalam column atas"], unit: "kN m", fn: function (P) { return P.bu; }, rtol: 0.015, atol: 0.2 }],
    hints: [function () { return bi("A is a joint with columns, not a pin: AB keeps its full K, and ΣK at A = K<sub>AB</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>.", "A ialah joint dengan column, bukan pin: AB mengekalkan K penuhnya, dan ΣK di A = K<sub>AB</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>."); },
            function () { return bi("At A only AB brings a fixed-end moment: FEM<sub>AB</sub> = −wL²/12 (left end, clockwise positive), so U = FEM<sub>AB</sub>.", "Di A hanya AB membawa fixed-end moment: FEM<sub>AB</sub> = −wL²/12 (hujung kiri, positif mengikut arah jam), jadi U = FEM<sub>AB</sub>."); },
            function () { return bi("Each member takes −F × U: positive here, since U is negative.", "Setiap member mengambil −F × U: positif di sini, kerana U negatif."); }],
    solution: function (P) {
      return sol([kLine(P, "K<sub>AB</sub> = 10 × " + f3(P.Ib) + "/" + P.L + " = " + f3(P.K) + ", "),
        "ΣK<sub>A</sub> = " + f3(P.K) + " + " + f3(P.Kcu) + " + " + f3(P.Kcl) + " = " + f3(P.S) + "; F<sub>AB</sub> = " + f3(P.F) + ", F<sub>c,u</sub> = " + f3(P.Fu),
        "FEM<sub>AB</sub> = −" + fmt(P.w, 1) + " × " + P.L + "²/12 = −" + f2(P.fem) + " kN m = U",
        bi("Balance at AB = −(−" + f2(P.fem) + ") × " + f3(P.F) + " = +" + f2(P.bA) + " kN m; upper column = +" + f2(P.fem) + " × " + f3(P.Fu) + " = +" + f2(P.bu) + " kN m", "Imbangan di AB = −(−" + f2(P.fem) + ") × " + f3(P.F) + " = +" + f2(P.bA) + " kN m; column atas = +" + f2(P.fem) + " × " + f3(P.Fu) + " = +" + f2(P.bu) + " kN m"),
        bi("In the next row half of the balance at AB, +" + f2(P.co) + " kN m, is carried to BA; the column keeps its share (Notes §2).", "Dalam baris seterusnya separuh imbangan di AB, +" + f2(P.co) + " kN m, dibawa ke BA; column menyimpan bahagiannya (Nota §2).")]);
    }
  });

  /* ---------- B3 half stiffness in the two-free-joint sub-frame of an end beam ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]); P.L2 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]);
      colData(r, P);
      P.K1 = 10 * P.Ib / P.L1; P.K2 = 10 * P.Ib / P.L2; P.K2h = 0.5 * P.K2; P.S = P.K1 + P.K2h + P.Kcu + P.Kcl;
      P.F1 = P.K1 / P.S; P.F2 = P.K2h / P.S;
      return P;
    },
    text: function (P) {
      return bi("The two-free-joint sub-frame of the end beam AB of a floor: AB is " + num(P.L1) + " m long and the next beam BC " + num(P.L2) + " m; BC is fixed at its far end C. ",
                "Two-free-joint sub-frame bagi beam hujung AB sesuatu lantai: AB sepanjang " + num(P.L1) + " m dan beam seterusnya BC " + num(P.L2) + " m; BC fixed di hujung jauhnya C. ") + secText(P) +
        bi(" Find the stiffness taken for BC, and the distribution factors F<sub>BA</sub> and F<sub>BC</sub> at B.", " Cari stiffness yang diambil bagi BC, dan distribution factor F<sub>BA</sub> dan F<sub>BC</sub> di B.");
    },
    fields: [{ id: "k", label: ["K taken for BC", "K yang diambil bagi BC"], unit: "", fn: function (P) { return P.K2h; }, rtol: 0.01 },
             { id: "a", label: ["F<sub>BA</sub>", "F<sub>BA</sub>"], unit: "", fn: function (P) { return P.F1; }, rtol: 0.01 },
             { id: "c", label: ["F<sub>BC</sub>", "F<sub>BC</sub>"], unit: "", fn: function (P) { return P.F2; }, rtol: 0.01 }],
    hints: [function () { return bi("The beam of interest keeps its full K; a neighbour fixed at its far end is taken at ½K (RDF §11.0).", "Beam yang dikaji mengekalkan K penuhnya; jiran yang fixed di hujung jauhnya diambil pada ½K (RDF §11.0)."); },
            function () { return bi("K = 10I/L with I = bh³/12 in 10⁹ mm⁴; for the columns use their storey heights.", "K = 10I/L dengan I = bh³/12 dalam 10⁹ mm⁴; bagi column gunakan ketinggian tingkatnya."); },
            function () { return bi("ΣK at B = K<sub>AB</sub> + ½K<sub>BC</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; F = K/ΣK, with ½K<sub>BC</sub> for BC.", "ΣK di B = K<sub>AB</sub> + ½K<sub>BC</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; F = K/ΣK, dengan ½K<sub>BC</sub> bagi BC."); }],
    solution: function (P) {
      return sol([kLine(P, "K<sub>AB</sub> = " + f3(P.K1) + ", K<sub>BC</sub> = 10 × " + f3(P.Ib) + "/" + P.L2 + " = " + f3(P.K2) + bi(", taken at ½K = ", ", diambil pada ½K = ") + f3(P.K2h) + "; "),
        "ΣK<sub>B</sub> = " + f3(P.K1) + " + " + f3(P.K2h) + " + " + f3(P.Kcu) + " + " + f3(P.Kcl) + " = " + f3(P.S),
        "F<sub>BA</sub> = " + f3(P.K1) + "/" + f3(P.S) + " = " + f3(P.F1) + "; F<sub>BC</sub> = " + f3(P.K2h) + "/" + f3(P.S) + " = " + f3(P.F2) + "; F<sub>c,u</sub> = " + f3(P.Kcu / P.S) + ", F<sub>c,l</sub> = " + f3(P.Kcl / P.S),
        bi("With BC at full K, F<sub>BA</sub> would be " + f3(P.K1 / (P.S + P.K2h)) + ": too small, and the beam’s own moments with it (Frame S4).", "Dengan BC pada K penuh, F<sub>BA</sub> menjadi " + f3(P.K1 / (P.S + P.K2h)) + ": terlalu kecil, begitu juga moment beam itu (Frame S4).")]);
    }
  });

  /* ---------- B4 column moments from the final beam moments ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = {};
      P.x = step(r, 120, 260, 0.1);
      var f = step(r, 0.55, 1.4, 0.01); if (Math.abs(f - 1) < 0.06) f = f < 1 ? 0.88 : 1.12;
      P.y = +(P.x * f).toFixed(1);
      colData(r, P);
      P.U = P.x - P.y; P.Mu = -P.U * P.Kcu / (P.Kcu + P.Kcl); P.Ml = -P.U * P.Kcl / (P.Kcu + P.Kcl); P.far = P.Mu / 2;
      return P;
    },
    text: function (P) {
      return bi("After the moment distribution of a one-level sub-frame, the final end moments at the interior joint B are M<sub>BA</sub> = +" + num(fmt(P.x, 1)) + " and M<sub>BC</sub> = −" + num(fmt(P.y, 1)) + " kN m (clockwise positive). ",
                "Selepas moment distribution satu one-level sub-frame, moment hujung akhir di joint dalaman B ialah M<sub>BA</sub> = +" + num(fmt(P.x, 1)) + " dan M<sub>BC</sub> = −" + num(fmt(P.y, 1)) + " kN m (positif mengikut arah jam). ") + secText(P) +
        bi(" Find the column moments at B, above and below, and the moment at the top of the upper column (sign as in the table).", " Cari moment column di B, di atas dan di bawah, dan moment di atas column atas (tanda seperti dalam jadual).");
    },
    fields: [{ id: "u", label: ["M<sub>c,u</sub>", "M<sub>c,u</sub>"], unit: "kN m", fn: function (P) { return P.Mu; }, rtol: 0.015, atol: 0.15 },
             { id: "l", label: ["M<sub>c,l</sub>", "M<sub>c,l</sub>"], unit: "kN m", fn: function (P) { return P.Ml; }, rtol: 0.015, atol: 0.15 },
             { id: "t", label: ["top of the upper column", "atas column atas"], unit: "kN m", fn: function (P) { return P.far; }, rtol: 0.015, atol: 0.1 }],
    hints: [function () { return bi("The joint is in equilibrium: M<sub>BA</sub> + M<sub>BC</sub> + M<sub>c,u</sub> + M<sub>c,l</sub> = 0.", "Joint dalam keseimbangan: M<sub>BA</sub> + M<sub>BC</sub> + M<sub>c,u</sub> + M<sub>c,l</sub> = 0."); },
            function () { return bi("Every balance gives the two columns shares in the ratio K<sub>c,u</sub> : K<sub>c,l</sub>, so share −(M<sub>BA</sub> + M<sub>BC</sub>) in that ratio, not with ΣK of the joint.", "Setiap imbangan memberi dua column bahagian dalam nisbah K<sub>c,u</sub> : K<sub>c,l</sub>, jadi bahagikan −(M<sub>BA</sub> + M<sub>BC</sub>) dalam nisbah itu, bukan dengan ΣK joint."); },
            function () { return bi("The far end of a column is fixed: it takes half of the column’s moment at the floor, with the same sign.", "Hujung jauh column adalah fixed: ia mengambil separuh moment column di lantai, dengan tanda yang sama."); }],
    solution: function (P) {
      return sol(["I<sub>c</sub> = " + P.bc + " × " + P.hc + "³/12 = " + f3(P.Ic) + " × 10⁹ mm⁴; K<sub>c,u</sub> = " + f3(P.Kcu) + ", K<sub>c,l</sub> = " + f3(P.Kcl),
        "M<sub>BA</sub> + M<sub>BC</sub> = " + fmt(P.x, 1) + " − " + fmt(P.y, 1) + " = " + sg(P.U) + bi(" kN m; the columns hold ", " kN m; column memegang ") + sg(-P.U),
        "M<sub>c,u</sub> = " + sg(-P.U) + " × " + f3(P.Kcu) + "/" + f3(P.Kcu + P.Kcl) + " = " + sg(P.Mu) + " kN m; M<sub>c,l</sub> = " + sg(-P.U) + " × " + f3(P.Kcl) + "/" + f3(P.Kcu + P.Kcl) + " = " + sg(P.Ml) + " kN m",
        bi("Top of the upper column: ½ × (" + sg(P.Mu) + ") = " + sg(P.far) + " kN m; foot of the lower column: " + sg(P.Ml / 2) + " kN m (4.3).", "Atas column atas: ½ × (" + sg(P.Mu) + ") = " + sg(P.far) + " kN m; kaki column bawah: " + sg(P.Ml / 2) + " kN m (4.3).")]);
    }
  });

  /* ---------- B5 shears and the span moment with hogging at both ends ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P = {};
      P.L = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]); P.w = step(r, 25, 65, 0.5);
      var fem = P.w * P.L * P.L / 12; P.ML = Math.round(fem * step(r, 0.3, 1.1, 0.05)); P.MR = Math.round(fem * step(r, 0.3, 1.25, 0.05));
      P.VL = P.w * P.L / 2 + (P.ML - P.MR) / P.L; P.VR = P.w * P.L - P.VL; P.x0 = P.VL / P.w; P.Ms = P.VL * P.VL / (2 * P.w) - P.ML;
      return P;
    },
    text: function (P) {
      return bi("A beam of a two-free-joint sub-frame spans " + num(P.L) + " m and carries " + num(fmt(P.w, 1)) + " kN/m. After the distribution its end moments are " + num(P.ML) + " kN m of hogging at the left end and " + num(P.MR) + " kN m at the right end. Find the shear at the left end, the position of the largest sagging moment from the left end, and the largest sagging moment.",
                "Satu beam two-free-joint sub-frame merentang " + num(P.L) + " m dan memikul " + num(fmt(P.w, 1)) + " kN/m. Selepas distribution, moment hujungnya ialah hogging " + num(P.ML) + " kN m di hujung kiri dan " + num(P.MR) + " kN m di hujung kanan. Cari shear di hujung kiri, kedudukan sagging moment terbesar dari hujung kiri, dan sagging moment terbesar.");
    },
    fields: [{ id: "v", label: ["V<sub>L</sub>", "V<sub>L</sub>"], unit: "kN", fn: function (P) { return P.VL; }, rtol: 0.005 },
             { id: "x", label: ["x₀", "x₀"], unit: "m", fn: function (P) { return P.x0; }, rtol: 0.01 },
             { id: "m", label: ["M<sub>span</sub>", "M<sub>span</sub>"], unit: "kN m", fn: function (P) { return P.Ms; }, rtol: 0.01, atol: 0.3 }],
    hints: [function () { return bi("Moments about the right end: V<sub>L</sub>L = wL²/2 + M<sub>L</sub> − M<sub>R</sub> (hogging magnitudes).", "Moment pada hujung kanan: V<sub>L</sub>L = wL²/2 + M<sub>L</sub> − M<sub>R</sub> (magnitud hogging)."); },
            function () { return bi("The shear is zero at x₀ = V<sub>L</sub>/w from the left end: the largest sagging is there.", "Shear sifar pada x₀ = V<sub>L</sub>/w dari hujung kiri: sagging terbesar berada di situ."); },
            function () { return bi("M<sub>span</sub> = V<sub>L</sub>x₀ − wx₀²/2 − M<sub>L</sub> = V<sub>L</sub>²/(2w) − M<sub>L</sub>. Do not drop M<sub>L</sub>: in a sub-frame both ends hog.", "M<sub>span</sub> = V<sub>L</sub>x₀ − wx₀²/2 − M<sub>L</sub> = V<sub>L</sub>²/(2w) − M<sub>L</sub>. Jangan tinggalkan M<sub>L</sub>: dalam sub-frame kedua-dua hujung hogging."); }],
    solution: function (P) {
      return sol(["V<sub>L</sub> = " + fmt(P.w, 1) + " × " + P.L + "/2 + (" + P.ML + " − " + P.MR + ")/" + P.L + " = " + f2(P.w * P.L / 2) + " + (" + f2((P.ML - P.MR) / P.L) + ") = " + f2(P.VL) + " kN; V<sub>R</sub> = " + f2(P.VR) + " kN",
        "x₀ = " + f2(P.VL) + "/" + fmt(P.w, 1) + " = " + fmt(P.x0, 3) + " m",
        "M<sub>span</sub> = " + f2(P.VL) + "²/(2 × " + fmt(P.w, 1) + ") − " + P.ML + " = " + f2(P.VL * P.VL / (2 * P.w)) + " − " + P.ML + " = " + f2(P.Ms) + " kN m",
        P.Ms < 0 ? bi("Negative: the span hogs along its whole length and needs top bars across it.", "Negatif: span hogging di sepanjang panjangnya dan memerlukan bar atas merentasinya.")
                 : bi("Without M<sub>L</sub> the sheet would show " + f2(P.VL * P.VL / (2 * P.w)) + " kN m, the slip of Frame S4.", "Tanpa M<sub>L</sub> helaian akan menunjukkan " + f2(P.VL * P.VL / (2 * P.w)) + " kN m, kesilapan Frame S4.")]);
    }
  });

  /* ---------- B6 the first row of the two-free-joint sub-frame of an end beam ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.L1 = pick(r, [5, 5.5, 6, 6.5, 7, 7.5, 8]); P.L2 = pick(r, [4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]);
      P.w1 = step(r, 45, 65, 0.5); P.w2 = step(r, 25, 38, 0.5);
      colData(r, P);
      P.K1 = 10 * P.Ib / P.L1; P.K2h = 0.5 * 10 * P.Ib / P.L2;
      P.SA = P.K1 + P.Kcu + P.Kcl; P.FA = P.K1 / P.SA;
      P.SB = P.K1 + P.K2h + P.Kcu + P.Kcl; P.FB = P.K1 / P.SB; P.FBu = P.Kcu / P.SB;
      P.f1 = P.w1 * P.L1 * P.L1 / 12; P.f2 = P.w2 * P.L2 * P.L2 / 12; P.UB = P.f1 - P.f2;
      P.bA = P.f1 * P.FA; P.bB = -P.UB * P.FB; P.bBu = -P.UB * P.FBu;
      return P;
    },
    text: function (P) {
      return bi("The two-free-joint sub-frame of the end beam AB, loaded for the largest sagging in AB: AB = " + num(P.L1) + " m at w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m; BC = " + num(P.L2) + " m at w<sub>min</sub> = " + num(fmt(P.w2, 1)) + " kN/m, fixed at its far end C. ",
                "Two-free-joint sub-frame bagi beam hujung AB, dibebani bagi sagging terbesar dalam AB: AB = " + num(P.L1) + " m pada w<sub>max</sub> = " + num(fmt(P.w1, 1)) + " kN/m; BC = " + num(P.L2) + " m pada w<sub>min</sub> = " + num(fmt(P.w2, 1)) + " kN/m, fixed di hujung jauhnya C. ") + secText(P) +
        bi(" In the first row, find the balancing moments at AB (joint A) and at BA (joint B), and the balancing moment in the upper column at B (clockwise positive).", " Dalam baris pertama, cari balancing moment di AB (joint A) dan di BA (joint B), serta balancing moment dalam column atas di B (positif mengikut arah jam).");
    },
    fields: [{ id: "a", label: ["balance at AB", "imbangan di AB"], unit: "kN m", fn: function (P) { return P.bA; }, rtol: 0.015, atol: 0.2 },
             { id: "b", label: ["balance at BA", "imbangan di BA"], unit: "kN m", fn: function (P) { return P.bB; }, rtol: 0.015, atol: 0.2 },
             { id: "u", label: ["balance in the upper column at B", "imbangan dalam column atas di B"], unit: "kN m", fn: function (P) { return P.bBu; }, rtol: 0.015, atol: 0.2 }],
    hints: [function () { return bi("ΣK at A = K<sub>AB</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; at B add ½K<sub>BC</sub> (the neighbour, fixed at C).", "ΣK di A = K<sub>AB</sub> + K<sub>c,u</sub> + K<sub>c,l</sub>; di B tambah ½K<sub>BC</sub> (jiran, fixed di C)."); },
            function () { return bi("FEM: AB −w<sub>1</sub>L<sub>1</sub>²/12 at A and +w<sub>1</sub>L<sub>1</sub>²/12 at B; BC −w<sub>2</sub>L<sub>2</sub>²/12 at B.", "FEM: AB −w<sub>1</sub>L<sub>1</sub>²/12 di A dan +w<sub>1</sub>L<sub>1</sub>²/12 di B; BC −w<sub>2</sub>L<sub>2</sub>²/12 di B."); },
            function () { return bi("U<sub>A</sub> = FEM<sub>AB</sub>; U<sub>B</sub> = FEM<sub>BA</sub> + FEM<sub>BC</sub>; each member takes −F × U at its joint.", "U<sub>A</sub> = FEM<sub>AB</sub>; U<sub>B</sub> = FEM<sub>BA</sub> + FEM<sub>BC</sub>; setiap member mengambil −F × U di joint-nya."); }],
    solution: function (P) {
      return sol([kLine(P, "K<sub>AB</sub> = " + f3(P.K1) + ", ½K<sub>BC</sub> = " + f3(P.K2h) + "; "),
        "ΣK<sub>A</sub> = " + f3(P.SA) + ", F<sub>AB</sub> = " + f3(P.FA) + "; ΣK<sub>B</sub> = " + f3(P.SB) + ", F<sub>BA</sub> = " + f3(P.FB) + ", F<sub>c,u</sub> = " + f3(P.FBu),
        "FEM<sub>AB</sub> = −" + f2(P.f1) + ", FEM<sub>BA</sub> = +" + f2(P.f1) + ", FEM<sub>BC</sub> = −" + f2(P.f2) + " kN m; U<sub>B</sub> = " + sg(P.UB) + " kN m",
        bi("Balance at AB = +" + f2(P.f1) + " × " + f3(P.FA) + " = " + sg(P.bA) + "; at BA = −(" + sg(P.UB) + ") × " + f3(P.FB) + " = " + sg(P.bB) + "; upper column at B = " + sg(P.bBu) + " kN m",
           "Imbangan di AB = +" + f2(P.f1) + " × " + f3(P.FA) + " = " + sg(P.bA) + "; di BA = −(" + sg(P.UB) + ") × " + f3(P.FB) + " = " + sg(P.bB) + "; column atas di B = " + sg(P.bBu) + " kN m"),
        bi("Next row: half of each beam balance crosses AB (" + sg(P.bB / 2) + " to AB, " + sg(P.bA / 2) + " to BA); the balance on BC at B is not carried over, because C is fixed.", "Baris seterusnya: separuh setiap imbangan beam menyeberangi AB (" + sg(P.bB / 2) + " ke AB, " + sg(P.bA / 2) + " ke BA); imbangan pada BC di B tidak dibawa, kerana C adalah fixed.")]);
    }
  });
  EX.ready();
})();
