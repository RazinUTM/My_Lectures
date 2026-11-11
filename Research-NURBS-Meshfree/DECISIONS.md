# Decisions

Defaults chosen while building are marked "for the author to confirm"; the rest come from the author's own
template (rz-tnl-app-template, rz-settings-buttons) or from his instructions.

## 2026-11-09 Place and folder name
Decision: `Research-NURBS-Meshfree/` in My_Lectures, beside the course folders; the primer home at its root.
Alternatives: a separate repository; `RESEARCH-Meshfree/` (the name used by the parallel N-RPIM site, see Open items).
Rationale: the primer belongs to no course, so the course-code-first rule does not apply; one repository keeps one GitHub Pages site.
Decided by: Claude (default, for the author to confirm).

## 2026-11-09 Tutor: scripted guide, AI off
Decision: Dr RJ's panel with scripted steps (Go to / Hint / Skip) and the screen guide; the AI chat ships offline (empty `shared/tutor_endpoint.txt`).
Alternatives: AI-assisted through rz-tutor-worker.
Rationale: the template's default; switching the AI on needs an `apps.json` entry, a class code and the golden set, and then only the endpoint line changes.
Decided by: the author's template.

## 2026-11-09 Engine: new `shared/site.js`, styles from SEAA 4243
Decision: a new engine for the template's header (search, fold, contact, settings buttons), views, progress, exercises, slides, Explorer sync, a compact scripted guide and the screen guide; `course.css` reused and extended.
Alternatives: copy SEAA 4243 `course.js` (no search, fold or guide, old A−/A+ buttons); port IMPAK `uikit.js` as `shared/guide.js`.
Rationale: fewer moving parts for one page; the compact guide lives in the rz-tutor panel bubble. Candidate to promote back to the source of record once the two T&L sites converge (Open items).
Decided by: Claude (for the author to confirm).

## 2026-11-09 Contact line, language and BM
Decision: contact line shows the UTM email only; default language BM; technical terms stay English; BM follows the Project glossary (`glossary-bm.md`: artikel, jejari, konsistensi, menghasilkan semula, derivation in English).
Alternatives: office phone in the contact line, as the template shows.
Rationale: the phone number was not available; the glossary already settles the terms used across the group's cracks.
Decided by: Claude (phone number needs the author's input).

## 2026-11-10 Equations at build time
Decision: TeX → SVG with MathJax 3.2.2 at build time, one glyph cache per equation, glyph ids re-prefixed when an equation appears twice (notes and slides), TeX kept in `data-tex`.
Alternatives: MathJax in the browser (runtime dependency, network); one global glyph cache.
Rationale: no runtime dependency; screen readers and the tutor manifest read the TeX; duplicate ids would be invalid HTML.
Decided by: Claude (template rule: equations pre-rendered, sources kept).

## 2026-11-10 Explorer design
Decision: one lab, B-splines against RK with blossom vectors or with node monomials (support a = c_a h); evaluated at cell midpoints, never on a knot, where one kernel vanishes and [M] is singular; palette from the validated dataviz slots (light #2a78d6 / #eb6834, dark #3987e5 / #d95926); it follows the part page's language, theme and text size by postMessage (works with storage blocked) and posts its height so the frame needs no inner scroll bar.
Alternatives: separate labs per mode; evaluate on a uniform grid including knots.
Rationale: the contrast between the modes is the lesson of Section 5; a knot-hitting grid shows spurious singular points.
Decided by: Claude (for the author to confirm).

## 2026-11-10 Parts 2–4 and the papers
Decision: Parts 2–4 planned around the papers already cracked: Wang & Zhang (2014), Valizadeh et al. (2015), Shaw et al. (2008); Chen, Hillman & Rüter (2013), Chi & Lin (2016); Mokhtaram et al. (2022), Rasin et al. (2025). Papers are cited, never reproduced; no figure from a paper is used.
Decided by: Claude, from the crack list (for the author to confirm).

## Open items for the author
1. A parallel T&L site exists: "N-RPIM research notes", folder `RESEARCH-Meshfree/01-nurbs-rpim/`, built on 10 November 2026 in another session from the Mokhtaram et al. (2022) crack, delivered as a zip and not pushed. Proposal: one folder name and one guide engine; that site becomes Part 4 (or a part of its own) of this primer.
2. Office phone number for the contact line.
3. A link from people.utm.my/arazin "For My Students" (razin-site `pages/for-my-students.html`).
4. AI tutor go-live (apps.json entry, class code, golden set), if wanted.
5. The author's review of the content and of the BM (glossary-aligned pass done; full audit with `terjemah-bm-dbp` not yet).
