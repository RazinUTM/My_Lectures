# My Lectures

Teaching material, Faculty of Civil Engineering, Universiti Teknologi Malaysia. One folder per course.

Website (GitHub Pages): <https://razinutm.github.io/My_Lectures/>

## Courses

| Course | Folder | Contents |
|---|---|---|
| SEAA 3012 Civil Engineering Laboratory II | [`SEAA3012-CE-Lab-II/`](SEAA3012-CE-Lab-II/) | S2 Influence Lines |
| SEAA 4243 Finite Element Method | [`SEAA4243-FEM/`](SEAA4243-FEM/) | 2D Heat Transfer (Parts 1–2); Plane Stress and ANSYS to follow |

## How the repository is organised

```
My_Lectures/
├── README.md                     this index
├── index.html                    landing page of the website
├── .nojekyll                     serve files as they are (no Jekyll build)
├── SEAA3012-CE-Lab-II/           one folder per course: <course code>-<short name>
│   ├── README.md                 list of topics in the course
│   └── S2-influence-lines/       one folder per topic, lab or week
│       ├── index.html            interactive course page (opens in any browser)
│       ├── pdf/                  built handouts
│       ├── notes/ slides/ exercises/ activity/   LaTeX sources
│       ├── shared/ figures/ web/                 shared data, figures, page sources
│       └── build.sh
└── <next course code>-<short name>/
```

Conventions: no spaces in folder names; course code first so courses sort together; each topic
folder builds on its own with its own `build.sh`; answer keys and instructor-only files are not
committed (see `.gitignore`).
