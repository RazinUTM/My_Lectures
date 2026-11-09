# Third-party components

| Component | Version | Licence (SPDX) | How used | Obligation / notice | Source |
| --- | --- | --- | --- | --- | --- |
| mathjax-full | 3.2.2 | Apache-2.0 | build-time dependency (`web/render_eq.cjs`); its SVG output, including glyph outlines from the MathJax TeX font data, is embedded in the part page | keep this row and the licence name; the package ships no NOTICE file | npmjs.com/package/mathjax-full |
| speech-rule-engine, mhchemparser, mj-context-menu | 4.1.5, 4.2.1, 0.6.1 | Apache-2.0 | transitive build-time dependencies of MathJax; not distributed | none beyond listing | npmjs.com |
| @xmldom/xmldom, commander, esm, wicked-good-xpath | 0.9.12, 13.1.0, 3.2.25, 1.3.0 | MIT | transitive build-time dependencies of MathJax; not distributed | none beyond listing | npmjs.com |
| rz-tutor-worker (panel, widget, `add_panel.py`, `build_manifest.py`) | 0.2.0 (commit a6197e9) | MIT | pinned copy in `web/rz-tutor/`, inlined into the part page by the build | same copyright holder; `LICENSE` kept beside the copy | github.com/RazinUTM/rz-tutor-worker |
| SEAA 4243 `course.css` | 2026-11-04 | CC BY-NC-SA 4.0 / MIT (same holder) | base of `shared/site.css` | same copyright holder | this repository, `SEAA4243-FEM/shared/` |
| numpy | any 1.x or 2.x | BSD-3-Clause | runtime dependency of `code/nmf_bspline_rk.py` (installed by the user) | none beyond listing | pypi.org/project/numpy |
| Playwright, Google Chrome | — | Apache-2.0, proprietary | test-time only, for the browser checks; not distributed | none | playwright.dev |

The lecturer's avatar in `shared/avatar/` is the author's own likeness (all rights reserved, see `LICENSE.md`).
No third-party image, font file or dataset is bundled.
