# AI use record — SEAA 4243

| Item | How it was made | Human review | Checks |
| --- | --- | --- | --- |
| Dr RJ guide panel on the five part pages, `tools/add_tutor.py`, the engine hook (window.RZ, window.RZ_AVS), the footer line on the AI tutor, `<part>/tutor/` and `tutor/` files, the README section (23 Nov 2026) | AI-generated (Claude; the session is configured for claude-opus-5-5) on the lecturer's request to switch Dr RJ on with the API for SEAA 4243; the panel code is the lecturer's MIT rz-tutor-worker 0.4.3, pinned in `tools/rz-tutor/`; the tutor files are generated from the pages | Lecturer to check the pages and run the golden set before the switch | the five pages in headless Chromium at 1400 px and 400 px (panel, hooks, Go to, no horizontal scroll); the English tutor files of Parts 1–2 are byte-identical to the rz-tutor-worker samples the earlier golden runs used |
