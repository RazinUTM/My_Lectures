# Lab S2 · Influence Lines

Teaching package for experiment S2 of *Civil Engineering Laboratory II* (SEAA 3012, Faculty of
Civil Engineering, UTM): a cantilever (Gerber) bridge model with six dial gauges. All material
uses the geometry, halts, notation η_R(x) and sign convention of the revised laboratory manual.

## Course page

`index.html` is a single self-contained page with six tabs: Start, Notes, Slides, Explorer,
Exercises and Lab. It works in any modern browser, on phones as well as projectors. Tabs open
directly with `#notes`, `#slides`, `#explorer`, `#exercises` or `#lab` after the address.

| Feature | Purpose |
|---|---|
| Mark as read, key points, quick checks (Notes) | self-paced reading, short notes, retrieval practice |
| Progress bar and tab badges | shows what is done in each part |
| Exercise timer (suggested 60 min), first-attempt score, confidence rating, hint count | self-monitoring during practice |
| Learning record (Start) | summary the student can copy into the report |
| Short notes drawer | formula sheet available from every tab |
| BM / EN switch | Malay explanations, technical terms kept in English |
| Theme switch (automatic, light, dark) | display preference |

Everything a student enters is stored only in that student's browser (`localStorage`); nothing is
collected or sent anywhere.

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
./build.sh                 # XeLaTeX with Latin Modern; also runs web/build_web.py
python3 web/build_web.py   # course page only
```

`web/src/` holds the page sources (two CSS files, three HTML parts and `app.js`).
`web/build_web.py` inserts the photo and QR code from `shared/*_b64.txt` and writes `index.html`
and `activity/influence-line-explorer.html` (the form published as a claude.ai artifact).
`shared/s2_numbers.py` computes every number used in the notes, slides and keys.

The practice readings in Exercise Question 6 and the Lab tab are synthetic (theory ± 1–2
divisions) and labelled as illustrative. Replace them with a real data set when one is available.
