import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *
from fe_heat import solve, klocal
import matplotlib.tri as mtri

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w10")
OUT.mkdir(exist_ok=True, parents=True)
rep = []

def mesh_base(ax, L=3.0, shade=None, local=None, point=None, hatch=True):
    h = L / 2
    for i in range(2):
        for j in range(2):
            e = i * 2 + j + 1
            fc = AMBER if (shade == e) else FILL
            ax.add_patch(Rectangle((j * h, i * h), h, h, facecolor=fc, edgecolor=NAVY, lw=2))
            ax.add_patch(Rectangle((j * h + h / 2 - 0.2, i * h + h / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.3))
            ax.text(j * h + h / 2, i * h + h / 2, str(e), ha="center", va="center", fontsize=15, color=NAVY)
    n = 1
    for i in range(3):
        for j in range(3):
            node(ax, j * h, i * h, str(n), r=0.16, fontsize=13)
            n += 1
    if local:
        # local numbers of element `local` in teal next to its nodes
        e = local; i, j = (e - 1) // 2, (e - 1) % 2
        corners = [(j * h, i * h), ((j + 1) * h, i * h), ((j + 1) * h, (i + 1) * h), (j * h, (i + 1) * h)]
        offs = [(0.28, 0.26), (-0.28, 0.26), (-0.28, -0.3), (0.28, -0.3)]
        for k, ((x, y), (dx, dy)) in enumerate(zip(corners, offs), 1):
            ax.text(x + dx, y + dy, f"({k})", ha="center", va="center", fontsize=13, color=TEAL, fontweight="bold")
    if hatch:
        for xx in np.arange(0.0, L, 0.22):
            ax.plot([xx, xx + 0.2], [-0.3, 0], color=NAVY, lw=1.2)
        for yy in np.arange(0.0, L, 0.22):
            ax.plot([L, L + 0.3], [yy, yy + 0.2], color=NAVY, lw=1.2)
        ax.text(L / 2, L + 0.22, r"$T=0\,^{\circ}\mathrm{C}$", ha="center", va="bottom", fontsize=15, color=MAROON)
        ax.text(-0.3, L / 2, r"$T=0\,^{\circ}\mathrm{C}$", ha="right", va="center", fontsize=15, color=MAROON, rotation=90)
    if point:
        px, py, lab = point
        X, Y = px / 1.0 * L, py / 1.0 * L
        ax.plot([X], [Y], marker="x", markersize=13, markeredgewidth=3, color=MAROON, zorder=7)
        ax.text(X - 0.12, Y - 0.14, lab, ha="right", va="top", fontsize=13, color=MAROON)

def fig_mesh_e1():
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_xlim(-1.1, 4.2); ax.set_ylim(-1.0, 4.1); ax.set_aspect("equal"); ax.axis("off")
    mesh_base(ax, shade=1, local=1)
    ax.plot([0, 3], [-0.6, -0.6], color=INK, lw=1.2)
    for xx in [0, 1.5, 3]:
        ax.plot([xx, xx], [-0.7, -0.5], color=INK, lw=1.2)
    ax.text(0.75, -0.75, r"$0.5\ \mathrm{m}$", ha="center", va="top", fontsize=14, color=INK); ax.text(2.25, -0.75, r"$0.5\ \mathrm{m}$", ha="center", va="top", fontsize=14, color=INK)
    return save_svg(fig, OUT / "fig_mesh_e1.svg", "fig_mesh_e1", "Two-by-two mesh with element 1 shaded; its local node numbers (1) to (4) sit beside global nodes 1, 2, 5, 4")
rep.append(fig_mesh_e1())

def fig_mesh_e2():
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_xlim(-1.1, 4.2); ax.set_ylim(-1.0, 4.1); ax.set_aspect("equal"); ax.axis("off")
    mesh_base(ax, shade=2, local=2)
    return save_svg(fig, OUT / "fig_mesh_e2.svg", "fig_mesh_e2", "Two-by-two mesh with element 2 shaded; its local node numbers (1) to (4) sit beside global nodes 2, 3, 6, 5")
rep.append(fig_mesh_e2())

def fig_mesh_point():
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_xlim(-1.1, 4.2); ax.set_ylim(-1.0, 4.1); ax.set_aspect("equal"); ax.axis("off")
    mesh_base(ax, shade=1, local=1, point=(0.3, 0.2, r"$(0.3,\,0.2)$"))
    return save_svg(fig, OUT / "fig_mesh_point.svg", "fig_mesh_point", "Two-by-two mesh with the point (0.3, 0.2) m marked inside element 1")
rep.append(fig_mesh_point())

def fig_mesh_T():
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_xlim(-1.1, 4.2); ax.set_ylim(-1.0, 4.1); ax.set_aspect("equal"); ax.axis("off")
    mesh_base(ax, hatch=True)
    vals = {2: "0.482", 3: "0.621", 5: "0.386", 6: "0.482"}
    pos = {2: (1.5, -0.45), 3: (3.0, -0.45), 5: (1.5, 1.85), 6: (3.45, 1.5)}
    for n, v in vals.items():
        x, y = pos[n]
        ax.text(x, y, rf"$T_{n}={v}$", ha="center" if n != 6 else "left", va="center", fontsize=13, color=TEAL, fontweight="bold")
    return save_svg(fig, OUT / "fig_mesh_T.svg", "fig_mesh_T", "Two-by-two mesh with the solved nodal temperatures written at the free nodes 2, 3, 5 and 6")
rep.append(fig_mesh_T())

def fig_edge_flux():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_xlim(-0.8, 9.2); ax.set_ylim(-1.1, 3.2); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.0, 2.0
    # left: distributed flux
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2))
    for (x, y), lab in zip([(0, 0), (A, 0), (A, B), (0, B)], ["1", "2", "3", "4"]):
        node(ax, x, y, lab, r=0.14, fontsize=12)
    for y in np.linspace(0.25, B - 0.25, 5):
        arrow(ax, (A + 0.9, y), (A, y), color=TEAL, lw=2, ms=13)
    ax.text(A + 1.0, B / 2, r"$q_b$", ha="left", va="center", fontsize=19, color=TEAL)
    ax.text(A / 2, -0.55, r"$\mathrm{distributed\ inward\ flux\ on\ edge\ 2\!-\!3}$", ha="center", va="top", fontsize=13, color=INK)
    # arrow between
    arrow(ax, (4.3, B / 2), (5.0, B / 2), color=AMBER, lw=4, ms=26)
    # right: nodal equivalents
    x0 = 5.9
    ax.add_patch(Rectangle((x0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2))
    for (x, y), lab in zip([(x0, 0), (x0 + A, 0), (x0 + A, B), (x0, B)], ["1", "2", "3", "4"]):
        node(ax, x, y, lab, r=0.14, fontsize=12)
    arrow(ax, (x0 + A + 1.0, 0), (x0 + A + 0.15, 0), color=MAROON, lw=3, ms=18)
    arrow(ax, (x0 + A + 1.0, B), (x0 + A + 0.15, B), color=MAROON, lw=3, ms=18)
    ax.text(x0 + A + 1.1, 0, r"$\dfrac{q_b\,b}{2}$", ha="left", va="center", fontsize=17, color=MAROON)
    ax.text(x0 + A + 1.1, B, r"$\dfrac{q_b\,b}{2}$", ha="left", va="center", fontsize=17, color=MAROON)
    ax.text(x0 + A / 2, -0.55, r"$\mathrm{equivalent\ nodal\ loads\ } \{b\}$", ha="center", va="top", fontsize=13, color=INK)
    ax.plot([x0 - 0.5, x0 - 0.5], [0, B], color=INK, lw=1.0); ax.plot([x0 - 0.6, x0 - 0.4], [0, 0], color=INK, lw=1); ax.plot([x0 - 0.6, x0 - 0.4], [B, B], color=INK, lw=1)
    ax.text(x0 - 0.62, B / 2, r"$b$", ha="right", va="center", fontsize=15, color=INK)
    return save_svg(fig, OUT / "fig_edge_flux.svg", "fig_edge_flux", "A uniform inward flux on the right edge of an element becomes two equal nodal loads qb times b over 2 at nodes 2 and 3")
rep.append(fig_edge_flux())

def fig_assign():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.set_xlim(-1.8, 8.0); ax.set_ylim(-1.3, 4.2); ax.set_aspect("equal"); ax.axis("off")
    a, b = 2.0, 3.0
    for e in range(3):
        fc = AMBER if e == 0 else FILL
        ax.add_patch(Rectangle((e * a, 0), a, b, facecolor=fc, edgecolor=NAVY, lw=2))
        ax.add_patch(Rectangle((e * a + a / 2 - 0.22, b / 2 - 0.22), 0.44, 0.44, facecolor=LIGHT, edgecolor=NAVY, lw=1.3))
        ax.text(e * a + a / 2, b / 2, str(e + 1), ha="center", va="center", fontsize=15, color=NAVY)
    for n in range(4):
        node(ax, n * a, 0, str(n + 1), r=0.17, fontsize=12); node(ax, n * a, b, str(n + 5), r=0.17, fontsize=12)
    ax.text(a / 2, b / 2 - 0.75, r"$Q=20\ \mathrm{W\,m^{-2}}$", ha="center", va="center", fontsize=13, color=MAROON)
    ax.text(-0.35, b / 2, r"$T=100\ \mathrm{K}$", ha="right", va="center", fontsize=16, color=MAROON, rotation=90)
    ax.text(3 * a / 2, b + 0.35, r"$q_b=0$", ha="center", va="bottom", fontsize=15, color=TEAL)
    ax.text(3 * a / 2, -0.4, r"$q_b=0$", ha="center", va="top", fontsize=15, color=TEAL)
    ax.text(3 * a + 0.35, b / 2, r"$q_b=0$", ha="left", va="center", fontsize=15, color=TEAL, rotation=90)
    ax.plot([0, 3 * a], [-0.85, -0.85], color=INK, lw=1.2)
    for xx in [0, a, 2 * a, 3 * a]:
        ax.plot([xx, xx], [-0.95, -0.75], color=INK, lw=1.2)
    for e in range(3):
        ax.text(e * a + a / 2, -1.0, r"$2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK)
    ax.plot([-1.2, -1.2], [0, b], color=INK, lw=1.2); ax.plot([-1.3, -1.1], [0, 0], color=INK, lw=1.2); ax.plot([-1.3, -1.1], [b, b], color=INK, lw=1.2)
    ax.text(-1.35, b / 2, r"$3\ \mathrm{m}$", ha="right", va="center", fontsize=13, color=INK, rotation=90)
    return save_svg(fig, OUT / "fig_assign.svg", "fig_assign", "Assignment 4 strip: three identical 2 m by 3 m elements, nodes 1 to 4 along the bottom and 5 to 8 along the top, T = 100 K on the left edge, zero flux elsewhere, heat source on element 1")
rep.append(fig_assign())

# contours: 2x2 bilinear FE field vs 16x16, jet, shared limits (PNG)
def fig_contours():
    bc = lambda x, y: 0.0 if (abs(x) < 1e-9 or abs(y - 1) < 1e-9) else None
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.2), dpi=160)
    vmin, vmax = 0.0, 0.62
    levels = np.linspace(vmin, vmax, 32)
    for ax, N, title in zip(axs, [2, 16], [r"$2\times2$ elements (hand calculation)", r"$16\times16$ elements (MATLAB)"]):
        nodes, conn, K, F, T, a, b = solve(1, 1, N, N, 300, 300, 600, bc)
        # evaluate bilinear field on a fine grid per element
        xs = np.linspace(0, 1, 161); X, Y = np.meshgrid(xs, xs); Z = np.zeros_like(X)
        for e in conn:
            x1, y1 = nodes[e[0]]; m = (X >= x1 - 1e-12) & (X <= x1 + a + 1e-12) & (Y >= y1 - 1e-12) & (Y <= y1 + b + 1e-12)
            xl, yl = X[m] - x1, Y[m] - y1
            Nf = np.array([(a - xl) * (b - yl), xl * (b - yl), xl * yl, yl * (a - xl)]) / (a * b)
            Z[m] = Nf.T @ T[e]
        cf = ax.contourf(X, Y, Z, levels=levels, cmap="jet", vmin=vmin, vmax=vmax)
        ax.contour(X, Y, Z, levels=np.linspace(0.1, 0.6, 6), colors="k", linewidths=0.5)
        # mesh lines
        for i in range(N + 1):
            ax.plot([i * a, i * a], [0, 1], color="w", lw=0.6, alpha=0.7); ax.plot([0, 1], [i * b, i * b], color="w", lw=0.6, alpha=0.7)
        ax.set_aspect("equal"); ax.set_title(title, fontsize=12, color=INK)
        ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 0.5, 1]); ax.tick_params(labelsize=9)
        ax.set_xlabel(r"$x$ (m)", fontsize=10); ax.set_ylabel(r"$y$ (m)", fontsize=10)
        for s in ax.spines.values():
            s.set_visible(True); s.set_linewidth(0.8)
    fig.subplots_adjust(left=0.06, right=0.88, top=0.9, bottom=0.14, wspace=0.25)
    cax = fig.add_axes([0.905, 0.14, 0.02, 0.76])
    cb = fig.colorbar(cf, cax=cax); cb.set_label(r"$T$ ($^{\circ}$C)", fontsize=11); cb.ax.tick_params(labelsize=9)
    fig.savefig(OUT / "fig_contours.png", dpi=160, transparent=False, facecolor="white", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return dict(name="fig_contours.png", bytes=(OUT / "fig_contours.png").stat().st_size)
rep.append(fig_contours())

for r in rep:
    print(r)
