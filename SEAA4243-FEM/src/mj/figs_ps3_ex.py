"""Figures for the Plane Stress Part 3 page of the course site: pure bending of one Q4 element
(FEM by Hand Example 10.6) and the consistent loads of a three-node edge (text (3.51))."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "figs_ps3_ex"
OUT.mkdir(exist_ok=True, parents=True)
rep = []


def fig_bend():
    """(a) exact pure bending: fibres curve, ends stay plane and square; (b) one Q4: sides stay straight, corners shear.
    Both drawn for the field of Example 10.6, u = -k' x y (top fibre shortened, bottom stretched)."""
    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.3))
    a, b, th = 3.0, 1.6, 0.30          # length, depth, end rotation (rad) each side
    for ax in axs:
        ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.05, 1.45); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((-a / 2, -b / 2), a, b, facecolor="none", edgecolor=GREY, lw=1.2, ls=(0, (4, 3))))
    ax = axs[0]
    R = (a / 2) / np.sin(th)            # radius of the neutral axis; centre of curvature above the block
    cy = R
    phi = np.linspace(-th, th, 60)
    def arc(r): return r * np.sin(phi), cy - r * np.cos(phi)
    xt, yt = arc(R - b / 2); xb, yb = arc(R + b / 2)
    poly = np.vstack([np.column_stack([xb, yb]), np.column_stack([xt[::-1], yt[::-1]])])
    ax.add_patch(Polygon(poly, closed=True, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    xn, yn = arc(R); ax.plot(xn, yn, color=GREY, lw=1, ls=":")
    for s in (-1, 1):                   # end couples, drawn as curved arrows beside each end
        x0 = s * (R * np.sin(th) + 0.35)
        ax.add_patch(FancyArrowPatch((x0, 0.55), (x0, -0.75), connectionstyle=f"arc3,rad={0.55 * s}", arrowstyle="-|>", mutation_scale=14, color=TEAL, lw=1.8))
    ax.text(0, -1.45, "(a) exact: fibres curve,", ha="center", va="center", fontsize=13, color=INK)
    ax.text(0, -1.85, r"ends stay square, $\gamma_{xy}=0$", ha="center", va="center", fontsize=13, color=INK)
    ax = axs[1]
    def disp(x, y): return x - 2 * th / a * x * y, y
    pts = [disp(-a / 2, -b / 2), disp(a / 2, -b / 2), disp(a / 2, b / 2), disp(-a / 2, b / 2)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for (x, y) in pts:
        ax.add_patch(Circle((x, y), 0.07, facecolor=LIGHT, edgecolor=MAROON, lw=2, zorder=5))
    xr, yr = pts[2]
    ax.text(xr + 0.15, yr + 0.05, r"$\neq 90^\circ$", fontsize=13, color=MAROON, va="bottom")
    ax.text(0, -1.45, "(b) one Q4: sides stay straight,", ha="center", va="center", fontsize=13, color=INK)
    ax.text(0, -1.85, r"corners shear, $\gamma_{xy}=-\kappa' x\neq0$", ha="center", va="center", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_bend.svg", "fig_bend",
                    "Pure bending of a block. Left, exact: the top and bottom fibres curve and the ends stay square to them. Right, one four-node element: its sides stay straight, so the ends can rotate only by shearing the corners")
rep.append(fig_bend())


def fig_edge_loads():
    """A uniform edge load q over a side of length l: one 8-node edge (l/6, 2l/3, l/6) against two 4-node edges (l/4, l/2, l/4)."""
    fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.7))
    L = 2.4
    for k, ax in enumerate(axs):
        ax.set_xlim(-1.0, 2.3); ax.set_ylim(-0.45, L + 0.45); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((-0.9, 0), 0.9, L, facecolor=FILL, edgecolor=NAVY, lw=2.0))
        ax.plot([0, 0], [0, L], color=NAVY, lw=2.6)
    shares = [(1 / 6, 2 / 3, 1 / 6, r"$q\ell/6$", r"$2q\ell/3$", r"$q\ell/6$", "one 8-node side"),
              (1 / 4, 1 / 2, 1 / 4, r"$q\ell/4$", r"$q\ell/2$", r"$q\ell/4$", "two 4-node sides")]
    for ax, (f1, f2, f3, l1, l2, l3, title) in zip(axs, shares):
        ys = [0, L / 2, L]
        for y, f, lab in zip(ys, [f1, f2, f3], [l3, l2, l1]):
            ln = 2.0 * f
            arrow(ax, (0.16, y + ln / 2), (0.16, y - ln / 2), color=MAROON, lw=2.4, ms=14)
            ax.text(0.42, y, lab, ha="left", va="center", fontsize=17, color=MAROON)
            ax.add_patch(Circle((0, y), 0.08, facecolor=LIGHT, edgecolor=MAROON, lw=2, zorder=5))
        if title.startswith("two"):
            ax.plot([-0.9, 0], [L / 2, L / 2], color=NAVY, lw=1.4)
        ax.text(0.65, L + 0.3, title, ha="center", va="bottom", fontsize=14, color=INK)
        ax.text(0.65, -0.3, r"total $q\ell$", ha="center", va="top", fontsize=14, color=INK)
    return save_svg(fig, OUT / "fig_edge_loads.svg", "fig_edge_loads",
                    "A uniform load q over a side of length l. Left, one eight-node side: q l over 6 at each corner and two thirds of q l at the mid-side node. Right, the same side as two four-node sides: q l over 4, q l over 2, q l over 4")
rep.append(fig_edge_loads())

(OUT / "_report.json").write_text(json.dumps(rep))
print([r["name"] for r in rep])
