import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *
from fe_ps import solve_cantilever, mesh
from matplotlib.colors import ListedColormap

GREEN = "#2E7D5B"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w12")
OUT.mkdir(exist_ok=True, parents=True)
rep = []
E, nu, t = 200e6, 0.33, 0.01

# 1. edge traction -> nodal loads -------------------------------------------------
def fig_edge_traction():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_xlim(-0.8, 9.4); ax.set_ylim(-1.3, 3.2); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.0, 2.0
    ax.add_patch(Rectangle((0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2))
    for (x, y), lab in zip([(0, 0), (A, 0), (A, B), (0, B)], ["1", "2", "3", "4"]):
        node(ax, x, y, lab, r=0.14, fontsize=12)
    ax.plot([A + 0.55, A + 0.55], [0, B], color=TEAL, lw=2)
    for y in np.linspace(0.15, B - 0.15, 6):
        arrow(ax, (A + 0.55, y + 0.22), (A + 0.55, y - 0.22), color=TEAL, lw=1.8, ms=12)
    ax.text(A + 0.75, B / 2, r"$q_y$", ha="left", va="center", fontsize=19, color=TEAL)
    ax.text(A / 2, -0.55, r"$\mathrm{traction\ } b_y=q_y/t \mathrm{\ on\ edge\ 2\!-\!3}$", ha="center", va="top", fontsize=13, color=INK)
    arrow(ax, (4.5, B / 2), (5.2, B / 2), color=AMBER, lw=4, ms=26)
    x0 = 6.0
    ax.add_patch(Rectangle((x0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2))
    for (x, y), lab in zip([(x0, 0), (x0 + A, 0), (x0 + A, B), (x0, B)], ["1", "2", "3", "4"]):
        node(ax, x, y, lab, r=0.14, fontsize=12)
    arrow(ax, (x0 + A, 0.9), (x0 + A, 0.15), color=MAROON, lw=3, ms=18); ax.text(x0 + A + 0.2, 0.55, r"$\dfrac{q_y\,b}{2}\ (v_2)$", ha="left", va="center", fontsize=15, color=MAROON)
    arrow(ax, (x0 + A, B - 0.15), (x0 + A, B - 0.9), color=MAROON, lw=3, ms=18); ax.text(x0 + A + 0.2, B - 0.5, r"$\dfrac{q_y\,b}{2}\ (v_3)$", ha="left", va="center", fontsize=15, color=MAROON)
    ax.text(x0 + A / 2, -0.55, r"$\mathrm{equivalent\ nodal\ loads\ }\{b\}$", ha="center", va="top", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_edge_traction.svg", "fig_edge_traction", "A uniform downward traction on the right edge of an element becomes two equal downward nodal loads at nodes 2 and 3")
rep.append(fig_edge_traction())

# 2. deflected shape: 2x2 vs fine -------------------------------------------------------
def fig_deflected():
    fig, ax = plt.subplots(figsize=(9.0, 4.2), dpi=160)
    scale = 4.0
    for (Nx, Ny), col, lw, lab in [((32, 16), "#B9C9DA", 0.4, r"$32\times16$ (converged, $U_{18}=-0.191$ m)"), ((2, 2), MAROON, 1.8, r"$2\times2$ hand mesh ($U_{18}=-0.131$ m)")]:
        nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, Nx, Ny, E, nu, t, -5000)
        X = nodes[:, 0] + scale * U[0::2]; Y = nodes[:, 1] + scale * U[1::2]
        first = True
        for e in conn:
            idx = list(e) + [e[0]]
            ax.plot(X[idx], Y[idx], color=col, lw=lw, label=lab if first else None); first = False
    a, b, nodes, conn = mesh(4, 2, 2, 2)
    for e in conn:
        idx = list(e) + [e[0]]
        ax.plot(nodes[idx, 0], nodes[idx, 1], color=GREY, lw=1.0, ls="--", label="undeformed" if e is conn[0] else None)
    ax.set_aspect("equal"); ax.set_xlim(-0.3, 4.6); ax.set_ylim(-1.2, 2.4)
    ax.set_xlabel(r"$x$ (m)", fontsize=11); ax.set_ylabel(r"$y$ (m)", fontsize=11); ax.tick_params(labelsize=9)
    ax.legend(fontsize=9, loc="lower left", frameon=False)
    ax.set_title(r"Deflected shapes, displacements scaled $\times4$", fontsize=12, color=INK)
    for s in ax.spines.values():
        s.set_visible(True); s.set_linewidth(0.8)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.14)
    fig.savefig(OUT / "fig_deflected.png", dpi=160, facecolor="white", bbox_inches="tight", pad_inches=0.05); plt.close(fig)
    return dict(name="fig_deflected.png", bytes=(OUT / "fig_deflected.png").stat().st_size)
rep.append(fig_deflected())

# 3. convergence pair: U18 vs elements along the length (linear) and error log-log -------
def fig_convergence():
    meshes = [(2, 2), (4, 2), (8, 4), (16, 8), (32, 16), (64, 32)]
    vals = []
    for Nx, Ny in meshes:
        nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, Nx, Ny, E, nu, t, -5000)
        i18 = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); vals.append(-U[2 * i18 + 1])
    vals = np.array(vals); ref = 0.1919; h = np.array([4 / m[0] for m in meshes])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0), dpi=160)
    a1.plot([m[0] for m in meshes], vals, marker="o", color=MAROON, lw=1.8, ms=6, label="Q4 FE, tip deflection")
    a1.axhline(ref, color=TEAL, ls="--", lw=1.5, label="beam theory (bending + shear) 0.192 m")
    a1.set_xscale("log", base=2); a1.set_xlabel("elements along the length", fontsize=11); a1.set_ylabel(r"$|U_{18}|$ (m)", fontsize=11)
    a1.set_ylim(0.1, 0.21); a1.legend(fontsize=9, frameon=False, loc="lower right"); a1.set_title("(a) tip deflection against mesh", fontsize=12, color=INK)
    err = np.abs(vals - ref) / ref
    a2.loglog(h, err, marker="s", color=MAROON, lw=1.8, ms=6, label="relative error")
    rate = np.polyfit(np.log(h[:-1]), np.log(err[:-1]), 1)[0]
    a2.loglog(h[:3], err[1] * (h[:3] / h[1]) ** 1, color=GREY, ls=":", lw=1.2, label="slope 1 reference")
    a2.set_xlabel(r"element size $h$ (m)", fontsize=11); a2.set_ylabel("relative error", fontsize=11); a2.set_title(f"(b) error against element size, observed rate {rate:.2f}", fontsize=12, color=INK)
    a2.legend(fontsize=9, frameon=False)
    for ax in (a1, a2):
        ax.tick_params(labelsize=9); ax.grid(True, which="both", lw=0.4, alpha=0.5)
        for s in ax.spines.values():
            s.set_visible(True); s.set_linewidth(0.8)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.88, bottom=0.17, wspace=0.3)
    fig.savefig(OUT / "fig_convergence.png", dpi=160, facecolor="white", bbox_inches="tight", pad_inches=0.05); plt.close(fig)
    print("convergence values", vals, "rate", rate)
    return dict(name="fig_convergence.png", bytes=(OUT / "fig_convergence.png").stat().st_size)
rep.append(fig_convergence())

# 4. 18x18 assembly map coloured by contributing elements (PNG) ---------------------------
def fig_Kmap():
    a, b, nodes, conn = mesh(4, 2, 2, 2)
    cols = {1: MAROON, 2: TEAL, 3: "#D98B2B", 4: "#6B5BA6"}
    img = np.ones((18, 18, 3))
    owner = [[[] for _ in range(18)] for _ in range(18)]
    for e, nd in enumerate(conn, 1):
        dofs = np.array([[2 * n, 2 * n + 1] for n in nd]).ravel()
        for i in dofs:
            for j in dofs:
                owner[i][j].append(e)
    fig, ax = plt.subplots(figsize=(6.6, 6.6), dpi=140)
    for i in range(18):
        for j in range(18):
            o = owner[i][j]
            if not o:
                fc = "#F2F2EF"
            elif len(o) == 1:
                fc = cols[o[0]]
            else:
                fc = GREEN
            ax.add_patch(Rectangle((j, 17 - i), 1, 1, facecolor=fc, edgecolor="white", lw=1.0))
            if len(o) > 1:
                ax.text(j + 0.5, 17 - i + 0.5, str(len(o)), ha="center", va="center", fontsize=7, color="white")
    ax.set_xlim(0, 18); ax.set_ylim(0, 18); ax.set_aspect("equal")
    ax.set_xticks(np.arange(18) + 0.5); ax.set_xticklabels([rf"$U_{{{i+1}}}$" for i in range(18)], fontsize=7, rotation=90)
    ax.set_yticks(np.arange(18) + 0.5); ax.set_yticklabels([rf"$U_{{{18-i}}}$" for i in range(18)], fontsize=7)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("[K] 18 × 18: which element fills each entry", fontsize=11, color=INK)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cols[1], label="element 1"), Patch(color=cols[2], label="element 2"), Patch(color=cols[3], label="element 3"), Patch(color=cols[4], label="element 4"), Patch(color=GREEN, label="shared (number = how many)"), Patch(color="#F2F2EF", label="zero")],
              fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False)
    fig.savefig(OUT / "fig_Kmap.png", dpi=140, facecolor="white", bbox_inches="tight", pad_inches=0.05); plt.close(fig)
    return dict(name="fig_Kmap.png", bytes=(OUT / "fig_Kmap.png").stat().st_size)
rep.append(fig_Kmap())

for r in rep:
    print(r)
