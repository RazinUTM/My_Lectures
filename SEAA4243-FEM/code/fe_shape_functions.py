"""
SEAA 4243 Finite Element Method - shape functions of the rectangular elements
==============================================================================

Companion code for the Shape Function Explorer (2D Heat Transfer, Part 1).

What it does
    Evaluates the shape functions N_i of the 4-node (Q4) and 8-node (Q8)
    rectangular elements at a point, checks them, interpolates a nodal field,
    and computes the gradient and the heat flux at that point.

Notation (text: Mohd Yassin et al., MSNM 2020, Sec. 2.2)
    Element a x b. Local nodes 1-4 anticlockwise from the bottom-left corner;
    the Q8 adds mid-side nodes 5-8 on the bottom, right, top and left sides.
    Local coordinates x in [0, a], y in [0, b].
        Q4:  N1 = (a-x)(b-y)/ab,  N2 = x(b-y)/ab,  N3 = xy/ab,  N4 = y(a-x)/ab   (2.21)
        T(x, y) = sum N_i T_i = {N}{T}^T                                          (2.22)
        gradient = {d}^T{N}{T}^T,  flux q = -[E] gradient                         (2.33)

Run
    python fe_shape_functions.py
        prints Activities 4 and 5 (a = 2, b = 1, P = (1.5, 0.3)) and the checks,
        and, if matplotlib is installed, saves maps of N1...N4 and N1...N8.

Use in your own work
    from fe_shape_functions import shape_q4, dshape_q4, interpolate, flux
    N = shape_q4(a, b, x, y)             # x, y LOCAL to the element
    T = interpolate(N, [T1, T2, T3, T4])

    For a point given in GLOBAL coordinates, find the element first and subtract
    the coordinates of its local node 1: x_loc = x - x1, y_loc = y - y1.

Requires Python 3.8+ and numpy; matplotlib only for the plots.
Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
Code: MIT licence.
"""
import numpy as np


# ---------------------------------------------------------------------------
# Q4: bilinear element, text (2.21) and (2.33)
# ---------------------------------------------------------------------------
def shape_q4(a, b, x, y):
    """N1..N4 at the local point (x, y) of an a x b element. Returns an array of 4."""
    return np.array([(a - x) * (b - y), x * (b - y), x * y, y * (a - x)], dtype=float) / (a * b)


def dshape_q4(a, b, x, y):
    """{d}^T{N}: 2 x 4 array, row 0 = dN_i/dx, row 1 = dN_i/dy, at local (x, y)."""
    return np.array([[-(b - y), (b - y), y, -y],
                     [-(a - x), -x, x, (a - x)]], dtype=float) / (a * b)


# ---------------------------------------------------------------------------
# Q8: serendipity element, text Sec. 2.2.1, evaluated through xi = 2x/a - 1, eta = 2y/b - 1
# ---------------------------------------------------------------------------
_CX = [-1, 1, 1, -1]
_CY = [-1, -1, 1, 1]


def shape_q8(a, b, x, y):
    """N1..N8 at the local point (x, y). Corners 1-4, mid-sides 5 (bottom), 6 (right), 7 (top), 8 (left)."""
    xi, eta = 2 * x / a - 1, 2 * y / b - 1
    N = np.zeros(8)
    for i in range(4):
        N[i] = 0.25 * (1 + _CX[i] * xi) * (1 + _CY[i] * eta) * (_CX[i] * xi + _CY[i] * eta - 1)
    N[4] = 0.5 * (1 - xi ** 2) * (1 - eta)
    N[5] = 0.5 * (1 + xi) * (1 - eta ** 2)
    N[6] = 0.5 * (1 - xi ** 2) * (1 + eta)
    N[7] = 0.5 * (1 - xi) * (1 - eta ** 2)
    return N


def dshape_q8(a, b, x, y):
    """2 x 8 array of dN_i/dx and dN_i/dy at local (x, y) (chain rule: d/dx = (2/a) d/dxi)."""
    xi, eta = 2 * x / a - 1, 2 * y / b - 1
    dxi, deta = np.zeros(8), np.zeros(8)
    for i in range(4):
        dxi[i] = 0.25 * _CX[i] * (1 + _CY[i] * eta) * (2 * _CX[i] * xi + _CY[i] * eta)
        deta[i] = 0.25 * _CY[i] * (1 + _CX[i] * xi) * (_CX[i] * xi + 2 * _CY[i] * eta)
    dxi[4], deta[4] = -xi * (1 - eta), -0.5 * (1 - xi ** 2)
    dxi[5], deta[5] = 0.5 * (1 - eta ** 2), -eta * (1 + xi)
    dxi[6], deta[6] = -xi * (1 + eta), 0.5 * (1 - xi ** 2)
    dxi[7], deta[7] = -0.5 * (1 - eta ** 2), -eta * (1 - xi)
    return np.vstack([dxi * 2 / a, deta * 2 / b])


def node_coords(a, b, nen=4):
    """Local coordinates of the element's nodes, in node order."""
    xy = [(0, 0), (a, 0), (a, b), (0, b), (a / 2, 0), (a, b / 2), (a / 2, b), (0, b / 2)]
    return np.array(xy[:nen], dtype=float)


# ---------------------------------------------------------------------------
# Field at a point
# ---------------------------------------------------------------------------
def interpolate(N, nodal_values):
    """T(x, y) = sum N_i T_i."""
    return float(np.dot(N, nodal_values))


def gradient(dN, nodal_values):
    """(dT/dx, dT/dy) = {d}^T{N}{T}^T."""
    return dN @ np.asarray(nodal_values, dtype=float)


def flux(dN, nodal_values, kx, ky=None):
    """Fourier's law: (qx, qy) = -(kx dT/dx, ky dT/dy). Heat flows from hot to cold."""
    ky = kx if ky is None else ky
    g = gradient(dN, nodal_values)
    return np.array([-kx * g[0], -ky * g[1]])


def check(a, b, nen=4, tol=1e-12):
    """The two properties every set of shape functions must pass.
    Kronecker delta: N_i = 1 at node i and 0 at the others. Partition of unity: sum N_i = 1."""
    f = shape_q4 if nen == 4 else shape_q8
    M = np.array([f(a, b, x, y) for x, y in node_coords(a, b, nen)])
    kron = np.allclose(M, np.eye(nen), atol=tol)
    rng = np.random.default_rng(0)
    pts = rng.random((50, 2)) * [a, b]
    pou = np.allclose([f(a, b, x, y).sum() for x, y in pts], 1.0, atol=tol)
    return kron, pou


# ---------------------------------------------------------------------------
# Plots (optional): one colour map per shape function, shared limits
# ---------------------------------------------------------------------------
def plot_shape_functions(a, b, nen=4, filename=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed: skipping the plot")
        return None
    f = shape_q4 if nen == 4 else shape_q8
    xs, ys = np.linspace(0, a, 81), np.linspace(0, b, 41)
    X, Y = np.meshgrid(xs, ys)
    lo, hi = (0.0, 1.0) if nen == 4 else (-0.25, 1.0)
    cols = 4
    rows = nen // cols
    fig, axs = plt.subplots(rows, cols, figsize=(3.2 * cols, 2.0 * rows * max(b / a, 0.5) + 0.8), squeeze=False)
    xy = node_coords(a, b, nen)
    for i in range(nen):
        ax = axs[i // cols][i % cols]
        Z = np.vectorize(lambda x, y: f(a, b, x, y)[i])(X, Y)
        cf = ax.contourf(X, Y, Z, levels=np.linspace(lo, hi, 21), cmap="jet", vmin=lo, vmax=hi)
        ax.contour(X, Y, Z, levels=[0.0], colors="k", linewidths=0.8)
        ax.plot(xy[:, 0], xy[:, 1], "ko", ms=4)
        ax.plot(*xy[i], "wo", ms=7, mec="k")
        ax.set_title(f"N{i + 1}")
        ax.set_aspect("equal")
        ax.set_xticks([0, a]); ax.set_yticks([0, b])
    fig.colorbar(cf, ax=axs, shrink=0.8, label="N_i (black line: N_i = 0)")
    filename = filename or f"shape_functions_q{nen}.png"
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", filename)
    return filename


# ---------------------------------------------------------------------------
# Course example: Activities 4 and 5 (a = 2 m, b = 1 m, P = (1.5, 0.3) m)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    a, b = 2.0, 1.0
    x, y = 1.5, 0.3
    T = [100.0, 140.0, 160.0, 120.0]
    k = 2.0

    N = shape_q4(a, b, x, y)
    print("Q4 element a = 2 m, b = 1 m, point (1.5, 0.3) m")
    print("  N1..N4      =", N, "  (expected 0.175 0.525 0.225 0.075)")
    print("  sum N_i     =", round(N.sum(), 12))
    print("  T           =", round(interpolate(N, T), 4), "K  (expected 136.0)")
    dN = dshape_q4(a, b, x, y)
    print("  dN/dx       =", dN[0], "  (expected -0.35 0.35 0.15 -0.15)")
    print("  gradient    =", gradient(dN, T), "K/m  (expected 20 20)")
    print("  flux, k = 2 =", flux(dN, T, k), "W/m2 (expected -40 -40)")
    print("  checks (Kronecker, partition of unity):", check(a, b, 4))

    N8 = shape_q8(a, b, a / 2, b / 2)
    print("\nQ8 element at the centre: N1..N8 =", N8)
    print("  corner functions are -0.25 there; sum =", round(N8.sum(), 12))
    print("  checks (Kronecker, partition of unity):", check(a, b, 8))

    plot_shape_functions(a, b, 4)
    plot_shape_functions(a, b, 8)
