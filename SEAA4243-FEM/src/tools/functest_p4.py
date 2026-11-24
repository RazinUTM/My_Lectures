"""Functional test of the Plane Stress Part 2 page: parameterised exercises checked against independent
Python ([k] by Gauss quadrature in fe_plane_stress.py, scatter-add assembly in numpy, Timoshenko by hand),
MCQ answers present, cantilever-lab milestones through the iframe, progress badges, slide images."""
import http.server, pathlib, re, socketserver, sys, threading
import numpy as np
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SITE / "code"))
from fe_plane_stress import element_stiffness, E_matrix

slug = sys.argv[1] if len(sys.argv) > 1 else "04-plane-stress-2"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def log_message(self, *a): pass
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/{slug}/index.html"
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
def num(t, pat): return float(re.search(pat, t).group(1).rstrip("."))
def given(pg, eid): return pg.inner_text(f'article[data-ex="{eid}"] .given').replace("−", "-")
def kq4(t):
    """Element [k] by 2 x 2 Gauss from the given text (E in 10^6 kN/m2)."""
    a = num(t, r"a = ([\d.]+) m"); b = num(t, r"b = ([\d.]+) m"); th = num(t, r"t = ([\d.]+) m"); E = num(t, r"E = ([\d.]+) × 10⁶") * 1e6; nu = num(t, r"ν = ([\d.]+)")
    return element_stiffness(4, a, b, E_matrix(E, nu, "stress"), th), (a, b, th, E, nu)
def submit(pg, eid, vals, fmtstr="{:.4f}"):
    for f, v in vals.items(): pg.fill(f'article[data-ex="{eid}"] input[data-f="{f}"]', fmtstr.format(v))
    pg.click(f'article[data-ex="{eid}"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
    return pg.inner_text(f'article[data-ex="{eid}"] .resline')
CONN = [[1, 2, 5, 4], [2, 3, 6, 5], [4, 5, 8, 7], [5, 6, 9, 8]]

with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    check(all(pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6", "c1"]), "every MCQ carries data-ans")
    check(pg.get_attribute('.q[data-q="c1"]', "data-ans") == "4", "c1 answer is line 4")
    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    for rnd in range(3):   # three sets of numbers per exercise
        # b1: s1, s2, s3, s7 = k11, k12, k13, k17 of the quadrature matrix
        t = given(pg, "b1"); k, prm = kq4(t)
        r = submit(pg, "b1", {"s1": k[0, 0] / 1e6, "s2": k[0, 1] / 1e6, "s3": k[0, 2] / 1e6, "s7": k[0, 6] / 1e6})
        check("Correct" in r, f"b1 [{rnd}] accepted Gauss-quadrature k11, k12, k13, k17 (a, b, t, E, ν = {prm})")
        # b2: consistent loads by 1D Gauss integration of N along side 2-3 plus the body force over the area
        t = given(pg, "b2"); a = num(t, r"a = ([\d.]+) m"); b = num(t, r"b = ([\d.]+) m"); th = num(t, r"t = ([\d.]+) m"); g = num(t, r"γ = ([\d.]+)")
        p2 = num(t, r"p2 = (-?[\d.]+)"); p3 = num(t, r"p3 = (-?[\d.]+)")
        gp, gw = np.polynomial.legendre.leggauss(3); y = (gp + 1) * b / 2; w = gw * b / 2; py = p2 + (p3 - p2) * y / b
        e4 = np.sum(w * (1 - y / b) * py); e6 = np.sum(w * (y / b) * py)
        X, Y = np.meshgrid((gp + 1) * a / 2, (gp + 1) * b / 2); W = np.outer(gw * b / 2, gw * a / 2)
        q1 = -g * th * np.sum(W * (a - X) * (b - Y) / (a * b))      # N1 integrated, times body force
        r = submit(pg, "b2", {"r2": q1, "r4": e4 + q1, "r6": e6 + q1})
        check("Correct" in r, f"b2 [{rnd}] accepted loads by numerical integration (a={a}, b={b}, p2={p2}, p3={p3})")
        # b3: global entries by scatter-add of the quadrature matrix
        t = given(pg, "b3"); k, prm = kq4(t); K = np.zeros((18, 18))
        for c in CONN:
            d = [x for n in c for x in (2 * n - 2, 2 * n - 1)]; K[np.ix_(d, d)] += k
        r = submit(pg, "b3", {"k33": K[2, 2] / 1e6, "k99": K[8, 8] / 1e6, "k56": K[4, 5] / 1e6, "k39": K[2, 8] / 1e6})
        check("Correct" in r, f"b3 [{rnd}] accepted numpy scatter-add K(3,3), K(9,9), K(5,6), K(3,9) = {K[2,2]/1e6:.3f}, {K[8,8]/1e6:.3f}, {K[4,5]/1e6:.3f}, {K[2,8]/1e6:.3f}")
        # b4: Timoshenko check
        t = given(pg, "b4"); L = num(t, r"L = ([\d.]+) m"); Hh = num(t, r"H = ([\d.]+) m"); th = num(t, r"t = ([\d.]+) m"); E = num(t, r"E = ([\d.]+) × 10⁶") * 1e6
        P = num(t, r"P = ([\d.]+) kN"); vfe = num(t, r"tip deflection of ([\d.]+) mm"); nu = 0.2
        I = th * Hh ** 3 / 12; G = E / (2 * (1 + nu)); db = P * L ** 3 / (3 * E * I) * 1e3; ds = P * L / (5 / 6 * G * th * Hh) * 1e3; err = (vfe - db - ds) / (db + ds) * 100
        r = submit(pg, "b4", {"db": db, "ds": ds, "err": err})
        check("Correct" in r, f"b4 [{rnd}] accepted δb = {db:.3f}, δs = {ds:.3f} mm, error {err:.1f}% (L={L}, H={Hh}, P={P})")
        if rnd == 0:
            # a halved self-weight share (W/2 at the loaded nodes) is caught; s7 with the sign lost is caught
            t = given(pg, "b2"); a = num(t, r"a = ([\d.]+) m"); b = num(t, r"b = ([\d.]+) m"); th = num(t, r"t = ([\d.]+) m"); g = num(t, r"γ = ([\d.]+)")
            pg.fill('article[data-ex="b2"] input[data-f="r2"]', f"{-g*th*a*b/2:.4f}"); pg.click('article[data-ex="b2"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
            check(pg.get_attribute('article[data-ex="b2"] input[data-f="r2"]', "data-state") == "wrong", "b2 self-weight halved (instead of quartered) flagged wrong")
            t = given(pg, "b1"); k, _ = kq4(t)
            if abs(k[0, 6]) > 0.01e6:
                pg.fill('article[data-ex="b1"] input[data-f="s7"]', f"{-k[0,6]/1e6:.4f}"); pg.click('article[data-ex="b1"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(120)
                check(pg.get_attribute('article[data-ex="b1"] input[data-f="s7"]', "data-state") == "wrong", "b1 s7 with the wrong sign flagged wrong")
        for eid in ["b1", "b2", "b3", "b4"]: pg.click(f'article[data-ex="{eid}"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(80)
    # hints and solution render for every exercise
    for eid in ["b1", "b2", "b3", "b4"]:
        pg.click(f'article[data-ex="{eid}"] .qbar button:nth-of-type(2)'); pg.click(f'article[data-ex="{eid}"] .qbar button:nth-of-type(3)'); pg.wait_for_timeout(80)
        sol = pg.inner_text(f'article[data-ex="{eid}"] .sol'); hint = pg.inner_text(f'article[data-ex="{eid}"] .hintbox')
        check(len(sol) > 60 and "NaN" not in sol and "undefined" not in sol and len(hint) > 40, f"{eid} hint and solution render")
    pg.click('.q[data-q="c1"] .errline button[data-k="4"]')
    check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="4"]', "data-state") == "right", "c1 line 4 is the slip")
    check("16 marks" in pg.inner_text("#v-exercises") or "16" in pg.inner_text('#v-exercises h3.part:nth-of-type(2)'), "part B heading counts 16 marks")
    # Explorer milestones through the iframe
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(2000)
    fr = pg.frame_locator("iframe.labframe")
    fr.locator("#b-reset").click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="book22"]', "class") or ""), "milestone book22 after “Text example”")
    for lab in ["4 × 2", "8 × 1", "2 × 4"]: fr.locator(f'#c-mesh label:text-is("{lab}")').click(); pg.wait_for_timeout(250)
    check("done" in (pg.get_attribute('.tk[data-ms="layouts"]', "class") or ""), "milestone layouts after 4 × 2, 8 × 1 and 2 × 4")
    fr.locator("#b-study").click(); pg.wait_for_timeout(3000)
    check("done" in (pg.get_attribute('.tk[data-ms="study"]', "class") or ""), "milestone study after the mesh study")
    fr.locator('label:has-text("Point force at top corner")').click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="point"]', "class") or ""), "milestone point after the corner force")
    check(pg.inner_text('[data-bd="lab"]') == "4/4", "Explorer badge 4/4")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def solve_cantilever') >= 0"), "Explorer tab shows fe_plane_stress.py")
    # examples read, badges
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200); pg.check('#v1 .readck input'); pg.check('#v2 .readck input')
    check(pg.inner_text('[data-bd="examples"]') == "2/3", "examples badge 2/3")
    check(pg.inner_text('[data-bd="exercises"]') == "5/11", "exercises badge 5/11 (b1–b4 + c1)")
    # notes: quick checks answerable, figures and equations present
    pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(300)
    n_eq = pg.evaluate("document.querySelectorAll('#v-notes .eqwrap svg').length"); n_img = pg.evaluate("Array.from(document.querySelectorAll('#v-notes img')).filter(i => i.complete && i.naturalWidth > 0).length")
    n_imgall = pg.evaluate("document.querySelectorAll('#v-notes img').length")
    check(n_eq >= 30 and n_img == n_imgall and n_imgall >= 7, f"notes carry {n_eq} equations and {n_img}/{n_imgall} loaded images")
    keys = {q: pg.get_attribute(f'.qc[data-qc="{q}"]', "data-ans") for q in ["q1", "q2", "q3", "q4", "q5", "q6"]}
    check(sorted(set(keys.values())) == ["a", "b", "c"], f"quick-check answers spread over a, b, c: {keys}")
    for q, k in keys.items():
        pg.click(f'.qc[data-qc="{q}"] .opt[data-k="{k}"]'); pg.wait_for_timeout(60)
        check(not pg.locator(f'.qc[data-qc="{q}"] .fb').is_hidden(), f"quick check {q}: feedback shown after answering {k}")
    qa = {q: pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6"]}
    check(len(set(qa.values())) == 3, f"part A answers spread over a, b, c: {qa}")
    # Start tab carries this part's own content
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    st = pg.inner_text("#v-start")
    check("§3.2.2–§3.4" in st and "A3 the global load vector" in st and "Recall from Plane Stress Part 1" in st, "Start tab shows this part's text sections, activities and recall title")
    check(pg.get_attribute('.partsw a[aria-current="page"]', "href").startswith("../04-"), "part switcher marks Part 4")
    # slides
    pg.click('.tab[data-view="slides"]'); pg.wait_for_timeout(2500)
    nsl = pg.evaluate("document.querySelectorAll('#svcv .sl').length")
    imgs = pg.evaluate("Array.from(document.querySelectorAll('#svcv img')).map(i => i.getAttribute('src'))")
    check(nsl > 20 and all(s.startswith("slides/img/") for s in imgs), f"{nsl} slides injected; images {sorted(set(imgs))}")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    br.close()
srv.shutdown()
print("FAILURES:", len(fails))
