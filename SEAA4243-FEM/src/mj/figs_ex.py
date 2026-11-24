"""Figures for the worked examples (answer schemes) of the course site: book Chapter 8 geometries."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_ex")
OUT.mkdir(exist_ok=True, parents=True)
rep = []

def hatch(ax, x0, x1, y, below=True, step=0.2, L=0.18):
    for xx in np.arange(x0, x1, step):
        ax.plot([xx, xx + L], [y - (0.22 if below else -0.22), y], color=NAVY, lw=1.1)

def vhatch(ax, y0, y1, x, left=True, step=0.2, L=0.18):
    for yy in np.arange(y0, y1, step):
        ax.plot([x, x - (0.22 if left else -0.22)], [yy, yy + L], color=NAVY, lw=1.1)

def fig_tri():
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    L = 3.0
    ax.set_xlim(-0.9, 4.3); ax.set_ylim(-0.8, 3.7); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Polygon([(0, 0), (L, 0), (L / 2, L)], closed=True, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    ax.plot([L / 2, L / 2], [0, L], color=GREY, lw=1, ls=":")
    arrow(ax, (-0.5, 0), (3.9, 0), color=INK, lw=1.2, ms=12); ax.text(4.0, -0.02, r"$x$", fontsize=16, va="center")
    arrow(ax, (0, -0.5), (0, 3.5), color=INK, lw=1.2, ms=12); ax.text(0.1, 3.5, r"$y$", fontsize=16, va="center")
    node(ax, 0, 0, "1"); node(ax, L, 0, "2"); node(ax, L / 2, L, "3")
    ax.text(-0.25, -0.38, r"$(0,0)$", ha="center", fontsize=14); ax.text(L + 0.1, -0.38, r"$(L,0)$", ha="center", fontsize=14)
    ax.text(L / 2 + 0.25, L + 0.12, r"$(L/2,\,L)$", ha="left", fontsize=14)
    ax.plot(L / 2, L / 3, "x", color=MAROON, ms=9, mew=2); ax.text(L / 2 + 0.15, L / 3 - 0.02, "centroid", fontsize=13, va="center", color=MAROON)
    return save_svg(fig, OUT / "fig_tri.svg", "fig_tri", "Three-node triangle with nodes at (0, 0), (L, 0) and (L/2, L), and its centroid marked")
rep.append(fig_tri())

def fig_pp83():
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    A, B = 4.0, 3.0
    ax.set_xlim(-1.5, 5.6); ax.set_ylim(-0.9, 3.8); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for (x, y, lab, pos) in [(0, 0, "1", (-0.35, -0.35)), (A, 0, "2", (0.35, -0.35)), (A, B, "3", (0.35, 0.35)), (0, B, "4", (-0.35, 0.35))]:
        node(ax, x, y, lab)
    ax.text(-0.3, -0.5, r"$1\!:\,20\,^{\circ}\mathrm{C}$", ha="right", va="top", fontsize=14, color=MAROON)
    ax.text(A + 0.3, -0.5, r"$2\!:\,40\,^{\circ}\mathrm{C}$", ha="left", va="top", fontsize=14, color=MAROON)
    ax.text(A + 0.3, B + 0.45, r"$3\!:\,60\,^{\circ}\mathrm{C}$", ha="left", va="bottom", fontsize=14, color=MAROON)
    ax.text(-0.3, B + 0.45, r"$4\!:\,30\,^{\circ}\mathrm{C}$", ha="right", va="bottom", fontsize=14, color=MAROON)
    ax.plot(2.0, 1.5, "x", color=INK, ms=10, mew=2.2); ax.text(2.2, 1.5, "centre", fontsize=13, va="center")
    ax.plot(1.0, 2.0, "x", color=INK, ms=10, mew=2.2); ax.text(1.2, 2.05, r"$(0.1,\,0.2)$", fontsize=13, va="center")
    dim(ax, (0, -0.45), (A, -0.45), r"$0.4\ \mathrm{m}$", side="below")
    dim(ax, (-0.9, 0), (-0.9, B), r"$0.3\ \mathrm{m}$", side="left")
    arrow(ax, (-1.4, 1.6), (-1.4, 2.5), color=INK, lw=1, ms=10); ax.text(-1.3, 2.55, r"$y$", fontsize=13)
    arrow(ax, (1.6, -0.85), (2.5, -0.85), color=INK, lw=1, ms=10); ax.text(2.55, -0.8, r"$x$", fontsize=13)
    return save_svg(fig, OUT / "fig_pp83.svg", "fig_pp83", "Four-node element 0.4 m by 0.3 m with nodal temperatures 20, 40, 60 and 30 degrees, the centre and the point (0.1, 0.2) marked")
rep.append(fig_pp83())

def fig_sq_flux():
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    A = 3.0
    ax.set_xlim(-1.4, 6.2); ax.set_ylim(-0.9, 3.7); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), A, A, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    node(ax, 0, 0, "1"); node(ax, A, 0, "2"); node(ax, A, A, "3"); node(ax, 0, A, "4")
    ax.text(A / 2, A / 2 + 0.45, r"$k=450\ \mathrm{W\,(m\,K)^{-1}}$", ha="center", fontsize=13, color=INK)
    ax.text(A / 2, A / 2, r"$t=0.005\ \mathrm{m}$", ha="center", fontsize=13, color=INK)
    ax.text(A / 2, A / 2 - 0.45, r"$Q=10^{7}\ \mathrm{W\,m^{-3}}$", ha="center", fontsize=13, color=INK)
    for y in np.linspace(0.4, A - 0.4, 5):
        arrow(ax, (A + 0.9, y), (A + 0.05, y), color=MAROON, lw=1.8, ms=12)
    ax.text(A + 1.05, A / 2 + 0.25, r"$q_n=10^{6}\ \mathrm{W\,m^{-2}}$", ha="left", va="center", fontsize=13, color=MAROON)
    ax.text(A + 1.05, A / 2 - 0.25, "(inward)", ha="left", va="center", fontsize=12, color=MAROON)
    dim(ax, (0, -0.45), (A, -0.45), r"$0.025\ \mathrm{m}$", side="below")
    dim(ax, (-0.75, 0), (-0.75, A), r"$0.025\ \mathrm{m}$", side="left")
    return save_svg(fig, OUT / "fig_sq_flux.svg", "fig_sq_flux", "Square element of side 0.025 m with conductivity 450, thickness 0.005 m, heat generation ten to the seven, and an inward flux of ten to the six on its right side")
rep.append(fig_sq_flux())

def fig_mesh_flux():
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    A = 3.0; h = A / 2
    ax.set_xlim(-2.6, 6.4); ax.set_ylim(-1.1, 4.0); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), A, A, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    ax.plot([h, h], [0, A], color=NAVY, lw=1.4); ax.plot([0, A], [h, h], color=NAVY, lw=1.4)
    for e, (cx, cy) in enumerate([(h / 2, h / 2), (3 * h / 2, h / 2), (h / 2, 3 * h / 2), (3 * h / 2, 3 * h / 2)]):
        ax.add_patch(Rectangle((cx - 0.2, cy - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.1))
        ax.text(cx, cy, str(e + 1), ha="center", va="center", fontsize=13, color=NAVY)
    k = 1
    for j in range(3):
        for i in range(3):
            node(ax, i * h, j * h, str(k), r=0.17, fontsize=12); k += 1
    ax.add_patch(Rectangle((-0.3, 0), 0.3, A, facecolor="#c9ced6", edgecolor="none"))
    ax.text(-0.5, A / 2, r"$T=400\ \mathrm{K}$", ha="right", va="center", fontsize=15, color=MAROON, rotation=90)
    hatch(ax, 0, A, 0, below=True); hatch(ax, 0, A, A, below=False)
    ax.text(A / 2, -0.35, "insulated", ha="center", va="top", fontsize=13, color=NAVY); ax.text(A / 2, A + 0.35, "insulated", ha="center", va="bottom", fontsize=13, color=NAVY)
    for y in np.linspace(0.3, A - 0.3, 6):
        arrow(ax, (A + 0.9, y), (A + 0.05, y), color=MAROON, lw=1.8, ms=12)
    ax.text(A + 1.05, A / 2 + 0.25, r"$q_n=10^{6}\ \mathrm{W\,m^{-2}}$", ha="left", va="center", fontsize=13, color=MAROON)
    ax.text(A + 1.05, A / 2 - 0.25, "(inward)", ha="left", va="center", fontsize=12, color=MAROON)
    dim(ax, (0, -0.8), (A, -0.8), r"$0.05\ \mathrm{m}$", side="below")
    dim(ax, (-1.6, 0), (-1.6, A), r"$0.05\ \mathrm{m}$", side="left")
    return save_svg(fig, OUT / "fig_mesh_flux.svg", "fig_mesh_flux", "Square plate 0.05 m, four elements, nine nodes numbered left to right and bottom to top: left side at 400 K, inward flux on the right side, top and bottom insulated")
rep.append(fig_mesh_flux())

(OUT / "_report.json").write_text(json.dumps(rep))
print([r["name"] for r in rep])
