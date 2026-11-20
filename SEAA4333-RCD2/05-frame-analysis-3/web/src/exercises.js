/* SEAA 4333 Unit 5 · Part B exercises: new numbers on every attempt (seeded, stored with the student's progress).
   Every number follows MS 1553:2002 as the course uses it (the RC Design app's wind, verified against the app):
   V_sit = V_s M_d M_z,cat M_s M_h (M_d = M_s = M_h = 1); V_des = V_sit I; V_des,z = V_des M_z,cat(z)/M_z,cat(h);
   M_z,cat from Table 4.1, linear between the tabulated heights; p = 0.613 V^2 C_fig C_dyn / 1000 in kN/m^2;
   windward C_p,e = 0.8 with V_des,z; leeward C_p,e from Table 5.2(b) (roof pitch < 10 deg) with V_des at z = h;
   W_k = (p_W - p_L) B_w h_trib; minimum 0.65 kN/m^2 on the average net pressure (2.4.2, A2.2);
   EC2 5.2: theta_i = (1/200) alpha_h alpha_m, alpha_h = 2/sqrt(l) within [2/3, 1], alpha_m = sqrt(0.5(1 + 1/m)), H_i = theta_i N. */
(function () {
  "use strict";
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr) { return arr[Math.floor(r() * arr.length)]; }
  function step(r, a, b, s) { var n = Math.round((b - a) / s); return +(a + s * Math.floor(r() * (n + 1))).toFixed(6); }
  function num(v) { return '<span class="num">' + v + '</span>'; }
  function sol(lines) { return "<h5>" + bi("Solution with these numbers", "Penyelesaian dengan nombor ini") + '</h5><p class="num">' + lines.join("<br>") + "</p>"; }
  function f2(v) { return fmt(v, 2); }
  function f3(v) { return fmt(v, 3); }
  var MZ_H = [3, 5, 10, 15, 20, 30, 40, 50];
  var MZ = { 2: [0.85, 0.91, 1.00, 1.05, 1.08, 1.12, 1.16, 1.18], 3: [0.75, 0.75, 0.83, 0.89, 0.94, 1.00, 1.04, 1.07], 4: [0.75, 0.75, 0.75, 0.75, 0.75, 0.80, 0.85, 0.90] };
  function interp(xs, ys, x) {
    if (x <= xs[0]) return ys[0]; if (x >= xs[xs.length - 1]) return ys[ys.length - 1];
    for (var i = 1; i < xs.length; i++) if (x <= xs[i]) { var t = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + t * (ys[i] - ys[i - 1]); }
    return ys[ys.length - 1];
  }
  function mz(tc, z) { return interp(MZ_H, MZ[tc], z); }
  function cpl(db) { return interp([1, 2, 4], [-0.5, -0.3, -0.2], db); }
  function rowText(tc) {
    return bi("Table 4.1, terrain category " + tc + ": ", "Table 4.1, terrain category " + tc + ": ") + MZ_H.map(function (h, k) { return h + " m " + fmt(MZ[tc][k], 2); }).join(", ") + ".";
  }
  var TCN = { 2: ["open terrain with scattered obstructions (category 2)", "terrain terbuka dengan halangan berselerak (category 2)"],
              3: ["a suburb of houses (category 3)", "kawasan perumahan pinggir bandar (category 3)"],
              4: ["a city centre with tall buildings (category 4)", "pusat bandar dengan bangunan tinggi (category 4)"] };

  /* ---------- B1 the design wind speed at the roof and at a level ---------- */
  EX.define("b1", {
    gen: function (r) {
      var P = {};
      P.tc = pick(r, [2, 3, 3, 4]); P.Vs = pick(r, [32.5, 33.5]); P.cat = pick(r, [2, 2, 3]);
      P.n = pick(r, [4, 5, 6, 7, 8]); P.hg = pick(r, [4.0, 4.5]); P.ht = pick(r, [3.0, 3.5]);
      P.h = P.hg + (P.n - 1) * P.ht; P.k = 1 + Math.floor(r() * (P.n - 1)); P.z = P.hg + (P.k - 1) * P.ht;
      P.I = P.cat === 3 ? 1.15 : 1.0; P.mzh = mz(P.tc, P.h); P.mzz = mz(P.tc, P.z);
      P.Vsit = P.Vs * P.mzh; P.Vdes = P.Vsit * P.I; P.Vz = P.Vdes * P.mzz / P.mzh;
      return P;
    },
    text: function (P) {
      var use = P.cat === 3 ? ["an exhibition hall where up to 500 people gather", "dewan pameran yang menghimpunkan sehingga 500 orang"] : ["an office building", "bangunan pejabat"];
      return bi("A " + num(P.n) + "-storey frame building, " + use[0] + ", stands in " + TCN[P.tc][0] + " on level ground, with V<sub>s</sub> = " + num(P.Vs) + " m/s. The ground storey is " + num(P.hg) + " m and the others " + num(P.ht) + " m, so the roof is at h = " + num(f2(P.h)) + " m. ",
                "Sebuah bangunan frame " + num(P.n) + " tingkat, " + use[1] + ", terletak di " + TCN[P.tc][1] + " di atas tanah rata, dengan V<sub>s</sub> = " + num(P.Vs) + " m/s. Tingkat bawah setinggi " + num(P.hg) + " m dan yang lain " + num(P.ht) + " m, jadi bumbung pada h = " + num(f2(P.h)) + " m. ") + rowText(P.tc) +
        bi(" Find V<sub>des</sub> at the roof and V<sub>des,z</sub> at level " + P.k + " (z = " + f2(P.z) + " m).", " Cari V<sub>des</sub> di bumbung dan V<sub>des,z</sub> pada aras " + P.k + " (z = " + f2(P.z) + " m).");
    },
    fields: [{ id: "v", label: ["V<sub>des</sub>", "V<sub>des</sub>"], unit: "m/s", fn: function (P) { return P.Vdes; }, rtol: 0.01 },
             { id: "z", label: ["V<sub>des,z</sub>", "V<sub>des,z</sub>"], unit: "m/s", fn: function (P) { return P.Vz; }, rtol: 0.01 }],
    hints: [function (P) { return bi("Interpolate M<sub>z,cat</sub> linearly between the two tabulated heights on either side of h, and again at z.", "Interpolasi M<sub>z,cat</sub> secara linear di antara dua ketinggian dalam jadual di kedua-dua sisi h, dan sekali lagi pada z."); },
            function (P) { return bi("V<sub>sit</sub> = V<sub>s</sub>M<sub>z,cat</sub>(h) with M<sub>d</sub> = M<sub>s</sub> = M<sub>h</sub> = 1.0; I from Table 3.2: 1.15 where more than 300 people gather, 1.0 for offices.", "V<sub>sit</sub> = V<sub>s</sub>M<sub>z,cat</sub>(h) dengan M<sub>d</sub> = M<sub>s</sub> = M<sub>h</sub> = 1.0; I daripada Table 3.2: 1.15 jika lebih daripada 300 orang berkumpul, 1.0 bagi pejabat."); },
            function (P) { return bi("V<sub>des,z</sub> = V<sub>des</sub> × M<sub>z,cat</sub>(z)/M<sub>z,cat</sub>(h).", "V<sub>des,z</sub> = V<sub>des</sub> × M<sub>z,cat</sub>(z)/M<sub>z,cat</sub>(h)."); }],
    solution: function (P) {
      return sol(["M<sub>z,cat</sub>(" + f2(P.h) + " m) = " + f3(P.mzh) + "; V<sub>sit</sub> = " + P.Vs + " × " + f3(P.mzh) + " = " + f2(P.Vsit) + " m/s",
        "I = " + f2(P.I) + "; V<sub>des</sub> = " + f2(P.Vsit) + " × " + f2(P.I) + " = " + f2(P.Vdes) + " m/s",
        "M<sub>z,cat</sub>(" + f2(P.z) + " m) = " + f3(P.mzz) + "; V<sub>des,z</sub> = " + f2(P.Vdes) + " × " + f3(P.mzz) + "/" + f3(P.mzh) + " = " + f2(P.Vz) + " m/s"]);
    }
  });

  /* ---------- B2 the leeward suction: which face, d/b, C_p,e and p_L ---------- */
  EX.define("b2", {
    gen: function (r) {
      var P = {};
      P.L = pick(r, [30, 36, 42, 48, 54, 60]); P.W = pick(r, [12, 15, 18, 20, 24]);
      P.dir = pick(r, ["across", "along"]);        // frames span the width W ("across") or run along the length L
      if (P.dir === "across") { P.b = P.L; P.d = P.W; } else { P.b = P.W; P.d = P.L; }
      P.Vdes = step(r, 30, 40, 0.1); P.Cd = pick(r, [1.0, 1.0, step(r, 1.05, 1.35, 0.01)]);
      P.db = P.d / P.b; P.cpl = cpl(P.db); P.pL = 0.613 * P.Vdes * P.Vdes * P.cpl * P.Cd / 1000;
      return P;
    },
    text: function (P) {
      var fr = P.dir === "across" ? ["frames that span the " + P.W + " m width", "frame yang merentang lebar " + P.W + " m"] : ["frame lines that run along the " + P.L + " m length", "frame line yang memanjang sepanjang " + P.L + " m"];
      return bi("A building is " + num(P.L) + " m long and " + num(P.W) + " m wide, with a flat roof. Consider the " + fr[0] + ". At the roof V<sub>des</sub> = " + num(f2(P.Vdes)) + " m/s and C<sub>dyn</sub> = " + num(f2(P.Cd)) + ". Table 5.2(b), roof pitch below 10°: d/b ≤ 1, −0.5; d/b = 2, −0.3; d/b ≥ 4, −0.2. Find C<sub>p,e</sub> of the leeward wall for the wind these frames carry, and the leeward pressure p<sub>L</sub>.",
                "Sebuah bangunan sepanjang " + num(P.L) + " m dan selebar " + num(P.W) + " m, dengan bumbung rata. Pertimbangkan " + fr[1] + ". Di bumbung V<sub>des</sub> = " + num(f2(P.Vdes)) + " m/s dan C<sub>dyn</sub> = " + num(f2(P.Cd)) + ". Table 5.2(b), kecerunan bumbung di bawah 10°: d/b ≤ 1, −0.5; d/b = 2, −0.3; d/b ≥ 4, −0.2. Cari C<sub>p,e</sub> dinding leeward bagi angin yang ditanggung frame ini, dan tekanan leeward p<sub>L</sub>.");
    },
    fields: [{ id: "c", label: ["C<sub>p,e</sub>", "C<sub>p,e</sub>"], unit: "", fn: function (P) { return P.cpl; }, rtol: 0.02 },
             { id: "p", label: ["p<sub>L</sub>", "p<sub>L</sub>"], unit: "kN/m²", fn: function (P) { return P.pL; }, rtol: 0.02 }],
    hints: [function () { return bi("A plane frame carries the wind that blows in its own plane. The face it blows on is b, the depth along the wind is d.", "Plane frame menanggung angin yang bertiup dalam satahnya sendiri. Muka yang ditiup ialah b, dalam sepanjang arah angin ialah d."); },
            function () { return bi("Interpolate C<sub>p,e</sub> linearly in d/b between the columns of the table.", "Interpolasi C<sub>p,e</sub> secara linear dalam d/b di antara lajur jadual."); },
            function () { return bi("p<sub>L</sub> = 0.613 V<sub>des</sub>² C<sub>p,e</sub> C<sub>dyn</sub>/1000, the speed at the roof for every level; it comes out negative (suction).", "p<sub>L</sub> = 0.613 V<sub>des</sub>² C<sub>p,e</sub> C<sub>dyn</sub>/1000, laju di bumbung bagi setiap aras; nilainya negatif (suction)."); }],
    solution: function (P) {
      return sol([bi("The frames carry the wind blowing onto the " + P.b + " m face: b = " + P.b + " m, d = " + P.d + " m, d/b = " + f3(P.db), "Frame menanggung angin yang bertiup ke atas muka " + P.b + " m: b = " + P.b + " m, d = " + P.d + " m, d/b = " + f3(P.db)),
        "C<sub>p,e</sub> = " + f3(P.cpl),
        "p<sub>L</sub> = 0.613 × " + f2(P.Vdes) + "² × (" + f3(P.cpl) + ") × " + f2(P.Cd) + "/1000 = " + f3(P.pL) + " kN/m²"]);
    }
  });

  /* ---------- B3 the net pressure at a level ---------- */
  EX.define("b3", {
    gen: function (r) {
      var P = {};
      P.tc = pick(r, [2, 3]); P.h = pick(r, [18, 21, 22.5, 25, 28]); P.z = pick(r, [4, 7.5, 11, 14.5]);
      P.Vdes = step(r, 30, 40, 0.1); P.Cd = pick(r, [1.0, step(r, 1.05, 1.35, 0.01)]); P.cpl = pick(r, [-0.5, -0.5, -0.4, -0.3]);
      P.mzh = mz(P.tc, P.h); P.mzz = mz(P.tc, P.z); P.Vz = P.Vdes * P.mzz / P.mzh;
      P.pW = 0.613 * P.Vz * P.Vz * 0.8 * P.Cd / 1000; P.pL = 0.613 * P.Vdes * P.Vdes * P.cpl * P.Cd / 1000; P.net = P.pW - P.pL;
      return P;
    },
    text: function (P) {
      return bi("A building with its roof at h = " + num(P.h) + " m stands in terrain category " + P.tc + ". At the roof V<sub>des</sub> = " + num(f2(P.Vdes)) + " m/s; C<sub>dyn</sub> = " + num(f2(P.Cd)) + "; the leeward C<sub>p,e</sub> = " + num(f2(P.cpl)) + ". ",
                "Sebuah bangunan dengan bumbung pada h = " + num(P.h) + " m terletak dalam terrain category " + P.tc + ". Di bumbung V<sub>des</sub> = " + num(f2(P.Vdes)) + " m/s; C<sub>dyn</sub> = " + num(f2(P.Cd)) + "; C<sub>p,e</sub> leeward = " + num(f2(P.cpl)) + ". ") + rowText(P.tc) +
        bi(" Find the windward pressure p<sub>W</sub> and the net pressure p<sub>W</sub> − p<sub>L</sub> at z = " + P.z + " m.", " Cari tekanan windward p<sub>W</sub> dan net pressure p<sub>W</sub> − p<sub>L</sub> pada z = " + P.z + " m.");
    },
    fields: [{ id: "w", label: ["p<sub>W</sub>", "p<sub>W</sub>"], unit: "kN/m²", fn: function (P) { return P.pW; }, rtol: 0.015 },
             { id: "n", label: ["p<sub>W</sub> − p<sub>L</sub>", "p<sub>W</sub> − p<sub>L</sub>"], unit: "kN/m²", fn: function (P) { return P.net; }, rtol: 0.015 }],
    hints: [function () { return bi("The windward wall uses the speed at its own level: V<sub>des,z</sub> = V<sub>des</sub>M<sub>z,cat</sub>(z)/M<sub>z,cat</sub>(h), with C<sub>p,e</sub> = 0.8.", "Dinding windward menggunakan laju pada arasnya sendiri: V<sub>des,z</sub> = V<sub>des</sub>M<sub>z,cat</sub>(z)/M<sub>z,cat</sub>(h), dengan C<sub>p,e</sub> = 0.8."); },
            function () { return bi("The leeward wall uses V<sub>des</sub> at the roof for every level.", "Dinding leeward menggunakan V<sub>des</sub> di bumbung bagi setiap aras."); },
            function () { return bi("Both push the frame downwind: net = p<sub>W</sub> − p<sub>L</sub>, and p<sub>L</sub> is negative, so the net is larger than p<sub>W</sub>.", "Kedua-duanya menolak frame ke arah angin: net = p<sub>W</sub> − p<sub>L</sub>, dan p<sub>L</sub> negatif, jadi net lebih besar daripada p<sub>W</sub>."); }],
    solution: function (P) {
      return sol(["M<sub>z,cat</sub>(h) = " + f3(P.mzh) + ", M<sub>z,cat</sub>(z) = " + f3(P.mzz) + "; V<sub>des,z</sub> = " + f2(P.Vdes) + " × " + f3(P.mzz) + "/" + f3(P.mzh) + " = " + f2(P.Vz) + " m/s",
        "p<sub>W</sub> = 0.613 × " + f2(P.Vz) + "² × 0.8 × " + f2(P.Cd) + "/1000 = " + f3(P.pW) + " kN/m²",
        "p<sub>L</sub> = 0.613 × " + f2(P.Vdes) + "² × (" + f2(P.cpl) + ") × " + f2(P.Cd) + "/1000 = " + f3(P.pL) + "; p<sub>W</sub> − p<sub>L</sub> = " + f3(P.net) + " kN/m²"]);
    }
  });

  /* ---------- B4 the force on the frame at one level ---------- */
  EX.define("b4", {
    gen: function (r) {
      var P = {};
      P.s1 = pick(r, [4, 4.5, 5, 6, 7.5]); P.s2 = pick(r, [4, 5, 6, 7.5, 8]); P.hg = pick(r, [3.5, 4.0, 4.5]); P.ht = pick(r, [3.0, 3.2, 3.5, 4.0]);
      P.lev = pick(r, ["roof", "mid", "one"]); P.p = step(r, 0.60, 1.60, 0.005);
      P.Bw = (P.s1 + P.s2) / 2; P.hT = P.lev === "roof" ? P.ht / 2 : P.lev === "one" ? (P.hg + P.ht) / 2 : P.ht; P.Wk = P.p * P.Bw * P.hT;
      return P;
    },
    text: function (P) {
      var lv = P.lev === "roof" ? ["the roof", "bumbung"] : P.lev === "one" ? ["level 1, the first floor above the ground storey", "aras 1, lantai pertama di atas tingkat bawah"] : ["a floor between two typical storeys", "satu lantai di antara dua tingkat biasa"];
      return bi("A frame stands between bays of " + num(P.s1) + " m and " + num(P.s2) + " m. The ground storey is " + num(P.hg) + " m high and every storey above it " + num(P.ht) + " m. At " + lv[0] + " the net pressure is p<sub>W</sub> − p<sub>L</sub> = " + num(f3(P.p)) + " kN/m². Find the height the level carries and the force W<sub>k</sub> on the frame there.",
                "Sebuah frame terletak di antara bay " + num(P.s1) + " m dan " + num(P.s2) + " m. Tingkat bawah setinggi " + num(P.hg) + " m dan setiap tingkat di atasnya " + num(P.ht) + " m. Pada " + lv[1] + " net pressure ialah p<sub>W</sub> − p<sub>L</sub> = " + num(f3(P.p)) + " kN/m². Cari ketinggian yang ditanggung aras itu dan daya W<sub>k</sub> pada frame di situ.");
    },
    fields: [{ id: "h", label: ["h<sub>trib</sub>", "h<sub>trib</sub>"], unit: "m", fn: function (P) { return P.hT; }, rtol: 0.005 },
             { id: "w", label: ["W<sub>k</sub>", "W<sub>k</sub>"], unit: "kN", fn: function (P) { return P.Wk; }, rtol: 0.01 }],
    hints: [function () { return bi("B<sub>w</sub> is half the bay on each side of the frame.", "B<sub>w</sub> ialah separuh bay pada setiap sisi frame."); },
            function () { return bi("Each floor carries half the storey above and half the storey below; the roof has no storey above; level 1 sits between two different storeys.", "Setiap lantai menanggung separuh tingkat di atas dan separuh tingkat di bawah; bumbung tiada tingkat di atasnya; aras 1 terletak di antara dua tingkat yang berbeza."); },
            function () { return bi("W<sub>k</sub> = (p<sub>W</sub> − p<sub>L</sub>) × B<sub>w</sub> × h<sub>trib</sub>.", "W<sub>k</sub> = (p<sub>W</sub> − p<sub>L</sub>) × B<sub>w</sub> × h<sub>trib</sub>."); }],
    solution: function (P) {
      var hl = P.lev === "roof" ? P.ht + "/2" : P.lev === "one" ? "(" + P.hg + " + " + P.ht + ")/2" : P.ht + "/2 + " + P.ht + "/2";
      return sol(["B<sub>w</sub> = " + P.s1 + "/2 + " + P.s2 + "/2 = " + f2(P.Bw) + " m", "h<sub>trib</sub> = " + hl + " = " + f2(P.hT) + " m",
        "W<sub>k</sub> = " + f3(P.p) + " × " + f2(P.Bw) + " × " + f2(P.hT) + " = " + f2(P.Wk) + " kN"]);
    }
  });

  /* ---------- B5 the minimum design wind load ---------- */
  EX.define("b5", {
    gen: function (r) {
      var P = {};
      P.hg = pick(r, [3.5, 4.0, 4.5]); P.ht = pick(r, [3.0, 3.5]); P.H = P.hg + 2 * P.ht;
      P.p3 = step(r, 0.50, 0.85, 0.005); P.p2 = +(P.p3 - step(r, 0.03, 0.06, 0.005)).toFixed(3); P.p1 = +(P.p2 - step(r, 0.02, 0.05, 0.005)).toFixed(3); P.pb = P.p1;
      P.sum = P.p3 * P.ht / 2 + P.p2 * P.ht + P.p1 * (P.hg + P.ht) / 2 + P.pb * P.hg / 2;
      P.pavg = P.sum / P.H; P.k = Math.max(1, 0.65 / P.pavg);
      return P;
    },
    text: function (P) {
      return bi("A three-storey frame has storeys of " + num(P.hg) + ", " + num(P.ht) + " and " + num(P.ht) + " m, roof at " + num(f2(P.H)) + " m. The net pressures are " + num(f3(P.p3)) + " kN/m² at the roof, " + num(f3(P.p2)) + " at level 2 and " + num(f3(P.p1)) + " at level 1; the bottom half of the ground storey takes " + num(f3(P.pb)) + ". Find the average net pressure over the height and the factor the level forces must be multiplied by (2.4.2).",
                "Sebuah frame tiga tingkat mempunyai tingkat " + num(P.hg) + ", " + num(P.ht) + " dan " + num(P.ht) + " m, bumbung pada " + num(f2(P.H)) + " m. Net pressure ialah " + num(f3(P.p3)) + " kN/m² di bumbung, " + num(f3(P.p2)) + " pada aras 2 dan " + num(f3(P.p1)) + " pada aras 1; separuh bawah tingkat bawah mengambil " + num(f3(P.pb)) + ". Cari purata net pressure sepanjang ketinggian dan faktor yang mesti didarab dengan daya aras (2.4.2).");
    },
    fields: [{ id: "a", label: ["p<sub>avg</sub>", "p<sub>avg</sub>"], unit: "kN/m²", fn: function (P) { return P.pavg; }, rtol: 0.01 },
             { id: "k", label: ["k", "k"], unit: "", fn: function (P) { return P.k; }, rtol: 0.01 }],
    hints: [function () { return bi("Weight each pressure by the height it covers: half a storey at the roof, a storey at level 2, half of each storey at level 1, half the ground storey at the bottom.", "Wajarkan setiap tekanan dengan ketinggian yang diliputinya: separuh tingkat di bumbung, satu tingkat pada aras 2, separuh setiap tingkat pada aras 1, separuh tingkat bawah di bahagian bawah."); },
            function () { return bi("p<sub>avg</sub> = Σ(p × height)/H, with H the height of the roof.", "p<sub>avg</sub> = Σ(p × ketinggian)/H, dengan H ketinggian bumbung."); },
            function () { return bi("k = 0.65/p<sub>avg</sub> when p<sub>avg</sub> < 0.65 kN/m²; otherwise k = 1.0.", "k = 0.65/p<sub>avg</sub> apabila p<sub>avg</sub> < 0.65 kN/m²; jika tidak, k = 1.0."); }],
    solution: function (P) {
      return sol(["Σ(p × h) = " + f3(P.p3) + " × " + f2(P.ht / 2) + " + " + f3(P.p2) + " × " + f2(P.ht) + " + " + f3(P.p1) + " × " + f2((P.hg + P.ht) / 2) + " + " + f3(P.pb) + " × " + f2(P.hg / 2) + " = " + f3(P.sum),
        "p<sub>avg</sub> = " + f3(P.sum) + "/" + f2(P.H) + " = " + f3(P.pavg) + " kN/m²",
        P.pavg < 0.65 ? bi("Below 0.65: k = 0.65/" + f3(P.pavg) + " = " + f3(P.k), "Di bawah 0.65: k = 0.65/" + f3(P.pavg) + " = " + f3(P.k)) : bi("Not below 0.65: the minimum does not govern, k = 1.0", "Tidak di bawah 0.65: minimum tidak menguasai, k = 1.0")]);
    }
  });

  /* ---------- B6 the EC2 geometric imperfections ---------- */
  EX.define("b6", {
    gen: function (r) {
      var P = {};
      P.l = pick(r, [6.5, 8, 10, 12.5, 15, 18, 21.5, 25, 32, 40]); P.m = pick(r, [3, 4, 5, 6]); P.N = step(r, 800, 2000, 25);
      P.ah0 = 2 / Math.sqrt(P.l); P.ah = Math.min(1, Math.max(2 / 3, P.ah0)); P.am = Math.sqrt(0.5 * (1 + 1 / P.m));
      P.th = P.ah * P.am / 200; P.inv = 1 / P.th; P.H = P.th * P.N;
      return P;
    },
    text: function (P) {
      return bi("An unbraced frame is " + num(P.l) + " m high and has " + num(P.m) + " columns. At one floor the vertical load that enters the frame is N = " + num(P.N) + " kN. With θ<sub>0</sub> = 1/200, find the inclination θ<sub>i</sub> (as 1 in …) and the horizontal force H<sub>i</sub> at that floor (EC2 5.2).",
                "Sebuah unbraced frame setinggi " + num(P.l) + " m dan mempunyai " + num(P.m) + " column. Pada satu lantai, load menegak yang memasuki frame ialah N = " + num(P.N) + " kN. Dengan θ<sub>0</sub> = 1/200, cari kecondongan θ<sub>i</sub> (sebagai 1 dalam …) dan daya mengufuk H<sub>i</sub> pada lantai itu (EC2 5.2).");
    },
    fields: [{ id: "i", label: ["1/θ<sub>i</sub>", "1/θ<sub>i</sub>"], unit: "", fn: function (P) { return P.inv; }, rtol: 0.01 },
             { id: "h", label: ["H<sub>i</sub>", "H<sub>i</sub>"], unit: "kN", fn: function (P) { return P.H; }, rtol: 0.01 }],
    hints: [function () { return bi("α<sub>h</sub> = 2/√l, but not less than 2/3 and not more than 1.", "α<sub>h</sub> = 2/√l, tetapi tidak kurang daripada 2/3 dan tidak lebih daripada 1."); },
            function () { return bi("α<sub>m</sub> = √(0.5(1 + 1/m)), with m the number of columns.", "α<sub>m</sub> = √(0.5(1 + 1/m)), dengan m bilangan column."); },
            function () { return bi("θ<sub>i</sub> = α<sub>h</sub>α<sub>m</sub>/200; H<sub>i</sub> = θ<sub>i</sub>N.", "θ<sub>i</sub> = α<sub>h</sub>α<sub>m</sub>/200; H<sub>i</sub> = θ<sub>i</sub>N."); }],
    solution: function (P) {
      return sol(["α<sub>h</sub> = 2/√" + P.l + " = " + f3(P.ah0) + (P.ah !== P.ah0 ? " → " + f3(P.ah) + bi(" (limit)", " (had)") : ""),
        "α<sub>m</sub> = √(0.5 × (1 + 1/" + P.m + ")) = " + f3(P.am),
        "θ<sub>i</sub> = " + f3(P.ah) + " × " + f3(P.am) + "/200 = 1/" + fmt(P.inv, 1) + "; H<sub>i</sub> = " + P.N + "/" + fmt(P.inv, 1) + " = " + f2(P.H) + " kN"]);
    }
  });
})();
