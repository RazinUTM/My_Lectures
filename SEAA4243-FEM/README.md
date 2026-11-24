# SEAA 4243 Finite Element Method

Faculty of Civil Engineering, Universiti Teknologi Malaysia. Two-dimensional problems: heat
transfer and plane stress by finite elements, then one session with ANSYS.

Website: <https://razinutm.github.io/My_Lectures/SEAA4243-FEM/>

| Part | Folder | Contents |
|---|---|---|
| 2D Heat Transfer, Part 1 | [`01-heat-transfer-1/`](01-heat-transfer-1/) | PDE, boundary conditions, the four-node element, shape functions, gradient and flux |
| 2D Heat Transfer, Part 2 | [`02-heat-transfer-2/`](02-heat-transfer-2/) | Galerkin, integration by parts, [k], assembly, essential conditions, the worked example |
| Plane Stress, Part 1 | [`03-plane-stress-1/`](03-plane-stress-1/) | equilibrium, Hooke’s law (plane stress and plane strain), strain–displacement, boundary conditions, [N] |
| Plane Stress, Part 2 | [`04-plane-stress-2/`](04-plane-stress-2/) | Galerkin, [B], the 8 × 8 [k], consistent loads, assembly, the cantilever solved and checked |
| Plane Stress, Part 3 | [`05-plane-stress-3/`](05-plane-stress-3/) | stress recovery, principal and von Mises stresses, accuracy and singularities, the 8-node element, the project |
| ANSYS demo | [`06-ansys-demo/`](06-ansys-demo/) | the plate and the cantilever rebuilt in Workbench, four wrong models, verification against validation and the stage gates of the project |

The pages follow the lecturer's T&L app template, the same as the SEAA 4333 Units: a header with the
way back (For My Students › My Lectures › SEAA 4243 › part), the lecturer's email, a foldable
description, a search box over the page, the part switcher, Short notes, and the settings buttons
(BM/EN · theme · text size AA · screen guide ⓘ with a tour). Each part page has eight tabs: Start (plan
and progress), Notes (with quick checks and “Try it yourself” boxes that open the matching Explorer task
and lead back to the same place in the notes), Slides (viewer and PDF), Examples (model answers in exam
form), Exercises (new numbers each attempt), Explorer, Glossary and Feedback. The slide viewer has first/last buttons, a page
slider, mouse-wheel and swipe paging, and a PDF download. Explanations switch between English and
Bahasa Melayu; technical terms stay in English.

## Folder layout

```
SEAA4243-FEM/
├── index.html                course home: parts, Explorers, Python code, progress export
├── 01-heat-transfer-1/       one folder per part
│   ├── index.html            the part page (engine and styles inlined)
│   ├── slides/deck.html      slide sections, loaded by the Slides tab
│   ├── slides/img/           slide images
│   └── pdf/                  slides as PDF
├── labs/                     the Explorers (interactive, also linked by QR codes in the slides)
├── code/                     companion Python code and READMEs (the pages zip them on download)
├── tutor/                    course.json and extra/ for Dr RJ (each part folder has its own tutor/)
├── tools/                    add_tutor.py and the pinned rz-tutor panel and feedback code
├── src/                      the sources the pages are built from (see src/README.md)
└── shared/                   course.css and course.js, the engine the pages inline; annotate.js, the annotation toolbar; avatar/; tutor_endpoint.txt; whats_new.txt
```

Progress, language, theme and text size are kept in the student's own browser
(localStorage); the course home can export and import it.

Every page has a pencil button at the bottom right: the annotation toolbar, for writing on the screen while
teaching (five pens, line thickness, an eraser that removes whole lines, clear all, and a blank page behind the
writing from 0% to 100%; mouse, touch or pen). While it is on, the page cannot
be clicked or scrolled; Esc or the pencil turns it off. What is written stays only while the page is open and
is never stored or sent; the browser remembers only the pen and where the toolbar was put (`rz-annotate`).
The code is one file, `shared/annotate.js`: the source of record for the lecturer's other courses, which carry a copy.

## Dr RJ, the guide panel

Each part page has the guide panel with Dr RJ (Dr Razin Junior), the lecturer's avatar, beside the
contents. In offline mode he points to the matching sections of the page and nothing typed leaves the
browser. When the AI tutor is switched on (the secret `AI_SEAA4243` of the rz-tutor Worker, app
`seaa4243` in [RazinUTM/rz-tutor-worker](https://github.com/RazinUTM/rz-tutor-worker)), his panel shows a
notice first; the questions then typed to him go through the course server to an AI service (Anthropic,
model Claude Haiku 5.5) to be answered from this part's material, and the server keeps counts only, not
the questions. Exercise answers, hints and worked solutions are never sent to the AI.

The tutor files are generated from the pages: `<part>/tutor/` (manifest, blocks and plain text, in
English and as the page reads in Bahasa Melayu), `tutor/course.json` for the course, and
`tutor/extra/` (the lecturer's rz-tools heat-conduction text, a supplementary document for Parts 1–2).
`tools/add_tutor.py` writes them and adds the panel; `tools/rz-tutor/` is the pinned panel code
(see its VERSION); `shared/tutor_endpoint.txt` holds the Worker address.

The Feedback tab (rating, the point still unclear, mistake report, and "What's new" from
`shared/whats_new.txt`) sends to the same Worker (`/v1/feedback`). Its forms stay disabled until the
Worker has `"feedback": true` for app `seaa4243`.

## Python code

`code/fe_shape_functions.py`, `code/fe_heat_q4.py` and `code/fe_plane_stress.py` follow the notes
step by step in the text's notation. Each reproduces the course example when run; the README
next to it lists the expected output. Requires Python 3.8+ and numpy (matplotlib for plots).

Each part's Explorer tab also has a **Run in browser** panel (trial): three short scripts that
import the part's module, editable and run in the student's browser with Pyodide 0.29.5
(Python 3.13, numpy, matplotlib), in a Web Worker so Stop can end a runaway loop. The first run
downloads about 9 MB (about 20 MB once a script plots); nothing is sent anywhere. It runs on
GitHub Pages and on a local server; other hosts show the scripts with a link here.

## Text and licence

Text: Mohd Yassin et al., *Two-Dimensional Finite Element Formulations for Heat, Solids and
Fluids (with Matlab)*, MSNM 2020. Course material: CC BY-NC-SA 4.0; code: MIT. See
[`LICENSE.md`](LICENSE.md). Third-party images are credited where they appear.

Lecturers: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin (arazin@utm.my) and Dr. Yip Bao Fang.
