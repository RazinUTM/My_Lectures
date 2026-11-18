/* SEAA 4333 Unit 9 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's column module): e_i = l0/400;
   M02 = |M|max + NEd e_i, M01 = |M|min + NEd e_i, M0e = 0.6|M|max +/- 0.4|M|min + NEd e_i >= 0.4 M02 (minus in double
   curvature); phi_ef = phi(inf,t0) M0Eqp/M0Ed, beta = 0.35 + fck/200 - lambda/150, K_phi = max(1, 1 + beta phi_ef);
   1/r0 = eps_yd/(0.45 d), eps_yd = 435/200 000; K_r = (nu - n)/(nu - 0.4) <= 1, nu = 1 + omega, omega = As fyd/(Ac fcd),
   fcd = 0.85 fck/1.5; e2 = (1/r) l0^2/10, M2 = NEd e2; braced MEd = max(M02, M0e + M2, M01 + 0.5 M2, NEd e0);
   EC2 Eq. 5.39 with a = 1 / 1.5 / 2 at NEd/NRd = 0.1 / 0.7 / 1.0, interpolated. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return a + s * Math.floor(r() * (n + 1)); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  var EYD = 435 / 200000, CLS = { 25: "C25/30", 30: "C30/37", 35: "C35/45" };
  function aExp(r) { return r <= 0.1 ? 1 : r >= 1 ? 2 : r <= 0.7 ? 1 + (r - 0.1) / 0.6 * 0.5 : 1.5 + (r - 0.7) / 0.3 * 0.5; }

  /* ---------- B1 first-order moments with the imperfection ---------- */
  EX.define("b1", {
    gen: function (r) {
      var l0 = step(r, 2500, 6000, 100), N = step(r, 400, 2500, 50), Mt = step(r, 20, 120, 5), Mb = Math.round(Mt * (0.2 + 0.7 * r())), dbl = r() < 0.6;
      var ei = l0 / 400, Mi = N * ei / 1e3, M02 = Mt + Mi, M0e = Math.max(0.6 * Mt + (dbl ? -0.4 : 0.4) * Mb + Mi, 0.4 * M02);
      return { l0: l0, N: N, Mt: Mt, Mb: Mb, dbl: dbl, ei: ei, Mi: Mi, M02: M02, M0e: M0e, floor: 0.4 * M02 > 0.6 * Mt + (dbl ? -0.4 : 0.4) * Mb + Mi };
    },
    text: function (P) {
      var c = P.dbl ? bi("tension on opposite faces (double curvature)", "tension pada muka bertentangan (double curvature)") : bi("tension on the same face (single curvature)", "tension pada muka yang sama (single curvature)");
      return bi("A braced slender column has l<sub>0</sub> = " + num(P.l0) + " mm and N<sub>Ed</sub> = " + num(P.N) + " kN; its first-order end moments are " + num(P.Mt) + " and " + num(P.Mb) + " kN m, " + c + ". With the course reading of the imperfection, find e<sub>i</sub>, M<sub>02</sub> and the equivalent moment M<sub>0e</sub>.",
                "Satu column slender braced mempunyai l<sub>0</sub> = " + num(P.l0) + " mm dan N<sub>Ed</sub> = " + num(P.N) + " kN; first-order end moment-nya ialah " + num(P.Mt) + " dan " + num(P.Mb) + " kN m, " + c + ". Dengan bacaan imperfection kursus, cari e<sub>i</sub>, M<sub>02</sub> dan equivalent moment M<sub>0e</sub>.");
    },
    fields: [{ id: "ei", label: ["e<sub>i</sub>", "e<sub>i</sub>"], unit: "mm", fn: function (P) { return P.ei; }, rtol: 0.01 },
             { id: "m02", label: ["M<sub>02</sub>", "M<sub>02</sub>"], unit: "kN m", fn: function (P) { return P.M02; }, rtol: 0.01 },
             { id: "m0e", label: ["M<sub>0e</sub>", "M<sub>0e</sub>"], unit: "kN m", fn: function (P) { return P.M0e; }, rtol: 0.01, atol: 0.2 }],
    hints: [function () { return bi("e<sub>i</sub> = l<sub>0</sub>/400; N<sub>Ed</sub>e<sub>i</sub> is the imperfection moment.", "e<sub>i</sub> = l<sub>0</sub>/400; N<sub>Ed</sub>e<sub>i</sub> ialah moment imperfection."); },
            function () { return bi("M<sub>02</sub> = the larger end moment + N<sub>Ed</sub>e<sub>i</sub>.", "M<sub>02</sub> = end moment yang lebih besar + N<sub>Ed</sub>e<sub>i</sub>."); },
            function (P) { return bi("M<sub>0e</sub> = 0.6 × " + P.Mt + (P.dbl ? " − " : " + ") + "0.4 × " + P.Mb + " + N<sub>Ed</sub>e<sub>i</sub>, but not less than 0.4M<sub>02</sub>" + (P.dbl ? ": minus, because the end moments have opposite signs." : "."),
                                   "M<sub>0e</sub> = 0.6 × " + P.Mt + (P.dbl ? " − " : " + ") + "0.4 × " + P.Mb + " + N<sub>Ed</sub>e<sub>i</sub>, tetapi tidak kurang daripada 0.4M<sub>02</sub>" + (P.dbl ? ": tolak, kerana end moment mempunyai tanda bertentangan." : ".")); }],
    solution: function (P) {
      return sol(["e<sub>i</sub> = " + P.l0 + "/400 = " + fmt(P.ei, 2) + " mm; N<sub>Ed</sub>e<sub>i</sub> = " + P.N + " × " + fmt(P.ei / 1000, 5) + " = " + fmt(P.Mi, 2) + " kN m",
        "M<sub>02</sub> = " + P.Mt + " + " + fmt(P.Mi, 2) + " = " + fmt(P.M02, 2) + " kN m",
        "M<sub>0e</sub> = 0.6 × " + P.Mt + (P.dbl ? " − " : " + ") + "0.4 × " + P.Mb + " + " + fmt(P.Mi, 2) + " = " + fmt(0.6 * P.Mt + (P.dbl ? -0.4 : 0.4) * P.Mb + P.Mi, 2) + "; 0.4M<sub>02</sub> = " + fmt(0.4 * P.M02, 2) + " → M<sub>0e</sub> = " + fmt(P.M0e, 2) + " kN m" + (P.floor ? bi(" (the floor governs)", " (lantai menentukan)") : "")]);
    }
  });

  /* ---------- B2 creep and K_phi ---------- */
  EX.define("b2", {
    gen: function (r) {
      var fck = pick(r, [25, 30, 35]), lam = step(r, 25, 85, 0.5), phi = step(r, 1.4, 2.6, 0.05), rq = pick(r, [0.6, 0.65, 0.67, 0.7, 0.75, 0.8]);
      var phief = phi * rq, beta = 0.35 + fck / 200 - lam / 150, Kphi = Math.max(1, 1 + beta * phief);
      return { fck: fck, lam: lam, phi: phi, rq: rq, phief: phief, beta: beta, Kphi: Kphi };
    },
    text: function (P) {
      return bi("A slender column in " + num(CLS[P.fck]) + " concrete has λ = " + num(fmt(P.lam, 1)) + " about the axis of bending. EC2 Annex B gives φ(∞,t<sub>0</sub>) = " + num(fmt(P.phi, 2)) + ", and the quasi-permanent share of the first-order moment is M<sub>0Eqp</sub>/M<sub>0Ed</sub> = " + num(P.rq) + ". Find φ<sub>ef</sub>, β and K<sub>φ</sub>.",
                "Satu column slender daripada konkrit " + num(CLS[P.fck]) + " mempunyai λ = " + num(fmt(P.lam, 1)) + " pada paksi bending. EC2 Annex B memberi φ(∞,t<sub>0</sub>) = " + num(fmt(P.phi, 2)) + ", dan bahagian quasi-permanent first-order moment ialah M<sub>0Eqp</sub>/M<sub>0Ed</sub> = " + num(P.rq) + ". Cari φ<sub>ef</sub>, β dan K<sub>φ</sub>.");
    },
    fields: [{ id: "phief", label: ["φ<sub>ef</sub>", "φ<sub>ef</sub>"], unit: "", fn: function (P) { return P.phief; }, rtol: 0.01 },
             { id: "beta", label: ["β", "β"], unit: "", fn: function (P) { return P.beta; }, rtol: 0.01, atol: 0.003 },
             { id: "kphi", label: ["K<sub>φ</sub>", "K<sub>φ</sub>"], unit: "", fn: function (P) { return P.Kphi; }, rtol: 0.005 }],
    hints: [function () { return bi("φ<sub>ef</sub> = φ(∞,t<sub>0</sub>) × M<sub>0Eqp</sub>/M<sub>0Ed</sub> (EC2 5.8.4(2)).", "φ<sub>ef</sub> = φ(∞,t<sub>0</sub>) × M<sub>0Eqp</sub>/M<sub>0Ed</sub> (EC2 5.8.4(2))."); },
            function () { return bi("β = 0.35 + f<sub>ck</sub>/200 − λ/150 (EC2 5.8.8.3(4)); it can be negative for a very slender column.", "β = 0.35 + f<sub>ck</sub>/200 − λ/150 (EC2 5.8.8.3(4)); ia boleh menjadi negatif bagi column yang sangat slender."); },
            function () { return bi("K<sub>φ</sub> = 1 + βφ<sub>ef</sub>, but never less than 1.", "K<sub>φ</sub> = 1 + βφ<sub>ef</sub>, tetapi tidak pernah kurang daripada 1."); }],
    solution: function (P) {
      return sol(["φ<sub>ef</sub> = " + fmt(P.phi, 2) + " × " + P.rq + " = " + fmt(P.phief, 3),
        "β = 0.35 + " + P.fck + "/200 − " + fmt(P.lam, 1) + "/150 = " + fmt(P.beta, 4),
        "K<sub>φ</sub> = max(1; 1 + " + fmt(P.beta, 4) + " × " + fmt(P.phief, 3) + ") = " + fmt(P.Kphi, 3) + (P.beta <= 0 ? bi(": β ≤ 0, so creep adds nothing here", ": β ≤ 0, jadi creep tidak menambah apa-apa di sini") : "")]);
    }
  });

  /* ---------- B3 curvature and M2 ---------- */
  EX.define("b3", {
    gen: function (r) {
      var d = pick(r, [199.5, 204, 254, 304, 354, 404]), l0 = step(r, 3500, 7000, 100), N = step(r, 500, 2500, 50), Kr = step(r, 0.35, 1.0, 0.01), Kphi = step(r, 1.0, 1.4, 0.01);
      var r0 = EYD / (0.45 * d), rr = Kr * Kphi * r0, e2 = rr * l0 * l0 / 10, M2 = N * e2 / 1e3;
      return { d: d, l0: l0, N: N, Kr: Kr, Kphi: Kphi, r0: r0, rr: rr, e2: e2, M2: M2 };
    },
    text: function (P) {
      return bi("A slender column with B500 bars has d = " + num(P.d) + " mm in the plane of bending and l<sub>0</sub> = " + num(P.l0) + " mm; N<sub>Ed</sub> = " + num(P.N) + " kN, K<sub>r</sub> = " + num(fmt(P.Kr, 2)) + " and K<sub>φ</sub> = " + num(fmt(P.Kphi, 2)) + ". Find 1/r<sub>0</sub> (in 10⁻⁵ per mm), e<sub>2</sub> and M<sub>2</sub>.",
                "Satu column slender dengan bar B500 mempunyai d = " + num(P.d) + " mm dalam satah bending dan l<sub>0</sub> = " + num(P.l0) + " mm; N<sub>Ed</sub> = " + num(P.N) + " kN, K<sub>r</sub> = " + num(fmt(P.Kr, 2)) + " dan K<sub>φ</sub> = " + num(fmt(P.Kphi, 2)) + ". Cari 1/r<sub>0</sub> (dalam 10⁻⁵ per mm), e<sub>2</sub> dan M<sub>2</sub>.");
    },
    fields: [{ id: "r0", label: ["1/r<sub>0</sub>", "1/r<sub>0</sub>"], unit: "×10⁻⁵ /mm", fn: function (P) { return P.r0 * 1e5; }, rtol: 0.01 },
             { id: "e2", label: ["e<sub>2</sub>", "e<sub>2</sub>"], unit: "mm", fn: function (P) { return P.e2; }, rtol: 0.01 },
             { id: "m2", label: ["M<sub>2</sub>", "M<sub>2</sub>"], unit: "kN m", fn: function (P) { return P.M2; }, rtol: 0.01 }],
    hints: [function () { return bi("1/r<sub>0</sub> = ε<sub>yd</sub>/(0.45d) with ε<sub>yd</sub> = 435/200 000 = 0.002175.", "1/r<sub>0</sub> = ε<sub>yd</sub>/(0.45d) dengan ε<sub>yd</sub> = 435/200 000 = 0.002175."); },
            function () { return bi("1/r = K<sub>r</sub>K<sub>φ</sub>(1/r<sub>0</sub>); e<sub>2</sub> = (1/r)l<sub>0</sub>²/10.", "1/r = K<sub>r</sub>K<sub>φ</sub>(1/r<sub>0</sub>); e<sub>2</sub> = (1/r)l<sub>0</sub>²/10."); },
            function () { return bi("M<sub>2</sub> = N<sub>Ed</sub>e<sub>2</sub>, with e<sub>2</sub> in metres for kN m.", "M<sub>2</sub> = N<sub>Ed</sub>e<sub>2</sub>, dengan e<sub>2</sub> dalam meter untuk kN m."); }],
    solution: function (P) {
      return sol(["1/r<sub>0</sub> = 0.002175/(0.45 × " + P.d + ") = " + fmt(P.r0 * 1e5, 4) + " × 10⁻⁵ /mm",
        "1/r = " + fmt(P.Kr, 2) + " × " + fmt(P.Kphi, 2) + " × " + fmt(P.r0 * 1e5, 4) + " × 10⁻⁵ = " + fmt(P.rr * 1e5, 4) + " × 10⁻⁵ /mm",
        "e<sub>2</sub> = " + fmt(P.rr * 1e5, 4) + " × 10⁻⁵ × " + P.l0 + "²/10 = " + fmt(P.e2, 2) + " mm",
        "M<sub>2</sub> = " + P.N + " × " + fmt(P.e2 / 1000, 5) + " = " + fmt(P.M2, 2) + " kN m"]);
    }
  });

  /* ---------- B4 design moment of a braced slender column ---------- */
  EX.define("b4", {
    gen: function (r) {
      var h = pick(r, [250, 300, 350, 400]), l0 = step(r, 3500, 6500, 100), N = step(r, 500, 2000, 50), Mt = step(r, 20, 90, 5), Mb = Math.round(Mt * (0.2 + 0.8 * r())), dbl = r() < 0.5, M2 = step(r, 8, 50, 0.5);
      var ei = l0 / 400, Mi = N * ei / 1e3, M02 = Mt + Mi, M01 = Mb + Mi, M0e = Math.max(0.6 * Mt + (dbl ? -0.4 : 0.4) * Mb + Mi, 0.4 * M02), Me0 = N * Math.max(h / 30, 20) / 1e3;
      var c = [["M02", M02], ["M0e+M2", M0e + M2], ["M01+0.5M2", M01 + 0.5 * M2], ["NEde0", Me0]], g = c[0];
      for (var i = 1; i < 4; i++) if (c[i][1] > g[1]) g = c[i];
      return { h: h, l0: l0, N: N, Mt: Mt, Mb: Mb, dbl: dbl, M2: M2, Mi: Mi, M02: M02, M01: M01, M0e: M0e, Me0: Me0, MEd: g[1], gov: g[0] };
    },
    text: function (P) {
      var c = P.dbl ? bi("tension on opposite faces", "tension pada muka bertentangan") : bi("tension on the same face", "tension pada muka yang sama");
      return bi("A braced slender column has h = " + num(P.h) + " mm in the plane of bending, l<sub>0</sub> = " + num(P.l0) + " mm and N<sub>Ed</sub> = " + num(P.N) + " kN; its end moments are " + num(P.Mt) + " and " + num(P.Mb) + " kN m, " + c + ". Its second-order moment is M<sub>2</sub> = " + num(fmt(P.M2, 1)) + " kN m. Find M<sub>0e</sub>, M<sub>01</sub> + 0.5M<sub>2</sub> and the design moment M<sub>Ed</sub>.",
                "Satu column slender braced mempunyai h = " + num(P.h) + " mm dalam satah bending, l<sub>0</sub> = " + num(P.l0) + " mm dan N<sub>Ed</sub> = " + num(P.N) + " kN; end moment-nya ialah " + num(P.Mt) + " dan " + num(P.Mb) + " kN m, " + c + ". Second-order moment-nya ialah M<sub>2</sub> = " + num(fmt(P.M2, 1)) + " kN m. Cari M<sub>0e</sub>, M<sub>01</sub> + 0.5M<sub>2</sub> dan design moment M<sub>Ed</sub>.");
    },
    fields: [{ id: "m0e", label: ["M<sub>0e</sub>", "M<sub>0e</sub>"], unit: "kN m", fn: function (P) { return P.M0e; }, rtol: 0.01, atol: 0.2 },
             { id: "m01", label: ["M<sub>01</sub> + 0.5M<sub>2</sub>", "M<sub>01</sub> + 0.5M<sub>2</sub>"], unit: "kN m", fn: function (P) { return P.M01 + 0.5 * P.M2; }, rtol: 0.01 },
             { id: "med", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.MEd; }, rtol: 0.01 }],
    hints: [function () { return bi("Add N<sub>Ed</sub>e<sub>i</sub> (e<sub>i</sub> = l<sub>0</sub>/400) to both end magnitudes for M<sub>02</sub> and M<sub>01</sub>, and once to M<sub>0e</sub>.", "Tambah N<sub>Ed</sub>e<sub>i</sub> (e<sub>i</sub> = l<sub>0</sub>/400) kepada kedua-dua magnitud hujung bagi M<sub>02</sub> dan M<sub>01</sub>, dan sekali kepada M<sub>0e</sub>."); },
            function () { return bi("M<sub>0e</sub> = 0.6|M|<sub>max</sub> ± 0.4|M|<sub>min</sub> + N<sub>Ed</sub>e<sub>i</sub> ≥ 0.4M<sub>02</sub>; minus in double curvature.", "M<sub>0e</sub> = 0.6|M|<sub>max</sub> ± 0.4|M|<sub>min</sub> + N<sub>Ed</sub>e<sub>i</sub> ≥ 0.4M<sub>02</sub>; tolak dalam double curvature."); },
            function () { return bi("M<sub>Ed</sub> = max(M<sub>02</sub>; M<sub>0e</sub> + M<sub>2</sub>; M<sub>01</sub> + 0.5M<sub>2</sub>; N<sub>Ed</sub>e<sub>0</sub>), e<sub>0</sub> = max(h/30; 20 mm).", "M<sub>Ed</sub> = max(M<sub>02</sub>; M<sub>0e</sub> + M<sub>2</sub>; M<sub>01</sub> + 0.5M<sub>2</sub>; N<sub>Ed</sub>e<sub>0</sub>), e<sub>0</sub> = max(h/30; 20 mm)."); }],
    solution: function (P) {
      var names = { "M02": "M<sub>02</sub>", "M0e+M2": "M<sub>0e</sub> + M<sub>2</sub>", "M01+0.5M2": "M<sub>01</sub> + 0.5M<sub>2</sub>", "NEde0": "N<sub>Ed</sub>e<sub>0</sub>" };
      return sol(["N<sub>Ed</sub>e<sub>i</sub> = " + P.N + " × " + P.l0 + "/400 × 10⁻³ = " + fmt(P.Mi, 2) + " kN m; M<sub>02</sub> = " + fmt(P.M02, 2) + "; M<sub>01</sub> = " + fmt(P.M01, 2),
        "M<sub>0e</sub> = max(0.6 × " + P.Mt + (P.dbl ? " − " : " + ") + "0.4 × " + P.Mb + " + " + fmt(P.Mi, 2) + "; 0.4 × " + fmt(P.M02, 2) + ") = " + fmt(P.M0e, 2) + " kN m",
        "M<sub>01</sub> + 0.5M<sub>2</sub> = " + fmt(P.M01, 2) + " + " + fmt(0.5 * P.M2, 2) + " = " + fmt(P.M01 + 0.5 * P.M2, 2) + "; N<sub>Ed</sub>e<sub>0</sub> = " + fmt(P.Me0, 2),
        "M<sub>Ed</sub> = max(" + fmt(P.M02, 2) + "; " + fmt(P.M0e + P.M2, 2) + "; " + fmt(P.M01 + 0.5 * P.M2, 2) + "; " + fmt(P.Me0, 2) + ") = " + fmt(P.MEd, 2) + " kN m: " + names[P.gov] + bi(" governs", " menentukan")]);
    }
  });

  /* ---------- B5 K_r from the steel ---------- */
  EX.define("b5", {
    gen: function (r) {
      for (var t = 0; t < 50; t++) {
        var b = pick(r, [250, 300, 350, 400]), h = pick(r, [300, 350, 400, 450, 500]), fck = pick(r, [25, 30, 35]), N = step(r, 400, 3000, 50);
        var nb = pick(r, [4, 6, 8]), dia = pick(r, [16, 20, 25, 32]), As = nb * Math.PI * dia * dia / 4;
        var Ac = b * h, fcd = 0.85 * fck / 1.5, n = N * 1e3 / (Ac * fcd), om = As * 435 / (Ac * fcd), nu = 1 + om, Kr = Math.min(1, (nu - n) / (nu - 0.4));
        if (n <= nu - 0.05 || t === 49) return { b: b, h: h, fck: fck, N: N, nb: nb, dia: dia, As: As, fcd: fcd, n: n, om: om, nu: nu, Kr: Kr };
      }
    },
    text: function (P) {
      return bi("A column " + num(P.b) + " × " + num(P.h) + " in " + num(CLS[P.fck]) + " concrete carries N<sub>Ed</sub> = " + num(P.N) + " kN and has " + num(P.nb + "H" + P.dia) + " (B500). Find n, ω and K<sub>r</sub>.",
                "Satu column " + num(P.b) + " × " + num(P.h) + " daripada konkrit " + num(CLS[P.fck]) + " membawa N<sub>Ed</sub> = " + num(P.N) + " kN dan mempunyai " + num(P.nb + "H" + P.dia) + " (B500). Cari n, ω dan K<sub>r</sub>.");
    },
    fields: [{ id: "n", label: ["n", "n"], unit: "", fn: function (P) { return P.n; }, rtol: 0.01 },
             { id: "om", label: ["ω", "ω"], unit: "", fn: function (P) { return P.om; }, rtol: 0.01 },
             { id: "kr", label: ["K<sub>r</sub>", "K<sub>r</sub>"], unit: "", fn: function (P) { return P.Kr; }, rtol: 0.01, atol: 0.005 }],
    hints: [function () { return bi("n = N<sub>Ed</sub>/(A<sub>c</sub>f<sub>cd</sub>), f<sub>cd</sub> = 0.85f<sub>ck</sub>/1.5.", "n = N<sub>Ed</sub>/(A<sub>c</sub>f<sub>cd</sub>), f<sub>cd</sub> = 0.85f<sub>ck</sub>/1.5."); },
            function () { return bi("ω = A<sub>s</sub>f<sub>yd</sub>/(A<sub>c</sub>f<sub>cd</sub>), f<sub>yd</sub> = 435 N/mm²: not the chart’s A<sub>s</sub>f<sub>yk</sub>/(bhf<sub>ck</sub>).", "ω = A<sub>s</sub>f<sub>yd</sub>/(A<sub>c</sub>f<sub>cd</sub>), f<sub>yd</sub> = 435 N/mm²: bukan A<sub>s</sub>f<sub>yk</sub>/(bhf<sub>ck</sub>) chart."); },
            function () { return bi("K<sub>r</sub> = (n<sub>u</sub> − n)/(n<sub>u</sub> − 0.4) ≤ 1 with n<sub>u</sub> = 1 + ω.", "K<sub>r</sub> = (n<sub>u</sub> − n)/(n<sub>u</sub> − 0.4) ≤ 1 dengan n<sub>u</sub> = 1 + ω."); }],
    solution: function (P) {
      return sol(["A<sub>s</sub> = " + P.nb + " × π × " + P.dia + "²/4 = " + fmt(P.As, 0) + " mm²; f<sub>cd</sub> = 0.85 × " + P.fck + "/1.5 = " + fmt(P.fcd, 2) + " N/mm²",
        "n = " + P.N + " × 10³/(" + P.b + " × " + P.h + " × " + fmt(P.fcd, 2) + ") = " + fmt(P.n, 3),
        "ω = " + fmt(P.As, 0) + " × 435/(" + P.b * P.h + " × " + fmt(P.fcd, 2) + ") = " + fmt(P.om, 3) + "; n<sub>u</sub> = " + fmt(P.nu, 3),
        "K<sub>r</sub> = min(1; (" + fmt(P.nu, 3) + " − " + fmt(P.n, 3) + ")/(" + fmt(P.nu, 3) + " − 0.4)) = " + fmt(P.Kr, 3)]);
    }
  });

  /* ---------- B6 biaxial interaction ---------- */
  EX.define("b6", {
    gen: function (r) {
      var Rz = step(r, 80, 260, 1), Ry = Math.round(Rz * (0.55 + 0.45 * r())), Mz = Math.round(Rz * (0.35 + 0.5 * r())), My = Math.round(Ry * (0.15 + 0.45 * r()));
      var NRd = step(r, 1500, 4500, 10), N = Math.round(NRd * (0.05 + 0.85 * r()) / 10) * 10;
      var rN = N / NRd, a = aExp(rN), s = Math.pow(Mz / Rz, a) + Math.pow(My / Ry, a);
      return { Rz: Rz, Ry: Ry, Mz: Mz, My: My, NRd: NRd, N: N, rN: rN, a: a, s: s };
    },
    text: function (P) {
      return bi("A column carries N<sub>Ed</sub> = " + num(P.N) + " kN with M<sub>Ed,z</sub> = " + num(P.Mz) + " and M<sub>Ed,y</sub> = " + num(P.My) + " kN m (the case with the imperfection, as worked). Its bars give M<sub>Rd,z</sub> = " + num(P.Rz) + " and M<sub>Rd,y</sub> = " + num(P.Ry) + " kN m at N<sub>Ed</sub>, and N<sub>Rd</sub> = " + num(P.NRd) + " kN. Find N<sub>Ed</sub>/N<sub>Rd</sub>, the exponent a and the interaction sum of Eq. 5.39.",
                "Satu column membawa N<sub>Ed</sub> = " + num(P.N) + " kN dengan M<sub>Ed,z</sub> = " + num(P.Mz) + " dan M<sub>Ed,y</sub> = " + num(P.My) + " kN m (kes dengan imperfection, seperti yang dikira). Bar-nya memberi M<sub>Rd,z</sub> = " + num(P.Rz) + " dan M<sub>Rd,y</sub> = " + num(P.Ry) + " kN m pada N<sub>Ed</sub>, dan N<sub>Rd</sub> = " + num(P.NRd) + " kN. Cari N<sub>Ed</sub>/N<sub>Rd</sub>, eksponen a dan jumlah interaction Eq. 5.39.");
    },
    fields: [{ id: "rn", label: ["N<sub>Ed</sub>/N<sub>Rd</sub>", "N<sub>Ed</sub>/N<sub>Rd</sub>"], unit: "", fn: function (P) { return P.rN; }, rtol: 0.01, atol: 0.002 },
             { id: "a", label: ["a", "a"], unit: "", fn: function (P) { return P.a; }, rtol: 0.005 },
             { id: "s", label: ["sum", "jumlah"], unit: "", fn: function (P) { return P.s; }, rtol: 0.01 }],
    hints: [function () { return bi("a = 1.0 for N<sub>Ed</sub>/N<sub>Rd</sub> ≤ 0.1, 1.5 at 0.7, 2.0 at 1.0; interpolate linearly between.", "a = 1.0 bagi N<sub>Ed</sub>/N<sub>Rd</sub> ≤ 0.1, 1.5 pada 0.7, 2.0 pada 1.0; interpolasi secara linear di antaranya."); },
            function () { return bi("Sum = (M<sub>Ed,z</sub>/M<sub>Rd,z</sub>)<sup>a</sup> + (M<sub>Ed,y</sub>/M<sub>Rd,y</sub>)<sup>a</sup>; it must not exceed 1.", "Jumlah = (M<sub>Ed,z</sub>/M<sub>Rd,z</sub>)<sup>a</sup> + (M<sub>Ed,y</sub>/M<sub>Rd,y</sub>)<sup>a</sup>; ia tidak boleh melebihi 1."); }],
    solution: function (P) {
      return sol(["N<sub>Ed</sub>/N<sub>Rd</sub> = " + P.N + "/" + P.NRd + " = " + fmt(P.rN, 3) + " → a = " + fmt(P.a, 3),
        "(" + P.Mz + "/" + P.Rz + ")<sup>" + fmt(P.a, 3) + "</sup> + (" + P.My + "/" + P.Ry + ")<sup>" + fmt(P.a, 3) + "</sup> = " + fmt(Math.pow(P.Mz / P.Rz, P.a), 3) + " + " + fmt(Math.pow(P.My / P.Ry, P.a), 3) + " = " + fmt(P.s, 3),
        P.s <= 1 ? bi("≤ 1: adequate in biaxial bending (check the other imperfection case too)", "≤ 1: mencukupi dalam biaxial bending (semak juga kes imperfection yang satu lagi)") : bi("&gt; 1: add steel", "&gt; 1: tambah steel")]);
    }
  });

  EX.ready();
})();
