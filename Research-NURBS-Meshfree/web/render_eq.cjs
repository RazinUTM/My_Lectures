// SPDX-License-Identifier: MIT · Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
// Render the primer's LaTeX equations to self-contained SVG at build time (MathJax 3, Apache-2.0).
// How to call it: node render_eq.cjs equations.json svgs.json   (input {id: tex}, output {id: svg})
// Why: the pages carry no runtime dependency, so equations are drawn once here; the LaTeX stays in the page
// as data-tex on each .eqwrap for screen readers, search and the tutor.
"use strict";
const fs = require("fs");
const { mathjax } = require("mathjax-full/js/mathjax.js");
const { TeX } = require("mathjax-full/js/input/tex.js");
const { SVG } = require("mathjax-full/js/output/svg.js");
const { liteAdaptor } = require("mathjax-full/js/adaptors/liteAdaptor.js");
const { RegisterHTMLHandler } = require("mathjax-full/js/handlers/html.js");
const { AllPackages } = require("mathjax-full/js/input/tex/AllPackages.js");

const [inp, out] = process.argv.slice(2);
const eqs = JSON.parse(fs.readFileSync(inp, "utf8"));
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document("", {
  InputJax: new TeX({ packages: AllPackages }),
  OutputJax: new SVG({ fontCache: "local" }),
});
const res = {};
for (const [id, tex] of Object.entries(eqs)) {
  const node = doc.convert(tex, { display: true });
  let svg = adaptor.innerHTML(node);
  // ids of the glyph definitions must be unique across the page: prefix them with the equation id
  svg = svg.replace(/id="MJX-/g, `id="${id}-MJX-`).replace(/xlink:href="#MJX-/g, `xlink:href="#${id}-MJX-`);
  if (/data-mjx-error|merror/.test(svg)) { console.error(`render_eq: TeX error in ${id}: ${tex}`); process.exitCode = 1; }
  res[id] = svg.replace("<svg ", `<svg aria-label="${id}" `);
}
fs.writeFileSync(out, JSON.stringify(res));
console.log(`render_eq: ${Object.keys(res).length} equations`);
