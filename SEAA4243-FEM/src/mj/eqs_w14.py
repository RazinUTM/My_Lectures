"""LaTeX sources for Week 14 equations (ANSYS demo)."""
EQS = [
 ("t_load_conv", r"F_y=q_y\,H=(-5000\ \mathrm{N\,m^{-1}})(2\ \mathrm{m})=-10\,000\ \mathrm{N}\qquad\text{or}\qquad p_y=\frac{q_y}{t}=\frac{-5000}{0.01}=-500\ \mathrm{kPa}"),
 ("t_check_load", r"p_y\times(\text{edge length}\times t)=(-500\times10^{3})(2)(0.01)=-10\,000\ \mathrm{N}\quad\checkmark"),
 ("t_conv_pct", r"\text{change}=\frac{u_{\text{fine}}-u_{\text{coarse}}}{u_{\text{fine}}}\times100\%\qquad\text{report the mesh after which }|\text{change}|<\text{your tolerance (say 2\%)}"),
 ("t_strain_E", r"[E]_{\text{plane strain}}=\frac{E}{(1+\nu)(1-2\nu)}\begin{bmatrix}1-\nu&\nu&0\\\nu&1-\nu&0\\0&0&\frac{1-2\nu}{2}\end{bmatrix}\qquad\text{versus}\qquad[E]_{\text{plane stress}}=\frac{E}{1-\nu^2}\begin{bmatrix}1&\nu&0\\\nu&1&0\\0&0&\frac{1-\nu}{2}\end{bmatrix}"),
 ("t_strain_ratio", r"\frac{v_{\text{plane strain}}}{v_{\text{plane stress}}}\approx1-\nu^{2}=0.891\qquad\text{(course solver, 32}\times\text{16: }0.171/0.191=0.90\text{)}"),
 ("t_thick", r"v_{\text{tip}}\propto\frac{1}{t}:\qquad t=1\ \mathrm{m}\ \text{instead of}\ 0.01\ \mathrm{m}\ \Rightarrow\ v_{\text{tip}}=0.0019\ \mathrm{m}\ \text{instead of}\ 0.191\ \mathrm{m}"),
 ("t_reaction", r"\begin{aligned}\sum R_y&=+10\,000\ \mathrm{N}\ \ (=\text{applied load}),\qquad\sum M_{\text{support}}=10\,000\times4=40\,000\ \mathrm{N\,m}\\&\text{Reaction probe on the Fixed Support: the first check, before any contour plot}\end{aligned}"),
 ("t_heat_check", r"\begin{aligned}\text{heat generated}&=q_h\times\text{area}\times\text{thickness}=600\times1\times t\ \mathrm{W}\\&=\text{heat leaving through the two cold edges (Reaction probe on the Temperature conditions)}\end{aligned}"),
 ("t_predict", r"\text{predict}\ \rightarrow\ \text{run}\ \rightarrow\ \text{compare}\ \rightarrow\ \text{explain the difference}\ \rightarrow\ \text{only then trust}"),
]
