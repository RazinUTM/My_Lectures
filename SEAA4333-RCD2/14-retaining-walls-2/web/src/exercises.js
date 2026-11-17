/* SEAA 4333 Unit 14 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method of the notes (the RC Design app's retaining-wall model), per metre of wall:
   STR: N_d = 1.35 V_kG + 1.5 V_kQ, dM_d = 1.35 (M_rG - M_oG) + 1.5 (M_rQ - M_oQ), q_d = N_d/B +- 6 N_d e_d/B^2;
   toe: n = q_d - 1.35 x 25 h (upwards); heel: n = 1.35 (25 h + gamma h3) + 1.5 w - q_d (downwards);
   cantilever under a trapezium: M = n_f a^2/2 + (n_e - n_f) a^2/3, V = (n_f + n_e) a/2;
   stem over h_s = h3: M = 1.35 P_s h_s/3 + 1.5 P_q h_s/2, V = 1.35 P_s + 1.5 P_q;
   flexure: K = M/(b d^2 f_ck), z = d [0.5 + sqrt(0.25 - K/1.134)] <= 0.95 d, A_s = M/(0.87 f_yk z), A_s,min = 0.26 f_ctm/f_yk b d;
   crack control: sigma_s = (f_yk/1.15) x ratio x A_s,req/A_s,prov, spacing from EC2 Table 7.3N (w_k = 0.3 mm), interpolated;
   sloping backfill: K_a = cos t (cos t - sqrt(cos^2 t - cos^2 phi))/(cos t + sqrt(...)), P_h = P cos t, P_v = P sin t at the heel end. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function rad(a) { return a * Math.PI / 180; }
  function Ka(phi) { var s = Math.sin(rad(phi)); return (1 - s) / (1 + s); }
  function KaS(phi, th) { var c = Math.cos(rad(th)), p = Math.cos(rad(phi)), q = Math.sqrt(c * c - p * p); return c * (c - q) / (c + q); }
  function r1(v) { return Math.round(v * 10) / 10; }
  var FCTM = 0.3 * Math.pow(30, 2 / 3), RMIN = Math.max(0.26 * FCTM / 500, 0.0013);
  function flex(M, d) { var K = M * 1e6 / (1000 * d * d * 30), z0 = d * (0.5 + Math.sqrt(0.25 - K / 1.134)), z = Math.min(z0, 0.95 * d); return { K: K, z0: z0, z: z, As: M * 1e6 / (0.87 * 500 * z), Asmin: RMIN * 1000 * d }; }
  var T73 = [[160, 300], [200, 250], [240, 200], [280, 150], [320, 100], [360, 50]];
  function smax(sig) {
    if (sig <= 160) return 300; if (sig >= 360) return 50;
    for (var i = 0; i < 5; i++) if (sig <= T73[i + 1][0]) return T73[i][1] + (T73[i + 1][1] - T73[i][1]) * (sig - T73[i][0]) / 40;
    return 50;
  }
  function trap(nf, ne, a) { return { M: nf * a * a / 2 + (ne - nf) * a * a / 3, V: (nf + ne) * a / 2 }; }
  /* a simple wall (uniform stem) with its Unit 13 sums and its STR design pressures; the sums are rounded to 0.1 as a student would carry them */
  function wall(r) {
    var W, k = 0;
    do {
      W = {};
      W.h3 = step(r, 3.0, 5.5, 0.5); W.h = pick(r, [0.3, 0.4, 0.5]); W.t = pick(r, [0.3, 0.35, 0.4, 0.45]);
      W.H = +(W.h3 + W.h).toFixed(2); W.gs = pick(r, [17, 18, 19, 20]); W.phi = pick(r, [28, 30, 32, 33, 35, 36]); W.w = pick(r, [5, 10, 15]);
      W.a1 = step(r, 0.4, 1.0, 0.1); W.a2 = +(Math.round((0.38 + 0.12 * r()) * W.H * 10) / 10).toFixed(1); W.B = +(W.a1 + W.t + W.a2).toFixed(2);
      W.Ka = Ka(W.phi);
      var Ps = 0.5 * W.Ka * W.gs * W.H * W.H, Pq = W.Ka * W.w * W.H, Ws = W.t * W.h3 * 25, Wb = W.h * W.B * 25, W4 = W.gs * W.h3 * W.a2, Wq = W.w * W.a2;
      W.VG = r1(Ws + Wb + W4); W.VQ = r1(Wq);
      W.MrG = r1(Ws * (W.a1 + W.t / 2) + Wb * W.B / 2 + W4 * (W.a1 + W.t + W.a2 / 2)); W.MrQ = r1(Wq * (W.a1 + W.t + W.a2 / 2));
      W.MoG = r1(Ps * W.H / 3); W.MoQ = r1(Pq * W.H / 2);
      W.Nd = 1.35 * W.VG + 1.5 * W.VQ; W.Md = 1.35 * (W.MrG - W.MoG) + 1.5 * (W.MrQ - W.MoQ);
      W.xd = W.Md / W.Nd; W.ed = W.B / 2 - W.xd; W.qm = W.Nd / W.B; W.dq = 6 * W.Nd * W.ed / (W.B * W.B);
      W.qmax = W.qm + W.dq; W.qmin = W.qm - W.dq;
      W.Q1 = r1(W.qmax); W.Q2 = r1(W.qmin);
      W.gh = 1.35 * (25 * W.h + W.gs * W.h3) + 1.5 * W.w;
      W.qhf = W.Q2 + (W.Q1 - W.Q2) * W.a2 / W.B; W.nhf = W.gh - W.qhf; W.nhe = W.gh - W.Q2;
      k++;
    } while (k < 60 && !(W.ed >= 0.03 && W.ed <= W.B / 6 - 0.03 && W.nhf >= 2 && W.qmin > 10));
    return W;
  }

  /* ---------- B1 the stem ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.phi = pick(r, [28, 30, 32, 33, 35, 36, 38]); P.gs = pick(r, [17, 18, 19, 20]); P.w = pick(r, [5, 10, 15, 20]);
      P.h3 = step(r, 3.0, 6.0, 0.5); P.h = pick(r, [0.3, 0.4, 0.5]); P.Ka = Ka(P.phi);
      P.Ps = 0.5 * P.Ka * P.gs * P.h3 * P.h3; P.Pq = P.Ka * P.w * P.h3;
      P.M = 1.35 * P.Ps * P.h3 / 3 + 1.5 * P.Pq * P.h3 / 2; P.V = 1.35 * P.Ps + 1.5 * P.Pq;
      return P;
    },
    text: function (P) {
      return bi("The stem of a cantilever wall is " + num(fmt(P.h3, 1)) + " m high and stands on a base " + num(fmt(P.h, 1)) + " m thick. It retains drained sand with γ = " + num(P.gs) + " kN/m³ and φ = " + num(P.phi) + "° under a surcharge of " + num(P.w) + " kN/m². Per metre of wall, find the soil thrust on the stem, and the design moment and the design shear at its root (STR).",
                "Stem satu cantilever wall setinggi " + num(fmt(P.h3, 1)) + " m dan berdiri di atas base setebal " + num(fmt(P.h, 1)) + " m. Ia menahan pasir bersaliran dengan γ = " + num(P.gs) + " kN/m³ dan φ = " + num(P.phi) + "° di bawah surcharge " + num(P.w) + " kN/m². Bagi setiap meter wall, cari thrust tanah pada stem, serta design moment dan design shear di pangkalnya (STR).");
    },
    fields: [{ id: "ps", label: ["P<sub>s,s</sub>", "P<sub>s,s</sub>"], unit: "kN", fn: function (P) { return P.Ps; }, rtol: 0.01 },
             { id: "m", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.01 },
             { id: "v", label: ["V<sub>Ed</sub>", "V<sub>Ed</sub>"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.01 }],
    hints: [function () { return bi("The stem is bent by the pressure on its own height: h<sub>s</sub> is the height of the stem, not the stem plus the base.", "Stem dilenturkan oleh tekanan pada tingginya sendiri: h<sub>s</sub> ialah tinggi stem, bukan stem ditambah base."); },
            function () { return bi("P<sub>s,s</sub> = ½K<sub>a</sub>γh<sub>s</sub>² at h<sub>s</sub>/3 above the root; P<sub>q,s</sub> = K<sub>a</sub>wh<sub>s</sub> at h<sub>s</sub>/2.", "P<sub>s,s</sub> = ½K<sub>a</sub>γh<sub>s</sub>² pada h<sub>s</sub>/3 di atas pangkal; P<sub>q,s</sub> = K<sub>a</sub>wh<sub>s</sub> pada h<sub>s</sub>/2."); },
            function () { return bi("STR: 1.35 on the soil thrust, 1.5 on the surcharge thrust, in the moment and in the shear.", "STR: 1.35 pada thrust tanah, 1.5 pada thrust surcharge, dalam moment dan dalam shear."); }],
    solution: function (P) {
      return sol(["K<sub>a</sub> = (1 − sin " + P.phi + "°)/(1 + sin " + P.phi + "°) = " + fmt(P.Ka, 4) + "; h<sub>s</sub> = " + fmt(P.h3, 1) + " m",
        "P<sub>s,s</sub> = ½ × " + fmt(P.Ka, 4) + " × " + P.gs + " × " + fmt(P.h3, 1) + "² = " + fmt(P.Ps, 2) + " kN; P<sub>q,s</sub> = " + fmt(P.Ka, 4) + " × " + P.w + " × " + fmt(P.h3, 1) + " = " + fmt(P.Pq, 2) + " kN",
        "M<sub>Ed</sub> = 1.35 × " + fmt(P.Ps, 2) + " × " + fmt(P.h3, 1) + "/3 + 1.5 × " + fmt(P.Pq, 2) + " × " + fmt(P.h3, 1) + "/2 = " + fmt(P.M, 1) + " kN m/m",
        "V<sub>Ed</sub> = 1.35 × " + fmt(P.Ps, 2) + " + 1.5 × " + fmt(P.Pq, 2) + " = " + fmt(P.V, 1) + " kN/m",
        bi("Tension is on the earth face; the base thickness plays no part here (Notes §3).", "Tegangan berada di muka tanah; ketebalan base tidak terlibat di sini (Nota §3).")]);
    }
  });

  /* ---------- B2 the design pressures ---------- */
  EX.define("b2", {
    gen: function (r) { return wall(r); },
    text: function (P) {
      return bi("The stability table of a wall on a base " + num(fmt(P.B, 2)) + " m wide gives, per metre: ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN, V<sub>k,Q</sub> = " + num(fmt(P.VQ, 1)) + " kN; ΣM<sub>r,G</sub> = " + num(fmt(P.MrG, 1)) + " kN m, M<sub>r,Q</sub> = " + num(fmt(P.MrQ, 1)) + " kN m; M<sub>o,G</sub> = " + num(fmt(P.MoG, 1)) + " kN m, M<sub>o,Q</sub> = " + num(fmt(P.MoQ, 1)) + " kN m, all about the toe. For the design of the members (STR), find the eccentricity e<sub>d</sub> and the design pressures at the toe and at the heel end.",
                "Jadual kestabilan satu wall di atas base selebar " + num(fmt(P.B, 2)) + " m memberi, bagi setiap meter: ΣV<sub>k,G</sub> = " + num(fmt(P.VG, 1)) + " kN, V<sub>k,Q</sub> = " + num(fmt(P.VQ, 1)) + " kN; ΣM<sub>r,G</sub> = " + num(fmt(P.MrG, 1)) + " kN m, M<sub>r,Q</sub> = " + num(fmt(P.MrQ, 1)) + " kN m; M<sub>o,G</sub> = " + num(fmt(P.MoG, 1)) + " kN m, M<sub>o,Q</sub> = " + num(fmt(P.MoQ, 1)) + " kN m, semuanya pada toe. Bagi design bahagian-bahagian wall (STR), cari eccentricity e<sub>d</sub> dan design pressure di toe dan di hujung heel.");
    },
    fields: [{ id: "ed", label: ["e<sub>d</sub>", "e<sub>d</sub>"], unit: "m", fn: function (P) { return P.ed; }, rtol: 0.02, atol: 0.003 },
             { id: "q1", label: ["q<sub>d</sub> (toe)", "q<sub>d</sub> (toe)"], unit: "kN/m²", fn: function (P) { return P.qmax; }, rtol: 0.01 },
             { id: "q2", label: ["q<sub>d</sub> (heel end)", "q<sub>d</sub> (hujung heel)"], unit: "kN/m²", fn: function (P) { return P.qmin; }, rtol: 0.015, atol: 0.6 }],
    hints: [function () { return bi("N<sub>d</sub> = 1.35ΣV<sub>k,G</sub> + 1.5V<sub>k,Q</sub>: here the surcharge on the heel is counted.", "N<sub>d</sub> = 1.35ΣV<sub>k,G</sub> + 1.5V<sub>k,Q</sub>: di sini surcharge di atas heel dikira."); },
            function () { return bi("ΔM<sub>d</sub> = 1.35(ΣM<sub>r,G</sub> − M<sub>o,G</sub>) + 1.5(M<sub>r,Q</sub> − M<sub>o,Q</sub>); x<sub>d</sub> = ΔM<sub>d</sub>/N<sub>d</sub>; e<sub>d</sub> = B/2 − x<sub>d</sub>. Carry x<sub>d</sub> to four decimals.", "ΔM<sub>d</sub> = 1.35(ΣM<sub>r,G</sub> − M<sub>o,G</sub>) + 1.5(M<sub>r,Q</sub> − M<sub>o,Q</sub>); x<sub>d</sub> = ΔM<sub>d</sub>/N<sub>d</sub>; e<sub>d</sub> = B/2 − x<sub>d</sub>. Bawa x<sub>d</sub> hingga empat tempat perpuluhan."); },
            function () { return bi("q<sub>d</sub> = N<sub>d</sub>/B ± 6N<sub>d</sub>e<sub>d</sub>/B²: the larger value is at the toe.", "q<sub>d</sub> = N<sub>d</sub>/B ± 6N<sub>d</sub>e<sub>d</sub>/B²: nilai yang lebih besar berada di toe."); }],
    solution: function (P) {
      return sol(["N<sub>d</sub> = 1.35 × " + fmt(P.VG, 1) + " + 1.5 × " + fmt(P.VQ, 1) + " = " + fmt(P.Nd, 2) + " kN",
        "ΔM<sub>d</sub> = 1.35 × (" + fmt(P.MrG, 1) + " − " + fmt(P.MoG, 1) + ") + 1.5 × (" + fmt(P.MrQ, 1) + " − " + fmt(P.MoQ, 1) + ") = " + fmt(P.Md, 2) + " kN m",
        "x<sub>d</sub> = " + fmt(P.Md, 2) + "/" + fmt(P.Nd, 2) + " = " + fmt(P.xd, 4) + " m; e<sub>d</sub> = " + fmt(P.B, 2) + "/2 − " + fmt(P.xd, 4) + " = " + fmt(P.ed, 4) + " m (≤ B/6 = " + fmt(P.B / 6, 3) + " m)",
        "q<sub>d</sub> = " + fmt(P.Nd, 2) + "/" + fmt(P.B, 2) + " ± 6 × " + fmt(P.Nd, 2) + " × " + fmt(P.ed, 4) + "/" + fmt(P.B, 2) + "² = " + fmt(P.qm, 2) + " ± " + fmt(P.dq, 2) + ": " + fmt(P.qmax, 1) + bi(" and ", " dan ") + fmt(P.qmin, 1) + " kN/m²",
        bi("These pressures load the toe from below and relieve the heel (B3, B4; Notes §2).", "Tekanan ini membebani toe dari bawah dan meringankan heel (B3, B4; Nota §2).")]);
    }
  });

  /* ---------- B3 the toe ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.B = step(r, 2.6, 4.2, 0.1); P.a1 = step(r, 0.5, 1.2, 0.1); P.h = pick(r, [0.3, 0.4, 0.5]);
      P.q1 = step(r, 100, 180, 1); P.q2 = P.q1 - step(r, 20, 70, 1);
      P.gb = 1.35 * 25 * P.h; P.qf = P.q1 - (P.q1 - P.q2) * P.a1 / P.B; P.ne = P.q1 - P.gb; P.nf = P.qf - P.gb;
      var t = trap(P.nf, P.ne, P.a1); P.M = t.M; P.V = t.V;
      return P;
    },
    text: function (P) {
      return bi("Under the base of a wall, " + num(fmt(P.B, 1)) + " m wide and " + num(fmt(P.h * 1000, 0)) + " mm thick, the design pressure (STR) is " + num(P.q1) + " kN/m² at the toe and " + num(P.q2) + " kN/m² at the heel end. The toe is " + num(fmt(P.a1, 1)) + " m long; concrete 25 kN/m³; the soil over the toe is ignored. Find the net upward load at the front face of the stem, and the design moment and shear of the toe there, per metre.",
                "Di bawah base satu wall, selebar " + num(fmt(P.B, 1)) + " m dan setebal " + num(fmt(P.h * 1000, 0)) + " mm, design pressure (STR) ialah " + num(P.q1) + " kN/m² di toe dan " + num(P.q2) + " kN/m² di hujung heel. Toe sepanjang " + num(fmt(P.a1, 1)) + " m; konkrit 25 kN/m³; tanah di atas toe diabaikan. Cari net load ke atas di muka hadapan stem, serta design moment dan shear toe di situ, bagi setiap meter.");
    },
    fields: [{ id: "nf", label: ["n (at the stem)", "n (di stem)"], unit: "kN/m²", fn: function (P) { return P.nf; }, rtol: 0.01 },
             { id: "m", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.01 },
             { id: "v", label: ["V<sub>Ed</sub>", "V<sub>Ed</sub>"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.01 }],
    hints: [function () { return bi("The pressure falls in a straight line from the toe to the heel end: at the stem it has fallen by (q<sub>toe</sub> − q<sub>heel</sub>) × toe/B.", "Tekanan berkurang mengikut garis lurus dari toe ke hujung heel: di stem ia telah berkurang sebanyak (q<sub>toe</sub> − q<sub>heel</sub>) × toe/B."); },
            function () { return bi("Net load = pressure less the weight of the slab, 1.35 × 25 × h, at both ends of the toe.", "Net load = tekanan tolak berat slab, 1.35 × 25 × h, di kedua-dua hujung toe."); },
            function () { return bi("M = n<sub>f</sub>a²/2 + (n<sub>e</sub> − n<sub>f</sub>)a²/3; V = ½(n<sub>f</sub> + n<sub>e</sub>)a. The larger load is at the free end.", "M = n<sub>f</sub>a²/2 + (n<sub>e</sub> − n<sub>f</sub>)a²/3; V = ½(n<sub>f</sub> + n<sub>e</sub>)a. Load yang lebih besar berada di hujung bebas."); }],
    solution: function (P) {
      return sol([bi("At the stem: ", "Di stem: ") + P.q1 + " − (" + P.q1 + " − " + P.q2 + ") × " + fmt(P.a1, 1) + "/" + fmt(P.B, 1) + " = " + fmt(P.qf, 2) + " kN/m²",
        bi("Slab: ", "Slab: ") + "1.35 × 25 × " + fmt(P.h, 1) + " = " + fmt(P.gb, 2) + " kN/m²; n<sub>e</sub> = " + P.q1 + " − " + fmt(P.gb, 2) + " = " + fmt(P.ne, 2) + "; n<sub>f</sub> = " + fmt(P.qf, 2) + " − " + fmt(P.gb, 2) + " = " + fmt(P.nf, 2) + " kN/m²",
        "M<sub>Ed</sub> = " + fmt(P.nf, 2) + " × " + fmt(P.a1, 1) + "²/2 + (" + fmt(P.ne, 2) + " − " + fmt(P.nf, 2) + ") × " + fmt(P.a1, 1) + "²/3 = " + fmt(P.M, 1) + " kN m/m",
        "V<sub>Ed</sub> = ½ × (" + fmt(P.nf, 2) + " + " + fmt(P.ne, 2) + ") × " + fmt(P.a1, 1) + " = " + fmt(P.V, 1) + " kN/m",
        bi("Upward net load: the toe bends up and its bars go in the bottom (Notes §4).", "Net load ke atas: toe melentur ke atas dan bar-nya di bahagian bawah (Nota §4).")]);
    }
  });

  /* ---------- B4 the heel ---------- */
  EX.define("b4", {
    gen: function (r) { var P = wall(r); var t = trap(P.nhf, P.nhe, P.a2); P.M = t.M; P.V = t.V; return P; },
    text: function (P) {
      return bi("A wall has a stem " + num(fmt(P.h3, 1)) + " m high on a base " + num(fmt(P.B, 2)) + " m wide and " + num(fmt(P.h * 1000, 0)) + " mm thick, with a heel of " + num(fmt(P.a2, 1)) + " m. Backfill γ = " + num(P.gs) + " kN/m³, level, with a surcharge of " + num(P.w) + " kN/m²; concrete 25 kN/m³. The design pressure under the base (STR) is " + num(fmt(P.Q1, 1)) + " kN/m² at the toe and " + num(fmt(P.Q2, 1)) + " kN/m² at the heel end. Find the net downward load at the back face of the stem, and the design moment and shear of the heel there, per metre.",
                "Satu wall mempunyai stem setinggi " + num(fmt(P.h3, 1)) + " m di atas base selebar " + num(fmt(P.B, 2)) + " m dan setebal " + num(fmt(P.h * 1000, 0)) + " mm, dengan heel " + num(fmt(P.a2, 1)) + " m. Backfill γ = " + num(P.gs) + " kN/m³, rata, dengan surcharge " + num(P.w) + " kN/m²; konkrit 25 kN/m³. Design pressure di bawah base (STR) ialah " + num(fmt(P.Q1, 1)) + " kN/m² di toe dan " + num(fmt(P.Q2, 1)) + " kN/m² di hujung heel. Cari net load ke bawah di muka belakang stem, serta design moment dan shear heel di situ, bagi setiap meter.");
    },
    fields: [{ id: "nf", label: ["n (at the stem)", "n (di stem)"], unit: "kN/m²", fn: function (P) { return P.nhf; }, rtol: 0.02, atol: 0.4 },
             { id: "m", label: ["M<sub>Ed</sub>", "M<sub>Ed</sub>"], unit: "kN m", fn: function (P) { return P.M; }, rtol: 0.015 },
             { id: "v", label: ["V<sub>Ed</sub>", "V<sub>Ed</sub>"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.015 }],
    hints: [function () { return bi("Downward load on the heel: 1.35 × (25h + γh<sub>3</sub>) + 1.5w. Here the surcharge is counted.", "Load ke bawah pada heel: 1.35 × (25h + γh<sub>3</sub>) + 1.5w. Di sini surcharge dikira."); },
            function () { return bi("Pressure at the back face of the stem: q<sub>heel</sub> + (q<sub>toe</sub> − q<sub>heel</sub>) × heel/B. Net load = downward load less pressure.", "Tekanan di muka belakang stem: q<sub>heel</sub> + (q<sub>toe</sub> − q<sub>heel</sub>) × heel/B. Net load = load ke bawah tolak tekanan."); },
            function () { return bi("M = n<sub>f</sub>a²/2 + (n<sub>e</sub> − n<sub>f</sub>)a²/3, with the larger net load at the heel end.", "M = n<sub>f</sub>a²/2 + (n<sub>e</sub> − n<sub>f</sub>)a²/3, dengan net load yang lebih besar di hujung heel."); }],
    solution: function (P) {
      return sol([bi("Downward: ", "Ke bawah: ") + "1.35 × (25 × " + fmt(P.h, 1) + " + " + P.gs + " × " + fmt(P.h3, 1) + ") + 1.5 × " + P.w + " = " + fmt(P.gh, 2) + " kN/m²",
        bi("At the stem: ", "Di stem: ") + fmt(P.Q2, 1) + " + (" + fmt(P.Q1, 1) + " − " + fmt(P.Q2, 1) + ") × " + fmt(P.a2, 1) + "/" + fmt(P.B, 2) + " = " + fmt(P.qhf, 2) + " kN/m²",
        "n<sub>f</sub> = " + fmt(P.gh, 2) + " − " + fmt(P.qhf, 2) + " = " + fmt(P.nhf, 2) + " kN/m²; n<sub>e</sub> = " + fmt(P.gh, 2) + " − " + fmt(P.Q2, 1) + " = " + fmt(P.nhe, 2) + " kN/m²",
        "M<sub>Ed</sub> = " + fmt(P.nhf, 2) + " × " + fmt(P.a2, 1) + "²/2 + (" + fmt(P.nhe, 2) + " − " + fmt(P.nhf, 2) + ") × " + fmt(P.a2, 1) + "²/3 = " + fmt(P.M, 1) + " kN m/m; V<sub>Ed</sub> = " + fmt(P.V, 1) + " kN/m",
        bi("Downward net load: the heel sags and its bars go in the top (Notes §1, §4).", "Net load ke bawah: heel melendut dan bar-nya di bahagian atas (Nota §1, §4).")]);
    }
  });

  /* ---------- B5 steel and crack control ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P = {}, SP = [250, 200, 175, 150, 125, 100, 75], k = 0, i;
      do {
        P.hh = pick(r, [300, 350, 400, 450, 500]); P.ph = pick(r, [12, 16]); P.d = P.hh - 45 - P.ph / 2;
        P.M = Math.round(step(r, 520, 1400, 20) * 0.87 * 500 * 0.95 * P.d / 1e6);
        P.rq = pick(r, [0.55, 0.60, 0.65, 0.70, 0.74]);
        P.f = flex(P.M, P.d); P.need = Math.max(P.f.As, P.f.Asmin); P.s = 0;
        for (i = 0; i < SP.length; i++) if (Math.PI * P.ph * P.ph / 4 * 1000 / SP[i] >= P.need) { P.s = SP[i]; break; }
        if (P.s && r() < 0.5 && i + 1 < SP.length) P.s = SP[i + 1];
        P.Asp = P.s ? Math.PI * P.ph * P.ph / 4 * 1000 / P.s : 0;
        P.sig = P.s ? 500 / 1.15 * P.rq * P.f.As / P.Asp : 0; P.sm = smax(P.sig);
        k++;
      } while (k < 60 && !(P.s && P.f.K < 0.12 && P.sig > 120 && P.sig < 350));
      P.ok = P.s <= P.sm;
      return P;
    },
    text: function (P) {
      return bi("A part of a wall " + num(P.hh) + " mm thick carries M<sub>Ed</sub> = " + num(P.M) + " kN m per metre. Concrete C30/37, f<sub>yk</sub> = 500 N/mm², cover 45 mm; H" + num(P.ph) + " bars at " + num(P.s) + " mm are proposed (" + num(fmt(P.Asp, 0)) + " mm²/m). The ratio of the quasi-permanent to the design effect is " + num(fmt(P.rq, 2)) + ". Find the steel needed for the moment, the steel stress σ<sub>s</sub> and the largest bar spacing Table 7.3N allows.",
                "Satu bahagian wall setebal " + num(P.hh) + " mm memikul M<sub>Ed</sub> = " + num(P.M) + " kN m bagi setiap meter. Konkrit C30/37, f<sub>yk</sub> = 500 N/mm², cover 45 mm; bar H" + num(P.ph) + " pada " + num(P.s) + " mm dicadangkan (" + num(fmt(P.Asp, 0)) + " mm²/m). Nisbah kesan quasi-permanent kepada kesan design ialah " + num(fmt(P.rq, 2)) + ". Cari steel yang diperlukan bagi moment, steel stress σ<sub>s</sub> dan jarak bar terbesar yang dibenarkan oleh Table 7.3N.");
    },
    fields: [{ id: "as", label: ["A<sub>s</sub> (moment)", "A<sub>s</sub> (moment)"], unit: "mm²", fn: function (P) { return P.f.As; }, rtol: 0.01 },
             { id: "sg", label: ["σ<sub>s</sub>", "σ<sub>s</sub>"], unit: "N/mm²", fn: function (P) { return P.sig; }, rtol: 0.015 },
             { id: "sm", label: ["s<sub>max</sub>", "s<sub>max</sub>"], unit: "mm", fn: function (P) { return P.sm; }, rtol: 0.02, atol: 4 }],
    hints: [function () { return bi("d = h − cover − φ/2. K = M/(bd²f<sub>ck</sub>) with b = 1000 mm; z = d[0.5 + √(0.25 − K/1.134)] but not more than 0.95d; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z).", "d = h − cover − φ/2. K = M/(bd²f<sub>ck</sub>) dengan b = 1000 mm; z = d[0.5 + √(0.25 − K/1.134)] tetapi tidak melebihi 0.95d; A<sub>s</sub> = M/(0.87f<sub>yk</sub>z)."); },
            function () { return bi("σ<sub>s</sub> = (500/1.15) × ratio × A<sub>s,req</sub>/A<sub>s,prov</sub>, with A<sub>s,req</sub> the steel needed for the moment.", "σ<sub>s</sub> = (500/1.15) × nisbah × A<sub>s,req</sub>/A<sub>s,prov</sub>, dengan A<sub>s,req</sub> steel yang diperlukan bagi moment."); },
            function () { return bi("Table 7.3N (w<sub>k</sub> = 0.3 mm): 160 → 300, 200 → 250, 240 → 200, 280 → 150, 320 → 100, 360 → 50 mm. Interpolate between columns; below 160 N/mm² take 300 mm.", "Table 7.3N (w<sub>k</sub> = 0.3 mm): 160 → 300, 200 → 250, 240 → 200, 280 → 150, 320 → 100, 360 → 50 mm. Interpolasi di antara lajur; di bawah 160 N/mm² ambil 300 mm."); }],
    solution: function (P) {
      var f = P.f;
      return sol(["d = " + P.hh + " − 45 − " + P.ph + "/2 = " + fmt(P.d, 0) + " mm; K = " + P.M + " × 10⁶/(1000 × " + fmt(P.d, 0) + "² × 30) = " + fmt(f.K, 4),
        "z = " + fmt(P.d, 0) + " × [0.5 + √(0.25 − " + fmt(f.K, 4) + "/1.134)] = " + fmt(f.z0, 1) + " mm" + (f.z0 > 0.95 * P.d ? bi(" &gt; 0.95d: z = ", " &gt; 0.95d: z = ") + fmt(f.z, 1) + " mm" : " ≤ 0.95d"),
        "A<sub>s</sub> = " + P.M + " × 10⁶/(0.87 × 500 × " + fmt(f.z, 1) + ") = " + fmt(f.As, 0) + " mm²/m; A<sub>s,min</sub> = 0.001506 × 1000 × " + fmt(P.d, 0) + " = " + fmt(f.Asmin, 0) + " mm²/m; H" + P.ph + bi(" at ", " pada ") + P.s + ": " + fmt(P.Asp, 0) + " mm²/m ✓",
        "σ<sub>s</sub> = 434.8 × " + fmt(P.rq, 2) + " × " + fmt(f.As, 0) + "/" + fmt(P.Asp, 0) + " = " + fmt(P.sig, 1) + " N/mm²",
        "s<sub>max</sub> = " + fmt(P.sm, 0) + " mm " + (P.ok ? "≥ " + P.s + " mm ✓" : "&lt; " + P.s + " mm ✗" + bi(": close the bars", ": rapatkan bar")),
        bi("More steel lowers the stress and widens the limit at the same time (Notes §5).", "Lebih banyak steel menurunkan stress dan melebarkan had pada masa yang sama (Nota §5).")]);
    }
  });

  /* ---------- B6 a sloping backfill ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.th = pick(r, [10, 12, 15, 18, 20]); P.phi = pick(r, [30, 32, 33, 35, 36]); P.gs = pick(r, [16, 17, 18, 19]);
      P.H = step(r, 4.5, 7.0, 0.1); P.a2 = step(r, 2.0, 3.2, 0.1);
      P.Ka = KaS(P.phi, P.th); P.P = 0.5 * P.Ka * P.gs * P.H * P.H; P.Ph = P.P * Math.cos(rad(P.th)); P.Pv = P.P * Math.sin(rad(P.th));
      P.Mv = 1.35 * P.Pv * P.a2;
      return P;
    },
    text: function (P) {
      return bi("The backfill behind a cantilever wall slopes upwards at " + num(P.th) + "°; γ = " + num(P.gs) + " kN/m³, φ = " + num(P.phi) + "°, no surcharge. The virtual back, through the end of the heel, is " + num(fmt(P.H, 1)) + " m high from the surface to the underside of the base, and the heel is " + num(fmt(P.a2, 1)) + " m long. Per metre of wall, find K<sub>a</sub>, the horizontal component of the thrust, and the design moment that the vertical component alone puts on the heel at the back face of the stem.",
                "Backfill di belakang satu cantilever wall bercerun ke atas pada " + num(P.th) + "°; γ = " + num(P.gs) + " kN/m³, φ = " + num(P.phi) + "°, tiada surcharge. Virtual back, melalui hujung heel, setinggi " + num(fmt(P.H, 1)) + " m dari permukaan hingga bahagian bawah base, dan heel sepanjang " + num(fmt(P.a2, 1)) + " m. Bagi setiap meter wall, cari K<sub>a</sub>, komponen mendatar thrust, dan design moment yang diberikan oleh komponen menegak sahaja kepada heel di muka belakang stem.");
    },
    fields: [{ id: "ka", label: ["K<sub>a</sub>", "K<sub>a</sub>"], unit: "", fn: function (P) { return P.Ka; }, rtol: 0.01, atol: 0.003 },
             { id: "ph", label: ["P<sub>h</sub>", "P<sub>h</sub>"], unit: "kN", fn: function (P) { return P.Ph; }, rtol: 0.012 },
             { id: "mv", label: ["M (from P<sub>v</sub>)", "M (daripada P<sub>v</sub>)"], unit: "kN m", fn: function (P) { return P.Mv; }, rtol: 0.015 }],
    hints: [function () { return bi("K<sub>a</sub> = cos θ × (cos θ − √(cos²θ − cos²φ))/(cos θ + √(cos²θ − cos²φ)). Work in degrees.", "K<sub>a</sub> = cos θ × (cos θ − √(cos²θ − cos²φ))/(cos θ + √(cos²θ − cos²φ)). Gunakan darjah."); },
            function () { return bi("P = ½K<sub>a</sub>γH² acts parallel to the slope: P<sub>h</sub> = P cos θ, P<sub>v</sub> = P sin θ.", "P = ½K<sub>a</sub>γH² bertindak selari dengan cerun: P<sub>h</sub> = P cos θ, P<sub>v</sub> = P sin θ."); },
            function () { return bi("P<sub>v</sub> acts at the end of the heel: a line load of 1.35P<sub>v</sub> at the tip of the cantilever, with a lever arm equal to the heel length.", "P<sub>v</sub> bertindak di hujung heel: line load 1.35P<sub>v</sub> di hujung cantilever, dengan lever arm sama dengan panjang heel."); }],
    solution: function (P) {
      var c = Math.cos(rad(P.th)), q = Math.sqrt(c * c - Math.pow(Math.cos(rad(P.phi)), 2));
      return sol(["cos " + P.th + "° = " + fmt(c, 4) + "; √(cos² " + P.th + "° − cos² " + P.phi + "°) = " + fmt(q, 4),
        "K<sub>a</sub> = " + fmt(c, 4) + " × (" + fmt(c, 4) + " − " + fmt(q, 4) + ")/(" + fmt(c, 4) + " + " + fmt(q, 4) + ") = " + fmt(P.Ka, 4),
        "P = ½ × " + fmt(P.Ka, 4) + " × " + P.gs + " × " + fmt(P.H, 1) + "² = " + fmt(P.P, 2) + " kN; P<sub>h</sub> = " + fmt(P.P, 2) + " cos " + P.th + "° = " + fmt(P.Ph, 1) + " kN; P<sub>v</sub> = " + fmt(P.P, 2) + " sin " + P.th + "° = " + fmt(P.Pv, 2) + " kN",
        "M = 1.35 × " + fmt(P.Pv, 2) + " × " + fmt(P.a2, 1) + " = " + fmt(P.Mv, 1) + " kN m/m",
        bi("This is added to the moment of the net pressure on the heel. P<sub>v</sub> helps the stability and loads the heel: count it in both (Notes §6).", "Ini ditambah kepada moment net pressure pada heel. P<sub>v</sub> membantu kestabilan dan membebani heel: kira ia dalam kedua-duanya (Nota §6).")]);
    }
  });

  EX.ready();
})();
