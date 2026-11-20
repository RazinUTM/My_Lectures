/* SEAA 4333 Unit 13 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's retaining-wall model), per metre of wall:
   K_a = (1 - sin phi)/(1 + sin phi); p = K_a (gamma z + w); P_s = K_a gamma H^2/2 at H/3; P_q = K_a w H at H/2,
   with H from the backfill surface to the underside of the base; moments about the toe A;
   EQU: 1.1 M_oG + 1.5 M_oQ <= 0.9 M_rG; sliding, combination 1: 1.35 H_kG + 1.5 H_kQ <= mu V_kG;
   EC7 DA1 Combination 2: phi_d = atan(tan phi/1.25), thrusts x K_a,d/K_a, (H_kG + 1.3 H_kQ) K_a,d/K_a <= (mu/1.25) V_kG;
   the surcharge on the heel is left out of every resistance; bearing with service loads: x = dM/N, e = B/2 - x,
   q = N/B +- 6Ne/B^2 inside the middle third, q_max = 2N/(3x) outside it. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function rad(a) { return a * Math.PI / 180; }
  function Ka(phi) { var s = Math.sin(rad(phi)); return (1 - s) / (1 + s); }
  function r1(v) { return Math.round(v * 10) / 10; }
  /* a simple wall (uniform stem) that gives realistic sums for B4 to B6 */
  function wall(r) {
    var W = {};
    W.h3 = step(r, 3.0, 5.5, 0.5); W.h = pick(r, [0.3, 0.4, 0.5]); W.t = pick(r, [0.3, 0.35, 0.4, 0.45]);
    W.H = +(W.h3 + W.h).toFixed(2); W.gs = pick(r, [17, 18, 19, 20]); W.phi = pick(r, [28, 30, 32, 33, 35, 36]); W.w = pick(r, [5, 10, 15]);
    W.a1 = step(r, 0.4, 1.0, 0.1); W.a2 = +(Math.round((0.36 + 0.12 * r()) * W.H * 10) / 10).toFixed(1); W.B = +(W.a1 + W.t + W.a2).toFixed(2);
    W.Ka = Ka(W.phi); W.Ps = 0.5 * W.Ka * W.gs * W.H * W.H; W.Pq = W.Ka * W.w * W.H;
    W.MoG = W.Ps * W.H / 3; W.MoQ = W.Pq * W.H / 2;
    W.Ws = W.t * W.h3 * 25; W.Wb = W.h * W.B * 25; W.W4 = W.gs * W.h3 * W.a2; W.Wq = W.w * W.a2;
    W.VG = W.Ws + W.Wb + W.W4; W.MrG = W.Ws * (W.a1 + W.t / 2) + W.Wb * W.B / 2 + W.W4 * (W.a1 + W.t + W.a2 / 2);
    W.MrQ = W.Wq * (W.a1 + W.t + W.a2 / 2);
    return W;
  }

  /* ---------- B1 the active pressure ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.phi = pick(r, [28, 30, 32, 33, 35, 36, 38]); P.gs = pick(r, [17, 18, 19, 20]); P.w = pick(r, [5, 10, 15, 20]);
      P.h3 = step(r, 3.0, 6.0, 0.5); P.h = pick(r, [0.3, 0.4, 0.5, 0.6]); P.H = +(P.h3 + P.h).toFixed(2);
      P.Ka = Ka(P.phi); P.p0 = P.Ka * P.w; P.pH = P.Ka * (P.gs * P.H + P.w);
      return P;
    },
    text: function (P) {
      return bi("A cantilever wall retains drained sand with γ = " + num(P.gs) + " kN/m³ and φ = " + num(P.phi) + "°; the level backfill carries a surcharge of " + num(P.w) + " kN/m². The stem is " + num(fmt(P.h3, 1)) + " m high and the base " + num(fmt(P.h, 1)) + " m thick. For the stability checks, find K<sub>a</sub> and the active pressure at the backfill surface and at the underside of the base.",
                "Satu cantilever wall menahan pasir bersaliran dengan γ = " + num(P.gs) + " kN/m³ dan φ = " + num(P.phi) + "°; backfill yang rata membawa surcharge " + num(P.w) + " kN/m². Stem setinggi " + num(fmt(P.h3, 1)) + " m dan base setebal " + num(fmt(P.h, 1)) + " m. Bagi semakan kestabilan, cari K<sub>a</sub> dan active pressure di permukaan backfill dan di bahagian bawah base.");
    },
    fields: [{ id: "ka", label: ["K<sub>a</sub>", "K<sub>a</sub>"], unit: "", fn: function (P) { return P.Ka; }, rtol: 0.01, atol: 0.002 },
             { id: "p0", label: ["p (surface)", "p (permukaan)"], unit: "kN/m²", fn: function (P) { return P.p0; }, rtol: 0.015, atol: 0.03 },
             { id: "ph", label: ["p (underside)", "p (bahagian bawah)"], unit: "kN/m²", fn: function (P) { return P.pH; }, rtol: 0.01 }],
    hints: [function () { return bi("Rankine: K<sub>a</sub> = (1 − sin φ)/(1 + sin φ). Set the calculator to degrees.", "Rankine: K<sub>a</sub> = (1 − sin φ)/(1 + sin φ). Tetapkan kalkulator kepada darjah."); },
            function () { return bi("p = K<sub>a</sub>(γz + w): at the surface z = 0, so only the surcharge acts.", "p = K<sub>a</sub>(γz + w): di permukaan z = 0, jadi hanya surcharge bertindak."); },
            function () { return bi("The depth runs to the underside of the base: H = h<sub>3</sub> + h, not the stem height.", "Kedalaman diukur hingga bahagian bawah base: H = h<sub>3</sub> + h, bukan tinggi stem."); }],
    solution: function (P) {
      return sol(["K<sub>a</sub> = (1 − sin " + P.phi + "°)/(1 + sin " + P.phi + "°) = " + fmt(P.Ka, 4),
        "H = " + fmt(P.h3, 1) + " + " + fmt(P.h, 1) + " = " + fmt(P.H, 1) + " m",
        bi("Surface: p = ", "Permukaan: p = ") + fmt(P.Ka, 4) + " × " + P.w + " = " + fmt(P.p0, 2) + " kN/m²",
        bi("Underside: p = ", "Bahagian bawah: p = ") + fmt(P.Ka, 4) + " × (" + P.gs + " × " + fmt(P.H, 1) + " + " + P.w + ") = " + fmt(P.pH, 2) + " kN/m²",
        bi("A rectangle from the surcharge and a triangle from the soil: the two thrusts are B2 (Notes §2).", "Segi empat tepat daripada surcharge dan segi tiga daripada tanah: dua thrust ialah B2 (Nota §2).")]);
    }
  });

  /* ---------- B2 the two thrusts and the overturning moment ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.phi = pick(r, [28, 30, 32, 33, 35, 36, 38]); P.gs = pick(r, [17, 18, 19, 20]); P.w = pick(r, [5, 10, 15, 20]);
      P.H = step(r, 3.4, 6.6, 0.1); P.Ka = Ka(P.phi);
      P.Ps = 0.5 * P.Ka * P.gs * P.H * P.H; P.Pq = P.Ka * P.w * P.H;
      P.MoG = P.Ps * P.H / 3; P.MoQ = P.Pq * P.H / 2; P.Mod = 1.1 * P.MoG + 1.5 * P.MoQ;
      return P;
    },
    text: function (P) {
      return bi("A wall is " + num(fmt(P.H, 1)) + " m high from the surface of its level backfill to the underside of its base. Backfill: γ = " + num(P.gs) + " kN/m³, φ = " + num(P.phi) + "°; surcharge " + num(P.w) + " kN/m². Per metre of wall, find the thrust of the soil, the thrust of the surcharge and the design overturning moment about the toe for the EQU check.",
                "Satu wall setinggi " + num(fmt(P.H, 1)) + " m dari permukaan backfill yang rata ke bahagian bawah base-nya. Backfill: γ = " + num(P.gs) + " kN/m³, φ = " + num(P.phi) + "°; surcharge " + num(P.w) + " kN/m². Bagi setiap meter wall, cari thrust tanah, thrust surcharge dan design overturning moment pada toe bagi semakan EQU.");
    },
    fields: [{ id: "ps", label: ["P<sub>s</sub>", "P<sub>s</sub>"], unit: "kN", fn: function (P) { return P.Ps; }, rtol: 0.01 },
             { id: "pq", label: ["P<sub>q</sub>", "P<sub>q</sub>"], unit: "kN", fn: function (P) { return P.Pq; }, rtol: 0.01 },
             { id: "mo", label: ["M<sub>o,d</sub>", "M<sub>o,d</sub>"], unit: "kN m", fn: function (P) { return P.Mod; }, rtol: 0.01 }],
    hints: [function () { return bi("Soil: a triangle, P<sub>s</sub> = ½K<sub>a</sub>γH², acting at H/3 above the underside.", "Tanah: segi tiga, P<sub>s</sub> = ½K<sub>a</sub>γH², bertindak pada H/3 di atas bahagian bawah."); },
            function () { return bi("Surcharge: a rectangle, P<sub>q</sub> = K<sub>a</sub>wH, acting at H/2.", "Surcharge: segi empat tepat, P<sub>q</sub> = K<sub>a</sub>wH, bertindak pada H/2."); },
            function () { return bi("EQU: 1.1 on the permanent overturning moment, 1.5 on the variable one.", "EQU: 1.1 pada overturning moment permanent, 1.5 pada yang variable."); }],
    solution: function (P) {
      return sol(["K<sub>a</sub> = (1 − sin " + P.phi + "°)/(1 + sin " + P.phi + "°) = " + fmt(P.Ka, 4),
        "P<sub>s</sub> = ½ × " + fmt(P.Ka, 4) + " × " + P.gs + " × " + fmt(P.H, 1) + "² = " + fmt(P.Ps, 2) + " kN" + bi(" at ", " pada ") + fmt(P.H, 1) + "/3 = " + fmt(P.H / 3, 3) + " m: M<sub>o,G</sub> = " + fmt(P.MoG, 1) + " kN m",
        "P<sub>q</sub> = " + fmt(P.Ka, 4) + " × " + P.w + " × " + fmt(P.H, 1) + " = " + fmt(P.Pq, 2) + " kN" + bi(" at ", " pada ") + fmt(P.H, 1) + "/2 = " + fmt(P.H / 2, 2) + " m: M<sub>o,Q</sub> = " + fmt(P.MoQ, 1) + " kN m",
        "M<sub>o,d</sub> = 1.1 × " + fmt(P.MoG, 1) + " + 1.5 × " + fmt(P.MoQ, 1) + " = " + fmt(P.Mod, 1) + " kN m",
        bi("It is compared with 0.9 times the restoring moment of the weights (B3, B4).", "Ia dibandingkan dengan 0.9 kali restoring moment berat (B3, B4).")]);
    }
  });

  /* ---------- B3 the weights and the restoring moment ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.h3 = step(r, 3.0, 5.5, 0.5); P.h = pick(r, [0.3, 0.4, 0.5]); P.t = pick(r, [0.3, 0.35, 0.4, 0.45]);
      P.a1 = step(r, 0.5, 1.0, 0.1); P.a2 = step(r, 1.6, 3.0, 0.1); P.gs = pick(r, [17, 18, 19, 20]); P.B = +(P.a1 + P.t + P.a2).toFixed(2);
      P.Ws = P.t * P.h3 * 25; P.xs = P.a1 + P.t / 2; P.Wb = P.h * P.B * 25; P.xb = P.B / 2; P.W4 = P.gs * P.h3 * P.a2; P.x4 = P.a1 + P.t + P.a2 / 2;
      P.VG = P.Ws + P.Wb + P.W4; P.MrG = P.Ws * P.xs + P.Wb * P.xb + P.W4 * P.x4;
      return P;
    },
    text: function (P) {
      return bi("A cantilever wall has a stem " + num(fmt(P.h3, 1)) + " m high and " + num(fmt(P.t * 1000, 0)) + " mm thick throughout, on a base " + num(fmt(P.h * 1000, 0)) + " mm thick with a toe of " + num(fmt(P.a1, 1)) + " m and a heel of " + num(fmt(P.a2, 1)) + " m. The level backfill has γ = " + num(P.gs) + " kN/m³; concrete 25 kN/m³. Per metre of wall, find the weight of the soil on the heel, the total permanent vertical load and its restoring moment about the toe.",
                "Satu cantilever wall mempunyai stem setinggi " + num(fmt(P.h3, 1)) + " m dan setebal " + num(fmt(P.t * 1000, 0)) + " mm sepanjangnya, di atas base setebal " + num(fmt(P.h * 1000, 0)) + " mm dengan toe " + num(fmt(P.a1, 1)) + " m dan heel " + num(fmt(P.a2, 1)) + " m. Backfill yang rata mempunyai γ = " + num(P.gs) + " kN/m³; konkrit 25 kN/m³. Bagi setiap meter wall, cari berat tanah di atas heel, jumlah load menegak permanent dan restoring moment-nya pada toe.");
    },
    fields: [{ id: "w4", label: ["W (soil on heel)", "W (tanah di atas heel)"], unit: "kN", fn: function (P) { return P.W4; }, rtol: 0.005 },
             { id: "vg", label: ["ΣV<sub>k,G</sub>", "ΣV<sub>k,G</sub>"], unit: "kN", fn: function (P) { return P.VG; }, rtol: 0.005 },
             { id: "mr", label: ["ΣM<sub>r,G</sub>", "ΣM<sub>r,G</sub>"], unit: "kN m", fn: function (P) { return P.MrG; }, rtol: 0.01 }],
    hints: [function () { return bi("Three weights: the stem t × h<sub>3</sub> × 25, the base h × B × 25 with B = toe + stem + heel, and the soil γ × h<sub>3</sub> × heel.", "Tiga berat: stem t × h<sub>3</sub> × 25, base h × B × 25 dengan B = toe + stem + heel, dan tanah γ × h<sub>3</sub> × heel."); },
            function () { return bi("Arms from the end of the toe: stem toe + t/2; base B/2; soil toe + t + heel/2.", "Arm dari hujung toe: stem toe + t/2; base B/2; tanah toe + t + heel/2."); },
            function () { return bi("Sum the weights, then sum each weight times its arm. The surcharge on the heel is variable: keep it out of these sums.", "Jumlahkan berat, kemudian jumlahkan setiap berat kali arm-nya. Surcharge di atas heel ialah variable: jangan masukkan dalam jumlah ini."); }],
    solution: function (P) {
      return sol(["B = " + fmt(P.a1, 1) + " + " + fmt(P.t, 2) + " + " + fmt(P.a2, 1) + " = " + fmt(P.B, 2) + " m",
        bi("Stem: ", "Stem: ") + fmt(P.t, 2) + " × " + fmt(P.h3, 1) + " × 25 = " + fmt(P.Ws, 2) + " kN" + bi(" at ", " pada ") + fmt(P.xs, 3) + " m: " + fmt(P.Ws * P.xs, 2) + " kN m",
        bi("Base: ", "Base: ") + fmt(P.h, 1) + " × " + fmt(P.B, 2) + " × 25 = " + fmt(P.Wb, 2) + " kN" + bi(" at ", " pada ") + fmt(P.xb, 3) + " m: " + fmt(P.Wb * P.xb, 2) + " kN m",
        bi("Soil on the heel: ", "Tanah di atas heel: ") + P.gs + " × " + fmt(P.h3, 1) + " × " + fmt(P.a2, 1) + " = " + fmt(P.W4, 1) + " kN" + bi(" at ", " pada ") + fmt(P.x4, 3) + " m: " + fmt(P.W4 * P.x4, 2) + " kN m",
        "ΣV<sub>k,G</sub> = " + fmt(P.VG, 1) + " kN; ΣM<sub>r,G</sub> = " + fmt(P.MrG, 1) + " kN m",
        bi("The soil is " + fmt(100 * P.W4 / P.VG, 0) + " % of the weight: the heel holds the wall (Notes §6).", "Tanah ialah " + fmt(100 * P.W4 / P.VG, 0) + " % daripada berat: heel yang menahan wall (Nota §6).")]);
    }
  });

  /* ---------- B4 overturning and sliding, combination 1 ---------- */
  EX.define("b4", {
    gen: function (r) {
      var W = wall(r), P = {};
      P.VG = r1(W.VG); P.MrG = r1(W.MrG); P.VQ = r1(W.Wq); P.MrQ = r1(W.MrQ); P.HG = r1(W.Ps); P.MoG = r1(W.MoG); P.HQ = r1(W.Pq); P.MoQ = r1(W.MoQ);
      P.mu = pick(r, [0.45, 0.5, 0.55, 0.6]);
      P.Mod = 1.1 * P.MoG + 1.5 * P.MoQ; P.Mrd = 0.9 * P.MrG; P.Hd = 1.35 * P.HG + 1.5 * P.HQ; P.Rd = P.mu * P.VG;
      return P;
    },
    text: function (P) {
      return bi("The table of loads of a cantilever wall gives, per metre and with characteristic values: weights ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN with a restoring moment of " + num(fmt(P.MrG, 1)) + " kN m about the toe; surcharge on the heel " + num(fmt(P.VQ, 1)) + " kN with " + num(fmt(P.MrQ, 1)) + " kN m; soil thrust " + num(fmt(P.HG, 1)) + " kN with an overturning moment of " + num(fmt(P.MoG, 1)) + " kN m; surcharge thrust " + num(fmt(P.HQ, 1)) + " kN with " + num(fmt(P.MoQ, 1)) + " kN m. μ = " + num(P.mu) + ". Find the design overturning and restoring moments (EQU), and the sliding force and the friction in combination 1.",
                "Jadual load satu cantilever wall memberi, bagi setiap meter dan dengan characteristic value: berat ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN dengan restoring moment " + num(fmt(P.MrG, 1)) + " kN m pada toe; surcharge di atas heel " + num(fmt(P.VQ, 1)) + " kN dengan " + num(fmt(P.MrQ, 1)) + " kN m; thrust tanah " + num(fmt(P.HG, 1)) + " kN dengan overturning moment " + num(fmt(P.MoG, 1)) + " kN m; thrust surcharge " + num(fmt(P.HQ, 1)) + " kN dengan " + num(fmt(P.MoQ, 1)) + " kN m. μ = " + num(P.mu) + ". Cari design overturning moment dan restoring moment (EQU), serta daya sliding dan friction dalam combination 1.");
    },
    fields: [{ id: "mo", label: ["M<sub>o,d</sub>", "M<sub>o,d</sub>"], unit: "kN m", fn: function (P) { return P.Mod; }, rtol: 0.005 },
             { id: "mr", label: ["M<sub>r,d</sub>", "M<sub>r,d</sub>"], unit: "kN m", fn: function (P) { return P.Mrd; }, rtol: 0.005 },
             { id: "hd", label: ["H<sub>d</sub>", "H<sub>d</sub>"], unit: "kN", fn: function (P) { return P.Hd; }, rtol: 0.005 },
             { id: "rd", label: ["R<sub>d</sub>", "R<sub>d</sub>"], unit: "kN", fn: function (P) { return P.Rd; }, rtol: 0.005 }],
    hints: [function () { return bi("Ask of every load: does it help or harm this check? The thrusts harm; the weights help.", "Tanya bagi setiap load: adakah ia membantu atau memudaratkan semakan ini? Thrust memudaratkan; berat membantu."); },
            function () { return bi("EQU: 1.1M<sub>o,G</sub> + 1.5M<sub>o,Q</sub> against 0.9M<sub>r,G</sub>. The surcharge on the heel takes 0.", "EQU: 1.1M<sub>o,G</sub> + 1.5M<sub>o,Q</sub> berbanding 0.9M<sub>r,G</sub>. Surcharge di atas heel menerima 0."); },
            function () { return bi("Sliding: 1.35H<sub>k,G</sub> + 1.5H<sub>k,Q</sub> against μ × 1.0 × ΣV<sub>k,G</sub>.", "Sliding: 1.35H<sub>k,G</sub> + 1.5H<sub>k,Q</sub> berbanding μ × 1.0 × ΣV<sub>k,G</sub>."); }],
    solution: function (P) {
      return sol(["M<sub>o,d</sub> = 1.1 × " + fmt(P.MoG, 1) + " + 1.5 × " + fmt(P.MoQ, 1) + " = " + fmt(P.Mod, 1) + " kN m",
        "M<sub>r,d</sub> = 0.9 × " + fmt(P.MrG, 1) + " = " + fmt(P.Mrd, 1) + " kN m: " + (P.Mod <= P.Mrd ? "✓" : bi("✗, the wall overturns", "✗, wall terbalik")),
        "H<sub>d</sub> = 1.35 × " + fmt(P.HG, 1) + " + 1.5 × " + fmt(P.HQ, 1) + " = " + fmt(P.Hd, 1) + " kN",
        "R<sub>d</sub> = " + P.mu + " × " + fmt(P.VG, 1) + " = " + fmt(P.Rd, 1) + " kN: " + (P.Hd <= P.Rd ? "✓" : bi("✗, the wall slides: lengthen the heel", "✗, wall menggelongsor: panjangkan heel")),
        bi("The " + fmt(P.VQ, 1) + " kN of surcharge on the heel is in neither resistance: a favourable variable action counts as zero. EC7 Combination 2 comes next (B5).", fmt(P.VQ, 1) + " kN surcharge di atas heel tidak berada dalam mana-mana rintangan: variable action yang favourable dikira sifar. EC7 Combination 2 menyusul (B5).")]);
    }
  });

  /* ---------- B5 sliding in EC7 Combination 2 ---------- */
  EX.define("b5", {
    gen: function (r) {
      var W = wall(r), P = {};
      P.phi = W.phi; P.VG = r1(W.VG); P.HG = r1(W.Ps); P.HQ = r1(W.Pq); P.mu = pick(r, [0.45, 0.5, 0.55, 0.6]);
      P.Ka = Ka(P.phi); P.phid = Math.atan(Math.tan(rad(P.phi)) / 1.25) * 180 / Math.PI; P.Kad = Ka(P.phid); P.rk = P.Kad / P.Ka;
      P.Hd2 = (P.HG + 1.3 * P.HQ) * P.rk; P.Rd2 = P.mu / 1.25 * P.VG;
      return P;
    },
    text: function (P) {
      return bi("A wall retains sand with φ = " + num(P.phi) + "°. With characteristic values, per metre: soil thrust " + num(fmt(P.HG, 1)) + " kN, surcharge thrust " + num(fmt(P.HQ, 1)) + " kN, weights ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN, μ = " + num(P.mu) + ". For sliding in EC7 Combination 2, find the design angle φ<sub>d</sub>, the sliding force and the friction.",
                "Satu wall menahan pasir dengan φ = " + num(P.phi) + "°. Dengan characteristic value, bagi setiap meter: thrust tanah " + num(fmt(P.HG, 1)) + " kN, thrust surcharge " + num(fmt(P.HQ, 1)) + " kN, berat ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN, μ = " + num(P.mu) + ". Bagi sliding dalam EC7 Combination 2, cari sudut design φ<sub>d</sub>, daya sliding dan friction.");
    },
    fields: [{ id: "phid", label: ["φ<sub>d</sub>", "φ<sub>d</sub>"], unit: "°", fn: function (P) { return P.phid; }, rtol: 0.003, atol: 0.06 },
             { id: "hd", label: ["H<sub>d,2</sub>", "H<sub>d,2</sub>"], unit: "kN", fn: function (P) { return P.Hd2; }, rtol: 0.01 },
             { id: "rd", label: ["R<sub>d,2</sub>", "R<sub>d,2</sub>"], unit: "kN", fn: function (P) { return P.Rd2; }, rtol: 0.005 }],
    hints: [function () { return bi("The factor 1.25 divides tan φ, not φ: φ<sub>d</sub> = tan⁻¹(tan φ/1.25).", "Faktor 1.25 membahagi tan φ, bukan φ: φ<sub>d</sub> = tan⁻¹(tan φ/1.25)."); },
            function () { return bi("A weaker soil pushes harder: every thrust grows by K<sub>a,d</sub>/K<sub>a</sub>. The actions take 1.0 (permanent) and 1.3 (variable).", "Tanah yang lebih lemah menolak lebih kuat: setiap thrust bertambah sebanyak K<sub>a,d</sub>/K<sub>a</sub>. Action menerima 1.0 (permanent) dan 1.3 (variable)."); },
            function () { return bi("The friction is factored as well: R<sub>d,2</sub> = (μ/1.25)ΣV<sub>k,G</sub>.", "Friction juga difaktorkan: R<sub>d,2</sub> = (μ/1.25)ΣV<sub>k,G</sub>."); }],
    solution: function (P) {
      return sol(["φ<sub>d</sub> = tan⁻¹(tan " + P.phi + "°/1.25) = tan⁻¹(" + fmt(Math.tan(rad(P.phi)) / 1.25, 4) + ") = " + fmt(P.phid, 2) + "°",
        "K<sub>a</sub> = " + fmt(P.Ka, 4) + "; K<sub>a,d</sub> = (1 − sin " + fmt(P.phid, 2) + "°)/(1 + sin " + fmt(P.phid, 2) + "°) = " + fmt(P.Kad, 4) + "; K<sub>a,d</sub>/K<sub>a</sub> = " + fmt(P.rk, 4),
        "H<sub>d,2</sub> = (1.0 × " + fmt(P.HG, 1) + " + 1.3 × " + fmt(P.HQ, 1) + ") × " + fmt(P.rk, 4) + " = " + fmt(P.Hd2, 1) + " kN",
        "R<sub>d,2</sub> = (" + P.mu + "/1.25) × " + fmt(P.VG, 1) + " = " + fmt(P.Rd2, 1) + " kN: " + (P.Hd2 <= P.Rd2 ? "✓" : bi("✗, the wall slides in Combination 2", "✗, wall menggelongsor dalam Combination 2")),
        bi("Combination 1 for comparison: " + fmt(1.35 * P.HG + 1.5 * P.HQ, 1) + " against " + fmt(P.mu * P.VG, 1) + " kN. The design must satisfy both (Notes §4).", "Combination 1 sebagai perbandingan: " + fmt(1.35 * P.HG + 1.5 * P.HQ, 1) + " berbanding " + fmt(P.mu * P.VG, 1) + " kN. Design mesti memenuhi kedua-duanya (Nota §4).")]);
    }
  });

  /* ---------- B6 the resultant, the middle third and the bearing pressure ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P;
      for (var t = 0; t < 60; t++) {
        P = {};
        P.B = step(r, 2.4, 4.2, 0.1); P.N = step(r, 180, 360, 5); P.Mo = step(r, 80, 220, 5);
        var eb = 0.02 + 0.2 * r();
        P.Mr = r1(P.N * (P.B / 2 - eb * P.B) + P.Mo);
        P.dM = P.Mr - P.Mo; P.x = P.dM / P.N; P.e = P.B / 2 - P.x; P.B6 = P.B / 6;
        if (Math.abs(P.e - P.B6) < 0.012 || P.e < 0.02) continue;
        P.out = P.e > P.B6;
        if (P.out) { P.qmax = 2 * P.N / (3 * P.x); P.qmin = 0; } else { P.qm = P.N / P.B; P.dq = 6 * P.N * P.e / (P.B * P.B); P.qmax = P.qm + P.dq; P.qmin = P.qm - P.dq; }
        return P;
      }
      return P;
    },
    text: function (P) {
      return bi("Under service loads, a wall on a base " + num(fmt(P.B, 1)) + " m wide carries a vertical load of " + num(P.N) + " kN per metre, the surcharge on the heel included. About the toe, the restoring moments sum to " + num(fmt(P.Mr, 1)) + " kN m and the overturning moments to " + num(P.Mo) + " kN m. Find the eccentricity of the resultant and the largest and smallest bearing pressures (enter 0 where the base lifts).",
                "Di bawah service load, satu wall di atas base selebar " + num(fmt(P.B, 1)) + " m memikul load menegak " + num(P.N) + " kN bagi setiap meter, termasuk surcharge di atas heel. Pada toe, restoring moment berjumlah " + num(fmt(P.Mr, 1)) + " kN m dan overturning moment " + num(P.Mo) + " kN m. Cari eccentricity resultant serta bearing pressure terbesar dan terkecil (masukkan 0 jika base terangkat).");
    },
    fields: [{ id: "e", label: ["e", "e"], unit: "m", fn: function (P) { return P.e; }, rtol: 0.01, atol: 0.004 },
             { id: "qmax", label: ["q<sub>max</sub>", "q<sub>max</sub>"], unit: "kN/m²", fn: function (P) { return P.qmax; }, rtol: 0.01 },
             { id: "qmin", label: ["q<sub>min</sub>", "q<sub>min</sub>"], unit: "kN/m²", fn: function (P) { return P.qmin; }, rtol: 0.015, atol: 0.6 }],
    hints: [function () { return bi("<span style='text-decoration:overline'>x</span> = ΔM/N from the toe, with ΔM = restoring − overturning.", "<span style='text-decoration:overline'>x</span> = ΔM/N dari toe, dengan ΔM = restoring − overturning."); },
            function () { return bi("The eccentricity is measured from the centre of the base: e = B/2 − <span style='text-decoration:overline'>x</span>. Compare it with B/6.", "Eccentricity diukur dari pusat base: e = B/2 − <span style='text-decoration:overline'>x</span>. Bandingkan dengan B/6."); },
            function () { return bi("Inside the middle third: q = N/B ± 6Ne/B². Outside it: q<sub>max</sub> = 2N/(3<span style='text-decoration:overline'>x</span>) and the heel end lifts.", "Di dalam middle third: q = N/B ± 6Ne/B². Di luarnya: q<sub>max</sub> = 2N/(3<span style='text-decoration:overline'>x</span>) dan hujung heel terangkat."); }],
    solution: function (P) {
      var L = ["ΔM = " + fmt(P.Mr, 1) + " − " + P.Mo + " = " + fmt(P.dM, 1) + " kN m; <span style='text-decoration:overline'>x</span> = " + fmt(P.dM, 1) + "/" + P.N + " = " + fmt(P.x, 4) + " m",
        "e = " + fmt(P.B, 1) + "/2 − " + fmt(P.x, 4) + " = " + fmt(P.e, 4) + " m; B/6 = " + fmt(P.B6, 3) + " m"];
      if (P.out) {
        L.push(bi("e &gt; B/6: outside the middle third; the heel end lifts", "e &gt; B/6: di luar middle third; hujung heel terangkat"));
        L.push("q<sub>max</sub> = 2 × " + P.N + "/(3 × " + fmt(P.x, 4) + ") = " + fmt(P.qmax, 1) + " kN/m²; q<sub>min</sub> = 0" + bi("; contact over 3<span style='text-decoration:overline'>x</span> = ", "; sentuhan sepanjang 3<span style='text-decoration:overline'>x</span> = ") + fmt(3 * P.x, 2) + " m");
        L.push(bi("The course does not accept this under service loads: widen the base, usually at the toe (Notes §5, §6).", "Kursus tidak menerima keadaan ini di bawah service load: lebarkan base, lazimnya di toe (Nota §5, §6)."));
      } else {
        L.push(bi("e ≤ B/6: inside the middle third, the whole base in contact", "e ≤ B/6: di dalam middle third, seluruh base bersentuhan"));
        L.push("q = " + P.N + "/" + fmt(P.B, 1) + " ± 6 × " + P.N + " × " + fmt(P.e, 4) + "/" + fmt(P.B, 1) + "² = " + fmt(P.qm, 2) + " ± " + fmt(P.dq, 2));
        L.push("q<sub>max</sub> = " + fmt(P.qmax, 1) + " kN/m²" + bi(" at the toe; ", " di toe; ") + "q<sub>min</sub> = " + fmt(P.qmin, 1) + " kN/m²" + bi(" at the heel end. Compare q<sub>max</sub> with q<sub>a</sub>.", " di hujung heel. Bandingkan q<sub>max</sub> dengan q<sub>a</sub>."));
      }
      return sol(L);
    }
  });

  EX.ready();
})();
