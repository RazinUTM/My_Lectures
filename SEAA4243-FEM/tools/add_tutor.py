#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Add Dr RJ (the guide panel of the T&L app template) to SEAA 4243 part pages, and write their tutor files.

What: for each part page given (all five by default), this script
  1. writes the files the rz-tutor Worker and the offline guide read, from the page itself:
     <part>/tutor/manifest.json, blocks-<pk>.json and content-<pk>.txt (with their .ms twins, the page as it
     reads in Bahasa Melayu), and tutor/course.json for the course, rebuilt from every part's manifest
     (exercise answers, hints and worked solutions are left out);
  2. adds the guide panel with Dr RJ to <part>/index.html: the panel CSS, a <meta name="rz-tutor"> with the
     Worker address, the panel beside <main>, the widget script and the page glue (the engine in
     shared/course.js gives the panel window.RZ = {show, goTo, goSlide, current, lang} and window.RZ_AVS itself);
  3. fills the Feedback tab (<div id="rzfeedback">): rating, the point still unclear, mistake report, and
     "What's new" from shared/whats_new.txt. Feedback goes to the same Worker (/v1/feedback); its forms stay
     disabled until rz-tutor-worker has "feedback": true for app "seaa4243".
The Worker address is read from shared/tutor_endpoint.txt (set on 23 Nov 2026; app "seaa4243" is registered in
rz-tutor-worker). The AI answers only while the Worker's switch AI_SEAA4243 is on. With the switch off, or with
no address in that file, Dr RJ is in offline mode: he points to the matching sections of the page and nothing
typed leaves the browser.

How to call it, from the course folder (needs beautifulsoup4 and lxml):
  python3 tools/add_tutor.py                      all five parts
  python3 tools/add_tutor.py 03-plane-stress-1    one part

Why it is like this: the part pages are generated (src/build.sh runs the page builder, then this script), so the
panel has to be added by the build, or the next build would drop Dr RJ; the script refuses a page that already
has it.
The panel code in tools/rz-tutor/ is a pinned copy of rz-tutor-worker (see tools/rz-tutor/VERSION).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

course = Path(__file__).resolve().parent.parent  # SEAA4243-FEM/
tools = course / "tools" / "rz-tutor" / "tools"

APP = "seaa4243"
PARTS = {"01-heat-transfer-1": "p1", "02-heat-transfer-2": "p2", "03-plane-stress-1": "p3",
         "04-plane-stress-2": "p4", "05-plane-stress-3": "p5"}
CSS = ":root{--rz-top:86px}"                      # height of the sticky tab bar and progress line (.navwrap), as on SEAA 4333
HOOKS = []                                        # the engine exposes window.RZ and window.RZ_AVS itself (since 24 Nov 2026)


def endpoint() -> str:
    """The first line of shared/tutor_endpoint.txt that is neither empty nor a # comment, else ''."""
    f = course / "shared" / "tutor_endpoint.txt"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                if not line.startswith("https://") or not line.endswith("/v1/chat"):
                    sys.exit(f"add_tutor: {f.name} must hold an address like https://rz-tutor.<subdomain>.workers.dev/v1/chat, got {line}")
                return line
    return ""


def course_index() -> int:
    """Rewrite tutor/course.json from every part's tutor/manifest.json, so that building one part does not drop the
    others from the course-wide navigation manifest (build_manifest.py writes only the parts it is given)."""
    parts = []
    for mf in sorted(course.glob("*/tutor/manifest.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        parts.append({"part": m["part"], "folder": mf.parent.parent.name, "title": m["title"],
                      "sections": [{"id": s["id"], "title_en": s["title_en"], "title_ms": s["title_ms"]} for s in m["sections"]]})
    (course / "tutor" / "course.json").write_text(json.dumps({"app": APP, "course": course.name, "parts": parts}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(parts)


def main(argv: list[str]) -> int:
    folders = argv or list(PARTS)
    for f in folders:
        if f not in PARTS:
            sys.exit(f"add_tutor: unknown part folder {f}; known: {', '.join(PARTS)}")
        if 'id="rzguide"' in (course / f / "index.html").read_text(encoding="utf-8"):
            sys.exit(f"add_tutor: {f}/index.html already has Dr RJ; start from the page without the panel")
    try:
        import bs4  # noqa: F401
    except ImportError:
        sys.exit("add_tutor: needs beautifulsoup4 (python3 -m pip install --user beautifulsoup4 lxml)")
    # 1. tutor files from the plain pages, before the panel is added
    subprocess.run([sys.executable, "-B", str(tools / "build_manifest.py"), "--course", str(course), "--app", APP,
                    *[f"{f}:{PARTS[f]}" for f in folders]], check=True)
    print(f"  tutor/course.json: {course_index()} parts")
    # 2. the panel
    sys.path.insert(0, str(tools))
    import add_panel
    url = endpoint()
    news = add_panel.read_whats_new(course / "shared" / "whats_new.txt")
    for f in folders:
        page = course / f / "index.html"
        out, log = add_panel.inject(page.read_text(encoding="utf-8"), APP, PARTS[f], url, HOOKS, CSS)
        out, more = add_panel.inject_feedback(out, APP, PARTS[f], news)
        log += more
        page.write_text(out, encoding="utf-8")
        print(f"{f}/index.html: Dr RJ added, " + (f"Worker {url}" if url else "offline mode (shared/tutor_endpoint.txt holds no address)"))
        for line in log:
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
