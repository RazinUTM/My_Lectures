import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *
from fe_ps import solve_cantilever, Bmat, Emat

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w13")
OUT.mkdir(exist_ok=True, parents=True)
rep = []
E, nu, t = 200e6, 0.33, 0.01; Em = Emat(E, nu); I = t * 8 / 12

def centroid_stress(Nx, Ny):
    nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, Nx, Ny, E, nu, t, -5000)
    cent = []; sig = []
    for e in conn:
        dofs = np.array([[2 * n, 2 * n + 1] for n in e]).ravel()
        s = Em @ (Bmat(a, b, a / 2, b / 2) @ U[dofs]); x1, y1 = nodes[e[0]]
        cent.append((x1 + a / 2, y1 + b / 2)); sig.append(s)
    return np.array(cent), np.array(sig), a, b

# 1. sigma_xx contour (element-wise, 32x16) + line plot through the depth ---------------
def fig_sxx():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.0), dpi=160, gridspec_kw={"width_ratios": [1.5, 1]})
    cent, sig, a, b = centroid_stress(32, 16)
    Z = sig[:, 0].reshape(16, 32) / 1e3
    vmax = 3000
    im = a1.imshow(Z, origin="lower", extent=[0, 4, 0, 2], cmap="jet", vmin=-vmax, vmax=vmax, aspect="equal", interpolation="nearest")
    a1.set_title(r"$\sigma_{xx}$ at element centroids, $32\times16$ mesh (kN m$^{-2}$)", fontsize=11, color=INK)
    a1.set_xlabel(r"$x$ (m)", fontsize=10); a1.set_ylabel(r"$y$ (m)", fontsize=10); a1.tick_params(labelsize=8)
    cb = fig.colorbar(im, ax=a1, fraction=0.025, pad=0.02); cb.ax.tick_params(labelsize=8); cb.set_label(r"kN m$^{-2}$ (clipped at $\pm3000$)", fontsize=8)
    a1.plot([2, 2], [0, 2], color="k", ls="--", lw=1)
    # line through depth at x ~ 2 (centroids at x = 2 - a/2 and 2 + a/2 -> take the column just left)
    xc = 2 - a / 2
    m = np.isclose(cent[:, 0], xc)
    ys = cent[m, 1]; sx = sig[m, 0] / 1e3
    yb = np.linspace(0, 2, 50); M = 10000 * (4 - xc); sbeam = M * (yb - 1) / I / 1e3
    a2.plot(sbeam, yb, color=TEAL, lw=1.8, ls="--", label="beam theory, M(y − 1)/I")
    a2.plot(sx, ys, marker="o", ms=4, color=MAROON, lw=1.2, label="FE centroids, 32 × 16")
    a2.set_xlabel(r"$\sigma_{xx}$ (kN m$^{-2}$)", fontsize=10); a2.set_ylabel(r"$y$ (m)", fontsize=10); a2.set_title(r"through the depth at $x\approx2$ m", fontsize=11, color=INK)
    a2.legend(fontsize=8, frameon=False, loc="upper left"); a2.grid(True, lw=0.4, alpha=0.5); a2.tick_params(labelsize=8)
    for ax in (a1, a2):
        for s in ax.spines.values():
            s.set_visible(True); s.set_linewidth(0.8)
    fig.subplots_adjust(left=0.05, right=0.99, top=0.88, bottom=0.16, wspace=0.42)
    fig.savefig(OUT / "fig_sxx.png", dpi=160, facecolor="white", bbox_inches="tight", pad_inches=0.05); plt.close(fig)
    print("depth line (32x16):", list(zip(np.round(ys, 3), np.round(sx, 0))))
    return dict(name="fig_sxx.png", bytes=(OUT / "fig_sxx.png").stat().st_size)
rep.append(fig_sxx())

# 2. Q8 mesh 2x1 (book Fig 3.6) ------------------------------------------------------------
def fig_q8_mesh():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.set_xlim(-0.9, 6.4); ax.set_ylim(-1.0, 3.6); ax.set_aspect("equal"); ax.axis("off")
    L, H = 5.2, 2.6; hx = L / 2
    for j in range(2):
        ax.add_patch(Rectangle((j * hx, 0), hx, H, facecolor=FILL, edgecolor=NAVY, lw=2))
        ax.add_patch(Rectangle((j * hx + hx / 2 - 0.2, H / 2 - 0.2), 0.4, 0.4, facecolor=LIGHT, edgecolor=NAVY, lw=1.3))
        ax.text(j * hx + hx / 2, H / 2, str(j + 1), ha="center", va="center", fontsize=14, color=NAVY)
    for yy in np.arange(-0.1, H + 0.1, 0.22):
        ax.plot([-0.3, 0], [yy - 0.2, yy], color=NAVY, lw=1.2)
    # book Fig 3.6 numbering: bottom row 1..5, middle 6,7,8 at x=0,2,4, top 9..13
    pts = {1: (0, 0), 2: (hx / 2, 0), 3: (hx, 0), 4: (1.5 * hx, 0), 5: (L, 0), 6: (0, H / 2), 7: (hx, H / 2), 8: (L, H / 2),
           9: (0, H), 10: (hx / 2, H), 11: (hx, H), 12: (1.5 * hx, H), 13: (L, H)}
    for n, (x, y) in pts.items():
        node(ax, x, y, str(n), r=0.19, fontsize=12)
    ax.plot([L + 0.6, L + 0.6], [0, H], color=TEAL, lw=2)
    for y in np.linspace(0.15, H - 0.15, 7):
        arrow(ax, (L + 0.6, y + 0.22), (L + 0.6, y - 0.22), color=TEAL, lw=1.6, ms=11)
    ax.text(L + 0.8, H / 2, r"$q_y$", ha="left", va="center", fontsize=17, color=TEAL)
    ax.plot([0, L], [-0.6, -0.6], color=INK, lw=1.2)
    for xx in [0, hx, L]:
        ax.plot([xx, xx], [-0.7, -0.5], color=INK, lw=1.2)
    ax.text(hx / 2, -0.75, r"$2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK); ax.text(1.5 * hx, -0.75, r"$2\ \mathrm{m}$", ha="center", va="top", fontsize=13, color=INK)
    ax.text(L / 2, H + 0.35, r"$\mathrm{two\ 8\!-\!node\ elements,\ 13\ nodes,\ 26\ dofs}$", ha="center", va="bottom", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_q8_mesh.svg", "fig_q8_mesh", "The cantilever meshed with two eight-node elements: thirteen nodes, corner and mid-side, numbered 1 to 13 as in the text")
rep.append(fig_q8_mesh())

# 3. Q8 edge loads 1/6, 2/3, 1/6 -----------------------------------------------------------
def fig_q8_loads():
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.set_xlim(-0.8, 10.2); ax.set_ylim(-1.7, 3.0); ax.set_aspect("equal"); ax.axis("off")
    A, B = 3.0, 2.0
    for x0, kind in [(0, "trac"), (6.0, "nodal")]:
        ax.add_patch(Rectangle((x0, 0), A, B, facecolor=FILL, edgecolor=NAVY, lw=2))
        for (x, y) in [(x0, 0), (x0 + A / 2, 0), (x0 + A, 0), (x0, B / 2), (x0 + A, B / 2), (x0, B), (x0 + A / 2, B), (x0 + A, B)]:
            node(ax, x, y, None, r=0.12)
        if kind == "trac":
            ax.plot([A + 0.55, A + 0.55], [0, B], color=TEAL, lw=2)
            for y in np.linspace(0.15, B - 0.15, 6):
                arrow(ax, (A + 0.55, y + 0.22), (A + 0.55, y - 0.22), color=TEAL, lw=1.8, ms=12)
            ax.text(A + 0.75, B / 2, r"$q_y$", ha="left", va="center", fontsize=18, color=TEAL)
        else:
            for y, lab, lw in [(0, r"$\frac{1}{6}q_yb$", 2.4), (B / 2, r"$\frac{2}{3}q_yb$", 3.6), (B, r"$\frac{1}{6}q_yb$", 2.4)]:
                arrow(ax, (x0 + A, y), (x0 + A, y - 0.7), color=MAROON, lw=lw, ms=16)
                ax.text(x0 + A + 0.2, y - 0.35, lab, ha="left", va="center", fontsize=16, color=MAROON)
    arrow(ax, (4.5, B / 2), (5.2, B / 2), color=AMBER, lw=4, ms=26)
    ax.text(A / 2, -1.0, r"$\mathrm{uniform\ traction\ on\ a\ 3\!-\!node\ edge}$", ha="center", va="top", fontsize=13, color=INK)
    ax.text(6.0 + A / 2, -1.0, r"$\mathrm{corner\ }\frac{1}{6},\ \mathrm{mid\!-\!side\ }\frac{2}{3},\ \mathrm{corner\ }\frac{1}{6}$", ha="center", va="top", fontsize=13, color=INK)
    return save_svg(fig, OUT / "fig_q8_loads.svg", "fig_q8_loads", "A uniform traction on the three-node edge of an eight-node element becomes nodal loads of one sixth, two thirds and one sixth of the total")
rep.append(fig_q8_loads())

for r in rep:
    print(r)
