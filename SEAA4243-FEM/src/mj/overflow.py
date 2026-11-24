import json, sys, pathlib
from playwright.sync_api import sync_playwright
JS = """() => {
  const out = [];
  for (const s of document.querySelectorAll('section')) {
    const r0 = s.getBoundingClientRect(); let maxB = 0, maxR = 0, who = '';
    for (const e of s.querySelectorAll('*')) {
      if (getComputedStyle(e).position === 'absolute') continue;
      let p = e.parentElement, abs = false; while (p && p !== s) { if (getComputedStyle(p).position === 'absolute') { abs = true; break; } p = p.parentElement; }
      if (abs) continue;
      const r = e.getBoundingClientRect(); if (r.width === 0 && r.height === 0) continue;
      const b = r.bottom - r0.top, rr = r.right - r0.left;
      if (b > maxB) { maxB = b; who = e.tagName + ':' + (e.textContent || e.getAttribute('alt') || '').slice(0, 40); }
      if (rr > maxR) maxR = rr;
    }
    out.push([s.id, Math.round(maxB), Math.round(maxR), who]);
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for root in sys.argv[1:]:
        root = pathlib.Path(root).resolve(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        pg.goto('file://' + str(root / '_preview.html')); pg.wait_for_timeout(400)
        res = pg.evaluate(JS); bad = [r for r in res if r[1] > 932 or r[2] > 1794]
        print(root.name, 'slides', len(res), 'overflowing', len(bad))
        for r in bad: print('   ', r)
        pg.close()
    b.close()
