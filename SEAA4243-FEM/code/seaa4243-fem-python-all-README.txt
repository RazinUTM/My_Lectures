SEAA 4243 Finite Element Method - Python companion code
========================================================

All companion code (shape functions, heat conduction, plane stress)

Files
  fe_shape_functions.py
  fe_heat_q4.py
  fe_plane_stress.py

Quick start
  1. Install Python 3.8 or newer, then:  pip install numpy matplotlib
     (matplotlib is optional; without it the scripts skip the plots).
  2. Run a script:  python fe_shape_functions.py
     It reproduces the course example. Compare the printout with the
     expected output below: if they agree, your setup is right.
  3. Read the docstring at the top of each file: notation, numbering,
     units, and how to call the functions for your own problem.

Expected output: python fe_shape_functions.py
----------------------------------------
  Q4 element a = 2 m, b = 1 m, point (1.5, 0.3) m
    N1..N4      = [0.175 0.525 0.225 0.075]   (expected 0.175 0.525 0.225 0.075)
    sum N_i     = 1.0
    T           = 136.0 K  (expected 136.0)
    dN/dx       = [-0.35  0.35  0.15 -0.15]   (expected -0.35 0.35 0.15 -0.15)
    gradient    = [20. 20.] K/m  (expected 20 20)
    flux, k = 2 = [-40. -40.] W/m2 (expected -40 -40)
    checks (Kronecker, partition of unity): (True, True)
  
  Q8 element at the centre: N1..N8 = [-0.25 -0.25 -0.25 -0.25  0.5   0.5   0.5   0.5 ]
    corner functions are -0.25 there; sum = 1.0
    checks (Kronecker, partition of unity): (True, True)
  saved shape_functions_q4.png
  saved shape_functions_q8.png

Expected output: python fe_heat_q4.py
----------------------------------------
  Text Sec. 2.3, 2 x 2 mesh
    element s1..s4 = [ 200.  -50. -100.  -50.]  (expected 200 -50 -100 -50)
    [K] =
  [[ 200.  -50.    0.  -50. -100.    0.    0.    0.    0.]
   [ -50.  400.  -50. -100. -100. -100.    0.    0.    0.]
   [   0.  -50.  200.    0. -100.  -50.    0.    0.    0.]
   [ -50. -100.    0.  400. -100.    0.  -50. -100.    0.]
   [-100. -100. -100. -100.  800. -100. -100. -100. -100.]
   [   0. -100.  -50.    0. -100.  400.    0. -100.  -50.]
   [   0.    0.    0.  -50. -100.    0.  200.  -50.    0.]
   [   0.    0.    0. -100. -100. -100.  -50.  400.  -50.]
   [   0.    0.    0.    0. -100.  -50.    0.  -50.  200.]]
    {R} = [ 37.5  75.   37.5  75.  150.   75.   37.5  75.   37.5]
    T2 = T6 = 0.4821, T3 = 0.6214, T5 = 0.3857 degC  (text (2.55): 0.4821, 0.6214, 0.3857)
    heat at fixed nodes [1, 4, 7, 8, 9] = [-100.18 -161.79  -76.07 -161.79 -100.18] W
    energy balance: generated 600.0 W, removed 600.0 W
    T(0.3, 0.2) = 0.2661 degC in element 1  (Activity 6: 0.266)
    flux at the centroid of element 2 = (-70.7, 70.7) W/m2  (-70.5, +70.5)
  
  Mesh study, T at the corner (1, 0); exact 0.5894 degC
     1 x 1   T = 0.7500
     2 x 2   T = 0.6214  change -20.69 %
     4 x 4   T = 0.5968  change -4.13 %
     8 x 8   T = 0.5912  change -0.95 %
    16 x 16  T = 0.5898  change -0.23 %
    32 x 32  T = 0.5895  change -0.06 %
  
  Plate with an inward flux, 2 x 2 mesh
    T5 = 455.56 K, T6 = 511.11 K  (expected 455.56, 511.11)
    heat at nodes 1, 4, 7 = [ -62.5 -125.   -62.5] W; flux in = 250.0 W
  saved temperature_16x16.png

Expected output: python fe_plane_stress.py
----------------------------------------
  Text cantilever, 4-node 2 x 2 mesh, (3.44)-(3.49) (nodes 1-3 along the bottom)
    node 1: u = +0.000000  v = +0.000000 m
    node 2: u = -0.030966  v = -0.045520 m
    node 3: u = -0.041967  v = -0.130578 m
    node 4: u = +0.000000  v = +0.000000 m
    node 5: u = +0.000000  v = -0.043013 m
    node 6: u = +0.000000  v = -0.130421 m
    node 7: u = +0.000000  v = +0.000000 m
    node 8: u = +0.030966  v = -0.045520 m
    node 9: u = +0.041967  v = -0.130578 m
    tip deflection = -0.1306 m  (text: -0.131)
    reactions: Rx = -0.0 N, Ry = 10000.0 N, M = 40000.0 N m  (10 kN up, 40 kN m)
    stress at (3.5, 1.3) = [ 315.2  -44.9 -310.9] kN/m2  (315.2, -44.9, -310.9)
    principal 494.4, -224.1 kN/m2 at -30.0 deg; von Mises 636.8  (494.4, -224.1; 636.8)
  
  Convergence of the tip deflection; Timoshenko beam 0.160 + 0.032 = 0.192 m
    4-node  2 x 1  dofs    12  tip -0.1267 m
    4-node  2 x 2  dofs    18  tip -0.1306 m
    4-node  4 x 2  dofs    30  tip -0.1643 m
    4-node  8 x 4  dofs    90  tip -0.1824 m
    4-node 16 x 8  dofs   306  tip -0.1886 m
    4-node 32 x 16 dofs  1122  tip -0.1906 m
    8-node  2 x 1  dofs    26  tip -0.1780 m
    8-node  4 x 2  dofs    74  tip -0.1885 m
    8-node  8 x 4  dofs   242  tip -0.1906 m
    8-node 16 x 8  dofs   866  tip -0.1913 m
  
  8-node 16 x 8: sxx(2.0, 1.3) = 900.4 kN/m2 (beam theory 900); sxx(3.5, 1.3) = 143.3 (beam 225: end effect, St-Venant)
  
  Fixed corner: sxx at the centroid of the top-left element grows with every refinement (a singularity)
    4-node 8 x 4: 4134 kN/m2
    4-node 16 x 8: 5372 kN/m2
    4-node 32 x 16: 6400 kN/m2
  saved von_mises_q8_16x8.png

Licence
  Code: MIT licence. Use, change and share it, keeping this notice.
  Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
