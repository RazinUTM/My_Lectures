"""Figures for the worked examples of Plane Stress Part 1 (course site): book Chapter 9 geometries."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_ps1_ex")
OUT.mkdir(exist_ok=True, parents=True)
rep = []


def vhatch(ax, y0, y1, x, step=0.25, L=0.2):
    for yy in np.arange(y0, y1 + 1e-9, step):
        ax.plot([x, x - 0.22], [yy, yy + L], color=NAVY, lw=1.1)


def fig_ps1_el():
    """Element of Example 1 (book Example 9.1): 0.6 m by 0.4 m, nodes, dofs, the point and the centre."""
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    A, B = 4.5, 3.0                     # drawing units for 0.6 m by 0.4 m
    ax.set_xlim(-1.6, 6.4); ax.set_ylim(-1.1, 4.0); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for (x, y, lab) in [(0, 0, "1"), (A, 0, "2"), (A, B, "3"), (0, B, "4")]:
        node(ax, x, y, lab, r=0.2)
        arrow(ax, (x + 0.22, y), (x + 0.9, y), color=TEAL, lw=1.8, ms=12)
        arrow(ax, (x, y + 0.22), (x, y + 0.9), color=TEAL, lw=1.8, ms=12)
        ax.text(x + 0.95, y - 0.12, rf"$u_{lab}$", fontsize=14, color=TEAL, va="top")
        ax.text(x - 0.12, y + 0.95, rf"$v_{lab}$", fontsize=14, color=TEAL, ha="right")
    px, py = 0.15 / 0.6 * A, 0.3 / 0.4 * B
    ax.plot(px, py, "x", color=MAROON, ms=11, mew=2.4); ax.text(px + 0.2, py - 0.05, r"$(0.15,\,0.3)$", fontsize=14, color=MAROON, va="top")
    ax.plot(A / 2, B / 2, "x", color=INK, ms=11, mew=2.4); ax.text(A / 2 + 0.2, B / 2 - 0.05, "centre", fontsize=14, va="top")
    dim(ax, (0, -0.6), (A, -0.6), r"$0.6\ \mathrm{m}$", side="below")
    dim(ax, (-1.0, 0), (-1.0, B), r"$0.4\ \mathrm{m}$", side="left")
    return save_svg(fig, OUT / "fig_ps1_el.svg", "fig_ps1_el", "Four-node element 0.6 m by 0.4 m with nodes 1 to 4 anticlockwise, the dofs u and v at each node, the point (0.15, 0.3) and the centre marked")
rep.append(fig_ps1_el())


def fig_ps1_hole():
    """Plate with a rectangular hole (book Example 9.5): 16 nodes in rows of four, 8 elements, left side fixed, traction q on the right."""
    fig, ax = plt.subplots(figsize=(7.8, 5.6))
    h = 1.6
    ax.set_xlim(-1.2, 3 * h + 2.4); ax.set_ylim(-0.7, 3 * h + 0.6); ax.set_aspect("equal"); ax.axis("off")
    cells = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    for e, (i, j) in enumerate(cells):
        ax.add_patch(Rectangle((i * h, j * h), h, h, facecolor=FILL, edgecolor=NAVY, lw=1.6))
        ax.add_patch(Rectangle((i * h + h / 2 - 0.22, j * h + h / 2 - 0.22), 0.44, 0.44, facecolor=LIGHT, edgecolor=NAVY, lw=1.1))
        ax.text(i * h + h / 2, j * h + h / 2, str(e + 1), ha="center", va="center", fontsize=14, color=NAVY)
    ax.text(1.5 * h, 1.5 * h, "hole", ha="center", va="center", fontsize=15, color=GREY, style="italic")
    k = 1
    for j in range(4):
        for i in range(4):
            node(ax, i * h, j * h, str(k), r=0.22, fontsize=12); k += 1
    vhatch(ax, 0, 3 * h, -0.25)
    ax.plot([-0.25, -0.25], [0, 3 * h], color=NAVY, lw=1.6)
    ax.text(-0.75, 1.5 * h, r"$u=v=0$", ha="center", va="center", fontsize=14, color=MAROON, rotation=90)
    for y in np.linspace(0.2, 3 * h - 0.2, 8):
        arrow(ax, (3 * h + 0.3, y), (3 * h + 1.1, y), color=MAROON, lw=1.8, ms=12)
    ax.text(3 * h + 1.25, 1.5 * h, r"$q$", ha="left", va="center", fontsize=18, color=MAROON)
    dim(ax, (3 * h + 1.9, 0), (3 * h + 1.9, h), r"$h$", side="right")
    return save_svg(fig, OUT / "fig_ps1_hole.svg", "fig_ps1_hole", "Plate with a rectangular hole: sixteen nodes numbered in rows of four from the bottom left, eight elements numbered row by row around the hole, the left side fixed and a traction q pulling the right side")
rep.append(fig_ps1_hole())

(OUT / "_report.json").write_text(json.dumps(rep))
print([r["name"] for r in rep])
