# Lab S2 · Influence Lines

Teaching package for experiment S2 of *Civil Engineering Laboratory II* (SEAA 3012, Faculty of
Civil Engineering, UTM): a cantilever (Gerber) bridge model with six dial gauges. All material
uses the geometry, halts, notation η_R(x) and sign convention of the revised laboratory manual.

## Course page

`index.html` is a single self-contained page with six tabs: Start, Notes, Slides, Explorer,
Exercises and Lab. It works in any modern browser, on phones as well as projectors. Tabs open
directly with `#notes`, `#slides`, `#explorer`, `#exercises` or `#lab` after the address.

Published with GitHub Pages at
<https://razinutm.github.io/My_Lectures/SEAA3012-CE-Lab-II/S2-influence-lines/>
(address in `shared/pages_url.txt`). All QR codes in `figures/` and in the handouts point there,
one per tab (`qr_s2_explorer.png`, `qr_s2_notes.png`, …).

| Feature | Purpose |
|---|---|
| Mark as read, key points, quick checks (Notes) | self-paced reading, short notes, retrieval practice |
| Progress bar and tab badges | shows what is done in each part |
| Exercise timer (suggested 60 min), first-attempt score, confidence rating, hint count | self-monitoring during practice |
| Learning record (Start) | summary the student can copy into the report |
| Short notes drawer | formula sheet available from every tab |
| BM / EN switch | Malay explanations, technical terms kept in English |
| Theme switch (automatic, light, dark) | display preference |
| Explorer: influence lines R_A to R_F, each switched on or off (all off shows the structure only) | compare lines, or study the structure alone |
| Explorer: group of three loads with chosen values and spacings, with quick fill for a unit load, 2.5 kg and the Test 2 pair | any vehicle or load train |
| Explorer: hover or tap a reaction for its step-by-step calculation (kgf and N) | links each number to the free-body diagrams |
| Lab: example readings for Test 1 and Test 2 | shows what a comparison with theory looks like |

Everything a student enters in the tabs is stored only in that student's browser (`localStorage`).
The one exception is a question typed to Dr RJ once his AI is switched on: it goes through the course's
rz-tutor Worker to the Claude API (Anthropic) to be answered. The Worker keeps counts, never the text, and
the panel asks students not to type names, matric numbers or other personal details. While
`shared/tutor_endpoint.txt` holds no address, nothing leaves the browser.

## Dr RJ, the guide panel and AI tutor

Beside the tabs stands a guide panel fronted by the lecturer's avatar, Dr RJ (Dr Razin Junior). His
answers are built from this page's own content and cite it: he explains from the notes, says where to read
more, suggests one exercise or Explorer task to practise, and his "Go to" buttons open the right tab,
section or slide. He is instructed never to give the final values of an exercise or write any part of a lab
report, and to remind students once that work handed in for marks must be their own; a golden set of test
questions in rz-tutor-worker checks this before each release. On phones the panel moves below the content and a round
Dr RJ button brings it back into view.

The answers come from the rz-tutor Worker (Cloudflare), which holds the API key and reads the files in
`tutor/` and `../tutor/` from this website. Those files and the panel are written by `web/add_tutor.py`
on every build; exercise answers, hints and worked solutions are left out of them. While
`shared/tutor_endpoint.txt` holds no Worker address, Dr RJ is in offline mode: he points to the sections
whose titles match the question, and no request is made.

Earlier versions of the page are kept in [`archive/`](archive/), each with a banner that points here.

**The exercise answers are embedded in the page**, so the online Exercises tab is for formative
practice. Use the printed sheet for graded work.

## Printed material

| Item | Source | Built PDF |
|---|---|---|
| Lecture notes (9 pp, A4) | `notes/s2_lecture_notes.tex` | `pdf/s2_lecture_notes.pdf` |
| Slides (28 frames, 16:9, Beamer/metropolis) | `slides/s2_slides.tex` | `pdf/s2_slides.pdf` |
| Exercise sheet, student version (10 questions, 60 marks + 4 bonus) | `exercises/s2_exercises.tex` | `pdf/s2_exercises_student.pdf` |
| Exercise sheet, instructor key | same source with `\def\showkey{1}` | not published here |
| One-page activity handout (predict, scan, check) | `activity/s2_activity_sheet.tex` | `pdf/s2_activity_sheet.pdf` |

The instructor key PDF is deliberately left out of this public repository; rebuild it locally
with `./build.sh`. The answers are, however, also in `exercises/s2_exercises.tex`.

## Building

```bash
./build.sh                                           # XeLaTeX with Latin Modern; also builds the page and Dr RJ
python3 web/build_web.py && python3 web/add_tutor.py  # course page with Dr RJ only
```

`web/add_tutor.py` needs beautifulsoup4 (`python3 -m pip install --user beautifulsoup4`). It refuses to run
twice on the same `index.html`; run `web/build_web.py` first. `web/rz-tutor/` is a pinned copy of the panel,
widget and tools of rz-tutor-worker (MIT; see its `VERSION`).

`web/src/` holds the page sources (two CSS files, three HTML parts and `app.js`).
`web/build_web.py` inserts the photo and QR code from `shared/*_b64.txt` and writes `index.html`
and `activity/influence-line-explorer.html` (the form published as a claude.ai artifact).
`shared/s2_numbers.py` computes every number used in the notes, slides and keys.

The practice readings in Exercise Question 6 and the Lab tab are synthetic (theory ± 1–2
divisions) and labelled as illustrative. Replace them with a real data set when one is available.

## Avatar and slide PDFs

`avatar/` holds the author's avatar: the original sheet (`avatar_sheet.png`), ten cut-out poses as PNG (used by the LaTeX
files) and WebP (embedded in the page by `web/build_web.py`), and a round head badge. The page shows a pose in each tab, the
badge in the header, the footer and every slide footer.

`pdf/s2_slides_online_EN.pdf` and `_BM.pdf` are vector prints of the 21 slides of the page, linked from the slide toolbar.
Regenerate them after changing the slides with `node web/make_slide_pdfs.js <dir>`, where `<dir>/node_modules` contains
`mathjax` 3.2.2 and `@ibm/plex-sans`, `@ibm/plex-serif`, `@ibm/plex-mono` (npm), and poppler's `pdfunite` is installed.

## Copyright

© 2026 Ahmad Razin Zainal Abidin and co-authors, Faculty of Civil Engineering, Universiti Teknologi Malaysia. Free to share and adapt for non-commercial teaching and learning.
