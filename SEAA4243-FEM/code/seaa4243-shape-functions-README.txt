SEAA 4243 Finite Element Method - Python companion code
========================================================

Shape functions of the 4-node and 8-node rectangles

Goes with: Heat Transfer Part 1 (Shape Function Explorer)

What it does
  N_i at a point, the two checks (Kronecker delta, partition of unity), interpolation of a nodal field, gradient and heat flux; maps of N_i.

Files
  fe_shape_functions.py

Quick start
  1. Install Python 3.8 or newer, then:  pip install numpy matplotlib
     (matplotlib is optional; without it the scripts skip the plots).
  2. Run a script:  python fe_shape_functions.py
     It reproduces the course example. Compare the printout with the
     expected output below: if they agree, your setup is right.
  3. Read the docstring at the top of each file: notation, numbering,
     units, and how to call the functions for your own problem.

For an assignment or project
  - Check N_i, T(x, y) and the flux at any point of an assignment element.
  - Plot the Q4 and Q8 shape functions for a report (plot_shape_functions).
  - A hand calculation is still a hand calculation: use the script to
    check your numbers and to go beyond what is practical by hand.

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

Licence
  Code: MIT licence. Use, change and share it, keeping this notice.
  Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
