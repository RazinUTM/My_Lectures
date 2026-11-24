"""Render every QR slide of the six published deck folders and decode the codes.

Checks: each QR decodes, the decoded URL is one of the four lab URLs, and the
expected lab appears on the expected slide. Decoding is repeated at 1/2 and 1/3
scale as a rough proxy for reading the code off a projector screen.
"""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright
from PIL import Image
import zxingcpp

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from decklib import LABS

EXPECT = {
    ("w9", "qr-shape"): ["shape"],
    ("w10", "qr-heat"): ["heat"],
    ("w11", "qr-cant-w11"): ["cant"],
    ("w12", "qr-cant-w12"): ["cant"],
    ("w13", "qr-stress"): ["stress"],
    ("w14", "qr-predict"): ["cant", "stress"],
}
URL2KEY = {v[0]: k for k, v in LABS.items()}

from fontcss import font_css
css = font_css() + """
body{margin:0;background:#fff;font-family:"IBM Plex Sans",Arial,sans-serif}
h1,h2,h3,p,ul{margin:0} ul{padding-left:1.1em} img{display:block} svg{display:block}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #ddd;padding:0.35em 0.6em}"""

out = HERE / "test_out" / "qr_check"
out.mkdir(parents=True, exist_ok=True)
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for (wk, sid), keys in EXPECT.items():
        root = HERE / f"deck_{wk}"
        order = json.loads((root / "project/deck.json").read_text())["order"]
        assert sid in order, f"{sid} missing from {wk} deck order"
        s = (root / f"project/slides/{sid}.html").read_text()
        s = re.sub(r"<aside>.*?</aside>", "", s, flags=re.S)
        s = re.sub(r'<section id="([^"]+)" data-transition="[^"]+" style="',
                   r'<section id="\1" style="position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;',
                   s, count=1)
        f = out / f"{wk}_{sid}.html"
        f.write_text(f"<html><head><style>{css}</style></head><body>{s}</body></html>")
        pg.goto("file://" + str(f.resolve()))
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        png = out / f"{wk}_{sid}.png"
        pg.screenshot(path=str(png))
        im = Image.open(png).convert("L")
        for scale in (1, 2, 3):
            img = im if scale == 1 else im.resize((1920 // scale, 1080 // scale), Image.LANCZOS)
            res = zxingcpp.read_barcodes(img)
            urls = sorted(r.text for r in res)
            got = sorted(URL2KEY.get(u, "??" + u) for u in urls)
            ok = got == sorted(keys)
            fails += not ok
            print(f"{wk:4s} {sid:13s} 1/{scale}: {'PASS' if ok else 'FAIL'}  {got}  "
                  f"{[r.format.name for r in res]} pos={[ (r.position.top_left.x, r.position.top_left.y) for r in res]}")
    b.close()
print("FAILURES:", fails)
