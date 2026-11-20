# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""B-splines, NURBS and reproducing-kernel (RK) shape functions in one dimension, in the primer's notation.

What it gives you
    bspline_table(t, p, xi)   Cox-de Boor triangle: every N_{I,k}(xi) for k = 0..p (1-based I)
    bspline(t, p, xi)         the degree-p values N_{I,p}(xi), I = 1..n
    greville(t, p)            Greville abscissae xi_bar_I
    blossom(t, p)             blossom vectors {Q_I} = {1, q_I1, ..., q_Ip}, Eq. (5.1) of Part 1
    nurbs_curve(t, p, P, lam, xi)   point of a NURBS curve, Eqs. (3.1)-(3.2)
    cubic_kernel(r)           the cubic B-spline window w(r), Eq. (4.6)
    rk_standard(x, nodes, a, p)     RK shape functions with node monomials {H(x_I)}, Eqs. (4.4)-(4.5)
    rk_blossom(xi, t, p, kernel)    RK shape functions with blossom vectors, Eq. (5.3)

How to run it
    python3 nmf_bspline_rk.py      prints the numbers of Examples 1-3 of Part 1 and the check RK = B-spline.
    Requires Python 3.8+ and numpy.

Why it is written like this
    Indices follow the notes (I = 1..n, knots t_1..t_{n+p+1}); Python lists are 0-based, so t[i-1] is t_i.
    Every function is short enough to read next to the equation it implements.
"""
from __future__ import annotations

from math import comb, sqrt
from itertools import combinations

import numpy as np


def _span_ok(t, i, xi):
    """True when t_i <= xi < t_{i+1}; the last non-empty span also takes xi = t_end."""
    lo, hi = t[i - 1], t[i]
    if lo <= xi < hi:
        return True
    return xi == t[-1] and hi == t[-1] and lo < hi


def bspline_table(t, p, xi):
    """All N_{I,k}(xi), k = 0..p, by the Cox-de Boor recursion (2.1)-(2.2); 0/0 is taken as 0.

    Returns a list `tab` with tab[k] = [N_{1,k}, ..., N_{m-k-1,k}] for m = len(t)."""
    m = len(t)
    tab = [[1.0 if _span_ok(t, i, xi) else 0.0 for i in range(1, m)]]
    for k in range(1, p + 1):
        prev, row = tab[-1], []
        for i in range(1, m - k):
            a = b = 0.0
            d1 = t[i + k - 1] - t[i - 1]          # t_{I+k} - t_I
            d2 = t[i + k] - t[i]                  # t_{I+k+1} - t_{I+1}
            if d1 > 0:
                a = (xi - t[i - 1]) / d1 * prev[i - 1]
            if d2 > 0:
                b = (t[i + k] - xi) / d2 * prev[i]
            row.append(a + b)
        tab.append(row)
    return tab


def bspline(t, p, xi):
    """The n = len(t) - p - 1 basis functions N_{I,p}(xi)."""
    return np.array(bspline_table(t, p, xi)[p])


def greville(t, p):
    """Greville abscissae xi_bar_I = (t_{I+1} + ... + t_{I+p}) / p, Eq. (2.5)."""
    n = len(t) - p - 1
    return np.array([sum(t[i:i + p]) / p for i in range(1, n + 1)])


def elementary(vals, l):
    """Elementary symmetric polynomial e_l of the numbers in vals (e_0 = 1)."""
    return float(sum(np.prod(c) for c in combinations(vals, l))) if l else 1.0


def blossom(t, p):
    """Blossom vectors {Q_I} = {1, q_I1, ..., q_Ip}, q_Il = e_l(t_{I+1}, ..., t_{I+p}) / C(p, l), Eq. (5.1)."""
    n = len(t) - p - 1
    return np.array([[elementary(t[i:i + p], l) / comb(p, l) for l in range(p + 1)] for i in range(1, n + 1)])


def nurbs_curve(t, p, P, lam, xi):
    """Point of the NURBS curve sum_I R_I(xi) {P_I}, with R_I = lam_I N_I / sum_J lam_J N_J, Eqs. (3.1)-(3.2)."""
    N = bspline(t, p, xi)
    R = np.asarray(lam) * N
    R = R / R.sum()
    return R @ np.asarray(P, dtype=float), R


def cubic_kernel(r):
    """Cubic B-spline window w(r) of Eq. (4.6), r = |x - x_I| / a."""
    r = abs(r)
    if r <= 0.5:
        return 2 / 3 - 4 * r ** 2 + 4 * r ** 3
    if r <= 1.0:
        return 4 / 3 - 4 * r + 4 * r ** 2 - 4 / 3 * r ** 3
    return 0.0


def rk_standard(x, nodes, a, p, kernel=cubic_kernel):
    """RK shape functions Psi_I(x) = {H(x_I)}^T [M]^-1 {H(x)} W_I(x), Eqs. (4.4)-(4.5).

    Returns Psi (one value per node) and the pieces of the computation for printing."""
    nodes = np.asarray(nodes, dtype=float)
    H = lambda s: np.array([s ** l for l in range(p + 1)])
    W = np.array([kernel((x - xi) / a) for xi in nodes])
    M = sum(W[j] * np.outer(H(nodes[j]), H(nodes[j])) for j in range(len(nodes)))
    b = np.linalg.solve(M, H(x))
    Psi = np.array([H(nodes[i]) @ b * W[i] for i in range(len(nodes))])
    return Psi, {"W": W, "M": M, "b": b}


def rk_blossom(xi, t, p, kernel=lambda r: 1.0):
    """RK shape functions with blossom vectors, Eq. (5.3): node I has the support of N_{I,p}.

    `kernel(r)` may be any function positive on 0 <= r < 1 (r = distance to the support centre / half-width):
    the result does not depend on it, which is the point of Section 5."""
    Q = blossom(t, p)
    n = len(Q)
    H = np.array([xi ** l for l in range(p + 1)])
    W = np.zeros(n)
    for i in range(1, n + 1):
        lo, hi = t[i - 1], t[i + p]                       # support [t_I, t_{I+p+1}]
        inside = (lo <= xi < hi) or (xi == t[-1] and hi == t[-1] and lo < hi)
        if inside and hi > lo:
            c, h = (lo + hi) / 2, (hi - lo) / 2
            W[i - 1] = kernel(abs(xi - c) / h)
    M = sum(W[j] * np.outer(Q[j], Q[j]) for j in range(n))
    b = np.linalg.solve(M, H)
    return np.array([Q[i] @ b * W[i] for i in range(n)])


if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)
    t = [0, 0, 0, 0.5, 1, 1, 1]
    print("Example 1  quadratic B-splines on", t, "at xi = 0.75")
    for k, row in enumerate(bspline_table(t, 2, 0.75)):
        print(f"  degree {k}:", np.round(row, 6))
    N = bspline(t, 2, 0.75)
    print("  partition of unity:", N.sum(), " linear reproduction:", N @ greville(t, 2))
    print("Example 2  linear RK at x = 0.4, nodes 0, 0.5, 1, support a = 0.75")
    Psi, d = rk_standard(0.4, [0, 0.5, 1], 0.75, 1)
    print("  W =", d["W"], "\n  M =", d["M"].tolist(), "\n  Psi =", Psi, " sum =", Psi.sum(), " sum Psi x_I =", Psi @ [0, 0.5, 1])
    print("Example 3  blossom vectors and RK = B-spline at xi = 0.75")
    print("  Q =", blossom(t, 2).tolist())
    for name, ker in [("constant", lambda r: 1.0), ("cubic", cubic_kernel), ("cosine", lambda r: 1 + np.cos(np.pi * r))]:
        print(f"  {name:8s} kernel: Psi =", np.round(rk_blossom(0.75, t, 2, ker), 12) + 0.0)  # + 0.0 prints -0 as 0
    print("  B-splines:         N   =", N)
    P, R = nurbs_curve([0, 0, 0, 1, 1, 1], 2, [[1, 0], [1, 1], [0, 1]], [1, 1 / sqrt(2), 1], 0.5)
    print("Quarter circle at xi = 0.5:", P, " radius", float(np.hypot(*P)))
