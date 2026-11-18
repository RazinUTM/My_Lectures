/* SEAA 4333 Unit 6 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows the course method as the RC Design app computes it (its cantilever and portal methods and the level
   combination, verified against the app): points of contraflexure at mid-height and mid-span; portal: H_i = k_i V with
   k_i = (L_left + L_right)/(2 sum L), M_col = H h/2, joint balance M_b,right = M_c,above + M_c,below - M_b,left, F = 2M_b/L;
   cantilever: N_i = r_i P, r_i = d_i/d_min, P = M_o/sum|r||d|, beam shears from the axial forces to the left of each beam cut,
   column shears from moments about each beam cut; combination (BS 8110 load combination 3): M_end = M_v + M_w, reversal
   M_w - M_v when positive, columns |M_v| + M_w. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function f2(v) { return fmt(v, 2); }
  function f3(v) { return fmt(v, 3); }
  function spansText(L) { return L.map(function (l) { return fmt(l, 1); }).join(", "); }

  /* ---------- B1 portal method: the column shears of a storey ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.L = [pick(r, [4, 5, 6, 7]), pick(r, [4, 5, 6, 7, 8]), pick(r, [5, 6, 7, 8])];
      P.V = step(r, 12, 90, 0.5);
      P.sum = P.L[0] + P.L[1] + P.L[2];
      P.kA = P.L[0] / (2 * P.sum); P.kB = (P.L[0] + P.L[1]) / (2 * P.sum);
      P.HA = P.kA * P.V; P.HB = P.kB * P.V;
      return P;
    },
    text: function (P) {
      return bi("A frame ABCD has spans AB, BC and CD of " + num(spansText(P.L)) + " m. A storey of the frame carries a storey shear of " + num(f2(P.V)) + " kN. By the portal method, find the shears in columns A and B of that storey.",
                "Sebuah frame ABCD mempunyai span AB, BC dan CD " + num(spansText(P.L)) + " m. Satu tingkat frame itu membawa storey shear " + num(f2(P.V)) + " kN. Dengan portal method, cari shear dalam column A dan B bagi tingkat itu.");
    },
    fields: [{ id: "a", label: ["H<sub>A</sub>", "H<sub>A</sub>"], unit: "kN", fn: function (P) { return P.HA; }, rtol: 0.01 },
             { id: "b", label: ["H<sub>B</sub>", "H<sub>B</sub>"], unit: "kN", fn: function (P) { return P.HB; }, rtol: 0.01 }],
    hints: [function () { return bi("The storey shear is shared between the bays in proportion to their spans; each bay's share goes half to each of its columns.", "Storey shear diagihkan kepada bay mengikut span-nya; bahagian setiap bay separuh kepada setiap column-nya."); },
            function () { return bi("k<sub>i</sub> = (L<sub>left</sub> + L<sub>right</sub>)/(2ΣL); an outer column has one span beside it.", "k<sub>i</sub> = (L<sub>left</sub> + L<sub>right</sub>)/(2ΣL); column luar mempunyai satu span di sebelahnya."); },
            function () { return bi("H<sub>i</sub> = k<sub>i</sub> × V.", "H<sub>i</sub> = k<sub>i</sub> × V."); }],
    solution: function (P) {
      return sol(["ΣL = " + spansText(P.L).replace(/, /g, " + ") + " = " + fmt(P.sum, 1) + " m",
        "k<sub>A</sub> = " + fmt(P.L[0], 1) + "/(2 × " + fmt(P.sum, 1) + ") = " + f3(P.kA) + "; H<sub>A</sub> = " + f3(P.kA) + " × " + f2(P.V) + " = " + f2(P.HA) + " kN",
        "k<sub>B</sub> = (" + fmt(P.L[0], 1) + " + " + fmt(P.L[1], 1) + ")/(2 × " + fmt(P.sum, 1) + ") = " + f3(P.kB) + "; H<sub>B</sub> = " + f3(P.kB) + " × " + f2(P.V) + " = " + f2(P.HB) + " kN"]);
    }
  });

  /* ---------- B2 portal method: the beam moments at a level, joint by joint ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.L = [pick(r, [5, 6, 7]), pick(r, [4, 5, 6]), pick(r, [6, 7, 8])];
      P.sum = P.L[0] + P.L[1] + P.L[2];
      P.Va = step(r, 10, 40, 0.5); P.V = +(P.Va + step(r, 8, 25, 0.5)).toFixed(2);
      P.ha = pick(r, [3.0, 3.5]); P.h = pick(r, [3.5, 4.0, 4.5]);
      P.kA = P.L[0] / (2 * P.sum); P.kB = (P.L[0] + P.L[1]) / (2 * P.sum);
      P.MuA = P.kA * P.Va * P.ha / 2; P.MlA = P.kA * P.V * P.h / 2;
      P.MuB = P.kB * P.Va * P.ha / 2; P.MlB = P.kB * P.V * P.h / 2;
      P.MAB = P.MuA + P.MlA; P.MBC = P.MuB + P.MlB - P.MAB; P.F = 2 * P.MAB / P.L[0];
      return P;
    },
    text: function (P) {
      return bi("A frame ABCD has spans AB, BC and CD of " + num(spansText(P.L)) + " m. At a floor level, the storey above (" + num(fmt(P.ha, 1)) + " m high) carries a storey shear of " + num(f2(P.Va)) + " kN and the storey below (" + num(fmt(P.h, 1)) + " m) " + num(f2(P.V)) + " kN. By the portal method, find the moments in beams AB and BC at that level and the shear in beam AB.",
                "Sebuah frame ABCD mempunyai span AB, BC dan CD " + num(spansText(P.L)) + " m. Pada satu aras lantai, tingkat di atas (setinggi " + num(fmt(P.ha, 1)) + " m) membawa storey shear " + num(f2(P.Va)) + " kN dan tingkat di bawah (" + num(fmt(P.h, 1)) + " m) " + num(f2(P.V)) + " kN. Dengan portal method, cari moment dalam beam AB dan BC pada aras itu dan shear dalam beam AB.");
    },
    fields: [{ id: "m1", label: ["M<sub>AB</sub>", "M<sub>AB</sub>"], unit: "kN m", fn: function (P) { return P.MAB; }, rtol: 0.01 },
             { id: "m2", label: ["M<sub>BC</sub>", "M<sub>BC</sub>"], unit: "kN m", fn: function (P) { return P.MBC; }, rtol: 0.01 },
             { id: "f", label: ["F<sub>AB</sub>", "F<sub>AB</sub>"], unit: "kN", fn: function (P) { return P.F; }, rtol: 0.01 }],
    hints: [function () { return bi("Column moments: H h/2 with H = k V, for the column above the level (its own storey shear and height) and the column below.", "Moment column: H h/2 dengan H = k V, bagi column di atas aras (storey shear dan ketinggiannya sendiri) dan column di bawah."); },
            function () { return bi("At A: M<sub>AB</sub> = M<sub>col,above</sub> + M<sub>col,below</sub>. At B: M<sub>BC</sub> = M<sub>col,above</sub> + M<sub>col,below</sub> − M<sub>AB</sub>.", "Di A: M<sub>AB</sub> = M<sub>col,atas</sub> + M<sub>col,bawah</sub>. Di B: M<sub>BC</sub> = M<sub>col,atas</sub> + M<sub>col,bawah</sub> − M<sub>AB</sub>."); },
            function () { return bi("The moment is zero at mid-span, so F = 2M/L.", "Moment sifar di tengah span, jadi F = 2M/L."); }],
    solution: function (P) {
      return sol(["k<sub>A</sub> = " + f3(P.kA) + ", k<sub>B</sub> = " + f3(P.kB),
        bi("A: ", "A: ") + f3(P.kA) + " × " + f2(P.Va) + " × " + fmt(P.ha / 2, 2) + " + " + f3(P.kA) + " × " + f2(P.V) + " × " + fmt(P.h / 2, 2) + " = " + f2(P.MuA) + " + " + f2(P.MlA) + " = " + f2(P.MAB) + " kN m",
        bi("B: ", "B: ") + f2(P.MuB) + " + " + f2(P.MlB) + " − " + f2(P.MAB) + " = " + f2(P.MBC) + " kN m",
        "F<sub>AB</sub> = 2 × " + f2(P.MAB) + "/" + fmt(P.L[0], 1) + " = " + f2(P.F) + " kN " + bi("(every beam at this level carries the same shear)", "(setiap beam pada aras ini membawa shear yang sama)")]);
    }
  });

  /* ---------- B3 cantilever method: centroid and the axial force of the windward column, top storey ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.n = pick(r, [3, 3, 4]);
      P.L = P.n === 3 ? [pick(r, [4, 5, 6, 7]), pick(r, [3, 4, 5, 6, 8])] : [pick(r, [5, 6, 7]), pick(r, [4, 5, 6]), pick(r, [5, 6, 8])];
      P.x = [0]; for (var i = 0; i < P.L.length; i++) P.x.push(P.x[i] + P.L[i]);
      P.F = step(r, 6, 20, 0.1); P.h = pick(r, [3.0, 3.5, 4.0]);
      var s = 0; for (i = 0; i < P.n; i++) s += P.x[i]; P.xbar = s / P.n;
      P.d = P.x.map(function (v) { return v - P.xbar; });
      P.dmin = Math.min.apply(null, P.d.map(Math.abs).filter(function (v) { return v > 1e-9; }));
      P.srd = 0; for (i = 0; i < P.n; i++) P.srd += P.d[i] * P.d[i] / P.dmin;
      P.Mo = P.F * P.h / 2; P.P = P.Mo / P.srd; P.NA = Math.abs(P.d[0]) / P.dmin * P.P;
      if (P.dmin < 0.5) return this.gen(r);
      return P;
    },
    text: function (P) {
      return bi("A frame has " + P.n + " columns of equal area at x = " + num(P.x.map(function (v) { return fmt(v, 1); }).join(", ")) + " m. The roof force is " + num(fmt(P.F, 1)) + " kN, from the left, and the top storey is " + num(fmt(P.h, 1)) + " m high. By the cantilever method, find the centroid of the columns and the axial force in the windward column A of the top storey.",
                "Sebuah frame mempunyai " + P.n + " column dengan luas yang sama pada x = " + num(P.x.map(function (v) { return fmt(v, 1); }).join(", ")) + " m. Daya bumbung ialah " + num(fmt(P.F, 1)) + " kN, dari kiri, dan tingkat teratas setinggi " + num(fmt(P.h, 1)) + " m. Dengan cantilever method, cari centroid column dan axial force dalam column windward A bagi tingkat teratas.");
    },
    fields: [{ id: "x", label: ["<span style='text-decoration:overline'>x</span>", "<span style='text-decoration:overline'>x</span>"], unit: "m", fn: function (P) { return P.xbar; }, rtol: 0.01 },
             { id: "n", label: ["N<sub>A</sub>", "N<sub>A</sub>"], unit: "kN", fn: function (P) { return P.NA; }, rtol: 0.015 }],
    hints: [function () { return bi("Equal areas: <span style='text-decoration:overline'>x</span> is the average position. Cut the top storey at mid-height: M<sub>o</sub> = F × h/2.", "Luas sama: <span style='text-decoration:overline'>x</span> ialah purata kedudukan. Potong tingkat teratas di tengah ketinggian: M<sub>o</sub> = F × h/2."); },
            function () { return bi("r<sub>i</sub> = d<sub>i</sub>/d<sub>min</sub>; P = M<sub>o</sub>/Σ|r||d|.", "r<sub>i</sub> = d<sub>i</sub>/d<sub>min</sub>; P = M<sub>o</sub>/Σ|r||d|."); },
            function () { return bi("N<sub>A</sub> = |r<sub>A</sub>| P, in tension (windward side).", "N<sub>A</sub> = |r<sub>A</sub>| P, dalam tegangan (sisi windward)."); }],
    solution: function (P) {
      var r = P.d.map(function (v) { return v / P.dmin; });
      return sol(["<span style='text-decoration:overline'>x</span> = (" + P.x.map(function (v) { return fmt(v, 1); }).join(" + ") + ")/" + P.n + " = " + f2(P.xbar) + " m; d = " + P.d.map(f2).join(", ") + " m",
        "r = " + r.map(f2).join(", ") + "; Σ|r||d| = " + f2(P.srd) + " m",
        "M<sub>o</sub> = " + fmt(P.F, 1) + " × " + fmt(P.h / 2, 2) + " = " + f2(P.Mo) + " kN m; P = " + f2(P.Mo) + "/" + f2(P.srd) + " = " + f3(P.P) + " kN",
        "N<sub>A</sub> = " + f2(Math.abs(r[0])) + " × " + f3(P.P) + " = " + f2(P.NA) + " kN " + bi("(tension)", "(tegangan)")]);
    }
  });

  /* ---------- B4 cantilever method: the beam shear and the column shear at A, top storey of a two-bay frame ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = {};
      P.L = [pick(r, [4, 5, 6, 7, 8]), pick(r, [4, 5, 6, 7, 8])];
      if (P.L[0] === P.L[1]) P.L[1] = P.L[1] === 8 ? 5 : P.L[1] + 1;
      P.x = [0, P.L[0], P.L[0] + P.L[1]];
      P.F = step(r, 6, 20, 0.1); P.h = pick(r, [3.0, 3.5, 4.0]);
      P.xbar = (P.x[0] + P.x[1] + P.x[2]) / 3;
      P.d = P.x.map(function (v) { return v - P.xbar; });
      P.dmin = Math.min.apply(null, P.d.map(Math.abs));
      if (P.dmin < 0.3) return this.gen(r);
      P.srd = 0; for (var i = 0; i < 3; i++) P.srd += P.d[i] * P.d[i] / P.dmin;
      P.Mo = P.F * P.h / 2; P.P = P.Mo / P.srd;
      P.NA = Math.abs(P.d[0]) / P.dmin * P.P;            /* tension */
      P.FAB = P.NA;                                        /* beam shear at the AB cut: the axial change to its left */
      P.HA = P.NA * (P.L[0] / 2) / (P.h / 2);              /* moments about the AB cut */
      return P;
    },
    text: function (P) {
      return bi("A two-bay frame has spans AB = " + num(fmt(P.L[0], 1)) + " m and BC = " + num(fmt(P.L[1], 1)) + " m, columns of equal area. The roof force is " + num(fmt(P.F, 1)) + " kN, from the left; the top storey is " + num(fmt(P.h, 1)) + " m high. By the cantilever method, find for the top storey the shear in beam AB at its mid-span and the shear in column A at its mid-height.",
                "Sebuah frame dua bay mempunyai span AB = " + num(fmt(P.L[0], 1)) + " m dan BC = " + num(fmt(P.L[1], 1)) + " m, column dengan luas yang sama. Daya bumbung ialah " + num(fmt(P.F, 1)) + " kN, dari kiri; tingkat teratas setinggi " + num(fmt(P.h, 1)) + " m. Dengan cantilever method, cari bagi tingkat teratas shear dalam beam AB di tengah span-nya dan shear dalam column A di tengah ketinggiannya.");
    },
    fields: [{ id: "f", label: ["F<sub>AB</sub>", "F<sub>AB</sub>"], unit: "kN", fn: function (P) { return P.FAB; }, rtol: 0.015 },
             { id: "h", label: ["H<sub>A</sub>", "H<sub>A</sub>"], unit: "kN", fn: function (P) { return P.HA; }, rtol: 0.015 }],
    hints: [function () { return bi("First the axial force in A: <span style='text-decoration:overline'>x</span>, the ratios r = d/d<sub>min</sub>, P = M<sub>o</sub>/Σ|r||d| with M<sub>o</sub> = F h/2.", "Mula-mula axial force dalam A: <span style='text-decoration:overline'>x</span>, nisbah r = d/d<sub>min</sub>, P = M<sub>o</sub>/Σ|r||d| dengan M<sub>o</sub> = F h/2."); },
            function () { return bi("The part left of the cut through beam AB at mid-span holds column A only: the beam shear balances N<sub>A</sub>.", "Bahagian di kiri keratan beam AB di tengah span hanya mengandungi column A: shear beam mengimbangi N<sub>A</sub>."); },
            function () { return bi("Moments about the beam cut for the same part: H<sub>A</sub> × h/2 = N<sub>A</sub> × L<sub>AB</sub>/2.", "Moment terhadap keratan beam bagi bahagian yang sama: H<sub>A</sub> × h/2 = N<sub>A</sub> × L<sub>AB</sub>/2."); }],
    solution: function (P) {
      var r = P.d.map(function (v) { return v / P.dmin; });
      return sol(["<span style='text-decoration:overline'>x</span> = " + f2(P.xbar) + " m; d = " + P.d.map(f2).join(", ") + " m; r = " + r.map(f2).join(", ") + "; Σ|r||d| = " + f2(P.srd) + " m",
        "M<sub>o</sub> = " + fmt(P.F, 1) + " × " + fmt(P.h / 2, 2) + " = " + f2(P.Mo) + " kN m; P = " + f3(P.P) + " kN; N<sub>A</sub> = " + f2(P.NA) + " kN " + bi("(tension)", "(tegangan)"),
        "F<sub>AB</sub> = N<sub>A</sub> = " + f2(P.FAB) + " kN",
        "H<sub>A</sub> = " + f2(P.NA) + " × " + fmt(P.L[0] / 2, 2) + "/" + fmt(P.h / 2, 2) + " = " + f2(P.HA) + " kN"]);
    }
  });

  /* ---------- B5 combination at a beam: the larger hogging and the reversal ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P = {};
      P.ML = step(r, 20, 140, 0.5); P.MR = step(r, 60, 220, 0.5);
      P.Mw = step(r, 15, 120, 0.5);
      P.hog = Math.max(P.ML, P.MR) + P.Mw;
      P.rev = Math.max(0, P.Mw - Math.min(P.ML, P.MR));
      return P;
    },
    text: function (P) {
      return bi("At level 1 of an unbraced frame, a beam has hogging moments of " + num(f2(P.ML)) + " kN m at its left end and " + num(f2(P.MR)) + " kN m at its right end under 1.2(G<sub>k</sub> + Q<sub>k</sub>). The wind, 1.2W<sub>k</sub>, gives it a moment of " + num(f2(P.Mw)) + " kN m at each end. By the course method, find the largest hogging moment at an end of the beam, and the sagging moment of a reversal (enter 0 if none).",
                "Pada aras 1 sebuah unbraced frame, sebatang beam mempunyai moment hogging " + num(f2(P.ML)) + " kN m di hujung kirinya dan " + num(f2(P.MR)) + " kN m di hujung kanannya di bawah 1.2(G<sub>k</sub> + Q<sub>k</sub>). Angin, 1.2W<sub>k</sub>, memberinya moment " + num(f2(P.Mw)) + " kN m di setiap hujung. Mengikut course method, cari moment hogging terbesar di hujung beam, dan moment sagging bagi reversal (masukkan 0 jika tiada).");
    },
    fields: [{ id: "h", label: ["Largest hogging", "Hogging terbesar"], unit: "kN m", fn: function (P) { return P.hog; }, rtol: 0.01 },
             { id: "r", label: ["Reversal (sagging)", "Reversal (sagging)"], unit: "kN m", fn: function (P) { return P.rev; }, rtol: 0.01, atol: 0.05 }],
    hints: [function () { return bi("The wind hogs one end and relieves the other; each wind direction in turn.", "Angin menyebabkan hogging di satu hujung dan melegakan hujung yang lain; setiap arah angin secara bergilir."); },
            function () { return bi("Largest hogging: the larger vertical end moment plus M<sub>w</sub>.", "Hogging terbesar: moment hujung menegak yang lebih besar ditambah M<sub>w</sub>."); },
            function () { return bi("Reversal at the smaller end: M<sub>w</sub> − M<sub>v</sub>, if positive.", "Reversal di hujung yang lebih kecil: M<sub>w</sub> − M<sub>v</sub>, jika positif."); }],
    solution: function (P) {
      var big = Math.max(P.ML, P.MR), small = Math.min(P.ML, P.MR);
      return sol([bi("Largest hogging: ", "Hogging terbesar: ") + f2(big) + " + " + f2(P.Mw) + " = " + f2(P.hog) + " kN m",
        bi("Relieved end: ", "Hujung dilegakan: ") + f2(P.Mw) + " − " + f2(small) + " = " + f2(P.Mw - small) + (P.rev > 0 ? bi(" > 0: a reversal of " + f2(P.rev) + " kN m sagging", " > 0: reversal " + f2(P.rev) + " kN m sagging") : bi(" ≤ 0: no reversal", " ≤ 0: tiada reversal"))]);
    }
  });

  /* ---------- B6 cantilever method: the storey shear and the overturning moment at a cut ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.hg = pick(r, [3.5, 4.0, 4.5]); P.ht = pick(r, [3.0, 3.5]);
      P.z = [P.hg + 2 * P.ht, P.hg + P.ht, P.hg];
      P.F = [step(r, 5, 15, 0.1), step(r, 10, 25, 0.1), step(r, 10, 25, 0.1)];
      P.zc = P.hg / 2;
      P.V = P.F[0] + P.F[1] + P.F[2];
      P.Mo = P.F[0] * (P.z[0] - P.zc) + P.F[1] * (P.z[1] - P.zc) + P.F[2] * (P.z[2] - P.zc);
      return P;
    },
    text: function (P) {
      return bi("A three-storey frame carries design wind forces of " + num(fmt(P.F[0], 1)) + " kN at the roof (z = " + num(fmt(P.z[0], 1)) + " m), " + num(fmt(P.F[1], 1)) + " kN at level 2 (z = " + num(fmt(P.z[1], 1)) + " m) and " + num(fmt(P.F[2], 1)) + " kN at level 1 (z = " + num(fmt(P.z[2], 1)) + " m). The ground storey is " + num(fmt(P.hg, 1)) + " m high. Find the storey shear of the ground storey and the overturning moment about its cut at mid-height.",
                "Sebuah frame tiga tingkat menanggung daya angin rekabentuk " + num(fmt(P.F[0], 1)) + " kN di bumbung (z = " + num(fmt(P.z[0], 1)) + " m), " + num(fmt(P.F[1], 1)) + " kN pada aras 2 (z = " + num(fmt(P.z[1], 1)) + " m) dan " + num(fmt(P.F[2], 1)) + " kN pada aras 1 (z = " + num(fmt(P.z[2], 1)) + " m). Tingkat bawah setinggi " + num(fmt(P.hg, 1)) + " m. Cari storey shear tingkat bawah dan overturning moment terhadap keratannya di tengah ketinggian.");
    },
    fields: [{ id: "v", label: ["V", "V"], unit: "kN", fn: function (P) { return P.V; }, rtol: 0.01 },
             { id: "m", label: ["M<sub>o</sub>", "M<sub>o</sub>"], unit: "kN m", fn: function (P) { return P.Mo; }, rtol: 0.01 }],
    hints: [function () { return bi("The cut is at the mid-height of the ground storey, z = h<sub>g</sub>/2.", "Keratan berada di tengah ketinggian tingkat bawah, z = h<sub>g</sub>/2."); },
            function () { return bi("V = the sum of every force above the cut.", "V = jumlah setiap daya di atas keratan."); },
            function () { return bi("M<sub>o</sub> = Σ F × (z − z<sub>cut</sub>): each lever arm from the cut, not from the ground.", "M<sub>o</sub> = Σ F × (z − z<sub>cut</sub>): setiap lengan tuas dari keratan, bukan dari tanah."); }],
    solution: function (P) {
      return sol(["z<sub>cut</sub> = " + fmt(P.hg, 1) + "/2 = " + fmt(P.zc, 2) + " m; V = " + P.F.map(function (v) { return fmt(v, 1); }).join(" + ") + " = " + f2(P.V) + " kN",
        "M<sub>o</sub> = " + P.F.map(function (v, k) { return fmt(v, 1) + " × " + fmt(P.z[k] - P.zc, 2); }).join(" + ") + " = " + f2(P.Mo) + " kN m"]);
    }
  });
})();
