/* SEAA 4333 Unit 11 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's foundation module):
   strap footing, service: W_A = 0.1 N_A, W_B = 0.1 N_B, W_R = 25 b h (L - c_A/2 - c_B/2) between the column faces at
   x_R = (L - c_A/2 - c_B/2)/2 + c_B/2 from column B; e = L_A/2 - c_A/2; R_A = W_A + (N_A L + W_R x_R)/(L - e);
   R_B = N_A + N_B + W_A + W_B + W_R - R_A; B_A = R_A/(q L_A); S_B = sqrt(R_B/q);
   strap, ultimate: R_A,Ed = (N_A,Ed L + 1.35 W_R x_R)/(L - e), w_A = R_A,Ed/L_A, w_r = 1.35 W_R/(strap length),
   x_0 = (N_A,Ed - w_r c_A)/(w_A - w_r) from the boundary, M = w_A x_0^2/2 - N_A,Ed (x_0 - c_A/2) - w_r (x_0 - c_A)^2/2;
   trapezoid: A = 1.1 (N_A + N_B)/q, x_bar = c_A/2 + N_B s/(N_A + N_B), b1 + b2 = 2A/L, b1 + 2 b2 = 3 x_bar (b1 + b2)/L;
   piles: n = (G_k + Q_k + W)/F_p rounded up to a regular group, s = 3 phi, cap side = ((n_i - 1) 3 + 1) phi + 300;
   P = (N + W)/n +- M_y x/sum(x^2) +- M_x y/sum(y^2), every pile counted in the sums. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }

  /* shared strap geometry: everything in kN and m */
  function strapCase(r) {
    var cA = pick(r, [300, 350, 400]), cB = pick(r, [300, 350, 400, 450]), L = step(r, 4.5, 7.0, 0.25), LA = pick(r, [1.6, 1.8, 2.0, 2.2, 2.4]);
    var bs = pick(r, [300, 350, 400]), hs = pick(r, [700, 750, 800, 850, 900]);
    var Ls = L - cA / 2000 - cB / 2000, e = LA / 2 - cA / 2000;
    return { cA: cA, cB: cB, L: L, LA: LA, bs: bs, hs: hs, Ls: Ls, e: e, xR: Ls / 2 + cB / 2000, WR: 25 * bs / 1000 * hs / 1000 * Ls };
  }

  /* ---------- B1 strap footing: service reactions and sizes ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        P = strapCase(r);
        P.q = pick(r, [150, 175, 200, 225, 250]); P.GkA = step(r, 450, 1000, 25); P.QkA = step(r, 150, 450, 25); P.GkB = step(r, 700, 1400, 25); P.QkB = step(r, 300, 800, 25);
        P.NA = P.GkA + P.QkA; P.NB = P.GkB + P.QkB; P.WA = 0.1 * P.NA; P.WB = 0.1 * P.NB;
        P.RA = P.WA + (P.NA * P.L + P.WR * P.xR) / (P.L - P.e); P.BA = P.RA / (P.q * P.LA);
        P.RB = P.NA + P.NB + P.WA + P.WB + P.WR - P.RA; P.SB = Math.sqrt(P.RB / P.q);
        if (P.BA < P.LA + 0.3 || P.BA > 4.6 || P.SB < 1.8 || P.SB > 4.2) continue;
        if (P.cA / 2000 + P.L - P.SB / 2 - P.LA < 0.6) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("Column A, " + num(P.cA) + " mm square, stands on the site boundary and carries G<sub>k</sub> = " + num(P.GkA) + " kN and Q<sub>k</sub> = " + num(P.QkA) + " kN. Column B, " + num(P.cB) + " mm square, " + num(fmt(P.L, 2)) + " m away (centre to centre), carries G<sub>k</sub> = " + num(P.GkB) + " kN and Q<sub>k</sub> = " + num(P.QkB) + " kN. Footing A starts at the boundary and is " + num(fmt(P.LA, 1)) + " m long along the strap; footing B is square; q<sub>all</sub> = " + num(P.q) + " kN/m². The strap, " + num(P.bs) + " × " + num(P.hs) + " mm, runs between the column faces. Taking each footing’s weight as 10 % of its column load, find the service reaction R<sub>A</sub>, the width B<sub>A</sub> footing A needs and the side S<sub>B</sub> of footing B, before rounding.",
                "Column A, " + num(P.cA) + " mm segi empat sama, berdiri di sempadan tapak dan membawa G<sub>k</sub> = " + num(P.GkA) + " kN dan Q<sub>k</sub> = " + num(P.QkA) + " kN. Column B, " + num(P.cB) + " mm segi empat sama, " + num(fmt(P.L, 2)) + " m darinya (pusat ke pusat), membawa G<sub>k</sub> = " + num(P.GkB) + " kN dan Q<sub>k</sub> = " + num(P.QkB) + " kN. Footing A bermula di sempadan dan sepanjang " + num(fmt(P.LA, 1)) + " m sepanjang strap; footing B segi empat sama; q<sub>all</sub> = " + num(P.q) + " kN/m². Strap, " + num(P.bs) + " × " + num(P.hs) + " mm, merentang di antara muka column. Dengan berat setiap footing 10 % daripada load column-nya, cari reaction service R<sub>A</sub>, lebar B<sub>A</sub> yang diperlukan footing A dan sisi S<sub>B</sub> footing B, sebelum dibundarkan.");
    },
    fields: [{ id: "ra", label: ["R<sub>A</sub>", "R<sub>A</sub>"], unit: "kN", fn: function (P) { return P.RA; }, rtol: 0.005 },
             { id: "ba", label: ["B<sub>A</sub>", "B<sub>A</sub>"], unit: "m", fn: function (P) { return P.BA; }, rtol: 0.01 },
             { id: "sb", label: ["S<sub>B</sub>", "S<sub>B</sub>"], unit: "m", fn: function (P) { return P.SB; }, rtol: 0.01 }],
    hints: [function () { return bi("e = L<sub>A</sub>/2 − c<sub>A</sub>/2: footing A’s centre is e from column A. W<sub>R</sub> = 25bh × (length between the column faces), acting at x<sub>R</sub> from column B.", "e = L<sub>A</sub>/2 − c<sub>A</sub>/2: pusat footing A berada e dari column A. W<sub>R</sub> = 25bh × (panjang di antara muka column), bertindak pada x<sub>R</sub> dari column B."); },
            function () { return bi("Moments about column B: R<sub>A</sub> acts L − e from it, so R<sub>A</sub> = W<sub>A</sub> + (N<sub>A</sub>L + W<sub>R</sub>x<sub>R</sub>)/(L − e).", "Moment pada column B: R<sub>A</sub> bertindak L − e darinya, jadi R<sub>A</sub> = W<sub>A</sub> + (N<sub>A</sub>L + W<sub>R</sub>x<sub>R</sub>)/(L − e)."); },
            function () { return bi("R<sub>B</sub> from ΣV = 0; then B<sub>A</sub> = R<sub>A</sub>/(q<sub>all</sub>L<sub>A</sub>) and S<sub>B</sub> = √(R<sub>B</sub>/q<sub>all</sub>).", "R<sub>B</sub> daripada ΣV = 0; kemudian B<sub>A</sub> = R<sub>A</sub>/(q<sub>all</sub>L<sub>A</sub>) dan S<sub>B</sub> = √(R<sub>B</sub>/q<sub>all</sub>)."); }],
    solution: function (P) {
      return sol(["N<sub>A</sub> = " + P.GkA + " + " + P.QkA + " = " + P.NA + " kN; N<sub>B</sub> = " + P.GkB + " + " + P.QkB + " = " + P.NB + " kN; W<sub>A</sub> = " + fmt(P.WA, 1) + ", W<sub>B</sub> = " + fmt(P.WB, 1) + " kN",
        "W<sub>R</sub> = 25 × " + fmt(P.bs / 1000, 2) + " × " + fmt(P.hs / 1000, 2) + " × " + fmt(P.Ls, 3) + " = " + fmt(P.WR, 1) + bi(" kN at x<sub>R</sub> = " + fmt(P.xR, 4) + " m from column B", " kN pada x<sub>R</sub> = " + fmt(P.xR, 4) + " m dari column B"),
        "e = " + fmt(P.LA, 1) + "/2 − " + fmt(P.cA / 1000, 3) + "/2 = " + fmt(P.e, 3) + " m; L − e = " + fmt(P.L - P.e, 3) + " m",
        "R<sub>A</sub> = " + fmt(P.WA, 1) + " + (" + P.NA + " × " + fmt(P.L, 2) + " + " + fmt(P.WR, 1) + " × " + fmt(P.xR, 4) + ")/" + fmt(P.L - P.e, 3) + " = " + fmt(P.RA, 1) + " kN",
        "B<sub>A</sub> = " + fmt(P.RA, 1) + "/(" + P.q + " × " + fmt(P.LA, 1) + ") = " + fmt(P.BA, 3) + " m",
        "R<sub>B</sub> = " + P.NA + " + " + P.NB + " + " + fmt(P.WA, 1) + " + " + fmt(P.WB, 1) + " + " + fmt(P.WR, 1) + " − " + fmt(P.RA, 1) + " = " + fmt(P.RB, 1) + " kN; S<sub>B</sub> = √(" + fmt(P.RB, 1) + "/" + P.q + ") = " + fmt(P.SB, 3) + " m",
        bi("Round both up to 0.05 m, then check the pressures with the real weights (Worked Example 11.1, step 3).", "Bundarkan kedua-duanya ke atas kepada 0.05 m, kemudian semak tekanan dengan berat sebenar (Worked Example 11.1, langkah 3).")]);
    }
  });

  /* ---------- B2 strap: zero shear and the largest moment ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        P = strapCase(r);
        P.GkA = step(r, 450, 1000, 25); P.QkA = step(r, 150, 450, 25);
        P.NA = 1.35 * P.GkA + 1.5 * P.QkA; P.WRu = 1.35 * P.WR;
        P.RA = (P.NA * P.L + P.WRu * P.xR) / (P.L - P.e); P.wA = P.RA / P.LA; P.wr = P.WRu / P.Ls;
        var c = P.cA / 1000;
        P.x0 = (P.NA - P.wr * c) / (P.wA - P.wr);
        P.M = P.wA * P.x0 * P.x0 / 2 - P.NA * (P.x0 - c / 2) - P.wr * Math.pow(P.x0 - c, 2) / 2;
        if (P.x0 < c + 0.1 || P.x0 > P.LA - 0.05) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("Column A, " + num(P.cA) + " mm square, stands on the site boundary and carries G<sub>k</sub> = " + num(P.GkA) + " kN and Q<sub>k</sub> = " + num(P.QkA) + " kN. Column B, " + num(P.cB) + " mm square, is " + num(fmt(P.L, 2)) + " m away. Footing A is " + num(fmt(P.LA, 1)) + " m long along the strap, and the strap, " + num(P.bs) + " × " + num(P.hs) + " mm, runs between the column faces. At the ultimate limit state, with the footing weights left out of the strap statics and 1.35W<sub>R</sub> kept, find the net reaction R<sub>A,Ed</sub>, the position x<sub>0</sub> of zero shear in the strap measured from the boundary, and the largest hogging moment.",
                "Column A, " + num(P.cA) + " mm segi empat sama, berdiri di sempadan tapak dan membawa G<sub>k</sub> = " + num(P.GkA) + " kN dan Q<sub>k</sub> = " + num(P.QkA) + " kN. Column B, " + num(P.cB) + " mm segi empat sama, berada " + num(fmt(P.L, 2)) + " m darinya. Footing A sepanjang " + num(fmt(P.LA, 1)) + " m sepanjang strap, dan strap, " + num(P.bs) + " × " + num(P.hs) + " mm, merentang di antara muka column. Pada ultimate limit state, dengan berat footing tidak dimasukkan dalam statik strap dan 1.35W<sub>R</sub> dikekalkan, cari reaction bersih R<sub>A,Ed</sub>, kedudukan x<sub>0</sub> ricih sifar dalam strap diukur dari sempadan, dan moment hogging terbesar.");
    },
    fields: [{ id: "ra", label: ["R<sub>A,Ed</sub>", "R<sub>A,Ed</sub>"], unit: "kN", fn: function (P) { return P.RA; }, rtol: 0.005 },
             { id: "x0", label: ["x<sub>0</sub>", "x<sub>0</sub>"], unit: "m", fn: function (P) { return P.x0; }, rtol: 0.01, atol: 0.005 },
             { id: "m", label: ["|M<sub>max</sub>|", "|M<sub>max</sub>|"], unit: "kN m", fn: function (P) { return Math.abs(P.M); }, rtol: 0.015, atol: 1 }],
    hints: [function () { return bi("N<sub>A,Ed</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>; R<sub>A,Ed</sub> = (N<sub>A,Ed</sub>L + 1.35W<sub>R</sub>x<sub>R</sub>)/(L − e), with e = L<sub>A</sub>/2 − c<sub>A</sub>/2.", "N<sub>A,Ed</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>; R<sub>A,Ed</sub> = (N<sub>A,Ed</sub>L + 1.35W<sub>R</sub>x<sub>R</sub>)/(L − e), dengan e = L<sub>A</sub>/2 − c<sub>A</sub>/2."); },
            function () { return bi("Over footing A the strap carries w<sub>A</sub> = R<sub>A,Ed</sub>/L<sub>A</sub> upwards; its own weight w<sub>r</sub> = 1.35W<sub>R</sub>/(its length) starts at the face of column A. x<sub>0</sub> = (N<sub>A,Ed</sub> − w<sub>r</sub>c<sub>A</sub>)/(w<sub>A</sub> − w<sub>r</sub>).", "Di atas footing A, strap menerima w<sub>A</sub> = R<sub>A,Ed</sub>/L<sub>A</sub> ke atas; berat sendirinya w<sub>r</sub> = 1.35W<sub>R</sub>/(panjangnya) bermula di muka column A. x<sub>0</sub> = (N<sub>A,Ed</sub> − w<sub>r</sub>c<sub>A</sub>)/(w<sub>A</sub> − w<sub>r</sub>)."); },
            function () { return bi("N<sub>A,Ed</sub> acts at the column centre, c<sub>A</sub>/2 from the boundary: M = w<sub>A</sub>x<sub>0</sub>²/2 − N<sub>A,Ed</sub>(x<sub>0</sub> − c<sub>A</sub>/2) − w<sub>r</sub>(x<sub>0</sub> − c<sub>A</sub>)²/2.", "N<sub>A,Ed</sub> bertindak di pusat column, c<sub>A</sub>/2 dari sempadan: M = w<sub>A</sub>x<sub>0</sub>²/2 − N<sub>A,Ed</sub>(x<sub>0</sub> − c<sub>A</sub>/2) − w<sub>r</sub>(x<sub>0</sub> − c<sub>A</sub>)²/2."); }],
    solution: function (P) {
      var c = P.cA / 1000;
      return sol(["N<sub>A,Ed</sub> = 1.35 × " + P.GkA + " + 1.5 × " + P.QkA + " = " + fmt(P.NA, 1) + " kN; 1.35W<sub>R</sub> = 1.35 × 25 × " + fmt(P.bs / 1000, 2) + " × " + fmt(P.hs / 1000, 2) + " × " + fmt(P.Ls, 3) + " = " + fmt(P.WRu, 2) + " kN",
        "e = " + fmt(P.e, 3) + " m; x<sub>R</sub> = " + fmt(P.xR, 4) + " m; R<sub>A,Ed</sub> = (" + fmt(P.NA, 1) + " × " + fmt(P.L, 2) + " + " + fmt(P.WRu, 2) + " × " + fmt(P.xR, 4) + ")/" + fmt(P.L - P.e, 3) + " = " + fmt(P.RA, 1) + " kN",
        "w<sub>A</sub> = " + fmt(P.RA, 1) + "/" + fmt(P.LA, 1) + " = " + fmt(P.wA, 2) + " kN/m; w<sub>r</sub> = " + fmt(P.WRu, 2) + "/" + fmt(P.Ls, 3) + " = " + fmt(P.wr, 3) + " kN/m",
        "x<sub>0</sub> = (" + fmt(P.NA, 1) + " − " + fmt(P.wr, 3) + " × " + fmt(c, 3) + ")/(" + fmt(P.wA, 2) + " − " + fmt(P.wr, 3) + ") = " + fmt(P.x0, 3) + bi(" m from the boundary", " m dari sempadan"),
        "M = " + fmt(P.wA, 2) + " × " + fmt(P.x0, 3) + "²/2 − " + fmt(P.NA, 1) + " × " + fmt(P.x0 - c / 2, 3) + " − " + fmt(P.wr, 3) + " × " + fmt(P.x0 - c, 3) + "²/2 = " + fmt(P.M, 1) + bi(" kN m: the top of the strap in tension", " kN m: bahagian atas strap tegang")]);
    }
  });

  /* ---------- B3 a trapezoidal combined footing ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        var cA = pick(r, [300, 350, 400]), s = step(r, 4.0, 6.5, 0.25), ov = step(r, 0.6, 1.2, 0.05), NA = step(r, 700, 1300, 25), NB = step(r, 1100, 2400, 25), q = pick(r, [150, 175, 200, 225, 250]);
        var L = cA / 2000 + s + ov, A = 1.1 * (NA + NB) / q, xb = cA / 2000 + NB * s / (NA + NB), sum = 2 * A / L, s2 = 3 * xb * sum / L, b2 = s2 - sum, b1 = sum - b2;
        P = { cA: cA, s: s, ov: ov, NA: NA, NB: NB, q: q, L: L, A: A, xb: xb, sum: sum, s2: s2, b1: b1, b2: b2 };
        if (b1 < 0.8 || b2 > 4.5 || b2 - b1 < 0.2) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("Column A, " + num(P.cA) + " mm square, stands on the site boundary and carries N<sub>A</sub> = " + num(P.NA) + " kN in service; column B, " + num(fmt(P.s, 2)) + " m away, carries N<sub>B</sub> = " + num(P.NB) + " kN. A combined footing must run from the boundary to a line " + num(fmt(P.ov, 2)) + " m beyond column B, so it is L = " + num(fmt(P.L, 3)) + " m long. With q<sub>all</sub> = " + num(P.q) + " kN/m², make it a trapezoid of area A<sub>req</sub> = 1.1(N<sub>A</sub> + N<sub>B</sub>)/q<sub>all</sub> with its centroid under the resultant of the column loads. Find A<sub>req</sub>, the resultant x̄ measured from the boundary, the width b<sub>1</sub> at the boundary and b<sub>2</sub> at the far end.",
                "Column A, " + num(P.cA) + " mm segi empat sama, berdiri di sempadan tapak dan membawa N<sub>A</sub> = " + num(P.NA) + " kN dalam service; column B, " + num(fmt(P.s, 2)) + " m darinya, membawa N<sub>B</sub> = " + num(P.NB) + " kN. Satu combined footing mesti merentang dari sempadan hingga satu garis " + num(fmt(P.ov, 2)) + " m melepasi column B, jadi panjangnya L = " + num(fmt(P.L, 3)) + " m. Dengan q<sub>all</sub> = " + num(P.q) + " kN/m², jadikannya trapezium dengan luas A<sub>req</sub> = 1.1(N<sub>A</sub> + N<sub>B</sub>)/q<sub>all</sub> dan centroid di bawah paduan load column. Cari A<sub>req</sub>, paduan x̄ diukur dari sempadan, lebar b<sub>1</sub> di sempadan dan b<sub>2</sub> di hujung yang jauh.");
    },
    fields: [{ id: "a", label: ["A<sub>req</sub>", "A<sub>req</sub>"], unit: "m²", fn: function (P) { return P.A; }, rtol: 0.005 },
             { id: "xb", label: ["x̄", "x̄"], unit: "m", fn: function (P) { return P.xb; }, rtol: 0.005 },
             { id: "b1", label: ["b<sub>1</sub>", "b<sub>1</sub>"], unit: "m", fn: function (P) { return P.b1; }, rtol: 0.01, atol: 0.005 },
             { id: "b2", label: ["b<sub>2</sub>", "b<sub>2</sub>"], unit: "m", fn: function (P) { return P.b2; }, rtol: 0.01, atol: 0.005 }],
    hints: [function () { return bi("A<sub>req</sub> = 1.1(N<sub>A</sub> + N<sub>B</sub>)/q<sub>all</sub>; x̄ = c<sub>A</sub>/2 + N<sub>B</sub>s/(N<sub>A</sub> + N<sub>B</sub>) from the boundary.", "A<sub>req</sub> = 1.1(N<sub>A</sub> + N<sub>B</sub>)/q<sub>all</sub>; x̄ = c<sub>A</sub>/2 + N<sub>B</sub>s/(N<sub>A</sub> + N<sub>B</sub>) dari sempadan."); },
            function () { return bi("From the area: b<sub>1</sub> + b<sub>2</sub> = 2A/L. From the centroid, x̄ = (L/3)(b<sub>1</sub> + 2b<sub>2</sub>)/(b<sub>1</sub> + b<sub>2</sub>): b<sub>1</sub> + 2b<sub>2</sub> = 3x̄(b<sub>1</sub> + b<sub>2</sub>)/L.", "Daripada luas: b<sub>1</sub> + b<sub>2</sub> = 2A/L. Daripada centroid, x̄ = (L/3)(b<sub>1</sub> + 2b<sub>2</sub>)/(b<sub>1</sub> + b<sub>2</sub>): b<sub>1</sub> + 2b<sub>2</sub> = 3x̄(b<sub>1</sub> + b<sub>2</sub>)/L."); },
            function () { return bi("Subtract the two: b<sub>2</sub> = (b<sub>1</sub> + 2b<sub>2</sub>) − (b<sub>1</sub> + b<sub>2</sub>); then b<sub>1</sub>. The wider end is at the heavier column.", "Tolak kedua-duanya: b<sub>2</sub> = (b<sub>1</sub> + 2b<sub>2</sub>) − (b<sub>1</sub> + b<sub>2</sub>); kemudian b<sub>1</sub>. Hujung yang lebih lebar berada di column yang lebih berat."); }],
    solution: function (P) {
      return sol(["A<sub>req</sub> = 1.1 × (" + P.NA + " + " + P.NB + ")/" + P.q + " = " + fmt(P.A, 3) + " m²",
        "x̄ = " + fmt(P.cA / 2000, 3) + " + " + P.NB + " × " + fmt(P.s, 2) + "/" + (P.NA + P.NB) + " = " + fmt(P.xb, 4) + bi(" m from the boundary (L/2 = " + fmt(P.L / 2, 3) + " m)", " m dari sempadan (L/2 = " + fmt(P.L / 2, 3) + " m)"),
        "b<sub>1</sub> + b<sub>2</sub> = 2 × " + fmt(P.A, 3) + "/" + fmt(P.L, 3) + " = " + fmt(P.sum, 4) + " m; b<sub>1</sub> + 2b<sub>2</sub> = 3 × " + fmt(P.xb, 4) + " × " + fmt(P.sum, 4) + "/" + fmt(P.L, 3) + " = " + fmt(P.s2, 4) + " m",
        "b<sub>2</sub> = " + fmt(P.s2, 4) + " − " + fmt(P.sum, 4) + " = " + fmt(P.b2, 3) + " m; b<sub>1</sub> = " + fmt(P.sum, 4) + " − " + fmt(P.b2, 3) + " = " + fmt(P.b1, 3) + " m",
        bi("Round the widths to practical values and check the pressure with the real weight; a small eccentricity is left (Notes §4).", "Bundarkan lebar kepada nilai praktikal dan semak tekanan dengan berat sebenar; eccentricity yang kecil tertinggal (Notes §4).")]);
    }
  });

  /* ---------- B4 number of piles and the cap ---------- */
  var GROUPS = { 4: [2, 2], 6: [3, 2], 8: [4, 2], 9: [3, 3] };
  EX.define("b4", {
    gen: function (r) {
      var P, FP = { 250: [350, 400, 450], 300: [450, 500, 550, 600], 350: [600, 650, 700, 750], 400: [750, 800, 900, 1000] };
      for (var t = 0; t < 80; t++) {
        var ph = pick(r, [250, 300, 350, 400]), Fp = pick(r, FP[ph]), W = pick(r, [150, 200, 250]), Gk = step(r, 800, 3500, 50), Qk = step(r, 300, 1800, 50);
        var nr = (Gk + Qk + W) / Fp, n = [4, 6, 8, 9].filter(function (k) { return k >= nr - 1e-9; })[0];
        if (!n || nr < 3.2) continue;
        var g = GROUPS[n], k = 3;
        P = { ph: ph, Fp: Fp, W: W, Gk: Gk, Qk: Qk, N: Gk + Qk, nr: nr, n: n, nx: g[0], ny: g[1], s: k * ph, Lc: ((g[0] - 1) * k + 1) * ph + 300, Bc: ((g[1] - 1) * k + 1) * ph + 300 };
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("A column carries G<sub>k</sub> = " + num(P.Gk) + " kN and Q<sub>k</sub> = " + num(P.Qk) + " kN. It is to stand on precast piles " + num(P.ph) + " mm square, each with a working load of " + num(P.Fp) + " kN; assume a cap weight of " + num(P.W) + " kN. Use the smallest of the regular groups 2 × 2, 2 × 3, 2 × 4 or 3 × 3 that carries the load, at a spacing of 3φ, with the cap 150 mm beyond the pile faces. Find the number of piles and the length L and width B of the cap.",
                "Satu column membawa G<sub>k</sub> = " + num(P.Gk) + " kN dan Q<sub>k</sub> = " + num(P.Qk) + " kN. Ia akan berdiri di atas pile pratuang " + num(P.ph) + " mm segi empat sama, setiap satu dengan working load " + num(P.Fp) + " kN; andaikan berat pile cap " + num(P.W) + " kN. Gunakan kumpulan sekata terkecil antara 2 × 2, 2 × 3, 2 × 4 atau 3 × 3 yang mampu memikul load itu, pada jarak 3φ, dengan pile cap 150 mm melepasi muka pile. Cari bilangan pile serta panjang L dan lebar B pile cap.");
    },
    fields: [{ id: "n", label: ["n", "n"], unit: "", fn: function (P) { return P.n; }, rtol: 0, atol: 0.01 },
             { id: "lc", label: ["L", "L"], unit: "mm", fn: function (P) { return P.Lc; }, rtol: 0, atol: 1 },
             { id: "bc", label: ["B", "B"], unit: "mm", fn: function (P) { return P.Bc; }, rtol: 0, atol: 1 }],
    hints: [function () { return bi("n = (G<sub>k</sub> + Q<sub>k</sub> + W)/F<sub>p</sub>: service loads, because F<sub>p</sub> is a working load. Round up to the next regular group.", "n = (G<sub>k</sub> + Q<sub>k</sub> + W)/F<sub>p</sub>: service load, kerana F<sub>p</sub> ialah working load. Bundarkan ke atas kepada kumpulan sekata berikutnya."); },
            function () { return bi("s = 3φ. Put the longer row along L: n<sub>x</sub> piles along the length, n<sub>y</sub> across.", "s = 3φ. Letakkan baris yang lebih panjang sepanjang L: n<sub>x</sub> pile sepanjang panjang, n<sub>y</sub> merentas."); },
            function () { return bi("L = ((n<sub>x</sub> − 1) × 3 + 1)φ + 300; B = ((n<sub>y</sub> − 1) × 3 + 1)φ + 300.", "L = ((n<sub>x</sub> − 1) × 3 + 1)φ + 300; B = ((n<sub>y</sub> − 1) × 3 + 1)φ + 300."); }],
    solution: function (P) {
      return sol(["n = (" + P.Gk + " + " + P.Qk + " + " + P.W + ")/" + P.Fp + " = " + fmt(P.nr, 2) + " → " + P.n + bi(" piles: " + P.ny + " rows of " + P.nx, " pile: " + P.ny + " baris " + P.nx),
        "s = 3 × " + P.ph + " = " + P.s + " mm",
        "L = ((" + P.nx + " − 1) × 3 + 1) × " + P.ph + " + 300 = " + P.Lc + " mm; B = ((" + P.ny + " − 1) × 3 + 1) × " + P.ph + " + 300 = " + P.Bc + " mm",
        bi("Then check the real cap weight against the " + P.W + " kN assumed, and the pile loads under any moment (B5).", "Kemudian semak berat sebenar pile cap berbanding " + P.W + " kN yang diandaikan, dan load pile di bawah sebarang moment (B5).")]);
    }
  });

  function rowSum(nr, s) { var t = 0; for (var i = 0; i < nr; i++) { var x = (i - (nr - 1) / 2) * s; t += x * x; } return t; }

  /* ---------- B5 pile loads under a moment ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        var g = pick(r, [[2, 2], [3, 2], [4, 2], [3, 3]]), ph = pick(r, [300, 350, 400, 450]), s = 3 * ph / 1000, n = g[0] * g[1];
        var Nt = step(r, n * 300, n * 900, 25), M = step(r, 20, 400, 5);
        var sx2 = g[1] * rowSum(g[0], s), xm = (g[0] - 1) * s / 2, Pm = Nt / n, dP = M * xm / sx2;
        P = { nx: g[0], ny: g[1], n: n, ph: ph, s: s, Nt: Nt, M: M, sx2: sx2, xm: xm, Pm: Pm, dP: dP, Pmax: Pm + dP, Pmin: Pm - dP };
        if (P.Pmin < 0.25 * Pm || dP < 0.04 * Pm) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("A pile cap stands on " + num(P.n) + " piles, " + num(P.ny) + " rows of " + num(P.nx) + " at " + num(fmt(P.s * 1000, 0)) + " mm centres, with the rows of " + num(P.nx) + " along the direction in which the moment turns. In service it carries N + W = " + num(P.Nt) + " kN, cap included, and M = " + num(P.M) + " kN m. Find Σx² of the group and the largest and smallest pile loads.",
                "Satu pile cap berdiri di atas " + num(P.n) + " pile, " + num(P.ny) + " baris " + num(P.nx) + " pada jarak pusat " + num(fmt(P.s * 1000, 0)) + " mm, dengan baris " + num(P.nx) + " sepanjang arah moment berpusing. Dalam service ia membawa N + W = " + num(P.Nt) + " kN, termasuk pile cap, dan M = " + num(P.M) + " kN m. Cari Σx² kumpulan itu serta load pile terbesar dan terkecil.");
    },
    fields: [{ id: "sx2", label: ["Σx²", "Σx²"], unit: "m²", fn: function (P) { return P.sx2; }, rtol: 0.002 },
             { id: "pmax", label: ["P<sub>max</sub>", "P<sub>max</sub>"], unit: "kN", fn: function (P) { return P.Pmax; }, rtol: 0.005 },
             { id: "pmin", label: ["P<sub>min</sub>", "P<sub>min</sub>"], unit: "kN", fn: function (P) { return P.Pmin; }, rtol: 0.005 }],
    hints: [function () { return bi("x is measured from the centroid of the group to each pile, along the direction of the moment. Every pile counts; piles on the axis have x = 0.", "x diukur dari centroid kumpulan ke setiap pile, sepanjang arah moment. Setiap pile dikira; pile di atas paksi mempunyai x = 0."); },
            function () { return bi("Σx² = (number of rows) × Σx<sub>i</sub>² over one row.", "Σx² = (bilangan baris) × Σx<sub>i</sub>² bagi satu baris."); },
            function () { return bi("P = (N + W)/n ± Mx<sub>max</sub>/Σx².", "P = (N + W)/n ± Mx<sub>max</sub>/Σx²."); }],
    solution: function (P) {
      var xs = [], i; for (i = 0; i < P.nx; i++) xs.push(fmt((i - (P.nx - 1) / 2) * P.s, 3));
      return sol([bi("Along a row x = " + xs.join(", ") + " m", "Sepanjang satu baris x = " + xs.join(", ") + " m") + "; Σx² = " + P.ny + " × " + fmt(rowSum(P.nx, P.s), 4) + " = " + fmt(P.sx2, 4) + " m²",
        "(N + W)/n = " + P.Nt + "/" + P.n + " = " + fmt(P.Pm, 1) + " kN; Mx<sub>max</sub>/Σx² = " + P.M + " × " + fmt(P.xm, 3) + "/" + fmt(P.sx2, 4) + " = " + fmt(P.dP, 1) + " kN",
        "P<sub>max</sub> = " + fmt(P.Pm, 1) + " + " + fmt(P.dP, 1) + " = " + fmt(P.Pmax, 1) + " kN; P<sub>min</sub> = " + fmt(P.Pm, 1) + " − " + fmt(P.dP, 1) + " = " + fmt(P.Pmin, 1) + " kN",
        bi("Compare P<sub>max</sub> with the working load; P<sub>min</sub> &gt; 0, so no pile is in tension.", "Bandingkan P<sub>max</sub> dengan working load; P<sub>min</sub> &gt; 0, jadi tiada pile dalam tegangan.")]);
    }
  });

  /* ---------- B6 two moments: the corner pile ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        var g = pick(r, [[3, 2], [3, 3], [4, 2], [4, 3]]), ph = pick(r, [300, 350, 400]), s = 3 * ph / 1000, n = g[0] * g[1];
        var Nt = step(r, n * 300, n * 900, 25), My = step(r, 20, 300, 5), Mx = step(r, 20, 300, 5);
        var sx2 = g[1] * rowSum(g[0], s), sy2 = g[0] * rowSum(g[1], s), xm = (g[0] - 1) * s / 2, ym = (g[1] - 1) * s / 2;
        var Pm = Nt / n, dx = My * xm / sx2, dy = Mx * ym / sy2;
        P = { nx: g[0], ny: g[1], n: n, ph: ph, s: s, Nt: Nt, My: My, Mx: Mx, sx2: sx2, sy2: sy2, xm: xm, ym: ym, Pm: Pm, dx: dx, dy: dy, Pmax: Pm + dx + dy, Pmin: Pm - dx - dy };
        if (P.Pmin < 0.2 * Pm || dx < 0.03 * Pm || dy < 0.03 * Pm) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("A pile cap stands on " + num(P.n) + " piles at " + num(fmt(P.s * 1000, 0)) + " mm centres: " + num(P.nx) + " along x and " + num(P.ny) + " along y. In service it carries N + W = " + num(P.Nt) + " kN, M<sub>y</sub> = " + num(P.My) + " kN m about the y axis and M<sub>x</sub> = " + num(P.Mx) + " kN m about the x axis. Find Σx², Σy² and the load on the most heavily loaded corner pile.",
                "Satu pile cap berdiri di atas " + num(P.n) + " pile pada jarak pusat " + num(fmt(P.s * 1000, 0)) + " mm: " + num(P.nx) + " sepanjang x dan " + num(P.ny) + " sepanjang y. Dalam service ia membawa N + W = " + num(P.Nt) + " kN, M<sub>y</sub> = " + num(P.My) + " kN m pada paksi y dan M<sub>x</sub> = " + num(P.Mx) + " kN m pada paksi x. Cari Σx², Σy² dan load pada pile bucu yang paling berat.");
    },
    fields: [{ id: "sx2", label: ["Σx²", "Σx²"], unit: "m²", fn: function (P) { return P.sx2; }, rtol: 0.002 },
             { id: "sy2", label: ["Σy²", "Σy²"], unit: "m²", fn: function (P) { return P.sy2; }, rtol: 0.002 },
             { id: "pmax", label: ["P<sub>max</sub>", "P<sub>max</sub>"], unit: "kN", fn: function (P) { return P.Pmax; }, rtol: 0.005 }],
    hints: [function () { return bi("M<sub>y</sub> turns about the y axis, so the pile loads change along x: it goes with x/Σx². M<sub>x</sub> goes with y/Σy².", "M<sub>y</sub> berpusing pada paksi y, jadi load pile berubah sepanjang x: ia bersama x/Σx². M<sub>x</sub> bersama y/Σy²."); },
            function () { return bi("Σx² = n<sub>y</sub> × Σx<sub>i</sub>² over one row along x; Σy² = n<sub>x</sub> × Σy<sub>j</sub>² over one row along y.", "Σx² = n<sub>y</sub> × Σx<sub>i</sub>² bagi satu baris sepanjang x; Σy² = n<sub>x</sub> × Σy<sub>j</sub>² bagi satu baris sepanjang y."); },
            function () { return bi("The worst corner takes both increments: P = (N + W)/n + M<sub>y</sub>x<sub>max</sub>/Σx² + M<sub>x</sub>y<sub>max</sub>/Σy².", "Bucu terburuk menerima kedua-dua tambahan: P = (N + W)/n + M<sub>y</sub>x<sub>max</sub>/Σx² + M<sub>x</sub>y<sub>max</sub>/Σy²."); }],
    solution: function (P) {
      return sol(["Σx² = " + P.ny + " × " + fmt(rowSum(P.nx, P.s), 4) + " = " + fmt(P.sx2, 4) + " m²; Σy² = " + P.nx + " × " + fmt(rowSum(P.ny, P.s), 4) + " = " + fmt(P.sy2, 4) + " m²",
        "(N + W)/n = " + P.Nt + "/" + P.n + " = " + fmt(P.Pm, 1) + " kN; M<sub>y</sub>x<sub>max</sub>/Σx² = " + P.My + " × " + fmt(P.xm, 3) + "/" + fmt(P.sx2, 4) + " = " + fmt(P.dx, 1) + " kN; M<sub>x</sub>y<sub>max</sub>/Σy² = " + P.Mx + " × " + fmt(P.ym, 3) + "/" + fmt(P.sy2, 4) + " = " + fmt(P.dy, 1) + " kN",
        "P<sub>max</sub> = " + fmt(P.Pm, 1) + " + " + fmt(P.dx, 1) + " + " + fmt(P.dy, 1) + " = " + fmt(P.Pmax, 1) + bi(" kN at the corner on the positive side of both axes", " kN di bucu pada sisi positif kedua-dua paksi"),
        bi("The opposite corner carries " + fmt(P.Pmin, 1) + " kN.", "Bucu bertentangan memikul " + fmt(P.Pmin, 1) + " kN.")]);
    }
  });

  EX.ready();
})();
