"""LaTeX sources for the worked-example (answer scheme) equations of the course site.
Book notation (FEM by Hand, Chapter 8): [k]{T} = {q} + {b} = {r}, Q heat generated per unit
volume, q_n inward boundary flux, thickness t, s1..s4 of Eq. (8.6)."""
EQS = [
 # ---- Part 1 · Example 1: three-node triangle (book Example 8.1) ----
 ("x1_cond", r"\begin{aligned}T(0,0)&=a_1=T_1\\T(L,0)&=a_1+a_2L=T_2\\T\!\left(\tfrac{L}{2},L\right)&=a_1+\tfrac{L}{2}a_2+La_3=T_3\end{aligned}"),
 ("x1_coef", r"\begin{aligned}a_1&=T_1,\qquad a_2=\frac{T_2-T_1}{L}\\[4pt]a_3&=\frac{1}{L}\Big(T_3-T_1-\frac{T_2-T_1}{2}\Big)=\frac{2T_3-T_1-T_2}{2L}\end{aligned}"),
 ("x1_collect", r"\begin{aligned}T&=T_1+\frac{T_2-T_1}{L}\,x+\frac{2T_3-T_1-T_2}{2L}\,y\\[4pt]&=\Big(1-\frac{x}{L}-\frac{y}{2L}\Big)T_1+\Big(\frac{x}{L}-\frac{y}{2L}\Big)T_2+\frac{y}{L}\,T_3\end{aligned}"),
 ("x1_N", r"N_1=1-\frac{x}{L}-\frac{y}{2L},\qquad N_2=\frac{x}{L}-\frac{y}{2L},\qquad N_3=\frac{y}{L}"),
 ("x1_checks", r"\begin{aligned}\text{node 3 }(\tfrac{L}{2},L):\quad&N_1=1-\tfrac12-\tfrac12=0,\quad N_2=\tfrac12-\tfrac12=0,\quad N_3=1\\\sum N_i&=1-\tfrac{x}{L}-\tfrac{y}{2L}+\tfrac{x}{L}-\tfrac{y}{2L}+\tfrac{y}{L}=1\end{aligned}"),
 ("x1_dN", r"\Big\{\frac{\partial N}{\partial x}\Big\}=\frac{1}{L}\begin{Bmatrix}-1\\1\\0\end{Bmatrix},\qquad\Big\{\frac{\partial N}{\partial y}\Big\}=\frac{1}{L}\begin{Bmatrix}-1/2\\-1/2\\1\end{Bmatrix},\qquad A=\frac{L^2}{2}"),
 ("x1_kij", r"\begin{aligned}k_{11}&=tAk\,\frac{1+\tfrac14}{L^2}=\frac{5kt}{8}, & k_{12}&=tAk\,\frac{-1+\tfrac14}{L^2}=-\frac{3kt}{8}\\[4pt]k_{13}&=tAk\,\frac{0-\tfrac12}{L^2}=-\frac{kt}{4}, & k_{33}&=tAk\,\frac{0+1}{L^2}=\frac{kt}{2}\end{aligned}"),
 ("x1_k", r"[k]=\frac{kt}{8}\begin{bmatrix}5&-3&-2\\-3&5&-2\\-2&-2&4\end{bmatrix}"),
 # ---- Part 1 · Example 2: temperature and flux at a point (book Practice Problem 8.3) ----
 ("x2_Nc", r"N_i\Big(\frac{a}{2},\frac{b}{2}\Big)=\frac{(a/2)(b/2)}{ab}=\frac14\quad\Rightarrow\quad T=\frac14(20+40+60+30)=37.5\ ^{\circ}\mathrm{C}"),
 ("x2_dNc", r"\begin{aligned}\frac{\partial N_i}{\partial x}&=\frac{1}{ab}\{-(b-y),\ b-y,\ y,\ -y\}\\&=\frac{1}{0.12}\{-0.15,\ 0.15,\ 0.15,\ -0.15\}=\{-1.25,\ 1.25,\ 1.25,\ -1.25\}\ \mathrm{m^{-1}}\end{aligned}"),
 ("x2_dNcy", r"\begin{aligned}\frac{\partial N_i}{\partial y}&=\frac{1}{ab}\{-(a-x),\ -x,\ x,\ a-x\}\\&=\frac{1}{0.12}\{-0.2,\ -0.2,\ 0.2,\ 0.2\}=\{-1.667,\ -1.667,\ 1.667,\ 1.667\}\ \mathrm{m^{-1}}\end{aligned}"),
 ("x2_gradc", r"\begin{aligned}\frac{\partial T}{\partial x}&=1.25(-20+40+60-30)=62.5\ \mathrm{K\,m^{-1}}\\\frac{\partial T}{\partial y}&=1.667(-20-40+60+30)=50.0\ \mathrm{K\,m^{-1}}\\[4pt]q_x&=-k\frac{\partial T}{\partial x}=-15(62.5)=-937.5\ \mathrm{W\,m^{-2}}\\q_y&=-15(50.0)=-750\ \mathrm{W\,m^{-2}}\end{aligned}"),
 ("x2_Np", r"\begin{aligned}N_1&=\frac{(0.3)(0.1)}{0.12}=0.25, & N_2&=\frac{(0.1)(0.1)}{0.12}=0.0833\\[4pt]N_3&=\frac{(0.1)(0.2)}{0.12}=0.1667, & N_4&=\frac{(0.2)(0.3)}{0.12}=0.5\\[4pt]\sum N_i&=1.000\\T&=0.25(20)+0.0833(40)+0.1667(60)+0.5(30)=33.3\ ^{\circ}\mathrm{C}\end{aligned}"),
 ("x2_gradp", r"\begin{aligned}\frac{\partial N_i}{\partial x}&=\frac{1}{0.12}\{-0.1,\ 0.1,\ 0.2,\ -0.2\}, & \frac{\partial T}{\partial x}&=\frac{-2+4+12-6}{0.12}=66.7\ \mathrm{K\,m^{-1}}\\[4pt]\frac{\partial N_i}{\partial y}&=\frac{1}{0.12}\{-0.3,\ -0.1,\ 0.1,\ 0.3\}, & \frac{\partial T}{\partial y}&=\frac{-6-4+6+9}{0.12}=41.7\ \mathrm{K\,m^{-1}}\\[4pt]q_x&=-15(66.7)=-1000\ \mathrm{W\,m^{-2}}, & q_y&=-15(41.7)=-625\ \mathrm{W\,m^{-2}}\end{aligned}"),
 ("x3_rowsum", r"\sum_i N_i=1\ \Rightarrow\ [k]\{1\ \ 1\ \ \cdots\}^{\mathsf T}=\{0\}"),
 # ---- Part 2 · Example 1: [k] and loads of a square element (book Examples 8.2 and 8.3) ----
 ("y1_dN", r"\begin{aligned}\frac{\partial N_1}{\partial x}&=-\frac{b-y}{ab}, & \frac{\partial N_2}{\partial x}&=\frac{b-y}{ab}, & \frac{\partial N_3}{\partial x}&=\frac{y}{ab}\\[6pt]\frac{\partial N_1}{\partial y}&=-\frac{a-x}{ab}, & \frac{\partial N_2}{\partial y}&=-\frac{x}{ab}, & \frac{\partial N_3}{\partial y}&=\frac{x}{ab}\end{aligned}"),
 ("y1_k12", r"\begin{aligned}k_{12}&=t\int_0^a\!\!\int_0^b\frac{-k_x(b-y)^2+k_y\,x(a-x)}{a^2b^2}\,dy\,dx=\frac{t}{a^2b^2}\Big(-k_x\frac{ab^3}{3}+k_y\frac{a^3b}{6}\Big)\\[4pt]&=t\Big(-\frac{bk_x}{3a}+\frac{ak_y}{6b}\Big)=ts_2\end{aligned}"),
 ("y1_k13", r"\begin{aligned}k_{13}&=t\int_0^a\!\!\int_0^b\frac{-k_x(b-y)y-k_y\,x(a-x)}{a^2b^2}\,dy\,dx=\frac{t}{a^2b^2}\Big(-k_x\frac{ab^3}{6}-k_y\frac{a^3b}{6}\Big)\\[4pt]&=t\Big(-\frac{bk_x}{6a}-\frac{ak_y}{6b}\Big)=ts_3\end{aligned}"),
 ("y1_nums", r"\begin{aligned}\frac{bk_x}{3a}&=\frac{ak_y}{3b}=150,\qquad\frac{ak_y}{6b}=75\ \mathrm{W\,(m\,K)^{-1}}\\[4pt]ts_1&=0.005(150+150)=1.5, & ts_2&=0.005(-150+75)=-0.375\\ts_3&=0.005(-75-75)=-0.75, & ts_4&=0.005(75-150)=-0.375\ \mathrm{W\,K^{-1}}\end{aligned}"),
 ("y1_k", r"[k]=\begin{bmatrix}1.5&-0.375&-0.75&-0.375\\-0.375&1.5&-0.375&-0.75\\-0.75&-0.375&1.5&-0.375\\-0.375&-0.75&-0.375&1.5\end{bmatrix}\ \mathrm{W\,K^{-1}}"),
 ("y1_b", r"\begin{aligned}b_2=b_3&=t\,q_n\frac{b}{2}=0.005\,(10^6)\,\frac{0.025}{2}=62.5\ \mathrm{W}\\\{b\}&=\{0,\ 62.5,\ 62.5,\ 0\}^{\mathsf T}\ \mathrm{W}\qquad\text{total }125\ \mathrm{W}=q_n\,t\,b\end{aligned}"),
 ("y1_q", r"\begin{aligned}q_i&=t\,Q\,\frac{ab}{4}=0.005\,(10^7)\,\frac{0.025^2}{4}=7.8125\ \mathrm{W}\\\{q\}&=7.8125\{1,\ 1,\ 1,\ 1\}^{\mathsf T}\ \mathrm{W}\qquad\text{total }31.25\ \mathrm{W}=Q\,t\,ab\end{aligned}"),
 ("y1_qc", r"\begin{aligned}r_i&=Q\frac{ab}{4}=20\,\frac{2(3)}{4}=30\ \mathrm{W}\\\{r\}^1&=\{30,\ 30,\ 30,\ 30\}^{\mathsf T}\ \mathrm{W}\qquad(\text{total }120\ \mathrm{W}=Q\,ab)\end{aligned}"),
 # ---- Part 2 · Example 2: 2 x 2 mesh with a prescribed temperature and an inward flux (book Example 8.6) ----
 ("y2_K", r"[K]=0.375\begin{bmatrix}4&-1&0&-1&-2&0&0&0&0\\-1&8&-1&-2&-2&-2&0&0&0\\0&-1&4&0&-2&-1&0&0&0\\-1&-2&0&8&-2&0&-1&-2&0\\-2&-2&-2&-2&16&-2&-2&-2&-2\\0&-2&-1&0&-2&8&0&-2&-1\\0&0&0&-1&-2&0&4&-1&0\\0&0&0&-2&-2&-2&-1&8&-1\\0&0&0&0&-2&-1&0&-1&4\end{bmatrix}\ \mathrm{W\,K^{-1}}"),
 ("y2_loads", r"R_3=R_9=62.5\ \mathrm{W},\qquad R_6=62.5+62.5=125\ \mathrm{W},\qquad\text{all other }R_i=0"),
 ("y2_cols", r"\begin{aligned}T_2=T_5=T_8&=T_A,\qquad T_3=T_6=T_9=T_B\\9T_A-4.5T_B-4.5(400)&=0\\-4.5T_A+4.5T_B&=62.5+125+62.5=250\end{aligned}"),
 ("y2_sol", r"4.5T_A=1800+250\ \Rightarrow\ T_A=455.56\ \mathrm{K},\qquad T_B=T_A+\frac{250}{4.5}=511.11\ \mathrm{K}"),
 ("y2_check", r"\begin{aligned}\text{row 5: }&6(455.56)-0.75(400+455.56+511.11+400+511.11+400+455.56+511.11)\\&=2733.3-2733.3=0=R_5\end{aligned}"),
 ("y2_bal", r"\begin{aligned}&\text{struck rows 1, 4, 7: }-62.5,\ -125,\ -62.5\ \mathrm{W}\\&250\ \mathrm{W}\text{ leaves at the left edge}=250\ \mathrm{W}\text{ entering at the right edge}\end{aligned}"),
 ("y2_exact", r"T=400+\frac{q_n}{k}\,x=400+\frac{10^6}{450}\,x:\qquad T(0.025)=455.56,\quad T(0.05)=511.11\ \mathrm{K}"),
 # ---- Part 2 · Example 3: the textbook's worked example (book Example 8.7, text §2.3) ----
 ("y3_k", r"\begin{aligned}a=b=0.5\ \mathrm{m}:\quad s_1&=\frac{2k}{3}=200,\qquad s_2=s_4=-\frac{k}{6}=-50,\qquad s_3=-\frac{k}{3}=-100\ \mathrm{W\,^{\circ}C^{-1}}\\q_i&=Q\frac{ab}{4}=\frac{600(0.25)}{4}=37.5\ \mathrm{W}\end{aligned}"),
 ("y3_K", r"\begin{aligned}K_{11}&=200,\qquad K_{22}=2s_1=400,\qquad K_{55}=4s_1=800\ \mathrm{W\,^{\circ}C^{-1}}\\R_1&=37.5,\qquad R_2=75,\qquad R_5=150\ \mathrm{W}\end{aligned}"),
 ("y3_red", r"\begin{bmatrix}400&-50&-100&-100\\-50&200&-100&-50\\-100&-100&800&-100\\-100&-50&-100&400\end{bmatrix}\begin{Bmatrix}T_2\\T_3\\T_5\\T_6\end{Bmatrix}=\begin{Bmatrix}75\\37.5\\150\\75\end{Bmatrix}"),
 ("y3_sym", r"\begin{aligned}T_6=T_2:\qquad 300T_2-50T_3-100T_5&=75\\-100T_2+200T_3-100T_5&=37.5\\-200T_2-100T_3+800T_5&=150\end{aligned}"),
 ("y3_solve", r"\begin{aligned}T_3&=0.1875+0.5T_2+0.5T_5\\275T_2-125T_5&=84.375,\qquad -250T_2+750T_5=168.75\ \Rightarrow\ T_5=0.225+\frac{T_2}{3}\\233.33\,T_2&=112.5\end{aligned}"),
 ("y3_T", r"T_2=T_6=0.4821\ ^{\circ}\mathrm{C},\qquad T_5=0.3857\ ^{\circ}\mathrm{C},\qquad T_3=0.6214\ ^{\circ}\mathrm{C}"),
 ("y3_bal", r"\begin{aligned}&\text{rows 1, 4, 7, 8, 9 of }[K]\{T\}-\{R\}:\ -100.18,\ -161.79,\ -76.07,\ -161.79,\ -100.18\ \mathrm{W}\\&\text{sum }-600\ \mathrm{W}=-Q\times\text{area}\end{aligned}"),
 ("y3_exact", r"\begin{aligned}T_2^{\mathrm{exact}}&=0.4587,\qquad T_3^{\mathrm{exact}}=0.5894,\qquad T_5^{\mathrm{exact}}=0.3623\ ^{\circ}\mathrm{C}\\&(\text{double Fourier series, confirmed by a }128\times128\text{ mesh})\end{aligned}"),
]
