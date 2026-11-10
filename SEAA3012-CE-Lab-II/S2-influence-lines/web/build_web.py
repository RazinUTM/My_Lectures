"""Assemble the Lab S2 course page from web/src into two outputs:
   activity/influence-line-explorer.html  - body-only form published as the claude.ai artifact
   index.html (topic root)                - complete HTML document for GitHub Pages or any web server
"""
import pathlib
here = pathlib.Path(__file__).resolve().parent
src, shared = here / "src", here.parent / "shared"
import re
# Text size (AA button): every px font size in the page styles is multiplied by --font-scale (90/100/115/130 %).
# The header styles (header.css) are appended unscaled, so the header and tab bar keep their size.
def scale_fonts(t):
    def fix(m):
        decl = m.group(0)
        if "!important" in decl or "var(--font-scale" in decl:
            return decl
        return re.sub(r"(?<![\w.-])(\d+(?:\.\d+)?)px", r"calc(\1px*var(--font-scale,1))", decl)
    return re.sub(r"(?<![\w-])font(?:-size)?\s*:[^;}\"]*", fix, t)
css = (scale_fonts((src / "style_v2.css").read_text() + "\n" + (src / "style_add.css").read_text())
       + "\n" + (src / "header.css").read_text())
body = scale_fonts("".join((src / p).read_text() for p in ["p1_start_notes.html", "p2_slides.html", "p3_explorer_ex_lab.html"]))
js = (src / "app.js").read_text()
photo = (shared / "photo_b64.txt").read_text().strip()
qr = (shared / "qr_explorer_b64.txt").read_text().strip()
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">'
MJCONF = ('<script>\nwindow.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]},svg:{fontCache:"global"},\n'
          '  startup:{typeset:false,ready:function(){MathJax.startup.defaultReady();MathJax.startup.promise.then(function(){if(window.__mjReady)window.__mjReady();});}}};\n</script>\n'
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>')
TITLE = "<title>Lab S2 Influence Lines</title>"
# Preferences (language, theme, text size, folded description) applied before first paint: rz-settings-buttons.
PREFS = ('<script>(function(){try{var r=document.documentElement,p=JSON.parse(localStorage.getItem("seaa3012-prefs")||"null");'
         'if(!p){var s=JSON.parse(localStorage.getItem("s2-il-v3")||"{}");p={lang:s.lang,theme:s.theme}}'
         'if(p.lang==="ms"){r.setAttribute("data-lang","ms");r.lang="ms"}'
         'if(p.theme==="light"||p.theme==="dark")r.setAttribute("data-theme",p.theme);'
         'if(+p.font)r.style.setProperty("--font-scale",String(+p.font));if(p.fold)r.classList.add("subfold")}catch(e){}})();</script>')
import base64
AVD = here.parent / "avatar"
def avatars(t):
    for f in sorted(AVD.glob("*.webp")):
        t = t.replace("%%AVURL_" + f.stem + "%%", "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode())
    return t
body = avatars(body.replace("%%PHOTO%%", photo).replace("%%QR%%", qr))
js = avatars(js)
assert "%%" not in body
art = (TITLE + "\n" + PREFS + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + FONTS + "\n<style>\n" + css + "</style>\n" + MJCONF
       + "\n" + body + "\n<script>\n" + js + "</script>\n")
(here.parent / "activity" / "influence-line-explorer.html").write_text(art)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + TITLE + "\n"
       '<meta name="description" content="SEAA 3012 Civil Engineering Laboratory II, Lab S2 Influence Lines: notes, slides, interactive explorer, exercises and lab data sheet.">\n'
       + PREFS + "\n" + FONTS + "\n<style>\nhtml,body{margin:0}\n" + css + "</style>\n" + MJCONF + "\n</head>\n<body>\n" + body + "\n<script>\n" + js + "</script>\n</body>\n</html>\n")
(here.parent / "index.html").write_text(doc)
print("artifact", len(art), "bytes; index.html", len(doc), "bytes")
