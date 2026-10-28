SEAA 4243 Finite Element Method - Python companion code
========================================================

Plane stress and plane strain with 4-node and 8-node elements

Goes with: Plane Stress Parts 1-3 (Cantilever Explorer, Stress Recovery Explorer)

What it does
  [E], [B] and [k] by Gauss quadrature, consistent edge loads, the cantilever solve with reactions, stresses at any point, principal stresses, von Mises, averaged and unaveraged nodal stresses; Timoshenko beam check; contour plot.

Files
  fe_plane_stress.py

Quick start
  1. Install Python 3.8 or newer, then:  pip install numpy matplotlib
     (matplotlib is optional; without it the scripts skip the plots).
  2. Run a script:  python fe_plane_stress.py
     It reproduces the course example. Compare the printout with the
     expected output below: if they agree, your setup is right.
  3. Read the docstring at the top of each file: notation, numbering,
     units, and how to call the functions for your own problem.

For an assignment or project
  - Check the 2 x 2 cantilever of the text step by step (K, U, reactions, stresses).
  - Run the 4-node versus 8-node convergence study against beam theory.
  - Show why the stress at a fixed corner keeps growing with refinement.
  - A hand calculation is still a hand calculation: use the script to
    check your numbers and to go beyond what is practical by hand.

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
