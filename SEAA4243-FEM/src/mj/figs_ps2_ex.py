"""Figures for the Plane Stress Part 2 worked examples (FEM by Hand, Examples 9.2–9.4 and 9.6)."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "figs_ps2_ex"
OUT.mkdir(exist_ok=True, parents=True)
rep = []


def vhatch(ax, y0, y1, x, step=0.2, L=0.18):
    for yy in np.arange(y0, y1 + 1e-9, step):
        ax.plot([x, x - 0.22], [yy, yy + L], color=NAVY, lw=1.1)


def fig_v1_square():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    A = 3.0
    ax.set_xlim(-1.5, 6.6); ax.set_ylim(-1.0, 3.7); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), A, A, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for n, (x, y) in enumerate([(0, 0), (A, 0), (A, A), (0, A)]):
        node(ax, x, y, str(n + 1), r=0.2, fontsize=12)
    ax.text(A / 2, A / 2 + 0.45, r"$E=2.05\times10^{8}\ \mathrm{kN\,m^{-2}}$", ha="center", fontsize=12.5, color=INK)
    ax.text(A / 2, A / 2, r"$\nu=0.3,\ \ t=0.05\ \mathrm{m}$", ha="center", fontsize=12.5, color=INK)
    ax.text(A / 2, A / 2 - 0.45, r"$\gamma=78.5\ \mathrm{kN\,m^{-3}}$", ha="center", fontsize=12.5, color=INK)
    for y in np.linspace(0.35, A - 0.35, 5):
        arrow(ax, (A + 0.55, y + 0.45), (A + 0.55, y - 0.25), color=MAROON, lw=1.8, ms=12)
    ax.plot([A + 0.55, A + 0.55], [0.1, A - 0.1], color=MAROON, lw=1.0, alpha=0.5)
    ax.text(A + 0.85, A / 2 + 0.2, r"$p=-25\ \mathrm{kN\,m^{-1}}$", ha="left", va="center", fontsize=13, color=MAROON)
    ax.text(A + 0.85, A / 2 - 0.25, "in y, side 2–3", ha="left", va="center", fontsize=12, color=MAROON)
    dim(ax, (0, -0.5), (A, -0.5), r"$0.5\ \mathrm{m}$", side="below")
    dim(ax, (-0.75, 0), (-0.75, A), r"$0.5\ \mathrm{m}$", side="left")
    return save_svg(fig, OUT / "fig_v1_square.svg", "fig_v1_square",
                    "Square plane-stress element of side 0.5 m, thickness 0.05 m, E 2.05 times ten to the eight kilonewtons per square metre, Poisson's ratio 0.3, with a downward load of 25 kilonewtons per metre on its right side")
rep.append(fig_v1_square())


def fig_v2_mesh():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    h = 1.5
    ax.set_xlim(-0.8, 5.4); ax.set_ylim(-0.7, 3.6); ax.set_aspect("equal"); ax.axis("off")
    els = [(1, 0, 1), (2, 0, 1 + 0), (3, 1, 1), (4, 2, 1)]
    boxes = {1: (h, 0), 2: (0, h), 3: (h, h), 4: (2 * h, h)}
    for e, (x0, y0) in boxes.items():
        ax.add_patch(Rectangle((x0, y0), h, h, facecolor=FILL, edgecolor=NAVY, lw=2.0))
        cx, cy = x0 + h / 2, y0 + h / 2
        ax.add_patch(Rectangle((cx - 0.2, cy - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.1))
        ax.text(cx, cy, str(e), ha="center", va="center", fontsize=13, color=NAVY)
    pos = {1: (h, 0), 2: (2 * h, 0), 3: (0, h), 4: (h, h), 5: (2 * h, h), 6: (3 * h, h),
           7: (0, 2 * h), 8: (h, 2 * h), 9: (2 * h, 2 * h), 10: (3 * h, 2 * h)}
    for n, (x, y) in pos.items():
        node(ax, x, y, str(n), r=0.2, fontsize=11.5)
    ax.text(0.0, -0.35, r"node $i$: dofs $U_i=2i-1,\ V_i=2i$", ha="left", va="center", fontsize=12.5, color=INK)
    return save_svg(fig, OUT / "fig_v2_mesh.svg", "fig_v2_mesh",
                    "Four identical square elements: element 1 at the bottom between nodes 1, 2, 5 and 4; elements 2, 3 and 4 in a row above it on nodes 3 to 10")
rep.append(fig_v2_mesh())


def fig_v3_tension():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.0))
    A = 2.4
    for k, ax in enumerate(axs):
        ax.set_xlim(-1.0, A + 1.5); ax.set_ylim(-1.0, A + 0.6); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), A, A, facecolor=FILL, edgecolor=NAVY, lw=2.2))
        node(ax, 0, 0, "1", r=0.16, fontsize=12); node(ax, A, 0, "2", r=0.16, fontsize=12); node(ax, A, A, "3", r=0.16, fontsize=12); node(ax, 0, A, "4", r=0.16, fontsize=12)
        for y in np.linspace(0.3, A - 0.3, 5):
            arrow(ax, (A + 0.1, y), (A + 0.75, y), color=MAROON, lw=1.8, ms=12)
        ax.text(A + 0.85, A / 2, r"$\sigma$", ha="left", va="center", fontsize=16, color=MAROON)
        if k == 0:
            for (x, y, side) in [(0, 0, "left"), (0, A, "left"), (0, 0, "below"), (A, 0, "below")]:
                if side == "left":
                    ax.add_patch(Circle((x - 0.32, y), 0.12, facecolor=LIGHT, edgecolor=NAVY, lw=1.6)); ax.plot([x - 0.46, x - 0.46], [y - 0.25, y + 0.25], color=NAVY, lw=1.6)
                else:
                    ax.add_patch(Circle((x, y - 0.32), 0.12, facecolor=LIGHT, edgecolor=NAVY, lw=1.6)); ax.plot([x - 0.25, x + 0.25], [y - 0.46, y - 0.46], color=NAVY, lw=1.6)
            ax.text(A / 2, -0.8, "(a) rollers", ha="center", va="center", fontsize=14, color=INK)
        else:
            ax.add_patch(Rectangle((-0.25, -0.15), 0.25, A + 0.3, facecolor="#c9ced6", edgecolor="none"))
            vhatch(ax, -0.1, A, -0.25)
            ax.text(A / 2, -0.8, "(b) clamped", ha="center", va="center", fontsize=14, color=INK)
        ax.text(A / 2, A / 2, r"$1\times1\ \mathrm{m}$", ha="center", va="center", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_v3_tension.svg", "fig_v3_tension",
                    "Unit square plate pulled by a uniform stress on its right side: (a) on rollers along the left and bottom sides, (b) clamped along the left side")
rep.append(fig_v3_tension())

(OUT / "_report.json").write_text(json.dumps(rep))
print([r["name"] for r in rep])
