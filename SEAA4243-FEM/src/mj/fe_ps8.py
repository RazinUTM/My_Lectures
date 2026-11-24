"""Q8 (serendipity) plane-stress / plane-strain solver on a structured mesh of the cantilever.
Used to produce the 'expected' numbers for the ANSYS demo (PLANE183 ~ Q8, PLANE182 ~ Q4)."""
import numpy as np
from fe_ps import Emat, solve_cantilever, mesh as mesh4, klocal as k4, Bmat as B4

def Emat_strain(E, nu):
    c = E / ((1 + nu) * (1 - 2 * nu))
    return c * np.array([[1 - nu, nu, 0], [nu, 1 - nu, 0], [0, 0, (1 - 2 * nu) / 2]])

def shape8(xi, eta):
    """serendipity Q8 on [-1,1]^2; node order: corners (-1,-1),(1,-1),(1,1),(-1,1), mid-sides bottom,right,top,left"""
    N = np.zeros(8); dN = np.zeros((8, 2))
    cx = [-1, 1, 1, -1]; cy = [-1, -1, 1, 1]
    for i in range(4):
        N[i] = 0.25 * (1 + cx[i] * xi) * (1 + cy[i] * eta) * (cx[i] * xi + cy[i] * eta - 1)
        dN[i, 0] = 0.25 * cx[i] * (1 + cy[i] * eta) * (2 * cx[i] * xi + cy[i] * eta)
        dN[i, 1] = 0.25 * cy[i] * (1 + cx[i] * xi) * (cx[i] * xi + 2 * cy[i] * eta)
    N[4] = 0.5 * (1 - xi**2) * (1 - eta); dN[4] = [-xi * (1 - eta), -0.5 * (1 - xi**2)]
    N[5] = 0.5 * (1 + xi) * (1 - eta**2); dN[5] = [0.5 * (1 - eta**2), -eta * (1 + xi)]
    N[6] = 0.5 * (1 - xi**2) * (1 + eta); dN[6] = [-xi * (1 + eta), 0.5 * (1 - xi**2)]
    N[7] = 0.5 * (1 - xi) * (1 - eta**2); dN[7] = [-0.5 * (1 - eta**2), -eta * (1 - xi)]
    return N, dN

def k8(Em, t, a, b, ng=3):
    g, w = np.polynomial.legendre.leggauss(ng)
    k = np.zeros((16, 16))
    for gi, wi in zip(g, w):
        for gj, wj in zip(g, w):
            N, dN = shape8(gi, gj)
            dNdx = dN[:, 0] * 2 / a; dNdy = dN[:, 1] * 2 / b
            B = np.zeros((3, 16))
            for i in range(8):
                B[0, 2 * i] = dNdx[i]; B[1, 2 * i + 1] = dNdy[i]; B[2, 2 * i] = dNdy[i]; B[2, 2 * i + 1] = dNdx[i]
            k += t * (a / 2) * (b / 2) * wi * wj * B.T @ Em @ B
    return k

def mesh8(L, H, Nx, Ny):
    a, b = L / Nx, H / Ny
    nid = {}; nodes = []
    def node(x, y):
        key = (round(x, 9), round(y, 9))
        if key not in nid:
            nid[key] = len(nodes); nodes.append((x, y))
        return nid[key]
    conn = []
    for i in range(Ny):
        for j in range(Nx):
            x0, y0 = j * a, i * b
            c = [node(x0, y0), node(x0 + a, y0), node(x0 + a, y0 + b), node(x0, y0 + b),
                 node(x0 + a / 2, y0), node(x0 + a, y0 + b / 2), node(x0 + a / 2, y0 + b), node(x0, y0 + b / 2)]
            conn.append(c)
    return a, b, np.array(nodes), np.array(conn)

def solve8(L, H, Nx, Ny, Em, t, qy, point_load=False):
    a, b, nodes, conn = mesh8(L, H, Nx, Ny)
    n = len(nodes); K = np.zeros((2 * n, 2 * n)); F = np.zeros(2 * n)
    k = k8(Em, t, a, b)
    for e in conn:
        dofs = np.array([[2 * nd, 2 * nd + 1] for nd in e]).ravel()
        K[np.ix_(dofs, dofs)] += k
    if point_load:
        itop = np.argmin(np.hypot(nodes[:, 0] - L, nodes[:, 1] - H)); F[2 * itop + 1] = qy * H
    else:
        # consistent loads on the right edge: 1/6, 2/3, 1/6 per edge of length b
        for e in conn:
            if np.isclose(nodes[e[1], 0], L):
                F[2 * e[1] + 1] += qy * b / 6; F[2 * e[5] + 1] += 2 * qy * b / 3; F[2 * e[2] + 1] += qy * b / 6
    fixed = np.where(np.isclose(nodes[:, 0], 0))[0]
    kd = np.array([[2 * nd, 2 * nd + 1] for nd in fixed]).ravel()
    free = np.setdiff1d(np.arange(2 * n), kd)
    U = np.zeros(2 * n); U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    return nodes, conn, K, F, U

if __name__ == "__main__":
    E, nu, t = 200e6, 0.33, 0.01
    Em = Emat(E, nu)
    print("Q8 plane stress, edge traction 5 kN/m:")
    for N in [(2, 1), (2, 2), (4, 2), (4, 4), (8, 4), (16, 8), (32, 16)]:
        nodes, conn, K, F, U = solve8(4, 2, N[0], N[1], Em, t, -5000)
        itop = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); ibot = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 0))
        print(f"  {N}: nodes={len(nodes)} dofs={2*len(nodes)}  v_top={U[2*itop+1]:.4f}  v_bot={U[2*ibot+1]:.4f}")
    print("Q4 plane strain (wrong idealisation) on 32x16:")
    import fe_ps
    Es = Emat_strain(E, nu)
    # reuse Q4 solver by monkeypatching Emat via klocal_gauss
    a, b, nodes, conn = mesh4(4, 2, 32, 16)
    n = len(nodes); K = np.zeros((2 * n, 2 * n)); F = np.zeros(2 * n)
    g, w = np.polynomial.legendre.leggauss(2); k = np.zeros((8, 8))
    for gi, wi in zip(g, w):
        for gj, wj in zip(g, w):
            B = B4(a, b, (gi + 1) / 2 * a, (gj + 1) / 2 * b); k += t * (a / 2) * (b / 2) * wi * wj * B.T @ Es @ B
    for e in conn:
        dofs = np.array([[2 * nd, 2 * nd + 1] for nd in e]).ravel(); K[np.ix_(dofs, dofs)] += k
    right = np.where(np.isclose(nodes[:, 0], 4))[0]
    for nd in right:
        F[2 * nd + 1] += -5000 * b / 2 * (2 if (0 < nodes[nd, 1] < 2) else 1)
    fixed = np.where(np.isclose(nodes[:, 0], 0))[0]; kd = np.array([[2 * nd, 2 * nd + 1] for nd in fixed]).ravel()
    free = np.setdiff1d(np.arange(2 * n), kd); U = np.zeros(2 * n); U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    itop = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); print(f"  v_top (plane strain) = {U[2*itop+1]:.4f}  ratio to plane stress 0.1906 = {U[2*itop+1]/-0.1906:.3f}  (1-nu^2 = {1-nu**2:.3f})")
    print("Q8 32x16 with a single point load 10 kN at the top-right vertex:")
    nodes, conn, K, F, U = solve8(4, 2, 32, 16, Em, t, -5000, point_load=True)
    itop = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 2)); ibot = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 0)); imid = np.argmin(np.hypot(nodes[:, 0] - 4, nodes[:, 1] - 1))
    print(f"  v_top={U[2*itop+1]:.4f} v_mid={U[2*imid+1]:.4f} v_bot={U[2*ibot+1]:.4f}")
    # stress at centroid of the element under the load vs edge-traction case
    def cstress(nodes, conn, U, Em, a, b, xc, yc):
        for e in conn:
            x0, y0 = nodes[e[0]]
            if np.isclose(x0 + a / 2, xc) and np.isclose(y0 + b / 2, yc):
                N, dN = shape8(0, 0); dNdx = dN[:, 0] * 2 / a; dNdy = dN[:, 1] * 2 / b
                B = np.zeros((3, 16))
                for i in range(8):
                    B[0, 2 * i] = dNdx[i]; B[1, 2 * i + 1] = dNdy[i]; B[2, 2 * i] = dNdy[i]; B[2, 2 * i + 1] = dNdx[i]
                dofs = np.array([[2 * nd, 2 * nd + 1] for nd in e]).ravel()
                return Em @ (B @ U[dofs])
    a, b = 4 / 32, 2 / 16
    s_pt = cstress(nodes, conn, U, Em, a, b, 4 - a / 2, 2 - b / 2)
    nodes2, conn2, K2, F2, U2 = solve8(4, 2, 32, 16, Em, t, -5000)
    s_ed = cstress(nodes2, conn2, U2, Em, a, b, 4 - a / 2, 2 - b / 2)
    vm = lambda s: np.sqrt(s[0]**2 - s[0] * s[1] + s[1]**2 + 3 * s[2]**2)
    print(f"  element under the load: point load sigma={np.round(s_pt/1e3,0)} vM={vm(s_pt)/1e3:.0f} kN/m2 ; edge traction sigma={np.round(s_ed/1e3,0)} vM={vm(s_ed)/1e3:.0f}")
    # mid-span comparison (should be nearly equal, St-Venant)
    s_pt2 = cstress(nodes, conn, U, Em, a, b, 2 - a / 2, 2 - b / 2); s_ed2 = cstress(nodes2, conn2, U2, Em, a, b, 2 - a / 2, 2 - b / 2)
    print(f"  mid-span top element: point load sxx={s_pt2[0]/1e3:.0f} ; edge traction sxx={s_ed2[0]/1e3:.0f}")
