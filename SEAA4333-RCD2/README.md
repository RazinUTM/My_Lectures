# SEAA 4333 Reinforced Concrete Design II

Faculty of Civil Engineering, Universiti Teknologi Malaysia. Semester 1, 2026/27 (12 October 2026 to
24 January 2027). Five topics in fourteen Units, designed to Eurocode 2: staircases, frame analysis,
columns, foundations and retaining walls.

Website: <https://razinutm.github.io/My_Lectures/SEAA4333-RCD2/>

| Unit | Folder | Contents |
|---|---|---|
| 1 · Staircases I | [`01-staircases-1/`](01-staircases-1/) | geometry by UBBL By-laws 106 and 108, load on plan, the stair as a beam on plan, design and detailing of the waist, the kink |
| 2 · Staircases II | coming | stairs supported by landings, two flights at right angles, stairs with their sides built into walls |
| 3–6 | coming | frame analysis |
| 7 · Columns I | [`07-columns-1/`](07-columns-1/) | braced or unbraced, effective length from the beams at the ends (EC2 Eq. 5.15 and 5.16), slenderness against λ<sub>lim</sub> about each axis |
| 8 · Columns II | [`08-columns-2/`](08-columns-2/) | short columns: the design moment with e<sub>i</sub> and e<sub>0</sub>, strain compatibility and the N–M interaction diagram, design charts drawn for the course and the direct check, bars, cover for fire, links |
| 9 · Columns III | [`09-columns-3/`](09-columns-3/) | slender columns: the second-order moment by nominal curvature (EC2 5.8.8) with creep and the K<sub>r</sub> iteration, braced and unbraced; bending about both axes: the screening of EC2 5.8.9, the enhanced moment and Eq. 5.39 |
| 10 · Foundations I | [`10-foundations-1/`](10-foundations-1/) | foundation types and requirements; the pad footing under an axial load and with a moment: sizing, the pressure when the load moves off-centre (the kern, partial contact, both axes), bending, shear and punching at the critical sections with every perimeter inside 2d (EC2 6.4.4(2)); combined and strip footings; detailing |
| 11 · Foundations II | [`11-foundations-2/`](11-foundations-2/) | a column on the site boundary: the strap footing by statics (moments about the inner column), the net ultimate reactions, the strap's moment, shear and links, and the two footings; the trapezoidal combined footing; piles: types, capacity, number and spacing, the cap size and the load on each pile under moments |
| 12 · Foundations III | [`12-foundations-3/`](12-foundations-3/) | pile caps: the truss analogy for two, three and four piles (T = Ns/4d, Ns/9d, Ns/8d), beam theory at the column faces for six piles under a moment; shear at φ/5 inside the piles with β = max(a<sub>v</sub>, 0.5d)/2d (EC2 6.2.2(6)), the anchorage that the enhancement needs, and the unreduced limit 0.5bdνf<sub>cd</sub>; the column face against 0.4νf<sub>cd</sub>; cracks and detailing |
| 13 · Retaining Walls I | [`13-retaining-walls-1/`](13-retaining-walls-1/) | types of wall and how a wall fails the ground; first dimensions of a cantilever wall; Rankine's active pressure with a surcharge and the two thrusts over H, to the underside of the base; the table of loads and moments about the toe; overturning (EQU), sliding in combination 1 and in EC7 Design Approach 1 Combination 2, the middle third and the bearing pressure in service; sizing the base (the heel holds, the toe spreads) |
| 14 · Retaining Walls II | [`14-retaining-walls-2/`](14-retaining-walls-2/) | the stem, the toe and the heel as three cantilevers and their tension faces; the design pressures under the base (STR) and the net loads; flexure with the minimum steel, shear without links and crack control by the bar spacing of EC2 Table 7.3N; secondary steel, the lap of the starter bars and curtailment; a sloping backfill (Rankine's K<sub>a</sub>, P<sub>h</sub> and P<sub>v</sub>, with P<sub>v</sub> on the heel tip); a key under the base and a water table behind the wall; course review and the examination |

Each Unit page is built on the lecturer's T&L app template: a header with breadcrumbs, search, Short notes
and the settings buttons (BM/EN · theme · text size · screen guide); seven tabs (Start with the plan before,
in and after class; Notes with quick checks; Slides; Examples in answer-scheme form; Exercises with new
numbers on every attempt; Explorer; Glossary); Dr RJ, the guide panel; and the licence footer.
Explanations switch between English and Bahasa Melayu; technical terms stay in English. The printed
workbook stays the book students write in during class.

## Folder layout

```
SEAA4333-RCD2/
├── index.html                course home: Units, Explorers, assessment, progress export (built by shared/build_home.py)
├── 01-staircases-1/          one folder per Unit
│   ├── index.html            the Unit page (built; engine, styles and equations inlined)
│   ├── build.sh              rebuilds index.html: web/build_page.py, then web/add_tutor.py
│   ├── web/src/              page sources (p0–p5 HTML, exercises.js)
│   ├── web/                  build scripts, tex2svg.js (MathJax at build time), rz-tutor/ (pinned panel)
│   ├── img/                  figures (WebP), used by the notes, the examples and the slides
│   ├── slides/deck.html      the Unit deck without speaker notes, loaded by the Slides tab
│   ├── pdf/                  the slides as PDF
│   ├── shared/               tutor_endpoint.txt (empty: Dr RJ in offline mode)
│   └── tutor/                manifest and content for Dr RJ (generated by the build)
├── 07-columns-1/             Unit 7, the same layout
├── 08-columns-2/             Unit 8, the same layout
├── 09-columns-3/             Unit 9, the same layout
├── 10-foundations-1/         Unit 10, the same layout
├── 11-foundations-2/         Unit 11, the same layout
├── 12-foundations-3/         Unit 12, the same layout
├── 13-retaining-walls-1/     Unit 13, the same layout
├── 14-retaining-walls-2/     Unit 14, the same layout
├── labs/staircase.html       the Staircase Lab (Explorer of Unit 1; QR code on the first slide)
├── labs/column.html          the Column Lab (Explorer of Units 7 to 9, six tabs; QR codes on the first slides)
├── labs/foundation.html      the Foundation Lab (Explorer of Units 10 to 12: bearing pressure, critical sections, spot the error, strap footing, pile group, pile cap)
├── labs/retaining-wall.html  the Retaining Wall Lab (Explorer of Units 13 and 14: earth pressure, stability with a design challenge, spot the error, members, key and water)
├── shared/                   course.css, course.js, the avatar poses, the course home source
└── tutor/course.json         every Unit's sections, for the tutor (generated)
```

## Build

From a Unit folder: `./build.sh` (needs Python 3 with Pillow, beautifulsoup4 and lxml, and Node; the
script installs MathJax into `web/node_modules/` on first run). The course home: `python3 shared/build_home.py`.
Open the pages through a local server (`python3 -m http.server` in `My_Lectures/`) so that the slides, the
Explorer and Dr RJ's manifest load.

## Privacy

Progress, preferences, the Staircase Lab's class table and the answers in the Column, Foundation and Retaining Wall Labs are kept in the student's own browser (localStorage);
the course home can export and import them. Dr RJ is in offline mode: he points to sections of the page
and nothing typed leaves the browser. Graded work stays in UTM eLearning.

## Records and licence

[`DECISIONS.md`](DECISIONS.md) · [`AI_USAGE.md`](AI_USAGE.md) · [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).
Course material: CC BY-NC-SA 4.0; code: MIT; the lecturer's avatar is excepted. See [`LICENSE.md`](LICENSE.md).

Lecturer: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin (arazin@utm.my).
