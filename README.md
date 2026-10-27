# My Lectures

Teaching material, Faculty of Civil Engineering, Universiti Teknologi Malaysia. One folder per course.

## Courses

| Course | Folder | Contents |
|---|---|---|
| SEAA 3012 Civil Engineering Laboratory II | [`SEAA3012-CE-Lab-II/`](SEAA3012-CE-Lab-II/) | S2 Influence Lines |

## How the repository is organised

```
My_Lectures/
├── README.md                     this index
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
