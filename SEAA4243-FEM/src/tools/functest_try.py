"""Functional test of the "Try it yourself" boxes (Notes -> Explorer task -> back to the same box).

    python3 functest_try.py                       all six parts, at 1400 px and 400 px
    python3 functest_try.py 03-plane-stress-1     one part

For every part and both widths: every Explorer task sits in exactly one box, the box text is the task card's
text, and every "Open in the Explorer" button opens the Explorer view, leaves the Lab on the tab the task
names ("Tab N" in the task text; the SEAA 4243 Explorers have no tabs, so the test checks that there is
nothing to set and nothing was set), marks the task card, and shows the bar that leads back to the same box.
Also: the tick of a finished task, the route #notes-try-<section>, Malay, print, and no page errors.
"""
import http.server, pathlib, re, socketserver, sys, threading
from playwright.sync_api import sync_playwright

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
PARTS = sys.argv[1:] or sorted(p.name for p in SITE.glob("0*-*") if (p / "index.html").exists())
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

INFO = """() => { const T = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : '';
  return { cards: [...document.querySelectorAll('#v-lab .tk[data-ms]')].map(c => ({ id: c.getAttribute('data-ms'), n: T(c.querySelector('.tkn')), en: T(c.querySelector('h4 .en')), ms: T(c.querySelector('h4 .ms')) })),
    boxes: [...document.querySelectorAll('#v-notes aside.try')].map(x => { const sec = x.closest('section.nsec'), h = sec.querySelector('h2');
      return { id: x.id, hidden: x.hidden, sec: sec.id, next: x.nextElementSibling ? x.nextElementSibling.className : '', h2: T(h.querySelector('.en')), no: (/^\\s*(\\d+)\\./.exec(h.textContent) || [])[1],
        items: [...x.querySelectorAll('li[data-ms]')].map(li => ({ id: li.getAttribute('data-ms'), n: T(li.querySelector('.tkn')), en: T(li.querySelector('.tt .en')), ms: T(li.querySelector('.tt .ms')), btn: !!li.querySelector('button[data-try]') })) }; }) }; }"""
OPENED = """() => { const q = s => document.querySelector(s), vis = e => !!e && !e.hidden && e.getClientRects().length > 0;
  const bar = q('#v-lab .tryback'), nav = q('.navwrap'), lf = q('#labframe'), g = q('#v-lab .labgrid');
  let tabs = -1, lhash = null; try { tabs = lf.contentWindow.document.querySelectorAll('button.tab[data-tab]').length; lhash = lf.contentWindow.location.hash; } catch (e) {}
  return { view: (q('.view:not([hidden])') || {}).id, tab: (q('.tab[aria-selected="true"]') || {}).id, hash: location.hash,
    bar: vis(bar), barText: bar ? bar.innerText.replace(/\\s+/g, ' ') : '', barTop: bar ? bar.getBoundingClientRect().top : null, barH: bar ? bar.offsetHeight : 0,
    navBottom: nav ? nav.getBoundingClientRect().bottom : 0, gridTop: g ? g.getBoundingClientRect().top : null,
    flashed: [...document.querySelectorAll('.hflash')].map(e => e.id || e.getAttribute('data-ms')), labTabs: tabs, labHash: lhash, labSrc: lf ? lf.getAttribute('src') : null, vh: innerHeight }; }"""
# resolves when the page has stopped scrolling (a smooth scroll over a long page takes more than a second)
SETTLE = "() => new Promise(done => { let y = scrollY, n = 0; const t = setInterval(() => { if (scrollY === y) { if (++n >= 4) { clearInterval(t); done(scrollY); } } else { y = scrollY; n = 0; } }, 70); })"
BACK = """id => { const x = document.getElementById(id), rc = x.getBoundingClientRect();
  return { view: (document.querySelector('.view:not([hidden])') || {}).id, hash: location.hash, top: rc.top, vh: innerHeight,
    barHidden: document.querySelector('#v-lab .tryback').hidden, nav: document.querySelector('.navwrap').getBoundingClientRect().bottom }; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for width, height in ((1400, 900), (400, 800)):
        for slug in PARTS:
            ctx = b.new_context(viewport={"width": width, "height": height}); pg = ctx.new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            # nothing leaves the machine: the font sheet is served empty, every other outside request is refused
            pg.route(lambda u: not u.startswith(BASE), lambda r: r.fulfill(status=200, content_type="text/css", body="") if "fonts.googleapis" in r.request.url else r.abort())
            tag = f"{slug} @{width}"
            pg.goto(BASE + slug + "/index.html#notes"); pg.wait_for_timeout(700)
            info = pg.evaluate(INFO)
            cards = {c["id"]: c for c in info["cards"]}
            placed = [i["id"] for x in info["boxes"] for i in x["items"]]
            check(len(cards) >= 4 and sorted(placed) == sorted(cards), f"{tag}: every Explorer task in exactly one box ({len(placed)} placed, {len(cards)} tasks)")
            check(all(not x["hidden"] and x["id"] == "try-" + x["sec"] and x["next"] == "kp" for x in info["boxes"]), f"{tag}: boxes shown, id try-<section>, just before Key points")
            check(all(i["btn"] and i["en"] == cards[i["id"]]["en"] and i["ms"] == cards[i["id"]]["ms"] and i["n"] == cards[i["id"]]["n"] for x in info["boxes"] for i in x["items"]),
                  f"{tag}: box text and number are the task card's")
            check(pg.evaluate("document.documentElement.scrollWidth - innerWidth") <= 0, f"{tag}: no sideways scroll in Notes")
            for x in info["boxes"]:
                for it in x["items"]:
                    t = f"{tag} {x['id']}/{it['id']}"
                    pg.evaluate("window.RZ.show('notes')"); pg.wait_for_timeout(120)
                    btn = pg.locator(f'#{x["id"]} button[data-try="{it["id"]}"]'); btn.scroll_into_view_if_needed(); btn.click()
                    pg.wait_for_function("id => { const c = document.querySelector('#v-lab .tk[data-ms=\"' + id + '\"]'); return !!c && c.classList.contains('hflash'); }", arg=it["id"], timeout=4000)
                    pg.evaluate(SETTLE); s = pg.evaluate(OPENED)        # the mark lasts 2.4 s, longer than the scroll
                    check(s["view"] == "v-lab" and s["tab"] == "t-lab" and s["hash"] == "#lab", f"{t}: opens the Explorer view")
                    check(s["flashed"] == [it["id"]], f"{t}: marks this task card only ({s['flashed']})")
                    want = f"← Back to Notes §{x['no']} · {x['h2']}"
                    check(s["bar"] and s["barText"].startswith(want) and f"Task {it['n']} is marked" in s["barText"], f"{t}: back bar reads {want!r} (got {s['barText'][:80]!r})")
                    check(s["barTop"] is not None and s["navBottom"] - 1 <= s["barTop"] < s["vh"] / 2, f"{t}: back bar under the tab bar (bar {s['barTop']}, tab bar ends {s['navBottom']})")
                    # the bar may cover the frame's top edge by a few px: the scroll allows 16 px under the tab bar, the bar sits at --rz-top + 4
                    check(s["gridTop"] is not None and s["barTop"] + s["barH"] - 8 <= s["gridTop"] < s["vh"] * 0.6, f"{t}: scrolled to the Explorer (top {s['gridTop']:.0f}, bar ends {s['barTop'] + s['barH']:.0f})")
                    named = re.match(r"\s*Tab\s+(\d+)", cards[it["id"]]["en"])
                    check(named is None and s["labTabs"] == 0 and s["labHash"] == "", f"{t}: Lab tab: task names {named and named.group(1)}, {s['labSrc']} has {s['labTabs']} tabs, hash {s['labHash']!r}")
                    pg.click("#v-lab .tryback button"); pg.wait_for_timeout(350)
                    marked = pg.evaluate("id => document.getElementById(id).classList.contains('hflash')", x["id"])
                    pg.evaluate(SETTLE); r = pg.evaluate(BACK, x["id"])
                    check(r["view"] == "v-notes" and r["hash"] == "#notes-" + x["id"] and r["barHidden"], f"{t}: back opens Notes at #notes-{x['id']}, bar gone")
                    check(marked and r["nav"] - 2 <= r["top"] < r["vh"] * 0.6, f"{t}: back lands on the box and marks it (top {r['top']:.0f}, tab bar ends {r['nav']:.0f})")
                    pg.wait_for_timeout(300)
            first = info["boxes"][0]; fid, tid = first["id"], first["items"][0]["id"]
            # leaving the Explorer by a tab clears the way back
            pg.evaluate("window.RZ.show('notes')"); pg.locator(f"#{fid} button[data-try]").first.click(); pg.wait_for_timeout(300)
            pg.evaluate("document.getElementById('t-slides').click()"); pg.wait_for_timeout(150); pg.evaluate("document.getElementById('t-lab').click()"); pg.wait_for_timeout(150)
            check(pg.evaluate("document.querySelector('#v-lab .tryback').hidden"), f"{tag}: leaving the Explorer by a tab clears the back bar")
            # a finished task is ticked in its box too (the card's own "mark done", which runs the same sync as the Lab's message)
            tick = "id => { const li = document.querySelector('#v-notes .try li[data-ms=\"' + id + '\"]'); return li.classList.contains('done') && getComputedStyle(li.querySelector('.tkok')).visibility === 'visible'; }"
            before = pg.evaluate(tick, tid)
            pg.evaluate("id => document.querySelector('#v-lab .tk[data-ms=\"' + id + '\"] .tkself').click()", tid); pg.wait_for_timeout(150)
            check(not before and pg.evaluate(tick, tid), f"{tag}: task {tid} done -> ticked in its box")
            # Malay
            pg.evaluate("window.RZ.show('notes')"); pg.click("#btn-lang"); pg.wait_for_timeout(150)
            ms = pg.evaluate("id => document.getElementById(id).innerText", fid)
            check("CUBA SENDIRI" in ms.upper() and "Buka dalam Explorer →" in ms and "Open in the Explorer" not in ms, f"{tag}: box in Malay")
            pg.locator(f"#{fid} button[data-try]").first.click(); pg.wait_for_timeout(300)
            check(pg.evaluate("document.querySelector('#v-lab .tryback').innerText").startswith("← Kembali ke Nota §"), f"{tag}: back bar in Malay")
            pg.click("#v-lab .tryback button"); pg.wait_for_timeout(200); pg.click("#btn-lang")
            # the route to a box, and print
            pg.goto(BASE + slug + "/index.html#notes-" + fid); pg.reload(); pg.wait_for_timeout(500); pg.evaluate(SETTLE)
            rt = pg.evaluate("id => ({ view: document.querySelector('.view:not([hidden])').id, top: document.getElementById(id).getBoundingClientRect().top, vh: innerHeight })", fid)
            check(rt["view"] == "v-notes" and 0 <= rt["top"] < rt["vh"] * 0.6, f"{tag}: #notes-{fid} opens the notes at the box (top {rt['top']:.0f})")
            pg.emulate_media(media="print")
            check(pg.evaluate("id => getComputedStyle(document.getElementById(id)).display", fid) == "none", f"{tag}: boxes hidden in print")
            check(not errs, f"{tag}: no page errors {errs[:2]}")
            print(f"{tag}: {len(info['boxes'])} boxes, {len(placed)} buttons, done")
            ctx.close()
    b.close()
print(f"\n{npass} checks passed, {len(fails)} failed"); sys.exit(1 if fails else 0)
