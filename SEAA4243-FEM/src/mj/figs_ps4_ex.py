"""Figures for the ANSYS demo page (Part 6) of the course site: the patch test of Example 4
(four rectangles of unequal size under uniform tension, the Stage 1 gate of the hybrid project)."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "figs_ps4_ex"
OUT.mkdir(exist_ok=True, parents=True)
rep = []


def fig_patch():
    """2 m x 1 m plate, node lines x = 0, 0.7, 2.0 and y = 0, 0.4, 1.0; rollers (u = 0) on the left edge,
    v = 0 at node 1 as well; uniform tension sigma_0 on the right edge."""
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    xs, ys = [0, 0.7, 2.0], [0, 0.4, 1.0]
    ax.set_xlim(-0.55, 2.95); ax.set_ylim(-0.42, 1.28); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 2.0, 1.0, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for x in xs[1:-1]: ax.plot([x, x], [0, 1], color=NAVY, lw=1.6)
    for y in ys[1:-1]: ax.plot([0, 2], [y, y], color=NAVY, lw=1.6)
    k = 0
    for y in ys:
        for x in xs:
            k += 1
            ax.add_patch(Circle((x, y), 0.045, facecolor=LIGHT, edgecolor=MAROON, lw=1.8, zorder=5))
            ax.text(x + (-0.11 if x == 2.0 else 0.06), y + 0.05, str(k), fontsize=12, color=MAROON, zorder=6)
    for y in ys:                                   # rollers: u = 0 on x = 0
        ax.add_patch(Polygon([(0, y), (-0.13, y + 0.07), (-0.13, y - 0.07)], closed=True, facecolor="none", edgecolor=INK, lw=1.4))
        ax.add_patch(Circle((-0.17, y), 0.035, facecolor="none", edgecolor=INK, lw=1.2))
    ax.plot([-0.24, -0.24], [-0.12, 1.12], color=INK, lw=1.2)
    ax.add_patch(Polygon([(0, 0), (-0.07, -0.13), (0.07, -0.13)], closed=True, facecolor="none", edgecolor=INK, lw=1.4))   # pin: v = 0 at node 1
    ax.plot([-0.11, 0.11], [-0.16, -0.16], color=INK, lw=1.2)
    for y in np.linspace(0.06, 0.94, 6):          # uniform tension on x = 2
        arrow(ax, (2.04, y), (2.36, y), color=MAROON, lw=2.0, ms=12)
    ax.text(2.42, 0.5, r"$\sigma_0$", fontsize=18, color=MAROON, va="center")
    dim(ax, (0, -0.3), (0.7, -0.3), "0.7", fontsize=13)
    dim(ax, (0.7, -0.3), (2.0, -0.3), "1.3", fontsize=13)
    ax.text(-0.5, 0.2, "0.4", fontsize=13, color=INK, va="center", ha="left")
    ax.text(-0.5, 0.7, "0.6", fontsize=13, color=INK, va="center", ha="left")
    return save_svg(fig, OUT / "fig_patch.svg", "fig_patch",
                    "A 2 m by 1 m plate divided into four rectangles of unequal size by node lines at x = 0, 0.7 and 2.0 m and y = 0, 0.4 and 1.0 m, "
                    "nodes numbered 1 to 9 from the bottom left. Rollers on the left edge stop the horizontal displacement, a pin at node 1 also stops the vertical one, "
                    "and a uniform tension sigma zero pulls on the right edge.")
rep.append(fig_patch())

(OUT / "_report.json").write_text(json.dumps(rep))
print([r["name"] for r in rep])
