"""Functional test of the annotation toolbar (shared/annotate.js) in headless Chromium.

    python3 functest_annotate.py                                  Part 1 of this course
    python3 functest_annotate.py --site <course folder> <page>    another page built on the template

Three screens: a desktop with a mouse (1400 x 900), a tablet with touch and a pen (820 x 1180, 2x), and a
phone (400 x 800). The checks read the canvas pixels, so "red line drawn" means red pixels where the pointer
went. A real iPad with an Apple Pencil is not something this test can stand in for: touch and pen input are
synthesised through the browser's debugging interface.
"""
import http.server, pathlib, socketserver, sys, threading
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
if args[:1] == ["--site"]: SITE = pathlib.Path(args[1]).resolve(); args = args[2:]
PAGE = args[0] if args else "01-heat-transfer-1/index.html"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def log_message(self, *a): pass
class Q(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
srv = Q(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{port}/"
fails, npass = [], 0
def check(cond, msg):
    global npass
    if cond: npass += 1
    else: fails.append(msg); print("FAIL " + msg)

PROBES = """
window.__cv = () => document.querySelector('.rzan-cv');
window.__k = () => { const c = __cv(); return c.width / c.getBoundingClientRect().width; };
window.__px = (x, y) => { const c = __cv(), k = __k(); return Array.from(c.getContext('2d').getImageData(Math.round(x * k), Math.round(y * k), 1, 1).data); };
window.__count = () => { const c = __cv(), a = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < a.length; i += 4) if (a[i] > 0) n++; return n; };
window.__thick = (x, y0, y1) => { const c = __cv(), k = __k(), a = c.getContext('2d').getImageData(Math.round(x * k), Math.round(y0 * k), 1, Math.round((y1 - y0) * k)).data; let n = 0; for (let i = 3; i < a.length; i += 4) if (a[i] > 128) n++; return n / k; };
window.__rect = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, r: r.right, b: r.bottom, shown: !e.hidden && e.getClientRects().length > 0 }; };
window.__view = () => { const v = document.querySelector('.view:not([hidden])'); return v ? v.getAttribute('data-view') : ''; };
window.__slide = () => { const s = document.querySelector('.sl.on, .slide.on'); return s ? Array.prototype.indexOf.call(s.parentNode.children, s) : -1; };
"""
def near(p, rgb, tol=40): return p[3] > 200 and all(abs(p[i] - rgb[i]) <= tol for i in range(3))
RED, BLUE, GREEN, BLACK, WHITE, YELLOW = (224, 32, 44), (20, 99, 214), (18, 150, 74), (17, 17, 17), (255, 255, 255), (246, 196, 0)
SET = "(v => { const r = document.querySelectorAll('.rzan-size input')[%d]; r.value = v; r.dispatchEvent(new Event('input', { bubbles: true })); })"   # 0: thickness, 1: blank page
PAPER = "getComputedStyle(__cv()).backgroundColor"

def open_page(b, width, height, touch=False, scale=1, hash_="#notes"):
    ctx = b.new_context(viewport={"width": width, "height": height}, has_touch=touch, device_scale_factor=scale)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route(lambda u: not u.startswith(BASE), lambda r: r.fulfill(status=200, content_type="text/css", body="") if "fonts.googleapis" in r.request.url else r.abort())
    pg.add_init_script(PROBES)
    pg.goto(BASE + PAGE + hash_); pg.wait_for_timeout(800)
    return ctx, pg, errs
def stroke(pg, x0, y0, x1, y1, steps=14):
    pg.mouse.move(x0, y0); pg.mouse.down(); pg.mouse.move(x1, y1, steps=steps); pg.mouse.up(); pg.wait_for_timeout(60)
def toggle(pg): pg.click(".rzan-toggle"); pg.wait_for_timeout(120)
def first(pg, *sels):
    for s in sels:
        if pg.locator(s).count(): return s
    return None

with sync_playwright() as p:
    b = p.chromium.launch()

    # ================= desktop, mouse =================
    ctx, pg, errs = open_page(b, 1400, 900); T = "desktop"
    part = pg.locator("#t-slides").count() > 0                       # a part page (tabs, slides); otherwise a plain page such as the course home
    bar = pg.evaluate("__rect('.rzan-bar')")
    check(bar and bar["shown"] and 1400 - bar["r"] <= 20 and 900 - bar["b"] <= 20 and bar["w"] <= 50 and bar["h"] <= 50, f"{T}: only the pencil button shows, in the bottom right corner ({bar})")
    check(pg.evaluate("!__rect('.rzan-cv').shown && !__rect('.rzan-tools').shown") and pg.evaluate("window.RZAnnotate.isOn()") is False, f"{T}: off at load: canvas and tools hidden")
    check(pg.evaluate("document.elementFromPoint(700, 450).className") != "rzan-cv", f"{T}: off: the page is on top")
    pg.mouse.move(700, 450); pg.mouse.wheel(0, 300); pg.wait_for_timeout(250); y0 = pg.evaluate("scrollY")
    check(y0 > 0, f"{T}: off: the wheel scrolls the page ({y0})")
    toggle(pg)
    cv = pg.evaluate("({ r: __rect('.rzan-cv'), w: __cv().width, h: __cv().height, top: document.elementFromPoint(700, 450).className, pressed: document.querySelector('.rzan-toggle').getAttribute('aria-pressed') })")
    check(cv["r"]["shown"] and cv["top"] == "rzan-cv" and cv["pressed"] == "true" and abs(cv["w"] - cv["r"]["w"]) <= 1 and abs(cv["h"] - cv["r"]["h"]) <= 1 and cv["r"]["h"] >= 880, f"{T}: on: the canvas covers the page ({cv})")
    bar_on = pg.evaluate("__rect('.rzan-bar')")
    check(bar_on["w"] > 300 and abs(bar_on["r"] - bar["r"]) <= 1 and abs(bar_on["b"] - bar["b"]) <= 1 and bar_on["x"] >= 0, f"{T}: on: the tools open to the left of the pencil ({bar_on})")
    # the page takes no input while it is on
    pg.mouse.move(700, 450); pg.mouse.wheel(0, 400); pg.wait_for_timeout(200)
    for key in ("PageDown", "End", "ArrowDown"): pg.keyboard.press(key)        # the focus is still on the pencil button
    pg.evaluate("document.activeElement.blur()")
    for key in ("PageDown", "Space", "End", "ArrowDown", "/"): pg.keyboard.press(key)
    pg.wait_for_timeout(250)
    check(pg.evaluate("scrollY") == y0 and pg.evaluate("window.RZAnnotate.isOn()") and pg.evaluate("document.activeElement.tagName") != "INPUT",
          f"{T}: on: wheel and keys do not scroll or reach the page ({pg.evaluate('scrollY')} vs {y0})")
    if part:
        t = pg.evaluate("__rect('#t-slides')"); v0 = pg.evaluate("__view()")
        pg.mouse.click(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2); pg.wait_for_timeout(150)
        check(pg.evaluate("__view()") == v0 == "notes", f"{T}: on: a click where a tab is does not change the view")
        pg.click('.rzan-b[data-act="clear"]')
    # drawing: colour, thickness, eraser, undo, clear
    pg.click('.rzan-c[data-c="red"]'); pg.evaluate("(() => { const r = document.querySelector('.rzan-size input'); r.value = 6; r.dispatchEvent(new Event('input', { bubbles: true })); })()")
    stroke(pg, 300, 400, 600, 400)
    check(near(pg.evaluate("__px(450, 400)"), RED) and pg.evaluate("__px(450, 330)")[3] == 0, f"{T}: a red line where the mouse went ({pg.evaluate('__px(450, 400)')})")
    th = pg.evaluate("__thick(450, 380, 420)"); check(4.5 <= th <= 7.5, f"{T}: thickness 6 draws about 6 px ({th})")
    for slot, rgb, y in (("blue", BLUE, 440), ("ink", BLACK, 480), ("yellow", YELLOW, 520), ("green", GREEN, 548)):
        pg.click(f'.rzan-c[data-c="{slot}"]'); stroke(pg, 300, y, 600, y)
        check(near(pg.evaluate(f"__px(450, {y})"), rgb), f"{T}: {slot} pen draws its colour ({pg.evaluate(f'__px(450, {y})')})")
        check(pg.evaluate(f"""document.querySelector('.rzan-c[data-c="{slot}"]').getAttribute('aria-pressed')""") == "true", f"{T}: {slot} is shown as the pen in use")
    rg = pg.evaluate("__rect('.rzan-size input')"); bar1 = pg.evaluate("__rect('.rzan-bar')")
    pg.mouse.click(rg["x"] + rg["w"] * 0.88, rg["y"] + rg["h"] / 2); pg.wait_for_timeout(100)
    val = int(pg.evaluate("document.querySelector('.rzan-size input').value")); bar2 = pg.evaluate("__rect('.rzan-bar')")
    check(val >= 18 and abs(bar1["x"] - bar2["x"]) < 1 and abs(bar1["y"] - bar2["y"]) < 1, f"{T}: the slider sets the thickness by mouse ({val}) and does not drag the toolbar")
    pg.click('.rzan-c[data-c="red"]'); stroke(pg, 300, 580, 600, 580)
    th = pg.evaluate("__thick(450, 550, 610)"); check(val - 2.5 <= th <= val + 2.5, f"{T}: thickness {val} draws about {val} px ({th})")
    # the eraser works by object: the line it touches goes as a whole, its neighbours stay
    n0 = pg.evaluate("__count()")
    pg.click('.rzan-b[data-act="eraser"]'); stroke(pg, 450, 386, 450, 412)
    check(pg.evaluate("__px(450, 400)")[3] == 0 and pg.evaluate("__px(310, 400)")[3] == 0 and pg.evaluate("__px(590, 400)")[3] == 0 and near(pg.evaluate("__px(340, 440)"), BLUE),
          f"{T}: the eraser removes the whole line it crosses, and only that line")
    pg.keyboard.press("Control+z"); pg.wait_for_timeout(80)
    check(near(pg.evaluate("__px(450, 400)"), RED) and near(pg.evaluate("__px(310, 400)"), RED) and pg.evaluate("__count()") == n0, f"{T}: Ctrl+Z brings the erased line back")
    pg.mouse.click(520, 441); pg.wait_for_timeout(60)
    check(pg.evaluate("__px(340, 440)")[3] == 0 and near(pg.evaluate("__px(340, 400)"), RED) and near(pg.evaluate("__px(340, 480)"), BLACK), f"{T}: one click with the eraser on a line removes that line")
    stroke(pg, 700, 300, 760, 340); check(pg.evaluate("__count()") < n0 and near(pg.evaluate("__px(340, 400)"), RED), f"{T}: the eraser on empty space removes nothing more")
    stroke(pg, 320, 470, 330, 556, steps=3)
    check(all(pg.evaluate(f"__px(450, {y})")[3] == 0 for y in (480, 520, 548)) and near(pg.evaluate("__px(450, 400)"), RED), f"{T}: a quick sweep of the eraser removes every line it crosses")
    for _ in range(2): pg.keyboard.press("Control+z")
    pg.wait_for_timeout(80); check(pg.evaluate("__count()") == n0, f"{T}: Ctrl+Z twice brings back the sweep and the single line")
    pg.click('.rzan-b[data-act="clear"]'); pg.wait_for_timeout(60); empty = pg.evaluate("__count()"); pg.keyboard.press("Control+z"); pg.wait_for_timeout(80)
    check(empty == 0 and pg.evaluate("__count()") == n0, f"{T}: Ctrl+Z brings back what Clear all removed")
    # the blank page behind the ink
    check(pg.evaluate(PAPER) == "rgba(0, 0, 0, 0)" and pg.evaluate("document.querySelectorAll('.rzan-size input')[1].value") == "0", f"{T}: the blank page starts at 0%: the canvas is see-through")
    pg.evaluate(SET % 1 + "(100)"); full = pg.evaluate(PAPER); pg.evaluate(SET % 1 + "(50)"); half = pg.evaluate(PAPER)
    check(full == "rgb(255, 255, 255)" and half == "rgba(255, 255, 255, 0.5)" and near(pg.evaluate("__px(450, 400)"), RED), f"{T}: the blank page is white at 100% and half see-through at 50%, under the ink ({full} / {half})")
    rv = pg.evaluate("__rect('.rzan-pg + input')"); barA = pg.evaluate("__rect('.rzan-bar')")
    pg.mouse.click(rv["x"] + rv["w"] * 0.9, rv["y"] + rv["h"] / 2); pg.wait_for_timeout(100); barB = pg.evaluate("__rect('.rzan-bar')")
    cov = int(pg.evaluate("document.querySelectorAll('.rzan-size input')[1].value"))
    check(cov >= 75 and abs(barA["x"] - barB["x"]) < 1 and "%d%%" % cov in pg.evaluate("document.querySelectorAll('.rzan-size input')[1].title"), f"{T}: the blank-page slider works by mouse ({cov}%) and does not drag the toolbar")
    pg.evaluate(SET % 1 + "(0)"); check(pg.evaluate(PAPER) == "rgba(0, 0, 0, 0)", f"{T}: back at 0% the page shows through again")
    pg.click('.rzan-c[data-c="red"]')
    check(pg.evaluate("document.querySelector('.rzan-b[data-act=\"eraser\"]').getAttribute('aria-pressed')") == "false", f"{T}: choosing a colour goes back to the pen")
    # off and on again; the ink stays on what it was written on
    toggle(pg)
    check(pg.evaluate("!__rect('.rzan-cv').shown && !__rect('.rzan-tools').shown && document.elementFromPoint(700, 450).className !== 'rzan-cv'"), f"{T}: off again: canvas hidden, page on top")
    pg.mouse.move(700, 450); pg.mouse.wheel(0, 150); pg.wait_for_timeout(300); y1 = pg.evaluate("scrollY")
    check(y1 == y0 + 150, f"{T}: off again: the page scrolls ({y0} -> {y1})")
    toggle(pg)
    check(near(pg.evaluate("__px(340, 250)"), RED) and near(pg.evaluate("__px(340, 290)"), BLUE) and pg.evaluate("__px(340, 270)")[3] == 0, f"{T}: the ink is kept, and moved with the page it was written on ({pg.evaluate('__px(340, 250)')})")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    check(pg.evaluate("window.RZAnnotate.isOn()") is False, f"{T}: Esc turns annotation off")
    if part:
        # each view, and each slide, keeps its own ink
        pg.click("#t-slides"); pg.wait_for_timeout(400)
        pg.evaluate("document.querySelector('.sl.on, .slide.on').scrollIntoView({ block: 'center' })"); pg.wait_for_timeout(200); toggle(pg)   # the whole slide on screen: the test's mouse must stay inside the window
        check(pg.evaluate("__count()") == 0, f"{T}: the Slides view starts with no ink of the Notes")
        fr = pg.evaluate("__rect('.sl.on, .slide.on')"); cx, cy = fr["x"] + fr["w"] / 2, fr["y"] + fr["h"] / 2
        pg.click('.rzan-c[data-c="blue"]'); s0 = pg.evaluate("__slide()"); stroke(pg, cx - 80, cy, cx + 80, cy)
        pg.mouse.click(cx + 150, cy + 60); pg.mouse.wheel(0, 300); pg.wait_for_timeout(200)
        check(pg.evaluate("__slide()") == s0 and near(pg.evaluate(f"__px({cx}, {cy})"), BLUE), f"{T}: writing, clicking and the wheel on a slide do not turn it")
        toggle(pg); nxt = first(pg, "#svnext", "#snext"); pg.click(nxt); pg.wait_for_timeout(250); toggle(pg)
        check(pg.evaluate("__slide()") == s0 + 1 and pg.evaluate("__count()") == 0, f"{T}: the next slide has no ink of the one before")
        toggle(pg); pg.click(first(pg, "#svprev", "#sprev")); pg.wait_for_timeout(250); toggle(pg)
        fr = pg.evaluate("__rect('.sl.on, .slide.on')"); cx, cy = fr["x"] + fr["w"] / 2, fr["y"] + fr["h"] / 2
        check(near(pg.evaluate(f"__px({cx}, {cy})"), BLUE), f"{T}: back on the slide, its ink is there again")
        pg.click('.rzan-b[data-act="clear"]'); pg.wait_for_timeout(60)
        check(pg.evaluate("__count()") == 0, f"{T}: Clear all clears the screen")
        toggle(pg); pg.click("#t-notes"); pg.wait_for_timeout(300); pg.evaluate(f"window.scrollTo(0, {y1})"); pg.wait_for_timeout(200); toggle(pg)
        check(near(pg.evaluate("__px(340, 250)"), RED), f"{T}: Clear all on the slide left the ink of the Notes alone")
        # the slide viewer in full screen takes the toolbar with it
        full = first(pg, "#svfull", "#sfull")
        toggle(pg); pg.click("#t-slides"); pg.wait_for_timeout(300); pg.click(full); pg.wait_for_timeout(500)
        fs = pg.evaluate("({ el: document.fullscreenElement ? document.fullscreenElement.id : null, inside: !!document.fullscreenElement && document.fullscreenElement.contains(document.querySelector('.rzan')), bar: __rect('.rzan-bar'), vw: innerWidth, vh: innerHeight })")
        if fs["el"]:
            check(fs["inside"] and fs["bar"]["shown"] and fs["bar"]["r"] <= fs["vw"] and fs["bar"]["b"] <= fs["vh"] and fs["bar"]["x"] >= 0, f"{T}: full screen: the toolbar is inside #{fs['el']} and on screen ({fs})")
            toggle(pg); check(pg.evaluate("__count()") == 0, f"{T}: full screen starts with no ink")
            mx, my = fs["vw"] / 2, fs["vh"] / 2; s0 = pg.evaluate("__slide()"); stroke(pg, mx - 100, my, mx + 100, my); pg.mouse.click(mx + 200, my + 100); pg.wait_for_timeout(150)
            check(near(pg.evaluate(f"__px({mx}, {my})"), BLUE) and pg.evaluate("__slide()") == s0, f"{T}: full screen: writing works and does not turn the slide")
            toggle(pg); pg.evaluate("document.exitFullscreen()"); pg.wait_for_timeout(500)
            check(pg.evaluate("document.querySelector('.rzan').parentNode === document.body && __rect('.rzan-bar').shown"), f"{T}: leaving full screen brings the toolbar back to the page")
            toggle(pg); check(pg.evaluate("__count()") == 0, f"{T}: the full-screen ink is not shown on the windowed slide"); toggle(pg)
        else:
            print(f"note {T}: this browser gave no full screen; that part was not tested")
        pg.click("#t-notes"); pg.wait_for_timeout(300)
    # dragging the toolbar; a drag is not a click; the place and the pen are remembered
    b0 = pg.evaluate("__rect('.rzan-toggle')")
    pg.mouse.move(b0["x"] + 18, b0["y"] + 18); pg.mouse.down(); pg.mouse.move(b0["x"] - 282, b0["y"] - 182, steps=10); pg.mouse.up(); pg.wait_for_timeout(450)
    b1 = pg.evaluate("__rect('.rzan-toggle')")
    check(abs((b0["x"] - b1["x"]) - 300) <= 4 and abs((b0["y"] - b1["y"]) - 200) <= 4 and pg.evaluate("window.RZAnnotate.isOn()") is False, f"{T}: the pencil button can be dragged, and a drag does not switch it on ({b0['x']:.0f},{b0['y']:.0f} -> {b1['x']:.0f},{b1['y']:.0f})")
    toggle(pg); g = pg.evaluate("__rect('.rzan-grip')")
    pg.mouse.move(g["x"] + 8, g["y"] + 18); pg.mouse.down(); pg.mouse.move(g["x"] + 8 + 2000, g["y"] + 18 + 2000, steps=8); pg.mouse.up(); pg.wait_for_timeout(450)
    bb = pg.evaluate("__rect('.rzan-bar')")
    check(bb["x"] >= 0 and bb["y"] >= 0 and bb["r"] <= 1400 and bb["b"] <= 900 and bb["r"] >= 1380, f"{T}: dragged past the corner, the toolbar stops at the edge ({bb})")
    pg.mouse.move(g["x"] + 8, g["y"] + 18); toggle(pg)
    b0 = pg.evaluate("__rect('.rzan-toggle')"); pg.mouse.move(b0["x"] + 18, b0["y"] + 18); pg.mouse.down(); pg.mouse.move(b0["x"] - 400, b0["y"] - 300, steps=8); pg.mouse.up(); pg.wait_for_timeout(450)
    b1 = pg.evaluate("__rect('.rzan-toggle')"); pg.click('.rzan-toggle'); pg.click('.rzan-c[data-c="yellow"]'); pg.evaluate(SET % 1 + "(100)"); toggle(pg)
    pg.reload(); pg.wait_for_timeout(700)
    b2 = pg.evaluate("__rect('.rzan-toggle')"); toggle(pg)
    check(abs(b2["x"] - b1["x"]) <= 2 and abs(b2["y"] - b1["y"]) <= 2 and pg.evaluate("document.querySelector('.rzan-c[data-c=\"yellow\"]').getAttribute('aria-pressed')") == "true" and pg.evaluate("__count()") == 0 and pg.evaluate(PAPER) == "rgba(0, 0, 0, 0)",
          f"{T}: after a reload the toolbar's place and the pen are kept, and no ink is stored ({b1['x']:.0f},{b1['y']:.0f} -> {b2['x']:.0f},{b2['y']:.0f})")
    toggle(pg); pg.set_viewport_size({"width": 700, "height": 500}); pg.wait_for_timeout(300); bb = pg.evaluate("__rect('.rzan-bar')")
    check(bb["x"] >= 0 and bb["y"] >= 0 and bb["r"] <= 700 and bb["b"] <= 500, f"{T}: a smaller window keeps the toolbar on screen ({bb})")
    pg.set_viewport_size({"width": 1400, "height": 900}); pg.evaluate("localStorage.removeItem('rz-annotate')"); pg.reload(); pg.wait_for_timeout(700)
    # theme, language, print
    panel = pg.evaluate("(() => { const d = document.createElement('div'); d.style.background = 'var(--panel)'; document.body.appendChild(d); const c = getComputedStyle(d).backgroundColor; d.remove(); return c; })")
    light = pg.evaluate("({ bg: getComputedStyle(document.querySelector('.rzan-bar')).backgroundColor, ink: document.querySelector('.rzan-c[data-c=\"ink\"]').title, sw: getComputedStyle(document.querySelector('.rzan-c[data-c=\"ink\"] i')).backgroundColor, dark: document.documentElement.getAttribute('data-theme') })")
    pg.click("#btn-theme"); pg.wait_for_timeout(150)
    dark = pg.evaluate("({ bg: getComputedStyle(document.querySelector('.rzan-bar')).backgroundColor, ink: document.querySelector('.rzan-c[data-c=\"ink\"]').title, sw: getComputedStyle(document.querySelector('.rzan-c[data-c=\"ink\"] i')).backgroundColor, theme: document.documentElement.getAttribute('data-theme') })")
    panel_d = pg.evaluate("(() => { const d = document.createElement('div'); d.style.background = 'var(--panel)'; document.body.appendChild(d); const c = getComputedStyle(d).backgroundColor; d.remove(); return c; })")
    check(light["bg"] == panel and dark["bg"] == panel_d and panel != panel_d, f"{T}: the toolbar takes the page's panel colour in both themes ({light['bg']} / {dark['bg']})")
    check({light["ink"], dark["ink"]} == {"Black pen", "White pen"} and {light["sw"], dark["sw"]} == {"rgb(17, 17, 17)", "rgb(255, 255, 255)"}, f"{T}: the black pen is white on the dark theme ({light['ink']} / {dark['ink']})")
    pg.click(".rzan-toggle"); pg.evaluate(SET % 1 + "(100)"); pd = pg.evaluate(PAPER)
    check(pd == ("rgb(22, 24, 28)" if dark["theme"] == "dark" else "rgb(255, 255, 255)"), f"{T}: the blank page is dark on the dark theme and white on the light one ({pd}, theme {dark['theme']})")
    pg.evaluate(SET % 1 + "(0)"); pg.click(".rzan-toggle")
    toggle(pg); pg.click('.rzan-c[data-c="ink"]'); stroke(pg, 300, 300, 500, 300)
    is_dark = dark["theme"] == "dark"
    check(near(pg.evaluate("__px(400, 300)"), WHITE if is_dark else BLACK), f"{T}: that pen writes {'white' if is_dark else 'black'} now ({pg.evaluate('__px(400, 300)')})"); toggle(pg)
    pg.click("#btn-theme"); pg.click("#btn-lang"); pg.wait_for_timeout(150)
    ms = pg.evaluate("[document.querySelector('.rzan-toggle').title, document.querySelector('.rzan-b[data-act=\"eraser\"]').title, document.querySelector('.rzan-b[data-act=\"clear\"]').title, document.querySelector('.rzan-bar').getAttribute('aria-label')]")
    pg.click("#btn-lang"); pg.wait_for_timeout(150); en = pg.evaluate("[document.querySelector('.rzan-toggle').title, document.querySelector('.rzan-b[data-act=\"eraser\"]').title]")
    both = {tuple(ms[:2]), tuple(en)}
    check(both == {("Tulis pada skrin", "Pemadam: sentuh satu garisan untuk memadam seluruh garisan itu"), ("Write on the screen", "Eraser: touch a line to remove the whole line")}, f"{T}: labels in Malay and English ({ms} / {en})")
    pg.emulate_media(media="print"); check(pg.evaluate("getComputedStyle(document.querySelector('.rzan')).display") == "none", f"{T}: nothing of it in print"); pg.emulate_media(media="screen")
    # the exercise timer sits in the same corner: the pencil moves above it
    if pg.locator(".tpill").count():                              # shown here by hand; the engine hides it again at its next tick, so read at once
        a, c = pg.evaluate("(async () => { const t = document.querySelector('.tpill'); t.hidden = false; if (!t.textContent) t.textContent = '00:42'; await new Promise(r => setTimeout(r, 60)); const o = [__rect('.rzan-bar'), __rect('.tpill')]; t.hidden = true; return o; })()")
        if c["shown"]: check(a["b"] <= c["y"] or a["x"] >= c["r"] or a["r"] <= c["x"], f"{T}: the pencil button stays clear of the exercise timer ({a} / {c})")
        else: print(f"note {T}: the exercise timer was not on screen (another view, or hidden again by the page); that check was not made")
    check(not errs, f"{T}: no page errors {errs[:2]}"); print(f"{T}: done"); ctx.close()

    # ================= tablet: touch and pen =================
    ctx, pg, errs = open_page(b, 820, 1180, touch=True, scale=2); T = "tablet"
    cdp = ctx.new_cdp_session(pg)
    def touch(kind, pts): cdp.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": [{"x": x, "y": y, "id": i} for i, (x, y) in enumerate(pts)]})
    def touch_line(x0, y0, x1, y1, n=12):
        touch("touchStart", [(x0, y0)])
        for i in range(1, n + 1): touch("touchMove", [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)])
        touch("touchEnd", []); pg.wait_for_timeout(80)
    def pen(kind, x, y, down=True): cdp.send("Input.dispatchMouseEvent", {"type": kind, "x": x, "y": y, "button": "left" if kind != "mouseMoved" or down else "none", "buttons": 1 if down else 0, "clickCount": 1, "pointerType": "pen"})
    def pen_line(x0, y0, x1, y1, n=12, lift=True):
        pen("mousePressed", x0, y0)
        for i in range(1, n + 1): pen("mouseMoved", x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
        if lift: pen("mouseReleased", x1, y1, down=False); pg.wait_for_timeout(80)
    a, fab = pg.evaluate("__rect('.rzan-bar')"), pg.evaluate("__rect('.rjfab')")
    if fab and fab["shown"]:
        check(a["b"] <= fab["y"] and a["r"] <= 820 and a["b"] <= 1180, f"{T}: the pencil button sits above the Dr RJ button, not on it ({a} / {fab})")
    else:
        check(820 - a["r"] <= 20 and 1180 - a["b"] <= 20, f"{T}: the pencil button is in the bottom right corner ({a})")
    tb = pg.evaluate("__rect('.rzan-toggle')"); pg.touchscreen.tap(tb["x"] + 18, tb["y"] + 18); pg.wait_for_timeout(200)
    cv = pg.evaluate("({ on: window.RZAnnotate.isOn(), w: __cv().width, cw: __rect('.rzan-cv').w })")
    check(cv["on"] and abs(cv["w"] - 2 * cv["cw"]) <= 2, f"{T}: a tap switches it on; the canvas is drawn at 2x ({cv})")
    y0 = pg.evaluate("scrollY"); red = pg.evaluate("__rect('.rzan-c[data-c=\"red\"]')"); pg.touchscreen.tap(red["x"] + 15, red["y"] + 18)
    touch_line(200, 500, 500, 700)
    check(near(pg.evaluate("__px(350, 600)"), RED) and pg.evaluate("scrollY") == y0, f"{T}: a finger draws, and the page does not scroll under it ({pg.evaluate('__px(350, 600)')})")
    bl = pg.evaluate("__rect('.rzan-c[data-c=\"blue\"]')"); pg.touchscreen.tap(bl["x"] + 15, bl["y"] + 18); pg.wait_for_timeout(800)
    pen_line(200, 300, 500, 300)
    check(near(pg.evaluate("__px(350, 300)"), BLUE), f"{T}: a pen draws ({pg.evaluate('__px(350, 300)')})")
    # the palm: a touch while the pen is writing, or just after it, leaves no mark
    pen_line(200, 380, 400, 380, lift=False); touch_line(600, 800, 700, 800); pen("mouseReleased", 400, 380, down=False); pg.wait_for_timeout(60)
    check(near(pg.evaluate("__px(300, 380)"), BLUE) and pg.evaluate("__px(650, 800)")[3] == 0, f"{T}: a touch while the pen is down is ignored")
    touch_line(600, 850, 700, 850)
    check(pg.evaluate("__px(650, 850)")[3] == 0, f"{T}: a touch just after the pen is ignored")
    pg.wait_for_timeout(800); touch_line(600, 900, 700, 900)
    check(near(pg.evaluate("__px(650, 900)"), BLUE), f"{T}: a moment later the finger draws again")
    pg.wait_for_timeout(800); touch("touchStart", [(600, 950)]); touch("touchMove", [(640, 950)]); pen_line(200, 450, 400, 450); touch("touchEnd", []); pg.wait_for_timeout(80)
    check(pg.evaluate("__px(620, 950)")[3] == 0 and near(pg.evaluate("__px(300, 450)"), BLUE), f"{T}: a palm that lands first gives way to the pen, and its mark is removed")
    # a tap where a page control is does nothing; the toolbar can be dragged by touch
    if pg.locator("#t-slides").count():
        t = pg.evaluate("__rect('#t-slides')"); pg.wait_for_timeout(800); pg.touchscreen.tap(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2); pg.wait_for_timeout(150)
        check(pg.evaluate("__view()") == "notes", f"{T}: a tap where a tab is does not change the view")
    g = pg.evaluate("__rect('.rzan-grip')"); bb0 = pg.evaluate("__rect('.rzan-bar')")
    touch_line(g["x"] + 8, g["y"] + 18, g["x"] + 8 - 60, g["y"] + 18 - 300, n=8); pg.wait_for_timeout(400); bb1 = pg.evaluate("__rect('.rzan-bar')")
    check(abs((bb0["y"] - bb1["y"]) - 300) <= 6 and bb1["x"] >= 0 and bb1["r"] <= 820, f"{T}: the toolbar is dragged by touch ({bb0['y']:.0f} -> {bb1['y']:.0f})")
    er = pg.evaluate("__rect('.rzan-b[data-act=\"eraser\"]')"); pg.touchscreen.tap(er["x"] + 18, er["y"] + 18); pg.wait_for_timeout(800)
    was = near(pg.evaluate("__px(350, 600)"), RED); touch_line(330, 640, 372, 558, n=6)
    check(was and pg.evaluate("__px(350, 600)")[3] == 0 and pg.evaluate("__px(230, 520)")[3] == 0 and near(pg.evaluate("__px(350, 300)"), BLUE), f"{T}: a finger with the eraser removes the whole line it crosses, and only that one")
    cl = pg.evaluate("__rect('.rzan-b[data-act=\"clear\"]')"); pg.touchscreen.tap(cl["x"] + 18, cl["y"] + 18); pg.wait_for_timeout(100)
    check(pg.evaluate("__count()") == 0, f"{T}: Clear all by a tap")
    tb = pg.evaluate("__rect('.rzan-toggle')"); pg.touchscreen.tap(tb["x"] + 18, tb["y"] + 18); pg.wait_for_timeout(200)
    touch("touchStart", [(400, 700)])
    for i in range(1, 9): touch("touchMove", [(400, 700 - 40 * i)])
    touch("touchEnd", []); pg.wait_for_timeout(500)
    check(pg.evaluate("window.RZAnnotate.isOn()") is False and pg.evaluate("scrollY") > y0, f"{T}: off again, a swipe scrolls the page ({y0} -> {pg.evaluate('scrollY')})")
    check(not errs, f"{T}: no page errors {errs[:2]}"); print(f"{T}: done"); ctx.close()

    # ================= phone =================
    ctx, pg, errs = open_page(b, 400, 800, touch=True, scale=2); T = "phone"
    a, fab = pg.evaluate("__rect('.rzan-bar')"), pg.evaluate("__rect('.rjfab')")
    if fab and fab["shown"]: check(a["b"] <= fab["y"] and a["r"] <= 400, f"{T}: the pencil button sits above the Dr RJ button ({a} / {fab})")
    check(pg.evaluate("document.documentElement.scrollWidth - innerWidth") <= 0, f"{T}: no sideways scroll")
    tb = pg.evaluate("__rect('.rzan-toggle')"); pg.touchscreen.tap(tb["x"] + 18, tb["y"] + 18); pg.wait_for_timeout(200)
    a2, tb2 = pg.evaluate("__rect('.rzan-bar')"), pg.evaluate("__rect('.rzan-toggle')")
    inside = pg.evaluate("[...document.querySelectorAll('.rzan-bar button, .rzan-bar input')].every(e => { const r = e.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth && r.top >= 0 && r.bottom <= innerHeight; })")
    check(a2["x"] >= 0 and a2["r"] <= 400 and inside and abs(tb2["x"] - tb["x"]) <= 1 and abs(tb2["y"] - tb["y"]) <= 1, f"{T}: the open toolbar fits the screen and the pencil button stays where it was ({a2})")
    check(pg.evaluate("document.documentElement.scrollWidth - innerWidth") <= 0 and not errs, f"{T}: still no sideways scroll, no page errors {errs[:2]}"); print(f"{T}: done"); ctx.close()
    b.close()
print(f"\n{npass} checks passed, {len(fails)} failed"); sys.exit(1 if fails else 0)
