// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
// Render display equations to SVG at build time, so the page needs no maths library when it runs.
// Reads a JSON array [{id, tex}] on stdin and writes {id: "<svg …>"} on stdout. Each SVG carries its own
// glyph definitions (fontCache "local") with ids prefixed by the equation id, so several equations can
// sit in one page without clashing. Needs mathjax-full 3.2.2 (npm ci in this folder; see package.json).
const { mathjax } = require("mathjax-full/js/mathjax.js");
const { TeX } = require("mathjax-full/js/input/tex.js");
const { SVG } = require("mathjax-full/js/output/svg.js");
const { liteAdaptor } = require("mathjax-full/js/adaptors/liteAdaptor.js");
const { RegisterHTMLHandler } = require("mathjax-full/js/handlers/html.js");
const { AllPackages } = require("mathjax-full/js/input/tex/AllPackages.js");

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document("", {
  InputJax: new TeX({ packages: AllPackages }),
  OutputJax: new SVG({ fontCache: "local" }),
});

let input = "";
process.stdin.on("data", (c) => (input += c));
process.stdin.on("end", () => {
  const out = {};
  for (const { id, tex } of JSON.parse(input)) {
    const node = doc.convert(tex, { display: true, em: 16, ex: 8, containerWidth: 1280 });
    let svg = adaptor.innerHTML(node);
    svg = svg.replace(/MJX-\d+-/g, id + "-");       // glyph ids: unique per equation
    out[id] = svg;
  }
  process.stdout.write(JSON.stringify(out));
});
