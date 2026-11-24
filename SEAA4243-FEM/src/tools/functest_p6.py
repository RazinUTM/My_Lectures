"""Functional test of the ANSYS demo page (Part 6): parameterised exercises checked against independent Python
(fe_plane_stress.timoshenko_tip; Force, Pressure, consistent loads and Richardson by hand), on the displayed numbers and on
a sweep of 3000 seeds of each generator; MCQ answers present; Cantilever Explorer milestones through the iframe; progress
badges; Start tab, slides, examples, notes and the Part 6 browser scripts. The numbers quoted in the notes are re-derived
from the course solvers at the end, so a change of solver or text is caught here."""
import http.server, math, pathlib, re, socketserver, sys, threading
import numpy as np
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SITE / "code"))
import fe_plane_stress as ps
from fe_heat_q4 import solve_plate, temperature_at

slug = sys.argv[1] if len(sys.argv) > 1 else "06-ansys-demo"
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
def state(pg, ex, f): return pg.get_attribute(f'article[data-ex="{ex}"] input[data-f="{f}"]', "data-state")


# ---- independent answers ----
def b1_py(q, H, t, n): return {"F": q * H, "p": q / t, "fm": q * H / n}           # kN, kPa, kN

def b2_py(v):
    d1, d2 = v[1] - v[0], v[2] - v[1]; r = d1 / d2
    return {"c": d2 / v[2] * 100, "r": r, "p": math.log2(r), "q": v[2] + d2 / (r - 1)}

def b3_py(L, H, t, E, nu, q, fe):
    bend, shear = ps.timoshenko_tip(L, H, E, nu, t, -q)                          # magnitudes, m
    vt = (bend + shear) * 1000
    return {"R": q * H / 1000, "M": q * H * L / 1000, "vt": vt, "e": (fe - vt) / vt * 100}


SWEEP = r"""(function(N){
  function rng(seed){ var t=seed>>>0; return function(){ t+=0x6D2B79F5; var r=Math.imul(t^(t>>>15),1|t); r^=r+Math.imul(r^(r>>>7),61|r); return ((r^(r>>>14))>>>0)/4294967296; }; }
  var out={};
  ["b1","b2","b3"].forEach(function(id){ var s=EX.specs[id], L=[];
    for (var k=1;k<=N;k++){ var P=s.gen(rng(1000+37*k)), v={}; s.fields.forEach(function(f){ v[f.id]=f.fn(P); }); L.push({P:P, v:v}); }
    out[id]=L; });
  return out; })"""

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    check(all(pg.get_attribute(f'.q[data-q="{q}"]', "data-ans") for q in ["a1", "a2", "a3", "a4", "a5", "a6", "c1"]), "every MCQ carries data-ans")
    check(all(pg.get_attribute(f'.qc[data-qc="{q}"]', "data-ans") for q in ["r1", "r2", "q1", "q2", "q3", "q4", "q5", "q6"]), "every quick check and recall carries data-ans")

    # ---- seed sweep: every generator against independent Python, 3000 number sets each ----
    sw = pg.evaluate(SWEEP + "(3000)")
    bad = [s for s in sw["b1"] if any(abs(s["v"][k] - b1_py(s["P"]["q"], s["P"]["H"], s["P"]["t"], s["P"]["n"])[k]) > 1e-9 * max(1, abs(s["v"][k])) for k in "F p fm".split())]
    check(not bad, f"b1 sweep: 3000 seeds agree with q·H, q/t, q·H/n ({len(bad)} disagree)")
    bad = [s for s in sw["b2"] if any(abs(s["v"][k] - b2_py(s["P"]["q"])[k]) > 1e-9 * max(1, abs(s["v"][k])) for k in "c r p q".split())]
    deg = [s for s in sw["b2"] if not (s["v"]["r"] > 1.2 and 0 < s["v"]["c"] < 50 and s["v"]["p"] > 0.2)]
    check(not bad, f"b2 sweep: 3000 seeds agree with Richardson in Python ({len(bad)} disagree)")
    check(not deg, f"b2 sweep: no degenerate set (2^p > 1.2, 0 < change < 50 %, p > 0.2) ({len(deg)} degenerate)")
    bad, deg = [], []
    for s in sw["b3"]:
        P_ = s["P"]; ref = b3_py(P_["L"], P_["H"], P_["t"], P_["E"], P_["nu"], P_["q"], P_["fe"])
        if any(abs(s["v"][k] - ref[k]) > 1e-9 * max(1, abs(ref[k])) for k in "R M vt e".split()): bad.append(s)
        if not (P_["L"] / P_["H"] >= 2 and 2 <= ref["vt"] <= 900 and -6.5 < ref["e"] < 0): deg.append(s)
    check(not bad, f"b3 sweep: 3000 seeds agree with fe_plane_stress.timoshenko_tip ({len(bad)} disagree)")
    check(not deg, f"b3 sweep: L/H ≥ 2, 2–900 mm, ANSYS value 0–6.5 % stiff in every set ({len(deg)} outside)")

    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    # b1: three displayed number sets, typed as a student would round them
    for k in range(3):
        if k: pg.click('article[data-ex="b1"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        t = given(pg, "b1"); q = num(t, r"load of ([\d.]+) kN"); H_ = num(t, r"H = ([\d.]+) m"); tt = num(t, r"t = ([\d.]+) m"); n = int(num(t, r"into (\d+) equal"))
        A1 = b1_py(q, H_, tt, n)
        for f, fm in [("F", "{:.3f}"), ("p", "{:.1f}"), ("fm", "{:.3f}")]: pg.fill(f'article[data-ex="b1"] input[data-f="{f}"]', fm.format(A1[f]))
        submit(pg, "b1"); check(ok(pg, "b1"), f"b1 accepted F {A1['F']:.3f} kN, p {A1['p']:.1f} kPa, interior {A1['fm']:.3f} kN for q, H, t, n = {q}, {H_}, {tt}, {n}")
    pg.fill('article[data-ex="b1"] input[data-f="p"]', f"{q * tt:.1f}"); pg.fill('article[data-ex="b1"] input[data-f="fm"]', f"{q * H_ / (2 * n):.3f}"); submit(pg, "b1")
    check(state(pg, "b1", "p") == "wrong" and state(pg, "b1", "fm") == "wrong", "b1 flags Pressure = q × t and the end-node share qh/2 at an interior node")
    pg.click('article[data-ex="b1"] .qbar button:nth-of-type(2)'); pg.wait_for_timeout(100)
    check(pg.locator('article[data-ex="b1"] .hintbox').count() == 1, "b1 hint opens (second qbar button)")
    # b2
    for k in range(3):
        if k: pg.click('article[data-ex="b2"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        t = given(pg, "b2"); v = [float(x) for x in re.search(r"deflections of ([\d.]+), ([\d.]+), ([\d.]+) mm", t).groups()]
        A2 = b2_py(v)
        for f, fm in [("c", "{:.2f}"), ("r", "{:.2f}"), ("p", "{:.2f}"), ("q", "{:.3f}")]: pg.fill(f'article[data-ex="b2"] input[data-f="{f}"]', fm.format(A2[f]))
        submit(pg, "b2"); check(ok(pg, "b2"), f"b2 accepted change {A2['c']:.2f} %, 2^p {A2['r']:.2f}, p {A2['p']:.2f}, Q {A2['q']:.3f} for {v}")
    pg.fill('article[data-ex="b2"] input[data-f="p"]', f"{A2['r']:.2f}"); submit(pg, "b2")
    check(state(pg, "b2", "p") == "wrong", "b2 flags 2^p given as p")
    # b3
    for k in range(3):
        if k: pg.click('article[data-ex="b3"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
        t = given(pg, "b3")
        L = num(t, r"L = ([\d.]+) m"); H_ = num(t, r"H = ([\d.]+) m"); tt = num(t, r"t = ([\d.]+) m"); E = num(t, r"E = ([\d.]+) × 10⁶") * 1e6
        nu = num(t, r"ν = ([\d.]+)"); q = num(t, r"traction of ([\d.]+) N"); fe = num(t, r"deflection of ([\d.]+) mm")
        A3 = b3_py(L, H_, tt, E, nu, q, fe)
        for f, fm in [("R", "{:.3f}"), ("M", "{:.3f}"), ("vt", "{:.3f}"), ("e", "{:.2f}")]: pg.fill(f'article[data-ex="b3"] input[data-f="{f}"]', fm.format(A3[f]))
        submit(pg, "b3"); check(ok(pg, "b3"), f"b3 accepted R {A3['R']:.3f} kN, M {A3['M']:.3f} kN m, Timoshenko {A3['vt']:.3f} mm, diff {A3['e']:.2f} % for L, H, t, E, ν, q, FE = {L}, {H_}, {tt}, {E:.0e}, {nu}, {q}, {fe}")
    bend, _ = ps.timoshenko_tip(L, H_, E, nu, tt, -q)
    pg.fill('article[data-ex="b3"] input[data-f="vt"]', f"{bend * 1000:.3f}"); pg.fill('article[data-ex="b3"] input[data-f="M"]', f"{q * H_ * H_ / 1000:.3f}"); submit(pg, "b3")
    check(state(pg, "b3", "vt") == "wrong" and state(pg, "b3", "M") == "wrong", "b3 flags Timoshenko without the shear term and the moment with the depth as lever arm")
    labels = [x.strip() for x in pg.locator('article[data-ex="b1"] .qbar button').all_inner_texts()]
    check(len(labels) >= 4 and labels[0] == "Check" and labels[1].startswith("Hint") and labels[2:4] == ["Show solution", "New numbers"], f"qbar order {labels[:4]}")
    pg.click('.q[data-q="c1"] .errline button[data-k="4"]'); check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="4"]', "data-state") == "right", "c1 line 4 (moment lever arm) is the slip")
    check("12" in pg.inner_text('#v-exercises h3.part:nth-of-type(2)'), "part B heading counts 12 marks")
    check("6 × 1" in pg.inner_text('#v-exercises h3.part:nth-of-type(1)'), "part A heading counts 6 × 1 marks")

    # ---- Explorer: the Cantilever Explorer, six milestones ----
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(2500)
    fr = pg.frame_locator("iframe.labframe")
    fr.locator("#b-reset").click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="book22"]', "class") or ""), "milestone book22 after “Text example”")
    ro = fr.locator("#ro").inner_text().replace("−", "-")
    check("-0.1306" in ro, "Explorer shows the 2 × 2 hand value −0.1306 m (the prediction for the Linear 2 × 2 run)")
    fr.locator("#b-study").click(); pg.wait_for_timeout(3000)
    check("done" in (pg.get_attribute('.tk[data-ms="study"]', "class") or ""), "milestone study after the mesh study")
    fr.locator('label:has-text("8-node (quadratic)")').click(); fr.locator('#c-mesh label:text-is("8 × 4")').click(); pg.wait_for_timeout(400)
    ro = fr.locator("#ro").inner_text().replace("−", "-")
    check("-0.1906" in ro, "Explorer 8-node 8 × 4 tip −0.1906 m, as in the notes’ mesh-study table")
    fr.locator('label:has-text("Plane strain")').click(); fr.locator('label:has-text("Plane stress")').click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="pstrain"]', "class") or ""), "milestone pstrain after both idealisations")
    fr.locator('label:has-text("Point force at top corner")').click(); pg.wait_for_timeout(400)
    check("done" in (pg.get_attribute('.tk[data-ms="point"]', "class") or ""), "milestone point after the corner force")
    fr.locator('#c-load label:text-is("Edge traction")').click(); pg.wait_for_timeout(200)
    fr.locator('label:has-text("Vertical only")').click(); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="vonly"]', "class") or ""), "milestone vonly after the vertical-only support")
    fr.locator('label:has-text("Fixed: u = v = 0")').click(); pg.wait_for_timeout(200)
    fr.locator("details:has(#i-t) summary").click(); fr.locator("#i-t").fill("0.02"); fr.locator("#i-t").press("Enter"); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="thick"]', "class") or ""), "milestone thick after changing t")
    check(pg.inner_text('[data-bd="lab"]') == "6/6", "Explorer badge 6/6")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def solve_cantilever') >= 0"), "Explorer tab code card shows fe_plane_stress.py")
    tabs = pg.locator("#run .pyseg button").all_inner_texts()
    check(len(tabs) == 3 and "Patch test" in tabs[0] and "Wrong-model" in tabs[1], f"Run-in-browser panel carries the Part 6 scripts {tabs}")

    # ---- examples, slides, badges ----
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200)
    check(pg.locator(".xarticle .xhead").count() == 4, "four worked examples")
    pg.check('#y1 .readck input'); pg.check('#y4 .readck input')
    check(pg.inner_text('[data-bd="examples"]') == "2/4", "examples badge 2/4")
    check(pg.inner_text('[data-bd="exercises"]') == "4/10", "exercises badge 4/10 (b1–b3 + c1)")
    # the template engine reveals the steps of a model answer one at a time: show them all first
    for sb in pg.locator("#v-examples .xbar .btn.ghost").all():
        if sb.is_visible(): sb.click()
    ex = pg.inner_text("#v-examples")
    for s in ["0.6214", "0.4821", "0.3857", "−600 W", "0.19155", "0.35%", "5353", "0.8753", "−20 000"]:
        check(s.replace("−", "-") in ex.replace("−", "-") or s in ex, f"examples show {s}")
    pg.click('.tab[data-view="slides"]'); pg.wait_for_timeout(2500)
    check(pg.evaluate("document.querySelectorAll('#svcv .sl').length") == 36, "36 slides injected")
    imgs = pg.evaluate("Array.from(document.querySelectorAll('#svcv img')).map(i => i.getAttribute('src'))")
    check(all(s.startswith("slides/img/") for s in imgs) and sum("fig_" in s for s in imgs) >= 5, f"slide images mapped to local files ({len(imgs)})")
    # ---- Start tab, switcher ----
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    st = pg.inner_text("#v-start")
    check("§2.3 and §3.4" in st and "A5 project lab" in st and "A1 convert the textbook data" in st and "§3.4–§3.5" not in st, "Start tab shows Part 6's text sections and activities")
    check("Recall from Plane Stress Part 3" in st, "Start tab recall title")
    check(pg.get_attribute('.partsw a[aria-current="page"]', "href").startswith("../06-"), "part switcher marks Part 6")
    # ---- notes: quick checks and the Malay twin ----
    pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(200)
    for q, k in [("q1", "a"), ("q2", "a"), ("q3", "b"), ("q4", "b"), ("q5", "b"), ("q6", "b")]:
        pg.click(f'#{q} .opt[data-k="{k}"]'); pg.wait_for_timeout(50)
    check(pg.locator('.qc .fb:not([hidden])').count() >= 6, "the six quick checks give feedback")
    n_en = pg.evaluate("document.querySelectorAll('#v-notes .en').length"); n_ms = pg.evaluate("document.querySelectorAll('#v-notes .ms').length")
    check(n_en == n_ms and n_en > 100, f"notes carry a Malay twin for every English span ({n_en} / {n_ms})")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    b.close()
srv.shutdown()

# ---- the numbers quoted on the page, re-derived from the course solvers ----
pl = {N: temperature_at(solve_plate(1, 1, N, N, 300, edges=dict(top=("T", 0.0), left=("T", 0.0)), Q=600.0), 1.0, 0.0)["T"] for N in (2, 4, 8, 16)}
check([round(pl[N], 4) for N in (2, 4, 8, 16)] == [0.6214, 0.5968, 0.5912, 0.5898], f"plate corner 2/4/8/16: {[round(pl[N], 4) for N in (2, 4, 8, 16)]}")
r2 = solve_plate(1, 1, 2, 2, 300, edges=dict(top=("T", 0.0), left=("T", 0.0)), Q=600.0)
check(abs(r2["heat"].sum() + 600) < 1e-6 and [round(x, 4) for x in r2["T"][[1, 4, 5]]] == [0.4821, 0.3857, 0.4821], "plate 2 × 2: T2, T5, T6 and Σ heat = −600 W")
q8 = {m: abs(ps.solve_cantilever(Nx=m[0], Ny=m[1], nen=8)["tip"]) for m in [(2, 1), (4, 2), (8, 4), (16, 8), (32, 16)]}
q4 = {m: abs(ps.solve_cantilever(Nx=m[0], Ny=m[1], nen=4)["tip"]) for m in [(2, 2), (4, 2), (8, 4), (16, 8)]}
check([round(q8[m], 5) for m in q8] == [0.17796, 0.18846, 0.19059, 0.19125, 0.19151], f"Q8 tips {[round(q8[m], 5) for m in q8]}")
check([round(q4[m], 4) for m in q4] == [0.1306, 0.1643, 0.1824, 0.1886], f"Q4 tips {[round(q4[m], 4) for m in q4]}")
ch = [round((q8[b_] - q8[a_]) / q8[b_] * 100, 2) for a_, b_ in [((2, 1), (4, 2)), ((4, 2), (8, 4)), ((8, 4), (16, 8))]]
check(ch == [5.57, 1.12, 0.35], f"changes {ch}")
tim = sum(ps.timoshenko_tip(4, 2, 200e6, 0.33, 0.01, -5000))
check(round(tim, 4) == 0.1919 and round((q8[(16, 8)] - tim) / tim * 100, 2) == -0.35 and round((q4[(16, 8)] - tim) / tim * 100, 1) == -1.7, "Timoshenko 0.1919 m; Q8 16 × 8 −0.35 %; Q4 16 × 8 −1.7 %")
s16 = ps.solve_cantilever(Nx=16, Ny=8, nen=8)
check(round(ps.stress_at(s16, 2.0, 1.5)[0] / 1e3, 1) == 1500.3, "Q8 16 × 8 σxx at (2, 1.5) = 1500.3 kN/m2 (beam 1500)")
wr = {k: ps.solve_cantilever(Nx=32, Ny=16, nen=8, **kw) for k, kw in [("ok", {}), ("strain", dict(plane="strain")), ("point", dict(load="point")), ("t1", dict(t=1.0))]}
check([round(abs(wr[k]["tip"]), 4) for k in ("ok", "strain", "point")] == [0.1915, 0.1722, 0.2298] and round(abs(wr["t1"]["tip"]), 6) == 0.001915
      and all(abs(wr[k]["reactions"]["Ry"] - 10000) < 1e-6 for k in wr), "wrong models: 0.1915 / 0.1722 / 0.2298 / 0.001915 m, Ry = 10 000 N in all")
e_top = len(wr["ok"]["conn"]) - 1
vm = [round(ps.von_mises(ps.stress_in_element(wr[k], e_top, 0, 0)) / 1e3) for k in ("ok", "point")]
check(vm == [523, 5353], f"σvM in the element under the load: {vm}")
check(round(ps.element_stiffness(4, 2, 1, ps.E_matrix(200e6, 0.33), 0.01)[0, 0] / 1e6, 4) == 0.8753, "k11 = 0.8753e6 N/m")
print("FAILURES:", len(fails))
