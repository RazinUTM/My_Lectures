#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Add the guide panel with the Dr RJ tutor widget to an existing T&L page.

What: injects, into one self-contained `index.html`, (1) the panel CSS and the widget CSS before
`</head>`, (2) a `<meta name="rz-tutor" content="<endpoint>">`, (3) `<div class="cols">` around
`<main>…</main>` with the panel fragment after the main column, (4) the widget script and the
page glue (`panel-mount.js`, with the app id and part key filled in) before `</body>`, and (5) the
engine hooks the page needs so that the glue can navigate and change poses.

How to call it (S2 example; the hooks are page-specific, see README "Adding the panel to a page"):

  python3 tools/add_panel.py path/to/index.html --app seaa3012 --part s2 --write \
     --hook 'var AVS={' 'after-statement' 'window.RZ_AVS=AVS;' \
     --hook 'show(start,true);updateProgress();' 'before' 'window.RZ={show:show,goTo:goTo,goSlide:goSlide,current:function(){return current},lang:function(){return ST.lang}};'

Why it is like this: the pages are single files with no build step, so the panel is inlined like
everything else, and the only engine changes are two one-line hooks; the script refuses to run twice
on the same page and prints what it changed so the diff can be reviewed before a commit.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def statement_end(src: str, start: int) -> int:
    """Index of the first ';' at or after start that is not inside a '…', "…" or `…` literal."""
    quote = ""
    k = start
    while k < len(src):
        c = src[k]
        if quote:
            if c == "\\":
                k += 2
                continue
            if c == quote:
                quote = ""
        elif c in "\"'`":
            quote = c
        elif c == ";":
            return k
        k += 1
    raise SystemExit("statement end not found")


def inject(html: str, app: str, part: str, endpoint: str, hooks: list[tuple[str, str, str]], extra_css: str = "") -> tuple[str, list[str]]:
    if 'id="rzguide"' in html:
        raise SystemExit("the page already has the guide panel (id=rzguide); nothing done")
    log: list[str] = []
    css = (HERE / "panel" / "panel.css").read_text(encoding="utf-8") + "\n" + (HERE / "widget" / "tutor-widget.css").read_text(encoding="utf-8")
    panel = (HERE / "panel" / "panel.html").read_text(encoding="utf-8")
    js = (HERE / "widget" / "tutor-widget.js").read_text(encoding="utf-8")
    glue = (HERE / "panel" / "panel-mount.js").read_text(encoding="utf-8").replace("__APP__", app).replace("__PART__", part)

    head_add = f'<meta name="rz-tutor" content="{endpoint}">\n<style>\n/* rz guide panel + tutor widget (rz-tutor-worker) */\n{css}{extra_css}\n</style>\n'
    assert "</head>" in html, "no </head>"
    html = html.replace("</head>", head_add + "</head>", 1)
    log.append("head: meta rz-tutor + panel/widget CSS")

    m_open = re.search(r"<main\b[^>]*>", html)
    m_close = html.find("</main>")
    assert m_open and m_close > 0, "no <main>…</main>"
    html = html[: m_open.start()] + '<div class="cols">\n' + html[m_open.start(): m_close + len("</main>")] + "\n" + panel + "</div>\n" + html[m_close + len("</main>"):]
    log.append("body: <div class=cols> around <main>, panel fragment + floating button after it")

    for pat, where, code in hooks:
        i = html.find(pat)
        assert i >= 0, f"hook pattern not found: {pat!r}"
        if where == "after-statement":
            j = statement_end(html, i + len(pat))   # the first ';' outside string literals ("data:image/webp;base64" has one inside)
            html = html[: j + 1] + code + html[j + 1:]
        elif where == "after":
            html = html[: i + len(pat)] + code + html[i + len(pat):]
        else:
            html = html[:i] + code + html[i:]
        log.append(f"hook ({where}) at {pat[:40]!r}: {code[:60]}…")

    tail = f"<script>\n{js}</script>\n<script>\n{glue}</script>\n"
    assert "</body>" in html, "no </body>"
    html = html[: html.rfind("</body>")] + tail + html[html.rfind("</body>"):]
    log.append("body end: widget script + panel glue")
    return html, log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("page")
    ap.add_argument("--app", required=True)
    ap.add_argument("--part", required=True)
    ap.add_argument("--endpoint", default="", help="Worker URL …/v1/chat; leave empty until deployed (offline quote mode)")
    ap.add_argument("--css", default="", help="extra CSS for this page, e.g. ':root{--rz-top:82px}' when the page has a sticky tab bar")
    ap.add_argument("--hook", nargs=3, action="append", default=[], metavar=("PATTERN", "WHERE", "CODE"), help="WHERE: before | after | after-statement")
    ap.add_argument("--write", action="store_true", help="write the page in place (otherwise dry run)")
    ap.add_argument("--out", default="", help="write to another path instead of in place")
    a = ap.parse_args()
    page = Path(a.page)
    html = page.read_text(encoding="utf-8")
    new, log = inject(html, a.app, a.part, a.endpoint, [tuple(h) for h in a.hook], a.css)
    for line in log:
        print("-", line)
    print(f"size {len(html):,} -> {len(new):,} bytes")
    if a.out:
        Path(a.out).write_text(new, encoding="utf-8"); print(f"wrote {a.out}")
    elif a.write:
        page.write_text(new, encoding="utf-8"); print(f"wrote {page}")
    else:
        print("dry run: add --write to change the page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
