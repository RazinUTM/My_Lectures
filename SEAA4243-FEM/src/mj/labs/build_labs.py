import base64, pathlib, sys
HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
css, core, ui = (HERE / "lab.css").read_text(), (HERE / "fe_core.js").read_text(), (HERE / "lab_ui.js").read_text()
# the lecturer's avatar in every Explorer's header, inlined so a single-file Explorer stays one file
AV = HERE.parent.parent.parent / "shared" / "avatar"   # src/mj/labs -> SEAA4243-FEM
POSE = {"shape": "present", "heat": "explain", "cant": "ok", "stress": "think"}
for name in ["shape", "heat", "cant", "stress"]:
    src = (HERE / f"{name}.src.html").read_text()
    uri = "data:image/webp;base64," + base64.b64encode((AV / f"{POSE[name]}.webp").read_bytes()).decode()
    img = f'<img class="labava" src="{uri}" alt="" title="Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin">'
    assert src.count('<header class="top">') == 1, name
    src = src.replace('<header class="top">', '<header class="top">' + img, 1)
    assert "/*{{CSS}}*/" in src and "/*{{CORE}}*/" in src and "/*{{UI}}*/" in src, name
    html = src.replace("/*{{CSS}}*/", css).replace("/*{{CORE}}*/", core).replace("/*{{UI}}*/", ui)
    assert "</script" not in core and "</script" not in ui
    (OUT / f"{name}.html").write_text(html)
    print(name, len(html) // 1024, "KB")
