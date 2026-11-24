"""Slides handout PDF from the same sections the viewer shows (speaker notes already stripped).
python3 make_pdf.py 01-heat-transfer-1 heat-transfer-1-slides.pdf"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
slug, name = sys.argv[1], sys.argv[2]
part = SITE / slug; frag = (part / "slides/deck.html").read_text()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mj")); from fontcss import font_css; fonts = font_css()
css = (SITE / "shared/course.css").read_text()
# only the slide-canvas rules are needed; the sections keep their inline styles
rules = "\n".join(l for l in css.splitlines() if l.startswith(".frame .cv"))
rules = rules.replace(".frame .cv .sl{position:absolute;inset:0;width:1920px;height:1080px;display:none}", ".frame .cv .sl{width:1920px;height:1080px;display:block;page-break-after:always;break-after:page;overflow:hidden}")
rules = rules.replace(".frame .cv .sl.on{display:block}", "")
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
@page{{size:1920px 1080px;margin:0}} html,body{{margin:0;padding:0;background:#fff}}
.frame .cv{{width:1920px}} {rules}
.frame .cv .sl:last-child{{page-break-after:auto;break-after:auto}}
</style></head><body><div class="frame"><div class="cv">{frag}</div></div></body></html>"""
tmp = part / "_print.html"; tmp.write_text(html)
out = part / "pdf" / name; out.parent.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("file://" + str(tmp)); pg.wait_for_timeout(800); pg.evaluate("document.fonts.ready")
    pg.emulate_media(media="print")
    pg.pdf(path=str(out), width="1920px", height="1080px", print_background=True, prefer_css_page_size=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
    b.close()
tmp.unlink()
try:
    from pypdf import PdfReader
    r = PdfReader(str(out)); print(out.name, len(r.pages), "pages", round(out.stat().st_size / 1e6, 2), "MB")
except ImportError:
    print(out.name, round(out.stat().st_size / 1e6, 2), "MB (pypdf not installed for a page count)")
