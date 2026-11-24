"""Helper: render a dict of LaTeX equations to SVG via MathJax (node), return inline-svg strings."""
import json, os, subprocess, pathlib

HERE = pathlib.Path(__file__).parent
NODE = "node"

def render(items, outdir, em=44, color="#1b2330"):
    """items: list of dicts {name, tex, [em], [color], [display], [alt]}"""
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    for it in items:
        it.setdefault("em", em); it.setdefault("color", color)
    f = outdir / "_items.json"
    f.write_text(json.dumps(items))
    r = subprocess.run([NODE, str(HERE / "render_eq.js"), str(f), str(outdir)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    rep = json.loads((outdir / "_report.json").read_text())
    return {x["name"]: x for x in rep}

def svg_text(outdir, name):
    return (pathlib.Path(outdir) / f"{name}.svg").read_text()
