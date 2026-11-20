# AI usage disclosure

Tools: Claude (Claude Opus 5.5, Claude Code on claude.ai), 9–10 November 2026; Playwright with Google Chrome
for the browser checks.
Scope: drafting of the primer content (notes, slides, worked examples, exercises, glossary, guide lines, BM
text), code generation (engine, Explorer, build scripts, companion Python), browser tests and these records.
Human verification: the author reviews all generated material before it is merged and published; the
architectural and design decisions are his and are recorded in `DECISIONS.md`. Status on 10 November 2026:
review pending (this folder arrives as a pull request).
Last updated: 2026-11-10

| Component | Origin | Human role | Verified by |
| --- | --- | --- | --- |
| `web/content_p1.py` | AI-drafted from the author's paper cracks (paper-cracks repository) and the reference texts named in the notes; worked numbers imported from `code/nmf_bspline_rk.py` | specified audience, scope and template; review pending | build (every equation filled, manifest generated), Playwright checks |
| `code/nmf_bspline_rk.py` | AI-generated from the equations of Part 1 | review pending | its `__main__` reproduces Examples 1–3 and RK with blossom vectors = B-splines for three kernels |
| `labs/rk-bspline.html` | AI-generated | review pending | Playwright sweep over 144 settings; values against the Python code |
| `shared/site.js` | AI-generated (implemented from the template's description; IMPAK `uikit.js` not copied) | review pending | Playwright: 53 behaviour checks, routes, guide targets, search |
| `shared/site.css` | SEAA 4243 `course.css` (author's own) with an AI-written block appended | review pending | screenshots at 1440 and 390 px, light and dark |
| `web/build.py`, `web/render_eq.cjs` | AI-generated | review pending | rebuild |
| `web/rz-tutor/` | author's rz-tutor-worker 0.2.0, copied unmodified | — | upstream |
| `shared/avatar/` | author's own likeness, copied from SEAA 4243 | — | — |
| `README.md`, `LICENSE.md`, `DECISIONS.md`, `THIRD_PARTY_LICENSES.md`, this file | AI-drafted | review pending | — |
