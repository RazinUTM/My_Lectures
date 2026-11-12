#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Build the tutor manifest and plain-text content of a T&L part page.

What: reads one or more part pages of a course built on the rz-tnl-app-template
(`index.html` with `section.view[data-view]`, `section.nsec`, `section.xsec`,
`article.qx`, `div.tk[data-ms]`, `table.gloss`, and `slides/deck.html` with
`div.sl[data-title]`) and writes, per part:

  <part>/tutor/manifest.json      every navigable section with a stable id
  <part>/tutor/blocks-<pk>.json   one citable text block per section, in manifest order: the
                                  document the Worker sends with citations enabled (English,
                                  no Malay spans, no exercise answers, hints or solutions)
  <part>/tutor/content-<pk>.txt   the same blocks as one plain text, for reading and review

and, for the course folder, `tutor/course.json`: every part's sections (ids and
titles only), which the Worker sends as the course-wide navigation manifest.

How to call it:

  python3 tools/build_manifest.py --course SEAA4243-FEM --app seaa4243 \
      01-heat-transfer-1:p1 02-heat-transfer-2:p2

Why it is like this: the manifest is the single source for the search box, the
scripted guide's targets and the AI tutor's `[[goto:<id>]]` navigation. A hand-kept
list drifts within a week, so it is generated from the page itself, and the content
text is deterministic (no timestamps inside it) because the Worker's prompt cache
needs a byte-identical prefix. Equations in these pages are pre-rendered SVG; the
LaTeX source is taken from `data-tex` on the equation wrapper, from a `<title>` inside
the SVG, or from an `equations.json` map (`{"e_pde": "..."}`) next to the page or in
`shared/`; when none exists the equation is written as a placeholder and counted, so
the gap is visible in the summary rather than silent.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

SLIDE_TEXT_CHARS = 420   # per slide, enough for the flow of the lecture, not a second copy of the notes
MS_SELECTORS = [".ms"]   # bilingual pairs: <span class="en"> … <span class="ms"> …


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_ms(node: Tag) -> None:
    """Remove the Malay half of every bilingual pair (in place)."""
    for sel in MS_SELECTORS:
        for ms in node.select(sel):
            ms.decompose()


def mark_subsup(soup: BeautifulSoup) -> None:
    """Turn <sub>i</sub> into _i and <sup>2</sup> into ^2 so that T̂_i and W m^-2 survive as text."""
    for tag, mark in (("sub", "_"), ("sup", "^")):
        for t in soup.find_all(tag):
            s = text_of(t)
            t.replace_with(mark + (s if len(s) == 1 else "{" + s + "}"))


def clean(text: str) -> str:
    text = text.replace(" ", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r" ([_^])(?=\{|\w)", r"\1", text)   # 'N _1' (from <sub>) -> 'N_1'
    return text.strip()


def text_of(node: Tag) -> str:
    return clean(node.get_text(" ", strip=True))


def lang_text(node: Tag, lang: str) -> str:
    """Text of one language of a bilingual node (falls back to the whole text)."""
    spans = node.select(f":scope > span.{lang}") or node.select(f"span.{lang}")
    if spans:
        return clean(" ".join(text_of(s) for s in spans))
    return text_of(node)


def heading_text(h: Tag, lang: str) -> str:
    """'3. Boundary conditions' from <h2>3. <span class=en>…</span><span class=ms>…</span></h2>."""
    parts = []
    for child in h.children:
        if isinstance(child, Tag):
            if "en" in child.get("class", []) or "ms" in child.get("class", []):
                if lang in child.get("class", []):
                    parts.append(text_of(child))
            else:
                parts.append(text_of(child))
        else:
            parts.append(str(child))
    return clean("".join(parts))


class Equations:
    """Resolve the LaTeX of a pre-rendered equation; count what cannot be resolved."""

    def __init__(self, maps: list[Path]):
        self.map: dict[str, str] = {}
        for p in maps:
            if p.exists():
                self.map.update(json.loads(read(p)))
        self.missing: list[str] = []

    def resolve(self, eqwrap: Tag) -> str:
        svg = eqwrap.find("svg")
        key = (svg.get("aria-label") if svg else None) or eqwrap.get("data-eq") or ""
        tex = eqwrap.get("data-tex") or (svg.get("data-tex") if svg else None)
        if not tex and svg is not None:
            title = svg.find("title")
            if title and text_of(title) and text_of(title) != key:
                tex = text_of(title)
        if not tex and key in self.map:
            tex = self.map[key]
        if tex:
            return tex.strip()
        self.missing.append(key or "?")
        return f"[equation {key or '?'}: source not available in the page]"


def render_block(node: Tag, eqs: Equations) -> str:
    """Plain text of a notes/example block: equations as LaTeX with their labels, lists as lines."""
    node = BeautifulSoup(str(node), "lxml").body
    strip_ms(node)
    for row in node.select(".eqrow"):
        wrap = row.select_one(".eqwrap") or row
        lbl = row.select_one(".lbl")
        label = text_of(lbl) if lbl else ""
        row.replace_with(f"\nEQUATION {label}: {eqs.resolve(wrap)}\n")
    for fig in node.select("figure"):
        cap = fig.find("figcaption")
        fig.replace_with(f"\n[Figure: {text_of(cap) if cap else 'no caption'}]\n")
    for kp in node.select("details.kp"):
        items = [text_of(li) for li in kp.select("li")]
        kp.replace_with("\nKey points:\n" + "\n".join(f"- {i}" for i in items) + "\n")
    for qc in node.select(".qc"):
        q = qc.find("p")
        fb = qc.select_one(".fb")
        opts = [text_of(o) for o in qc.select(".opt")]
        qc.replace_with(
            "\nQuick check (not graded): " + (text_of(q) if q else "")
            + "\nOptions: " + " | ".join(opts)
            + ("\nExplanation shown after answering: " + text_of(fb) if fb else "") + "\n")
    for foot in node.select(".sfoot, .readck, .readtime, .credit"):
        foot.decompose()
    for h in node.select("h3, h4"):
        h.replace_with(f"\n## {text_of(h)}\n")
    for li in node.select("li"):
        li.insert_before("\n- ")
    for p in node.select("p, div.def, div.sb, tr"):
        p.insert_after("\n")
    return clean(node.get_text(" ", strip=False))


def slide_text(body: Tag) -> str:
    """Plain text of a slide with each bullet and paragraph on its own line, so that a quoted slide
    does not run its points together ("pin A, roller B, cantilever BC CD: suspended span…")."""
    for li in body.select("li"):
        li.insert_before("\n- ")
    for p in body.select("p, div, tr"):
        p.insert_after("\n")
    return clean(body.get_text(" ", strip=False))


def prefixed(word: str, title: str) -> str:
    """'Example 1 · …' stays as it is; a bare '1 · …' gets the word in front."""
    return title if re.match(r"^(Example|Contoh|Exercise|Latihan)\b", title) else f"{word} {title}"


def short(s: str, n: int = 64) -> str:
    s = s.split(". ")[0].rstrip(".")
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def minutes_of(sec: Tag) -> int | None:
    if sec.get("data-rt"):
        return int(sec["data-rt"])
    rt = sec.select_one(".readtime")
    if not rt:
        return None
    m = re.search(r"(\d+)", text_of(rt))
    return int(m.group(1)) if m else None


ANSWER_SELECTORS = ".sol, .hintbox, .fb, .qbar, input, select, textarea, .tfs, .anstab, .tkok, .res, img, svg"


def statement_of(node: Tag) -> str:
    """The student-facing text of an exercise or task: never its answers, hints or solution."""
    b = BeautifulSoup(str(node), "lxml").body
    for x in b.select(ANSWER_SELECTORS):
        x.decompose()
    for h in b.select("header, h4, h5"):
        h.decompose()
    strip_ms(b)
    return text_of(b)


def build_part(part_dir: Path, pk: str, app: str, eq_maps: list[Path]) -> tuple[dict, list[dict], str, Equations]:
    """Return (manifest, blocks, content text, equations) for one part page.

    Every navigable section becomes one citable block {id, text}; the blocks are what the Worker
    sends as a custom-content document with citations enabled, so a citation of block i is a
    citation of manifest section i and becomes a "Go to" button without any guessing.
    """
    html = read(part_dir / "index.html")
    soup = BeautifulSoup(html, "lxml")
    mark_subsup(soup)
    eqs = Equations(eq_maps)
    course_meta = {}
    m = re.search(r"window\.COURSE\s*=\s*(\{.*?\});", html, re.S)
    if m:
        course_meta = json.loads(m.group(1))

    h1 = soup.find("h1")
    sub = soup.select_one("header .sub")
    title = text_of(h1) if h1 else part_dir.name
    sections: list[dict] = []
    blocks: list[dict] = []

    def add(section: dict, body: str, label: str = "") -> None:
        sections.append(section)
        head = f"[{section['id']}] {label or section['title_en']}"
        blocks.append({"id": section["id"], "text": (head + "\n" + body.strip()).strip()})

    # Start: outcomes
    lo = [li for li in soup.select("#v-start ol.lo li") if not li.find_parent(class_="ms")]   # S2 keeps a whole <ol class="lo ms">
    if lo:
        outcomes = "\n".join(f"{i}. {lang_text(li, 'en')}" for i, li in enumerate(lo, 1))
        add({"id": "start-outcomes", "view": "start", "anchor": None, "selector": "ol.lo",
             "title_en": "After this part you should be able to", "title_ms": "Selepas bahagian ini, anda sepatutnya boleh"}, outcomes)

    # Notes
    for sec in soup.select("#v-notes section.nsec"):
        sid = sec.get("id")
        h2 = sec.find("h2")
        body = BeautifulSoup(str(sec), "lxml").body.find("section")
        body.find("h2").decompose()
        add({"id": f"notes-{sid}", "view": "notes", "anchor": sid,
             "title_en": heading_text(h2, "en"), "title_ms": heading_text(h2, "ms"), "minutes": minutes_of(sec)},
            render_block(body, eqs), label=f"Notes {heading_text(h2, 'en')}")

    # Slides: slides/deck.html (div.sl[data-title]) or section.slide inside the page
    in_page = soup.select("#v-slides section.slide")
    if in_page:
        for n, sl in enumerate(in_page, 1):
            body = BeautifulSoup(str(sl), "lxml").body
            strip_ms(body)
            for x in body.select("style, script, svg, img"):
                x.decompose()
            hd = body.select_one("h1, h2, h3, .t")
            t = text_of(hd) if hd else f"Slide {n}"
            if hd:
                hd.decompose()
            add({"id": f"slides-{n}", "view": "slides", "anchor": str(n),
                 "title_en": f"Slide {n}: {t}", "title_ms": f"Slide {n}: {t}"}, slide_text(body)[:SLIDE_TEXT_CHARS])
    deck = part_dir / "slides" / "deck.html"
    if deck.exists() and not in_page:
        dsoup = BeautifulSoup(read(deck), "lxml")
        mark_subsup(dsoup)
        for n, sl in enumerate(dsoup.select("div.sl"), 1):
            t = sl.get("data-title", "").strip()
            body = BeautifulSoup(str(sl), "lxml").body
            for x in body.select("style, script"):
                x.decompose()
            txt = text_of(body)
            if txt.startswith(t):
                txt = txt[len(t):].strip()
            add({"id": f"slides-{n}", "view": "slides", "anchor": str(n),
                 "title_en": f"Slide {n}: {t}", "title_ms": f"Slide {n}: {t}"}, txt[:SLIDE_TEXT_CHARS])

    # Examples (model answers, answer-scheme form: shown to students in full)
    for x in soup.select("#v-examples section.xsec"):
        xid = x.get("id")
        h2 = x.find("h2")
        t_en, t_ms = (heading_text(h2, "en"), heading_text(h2, "ms")) if h2 else (xid, xid)
        body = BeautifulSoup(str(x), "lxml").body.find("section")
        if body.find("h2"):
            body.find("h2").decompose()
        add({"id": f"examples-{xid}", "view": "examples", "anchor": xid,
             "title_en": prefixed("Example", t_en), "title_ms": prefixed("Contoh", t_ms)}, render_block(body, eqs))

    # Exercises: statement only; hints, answers and solutions are left out on purpose
    for q in soup.select("#v-exercises article.qx"):
        qid = q.get("id") or q.get("data-ex")
        h4 = q.find("h4")
        t_en, t_ms = (heading_text(h4, "en"), heading_text(h4, "ms")) if h4 else (qid, qid)
        stmt = statement_of(q.select_one(".exbody") or q) or "generated in the app at run time (numbers change per attempt)"
        add({"id": f"exercises-{qid}", "view": "exercises", "anchor": qid,
             "title_en": prefixed("Exercise", t_en), "title_ms": prefixed("Latihan", t_ms)},
            f"Statement: {stmt}\nHints and the solution are in the app; the tutor gives the next hint only.")
    quick = [lang_text(q.find("p"), "en") for q in soup.select("#v-exercises div.q") if q.find("p")]
    if quick:
        add({"id": "exercises-quick", "view": "exercises", "anchor": None, "selector": "#v-exercises div.q",
             "title_en": "Exercises: quick concept questions", "title_ms": "Latihan: soalan konsep pantas"},
            "\n".join(f"- {t}" for t in quick))

    # Explorer tasks: .tk[data-ms] (view "lab", SEAA 4243) or article.tk[id] (view "explorer", S2)
    for tk in soup.select(".view .tk[data-ms], .view article.tk[id]"):
        view_el = tk.find_parent("section", class_="view")
        tview = view_el.get("data-view") if view_el else "lab"
        ms = tk.get("data-ms") or tk.get("id")
        h4 = tk.find("h4")
        n = h4.select_one(".tkn") if h4 else None
        num = text_of(n) if n else ""
        if n:
            n.decompose()
        t_en, t_ms = (lang_text(h4, "en"), lang_text(h4, "ms")) if h4 else (ms, ms)
        has_id = bool(tk.get("id"))
        add({"id": f"{tview}-{ms}", "view": tview, "anchor": ms if has_id else None,
             "selector": None if has_id else f'.tk[data-ms="{ms}"]',
             "title_en": f"Explorer task {num}: {short(t_en)}", "title_ms": f"Tugasan Explorer {num}: {short(t_ms)}"},
            statement_of(tk) + "\n(The task's answer fields are checked in the app; they are not included here.)",
            label=f"Explorer task {num} · {t_en}")

    # Other views: cards with a heading (e.g. the S2 lab sheet), navigable by id when they have one
    handled = {"start", "notes", "slides", "examples", "exercises", "glossary"}
    for view_el in soup.select("section.view[data-view]"):
        vname = view_el.get("data-view")
        if vname in handled:
            continue
        for card in view_el.select(".card"):
            if card.select_one(".tk, .qx") or card.get("id") == "tasks":
                continue  # tasks are listed above
            hd = card.select_one("h2, h3")
            if not hd:
                continue
            t_en, t_ms = lang_text(hd, "en"), lang_text(hd, "ms")
            slug = re.sub(r"[^a-z0-9]+", "-", t_en.lower()).strip("-")[:40]
            cid = card.get("id") or (hd.get("id") if hd.get("id") else None)
            sid = f"{vname}-{cid or slug}"
            if any(x["id"] == sid for x in sections):
                continue
            add({"id": sid, "view": vname, "anchor": cid, "selector": None,
                 "title_en": f"{vname.capitalize()}: {short(t_en)}", "title_ms": f"{vname.capitalize()}: {short(t_ms)}"},
                statement_of(card)[:1500], label=f"{vname.capitalize()} · {t_en}")

    # Glossary: one block per term
    for tr in soup.select("#v-glossary table.gloss tr"):
        tds = tr.find_all("td")
        if len(tds) < 2:
            continue
        term = text_of(tds[0])
        slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-") or "term"
        base, k = slug, 2
        while any(x["id"] == f"glossary-{slug}" for x in sections):
            slug, k = f"{base}-{k}", k + 1       # symbols such as x and x̄ can share a slug
        add({"id": f"glossary-{slug}", "view": "glossary", "anchor": None, "selector": None,
             "title_en": f"Glossary: {term}", "title_ms": f"Glosari: {term}"}, f"{term}: {lang_text(tds[1], 'en')}")

    ids = [s["id"] for s in sections]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise SystemExit(f"duplicate ids: {sorted(dup)}")

    manifest = {
        "app": app, "part": pk, "title": title, "folder": part_dir.name,
        "course_meta": {k: course_meta.get(k) for k in ("key", "notes", "slides", "examples", "cando", "targetMin")},
        "sections": sections,
        "equations_missing": len(eqs.missing),
    }
    text = f"# {title}\n{lang_text(sub, 'en') if sub else ''}\n\n" + "\n\n".join(b["text"] for b in blocks) + "\n"
    return manifest, blocks, text, eqs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--course", required=True, help="course folder, e.g. SEAA4243-FEM")
    ap.add_argument("--app", required=True, help="app id used by the Worker, e.g. seaa4243")
    ap.add_argument("parts", nargs="+", help="<part folder>:<part key>, e.g. 01-heat-transfer-1:p1")
    ap.add_argument("--equations", action="append", default=[], help="extra equations.json map(s)")
    a = ap.parse_args()
    course = Path(a.course)
    if not course.is_dir():
        print(f"not a folder: {course}", file=sys.stderr)
        return 2
    index = {"app": a.app, "course": course.name, "parts": []}
    for spec in a.parts:
        folder, _, pk = spec.partition(":")
        if not pk:
            print(f"use <folder>:<part key>, got {spec}", file=sys.stderr)
            return 2
        pdir = course / folder
        maps = [pdir / "equations.json", course / "shared" / "equations.json"] + [Path(p) for p in a.equations]
        manifest, blocks, text, eqs = build_part(pdir, pk, a.app, maps)
        out = pdir / "tutor"
        out.mkdir(exist_ok=True)
        (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (out / f"blocks-{pk}.json").write_text(json.dumps({"part": pk, "title": manifest["title"], "blocks": blocks}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (out / f"content-{pk}.txt").write_text(text, encoding="utf-8")
        index["parts"].append({
            "part": pk, "folder": folder, "title": manifest["title"],
            "sections": [{"id": s["id"], "title_en": s["title_en"], "title_ms": s["title_ms"]} for s in manifest["sections"]],
        })
        words = len(text.split())
        print(f"{folder} ({pk}): {len(manifest['sections'])} sections, {words} words (~{words * 4 // 3} tokens), "
              f"{len(eqs.missing)} equations without source" + (f": {sorted(set(eqs.missing))[:8]}…" if eqs.missing else ""))
    (course / "tutor").mkdir(exist_ok=True)
    (course / "tutor" / "course.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {course / 'tutor' / 'course.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
