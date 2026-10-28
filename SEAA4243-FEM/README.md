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
| ANSYS demo | coming | the plate and the cantilever rebuilt in Workbench |

Each part page has seven tabs: Start (plan and progress), Notes, Slides (viewer and PDF),
Examples (model answers in exam form), Exercises (new numbers each attempt), Explorer, Glossary.
Explanations switch between English and Bahasa Melayu; technical terms stay in English.

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
└── shared/                   course.css and course.js, the engine the pages inline
```

Progress, language, theme and text size are kept in the student's own browser
(localStorage). Nothing is sent anywhere; the course home can export and import it.

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

Lecturer: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · arazin@utm.my
