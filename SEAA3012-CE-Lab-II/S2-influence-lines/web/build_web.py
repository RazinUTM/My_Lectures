"""Assemble the Lab S2 course page from web/src into two outputs:
   activity/influence-line-explorer.html  - body-only form published as the claude.ai artifact
   index.html (topic root)                - complete HTML document for GitHub Pages or any web server
"""
import pathlib
here = pathlib.Path(__file__).resolve().parent
src, shared = here / "src", here.parent / "shared"
css = (src / "style_v2.css").read_text() + "\n" + (src / "style_add.css").read_text()
body = "".join((src / p).read_text() for p in ["p1_start_notes.html", "p2_slides.html", "p3_explorer_ex_lab.html"])
js = (src / "app.js").read_text()
photo = (shared / "photo_b64.txt").read_text().strip()
qr = (shared / "qr_explorer_b64.txt").read_text().strip()
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">'
MJCONF = ('<script>\nwindow.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]},svg:{fontCache:"global"},\n'
          '  startup:{typeset:false,ready:function(){MathJax.startup.defaultReady();MathJax.startup.promise.then(function(){if(window.__mjReady)window.__mjReady();});}}};\n</script>\n'
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>')
TITLE = "<title>Lab S2 Influence Lines</title>"
body = body.replace("%%PHOTO%%", photo).replace("%%QR%%", qr)
assert "%%" not in body
art = (TITLE + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + FONTS + "\n<style>\n" + css + "</style>\n" + MJCONF
       + "\n" + body + "\n<script>\n" + js + "</script>\n")
(here.parent / "activity" / "influence-line-explorer.html").write_text(art)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + TITLE + "\n"
       '<meta name="description" content="SEAA 3012 Civil Engineering Laboratory II, Lab S2 Influence Lines: notes, slides, interactive explorer, exercises and lab data sheet.">\n'
       + FONTS + "\n<style>\nhtml,body{margin:0}\n" + css + "</style>\n" + MJCONF + "\n</head>\n<body>\n" + body + "\n<script>\n" + js + "</script>\n</body>\n</html>\n")
(here.parent / "index.html").write_text(doc)
print("artifact", len(art), "bytes; index.html", len(doc), "bytes")
