"""Run in browser: short scripts per part, edited and run with Pyodide (Python compiled to WebAssembly).

The panel sits in each part's Explorer tab, under the code card. The scripts import the course module
of that part, which the page fetches from ../code/ and writes into Pyodide's file system before a run.
Python runs in a Web Worker, so a long run never freezes the page and Stop can end it.

Only GitHub Pages (and a local server) load Pyodide; elsewhere, such as the claude.ai preview, the panel
shows the scripts and points to the course website."""
import html
import json

from sitelib import B, P, code_manifest

PAGES = "https://razinutm.github.io/My_Lectures/SEAA4243-FEM/"


def course_example(f):
    return (f"# The course example: the same as running  python {f}  on your computer.\n"
            f"# Its README lists the output to expect.\n"
            "import runpy\n"
            f'runpy.run_path("{f}", run_name="__main__")\n')


SCRIPTS = {
    1: [
        ("N at a point", "N pada satu titik",
         '''# Q4 element: shape functions, temperature and heat flux at one point.
# Change the numbers and press Run (or Ctrl+Enter).
from fe_shape_functions import shape_q4, dshape_q4, interpolate, flux

a, b = 2.0, 1.0                    # element size (m)
x, y = 1.5, 0.3                    # the point, LOCAL coordinates (m)
T = [100.0, 140.0, 160.0, 120.0]   # nodal temperatures T1..T4
k = 2.0                            # conductivity (W/m.K)

N = shape_q4(a, b, x, y)
print("N1..N4 =", N.round(4), "  sum =", round(N.sum(), 12))
print("T      =", round(interpolate(N, T), 4))
print("q      =", flux(dshape_q4(a, b, x, y), T, k).round(3), "W/m2")
'''),
        ("Maps of N1…N8", "Peta N1…N8",
         '''# Colour maps of the shape functions; nen = 4 or 8.
# Where does each N_i equal 1, and where is it negative?
from fe_shape_functions import plot_shape_functions, check

a, b, nen = 2.0, 1.0, 8
kron, pou = check(a, b, nen)
print("Kronecker delta:", kron, "  partition of unity:", pou)
plot_shape_functions(a, b, nen)
'''),
        ("Course example", "Contoh kursus", course_example("fe_shape_functions.py")),
    ],
    2: [
        ("Mesh study", "Kajian mesh",
         '''# The text's plate (Sec. 2.3): refine the mesh and watch T at the corner (1, 0).
# Try other k, Q or edge conditions.
from fe_heat_q4 import solve_plate, temperature_at, plot_temperature

edges = {"top": ("T", 0.0), "left": ("T", 0.0),
         "right": ("insulated",), "bottom": ("insulated",)}
for n in (2, 4, 8):
    res = solve_plate(L=1, H=1, Nx=n, Ny=n, kx=300, edges=edges, Q=600)
    print(f"{n} x {n}: T(1, 0) = {temperature_at(res, 1.0, 0.0)['T']:.4f} degC  (exact 0.5894)")
plot_temperature(res)
'''),
        ("[K] and {R}, 2 × 2 mesh", "[K] dan {R}, mesh 2 × 2",
         '''# Compare with your hand assembly: the global [K], the load vector {R}
# and the temperatures of the 2 x 2 mesh.
from fe_heat_q4 import solve_plate, print_matrix

edges = {"top": ("T", 0.0), "left": ("T", 0.0),
         "right": ("insulated",), "bottom": ("insulated",)}
res = solve_plate(L=1, H=1, Nx=2, Ny=2, kx=300, edges=edges, Q=600)
print_matrix(res["K"], name="[K]")
print("{R} =", res["R"].round(3))
print("T   =", res["T"].round(4))
'''),
        ("Course example", "Contoh kursus", course_example("fe_heat_q4.py")),
    ],
    3: [
        ("[E]: stress or strain", "[E]: stress atau strain",
         '''# [E] of text (3.10). Try nu = 0, 0.3 and 0.49:
# which case grows without limit as nu approaches 0.5?
from fe_plane_stress import E_matrix

E, nu = 200e6, 0.33                # N/m2, Poisson's ratio
print("plane stress [E] / 1e6 =")
print((E_matrix(E, nu, "stress") / 1e6).round(2))
print("plane strain [E] / 1e6 =")
print((E_matrix(E, nu, "strain") / 1e6).round(2))
'''),
        ("Strains, then stresses", "Strains, kemudian stresses",
         '''# One 4-node element: strains at a point from the nodal displacements,
# then stresses. Nodes 1-4 anticlockwise from the bottom-left corner.
import numpy as np
from fe_plane_stress import B_matrix, E_matrix

a, b = 2.0, 1.0                    # element size (m)
x, y = 1.0, 0.5                    # the point, LOCAL coordinates (m)
u = [0, 0, 1e-4, 0, 1.2e-4, -0.5e-4, 0, -0.4e-4]   # u1 v1 u2 v2 u3 v3 u4 v4 (m)

xi, eta = 2 * x / a - 1, 2 * y / b - 1             # natural coordinates
eps = B_matrix(4, a, b, xi, eta) @ np.array(u)     # exx, eyy, gamma_xy
sig = E_matrix(200e6, 0.33, "stress") @ eps        # sxx, syy, sxy (N/m2)
print("exx = %.3e, eyy = %.3e, gamma_xy = %.3e" % tuple(eps))
print("sxx = %.2f, syy = %.2f, sxy = %.2f kN/m2" % tuple(sig / 1e3))
'''),
        ("Course example", "Contoh kursus", course_example("fe_plane_stress.py")),
    ],
    4: [
        ("Element [k]", "[k] element",
         '''# [k] = t * integral [B]^T [E] [B] dA of one 4-node element, text (3.42).
# Check: every row sums to zero (a rigid-body shift needs no force).
import numpy as np
from fe_plane_stress import E_matrix, element_stiffness

np.set_printoptions(precision=1, suppress=True, linewidth=120)
a, b, t = 2.0, 1.0, 0.01
k = element_stiffness(4, a, b, E_matrix(200e6, 0.33), t)
print("[k] / 1e3 =")
print(k / 1e3)
print("row sums:", k.sum(axis=1).round(6))
'''),
        ("Cantilever mesh study", "Kajian mesh cantilever",
         '''# The text's cantilever: tip deflection against Timoshenko beam theory.
# Add finer meshes, or change nen to 8.
from fe_plane_stress import solve_cantilever, timoshenko_tip

base = dict(L=4.0, H=2.0, E=200e6, nu=0.33, t=0.01, q=-5000.0)
bend, shear = timoshenko_tip(**base)
print(f"Timoshenko beam: {bend + shear:.4f} m")
for Nx, Ny in [(2, 2), (4, 2), (8, 4), (16, 8)]:
    r = solve_cantilever(Nx=Nx, Ny=Ny, nen=4, **base)
    err = 100 * (-r["tip"] / (bend + shear) - 1)
    print(f"4-node {Nx:2d} x {Ny:<2d}  tip = {r['tip']:.4f} m  ({err:+.1f} %)")
'''),
        ("Course example", "Contoh kursus", course_example("fe_plane_stress.py")),
    ],
    5: [
        ("Stress at a point", "Stress pada satu titik",
         '''# Stresses at a point, then the principal stresses and von Mises (the Mohr circle).
# Move the point, or refine the mesh.
from fe_plane_stress import solve_cantilever, stress_at, principal, von_mises

r = solve_cantilever(L=4, H=2, Nx=2, Ny=2, E=200e6, nu=0.33, t=0.01, q=-5000)
s = stress_at(r, 3.5, 1.3) / 1e3                   # kN/m2
s1, s2, th = principal(s)
print("sxx, syy, sxy =", s.round(1), "kN/m2")
print(f"sigma1 = {s1:.1f}, sigma2 = {s2:.1f} kN/m2 at {th:.1f} deg")
print(f"von Mises = {von_mises(s):.1f} kN/m2")
'''),
        ("von Mises plot", "Plot von Mises",
         '''# Contour plot of the von Mises stress. Refine the mesh or change nen:
# where is it largest, and does that value settle?
from fe_plane_stress import solve_cantilever, plot_von_mises

r = solve_cantilever(L=4, H=2, Nx=8, Ny=4, E=200e6, nu=0.33, t=0.01, q=-5000, nen=8)
plot_von_mises(r)
'''),
        ("Course example", "Contoh kursus", course_example("fe_plane_stress.py")),
    ],
}


def run_card(n, slug, pack_id, rel="../code/"):
    """The Run in browser panel of part n."""
    files = code_manifest()[pack_id]["files"]
    sc = SCRIPTS[n]
    seg = "".join(f'<button type="button" data-py="{i}" aria-pressed="{str(i == 0).lower()}">{B(e, m)}</button>'
                  for i, (e, m, _) in enumerate(sc))
    data = json.dumps([c for _, _, c in sc]).replace("</", "<\\/")
    here = PAGES + slug + "/index.html#lab-run"
    return (f'<div class="card pyrun" id="run" data-part="{n}" data-base="{rel}" data-files="{",".join(files)}" data-pages="{here}">'
            f'<h2>{B("Run the code in your browser", "Jalankan kod dalam browser")} <span class="trial">{B("trial", "percubaan")}</span></h2>'
            + P("Edit a short script and run it here, with no installation. Python runs on your own device; nothing is sent anywhere. "
                "The first run downloads Python, about 9 MB (about 20 MB once a script plots), and takes 10–30 s; later runs take a second or two.",
                "Ubah skrip pendek dan jalankan di sini, tanpa pemasangan. Python berjalan pada peranti anda sendiri; tiada apa yang dihantar ke mana-mana. "
                "Larian pertama memuat turun Python, lebih kurang 9 MB (lebih kurang 20 MB apabila skrip membuat plot), dan mengambil 10–30 s; larian seterusnya sesaat dua.", "lead")
            + f'<div class="seg pyseg" role="group" aria-label="Script">{seg}</div>'
            f'<script type="application/json" class="pysrc">{data}</script>'
            f'<textarea class="pyedit" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" wrap="off" aria-label="Python script" rows="12"></textarea>'
            f'<div class="pybar"><button class="btn" type="button" data-pyrun>▶ {B("Run", "Jalankan")}</button>'
            f'<button class="btn ghost" type="button" data-pystop hidden>■ {B("Stop", "Henti")}</button>'
            f'<button class="btn ghost" type="button" data-pyreset disabled>{B("Reset script", "Set semula skrip")}</button>'
            f'<span class="pystat" aria-live="polite"></span></div>'
            f'<pre class="pyout" hidden></pre><div class="pyfigs"></div>'
            f'<p class="pynote">{B("Ctrl+Enter (⌘+Enter) runs. Your edits are kept in this browser; Reset script brings back the original. "
                                   "For an assignment or a project, download the code above and run it on your computer.",
                                   "Ctrl+Enter (⌘+Enter) menjalankan skrip. Suntingan anda disimpan dalam browser ini; Set semula skrip memulihkan yang asal. "
                                   "Untuk assignment atau projek, muat turun kod di atas dan jalankan di komputer anda.")}</p>'
            '</div>')
