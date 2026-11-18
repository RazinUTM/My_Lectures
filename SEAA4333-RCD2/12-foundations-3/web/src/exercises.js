/* SEAA 4333 Unit 12 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's pile-cap model):
   N_Ed = 1.35 G_k + 1.5 Q_k; truss: two piles T = N s/(4d), d = h - 75 - phi/2; three piles T = N s/(9d) per side,
   d = h - 75 - 2.5 phi; four piles T = N s/(8d) per truss, two trusses each way, d = h - 75 - 1.5 phi; A_s = T/(0.87 f_yk);
   A_s,min = max(0.26 f_ctm/f_yk, 0.0013) b d (0.0015062 b d for C30/37);
   beam theory, 2 x 3 group with M about y: F_max = N/6 + M s/(4 s^2), M_xx = 2 F_max (s - c/2), M_yy = 3 (N/6)(s/2 - c/2);
   shear at phi/5 inside the pile face: a_v = s/2 - c/2 - 0.3 phi, beta = max(a_v, 0.5 d)/(2 d), V_Ed,red = beta V_Ed,
   V_Rd,c = v_min b d (bars not counted), v_min = 0.035 k^1.5 sqrt(f_ck), k = 1 + sqrt(200/d) <= 2;
   column face: beta = 1 + 0.6 (M/N)(u0/W0), W0 = 1.5 c^2, v_Ed,0 = beta N_Ed/(u0 d), d = h - 75 - phi, against 0.4 nu f_cd. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  var RMIN = Math.max(0.26 * 0.3 * Math.pow(30, 2 / 3) / 500, 0.0013);
  function vmin(d) { var k = Math.min(1 + Math.sqrt(200 / d), 2); return { k: k, v: 0.035 * Math.pow(k, 1.5) * Math.sqrt(30) }; }

  /* ---------- B1 two-pile cap: the tie ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.pp = pick(r, [350, 400, 450, 500, 550]); P.s = 3 * P.pp; P.c = pick(r, [300, 350, 400, 450]);
      P.Gk = step(r, 400, 1100, 25); P.Qk = step(r, 150, 600, 25); P.N = 1.35 * P.Gk + 1.5 * P.Qk;
      P.h = 2 * P.pp + 100 + pick(r, [0, 0, 100]); P.phi = pick(r, [16, 20, 25]);
      P.d = P.h - 75 - P.phi / 2; P.T = P.N * P.s / (4 * P.d); P.As = P.T * 1e3 / 435;
      return P;
    },
    text: function (P) {
      return bi("A " + num(P.c) + " mm square column carries G<sub>k</sub> = " + num(P.Gk) + " kN and Q<sub>k</sub> = " + num(P.Qk) + " kN on a two-pile cap. The piles are " + num(P.pp) + " mm in diameter at 3φ; the cap is " + num(P.h) + " mm deep with 75 mm cover and one layer of H" + num(P.phi) + " tie bars. By the truss analogy, find the effective depth of the tie, the tie force and the area of the tie bars.",
                "Satu column " + num(P.c) + " mm segi empat sama membawa G<sub>k</sub> = " + num(P.Gk) + " kN dan Q<sub>k</sub> = " + num(P.Qk) + " kN di atas pile cap dua pile. Pile berdiameter " + num(P.pp) + " mm pada 3φ; pile cap sedalam " + num(P.h) + " mm dengan cover 75 mm dan satu lapisan bar tie H" + num(P.phi) + ". Melalui truss analogy, cari effective depth tie, daya tie dan luas bar tie.");
    },
    fields: [{ id: "d", label: ["d", "d"], unit: "mm", fn: function (P) { return P.d; }, rtol: 0.002, atol: 1 },
             { id: "t", label: ["T", "T"], unit: "kN", fn: function (P) { return P.T; }, rtol: 0.005 },
             { id: "as", label: ["A<sub>s</sub>", "A<sub>s</sub>"], unit: "mm²", fn: function (P) { return P.As; }, rtol: 0.01 }],
    hints: [function () { return bi("One layer of bars: d = h − c − φ/2.", "Satu lapisan bar: d = h − c − φ/2."); },
            function () { return bi("N<sub>Ed</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>; similar triangles at a pile node give T = N<sub>Ed</sub>s/(4d), with s = 3φ.", "N<sub>Ed</sub> = 1.35G<sub>k</sub> + 1.5Q<sub>k</sub>; segi tiga serupa di nod pile memberi T = N<sub>Ed</sub>s/(4d), dengan s = 3φ."); },
            function () { return bi("A<sub>s</sub> = T/(0.87f<sub>yk</sub>) = T × 10³/435.", "A<sub>s</sub> = T/(0.87f<sub>yk</sub>) = T × 10³/435."); }],
    solution: function (P) {
      return sol(["N<sub>Ed</sub> = 1.35 × " + P.Gk + " + 1.5 × " + P.Qk + " = " + fmt(P.N, 1) + " kN; s = 3 × " + P.pp + " = " + P.s + " mm",
        "d = " + P.h + " − 75 − " + P.phi + "/2 = " + fmt(P.d, 1) + " mm",
        "T = " + fmt(P.N, 1) + " × " + P.s + "/(4 × " + fmt(P.d, 1) + ") = " + fmt(P.T, 1) + " kN",
        "A<sub>s</sub> = " + fmt(P.T, 1) + " × 10³/435 = " + fmt(P.As, 0) + " mm²",
        bi("Then check A<sub>s,min</sub> over the cap width and choose the bars, bent up at both ends (Notes §2, §6).", "Kemudian semak A<sub>s,min</sub> merentas lebar pile cap dan pilih bar, dibengkokkan ke atas di kedua-dua hujung (Nota §2, §6).")]);
    }
  });

  /* ---------- B2 four-pile cap: the ties each way ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.pp = pick(r, [400, 450, 500, 550, 600]); P.s = 3 * P.pp; P.B = 4 * P.pp + 300;
      P.Gk = step(r, 1500, 4000, 50); P.Qk = step(r, 800, 2500, 50); P.N = 1.35 * P.Gk + 1.5 * P.Qk;
      P.h = 2 * P.pp + 100 + pick(r, [0, 100, 200]); P.phi = pick(r, [20, 25, 32]);
      P.d = P.h - 75 - 1.5 * P.phi; P.T = P.N * P.s / (8 * P.d); P.As = 2 * P.T * 1e3 / 435; P.Asmin = RMIN * P.B * P.d;
      return P;
    },
    text: function (P) {
      return bi("Four piles of " + num(P.pp) + " mm diameter at 3φ carry a column with G<sub>k</sub> = " + num(P.Gk) + " kN and Q<sub>k</sub> = " + num(P.Qk) + " kN. The cap is " + num(P.B) + " mm square and " + num(P.h) + " mm deep, cover 75 mm, H" + num(P.phi) + " bars in two layers (use the upper layer’s d for both directions), C30/37. Find the force in each truss, the steel needed in each direction and A<sub>s,min</sub>.",
                "Empat pile berdiameter " + num(P.pp) + " mm pada 3φ memikul column dengan G<sub>k</sub> = " + num(P.Gk) + " kN dan Q<sub>k</sub> = " + num(P.Qk) + " kN. Pile cap berukuran " + num(P.B) + " mm segi empat sama dan sedalam " + num(P.h) + " mm, cover 75 mm, bar H" + num(P.phi) + " dalam dua lapisan (guna d lapisan atas bagi kedua-dua arah), C30/37. Cari daya dalam setiap truss, steel yang diperlukan dalam setiap arah dan A<sub>s,min</sub>.");
    },
    fields: [{ id: "t", label: ["T (each truss)", "T (setiap truss)"], unit: "kN", fn: function (P) { return P.T; }, rtol: 0.005 },
             { id: "as", label: ["A<sub>s</sub> (each way)", "A<sub>s</sub> (setiap arah)"], unit: "mm²", fn: function (P) { return P.As; }, rtol: 0.01 },
             { id: "asmin", label: ["A<sub>s,min</sub>", "A<sub>s,min</sub>"], unit: "mm²", fn: function (P) { return P.Asmin; }, rtol: 0.01 }],
    hints: [function () { return bi("Upper layer: d = h − c − 1.5φ.", "Lapisan atas: d = h − c − 1.5φ."); },
            function () { return bi("Each of the two parallel trusses carries N<sub>Ed</sub>/2: T = N<sub>Ed</sub>s/(8d).", "Setiap satu daripada dua truss selari membawa N<sub>Ed</sub>/2: T = N<sub>Ed</sub>s/(8d)."); },
            function () { return bi("The bars in one direction serve both trusses: A<sub>s</sub> = 2T/0.87f<sub>yk</sub>. A<sub>s,min</sub> = 0.0015bd for C30/37, b the whole width.", "Bar dalam satu arah berkhidmat kepada kedua-dua truss: A<sub>s</sub> = 2T/0.87f<sub>yk</sub>. A<sub>s,min</sub> = 0.0015bd bagi C30/37, b seluruh lebar."); }],
    solution: function (P) {
      return sol(["N<sub>Ed</sub> = 1.35 × " + P.Gk + " + 1.5 × " + P.Qk + " = " + fmt(P.N, 1) + " kN; s = " + P.s + " mm",
        "d = " + P.h + " − 75 − 1.5 × " + P.phi + " = " + fmt(P.d, 1) + " mm",
        "T = " + fmt(P.N, 1) + " × " + P.s + "/(8 × " + fmt(P.d, 1) + ") = " + fmt(P.T, 1) + bi(" kN per truss", " kN setiap truss"),
        "A<sub>s</sub> = 2 × " + fmt(P.T, 1) + " × 10³/435 = " + fmt(P.As, 0) + bi(" mm² each way", " mm² setiap arah"),
        "A<sub>s,min</sub> = 0.001506 × " + P.B + " × " + fmt(P.d, 1) + " = " + fmt(P.Asmin, 0) + " mm²" + (P.Asmin > P.As ? bi(": it governs", ": ia menentukan") : ""),
        bi("Bars spread evenly (s = 3φ), bent up at both ends; then shear at φ/5 (B5).", "Bar disebar sekata (s = 3φ), dibengkokkan ke atas di kedua-dua hujung; kemudian shear pada φ/5 (B5).")]);
    }
  });

  /* ---------- B3 three-pile cap ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.pp = pick(r, [350, 400, 450, 500]); P.s = 3 * P.pp;
      P.Gk = step(r, 700, 1800, 25); P.Qk = step(r, 300, 1000, 25); P.N = 1.35 * P.Gk + 1.5 * P.Qk;
      P.h = 2 * P.pp + 100 + pick(r, [0, 100]); P.phi = pick(r, [16, 20, 25]);
      P.d = P.h - 75 - 2.5 * P.phi; P.T = P.N * P.s / (9 * P.d); P.As = P.T * 1e3 / 435;
      return P;
    },
    text: function (P) {
      return bi("Three piles of " + num(P.pp) + " mm diameter at 3φ, at the corners of an equilateral triangle, carry a column with G<sub>k</sub> = " + num(P.Gk) + " kN and Q<sub>k</sub> = " + num(P.Qk) + " kN. The cap is " + num(P.h) + " mm deep, cover 75 mm, with three bands of H" + num(P.phi) + " bars over the pile lines in three layers. Find d for the uppermost band, the tie force in each side and the steel in each band.",
                "Tiga pile berdiameter " + num(P.pp) + " mm pada 3φ, di bucu segi tiga sama sisi, memikul column dengan G<sub>k</sub> = " + num(P.Gk) + " kN dan Q<sub>k</sub> = " + num(P.Qk) + " kN. Pile cap sedalam " + num(P.h) + " mm, cover 75 mm, dengan tiga jalur bar H" + num(P.phi) + " di atas garis pile dalam tiga lapisan. Cari d bagi jalur paling atas, daya tie dalam setiap sisi dan steel dalam setiap jalur.");
    },
    fields: [{ id: "d", label: ["d", "d"], unit: "mm", fn: function (P) { return P.d; }, rtol: 0.002, atol: 1 },
             { id: "t", label: ["T (each side)", "T (setiap sisi)"], unit: "kN", fn: function (P) { return P.T; }, rtol: 0.005 },
             { id: "as", label: ["A<sub>s</sub> (each band)", "A<sub>s</sub> (setiap jalur)"], unit: "mm²", fn: function (P) { return P.As; }, rtol: 0.01 }],
    hints: [function () { return bi("Three layers: the uppermost band sits two bar diameters above the lowest, d = h − c − 2.5φ.", "Tiga lapisan: jalur paling atas berada dua diameter bar di atas yang paling bawah, d = h − c − 2.5φ."); },
            function () { return bi("Mosley Table 10.4 with 2l = s: T = 2N(s/2)/(9d) = N<sub>Ed</sub>s/(9d) in each side.", "Mosley Table 10.4 dengan 2l = s: T = 2N(s/2)/(9d) = N<sub>Ed</sub>s/(9d) dalam setiap sisi."); },
            function () { return bi("A<sub>s</sub> = T/(0.87f<sub>yk</sub>) for each band; A<sub>s,min</sub> is taken over the width across a tie and often governs.", "A<sub>s</sub> = T/(0.87f<sub>yk</sub>) bagi setiap jalur; A<sub>s,min</sub> diambil merentas lebar pada satu tie dan sering menentukan."); }],
    solution: function (P) {
      return sol(["N<sub>Ed</sub> = 1.35 × " + P.Gk + " + 1.5 × " + P.Qk + " = " + fmt(P.N, 1) + " kN; s = " + P.s + " mm",
        "d = " + P.h + " − 75 − 2.5 × " + P.phi + " = " + fmt(P.d, 1) + " mm",
        "T = " + fmt(P.N, 1) + " × " + P.s + "/(9 × " + fmt(P.d, 1) + ") = " + fmt(P.T, 1) + " kN",
        "A<sub>s</sub> = " + fmt(P.T, 1) + " × 10³/435 = " + fmt(P.As, 0) + bi(" mm² in each band", " mm² dalam setiap jalur"),
        bi("Compare with A<sub>s,min</sub> across the tie (app case F11: 887 against 2606 mm²) and check that the outer bars of each band anchor beyond the pile lines.", "Bandingkan dengan A<sub>s,min</sub> merentas tie (kes app F11: 887 berbanding 2606 mm²) dan semak bar luar setiap jalur di-anchor melepasi garis pile.")]);
    }
  });

  /* ---------- B4 six-pile cap: beam theory ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = {};
      P.pp = pick(r, [250, 300, 350, 400]); P.s = 3 * P.pp / 1000; P.c = pick(r, [350, 400, 450, 500]) / 1000;
      P.N = step(r, 3000, 6000, 100); P.M = step(r, 40, 200, 5);
      P.Fm = P.N / 6; P.Fmax = P.Fm + P.M * P.s / (4 * P.s * P.s);
      P.Mxx = 2 * P.Fmax * (P.s - P.c / 2); P.Myy = 3 * P.Fm * (P.s / 2 - P.c / 2);
      return P;
    },
    text: function (P) {
      return bi("Six square piles of " + num(P.pp) + " mm, in two rows of three at 3φ, carry a " + num(fmt(P.c * 1000, 0)) + " mm square column with N<sub>Ed</sub> = " + num(P.N) + " kN and M<sub>Ed</sub> = " + num(P.M) + " kN m about the axis across the rows (the loads change along the rows of three). Leaving out the cap weight, find the largest pile load and, by beam theory, the moments at the column faces for the bars along the length and across.",
                "Enam pile segi empat sama " + num(P.pp) + " mm, dalam dua baris tiga pada 3φ, memikul column segi empat sama " + num(fmt(P.c * 1000, 0)) + " mm dengan N<sub>Ed</sub> = " + num(P.N) + " kN dan M<sub>Ed</sub> = " + num(P.M) + " kN m pada paksi merentas baris (load berubah sepanjang baris tiga). Tanpa berat pile cap, cari load pile terbesar dan, melalui beam theory, moment di muka column bagi bar sepanjang panjang dan merentas.");
    },
    fields: [{ id: "f", label: ["F<sub>max</sub>", "F<sub>max</sub>"], unit: "kN", fn: function (P) { return P.Fmax; }, rtol: 0.005 },
             { id: "mx", label: ["M<sub>xx</sub>", "M<sub>xx</sub>"], unit: "kN m", fn: function (P) { return P.Mxx; }, rtol: 0.01 },
             { id: "my", label: ["M<sub>yy</sub>", "M<sub>yy</sub>"], unit: "kN m", fn: function (P) { return P.Myy; }, rtol: 0.01 }],
    hints: [function () { return bi("Four piles at x = ±s, two on the axis: Σx² = 4s²; F<sub>max</sub> = N<sub>Ed</sub>/6 + M<sub>Ed</sub>s/Σx².", "Empat pile pada x = ±s, dua pada paksi: Σx² = 4s²; F<sub>max</sub> = N<sub>Ed</sub>/6 + M<sub>Ed</sub>s/Σx²."); },
            function () { return bi("Bars along the length: the two end piles beyond the face, s − c/2 from it: M<sub>xx</sub> = 2F<sub>max</sub>(s − c/2).", "Bar sepanjang panjang: dua pile hujung di luar muka, s − c/2 darinya: M<sub>xx</sub> = 2F<sub>max</sub>(s − c/2)."); },
            function () { return bi("Across: a row of three sums to 3N<sub>Ed</sub>/6 whatever the moment, at s/2 − c/2 from the face.", "Merentas: satu baris tiga berjumlah 3N<sub>Ed</sub>/6 walau apa pun moment, pada s/2 − c/2 dari muka."); }],
    solution: function (P) {
      return sol(["s = " + fmt(P.s, 2) + " m; Σx² = 4 × " + fmt(P.s, 2) + "² = " + fmt(4 * P.s * P.s, 3) + " m²",
        "F<sub>max</sub> = " + P.N + "/6 + " + P.M + " × " + fmt(P.s, 2) + "/" + fmt(4 * P.s * P.s, 3) + " = " + fmt(P.Fm, 1) + " + " + fmt(P.Fmax - P.Fm, 1) + " = " + fmt(P.Fmax, 1) + " kN",
        "M<sub>xx</sub> = 2 × " + fmt(P.Fmax, 1) + " × (" + fmt(P.s, 2) + " − " + fmt(P.c / 2, 3) + ") = " + fmt(P.Mxx, 1) + " kN m",
        "M<sub>yy</sub> = 3 × " + fmt(P.Fm, 1) + " × (" + fmt(P.s / 2, 3) + " − " + fmt(P.c / 2, 3) + ") = " + fmt(P.Myy, 1) + " kN m",
        bi("The larger moment takes the outer layer (d<sub>x</sub> = h − c − φ/2); expect A<sub>s,min</sub> to govern across (Faded Example 12.2).", "Moment yang lebih besar mengambil lapisan luar (d<sub>x</sub> = h − c − φ/2); jangkakan A<sub>s,min</sub> menentukan merentas (Faded Example 12.2).")]);
    }
  });

  /* ---------- B5 shear at the phi/5 section: a four-pile cap, or the long direction of a six-pile cap ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 80; t++) {
        P = {};
        P.six = r() < 0.5;
        P.pp = pick(r, P.six ? [250, 300, 350, 400] : [400, 450, 500, 550]); P.s = 3 * P.pp; P.c = pick(r, P.six ? [350, 400, 450, 500] : [400, 450, 500, 550, 600]); P.B = 4 * P.pp + 300;
        P.N = P.six ? step(r, 2500, 6000, 100) : step(r, 3000, 9000, 100); P.h = 2 * P.pp + 100 + 100 * Math.floor(r() * 6); P.phi = pick(r, P.six ? [16, 20] : [20, 25]);
        P.d = P.h - 75 - (P.six ? 0.5 : 1.5) * P.phi; P.V = P.six ? P.N / 3 : P.N / 2;
        P.av = P.six ? P.s - P.c / 2 - 0.3 * P.pp : P.s / 2 - P.c / 2 - 0.3 * P.pp;
        P.beta = Math.min(Math.max(P.av, 0.5 * P.d) / (2 * P.d), 1); P.Vr = P.beta * P.V;
        var m = vmin(P.d); P.k = m.k; P.vm = m.v; P.VRc = m.v * P.B * P.d / 1000; P.ratio = P.Vr / P.VRc;
        if (P.av < 120 || P.ratio < 0.6 || P.ratio > 1.4) continue;
        return P;
      }
      return P;
    },
    text: function (P) {
      if (P.six) return bi("A six-pile cap, two rows of three square piles of " + num(P.pp) + " mm at 3φ, is " + num(P.B) + " mm wide and " + num(P.h) + " mm deep, under a " + num(P.c) + " mm square column with N<sub>Ed</sub> = " + num(P.N) + " kN (no moment). The bars along the length, H" + num(P.phi) + " in the outer layer (cover 75 mm), are bent up and anchored beyond the piles but do not run l<sub>bd</sub> + d past the shear section. C30/37. At the section across the width, φ/5 inside the end row, find β, V<sub>Ed,red</sub> and V<sub>Rd,c</sub>.",
                "Satu pile cap enam pile, dua baris tiga pile segi empat sama " + num(P.pp) + " mm pada 3φ, selebar " + num(P.B) + " mm dan sedalam " + num(P.h) + " mm, di bawah column segi empat sama " + num(P.c) + " mm dengan N<sub>Ed</sub> = " + num(P.N) + " kN (tiada moment). Bar sepanjang panjang, H" + num(P.phi) + " di lapisan luar (cover 75 mm), dibengkokkan ke atas dan di-anchor melepasi pile tetapi tidak melepasi shear section sejauh l<sub>bd</sub> + d. C30/37. Pada section merentas lebar, φ/5 ke dalam dari baris hujung, cari β, V<sub>Ed,red</sub> dan V<sub>Rd,c</sub>.");
      return bi("A four-pile cap " + num(P.B) + " mm square and " + num(P.h) + " mm deep carries N<sub>Ed</sub> = " + num(P.N) + " kN from a " + num(P.c) + " mm square column; the piles are " + num(P.pp) + " mm in diameter at 3φ. The tie bars, H" + num(P.phi) + " in two layers (d to the upper layer, cover 75 mm), are bent up and anchored beyond the piles but do not run l<sub>bd</sub> + d past the shear section. C30/37. Find β, the reduced shear V<sub>Ed,red</sub> and V<sub>Rd,c</sub> at the section φ/5 inside the piles.",
                "Satu pile cap empat pile " + num(P.B) + " mm segi empat sama dan sedalam " + num(P.h) + " mm memikul N<sub>Ed</sub> = " + num(P.N) + " kN daripada column " + num(P.c) + " mm segi empat sama; pile berdiameter " + num(P.pp) + " mm pada 3φ. Bar tie, H" + num(P.phi) + " dalam dua lapisan (d ke lapisan atas, cover 75 mm), dibengkokkan ke atas dan di-anchor melepasi pile tetapi tidak melepasi shear section sejauh l<sub>bd</sub> + d. C30/37. Cari β, shear terkurang V<sub>Ed,red</sub> dan V<sub>Rd,c</sub> pada section φ/5 ke dalam dari muka pile.");
    },
    fields: [{ id: "beta", label: ["β", "β"], unit: "", fn: function (P) { return P.beta; }, rtol: 0.01, atol: 0.003 },
             { id: "vr", label: ["V<sub>Ed,red</sub>", "V<sub>Ed,red</sub>"], unit: "kN", fn: function (P) { return P.Vr; }, rtol: 0.01 },
             { id: "vrc", label: ["V<sub>Rd,c</sub>", "V<sub>Rd,c</sub>"], unit: "kN", fn: function (P) { return P.VRc; }, rtol: 0.01 }],
    hints: [function (P) { return P && P.six ? bi("Two end piles stand beyond the section: V<sub>Ed</sub> = 2N<sub>Ed</sub>/6. a<sub>v</sub> = s − c/2 − 0.3φ; d = h − c − φ/2.", "Dua pile hujung berada di luar section: V<sub>Ed</sub> = 2N<sub>Ed</sub>/6. a<sub>v</sub> = s − c/2 − 0.3φ; d = h − c − φ/2.")
                                     : bi("Two piles stand beyond the section: V<sub>Ed</sub> = N<sub>Ed</sub>/2. a<sub>v</sub> = s/2 − c/2 − 0.3φ; d = h − c − 1.5φ.", "Dua pile berada di luar section: V<sub>Ed</sub> = N<sub>Ed</sub>/2. a<sub>v</sub> = s/2 − c/2 − 0.3φ; d = h − c − 1.5φ."); },
            function () { return bi("EC2 6.2.2(6): β = a<sub>v</sub>/2d, but with a<sub>v</sub> not less than 0.5d, so β ≥ 0.25.", "EC2 6.2.2(6): β = a<sub>v</sub>/2d, tetapi dengan a<sub>v</sub> tidak kurang daripada 0.5d, jadi β ≥ 0.25."); },
            function () { return bi("Bars not counted: V<sub>Rd,c</sub> = v<sub>min</sub>bd with v<sub>min</sub> = 0.035k<sup>1.5</sup>√f<sub>ck</sub>, k = 1 + √(200/d), b the whole width.", "Bar tidak dikira: V<sub>Rd,c</sub> = v<sub>min</sub>bd dengan v<sub>min</sub> = 0.035k<sup>1.5</sup>√f<sub>ck</sub>, k = 1 + √(200/d), b seluruh lebar."); }],
    solution: function (P) {
      var fl = P.av < 0.5 * P.d;
      return sol([(P.six ? "d = " + P.h + " − 75 − " + P.phi + "/2 = " + fmt(P.d, 1) + " mm; V<sub>Ed</sub> = 2 × " + P.N + "/6 = " : "d = " + P.h + " − 75 − 1.5 × " + P.phi + " = " + fmt(P.d, 1) + " mm; V<sub>Ed</sub> = " + P.N + "/2 = ") + fmt(P.V, 1) + " kN",
        "a<sub>v</sub> = " + (P.six ? P.s : P.s + "/2") + " − " + P.c + "/2 − 0.3 × " + P.pp + " = " + fmt(P.av, 1) + " mm; 0.5d = " + fmt(0.5 * P.d, 1) + " mm",
        (fl ? bi("a<sub>v</sub> &lt; 0.5d, so a<sub>v</sub> = 0.5d: β = 0.25", "a<sub>v</sub> &lt; 0.5d, jadi a<sub>v</sub> = 0.5d: β = 0.25") : "β = " + fmt(P.av, 1) + "/(2 × " + fmt(P.d, 1) + ") = " + fmt(P.beta, 3)),
        "V<sub>Ed,red</sub> = " + fmt(P.beta, 3) + " × " + fmt(P.V, 1) + " = " + fmt(P.Vr, 1) + " kN",
        "k = " + fmt(P.k, 3) + "; v<sub>min</sub> = 0.035 × " + fmt(P.k, 3) + "<sup>1.5</sup> × √30 = " + fmt(P.vm, 4) + " N/mm²; V<sub>Rd,c</sub> = " + fmt(P.vm, 4) + " × " + P.B + " × " + fmt(P.d, 1) + " = " + fmt(P.VRc, 1) + " kN",
        (P.Vr <= P.VRc ? bi("V<sub>Ed,red</sub> ≤ V<sub>Rd,c</sub>: the section passes.", "V<sub>Ed,red</sub> ≤ V<sub>Rd,c</sub>: section lulus.") : bi("V<sub>Ed,red</sub> &gt; V<sub>Rd,c</sub>: deepen the cap" + (fl ? "; inside the floor only V<sub>Rd,c</sub> grows." : "."), "V<sub>Ed,red</sub> &gt; V<sub>Rd,c</sub>: dalamkan pile cap" + (fl ? "; di dalam lantai hanya V<sub>Rd,c</sub> bertambah." : ".")))]);
    }
  });

  /* ---------- B6 the column face with a moment ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.c = pick(r, [350, 400, 450, 500]); P.N = step(r, 2500, 6000, 100); P.M = step(r, 30, 250, 5);
      P.h = pick(r, [900, 1000, 1100, 1200, 1300]); P.phi = pick(r, [16, 20, 25]);
      P.d = P.h - 75 - P.phi; P.u0 = 4 * P.c; P.W0 = 1.5 * P.c * P.c;
      P.beta = 1 + 0.6 * (P.M * 1e3 / P.N) * (P.u0 / P.W0);
      P.v = P.beta * P.N * 1e3 / (P.u0 * P.d); P.vmax = 0.4 * 0.6 * (1 - 30 / 250) * 30 / 1.5;
      return P;
    },
    text: function (P) {
      return bi("A " + num(P.c) + " mm square column brings N<sub>Ed</sub> = " + num(P.N) + " kN and M<sub>Ed</sub> = " + num(P.M) + " kN m onto a pile cap " + num(P.h) + " mm deep, cover 75 mm, H" + num(P.phi) + " bars (mean d = h − c − φ), C30/37. Find the factor β for the moment (k = 0.6) and the shear stress at the column face, v<sub>Ed,0</sub>.",
                "Satu column " + num(P.c) + " mm segi empat sama membawa N<sub>Ed</sub> = " + num(P.N) + " kN dan M<sub>Ed</sub> = " + num(P.M) + " kN m ke atas pile cap sedalam " + num(P.h) + " mm, cover 75 mm, bar H" + num(P.phi) + " (d purata = h − c − φ), C30/37. Cari faktor β bagi moment (k = 0.6) dan stress shear di muka column, v<sub>Ed,0</sub>.");
    },
    fields: [{ id: "beta", label: ["β", "β"], unit: "", fn: function (P) { return P.beta; }, rtol: 0.005, atol: 0.002 },
             { id: "v", label: ["v<sub>Ed,0</sub>", "v<sub>Ed,0</sub>"], unit: "N/mm²", fn: function (P) { return P.v; }, rtol: 0.01 }],
    hints: [function () { return bi("At the column perimeter u<sub>0</sub> = 4c and W<sub>0</sub> = c<sub>1</sub>²/2 + c<sub>1</sub>c<sub>2</sub> = 1.5c².", "Di perimeter column u<sub>0</sub> = 4c dan W<sub>0</sub> = c<sub>1</sub>²/2 + c<sub>1</sub>c<sub>2</sub> = 1.5c²."); },
            function () { return bi("β = 1 + k(M<sub>Ed</sub>/N<sub>Ed</sub>)(u<sub>0</sub>/W<sub>0</sub>), with M/N in mm.", "β = 1 + k(M<sub>Ed</sub>/N<sub>Ed</sub>)(u<sub>0</sub>/W<sub>0</sub>), dengan M/N dalam mm."); },
            function () { return bi("v<sub>Ed,0</sub> = βN<sub>Ed</sub>/(u<sub>0</sub>d); compare with 0.4νf<sub>cd</sub> = 4.22 N/mm² for C30/37.", "v<sub>Ed,0</sub> = βN<sub>Ed</sub>/(u<sub>0</sub>d); bandingkan dengan 0.4νf<sub>cd</sub> = 4.22 N/mm² bagi C30/37."); }],
    solution: function (P) {
      return sol(["d = " + P.h + " − 75 − " + P.phi + " = " + P.d + " mm; u<sub>0</sub> = 4 × " + P.c + " = " + P.u0 + " mm; W<sub>0</sub> = 1.5 × " + P.c + "² = " + fmt(P.W0, 0) + " mm²",
        "M/N = " + P.M + " × 10³/" + P.N + " = " + fmt(P.M * 1e3 / P.N, 2) + " mm; β = 1 + 0.6 × " + fmt(P.M * 1e3 / P.N, 2) + " × " + P.u0 + "/" + fmt(P.W0, 0) + " = " + fmt(P.beta, 3),
        "v<sub>Ed,0</sub> = " + fmt(P.beta, 3) + " × " + P.N + " × 10³/(" + P.u0 + " × " + P.d + ") = " + fmt(P.v, 2) + " N/mm²",
        "v<sub>Rd,max</sub> = 0.4 × 0.528 × 20 = " + fmt(P.vmax, 2) + " N/mm²: " + (P.v <= P.vmax ? "✓" : bi("✗, a larger column or a deeper cap", "✗, column yang lebih besar atau pile cap yang lebih dalam")),
        bi("The course notes use 0.5νf<sub>cd</sub> = 5.28 N/mm² (EN 1992-1-1:2004).", "Nota kursus menggunakan 0.5νf<sub>cd</sub> = 5.28 N/mm² (EN 1992-1-1:2004).")]);
    }
  });

  EX.ready();
})();
