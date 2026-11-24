"""LaTeX sources for the ANSYS demo page (Part 6) of the course site (notes: p6_*, worked examples: x1_* to x4_*).
Every number was recomputed with SEAA4243-FEM/code/fe_heat_q4.py and fe_plane_stress.py (the patch test of Example 4
with a small independent assembly that calls fe_plane_stress.element_stiffness); see src/tools/content_p6.py.
Lines are stacked so that each equation stays near 1000 px wide at em 44 (readable on a phone).
Render: python3 eqs_ps4_ex.py   (needs `npm ci` in this folder)"""
EQS = [
 # ---------------- notes ----------------
 ("p6_load", r"\begin{aligned}\text{Force: }\ F_y&=q_y\,H=(-5000)(2)=-10\,000\ \mathrm{N}\\\text{Pressure: }\ p_y&=\frac{q_y}{t}=\frac{-5000}{0.01}\\&=-500\times10^{3}\ \mathrm{N\,m^{-2}}=-500\ \mathrm{kPa}\end{aligned}"),
 ("p6_load_chk", r"p_y\times(H\,t)=(-500\times10^{3})(2)(0.01)=-10\,000\ \mathrm{N}\quad\checkmark"),
 ("p6_size", r"\begin{aligned}\text{cantilever: }\ a&=\frac{L}{N_x}=\frac{4}{2}=2\ \mathrm{m},\qquad b=\frac{H}{N_y}=\frac{2}{2}=1\ \mathrm{m}\\\text{plate: }\ h&=\frac{1}{16}=0.0625\ \mathrm{m}\ \Rightarrow\ 16\times16\end{aligned}"),
 ("p6_heat", r"\begin{aligned}\text{generated: }\ Q\,A\,t&=600\times1\times t\ \mathrm{W}\\\textstyle\sum\text{reactions, Temperature edges}&=-600\,t\ \mathrm{W}\ \ (\text{removed})\end{aligned}"),
 ("p6_plate_err", r"\begin{aligned}2\times2:&\ \ \frac{0.6214-0.5897}{0.5897}=+5.4\%\\16\times16:&\ \ \frac{0.5898-0.5897}{0.5897}=+0.02\%\end{aligned}"),
 ("p6_change", r"\text{change}=\frac{v_{\text{fine}}-v_{\text{coarse}}}{v_{\text{fine}}}\times100\%"),
 ("p6_timo", r"\begin{aligned}v_{\text{tip}}&=\frac{PL^{3}}{3EI}+\frac{PL}{\kappa GA}=0.1600+0.0319=0.1919\ \mathrm{m}\\I&=\frac{tH^{3}}{12}=6.667\times10^{-3}\ \mathrm{m^{4}},\quad A=tH=0.02\ \mathrm{m^{2}}\\G&=\frac{E}{2(1+\nu)}=75.19\times10^{6}\ \mathrm{N\,m^{-2}},\quad\kappa=\tfrac56\end{aligned}"),
 ("p6_reaction", r"\begin{aligned}\textstyle\sum R_y&=-F_y=+10\,000\ \mathrm{N},\qquad\sum R_x=0\\M_{\text{support}}&=P\,L=10\,000\times4=40\,000\ \mathrm{N\,m}\end{aligned}"),
 ("p6_beam_mid", r"\begin{aligned}(2,\,1.5):\quad M&=10\,000\,(4-2)=20\,000\ \mathrm{N\,m}\\\sigma_{xx}^{\text{beam}}&=\frac{M\,(y-H/2)}{I}=\frac{20\,000\,(0.5)}{6.667\times10^{-3}}\\&=1500\ \mathrm{kN\,m^{-2}}\end{aligned}"),
 ("p6_strain_ratio", r"\begin{aligned}\frac{v_{\text{plane strain}}}{v_{\text{plane stress}}}&\approx1-\nu^{2}=0.891\\\text{Q8 }32\times16:\ \ &\frac{0.1722}{0.1915}=0.899\end{aligned}"),
 ("p6_thick", r"\begin{aligned}v_{\text{tip}}\propto\frac1t:\quad t=1\ \mathrm{m}\ \Rightarrow\ v_{\text{tip}}&=0.001915\ \mathrm{m}\\\text{instead of}\ &\ 0.1915\ \mathrm{m}\ \ (t=0.01\ \mathrm{m})\end{aligned}"),
 ("p6_k11", r"\begin{aligned}k_{11}&=\bar E\,t\Big[\frac{b}{3a}+\frac{(1-\nu)\,a}{6b}\Big]\\&=2.2444\times10^{6}\Big[\frac16+\frac{0.67(2)}{6}\Big]=0.8753\times10^{6}\ \mathrm{N\,m^{-1}}\end{aligned}"),
 ("p6_predict", r"\text{predict}\ \rightarrow\ \text{run}\ \rightarrow\ \text{compare}\ \rightarrow\ \text{explain}\ \rightarrow\ \text{trust}"),
 # ---------------- Example 1: the plate (text §2.3) in Steady-State Thermal ----------------
 ("x1_k", r"\begin{aligned}a=b=0.5\ \mathrm{m}:\quad[k]&=\frac{k\,t}{6}\begin{bmatrix}4&-1&-2&-1\\-1&4&-1&-2\\-2&-1&4&-1\\-1&-2&-1&4\end{bmatrix}\\&=50\,[\,\cdots]\ \mathrm{W\,{}^{\circ}C^{-1}}\quad(k=300,\ t=1)\end{aligned}"),
 ("x1_q", r"\begin{aligned}\{q\}^{e}&=\frac{Q\,a\,b\,t}{4}\{1,\,1,\,1,\,1\}^{T}=\frac{600(0.25)(1)}{4}=37.5\ \mathrm{W\ each}\\R_2&=R_6=75,\quad R_3=37.5,\quad R_5=150\ \mathrm{W}\end{aligned}"),
 ("x1_sys", r"\begin{bmatrix}400&-50&-100&-100\\-50&200&-100&-50\\-100&-100&800&-100\\-100&-50&-100&400\end{bmatrix}\begin{Bmatrix}T_2\\T_3\\T_5\\T_6\end{Bmatrix}=\begin{Bmatrix}75\\37.5\\150\\75\end{Bmatrix}"),
 ("x1_red", r"\begin{aligned}T_6=T_2:\quad300\,T_2-50\,T_3-100\,T_5&=75\\-100\,T_2+200\,T_3-100\,T_5&=37.5\\-200\,T_2-100\,T_3+800\,T_5&=150\end{aligned}"),
 ("x1_T", r"T_2=T_6=0.4821,\qquad T_3=0.6214,\qquad T_5=0.3857\ \ {}^{\circ}\mathrm{C}"),
 ("x1_chk", r"\begin{aligned}&300(0.48214)-50(0.62143)-100(0.38571)\\&=144.64-31.07-38.57=75.00\quad\checkmark\end{aligned}"),
 ("x1_heat", r"\begin{aligned}\text{nodes }1,4,7,8,9:\ \ &-100.18-161.79-76.07\\&-161.79-100.18\\&=-600.0\ \mathrm{W}=-Q\,A\,t\quad\checkmark\end{aligned}"),
 ("x1_err", r"\begin{aligned}\frac{T_h-0.5897}{0.5897}:\quad2\times2&:\ +5.4\%,\qquad4\times4:\ +1.2\%\\8\times8&:\ +0.25\%,\qquad16\times16:\ +0.02\%\end{aligned}"),
 # ---------------- Example 2: the cantilever (text §3.4) in Static Structural ----------------
 ("x2_in", r"\begin{aligned}F_y&=q_yH=-10\,000\ \mathrm{N}\quad\text{or}\quad p_y=\frac{q_y}{t}=-500\ \mathrm{kPa}\\E&=200\times10^{6}\ \mathrm{N\,m^{-2}}=2\times10^{8}\ \mathrm{Pa},\qquad\nu=0.33\\\text{Edge Sizing}&=2\ \text{divisions on each edge}\\&\Rightarrow\ 2\ \mathrm{m}\times1\ \mathrm{m}\ \text{elements}\end{aligned}"),
 ("x2_chg", r"\begin{aligned}4\times2:&\ \frac{0.18846-0.17796}{0.18846}=5.57\%\\8\times4:&\ \frac{0.19059-0.18846}{0.19059}=1.12\%\\16\times8:&\ \frac{0.19125-0.19059}{0.19125}=0.35\%\end{aligned}"),
 ("x2_diff", r"\begin{aligned}8\times4:&\ \frac{0.19059-0.19192}{0.19192}=-0.69\%\\16\times8:&\ \frac{0.19125-0.19192}{0.19192}=-0.35\%\end{aligned}"),
 ("x2_rich", r"\begin{aligned}\Delta_1&=0.19059-0.18846=0.00213\\\Delta_2&=0.19125-0.19059=0.00066\\2^{p}&\approx\frac{0.00213}{0.00066}=3.23,\qquad p\approx1.69\\Q&\approx0.19125+\frac{0.00066}{3.23-1}=0.19155\ \mathrm{m}\\\text{error of }16\times8&=\frac{0.19125-0.19155}{0.19155}=-0.16\%\end{aligned}"),
 ("x2_lin", r"\begin{aligned}\text{Linear }16\times8:&\ 0.18863\ \mathrm{m}\ \ (-1.7\%\ \text{from Timoshenko})\\\text{Linear }8\times4:&\ 0.18243\ \mathrm{m}\ \ (-4.3\%\ \text{from quadratic }8\times4)\end{aligned}"),
 # ---------------- Example 3: four wrong runs ----------------
 ("x3_ratio", r"\begin{aligned}\text{A: }&\frac{0.001915}{0.1915}=0.0100=\frac{0.01}{1}\\\text{B: }&\frac{0.2298}{0.1915}=1.20\ \text{(loaded vertex)}\\&\frac{0.1875}{0.1889}=0.993\ \text{(mid-depth)}\\\text{C: }&\frac{0.1722}{0.1915}=0.899\approx1-\nu^{2}=0.891\end{aligned}"),
 ("x3_vm", r"\begin{aligned}\text{B: }\ \sigma_{\mathrm{vM}}\ \text{under the load}&=5353\ \mathrm{kN\,m^{-2}}\\\text{edge traction}&=523\ \mathrm{kN\,m^{-2}}\quad(\times10.2)\end{aligned}"),
 # ---------------- Example 4: Stage 1 gates for your own solver ----------------
 ("x4_loads", r"\begin{aligned}F_x&=\sigma_0\,t\,\frac{b}{2}\ \text{per node of each side}\\&=\frac{10^{6}(0.01)(0.4)}{2}=2000,\quad\frac{10^{6}(0.01)(0.6)}{2}=3000\ \mathrm{N}\\\{F_x\}_{x=2}&=\{2000,\ 5000,\ 3000\}\ \mathrm{N}\end{aligned}"),
 ("x4_exact", r"\begin{aligned}u&=\frac{\sigma_0\,x}{E},\qquad v=-\frac{\nu\,\sigma_0\,y}{E}\\u(2,y)&=\frac{10^{6}(2)}{200\times10^{6}}=0.0100\ \mathrm{m}\\v(x,1)&=-\frac{0.3(10^{6})(1)}{200\times10^{6}}=-0.0015\ \mathrm{m}\end{aligned}"),
 ("x4_R", r"\textstyle\sum R_x=-2000-5000-3000=-10\,000\ \mathrm{N}=-\sigma_0\,t\,H\quad\checkmark"),
 ("x4_bug", r"\begin{aligned}\text{load bug }(\sigma_0tb\text{ for }\sigma_0tb/2):&\ \ u(2,y)=0.0200\ \mathrm{m}\\&\ \ \textstyle\sum R_x=-20\,000\ \mathrm{N}\\\text{shear bug }(\bar E\text{ for }\bar E\tfrac{1-\nu}{2}):&\ \ \text{patch test exact}\\&\ \ v_{\text{tip}}^{\,\text{Q8 }16\times8}=0.1696\ \mathrm{m}\ (-11.6\%)\end{aligned}"),
]

if __name__ == "__main__":
    import pathlib, sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from eqlib import render
    out = pathlib.Path(__file__).parent / "eqs_ps4_ex"
    rep = render([{"name": n, "tex": t} for n, t in EQS], out)
    for n, r in rep.items():
        print(f"{n:16s} {r['w']:5d} x {r['h']:4d}" + ("   WIDE" if r["w"] > 1150 else ""))
