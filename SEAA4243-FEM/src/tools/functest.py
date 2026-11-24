"""Functional test of a part page: answers computed independently in Python are entered into the
parameterised exercises and must be accepted; MCQs, confidence, hints, timer, lab milestones,
language toggle, persistence across reload, and progress arithmetic are exercised."""
import http.server, pathlib, re, socketserver, sys, threading, json
from playwright.sync_api import sync_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
slug = sys.argv[1]
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

def N4(a, b, x, y): return [(a - x) * (b - y) / (a * b), x * (b - y) / (a * b), x * y / (a * b), y * (a - x) / (a * b)]
def dN(a, b, x, y): return ([-(b - y) / (a * b), (b - y) / (a * b), y / (a * b), -y / (a * b)], [-(a - x) / (a * b), -x / (a * b), x / (a * b), (a - x) / (a * b)])

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 900}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(status=200, content_type="text/css", body=""))
    pg.goto(url); pg.wait_for_timeout(800)
    # --- recall + quick check in notes
    pg.click('.qc[data-qc="r1"] .opt[data-k="a"]'); pg.click('.qc[data-qc="r2"] .opt[data-k="a"]')  # second deliberately wrong
    check(pg.get_attribute('.qc[data-qc="r1"] .opt[data-k="a"]', "data-state") == "right", "recall r1 marked right")
    check(pg.get_attribute('.qc[data-qc="r2"] .opt[data-k="a"]', "data-state") == "wrong" and pg.get_attribute('.qc[data-qc="r2"] .opt[data-k="b"]', "data-state") == "right", "recall r2 wrong pick shows the right one")
    check("your answer" in pg.inner_text('.qc[data-qc="r2"] .opt[data-k="a"]').lower() and "✗ Not quite" in pg.inner_text('.qc[data-qc="r2"] .fb'), "recall r2: 'your answer' tag and ✗ verdict")
    check("done" in (pg.get_attribute('li[data-stage-item="qc:r1"]', "class") or ""), "plan item for recall 1 ticked")
    # way-finding: home button, breadcrumb, part switcher, plan item links
    check(pg.get_attribute(".homeicon", "href") == "../index.html" and pg.get_attribute(".crumbs .homelink", "href") == "../index.html", "home icon and breadcrumb link to the course home")
    check(pg.evaluate("document.querySelectorAll('.partsw a').length") == 2 and pg.get_attribute('.partsw a[aria-current="page"]', "href").startswith("../01-"), "part switcher: Part 1 current, Part 2 linked")
    check(pg.evaluate("document.querySelectorAll('.pagenav a.phome').length") == 1, "page footer has a course-home link")
    pg.click('li[data-stage-item="read:n1"] a'); pg.wait_for_timeout(300)
    check(pg.get_attribute('.tab[data-view="notes"]', "aria-selected") == "true" and pg.evaluate("location.hash") == "#notes-n1", "plan item opens Notes §1, hash #notes-n1")
    pg.click('.toc a[data-toc="n3"]'); pg.wait_for_timeout(300)
    check(pg.evaluate("location.hash") == "#notes-n3", "toc link uses #notes-n3")
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    # downloads fall back to an ordinary download outside claude.ai
    with pg.expect_download() as dl:
        pg.click('#files [data-zip]')
    check(dl.value.suggested_filename == "seaa4243-shape-functions.zip", "Python zip downloads: " + dl.value.suggested_filename)
    import zipfile, io
    zb = zipfile.ZipFile(dl.value.path()); ref = zipfile.ZipFile(SITE / "code" / "seaa4243-shape-functions.zip")
    check(zb.testzip() is None and zb.namelist() == ref.namelist() and all(zb.read(n) == ref.read(n) for n in ref.namelist()),
          "browser-built zip is valid and matches the reference: " + ", ".join(zb.namelist()))
    with pg.expect_download() as dl:
        pg.click('#files [data-save$=".pdf"]')
    check(dl.value.suggested_filename == "heat-transfer-1-slides.pdf", "slides PDF downloads: " + dl.value.suggested_filename)
    # --- notes: mark read
    pg.click('.tab[data-view="notes"]'); pg.wait_for_timeout(200)
    for sid in ["n1", "n2"]: pg.check(f'#{sid} .readck input')
    check(pg.inner_text('[data-bd="notes"]') == "2/6", "notes badge 2/6")
    # --- exercises
    pg.click('.tab[data-view="exercises"]'); pg.wait_for_timeout(300)
    pg.click("#tstart"); pg.wait_for_timeout(2300)   # the display ticks once a second, phase set by page load
    check(pg.inner_text("#tmr") != "0:00", "timer runs")
    pg.click('.q[data-q="a1"] .conf button[data-c="sure"]'); pg.click('.q[data-q="a1"] .opt[data-k="b"]')
    pg.click('.q[data-q="a2"] .conf button[data-c="unsure"]'); pg.click('.q[data-q="a2"] .opt[data-k="b"]')  # wrong
    check(pg.get_attribute('.q[data-q="a1"] .opt[data-k="b"]', "data-state") == "right", "a1 right")
    check(pg.get_attribute('.q[data-q="a2"] .opt[data-k="a"]', "data-state") == "right" and pg.get_attribute('.q[data-q="a2"] .opt[data-k="b"]', "data-state") == "wrong", "a2 wrong shows right")
    check("✓ Correct" in pg.inner_text('.q[data-q="a1"] .fb') and "sure" in pg.inner_text('.q[data-q="a1"] .fb'), "a1 feedback shows ✓ verdict and confidence")
    check(pg.inner_text('.q[data-q="a1"] .opt[data-k="b"] .mark') == "✓" and pg.inner_text('.q[data-q="a2"] .opt[data-k="b"] .mark') == "✗", "a1 ✓ mark on the right option; a2 ✗ on the wrong pick")
    check("✗ Not quite" in pg.inner_text('.q[data-q="a2"] .fb') and pg.get_attribute('.q[data-q="a2"] .fb', "data-ok") == "false", "a2 verdict ✗ Not quite, red feedback box")
    check(pg.get_attribute('.q[data-q="a2"] .opt[data-k="c"]', "data-state") == "other", "a2 untouched option dimmed")
    # parameterised: read the given numbers from the page, compute in Python, enter, check
    def params(eid):
        t = pg.inner_text(f'article[data-ex="{eid}"] .given')
        a = float(re.search(r"a = ([\d.]+) m", t).group(1)); bb = float(re.search(r"b = ([\d.]+) m", t).group(1))
        m = re.search(r"\(x, y\) = \(([\d.]+), ([\d.]+)\)", t); x, y = (float(m.group(1)), float(m.group(2))) if m else (None, None)
        T = [float(v) for v in re.search(r"T̂ = \{([^}]+)\}", t).group(1).split(",")]
        km = re.search(r"= ([\d.]+) W m", t); k = float(km.group(1)) if km else None
        return a, bb, x, y, T, k
    a, bb, x, y, T, k = params("b1"); N = N4(a, bb, x, y)
    for i in range(4): pg.fill(f'article[data-ex="b1"] input[data-f="n{i+1}"]', f"{N[i]:.3f}")
    pg.fill('article[data-ex="b1"] input[data-f="t"]', f"{sum(n * t for n, t in zip(N, T)):.1f}")
    pg.click('article[data-ex="b1"] .conf button[data-c="sure"]')
    pg.click('article[data-ex="b1"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(200)
    check("Correct" in pg.inner_text('article[data-ex="b1"] .resline'), f"b1 accepted Python values a={a} b={bb} P=({x},{y}) T={T}")
    # wrong entry then new numbers
    a, bb, x, y, T, k = params("b2"); dx, dy = dN(a, bb, x, y)
    gx = sum(d * t for d, t in zip(dx, T)); gy = sum(d * t for d, t in zip(dy, T))
    pg.fill('article[data-ex="b2"] input[data-f="gx"]', f"{gx:.1f}"); pg.fill('article[data-ex="b2"] input[data-f="gy"]', f"{gy:.1f}")
    pg.fill('article[data-ex="b2"] input[data-f="qx"]', f"{-k*gx:.1f}"); pg.fill('article[data-ex="b2"] input[data-f="qy"]', f"{k*gy:.1f}")  # qy sign wrong on purpose
    pg.click('article[data-ex="b2"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(200)
    r = pg.inner_text('article[data-ex="b2"] .resline'); check("3 of 4" in r, "b2 partial: 3 of 4 (wrong qy sign caught) → " + r.split("\n")[0])
    check(pg.get_attribute('article[data-ex="b2"] input[data-f="qy"]', "data-state") == "wrong", "b2 qy field flagged wrong")
    check(pg.inner_text('article[data-ex="b2"] input[data-f="qy"] + .fmark') == "✗" and pg.inner_text('article[data-ex="b2"] input[data-f="qx"] + .fmark') == "✓", "b2 field marks: qx ✓, qy ✗")
    # hints and solution
    pg.click('article[data-ex="b2"] .qbar button:nth-of-type(2)'); pg.wait_for_timeout(100)
    check(len(pg.query_selector_all('article[data-ex="b2"] .hintbox')) == 1, "hint 1 shown")
    pg.click('article[data-ex="b2"] .qbar button:nth-of-type(3)'); pg.wait_for_timeout(100)
    sol = pg.inner_text('article[data-ex="b2"] .sol'); check(f"{gx:.1f}".replace("-", "−") in sol, "solution uses the current numbers")
    # new numbers changes the statement and clears fields
    before = pg.inner_text('article[data-ex="b3"] .given'); pg.click('article[data-ex="b3"] .qbar button:nth-of-type(4)'); pg.wait_for_timeout(150)
    check(pg.inner_text('article[data-ex="b3"] .given') != before, "b3 new numbers changes the statement")
    a, bb, x, y, T, k = params("b3")
    vals = {"a1": T[0], "a2": (T[1] - T[0]) / a, "a3": (T[3] - T[0]) / bb, "a4": (T[0] - T[1] + T[2] - T[3]) / (a * bb)}
    for f, v in vals.items(): pg.fill(f'article[data-ex="b3"] input[data-f="{f}"]', f"{v:.2f}")
    pg.click('article[data-ex="b3"] .qbar .btn:not(.ghost)'); pg.wait_for_timeout(200)
    check("Correct" in pg.inner_text('article[data-ex="b3"] .resline'), "b3 accepted Python coefficients")
    # error spotting
    pg.click('.q[data-q="c1"] .conf button[data-c="sure"]'); pg.click('.q[data-q="c1"] .errline button[data-k="4"]')
    check(pg.get_attribute('.q[data-q="c1"] .errline button[data-k="4"]', "data-state") == "right", "c1 line 4 right")
    st = pg.inner_text("#exstats"); check("6/10" in st, "stats: 6/10 answered → " + st.split("\n")[0])
    check("Sure" in st and "A2" in st or "Sure and wrong" in st, "calibration table rendered")
    # --- lab milestone via postMessage and via localStorage
    pg.click('.tab[data-view="lab"]'); pg.wait_for_timeout(1500)
    fr = pg.frame_locator("iframe.labframe"); fr.locator("#b-n3").click(); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="node3"]', "class") or ""), "lab milestone node3 ticked via postMessage")
    fr.locator("#b-act4").click(); pg.wait_for_timeout(300)
    check("done" in (pg.get_attribute('.tk[data-ms="act4"]', "class") or ""), "lab milestone act4 ticked")
    check(pg.inner_text('[data-bd="lab"]') == "2/4", "lab badge 2/4")
    check(pg.evaluate("document.querySelector('#code pre.code').textContent.indexOf('def shape_q4') >= 0"), "Explorer tab shows the Python code")
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    pg.click('#code summary'); pg.click('#code [data-copy]'); pg.wait_for_timeout(200)
    check("Copied" in pg.inner_text('#code .copymsg') and "def shape_q4" in pg.evaluate("navigator.clipboard.readText()"), "copy puts the code on the clipboard")
    # --- can-do + progress arithmetic
    pg.click('.tab[data-view="start"]'); pg.wait_for_timeout(200)
    pg.click('.cando .row[data-c="c1"] button[data-v="2"]'); pg.click('.cando .row[data-c="c2"] button[data-v="1"]')
    pct = pg.inner_text("#ppct")
    # notes 2/6, slides 0/49, exercises 6/10, lab 2/4, checklist 1.5/4 -> mean = (0.3333+0+0.6+0.5+0.375)/5 = 0.3617 -> 36 %
    check(pct.strip() == "30 %", f"progress arithmetic 30 % (six parts, examples unread) (got {pct})")
    # --- language toggle and persistence
    pg.click('[data-setlang="ms"]'); pg.wait_for_timeout(100)
    check(pg.evaluate("getComputedStyle(document.querySelector('#t-notes .ms')).display") != "none" and pg.evaluate("getComputedStyle(document.querySelector('#t-notes .en')).display") == "none", "BM shows Malay, hides English")
    pg.click("#themebtn"); pg.click("#themebtn")  # auto -> light -> dark
    check(pg.get_attribute("html", "data-theme") == "dark", "theme cycles to dark")
    pg.reload(); pg.wait_for_timeout(800)
    check(pg.get_attribute("html", "data-lang") == "ms" and pg.get_attribute("html", "data-theme") == "dark", "prefs persist after reload")
    check(pg.inner_text("#ppct").strip() == "30 %", "progress persists after reload")
    check(pg.inner_text('[data-bd="exercises"]') == "6/10", "exercise records persist")
    # examples: mark one worked through
    pg.click('.tab[data-view="examples"]'); pg.wait_for_timeout(200); pg.check('#x1 .readck input'); pg.wait_for_timeout(100)
    check(pg.inner_text('[data-bd="examples"]') == "1/3", "examples badge 1/3 after marking x1")
    # slides tab loads the fragment and tracks seen
    pg.click('.tab[data-view="slides"]'); pg.wait_for_timeout(2500)
    pg.keyboard.press("ArrowRight"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(200)
    check(pg.inner_text("#svcount").strip() == "3 / 49", "keyboard advances to slide 3")
    check(pg.inner_text('[data-bd="slides"]') == "3/49", "slides seen badge 3/49")
    check(pg.evaluate("document.querySelectorAll('#svcv .sl').length") == 49, "49 slides injected")
    check(pg.evaluate("document.querySelector('#svcv .sl.on img') ? document.querySelector('#svcv .sl.on img').naturalWidth : 1") > 0, "slide image loads (if any on this slide)")
    # glossary filter
    pg.click('.tab[data-view="glossary"]'); pg.fill("#gfilter", "Kronecker"); pg.wait_for_timeout(100)
    vis = pg.evaluate("Array.from(document.querySelectorAll('.gloss tbody tr')).filter(t=>!t.hidden).length"); check(vis == 1, f"glossary filter leaves 1 row ({vis})")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    b.close()
srv.shutdown()
print("FAILURES:", len(fails))
