"""Copy the built labs (Explorers) into the site as full HTML documents (GitHub Pages serves them raw).

The site copies get a thin bar with a way back to the course home and to the Python code. It shows
only when the Explorer is opened on its own: inside a part page's iframe (same origin, so
window.frameElement is set) the part page already has these links."""
import pathlib
SITE = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = pathlib.Path(__file__).resolve().parent.parent / "mj" / "labs" / "out"
SK = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
      '<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style>\n</head>\n<body>\n')
CODE = {"shape": "../01-heat-transfer-1/index.html#lab-code", "heat": "../02-heat-transfer-2/index.html#lab-code",
        "cant": "../index.html", "stress": "../index.html"}
LICENCE = "https://github.com/RazinUTM/My_Lectures/blob/main/SEAA4243-FEM/LICENSE.md"
A = "color:#830f3e;text-decoration:none;font-weight:600"
for name in ["shape", "heat", "cant", "stress"]:
    src = (OUT / f"{name}.html").read_text()
    bar = (f'<nav id="sitebar" hidden aria-label="Course" style="display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;'
           f'padding:8px max(16px,env(safe-area-inset-left,0px));border-bottom:1px solid #d6d8d0;background:#f5f4ef;font:600 13.5px system-ui,-apple-system,sans-serif">'
           f'<a href="../index.html" style="{A}">⌂ SEAA 4243 · Course home</a>'
           f'<a href="{CODE[name]}" style="{A}">⤓ Python code</a></nav>'
           '<script>try{if(!window.frameElement)document.getElementById("sitebar").hidden=false;}catch(e){}</script>\n')
    foot = ('<footer id="sitefoot" hidden style="padding:14px max(16px,env(safe-area-inset-left,0px)) 22px;border-top:1px solid #ded5d0;'
            'color:#6b5f63;font:12.5px/1.5 system-ui,-apple-system,sans-serif;max-width:900px">'
            '© 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia (Faculty of Civil Engineering). '
            'Free to share and adapt for non-commercial teaching and learning, with credit (CC BY-NC-SA 4.0); the code is MIT-licensed. '
            f'The lecturer\'s avatar and some other items are excepted: see the <a href="{LICENCE}" target="_blank" rel="noopener" style="color:#830f3e">licence</a>.</footer>'
            '<script>try{if(!window.frameElement)document.getElementById("sitefoot").hidden=false;}catch(e){}</script>\n')
    (SITE / "labs" / f"{name}.html").write_text(SK + bar + src + foot + "\n</body>\n</html>\n")
    print(name, "synced", len(src) // 1024, "KB")
