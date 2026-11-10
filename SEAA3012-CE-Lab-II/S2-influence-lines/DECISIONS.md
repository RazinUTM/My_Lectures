# Decisions · Lab S2 Influence Lines

| Date | Decision | Why |
|---|---|---|
| 8 Nov 2026 | Dr RJ guide panel added by the build (`web/add_tutor.py`), not by hand | `index.html` is generated; a hand edit would vanish at the next build |
| 10 Nov 2026 | Header moved to the T&L app template: crumbs, contact line, kicker, foldable description, search, Short notes, settings buttons, home icon in the tab bar | same header as the lecturer's other apps (owner's request) |
| 10 Nov 2026 | Settings buttons per rz-settings-buttons: BM/EN · theme · AA · ⓘ, 30 × 30 px, applied before first paint | one look and one behaviour in every app; replaces the BM|EN segment and the three-state theme button |
| 10 Nov 2026 | Preferences in `seaa3012-prefs` (course-wide), read once from the old `s2-il-v3` lang/theme | the template keeps preferences per course and progress per page |
| 10 Nov 2026 | Text size scales the page content through `--font-scale`; header and tab bar stay in px | the header must not grow with the text size; slides scale with their frame anyway |
| 10 Nov 2026 | Search and screen guide built from the page itself at run time; no network | a hand-kept index drifts; the page must work offline |
| 10 Nov 2026 | Local patch to the pinned tutor widget: notice gate repaints on language change (noted in `web/rz-tutor/VERSION`) | the notice stayed in the first language; to be promoted to rz-tutor-worker |
