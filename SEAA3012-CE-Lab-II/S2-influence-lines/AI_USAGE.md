# AI usage · Lab S2 Influence Lines

| Date | Tool (developer, model) | What it did | Checked by |
|---|---|---|---|
| 10 Nov 2026 | Claude (Anthropic, claude-opus-5-5) in claude.ai | Header on the T&L template, standard settings buttons, page search, screen guide; reused the owner's rz-settings-buttons reference code (MIT, © 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia) | Playwright checks at 1440, 768, 390 and 360 px, light and dark, BM and EN; owner review |
| 11 Nov 2026 | Claude (Anthropic, claude-opus-5-5) in claude.ai | Feedback tab: the tab and its section in `web/src`, `web/add_tutor.py` wiring, `shared/whats_new.txt`, the privacy sentences; the module itself is rz-tutor-worker 0.3.0 (MIT) | Headless Chromium at 1366 and 390 px, EN and BM, light and dark, live (local Worker) and offline; rebuild identical; owner review |

