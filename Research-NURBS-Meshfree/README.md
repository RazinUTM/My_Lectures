# NURBS–meshfree research primer

Faculty of Civil Engineering, Universiti Teknologi Malaysia. A self-study primer for research students
(postgraduate and final-year project) joining the group's work on NURBS-based meshfree methods: how the
CAD geometry and the meshfree approximation are built, the exact point where they meet, and how to read
and reproduce the papers of the area.

Website: <https://razinutm.github.io/My_Lectures/Research-NURBS-Meshfree/>

| Part | Folder | Contents |
|---|---|---|
| 1 Foundations | [`01-foundations/`](01-foundations/) | knot vectors and the Cox–de Boor recursion, NURBS and the exact circle, reproducing-kernel shape functions, blossom vectors (RK with blossom vectors = B-splines), reading the literature like a reproducer |
| 2 Coupling IGA and meshfree regions | planned | Wang & Zhang (2014), Valizadeh et al. (2015), Shaw et al. (2008) |
| 3 Integration, boundaries and consistency | planned | Chen, Hillman & Rüter (2013), Chi & Lin (2016) |
| 4 NURBS-based meshless methods of the group | planned | N-RPIM (Mokhtaram et al. 2022), NDM (Rasin et al. 2025) |

Each part page follows the course pages of this repository: seven tabs (Start, Notes, Slides, Examples,
Exercises, Explorer, Glossary), Bahasa Melayu and English (technical terms stay in English), the settings
buttons (language, theme, text size, screen guide), search, progress, and Dr RJ's guide panel. Dr RJ runs
offline: his steps and pointers come from the page, and no AI service is called (`shared/tutor_endpoint.txt`
holds no address).

## Folder layout

```
Research-NURBS-Meshfree/
├── index.html                primer home: parts, Explorer, Python code, progress export (generated)
├── 01-foundations/
│   ├── index.html            the Part 1 page, engine and styles inlined (generated)
│   └── tutor/                manifest, blocks and plain text for search and the tutor (generated)
├── tutor/course.json         course-wide tutor index (generated)
├── labs/rk-bspline.html      B-spline and RK Explorer (hand-written, standalone or embedded)
├── code/nmf_bspline_rk.py    companion Python code; the page's worked numbers are imported from it
├── shared/                   site.css, site.js (the engine), avatar/, tutor_endpoint.txt
└── web/                      sources and build: content_p1.py, build.py, render_eq.cjs, rz-tutor/ (pinned)
```

## Build

Requires Python 3.9+ and Node 18+ (MathJax runs at build time only).

```bash
cd web && npm ci && cd ..      # mathjax-full 3.2.2 into web/node_modules (not committed)
python3 -B web/build.py        # writes the part page, its tutor files and the primer home
```

Edit the content in `web/content_p1.py`, the engine in `shared/site.js` and the styles in `shared/site.css`;
never edit a generated page by hand. Equations are rendered to SVG with their TeX kept in `data-tex`, so
screen readers and the tutor manifest can read them.

## Python code

`code/nmf_bspline_rk.py` implements the equations of Part 1 in the notes' notation: B-splines, Greville
points, blossom vectors, a NURBS curve, standard RK and RK with blossom vectors. Running it prints the
numbers of Examples 1–3 and the check that RK with blossom vectors gives the B-splines for three kernels.
Requires Python 3.8+ and numpy.

## Validation status (10 November 2026)

- The worked numbers on the page are imported from `code/nmf_bspline_rk.py` at build time, so the page and
  the code cannot disagree.
- Explorer: RK with blossom vectors equals the B-splines to round-off, worst max |Ψ − N| = 6.1 × 10⁻⁹ over 144
  settings (degree 1–3; 2, 4, 7 and 8 spans; three knot positions; four kernels); the deviation comes from the
  moment matrix becoming ill-conditioned next to a knot. B-spline values agree with the Python code to six
  decimals.
- Exercises: for the stored seed, every generator's answers are accepted by its own checker.
- Page (Playwright, Chrome): 53 behaviour checks at 1440 and 390 px, light and dark, BM and EN, and with
  localStorage blocked; all 62 page routes, 13 guide targets and 60 unique manifest ids; search finds every
  section title in both languages; no console errors or failed requests.
- Not checked: Safari and Firefox; screen readers beyond the ARIA attributes; the AI tutor (off).

## Licence

© 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia. Content CC BY-NC-SA 4.0, code MIT, the
lecturer's avatar excepted: see [`LICENSE.md`](LICENSE.md).

## AI-assisted development

The content, the engine, the Explorer and the build scripts were drafted with Claude (Anthropic) and are
reviewed by the author before release; see [`AI_USAGE.md`](AI_USAGE.md). Design decisions are recorded in
[`DECISIONS.md`](DECISIONS.md).

## Third-party components

MathJax runs at build time and its SVG output is embedded in the pages; the guide panel is a pinned copy of
the author's own rz-tutor-worker. See [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

Author: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin (arazin@utm.my).
