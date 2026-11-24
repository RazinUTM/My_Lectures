import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figlib import *
from matplotlib.patches import FancyBboxPatch
from fe_ps import solve_cantilever, Emat
from fe_ps8 import solve8

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("figs_w14")
OUT.mkdir(exist_ok=True, parents=True)
rep = []
GREEN = "#2E7D5B"

def box(ax, x, y, w, h, title, sub, fc=FILL, ec=NAVY, tc=NAVY, fs=12, fs2=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", facecolor=fc, edgecolor=ec, lw=1.6))
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=fs2, color=INK)

# 1. Workbench cells vs the textbook pipeline ---------------------------------------------
def fig_wb_flow():
    fig, ax = plt.subplots(figsize=(12.0, 4.2))
    ax.set_xlim(-0.2, 12.5); ax.set_ylim(-0.3, 4.1); ax.set_aspect("equal"); ax.axis("off")
    cells = [("Engineering Data", "E, ν  ·  k"), ("Geometry", "2D surface body"), ("Model / Mesh", "type · size · order"),
             ("Setup", "supports · loads"), ("Solution", "Solve"), ("Results", "contours · probes")]
    hand = [("[E]  or  k", "material matrix"), ("nodes, a, b", "the domain"), ("[k], [B], N", "shape functions"),
            ("{r}, Û = 0", "natural · essential"), ("[K]{U} = {R}", "reduced system"), ("[E][B]{û}", "post-processing")]
    w, h, gap = 1.84, 1.05, 0.22
    for i, ((t, s), (ht, hs)) in enumerate(zip(cells, hand)):
        x = i * (w + gap)
        box(ax, x, 2.6, w, h, t, s, fc=FILL, ec=NAVY, tc=NAVY, fs=10.5, fs2=9.5)
        box(ax, x, 0.7, w, h, ht, hs, fc="#FBF1D6", ec="#C9A227", tc=MAROON, fs=10.5, fs2=9.5)
        if i < 5:
            arrow(ax, (x + w + 0.02, 2.6 + h / 2), (x + w + gap - 0.02, 2.6 + h / 2), color=NAVY, lw=1.6, ms=10)
            arrow(ax, (x + w + 0.02, 0.7 + h / 2), (x + w + gap - 0.02, 0.7 + h / 2), color="#C9A227", lw=1.6, ms=10)
        ax.plot([x + w / 2, x + w / 2], [2.55, 1.8], color=GREY, lw=1.0, ls=(0, (3, 3)))
    ax.text(-0.1, 3.85, "ANSYS Workbench cells", ha="left", va="center", fontsize=12, color=NAVY, fontweight="bold")
    ax.text(-0.1, 0.25, "Weeks 9–13 by hand", ha="left", va="center", fontsize=12, color=MAROON, fontweight="bold")
    fig.savefig(OUT / "fig_wb_flow.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    return save_svg(fig, OUT / "fig_wb_flow.svg", "fig_wb_flow", "The six Workbench cells, Engineering Data to Results, drawn above the matching steps of the hand calculation: material matrix, domain, element matrices, boundary conditions, solve, post-processing")
rep.append(fig_wb_flow())

# 2. Heat plate in ANSYS terms --------------------------------------------------------------
def fig_plate_ansys():
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.set_xlim(-1.6, 6.6); ax.set_ylim(-1.9, 4.7); ax.set_aspect("equal"); ax.axis("off")
    S = 3.2
    ax.add_patch(Rectangle((0, 0), S, S, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    ax.plot([0, S], [S, S], color=MAROON, lw=5); ax.plot([0, 0], [0, S], color=MAROON, lw=5)
    ax.text(S / 2, S + 0.18, "Temperature = 0 °C", ha="center", va="bottom", fontsize=13, color=MAROON, fontweight="bold")
    ax.text(-0.2, S / 2, "Temperature = 0 °C", ha="right", va="center", fontsize=13, color=MAROON, fontweight="bold", rotation=90)
    ax.text(S / 2, -0.22, "no condition applied = insulated", ha="center", va="top", fontsize=12, color=TEAL)
    ax.text(S + 0.2, S / 2, "no condition = insulated", ha="left", va="center", fontsize=11, color=TEAL, rotation=-90)
    ax.text(S / 2, S / 2 + 0.35, "Internal Heat\nGeneration", ha="center", va="center", fontsize=12, color=INK, fontweight="bold", linespacing=1.1)
    ax.text(S / 2, S / 2 - 0.4, r"$600\ \mathrm{W\,m^{-3}}$ on the body", ha="center", va="center", fontsize=10.5, color=INK)
    node(ax, S, 0, None, r=0.1)
    ax.text(S + 0.6, -0.95, "probe: T at this corner\nexpected 0.5897 °C", ha="left", va="top", fontsize=11, color=GREEN)
    arrow(ax, (S + 0.75, -0.95), (S + 0.12, -0.12), color=GREEN, lw=1.2, ms=9)
    ax.text(S / 2, 4.25, r"$1\ \mathrm{m}\times1\ \mathrm{m},\ k=300\ \mathrm{W\,m^{-1}K^{-1}}$", ha="center", va="bottom", fontsize=12, color=INK)
    ax.text(S / 2, 3.95, "(Isotropic Thermal Conductivity)", ha="center", va="bottom", fontsize=11, color=INK)
    fig.savefig(OUT / "fig_plate_ansys.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    return save_svg(fig, OUT / "fig_plate_ansys.svg", "fig_plate_ansys", "The one metre square plate with its ANSYS boundary conditions: Temperature zero on the top and left edges, no condition on the other two edges, Internal Heat Generation on the body, and a temperature probe at the bottom-right corner")
rep.append(fig_plate_ansys())

# 3. Cantilever in ANSYS terms --------------------------------------------------------------
def fig_cant_ansys():
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.set_xlim(-2.1, 8.2); ax.set_ylim(-1.5, 3.7); ax.set_aspect("equal"); ax.axis("off")
    L, H = 5.2, 2.6
    ax.add_patch(Rectangle((0, 0), L, H, facecolor=FILL, edgecolor=NAVY, lw=2.2))
    for yy in np.arange(-0.1, H + 0.1, 0.22):
        ax.plot([-0.3, 0], [yy - 0.2, yy], color=NAVY, lw=1.3)
    ax.plot([0, 0], [-0.1, H + 0.1], color=MAROON, lw=5)
    ax.text(-0.45, H / 2, "Fixed Support\n(left edge)", ha="right", va="center", fontsize=13, color=MAROON, fontweight="bold")
    ax.plot([L, L], [0, H], color=TEAL, lw=5)
    for y in np.linspace(0.2, H - 0.2, 6):
        arrow(ax, (L + 0.55, y + 0.26), (L + 0.55, y - 0.26), color=TEAL, lw=1.8, ms=12)
    ax.text(L + 0.8, H / 2 + 0.5, "Force on the right edge", ha="left", va="center", fontsize=13, color=TEAL, fontweight="bold")
    ax.text(L + 0.8, H / 2 + 0.05, r"components: $F_y=-10\,000\ \mathrm{N}$", ha="left", va="center", fontsize=12, color=TEAL)
    ax.text(L + 0.8, H / 2 - 0.4, r"$= 5\ \mathrm{kN\,m^{-1}}\times 2\ \mathrm{m}$", ha="left", va="center", fontsize=12, color=TEAL)
    ax.text(L + 0.8, H / 2 - 0.9, r"or Pressure, components: $p_y=-500\ \mathrm{kPa}$", ha="left", va="center", fontsize=12, color=TEAL)
    ax.text(L + 0.8, H / 2 - 1.3, r"$= 5\ \mathrm{kN\,m^{-1}}\div 0.01\ \mathrm{m}$", ha="left", va="center", fontsize=12, color=TEAL)
    ax.text(L / 2, H / 2 + 0.3, "2D Behavior: Plane Stress", ha="center", va="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(L / 2, H / 2 - 0.25, r"Thickness $= 0.01\ \mathrm{m}$", ha="center", va="center", fontsize=13, color=INK)
    node(ax, L, H, None, r=0.1); ax.text(L - 0.15, H + 0.15, "probe: v at the tip\nexpected −0.192 m", ha="right", va="bottom", fontsize=11, color=GREEN)
    ax.text(L / 2, -0.35, r"$4\ \mathrm{m}\times2\ \mathrm{m},\ E=200\times10^{6}\ \mathrm{Pa},\ \nu=0.33$ (Isotropic Elasticity)", ha="center", va="top", fontsize=12, color=INK)
    fig.savefig(OUT / "fig_cant_ansys.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    return save_svg(fig, OUT / "fig_cant_ansys.svg", "fig_cant_ansys", "The cantilever with its ANSYS inputs: Fixed Support on the left edge, a Force of minus ten kilonewtons in y on the right edge or an equivalent pressure, plane stress behaviour with thickness 0.01 metre, and a deflection probe at the tip")
rep.append(fig_cant_ansys())

# 4. Convergence: linear vs quadratic, deflection vs dofs (PNG) -----------------------------
def fig_conv14():
    E, nu, t = 200e6, 0.33, 0.01; Em = Emat(E, nu)
    q4 = []; q8 = []
    for N in [(2, 2), (4, 2), (8, 4), (16, 8), (32, 16), (64, 32)]:
        nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, N[0], N[1], E, nu, t, -5000)
        i = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); q4.append((2 * len(nodes), -U[2 * i + 1]))
    for N in [(2, 1), (2, 2), (4, 2), (4, 4), (8, 4), (16, 8), (32, 16)]:
        nodes, conn, K, F, U = solve8(4, 2, N[0], N[1], Em, t, -5000)
        i = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); q8.append((2 * len(nodes), -U[2 * i + 1]))
    print("Q4:", [(d, round(v, 4)) for d, v in q4]); print("Q8:", [(d, round(v, 4)) for d, v in q8])
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=160)
    ax.axhline(0.192, color=GREY, lw=1.2, ls="--"); ax.text(1500, 0.1865, "Timoshenko 0.192 m", fontsize=9, color=GREY, va="top")
    ax.plot([d for d, v in q4], [v for d, v in q4], marker="o", ms=5, color=MAROON, lw=1.6, label="linear, 4-node (PLANE182 ≈ Q4)")
    ax.plot([d for d, v in q8], [v for d, v in q8], marker="s", ms=5, color=TEAL, lw=1.6, label="quadratic, 8-node (PLANE183 ≈ Q8)")
    for d, v in q4[:2] + q8[:1]:
        ax.annotate(f"{v:.3f}", (d, v), textcoords="offset points", xytext=(8, -12), fontsize=8, color=INK)
    ax.set_xscale("log"); ax.set_xlabel("degrees of freedom", fontsize=10); ax.set_ylabel("tip deflection (m)", fontsize=10)
    ax.set_ylim(0.12, 0.20); ax.tick_params(labelsize=8); ax.grid(True, lw=0.4, alpha=0.5); ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.set_title("Expected before the demo: course solvers, same meshes you will run", fontsize=10, color=INK)
    for s in ax.spines.values():
        s.set_linewidth(0.8)
    fig.tight_layout(); fig.savefig(OUT / "fig_conv14.png", dpi=160, facecolor="white"); plt.close(fig)
    return dict(name="fig_conv14.png", bytes=(OUT / "fig_conv14.png").stat().st_size)
rep.append(fig_conv14())

# 5. Four wrong models (mini sketches) ----------------------------------------------------
def fig_wrong():
    fig, axs = plt.subplots(1, 4, figsize=(12.4, 3.0))
    L, H = 2.6, 1.3
    def base(ax, title):
        ax.set_xlim(-1.0, 4.2); ax.set_ylim(-1.1, 2.3); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), L, H, facecolor=FILL, edgecolor=NAVY, lw=1.8))
        ax.text(L / 2, 2.1, title, ha="center", va="center", fontsize=12, color=MAROON, fontweight="bold")
    # (a) plane strain: draw a long prism behind
    ax = axs[0]; base(ax, "(a) 2D Behavior: Plane Strain")
    for d in [0.25, 0.5]:
        ax.add_patch(Rectangle((d, d), L, H, facecolor="none", edgecolor=GREY, lw=1.0, ls=(0, (3, 3))))
    ax.text(L / 2, -0.35, "strain out of plane set to zero:\nthe body behaves as a long prism", ha="center", va="top", fontsize=9.5, color=INK)
    # (b) point load at vertex
    ax = axs[1]; base(ax, "(b) Force on a vertex")
    arrow(ax, (L, H + 0.8), (L, H + 0.05), color=TEAL, lw=2.6, ms=16); ax.text(L + 0.15, H + 0.45, "10 kN", fontsize=10, color=TEAL)
    ax.plot([0, 0], [0, H], color=MAROON, lw=4)
    ax.text(L / 2, -0.35, "one node carries the whole load:\nstress spike under it", ha="center", va="top", fontsize=9.5, color=INK)
    # (c) displacement Y only
    ax = axs[2]; base(ax, "(c) Displacement: Y = 0 only")
    for y in np.linspace(0.15, H - 0.15, 4):
        ax.add_patch(Circle((-0.18, y), 0.09, facecolor=LIGHT, edgecolor=MAROON, lw=1.4))
    ax.text(L / 2, -0.35, "free to slide in x:\nrigid-body motion, solver warning", ha="center", va="top", fontsize=9.5, color=INK)
    # (d) thickness default
    ax = axs[3]; base(ax, "(d) Thickness left at default")
    ax.text(L / 2, H / 2, "t = 1 m ?", ha="center", va="center", fontsize=13, color=MAROON, fontweight="bold")
    ax.text(L / 2, -0.35, "deflection scales with 1/t:\na clean factor of 100", ha="center", va="top", fontsize=9.5, color=INK)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02, wspace=0.05)
    fig.savefig(OUT / "fig_wrong.png", dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    return save_svg(fig, OUT / "fig_wrong.svg", "fig_wrong", "Four deliberately wrong versions of the cantilever model: plane strain instead of plane stress, a force on a single vertex, a support that fixes only the vertical direction, and a thickness left at its default")
rep.append(fig_wrong())

for r in rep:
    print(r)
