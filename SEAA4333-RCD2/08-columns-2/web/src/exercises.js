/* SEAA 4333 Unit 8 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes: e_i = l0/400, M02 = larger end moment + NEd e_i,
   e0 = max(h/30, 20 mm), MEd = max(M02, NEd e0); strain compatibility with the 0.567fck block over s = min(0.8x, h),
   0.0035 at the compression face for x <= h and a pivot of 0.002 at 3h/7 for x > h, Es = 200 kN/mm2,
   fyd = 0.87fyk = 435 N/mm2 (B500), concrete displaced by the bars ignored; nu = N/(bh fck), mu = M/(bh^2 fck),
   omega = As fyk/(bh fck); As,min = max(0.10NEd/fyd, 0.002Ac), As,max = 0.04Ac; links: phi >= max(6, phi_max/4),
   s_cl,max = min(20 phi_min, smaller side, 400), 0.6 s_cl,max within the larger side of beams and slabs. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return a + s * Math.floor(r() * (n + 1)); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  var CLS = { 25: "C25/30", 30: "C30/37", 35: "C35/45" };
  function barA(d) { return Math.PI * d * d / 4; }

  /* ---------- the course method: strain compatibility ---------- */
  var ES = 200000, FYD = 435, EYD = FYD / ES, XBAL = 0.0035 / (0.0035 + EYD);
  function nmAt(x, H, B, bars, fck) {                                  // bars: [[depth from the compression face, area]]
    var s = Math.min(0.8 * x, H), Fc = 0.567 * fck * B * s, N = Fc, M = Fc * (H / 2 - s / 2);
    for (var i = 0; i < bars.length; i++) {
      var y = bars[i][0], A = bars[i][1], e = x <= H ? 0.0035 * (x - y) / x : 0.002 * (x - y) / (x - 3 * H / 7);
      var sg = Math.max(-FYD, Math.min(FYD, ES * e)); N += sg * A; M += sg * A * (H / 2 - y);
    }
    return { N: N / 1e3, M: M / 1e6 };
  }
  function mRd(N, H, B, bars, fck) {
    var lo = 1e-6, hi = 1e4 * H;
    if (N < nmAt(lo, H, B, bars, fck).N || N > nmAt(hi, H, B, bars, fck).N) return -1;
    for (var k = 0; k < 110; k++) { var mid = (lo + hi) / 2; if (nmAt(mid, H, B, bars, fck).N < N) lo = mid; else hi = mid; }
    return nmAt((lo + hi) / 2, H, B, bars, fck).M;
  }
  function asReq(N, M, H, B, d2, fck) {
    function cap(A) { return mRd(N, H, B, [[d2, A / 2], [H - d2, A / 2]], fck); }
    if (cap(0) >= M) return 0;
    var lo = 0, hi = 0.2 * B * H;
    if (cap(hi) < M) return Infinity;
    for (var k = 0; k < 60; k++) { var mid = (lo + hi) / 2; if (cap(mid) < M) lo = mid; else hi = mid; }
    return hi;
  }

  /* ---------- B1 design moment ---------- */
  EX.define("b1", {
    gen: function (r) {
      var h = pick(r, [250, 300, 350, 400, 450, 500, 600]), l0 = step(r, 2000, 4500, 100), N = step(r, 300, 3000, 50);
      var small = r() < 0.4, Mt = small ? step(r, 5, 25, 1) : step(r, 30, 140, 5), Mb = Math.round(Mt * (0.3 + 0.6 * r())), dbl = r() < 0.7;
      var ei = l0 / 400, M02 = Mt + N * ei / 1e3, e0 = Math.max(h / 30, 20), Me0 = N * e0 / 1e3;
      return { h: h, l0: l0, N: N, Mt: Mt, Mb: Mb, dbl: dbl, ei: ei, M02: M02, e0: e0, Me0: Me0, MEd: Math.max(M02, Me0) };
    },
    text: function (P) {
      var c = P.dbl ? bi("tension on opposite faces", "tegangan pada muka bertentangan") : bi("tension on the same face", "tegangan pada muka yang sama");
      return bi("A braced, non-slender column has h = " + num(P.h) + " mm in the plane of bending and l<sub>0</sub> = " + num(P.l0) + " mm. N<sub>Ed</sub> = " + num(P.N) + " kN; the first-order end moments are " + num(P.Mt) + " and " + num(P.Mb) + " kN m, " + c + ". Find the imperfection eccentricity e<sub>i</sub>, the moment M<sub>02</sub> and the design moment M<sub>Ed</sub>.",
                "Satu column braced dan non-slender mempunyai h = " + num(P.h) + " mm dalam satah lenturan dan l<sub>0</sub> = " + num(P.l0) + " mm. N<sub>Ed</sub> = " + num(P.N) + " kN; first-order end moment ialah " + num(P.Mt) + " dan " + num(P.Mb) + " kN m, " + c + ". Cari imperfection eccentricity e<sub>i</sub>, moment M<sub>02</sub> dan design moment M<sub>Ed</sub>.");
    },
    fields: [{ id: "ei", label: ["e<sub>i</sub>", "e<sub>i</sub>"], unit: "mm", fn: function (P) { return P.ei; }, rtol: 0.01 },
             { id: "m02", label: ["M<sub>02</sub>", "M<sub>02</sub>"], unit: "kN m", fn: function (P) { return P.M02; }, rtol: 0.01 },
             { id: "med", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.MEd; }, rtol: 0.01 }],
    hints: [function () { return bi("e<sub>i</sub> = l<sub>0</sub>/400 (EC2 5.2(9)).", "e<sub>i</sub> = l<sub>0</sub>/400 (EC2 5.2(9))."); },
            function () { return bi("M<sub>02</sub> = the larger end moment + N<sub>Ed</sub>e<sub>i</sub>; the curvature does not matter here.", "M<sub>02</sub> = end moment yang lebih besar + N<sub>Ed</sub>e<sub>i</sub>; curvature tidak penting di sini."); },
            function (P) { return bi("e<sub>0</sub> = max(h/30; 20 mm) = " + fmt(P.e0, 1) + " mm; M<sub>Ed</sub> = max(M<sub>02</sub>; N<sub>Ed</sub>e<sub>0</sub>).", "e<sub>0</sub> = max(h/30; 20 mm) = " + fmt(P.e0, 1) + " mm; M<sub>Ed</sub> = max(M<sub>02</sub>; N<sub>Ed</sub>e<sub>0</sub>)."); }],
    solution: function (P) {
      return sol(["e<sub>i</sub> = " + P.l0 + "/400 = " + fmt(P.ei, 2) + " mm",
        "M<sub>02</sub> = " + P.Mt + " + " + P.N + " × " + fmt(P.ei / 1000, 5) + " = " + fmt(P.M02, 2) + " kN m",
        "e<sub>0</sub> = max(" + P.h + "/30; 20) = " + fmt(P.e0, 1) + " mm; N<sub>Ed</sub>e<sub>0</sub> = " + P.N + " × " + fmt(P.e0 / 1000, 4) + " = " + fmt(P.Me0, 2) + " kN m",
        "M<sub>Ed</sub> = max(" + fmt(P.M02, 2) + "; " + fmt(P.Me0, 2) + ") = " + fmt(P.MEd, 2) + " kN m" + (P.Me0 > P.M02 ? bi(": the minimum eccentricity governs", ": minimum eccentricity menentukan") : "")]);
    }
  });

  /* ---------- B2 chart parameters and steel ---------- */
  EX.define("b2", {
    gen: function (r) {
      var c, tries = 0;
      do {
        var b = pick(r, [250, 300, 350, 400]), h = pick(r, [300, 350, 400, 450, 500, 600]), fck = pick(r, [25, 30, 35]);
        var nu = 0.1 + 0.7 * r(), mu = 0.03 + 0.15 * r();
        var N = Math.round(nu * b * h * fck / 1e4) * 10, M = Math.round(mu * b * h * h * fck / 1e7) * 10;
        var As = asReq(N, M, h, b, 0.15 * h, fck), om = As * 500 / (b * h * fck);
        c = { b: b, h: h, fck: fck, N: N, M: M, om: Math.round(om * 100) / 100 }; tries++;
      } while ((!isFinite(om) || c.om < 0.03 || c.om > 0.9) && tries < 40);
      c.nu = c.N * 1e3 / (c.b * c.h * c.fck); c.mu = c.M * 1e6 / (c.b * c.h * c.h * c.fck); c.As = c.om * c.b * c.h * c.fck / 500;
      return c;
    },
    text: function (P) {
      return bi("A non-slender column " + num(P.b + " × " + P.h) + " (h = " + P.h + " mm in the plane of bending), " + CLS[P.fck] + ", B500, carries N<sub>Ed</sub> = " + num(P.N) + " kN and M<sub>Ed</sub> = " + num(P.M) + " kN m. Find ν and μ for the design chart. On the chart for d<sub>2</sub>/h = 0.15 the point reads A<sub>s</sub>f<sub>yk</sub>/(bhf<sub>ck</sub>) = " + num(fmt(P.om, 2)) + ": find A<sub>s</sub>.",
                "Satu column non-slender " + num(P.b + " × " + P.h) + " (h = " + P.h + " mm dalam satah lenturan), " + CLS[P.fck] + ", B500, membawa N<sub>Ed</sub> = " + num(P.N) + " kN dan M<sub>Ed</sub> = " + num(P.M) + " kN m. Cari ν dan μ untuk design chart. Pada chart bagi d<sub>2</sub>/h = 0.15 titik itu memberi bacaan A<sub>s</sub>f<sub>yk</sub>/(bhf<sub>ck</sub>) = " + num(fmt(P.om, 2)) + ": cari A<sub>s</sub>.");
    },
    fields: [{ id: "nu", label: ["ν = N/(bhf<sub>ck</sub>)", "ν = N/(bhf<sub>ck</sub>)"], fn: function (P) { return P.nu; }, rtol: 0.01, atol: 0.002 },
             { id: "mu", label: ["μ = M/(bh²f<sub>ck</sub>)", "μ = M/(bh²f<sub>ck</sub>)"], fn: function (P) { return P.mu; }, rtol: 0.01, atol: 0.001 },
             { id: "as", label: ["A<sub>s</sub>", "A<sub>s</sub>"], unit: "mm²", fn: function (P) { return P.As; }, rtol: 0.01 }],
    hints: [function () { return bi("Use h, the full depth, not d: ν = N<sub>Ed</sub>/(bhf<sub>ck</sub>), μ = M<sub>Ed</sub>/(bh²f<sub>ck</sub>), with N in N and M in N mm.", "Gunakan h, kedalaman penuh, bukan d: ν = N<sub>Ed</sub>/(bhf<sub>ck</sub>), μ = M<sub>Ed</sub>/(bh²f<sub>ck</sub>), dengan N dalam N dan M dalam N mm."); },
            function () { return bi("A<sub>s</sub> = ω × bhf<sub>ck</sub>/f<sub>yk</sub>, the total of both faces.", "A<sub>s</sub> = ω × bhf<sub>ck</sub>/f<sub>yk</sub>, jumlah kedua-dua muka."); }],
    solution: function (P) {
      return sol(["ν = " + P.N + " × 10³/(" + P.b + " × " + P.h + " × " + P.fck + ") = " + fmt(P.nu, 3),
        "μ = " + P.M + " × 10⁶/(" + P.b + " × " + P.h + "² × " + P.fck + ") = " + fmt(P.mu, 4),
        "A<sub>s</sub> = " + fmt(P.om, 2) + " × " + P.b + " × " + P.h + " × " + P.fck + "/500 = " + fmt(P.As, 0) + " mm²"]);
    }
  });

  /* ---------- B3 steel limits ---------- */
  EX.define("b3", {
    gen: function (r) {
      var b = pick(r, [250, 300, 350, 400, 450]), h = pick(r, [300, 350, 400, 450, 500, 600]), N = step(r, 400, 4000, 50);
      var Ac = b * h, a1 = 0.10 * N * 1e3 / FYD, a2 = 0.002 * Ac, mn = Math.max(a1, a2), req = Math.round(mn * (0.55 + 2.0 * r()) / 10) * 10;
      return { b: b, h: h, N: N, Ac: Ac, a1: a1, a2: a2, mn: mn, mx: 0.04 * Ac, req: req, prov: Math.max(req, mn) };
    },
    text: function (P) {
      return bi("A column " + num(P.b + " × " + P.h) + " with B500 bars carries N<sub>Ed</sub> = " + num(P.N) + " kN; the design chart asks for A<sub>s</sub> = " + num(P.req) + " mm². Find A<sub>s,min</sub>, A<sub>s,max</sub> (outside laps) and the smallest total area you must provide.",
                "Satu column " + num(P.b + " × " + P.h) + " dengan bar B500 membawa N<sub>Ed</sub> = " + num(P.N) + " kN; design chart meminta A<sub>s</sub> = " + num(P.req) + " mm². Cari A<sub>s,min</sub>, A<sub>s,max</sub> (di luar lap) dan jumlah luas terkecil yang mesti anda sediakan.");
    },
    fields: [{ id: "mn", label: ["A<sub>s,min</sub>", "A<sub>s,min</sub>"], unit: "mm²", fn: function (P) { return P.mn; }, rtol: 0.01 },
             { id: "mx", label: ["A<sub>s,max</sub>", "A<sub>s,max</sub>"], unit: "mm²", fn: function (P) { return P.mx; }, rtol: 0.005 },
             { id: "pv", label: ["A<sub>s</sub> to provide, at least", "A<sub>s</sub> yang mesti disediakan, sekurang-kurangnya"], unit: "mm²", fn: function (P) { return P.prov; }, rtol: 0.01 }],
    hints: [function () { return bi("A<sub>s,min</sub> = the larger of 0.10N<sub>Ed</sub>/f<sub>yd</sub> (f<sub>yd</sub> = 435 N/mm²) and 0.002A<sub>c</sub>.", "A<sub>s,min</sub> = yang lebih besar antara 0.10N<sub>Ed</sub>/f<sub>yd</sub> (f<sub>yd</sub> = 435 N/mm²) dan 0.002A<sub>c</sub>."); },
            function () { return bi("A<sub>s,max</sub> = 0.04A<sub>c</sub>; provide the larger of the chart value and A<sub>s,min</sub>.", "A<sub>s,max</sub> = 0.04A<sub>c</sub>; sediakan yang lebih besar antara nilai chart dan A<sub>s,min</sub>."); }],
    solution: function (P) {
      return sol(["0.10 × " + P.N + " × 10³/435 = " + fmt(P.a1, 0) + " mm²; 0.002 × " + P.Ac + " = " + fmt(P.a2, 0) + " mm² → A<sub>s,min</sub> = " + fmt(P.mn, 0) + " mm²",
        "A<sub>s,max</sub> = 0.04 × " + P.Ac + " = " + fmt(P.mx, 0) + " mm²",
        bi("Provide at least max(" + P.req + "; " + fmt(P.mn, 0) + ") = " + fmt(P.prov, 0) + " mm²", "Sediakan sekurang-kurangnya max(" + P.req + "; " + fmt(P.mn, 0) + ") = " + fmt(P.prov, 0) + " mm²")]);
    }
  });

  /* ---------- a section for B4 and B5 ---------- */
  function section(r) {
    var b = pick(r, [300, 350, 400, 450]), h = pick(r, [300, 350, 400, 450, 500]), fck = pick(r, [25, 30, 35]);
    var nb = pick(r, [2, 3]), phi = pick(r, [16, 20, 25]), lk = phi > 20 ? 8 : 6, cn = pick(r, [30, 35]);
    var d2 = cn + lk + phi / 2, As = 2 * nb * barA(phi);
    return { b: b, h: h, fck: fck, nb: nb, phi: phi, lk: lk, cn: cn, d2: d2, d: h - d2, As: As, half: As / 2 };
  }
  function secText(S) {
    return bi("A column section " + num(S.b + " × " + S.h) + " (h = " + S.h + " mm in the plane of bending), " + CLS[S.fck] + ", has " + num(S.nb + "H" + S.phi) + " at each of the two faces, with d<sub>2</sub> = " + num(fmt(S.d2, 0)) + " mm (A<sub>s</sub> = " + fmt(S.As, 0) + " mm² in all). B500, E<sub>s</sub> = 200 kN/mm², f<sub>yd</sub> = 435 N/mm².",
              "Satu section column " + num(S.b + " × " + S.h) + " (h = " + S.h + " mm dalam satah lenturan), " + CLS[S.fck] + ", mempunyai " + num(S.nb + "H" + S.phi) + " pada setiap satu daripada dua muka, dengan d<sub>2</sub> = " + num(fmt(S.d2, 0)) + " mm (A<sub>s</sub> = " + fmt(S.As, 0) + " mm² keseluruhannya). B500, E<sub>s</sub> = 200 kN/mm², f<sub>yd</sub> = 435 N/mm².");
  }

  /* ---------- B4 squash load and balance point ---------- */
  EX.define("b4", {
    gen: function (r) {
      var S = section(r), N0 = (0.567 * S.fck * S.b * S.h + 400 * S.As) / 1e3, xb = XBAL * S.d, s = 0.8 * xb, Fc = 0.567 * S.fck * S.b * s;
      var e1 = 0.0035 * (xb - S.d2) / xb, sg1 = Math.min(FYD, ES * e1), F1 = sg1 * S.half, F2 = FYD * S.half;
      S.N0 = N0; S.xb = xb; S.s = s; S.Fc = Fc / 1e3; S.e1 = e1; S.sg1 = sg1; S.F1 = F1 / 1e3; S.F2 = F2 / 1e3;
      S.Nb = (Fc + F1 - F2) / 1e3; S.Mb = (Fc * (S.h / 2 - s / 2) + F1 * (S.h / 2 - S.d2) + F2 * (S.d - S.h / 2)) / 1e6;
      return S;
    },
    text: function (P) { return secText(P) + " " + bi("Find the squash load N<sub>0</sub> (strain 0.002 everywhere), the neutral axis depth at balance x<sub>bal</sub>, and N and M at balance.", "Cari squash load N<sub>0</sub> (strain 0.002 di semua tempat), neutral axis depth pada balance x<sub>bal</sub>, dan N serta M pada balance."); },
    fields: [{ id: "n0", label: ["N<sub>0</sub>", "N<sub>0</sub>"], unit: "kN", fn: function (P) { return P.N0; }, rtol: 0.01 },
             { id: "xb", label: ["x<sub>bal</sub>", "x<sub>bal</sub>"], unit: "mm", fn: function (P) { return P.xb; }, rtol: 0.01 },
             { id: "nb", label: ["N<sub>bal</sub>", "N<sub>bal</sub>"], unit: "kN", fn: function (P) { return P.Nb; }, rtol: 0.015 },
             { id: "mb", label: ["M<sub>bal</sub>", "M<sub>bal</sub>"], unit: "kN m", fn: function (P) { return P.Mb; }, rtol: 0.015 }],
    hints: [function () { return bi("N<sub>0</sub> = 0.567f<sub>ck</sub>bh + 400A<sub>s</sub>: at a strain of 0.002 the bars carry 200 000 × 0.002 = 400 N/mm², not 435.", "N<sub>0</sub> = 0.567f<sub>ck</sub>bh + 400A<sub>s</sub>: pada strain 0.002 bar membawa 200 000 × 0.002 = 400 N/mm², bukan 435."); },
            function () { return bi("x<sub>bal</sub> = 0.0035/(0.0035 + 0.002175) × d = 0.617d, with d = h − d<sub>2</sub>.", "x<sub>bal</sub> = 0.0035/(0.0035 + 0.002175) × d = 0.617d, dengan d = h − d<sub>2</sub>."); },
            function () { return bi("Check the top bars: ε = 0.0035(x − d<sub>2</sub>)/x; the bottom bars carry 435 N/mm² in tension. N = F<sub>c</sub> + F<sub>sc</sub> − F<sub>s</sub>; M about h/2 by Eq. (8.6).", "Semak bar atas: ε = 0.0035(x − d<sub>2</sub>)/x; bar bawah membawa 435 N/mm² dalam tegangan. N = F<sub>c</sub> + F<sub>sc</sub> − F<sub>s</sub>; M pada h/2 dengan Eq. (8.6)."); }],
    solution: function (P) {
      return sol(["N<sub>0</sub> = (0.567 × " + P.fck + " × " + P.b + " × " + P.h + " + 400 × " + fmt(P.As, 0) + ")/10³ = " + fmt(P.N0, 0) + " kN",
        "d = " + P.h + " − " + fmt(P.d2, 0) + " = " + fmt(P.d, 0) + " mm; x<sub>bal</sub> = 0.6167 × " + fmt(P.d, 0) + " = " + fmt(P.xb, 1) + " mm; s = 0.8x = " + fmt(P.s, 1) + " mm",
        "F<sub>c</sub> = 0.567 × " + P.fck + " × " + P.b + " × " + fmt(P.s, 1) + " = " + fmt(P.Fc, 1) + " kN",
        bi("top bars: ε = 0.0035 × (" + fmt(P.xb, 1) + " − " + fmt(P.d2, 0) + ")/" + fmt(P.xb, 1) + " = " + fmt(P.e1, 5) + " → σ = " + fmt(P.sg1, 0) + " N/mm², F<sub>sc</sub> = " + fmt(P.F1, 1) + " kN; bottom bars F<sub>s</sub> = 435 × " + fmt(P.half, 0) + " = " + fmt(P.F2, 1) + " kN",
           "bar atas: ε = 0.0035 × (" + fmt(P.xb, 1) + " − " + fmt(P.d2, 0) + ")/" + fmt(P.xb, 1) + " = " + fmt(P.e1, 5) + " → σ = " + fmt(P.sg1, 0) + " N/mm², F<sub>sc</sub> = " + fmt(P.F1, 1) + " kN; bar bawah F<sub>s</sub> = 435 × " + fmt(P.half, 0) + " = " + fmt(P.F2, 1) + " kN"),
        "N<sub>bal</sub> = " + fmt(P.Fc, 1) + " + " + fmt(P.F1, 1) + " − " + fmt(P.F2, 1) + " = " + fmt(P.Nb, 0) + " kN",
        "M<sub>bal</sub> = " + fmt(P.Fc, 1) + " × " + fmt((P.h / 2 - P.s / 2) / 1000, 4) + " + " + fmt(P.F1, 1) + " × " + fmt((P.h / 2 - P.d2) / 1000, 4) + " + " + fmt(P.F2, 1) + " × " + fmt((P.d - P.h / 2) / 1000, 4) + " = " + fmt(P.Mb, 1) + " kN m"]);
    }
  });

  /* ---------- B5 the point x = h ---------- */
  EX.define("b5", {
    gen: function (r) {
      var S = section(r), s = 0.8 * S.h, Fc = 0.567 * S.fck * S.b * s, e1 = 0.0035 * (S.h - S.d2) / S.h, sg1 = Math.min(FYD, ES * e1);
      var e2 = 0.0035 * S.d2 / S.h, sg2 = ES * e2, F1 = sg1 * S.half, F2 = sg2 * S.half, arm = S.h / 2 - S.d2;
      S.s = s; S.Fc = Fc / 1e3; S.e1 = e1; S.sg1 = sg1; S.e2 = e2; S.sg2 = sg2; S.F1 = F1 / 1e3; S.F2 = F2 / 1e3; S.arm = arm;
      S.N = (Fc + F1 + F2) / 1e3; S.M = (Fc * (S.h / 2 - s / 2) + F1 * arm - F2 * arm) / 1e6;
      return S;
    },
    text: function (P) { return secText(P) + " " + bi("Take the neutral axis at the bottom face, x = h. Find the concrete force F<sub>c</sub>, and N and M of the section.", "Ambil neutral axis pada muka bawah, x = h. Cari concrete force F<sub>c</sub>, dan N serta M bagi section itu."); },
    fields: [{ id: "fc", label: ["F<sub>c</sub>", "F<sub>c</sub>"], unit: "kN", fn: function (P) { return P.Fc; }, rtol: 0.01 },
             { id: "n", label: ["N", "N"], unit: "kN", fn: function (P) { return P.N; }, rtol: 0.01 },
             { id: "m", label: ["M", "M"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.015 }],
    hints: [function () { return bi("s = 0.8h; F<sub>c</sub> = 0.567f<sub>ck</sub>b × 0.8h, acting 0.4h from the top, so 0.1h above the centre.", "s = 0.8h; F<sub>c</sub> = 0.567f<sub>ck</sub>b × 0.8h, bertindak 0.4h dari atas, jadi 0.1h di atas pusat."); },
            function () { return bi("Strains: 0.0035 at the top, zero at the bottom face. Top bars ε = 0.0035(h − d<sub>2</sub>)/h; bottom bars ε = 0.0035d<sub>2</sub>/h, a small compression.", "Strain: 0.0035 di atas, sifar pada muka bawah. Bar atas ε = 0.0035(h − d<sub>2</sub>)/h; bar bawah ε = 0.0035d<sub>2</sub>/h, mampatan yang kecil."); },
            function () { return bi("Both bar forces are compressions: N = F<sub>c</sub> + F<sub>1</sub> + F<sub>2</sub>; M = F<sub>c</sub> × 0.1h + (F<sub>1</sub> − F<sub>2</sub>)(h/2 − d<sub>2</sub>).", "Kedua-dua daya bar ialah mampatan: N = F<sub>c</sub> + F<sub>1</sub> + F<sub>2</sub>; M = F<sub>c</sub> × 0.1h + (F<sub>1</sub> − F<sub>2</sub>)(h/2 − d<sub>2</sub>)."); }],
    solution: function (P) {
      return sol(["s = 0.8 × " + P.h + " = " + fmt(P.s, 0) + " mm; F<sub>c</sub> = 0.567 × " + P.fck + " × " + P.b + " × " + fmt(P.s, 0) + " = " + fmt(P.Fc, 1) + " kN",
        bi("top bars: ε = " + fmt(P.e1, 5) + " → σ = " + fmt(P.sg1, 0) + " N/mm², F<sub>1</sub> = " + fmt(P.F1, 1) + " kN; bottom bars: ε = " + fmt(P.e2, 5) + " → σ = " + fmt(P.sg2, 0) + " N/mm², F<sub>2</sub> = " + fmt(P.F2, 1) + " kN",
           "bar atas: ε = " + fmt(P.e1, 5) + " → σ = " + fmt(P.sg1, 0) + " N/mm², F<sub>1</sub> = " + fmt(P.F1, 1) + " kN; bar bawah: ε = " + fmt(P.e2, 5) + " → σ = " + fmt(P.sg2, 0) + " N/mm², F<sub>2</sub> = " + fmt(P.F2, 1) + " kN"),
        "N = " + fmt(P.Fc, 1) + " + " + fmt(P.F1, 1) + " + " + fmt(P.F2, 1) + " = " + fmt(P.N, 0) + " kN",
        "M = " + fmt(P.Fc, 1) + " × " + fmt(P.h / 10000, 4) + " + (" + fmt(P.F1, 1) + " − " + fmt(P.F2, 1) + ") × " + fmt(P.arm / 1000, 4) + " = " + fmt(P.M, 1) + " kN m"]);
    }
  });

  /* ---------- B6 links ---------- */
  EX.define("b6", {
    gen: function (r) {
      var b = pick(r, [250, 300, 350, 400]), h = pick(r, [300, 350, 400, 450, 500, 600]); if (h < b) { var t = b; b = h; h = t; }
      var pc = pick(r, [16, 20, 25, 32]), mid = r() < 0.6, pm = mid ? pick(r, [12, 16, 20].filter(function (v) { return v <= pc; })) : 0;
      var pmax = pc, pmin = mid ? pm : pc, phl = Math.max(6, pmax / 4), smax = Math.min(20 * pmin, b, 400);
      return { b: b, h: h, pc: pc, mid: mid, pm: pm, phl: phl, smax: smax, s6: 0.6 * smax, zone: h };
    },
    text: function (P) {
      var bars = P.mid ? bi("4H" + P.pc + " at the corners and 2H" + P.pm + " at the middle of the two longer faces", "4H" + P.pc + " di sudut dan 2H" + P.pm + " di tengah dua muka yang lebih panjang") : bi("4H" + P.pc + " at the corners", "4H" + P.pc + " di sudut");
      return bi("A column " + num(P.b + " × " + P.h) + " has " + num(bars) + ". Find the smallest link diameter EC2 allows, the largest link spacing s<sub>cl,max</sub> away from the beams, the reduced spacing near the beams and slabs, and the length of column, above or below each floor, over which the reduced spacing applies.",
                "Satu column " + num(P.b + " × " + P.h) + " mempunyai " + num(bars) + ". Cari diameter link terkecil yang dibenarkan oleh EC2, jarak link terbesar s<sub>cl,max</sub> jauh dari beam, jarak yang dikurangkan berhampiran beam dan slab, dan panjang column, di atas atau di bawah setiap lantai, yang jarak dikurangkan itu terpakai.");
    },
    fields: [{ id: "phl", label: ["φ<sub>link</sub>, smallest", "φ<sub>link</sub>, terkecil"], unit: "mm", fn: function (P) { return P.phl; }, atol: 0.05, rtol: 0 },
             { id: "smax", label: ["s<sub>cl,max</sub>", "s<sub>cl,max</sub>"], unit: "mm", fn: function (P) { return P.smax; }, atol: 0.5, rtol: 0 },
             { id: "s6", label: ["0.6s<sub>cl,max</sub>", "0.6s<sub>cl,max</sub>"], unit: "mm", fn: function (P) { return P.s6; }, atol: 0.5, rtol: 0 },
             { id: "zone", label: ["length of the closer zone", "panjang zon rapat"], unit: "mm", fn: function (P) { return P.zone; }, atol: 0.5, rtol: 0 }],
    hints: [function () { return bi("Diameter: the larger of 6 mm and a quarter of the largest bar.", "Diameter: yang lebih besar antara 6 mm dan satu perempat bar terbesar."); },
            function () { return bi("Spacing: the least of 20 × the smallest bar, the smaller side of the column, and 400 mm.", "Jarak: yang terkecil antara 20 × bar terkecil, sisi column yang lebih kecil, dan 400 mm."); },
            function () { return bi("0.6 × s<sub>cl,max</sub> over a length equal to the larger side of the column (EC2 9.5.3(4)).", "0.6 × s<sub>cl,max</sub> sepanjang jarak yang sama dengan sisi column yang lebih besar (EC2 9.5.3(4))."); }],
    solution: function (P) {
      return sol(["φ<sub>link</sub> ≥ max(6; " + P.pc + "/4) = " + fmt(P.phl, 2) + " mm" + (P.phl > 6 ? bi(" → use H8 (or larger)", " → guna H8 (atau lebih besar)") : bi(" → H6", " → H6")),
        "s<sub>cl,max</sub> = min(20 × " + (P.mid ? P.pm : P.pc) + "; " + P.b + "; 400) = " + fmt(P.smax, 0) + " mm",
        "0.6 × " + fmt(P.smax, 0) + " = " + fmt(P.s6, 0) + " mm " + bi("(round down to a multiple of 25 mm on the drawing)", "(bundarkan ke bawah kepada gandaan 25 mm pada lukisan)"),
        bi("over max(b; h) = " + P.h + " mm above and below each beam or slab", "sepanjang max(b; h) = " + P.h + " mm di atas dan di bawah setiap beam atau slab")]);
    }
  });

  EX.ready();
})();
