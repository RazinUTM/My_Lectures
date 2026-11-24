"""Functional test of Plane Stress Part 1 (site part 3): parameterised exercises checked against
independent Python, MCQ answers present, Cantilever Explorer milestones through the iframe, the
Start tab's own content, and the code card."""
import http.server, pathlib, re, socketserver, sys, threading
import numpy as np
from playwright.sync_api import sync_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def log_message(self, *a): pass
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/03-plane-stress-1/index.html"
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
def num(t, pat): return float(re.search(pat, t).group(1).replace("−", "-"))

def Emat(E, nu, strain):
    if not strain:
        c = E / (1 - nu ** 2); return c, nu * c, c * (1 - nu) / 2
    d = E / ((1 + nu) * (1 - 2 * nu)); return d * (1 - nu), d * nu, d * (1 - 2 * nu) / 2

def N4(a, b, x, y): return np.array([(a - x) * (b - y), x * (b - y), x * y, y * (a - x)]) / (a * b)

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    check(all(pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6", "c1"]), "every MCQ carries data-ans")
    check(all(pg.get_attribute(f'.qc[data-qc="{q}"]', "data-ans") for q in ["q1", "q2", "q3", "q4", "q5", "q6", "r1", "r2"]), "every quick check carries data-ans")
    st = pg.inner_text("#v-start")
    check("§3.1–§3.2.1" in st and "A5 u and v at (3.5, 1.3)" in st and "Recall from Heat Transfer" in st, "Start tab shows this part's text sections, activities and recall")
    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    check("14 marks" in pg.inner_text('#v-exercises'), "part B heading counts 14 marks")
    for rep in range(3):   # three sets of numbers each
        # b1: [E]
        t = pg.inner_text('article[data-ex="b1"] .given'); E = num(t, r"E = ([\d.]+) GPa"); nu = num(t, r"ν = ([\d.]+)"); strain = "plane strain" in t
        e = Emat(E, nu, strain)
        for f, v in zip(["e11", "e12", "e33"], e): pg.fill(f'article[data-ex="b1"] input[data-f="{f}"]', f"{v:.4g}")
        pg.click('article[data-ex="b1"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
        check("Correct" in pg.inner_text('article[data-ex="b1"] .resline'), f"b1 accepted [E] (E={E}, ν={nu}, {'strain' if strain else 'stress'}) = {[round(x, 3) for x in e]}")
        # b2: u, v at a point
        t = pg.inner_text('article[data-ex="b2"] .given')
        a = num(t, r"a = ([\d.]+) m"); bb = num(t, r"b = ([\d.]+) m"); m = re.search(r"\(x, y\) = \(([\d.]+), ([\d.]+)\)", t); x, y = float(m.group(1)), float(m.group(2))
        u = [float(s.replace("−", "-")) for s in re.search(r"u = \{([^}]+)\}", t).group(1).split(",")]; v = [float(s.replace("−", "-")) for s in re.search(r"v = \{([^}]+)\}", t).group(1).split(",")]
        Nn = N4(a, bb, x, y)
        pg.fill('article[data-ex="b2"] input[data-f="u"]', f"{Nn @ u:.3f}"); pg.fill('article[data-ex="b2"] input[data-f="v"]', f"{Nn @ v:.3f}")
        pg.click('article[data-ex="b2"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
        check("Correct" in pg.inner_text('article[data-ex="b2"] .resline'), f"b2 accepted u, v = {Nn @ u:.3f}, {Nn @ v:.3f} at ({x}, {y}) in {a} × {bb}")
        # b3: strains and stresses
        t = pg.inner_text('article[data-ex="b3"] .given').replace("−", "-")
        mu = re.search(r"u = \((-?[\d.]+)x ([+-]) ([\d.]+)y\)", t); mv = re.search(r"v = \((-?[\d.]+)x ([+-]) ([\d.]+)y\)", t)
        a2 = float(mu.group(1)); a3 = float(mu.group(3)) * (1 if mu.group(2) == "+" else -1); b2 = float(mv.group(1)); b3 = float(mv.group(3)) * (1 if mv.group(2) == "+" else -1)
        E = num(t, r"E = ([\d.]+) GPa"); nu = num(t, r"ν = ([\d.]+)")
        sxx = E * 1e3 / (1 - nu ** 2) * (a2 + nu * b3) * 1e-4; sxy = E * 1e3 / (2 * (1 + nu)) * (a3 + b2) * 1e-4
        for f, val in [("exx", a2), ("eyy", b3), ("exy", a3 + b2), ("sxx", sxx), ("sxy", sxy)]: pg.fill(f'article[data-ex="b3"] input[data-f="{f}"]', f"{val:.4g}")
        pg.click('article[data-ex="b3"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
        check("Correct" in pg.inner_text('article[data-ex="b3"] .resline'), f"b3 accepted strains {a2}, {b3}, {a3 + b2:.1f} and σxx {sxx:.3g}, σxy {sxy:.3g} MPa")
        for eid in ["b1", "b2", "b3"]: pg.click(f'article[data-ex="{eid}"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(80)
    # a halved shear strain is caught
    t = pg.inner_text('article[data-ex="b3"] .given').replace("−", "-")
    mu = re.search(r"u = \((-?[\d.]+)x ([+-]) ([\d.]+)y\)", t); mv = re.search(r"v = \((-?[\d.]+)x ([+-]) ([\d.]+)y\)", t)
    a3 = float(mu.group(3)) * (1 if mu.group(2) == "+" else -1); b2 = float(mv.group(1))
    if abs(a3 + b2) > 0.05:
        pg.fill('article[data-ex="b3"] input[data-f="exy"]', f"{(a3 + b2) / 2:.4g}"); pg.click('article[data-ex="b3"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
        check(pg.get_attribute('article[data-ex="b3"] input[data-f="exy"]', "data-state") == "wrong", "b3 tensor (halved) shear strain flagged wrong")
    pg.click('.q[data-q="c1"] .errline button[data-k="3"]')
    check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="3"]', "data-state") == "right", "c1 line 3 is the slip")
    # Explorer milestones through the iframe
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(2000)
    fr = pg.frame_locator("iframe.labframe")
    fr.locator('label:has-text("8-node (quadratic)")').click(); fr.locator('label:has-text("8 × 4")').click()
    fr.locator('label:has-text("Plane strain")').click(); fr.locator('label:has-text("Plane stress")').click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="pstrain"]', "class") or ""), "milestone pstrain after both idealisations on 8-node 8 × 4")
    fr.locator('label:has-text("Vertical only")').click(); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="vonly"]', "class") or ""), "milestone vonly after the vertical-only support")
    fr.locator('label:has-text("Fixed: u = v = 0")').click()
    fr.locator("details:has(#i-t) summary").click(); fr.locator("#i-t").fill("0.02"); fr.locator("#i-t").press("Enter"); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="thick"]', "class") or ""), "milestone thick after changing t")
    fr.locator("#i-t").fill("0.01"); fr.locator("#i-t").press("Enter"); fr.locator("#i-nu").fill("0"); fr.locator("#i-nu").press("Enter")
    fr.locator('label:has-text("Plane strain")').click(); fr.locator('label:has-text("Plane stress")').click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="nu0"]', "class") or ""), "milestone nu0 after ν = 0 in both idealisations")
    check(pg.inner_text('[data-bd="lab"]') == "4/4", "Explorer badge 4/4")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def solve_cantilever') >= 0"), "Explorer tab shows fe_plane_stress.py")
    # examples and slides
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200); pg.check('#x1 .readck input')
    check(pg.inner_text('[data-bd="examples"]') == "1/3", "examples badge 1/3")
    pg.click('.tab[data-view="slides"]'); pg.wait_for_timeout(2500)
    check(pg.evaluate("document.querySelectorAll('#svcv .sl').length") == 38, "38 slides injected")
    imgs = pg.evaluate("Array.from(document.querySelectorAll('#svcv img')).map(i => i.getAttribute('src'))")
    check(sum(s.startswith("slides/img/w11_") for s in imgs) == 4 and all(s.startswith("slides/img/") for s in imgs), f"slide images mapped to local files ({len(imgs)}, 4 figures + avatars)")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    b.close()
srv.shutdown()
print("FAILURES:", len(fails))
