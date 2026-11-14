/* SEAA 4333 Unit 1 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes: y = h√(R² + G²)/G, t = y + R/2, n_d = 1.35g_k + 1.5q_k;
   L on plan, centre to centre; M = FL/10 with a continuous end, FL/8 with none; V_A with the hogging moments;
   K, z, A_s by RDF §6; deflection by EC2 Eq. 7.16a with K = 1.5 / 1.3 / 1.0 and A_s,prov/A_s,req ≤ 1.5. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return a + s * Math.floor(r() * (n + 1)); }
  function r2(x) { return Math.round(x * 100) / 100; }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }

  /* ---------- the beam on plan, shared by B3 and B4 ---------- */
  function segments(c) {
    if (c.type === "straight") return [{ kind: "flight", l: c.flight + c.bA / 2 + c.bB / 2 }];
    if (c.type === "landTop") return [{ kind: "flight", l: c.flight + c.bA / 2 }, { kind: "landing", l: c.landing + c.bB / 2 }];
    return [{ kind: "landing", l: c.landing + c.bA / 2 }, { kind: "flight", l: c.flight + c.bB / 2 }];
  }
  function analyse(c) {
    var sg = segments(c), L = 0, x = 0, F = 0, mB = 0, parts = [];
    sg.forEach(function (s) { L += s.l; });
    L /= 1000;
    sg.forEach(function (s) { var lm = s.l / 1000, n = s.kind === "flight" ? c.ndf : c.ndL, Fi = n * lm, xc = x + lm / 2;
      parts.push({ kind: s.kind, l: s.l, lm: lm, n: n, Fi: Fi, xc: xc }); F += Fi; mB += Fi * (L - xc); x += lm; });
    var nc = (c.contA ? 1 : 0) + (c.contB ? 1 : 0), coef = nc ? 10 : 8, M = F * L / coef;
    var MA = c.contA ? M : 0, MB = c.contB ? M : 0, VA = mB / L + (MA - MB) / L;
    return { parts: parts, L: L, F: F, coef: coef, M: M, MA: MA, MB: MB, VA: VA, VB: F - VA, mB: mB, nc: nc };
  }
  function genStair(r, types) {
    var G = step(r, 255, 300, 5), nG = step(r, 8, 12, 1), type = pick(r, types);
    var contA = r() < 0.6, contB = r() < 0.5;
    var bA = contA ? pick(r, [200, 250, 300]) : pick(r, [200, 230]), bB = contB ? pick(r, [200, 250, 300]) : pick(r, [200, 230]);
    var ndf = r2(14 + 4.5 * r()), ndL = r2(ndf / (1.25 + 0.1 * r()));
    return { type: type, G: G, nG: nG, flight: nG * G, landing: type === "straight" ? 0 : step(r, 1200, 1800, 100),
      contA: contA, contB: contB, bA: bA, bB: bB, ndf: ndf, ndL: ndL };
  }
  function endTxt(name, cont, b) {
    return cont ? bi(name + ": a beam " + b + " mm wide, monolithic and continuous", name + ": beam selebar " + b + " mm, monolitik dan continuous")
                : bi(name + ": a brick wall " + b + " mm wide, simply supported", name + ": dinding bata selebar " + b + " mm, simply supported");
  }
  function stairTxt(c) {
    var kind = c.type === "straight" ? bi("A straight flight", "Satu flight lurus") : c.type === "landTop" ? bi("A flight with a landing at the top", "Satu flight dengan landing di atas") : bi("A flight with a landing at the bottom", "Satu flight dengan landing di bawah");
    var land = c.type === "straight" ? "" : " " + bi("Landing " + num(c.landing) + " mm clear, at the " + (c.type === "landTop" ? "top" : "bottom") + ".", "Landing " + num(c.landing) + " mm bersih, di " + (c.type === "landTop" ? "atas" : "bawah") + ".");
    return kind + ": " + bi(num(c.nG) + " goings of " + num(c.G) + " mm = " + num(c.flight) + " mm on plan.", num(c.nG) + " going sepanjang " + num(c.G) + " mm = " + num(c.flight) + " mm on plan.") + land + " " +
      endTxt("A", c.contA, c.bA) + "; " + endTxt("B", c.contB, c.bB) + ". " +
      bi("Design loads: n<sub>d</sub> = " + num(fmt(c.ndf, 2)) + " kN/m² on the flight" + (c.type === "straight" ? "" : " and " + num(fmt(c.ndL, 2)) + " kN/m² on the landing") + ", per m² on plan.",
         "Design load: n<sub>d</sub> = " + num(fmt(c.ndf, 2)) + " kN/m² pada flight" + (c.type === "straight" ? "" : " dan " + num(fmt(c.ndL, 2)) + " kN/m² pada landing") + ", per m² on plan.");
  }
  function segLines(c, a) {
    var sg = segments(c), out = [];
    sg.forEach(function (s, i) {
      var half = (i === 0 ? c.bA : c.bB) / 2, clear = s.kind === "flight" ? c.flight : c.landing;
      if (c.type === "straight") out.push("L = " + c.bA + "/2 + " + c.flight + " + " + c.bB + "/2 = " + fmt(s.l, 0) + " mm");
      else out.push("L<sub>" + (i + 1) + "</sub> = " + s.kind + " " + clear + " + " + (half * 2) + "/2 = " + fmt(s.l, 0) + " mm");
    });
    if (sg.length > 1) out.push("L = " + sg.map(function (s) { return fmt(s.l, 0); }).join(" + ") + " = " + fmt(a.L * 1000, 0) + " mm");
    return out;
  }
  function endsSay(a) {
    return a.nc === 2 ? bi("both ends continuous", "kedua-dua hujung continuous") : a.nc === 1 ? bi("one end continuous", "satu hujung continuous") : bi("both ends simply supported", "kedua-dua hujung simply supported");
  }

  /* ---------- B1 risers and flights ---------- */
  EX.define("b1", {
    gen: function (r) { var H = step(r, 2800, 4200, 50), G = step(r, 255, 300, 5), n = Math.ceil(H / 180 - 1e-9); return { H: H, G: G, n: n, R: H / n, fl: Math.ceil(n / 16) }; },
    text: function (P) { return bi("A stair in a building other than residential climbs a storey of H = " + num(P.H) + " mm, with a going G = " + num(P.G) + " mm. Find the least number of risers n, the rise R (1 decimal), the number of flights, and 2R + G.",
                                   "Satu tangga dalam bangunan selain kediaman mendaki satu tingkat H = " + num(P.H) + " mm, dengan going G = " + num(P.G) + " mm. Cari bilangan riser paling sedikit n, rise R (1 tempat perpuluhan), bilangan flight, dan 2R + G."); },
    fields: [{ id: "n", label: ["n", "n"], fn: function (P) { return P.n; }, atol: 0, rtol: 0 },
             { id: "R", label: ["R", "R"], unit: "mm", fn: function (P) { return P.R; }, atol: 0.15, rtol: 0 },
             { id: "fl", label: ["Flights", "Flight"], fn: function (P) { return P.fl; }, atol: 0, rtol: 0 },
             { id: "c", label: ["2R + G", "2R + G"], unit: "mm", fn: function (P) { return 2 * P.R + P.G; }, atol: 0.5, rtol: 0 }],
    hints: [function () { return bi("By-law 106: R ≤ 180 mm, so n ≥ H/180, rounded <b>up</b> to a whole number. Rounding down gives an illegal rise.", "By-law 106: R ≤ 180 mm, jadi n ≥ H/180, dibundarkan <b>ke atas</b> kepada nombor bulat. Membundarkan ke bawah memberi rise yang tidak sah."); },
            function (P) { return bi("H/180 = " + fmt(P.H / 180, 2) + ". Then R = H/n. By-law 108 allows at most 16 risers in one flight.", "H/180 = " + fmt(P.H / 180, 2) + ". Kemudian R = H/n. By-law 108 membenarkan paling banyak 16 riser dalam satu flight."); },
            function (P) { return bi("n = " + P.n + (P.n > 16 ? " > 16, so the stair needs a landing between flights." : " ≤ 16, so one flight is enough.") + " Comfort: 2R + G should be 550 to 700 mm.", "n = " + P.n + (P.n > 16 ? " > 16, jadi tangga memerlukan landing di antara flight." : " ≤ 16, jadi satu flight sudah cukup.") + " Keselesaan: 2R + G sepatutnya 550 hingga 700 mm."); }],
    solution: function (P) { var c = 2 * P.R + P.G;
      return sol(["n ≥ " + P.H + "/180 = " + fmt(P.H / 180, 2) + " → n = " + P.n,
        "R = " + P.H + "/" + P.n + " = " + fmt(P.R, 1) + " mm ≤ 180 ✓",
        P.n > 16 ? bi(P.n + " > 16 → " + P.fl + " flights (" + Math.ceil(P.n / 2) + " + " + Math.floor(P.n / 2) + " risers) with a landing", P.n + " > 16 → " + P.fl + " flight (" + Math.ceil(P.n / 2) + " + " + Math.floor(P.n / 2) + " riser) dengan landing") : bi(P.n + " ≤ 16 → one flight", P.n + " ≤ 16 → satu flight"),
        "2R + G = 2 × " + fmt(P.R, 1) + " + " + P.G + " = " + fmt(c, 1) + " mm " + (c >= 550 && c <= 700 ? bi("(comfortable)", "(selesa)") : bi("(outside 550 to 700: uncomfortable, though legal)", "(di luar 550 hingga 700: tidak selesa, walaupun sah)"))]); }
  });

  /* ---------- B2 average thickness and design loads ---------- */
  function b2calc(P) { var s = Math.sqrt(P.R * P.R + P.G * P.G), y = P.h * s / P.G, t = y + P.R / 2;
    var gkf = 25 * t / 1000 + P.fin, gkL = 25 * P.hL / 1000 + P.fin;
    return { s: s, y: y, t: t, gkf: gkf, gkL: gkL, ndf: 1.35 * gkf + 1.5 * P.qk, ndL: 1.35 * gkL + 1.5 * P.qk }; }
  EX.define("b2", {
    gen: function (r) { var h = step(r, 125, 200, 5), hL = pick(r, [h, h, h - 25, h + 25]); hL = Math.max(125, Math.min(200, hL));
      return { R: step(r, 150, 180, 5), G: step(r, 255, 300, 5), h: h, hL: hL, fin: pick(r, [1.0, 1.2, 1.5]), qk: pick(r, [3.0, 4.0, 5.0]) }; },
    text: function (P) { return bi("A flight has R = " + num(P.R) + " mm, G = " + num(P.G) + " mm and a waist h = " + num(P.h) + " mm; its landing is " + num(P.hL) + " mm thick. Finishes " + num(fmt(P.fin, 1)) + " kN/m² and imposed " + num(fmt(P.qk, 1)) + " kN/m², both on plan; concrete 25 kN/m³. Find y and t (1 decimal), and n<sub>d</sub> for the flight and for the landing (2 decimals).",
                                   "Satu flight mempunyai R = " + num(P.R) + " mm, G = " + num(P.G) + " mm dan waist h = " + num(P.h) + " mm; landing-nya setebal " + num(P.hL) + " mm. Finishes " + num(fmt(P.fin, 1)) + " kN/m² dan imposed " + num(fmt(P.qk, 1)) + " kN/m², kedua-duanya on plan; konkrit 25 kN/m³. Cari y dan t (1 tempat perpuluhan), dan n<sub>d</sub> bagi flight dan bagi landing (2 tempat perpuluhan)."); },
    fields: [{ id: "y", label: ["y", "y"], unit: "mm", fn: function (P) { return b2calc(P).y; }, atol: 0.15, rtol: 0 },
             { id: "t", label: ["t", "t"], unit: "mm", fn: function (P) { return b2calc(P).t; }, atol: 0.2, rtol: 0 },
             { id: "nf", label: ["n<sub>d</sub> flight", "n<sub>d</sub> flight"], unit: "kN/m²", fn: function (P) { return b2calc(P).ndf; }, atol: 0.015, rtol: 0 },
             { id: "nl", label: ["n<sub>d</sub> landing", "n<sub>d</sub> landing"], unit: "kN/m²", fn: function (P) { return b2calc(P).ndL; }, atol: 0.015, rtol: 0 }],
    hints: [function () { return bi("(1.1) y = h√(R² + G²)/G and (1.2) t = y + R/2. Keep at least 3 decimals in g<sub>k</sub>.", "(1.1) y = h√(R² + G²)/G dan (1.2) t = y + R/2. Simpan sekurang-kurangnya 3 tempat perpuluhan dalam g<sub>k</sub>."); },
            function (P) { var c = b2calc(P); return bi("√(R² + G²) = " + fmt(c.s, 1) + " mm. Flight self-weight = 25t with t in m; landing self-weight = 25 × " + fmt(P.hL / 1000, 3) + ".", "√(R² + G²) = " + fmt(c.s, 1) + " mm. Self-weight flight = 25t dengan t dalam m; self-weight landing = 25 × " + fmt(P.hL / 1000, 3) + "."); },
            function (P) { var c = b2calc(P); return bi("g<sub>k</sub> = self-weight + " + fmt(P.fin, 2) + "; n<sub>d</sub> = 1.35g<sub>k</sub> + 1.5 × " + fmt(P.qk, 1) + ". Check: the flight’s n<sub>d</sub> must exceed the landing’s n<sub>d</sub>" + (P.hL > P.h ? " (here the landing is thicker than the waist, so look at the ratio closely)" : "") + ".", "g<sub>k</sub> = self-weight + " + fmt(P.fin, 2) + "; n<sub>d</sub> = 1.35g<sub>k</sub> + 1.5 × " + fmt(P.qk, 1) + ". Semak: n<sub>d</sub> flight mesti melebihi n<sub>d</sub> landing" + (P.hL > P.h ? " (di sini landing lebih tebal daripada waist, jadi teliti nisbahnya)" : "") + "."); }],
    solution: function (P) { var c = b2calc(P);
      return sol(["y = " + P.h + " × √(" + P.R + "² + " + P.G + "²)/" + P.G + " = " + P.h + " × " + fmt(c.s, 1) + "/" + P.G + " = " + fmt(c.y, 1) + " mm",
        "t = " + fmt(c.y, 1) + " + " + fmt(P.R / 2, 1) + " = " + fmt(c.t, 1) + " mm",
        bi("Flight", "Flight") + ": g<sub>k</sub> = 25 × " + fmt(c.t / 1000, 4) + " + " + fmt(P.fin, 2) + " = " + fmt(c.gkf, 3) + "; n<sub>d</sub> = 1.35 × " + fmt(c.gkf, 3) + " + 1.5 × " + fmt(P.qk, 1) + " = " + fmt(c.ndf, 2) + " kN/m²",
        "Landing: g<sub>k</sub> = 25 × " + fmt(P.hL / 1000, 3) + " + " + fmt(P.fin, 2) + " = " + fmt(c.gkL, 3) + "; n<sub>d</sub> = 1.35 × " + fmt(c.gkL, 3) + " + 1.5 × " + fmt(P.qk, 1) + " = " + fmt(c.ndL, 2) + " kN/m²",
        bi("Ratio ", "Nisbah ") + fmt(c.ndf, 2) + "/" + fmt(c.ndL, 2) + " = " + fmt(c.ndf / c.ndL, 2) + (c.ndf > c.ndL ? " > 1 ✓" : " ≤ 1")]); }
  });

  /* ---------- B3 span, total load and moment ---------- */
  EX.define("b3", {
    gen: function (r) { return genStair(r, ["straight", "landTop", "landBottom"]); },
    text: function (P) { return stairTxt(P) + " " + bi("Find the span L, the total load F per metre width (2 decimals) and the design moment M by the course method.", "Cari span L, total load F per meter lebar (2 tempat perpuluhan) dan design moment M mengikut kaedah kursus."); },
    fields: [{ id: "L", label: ["L", "L"], unit: "mm", fn: function (P) { return analyse(P).L * 1000; }, atol: 0.5, rtol: 0 },
             { id: "F", label: ["F", "F"], unit: "kN", fn: function (P) { return analyse(P).F; }, atol: 0.03, rtol: 0 },
             { id: "M", label: ["M", "M"], unit: "kNm", fn: function (P) { return analyse(P).M; }, atol: 0.06, rtol: 0 }],
    hints: [function () { return bi("(1.5): L is on plan, centre to centre of the supports: each flight or landing plus half the width of the support at its end.", "(1.5): L diukur on plan, tengah ke tengah support: setiap flight atau landing tambah separuh lebar support di hujungnya."); },
            function (P) { var a = analyse(P); return bi("Segments: " + a.parts.map(function (q) { return q.kind + " " + fmt(q.l, 0) + " mm"; }).join(", ") + ". F = Σ n<sub>d</sub> × l, with l in m.", "Segmen: " + a.parts.map(function (q) { return q.kind + " " + fmt(q.l, 0) + " mm"; }).join(", ") + ". F = Σ n<sub>d</sub> × l, dengan l dalam m."); },
            function (P) { var a = analyse(P); return bi("Here " + "<b>" + (a.nc ? "at least one end is continuous, so M = FL/10" : "both ends are simply supported, so M = FL/8") + "</b>.", "Di sini " + "<b>" + (a.nc ? "sekurang-kurangnya satu hujung continuous, jadi M = FL/10" : "kedua-dua hujung simply supported, jadi M = FL/8") + "</b>."); }],
    solution: function (P) { var a = analyse(P);
      return sol(segLines(P, a).concat([
        "F = " + a.parts.map(function (q) { return fmt(q.n, 2) + " × " + fmt(q.lm, 3); }).join(" + ") + " = " + fmt(a.F, 2) + " kN",
        endsSay(a) + " → M = FL/" + a.coef + " = " + fmt(a.F, 2) + " × " + fmt(a.L, 3) + "/" + a.coef + " = " + fmt(a.M, 2) + " kNm"])); }
  });

  /* ---------- B4 reactions ---------- */
  EX.define("b4", {
    gen: function (r) { return genStair(r, ["landTop", "landBottom"]); },
    text: function (P) { return stairTxt(P) + " " + bi("Find the reactions V<sub>A</sub> and V<sub>B</sub> per metre width (2 decimals), including the hogging moment at any continuous end.", "Cari reaction V<sub>A</sub> dan V<sub>B</sub> per meter lebar (2 tempat perpuluhan), termasuk hogging moment di mana-mana hujung continuous."); },
    fields: [{ id: "VA", label: ["V<sub>A</sub>", "V<sub>A</sub>"], unit: "kN", fn: function (P) { return analyse(P).VA; }, atol: 0.05, rtol: 0 },
             { id: "VB", label: ["V<sub>B</sub>", "V<sub>B</sub>"], unit: "kN", fn: function (P) { return analyse(P).VB; }, atol: 0.05, rtol: 0 }],
    hints: [function () { return bi("First L, F and M as in B3. Then (1.7): V<sub>A</sub> = ΣF<sub>i</sub>(L − x<sub>i</sub>)/L + (M<sub>A</sub> − M<sub>B</sub>)/L, with x<sub>i</sub> the centroid of segment i measured from A.", "Mula-mula L, F dan M seperti B3. Kemudian (1.7): V<sub>A</sub> = ΣF<sub>i</sub>(L − x<sub>i</sub>)/L + (M<sub>A</sub> − M<sub>B</sub>)/L, dengan x<sub>i</sub> centroid segmen i diukur dari A."); },
            function (P) { var a = analyse(P); return bi("L = " + fmt(a.L, 3) + " m, F = " + fmt(a.F, 2) + " kN, M = FL/" + a.coef + " = " + fmt(a.M, 2) + " kNm. Centroids from A: " + a.parts.map(function (q) { return fmt(q.xc, 4) + " m"; }).join(" and ") + ".", "L = " + fmt(a.L, 3) + " m, F = " + fmt(a.F, 2) + " kN, M = FL/" + a.coef + " = " + fmt(a.M, 2) + " kNm. Centroid dari A: " + a.parts.map(function (q) { return fmt(q.xc, 4) + " m"; }).join(" dan ") + "."); },
            function (P) { var a = analyse(P); return bi("M<sub>A</sub> = " + (P.contA ? "M" : "0") + " and M<sub>B</sub> = " + (P.contB ? "M" : "0") + " (a hogging moment acts only at a continuous end). Then V<sub>B</sub> = F − V<sub>A</sub>.", "M<sub>A</sub> = " + (P.contA ? "M" : "0") + " dan M<sub>B</sub> = " + (P.contB ? "M" : "0") + " (hogging moment hanya bertindak di hujung continuous). Kemudian V<sub>B</sub> = F − V<sub>A</sub>."); }],
    solution: function (P) { var a = analyse(P);
      return sol(segLines(P, a).concat([
        "F = " + a.parts.map(function (q) { return fmt(q.n, 2) + " × " + fmt(q.lm, 3) + " = " + fmt(q.Fi, 3); }).join("; ") + "; F = " + fmt(a.F, 2) + " kN",
        "M = FL/" + a.coef + " = " + fmt(a.M, 2) + " kNm; M<sub>A</sub> = " + fmt(a.MA, 2) + ", M<sub>B</sub> = " + fmt(a.MB, 2),
        "ΣF<sub>i</sub>(L − x<sub>i</sub>) = " + a.parts.map(function (q) { return fmt(q.Fi, 3) + " × " + fmt(a.L - q.xc, 4); }).join(" + ") + " = " + fmt(a.mB, 2) + " kNm",
        "V<sub>A</sub> = (" + fmt(a.mB, 2) + (a.MA - a.MB >= 0 ? " + " : " − ") + fmt(Math.abs(a.MA - a.MB), 2) + ")/" + fmt(a.L, 3) + " = " + fmt(a.VA, 2) + " kN",
        "V<sub>B</sub> = " + fmt(a.F, 2) + " − " + fmt(a.VA, 2) + " = " + fmt(a.VB, 2) + " kN"])); }
  });

  /* ---------- B5 flexure ---------- */
  function b5calc(P) { var d = P.h - 25 - P.phi / 2, K = P.M * 1e6 / (1000 * d * d * P.fck), zr = d * (0.5 + Math.sqrt(0.25 - K / 1.134)), z = Math.min(zr, 0.95 * d);
    return { d: d, K: K, zr: zr, z: z, cap: zr > 0.95 * d, As: P.M * 1e6 / (0.87 * 500 * z) }; }
  EX.define("b5", {
    gen: function (r) { var h = step(r, 125, 200, 5), phi = pick(r, [10, 10, 12]), fck = pick(r, [25, 30]), d = h - 25 - phi / 2;
      var M = r2((0.03 + 0.06 * r()) * 1000 * d * d * fck / 1e6); return { h: h, phi: phi, fck: fck, M: M }; },
    text: function (P) { return bi("A waist h = " + num(P.h) + " mm carries M = " + num(fmt(P.M, 2)) + " kNm per metre width. C" + P.fck + "/" + (P.fck === 25 ? 30 : 37) + ", f<sub>yk</sub> = 500 N/mm², cover 25 mm, H" + P.phi + " main bars. Find d, K (3 decimals), z (1 decimal) and A<sub>s,req</sub> per metre.",
                                   "Waist h = " + num(P.h) + " mm membawa M = " + num(fmt(P.M, 2)) + " kNm per meter lebar. C" + P.fck + "/" + (P.fck === 25 ? 30 : 37) + ", f<sub>yk</sub> = 500 N/mm², cover 25 mm, main bar H" + P.phi + ". Cari d, K (3 tempat perpuluhan), z (1 tempat perpuluhan) dan A<sub>s,req</sub> per meter."); },
    fields: [{ id: "d", label: ["d", "d"], unit: "mm", fn: function (P) { return b5calc(P).d; }, atol: 0.01, rtol: 0 },
             { id: "K", label: ["K", "K"], fn: function (P) { return b5calc(P).K; }, atol: 0.0015, rtol: 0 },
             { id: "z", label: ["z", "z"], unit: "mm", fn: function (P) { return b5calc(P).z; }, atol: 0.3, rtol: 0 },
             { id: "As", label: ["A<sub>s,req</sub>", "A<sub>s,req</sub>"], unit: "mm²/m", fn: function (P) { return b5calc(P).As; }, atol: 1, rtol: 0.006 }],
    hints: [function () { return bi("d = h − c − φ/2 for the main bars, then (1.8): K = M/(bd²f<sub>ck</sub>) with b = 1000 mm and M in N mm.", "d = h − c − φ/2 bagi main bar, kemudian (1.8): K = M/(bd²f<sub>ck</sub>) dengan b = 1000 mm dan M dalam N mm."); },
            function (P) { var c = b5calc(P); return bi("d = " + fmt(c.d, 0) + " mm. z = d[0.5 + √(0.25 − K/1.134)], but never more than 0.95d.", "d = " + fmt(c.d, 0) + " mm. z = d[0.5 + √(0.25 − K/1.134)], tetapi tidak melebihi 0.95d."); },
            function (P) { var c = b5calc(P); return bi("K = " + fmt(c.K, 3) + " &lt; 0.167. The formula gives " + fmt(c.zr / c.d, 4) + "d" + (c.cap ? ", more than 0.95d, so z = 0.95d." : ".") + " Then (1.9): A<sub>s</sub> = M/(0.87f<sub>yk</sub>z).", "K = " + fmt(c.K, 3) + " &lt; 0.167. Formula memberi " + fmt(c.zr / c.d, 4) + "d" + (c.cap ? ", lebih daripada 0.95d, jadi z = 0.95d." : ".") + " Kemudian (1.9): A<sub>s</sub> = M/(0.87f<sub>yk</sub>z)."); }],
    solution: function (P) { var c = b5calc(P);
      return sol(["d = " + P.h + " − 25 − " + P.phi + "/2 = " + fmt(c.d, 0) + " mm",
        "K = " + fmt(P.M, 2) + " × 10⁶/(1000 × " + fmt(c.d, 0) + "² × " + P.fck + ") = " + fmt(c.K, 3) + " &lt; K<sub>bal</sub> = 0.167",
        "z = d[0.5 + √(0.25 − " + fmt(c.K, 3) + "/1.134)] = " + fmt(c.zr / c.d, 4) + "d" + (c.cap ? " &gt; 0.95d → z = 0.95 × " + fmt(c.d, 0) : " = " + fmt(c.zr / c.d, 4) + " × " + fmt(c.d, 0)) + " = " + fmt(c.z, 1) + " mm",
        "A<sub>s</sub> = " + fmt(P.M, 2) + " × 10⁶/(0.87 × 500 × " + fmt(c.z, 1) + ") = " + fmt(c.As, 0) + " mm²/m"]); }
  });

  /* ---------- B6 deflection ---------- */
  var BARS = [100, 125, 150, 175, 200, 225, 250];
  function b6calc(P) { var d = P.h - 30, rho = P.Asr / (1000 * d), r0 = Math.sqrt(P.fck) * 1e-3, sf = Math.sqrt(P.fck), q = r0 / rho;
    var K = [1.0, 1.3, 1.5][P.nc], t1 = 1.5 * sf * q, t2 = q > 1 ? 3.2 * sf * Math.pow(q - 1, 1.5) : 0, basic = K * (11 + t1 + t2);
    var ratio = Math.min(P.Asp / P.Asr, 1.5); return { d: d, rho: rho, r0: r0, q: q, K: K, t1: t1, t2: t2, basic: basic, ratio: ratio, allow: basic * ratio, actual: P.L / d }; }
  EX.define("b6", {
    gen: function (r) { var L = step(r, 2800, 4600, 25), h = Math.max(125, Math.ceil(L / 27 / 5) * 5), fck = pick(r, [25, 30]), nc = pick(r, [0, 1, 1, 2]), d = h - 30;
      var Asr = Math.round((0.0025 + 0.002 * r()) * 1000 * d), lim = Math.min(2 * h, 250), s = 100;
      BARS.forEach(function (b) { if (b <= lim && 78.54 * 1000 / b >= Asr) s = b; });
      return { L: L, h: h, fck: fck, nc: nc, Asr: Asr, s: s, Asp: Math.round(78.54 * 1000 / s) }; },
    text: function (P) { var ends = P.nc === 2 ? bi("both ends continuous", "kedua-dua hujung continuous") : P.nc === 1 ? bi("end A continuous, end B simply supported", "hujung A continuous, hujung B simply supported") : bi("both ends simply supported", "kedua-dua hujung simply supported");
      return bi("A stair spans L = " + num(P.L) + " mm on plan with " , "Satu tangga span L = " + num(P.L) + " mm on plan dengan ") + ends + ". " +
        bi("Waist h = " + num(P.h) + " mm, cover 25 mm, H10 main bars (d = h − 30). C" + P.fck + "/" + (P.fck === 25 ? 30 : 37) + ". A<sub>s,req</sub> = " + num(P.Asr) + " mm²/m; provided H10-" + P.s + " (" + num(P.Asp) + " mm²/m). Find the structural factor K, (l/d)<sub>allow</sub> and (l/d)<sub>actual</sub> (1 decimal).",
           "Waist h = " + num(P.h) + " mm, cover 25 mm, main bar H10 (d = h − 30). C" + P.fck + "/" + (P.fck === 25 ? 30 : 37) + ". A<sub>s,req</sub> = " + num(P.Asr) + " mm²/m; disediakan H10-" + P.s + " (" + num(P.Asp) + " mm²/m). Cari structural factor K, (l/d)<sub>allow</sub> dan (l/d)<sub>actual</sub> (1 tempat perpuluhan)."); },
    fields: [{ id: "K", label: ["K (Table 7.4N)", "K (Table 7.4N)"], fn: function (P) { return b6calc(P).K; }, atol: 0.001, rtol: 0 },
             { id: "al", label: ["(l/d)<sub>allow</sub>", "(l/d)<sub>allow</sub>"], fn: function (P) { return b6calc(P).allow; }, atol: 0.25, rtol: 0 },
             { id: "ac", label: ["(l/d)<sub>actual</sub>", "(l/d)<sub>actual</sub>"], fn: function (P) { return b6calc(P).actual; }, atol: 0.06, rtol: 0 }],
    hints: [function () { return bi("K counts the continuous ends: 1.5 for two, 1.3 for one (an end span), 1.0 for none. It is not the K of flexure.", "K mengira hujung continuous: 1.5 bagi dua, 1.3 bagi satu (end span), 1.0 tanpa hujung continuous. Ia bukan K bagi flexure."); },
            function (P) { var c = b6calc(P); return bi("ρ = A<sub>s,req</sub>/bd = " + fmt(c.rho, 5) + " and ρ<sub>0</sub> = √f<sub>ck</sub> × 10⁻³ = " + fmt(c.r0, 5) + ": ρ ≤ ρ<sub>0</sub>, so use (1.11), EC2 Eq. 7.16a.", "ρ = A<sub>s,req</sub>/bd = " + fmt(c.rho, 5) + " dan ρ<sub>0</sub> = √f<sub>ck</sub> × 10⁻³ = " + fmt(c.r0, 5) + ": ρ ≤ ρ<sub>0</sub>, jadi guna (1.11), EC2 Eq. 7.16a."); },
            function (P) { var c = b6calc(P); return bi("Multiply the basic value by A<sub>s,prov</sub>/A<sub>s,req</sub> = " + fmt(P.Asp / P.Asr, 3) + (P.Asp / P.Asr > 1.5 ? ", capped at 1.5" : "") + ". (l/d)<sub>actual</sub> = L/d.", "Darab nilai asas dengan A<sub>s,prov</sub>/A<sub>s,req</sub> = " + fmt(P.Asp / P.Asr, 3) + (P.Asp / P.Asr > 1.5 ? ", dihadkan kepada 1.5" : "") + ". (l/d)<sub>actual</sub> = L/d."); }],
    solution: function (P) { var c = b6calc(P);
      return sol([bi(["Both ends simple", "One end continuous (end span)", "Both ends continuous (interior span)"][P.nc], ["Kedua-dua hujung simple", "Satu hujung continuous (end span)", "Kedua-dua hujung continuous (interior span)"][P.nc]) + " → K = " + fmt(c.K, 1),
        "d = " + P.h + " − 30 = " + fmt(c.d, 0) + " mm; ρ = " + P.Asr + "/(1000 × " + fmt(c.d, 0) + ") = " + fmt(c.rho, 5) + " ≤ ρ<sub>0</sub> = " + fmt(c.r0, 5),
        "(l/d)<sub>basic</sub> = " + fmt(c.K, 1) + " × (11 + " + fmt(c.t1, 2) + " + " + fmt(c.t2, 2) + ") = " + fmt(c.basic, 1),
        "(l/d)<sub>allow</sub> = " + fmt(c.basic, 1) + " × " + fmt(c.ratio, 3) + " = " + fmt(c.allow, 1),
        "(l/d)<sub>actual</sub> = " + P.L + "/" + fmt(c.d, 0) + " = " + fmt(c.actual, 1) + (c.actual <= c.allow ? " ≤ " + fmt(c.allow, 1) + bi(": deflection OK", ": deflection OK") : " &gt; " + fmt(c.allow, 1) + bi(": increase h or the steel", ": tambah h atau steel"))]); }
  });

  EX.ready();
})();
