#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Print slides/deck.html to pdf/columns-1-slides.pdf, one 1920 × 1080 page per slide.

What: serves this topic folder on a local port, opens a print page that holds every slide of
slides/deck.html with the same base styles as the Slides tab, waits for the fonts and images, and prints it
with Chromium (Playwright) at 1920 × 1080 px per page.

How to call it, from this topic folder:
  python3 web/make_slides_pdf.py                    # fonts from Google Fonts
  python3 web/make_slides_pdf.py --fonts <dir>      # fonts from local @fontsource packages (no network)
Needs Python Playwright with its Chromium.

Why it is like this: the PDF is the copy students download and annotate, so it is printed from the same
deck.html the page shows; no slide is redrawn by hand.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

topic = Path(__file__).resolve().parent.parent
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400"
         "&family=JetBrains+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap")
BASE_CSS = """@page{size:1920px 1080px;margin:0}
html,body{margin:0;padding:0;background:#fff}
.sl{position:relative;width:1920px;height:1080px;overflow:hidden;break-after:page;page-break-after:always}
.sl section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;font-family:"IBM Plex Sans",system-ui,sans-serif}
.sl h1,.sl h2,.sl h3,.sl p,.sl ul,.sl ol{margin:0}
.sl ul,.sl ol{padding-left:1.1em}
.sl h1,.sl h2,.sl h3{font-weight:600}
.sl table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
.sl td,.sl th{border:1px solid #ddd;padding:.35em .6em;text-align:left;vertical-align:top}
.sl th{font-weight:600}
.sl img,.sl svg{display:block}
.sl x-shape[kind=arrow-right]{display:block;clip-path:polygon(0 25%,60% 25%,60% 0,100% 50%,60% 100%,60% 75%,0 75%)}
.sl a{color:inherit}
"""
FAMS = {"archivo": "Archivo", "atkinson-hyperlegible": "Atkinson Hyperlegible", "jetbrains-mono": "JetBrains Mono", "ibm-plex-sans": "IBM Plex Sans"}


def local_font_css(root: Path) -> str:
    rules = []
    for pkg, fam in FAMS.items():
        for f in sorted((root / pkg / "files").glob(f"{pkg}-latin-*-*.woff2")):
            w, style = f.stem.split("-latin-")[1].split("-")[:2]
            rules.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};src:url(https://fonts.gstatic.com/local/{pkg}/{f.name}) format('woff2')}}")
    return "\n".join(rules)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fonts", default="", help="folder holding @fontsource/<family> packages, to print without network")
    a = ap.parse_args()
    deck = (topic / "slides" / "deck.html").read_text(encoding="utf-8")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):            # no request log on the console
            pass
    handler = functools.partial(Quiet, directory=str(topic))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><base href="http://127.0.0.1:{port}/">'
           f'<link rel="stylesheet" href="{FONTS}"><style>{BASE_CSS}</style></head><body>{deck}</body></html>')
    out = topic / "pdf" / "columns-1-slides.pdf"
    out.parent.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            if a.fonts:
                root = Path(a.fonts)
                css = local_font_css(root)
                page.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=css))
                page.route("https://fonts.gstatic.com/local/**", lambda r: r.fulfill(status=200, content_type="font/woff2",
                           body=(root / r.request.url.split("/local/")[1].split("/")[0] / "files" / r.request.url.rsplit("/", 1)[1]).read_bytes()))
            page.set_content(doc, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(500)
            n = page.evaluate("document.querySelectorAll('.sl').length")
            page.pdf(path=str(out), width="1920px", height="1080px", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            browser.close()
    finally:
        httpd.shutdown()
    print(f"{out.relative_to(topic)}: {n} pages, {out.stat().st_size / 1024:.0f} kB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
