"""Functional test of the Part 2 page: parameterised exercises checked against independent Python
(fe_heat.klocal), MCQ answers present, heat-lab milestones through the iframe, progress parts."""
import http.server, pathlib, re, socketserver, sys, threading
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mj"))
from fe_heat import klocal

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def log_message(self, *a): pass
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/02-heat-transfer-2/index.html"
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
def num(t, pat): return float(re.search(pat, t).group(1))
TN = [0, 0.4821, 0.6214, 0, 0.3857, 0.4821, 0, 0, 0]; CONN = [[1, 2, 5, 4], [2, 3, 6, 5], [4, 5, 8, 7], [5, 6, 9, 8]]; ORG = [(0, 0), (0.5, 0), (0, 0.5), (0.5, 0.5)]
def N4(a, b, x, y): return [(a - x) * (b - y) / (a * b), x * (b - y) / (a * b), x * y / (a * b), y * (a - x) / (a * b)]

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    check(all(pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6", "c1"]), "every MCQ carries data-ans")
    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    # b1: s-values
    t = pg.inner_text('article[data-ex="b1"] .given'); a = num(t, r"a = ([\d.]+) m"); bb = num(t, r"b = ([\d.]+) m"); kx = num(t, r"kx = ([\d.]+)"); ky = num(t, r"ky = ([\d.]+)")
    k = klocal(a, bb, kx, ky); s = {"s1": k[0, 0], "s2": k[0, 1], "s3": k[0, 2], "s4": k[0, 3]}
    for f, v in s.items(): pg.fill(f'article[data-ex="b1"] input[data-f="{f}"]', f"{v:.3f}")
    pg.click('article[data-ex="b1"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
    check("Correct" in pg.inner_text('article[data-ex="b1"] .resline'), f"b1 accepted fe_heat.klocal values (a={a}, b={bb}, kx={kx}, ky={ky})")
    # b2: loads
    t = pg.inner_text('article[data-ex="b2"] .given'); a = num(t, r"a = ([\d.]+) m"); bb = num(t, r"b = ([\d.]+) m"); Qv = num(t, r"qh = ([\d.]+)"); qb = num(t, r"qb = ([\d.]+)")
    edge = re.search(r"on its (right|top|left|bottom)", t).group(1); L = bb if edge in ("right", "left") else a
    pg.fill('article[data-ex="b2"] input[data-f="qi"]', f"{Qv*a*bb/4:.2f}"); pg.fill('article[data-ex="b2"] input[data-f="bj"]', f"{qb*L/2:.2f}")
    pg.click('article[data-ex="b2"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
    check("Correct" in pg.inner_text('article[data-ex="b2"] .resline'), f"b2 accepted loads (edge {edge}, L={L})")
    # b3: assembly entries of the two-element strip, computed by scatter-add in numpy
    t = pg.inner_text('article[data-ex="b3"] .given'); a = num(t, r"a = ([\d.]+) m"); bb = num(t, r"b = ([\d.]+) m"); kk = num(t, r"ky = ([\d.]+)")
    ke = klocal(a, bb, kk, kk); K = np.zeros((6, 6))
    for e in ([0, 1, 4, 3], [1, 2, 5, 4]): K[np.ix_(e, e)] += ke
    for f, (i, j) in {"k22": (1, 1), "k25": (1, 4), "k12": (0, 1), "k15": (0, 4)}.items(): pg.fill(f'article[data-ex="b3"] input[data-f="{f}"]', f"{K[i, j]:.3f}")
    pg.click('article[data-ex="b3"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
    check("Correct" in pg.inner_text('article[data-ex="b3"] .resline'), "b3 accepted numpy scatter-add entries")
    # b4: point in the solved mesh
    t = pg.inner_text('article[data-ex="b4"] .given'); m = re.search(r"\(x, y\) = \(([\d.]+), ([\d.]+)\)", t); x, y = float(m.group(1)), float(m.group(2))
    e = (1 if x >= 0.5 else 0) + (2 if y >= 0.5 else 0); xl, yl = x - ORG[e][0], y - ORG[e][1]; N = N4(0.5, 0.5, xl, yl); c = CONN[e]
    T = sum(N[i] * TN[c[i] - 1] for i in range(4)); dx = [-(0.5 - yl), 0.5 - yl, yl, -yl]; g = sum(dx[i] / 0.25 * TN[c[i] - 1] for i in range(4))
    pg.fill('article[data-ex="b4"] input[data-f="e"]', str(e + 1)); pg.fill('article[data-ex="b4"] input[data-f="t"]', f"{T:.4f}"); pg.fill('article[data-ex="b4"] input[data-f="qx"]', f"{-300*g:.1f}")
    pg.click('article[data-ex="b4"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
    check("Correct" in pg.inner_text('article[data-ex="b4"] .resline'), f"b4 accepted point ({x}, {y}) in element {e+1}: T={T:.4f}, qx={-300*g:.1f}")
    # a wrong element number is caught
    pg.click('article[data-ex="b4"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
    t = pg.inner_text('article[data-ex="b4"] .given'); m = re.search(r"\(x, y\) = \(([\d.]+), ([\d.]+)\)", t); x, y = float(m.group(1)), float(m.group(2))
    e = (1 if x >= 0.5 else 0) + (2 if y >= 0.5 else 0)
    pg.fill('article[data-ex="b4"] input[data-f="e"]', str((e + 1) % 4 + 1)); pg.click('article[data-ex="b4"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
    check(pg.get_attribute('article[data-ex="b4"] input[data-f="e"]', "data-state") == "wrong", "b4 wrong element flagged")
    pg.click('.q[data-q="c1"] .errline button[data-k="2"]'); check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="2"]', "data-state") == "right", "c1 line 2 is the slip")
    # explorer milestones via the heat lab iframe
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(2000)
    fr = pg.frame_locator("iframe.labframe")
    fr.locator("#plot").click(position={"x": 120, "y": 120}); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="book2"]', "class") or ""), "milestone book2 after probing the plate")
    fr.locator("#b-study").click(); pg.wait_for_timeout(2500)
    check("done" in (pg.get_attribute('.tk[data-ms="study"]', "class") or ""), "milestone study after the mesh study")
    fr.locator("#e-right-type").select_option("T") if fr.locator("#e-right-type").count() else None
    # examples read, progress parts present
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200); pg.check('#y1 .readck input'); pg.check('#y2 .readck input')
    check(pg.inner_text('[data-bd="examples"]') == "2/3", "examples badge 2/3")
    check(pg.inner_text('[data-bd="exercises"]') == "5/11", "exercises badge 5/11 (b1–b4 + c1)")
    # Start tab carries this part's own content, not Part 1's
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    st = pg.inner_text("#v-start")
    check("§2.2.2–§2.4" in st and "A6 temperature" in st and "A4 + A5 shape functions" not in st, "Start tab shows Part 2's text sections and activities")
    check("16 marks" in pg.inner_text("#v-exercises") or "16" in pg.inner_text('#v-exercises h3.part:nth-of-type(2)'), "part B heading counts 16 marks")
    check(pg.get_attribute('.partsw a[aria-current="page"]', "href").startswith("../02-"), "part switcher marks Part 2")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def solve_plate') >= 0"), "Explorer tab shows fe_heat_q4.py")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    b.close()
srv.shutdown()
print("FAILURES:", len(fails))
