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
import json
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


def read_whats_new(path: Path) -> list[dict]:
    """Lines `YYYY-MM-DD | English | Bahasa Melayu` (# comments and blank lines skipped), newest first."""
    items = []
    if not path or not Path(path).exists():
        return items
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]):
            raise SystemExit(f"{path}:{n}: expected 'YYYY-MM-DD | English | Bahasa Melayu', got {line!r}")
        en = parts[1]
        ms = parts[2] if len(parts) > 2 and parts[2] else en
        items.append({"date": parts[0], "en": en, "ms": ms})
    return sorted(items, key=lambda x: x["date"], reverse=True)


def read_token(path: Path) -> str:
    """The first non-comment line of a token file (a Cloudflare Web Analytics site token), else ''."""
    if not path or not Path(path).exists():
        return ""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            if not re.fullmatch(r"[A-Za-z0-9]{16,64}", line):
                raise SystemExit(f"{path}: the Web Analytics token should be 16-64 letters and digits, got {line!r}")
            return line
    return ""


def inject_feedback(html: str, app: str, part: str, whats_new: list[dict] | None = None, manifest: str = "tutor/manifest.json") -> tuple[str, list[str]]:
    """Inline the Feedback tab module (feedback/feedback.css and feedback.js) and mount it into the page's
    `<div id="rzfeedback">`, which the page source places in its Feedback tab. The Worker address comes
    from the page's `<meta name="rz-tutor">` at run time, so add_panel's inject() must run as well."""
    if 'id="rzfeedback"' not in html:
        raise SystemExit('the page has no <div id="rzfeedback"> (put one in its Feedback tab)')
    if "window.RzFeedback" in html:
        raise SystemExit("the page already has the feedback module; nothing done")
    css = (HERE / "feedback" / "feedback.css").read_text(encoding="utf-8")
    js = (HERE / "feedback" / "feedback.js").read_text(encoding="utf-8")
    conf = json.dumps({"root": "#rzfeedback", "app": app, "part": part, "manifest": manifest, "whatsNew": whats_new or []},
                      ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("</head>", f"<style>\n/* rz feedback tab (rz-tutor-worker) */\n{css}</style>\n</head>", 1)
    tail = f"<script>\n{js}</script>\n<script>window.RzFeedback.mount({conf});</script>\n"
    html = html[: html.rfind("</body>")] + tail + html[html.rfind("</body>"):]
    return html, [f"head: feedback CSS; body end: feedback module, mounted in #rzfeedback ({len(whats_new or [])} 'What's new' items)"]


def inject_analytics(html: str, token: str) -> tuple[str, list[str]]:
    """Add the Cloudflare Web Analytics beacon (cookie-free page-view counts) when a site token is given."""
    if not token:
        return html, ["analytics: no token, no beacon"]
    if "cloudflareinsights.com/beacon" in html:
        raise SystemExit("the page already has the Web Analytics beacon; nothing done")
    tag = (f"<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
           f"data-cf-beacon='{{\"token\": \"{token}\"}}'></script>\n")
    html = html[: html.rfind("</body>")] + tag + html[html.rfind("</body>"):]
    return html, ["body end: Cloudflare Web Analytics beacon"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("page")
    ap.add_argument("--app", required=True)
    ap.add_argument("--part", required=True)
    ap.add_argument("--endpoint", default="", help="Worker URL …/v1/chat; leave empty until deployed (offline quote mode)")
    ap.add_argument("--css", default="", help="extra CSS for this page, e.g. ':root{--rz-top:82px}' when the page has a sticky tab bar")
    ap.add_argument("--hook", nargs=3, action="append", default=[], metavar=("PATTERN", "WHERE", "CODE"), help="WHERE: before | after | after-statement")
    ap.add_argument("--feedback", action="store_true", help='also inline the Feedback tab module (the page needs <div id="rzfeedback">)')
    ap.add_argument("--whats-new", default="", help="a file of 'YYYY-MM-DD | English | Bahasa Melayu' lines for the Feedback tab")
    ap.add_argument("--analytics-token", default="", help="a Cloudflare Web Analytics site token: adds the cookie-free beacon")
    ap.add_argument("--write", action="store_true", help="write the page in place (otherwise dry run)")
    ap.add_argument("--out", default="", help="write to another path instead of in place")
    a = ap.parse_args()
    page = Path(a.page)
    html = page.read_text(encoding="utf-8")
    new, log = inject(html, a.app, a.part, a.endpoint, [tuple(h) for h in a.hook], a.css)
    if a.feedback:
        new, more = inject_feedback(new, a.app, a.part, read_whats_new(Path(a.whats_new)) if a.whats_new else [])
        log += more
    if a.analytics_token:
        new, more = inject_analytics(new, a.analytics_token)
        log += more
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
