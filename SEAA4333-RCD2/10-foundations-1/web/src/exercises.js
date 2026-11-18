/* SEAA 4333 Unit 10 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's foundation module):
   A_req = 1.1(Gk + Qk)/q_all, then the real self-weight 25 A h; p_Ed = N_Ed/A without the self-weight;
   e = M/N; e <= L/6: p = (N/A)(1 + 6e/L); e > L/6: L_c = 3(L/2 - e), p = 2N/(B L_c);
   M at the column face = p B l^2/2, l = (L - c)/2; K = M/(fck b d^2), z = d(0.5 + sqrt(0.25 - K/1.134)) <= 0.95d,
   A_s = M/(0.87 fyk z), A_s,min = max(0.26 fctm/fyk, 0.0013) b d; V_Ed at d = p B (l - d), V_Rd,c = v_min b d with
   v_min = 0.035 k^1.5 fck^0.5, k = 1 + sqrt(200/d) <= 2 (bars not counted); punching at a: u = 2(c1 + c2) + 2 pi a,
   A = c1 c2 + 2a(c1 + c2) + pi a^2, V_Ed,red = N - p A, v_Rd = v_Rd,c 2d/a; combined footing: x_bar = N_B s/(N_A + N_B),
   w = N/L, zero shear at x0 = N_A/w, M = w x^2/2 - N_A (x - x_A). */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  var CLS = { 25: "C25/30", 30: "C30/37", 35: "C35/45" };
  function fctm(f) { return 0.3 * Math.pow(f, 2 / 3); }
  function vmin(d, f) { var k = Math.min(1 + Math.sqrt(200 / d), 2); return { k: k, v: 0.035 * Math.pow(k, 1.5) * Math.sqrt(f) }; }
  function r1(v) { return Math.round(v * 10) / 10; }

  /* ---------- B1 the plan size ---------- */
  EX.define("b1", {
    gen: function (r) {
      var Gk = step(r, 400, 1400, 50), Qk = step(r, 200, 900, 50), q = pick(r, [125, 150, 175, 200, 250, 300]), h = pick(r, [400, 450, 500, 550, 600]);
      var N = Gk + Qk, Areq = 1.1 * N / q, L0 = Math.ceil(Math.sqrt(Areq) * 10 - 1e-9) / 10, L = L0;
      function pr(L) { return (N + 25 * L * L * h / 1000) / (L * L); }
      while (pr(L) > q) L = r1(L + 0.1);
      return { Gk: Gk, Qk: Qk, q: q, h: h, N: N, Areq: Areq, L0: L0, L: L, W: 25 * L * L * h / 1000, p: pr(L), p0: pr(L0) };
    },
    text: function (P) {
      return bi("A column brings G<sub>k</sub> = " + num(P.Gk) + " kN and Q<sub>k</sub> = " + num(P.Qk) + " kN onto soil with an allowable bearing pressure of " + num(P.q) + " kN/m². The square pad will be " + num(P.h) + " mm thick. Taking the self-weight as 10% of the load at first, find the area required, the smallest side L (to 0.1 m) that passes the bearing check with the real self-weight, and the service pressure for that L.",
                "Satu column membawa G<sub>k</sub> = " + num(P.Gk) + " kN dan Q<sub>k</sub> = " + num(P.Qk) + " kN ke atas tanah dengan allowable bearing pressure " + num(P.q) + " kN/m². Pad segi empat sama itu akan setebal " + num(P.h) + " mm. Dengan self-weight diambil 10% daripada load pada mulanya, cari luas yang diperlukan, sisi L terkecil (hingga 0.1 m) yang lulus semakan bearing dengan self-weight sebenar, dan service pressure bagi L itu.");
    },
    fields: [{ id: "areq", label: ["A<sub>req</sub>", "A<sub>req</sub>"], unit: "m²", fn: function (P) { return P.Areq; }, rtol: 0.01 },
             { id: "L", label: ["L", "L"], unit: "m", fn: function (P) { return P.L; }, rtol: 0.004 },
             { id: "p", label: ["p", "p"], unit: "kN/m²", fn: function (P) { return P.p; }, rtol: 0.01 }],
    hints: [function () { return bi("A<sub>req</sub> = (G<sub>k</sub> + Q<sub>k</sub> + W)/q<sub>all</sub> with W = 0.1(G<sub>k</sub> + Q<sub>k</sub>): service loads, not ultimate.", "A<sub>req</sub> = (G<sub>k</sub> + Q<sub>k</sub> + W)/q<sub>all</sub> dengan W = 0.1(G<sub>k</sub> + Q<sub>k</sub>): service load, bukan ultimate."); },
            function () { return bi("L = √A<sub>req</sub>, rounded up to the next 0.1 m.", "L = √A<sub>req</sub>, dibundarkan ke atas kepada 0.1 m berikutnya."); },
            function () { return bi("Recompute W = 25L²h and p = (G<sub>k</sub> + Q<sub>k</sub> + W)/L². If p &gt; q<sub>all</sub>, try the next 0.1 m.", "Kira semula W = 25L²h dan p = (G<sub>k</sub> + Q<sub>k</sub> + W)/L². Jika p &gt; q<sub>all</sub>, cuba 0.1 m berikutnya."); }],
    solution: function (P) {
      var s = ["A<sub>req</sub> = 1.1 × " + P.N + "/" + P.q + " = " + fmt(P.Areq, 2) + " m²; √ = " + fmt(Math.sqrt(P.Areq), 3) + " m → try L = " + fmt(P.L0, 1) + " m"];
      if (P.L > P.L0 + 1e-9) s.push(bi("L = " + fmt(P.L0, 1) + ": p = " + fmt(P.p0, 1) + " &gt; " + P.q + " kN/m², the real self-weight is more than 10%; go up to L = " + fmt(P.L, 1) + " m", "L = " + fmt(P.L0, 1) + ": p = " + fmt(P.p0, 1) + " &gt; " + P.q + " kN/m², self-weight sebenar lebih daripada 10%; naikkan kepada L = " + fmt(P.L, 1) + " m"));
      s.push("W = 25 × " + fmt(P.L, 1) + "² × " + fmt(P.h / 1000, 2) + " = " + fmt(P.W, 1) + " kN; p = (" + P.N + " + " + fmt(P.W, 1) + ")/" + fmt(P.L * P.L, 2) + " = " + fmt(P.p, 1) + " ≤ " + P.q + " kN/m² ✓");
      return sol(s);
    }
  });

  /* ---------- B2 the pressure under an eccentric load ---------- */
  EX.define("b2", {
    gen: function (r) {
      var L = step(r, 2.0, 4.0, 0.1), B = Math.max(1.5, r1(L * (0.6 + 0.4 * r()))), N = Math.max(200, Math.round(L * B * (80 + 140 * r()) / 10) * 10);
      var part = r() < 0.45, ratio = part ? 0.175 + 0.10 * r() : 0.04 + 0.12 * r();
      var M = Math.max(5, Math.round(N * L * ratio / 5) * 5), e = M / N, A = L * B, Lc, pmax;
      if (e <= L / 6 + 1e-12) { Lc = L; pmax = N / A * (1 + 6 * e / L); } else { Lc = 3 * (L / 2 - e); pmax = 2 * N / (B * Lc); }
      return { L: L, B: B, N: N, M: M, e: e, A: A, Lc: Lc, pmax: pmax, part: e > L / 6 + 1e-12 };
    },
    text: function (P) {
      return bi("A base " + num(fmt(P.L, 1)) + " m long and " + num(fmt(P.B, 1)) + " m wide carries a service load N = " + num(P.N) + " kN, its self-weight included, and a moment M = " + num(P.M) + " kN m that tilts the pressure along the length. Find the eccentricity e, the length of base in contact with the soil (L itself if the whole base is in contact), and the maximum pressure.",
                "Satu tapak sepanjang " + num(fmt(P.L, 1)) + " m dan selebar " + num(fmt(P.B, 1)) + " m membawa service load N = " + num(P.N) + " kN, termasuk self-weight-nya, dan moment M = " + num(P.M) + " kN m yang mencondongkan tekanan sepanjang panjangnya. Cari eccentricity e, panjang tapak yang bersentuhan dengan tanah (L sendiri jika seluruh tapak bersentuhan), dan tekanan maksimum.");
    },
    fields: [{ id: "e", label: ["e", "e"], unit: "m", fn: function (P) { return P.e; }, rtol: 0.01, atol: 0.002 },
             { id: "lc", label: ["L<sub>c</sub>", "L<sub>c</sub>"], unit: "m", fn: function (P) { return P.Lc; }, rtol: 0.01 },
             { id: "pmax", label: ["p<sub>max</sub>", "p<sub>max</sub>"], unit: "kN/m²", fn: function (P) { return P.pmax; }, rtol: 0.01 }],
    hints: [function (P) { return bi("e = M/N; compare it with L/6 = " + fmt(P.L / 6, 3) + " m.", "e = M/N; bandingkan dengan L/6 = " + fmt(P.L / 6, 3) + " m."); },
            function () { return bi("e ≤ L/6: the whole length is in contact and p<sub>max</sub> = (N/A)(1 + 6e/L).", "e ≤ L/6: seluruh panjang bersentuhan dan p<sub>max</sub> = (N/A)(1 + 6e/L)."); },
            function () { return bi("e &gt; L/6: part lifts off; L<sub>c</sub> = 3(L/2 − e) and p<sub>max</sub> = 2N/(BL<sub>c</sub>).", "e &gt; L/6: sebahagian terangkat; L<sub>c</sub> = 3(L/2 − e) dan p<sub>max</sub> = 2N/(BL<sub>c</sub>)."); }],
    solution: function (P) {
      var s = ["e = " + P.M + "/" + P.N + " = " + fmt(P.e, 3) + " m; L/6 = " + fmt(P.L / 6, 3) + " m"];
      if (!P.part) s.push(bi("e ≤ L/6: full contact, L<sub>c</sub> = L = " + fmt(P.L, 1) + " m", "e ≤ L/6: sentuhan penuh, L<sub>c</sub> = L = " + fmt(P.L, 1) + " m"),
                         "p<sub>max</sub> = " + P.N + "/" + fmt(P.A, 2) + " × (1 + 6 × " + fmt(P.e, 3) + "/" + fmt(P.L, 1) + ") = " + fmt(P.pmax, 1) + " kN/m²; p<sub>min</sub> = " + fmt(P.N / P.A * (1 - 6 * P.e / P.L), 1) + " kN/m²");
      else s.push(bi("e &gt; L/6: part of the base lifts off; L<sub>c</sub> = 3 × (" + fmt(P.L / 2, 2) + " − " + fmt(P.e, 3) + ") = " + fmt(P.Lc, 3) + " m", "e &gt; L/6: sebahagian tapak terangkat; L<sub>c</sub> = 3 × (" + fmt(P.L / 2, 2) + " − " + fmt(P.e, 3) + ") = " + fmt(P.Lc, 3) + " m"),
                  "p<sub>max</sub> = 2 × " + P.N + "/(" + fmt(P.B, 1) + " × " + fmt(P.Lc, 3) + ") = " + fmt(P.pmax, 1) + " kN/m²" + (P.e > P.L / 3 ? bi(" (e &gt; L/3: special precautions, EC7 6.5.4)", " (e &gt; L/3: langkah berjaga-jaga khas, EC7 6.5.4)") : ""));
      return sol(s);
    }
  });

  /* ---------- shared generator for a square pad under an axial load ---------- */
  function padGen(r, needShear) {
    for (var t = 0; t < 40; t++) {
      var c = pick(r, [300, 350, 400, 450, 500]), L = step(r, 2.4, 3.8, 0.1), N = step(r, 1000, 3500, 50), h = step(r, 450, 750, 50), fck = pick(r, [25, 30, 35]), phi = pick(r, [12, 16]);
      var d = h - 40 - 1.5 * phi, l = (L - c / 1000) / 2, p = N / (L * L);
      if (needShear && l * 1000 - d < 120) continue;
      return { c: c, L: L, N: N, h: h, fck: fck, phi: phi, d: d, l: l, p: p };
    }
    return { c: 400, L: 3.0, N: 2000, h: 550, fck: 30, phi: 16, d: 486, l: 1.3, p: 2000 / 9 };
  }
  function padText(P, en, ms) {
    return bi("A " + num(P.c) + " mm square column carries N<sub>Ed</sub> = " + num(P.N) + " kN onto a square pad " + num(fmt(P.L, 1)) + " × " + num(fmt(P.L, 1)) + " m, " + num(P.h) + " mm thick, in " + num(CLS[P.fck]) + ", with c<sub>nom</sub> = 40 mm and H" + P.phi + " bars both ways (use the inner layer, d = h − c − 1.5φ, for both directions). " + en,
              "Satu column segi empat sama " + num(P.c) + " mm membawa N<sub>Ed</sub> = " + num(P.N) + " kN ke atas pad segi empat sama " + num(fmt(P.L, 1)) + " × " + num(fmt(P.L, 1)) + " m, setebal " + num(P.h) + " mm, dalam " + num(CLS[P.fck]) + ", dengan c<sub>nom</sub> = 40 mm dan bar H" + P.phi + " kedua-dua arah (gunakan lapisan dalam, d = h − c − 1.5φ, bagi kedua-dua arah). " + ms);
  }

  /* ---------- B3 the moment at the face and the bars ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = padGen(r, false), b = P.L * 1000;
      P.M = P.p * P.L * P.l * P.l / 2;
      P.K = P.M * 1e6 / (P.fck * b * P.d * P.d);
      P.z0 = P.d * (0.5 + Math.sqrt(0.25 - P.K / 1.134)); P.z = Math.min(P.z0, 0.95 * P.d);
      P.As = P.M * 1e6 / (435 * P.z);
      P.rmin = Math.max(0.26 * fctm(P.fck) / 500, 0.0013); P.Asmin = P.rmin * b * P.d;
      return P;
    },
    text: function (P) { return padText(P, "Find the moment at the column face, the steel required for it, and the minimum steel, each for one direction.", "Cari moment di muka column, steel yang diperlukan baginya, dan steel minimum, setiap satu bagi satu arah."); },
    fields: [{ id: "m", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.01 },
             { id: "as", label: ["A<sub>s</sub>", "A<sub>s</sub>"], unit: "mm²", fn: function (P) { return P.As; }, rtol: 0.015 },
             { id: "asmin", label: ["A<sub>s,min</sub>", "A<sub>s,min</sub>"], unit: "mm²", fn: function (P) { return P.Asmin; }, rtol: 0.015 }],
    hints: [function () { return bi("p<sub>Ed</sub> = N<sub>Ed</sub>/L² (no self-weight); l = (L − c)/2; M = p<sub>Ed</sub>Ll²/2 over the whole width.", "p<sub>Ed</sub> = N<sub>Ed</sub>/L² (tanpa self-weight); l = (L − c)/2; M = p<sub>Ed</sub>Ll²/2 merentasi seluruh lebar."); },
            function () { return bi("K = M/(f<sub>ck</sub>bd²) with b = L; z = d(0.5 + √(0.25 − K/1.134)) but not more than 0.95d; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z).", "K = M/(f<sub>ck</sub>bd²) dengan b = L; z = d(0.5 + √(0.25 − K/1.134)) tetapi tidak lebih daripada 0.95d; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z)."); },
            function () { return bi("A<sub>s,min</sub> = 0.26(f<sub>ctm</sub>/f<sub>yk</sub>)bd ≥ 0.0013bd, f<sub>ctm</sub> = 0.3f<sub>ck</sub><sup>2/3</sup>.", "A<sub>s,min</sub> = 0.26(f<sub>ctm</sub>/f<sub>yk</sub>)bd ≥ 0.0013bd, f<sub>ctm</sub> = 0.3f<sub>ck</sub><sup>2/3</sup>."); }],
    solution: function (P) {
      return sol(["p<sub>Ed</sub> = " + P.N + "/" + fmt(P.L * P.L, 2) + " = " + fmt(P.p, 1) + " kN/m²; l = (" + fmt(P.L, 1) + " − " + fmt(P.c / 1000, 2) + ")/2 = " + fmt(P.l, 3) + " m",
        "M<sub>Ed</sub> = " + fmt(P.p, 1) + " × " + fmt(P.L, 1) + " × " + fmt(P.l, 3) + "²/2 = " + fmt(P.M, 1) + " kN m",
        "d = " + P.h + " − 40 − 1.5 × " + P.phi + " = " + P.d + " mm; K = " + fmt(P.K, 4) + "; z = " + fmt(P.z0 / P.d, 3) + "d → " + fmt(P.z, 1) + " mm" + (P.z < P.z0 ? " (0.95d)" : ""),
        "A<sub>s</sub> = " + fmt(P.M, 1) + " × 10⁶/(435 × " + fmt(P.z, 1) + ") = " + fmt(P.As, 0) + " mm²",
        "A<sub>s,min</sub> = " + fmt(P.rmin, 5) + " × " + fmt(P.L * 1000, 0) + " × " + P.d + " = " + fmt(P.Asmin, 0) + " mm²" + (P.Asmin > P.As ? bi(": the minimum governs", ": minimum menentukan") : "")]);
    }
  });

  /* ---------- B4 vertical shear at d ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = padGen(r, true), b = P.L * 1000;
      P.V = P.p * P.L * (P.l - P.d / 1000);
      var s = vmin(P.d, P.fck); P.k = s.k; P.vmin = s.v; P.VR = s.v * b * P.d / 1000;
      return P;
    },
    text: function (P) { return padText(P, "The bottom bars do not run l<sub>bd</sub> + d beyond the shear section, so ρ<sub>l</sub> = 0. Find the shear force at d from the column face, the size factor k, and the shear resistance V<sub>Rd,c</sub>.", "Bar bawah tidak menjangkau l<sub>bd</sub> + d melepasi shear section, jadi ρ<sub>l</sub> = 0. Cari shear force pada d dari muka column, faktor saiz k, dan shear resistance V<sub>Rd,c</sub>."); },
    fields: [{ id: "v", label: ["V<sub>Ed</sub>", "V<sub>Ed</sub>"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.01 },
             { id: "k", label: ["k", "k"], unit: "", fn: function (P) { return P.k; }, rtol: 0.005 },
             { id: "vr", label: ["V<sub>Rd,c</sub>", "V<sub>Rd,c</sub>"], unit: "kN", fn: function (P) { return P.VR; }, rtol: 0.015 }],
    hints: [function () { return bi("The section is d from the face: V<sub>Ed</sub> = p<sub>Ed</sub>L(l − d), the pressure beyond it.", "Section berada d dari muka: V<sub>Ed</sub> = p<sub>Ed</sub>L(l − d), tekanan di luarnya."); },
            function () { return bi("k = 1 + √(200/d) ≤ 2.", "k = 1 + √(200/d) ≤ 2."); },
            function () { return bi("With ρ<sub>l</sub> = 0, V<sub>Rd,c</sub> = v<sub>min</sub>bd, v<sub>min</sub> = 0.035k<sup>3/2</sup>f<sub>ck</sub><sup>1/2</sup>, b = L.", "Dengan ρ<sub>l</sub> = 0, V<sub>Rd,c</sub> = v<sub>min</sub>bd, v<sub>min</sub> = 0.035k<sup>3/2</sup>f<sub>ck</sub><sup>1/2</sup>, b = L."); }],
    solution: function (P) {
      return sol(["p<sub>Ed</sub> = " + fmt(P.p, 1) + " kN/m²; d = " + P.d + " mm; l − d = " + fmt(P.l * 1000, 0) + " − " + P.d + " = " + fmt(P.l * 1000 - P.d, 0) + " mm",
        "V<sub>Ed</sub> = " + fmt(P.p, 1) + " × " + fmt(P.L, 1) + " × " + fmt(P.l - P.d / 1000, 3) + " = " + fmt(P.V, 1) + " kN",
        "k = 1 + √(200/" + P.d + ") = " + fmt(P.k, 3) + "; v<sub>min</sub> = 0.035 × " + fmt(P.k, 3) + "<sup>1.5</sup> × √" + P.fck + " = " + fmt(P.vmin, 3) + " N/mm²",
        "V<sub>Rd,c</sub> = " + fmt(P.vmin, 3) + " × " + fmt(P.L * 1000, 0) + " × " + P.d + " × 10⁻³ = " + fmt(P.VR, 1) + " kN " + (P.V <= P.VR ? "≥ V<sub>Ed</sub> ✓" : bi("&lt; V<sub>Ed</sub>: deepen the base", "&lt; V<sub>Ed</sub>: dalamkan tapak"))]);
    }
  });

  /* ---------- B5 punching inside 2d ---------- */
  EX.define("b5", {
    gen: function (r) {
      for (var t = 0; t < 40; t++) {
        var c = pick(r, [300, 350, 400, 450, 500]), d = step(r, 380, 650, 10), L = step(r, 2.4, 3.8, 0.1), fck = pick(r, [25, 30, 35]);
        var N = Math.round(L * L * (150 + 200 * r()) / 10) * 10;
        if ((L * 1000 - c) / 2 < 2 * d) continue;
        var p = N / (L * L), s = vmin(d, fck), u = 4 * c + 2 * Math.PI * d, A = (c * c + 4 * c * d + Math.PI * d * d) / 1e6, V = N - p * A;
        var vEd = V * 1e3 / (u * d), vRd = 2 * s.v;
        if (vEd / vRd < 0.5 || vEd / vRd > 1.3) continue;
        return { c: c, d: d, L: L, N: N, fck: fck, p: p, k: s.k, vr: s.v, u: u, A: A, V: V, vEd: vEd, vRd: vRd, ratio: vEd / vRd };
      }
    },
    text: function (P) {
      return bi("A " + num(P.c) + " mm square column carries N<sub>Ed</sub> = " + num(P.N) + " kN onto a square pad " + num(fmt(P.L, 1)) + " m wide with a mean effective depth d = " + num(P.d) + " mm, in " + num(CLS[P.fck]) + ". The bars do not count in ρ<sub>l</sub>, so v<sub>Rd,c</sub> = v<sub>min</sub>. Check the perimeter at a = d: find its length u, the reduced punching force V<sub>Ed,red</sub>, and v<sub>Ed</sub>/v<sub>Rd</sub>.",
                "Satu column segi empat sama " + num(P.c) + " mm membawa N<sub>Ed</sub> = " + num(P.N) + " kN ke atas pad segi empat sama selebar " + num(fmt(P.L, 1)) + " m dengan purata effective depth d = " + num(P.d) + " mm, dalam " + num(CLS[P.fck]) + ". Bar tidak dikira dalam ρ<sub>l</sub>, jadi v<sub>Rd,c</sub> = v<sub>min</sub>. Semak perimeter pada a = d: cari panjangnya u, reduced punching force V<sub>Ed,red</sub>, dan v<sub>Ed</sub>/v<sub>Rd</sub>.");
    },
    fields: [{ id: "u", label: ["u", "u"], unit: "mm", fn: function (P) { return P.u; }, rtol: 0.005 },
             { id: "v", label: ["V<sub>Ed,red</sub>", "V<sub>Ed,red</sub>"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.01 },
             { id: "r", label: ["v<sub>Ed</sub>/v<sub>Rd</sub>", "v<sub>Ed</sub>/v<sub>Rd</sub>"], unit: "", fn: function (P) { return P.ratio; }, rtol: 0.015, atol: 0.005 }],
    hints: [function () { return bi("u = 4c + 2πa and A = c² + 4ca + πa², with a = d.", "u = 4c + 2πa dan A = c² + 4ca + πa², dengan a = d."); },
            function () { return bi("p<sub>Ed</sub> = N<sub>Ed</sub>/L²; V<sub>Ed,red</sub> = N<sub>Ed</sub> − p<sub>Ed</sub>A; v<sub>Ed</sub> = V<sub>Ed,red</sub>/(ud).", "p<sub>Ed</sub> = N<sub>Ed</sub>/L²; V<sub>Ed,red</sub> = N<sub>Ed</sub> − p<sub>Ed</sub>A; v<sub>Ed</sub> = V<sub>Ed,red</sub>/(ud)."); },
            function () { return bi("v<sub>Rd</sub> = v<sub>Rd,c</sub> · 2d/a = 2v<sub>min</sub> at a = d; v<sub>min</sub> = 0.035k<sup>3/2</sup>f<sub>ck</sub><sup>1/2</sup>.", "v<sub>Rd</sub> = v<sub>Rd,c</sub> · 2d/a = 2v<sub>min</sub> pada a = d; v<sub>min</sub> = 0.035k<sup>3/2</sup>f<sub>ck</sub><sup>1/2</sup>."); }],
    solution: function (P) {
      return sol(["u = 4 × " + P.c + " + 2π × " + P.d + " = " + fmt(P.u, 0) + " mm; A = " + fmt(P.A, 3) + " m²",
        "p<sub>Ed</sub> = " + P.N + "/" + fmt(P.L * P.L, 2) + " = " + fmt(P.p, 1) + " kN/m²; V<sub>Ed,red</sub> = " + P.N + " − " + fmt(P.p, 1) + " × " + fmt(P.A, 3) + " = " + fmt(P.V, 1) + " kN",
        "v<sub>Ed</sub> = " + fmt(P.V, 1) + " × 10³/(" + fmt(P.u, 0) + " × " + P.d + ") = " + fmt(P.vEd, 3) + " N/mm²",
        "k = " + fmt(P.k, 3) + "; v<sub>min</sub> = " + fmt(P.vr, 3) + "; v<sub>Rd</sub> = " + fmt(P.vr, 3) + " × 2 = " + fmt(P.vRd, 3) + " N/mm²",
        "v<sub>Ed</sub>/v<sub>Rd</sub> = " + fmt(P.ratio, 3) + (P.ratio <= 1 ? " ≤ 1 ✓" : bi(" &gt; 1: deepen the base", " &gt; 1: dalamkan tapak"))]);
    }
  });

  /* ---------- B6 a combined footing ---------- */
  EX.define("b6", {
    gen: function (r) {
      for (var t = 0; t < 40; t++) {
        var NA = step(r, 800, 2000, 50), NB = step(r, 900, 2600, 50), s = step(r, 2.6, 4.6, 0.1), aL = step(r, 0.6, 1.2, 0.05);
        var N = NA + NB, xb = NB * s / N, L = 2 * (aL + xb), w = N / L, x0 = NA / w;
        if (x0 <= aL + 0.05 || x0 >= aL + s - 0.05) continue;
        var Mh = w * x0 * x0 / 2 - NA * (x0 - aL);
        if (Math.abs(Mh) < 100) continue;
        return { NA: NA, NB: NB, s: s, aL: aL, N: N, xb: xb, L: L, w: w, x0: x0, Mh: Mh };
      }
    },
    text: function (P) {
      return bi("Two columns stand " + num(fmt(P.s, 1)) + " m apart and carry N<sub>A</sub> = " + num(P.NA) + " kN and N<sub>B</sub> = " + num(P.NB) + " kN at the ultimate limit state (the same share of permanent load in both, so the service resultant lies at the same place). A rectangular combined footing starts " + num(fmt(P.aL, 2)) + " m beyond column A. Find the length L that centres the base on the resultant, the upward load per metre w at the ultimate limit state, and the largest hogging moment between the columns (as a positive number).",
                "Dua column berdiri " + num(fmt(P.s, 1)) + " m berjauhan dan membawa N<sub>A</sub> = " + num(P.NA) + " kN dan N<sub>B</sub> = " + num(P.NB) + " kN pada ultimate limit state (bahagian permanent load yang sama bagi kedua-duanya, jadi paduan service berada di tempat yang sama). Satu combined footing segi empat tepat bermula " + num(fmt(P.aL, 2)) + " m melepasi column A. Cari panjang L yang memusatkan tapak pada paduan, load ke atas per meter w pada ultimate limit state, dan hogging moment terbesar di antara column (sebagai nombor positif).");
    },
    fields: [{ id: "L", label: ["L", "L"], unit: "m", fn: function (P) { return P.L; }, rtol: 0.005 },
             { id: "w", label: ["w", "w"], unit: "kN/m", fn: function (P) { return P.w; }, rtol: 0.01 },
             { id: "mh", label: ["|M<sub>hog</sub>|", "|M<sub>hog</sub>|"], unit: "kN m", fn: function (P) { return Math.abs(P.Mh); }, rtol: 0.015, atol: 1 }],
    hints: [function () { return bi("x̄ = N<sub>B</sub>s/(N<sub>A</sub> + N<sub>B</sub>) from column A; the base is centred there, so L = 2(a + x̄).", "x̄ = N<sub>B</sub>s/(N<sub>A</sub> + N<sub>B</sub>) dari column A; tapak berpusat di situ, jadi L = 2(a + x̄)."); },
            function () { return bi("w = (N<sub>A</sub> + N<sub>B</sub>)/L: the pressure is uniform.", "w = (N<sub>A</sub> + N<sub>B</sub>)/L: tekanannya seragam."); },
            function () { return bi("From the left end, V = wx − N<sub>A</sub> is zero at x<sub>0</sub> = N<sub>A</sub>/w; M = wx<sub>0</sub>²/2 − N<sub>A</sub>(x<sub>0</sub> − a).", "Dari hujung kiri, V = wx − N<sub>A</sub> sifar pada x<sub>0</sub> = N<sub>A</sub>/w; M = wx<sub>0</sub>²/2 − N<sub>A</sub>(x<sub>0</sub> − a)."); }],
    solution: function (P) {
      return sol(["x̄ = " + P.NB + " × " + fmt(P.s, 1) + "/" + P.N + " = " + fmt(P.xb, 3) + " m from A; L = 2 × (" + fmt(P.aL, 2) + " + " + fmt(P.xb, 3) + ") = " + fmt(P.L, 3) + " m",
        "w = " + P.N + "/" + fmt(P.L, 3) + " = " + fmt(P.w, 1) + " kN/m",
        "x<sub>0</sub> = " + P.NA + "/" + fmt(P.w, 1) + " = " + fmt(P.x0, 3) + " m from the left end",
        "M = " + fmt(P.w, 1) + " × " + fmt(P.x0, 3) + "²/2 − " + P.NA + " × (" + fmt(P.x0, 3) + " − " + fmt(P.aL, 2) + ") = " + fmt(P.Mh, 1) + bi(" kN m: hogging, top bars between the columns", " kN m: hogging, bar atas di antara column")]);
    }
  });

  EX.ready();
})();
