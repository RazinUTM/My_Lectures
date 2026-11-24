"""Targeted screenshots of the way-finding and feedback states. python3 shoot2.py out_dir"""
import http.server, pathlib, socketserver, sys, threading
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
FONTS = SITE.parent.parent / "fonts"; FCSS = (pathlib.Path(__file__).resolve().parent / "fonts_http.css").read_text()
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def translate_path(self, path):
        if path.startswith("/__fonts/"): return str(FONTS / path[len("/__fonts/"):].split("?")[0])
        return super().translate_path(path)
    def log_message(self, *a): pass
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}/"
errors = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme, width in [("light", 1280), ("dark", 390)]:
        ctx = b.new_context(viewport={"width": width, "height": 900 if width > 400 else 844}, color_scheme=theme)
        pg = ctx.new_page()
        pg.on("console", lambda m: errors.append((m.type, m.text)) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errors.append(("pageerror", str(e))))
        pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=FCSS.replace("/__fonts/", f"http://127.0.0.1:{port}/__fonts/")))
        tag = f"{theme}_{width}"
        pg.goto(base + "index.html"); pg.wait_for_timeout(1200)
        pg.screenshot(path=str(out / f"home_top_{tag}.png"))
        pg.locator(".excard").first.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / f"home_explorers_{tag}.png"))
        pg.goto(base + "01-heat-transfer-1/index.html"); pg.wait_for_timeout(1200)
        pg.click('.qc[data-qc="r1"] .opt[data-k="a"]'); pg.click('.qc[data-qc="r2"] .opt[data-k="c"]')
        pg.evaluate("window.scrollTo(0,0)"); pg.screenshot(path=str(out / f"p1_start_{tag}.png"))
        pg.locator("#recall").screenshot(path=str(out / f"p1_recall_{tag}.png"))
        pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"p1_notes_top_{tag}.png"))
        q = pg.locator('.qc[data-qc="q1"]'); q.scroll_into_view_if_needed(); q.locator(".opt").nth(0).click(); pg.wait_for_timeout(100)
        q.screenshot(path=str(out / f"p1_qc_{tag}.png"))
        pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"p1_ex_top_{tag}.png"))
        pg.click('.q[data-q="a1"] .conf button[data-c="sure"]'); pg.click('.q[data-q="a1"] .opt[data-k="b"]')
        pg.click('.q[data-q="a2"] .opt[data-k="b"]')
        pg.locator('.q[data-q="a1"]').screenshot(path=str(out / f"p1_a1_{tag}.png"))
        pg.locator('.q[data-q="a2"]').screenshot(path=str(out / f"p1_a2_{tag}.png"))
        pg.fill('article[data-ex="b2"] input[data-f="gx"]', "20"); pg.fill('article[data-ex="b2"] input[data-f="gy"]', "5")
        pg.click('article[data-ex="b2"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
        pg.locator('article[data-ex="b2"]').screenshot(path=str(out / f"p1_b2_{tag}.png"))
        pg.click('.q[data-q="c1"] .errline button[data-k="2"]')
        pg.locator('.q[data-q="c1"]').screenshot(path=str(out / f"p1_c1_{tag}.png"))
        pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(out / f"p1_lab_top_{tag}.png"))
        pg.locator("#code summary").click(); pg.wait_for_timeout(100)
        pg.locator("#code").screenshot(path=str(out / f"p1_code_{tag}.png"))
        pg.locator(".pagenav").scroll_into_view_if_needed(); pg.screenshot(path=str(out / f"p1_footer_{tag}.png"))
        ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        print(tag, "horizontal overflow px:", ov)
        ctx.close()
    b.close()
srv.shutdown()
print("console issues:", len(errors)); [print("  ", e) for e in errors[:12]]
