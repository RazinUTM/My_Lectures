"""Q4 plane-stress FE solver with the book's closed-form [k] (3.42) — verifies Chapter 3 numbers."""
import numpy as np

def svals(E, nu, t, a, b):
    c = E * t / (1 - nu**2)
    s = {}
    s[1] = c * ((1 - nu) * a**2 + 2 * b**2) / (6 * a * b)
    s[2] = c * ((1 - nu) + 2 * nu) / 8
    s[3] = c * ((1 - nu) * a**2 - 4 * b**2) / (12 * a * b)
    s[4] = -c * ((1 - nu) - 2 * nu) / 8
    s[5] = -c * ((1 - nu) * a**2 + 2 * b**2) / (12 * a * b)
    s[6] = -c * ((1 - nu) + 2 * nu) / 8
    s[7] = -c * ((1 - nu) * a**2 - b**2) / (6 * a * b)
    s[8] = c * ((1 - nu) - 2 * nu) / 8
    s[9] = c * (2 * a**2 + (1 - nu) * b**2) / (6 * a * b)
    s[10] = -c * ((1 - nu) * b**2 - a**2) / (6 * a * b)
    s[11] = -c * (2 * a**2 + (1 - nu) * b**2) / (12 * a * b)
    s[12] = c * ((1 - nu) * b**2 - 4 * a**2) / (12 * a * b)
    return s

def klocal(E, nu, t, a, b):
    s = svals(E, nu, t, a, b)
    P = [[1, 2, 3, 4, 5, 6, 7, 8], [2, 9, 8, 10, 6, 11, 4, 12], [3, 8, 1, 6, 7, 4, 5, 2], [4, 10, 6, 9, 8, 12, 2, 11],
         [5, 6, 7, 8, 1, 2, 3, 4], [6, 11, 4, 12, 2, 9, 8, 10], [7, 4, 5, 2, 3, 8, 1, 6], [8, 12, 2, 11, 4, 10, 6, 9]]
    return np.array([[s[j] for j in row] for row in P])

def Bmat(a, b, x, y):
    dNdx = np.array([-(b - y), (b - y), y, -y]) / (a * b)
    dNdy = np.array([-(a - x), -x, x, (a - x)]) / (a * b)
    B = np.zeros((3, 8))
    for i in range(4):
        B[0, 2 * i] = dNdx[i]; B[1, 2 * i + 1] = dNdy[i]; B[2, 2 * i] = dNdy[i]; B[2, 2 * i + 1] = dNdx[i]
    return B

def Emat(E, nu):
    return E / (1 - nu**2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])

def klocal_gauss(E, nu, t, a, b, n=2):
    """numerical check of the closed form"""
    g, w = np.polynomial.legendre.leggauss(n)
    k = np.zeros((8, 8)); Em = Emat(E, nu)
    for gi, wi in zip(g, w):
        for gj, wj in zip(g, w):
            x = (gi + 1) / 2 * a; y = (gj + 1) / 2 * b
            B = Bmat(a, b, x, y)
            k += t * (a / 2) * (b / 2) * wi * wj * B.T @ Em @ B
    return k

def mesh(L, H, Nx, Ny):
    a, b = L / Nx, H / Ny
    nodes = np.array([(j * a, i * b) for i in range(Ny + 1) for j in range(Nx + 1)])
    conn = [[i * (Nx + 1) + j, i * (Nx + 1) + j + 1, (i + 1) * (Nx + 1) + j + 1, (i + 1) * (Nx + 1) + j] for i in range(Ny) for j in range(Nx)]
    return a, b, nodes, np.array(conn)

def solve_cantilever(L, H, Nx, Ny, E, nu, t, qy):
    a, b, nodes, conn = mesh(L, H, Nx, Ny)
    n = len(nodes); K = np.zeros((2 * n, 2 * n)); F = np.zeros(2 * n)
    k = klocal(E, nu, t, a, b)
    for e in conn:
        dofs = np.array([[2 * nd, 2 * nd + 1] for nd in e]).ravel()
        K[np.ix_(dofs, dofs)] += k
    # traction qy (N/m, downward negative) on the right edge x = L: each edge element contributes qy*b/2 to its two nodes (y-dof)
    right = np.where(np.isclose(nodes[:, 0], L))[0]
    for nd in right:
        nedge = 2 if (0 < nodes[nd, 1] < H) else 1
        F[2 * nd + 1] += qy * b / 2 * nedge
    fixed = np.where(np.isclose(nodes[:, 0], 0))[0]
    kd = np.array([[2 * nd, 2 * nd + 1] for nd in fixed]).ravel()
    free = np.setdiff1d(np.arange(2 * n), kd)
    U = np.zeros(2 * n); U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    return nodes, conn, K, F, U, a, b

if __name__ == "__main__":
    np.set_printoptions(precision=3, suppress=True, linewidth=160)
    E, nu, t = 200e6, 0.33, 0.01
    k = klocal(E, nu, t, 2.0, 1.0); kg = klocal_gauss(E, nu, t, 2.0, 1.0)
    print("closed-form vs Gauss max diff:", np.abs(k - kg).max() / np.abs(k).max())
    print("k (x1e6):\n", k / 1e6)
    s = svals(E, nu, t, 2.0, 1.0); print({i: round(v / 1e6, 4) for i, v in s.items()})
    nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, 2, 2, E, nu, t, -5000)
    print("F:", F); print("U (2x2):", U)
    for N in [(2, 2), (4, 2), (8, 4), (16, 8), (16, 16), (32, 16), (64, 32), (80, 40)]:
        nodes, conn, K, F, U, a, b = solve_cantilever(4, 2, N[0], N[1], E, nu, t, -5000)
        i6 = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 0)); i18 = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2))
        print(f"{N}: U5={U[2*i6]:.4f} U6={U[2*i6+1]:.4f} U17={U[2*i18]:.4f} U18={U[2*i18+1]:.4f}")
    # Timoshenko check
    P = 5000 * 2; L = 4; I = t * 2**3 / 12; G = E / (2 * (1 + nu)); A = t * 2; kappa = 5 / 6
    db = P * L**3 / (3 * E * I); ds = P * L / (kappa * G * A)
    print(f"beam: bending {db:.4f} shear {ds:.4f} total {db+ds:.4f}")
    # stresses at (3.5,1.3) in element 4 of the 2x2 mesh using the book's rounded U
    Ub = np.array([0, 0, -0.031, -0.046, -0.042, -0.131, 0, 0, 0.000, -0.043, 0.000, -0.130, 0, 0, 0.031, -0.046, 0.042, -0.131])
    d4 = np.array([8, 9, 10, 11, 16, 17, 14, 15])  # dofs of nodes 5,6,9,8 (0-based)
    B = Bmat(2, 1, 1.5, 0.3); eps = B @ Ub[d4]; sig = Emat(E, nu) @ eps
    print("eps at (3.5,1.3):", eps, "sigma kN/m2:", sig / 1e3)
    print("B at (1.5,0.3):\n", B)
