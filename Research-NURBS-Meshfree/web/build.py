#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Build the NURBS-meshfree research primer: Part 1 page, its tutor files, and the guide panel with Dr RJ.

What: reads web/content_p1.py, renders its LaTeX to SVG (web/render_eq.cjs, MathJax), assembles
01-foundations/index.html as one self-contained file (shared/site.css and shared/site.js inlined, avatars by
relative path), writes the tutor files with the pinned rz-tutor-worker tools (01-foundations/tutor/*.json,
tutor/course.json), then adds the guide panel and the tutor widget. The Worker address comes from
shared/tutor_endpoint.txt; while it holds none, Dr RJ stays offline (scripted steps and section pointers; nothing
leaves the browser).
How to call it, from the primer folder:  (cd web && npm install)  once, then  python3 web/build.py
Needs Python 3.9+, beautifulsoup4 + lxml (for the manifest tool) and Node.js 18+.
Why it is like this: the page is generated, so the panel must come from the build or the next build would drop
Dr RJ; the manifest is generated from the page so that search, the guide and the tutor never drift from it.
"""
from __future__ import annotations

import html as H
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
WEB = Path(__file__).resolve().parent
ROOT = WEB.parent                       # Research-NURBS-Meshfree/
PART_DIR = ROOT / "01-foundations"
sys.path.insert(0, str(WEB))
import content_p1 as C  # noqa: E402

B = C.B
M = C.META


def render_equations() -> dict:
    with tempfile.TemporaryDirectory() as td:
        src, out = Path(td) / "eq.json", Path(td) / "svg.json"
        src.write_text(json.dumps(C.EQS))
        subprocess.run(["node", str(WEB / "render_eq.cjs"), str(src), str(out)], check=True, cwd=WEB)
        return json.loads(out.read_text())


_EQ_SEEN: dict = {}


def fill_equations(s: str, svgs: dict) -> str:
    """Replace each %%EQ:id:label%% with its SVG. An equation shown twice (notes and slides) gets a fresh glyph-id
    prefix on its second showing, because the SVG carries its own glyph definitions and ids must be unique."""
    seen = _EQ_SEEN                      # shared across calls: notes and slides are filled separately

    def rep(m):
        eid, label = m.group(1), m.group(2)
        seen[eid] = seen.get(eid, 0) + 1
        svg = svgs[eid] if seen[eid] == 1 else svgs[eid].replace(f"{eid}-MJX-", f"{eid}-{seen[eid]}-MJX-")
        tex = H.escape(C.EQS[eid], quote=True)
        lbl = f'<span class="lbl">({label})</span>' if label else ""
        return f'<div class="eqrow"><div class="eqwrap" data-eq="{eid}" data-tex="{tex}">{svg}</div>{lbl}</div>'
    return re.sub(r"%%EQ:([A-Za-z0-9_]+):([0-9.]*)%%", rep, s)


def nobreak(text):
    """Wrap hyphenated words (B-splines, B-spline) in a no-wrap span so a heading never breaks at the hyphen."""
    return re.sub(r"\b([A-Za-z]+-[A-Za-z]+)\b", r'<span class="nw">\1</span>', text)


def vhead(pose, title_en, title_ms, todo_en, todo_ms, counts_en="", counts_ms="", extra=""):
    c = f'<p class="counts">{B("<b>Counts toward progress:</b> " + counts_en, "<b>Dikira dalam kemajuan:</b> " + counts_ms)}</p>' if counts_en else ""
    return (f'<div class="vhead"><img class="vava" src="../shared/avatar/{pose}.webp" alt="" title="Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin" '
            f'width="72" height="128" decoding="async" loading="lazy"><div class="vtxt"><h2>{B(title_en, title_ms)}</h2>'
            f'<p class="todo">{B("<b>What to do</b> " + todo_en, "<b>Apa yang perlu dibuat</b> " + todo_ms)}</p>{c}</div>{extra}</div>')


def view_start() -> str:
    S = C.START
    stages = []
    for key, (t_en, t_ms) in [("before", ("Before the meeting", "Sebelum perjumpaan")), ("in", ("In the meeting", "Dalam perjumpaan")), ("after", ("After the meeting", "Selepas perjumpaan"))]:
        st = S["plan"][key]
        em = st.get("label") or f"≈ {st['min']} min"
        lis = []
        for cond, goto, en, ms in st["items"]:
            if cond:
                v = goto.split("/")
                href = "#" + v[0] + ("-" + v[1] if len(v) > 1 else "")
                lis.append(f'<li data-stage-item="{cond}"><a href="{href}" data-goto="{goto}">{B(en, ms)}</a></li>')
            else:
                lis.append(f'<li class="untracked">{B(en, ms)}</li>')
        stages.append(f'<div class="stage" data-stage="{key}"><b>{B(t_en, t_ms)}</b><em>{em}</em><ul>{"".join(lis)}</ul><span class="st"></span></div>')
    plan = (f'<div class="card" id="plan"><h2>{B("Your plan", "Pelan anda")}</h2><div class="stages">{"".join(stages)}</div>'
            f'<p class="legend">{B("○ to do · ✓ done · – done in the meeting, not tracked. Click an item to go to it.", "○ belum · ✓ selesai · – dibuat dalam perjumpaan, tidak dijejak. Klik item untuk pergi kepadanya.")}</p>'
            f'<div class="contline"><button class="btn" id="contbtn" type="button" data-goto="notes/n1">{B("Continue", "Teruskan")}</button></div></div>')
    lo = "".join(f"<li>{B(en, ms)}</li>" for en, ms in S["outcomes"])
    covers = (f'<div class="card"><h2>{B("What this part covers", "Apa yang dirangkumi bahagian ini")}</h2><p>{S["covers"]}</p>'
              f'<h3>{B("After this part you should be able to", "Selepas bahagian ini anda sepatutnya boleh")}</h3><ol class="lo">{lo}</ol><p class="muted">{S["reference"]}</p></div>')
    recall = "".join(f'<details class="recall" id="{rid}" data-recall="{rid}"><summary>{B(*q)}</summary><p>{B(*a)}</p></details>' for rid, q, a in S["recall"])
    lv = [("no", "Not yet", "Belum"), ("partly", "Partly", "Sebahagian"), ("yes", "Confident", "Yakin")]
    cando = "".join(f'<div class="cdrow" data-cd="c{i + 1}"><span>{B(en, ms)}</span><span class="lv">'
                    + "".join(f'<button type="button" data-lv="{k}" aria-pressed="false">{B(a, b)}</button>' for k, a, b in lv) + "</span></div>"
                    for i, (en, ms) in enumerate(S["cando"]))
    files = (f'<div class="card files" id="files"><h2>{B("Files and settings", "Fail dan tetapan")}</h2>'
             f'<p>{B("Progress is your own record, kept in this browser only; it is not a gradebook. Export it to move to another device.", "Kemajuan ialah rekod anda sendiri, disimpan dalam pelayar ini sahaja; ia bukan buku markah. Eksport untuk berpindah ke peranti lain.")}</p>'
             f'<button class="btn ghost" id="exportbtn" type="button">⤓ {B("Export progress", "Eksport kemajuan")}</button>'
             f'<label class="btn ghost">⤒ {B("Import progress", "Import kemajuan")}<input type="file" id="importfile" accept="application/json" hidden></label>'
             f'<button class="btn ghost" id="resetbtn" type="button">{B("Reset progress", "Set semula kemajuan")}</button><p id="filemsg" role="status"></p>'
             f'<p>{B("Companion code: ", "Kod pengiring: ")}<a href="../code/nmf_bspline_rk.py" download>nmf_bspline_rk.py</a> '
             f'{B("(Python 3 + numpy; prints the numbers of Examples 1–3).", "(Python 3 + numpy; mencetak nombor Contoh 1–3).")}</p></div>')
    return ('<section class="view" data-view="start" id="v-start" role="tabpanel" aria-labelledby="t-start">'
            + vhead("welcome", "Start", "Mula", "Follow the plan: before the meeting, in the meeting, after it. Each item links to where it is done and ticks itself when it is. Continue takes you to the first thing not yet done.",
                    "Ikut pelan: sebelum perjumpaan, dalam perjumpaan, selepasnya. Setiap item dipautkan ke tempat ia dibuat dan ditanda sendiri apabila selesai. Teruskan membawa anda ke perkara pertama yang belum selesai.",
                    "the bar averages six parts equally: Notes, Slides, Examples, Exercises, Explorer and the can-do checklist.",
                    "bar ini mempuratakan enam bahagian sama rata: Nota, Slides, Contoh, Latihan, Explorer dan senarai semak boleh-buat.")
            + f'<p class="who">{S["who"]}</p><div class="start-hero">{plan}{covers}</div>'
            + f'<div class="grid2"><div class="card" id="recall"><h2>{B("Recall questions", "Soalan imbas kembali")}</h2><p class="muted">{B("Answer in your head first, then open.", "Jawab dalam kepala dahulu, kemudian buka.")}</p>{recall}</div>'
            + f'<div class="card cando" id="cando"><h2>{B("Can-do checklist", "Senarai semak boleh-buat")}</h2>{cando}</div></div>{files}</section>')


def view_notes(svgs) -> str:
    toc = "".join(f'<li><a href="#notes-{n["id"]}" data-goto="notes/{n["id"]}" data-toc="{n["id"]}">{i + 1}. {B(*n["title"])}</a></li>' for i, n in enumerate(C.NOTES))
    total = sum(n["min"] for n in C.NOTES)
    secs = []
    for i, n in enumerate(C.NOTES):
        body = fill_equations(n["html"], svgs)
        secs.append(f'<section class="nsec" id="{n["id"]}"><h2>{i + 1}. {B(*n["title"])}</h2><div class="readtime">≈ {n["min"]} min</div>{body}'
                    f'<div class="sfoot"><label class="readck"><input type="checkbox"><span class="rk-todo">{B("Mark this section as read", "Tanda seksyen ini sudah dibaca")}</span>'
                    f'<span class="rk-done">{B("Read ✓ — untick to review again", "Sudah dibaca ✓ — nyahtanda untuk ulang")}</span></label></div></section>')
    return ('<section class="view" data-view="notes" id="v-notes" role="tabpanel" aria-labelledby="t-notes" hidden>'
            + vhead("present", "Notes", "Nota", "Read each section, try its quick check, and mark it as read. Key points only gives the summary of every section.",
                    "Baca setiap seksyen, cuba semak cepatnya, dan tandakan sudah dibaca. Perkara utama sahaja memberi ringkasan setiap seksyen.", "sections marked as read.", "seksyen yang ditanda sudah dibaca.")
            + f'<div class="notes"><aside class="toc"><div class="eyebrow">{B("Sections", "Seksyen")}</div><ol>{toc}</ol><div class="rt">≈ {total} min · ✓ = {B("read", "dibaca")}</div></aside>'
            + f'<div><div class="ntools"><button class="btn ghost" id="kpmode" type="button" aria-pressed="false">{B("Key points only", "Perkara utama sahaja")}</button></div>'
            + f'<div class="article">{"".join(secs)}</div></div></div></section>')


def view_slides(svgs) -> str:
    n = len(C.SLIDES)
    sl = []
    for i, (t_en, t_ms, body) in enumerate(C.SLIDES):
        sl.append(f'<section class="slide" id="slide-{i + 1}" aria-label="Slide {i + 1}"><h2>{B(t_en, t_ms)}</h2>{fill_equations(body, svgs)}'
                  f'<div class="sfootline"><span>© 2026 Ahmad Razin Zainal Abidin · {B("NURBS–meshfree primer, Part 1", "Primer NURBS–meshfree, Bahagian 1")}</span><span>{i + 1} / {n}</span></div></section>')
    btn = lambda k, lab, aria: f'<button class="btn ghost" type="button" data-sl="{k}" aria-label="{aria}">{lab}</button>'
    return ('<section class="view" data-view="slides" id="v-slides" role="tabpanel" aria-labelledby="t-slides" hidden>'
            + vhead("explain", "Slides", "Slides", "Page through the slides with the buttons, the slider, ← → or a swipe. Every slide you open is counted.",
                    "Selak slides dengan butang, slider, ← → atau swipe. Setiap slide yang dibuka dikira.", "slides viewed.", "slides yang telah dilihat.")
            + f'<div class="sv"><div class="sframe" tabindex="0" role="group" aria-roledescription="slide viewer" aria-label="Slides: use the arrow keys"><div class="stage16">{"".join(sl)}</div></div><div class="slidebar">'
            + btn("first", "⏮", "First slide") + btn("prev", "◀", "Previous slide") + f'<span class="count" id="scount">1 / {n}</span>' + btn("next", "▶", "Next slide") + btn("last", "⏭", "Last slide")
            + f'<input type="range" id="srange" min="1" max="{n}" value="1" aria-label="Slide"><button class="btn ghost" type="button" id="sfull">⛶ {B("Full screen", "Skrin penuh")}</button></div></div></section>')


def view_examples() -> str:
    xs = []
    for x in C.EXAMPLES:
        steps = "".join(f'<div class="xstep"><h4><span class="xn">{B("Step", "Langkah")} {j + 1}</span> {B(*t)}</h4><div class="bd">{body}</div></div>' for j, (t, body) in enumerate(x["steps"]))
        xs.append(f'<section class="xsec" id="{x["id"]}"><div class="xhead"><h2>{B("Example " + x["id"][1:] + " · " + x["title"][0], "Contoh " + x["id"][1:] + " · " + x["title"][1])}</h2>'
                  f'<div class="xmeta"><span><b>{B("Type", "Jenis")}</b> {B(*x["meta"])}</span></div></div>'
                  f'<div class="xq"><span class="qlabel">{B("Question", "Soalan")}</span> {B(*x["q"])}</div><p class="plan"><b>{B("Plan.", "Pelan.")}</b> {B(*x["plan"])}</p>{steps}'
                  f'<button class="btn xnext" type="button"></button><button class="btn ghost xall" type="button">{B("Show all steps", "Tunjuk semua langkah")}</button>'
                  f'<p class="xdone" hidden>✓ {B("Example finished — try the exercise that follows it.", "Contoh selesai — cuba latihan yang mengikutinya.")}</p></section>')
    return ('<section class="view" data-view="examples" id="v-examples" role="tabpanel" aria-labelledby="t-examples" hidden>'
            + vhead("explain", "Examples", "Contoh", "Work each example on paper first, then reveal one step at a time and compare.",
                    "Selesaikan setiap contoh di atas kertas dahulu, kemudian buka satu langkah pada satu masa dan bandingkan.", "examples revealed to the end.", "contoh yang dibuka hingga ke hujung.")
            + f'<div class="xarticle">{"".join(xs)}</div></section>')


def view_exercises() -> str:
    arts = "".join(f'<article class="qx" data-ex="{e["id"]}" id="{e["id"]}"><header><h4>{e["id"][1:]} · {B(*e["title"])}</h4><span class="mk">{e["marks"]} {B("marks", "markah")}</span></header>'
                   f'<div class="exbody"><p>{e["stmt"]}</p></div><div class="exrun"></div></article>' for e in C.EXERCISES)
    quick = "".join(f'<div class="q"><p>{B(q_en, q_ms)}</p><button class="btn ghost" type="button" aria-expanded="false">{B("Answer", "Jawapan")}</button><p class="qa" hidden>{B(a_en, a_ms)}</p></div>' for q_en, q_ms, a_en, a_ms in C.QUICK)
    return ('<section class="view" data-view="exercises" id="v-exercises" role="tabpanel" aria-labelledby="t-exercises" hidden>'
            + vhead("tablet", "Exercises", "Latihan", "Every attempt has new numbers. Try first, then open the hints one by one; showing the solution switches checking off for those numbers.",
                    "Setiap cubaan ada nombor baharu. Cuba dahulu, kemudian buka petunjuk satu demi satu; menunjukkan penyelesaian menutup semakan untuk nombor itu.", "exercises checked correct.", "latihan yang disemak betul.")
            + f'<div class="card">{arts}</div><div class="card" style="margin-top:16px"><h2>{B("Quick concept questions", "Soalan konsep pantas")}</h2>{quick}</div></section>')


def view_lab() -> str:
    L = C.LAB
    tasks = "".join(f'<div class="tk" data-ms="{m}"><header><h4><span class="tkn">{i + 1}</span>{B(*t)}</h4><label class="tkmark"><input type="checkbox" class="tkck"> {B("done", "selesai")}</label></header>'
                    f'<p class="tkans">{B(*a)}</p></div>' for i, (m, t, a) in enumerate(L["tasks"]))
    return ('<section class="view" data-view="lab" id="v-lab" role="tabpanel" aria-labelledby="t-lab" hidden>'
            + vhead("ok", "Explorer", "Explorer", "Work in the B-spline and RK Explorer (on a phone, open it in its own tab). Each task ticks itself when the Explorer sees it done.",
                    "Bekerja dalam B-spline and RK Explorer (pada telefon, buka dalam tab tersendiri). Setiap tugasan ditanda sendiri apabila Explorer mengesannya selesai.", "tasks done.", "tugasan yang selesai.")
            + f'<div class="labgrid"><div><iframe class="labframe" id="labframe" src="{L["src"]}" title="{L["title"]}" loading="lazy"></iframe>'
            + f'<p class="lead"><a href="{L["src"]}" target="_blank" rel="noopener">{B("Open the Explorer in its own tab", "Buka Explorer dalam tab tersendiri")}</a></p></div>'
            + f'<div class="card"><h2>{B("Tasks", "Tugasan")} · {L["title"]}</h2>{tasks}</div></div></section>')


def view_glossary() -> str:
    rows = "".join(f'<tr id="g-{i + 1}"><td class="g1">{t}</td><td>{B(en, ms)}</td></tr>' for i, (t, en, ms) in enumerate(C.GLOSSARY))
    return ('<section class="view" data-view="glossary" id="v-glossary" role="tabpanel" aria-labelledby="t-glossary" hidden>'
            + vhead("think", "Glossary", "Glosari", "Terms stay in English, as in the papers; the explanations follow your language. Type to filter.",
                    "Istilah kekal dalam English, seperti dalam kertas kerja; penerangan mengikut bahasa anda. Taip untuk menapis.")
            + f'<input id="gfilter" type="search" aria-label="Filter the glossary" placeholder="filter · tapis"><div class="tbl"><table class="gloss"><tbody>{rows}</tbody></table></div></section>')


def search_index() -> list:
    idx = []
    for i, n in enumerate(C.NOTES):
        idx.append({"view": "notes", "anchor": n["id"], "en": f"Notes §{i + 1} · {n['title'][0]}", "ms": f"Nota §{i + 1} · {n['title'][1]}"})
    for x in C.EXAMPLES:
        idx.append({"view": "examples", "anchor": x["id"], "en": f"Example {x['id'][1:]} · {x['title'][0]}", "ms": f"Contoh {x['id'][1:]} · {x['title'][1]}"})
    for e in C.EXERCISES:
        idx.append({"view": "exercises", "anchor": e["id"], "en": f"Exercise {e['id'][1:]} · {e['title'][0]}", "ms": f"Latihan {e['id'][1:]} · {e['title'][1]}"})
    for i, (t_en, t_ms, _) in enumerate(C.SLIDES):
        idx.append({"view": "slides", "anchor": str(i + 1), "en": f"Slide {i + 1} · {t_en}", "ms": f"Slide {i + 1} · {t_ms}"})
    for i, (m, t, _) in enumerate(C.LAB["tasks"]):
        idx.append({"view": "lab", "anchor": "", "en": f"Explorer task {i + 1} · {t[0]}", "ms": f"Tugasan Explorer {i + 1} · {t[1]}"})
    for i, (t, en, ms) in enumerate(C.GLOSSARY):
        idx.append({"view": "glossary", "anchor": f"g-{i + 1}", "en": f"Glossary · {t}", "ms": f"Glosari · {t}", "k": en + " " + ms})
    for rid, q, _ in C.START["recall"]:
        idx.append({"view": "start", "anchor": rid, "en": f"Recall · {q[0]}", "ms": f"Imbas kembali · {q[1]}"})
    idx.append({"view": "start", "anchor": "cando", "en": "Can-do checklist", "ms": "Senarai semak boleh-buat"})
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    for d in idx:
        d["en"], d["ms"] = strip(d["en"]), strip(d["ms"])
        if "k" in d:
            d["k"] = strip(d["k"])
    return idx


TABS = [("start", "Start", "Mula", False), ("notes", "Notes", "Nota", True), ("slides", "Slides", "Slides", True), ("examples", "Examples", "Contoh", True),
        ("exercises", "Exercises", "Latihan", True), ("lab", "Explorer", "Explorer", True), ("glossary", "Glossary", "Glosari", False)]

HEAD_PREFS = """<script>
/* preferences before first paint (rz-settings-buttons): {lang, theme, font} in one key per app */
(function(){var p={};try{p=JSON.parse(localStorage.getItem("%s")||"{}")}catch(e){}var d=window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches,
h=document.documentElement,l=p.lang||"ms";h.setAttribute("data-theme",p.theme||(d?"dark":"light"));h.setAttribute("data-lang",l);h.lang=l==="ms"?"ms":"en";
var f=+p.font||1;h.style.setProperty("--font-scale",f);h.style.setProperty("--ts",f)})();
</script>"""


def page(svgs) -> str:
    css = (ROOT / "shared" / "site.css").read_text(encoding="utf-8")
    js = (ROOT / "shared" / "site.js").read_text(encoding="utf-8")
    tabs = "".join(f'<button class="tab" role="tab" data-view="{v}" id="t-{v}" aria-controls="v-{v}">{B(en, ms)}' + (f'<span class="bd" data-bd="{v}"></span>' if bd else "") + "</button>" for v, en, ms, bd in TABS)
    parts = "".join((f'<a href="../{d}/index.html"' + (' aria-current="page"' if d == "01-foundations" else "") + f">{lab}</a>") if d else
                    f'<span aria-disabled="true" title="coming">{lab}</span>' for d, lab in M["parts"])
    course = {"app": M["app"], "part": M["part"], "key": M["key"], "prefs": M["prefs"], "avatar": "../shared/avatar/",
              "notes": [n["id"] for n in C.NOTES], "slides": len(C.SLIDES), "examples": [x["id"] for x in C.EXAMPLES],
              "exercises": [e["id"] for e in C.EXERCISES], "lab": {"id": "rk-bspline", "key": M["lab_key"], "milestones": [t[0] for t in C.LAB["tasks"]]},
              "cando": len(C.START["cando"]), "targetMin": sum(n["min"] for n in C.NOTES), "sections": search_index(), "guide": C.GUIDE}
    header = (f'<header class="top"><div class="hl">'
              f'<nav class="crumbs host" aria-label="Site"><a href="https://people.utm.my/arazin/for-my-students/">For My Students</a><span class="sep" aria-hidden="true">›</span>'
              f'<a href="../../index.html">My Lectures</a><span class="sep" aria-hidden="true">›</span><span>{M["crumb_topic"]}</span></nav>'
              f'<nav class="crumbs" aria-label="Breadcrumb"><a class="homelink" href="../index.html"><span aria-hidden="true">⌂</span> {B("Primer home", "Laman primer")}</a>'
              f'<span class="sep" aria-hidden="true">›</span><span aria-current="page">{M["crumb_page"]}</span></nav>'
              f'<div class="kicker">{M["kicker"]}</div><h1>{nobreak(M["h1"])}</h1>'
              f'<div class="subwrap"><p class="sub" id="sub">{M["desc"]}</p><button class="foldbtn" id="foldbtn" type="button" aria-controls="sub" aria-expanded="true" aria-label="Fold the description"></button></div></div>'
              f'<div class="tools"><div class="contact">✉ <a href="mailto:arazin@utm.my">arazin@utm.my</a></div><div class="toolrow">'
              f'<div class="seg partsw" role="group" aria-label="Parts">{parts}</div>'
              f'<div class="search" role="search"><input id="q" type="search" autocomplete="off" aria-label="Search this part" aria-controls="qres"><div id="qres" class="qres" role="listbox" hidden></div></div>'
              f'<div class="prefs"><button type="button" id="btn-lang" class="iconbtn langbtn" title="Language">EN</button><button type="button" id="btn-theme" class="iconbtn" title="Theme"></button>'
              f'<button type="button" id="btn-font" class="iconbtn fontbtn" title="Text size"><span class="aa" aria-hidden="true">A<small>A</small></span><span class="lvl" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>'
              f'<button type="button" id="btn-info" class="iconbtn" aria-label="About this screen"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.6h.01"/></svg></button></div>'
              f"</div></div></header>")
    nav = (f'<div class="navwrap"><div class="navrow"><a class="homeicon" href="../index.html" title="Primer home" aria-label="Primer home">⌂</a>'
           f'<nav class="tabs" role="tablist" aria-label="Sections">{tabs}</nav></div>'
           f'<div class="prog"><span class="pct">{B("Progress", "Kemajuan")}</span><div class="bar" id="pbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Progress"><i></i></div><span class="pct" id="ppct">0 %</span></div></div>')
    footer = (f'<footer class="foot"><p class="lect"><img class="fava" src="../shared/avatar/head.webp" alt="" title="Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin" width="36" height="36" decoding="async" loading="lazy">'
              f'{B("NURBS–meshfree research primer · Faculty of Civil Engineering, Universiti Teknologi Malaysia. Prepared by Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin for his research students.", "Primer penyelidikan NURBS–meshfree · Fakulti Kejuruteraan Awam, Universiti Teknologi Malaysia. Disediakan oleh Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin untuk pelajar penyelidikannya.")}</p>'
              f'<p>{B("Dr RJ, the guide on the right, works offline on this page: his steps and pointers come from the page itself, and nothing you type leaves the browser.", "Dr RJ, pemandu di sebelah kanan, berfungsi secara offline di page ini: langkah dan penunjuknya datang daripada page ini sendiri, dan tiada apa yang anda taip keluar dari pelayar.")}</p>'
              f'<p class="copy">{B("© 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia (Faculty of Civil Engineering). Free to share and adapt for non-commercial teaching and learning, with credit (CC BY-NC-SA 4.0); the code is MIT-licensed. The lecturer\'s avatar is excepted: see the <a href=\"https://github.com/RazinUTM/My_Lectures/blob/main/Research-NURBS-Meshfree/LICENSE.md\" target=\"_blank\" rel=\"noopener\">licence</a>.", "© 2026 Ahmad Razin Zainal Abidin dan Universiti Teknologi Malaysia (Fakulti Kejuruteraan Awam). Bebas dikongsi dan diadaptasi untuk pengajaran dan pembelajaran bukan komersial, dengan kredit (CC BY-NC-SA 4.0); kod berlesen MIT. Avatar pensyarah dikecualikan: lihat <a href=\"https://github.com/RazinUTM/My_Lectures/blob/main/Research-NURBS-Meshfree/LICENSE.md\" target=\"_blank\" rel=\"noopener\">lesen</a>.")}</p></footer>')
    body = view_start() + view_notes(svgs) + view_slides(svgs) + view_examples() + view_exercises() + view_lab() + view_glossary()
    return ("<!doctype html>\n<html lang=\"ms\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%23830f3e'/%3E%3Cpath d='M3 12C5 3 11 3 13 12' stroke='%23e3a130' stroke-width='2' fill='none'/%3E%3C/svg%3E\">\n"
            f"<title>{M['title']}</title>\n<meta name=\"description\" content=\"B-splines, NURBS and reproducing kernels for research students: notes, slides, worked examples, exercises with new numbers, an interactive Explorer and a guide.\">\n"
            + HEAD_PREFS % M["prefs"] + f"\n<style>\n{css}\n</style>\n</head>\n<body>\n<div class=\"wrap\">\n{header}\n{nav}\n<main>\n{body}\n</main>\n{footer}\n</div>\n"
            + f"<script>window.COURSE={json.dumps(course, ensure_ascii=False)};var EX={{specs:{{}}}};</script>\n<script>{C.EXERCISE_JS}</script>\n<script>\n{js}</script>\n</body>\n</html>\n")


HOME_JS = r"""
/* SPDX-License-Identifier: MIT · Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
   Primer home: settings buttons (rz-settings-buttons), the screen-guide box, each part's progress and the Explorer
   tasks read from this browser, and progress export/import. Every storage access is in try/catch. */
(function () {
  "use strict";
  var D = document, html = D.documentElement, $ = function (s) { return D.querySelector(s); }, MEM = {};
  var PKEY = "nmf-prefs", KEYS = ["nmf-prefs", "nmf-p1-v1", "nmf-lab-rkbs-v1"];
  function ld(k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return MEM[k] || null; } }
  function sv(k, v) { MEM[k] = v; try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var FONT_STEPS = [0.9, 1, 1.15, 1.3];
  function fontStep(f) { var k = 0; FONT_STEPS.forEach(function (v, i) { if (Math.abs(v - f) < Math.abs(FONT_STEPS[k] - f)) k = i; }); return k; }
  function nextFont(f, dir) { var i; if (dir > 0) { for (i = 0; i < FONT_STEPS.length; i++) if (FONT_STEPS[i] > f + 1e-6) return FONT_STEPS[i]; return FONT_STEPS[0]; }
    for (i = FONT_STEPS.length - 1; i >= 0; i--) if (FONT_STEPS[i] < f - 1e-6) return FONT_STEPS[i]; return FONT_STEPS[FONT_STEPS.length - 1]; }
  var SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';
  var p0 = ld(PKEY) || {}, dark = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  var PR = { lang: p0.lang === "en" ? "en" : "ms", theme: p0.theme || (dark ? "dark" : "light"), font: +p0.font || 1 };
  function L(en, ms) { return PR.lang === "ms" ? ms : en; }
  function save() { var p = ld(PKEY) || {}; p.lang = PR.lang; p.theme = PR.theme; p.font = PR.font; sv(PKEY, p); }
  function apply() {
    html.setAttribute("data-theme", PR.theme); html.setAttribute("data-lang", PR.lang); html.lang = PR.lang;
    html.style.setProperty("--font-scale", String(PR.font)); html.style.setProperty("--ts", String(PR.font));
    var lb = $("#btn-lang"), tb = $("#btn-theme"), fb = $("#btn-font"), ib = $("#btn-info");
    lb.textContent = PR.lang === "ms" ? "EN" : "BM"; lb.title = PR.lang === "ms" ? "Language" : "Bahasa"; lb.setAttribute("aria-label", lb.title);
    tb.innerHTML = PR.theme === "dark" ? SUN : MOON; tb.title = PR.theme === "dark" ? L("Light theme", "Tema cerah") : L("Dark theme", "Tema gelap"); tb.setAttribute("aria-label", tb.title);
    var k = fontStep(PR.font); fb.querySelectorAll(".lvl i").forEach(function (d, i) { d.classList.toggle("on", i <= k); });
    fb.title = L("Text size ", "Saiz teks ") + Math.round(PR.font * 100) + "% (" + L("click: ", "klik: ") + Math.round(nextFont(PR.font, 1) * 100) + "%)"; fb.setAttribute("aria-label", fb.title);
    ib.title = L("About this screen", "Tentang skrin ini"); ib.setAttribute("aria-label", ib.title);
  }
  $("#btn-lang").addEventListener("click", function () { PR.lang = PR.lang === "ms" ? "en" : "ms"; save(); apply(); });
  $("#btn-theme").addEventListener("click", function () { PR.theme = PR.theme === "dark" ? "light" : "dark"; save(); apply(); });
  $("#btn-font").addEventListener("click", function (e) { PR.font = nextFont(PR.font, e.shiftKey ? -1 : 1); save(); apply(); });
  $("#btn-info").addEventListener("click", function () { var g = $("#hguide"); g.hidden = !g.hidden; this.setAttribute("aria-expanded", String(!g.hidden)); if (!g.hidden) g.scrollIntoView({ behavior: "smooth", block: "nearest" }); });
  function paintProgress() {
    var st = ld("nmf-p1-v1") || {}, lab = ld("nmf-lab-rkbs-v1") || {}, pct = +st.pct || 0, b = $("#p1bar");
    if (b) { b.setAttribute("aria-valuenow", pct); b.querySelector("i").style.width = pct + "%"; $("#p1pct").textContent = pct + " %"; }
    var m = ["m1", "m2", "m3", "m4"].filter(function (k) { return lab[k] || (st.ms && st.ms[k]); }).length; $("#labdone").textContent = m + "/4";
  }
  $("#hexport").addEventListener("click", function () {
    var out = { app: "nmf", exported: new Date().toISOString(), data: {} }; KEYS.forEach(function (k) { var v = ld(k); if (v !== null) out.data[k] = v; });
    var a = D.createElement("a"); a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 1)], { type: "application/json" })); a.download = "nmf-primer-progress.json"; D.body.appendChild(a); a.click(); a.remove();
    $("#hmsg").textContent = L("Saved nmf-primer-progress.json.", "nmf-primer-progress.json telah disimpan.");
  });
  $("#himport").addEventListener("change", function () { var f = this.files && this.files[0]; if (!f) return; var r = new FileReader();
    r.onload = function () { try { var d = JSON.parse(r.result); if (!d || d.app !== "nmf" || !d.data) throw 0; KEYS.forEach(function (k) { if (d.data[k]) sv(k, d.data[k]); });
        p0 = ld(PKEY) || {}; PR.lang = p0.lang === "en" ? "en" : "ms"; PR.theme = p0.theme || PR.theme; PR.font = +p0.font || PR.font; apply(); paintProgress();
        $("#hmsg").textContent = L("Progress restored.", "Kemajuan telah dipulihkan."); } catch (e) { $("#hmsg").textContent = L("That file is not a progress file of this primer.", "Fail itu bukan fail kemajuan primer ini."); } };
    r.readAsText(f); this.value = ""; });
  window.addEventListener("storage", paintProgress); window.addEventListener("focus", paintProgress);
  apply(); paintProgress();
})();
"""


def home_page() -> str:
    """The primer home: parts with progress, the Explorer, the Python code, progress export/import, references."""
    css = (ROOT / "shared" / "site.css").read_text(encoding="utf-8")

    def card(kicker, title, body, foot="", href="", soon=False):
        inner = (f'<div class="pk">{kicker}</div><h3>{title}</h3><p>{body}</p>{foot}')
        if href and not soon:
            return f'<a class="partcard" href="{href}">{inner}</a>'
        return f'<div class="partcard{" soon" if soon else ""}">{inner}</div>'

    parts = (card(B("Part 1 of 4 · ready", "Bahagian 1 daripada 4 · siap"), nobreak(B("Foundations: B-splines, NURBS and reproducing kernels", "Asas: B-spline, NURBS dan reproducing kernel")),
                  B("Knot vectors and the Cox–de Boor recursion, NURBS and the exact circle, reproducing-kernel shape functions, blossom vectors (RK with blossom vectors = B-splines), and how to read the papers of the area like a reproducer.",
                    "Knot vector dan rekursi Cox–de Boor, NURBS dan bulatan tepat, reproducing-kernel shape function, blossom vector (RK dengan blossom vector = B-spline), dan cara membaca artikel bidang ini untuk menghasilkan semula keputusannya."),
                  '<div class="pbar"><div class="bar" id="p1bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Part 1 progress"><i></i></div><span class="num" id="p1pct">0 %</span></div>',
                  href="01-foundations/index.html")
             + card(B("Part 2 of 4 · " + "planned", "Bahagian 2 daripada 4 · dirancang"), B("Coupling IGA and meshfree regions", "Coupling kawasan IGA dan meshfree"),
                    B("Consistent coupling across a transition region, and what it costs: Wang &amp; Zhang (2014), Valizadeh et al. (2015), Shaw et al. (2008).",
                      "Coupling yang konsisten merentasi kawasan peralihan, dan kosnya: Wang &amp; Zhang (2014), Valizadeh et al. (2015), Shaw et al. (2008)."), soon=True)
             + card(B("Part 3 of 4 · planned", "Bahagian 3 daripada 4 · dirancang"), B("Integration, boundaries and consistency", "Integration, sempadan dan konsistensi"),
                    B("Variational consistency and the integration constraint, essential boundary conditions, inserted nodes: Chen, Hillman &amp; Rüter (2013), Chi &amp; Lin (2016).",
                      "Variational consistency dan integration constraint, essential boundary condition, node yang dimasukkan: Chen, Hillman &amp; Rüter (2013), Chi &amp; Lin (2016)."), soon=True)
             + card(B("Part 4 of 4 · planned", "Bahagian 4 daripada 4 · dirancang"), B("NURBS-based meshless methods of the group", "Kaedah meshless berasaskan NURBS milik kumpulan"),
                    B("N-RPIM (Mokhtaram et al. 2022) and NDM (Rasin et al. 2025), read with the tools of Parts 1–3.",
                      "N-RPIM (Mokhtaram et al. 2022) dan NDM (Rasin et al. 2025), dibaca dengan alat daripada Bahagian 1–3."), soon=True))
    explorer = card(B("Explorer · Part 1 §5", "Explorer · Bahagian 1 §5"), "B-spline and RK Explorer",
                    B("B-splines against RK functions built with blossom vectors or with node monomials: change the degree, move a knot, switch the kernel and the support, and read the errors.",
                      "B-spline berbanding RK function yang dibina dengan blossom vector atau node monomial: ubah darjah, gerakkan knot, tukar kernel dan support, dan baca ralatnya."),
                    f'<p class="muted">{B("Tasks done in this browser: ", "Tugasan selesai dalam pelayar ini: ")}<b class="num" id="labdone">0/4</b></p>', href="labs/rk-bspline.html")
    code = card(B("Python · companion code", "Python · kod pengiring"), '<span class="num">nmf_bspline_rk.py</span>',
                B("B-splines, Greville points, blossom vectors, a NURBS curve, standard RK and RK with blossom vectors, in the notation of the notes. Running it prints the numbers of Examples 1–3 of Part 1. Python 3.8+ and numpy.",
                  "B-spline, Greville point, blossom vector, NURBS curve, RK biasa dan RK dengan blossom vector, dalam notasi nota. Apabila dijalankan, ia mencetak nombor Contoh 1–3 Bahagian 1. Python 3.8+ dan numpy."),
                href="code/nmf_bspline_rk.py")
    guide = (f'<div class="card hguide" id="hguide" hidden><h3>{B("About this screen", "Tentang skrin ini")}</h3><ul>'
             f'<li>{B("<b>Parts</b>: open a part; its bar shows the progress kept in this browser.", "<b>Bahagian</b>: buka satu bahagian; bar menunjukkan kemajuan yang disimpan dalam pelayar ini.")}</li>'
             f'<li>{B("<b>Explorer</b> and <b>Python code</b>: the interactive lab and the script behind the worked examples.", "<b>Explorer</b> dan <b>kod Python</b>: makmal interaktif dan skrip di sebalik contoh berkerja.")}</li>'
             f'<li>{B("<b>Your progress</b>: save it to a file to move it to another device; nothing is sent anywhere.", "<b>Kemajuan anda</b>: simpan ke fail untuk dipindahkan ke peranti lain; tiada apa yang dihantar ke mana-mana.")}</li>'
             f'<li>{B("<b>Buttons</b> top right: language (BM / EN), light or dark theme, text size (AA: four sizes in turn), and this guide (ⓘ).", "<b>Butang</b> di kanan atas: bahasa (BM / EN), tema cerah atau gelap, saiz teks (AA: empat saiz bergilir), dan panduan ini (ⓘ).")}</li></ul></div>')
    header = (f'<header class="top"><div class="hl">'
              f'<nav class="crumbs host" aria-label="Site"><a href="https://people.utm.my/arazin/for-my-students/">For My Students</a><span class="sep" aria-hidden="true">›</span>'
              f'<a href="../index.html">My Lectures</a><span class="sep" aria-hidden="true">›</span><span aria-current="page">{M["crumb_topic"]}</span></nav>'
              f'<div class="kicker">{M["kicker"]}</div><h1>{B("NURBS–meshfree research primer", "Primer penyelidikan NURBS–meshfree")}</h1>'
              f'<p class="sub">{B("A self-study primer for students joining the group’s work on NURBS-based meshfree methods: how the CAD geometry and the meshfree approximation are built, the exact point where they meet, and how to read and reproduce the papers of the area. Four parts; Part 1 is ready.", "Primer pembelajaran kendiri untuk pelajar yang menyertai kerja kumpulan dalam kaedah meshfree berasaskan NURBS: bagaimana geometri CAD dan meshfree approximation dibina, titik tepat pertemuan kedua-duanya, dan cara membaca artikel bidang ini serta menghasilkan semula keputusannya. Empat bahagian; Bahagian 1 sudah siap.")}</p></div>'
              f'<div class="tools"><div class="contact">✉ <a href="mailto:arazin@utm.my">arazin@utm.my</a></div><div class="toolrow"><div class="prefs">'
              f'<button type="button" id="btn-lang" class="iconbtn langbtn" title="Language">EN</button><button type="button" id="btn-theme" class="iconbtn" title="Theme"></button>'
              f'<button type="button" id="btn-font" class="iconbtn fontbtn" title="Text size"><span class="aa" aria-hidden="true">A<small>A</small></span><span class="lvl" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>'
              f'<button type="button" id="btn-info" class="iconbtn" aria-expanded="false" aria-controls="hguide"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.6h.01"/></svg></button>'
              f"</div></div></div></header>")
    main = (guide
            + f'<section class="hsec"><h2>{B("Parts", "Bahagian")}</h2><div class="parts">{parts}</div></section>'
            + f'<section class="hsec"><h2>{B("Explorer and code", "Explorer dan kod")}</h2><div class="parts">{explorer}{code}</div></section>'
            + f'<section class="hsec"><h2>{B("Your progress", "Kemajuan anda")}</h2><div class="card"><p>{B("Progress, language, theme and text size are kept in this browser only. Save them to a file to move them to another device or browser; nothing is sent anywhere. This is your own record, not a gradebook.", "Kemajuan, bahasa, tema dan saiz teks disimpan dalam pelayar ini sahaja. Simpan ke fail untuk dipindahkan ke peranti atau pelayar lain; tiada apa yang dihantar ke mana-mana. Ini rekod anda sendiri, bukan buku markah.")}</p>'
            + f'<p class="row"><button class="btn" type="button" id="hexport">{B("Save progress to a file", "Simpan kemajuan ke fail")}</button>'
            + f'<label class="btn ghost" for="himport">{B("Load a progress file", "Muat fail kemajuan")}</label><input type="file" id="himport" accept="application/json,.json" hidden>'
            + '<span class="muted" id="hmsg" role="status"></span></p></div></section>'
            + f'<section class="hsec"><h2>{B("Reference texts", "Teks rujukan")}</h2><div class="card"><p>{C.START["reference"].replace("Reference texts: ", "").replace("Teks rujukan: ", "")}</p>'
            + f'<p class="muted">{B("The papers named on this page are cited, not reproduced: read them through the UTM Library.", "Artikel yang dinamakan di page ini dipetik, bukan diterbitkan semula: baca melalui Perpustakaan UTM.")}</p></div></section>')
    footer = (f'<footer class="foot"><p class="lect"><img class="fava" src="shared/avatar/head.webp" alt="" title="Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin" width="36" height="36" decoding="async" loading="lazy">'
              f'{B("NURBS–meshfree research primer · Faculty of Civil Engineering, Universiti Teknologi Malaysia. Prepared by Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin for his research students.", "Primer penyelidikan NURBS–meshfree · Fakulti Kejuruteraan Awam, Universiti Teknologi Malaysia. Disediakan oleh Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin untuk pelajar penyelidikannya.")}</p>'
              f'<p class="copy">{B("© 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia (Faculty of Civil Engineering). Free to share and adapt for non-commercial teaching and learning, with credit (CC BY-NC-SA 4.0); the code is MIT-licensed. The lecturer’s avatar is excepted: see the <a href=\"https://github.com/RazinUTM/My_Lectures/blob/main/Research-NURBS-Meshfree/LICENSE.md\" target=\"_blank\" rel=\"noopener\">licence</a>.", "© 2026 Ahmad Razin Zainal Abidin dan Universiti Teknologi Malaysia (Fakulti Kejuruteraan Awam). Bebas dikongsi dan diadaptasi untuk pengajaran dan pembelajaran bukan komersial, dengan kredit (CC BY-NC-SA 4.0); kod berlesen MIT. Avatar pensyarah dikecualikan: lihat <a href=\"https://github.com/RazinUTM/My_Lectures/blob/main/Research-NURBS-Meshfree/LICENSE.md\" target=\"_blank\" rel=\"noopener\">lesen</a>.")}</p></footer>')
    home_css = """
.hsec { margin: 26px 0 0; } .hsec h2 { font-size: calc(19px * var(--ts)); margin: 0 0 10px; }
.parts { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
.partcard { display: block; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; color: var(--fg); text-decoration: none; }
a.partcard:hover, a.partcard:focus-visible { border-color: var(--accent); }
.partcard.soon { opacity: .72; border-style: dashed; }
.partcard .pk { color: var(--eyebrow); font: 600 calc(11.5px * var(--ts)) / 1.3 var(--font-ui); letter-spacing: .08em; text-transform: uppercase; }
.partcard h3 { margin: 4px 0 6px; font-size: calc(17px * var(--ts)); text-wrap: balance; } .partcard p { margin: 0 0 6px; font-size: calc(14px * var(--ts)); }
.pbar { display: flex; align-items: center; gap: 8px; margin-top: 8px; } .pbar .bar { flex: 1; height: 6px; border-radius: 3px; background: var(--line); overflow: hidden; }
.pbar .bar i { display: block; height: 100%; width: 0; background: var(--accent); } .pbar .num { font-size: calc(12px * var(--ts)); color: var(--muted); }
.card .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; } label.btn { cursor: pointer; }
.hguide { border-left: 4px solid var(--acc-guide); } .hguide ul { margin: 6px 0 0; padding-left: 20px; }
"""
    return ("<!doctype html>\n<html lang=\"ms\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%23830f3e'/%3E%3Cpath d='M3 12C5 3 11 3 13 12' stroke='%23e3a130' stroke-width='2' fill='none'/%3E%3C/svg%3E\">\n"
            "<title>NURBS–meshfree research primer · UTM</title>\n<meta name=\"description\" content=\"A self-study primer on NURBS-based meshfree methods for research students: parts, an interactive Explorer, Python code.\">\n"
            + HEAD_PREFS % M["prefs"] + f"\n<style>\n{css}\n{home_css}</style>\n</head>\n<body>\n<div class=\"wrap\">\n{header}\n<main class=\"home\">\n{main}\n</main>\n{footer}\n</div>\n<script>{HOME_JS}</script>\n</body>\n</html>\n")


def endpoint() -> str:
    f = ROOT / "shared" / "tutor_endpoint.txt"
    for line in (f.read_text(encoding="utf-8").splitlines() if f.exists() else []):
        line = line.strip()
        if line and not line.startswith("#"):
            if not (line.startswith("https://") and line.endswith("/v1/chat")):
                sys.exit(f"build: {f.name} must hold an address like https://rz-tutor.<subdomain>.workers.dev/v1/chat")
            return line
    return ""


def main() -> int:
    svgs = render_equations()
    out = page(svgs)
    assert "%%EQ" not in out, "an equation placeholder was not filled"
    PART_DIR.mkdir(exist_ok=True)
    target = PART_DIR / "index.html"
    target.write_text(out, encoding="utf-8")
    tools = WEB / "rz-tutor" / "tools"
    subprocess.run([sys.executable, "-B", str(tools / "build_manifest.py"), "--course", str(ROOT), "--app", M["app"], f"{PART_DIR.name}:{M['part']}"], check=True)
    sys.path.insert(0, str(tools))
    import add_panel
    url = endpoint()
    html2, log = add_panel.inject(target.read_text(encoding="utf-8"), M["app"], M["part"], url, [], ":root{--rz-top:96px}")
    target.write_text(html2, encoding="utf-8")
    for line in log:
        print("  " + line)
    print(f"01-foundations/index.html: {len(html2):,} bytes; Dr RJ " + (f"with Worker {url}" if url else "offline (shared/tutor_endpoint.txt holds no address)"))
    home = home_page()
    (ROOT / "index.html").write_text(home, encoding="utf-8")
    print(f"index.html (primer home): {len(home):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
