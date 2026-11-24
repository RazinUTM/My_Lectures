"""End-to-end test of the Run in browser panel with a local copy of Pyodide 0.29.5.

Serves the site and the Pyodide files from one local server; window.SEAA_PYURL points the page at the
local Pyodide (the website uses the jsDelivr CDN), and any request to the CDN fails the test.
A second host name, mapped to the same server, checks the gate that disables Run outside GitHub Pages."""
import http.server, json, os, pathlib, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright

import os, tempfile
SITE = pathlib.Path(__file__).resolve().parent.parent.parent      # SEAA4243-FEM
S = pathlib.Path(os.environ.get("SEAA_WORK", os.path.join(tempfile.gettempdir(), "seaa4243-work"))); (S / "shots").mkdir(parents=True, exist_ok=True)
ROOT = S / "serve"
ROOT.mkdir(exist_ok=True)
for name, target in (("SEAA4243-FEM", SITE), ("pyodide", pathlib.Path(os.environ.get("PYODIDE_DIR", str(S / "pyodide"))))):
    link = ROOT / name
    if not link.exists(): link.symlink_to(target)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *a): pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Quiet)
PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://localhost:{PORT}/SEAA4243-FEM/"

PARTS = {1: "01-heat-transfer-1", 2: "02-heat-transfer-2", 3: "03-plane-stress-1", 4: "04-plane-stress-2", 5: "05-plane-stress-3"}
EXPECT = {  # (substring in the output, number of figures)
    1: [("T      = 136.0", 0), ("partition of unity: True", 1), ("(expected 136.0)", 2)],
    2: [("8 x 8: T(1, 0) = 0.5912", 1), ("T   = [0.     0.4821 0.6214", 0), ("T2 = T6 = 0.4821", 1)],
    3: [("[[224.44  74.07   0.  ]", 0), ("sxx = 9.01, syy = -6.03, sxy = 0.56 kN/m2", 0), ("tip deflection = -0.1306 m", 1)],
    4: [("row sums: [ 0.  0.  0.  0.  0.  0.  0. -0.]", 0), ("16 x 8   tip = -0.1886 m  (-1.7 %)", 0), ("principal 494.4, -224.1", 1)],
    5: [("von Mises = 636.8 kN/m2", 0), ("saved von_mises.png", 1), ("8-node 16 x 8: sxx(2.0, 1.3)", 1)],
}
fails, notes = [], []
def check(cond, msg):
    (notes if cond else fails).append(("ok  " if cond else "FAIL ") + msg)


def wait_done(page, timeout=240):
    t0 = time.time()
    page.wait_for_function("() => { const s = document.querySelector('.pyrun .pystat'); return s && /\\bpy(ok|bad)\\b/.test(s.className); }", timeout=timeout * 1000)
    return time.time() - t0


with sync_playwright() as p:
    br = p.chromium.launch(args=[f"--host-resolver-rules=MAP preview.test 127.0.0.1"])
    ctx = br.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script(f"window.SEAA_PYURL = 'http://localhost:{PORT}/pyodide/';")
    cdn = []
    ctx.route("**/cdn.jsdelivr.net/**", lambda r: (cdn.append(r.request.url), r.abort()))
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    timings = {}
    for n, slug in PARTS.items():
        page.goto(BASE + slug + "/index.html#lab-run")
        page.wait_for_selector(".pyrun [data-pyrun]")
        btns = page.locator(".pyrun [data-py]")
        check(btns.count() == 3, f"part {n}: 3 scripts")
        for i in range(btns.count()):
            btns.nth(i).click()
            page.locator(".pyrun [data-pyrun]").click()
            dt = wait_done(page)
            out = page.locator(".pyrun .pyout").inner_text()
            nfig = page.locator(".pyrun .pyfigs img").count()
            stat = page.locator(".pyrun .pystat").inner_text()
            sub, nf = EXPECT[n][i]
            timings[f"{n}.{i}"] = round(dt, 1)
            check("pyok" in page.locator(".pyrun .pystat").get_attribute("class"), f"part {n} script {i}: status ok ({stat})")
            check(sub in out, f"part {n} script {i}: output has {sub!r}" + ("" if sub in out else f"\n----\n{out[-1500:]}\n----"))
            check(nfig == nf, f"part {n} script {i}: {nfig} figure(s), expected {nf}")
            if nfig:
                ok_img = page.evaluate("() => Array.from(document.querySelectorAll('.pyrun .pyfigs img')).every(i => i.complete && i.naturalWidth > 200)")
                check(ok_img, f"part {n} script {i}: figures decoded")
        if n == 5:
            page.locator(".pyrun [data-py]").nth(1).click(); page.locator(".pyrun [data-pyrun]").click(); wait_done(page)
            page.locator(".pyrun").screenshot(path=str(S / "shots" / "pyrun_p5_desktop.png"))

    # an error: the traceback names the script line
    page.goto(BASE + "index.html"); page.goto(BASE + "05-plane-stress-3/index.html#lab-run"); page.wait_for_selector(".pyrun [data-pyrun]")
    page.locator(".pyrun [data-py]").nth(0).click()
    ed = page.locator(".pyrun .pyedit")
    ed.fill("x = 1\ny = x / 0\n")
    page.locator(".pyrun [data-pyrun]").click(); wait_done(page)
    out = page.locator(".pyrun .pyout").inner_text()
    check("pybad" in page.locator(".pyrun .pystat").get_attribute("class") and 'File "script", line 2' in out and "ZeroDivisionError" in out and "_pyodide" not in out,
          "error: status bad, traceback gives script line 2, no Pyodide internals:\n" + out)
    page.locator(".pyrun").screenshot(path=str(S / "shots" / "pyrun_error.png"))
    # edits persist across a reload; Reset restores the original
    page.reload(); page.wait_for_selector(".pyrun [data-pyrun]")
    check(page.locator(".pyrun .pyedit").input_value() == "x = 1\ny = x / 0\n", "edit kept after reload")
    page.locator(".pyrun [data-pyreset]").click()
    check(page.locator(".pyrun .pyedit").input_value().startswith("# Stresses at a point"), "Reset script restores the original")
    check(page.locator(".pyrun [data-pyreset]").is_disabled(), "Reset disabled when unchanged")
    # auto-indent after a colon
    ed = page.locator(".pyrun .pyedit"); ed.fill(""); ed.click()
    page.keyboard.type("for i in range(3):"); page.keyboard.press("Enter"); page.keyboard.type("print(i * i)")
    check(ed.input_value() == "for i in range(3):\n    print(i * i)", "auto-indent after colon: " + repr(ed.input_value()))
    page.keyboard.press("Control+Enter"); wait_done(page)
    check(page.locator(".pyrun .pyout").inner_text().split() == ["0", "1", "4"], "Ctrl+Enter runs; output 0 1 4")
    # Stop ends a runaway loop; the next run starts Python again
    ed.fill("while True:\n    pass\n")
    page.locator(".pyrun [data-pyrun]").click()
    page.wait_for_function("() => /Running/.test(document.querySelector('.pyrun .pystat').textContent)", timeout=60000)
    time.sleep(1.5)
    check(page.locator(".pyrun [data-pystop]").is_visible(), "Stop visible while running")
    page.locator(".pyrun [data-pystop]").click()
    check("Stopped" in page.locator(".pyrun .pystat").inner_text() and page.locator(".pyrun [data-pyrun]").is_enabled(), "Stop ends the run")
    ed.fill("print('again')\n"); page.locator(".pyrun [data-pyrun]").click(); t = wait_done(page)
    check(page.locator(".pyrun .pyout").inner_text().strip() == "again", f"run after Stop works ({t:.1f} s)")
    # language: the status follows BM
    page.locator("#btn-lang").click()
    page.locator(".pyrun [data-pyrun]").click(); wait_done(page)
    check(page.locator(".pyrun .pystat").inner_text().startswith("Siap dalam"), "status in BM: " + page.locator(".pyrun .pystat").inner_text())
    page.locator("#btn-lang").click()
    page.evaluate("() => { for (const k of Object.keys(localStorage)) if (k.startsWith('seaa4243-py-')) localStorage.removeItem(k); }")

    # phone width, dark, largest text: no sideways scroll of the page
    for w in (320, 390):
        for ts in (1, 1.4):
            pg = ctx.new_page(); pg.set_viewport_size({"width": w, "height": 800})
            pg.goto(BASE + "05-plane-stress-3/index.html#lab-run"); pg.wait_for_selector(".pyrun [data-pyrun]")
            pg.evaluate(f"() => {{ document.documentElement.style.setProperty('--ts', '{ts}'); document.documentElement.setAttribute('data-theme', 'dark'); }}")
            if w == 390 and ts == 1:
                pg.locator(".pyrun [data-py]").nth(1).click(); pg.locator(".pyrun [data-pyrun]").click(); wait_done(pg)
                pg.locator(".pyrun").screenshot(path=str(S / "shots" / "pyrun_p5_phone_dark.png"))
            ov = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(ov <= 0, f"{w}px ts {ts}: page overflow {ov}px")
            pg.close()

    # the gate: another host shows the scripts but does not load Python
    pg = ctx.new_page()
    pg.add_init_script("delete window.SEAA_PYURL;")
    pg.goto(f"http://preview.test:{PORT}/SEAA4243-FEM/04-plane-stress-2/index.html#lab-run"); pg.wait_for_selector(".pyrun [data-pyrun]")
    pg.evaluate("() => { window.SEAA_PYURL = undefined; }")
    gate = pg.locator(".pyrun .pystat").inner_text()
    check(pg.locator(".pyrun [data-pyrun]").is_disabled() and "open this part there" in gate, "gate on another host: Run disabled, link shown: " + gate)
    href = pg.locator(".pyrun .pystat a").first.get_attribute("href")
    check(href == "https://razinutm.github.io/My_Lectures/SEAA4243-FEM/04-plane-stress-2/index.html#lab-run", "gate link: " + str(href))
    check(pg.locator(".pyrun .pyedit").input_value().startswith("# [k] = t"), "gate: scripts still readable")
    pg.close()

    # footers: copyright line on the home, the parts and the Explorers opened on their own
    for path in ["index.html"] + [s + "/index.html" for s in PARTS.values()] + [f"labs/{x}.html" for x in ("shape", "heat", "cant", "stress")]:
        pg = ctx.new_page(); pg.goto(BASE + path)
        sel = "#sitefoot" if path.startswith("labs") else "footer.foot p.copy"
        vis = pg.locator(sel).is_visible()
        txt = pg.locator(sel).inner_text() if vis else ""
        check(vis and txt.startswith("© 2026 Ahmad Razin Zainal Abidin") and "CC BY-NC-SA 4.0" in txt, f"footer on {path}")
        pg.close()
    # inside the part page's iframe the Explorer's own footer stays hidden
    page.goto(BASE + "04-plane-stress-2/index.html#lab"); page.wait_for_timeout(1500)
    fr = page.frame_locator("#labframe")
    check(not fr.locator("#sitefoot").is_visible(), "Explorer footer hidden inside the part page")

    check(not cdn, f"no CDN requests in the test ({len(cdn)})")
    check(not errs, "no page errors: " + "; ".join(errs[:3]))
    br.close()

print("\n".join(notes))
print("timings (s):", timings)
print("\n".join(fails) if fails else "ALL PASS")
print(f"{len(notes)} passed, {len(fails)} failed")
srv.shutdown()
sys.exit(1 if fails else 0)
