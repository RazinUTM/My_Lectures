const FE = require("./fe_core.js");
const f = (x, d = 4) => (+x).toFixed(d);
const base = { nen: 4, L: 4, H: 2, Nx: 2, Ny: 2, E: 200e6, nu: 0.33, t: 0.01, plane: "stress", q: -5000, load: "edge", support: "fixed" };
const run = (o) => FE.solvePlane(Object.assign({}, base, o));
const checks = [];
const chk = (name, got, exp, tol) => { const ok = Math.abs(got - exp) <= tol; checks.push(ok); console.log(`${ok ? "PASS" : "FAIL"}  ${name}: ${f(got, 4)} (expected ${exp})`); };
let r = run({});
chk("Q4 2x2 tip v", r.tip, -0.1306, 5e-5);
chk("Q4 2x2 reaction Ry", r.reaction.Ry, 10000, 1e-6);
chk("Q4 2x2 reaction M", r.reaction.M, 40000, 1e-4);
let s = FE.stressAt(r, 3.5, 1.3);
chk("Q4 2x2 sxx(3.5,1.3) kN/m2", s.sig[0] / 1e3, 315.2, 0.1); chk("syy", s.sig[1] / 1e3, -44.9, 0.1); chk("sxy", s.sig[2] / 1e3, -310.9, 0.1);
let d = FE.derived(s.sig.map(v => v / 1e3)); chk("s1", d.s1, 494.4, 0.1); chk("s2", d.s2, -224.1, 0.1); chk("vM", d.vm, 636.8, 0.1);
chk("Q4 32x16 tip", run({ Nx: 32, Ny: 16 }).tip, -0.1906, 5e-5);
chk("Q4 8x1 tip", run({ Nx: 8, Ny: 1 }).tip, -0.1657, 5e-5);
chk("Q4 2x4 tip", run({ Nx: 2, Ny: 4 }).tip, -0.1334, 5e-5);
chk("Q4 32x16 plane strain tip", run({ Nx: 32, Ny: 16, plane: "strain" }).tip, -0.1712, 5e-5);
chk("Q8 2x1 tip", run({ nen: 8, Nx: 2, Ny: 1 }).tip, -0.1780, 5e-5);
chk("Q8 4x2 tip", run({ nen: 8, Nx: 4, Ny: 2 }).tip, -0.1885, 5e-5);
let t0 = Date.now(); let r8 = run({ nen: 8, Nx: 32, Ny: 16 }); let ms = Date.now() - t0;
chk("Q8 32x16 tip", r8.tip, -0.1915, 5e-5); console.log("   Q8 32x16 solve time", ms, "ms, dofs", r8.nd, "hb", r8.hb);
chk("Q8 32x16 sxx(3.5,1.3)", FE.stressAt(r8, 3.5, 1.3).sig[0] / 1e3, 151.7, 0.2);
chk("Q8 32x16 sxx(2.0,1.3)", FE.stressAt(r8, 2.0, 1.3).sig[0] / 1e3, 900.3, 0.2);
// corner singularity: centroid of top-left element
for (const [nx, ny, exp] of [[8, 4, 4134], [16, 8, 5372], [32, 16, 6400], [64, 32, 7467]]) {
  const rr = run({ Nx: nx, Ny: ny }); const L = rr.mesh; const x = L.a / 2, y = 2 - L.b / 2;
  chk(`Q4 ${nx}x${ny} corner centroid sxx`, FE.stressAt(rr, x, y).sig[0] / 1e3, exp, 1);
}
chk("Q8 point-load tip node", run({ nen: 8, Nx: 32, Ny: 16, load: "point" }).tip, -0.2298, 5e-4);
const rv = run({ support: "vonly" }); console.log(rv.error ? "PASS  v-only support flagged: " + rv.error.message : "FAIL  v-only not flagged"); checks.push(!!rv.error);
// heat
const hb = { L: 1, n: 2, k: 300, q: 600, edges: { top: { type: "T", value: 0 }, left: { type: "T", value: 0 }, right: { type: "ins", value: 0 }, bottom: { type: "ins", value: 0 } } };
const H = (o) => FE.solveHeat(Object.assign({}, hb, o));
let h = H({});
chk("heat 2x2 T(1,0)", FE.heatAt(h, 1, 0).T, 0.6214, 5e-5); chk("heat 2x2 T(0.5,0)", FE.heatAt(h, 0.5, 0).T, 0.4821, 5e-5);
chk("heat 2x2 reaction", h.reaction, -600, 1e-6);
chk("heat 16x16 T(1,0)", FE.heatAt(H({ n: 16 }), 1, 0).T, 0.5898, 5e-5);
chk("heat 32x32 T(1,0)", FE.heatAt(H({ n: 32 }), 1, 0).T, 0.5895, 5e-5);
const h3 = H({ n: 16, edges: Object.assign({}, hb.edges, { right: { type: "T", value: 0 } }) });
chk("heat right-cold max", h3.T[h3.imax], 0.2280, 5e-5); console.log("   at", h3.X[h3.imax], h3.Y[h3.imax]);
const h4 = H({ edges: { top: { type: "ins" }, left: { type: "ins" }, right: { type: "ins" }, bottom: { type: "ins" } } });
console.log(h4.error ? "PASS  all-insulated flagged: " + h4.error.message : "FAIL"); checks.push(!!h4.error);
// interpolation check at Week 10 Activity 6 point (0.3, 0.2): ~0.266
chk("heat 2x2 T(0.3,0.2)", FE.heatAt(h, 0.3, 0.2).T, 0.266, 2e-3);
// shape functions at Week 9 Activity 4: a=2,b=1,(1.5,0.3)
const sq = FE.shapeQ4(2 * 1.5 / 2 - 1, 2 * 0.3 / 1 - 1).N; console.log("   N at (1.5,0.3):", Array.from(sq).map(v => v.toFixed(3)).join(", "));
chk("N2(1.5,0.3)", sq[1], 0.525, 1e-12);
const q8c = FE.shapeQ8(0, 0).N; chk("Q8 N1 at centre", q8c[0], -0.25, 1e-12);
console.log(checks.every(Boolean) ? "\nALL PASS" : "\nSOME FAILED");
