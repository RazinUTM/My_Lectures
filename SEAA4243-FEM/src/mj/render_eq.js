// Render LaTeX → standalone SVG (glyphs as paths) with MathJax, sized in px for a 1920x1080 canvas.
// usage: node render_eq.js items.json outdir
const fs = require('fs');
const path = require('path');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({packages: AllPackages, inlineMath: [['$', '$']]});
const svg = new SVG({fontCache: 'local'});
const html = mathjax.document('', {InputJax: tex, OutputJax: svg});

const [,, itemsFile, outDir] = process.argv;
const items = JSON.parse(fs.readFileSync(itemsFile, 'utf8'));
fs.mkdirSync(outDir, {recursive: true});
const report = [];
for (const it of items) {
  const em = it.em || 44;             // px per em on the 1920 canvas
  const color = it.color || '#1b2330';
  const node = html.convert(it.tex, {display: it.display !== false, em: 16, ex: 8, containerWidth: 80 * 16});
  let out = adaptor.outerHTML(node);
  // take the inner <svg ...>...</svg>
  const m = out.match(/<svg[\s\S]*<\/svg>/);
  if (!m) { report.push({name: it.name, error: 'no svg', raw: out.slice(0, 300)}); continue; }
  let s = m[0];
  const vb = s.match(/viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"/);
  const vbw = parseFloat(vb[3]), vbh = parseFloat(vb[4]);
  const wpx = Math.round(vbw / 1000 * em), hpx = Math.round(vbh / 1000 * em);
  // normalise attributes
  s = s.replace(/<svg[^>]*>/, `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${wpx}" height="${hpx}" viewBox="${vb[1]} ${vb[2]} ${vb[3]} ${vb[4]}" aria-label="${(it.alt || it.name).replace(/"/g, "'")}">`);
  s = s.replace(/currentColor/g, color);
  s = s.replace(/ data-mml-node="[^"]*"/g, '').replace(/ data-c="[^"]*"/g, '').replace(/ data-mjx-texclass="[^"]*"/g, '');
  s = s.replace(/ role="img"| focusable="false"/g, '');
  // unique id prefix per item so several svgs on one slide never share ids
  const pre = it.name.replace(/[^A-Za-z0-9_-]/g, '');
  s = s.replace(/id="MJX-/g, `id="${pre}-`).replace(/href="#MJX-/g, `href="#${pre}-`);
  // trim path precision a little
  s = s.replace(/(\d+\.\d{2})\d+/g, '$1');
  fs.writeFileSync(path.join(outDir, it.name + '.svg'), s);
  report.push({name: it.name, w: wpx, h: hpx, bytes: Buffer.byteLength(s)});
}
fs.writeFileSync(path.join(outDir, '_report.json'), JSON.stringify(report, null, 1));
for (const r of report) console.log(r.error ? `${r.name}: ERROR ${r.error} ${r.raw}` : `${r.name}: ${r.w}x${r.h}px ${r.bytes}B`);
