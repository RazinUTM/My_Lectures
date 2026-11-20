#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Turn the Unit 7 slide deck (claude.ai Slides project files) into slides/deck.html for the Slides tab.

What: reads project/deck.json and project/slides/<id>.html from a folder (the Slides artifact's own
files), keeps the slides in deck order, drops the speaker notes (<aside>), drops the slides listed in
SKIP, rewrites any artifact image addresses (/_blob/<id>) to img/<name>.webp (the figures the notes
use too, made by web/make_figs.py) through web/deck_assets.json (the Unit 7 slides already point at
img/<name>.webp, so the map is empty), applies the small web-only edits in EDITS, and writes slides/deck.html: one <div class="sl" data-title="…"> per slide, the format the
course engine's slide viewer reads.

How to call it, from this topic folder:
  python3 web/make_deck.py <folder that holds project/deck.json>

Why it is like this: the lecturer's presenter deck (with notes) stays with the lecturer; the web copy is for
students, so speaker notes and the D7 key-value slide (its answer scheme is released after class) are
left out.
"""
import html
import json
import re
import sys
from pathlib import Path

topic = Path(__file__).resolve().parent.parent
SKIP = {"exam-ans"}                       # D7 key values: released after class, not on the web
EDITS = {}                                # web-only wording (slide id: [(old, new)]); none for Unit 7


def title_of(sec: str) -> str:
    m = re.search(r"<h[12][^>]*>([\s\S]*?)</h[12]>", sec)
    t = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
    return html.unescape(re.sub(r"\s+", " ", t)).strip()


def main(src: Path) -> int:
    deck = json.loads((src / "project" / "deck.json").read_text(encoding="utf-8"))
    assets = json.loads((topic / "web" / "deck_assets.json").read_text(encoding="utf-8"))
    out = []
    for sid in deck["order"]:
        if sid in SKIP:
            continue
        s = (src / "project" / "slides" / f"{sid}.html").read_text(encoding="utf-8")
        s = re.sub(r"\s*<aside>[\s\S]*?</aside>", "", s)
        for old, new in EDITS.get(sid, []):
            assert old in s, f"{sid}: edit target not found: {old!r}"
            s = s.replace(old, new)
        def img(m):
            name = assets.get(m.group(1))
            assert name, f"{sid}: no file for asset {m.group(1)} in web/deck_assets.json"
            return f'src="img/{name}"'
        s = re.sub(r'src="/_blob/([0-9a-f]{32})"', img, s)
        assert "/_blob/" not in s, sid
        t = title_of(s).replace('"', "&quot;")
        out.append(f'<div class="sl" data-title="{t}">{s.strip()}</div>')
    (topic / "slides" / "deck.html").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"slides/deck.html: {len(out)} slides ({', '.join(sorted(SKIP))} left out)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
