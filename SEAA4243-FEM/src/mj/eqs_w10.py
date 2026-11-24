"""LaTeX sources for Week 10 equations (book notation)."""
import numpy as np
MAR = "8C1D2F"; TEA = "1F6FA3"; GRN = "2E7D5B"; GRY = "9AA3B2"

def kmat_colored(parts, labels=True):
    """parts: list of (conn(list of global 1-based nodes), color) ; returns bmatrix LaTeX of the 9x9 K with coloured entries"""
    s = np.array([[200, -50, -100, -50], [-50, 200, -50, -100], [-100, -50, 200, -50], [-50, -100, -50, 200]])
    K = np.zeros((9, 9)); owner = [[set() for _ in range(9)] for _ in range(9)]
    for conn, col in parts:
        for i, gi in enumerate(conn):
            for j, gj in enumerate(conn):
                K[gi - 1, gj - 1] += s[i, j]; owner[gi - 1][gj - 1].add(col)
    rows = []
    for i in range(9):
        cells = []
        for j in range(9):
            v = int(K[i, j]); o = owner[i][j]
            if not o:
                cells.append(rf"\color{{#{GRY}}}{{0}}")
            elif len(o) == 1:
                cells.append(rf"\color{{#{list(o)[0]}}}{{{v}}}")
            else:
                cells.append(rf"\color{{#{GRN}}}{{{v}}}")
        rows.append("&".join(cells))
    return r"\begin{bmatrix}" + r"\\".join(rows) + r"\end{bmatrix}"

E1 = [1, 2, 5, 4]; E2 = [2, 3, 6, 5]; E3 = [4, 5, 8, 7]; E4 = [5, 6, 9, 8]

EQS = [
 ("w_resid", r"\{\partial\}[E]\{\partial\}^T\{N\}\{\hat T\}^T\neq -q_h"),
 ("w_weighted", r"\int_x\!\int_y\{N\}^T\Big(\{\partial\}[E]\{\partial\}^T\{N\}\{\hat T\}^T+q_h\Big)\,dy\,dx=0"),
 ("w_ibp1d", r"\int_0^L N_i\,\frac{d}{dx}\Big(k\frac{dT}{dx}\Big)dx=\Big[N_i\,k\frac{dT}{dx}\Big]_0^L-\int_0^L\frac{dN_i}{dx}\,k\,\frac{dT}{dx}\,dx"),
 ("w_green", r"\int_x\!\int_y N_i\,\frac{\partial F}{\partial x}\,dy\,dx=\oint_s N_i\,F\,n_x\,ds-\int_x\!\int_y\frac{\partial N_i}{\partial x}\,F\,dy\,dx"),
 ("w_ibp", r"-\int_x\!\int_y\{N\}^T\{\partial\}[E]\{\partial\}^T\{N\}\{\hat T\}^T\,dy\,dx=-\int_x\!\int_y\{N\}^Tq_h\,dy\,dx-\int_s\{N\}^Tq_b\,ds"),
 ("w_rearr", r"\underbrace{\int_x\!\int_y\{N\}^T\{\partial\}[E]\{\partial\}^T\{N\}\,dy\,dx}_{[k]}\{\hat T\}^T=\underbrace{\int_x\!\int_y\{N\}^Tq_h\,dy\,dx}_{\{q\}}+\underbrace{\int_s\{N\}^Tq_b\,ds}_{\{b\}}"),
 ("w_qb", r"q_b=\Big(k_x\frac{\partial T}{\partial x}\Big)n_x+\Big(k_y\frac{\partial T}{\partial y}\Big)n_y=k\,\frac{\partial T}{\partial n}\qquad(\text{positive when heat enters})"),
 ("w_k", r"[k]=\int_x\!\int_y\{N\}^T\{\partial\}[E]\{\partial\}^T\{N\}\,dy\,dx"),
 ("w_q", r"\{q\}=\int_x\!\int_y\{N\}^Tq_h\,dy\,dx"),
 ("w_b", r"\{b\}=\int_s\{N\}^Tq_b\,ds"),
 ("w_sys", r"[k]\{\hat T\}^T=\{q\}+\{b\}=\{r\}"),
 ("w_s1", r"\cdots\{N_3\}\left\{\dfrac{\partial}{\partial x}\quad\dfrac{\partial}{\partial y}\right\}\cdots"),
 ("w_s2", r"\cdots\left\{\dfrac{\partial N_3}{\partial x}\quad\dfrac{\partial N_3}{\partial y}\right\}\begin{bmatrix}k_x&0\\0&k_y\end{bmatrix}\cdots"),
 ("w_s3", r"\cdots\left\{k_x\dfrac{\partial N_3}{\partial x}\quad k_y\dfrac{\partial N_3}{\partial y}\right\}\begin{Bmatrix}\dfrac{\partial}{\partial x}\\[8pt]\dfrac{\partial}{\partial y}\end{Bmatrix}\cdots"),
 ("w_s4", r"\cdots\left\{k_x\dfrac{\partial N_3}{\partial x}\dfrac{\partial}{\partial x}\quad k_y\dfrac{\partial N_3}{\partial y}\dfrac{\partial}{\partial y}\right\}\{N_4\}\cdots"),
 ("w_s5", r"k_{34}=\int_0^a\!\!\int_0^b\Big(k_x\frac{\partial N_3}{\partial x}\frac{\partial N_4}{\partial x}+k_y\frac{\partial N_3}{\partial y}\frac{\partial N_4}{\partial y}\Big)dy\,dx"),
 ("w_s5b", r"\begin{aligned}\frac{\partial N_3}{\partial x}\frac{\partial N_4}{\partial x}&=\frac{y}{ab}\cdot\frac{-y}{ab}=-\frac{y^2}{a^2b^2}&&\Rightarrow\ \int_0^a\!\!\int_0^b-\frac{k_x\,y^2}{a^2b^2}\,dy\,dx=-\frac{b\,k_x}{3a}\\[6pt]\frac{\partial N_3}{\partial y}\frac{\partial N_4}{\partial y}&=\frac{x}{ab}\cdot\frac{a-x}{ab}=\frac{x(a-x)}{a^2b^2}&&\Rightarrow\ \int_0^a\!\!\int_0^b\frac{k_y\,x(a-x)}{a^2b^2}\,dy\,dx=\frac{a\,k_y}{6b}\end{aligned}"),
 ("w_k34", r"k_{34}=-\frac{b\,k_x}{3a}+\frac{a\,k_y}{6b}"),
 ("w_kfull", r"[k]=\begin{bmatrix}s_1&s_2&s_3&s_4\\s_2&s_1&s_4&s_3\\s_3&s_4&s_1&s_2\\s_4&s_3&s_2&s_1\end{bmatrix}"),
 ("w_svals", r"\begin{aligned}s_1&=\frac{b\,k_x}{3a}+\frac{a\,k_y}{3b}, & s_2&=-\frac{b\,k_x}{3a}+\frac{a\,k_y}{6b}\\[4pt]s_3&=-\frac{b\,k_x}{6a}-\frac{a\,k_y}{6b}, & s_4&=\frac{b\,k_x}{6a}-\frac{a\,k_y}{3b}\end{aligned}"),
 ("w_qconst", r"\{q\}=q_h\int_0^a\!\!\int_0^b\{N\}^T dy\,dx=\frac{q_h\,a\,b}{4}\begin{Bmatrix}1\\1\\1\\1\end{Bmatrix}"),
 ("w_bedge", r"\{b\}=\int_0^b\{N\}^T\big|_{x=a}\,q_b\,dy=q_b\int_0^b\Big\{0\ \ \frac{b-y}{b}\ \ \frac{y}{b}\ \ 0\Big\}^T dy=\frac{q_b\,b}{2}\begin{Bmatrix}0\\1\\1\\0\end{Bmatrix}"),
 ("w_act2", r"\begin{aligned}s_1&=\frac{0.5(300)}{3(0.5)}+\frac{0.5(300)}{3(0.5)}=100+100=200, & s_2&=-100+50=-50\\[4pt]s_3&=-50-50=-100, & s_4&=50-100=-50\end{aligned}"),
 ("w_k251", r"[k^1]=[k^2]=[k^3]=[k^4]=\begin{bmatrix}200&-50&-100&-50\\-50&200&-50&-100\\-100&-50&200&-50\\-50&-100&-50&200\end{bmatrix}"),
 ("w_r252", r"\{r^1\}=\{r^2\}=\{r^3\}=\{r^4\}=\frac{600\,(0.5)(0.5)}{4}\begin{Bmatrix}1\\1\\1\\1\end{Bmatrix}=\begin{Bmatrix}37.5\\37.5\\37.5\\37.5\end{Bmatrix}"),
 ("w_rowsum", r"s_1+s_2+s_3+s_4=0\quad\Rightarrow\quad[k]\begin{Bmatrix}1\\1\\1\\1\end{Bmatrix}=\begin{Bmatrix}0\\0\\0\\0\end{Bmatrix}"),
 ("w_scatter", r"K_{IJ}\ \mathrel{+}=\ k^{e}_{ij}\qquad\text{with }I=\mathrm{conn}(e,i),\ J=\mathrm{conn}(e,j)"),
 ("w_K_e1", kmat_colored([(E1, MAR)])),
 ("w_K_e12", kmat_colored([(E1, MAR), (E2, TEA)])),
 ("w_K_full", r"\begin{bmatrix}200&-50&0&-50&-100&0&0&0&0\\-50&400&-50&-100&-100&-100&0&0&0\\0&-50&200&0&-100&-50&0&0&0\\-50&-100&0&400&-100&0&-50&-100&0\\-100&-100&-100&-100&800&-100&-100&-100&-100\\0&-100&-50&0&-100&400&0&-100&-50\\0&0&0&-50&-100&0&200&-50&0\\0&0&0&-100&-100&-100&-50&400&-50\\0&0&0&0&-100&-50&0&-50&200\end{bmatrix}\begin{Bmatrix}T_1\\T_2\\T_3\\T_4\\T_5\\T_6\\T_7\\T_8\\T_9\end{Bmatrix}=\begin{Bmatrix}37.5\\75\\37.5\\75\\150\\75\\37.5\\75\\37.5\end{Bmatrix}"),
 ("w_reduced", r"\begin{bmatrix}400&-50&-100&-100\\-50&200&-100&-50\\-100&-100&800&-100\\-100&-50&-100&400\end{bmatrix}\begin{Bmatrix}T_2\\T_3\\T_5\\T_6\end{Bmatrix}=\begin{Bmatrix}75\\37.5\\150\\75\end{Bmatrix}\quad\Rightarrow\quad\begin{Bmatrix}T_2\\T_3\\T_5\\T_6\end{Bmatrix}=\begin{Bmatrix}0.482\\0.621\\0.386\\0.482\end{Bmatrix}"),
 ("w_nonzero", r"\{F\}\leftarrow\{F\}-[K]_{(:,\,k)}\,\bar T_k\qquad\text{then delete row and column }k"),
 ("w_act5", r"\begin{aligned}400(0.482)-50(0.621)-100(0.386)-100(0.482)&=192.8-31.05-38.6-48.2\\&=74.95\approx75\ \checkmark\end{aligned}"),
 ("w_local", r"x_{\mathrm{loc}}=x-x_1^{e},\qquad y_{\mathrm{loc}}=y-y_1^{e}"),
 ("w_interp", r"\begin{aligned}T(x,y)&=\{N(x_{\mathrm{loc}},y_{\mathrm{loc}})\}\{\hat T^{e}\}^T\\[4pt]\{\hat T^{e}\}&=\{T_{\mathrm{conn}(e,1)}\ \ T_{\mathrm{conn}(e,2)}\ \ T_{\mathrm{conn}(e,3)}\ \ T_{\mathrm{conn}(e,4)}\}\end{aligned}"),
 ("w_fluxc", r"\begin{Bmatrix}q_x\\q_y\end{Bmatrix}=-[E]\{\partial\}^T\{N\}\{\hat T^{e}\}^T\qquad\text{element 2, centroid: }\begin{Bmatrix}q_x\\q_y\end{Bmatrix}=\begin{Bmatrix}-70.7\\+70.7\end{Bmatrix}\mathrm{W\,m^{-2}}"),
 ("w_act6_N", r"\begin{aligned}a=b=0.5\ \mathrm{m},\quad(x_{\mathrm{loc}},y_{\mathrm{loc}})&=(0.3,\,0.2)\ \mathrm{m}\\[4pt]N_1=\frac{(a-x)(b-y)}{ab}=\frac{(0.2)(0.3)}{0.25}=0.24,\qquad N_2&=\frac{x(b-y)}{ab}=\frac{(0.3)(0.3)}{0.25}=0.36\\[4pt]N_3=\frac{xy}{ab}=\frac{(0.3)(0.2)}{0.25}=0.24,\qquad N_4&=\frac{y(a-x)}{ab}=\frac{(0.2)(0.2)}{0.25}=0.16\end{aligned}"),
 ("w_act6_T", r"\begin{aligned}T&=N_1T_1+N_2T_2+N_3T_5+N_4T_4\\&=0.24(0)+0.36(0.482)+0.24(0.386)+0.16(0)=0.266\ ^{\circ}\mathrm{C}\end{aligned}"),
 ("w_err", r"\begin{aligned}\text{error}&=\frac{T_{2\times2}-T_{\mathrm{ref}}}{T_{\mathrm{ref}}}\\[4pt]\frac{0.4821-0.4589}{0.4589}&=+5.1\%,\qquad\frac{0.6214-0.5897}{0.5897}=+5.4\%\end{aligned}"),
 ("w_asg_hint", r"\{r^{1}\}=\frac{Q\,a\,b}{4}\{1\ \ 1\ \ 1\ \ 1\}^T,\qquad T(1.4,\,2.2)=\{N(x_{\mathrm{loc}},y_{\mathrm{loc}})\}\{\hat T^{1}\}^T"),
]
