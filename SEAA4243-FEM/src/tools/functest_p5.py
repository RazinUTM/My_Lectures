"""Functional test of the Plane Stress Part 3 page: parameterised exercises checked against independent Python
(fe_plane_stress.B_matrix, E_matrix, principal, von_mises; Richardson by hand), MCQ answers present, stress-lab
milestones and readouts through the iframe, progress badges, Start tab content, code card."""
import http.server, math, pathlib, re, socketserver, sys, threading
import numpy as np
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SITE / "code"))
from fe_plane_stress import B_matrix, E_matrix, principal, von_mises

slug = sys.argv[1] if len(sys.argv) > 1 else "05-plane-stress-3"
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
def num(t, pat): return float(re.search(pat, t).group(1).replace("−", "-"))
def given(pg, ex): return pg.inner_text(f'article[data-ex="{ex}"] .given').replace("−", "-")
def submit(pg, ex): pg.click(f'article[data-ex="{ex}"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(150)
def ok(pg, ex): return "Correct" in pg.inner_text(f'article[data-ex="{ex}"] .resline')

def b1_answer(t):
    a = num(t, r"a = ([\d.]+) m"); b = num(t, r"b = ([\d.]+) m"); nu = num(t, r"ν = ([\d.]+)")
    d = [float(v) * 1e-5 for v in re.search(r"v4\} = \{([^}]*)\}", t).group(1).split(",")]
    m = re.search(r"\(x, y\) = \(([\d.]+), ([\d.]+)\)", t); x, y = float(m.group(1)), float(m.group(2))
    B = B_matrix(4, a, b, 2 * x / a - 1, 2 * y / b - 1)              # natural coordinates of the local point
    return E_matrix(200e6, nu) @ B @ np.array(d), (a, b, nu, x, y)

def b3_answer(q):
    r = (q[1] - q[0]) / (q[2] - q[1]); Qx = q[2] + (q[2] - q[1]) / (r - 1)
    return {"r": r, "p": math.log2(r), "q": Qx, "e": (q[2] - Qx) / Qx * 100}

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    check(all(pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6", "c1"]), "every MCQ carries data-ans")
    check(all(pg.get_attribute(f'.qc[data-qc="{q}"]', "data-ans") for q in ["r1", "r2", "q1", "q2", "q3", "q4", "q5", "q6"]), "every quick check and recall carries data-ans")
    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    # b1: stresses at a point, from fe_plane_stress.B_matrix and E_matrix; three different number sets
    for k in range(3):
        if k: pg.click('article[data-ex="b1"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        s, prm = b1_answer(given(pg, "b1"))
        for f, v in zip(["sxx", "syy", "sxy"], s): pg.fill(f'article[data-ex="b1"] input[data-f="{f}"]', f"{v:.0f}")
        submit(pg, "b1"); check(ok(pg, "b1"), f"b1 accepted fe_plane_stress stresses {np.round(s, 1)} for a, b, ν, x, y = {prm}")
    # a slip in the shear term (Ē instead of Ē(1 − ν)/2) is caught
    s, prm = b1_answer(given(pg, "b1")); nu = prm[2]
    pg.fill('article[data-ex="b1"] input[data-f="sxy"]', f"{s[2] * 2 / (1 - nu):.0f}"); submit(pg, "b1")
    check(pg.get_attribute('article[data-ex="b1"] input[data-f="sxy"]', "data-state") == "wrong", "b1 flags σxy computed with Ē instead of G")
    pg.click('article[data-ex="b1"] .qbar button:nth-of-type(2)'); pg.wait_for_timeout(100)
    check(pg.locator('article[data-ex="b1"] .hintbox').count() == 1, "b1 hint opens (second qbar button)")
    # b2: principal stresses and von Mises, from fe_plane_stress.principal and von_mises
    for k in range(3):
        if k: pg.click('article[data-ex="b2"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        t = given(pg, "b2"); st = [num(t, r"σxx = ([-\d.]+)"), num(t, r"σyy = ([-\d.]+)"), num(t, r"σxy = ([-\d.]+)")]
        s1, s2, th = principal(st); vm = von_mises(st)
        for f, v in zip(["s1", "s2", "th", "vm"], [s1, s2, th, vm]): pg.fill(f'article[data-ex="b2"] input[data-f="{f}"]', f"{v:.1f}")
        submit(pg, "b2"); check(ok(pg, "b2"), f"b2 accepted σ1, σ2, θ, vM = {s1:.1f}, {s2:.1f}, {th:.1f}°, {vm:.1f} for {st}")
    # the angle of σ2 instead of σ1 is caught
    pg.fill('article[data-ex="b2"] input[data-f="th"]', f"{th - 90 if th > 0 else th + 90:.1f}"); submit(pg, "b2")
    check(pg.get_attribute('article[data-ex="b2"] input[data-f="th"]', "data-state") == "wrong", "b2 flags the direction of σ2 given as θp")
    # b3: Richardson from the three displayed values
    for k in range(3):
        if k: pg.click('article[data-ex="b3"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        t = given(pg, "b3"); q = [float(v) for v in re.search(r"give the .*? ([\d.]+), ([\d.]+), ([\d.]+) mm", t).groups()]
        A3 = b3_answer(q)
        for f, fmt in [("r", "{:.2f}"), ("p", "{:.2f}"), ("q", "{:.3f}"), ("e", "{:.2f}")]: pg.fill(f'article[data-ex="b3"] input[data-f="{f}"]', fmt.format(A3[f]))
        submit(pg, "b3"); check(ok(pg, "b3"), f"b3 accepted Richardson for {q}: 2^p {A3['r']:.2f}, p {A3['p']:.2f}, Q {A3['q']:.3f}, err {A3['e']:.2f}%")
    # b4: consistent edge loads
    t = given(pg, "b4"); qv = num(t, r"load of ([\d.]+) kN"); L = num(t, r"ℓ = ([\d.]+) m")
    for f, v in [("fc", qv * L / 6), ("fm", 2 * qv * L / 3), ("f4", qv * L / 2)]: pg.fill(f'article[data-ex="b4"] input[data-f="{f}"]', f"{v:.3f}")
    submit(pg, "b4"); check(ok(pg, "b4"), f"b4 accepted qℓ/6, 2qℓ/3, qℓ/2 for q = {qv}, ℓ = {L}")
    pg.fill('article[data-ex="b4"] input[data-f="fm"]', f"{qv * L / 2:.3f}"); submit(pg, "b4")
    check(pg.get_attribute('article[data-ex="b4"] input[data-f="fm"]', "data-state") == "wrong", "b4 flags qℓ/2 at the mid-side node of an 8-node side")
    pg.fill('article[data-ex="b4"] input[data-f="fm"]', f"{2 * qv * L / 3:.3f}"); submit(pg, "b4")
    # qbar order
    labels = [x.strip() for x in pg.locator('article[data-ex="b1"] .qbar button').all_inner_texts()]
    check(len(labels) >= 4 and labels[0] == "Check" and labels[1].startswith("Hint") and labels[2:4] == ["Show solution", "New numbers"], f"qbar order {labels[:4]}")
    pg.click('.q[data-q="c1"] .errline button[data-k="4"]'); check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="4"]', "data-state") == "right", "c1 line 4 is the slip")
    check("17" in pg.inner_text('#v-exercises h3.part:nth-of-type(2)'), "part B heading counts 17 marks")
    check("6 × 1" in pg.inner_text('#v-exercises h3.part:nth-of-type(1)'), "part A heading counts 6 × 1 marks")
    # Explorer milestones and the lecture-point readouts through the stress lab iframe
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(2500)
    fr = pg.frame_locator("iframe.labframe")
    fr.locator("#b-p13").click(); pg.wait_for_timeout(500)
    check("done" in (pg.get_attribute('.tk[data-ms="p13"]', "class") or ""), "milestone p13 after the lecture point on 4-node 2 × 2")
    ro = fr.locator("#ro").inner_text().replace("−", "-")
    check("315.2, -44.9, -310.9" in ro and "494.4, -224.1" in ro and "636.8" in ro, "Explorer readouts at (3.5, 1.3) match the notes: σ = 315.2, −44.9, −310.9; σ1, σ2 = 494.4, −224.1; vM 636.8")
    fr.locator("#b-study").click(); pg.wait_for_timeout(6000)
    check("done" in (pg.get_attribute('.tk[data-ms="corner"]', "class") or ""), "milestone corner after the corner study")
    def seg(host, text): fr.locator(f"#{host} label", has_text=text).first.click(); pg.wait_for_timeout(700)
    seg("c-mesh", "4 × 2")
    for d in ["Elemental mean", "Unaveraged", "Averaged"]: seg("c-disp", d)
    check("done" in (pg.get_attribute('.tk[data-ms="disp3"]', "class") or ""), "milestone disp3 after the three display options on 4-node 4 × 2")
    seg("c-nen", "8-node"); fr.locator("#b-p13").click(); pg.wait_for_timeout(300)
    seg("c-mesh", "16 × 8"); seg("c-mesh", "32 × 16")
    check("done" in (pg.get_attribute('.tk[data-ms="refine"]', "class") or ""), "milestone refine after 8-node 16 × 8 and 32 × 16 at the lecture point")
    sxx = float(fr.locator("#ro .ro:nth-child(3) .v").inner_text().replace("−", "-").split(",")[0])
    check(abs(sxx - 153) < 6, f"8-node 32 × 16 σxx at (3.5, 1.3) = {sxx} (notes: converged 153, beam theory 225)")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def solve_cantilever') >= 0"), "Explorer tab code card shows fe_plane_stress.py")
    # examples read, progress badges
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200); pg.check('#z1 .readck input'); pg.check('#z2 .readck input')
    check(pg.inner_text('[data-bd="examples"]') == "2/3", "examples badge 2/3")
    check(pg.inner_text('[data-bd="exercises"]') == "5/11", "exercises badge 5/11 (b1–b4 + c1)")
    check(pg.inner_text('[data-bd="lab"]') == "4/4", "Explorer badge 4/4")
    # Start tab carries this part's own content
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    st = pg.inner_text("#v-start")
    check("§3.4–§3.5" in st and "A5 project briefing" in st and "A1 strains and stresses at (3.5, 1.3)" in st and "§2.2.2" not in st, "Start tab shows Part 5's text sections and activities")
    check("Recall from Plane Stress Part 2" in st, "Start tab recall title")
    check(pg.get_attribute('.partsw a[aria-current="page"]', "href").startswith("../05-"), "part switcher marks Part 5")
    # notes: every section has its quick check, and the quick checks answer
    pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(200)
    for q, k in [("q1", "a"), ("q2", "a"), ("q3", "b"), ("q4", "b"), ("q5", "b"), ("q6", "b")]:
        pg.click(f'#{q} .opt[data-k="{k}"]'); pg.wait_for_timeout(50)
    check(pg.locator('.qc .fb:not([hidden])').count() >= 6, "the six quick checks give feedback")
    # Malay toggle leaves no English-only gaps in the notes
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    b.close()
srv.shutdown()
print("FAILURES:", len(fails))
