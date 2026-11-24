"""LaTeX sources for Week 13 equations."""
EQS = [
 ("t_beam_line", r"\sigma_{xx}^{\text{beam}}=\frac{M\,(y-1)}{I},\qquad M=P\,(L-x),\qquad P=10\ \mathrm{kN},\qquad I=\frac{t\,H^{3}}{12}=6.667\times10^{-3}\ \mathrm{m^{4}}"),
 ("t_recover", r"\{\varepsilon\}^T=[B]\{\hat u\}^T\quad(3\times8)(8\times1),\qquad\{\sigma\}^T=[E]\{\varepsilon\}^T=[E][B]\{\hat u\}^T"),
 ("t_Bnum", r"[B]_{(1.5,\,0.3)}=\begin{bmatrix}-0.35&0&0.35&0&0.15&0&-0.15&0\\0&-0.25&0&-0.75&0&0.75&0&0.25\\-0.25&-0.35&-0.75&0.35&0.75&0.15&0.25&-0.15\end{bmatrix}"),
 ("t_u4", r"\begin{aligned}\{\hat u^{4}\}&=\{u_5\ v_5\ \ u_6\ v_6\ \ u_9\ v_9\ \ u_8\ v_8\}\qquad\text{course MATLAB solution of (3.49), six decimals}\\&=\{0\ \ {-0.043013}\ \ 0\ \ {-0.130421}\ \ 0.041967\ \ {-0.130578}\ \ 0.030966\ \ {-0.045520}\}\ \mathrm{m}\end{aligned}"),
 ("t_eps_num", r"\begin{aligned}\varepsilon_{xx}&=0.15(0.041967)-0.15(0.030966)=0.0016501\\\varepsilon_{yy}&=-0.25(-0.043013)-0.75(-0.130421)+0.75(-0.130578)+0.25(-0.045520)=-0.0007445\\\varepsilon_{xy}&=-0.35(-0.043013)+0.35(-0.130421)+0.75(0.041967)+0.15(-0.130578)\\&\quad+0.25(0.030966)-0.15(-0.045520)=-0.0041348\end{aligned}"),
 ("t_sig_num", r"\begin{Bmatrix}\sigma_{xx}\\\sigma_{yy}\\\sigma_{xy}\end{Bmatrix}=\begin{bmatrix}224.44&74.07&0\\74.07&224.44&0\\0&0&75.19\end{bmatrix}\!\times10^{6}\begin{Bmatrix}0.0016501\\-0.0007445\\-0.0041348\end{Bmatrix}=\begin{Bmatrix}315.2\\-44.9\\-310.9\end{Bmatrix}\mathrm{kN\,m^{-2}}"),
 ("t_beam_sig", r"\begin{aligned}\sigma_{xx}&=\frac{M\,(y-1)}{I},\qquad I=\frac{t\,H^3}{12}=6.667\times10^{-3}\ \mathrm{m^4}\\[4pt]M&=P(L-x)=10^{4}(4-3.5)=5\ \mathrm{kN\,m}\\[4pt]\sigma_{xx}(3.5,\,1.3)&=\frac{5000\,(0.3)}{6.667\times10^{-3}}=225\ \mathrm{kN\,m^{-2}}\end{aligned}"),
 ("t_principal", r"\begin{aligned}\sigma_{1,2}&=\frac{\sigma_{xx}+\sigma_{yy}}{2}\pm\sqrt{\Big(\frac{\sigma_{xx}-\sigma_{yy}}{2}\Big)^2+\sigma_{xy}^2}=135.2\pm359.3\\&\Rightarrow\ \sigma_1=494,\quad\sigma_2=-224\ \mathrm{kN\,m^{-2}}\end{aligned}"),
 ("t_vm", r"\sigma_{\mathrm{vM}}=\sqrt{\sigma_{xx}^2-\sigma_{xx}\sigma_{yy}+\sigma_{yy}^2+3\sigma_{xy}^2}=637\ \mathrm{kN\,m^{-2}}\qquad(\text{plane stress})"),
 ("t_centroid", r"\begin{aligned}&\text{centroid of element 4, }(3,\,1.5),\ \text{local }(1,\,0.5):\quad\{\varepsilon\}=\{0.00275\ \ {-0.00133}\ \ {-0.00665}\}\\&\sigma_{xx}=518.6\ \mathrm{kN\,m^{-2}}\qquad\text{beam theory at the same point: }\frac{10^{4}(1)(0.5)}{6.667\times10^{-3}}=750\ \mathrm{kN\,m^{-2}}\end{aligned}"),
 ("t_q8_sizes", r"[N]:\ 2\times16,\qquad[B]=[\partial]^T[N]:\ 3\times16,\qquad[k]=t\int\!\!\int[B]^T[E][B]\,dA:\ 16\times16"),
 ("t_q8_N", r"\begin{aligned}N_1&=-\frac{(a-x)(b-y)(2ay-ab+2bx)}{a^2b^2}&&\text{corner node}\\[4pt]N_5&=\frac{4x(a-x)(b-y)}{a^2b}&&\text{mid-side node}\end{aligned}"),
 ("t_q8_loads", r"\begin{aligned}\{r^2\}:\quad\frac{Q_yb}{6}&=-1667\ \mathrm{N},\qquad\frac{2Q_yb}{3}=-6667\ \mathrm{N},\qquad\frac{Q_yb}{6}=-1667\ \mathrm{N}\\&(Q_y=-5000\ \mathrm{N\,m^{-1}},\ b=2\ \mathrm{m}\text{: one element spans the whole depth})\end{aligned}"),
 ("t_err", r"\begin{aligned}\text{Q4 }2\times2\ (4\text{ elements, 18 dofs}):&\quad\frac{0.131-0.192}{0.192}=-32\%\\\text{Q8 }2\times1\ (2\text{ elements, 26 dofs}):&\quad\frac{0.178-0.192}{0.192}=-7\%\\\text{Q8 }4\times4\ (16\text{ elements}):&\quad\frac{0.189-0.192}{0.192}=-1.6\%\end{aligned}"),
]
