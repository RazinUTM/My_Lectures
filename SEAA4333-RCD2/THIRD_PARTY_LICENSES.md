# Third-party components

What the SEAA 4333 pages use that was written by others, how, and under which licence. Nothing in this
list is copied into the repository except the equation glyphs noted under MathJax.

| Component | Used for | How it reaches the page | Licence |
|---|---|---|---|
| MathJax 3.2.2 (`mathjax-full`, npm) | equations rendered to SVG at build time (`01-staircases-1/web/tex2svg.js`) | the SVG output, with glyph outlines from MathJax's TeX font data, is inlined in `index.html`; the package itself stays in `web/node_modules/` (not committed) | Apache License 2.0 |
| IBM Plex Sans, Source Serif 4, JetBrains Mono, Archivo, Atkinson Hyperlegible | page, slide and Lab typefaces | loaded at run time from Google Fonts; system fonts take over offline. The slide PDF embeds subsets, as the licence allows | SIL Open Font License 1.1 |
| Pillow | WebP figures (`web/make_figs.py`), image sizes in the build | build time only | MIT-CMU (HPND) |
| Beautiful Soup 4, lxml | page assembly and the tutor manifest | build time only | MIT; BSD-3-Clause |
| Playwright with Chromium | the slide PDF (`web/make_slides_pdf.py`) and the page checks | build time only | Apache License 2.0; Chromium BSD-3-Clause |
| segno | the QR code on the first slide (`img/qr_explorer.webp`) | generated once; the image is the output, not the library | BSD-3-Clause |

Own components under the owners' MIT licence, listed for completeness: the course engine (`shared/course.js`,
derived from SEAA 4243), the header and settings buttons (SEAA 3012 Lab S2, rz-settings-buttons), and the guide
panel with the tutor widget (rz-tutor-worker 0.3.0, pinned in `01-staircases-1/web/rz-tutor/`).
