import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w9")
OUT.mkdir(exist_ok=True, parents=True)
rep = []

# 1. differential element -------------------------------------------------
def fig_diffelem():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    ax.set_xlim(-2.2, 5.2); ax.set_ylim(-1.6, 4.0); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 2.6, 1.8, facecolor=FILL, edgecolor=NAVY, lw=2))
    # flux arrows
    for y in np.linspace(0.25, 1.55, 4):
        arrow(ax, (-0.9, y), (0, y)); arrow(ax, (2.6, y), (3.5, y))
    for x in np.linspace(0.35, 2.25, 5):
        arrow(ax, (x, -0.8), (x, 0)); arrow(ax, (x, 1.8), (x, 2.6))
    ax.text(1.3, 0.9, r"$q_h$", ha="center", va="center", fontsize=20, color=INK)
    ax.text(-1.0, 0.9, r"$q_x$", ha="right", va="center", fontsize=19, color=TEAL)
    ax.text(3.6, 0.9, r"$q_x+\dfrac{\partial q_x}{\partial x}dx$", ha="left", va="center", fontsize=19, color=TEAL)
    ax.text(1.3, -0.95, r"$q_y$", ha="center", va="top", fontsize=19, color=TEAL)
    ax.text(1.3, 2.7, r"$q_y+\dfrac{\partial q_y}{\partial y}dy$", ha="center", va="bottom", fontsize=19, color=TEAL)
    # dimensions
    ax.plot([0, 2.6], [3.75, 3.75], color=INK, lw=1.2); ax.plot([0, 0], [3.65, 3.85], color=INK, lw=1.2); ax.plot([2.6, 2.6], [3.65, 3.85], color=INK, lw=1.2)
    ax.text(1.3, 3.82, r"$dx$", ha="center", va="bottom", fontsize=18, color=INK)
    ax.plot([-1.9, -1.9], [0, 1.8], color=INK, lw=1.2); ax.plot([-2.0, -1.8], [0, 0], color=INK, lw=1.2); ax.plot([-2.0, -1.8], [1.8, 1.8], color=INK, lw=1.2)
    ax.text(-2.0, 0.9, r"$dy$", ha="right", va="center", fontsize=18, color=INK)
    return save_svg(fig, OUT / "fig_diffelem.svg", "fig_diffelem", "Differential element dx by dy with heat fluxes qx and qy entering and leaving, and heat generation qh inside")
rep.append(fig_diffelem())

# 2. four-node element ------------------------------------------------------
def q4(fname, a_lab=r"$a$", b_lab=r"$b$", point=None, nodal=None, coords=True, title_box="1"):
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.set_xlim(-1.4, 5.0); ax.set_ylim(-1.2, 3.4); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.4, 2.1
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    pts = [(0, 0), (A, 0), (A, B), (0, B)]
    for i, (x, y) in enumerate(pts, 1):
        node(ax, x, y, str(i))
    lab = [r"$\hat T_1$", r"$\hat T_2$", r"$\hat T_3$", r"$\hat T_4$"]
    off = [(-0.22, -0.22), (0.22, -0.22), (0.22, 0.22), (-0.22, 0.22)]
    ha = ["right", "left", "left", "right"]; va = ["top", "top", "bottom", "bottom"]
    for i, (x, y) in enumerate(pts):
        txt = lab[i] if nodal is None else nodal[i]
        ax.text(x + off[i][0], y + off[i][1], txt, ha=ha[i], va=va[i], fontsize=19, color=MAROON)
    if coords:
        cl = [r"$(0,0)$", r"$(a,0)$", r"$(a,b)$", r"$(0,b)$"]
        coff = [(0.18, 0.16), (-0.18, 0.16), (-0.18, -0.16), (0.18, -0.16)]
        cha = ["left", "right", "right", "left"]; cva = ["bottom", "bottom", "top", "top"]
        for i, (x, y) in enumerate(pts):
            ax.text(x + coff[i][0], y + coff[i][1], cl[i], ha=cha[i], va=cva[i], fontsize=15, color=GREY)
    if title_box:
        ax.add_patch(Rectangle((A / 2 - 0.2, B / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.5))
        ax.text(A / 2, B / 2, title_box, ha="center", va="center", fontsize=15, color=NAVY)
    # dims
    ax.plot([0, A], [-0.75, -0.75], color=INK, lw=1.2); ax.plot([0, 0], [-0.85, -0.65], color=INK, lw=1.2); ax.plot([A, A], [-0.85, -0.65], color=INK, lw=1.2)
    ax.text(A / 2, -0.85, a_lab, ha="center", va="top", fontsize=18, color=INK)
    ax.plot([-0.9, -0.9], [0, B], color=INK, lw=1.2); ax.plot([-1.0, -0.8], [0, 0], color=INK, lw=1.2); ax.plot([-1.0, -0.8], [B, B], color=INK, lw=1.2)
    ax.text(-1.0, B / 2, b_lab, ha="right", va="center", fontsize=18, color=INK)
    # axes
    arrow(ax, (3.9, 0), (4.8, 0), color=INK, lw=1.4, ms=12); ax.text(4.85, 0, r"$x$", ha="left", va="center", fontsize=17, color=INK)
    arrow(ax, (0, 2.5), (0, 3.2), color=INK, lw=1.4, ms=12); ax.text(0, 3.25, r"$y$", ha="center", va="bottom", fontsize=17, color=INK)
    if point is not None:
        px, py, plab = point
        X, Y = px / 2.0 * A, py / 1.0 * B
        ax.plot([X], [Y], marker="x", markersize=13, markeredgewidth=3, color=MAROON)
        ax.text(X - 0.15, Y + 0.14, plab, ha="right", va="bottom", fontsize=16, color=MAROON)
    return save_svg(fig, OUT / fname, fname.replace(".svg", ""), "Four-node rectangular element with nodes numbered anticlockwise from the bottom-left corner")
rep.append(q4("fig_q4.svg"))
rep.append(q4("fig_q4_point.svg", a_lab=r"$a=2\ \mathrm{m}$", b_lab=r"$b=1\ \mathrm{m}$", point=(1.5, 0.3, r"$(1.5,\,0.3)$"),
              nodal=[r"$\hat T_1=100$", r"$\hat T_2=140$", r"$\hat T_3=160$", r"$\hat T_4=120$"], coords=False, title_box=None))

# 3. shape functions: one tent surface (PNG) + four colour maps (SVG) ----------
def fig_shape():
    a, b = 1.0, 1.0
    x = np.linspace(0, a, 41); y = np.linspace(0, b, 41); X, Y = np.meshgrid(x, y)
    N = [(a - X) * (b - Y) / (a * b), X * (b - Y) / (a * b), X * Y / (a * b), Y * (a - X) / (a * b)]
    # tent: N3 in 3D
    fig = plt.figure(figsize=(4.6, 3.6), dpi=160)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, N[2], cmap="Blues", edgecolor="none", alpha=0.95, rstride=2, cstride=2, vmin=-0.3, vmax=1.1)
    ax.plot_wireframe(X[::10, ::10], Y[::10, ::10], N[2][::10, ::10], color=NAVY, lw=0.6)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], color=GREY, lw=1.0)
    ax.plot([1, 1], [1, 1], [0, 1], color=MAROON, lw=1.2, ls="--")
    for j, (px, py) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        z = 1.0 if j == 2 else 0.0
        ax.scatter([px], [py], [z], color=MAROON, s=34, depthshade=False)
        ax.text(px, py, z + 0.1, str(j + 1), color=MAROON, fontsize=13, ha="center", va="center")
    ax.set_zlim(0, 1); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
    ax.view_init(elev=30, azim=-125); ax.set_box_aspect((1, 1, 0.8))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(OUT / "fig_shape_tent.png", dpi=160, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    # maps
    fig, axs = plt.subplots(1, 4, figsize=(11.2, 3.0))
    for i, ax in enumerate(axs):
        ax.contourf(X, Y, N[i], levels=np.linspace(0, 1, 11), cmap="Blues", vmin=-0.3, vmax=1.1)
        ax.contour(X, Y, N[i], levels=np.linspace(0.1, 0.9, 5), colors=NAVY, linewidths=0.6)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(True); s.set_linewidth(1.5); s.set_color(NAVY)
        for j, (px, py) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
            ax.plot([px], [py], "o", color=MAROON, ms=9, clip_on=False, zorder=5)
            lab = r"$1$" if j == i else r"$0$"
            dx = -0.09 if px == 0 else 0.09; dy = -0.09 if py == 0 else 0.09
            ax.text(px + dx, py + dy, lab, color=MAROON, fontsize=15, ha="center", va="center")
        ax.set_title(rf"$N_{i+1}$", fontsize=22, color=MAROON, pad=14)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.08, wspace=0.35)
    fig.savefig(OUT / "fig_shape_maps.png", dpi=160, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return dict(name="fig_shape_maps.png", bytes=(OUT / "fig_shape_maps.png").stat().st_size)
rep.append(fig_shape())

# 4. boundary types on a rectangular domain --------------------------------
def fig_bc():
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.set_xlim(-1.9, 5.4); ax.set_ylim(-1.5, 3.3); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.6, 2.2
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    ax.text(A / 2, B / 2, r"$\Omega$", ha="center", va="center", fontsize=24, color=NAVY)
    # outward normals
    for (x, y, dx, dy, lab, ha, va) in [(A, B * 0.5, 0.75, 0, r"$n=(1,0)$", "left", "center"), (0, B * 0.5, -0.75, 0, r"$n=(-1,0)$", "right", "center"),
                                     (A * 0.5, B, 0, 0.7, r"$n=(0,1)$", "center", "bottom"), (A * 0.5, 0, 0, -0.7, r"$n=(0,-1)$", "center", "top")]:
        arrow(ax, (x, y), (x + dx, y + dy), color=MAROON, lw=2.2, ms=16)
        ax.text(x + dx * 1.15, y + dy * 1.15, lab, ha=ha, va=va, fontsize=16, color=MAROON)
    ax.text(A + 0.05, B + 0.15, r"$\Gamma$", ha="left", va="bottom", fontsize=20, color=NAVY)
    return save_svg(fig, OUT / "fig_bc.svg", "fig_bc", "Rectangular domain with the outward unit normal on each of its four edges")
rep.append(fig_bc())

# 5. plate for Activity 3 (book Fig. 2.11) -----------------------------------
def fig_plate_ex5():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.set_xlim(-2.3, 6.6); ax.set_ylim(-1.5, 3.1); ax.set_aspect("equal"); ax.axis("off")
    A, B = 4.5, 1.5
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    # hatching under bottom edge = insulated
    for xx in np.arange(0.0, A, 0.22):
        ax.plot([xx, xx + 0.2], [-0.3, 0], color=NAVY, lw=1.3)
    ax.plot([0, A], [0, 0], color=NAVY, lw=3)
    ax.text(A / 2, -0.4, r"$\mathrm{insulated}$", ha="center", va="top", fontsize=16, color=NAVY)
    ax.text(A / 2, B + 0.12, r"$T=300\ \mathrm{K}$", ha="center", va="bottom", fontsize=18, color=MAROON)
    ax.text(-0.15, B / 2, r"$T=400\ \mathrm{K}$", ha="right", va="center", fontsize=18, color=MAROON, rotation=90)
    for y in np.linspace(0.2, B - 0.2, 4):
        arrow(ax, (A + 0.8, y), (A, y), color=TEAL, lw=2, ms=14)
    ax.text(A + 0.95, B / 2, r"$q_b=1\times10^{6}\ \mathrm{W\,m^{-2}}$", ha="left", va="center", fontsize=16, color=TEAL, rotation=90)
    # dims
    ax.plot([0, A], [2.55, 2.55], color=INK, lw=1.2); ax.plot([0, 0], [2.45, 2.65], color=INK, lw=1.2); ax.plot([A, A], [2.45, 2.65], color=INK, lw=1.2)
    ax.text(A / 2, 2.62, r"$0.15\ \mathrm{m}$", ha="center", va="bottom", fontsize=16, color=INK)
    ax.plot([-1.6, -1.6], [0, B], color=INK, lw=1.2); ax.plot([-1.7, -1.5], [0, 0], color=INK, lw=1.2); ax.plot([-1.7, -1.5], [B, B], color=INK, lw=1.2)
    ax.text(-1.75, B / 2, r"$0.05\ \mathrm{m}$", ha="right", va="center", fontsize=16, color=INK, rotation=90)
    return save_svg(fig, OUT / "fig_plate_ex5.svg", "fig_plate_ex5", "Rectangular plate 0.15 m by 0.05 m: top edge at 300 K, left edge at 400 K, right edge with inward flux of one million watts per square metre, bottom edge insulated")
rep.append(fig_plate_ex5())

# 6. eight-node element -------------------------------------------------------
def fig_q8():
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.set_xlim(-1.4, 5.0); ax.set_ylim(-1.2, 3.4); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.4, 2.1
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    # book Fig 2.3 numbering: 1(0,0) 2(a/2,0) 3(a,0) 4(0,b/2) 5(a,b/2) 6(0,b) 7(a/2,b) 8(a,b)
    pts = [(0, 0), (A / 2, 0), (A, 0), (0, B / 2), (A, B / 2), (0, B), (A / 2, B), (A, B)]
    for i, (x, y) in enumerate(pts, 1):
        node(ax, x, y, str(i))
    ax.add_patch(Rectangle((A / 2 - 0.2, B / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.5))
    ax.text(A / 2, B / 2, "1", ha="center", va="center", fontsize=15, color=NAVY)
    ax.plot([0, A], [-0.75, -0.75], color=INK, lw=1.2); ax.plot([0, 0], [-0.85, -0.65], color=INK, lw=1.2); ax.plot([A, A], [-0.85, -0.65], color=INK, lw=1.2)
    ax.text(A / 2, -0.85, r"$a$", ha="center", va="top", fontsize=18, color=INK)
    ax.plot([-0.9, -0.9], [0, B], color=INK, lw=1.2); ax.plot([-1.0, -0.8], [0, 0], color=INK, lw=1.2); ax.plot([-1.0, -0.8], [B, B], color=INK, lw=1.2)
    ax.text(-1.0, B / 2, r"$b$", ha="right", va="center", fontsize=18, color=INK)
    arrow(ax, (3.9, 0), (4.8, 0), color=INK, lw=1.4, ms=12); ax.text(4.85, 0, r"$x$", ha="left", va="center", fontsize=17, color=INK)
    arrow(ax, (0, 2.5), (0, 3.2), color=INK, lw=1.4, ms=12); ax.text(0, 3.25, r"$y$", ha="center", va="bottom", fontsize=17, color=INK)
    return save_svg(fig, OUT / "fig_q8.svg", "fig_q8", "Eight-node rectangular element: corner nodes 1, 3, 6, 8 and mid-side nodes 2, 4, 5, 7")
rep.append(fig_q8())

# 7. scalar vs vector node ----------------------------------------------------
def fig_scalar_vector():
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.4))
    for ax, kind in zip(axs, ["scalar", "vector"]):
        ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.9, 2.9); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 3.0, 2.0, facecolor=FILL, edgecolor=NAVY, lw=2))
        for (x, y) in [(0, 0), (3, 0), (3, 2), (0, 2)]:
            node(ax, x, y, None, r=0.09)
        if kind == "scalar":
            ax.text(3.18, 2.2, r"$\hat T_3$", ha="left", va="bottom", fontsize=20, color=MAROON)
            ax.text(1.5, -0.55, r"$\mathrm{1\ dof\ per\ node}$", ha="center", va="top", fontsize=16, color=INK)
        else:
            arrow(ax, (3, 2), (3.75, 2), color=MAROON, lw=2.4, ms=16); arrow(ax, (3, 2), (3, 2.75), color=MAROON, lw=2.4, ms=16)
            ax.text(3.8, 1.95, r"$u_3$", ha="left", va="center", fontsize=20, color=MAROON)
            ax.text(3.05, 2.8, r"$v_3$", ha="left", va="bottom", fontsize=20, color=MAROON)
            ax.text(1.5, -0.55, r"$\mathrm{2\ dof\ per\ node}$", ha="center", va="top", fontsize=16, color=INK)
    fig.subplots_adjust(wspace=0.25)
    return save_svg(fig, OUT / "fig_scalar_vector.svg", "fig_scalar_vector", "Left: a scalar element with one temperature unknown per node. Right: a plane-stress element with two displacement unknowns per node")
rep.append(fig_scalar_vector())

# 8. worked-example plate (book Fig 2.5) + 2x2 mesh (Fig 2.6) -----------------
def fig_plate_book():
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.set_xlim(-1.9, 4.2); ax.set_ylim(-1.3, 4.0); ax.set_aspect("equal"); ax.axis("off")
    L = 3.0
    ax.add_patch(Rectangle((0, 0), L, L, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for xx in np.arange(0.0, L, 0.22):
        ax.plot([xx, xx + 0.2], [-0.3, 0], color=NAVY, lw=1.3)
    for yy in np.arange(0.0, L, 0.22):
        ax.plot([L, L + 0.3], [yy, yy + 0.2], color=NAVY, lw=1.3)
    ax.plot([0, L], [0, 0], color=NAVY, lw=3); ax.plot([L, L], [0, L], color=NAVY, lw=3)
    ax.text(L / 2, L + 0.12, r"$T=0\,^{\circ}\mathrm{C}$", ha="center", va="bottom", fontsize=18, color=MAROON)
    ax.text(-0.15, L / 2, r"$T=0\,^{\circ}\mathrm{C}$", ha="right", va="center", fontsize=18, color=MAROON, rotation=90)
    ax.text(L / 2, L / 2, r"$q_h$", ha="center", va="center", fontsize=22, color=INK)
    ax.text(L + 0.45, L / 2, r"$\mathrm{insulated}$", ha="left", va="center", fontsize=15, color=NAVY, rotation=90)
    ax.text(L / 2, -0.42, r"$\mathrm{insulated}$", ha="center", va="top", fontsize=15, color=NAVY)
    ax.plot([0, L], [3.7, 3.7], color=INK, lw=1.2); ax.plot([0, 0], [3.6, 3.8], color=INK, lw=1.2); ax.plot([L, L], [3.6, 3.8], color=INK, lw=1.2)
    ax.text(L / 2, 3.77, r"$1\ \mathrm{m}$", ha="center", va="bottom", fontsize=16, color=INK)
    ax.plot([-1.3, -1.3], [0, L], color=INK, lw=1.2); ax.plot([-1.4, -1.2], [0, 0], color=INK, lw=1.2); ax.plot([-1.4, -1.2], [L, L], color=INK, lw=1.2)
    ax.text(-1.45, L / 2, r"$1\ \mathrm{m}$", ha="right", va="center", fontsize=16, color=INK, rotation=90)
    return save_svg(fig, OUT / "fig_plate_book.svg", "fig_plate_book", "Square plate 1 m by 1 m with heat source, top and left edges held at 0 degrees Celsius, right and bottom edges insulated")
rep.append(fig_plate_book())

def fig_mesh2x2():
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.set_xlim(-0.9, 4.2); ax.set_ylim(-1.0, 4.0); ax.set_aspect("equal"); ax.axis("off")
    L = 3.0; h = L / 2
    for i in range(2):
        for j in range(2):
            ax.add_patch(Rectangle((j * h, i * h), h, h, facecolor=FILL, edgecolor=NAVY, lw=2))
            e = i * 2 + j + 1
            ax.add_patch(Rectangle((j * h + h / 2 - 0.2, i * h + h / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.3))
            ax.text(j * h + h / 2, i * h + h / 2, str(e), ha="center", va="center", fontsize=15, color=NAVY)
    n = 1
    for i in range(3):
        for j in range(3):
            node(ax, j * h, i * h, str(n), r=0.16, fontsize=13)
            n += 1
    ax.plot([0, L], [-0.6, -0.6], color=INK, lw=1.2)
    for xx in [0, h, L]:
        ax.plot([xx, xx], [-0.7, -0.5], color=INK, lw=1.2)
    ax.text(h / 2, -0.75, r"$0.5\ \mathrm{m}$", ha="center", va="top", fontsize=15, color=INK)
    ax.text(h + h / 2, -0.75, r"$0.5\ \mathrm{m}$", ha="center", va="top", fontsize=15, color=INK)
    return save_svg(fig, OUT / "fig_mesh2x2.svg", "fig_mesh2x2", "Two-by-two mesh of four-node elements with global node numbers 1 to 9")
rep.append(fig_mesh2x2())

# 9. flux direction sketch for Fourier's law -----------------------------------
def fig_fourier():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.set_xlim(-0.4, 7.2); ax.set_ylim(-1.3, 2.6); ax.axis("off")
    x = np.linspace(0, 6, 60); T = 2.0 - 0.25 * x
    ax.fill_between(x, 0, T, color=FILL, alpha=0.9)
    ax.plot(x, T, color=MAROON, lw=2.5)
    ax.text(0.1, 2.1, r"$T\ \mathrm{high}$", ha="left", va="bottom", fontsize=17, color=MAROON)
    ax.text(6.0, 0.15, r"$T\ \mathrm{low}$", ha="right", va="bottom", fontsize=17, color=MAROON)
    arrow(ax, (1.5, -0.55), (4.5, -0.55), color=TEAL, lw=3, ms=22)
    ax.text(3.0, -0.75, r"$q_x=-k_x\,\dfrac{\partial T}{\partial x}>0$", ha="center", va="top", fontsize=17, color=TEAL)
    arrow(ax, (0, 0), (6.8, 0), color=INK, lw=1.3, ms=12); ax.text(6.9, 0, r"$x$", ha="left", va="center", fontsize=16, color=INK)
    ax.text(3.0, 1.0, r"$\dfrac{\partial T}{\partial x}<0$", ha="center", va="center", fontsize=17, color=INK)
    return save_svg(fig, OUT / "fig_fourier.svg", "fig_fourier", "Temperature falling along x; the heat flux points in the positive x direction, down the gradient")
rep.append(fig_fourier())

for r in rep:
    print(r)
