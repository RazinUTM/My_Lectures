#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Build index.html, the Unit 1 page, from web/src and the course's shared engine.

What: joins web/src/p*.html (the page body, in file-name order); renders every display equation
(div.eqwrap[data-tex]) to SVG with web/tex2svg.js and keeps its LaTeX in data-tex; gives every image in
img/ its width and height; builds window.COURSE (the manifest the engine counts, routes and searches
with) from the page itself and slides/deck.html; and writes one self-contained index.html in this topic
folder: the preferences script that runs before first paint, the fonts, ../shared/course.css,
the body, window.COURSE, ../shared/course.js and web/src/exercises.js, all inline.

How to call it, from this topic folder (build.sh runs it, then web/add_tutor.py for Dr RJ):
  python3 web/build_page.py
Needs Pillow and beautifulsoup4 (Python) and Node with mathjax-full (npm ci --prefix web).

Why it is like this: the page must work for years from GitHub Pages and in a lecture hall with poor
Wi-Fi, so nothing is fetched at run time except the fonts (with system fallbacks), the slide deck and the
Explorer; and a manifest typed by hand drifts from the page within a week, so it is generated.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent            # web/
topic = here.parent                               # 01-staircases-1/
course = topic.parent                             # SEAA4333-RCD2/

TITLE = "SEAA 4333 · Unit 1 · Staircases I"
DESCRIPTION = ("SEAA 4333 Reinforced Concrete Design II, Unit 1: stair geometry by the by-laws, load on plan, "
               "the stair as a beam on plan, and the design and detailing of the waist. Notes, slides, model "
               "answers, exercises and the Staircase Lab.")
PREFS_KEY = "seaa4333-prefs"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500;600'
         '&family=Archivo:wght@700;800&family=Atkinson+Hyperlegible:wght@400;700&display=swap">')
# Preferences (language, theme, text size, folded description) applied before first paint: rz-settings-buttons.
PREFS = ('<script>(function(){try{var r=document.documentElement,p=JSON.parse(localStorage.getItem("' + PREFS_KEY + '")||"null")||{};'
         'if(p.lang==="ms"){r.setAttribute("data-lang","ms");r.lang="ms"}'
         'if(p.theme==="light"||p.theme==="dark")r.setAttribute("data-theme",p.theme);'
         'var f=+p.font||1;r.style.setProperty("--font-scale",String(f));r.style.setProperty("--ts",String(f));'
         'if(p.fold)r.classList.add("subfold")}catch(e){}})();</script>')
EX_PX = 9.0          # px per ex for the equation SVGs (about 20 px per em: a little larger than the reading text)

# Screen guide (ⓘ): [selector, title EN, title MS, what it does EN, MS], in tour order.
REGIONS = [
    [".crumbs", "Where you are", "Di mana anda berada", "The way back: For My Students, My Lectures, the SEAA 4333 course home, this Unit.", "Jalan kembali: For My Students, My Lectures, laman kursus SEAA 4333, Unit ini."],
    ["#hcontact", "Your lecturer", "Pensyarah anda", "Questions about the course go to this email.", "Soalan tentang kursus dihantar ke e-mel ini."],
    [".htitle", "This Unit", "Unit ini", "The title and what the Unit covers. The arrow folds the description away.", "Tajuk dan apa yang Unit ini liputi. Anak panah melipat penerangan."],
    ["#hsearch", "Search", "Carian", "Finds sections, slides, examples, exercises, Explorer tasks and glossary terms on this page. Press / to jump here.", "Mencari seksyen, slide, contoh, latihan, tugasan Explorer dan istilah glosari dalam halaman ini. Tekan / untuk terus ke sini."],
    ["#snbtn", "Short notes", "Nota ringkas", "The formulas and rules of the Unit on one sheet, for revision.", "Formula dan peraturan Unit pada satu helaian, untuk ulang kaji."],
    [".prefs", "Settings", "Tetapan", "Language (BM/EN), light or dark theme, text size (AA), and this guide. The choice is kept for every Unit of the course.", "Bahasa (BM/EN), tema cerah atau gelap, saiz teks (AA), dan panduan ini. Pilihan disimpan untuk setiap Unit kursus."],
    [".navrow", "Tabs", "Tab", "Start, Notes, Slides, Examples, Exercises, Explorer and Glossary. A badge shows done out of total.", "Mula, Nota, Slides, Contoh, Latihan, Explorer dan Glosari. Lencana menunjukkan selesai daripada jumlah."],
    [".prog", "Progress", "Kemajuan", "The mean over the tabs that count. It is your own record, kept in this browser, not a gradebook.", "Purata tab yang dikira. Ia rekod anda sendiri, disimpan dalam pelayar ini, bukan buku gred."],
    ["main", "Contents", "Kandungan", "The tab you chose. On Start, the plan shows what to do before, in and after class.", "Tab yang anda pilih. Di Mula, pelan menunjukkan apa perlu dibuat sebelum, semasa dan selepas kelas."],
    ["#rzguide", "Dr RJ, your guide", "Dr RJ, panduan anda", "Ask a question in your own words; Dr RJ points to the matching sections of this page. Nothing you type leaves your browser.", "Tanya soalan dengan perkataan anda sendiri; Dr RJ menunjukkan bahagian yang berkaitan dalam halaman ini. Tiada apa yang anda taip keluar dari pelayar anda."],
    ["footer.foot", "Credits and licence", "Kredit dan lesen", "Who made the page, what you may reuse, and what stays in your browser.", "Siapa yang menghasilkan halaman ini, apa yang boleh digunakan semula, dan apa yang kekal dalam pelayar anda."],
]


def render_equations(soup: BeautifulSoup) -> dict:
    """Render every div.eqwrap[data-tex] with MathJax; the wrapper gets a placeholder that main() swaps for
    the SVG after the page is serialised (so the SVG never passes through an HTML parser that lowercases
    viewBox). Returns {placeholder: svg}."""
    wraps = soup.select("div.eqwrap[data-tex]")
    jobs, seen = [], {}
    for w in wraps:
        key = w.get("data-eq") or "eq"
        seen[key] = seen.get(key, 0) + 1
        uid = key if seen[key] == 1 else f"{key}{seen[key]}"
        w["data-eq"] = uid
        jobs.append({"id": uid, "tex": w["data-tex"]})
    if not jobs:
        return {}
    res = subprocess.run(["node", str(here / "tex2svg.js")], input=json.dumps(jobs), capture_output=True, text=True, cwd=here)
    if res.returncode:
        sys.exit("tex2svg.js failed:\n" + res.stderr)
    svgs, out = json.loads(res.stdout), {}
    for w in wraps:
        svg = svgs[w["data-eq"]]
        m_w, m_h = re.search(r'width="([\d.]+)ex"', svg), re.search(r'height="([\d.]+)ex"', svg)
        wpx, hpx = round(float(m_w.group(1)) * EX_PX), round(float(m_h.group(1)) * EX_PX)
        label = html.escape(w["data-tex"], quote=True)
        svg = re.sub(r'^<svg style="[^"]*"', f'<svg style="min-width:{round(wpx * 0.62)}px"', svg)
        svg = svg.replace(f'width="{m_w.group(1)}ex"', f'width="{wpx}"', 1).replace(f'height="{m_h.group(1)}ex"', f'height="{hpx}"', 1)
        svg = svg.replace('role="img"', f'role="img" aria-label="{label}"', 1)
        w["style"] = f"width:{wpx}px"
        token = f"@@EQ:{w['data-eq']}@@"
        w.clear()
        w.string = token
        out[token] = svg
    return out


def size_images(soup: BeautifulSoup) -> int:
    """Width and height on every figure (no layout shift), and a link to the full-size image: on a phone a
    1400 px figure is drawn 350 px wide, so a tap opens it in its own tab to zoom."""
    n = 0
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("img/") and not img.get("width"):
            w, h = Image.open(topic / src).size
            img["width"], img["height"] = str(w), str(h)
            n += 1
        if src.startswith("img/") and img.parent.name == "div" and "paper" in img.parent.get("class", []):
            a = soup.new_tag("a", href=src, target="_blank", rel="noopener")
            img.wrap(a)
    return n


def manifest(soup: BeautifulSoup) -> dict:
    deck = BeautifulSoup((topic / "slides" / "deck.html").read_text(encoding="utf-8"), "html.parser")
    titles = [d.get("data-title", "") for d in deck.select("div.sl")]
    return {
        "part": 1, "prefix": "seaa4333", "key": "seaa4333-u1-v1", "prefs": PREFS_KEY, "lang": "en",
        "notes": [s["id"] for s in soup.select("#v-notes section.nsec")],
        "slides": len(titles), "slideTitles": titles,
        "examples": [s["id"] for s in soup.select("#v-examples section.xsec")],
        "lab": {"id": "staircase", "milestones": [{"id": t["data-ms"]} for t in soup.select("#v-lab .tk[data-ms]")]},
        "cando": len(soup.select(".cando .row")), "targetMin": 45,
        "avatarBase": "../shared/avatar/",
        "regions": REGIONS,
    }


def main() -> int:
    body_src = "".join(p.read_text(encoding="utf-8") for p in sorted((here / "src").glob("p*.html")))
    soup = BeautifulSoup(body_src, "html.parser")
    eqs = render_equations(soup)
    n_img = size_images(soup)
    meta = manifest(soup)
    deck_n = meta["slides"]
    for node in soup.select("#svscrub"):            # the slide slider and counter start at the right length
        node["max"] = str(deck_n)
    body = str(soup)
    for token, svg in eqs.items():
        assert body.count(token) == 1, token
        body = body.replace(token, svg)
    css = (course / "shared" / "course.css").read_text(encoding="utf-8")
    js = (course / "shared" / "course.js").read_text(encoding="utf-8")
    ex = (here / "src" / "exercises.js").read_text(encoding="utf-8")
    conf = json.dumps(meta, ensure_ascii=False).replace("</", "<\\/")
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           f"<title>{TITLE}</title>\n"
           '<meta name="claude:viewport-fit-sides" content="cover">\n'
           f'<meta name="description" content="{html.escape(DESCRIPTION, quote=True)}">\n'
           + PREFS + "\n" + FONTS + "\n<style>\n" + css + "</style>\n</head>\n<body>\n"
           + body + f"\n<script>window.COURSE = {conf};</script>\n<script>\n{js}</script>\n<script>\n{ex}</script>\n</body>\n</html>\n")
    (topic / "index.html").write_text(doc, encoding="utf-8")
    print(f"index.html: {len(doc):,} bytes; {len(eqs)} equations as SVG, {n_img} images sized, "
          f"{len(meta['notes'])} notes sections, {deck_n} slides, {len(meta['examples'])} examples, "
          f"{len(meta['lab']['milestones'])} Explorer tasks, {meta['cando']} can-do rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
