SEAA 4243 Finite Element Method - Python companion code
========================================================

Steady 2D heat conduction with 4-node elements

Goes with: Heat Transfer Part 2 (Heat Conduction Explorer)

What it does
  Element matrix [k] (s1-s4), source and edge-flux loads, assembly, known temperatures by row-column elimination, heat flows at the fixed nodes, temperature and flux at any point; mesh study; contour plot.

Files
  fe_heat_q4.py

Quick start
  1. Install Python 3.8 or newer, then:  pip install numpy matplotlib
     (matplotlib is optional; without it the scripts skip the plots).
  2. Run a script:  python fe_heat_q4.py
     It reproduces the course example. Compare the printout with the
     expected output below: if they agree, your setup is right.
  3. Read the docstring at the top of each file: notation, numbering,
     units, and how to call the functions for your own problem.

For an assignment or project
  - Check your hand-assembled [K], {R} and temperatures (print res['K']).
  - Run the mesh study a project needs: change Nx, Ny and watch the value converge.
  - Change the edges dict and Q for your own plate, including a source in part of it.
  - A hand calculation is still a hand calculation: use the script to
    check your numbers and to go beyond what is practical by hand.

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

Licence
  Code: MIT licence. Use, change and share it, keeping this notice.
  Course SEAA 4243, Faculty of Civil Engineering, Universiti Teknologi Malaysia.
