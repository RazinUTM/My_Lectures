"""Minimal 4-node rectangular heat-conduction FE solver (book Chapter 2 formulas) — used to verify slide numbers."""
import numpy as np

def klocal(a, b, kx, ky):
    s1 = b * kx / (3 * a) + a * ky / (3 * b)
    s2 = -b * kx / (3 * a) + a * ky / (6 * b)
    s3 = -b * kx / (6 * a) - a * ky / (6 * b)
    s4 = b * kx / (6 * a) - a * ky / (3 * b)
    return np.array([[s1, s2, s3, s4], [s2, s1, s4, s3], [s3, s4, s1, s2], [s4, s3, s2, s1]])

def mesh(L, H, Nx, Ny):
    a, b = L / Nx, H / Ny
    nodes = np.array([(j * a, i * b) for i in range(Ny + 1) for j in range(Nx + 1)])
    conn = []
    for i in range(Ny):
        for j in range(Nx):
            n1 = i * (Nx + 1) + j
            conn.append([n1, n1 + 1, n1 + Nx + 2, n1 + Nx + 1])
    return a, b, nodes, np.array(conn)

def solve(L, H, Nx, Ny, kx, ky, Q, dirichlet):
    """dirichlet: function (x,y)->value or None"""
    a, b, nodes, conn = mesh(L, H, Nx, Ny)
    n = len(nodes); K = np.zeros((n, n)); F = np.zeros(n)
    k = klocal(a, b, kx, ky); fq = a * b * Q / 4 * np.ones(4)
    for e in conn:
        K[np.ix_(e, e)] += k; F[e] += fq
    T = np.zeros(n); known = []
    for i, (x, y) in enumerate(nodes):
        v = dirichlet(x, y)
        if v is not None:
            known.append(i); T[i] = v
    known = np.array(known); free = np.setdiff1d(np.arange(n), known)
    F2 = F - K[:, known] @ T[known]
    T[free] = np.linalg.solve(K[np.ix_(free, free)], F2[free])
    return nodes, conn, K, F, T, a, b

if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True, linewidth=150)
    # book worked example: L=H=1, k=300, Q=600, T=0 on top (y=1) and left (x=0)
    bc = lambda x, y: 0.0 if (abs(x) < 1e-9 or abs(y - 1) < 1e-9) else None
    nodes, conn, K, F, T, a, b = solve(1, 1, 2, 2, 300, 300, 600, bc)
    print("k local:\n", klocal(a, b, 300, 300))
    print("K global (9x9):\n", K)
    print("F:", F)
    print("T:", T)
    for N in [8, 16, 64]:
        nodes, conn, K, F, T, a, b = solve(1, 1, N, N, 300, 300, 600, bc)
        # bottom edge: x = L/2 and x = L at y = 0
        i_mid = np.argmin(np.hypot(nodes[:, 0] - 0.5, nodes[:, 1])); i_end = np.argmin(np.hypot(nodes[:, 0] - 1.0, nodes[:, 1]))
        print(f"{N}x{N}: T(L/2,0)={T[i_mid]:.4f} T(L,0)={T[i_end]:.4f}  max={T.max():.4f}")
    # Assignment: 3 identical elements a=2,b=3, T=100 at left, Q=20 on element 1
    a, b = 2.0, 3.0
    print("assignment s1..s4 / k:", [round(v, 4) for v in [b / (3 * a) + a / (3 * b), -b / (3 * a) + a / (6 * b), -b / (6 * a) - a / (6 * b), b / (6 * a) - a / (3 * b)]])
    print("assignment r1:", 20 * a * b / 4)
    x, y = 1.4, 2.2
    N = [(a - x) * (b - y) / (a * b), x * (b - y) / (a * b), x * y / (a * b), y * (a - x) / (a * b)]
    print("assignment N:", [round(v, 5) for v in N], "T=", sum(n * t for n, t in zip(N, [100, 150, 150, 100])))
    # Activity 6 (week 10): element 1 of 2x2 mesh, point (0.3,0.2), T = {0, 0.482, 0.386, 0}
    a = b = 0.5; x, y = 0.3, 0.2
    N = [(a - x) * (b - y) / (a * b), x * (b - y) / (a * b), x * y / (a * b), y * (a - x) / (a * b)]
    print("act6 N:", N, "sum", sum(N), "T=", sum(n * t for n, t in zip(N, [0, 0.482, 0.386, 0])))
    # Activity 5 check: row 1 of reduced system
    print("row1:", 400 * 0.482 - 50 * 0.621 - 100 * 0.386 - 100 * 0.482)
    # flux at centroid of element 2 (nodes 2,3,6,5): T = {0.482,0.621,0.482,0.386}
    Te = np.array([0.482, 0.621, 0.482, 0.386]); x = y = 0.25
    dNdx = np.array([-(b - y), (b - y), y, -y]) / (a * b); dNdy = np.array([-(a - x), -x, x, (a - x)]) / (a * b)
    print("elem2 centroid dT/dx", dNdx @ Te, "dT/dy", dNdy @ Te, "q =", -300 * dNdx @ Te, -300 * dNdy @ Te)
