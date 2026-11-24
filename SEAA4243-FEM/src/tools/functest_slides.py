"""Slide viewer: first/last buttons, scrubber, mouse wheel, swipe, PDF button; avatar heads on every tab."""
import http.server, socketserver, threading, pathlib, sys
from playwright.sync_api import sync_playwright
import os, tempfile
SITE = pathlib.Path(__file__).resolve().parent.parent.parent      # SEAA4243-FEM
S = pathlib.Path(os.environ.get("SEAA_WORK", os.path.join(tempfile.gettempdir(), "seaa4243-work"))); (S / "shots").mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def log_message(s, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Q); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
fails, ok = [], []
def check(c, m): (ok if c else fails).append(("ok  " if c else "FAIL ") + m)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.route("**/fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{PORT}/05-plane-stress-3/index.html#slides"); pg.wait_for_timeout(2500)
    cnt = lambda: pg.inner_text("#svcount")
    n = pg.evaluate("document.querySelectorAll('#svcv .sl').length")
    pg.click("#svlast"); check(cnt() == f"{n} / {n}" and pg.is_disabled("#svlast") and pg.is_disabled("#svnext"), f"⏭ goes to the last slide ({cnt()})")
    pg.click("#svfirst"); check(cnt() == f"1 / {n}" and pg.is_disabled("#svfirst"), "⏮ goes to the first slide")
    pg.evaluate("(() => { const s = document.querySelector('#svscrub'); s.value = 20; s.dispatchEvent(new Event('input')); })()")
    check(cnt() == f"20 / {n}", f"scrubber jumps to 20 ({cnt()})")
    check("20 ·" in pg.inner_text("#svtip"), "scrubber tip shows the slide title: " + pg.inner_text("#svtip"))
    pg.click("#svnext"); check(pg.input_value("#svscrub") == "21", "scrubber follows ◀ ▶")
    box = pg.locator("#svframe").bounding_box(); pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    pg.mouse.wheel(0, 120); pg.wait_for_timeout(100); pg.mouse.wheel(0, 120); pg.wait_for_timeout(400)
    check(cnt() == f"22 / {n}", f"one wheel gesture = one slide ({cnt()})")
    pg.mouse.wheel(0, -120); pg.wait_for_timeout(400); check(cnt() == f"21 / {n}", "wheel up goes back")
    y0 = pg.evaluate("scrollY"); pg.click("#svfirst"); pg.mouse.move(box["x"] + 50, box["y"] + 50); pg.mouse.wheel(0, -200); pg.wait_for_timeout(300)
    check(cnt() == f"1 / {n}", "wheel up on the first slide does not wrap")
    pdf = pg.locator(".slidebar [data-save]"); check("Download PDF" in pdf.inner_text(), "PDF button labelled Download PDF")
    # avatar heads on every tab
    for v in ["start", "notes", "slides", "examples", "exercises", "lab", "glossary"]:
        pg.click(f'.tab[data-view="{v}"]'); pg.wait_for_timeout(150)
        img = pg.locator(f'section[data-view="{v}"] .vhead .vava')
        check(img.count() == 1 and pg.evaluate(f"(() => {{ const i = document.querySelector('section[data-view=\"{v}\"] .vhead .vava'); return i.complete && i.naturalWidth > 100; }})()"), f"avatar on the {v} tab")
    check(pg.locator("footer.foot .fava").is_visible(), "head badge in the footer")
    fr = pg.frame_locator("#labframe"); pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(1200)
    check(fr.locator("header.top .labava").is_visible(), "avatar in the Explorer header (inside the part page)")
    pg.click('.tab[data-view="slides"]'); pg.wait_for_timeout(300)
    pg.screenshot(path=str(S / "shots" / "slides_bar.png"), clip={"x": 0, "y": 140, "width": 1280, "height": 760})
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200); pg.screenshot(path=str(S / "shots" / "start_head.png"), clip={"x": 0, "y": 0, "width": 1280, "height": 420})
    # phone: swipe, layout
    ph = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    ph.route("**/fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    q = ph.new_page(); q.goto(f"http://127.0.0.1:{PORT}/05-plane-stress-3/index.html#slides"); q.wait_for_timeout(2500)
    q.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    fb = q.locator("#svframe").bounding_box()
    q.evaluate(f"""(() => {{ const f = document.querySelector('#svframe'); const mk = (x) => new Touch({{identifier: 1, target: f, clientX: x, clientY: {fb['y'] + 60}}});
        f.dispatchEvent(new TouchEvent('touchstart', {{touches: [mk(300)], changedTouches: [mk(300)], bubbles: true}}));
        f.dispatchEvent(new TouchEvent('touchend', {{touches: [], changedTouches: [mk(120)], bubbles: true}})); }})()""")
    q.wait_for_timeout(200); check(q.inner_text("#svcount").startswith("2 /"), "swipe left = next slide on a phone: " + q.inner_text("#svcount"))
    ov = q.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"); check(ov <= 0, f"phone overflow {ov}px")
    q.screenshot(path=str(S / "shots" / "slides_phone.png"), full_page=False)
    q.evaluate("window.scrollTo(0,0)"); q.click('.tab[data-view="start"]'); q.wait_for_timeout(200)
    q.screenshot(path=str(S / "shots" / "start_phone.png"), clip={"x": 0, "y": 0, "width": 390, "height": 700})
    check(not errs, "no page errors " + "; ".join(errs[:2]))
    b.close()
print("\n".join(ok)); print("\n".join(fails) or "ALL PASS"); srv.shutdown(); sys.exit(1 if fails else 0)
