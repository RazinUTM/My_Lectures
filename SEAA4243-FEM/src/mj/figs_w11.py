import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w11")
OUT.mkdir(exist_ok=True, parents=True)
rep = []

# 1. plane-stress differential element (book Fig 3.1) --------------------------
def fig_ps_diffelem():
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    ax.set_xlim(-2.6, 6.2); ax.set_ylim(-2.2, 4.4); ax.set_aspect("equal"); ax.axis("off")
    W, H = 3.0, 2.0
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=FILL, edgecolor=NAVY, lw=2))
    # normal stresses
    arrow(ax, (W, H / 2), (W + 1.1, H / 2), color=MAROON, lw=2.4, ms=16); ax.text(W + 1.2, H / 2, r"$\sigma_{xx}+\dfrac{\partial\sigma_{xx}}{\partial x}dx$", ha="left", va="center", fontsize=15, color=MAROON)
    arrow(ax, (0, H / 2), (-1.1, H / 2), color=MAROON, lw=2.4, ms=16); ax.text(-1.2, H / 2, r"$\sigma_{xx}$", ha="right", va="center", fontsize=16, color=MAROON)
    arrow(ax, (W / 2, H), (W / 2, H + 1.0), color=MAROON, lw=2.4, ms=16); ax.text(W / 2, H + 1.1, r"$\sigma_{yy}+\dfrac{\partial\sigma_{yy}}{\partial y}dy$", ha="center", va="bottom", fontsize=15, color=MAROON)
    arrow(ax, (W / 2, 0), (W / 2, -1.0), color=MAROON, lw=2.4, ms=16); ax.text(W / 2, -1.1, r"$\sigma_{yy}$", ha="center", va="top", fontsize=16, color=MAROON)
    # shear stresses (tangential arrows along faces)
    arrow(ax, (W, 0.25), (W, 1.25), color=TEAL, lw=2.2, ms=14); ax.text(W + 0.15, 0.1, r"$\sigma_{xy}+\dfrac{\partial\sigma_{xy}}{\partial x}dx$", ha="left", va="top", fontsize=13, color=TEAL)
    arrow(ax, (0, 1.75), (0, 0.75), color=TEAL, lw=2.2, ms=14); ax.text(-0.12, 0.55, r"$\sigma_{xy}$", ha="right", va="top", fontsize=14, color=TEAL)
    arrow(ax, (0.6, H), (1.6, H), color=TEAL, lw=2.2, ms=14); ax.text(1.75, H + 0.1, r"$\sigma_{yx}+\dfrac{\partial\sigma_{yx}}{\partial y}dy$", ha="left", va="bottom", fontsize=13, color=TEAL)
    arrow(ax, (2.4, 0), (1.4, 0), color=TEAL, lw=2.2, ms=14); ax.text(1.25, -0.12, r"$\sigma_{yx}$", ha="right", va="top", fontsize=14, color=TEAL)
    # body forces
    arrow(ax, (W / 2, H / 2), (W / 2 + 0.7, H / 2), color=INK, lw=2, ms=13); ax.text(W / 2 + 0.75, H / 2 - 0.05, r"$f_x$", ha="left", va="top", fontsize=14, color=INK)
    arrow(ax, (W / 2, H / 2), (W / 2, H / 2 + 0.7), color=INK, lw=2, ms=13); ax.text(W / 2 + 0.08, H / 2 + 0.75, r"$f_y$", ha="left", va="bottom", fontsize=14, color=INK)
    # dims
    ax.plot([0, W], [3.9, 3.9], color=INK, lw=1.2); ax.plot([0, 0], [3.8, 4.0], color=INK, lw=1.2); ax.plot([W, W], [3.8, 4.0], color=INK, lw=1.2)
    ax.text(W / 2, 3.97, r"$dx$", ha="center", va="bottom", fontsize=15, color=INK)
    ax.plot([-2.3, -2.3], [0, H], color=INK, lw=1.2); ax.plot([-2.4, -2.2], [0, 0], color=INK, lw=1.2); ax.plot([-2.4, -2.2], [H, H], color=INK, lw=1.2)
    ax.text(-2.4, H / 2, r"$dy$", ha="right", va="center", fontsize=15, color=INK)
    return save_svg(fig, OUT / "fig_ps_diffelem.svg", "fig_ps_diffelem", "Plane-stress differential element with normal stresses, shear stresses and body forces, the far faces carrying the Taylor-expanded stresses")
rep.append(fig_ps_diffelem())

# 2. four-node plane stress element with u, v dofs (book Fig 3.2) ----------------
def fig_ps_q4(fname="fig_ps_q4.svg", a_lab=r"$a$", b_lab=r"$b$", nodal=None, point=None):
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    ax.set_xlim(-1.5, 5.4); ax.set_ylim(-1.3, 3.6); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.4, 2.1
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    pts = [(0, 0), (A, 0), (A, B), (0, B)]
    for i, (x, y) in enumerate(pts, 1):
        node(ax, x, y, str(i))
        if nodal is None:
            arrow(ax, (x + 0.12, y), (x + 0.75, y), color=MAROON, lw=2.2, ms=14); ax.text(x + 0.8, y + 0.02, rf"$u_{i}$", ha="left", va="center", fontsize=15, color=MAROON)
            arrow(ax, (x, y + 0.12), (x, y + 0.75), color=MAROON, lw=2.2, ms=14); ax.text(x + 0.06, y + 0.8, rf"$v_{i}$", ha="left", va="bottom", fontsize=15, color=MAROON)
    if nodal is not None:
        off = [(-0.2, -0.25), (0.2, -0.25), (0.2, 0.25), (-0.2, 0.25)]; ha = ["right", "left", "left", "right"]; va = ["top", "top", "bottom", "bottom"]
        for i, (x, y) in enumerate(pts):
            ax.text(x + off[i][0], y + off[i][1], nodal[i], ha=ha[i], va=va[i], fontsize=14, color=MAROON)
    ax.plot([0, A], [-0.9, -0.9], color=INK, lw=1.2); ax.plot([0, 0], [-1.0, -0.8], color=INK, lw=1.2); ax.plot([A, A], [-1.0, -0.8], color=INK, lw=1.2)
    ax.text(A / 2, -1.0, a_lab, ha="center", va="top", fontsize=17, color=INK)
    ax.plot([-1.1, -1.1], [0, B], color=INK, lw=1.2); ax.plot([-1.2, -1.0], [0, 0], color=INK, lw=1.2); ax.plot([-1.2, -1.0], [B, B], color=INK, lw=1.2)
    ax.text(-1.2, B / 2, b_lab, ha="right", va="center", fontsize=17, color=INK)
    if point is not None:
        px, py, lab = point
        X, Y = px / 2.0 * A, py / 1.0 * B
        ax.plot([X], [Y], marker="x", markersize=13, markeredgewidth=3, color=MAROON, zorder=7)
        ax.text(X - 0.15, Y + 0.15, lab, ha="right", va="bottom", fontsize=14, color=MAROON)
    return save_svg(fig, OUT / fname, fname.replace(".svg", ""), "Four-node plane-stress element with two displacement degrees of freedom u and v at each node")
rep.append(fig_ps_q4())
rep.append(fig_ps_q4("fig_ps_q4_point.svg", r"$a=2\ \mathrm{m}$", r"$b=1\ \mathrm{m}$",
                     nodal=[r"$(0,\,-0.043)$", r"$(0,\,-0.130)$", r"$(0.042,\,-0.131)$", r"$(0.031,\,-0.046)$"], point=(1.5, 0.3, r"$(1.5,\,0.3)$")))

# 3. cantilever (book Fig 3.4) ---------------------------------------------------
def fig_cantilever():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.set_xlim(-1.6, 7.6); ax.set_ylim(-1.3, 3.6); ax.set_aspect("equal"); ax.axis("off")
    L, H = 5.2, 2.6
    ax.add_patch(Rectangle((0, 0), L, H, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for yy in np.arange(-0.1, H + 0.1, 0.22):
        ax.plot([-0.3, 0], [yy - 0.2, yy], color=NAVY, lw=1.3)
    ax.plot([0, 0], [-0.1, H + 0.1], color=NAVY, lw=3)
    ax.plot([L + 0.75, L + 0.75], [0, H], color=TEAL, lw=2)
    for y in np.linspace(0.15, H - 0.15, 7):
        arrow(ax, (L + 0.75, y + 0.28), (L + 0.75, y - 0.28), color=TEAL, lw=1.8, ms=12)
    ax.text(L + 0.95, H / 2, r"$q_y=5\ \mathrm{kN\,m^{-1}}$", ha="left", va="center", fontsize=15, color=TEAL, rotation=90)
    ax.plot([0, L], [3.2, 3.2], color=INK, lw=1.2); ax.plot([0, 0], [3.1, 3.3], color=INK, lw=1.2); ax.plot([L, L], [3.1, 3.3], color=INK, lw=1.2)
    ax.text(L / 2, 3.27, r"$4\ \mathrm{m}$", ha="center", va="bottom", fontsize=15, color=INK)
    ax.plot([-1.0, -1.0], [0, H], color=INK, lw=1.2); ax.plot([-1.1, -0.9], [0, 0], color=INK, lw=1.2); ax.plot([-1.1, -0.9], [H, H], color=INK, lw=1.2)
    ax.text(-1.15, H / 2, r"$2\ \mathrm{m}$", ha="right", va="center", fontsize=15, color=INK, rotation=90)
    ax.text(L / 2, -0.4, r"$E=200\times10^{6}\ \mathrm{N\,m^{-2}},\ \nu=0.33,\ t=0.01\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_cantilever.svg", "fig_cantilever", "Cantilever plate 4 m long and 2 m deep, fixed on the left edge, with a downward edge load of 5 kN per metre on the right edge")
rep.append(fig_cantilever())

# 4. 2x2 plane-stress mesh with global dof numbers (book Fig 3.5) ------------------
def fig_ps_mesh(fname="fig_ps_mesh.svg", shade=None, point=None, dofs=True):
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.set_xlim(-0.9, 6.9); ax.set_ylim(-1.0, 3.9); ax.set_aspect("equal"); ax.axis("off")
    L, H = 5.2, 2.6; hx, hy = L / 2, H / 2
    for i in range(2):
        for j in range(2):
            e = i * 2 + j + 1
            ax.add_patch(Rectangle((j * hx, i * hy), hx, hy, facecolor=AMBER if shade == e else FILL, edgecolor=NAVY, lw=2))
            ax.add_patch(Rectangle((j * hx + hx / 2 - 0.2, i * hy + hy / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.3))
            ax.text(j * hx + hx / 2, i * hy + hy / 2, str(e), ha="center", va="center", fontsize=14, color=NAVY)
    for yy in np.arange(-0.1, H + 0.1, 0.22):
        ax.plot([-0.3, 0], [yy - 0.2, yy], color=NAVY, lw=1.2)
    n = 1
    for i in range(3):
        for j in range(3):
            x, y = j * hx, i * hy
            node(ax, x, y, str(n), r=0.17, fontsize=12)
            if dofs:
                arrow(ax, (x + 0.2, y), (x + 0.6, y), color=MAROON, lw=1.6, ms=10); ax.text(x + 0.63, y - 0.02, rf"$U_{{{2*n-1}}}$", ha="left", va="center", fontsize=11, color=MAROON)
                arrow(ax, (x, y + 0.2), (x, y + 0.6), color=MAROON, lw=1.6, ms=10); ax.text(x + 0.05, y + 0.62, rf"$U_{{{2*n}}}$", ha="left", va="bottom", fontsize=11, color=MAROON)
            n += 1
    ax.plot([0, L], [-0.65, -0.65], color=INK, lw=1.2)
    for xx in [0, hx, L]:
        ax.plot([xx, xx], [-0.75, -0.55], color=INK, lw=1.2)
    ax.text(hx / 2, -0.8, r"$2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK); ax.text(hx + hx / 2, -0.8, r"$2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK)
    if point is not None:
        px, py, lab = point
        X, Y = px / 4.0 * L, py / 2.0 * H
        ax.plot([X], [Y], marker="x", markersize=12, markeredgewidth=3, color=MAROON, zorder=8)
        ax.text(X - 0.15, Y - 0.2, lab, ha="right", va="top", fontsize=12, color=MAROON)
    return save_svg(fig, OUT / fname, fname.replace(".svg", ""), "Two-by-two mesh of the cantilever with nine global nodes and eighteen displacement degrees of freedom U1 to U18")
rep.append(fig_ps_mesh())
rep.append(fig_ps_mesh("fig_ps_mesh_e4.svg", shade=4, point=(3.5, 1.3, r"$(3.5,\,1.3)$")))

# 5. plane stress vs plane strain sketches ----------------------------------------
def fig_ps_vs_pe():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax = axs[0]; ax.set_xlim(-0.8, 5.2); ax.set_ylim(-0.6, 3.6); ax.set_aspect("equal"); ax.axis("off")
    # thin plate drawn in oblique view
    ax.add_patch(Polygon([(0, 0), (3.4, 0), (3.4, 2.4), (0, 2.4)], closed=True, facecolor=FILL, edgecolor=NAVY, lw=2))
    ax.add_patch(Polygon([(3.4, 0), (3.6, 0.2), (3.6, 2.6), (3.4, 2.4)], closed=True, facecolor="#B9C9DA", edgecolor=NAVY, lw=1.5))
    ax.add_patch(Polygon([(0, 2.4), (0.2, 2.6), (3.6, 2.6), (3.4, 2.4)], closed=True, facecolor="#CBD8E6", edgecolor=NAVY, lw=1.5))
    for y in np.linspace(0.3, 2.1, 4):
        arrow(ax, (3.95, y), (4.6, y), color=MAROON, lw=2, ms=13); arrow(ax, (-0.3, y), (-0.95, y), color=MAROON, lw=2, ms=13)
    ax.text(1.7, 1.2, r"$t\ \mathrm{small}$", ha="center", va="center", fontsize=15, color=INK)
    ax.text(1.7, 3.1, r"$\mathrm{plane\ stress:}\ \sigma_{zz}=0$", ha="center", va="center", fontsize=15, color=MAROON)
    ax = axs[1]; ax.set_xlim(-0.8, 5.2); ax.set_ylim(-0.6, 3.6); ax.set_aspect("equal"); ax.axis("off")
    # long body: trapezoid (dam section) extruded
    sec = [(0, 0), (2.6, 0), (1.3, 2.0), (0.4, 2.0)]
    ax.add_patch(Polygon([(x + 1.5, y + 0.6) for x, y in sec], closed=True, facecolor="#CBD8E6", edgecolor=NAVY, lw=1.2))
    for (x, y) in sec:
        ax.plot([x, x + 1.5], [y, y + 0.6], color=NAVY, lw=1.0)
    ax.add_patch(Polygon(sec, closed=True, facecolor=FILL, edgecolor=NAVY, lw=2))
    ax.text(1.0, 0.9, r"$\mathrm{section}$", ha="center", va="center", fontsize=14, color=INK)
    ax.text(2.2, 3.25, r"$\mathrm{plane\ strain:}\ \varepsilon_{zz}=0$", ha="center", va="center", fontsize=15, color=MAROON)
    ax.text(3.9, 0.4, r"$\mathrm{long}$", ha="center", va="center", fontsize=14, color=INK)
    fig.subplots_adjust(wspace=0.05)
    return save_svg(fig, OUT / "fig_ps_vs_pe.svg", "fig_ps_vs_pe", "Left: a thin plate loaded in its plane, plane stress with zero out-of-plane stress. Right: a long body with a constant cross-section, plane strain with zero out-of-plane strain")
rep.append(fig_ps_vs_pe())

# 6. strain sketches ----------------------------------------------------------------
def fig_strain():
    fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.3))
    titles = [r"$\varepsilon_{xx}=\partial u/\partial x$", r"$\varepsilon_{yy}=\partial v/\partial y$", r"$\varepsilon_{xy}=\partial u/\partial y+\partial v/\partial x$"]
    for k, ax in enumerate(axs):
        ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.6, 3.2); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 2, 2, facecolor="none", edgecolor=GREY, lw=1.5, ls="--"))
        if k == 0:
            ax.add_patch(Rectangle((0, 0), 2.7, 2, facecolor=FILL, edgecolor=NAVY, lw=2, alpha=0.9))
            arrow(ax, (2.0, 1.0), (2.65, 1.0), color=MAROON, lw=2, ms=13); ax.text(2.3, 1.15, r"$\Delta u$", ha="center", va="bottom", fontsize=13, color=MAROON)
        elif k == 1:
            ax.add_patch(Rectangle((0, 0), 2, 2.7, facecolor=FILL, edgecolor=NAVY, lw=2, alpha=0.9))
            arrow(ax, (1.0, 2.0), (1.0, 2.65), color=MAROON, lw=2, ms=13); ax.text(1.15, 2.3, r"$\Delta v$", ha="left", va="center", fontsize=13, color=MAROON)
        else:
            ax.add_patch(Polygon([(0, 0), (2, 0), (2.6, 2), (0.6, 2)], closed=True, facecolor=FILL, edgecolor=NAVY, lw=2, alpha=0.9))
            arrow(ax, (0, 2.0), (0.55, 2.0), color=MAROON, lw=2, ms=13); ax.text(0.3, 2.15, r"$\Delta u$", ha="center", va="bottom", fontsize=13, color=MAROON)
        ax.set_title(titles[k], fontsize=14, color=INK, pad=4)
    fig.subplots_adjust(wspace=0.1, top=0.82)
    return save_svg(fig, OUT / "fig_strain.svg", "fig_strain", "A square element stretched in x, stretched in y, and sheared, illustrating the two normal strains and the engineering shear strain")
rep.append(fig_strain())

# 7. shear wall with openings (book Fig 3.10, simplified) --------------------------
def fig_shearwall():
    fig, ax = plt.subplots(figsize=(5.6, 6.0))
    ax.set_xlim(-1.4, 6.6); ax.set_ylim(-1.0, 7.6); ax.set_aspect("equal"); ax.axis("off")
    W = 5.0; H = 6.0
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=FILL, edgecolor=NAVY, lw=2))
    for (x, y, w, h) in [(1.75, 0.5, 1.5, 2.0), (1.75, 3.5, 1.5, 2.0)]:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=LIGHT, edgecolor=NAVY, lw=1.5))
    for xx in np.arange(-0.1, W + 0.1, 0.25):
        ax.plot([xx, xx + 0.25], [-0.3, 0], color=NAVY, lw=1.2)
    ax.plot([-0.1, W + 0.1], [0, 0], color=NAVY, lw=3)
    ax.plot([0, W], [H + 0.55, H + 0.55], color=TEAL, lw=2)
    for x in np.linspace(0.2, W - 0.2, 10):
        arrow(ax, (x, H + 0.55), (x, H + 0.05), color=TEAL, lw=1.6, ms=11)
    ax.text(W / 2, H + 0.7, r"$125\ \mathrm{kN\,m^{-1}}$", ha="center", va="bottom", fontsize=14, color=TEAL)
    ax.text(W + 0.25, H / 2, r"$6\ \mathrm{m}$", ha="left", va="center", fontsize=13, color=INK, rotation=90)
    ax.text(W / 2, -0.55, r"$5\ \mathrm{m},\ t=0.2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_shearwall.svg", "fig_shearwall", "Shear wall 5 m wide and 6 m high with two openings, fixed at the base, carrying a vertical line load of 125 kN per metre on top")
rep.append(fig_shearwall())

for r in rep:
    print(r)
