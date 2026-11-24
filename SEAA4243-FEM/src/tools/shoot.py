"""Screenshot every tab of a part page in both themes and two widths; report console errors.
python3 shoot.py 01-heat-transfer-1 [out_dir]"""
import http.server, pathlib, socketserver, sys, threading, functools, json
from playwright.sync_api import sync_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
slug = sys.argv[1]; out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else SITE.parent / "shots"); out.mkdir(parents=True, exist_ok=True)
FONTS = SITE.parent.parent / "fonts"; FCSS = (pathlib.Path(__file__).resolve().parent / "fonts_http.css").read_text()
class H(http.server.SimpleHTTPRequestHandler):
    """Serves the site; /__fonts/ maps to the local Fontsource files so renders use the real fonts."""
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def translate_path(self, path):
        if path.startswith("/__fonts/"): return str(FONTS / path[len("/__fonts/"):].split("?")[0])
        return super().translate_path(path)
    def log_message(self, *a): pass
Handler = H
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(("127.0.0.1", 0), Handler); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/{slug}/index.html"
errors = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme, width in [("light", 1280), ("dark", 1280), ("light", 390), ("dark", 390)]:
        ctx = b.new_context(viewport={"width": width, "height": 900 if width > 400 else 844}, color_scheme=theme, device_scale_factor=1)
        pg = ctx.new_page()
        pg.on("console", lambda m: errors.append((m.type, m.text)) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errors.append(("pageerror", str(e))))
        pg.route("https://fonts.googleapis.com/**", lambda route: route.fulfill(status=200, content_type="text/css", body=FCSS.replace("/__fonts/", f"http://127.0.0.1:{port}/__fonts/")))
        pg.goto(url); pg.wait_for_timeout(1500); pg.evaluate("document.fonts.ready")
        for view in ["start", "notes", "slides", "examples", "exercises", "lab", "glossary"]:
            pg.click(f'.tab[data-view="{view}"]'); pg.wait_for_timeout(900 if view in ("slides", "lab") else 400)
            if view == "slides": pg.wait_for_timeout(1500)
            full = view in ("notes", "exercises", "start", "examples")
            pg.screenshot(path=str(out / f"{slug}_{view}_{theme}_{width}.png"), full_page=full)
        if width > 400 and theme == "light":
            # language toggle and drawer
            pg.click('[data-setlang="ms"]'); pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"{slug}_notes_ms_{width}.png"), full_page=True)
            pg.click('[data-setlang="en"]'); pg.click("#snbtn"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"{slug}_drawer_{width}.png"))
            pg.click("#drclose")
        ctx.close()
    b.close()
srv.shutdown()
print("shots in", out); print("console issues:", len(errors))
for e in errors[:20]: print("  ", e)
