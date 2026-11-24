/* fe_core.js — SEAA 4243 FE labs.
   Banded Cholesky solver, 4- and 8-node rectangular plane elements, 4-node heat element,
   structured meshes, stress recovery and perceptual colour ramps.
   Notation follows Mohd Yassin et al. (2020): nodes 1-2-3-4 anticlockwise from the bottom-left,
   mid-side nodes 5 (bottom), 6 (right), 7 (top), 8 (left). */
var FE = (function () {
  "use strict";

  function SingularError(message, kind) { this.name = "SingularError"; this.message = message; this.kind = kind || "singular"; this.singular = true; }
  SingularError.prototype = Object.create(Error.prototype);

  /* ---------------- banded symmetric matrix (upper band, row-major) ---------------- */
  function band(n, hb) { return { n: n, hb: hb, w: hb + 1, a: new Float64Array(n * (hb + 1)) }; }
  function bAdd(K, i, j, v) { if (j < i) { var t = i; i = j; j = t; } K.a[i * K.w + (j - i)] += v; }
  function bGet(K, i, j) { if (j < i) { var t = i; i = j; j = t; } var d = j - i; return d > K.hb ? 0 : K.a[i * K.w + d]; }
  function bCopy(K) { return { n: K.n, hb: K.hb, w: K.w, a: K.a.slice() }; }
  function bMul(K, x) {
    var n = K.n, hb = K.hb, w = K.w, a = K.a, y = new Float64Array(n);
    for (var i = 0; i < n; i++) {
      var base = i * w; y[i] += a[base] * x[i];
      var jmax = Math.min(n - 1, i + hb);
      for (var j = i + 1; j <= jmax; j++) { var v = a[base + j - i]; if (v !== 0) { y[i] += v * x[j]; y[j] += v * x[i]; } }
    }
    return y;
  }
  /* fixed: array of [dof, value]; modifies K and F in place */
  function bDirichlet(K, F, fixed) {
    var n = K.n, hb = K.hb, w = K.w, a = K.a, k, j;
    for (k = 0; k < fixed.length; k++) {
      var p = fixed[k][0], g = fixed[k][1];
      if (g !== 0) for (j = Math.max(0, p - hb); j <= Math.min(n - 1, p + hb); j++) if (j !== p) F[j] -= bGet(K, j, p) * g;
    }
    for (k = 0; k < fixed.length; k++) {
      var q = fixed[k][0];
      for (j = Math.max(0, q - hb); j < q; j++) a[j * w + (q - j)] = 0;
      for (var d = 1; d <= hb && q + d < n; d++) a[q * w + d] = 0;
      a[q * w] = 1; F[q] = fixed[k][1];
    }
  }
  /* Cholesky K = U^T U on the band; returns x with K x = F. Throws SingularError for a non-positive pivot. */
  function bSolve(K, F) {
    var n = K.n, hb = K.hb, w = K.w, a = K.a.slice(), i, j, k, s;
    for (i = 0; i < n; i++) {
      var jmax = Math.min(n - 1, i + hb), ref = Math.abs(K.a[i * w]) || 1;
      for (j = i; j <= jmax; j++) {
        s = a[i * w + (j - i)];
        for (k = Math.max(0, j - hb); k < i; k++) s -= a[k * w + (i - k)] * a[k * w + (j - k)];
        if (j === i) {
          if (!(s > 1e-10 * ref)) throw new SingularError("The stiffness matrix is singular at equation " + (i + 1) + ".", "pivot");
          a[i * w] = Math.sqrt(s);
        } else a[i * w + (j - i)] = s / a[i * w];
      }
    }
    var x = Float64Array.from(F);
    for (i = 0; i < n; i++) { s = x[i]; for (k = Math.max(0, i - hb); k < i; k++) s -= a[k * w + (i - k)] * x[k]; x[i] = s / a[i * w]; }
    for (i = n - 1; i >= 0; i--) { s = x[i]; var jm = Math.min(n - 1, i + hb); for (j = i + 1; j <= jm; j++) s -= a[i * w + (j - i)] * x[j]; x[i] = s / a[i * w]; }
    return x;
  }

  /* ---------------- shape functions on the natural square [-1, 1]^2 ---------------- */
  var XI = [-1, 1, 1, -1, 0, 1, 0, -1], ETA = [-1, -1, 1, 1, -1, 0, 1, 0];
  function shapeQ4(xi, eta) {
    var N = new Float64Array(4), dx = new Float64Array(4), de = new Float64Array(4);
    for (var i = 0; i < 4; i++) {
      N[i] = 0.25 * (1 + XI[i] * xi) * (1 + ETA[i] * eta);
      dx[i] = 0.25 * XI[i] * (1 + ETA[i] * eta);
      de[i] = 0.25 * ETA[i] * (1 + XI[i] * xi);
    }
    return { N: N, dxi: dx, deta: de };
  }
  function shapeQ8(xi, eta) {
    var N = new Float64Array(8), dx = new Float64Array(8), de = new Float64Array(8), i;
    for (i = 0; i < 4; i++) {
      var cx = XI[i], cy = ETA[i];
      N[i] = 0.25 * (1 + cx * xi) * (1 + cy * eta) * (cx * xi + cy * eta - 1);
      dx[i] = 0.25 * cx * (1 + cy * eta) * (2 * cx * xi + cy * eta);
      de[i] = 0.25 * cy * (1 + cx * xi) * (cx * xi + 2 * cy * eta);
    }
    N[4] = 0.5 * (1 - xi * xi) * (1 - eta); dx[4] = -xi * (1 - eta); de[4] = -0.5 * (1 - xi * xi);
    N[5] = 0.5 * (1 + xi) * (1 - eta * eta); dx[5] = 0.5 * (1 - eta * eta); de[5] = -eta * (1 + xi);
    N[6] = 0.5 * (1 - xi * xi) * (1 + eta); dx[6] = -xi * (1 + eta); de[6] = 0.5 * (1 - xi * xi);
    N[7] = 0.5 * (1 - xi) * (1 - eta * eta); dx[7] = -0.5 * (1 - eta * eta); de[7] = -eta * (1 - xi);
    return { N: N, dxi: dx, deta: de };
  }
  function shape(nen, xi, eta) { return nen === 8 ? shapeQ8(xi, eta) : shapeQ4(xi, eta); }

  /* strain-displacement matrix of a rectangular a x b element at (xi, eta); row-major 3 x 2nen */
  function Bmat(nen, a, b, xi, eta) {
    var s = shape(nen, xi, eta), m = 2 * nen, B = new Float64Array(3 * m);
    for (var i = 0; i < nen; i++) {
      var dNdx = s.dxi[i] * 2 / a, dNdy = s.deta[i] * 2 / b;
      B[2 * i] = dNdx; B[m + 2 * i + 1] = dNdy; B[2 * m + 2 * i] = dNdy; B[2 * m + 2 * i + 1] = dNdx;
    }
    return { B: B, N: s.N };
  }
  function Dmat(E, nu, plane) {
    var c;
    if (plane === "strain") {
      c = E / ((1 + nu) * (1 - 2 * nu));
      return [c * (1 - nu), c * nu, 0, c * nu, c * (1 - nu), 0, 0, 0, c * (1 - 2 * nu) / 2];
    }
    c = E / (1 - nu * nu);
    return [c, c * nu, 0, c * nu, c, 0, 0, 0, c * (1 - nu) / 2];
  }
  var G2 = [[-1 / Math.sqrt(3), 1], [1 / Math.sqrt(3), 1]];
  var G3 = [[-Math.sqrt(0.6), 5 / 9], [0, 8 / 9], [Math.sqrt(0.6), 5 / 9]];
  function kPlane(nen, a, b, D, t) {
    var m = 2 * nen, k = new Float64Array(m * m), g = nen === 8 ? G3 : G2, DB = new Float64Array(3 * m);
    for (var p = 0; p < g.length; p++) for (var q = 0; q < g.length; q++) {
      var B = Bmat(nen, a, b, g[p][0], g[q][0]).B, f = t * (a / 2) * (b / 2) * g[p][1] * g[q][1], r, c, i, j;
      for (r = 0; r < 3; r++) for (c = 0; c < m; c++) DB[r * m + c] = D[r * 3] * B[c] + D[r * 3 + 1] * B[m + c] + D[r * 3 + 2] * B[2 * m + c];
      for (i = 0; i < m; i++) for (j = 0; j < m; j++) k[i * m + j] += f * (B[i] * DB[j] + B[m + i] * DB[m + j] + B[2 * m + i] * DB[2 * m + j]);
    }
    return k;
  }
  /* 4-node heat element, text (2.49) */
  function kHeat(a, b, kx, ky) {
    var s1 = b * kx / (3 * a) + a * ky / (3 * b), s2 = -b * kx / (3 * a) + a * ky / (6 * b),
        s3 = -b * kx / (6 * a) - a * ky / (6 * b), s4 = b * kx / (6 * a) - a * ky / (3 * b);
    return [s1, s2, s3, s4, s2, s1, s4, s3, s3, s4, s1, s2, s4, s3, s2, s1];
  }

  /* ---------------- structured meshes (numbered by columns to keep the band narrow) ---------------- */
  function meshPlane(nen, L, H, Nx, Ny) {
    var a = L / Nx, b = H / Ny, X = [], Y = [], conn = [], i, j;
    if (nen === 4) {
      for (i = 0; i <= Nx; i++) for (j = 0; j <= Ny; j++) { X.push(i * a); Y.push(j * b); }
      var id = function (i, j) { return i * (Ny + 1) + j; };
      for (j = 0; j < Ny; j++) for (i = 0; i < Nx; i++) conn.push(id(i, j), id(i + 1, j), id(i + 1, j + 1), id(i, j + 1));
    } else {
      var S = 3 * Ny + 2;
      for (i = 0; i <= Nx; i++) {
        for (j = 0; j <= 2 * Ny; j++) { X.push(i * a); Y.push(j * b / 2); }
        if (i < Nx) for (j = 0; j <= Ny; j++) { X.push((i + 0.5) * a); Y.push(j * b); }
      }
      var full = function (i, j2) { return i * S + j2; }, mid = function (i, j) { return i * S + 2 * Ny + 1 + j; };
      for (j = 0; j < Ny; j++) for (i = 0; i < Nx; i++)
        conn.push(full(i, 2 * j), full(i + 1, 2 * j), full(i + 1, 2 * j + 2), full(i, 2 * j + 2), mid(i, j), full(i + 1, 2 * j + 1), mid(i, j + 1), full(i, 2 * j + 1));
    }
    return { nen: nen, L: L, H: H, Nx: Nx, Ny: Ny, a: a, b: b, nn: X.length, ne: Nx * Ny, X: Float64Array.from(X), Y: Float64Array.from(Y), conn: Int32Array.from(conn) };
  }
  function findNode(m, x, y) {
    var best = -1, d = Infinity;
    for (var i = 0; i < m.nn; i++) { var dd = Math.hypot(m.X[i] - x, m.Y[i] - y); if (dd < d) { d = dd; best = i; } }
    return best;
  }
  /* element containing (X, Y) and its natural coordinates */
  function locate(m, X, Y) {
    var i = Math.min(m.Nx - 1, Math.max(0, Math.floor(X / m.a))), j = Math.min(m.Ny - 1, Math.max(0, Math.floor(Y / m.b)));
    var e = j * m.Nx + i, x0 = i * m.a, y0 = j * m.b;
    return { e: e, i: i, j: j, x: X - x0, y: Y - y0, xi: 2 * (X - x0) / m.a - 1, eta: 2 * (Y - y0) / m.b - 1 };
  }

  /* ---------------- plane stress / plane strain cantilever ---------------- */
  /* o: {nen, L, H, Nx, Ny, E, nu, t, plane, q (N/m, + up), load: 'edge'|'point', support: 'fixed'|'vonly'} */
  function solvePlane(o) {
    var m = meshPlane(o.nen, o.L, o.H, o.Nx, o.Ny), nen = o.nen, nd = 2 * m.nn, D = Dmat(o.E, o.nu, o.plane);
    var ke = kPlane(nen, m.a, m.b, D, o.t), e, i, j, hb = 0, dofs = new Int32Array(2 * nen);
    for (e = 0; e < m.ne; e++) {
      var lo = Infinity, hi = -Infinity;
      for (i = 0; i < nen; i++) { var nd_ = m.conn[e * nen + i]; lo = Math.min(lo, 2 * nd_); hi = Math.max(hi, 2 * nd_ + 1); }
      hb = Math.max(hb, hi - lo);
    }
    var K = band(nd, hb), F = new Float64Array(nd), M = 2 * nen;
    for (e = 0; e < m.ne; e++) {
      for (i = 0; i < nen; i++) { dofs[2 * i] = 2 * m.conn[e * nen + i]; dofs[2 * i + 1] = 2 * m.conn[e * nen + i] + 1; }
      for (i = 0; i < M; i++) for (j = i; j < M; j++) bAdd(K, dofs[i], dofs[j], ke[i * M + j]);
    }
    var P = o.q * o.H; /* total end force (N), negative = downward */
    if (o.load === "point") F[2 * findNode(m, o.L, o.H) + 1] += P;
    else for (j = 0; j < m.Ny; j++) {
      e = j * m.Nx + (m.Nx - 1);
      var c = m.conn.subarray(e * nen, e * nen + nen);
      if (nen === 4) { F[2 * c[1] + 1] += o.q * m.b / 2; F[2 * c[2] + 1] += o.q * m.b / 2; }
      else { F[2 * c[1] + 1] += o.q * m.b / 6; F[2 * c[5] + 1] += 2 * o.q * m.b / 3; F[2 * c[2] + 1] += o.q * m.b / 6; }
    }
    var fixed = [];
    for (i = 0; i < m.nn; i++) if (Math.abs(m.X[i]) < 1e-12) { if (o.support !== "vonly") fixed.push([2 * i, 0]); fixed.push([2 * i + 1, 0]); }
    var res = { o: o, mesh: m, D: D, F: F, fixed: fixed, nd: nd, hb: hb, P: P };
    if (o.support === "vonly") {
      res.error = new SingularError("Nothing stops the plate from sliding in x: a rigid-body mode, so [K] is singular.", "rigid");
      return res;
    }
    var K0 = bCopy(K), F0 = F.slice();
    bDirichlet(K, F, fixed);
    try { res.U = bSolve(K, F); } catch (err) { res.error = err; return res; }
    var KU = bMul(K0, res.U), Rx = 0, Ry = 0, Mz = 0;
    for (i = 0; i < fixed.length; i++) {
      var p = fixed[i][0], r = KU[p] - F0[p], node = p >> 1;
      if (p % 2 === 0) { Rx += r; Mz += -(m.Y[node] - o.H / 2) * r; } else { Ry += r; Mz += m.X[node] * r; }
    }
    res.reaction = { Rx: Rx, Ry: Ry, M: Mz };
    res.tipNode = findNode(m, o.L, o.H);
    res.tip = res.U[2 * res.tipNode + 1];
    return res;
  }
  function elemDofs(res, e) {
    var nen = res.mesh.nen, d = new Int32Array(2 * nen);
    for (var i = 0; i < nen; i++) { var n = res.mesh.conn[e * nen + i]; d[2 * i] = 2 * n; d[2 * i + 1] = 2 * n + 1; }
    return d;
  }
  function stressInElement(res, e, xi, eta) {
    var m = res.mesh, nen = m.nen, M = 2 * nen, B = Bmat(nen, m.a, m.b, xi, eta).B, d = elemDofs(res, e), D = res.D;
    var eps = [0, 0, 0];
    for (var r = 0; r < 3; r++) for (var c = 0; c < M; c++) eps[r] += B[r * M + c] * res.U[d[c]];
    var sig = [D[0] * eps[0] + D[1] * eps[1], D[3] * eps[0] + D[4] * eps[1], D[8] * eps[2]];
    return { eps: eps, sig: sig };
  }
  function stressAt(res, X, Y) { var L = locate(res.mesh, X, Y), s = stressInElement(res, L.e, L.xi, L.eta); s.loc = L; return s; }
  function displacementAt(res, X, Y) {
    var m = res.mesh, L = locate(m, X, Y), N = shape(m.nen, L.xi, L.eta).N, u = 0, v = 0;
    for (var i = 0; i < m.nen; i++) { var n = m.conn[L.e * m.nen + i]; u += N[i] * res.U[2 * n]; v += N[i] * res.U[2 * n + 1]; }
    return [u, v];
  }
  function derived(s) {
    var c = (s[0] + s[1]) / 2, R = Math.hypot((s[0] - s[1]) / 2, s[2]);
    return { s1: c + R, s2: c - R, c: c, R: R, theta: 0.5 * Math.atan2(2 * s[2], s[0] - s[1]) * 180 / Math.PI,
             vm: Math.sqrt(s[0] * s[0] - s[0] * s[1] + s[1] * s[1] + 3 * s[2] * s[2]) };
  }
  /* nodal stresses: per element (unaveraged) and averaged over the elements sharing a node */
  function nodalStresses(res) {
    var m = res.mesh, nen = m.nen, ne = m.ne, un = new Float64Array(ne * nen * 3), av = new Float64Array(m.nn * 3), cnt = new Float64Array(m.nn);
    var cen = new Float64Array(ne * 3);
    for (var e = 0; e < ne; e++) {
      for (var i = 0; i < nen; i++) {
        var s = stressInElement(res, e, XI[i], ETA[i]).sig, n = m.conn[e * nen + i];
        for (var k = 0; k < 3; k++) { un[(e * nen + i) * 3 + k] = s[k]; av[n * 3 + k] += s[k]; }
        cnt[n] += 1;
      }
      var sc = stressInElement(res, e, 0, 0).sig; cen[e * 3] = sc[0]; cen[e * 3 + 1] = sc[1]; cen[e * 3 + 2] = sc[2];
    }
    for (var p = 0; p < m.nn; p++) for (var q = 0; q < 3; q++) av[p * 3 + q] /= cnt[p];
    return { unav: un, avg: av, cen: cen };
  }

  /* ---------------- steady heat conduction on a square plate ---------------- */
  /* o: {L, n, k, q, edges: {bottom, right, top, left}: {type: 'T'|'ins'|'flux', value}} */
  function solveHeat(o) {
    var n = o.n, L = o.L, a = L / n, nn = (n + 1) * (n + 1), id = function (i, j) { return j * (n + 1) + i; };
    var X = new Float64Array(nn), Y = new Float64Array(nn), i, j, e, conn = [];
    for (j = 0; j <= n; j++) for (i = 0; i <= n; i++) { X[id(i, j)] = i * a; Y[id(i, j)] = j * a; }
    for (j = 0; j < n; j++) for (i = 0; i < n; i++) conn.push(id(i, j), id(i + 1, j), id(i + 1, j + 1), id(i, j + 1));
    var ke = kHeat(a, a, o.k, o.k), K = band(nn, n + 2), F = new Float64Array(nn), fq = o.q * a * a / 4;
    for (e = 0; e < n * n; e++) for (var p = 0; p < 4; p++) {
      F[conn[4 * e + p]] += fq;
      for (var q = p; q < 4; q++) bAdd(K, conn[4 * e + p], conn[4 * e + q], ke[p * 4 + q]);
    }
    var sides = {
      bottom: function (s) { return id(s, 0); }, top: function (s) { return id(s, n); },
      left: function (s) { return id(0, s); }, right: function (s) { return id(n, s); }
    };
    var fluxIn = 0, fixedVal = {}, order = ["top", "left", "right", "bottom"];
    for (var name in sides) {
      var ed = o.edges[name];
      if (ed.type === "flux") { for (var s = 0; s < n; s++) { F[sides[name](s)] += ed.value * a / 2; F[sides[name](s + 1)] += ed.value * a / 2; } fluxIn += ed.value * L; }
    }
    order.forEach(function (name) {
      var ed = o.edges[name];
      if (ed.type === "T") for (var s = 0; s <= n; s++) { var node = sides[name](s); if (!(node in fixedVal)) fixedVal[node] = ed.value; }
    });
    var fixed = Object.keys(fixedVal).map(function (k) { return [+k, fixedVal[k]]; });
    var res = { n: n, L: L, a: a, nn: nn, X: X, Y: Y, conn: Int32Array.from(conn), generated: o.q * L * L, fluxIn: fluxIn, fixed: fixed, k: o.k };
    if (!fixed.length) { res.error = new SingularError("No edge has a fixed temperature, so the temperature level is undetermined and [K] is singular.", "float"); return res; }
    var K0 = bCopy(K), F0 = F.slice();
    bDirichlet(K, F, fixed);
    try { res.T = bSolve(K, F); } catch (err) { res.error = err; return res; }
    var KT = bMul(K0, res.T), R = 0;
    for (i = 0; i < fixed.length; i++) R += KT[fixed[i][0]] - F0[fixed[i][0]];
    res.reaction = R;
    var imax = 0; for (i = 1; i < nn; i++) if (res.T[i] > res.T[imax]) imax = i;
    res.imax = imax;
    return res;
  }
  function heatAt(res, X, Y) {
    var n = res.n, a = res.a, i = Math.min(n - 1, Math.max(0, Math.floor(X / a))), j = Math.min(n - 1, Math.max(0, Math.floor(Y / a)));
    var e = j * n + i, xi = 2 * (X - i * a) / a - 1, eta = 2 * (Y - j * a) / a - 1, s = shapeQ4(xi, eta), T = 0, gx = 0, gy = 0;
    for (var p = 0; p < 4; p++) { var t = res.T[res.conn[4 * e + p]]; T += s.N[p] * t; gx += s.dxi[p] * 2 / a * t; gy += s.deta[p] * 2 / a * t; }
    return { T: T, gx: gx, gy: gy, qx: -res.k * gx, qy: -res.k * gy, e: e };
  }

  /* ---------------- reference beam theory for the cantilever ---------------- */
  function timoshenko(o) {
    var P = -o.q * o.H, I = o.t * Math.pow(o.H, 3) / 12, A = o.t * o.H, G = o.E / (2 * (1 + o.nu));
    var Eb = o.plane === "strain" ? o.E / (1 - o.nu * o.nu) : o.E;
    var bend = P * Math.pow(o.L, 3) / (3 * Eb * I), shear = P * o.L / (5 / 6 * G * A);
    return { bend: bend, shear: shear, total: bend + shear, I: I };
  }
  function beamStress(o, X, Y) {
    var P = -o.q * o.H, I = o.t * Math.pow(o.H, 3) / 12, c = o.H / 2, yp = Y - c;
    return { sxx: P * (o.L - X) * yp / I, sxy: -P * (c * c - yp * yp) / (2 * I) };
  }

  /* ---------------- colour: OKLab interpolation of anchor ramps ---------------- */
  function hex2rgb(h) { h = h.replace("#", ""); return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255]; }
  function lin(c) { return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function gam(c) { return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055; }
  function toLab(hex) {
    var c = hex2rgb(hex).map(lin);
    var l = Math.cbrt(0.4122214708 * c[0] + 0.5363325363 * c[1] + 0.0514459929 * c[2]);
    var m = Math.cbrt(0.2119034982 * c[0] + 0.6806995451 * c[1] + 0.1073969566 * c[2]);
    var s = Math.cbrt(0.0883024619 * c[0] + 0.2817188376 * c[1] + 0.6299787005 * c[2]);
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
  }
  function fromLab(L) {
    var l = Math.pow(L[0] + 0.3963377774 * L[1] + 0.2158037573 * L[2], 3), m = Math.pow(L[0] - 0.1055613458 * L[1] - 0.0638541728 * L[2], 3), s = Math.pow(L[0] - 0.0894841775 * L[1] - 1.2914855480 * L[2], 3);
    var r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s;
    return [r, g, b].map(function (v) { return Math.round(255 * Math.min(1, Math.max(0, gam(v)))); });
  }
  /* returns a 256-entry Uint8ClampedArray LUT (rgb triplets) for anchor hex colours */
  function makeLUT(anchors) {
    var labs = anchors.map(toLab), lut = new Uint8ClampedArray(256 * 3), nseg = labs.length - 1;
    for (var i = 0; i < 256; i++) {
      var t = i / 255 * nseg, k = Math.min(nseg - 1, Math.floor(t)), f = t - k, A = labs[k], B = labs[k + 1];
      var rgb = fromLab([A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f, A[2] + (B[2] - A[2]) * f]);
      lut[3 * i] = rgb[0]; lut[3 * i + 1] = rgb[1]; lut[3 * i + 2] = rgb[2];
    }
    return lut;
  }
  var RAMPS = {
    heat: { light: ["#fdf3e6", "#f8c99c", "#ef9156", "#d4562b", "#9b2c17", "#5c1a0f"], dark: ["#2e1a14", "#6e2b17", "#b4472a", "#e57a48", "#f6b98c", "#fde9d6"] },
    mag: { light: ["#e6f0fc", "#9ec5f4", "#3987e5", "#1c5cab", "#0d366b"], dark: ["#16253a", "#1c4a85", "#2f7bd8", "#86b6ef", "#dce9fb"] },
    div: { light: ["#0d366b", "#3987e5", "#b7d3f6", "#f0efec", "#f5c1b7", "#e05544", "#7d1d18"], dark: ["#b7d3f6", "#4f94e6", "#21487a", "#383835", "#7a302a", "#e2604f", "#f6c1b7"] }
  };
  var lutCache = {};
  function lut(name, mode) { var key = name + mode; if (!lutCache[key]) lutCache[key] = makeLUT(RAMPS[name][mode]); return lutCache[key]; }
  function cssGradient(name, mode) {
    var L = lut(name, mode), stops = [];
    for (var i = 0; i <= 10; i++) { var k = Math.round(i * 25.5); stops.push("rgb(" + L[3 * k] + "," + L[3 * k + 1] + "," + L[3 * k + 2] + ") " + (i * 10) + "%"); }
    return "linear-gradient(90deg, " + stops.join(", ") + ")";
  }

  return {
    SingularError: SingularError, band: band, bAdd: bAdd, bGet: bGet, bMul: bMul, bDirichlet: bDirichlet, bSolve: bSolve,
    shapeQ4: shapeQ4, shapeQ8: shapeQ8, shape: shape, XI: XI, ETA: ETA, Bmat: Bmat, Dmat: Dmat, kPlane: kPlane, kHeat: kHeat,
    meshPlane: meshPlane, findNode: findNode, locate: locate, solvePlane: solvePlane, stressAt: stressAt, stressInElement: stressInElement,
    displacementAt: displacementAt, derived: derived, nodalStresses: nodalStresses, solveHeat: solveHeat, heatAt: heatAt,
    timoshenko: timoshenko, beamStress: beamStress, lut: lut, cssGradient: cssGradient, RAMPS: RAMPS
  };
})();
if (typeof module !== "undefined") module.exports = FE;
