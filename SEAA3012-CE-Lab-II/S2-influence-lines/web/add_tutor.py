"""Add Dr RJ (the guide panel with the AI tutor) to the Lab S2 course page, and write the tutor files.

What: after web/build_web.py has written index.html, this script
  1. writes the files the rz-tutor Worker reads, from the page itself: tutor/manifest.json,
     tutor/blocks-s2.json and tutor/content-s2.txt in this folder, and ../tutor/course.json for the
     course (exercise answers, hints and worked solutions are left out);
  2. adds the guide panel with Dr RJ to index.html (the claude.ai artifact form is left as it is);
  3. fills the Feedback tab (rating, muddiest point, mistake report, like, "What's new" from
     shared/whats_new.txt) and, when shared/analytics_token.txt holds a Cloudflare Web Analytics token,
     adds its cookie-free visit beacon.
The Worker address is read from shared/tutor_endpoint.txt. While that file holds no address, or while
the Worker's switch AI_SEAA3012 is off (the page asks the Worker first), Dr RJ stays in offline mode: he
points to matching sections of the page and nothing leaves the browser. Feedback goes to the same Worker
(/v1/feedback) and does not depend on the AI switch; without an address its forms stay disabled.

How to call it, from this topic folder (build.sh runs both lines):
  python3 web/build_web.py && python3 web/add_tutor.py
Needs beautifulsoup4 (python3 -m pip install --user beautifulsoup4).

Why it is like this: index.html is generated, so the panel has to be added by the build, or the next
build would drop Dr RJ without a word. The panel code in web/rz-tutor/ is a pinned copy of
rz-tutor-worker (see web/rz-tutor/VERSION); to update it, copy a newer release over that folder and
rebuild. The two hooks below are the only lines added to the page's own engine.
"""
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

here = Path(__file__).resolve().parent          # web/
topic = here.parent                              # S2-influence-lines/
course = topic.parent                            # SEAA3012-CE-Lab-II/
tools = here / "rz-tutor" / "tools"

APP, PART = "seaa3012", "s2"
CSS = ":root{--rz-top:82px}"                     # height of the page's sticky tab bar
HOOKS = [
    ("var AVS={", "after-statement", "window.RZ_AVS=AVS;"),
    ("show(start,true);updateProgress();", "before",
     "window.RZ={show:show,goTo:goTo,goSlide:goSlide,current:function(){return current},lang:function(){return ST.lang}};"),
]


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


def main() -> int:
    page = topic / "index.html"
    html = page.read_text(encoding="utf-8")
    if 'id="rzguide"' in html:
        sys.exit("add_tutor: index.html already has Dr RJ. Run python3 web/build_web.py first (it rewrites index.html), then this script.")
    try:
        import bs4  # noqa: F401
    except ImportError:
        sys.exit("add_tutor: needs beautifulsoup4 (python3 -m pip install --user beautifulsoup4)")
    # 1. tutor files from the plain page, before the panel is added
    subprocess.run([sys.executable, "-B", str(tools / "build_manifest.py"), "--course", str(course), "--app", APP,
                    f"{topic.name}:{PART}"], check=True)
    # 2. the panel
    sys.path.insert(0, str(tools))
    import add_panel
    url = endpoint()
    out, log = add_panel.inject(html, APP, PART, url, HOOKS, CSS)
    news = add_panel.read_whats_new(topic / "shared" / "whats_new.txt")
    out, more = add_panel.inject_feedback(out, APP, PART, news)
    log += more
    out, more = add_panel.inject_analytics(out, add_panel.read_token(topic / "shared" / "analytics_token.txt"))
    log += more
    page.write_text(out, encoding="utf-8")
    for line in log:
        print("  " + line)
    print("index.html: Dr RJ added, " + (f"Worker {url} (the AI answers only while the Worker's switch AI_SEAA3012 is on)"
                                          if url else "offline mode (shared/tutor_endpoint.txt holds no address)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
