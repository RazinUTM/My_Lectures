# SEAA 4243 sources

Everything the pages, Explorers, decks and slide PDFs are built from. The pages in the folders above are
generated: edit the sources here and rebuild; a hand edit to a built page is lost at the next build.

```
src/
├── build.sh        rebuild the site: Explorers → code packs → part pages → course home → Dr RJ (tools/add_tutor.py)
├── tools/          site builder: sitelib.py (shared pieces), build_part.py, content_pN.py (one per part),
│                   build_home.py, build_code.py (code/ packs and manifest), sync_labs.py, pyrun.py (Run in browser),
│                   make_pdf.py (slide PDFs), functest*.py (Playwright checks)
├── mj/             decks and their material: decklib.py, build_wN.py (one per claude.ai deck), eqs_*.py + eqs_*/
│                   (equations, MathJax SVG), figs_*.py + figs_*/ (figures), web_img/ (images with credits),
│                   deck_wN/ (deck projects as published, with the asset ids), labs/ (Explorer sources)
└── fonts/          fonts for PDFs and previews: run `npm ci` here once
```

Order of work after a content change:

1. Equations or figures changed: `python3 mj/eqs_<x>.py` or `mj/figs_<x>.py` (equations need `npm ci` in `mj/`).
2. Deck changed: `python3 mj/build_wN.py`, then publish `mj/deck_wN/project/` to its claude.ai deck
   (read the live files first; the site reads the same deck through `tools/build_part.py`).
3. `./build.sh` for the site; `python3 tools/make_pdf.py <part-folder> <file>.pdf` for a slide PDF.
4. Run the checks: `python3 tools/functest.py 01-heat-transfer-1`, `functest_p2.py` … `functest_p5.py`,
   `functest_slides.py`, `functest_py.py` (needs a local Pyodide 0.29.5 in `$PYODIDE_DIR`), and
   `functest_try.py` (every “Try it yourself” button of the six parts, at 1400 px and 400 px).

“Try it yourself” boxes: in `tools/content_pN.py`, `TRY("id id")` just before a section's `KP([...])` lists
the Explorer tasks (`LAB_TASKS` ids) that the section prepares. The box is empty in the page;
`shared/course.js` fills it from the task cards. The build stops unless every task is placed exactly once.

A fresh clone rebuilds to the committed pages byte for byte (checked 24 Nov 2026).
