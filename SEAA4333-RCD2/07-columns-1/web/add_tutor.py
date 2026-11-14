#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Add Dr RJ (the guide panel of the T&L app template) to the Unit 7 page, and write the tutor files.

What: after web/build_page.py has written index.html, this script
  1. writes the files the rz-tutor Worker and the offline guide read, from the page itself:
     tutor/manifest.json, tutor/blocks-u7.json and tutor/content-u7.txt in this folder, and
     ../tutor/course.json for the course, rebuilt from every Unit's manifest (exercise answers, hints and
     worked solutions are left out);
  2. adds the guide panel with Dr RJ to index.html: the panel CSS, a <meta name="rz-tutor"> with the
     Worker address, the panel beside <main>, the widget script and the page glue.
The Worker address is read from shared/tutor_endpoint.txt in this folder. While it holds no address
(as now), Dr RJ is in offline mode: he points to the matching sections of the page and nothing leaves
the browser. The AI answers only once the owner registers app "seaa4333" in rz-tutor-worker, switches
it on there, and puts the address in that file.

How to call it, from this topic folder (build.sh runs both lines):
  python3 web/build_page.py && python3 web/add_tutor.py
Needs beautifulsoup4 and lxml.

Why it is like this: index.html is generated, so the panel is added by the build, or the next build
would drop Dr RJ without a word. The panel code in web/rz-tutor/ is a pinned copy of rz-tutor-worker
(see web/rz-tutor/VERSION). No engine hooks are injected: ../shared/course.js already exposes
window.RZ = {show, goTo, goSlide, current, lang} and window.RZ_AVS (the avatar poses).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

here = Path(__file__).resolve().parent          # web/
topic = here.parent                              # 07-columns-1/
course = topic.parent                            # SEAA4333-RCD2/
tools = here / "rz-tutor" / "tools"

APP, PART = "seaa4333", "u7"
CSS = ":root{--rz-top:86px}"                     # height of the page's sticky tab bar and progress line
HOOKS = []                                       # the engine exposes window.RZ and window.RZ_AVS itself


def endpoint() -> str:
    """The first line of shared/tutor_endpoint.txt that is neither empty nor a # comment, else ''."""
    f = topic / "shared" / "tutor_endpoint.txt"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                if not line.startswith("https://") or not line.endswith("/v1/chat"):
                    sys.exit(f"add_tutor: {f.name} must hold an address like https://rz-tutor.<subdomain>.workers.dev/v1/chat, got {line}")
                return line
    return ""


def course_index() -> int:
    """Rewrite ../tutor/course.json from every Unit's tutor/manifest.json, so that building one Unit does not
    drop the others from the course-wide navigation manifest (build_manifest.py writes only the parts it is given)."""
    parts = []
    for mf in sorted(course.glob("*/tutor/manifest.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        parts.append({"part": m["part"], "folder": mf.parent.parent.name, "title": m["title"],
                      "sections": [{"id": s["id"], "title_en": s["title_en"], "title_ms": s["title_ms"]} for s in m["sections"]]})
    (course / "tutor" / "course.json").write_text(json.dumps({"app": APP, "course": course.name, "parts": parts}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(parts)


def main() -> int:
    page = topic / "index.html"
    html = page.read_text(encoding="utf-8")
    if 'id="rzguide"' in html:
        sys.exit("add_tutor: index.html already has Dr RJ. Run python3 web/build_page.py first (it rewrites index.html), then this script.")
    try:
        import bs4  # noqa: F401
    except ImportError:
        sys.exit("add_tutor: needs beautifulsoup4 (python3 -m pip install --user beautifulsoup4 lxml)")
    # 1. tutor files from the plain page, before the panel is added
    subprocess.run([sys.executable, "-B", str(tools / "build_manifest.py"), "--course", str(course), "--app", APP,
                    f"{topic.name}:{PART}"], check=True)
    print(f"  tutor/course.json: {course_index()} Units")
    # 2. the panel
    sys.path.insert(0, str(tools))
    import add_panel
    url = endpoint()
    out, log = add_panel.inject(html, APP, PART, url, HOOKS, CSS)
    page.write_text(out, encoding="utf-8")
    for line in log:
        print("  " + line)
    print("index.html: Dr RJ added, " + (f"Worker {url}" if url else "offline mode (shared/tutor_endpoint.txt holds no address)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
