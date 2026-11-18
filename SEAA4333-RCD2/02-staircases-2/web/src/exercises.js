/* SEAA 4333 Unit 2 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method (the RC Design app's staircase model), per metre width:
   plan: n_R = treads + 1 when the landing is the last step, R = (H/2)/n_R;
   span on a landing (BS 8110 3.10.1.3): L = L_a + (L_b1 + min(L_b2, 1800))/2, l_f = L_a + L_b1/2, l_L = min(L_b2, 1800)/2;
   F = n_f l_f + n_L l_L, M = FL/10 with a continuous end, V_A L = sum(n l x_B) + M_A - M_B;
   landing: w_L = n_L b_L + V_A, L_L = 2 b_F + well + t_w, M_L = w_L L_L^2/8, d_L = h_L - c - phi_flight - phi_L/2 (inner layer);
   right angles (Mosley 8.8.2): n'_L = n_L/2; walls (BS 8110 3.10.1.2): kappa_w = (b_F - 150 n_w)/(b_F + 75 n_w);
   flexure: K = M/(b d^2 f_ck), z = d [0.5 + sqrt(0.25 - K/1.134)] <= 0.95 d, A_s = M/(0.87 f_yk z). */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function r2(v) { return Math.round(v * 100) / 100; }
  function mm(v) { return fmt(v, Math.abs(v - Math.round(v)) > 1e-9 ? 1 : 0); }
  function flex(M, b, d, fck) { var K = M * 1e6 / (b * d * d * fck), z0 = d * (0.5 + Math.sqrt(0.25 - K / 1.134)), z = Math.min(z0, 0.95 * d); return { K: K, z0: z0, z: z, As: M * 1e6 / (0.87 * 500 * z) }; }
  function loads(r) { var nf = r2(step(r, 13.5, 17.5, 0.01)); return { nf: nf, nL: r2(nf * step(r, 0.70, 0.80, 0.01)) }; }

  /* ---------- B1 reading a stair plan ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.nR = pick(r, [8, 9, 10, 11, 12]); P.R = pick(r, [150, 155, 160, 165, 170, 175, 180]); P.G = pick(r, [255, 260, 265, 270, 275, 280, 290, 300]);
      P.H = 2 * P.nR * P.R; P.nT = P.nR - 1; P.Lf = P.nT * P.G; P.c = 2 * P.R + P.G;
      return P;
    },
    text: function (P) {
      return bi("A dog-leg stair climbs " + num(P.H) + " mm between two floors in two equal flights with a half landing. On the plan each flight shows " + num(P.nT + " @ " + P.G + " = " + P.Lf) + ", and each flight ends on the landing or on the floor above, which forms its last step. Find the number of risers in one flight, the rise R and 2R + G.",
                "Satu tangga dog-leg mendaki " + num(P.H) + " mm di antara dua lantai dalam dua flight yang sama dengan half landing. Pada pelan setiap flight menunjukkan " + num(P.nT + " @ " + P.G + " = " + P.Lf) + ", dan setiap flight berakhir pada landing atau pada lantai di atas, yang membentuk anak tangga terakhirnya. Cari bilangan riser dalam satu flight, rise R dan 2R + G.");
    },
    fields: [{ id: "nr", label: ["n<sub>R</sub> (one flight)", "n<sub>R</sub> (satu flight)"], unit: "", fn: function (P) { return P.nR; }, rtol: 0, atol: 0.01 },
             { id: "r", label: ["R", "R"], unit: "mm", fn: function (P) { return P.R; }, rtol: 0.005 },
             { id: "c", label: ["2R + G", "2R + G"], unit: "mm", fn: function (P) { return P.c; }, rtol: 0.004 }],
    hints: [function () { return bi("Each flight climbs half of the storey height.", "Setiap flight mendaki separuh daripada ketinggian tingkat."); },
            function () { return bi("The landing or the floor is the last step of each flight, so a flight has one riser more than the treads drawn on its slope.", "Landing atau lantai ialah anak tangga terakhir setiap flight, jadi satu flight mempunyai satu riser lebih daripada tread yang dilukis pada cerunnya."); },
            function () { return bi("R = (H/2)/n<sub>R</sub>. Then check R ≤ 180 mm and G ≥ 255 mm (By-law 106), and 2R + G between 550 and 700 mm.", "R = (H/2)/n<sub>R</sub>. Kemudian semak R ≤ 180 mm dan G ≥ 255 mm (By-law 106), dan 2R + G di antara 550 dan 700 mm."); }],
    solution: function (P) {
      var ok = P.c >= 550 && P.c <= 700;
      return sol([bi("Each flight climbs ", "Setiap flight mendaki ") + P.H + "/2 = " + (P.H / 2) + " mm",
        "n<sub>R</sub> = " + P.nT + " + 1 = " + P.nR + bi(" risers: the landing or the floor is the last step", " riser: landing atau lantai ialah anak tangga terakhir"),
        "R = " + (P.H / 2) + "/" + P.nR + " = " + P.R + " mm; 2R + G = 2 × " + P.R + " + " + P.G + " = " + P.c + " mm",
        bi("By-law 106: R = " + P.R + " ≤ 180 ✓, G = " + P.G + " ≥ 255 ✓; 2R + G " + (ok ? "within 550 to 700 mm ✓" : "outside 550 to 700 mm: legal, but not comfortable"),
           "By-law 106: R = " + P.R + " ≤ 180 ✓, G = " + P.G + " ≥ 255 ✓; 2R + G " + (ok ? "dalam julat 550 hingga 700 mm ✓" : "di luar julat 550 hingga 700 mm: sah, tetapi tidak selesa")),
        bi("Taking n<sub>R</sub> = " + P.nT + " would give R = " + fmt(P.H / 2 / P.nT, 1) + " mm: a stair that does not fit the storey (Notes §2).", "Mengambil n<sub>R</sub> = " + P.nT + " memberi R = " + fmt(P.H / 2 / P.nT, 1) + " mm: tangga yang tidak sepadan dengan ketinggian tingkat (Nota §2).")]);
    }
  });

  /* ---------- B2 the effective span on a landing ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.nG = pick(r, [8, 9, 10, 11, 12]); P.G = pick(r, [255, 260, 265, 270, 275, 280, 290, 300]); P.La = P.nG * P.G;
      P.tb = pick(r, [200, 225, 250, 300]); P.Ld = pick(r, [1200, 1350, 1500, 1650, 1800, 2000, 2100, 2400]);
      P.Lb2 = Math.min(P.Ld, 1800); P.L = P.La + (P.tb + P.Lb2) / 2; P.lf = P.La + P.tb / 2; P.lL = P.Lb2 / 2;
      return P;
    },
    text: function (P) {
      return bi("A flight rises from a beam " + num(P.tb) + " mm wide to a landing " + num(P.Ld) + " mm deep that spans between two walls. Its slope shows " + num(P.nG) + " goings of " + num(P.G) + " mm on plan. Find the effective span L of the flight, the length of flight l<sub>f</sub> and the length of landing l<sub>L</sub> inside that span.",
                "Satu flight naik dari beam selebar " + num(P.tb) + " mm hingga ke landing sedalam " + num(P.Ld) + " mm yang merentang di antara dua dinding. Cerunnya menunjukkan " + num(P.nG) + " going sepanjang " + num(P.G) + " mm pada pelan. Cari effective span L flight, panjang flight l<sub>f</sub> dan panjang landing l<sub>L</sub> di dalam span itu.");
    },
    fields: [{ id: "l", label: ["L", "L"], unit: "mm", fn: function (P) { return P.L; }, rtol: 0.002 },
             { id: "lf", label: ["l<sub>f</sub>", "l<sub>f</sub>"], unit: "mm", fn: function (P) { return P.lf; }, rtol: 0.002 },
             { id: "ll", label: ["l<sub>L</sub>", "l<sub>L</sub>"], unit: "mm", fn: function (P) { return P.lL; }, rtol: 0.002 }],
    hints: [function () { return bi("L<sub>a</sub>, the clear horizontal distance between the beam and the landing, is the goings on plan.", "L<sub>a</sub>, jarak mengufuk bersih di antara beam dan landing, ialah going pada pelan."); },
            function () { return bi("L = L<sub>a</sub> + ½(L<sub>b1</sub> + L<sub>b2</sub>), each L<sub>b</sub> not more than 1800 mm.", "L = L<sub>a</sub> + ½(L<sub>b1</sub> + L<sub>b2</sub>), setiap L<sub>b</sub> tidak melebihi 1800 mm."); },
            function () { return bi("The flight part runs to the centre of the beam: l<sub>f</sub> = L<sub>a</sub> + ½L<sub>b1</sub>; the rest of the span is landing: l<sub>L</sub> = ½L<sub>b2</sub>.", "Bahagian flight berjalan hingga tengah beam: l<sub>f</sub> = L<sub>a</sub> + ½L<sub>b1</sub>; baki span ialah landing: l<sub>L</sub> = ½L<sub>b2</sub>."); }],
    solution: function (P) {
      return sol(["L<sub>a</sub> = " + P.nG + " × " + P.G + " = " + P.La + " mm; L<sub>b1</sub> = " + P.tb + " mm; L<sub>b2</sub> = min(" + P.Ld + ", 1800) = " + P.Lb2 + " mm",
        "L = " + P.La + " + ½ × (" + P.tb + " + " + P.Lb2 + ") = " + mm(P.L) + " mm",
        "l<sub>f</sub> = " + P.La + " + " + P.tb + "/2 = " + mm(P.lf) + " mm; l<sub>L</sub> = " + P.Lb2 + "/2 = " + mm(P.lL) + " mm",
        P.Ld > 1800 ? bi("The landing is deeper than 1.8 m, so only 1800 mm of it is counted: the span ends 900 mm into it.", "Landing lebih dalam daripada 1.8 m, jadi hanya 1800 mm daripadanya dikira: span berakhir 900 mm ke dalamnya.")
                    : bi("The span ends at the centre of the landing.", "Span berakhir di tengah landing."),
        bi("The landing strip l<sub>L</sub> is part of the span and carries the landing load (Notes §3).", "Jalur landing l<sub>L</sub> sebahagian daripada span dan memikul load landing (Nota §3).")]);
    }
  });

  /* ---------- B3 load, moment and reaction ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = loads(r);
      P.La = pick(r, [8, 9, 10, 11]) * pick(r, [255, 260, 270, 280]); P.tb = pick(r, [200, 250, 300]); P.Ld = pick(r, [1200, 1350, 1500, 1800, 2000]);
      P.Lb2 = Math.min(P.Ld, 1800); P.L = (P.La + (P.tb + P.Lb2) / 2) / 1000; P.lf = (P.La + P.tb / 2) / 1000; P.lL = P.Lb2 / 2000;
      P.Ff = P.nf * P.lf; P.FL = P.nL * P.lL; P.F = P.Ff + P.FL; P.M = P.F * P.L / 10;
      P.xf = P.lf / 2; P.xL = P.lf + P.lL / 2; P.VA = (P.Ff * P.xf + P.FL * P.xL - P.M) / P.L; P.VB = P.F - P.VA;
      return P;
    },
    text: function (P) {
      return bi("A flight rests at its head on a landing " + num(P.Ld) + " mm deep and at its foot on a beam " + num(P.tb) + " mm wide, continuous with it; the slope is " + num(P.La) + " mm on plan. The design loads are n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " kN/m² on the flight and n<sub>L</sub> = " + num(fmt(P.nL, 2)) + " kN/m² on the landing. For a 1 m strip, find the total load F on the span, the design moment M and the reaction V<sub>A</sub> that the flight puts on the landing.",
                "Satu flight bertumpu di kepalanya pada landing sedalam " + num(P.Ld) + " mm dan di kakinya pada beam selebar " + num(P.tb) + " mm, selanjar dengannya; cerunnya " + num(P.La) + " mm pada pelan. Design load ialah n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " kN/m² pada flight dan n<sub>L</sub> = " + num(fmt(P.nL, 2)) + " kN/m² pada landing. Bagi jalur 1 m, cari jumlah load F pada span, design moment M dan reaction V<sub>A</sub> yang diletakkan oleh flight pada landing.");
    },
    fields: [{ id: "f", label: ["F", "F"], unit: "kN", fn: function (P) { return P.F; }, rtol: 0.006 },
             { id: "m", label: ["M", "M"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.008 },
             { id: "va", label: ["V<sub>A</sub>", "V<sub>A</sub>"], unit: "kN", fn: function (P) { return P.VA; }, rtol: 0.012 }],
    hints: [function () { return bi("L = L<sub>a</sub> + ½(L<sub>b1</sub> + min(L<sub>b2</sub>, 1800)); l<sub>f</sub> = L<sub>a</sub> + ½L<sub>b1</sub>; l<sub>L</sub> = L − l<sub>f</sub>.", "L = L<sub>a</sub> + ½(L<sub>b1</sub> + min(L<sub>b2</sub>, 1800)); l<sub>f</sub> = L<sub>a</sub> + ½L<sub>b1</sub>; l<sub>L</sub> = L − l<sub>f</sub>."); },
            function () { return bi("F = n<sub>f</sub>l<sub>f</sub> + n<sub>L</sub>l<sub>L</sub>: the landing strip inside the span carries n<sub>L</sub>. One end is continuous, so M = FL/10.", "F = n<sub>f</sub>l<sub>f</sub> + n<sub>L</sub>l<sub>L</sub>: jalur landing di dalam span memikul n<sub>L</sub>. Satu hujung selanjar, jadi M = FL/10."); },
            function () { return bi("Moments about the beam end B (x from B; M<sub>B</sub> = M, M<sub>A</sub> = 0): V<sub>A</sub>L = n<sub>f</sub>l<sub>f</sub> × l<sub>f</sub>/2 + n<sub>L</sub>l<sub>L</sub> × (l<sub>f</sub> + l<sub>L</sub>/2) − M.", "Moment pada hujung beam B (x dari B; M<sub>B</sub> = M, M<sub>A</sub> = 0): V<sub>A</sub>L = n<sub>f</sub>l<sub>f</sub> × l<sub>f</sub>/2 + n<sub>L</sub>l<sub>L</sub> × (l<sub>f</sub> + l<sub>L</sub>/2) − M."); }],
    solution: function (P) {
      return sol(["L = " + P.La + " + ½ × (" + P.tb + " + " + P.Lb2 + ") = " + fmt(P.L * 1000, 0) + " mm; l<sub>f</sub> = " + fmt(P.lf, 3) + " m; l<sub>L</sub> = " + fmt(P.lL, 3) + " m",
        "F = " + fmt(P.nf, 2) + " × " + fmt(P.lf, 3) + " + " + fmt(P.nL, 2) + " × " + fmt(P.lL, 3) + " = " + fmt(P.Ff, 3) + " + " + fmt(P.FL, 3) + " = " + fmt(P.F, 3) + " kN",
        "M = FL/10 = " + fmt(P.F, 3) + " × " + fmt(P.L, 3) + "/10 = " + fmt(P.M, 3) + " kN m/m",
        "V<sub>A</sub> = (" + fmt(P.Ff, 3) + " × " + fmt(P.xf, 4) + " + " + fmt(P.FL, 3) + " × " + fmt(P.xL, 4) + " − " + fmt(P.M, 3) + ")/" + fmt(P.L, 3) + " = " + fmt(P.VA, 3) + " kN/m; V<sub>B</sub> = " + fmt(P.VB, 3) + " kN/m",
        bi("Leaving out the landing strip would give F = " + fmt(P.Ff, 2) + " kN, " + fmt(100 * P.FL / P.F, 0) + " % less (Notes §3).", "Meninggalkan jalur landing akan memberi F = " + fmt(P.Ff, 2) + " kN, " + fmt(100 * P.FL / P.F, 0) + " % kurang (Nota §3).")]);
    }
  });

  /* ---------- B4 the landing between walls ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P, k = 0;
      do {
        P = {};
        P.bF = pick(r, [1100, 1200, 1300, 1400, 1500]); P.well = pick(r, [100, 150, 200, 250]); P.tw = pick(r, [150, 200, 230]);
        P.bL = P.bF + pick(r, [0, 150, 300]); P.hL = pick(r, [150, 175, 200]); P.gk = pick(r, [1.0, 1.2, 1.5]); P.qk = pick(r, [3.0, 4.0]);
        P.VA = step(r, 14, 26, 0.1); P.fck = pick(r, [25, 30]); P.pL = pick(r, [10, 12]);
        P.nL = 1.35 * (25 * P.hL / 1000 + P.gk) + 1.5 * P.qk; P.wL = P.nL * P.bL / 1000 + P.VA;
        P.LL = (2 * P.bF + P.well + P.tw) / 1000; P.ML = P.wL * P.LL * P.LL / 8;
        P.dL = P.hL - 25 - 10 - P.pL / 2; P.f = flex(P.ML, P.bL, P.dL, P.fck);
        k++;
      } while (k < 60 && !(P.f.K < 0.15));
      return P;
    },
    text: function (P) {
      return bi("An open-well stair has two flights " + num(P.bF) + " mm wide either side of a " + num(P.well) + " mm well. The landing at their heads is " + num(P.bL) + " mm deep and " + num(P.hL) + " mm thick, and spans between two walls " + num(P.tw) + " mm thick at the outer sides of the flights. Finishes " + num(fmt(P.gk, 1)) + " kN/m², imposed load " + num(fmt(P.qk, 1)) + " kN/m²; the flights put V<sub>A</sub> = " + num(fmt(P.VA, 1)) + " kN per metre width on the landing. C" + num(P.fck) + ", f<sub>yk</sub> = 500 N/mm², cover 25 mm; the flight bars are H10 and the landing bars H" + num(P.pL) + ", in the inner layer. Find the load on the landing per metre of its span, its design moment and the steel it needs.",
                "Satu tangga open-well mempunyai dua flight selebar " + num(P.bF) + " mm di kiri dan kanan well " + num(P.well) + " mm. Landing di kepala flight sedalam " + num(P.bL) + " mm dan setebal " + num(P.hL) + " mm, serta merentang di antara dua dinding setebal " + num(P.tw) + " mm di sisi luar flight. Kemasan " + num(fmt(P.gk, 1)) + " kN/m², imposed load " + num(fmt(P.qk, 1)) + " kN/m²; flight meletakkan V<sub>A</sub> = " + num(fmt(P.VA, 1)) + " kN per meter lebar pada landing. C" + num(P.fck) + ", f<sub>yk</sub> = 500 N/mm², cover 25 mm; bar flight ialah H10 dan bar landing H" + num(P.pL) + ", dalam lapisan dalam. Cari load pada landing per meter span-nya, design moment-nya dan steel yang diperlukannya.");
    },
    fields: [{ id: "w", label: ["w<sub>L</sub>", "w<sub>L</sub>"], unit: "kN/m", fn: function (P) { return P.wL; }, rtol: 0.006 },
             { id: "m", label: ["M<sub>L</sub>", "M<sub>L</sub>"], unit: "kN m", fn: function (P) { return P.ML; }, rtol: 0.008 },
             { id: "as", label: ["A<sub>s</sub>", "A<sub>s</sub>"], unit: "mm²", fn: function (P) { return P.f.As; }, rtol: 0.012 }],
    hints: [function () { return bi("n<sub>L</sub> = 1.35(25h<sub>L</sub> + g<sub>k</sub>) + 1.5q<sub>k</sub>; w<sub>L</sub> = n<sub>L</sub>b<sub>L</sub> + V<sub>A</sub>, with b<sub>L</sub> the depth of the landing in m.", "n<sub>L</sub> = 1.35(25h<sub>L</sub> + g<sub>k</sub>) + 1.5q<sub>k</sub>; w<sub>L</sub> = n<sub>L</sub>b<sub>L</sub> + V<sub>A</sub>, dengan b<sub>L</sub> kedalaman landing dalam m."); },
            function () { return bi("The landing spans between the wall centres: L<sub>L</sub> = 2b<sub>F</sub> + well + t<sub>w</sub>. M<sub>L</sub> = w<sub>L</sub>L<sub>L</sub>²/8.", "Landing merentang di antara pusat dinding: L<sub>L</sub> = 2b<sub>F</sub> + well + t<sub>w</sub>. M<sub>L</sub> = w<sub>L</sub>L<sub>L</sub>²/8."); },
            function () { return bi("d<sub>L</sub> = h<sub>L</sub> − c − φ<sub>flight</sub> − φ<sub>L</sub>/2; K and z ≤ 0.95d with b = b<sub>L</sub>; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z) over the whole breadth.", "d<sub>L</sub> = h<sub>L</sub> − c − φ<sub>flight</sub> − φ<sub>L</sub>/2; K dan z ≤ 0.95d dengan b = b<sub>L</sub>; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z) bagi seluruh lebar."); }],
    solution: function (P) {
      var f = P.f;
      return sol(["n<sub>L</sub> = 1.35 × (25 × " + fmt(P.hL / 1000, 3) + " + " + fmt(P.gk, 1) + ") + 1.5 × " + fmt(P.qk, 1) + " = " + fmt(P.nL, 4) + " kN/m²",
        "w<sub>L</sub> = " + fmt(P.nL, 4) + " × " + fmt(P.bL / 1000, 2) + " + " + fmt(P.VA, 1) + " = " + fmt(P.wL, 3) + " kN/m",
        "L<sub>L</sub> = (2 × " + P.bF + " + " + P.well + " + " + P.tw + ")/1000 = " + fmt(P.LL, 3) + " m; M<sub>L</sub> = " + fmt(P.wL, 3) + " × " + fmt(P.LL, 3) + "²/8 = " + fmt(P.ML, 3) + " kN m",
        "d<sub>L</sub> = " + P.hL + " − 25 − 10 − " + P.pL + "/2 = " + P.dL + " mm; K = " + fmt(P.ML, 3) + " × 10⁶/(" + P.bL + " × " + P.dL + "² × " + P.fck + ") = " + fmt(f.K, 4) + "; z = " + fmt(f.z, 2) + " mm" + (f.z0 > 0.95 * P.dL ? " (0.95d)" : ""),
        "A<sub>s</sub> = " + fmt(P.ML, 3) + " × 10⁶/(0.87 × 500 × " + fmt(f.z, 2) + ") = " + fmt(f.As, 0) + " mm²",
        bi("Then shear, deflection with K = 1.0, and the spacing ≤ min(2h<sub>L</sub>, 250) mm (Notes §4).", "Kemudian shear, deflection dengan K = 1.0, dan jarak ≤ min(2h<sub>L</sub>, 250) mm (Nota §4).")]);
    }
  });

  /* ---------- B5 two flights at right angles ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P = loads(r);
      P.La = pick(r, [8, 9, 10, 11]) * pick(r, [255, 260, 270, 280]); P.tA = pick(r, [200, 250, 300]); P.Ld = pick(r, [1200, 1350, 1500]); P.tB = pick(r, [150, 200, 230]);
      P.nLp = P.nL / 2; P.lf = (P.La + P.tA / 2) / 1000; P.lLB = (P.Ld + P.tB / 2) / 1000; P.L = P.lf + P.lLB;
      P.F = P.nf * P.lf + P.nLp * P.lLB; P.M = P.F * P.L / 10;
      return P;
    },
    text: function (P) {
      return bi("Two flights meet at right angles round an open well and share a quarter landing " + num(P.Ld) + " mm deep. The flight considered rises from a beam " + num(P.tA) + " mm wide, continuous with it, through the landing to a wall " + num(P.tB) + " mm thick on which it bears simply; its slope is " + num(P.La) + " mm on plan. n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " and n<sub>L</sub> = " + num(fmt(P.nL, 2)) + " kN/m². Find the landing load per m² that enters this flight’s span, the total load F and the design moment M, per metre width.",
                "Dua flight bertemu pada sudut tepat mengelilingi open well dan berkongsi quarter landing sedalam " + num(P.Ld) + " mm. Flight yang dipertimbangkan naik dari beam selebar " + num(P.tA) + " mm, selanjar dengannya, melalui landing hingga ke dinding setebal " + num(P.tB) + " mm tempat ia bertumpu secara mudah; cerunnya " + num(P.La) + " mm pada pelan. n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " dan n<sub>L</sub> = " + num(fmt(P.nL, 2)) + " kN/m². Cari load landing per m² yang masuk ke dalam span flight ini, jumlah load F dan design moment M, per meter lebar.");
    },
    fields: [{ id: "nl", label: ["n′<sub>L</sub>", "n′<sub>L</sub>"], unit: "kN/m²", fn: function (P) { return P.nLp; }, rtol: 0.005 },
             { id: "f", label: ["F", "F"], unit: "kN", fn: function (P) { return P.F; }, rtol: 0.006 },
             { id: "m", label: ["M", "M"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.008 }],
    hints: [function () { return bi("The landing is common to two spans at right angles round the well: each flight carries half of its load (Mosley §8.8.2).", "Landing sepunya bagi dua span bersudut tepat mengelilingi well: setiap flight memikul separuh daripada load-nya (Mosley §8.8.2)."); },
            function () { return bi("The span runs from the centre of the beam, through the landing, to the centre of the wall: L = L<sub>a</sub> + t<sub>A</sub>/2 + L<sub>land</sub> + t<sub>B</sub>/2.", "Span berjalan dari tengah beam, melalui landing, hingga tengah dinding: L = L<sub>a</sub> + t<sub>A</sub>/2 + L<sub>land</sub> + t<sub>B</sub>/2."); },
            function () { return bi("F = n<sub>f</sub>(L<sub>a</sub> + t<sub>A</sub>/2) + ½n<sub>L</sub>(L<sub>land</sub> + t<sub>B</sub>/2); one end is continuous: M = FL/10.", "F = n<sub>f</sub>(L<sub>a</sub> + t<sub>A</sub>/2) + ½n<sub>L</sub>(L<sub>land</sub> + t<sub>B</sub>/2); satu hujung selanjar: M = FL/10."); }],
    solution: function (P) {
      return sol(["n′<sub>L</sub> = " + fmt(P.nL, 2) + "/2 = " + fmt(P.nLp, 3) + " kN/m²",
        "l<sub>f</sub> = (" + P.La + " + " + P.tA + "/2)/1000 = " + fmt(P.lf, 3) + " m; l<sub>LB</sub> = (" + P.Ld + " + " + P.tB + "/2)/1000 = " + fmt(P.lLB, 3) + " m; L = " + fmt(P.L, 3) + " m",
        "F = " + fmt(P.nf, 2) + " × " + fmt(P.lf, 3) + " + " + fmt(P.nLp, 3) + " × " + fmt(P.lLB, 3) + " = " + fmt(P.nf * P.lf, 3) + " + " + fmt(P.nLp * P.lLB, 3) + " = " + fmt(P.F, 3) + " kN",
        "M = FL/10 = " + fmt(P.F, 3) + " × " + fmt(P.L, 3) + "/10 = " + fmt(P.M, 3) + " kN m/m",
        bi("Without the halving F would be " + fmt(P.nf * P.lf + P.nL * P.lLB, 2) + " kN. The second flight carries the other half (Notes §5).", "Tanpa dibahagi dua, F menjadi " + fmt(P.nf * P.lf + P.nL * P.lLB, 2) + " kN. Flight kedua memikul separuh lagi (Nota §5).")]);
    }
  });

  /* ---------- B6 a flight built into walls ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = { nf: r2(step(r, 13.5, 17.5, 0.01)) };
      P.bF = pick(r, [1000, 1100, 1200, 1300, 1400, 1500]); P.nw = pick(r, [1, 2]); P.L = step(r, 2.6, 4.0, 0.05);
      P.bld = P.bF - 150 * P.nw; P.bef = P.bF + 75 * P.nw; P.kw = P.bld / P.bef; P.nfw = P.kw * P.nf; P.F = P.nfw * P.L; P.M = P.F * P.L / 10;
      return P;
    },
    text: function (P) {
      var side = P.nw > 1 ? bi("both sides", "kedua-dua sisi") : bi("one side", "satu sisi");
      return bi("A flight " + num(P.bF) + " mm wide spans " + num(fmt(P.L, 2)) + " m between two beams, continuous at both ends, with no landing. It is built at least 110 mm into a wall on " + side + ". n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " kN/m². With the BS 8110 rule of the course, find κ<sub>w</sub>, the load per m² on a 1 m strip of the effective breadth, and the design moment per metre of that breadth.",
                "Satu flight selebar " + num(P.bF) + " mm merentang " + num(fmt(P.L, 2)) + " m di antara dua beam, selanjar di kedua-dua hujung, tanpa landing. Ia dibina sekurang-kurangnya 110 mm ke dalam dinding di " + side + ". n<sub>f</sub> = " + num(fmt(P.nf, 2)) + " kN/m². Dengan peraturan BS 8110 yang digunakan oleh kursus, cari κ<sub>w</sub>, load per m² pada jalur 1 m daripada lebar berkesan, dan design moment per meter lebar tersebut.");
    },
    fields: [{ id: "kw", label: ["κ<sub>w</sub>", "κ<sub>w</sub>"], unit: "", fn: function (P) { return P.kw; }, rtol: 0.003, atol: 0.002 },
             { id: "nfw", label: ["n′<sub>f</sub>", "n′<sub>f</sub>"], unit: "kN/m²", fn: function (P) { return P.nfw; }, rtol: 0.006 },
             { id: "m", label: ["M", "M"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.008 }],
    hints: [function () { return bi("Leave a 150 mm strip at each embedded side out of the loaded width: b<sub>ld</sub> = b<sub>F</sub> − 150n<sub>w</sub>.", "Keluarkan jalur 150 mm di setiap sisi yang tertanam daripada lebar yang dibebani: b<sub>ld</sub> = b<sub>F</sub> − 150n<sub>w</sub>."); },
            function () { return bi("The section works over b<sub>eff</sub> = b<sub>F</sub> + 75n<sub>w</sub>; κ<sub>w</sub> = b<sub>ld</sub>/b<sub>eff</sub> and n′<sub>f</sub> = κ<sub>w</sub>n<sub>f</sub>.", "Keratan bekerja di sepanjang b<sub>eff</sub> = b<sub>F</sub> + 75n<sub>w</sub>; κ<sub>w</sub> = b<sub>ld</sub>/b<sub>eff</sub> dan n′<sub>f</sub> = κ<sub>w</sub>n<sub>f</sub>."); },
            function () { return bi("F = n′<sub>f</sub>L; both ends are continuous, so M = FL/10.", "F = n′<sub>f</sub>L; kedua-dua hujung selanjar, jadi M = FL/10."); }],
    solution: function (P) {
      return sol(["b<sub>ld</sub> = " + P.bF + " − 150 × " + P.nw + " = " + P.bld + " mm; b<sub>eff</sub> = " + P.bF + " + 75 × " + P.nw + " = " + P.bef + " mm",
        "κ<sub>w</sub> = " + P.bld + "/" + P.bef + " = " + fmt(P.kw, 4) + "; n′<sub>f</sub> = " + fmt(P.kw, 4) + " × " + fmt(P.nf, 2) + " = " + fmt(P.nfw, 3) + " kN/m²",
        "F = " + fmt(P.nfw, 3) + " × " + fmt(P.L, 2) + " = " + fmt(P.F, 3) + " kN; M = FL/10 = " + fmt(P.M, 3) + " kN m" + bi(" per metre of b<sub>eff</sub>", " per meter b<sub>eff</sub>"),
        bi("Clear of the walls M would be " + fmt(P.nf * P.L * P.L / 10, 2) + " kN m/m. The bars are spaced across b<sub>eff</sub>, into the chases (Notes §6).", "Tanpa dinding, M menjadi " + fmt(P.nf * P.L * P.L / 10, 2) + " kN m/m. Bar dijarakkan di sepanjang b<sub>eff</sub>, hingga ke dalam alur (Nota §6).")]);
    }
  });

  EX.ready();
})();
