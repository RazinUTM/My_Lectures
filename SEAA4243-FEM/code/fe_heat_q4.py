"""
SEAA 4243 Finite Element Method - steady 2D heat conduction with 4-node elements
================================================================================

Companion code for the Heat Conduction Explorer (2D Heat Transfer, Part 2).
It follows the seven steps of the course, in the text's notation
(Mohd Yassin et al., MSNM 2020, Chapter 2):

    1-2  mesh of a rectangular plate, L x H, Nx x Ny four-node elements
    5    element matrix [k] from the closed-form s1...s4         text (2.49)
         source loads {q} = t Q ab/4 at each node                text (2.39)
         edge-flux loads {b} = t q_n l/2 at each edge node        text (2.40)
    6    assembly by the connectivity table (scatter-add),
         known temperatures by row-column elimination
    7    solve; heat flows at the fixed nodes (energy balance);
         temperature and heat flux at any point

Mesh and numbering
    Nodes are numbered left to right, then bottom to top, starting at 1 in
    the printout (the text's 2 x 2 mesh: nodes 1-3 along the bottom, 7-9 along
    the top). Element e has local nodes 1-4 anticlockwise from its bottom-left
    corner, e.g. element 1 of the 2 x 2 mesh = global nodes [1 2 5 4].

Units
    Any consistent set; the examples use m, W and degC (or K).
    Q is heat generated per unit VOLUME (W/m3) and is multiplied by t.
    A source given per unit AREA of the plate (W/m2) already contains the
    thickness: use t = 1 and Q = that value.
    q_n is the INWARD boundary flux (W/m2); an insulated edge has q_n = 0.

Run
    python fe_heat_q4.py
        reproduces the text's worked example (Sec. 2.3), its energy balance
        and mesh study, and the 2 x 2 plate with an inward flux; saves a
        contour plot if matplotlib is installed.

Use for your own problem: edit the block at the bottom, or
    from fe_heat_q4 import solve_plate, temperature_at
    res = solve_plate(L=4, H=2, Nx=4, Ny=2, kx=10, ky=10,
                      edges={"left": ("T", 50), "right": ("flux", 200),
                             "top": ("insulated",), "bottom": ("insulated",)},
                      Q=lambda xc, yc: 100 if xc < 1 else 0)  # source in the first column only
    print(res["K"])                     # compare with your hand assembly
    print(temperature_at(res, 1.4, 0.7))

A hand calculation is still a hand calculation: use this script to check your
matrices and numbers, and show the steps yourself.

Requires Python 3.8+ and numpy; matplotlib only for the plot.
Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
Code: MIT licence.
"""
import numpy as np


# ---------------------------------------------------------------------------
# Step 5: element matrix and loads
# ---------------------------------------------------------------------------
def s_values(a, b, kx, ky):
    """The four distinct entries of [k] for an a x b rectangle, text (2.49)."""
    s1 = b * kx / (3 * a) + a * ky / (3 * b)
    s2 = -b * kx / (3 * a) + a * ky / (6 * b)
    s3 = -b * kx / (6 * a) - a * ky / (6 * b)
    s4 = b * kx / (6 * a) - a * ky / (3 * b)
    return s1, s2, s3, s4


def element_matrix(a, b, kx, ky, t=1.0):
    """Conductance matrix [k] (4 x 4, W/K). Every row adds up to zero."""
    s1, s2, s3, s4 = s_values(a, b, kx, ky)
    return t * np.array([[s1, s2, s3, s4],
                         [s2, s1, s4, s3],
                         [s3, s4, s1, s2],
                         [s4, s3, s2, s1]])


# ---------------------------------------------------------------------------
# Steps 1-2: mesh
# ---------------------------------------------------------------------------
def mesh(L, H, Nx, Ny):
    """Node coordinates (n x 2) and connectivity (ne x 4, 0-based) of a structured mesh."""
    a, b = L / Nx, H / Ny
    nodes = np.array([(i * a, j * b) for j in range(Ny + 1) for i in range(Nx + 1)], dtype=float)
    conn = []
    for j in range(Ny):
        for i in range(Nx):
            n1 = j * (Nx + 1) + i
            conn.append([n1, n1 + 1, n1 + Nx + 2, n1 + Nx + 1])
    return a, b, nodes, np.array(conn, dtype=int)


def edge_nodes(nodes, L, H, edge, tol=1e-9):
    """Indices of the nodes on one edge of the plate, ordered along it."""
    x, y = nodes[:, 0], nodes[:, 1]
    if edge == "bottom":
        idx = np.where(abs(y) < tol)[0]; key = x
    elif edge == "top":
        idx = np.where(abs(y - H) < tol)[0]; key = x
    elif edge == "left":
        idx = np.where(abs(x) < tol)[0]; key = y
    elif edge == "right":
        idx = np.where(abs(x - L) < tol)[0]; key = y
    else:
        raise ValueError("edge must be bottom, right, top or left")
    return idx[np.argsort(key[idx])]


# ---------------------------------------------------------------------------
# Steps 5-7: assemble, impose, solve, post-process
# ---------------------------------------------------------------------------
def solve_plate(L, H, Nx, Ny, kx, ky=None, edges=None, Q=0.0, t=1.0):
    """Solve a rectangular plate.

    edges: dict with keys "bottom", "right", "top", "left"; each value is
           ("T", value)  prescribed temperature (essential)
           ("flux", qn)  inward heat flux, W/m2 (natural)
           ("insulated",) zero flux (natural; nothing to do)
           A corner shared by two prescribed edges takes the value of the
           first in the order top, left, right, bottom.
    Q:     heat generated per unit volume, a number or a function Q(xc, yc)
           of the element centroid (for a source on some elements only).
    Returns a dict with the mesh, [K], {R}, the temperatures and the heat
    flows at the fixed nodes.
    """
    ky = kx if ky is None else ky
    edges = edges or {}
    a, b, nodes, conn = mesh(L, H, Nx, Ny)
    n = len(nodes)
    K = np.zeros((n, n))
    R = np.zeros(n)
    k = element_matrix(a, b, kx, ky, t)
    generated = 0.0
    for e, c in enumerate(conn):
        K[np.ix_(c, c)] += k                                   # scatter-add
        xc, yc = nodes[c].mean(axis=0)
        Qe = Q(xc, yc) if callable(Q) else Q
        R[c] += t * Qe * a * b / 4                             # {q}: equal shares
        generated += t * Qe * a * b
    flux_in = 0.0
    for name, bc in edges.items():
        if bc[0] == "flux":
            ids = edge_nodes(nodes, L, H, name)
            h = b if name in ("left", "right") else a
            for i0, i1 in zip(ids[:-1], ids[1:]):
                R[i0] += t * bc[1] * h / 2                     # {b}: half to each node of the side
                R[i1] += t * bc[1] * h / 2
                flux_in += t * bc[1] * h
    fixed = {}
    for name in ("top", "left", "right", "bottom"):
        bc = edges.get(name, ("insulated",))
        if bc[0] == "T":
            for i in edge_nodes(nodes, L, H, name):
                fixed.setdefault(int(i), float(bc[1]))
    if not fixed:
        raise ValueError("No edge has a prescribed temperature: [K] is singular "
                         "(the temperature level is undetermined).")
    known = np.array(sorted(fixed))
    Tbar = np.array([fixed[i] for i in known])
    free = np.setdiff1d(np.arange(n), known)
    T = np.zeros(n)
    T[known] = Tbar
    # row-column elimination: move K(:, known) * Tbar to the right, keep the free rows
    rhs = R[free] - K[np.ix_(free, known)] @ Tbar
    T[free] = np.linalg.solve(K[np.ix_(free, free)], rhs)
    heat = K[known] @ T - R[known]          # struck rows: heat supplied (+) or removed (-) there
    return dict(L=L, H=H, Nx=Nx, Ny=Ny, a=a, b=b, kx=kx, ky=ky, t=t, nodes=nodes, conn=conn,
                K=K, R=R, T=T, known=known, free=free, heat=heat,
                generated=generated, flux_in=flux_in)


def locate(res, x, y):
    """Element containing the global point (x, y), and the local coordinates there."""
    a, b = res["a"], res["b"]
    i = min(res["Nx"] - 1, max(0, int(np.floor(x / a + 1e-12))))
    j = min(res["Ny"] - 1, max(0, int(np.floor(y / b + 1e-12))))
    e = j * res["Nx"] + i
    x1, y1 = res["nodes"][res["conn"][e][0]]
    return e, x - x1, y - y1


def temperature_at(res, x, y):
    """T and the heat flux (qx, qy) at a global point, from the element that contains it."""
    a, b = res["a"], res["b"]
    e, xl, yl = locate(res, x, y)
    Te = res["T"][res["conn"][e]]                       # nodal values in LOCAL order
    N = np.array([(a - xl) * (b - yl), xl * (b - yl), xl * yl, yl * (a - xl)]) / (a * b)
    dN = np.array([[-(b - yl), (b - yl), yl, -yl],
                   [-(a - xl), -xl, xl, (a - xl)]]) / (a * b)
    g = dN @ Te
    return dict(element=e + 1, local=(xl, yl), N=N, T=float(N @ Te),
                qx=float(-res["kx"] * g[0]), qy=float(-res["ky"] * g[1]))


def print_matrix(M, scale=1.0, name="[K]"):
    with np.printoptions(precision=3, suppress=True, linewidth=160):
        print(f"{name}" + (f" / {scale:g}" if scale != 1 else "") + " =")
        print(M / scale)


def plot_temperature(res, filename="temperature.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed: skipping the plot")
        return None
    xs = np.linspace(0, res["L"], 121)
    ys = np.linspace(0, res["H"], max(31, int(121 * res["H"] / res["L"])))
    X, Y = np.meshgrid(xs, ys)
    Z = np.vectorize(lambda x, y: temperature_at(res, x, y)["T"])(X, Y)
    fig, ax = plt.subplots(figsize=(6, 6 * res["H"] / res["L"] + 0.6))
    cf = ax.contourf(X, Y, Z, levels=21, cmap="jet")
    ax.contour(X, Y, Z, levels=10, colors="k", linewidths=0.5)
    for c in res["conn"]:
        p = res["nodes"][list(c) + [c[0]]]
        ax.plot(p[:, 0], p[:, 1], color="w", lw=0.8)
    ax.set_aspect("equal"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    fig.colorbar(cf, ax=ax, label="T")
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", filename)
    return filename


# ---------------------------------------------------------------------------
# Course examples
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # The text's worked example (Sec. 2.3): 1 m square, Q = 600 W/m3, k = 300,
    # top and left edges at 0 degC, right and bottom insulated, unit thickness.
    book = {"top": ("T", 0.0), "left": ("T", 0.0), "right": ("insulated",), "bottom": ("insulated",)}
    res = solve_plate(1, 1, 2, 2, 300, edges=book, Q=600)
    print("Text Sec. 2.3, 2 x 2 mesh")
    print("  element s1..s4 =", np.round(s_values(0.5, 0.5, 300, 300), 3), " (expected 200 -50 -100 -50)")
    print_matrix(res["K"], name="  [K]")
    print("  {R} =", res["R"])
    T = res["T"]
    print(f"  T2 = T6 = {T[1]:.4f}, T3 = {T[2]:.4f}, T5 = {T[4]:.4f} degC  (text (2.55): 0.4821, 0.6214, 0.3857)")
    print("  heat at fixed nodes", [int(i) + 1 for i in res["known"]], "=", np.round(res["heat"], 2), "W")
    print(f"  energy balance: generated {res['generated']:.1f} W, removed {-res['heat'].sum():.1f} W")
    p = temperature_at(res, 0.3, 0.2)
    print(f"  T(0.3, 0.2) = {p['T']:.4f} degC in element {p['element']}  (Activity 6: 0.266)")
    p = temperature_at(res, 0.75, 0.25)
    print(f"  flux at the centroid of element 2 = ({p['qx']:.1f}, {p['qy']:.1f}) W/m2  (-70.5, +70.5)")

    print("\nMesh study, T at the corner (1, 0); exact 0.5894 degC")
    prev = None
    for n in (1, 2, 4, 8, 16, 32):
        r = solve_plate(1, 1, n, n, 300, edges=book, Q=600)
        tc = temperature_at(r, 1.0, 0.0)["T"]
        change = "" if prev is None else f"  change {100 * (tc - prev) / tc:+.2f} %"
        print(f"  {n:2d} x {n:<2d}  T = {tc:.4f}{change}")
        prev = tc

    # Companion Example 8.6 (textbook Exercise 2.4): 0.05 m square, t = 0.005 m, k = 450,
    # left side at 400 K, inward flux 1e6 W/m2 on the right, top and bottom insulated.
    res2 = solve_plate(0.05, 0.05, 2, 2, 450, t=0.005,
                       edges={"left": ("T", 400), "right": ("flux", 1e6), "top": ("insulated",), "bottom": ("insulated",)})
    print("\nPlate with an inward flux, 2 x 2 mesh")
    print(f"  T5 = {res2['T'][4]:.2f} K, T6 = {res2['T'][5]:.2f} K  (expected 455.56, 511.11)")
    print("  heat at nodes 1, 4, 7 =", np.round(res2["heat"], 2), "W; flux in =", res2["flux_in"], "W")

    plot_temperature(solve_plate(1, 1, 16, 16, 300, edges=book, Q=600), "temperature_16x16.png")

    # ---- your problem: edit and run -------------------------------------
    # mine = solve_plate(L=..., H=..., Nx=..., Ny=..., kx=..., edges={...}, Q=..., t=...)
    # print_matrix(mine["K"], scale=1.0)
    # print(mine["T"])
    # print(temperature_at(mine, x, y))
