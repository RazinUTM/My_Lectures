"""
SEAA 4243 Finite Element Method - plane stress with 4-node and 8-node elements
==============================================================================

Companion code for the Cantilever and Stress Recovery Explorers (Plane Stress).
It follows the course's steps in the text's notation (Mohd Yassin et al.,
MSNM 2020, Chapter 3):

    [E]   3 x 3 material matrix, plane stress or plane strain       text (3.10)
    [B]   strains from nodal displacements, {eps} = [d]^T[N]{u}     weak form (3.31)-(3.38)
    [k]   = t * integral [B]^T [E] [B] dA                          closed form (3.42);
          here by Gauss quadrature (2 x 2 points for the 4-node
          element, 3 x 3 for the 8-node), which reproduces (3.42)
    loads a uniform traction on the free end becomes consistent nodal
          loads: q b/2 to each node (4-node, (3.45)); q b/6, 2q b/3,
          q b/6 (8-node, (3.51))
    solve assemble (3.46), strike the fixed edge's rows and columns
          (3.48), solve (3.49); reactions from the struck rows;
          stresses {sigma} = [E][B]{u} at any point; principal stresses,
          von Mises, and nodal averaging as in ANSYS.

The built-in problem is the text's cantilever: a plate 4 m x 2 m,
t = 0.01 m, E = 200e6 N/m2, nu = 0.33, fixed at x = 0, loaded at x = 4 by a
uniform downward traction of 5000 N per metre of edge (P = 10 kN in total).
The functions take any L, H, mesh, material, thickness and load.

Mesh and numbering
    4-node: nodes left to right, then bottom to top (the text's 2 x 2 mesh:
    nodes 1-3 along the bottom). dof 2i-1 = u_i, dof 2i = v_i (1-based).
    8-node: corner and mid-side nodes are numbered in the order they are
    created; use node_at(res, x, y) to find a node.

Units
    Any consistent set. The example uses N and m, so stresses come out in
    N/m2 (divide by 1e3 for kN/m2). The traction q is force per unit length
    of the loaded edge (N/m), the thickness already included.

Run
    python fe_plane_stress.py
        reproduces the 2 x 2 cantilever (tip deflection, reactions, stresses
        at (3.5, 1.3)), the convergence of the 4- and 8-node meshes against
        Timoshenko beam theory, and the growth of the stress at the fixed
        corner; saves a von Mises contour plot if matplotlib is installed.

Use for your own model
    from fe_plane_stress import solve_cantilever, stress_at, principal, von_mises
    res = solve_cantilever(L=4, H=2, Nx=8, Ny=4, E=200e6, nu=0.33, t=0.01, q=-5000, nen=8)
    s = stress_at(res, 2.0, 1.3)        # (sxx, syy, sxy)

A hand calculation is still a hand calculation: use this script to check your
matrices and numbers, and to run the mesh study a project needs.
Dense numpy solver: fine up to a few thousand degrees of freedom.

Requires Python 3.8+ and numpy; matplotlib only for the plot.
Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
Code: MIT licence.
"""
import numpy as np


# ---------------------------------------------------------------------------
# Material
# ---------------------------------------------------------------------------
def E_matrix(E, nu, plane="stress"):
    """[E] of text (3.10) for plane stress; plane strain when plane = "strain"."""
    if plane == "stress":
        c = E / (1 - nu ** 2)
        return c * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
    c = E / ((1 + nu) * (1 - 2 * nu))
    return c * np.array([[1 - nu, nu, 0], [nu, 1 - nu, 0], [0, 0, (1 - 2 * nu) / 2]])


# ---------------------------------------------------------------------------
# Shape functions in natural coordinates xi, eta in [-1, 1]
# ---------------------------------------------------------------------------
XI = np.array([-1, 1, 1, -1, 0, 1, 0, -1], dtype=float)
ETA = np.array([-1, -1, 1, 1, -1, 0, 1, 0], dtype=float)


def shape(nen, xi, eta):
    """N (nen,) and dN/dxi, dN/deta (2, nen) of the 4-node or 8-node element."""
    if nen == 4:
        N = 0.25 * (1 + XI[:4] * xi) * (1 + ETA[:4] * eta)
        dN = np.vstack([0.25 * XI[:4] * (1 + ETA[:4] * eta), 0.25 * ETA[:4] * (1 + XI[:4] * xi)])
        return N, dN
    N = np.zeros(8); dN = np.zeros((2, 8))
    for i in range(4):
        cx, cy = XI[i], ETA[i]
        N[i] = 0.25 * (1 + cx * xi) * (1 + cy * eta) * (cx * xi + cy * eta - 1)
        dN[0, i] = 0.25 * cx * (1 + cy * eta) * (2 * cx * xi + cy * eta)
        dN[1, i] = 0.25 * cy * (1 + cx * xi) * (cx * xi + 2 * cy * eta)
    N[4] = 0.5 * (1 - xi ** 2) * (1 - eta); dN[:, 4] = [-xi * (1 - eta), -0.5 * (1 - xi ** 2)]
    N[5] = 0.5 * (1 + xi) * (1 - eta ** 2); dN[:, 5] = [0.5 * (1 - eta ** 2), -eta * (1 + xi)]
    N[6] = 0.5 * (1 - xi ** 2) * (1 + eta); dN[:, 6] = [-xi * (1 + eta), 0.5 * (1 - xi ** 2)]
    N[7] = 0.5 * (1 - xi) * (1 - eta ** 2); dN[:, 7] = [-0.5 * (1 - eta ** 2), -eta * (1 - xi)]
    return N, dN


def B_matrix(nen, a, b, xi, eta):
    """[B] (3 x 2nen) of an a x b rectangle at (xi, eta): rows exx, eyy, gamma_xy."""
    _, dN = shape(nen, xi, eta)
    dx, dy = dN[0] * 2 / a, dN[1] * 2 / b
    B = np.zeros((3, 2 * nen))
    B[0, 0::2] = dx
    B[1, 1::2] = dy
    B[2, 0::2] = dy
    B[2, 1::2] = dx
    return B


def element_stiffness(nen, a, b, Em, t):
    """[k] = t * integral [B]^T[E][B] dA by Gauss quadrature (2 x 2 for Q4, 3 x 3 for Q8)."""
    g, w = np.polynomial.legendre.leggauss(2 if nen == 4 else 3)
    k = np.zeros((2 * nen, 2 * nen))
    for xi, wi in zip(g, w):
        for eta, wj in zip(g, w):
            B = B_matrix(nen, a, b, xi, eta)
            k += t * (a / 2) * (b / 2) * wi * wj * B.T @ Em @ B
    return k


# ---------------------------------------------------------------------------
# Mesh
# ---------------------------------------------------------------------------
def mesh(nen, L, H, Nx, Ny):
    a, b = L / Nx, H / Ny
    if nen == 4:
        nodes = np.array([(i * a, j * b) for j in range(Ny + 1) for i in range(Nx + 1)], dtype=float)
        conn = [[j * (Nx + 1) + i, j * (Nx + 1) + i + 1, (j + 1) * (Nx + 1) + i + 1, (j + 1) * (Nx + 1) + i]
                for j in range(Ny) for i in range(Nx)]
        return a, b, nodes, np.array(conn, dtype=int)
    ids, nodes = {}, []
    def node(x, y):
        key = (round(x, 9), round(y, 9))
        if key not in ids:
            ids[key] = len(nodes); nodes.append((x, y))
        return ids[key]
    conn = []
    for j in range(Ny):
        for i in range(Nx):
            x0, y0 = i * a, j * b
            conn.append([node(x0, y0), node(x0 + a, y0), node(x0 + a, y0 + b), node(x0, y0 + b),
                         node(x0 + a / 2, y0), node(x0 + a, y0 + b / 2), node(x0 + a / 2, y0 + b), node(x0, y0 + b / 2)])
    return a, b, np.array(nodes, dtype=float), np.array(conn, dtype=int)


def dofs_of(c):
    return np.ravel([[2 * n, 2 * n + 1] for n in c])


# ---------------------------------------------------------------------------
# Solve the cantilever
# ---------------------------------------------------------------------------
def solve_cantilever(L=4.0, H=2.0, Nx=2, Ny=2, E=200e6, nu=0.33, t=0.01, q=-5000.0,
                     nen=4, plane="stress", load="edge"):
    """Fixed at x = 0; vertical load on x = L. load = "edge": uniform traction q (N/m)
    by consistent nodal loads; load = "point": the total q*H at the top-right node."""
    Em = E_matrix(E, nu, plane)
    a, b, nodes, conn = mesh(nen, L, H, Nx, Ny)
    n = len(nodes)
    K = np.zeros((2 * n, 2 * n))
    F = np.zeros(2 * n)
    k = element_stiffness(nen, a, b, Em, t)
    for c in conn:
        d = dofs_of(c)
        K[np.ix_(d, d)] += k                                   # scatter-add by dof map
    if load == "point":
        F[2 * node_at_xy(nodes, L, H) + 1] += q * H
    else:
        for c in conn:
            if np.isclose(nodes[c[1], 0], L):                   # element side 2-3 on the loaded edge
                if nen == 4:
                    F[2 * c[1] + 1] += q * b / 2; F[2 * c[2] + 1] += q * b / 2
                else:
                    F[2 * c[1] + 1] += q * b / 6; F[2 * c[5] + 1] += 2 * q * b / 3; F[2 * c[2] + 1] += q * b / 6
    fixed_nodes = np.where(np.isclose(nodes[:, 0], 0.0))[0]
    known = dofs_of(fixed_nodes)
    free = np.setdiff1d(np.arange(2 * n), known)
    U = np.zeros(2 * n)
    U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    Rk = K[known] @ U - F[known]                               # struck rows: support reactions
    Rx, Ry = Rk[0::2].sum(), Rk[1::2].sum()
    M = sum(-(nodes[nd, 1] - H / 2) * Rk[2 * i] for i, nd in enumerate(fixed_nodes))
    return dict(nen=nen, L=L, H=H, Nx=Nx, Ny=Ny, a=a, b=b, E=E, nu=nu, t=t, q=q, plane=plane, Em=Em,
                nodes=nodes, conn=conn, K=K, F=F, U=U, known=known, reactions=dict(Rx=Rx, Ry=Ry, M=M),
                tip=U[2 * node_at_xy(nodes, L, H) + 1])


def node_at_xy(nodes, x, y):
    return int(np.argmin(np.hypot(nodes[:, 0] - x, nodes[:, 1] - y)))


def node_at(res, x, y):
    """0-based index of the node nearest to (x, y)."""
    return node_at_xy(res["nodes"], x, y)


# ---------------------------------------------------------------------------
# Stresses
# ---------------------------------------------------------------------------
def locate(res, x, y):
    """Element containing (x, y) and the natural coordinates of the point in it."""
    i = min(res["Nx"] - 1, max(0, int(np.floor(x / res["a"] + 1e-12))))
    j = min(res["Ny"] - 1, max(0, int(np.floor(y / res["b"] + 1e-12))))
    e = j * res["Nx"] + i
    x1, y1 = res["nodes"][res["conn"][e][0]]
    return e, 2 * (x - x1) / res["a"] - 1, 2 * (y - y1) / res["b"] - 1


def stress_in_element(res, e, xi, eta):
    c = res["conn"][e]
    B = B_matrix(res["nen"], res["a"], res["b"], xi, eta)
    return res["Em"] @ (B @ res["U"][dofs_of(c)])


def stress_at(res, x, y):
    """(sxx, syy, sxy) at a global point, from the element that contains it."""
    e, xi, eta = locate(res, x, y)
    return stress_in_element(res, e, xi, eta)


def principal(s):
    """sigma1, sigma2 and the angle (degrees) of sigma1 from x: the Mohr circle."""
    c = (s[0] + s[1]) / 2
    R = np.hypot((s[0] - s[1]) / 2, s[2])
    return c + R, c - R, 0.5 * np.degrees(np.arctan2(2 * s[2], s[0] - s[1]))


def von_mises(s):
    """Plane-stress von Mises stress."""
    return np.sqrt(s[0] ** 2 - s[0] * s[1] + s[1] ** 2 + 3 * s[2] ** 2)


def nodal_stresses(res, mode="averaged"):
    """Stresses at the nodes, as post-processors show them.
    "unaveraged": each element's own value at its nodes, (ne, nen, 3) - jumps visible;
    "averaged":   the mean over the elements sharing each node, (n, 3);
    "centroid":   one value per element, (ne, 3)."""
    nen, conn = res["nen"], res["conn"]
    if mode == "centroid":
        return np.array([stress_in_element(res, e, 0, 0) for e in range(len(conn))])
    un = np.array([[stress_in_element(res, e, XI[i], ETA[i]) for i in range(nen)] for e in range(len(conn))])
    if mode == "unaveraged":
        return un
    n = len(res["nodes"])
    av = np.zeros((n, 3)); cnt = np.zeros(n)
    for e, c in enumerate(conn):
        for i, nd in enumerate(c):
            av[nd] += un[e, i]; cnt[nd] += 1
    return av / cnt[:, None]


# ---------------------------------------------------------------------------
# Beam theory for comparison
# ---------------------------------------------------------------------------
def timoshenko_tip(L, H, E, nu, t, q, plane="stress", kappa=5 / 6):
    """Tip deflection magnitude: bending PL^3/(3EI) plus shear PL/(kappa G A)."""
    P = -q * H
    I, A, G = t * H ** 3 / 12, t * H, E / (2 * (1 + nu))
    Eb = E / (1 - nu ** 2) if plane == "strain" else E
    return P * L ** 3 / (3 * Eb * I), P * L / (kappa * G * A)


def plot_von_mises(res, filename="von_mises.png"):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
    except ImportError:
        print("matplotlib is not installed: skipping the plot")
        return None
    xs = np.linspace(0, res["L"], 161); ys = np.linspace(0, res["H"], 81)
    X, Y = np.meshgrid(xs, ys)
    Z = np.vectorize(lambda x, y: von_mises(stress_at(res, x, y)) / 1e3)(X, Y)
    fig, ax = plt.subplots(figsize=(8, 4.6))
    # the fixed corners are singular: cap the colour scale at the 99th percentile
    levels = MaxNLocator(nbins=20).tick_values(0, np.percentile(Z, 99))
    cf = ax.contourf(X, Y, Z, levels=levels, cmap="jet", extend="max")
    ax.set_aspect("equal"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    fig.colorbar(cf, ax=ax, label="von Mises (kN/m2)")
    ax.set_title(f"{res['nen']}-node, {res['Nx']} x {res['Ny']} mesh")
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", filename)
    return filename


# ---------------------------------------------------------------------------
# Course examples
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True, linewidth=140)
    base = dict(L=4.0, H=2.0, E=200e6, nu=0.33, t=0.01, q=-5000.0)

    r = solve_cantilever(Nx=2, Ny=2, **base)
    print("Text cantilever, 4-node 2 x 2 mesh, (3.44)-(3.49) (nodes 1-3 along the bottom)")
    U = r["U"].reshape(-1, 2)
    for i, (u, v) in enumerate(U):
        print(f"  node {i + 1}: u = {u:+.6f}  v = {v:+.6f} m")
    print(f"  tip deflection = {r['tip']:.4f} m  (text: -0.131)")
    R = r["reactions"]
    print(f"  reactions: Rx = {R['Rx']:.1f} N, Ry = {R['Ry']:.1f} N, M = {R['M']:.1f} N m  (10 kN up, 40 kN m)")
    s = stress_at(r, 3.5, 1.3) / 1e3
    s1, s2, th = principal(s)
    print(f"  stress at (3.5, 1.3) = {np.round(s, 1)} kN/m2  (315.2, -44.9, -310.9)")
    print(f"  principal {s1:.1f}, {s2:.1f} kN/m2 at {th:.1f} deg; von Mises {von_mises(s):.1f}  (494.4, -224.1; 636.8)")

    bend, shear = timoshenko_tip(**base)
    print(f"\nConvergence of the tip deflection; Timoshenko beam {bend:.3f} + {shear:.3f} = {bend + shear:.3f} m")
    for nen, meshes in ((4, [(2, 1), (2, 2), (4, 2), (8, 4), (16, 8), (32, 16)]), (8, [(2, 1), (4, 2), (8, 4), (16, 8)])):
        for Nx, Ny in meshes:
            rr = solve_cantilever(Nx=Nx, Ny=Ny, nen=nen, **base)
            print(f"  {nen}-node {Nx:2d} x {Ny:<2d} dofs {rr['U'].size:5d}  tip {rr['tip']:.4f} m")

    r8 = solve_cantilever(Nx=16, Ny=8, nen=8, **base)
    print(f"\n8-node 16 x 8: sxx(2.0, 1.3) = {stress_at(r8, 2.0, 1.3)[0] / 1e3:.1f} kN/m2 (beam theory 900);"
          f" sxx(3.5, 1.3) = {stress_at(r8, 3.5, 1.3)[0] / 1e3:.1f} (beam 225: end effect, St-Venant)")

    print("\nFixed corner: sxx at the centroid of the top-left element grows with every refinement (a singularity)")
    for Nx, Ny in ((8, 4), (16, 8), (32, 16)):
        rr = solve_cantilever(Nx=Nx, Ny=Ny, **base)
        print(f"  4-node {Nx} x {Ny}: {stress_at(rr, rr['a'] / 2, 2 - rr['b'] / 2)[0] / 1e3:.0f} kN/m2")

    plot_von_mises(r8, "von_mises_q8_16x8.png")
