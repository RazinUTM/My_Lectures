"""Run each companion script, write its README, and pack both into a zip under code/.

The published site does not carry the zips (artifacts cannot serve archives): it serves the .py
files and the READMEs as text and the page builds the same zip in the browser (store method,
same order, same timestamp), so the local zips here are the reference the page is tested against.
Also writes code/manifest.json used by the site builders.
"""
import json, os, subprocess, sys, tempfile, zipfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..")
CODE = os.path.join(SITE, "code")

PACKS = [
    dict(id="shape", zip="seaa4243-shape-functions.zip", files=["fe_shape_functions.py"],
         title="Shape functions of the 4-node and 8-node rectangles",
         explorers=["shape"], part="Heat Transfer Part 1",
         does="N_i at a point, the two checks (Kronecker delta, partition of unity), "
              "interpolation of a nodal field, gradient and heat flux; maps of N_i.",
         use=["Check N_i, T(x, y) and the flux at any point of an assignment element.",
              "Plot the Q4 and Q8 shape functions for a report (plot_shape_functions)."]),
    dict(id="heat", zip="seaa4243-heat-q4.zip", files=["fe_heat_q4.py"],
         title="Steady 2D heat conduction with 4-node elements",
         explorers=["heat"], part="Heat Transfer Part 2",
         does="Element matrix [k] (s1-s4), source and edge-flux loads, assembly, "
              "known temperatures by row-column elimination, heat flows at the fixed nodes, "
              "temperature and flux at any point; mesh study; contour plot.",
         use=["Check your hand-assembled [K], {R} and temperatures (print res['K']).",
              "Run the mesh study a project needs: change Nx, Ny and watch the value converge.",
              "Change the edges dict and Q for your own plate, including a source in part of it."]),
    dict(id="ps", zip="seaa4243-plane-stress.zip", files=["fe_plane_stress.py"],
         title="Plane stress and plane strain with 4-node and 8-node elements",
         explorers=["cant", "stress"], part="Plane Stress Parts 1-3",
         does="[E], [B] and [k] by Gauss quadrature, consistent edge loads, the cantilever "
              "solve with reactions, stresses at any point, principal stresses, von Mises, "
              "averaged and unaveraged nodal stresses; Timoshenko beam check; contour plot.",
         use=["Check the 2 x 2 cantilever of the text step by step (K, U, reactions, stresses).",
              "Run the 4-node versus 8-node convergence study against beam theory.",
              "Show why the stress at a fixed corner keeps growing with refinement."]),
]
ALL = dict(id="all", zip="seaa4243-fem-python-all.zip",
           files=[f for p in PACKS for f in p["files"]],
           title="All companion code (shape functions, heat conduction, plane stress)")

STAMP = (2026, 10, 1, 0, 0, 0)


def run(script):
    """Run a script in a scratch directory; return its stdout, fail loudly on error."""
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(CODE, script)], cwd=tmp,
                           capture_output=True, text=True, timeout=300)
        if r.returncode:
            raise SystemExit(f"{script} failed:\n{r.stderr}")
        return r.stdout


def readme(pack, outputs):
    L = ["SEAA 4243 Finite Element Method - Python companion code",
         "=" * 56, "", pack["title"], ""]
    if "does" in pack:
        L += ["Goes with: " + pack["part"] + " (" + ", ".join(
            {"shape": "Shape Function Explorer", "heat": "Heat Conduction Explorer",
             "cant": "Cantilever Explorer", "stress": "Stress Recovery Explorer"}[e]
            for e in pack["explorers"]) + ")", "",
              "What it does", "  " + pack["does"], ""]
    L += ["Files"] + [f"  {f}" for f in pack["files"]] + [""]
    L += ["Quick start",
          "  1. Install Python 3.8 or newer, then:  pip install numpy matplotlib",
          "     (matplotlib is optional; without it the scripts skip the plots).",
          "  2. Run a script:  python " + pack["files"][0],
          "     It reproduces the course example. Compare the printout with the",
          "     expected output below: if they agree, your setup is right.",
          "  3. Read the docstring at the top of each file: notation, numbering,",
          "     units, and how to call the functions for your own problem.", ""]
    if "use" in pack:
        L += ["For an assignment or project"] + [f"  - {u}" for u in pack["use"]] + [
              "  - A hand calculation is still a hand calculation: use the script to",
              "    check your numbers and to go beyond what is practical by hand.", ""]
    for f in pack["files"]:
        L += [f"Expected output: python {f}", "-" * 40] + ["  " + s for s in outputs[f].rstrip().splitlines()] + [""]
    L += ["Licence",
          "  Code: MIT licence. Use, change and share it, keeping this notice.",
          "  Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.", ""]
    return "\r\n".join(L)          # CRLF so the file reads cleanly in Notepad too


def write_zip(pack, outputs):
    path = os.path.join(CODE, pack["zip"])
    folder = pack["zip"][:-4]
    text = readme(pack, outputs)
    with open(os.path.join(CODE, folder + "-README.txt"), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        def add(name, data):
            zi = zipfile.ZipInfo(f"{folder}/{name}", STAMP)
            zi.compress_type = zipfile.ZIP_STORED
            z.writestr(zi, data)
        add("README.txt", text)
        for f in pack["files"]:
            with open(os.path.join(CODE, f), encoding="utf-8") as fh:
                add(f, fh.read())
    return path


if __name__ == "__main__":
    outputs = {}
    for p in PACKS:
        for f in p["files"]:
            outputs[f] = run(f)
            print(f"ran {f}: {len(outputs[f].splitlines())} lines")
    manifest = {}
    for p in PACKS + [ALL]:
        path = write_zip(p, outputs)
        size = os.path.getsize(path)
        manifest[p["id"]] = dict(zip=p["zip"], files=p["files"], title=p["title"], readme=p["zip"][:-4] + "-README.txt",
                                 explorers=p.get("explorers", []), bytes=size)
        print(f"wrote {p['zip']}  {size / 1024:.1f} kB")
    with open(os.path.join(CODE, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    shutil.rmtree(os.path.join(CODE, "__pycache__"), ignore_errors=True)
