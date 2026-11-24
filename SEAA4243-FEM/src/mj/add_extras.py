"""Insert web-image slides, QR-lab slides, session-map chips and the Week 13 corrections into build_w9..w14.py.
Idempotent: refuses to patch a file twice (marker comment)."""
import pathlib, re

HERE = pathlib.Path(__file__).parent
MARK = "# ==== extras: web images + QR labs ===="


def patch(week, consts, inserts, replaces=()):
    p = HERE / f"build_w{week}.py"; s = p.read_text()
    if MARK in s:
        print(f"W{week}: already patched"); return
    i = s.index('D.add("cover"'); s = s[:i] + MARK + "\n" + consts.strip() + "\n\n" + s[i:]
    for anchor, code in inserts:
        assert s.count(anchor) == 1, (week, anchor, s.count(anchor))
        k = s.index(anchor); line0 = s.rfind("\n", 0, k) + 1
        s = s[:line0] + code.strip("\n") + "\n\n" + s[line0:]
    for old, new in replaces:
        assert s.count(old) == 1, (week, old[:70], s.count(old))
        s = s.replace(old, new)
    p.write_text(s); print(f"W{week}: patched ({len(inserts)} insertions, {len(replaces)} replacements)")


# ------------------------------------------------------------------ Week 9
patch(9, '''
CHT = "/_blob/2df4ea670c559d53e9b66655a4c7f96e"; SHAPEN = "/_blob/7a67c37010a42bf8a488bcaeceaf2fc4"
TENT2D = "/_blob/4f57ba61e546d11d23d9eb6e2271dc3c"; HAT1D = "/_blob/64714eb9fe789ef11c1b805076358465"
''', [
('D.activity("act1", 1,', '''
D.content("w9-practice", "Block 1 · the same PDE in a real simulation", "A heated plate under a channel flow",
          col(webimg(CHT, "Temperature in a channel flow and in the solid plate below it, heated from its bottom face, from the preCICE flow-over-a-heated-plate tutorial", 1300, 409),
              row(callout("The solid plate obeys today’s conduction PDE (with ∂T/∂t kept; at steady state it is exactly {∂}[E]{∂}ᵀT = −q<sub>h</sub>), with T fixed on its heated bottom face.", "why", 26),
                  callout("At the interface the solid receives a temperature from the fluid code and returns a heat flux: one Dirichlet and one Neumann condition, as in Block 3.", "ok", 26), align="stretch"),
              credit("Image: preCICE tutorials, “Flow over a heated plate” (t = 10 s). Fluid by a CFD code; the solid can be FEniCS, Nutils or CalculiX (finite elements) or OpenFOAM. LGPL-3.0, github.com/precice/tutorials.")),
          notes="Use this slide to show that the PDE of today is not a textbook toy: in a coupled heat-transfer analysis the solid side is exactly our 2D conduction problem, "
                "solved by an FE code, while a CFD code solves the fluid. Ask: which boundary of the plate is Dirichlet (the heated bottom, T fixed), which is Neumann "
                "(the interface, where the solid hands a heat flux to the fluid), and which edges are insulated (the two short sides).")
'''),
('D.content("props",', '''
D.content("w9-ansys-N", "Block 4 · the same functions inside commercial code", "ANSYS’s four-node element uses these N₁ … N₄",
          two_col(webimg(SHAPEN, "Surface plots of the four bilinear shape functions N1 to N4 over the natural square from minus one to one", 560, 576),
                  col(D.card(D.h3("Same functions, new coordinates") + D.p("ξ = 2x/a − 1 and η = 2y/b − 1 map 0 ≤ x ≤ a, 0 ≤ y ≤ b onto −1 ≤ ξ, η ≤ 1, and", 27)
                             + D.p("N₁ = ¼(1 − ξ)(1 − η) = (a − x)(b − y)/ab", 30, DARK, 600) + D.p("which is the text’s (2.21). The other three follow by changing signs.", 27), pad=26, gap=10),
                      callout("Each surface is 1 at its own corner, 0 at the other three and straight along every edge: the three checks on the next slide.", "ok", 26),
                      callout("Week 12: the square lets one formula serve any four-sided element — the isoparametric idea behind PLANE182.", "why", 26),
                      credit("Image: PyMAPDL documentation, “Build a finite element model” (how a finite element works), © ANSYS, Inc., MIT licence, mapdl.docs.pyansys.com.")),
                  lw=616),
          notes="The plot comes from the PyMAPDL documentation example that builds a four-node element by hand and checks its stiffness against MAPDL. Point at N1: 1 at the corner "
                "(ξ, η) = (−1, −1), zero at the other corners, straight along every edge. Same functions as (2.21) after the change of variables on the slide.")
'''),
('D.activity("act4", 4,', '''
D.content("w9-tent", "Block 4 · from one element to the mesh", "One nodal value lifts one tent",
          row(col(webimg(HAT1D, "Two overlapping one-dimensional hat functions phi 2 and phi 3 on a mesh of five elements", 740, 281),
                  D.p("1D: φᵢ is a hat over the two elements that share node i.", 26, MUTED), extra="flex:1"),
              col(webimg(TENT2D, "A two-dimensional tent function rising to one at an interior node of a triangular mesh and zero at all other nodes", 470, 321),
                  D.p("2D: a tent over every element that shares the node (triangles here; four-node elements give curved faces).", 26, MUTED), extra="width:560px"), align="start")
          + callout("Each element that touches node i adds one face of its tent. That is why T is continuous across element edges, and why node i couples only to its neighbours: the global matrix is sparse (Week 10).", "why", 26)
          + credit("Images: H. P. Langtangen and K.-A. Mardal, <i>Introduction to Numerical Methods for Variational Problems</i> (Springer, 2019, open access); figures from github.com/hplgit/fem-book, MIT licence."),
          notes="Link the element view (four shape functions in one element) to the global view (one basis function per node, made of pieces from every element around it). "
                "This prepares assembly next week: the global row of node i has entries only for nodes in the elements around i.")
'''),
('D.divider("d5", "5",', '''
qr_lab(D, "qr-shape", 6, "Check Activity 4 on your phone, then explore",
       ["Press “Activity 4 point”. Do N₁ … N₄, their sum and T = 136.0 K match your sheet?",
        "Drag P onto node 3 and read the four weights. Which property is this?",
        "Find three points where N₁ = N₃. What line joins them?"],
       [LABS["shape"]], "6 minutes, optional in class: if the block is running late, set it as homework. Answers are inside the lab under “Check answer”.",
       notes="Before class: the lab must be shared (Share menu, anyone with the link) or students cannot open it; test the QR code with a phone that is not logged in to your account. "
             "Answers: (1) 0.175, 0.525, 0.225, 0.075; sum 1; T = 136.0 K. (2) N = (0, 0, 1, 0): the Kronecker delta property. (3) The diagonal from node 2 to node 4, x/a + y/b = 1. "
             "Extension in the lab: the 8-node N1 is negative over most of the element (−0.25 at the centre); the sum is still 1.")
'''),
], [
('("1:35", "Shape functions", 35, "A4 · 8 min", False)', '("1:35", "Shape functions", 35, "A4 + QR lab", False)'),
])

# ------------------------------------------------------------------ Week 10
patch(10, '''
ASTER = "/_blob/15e4f769f19df6cd203c646cc3013c7c"; MTHERM = "/_blob/c133309344d3f4e9f43444105100e532"
''', [
('D.activity("act6", 6,', '''
D.content("w10-practice", "Block 5 · the same steady conduction in other FE codes", "Same equations, same checks, other codes",
          row(col(webimg(ASTER, "Gmsh window showing the temperature in a solid plate computed with Code_Aster, from 302 kelvin at the top to 310 kelvin at the heated bottom", 695, 380),
                  credit("Code_Aster (open-source FE), solid plate heated from below, shown in Gmsh. preCICE tutorials, “Flow over a heated plate, steady state”, LGPL-3.0."), extra="flex:1"),
              col(webimg(MTHERM, "ANSYS MAPDL nodal temperature in a plate held at 5 and 100 degrees on two opposite faces, varying linearly between them", 665, 380),
                  credit("ANSYS MAPDL, plate with two faces at 5 and 100 °C. PyMAPDL documentation, “Basic thermal analysis”, © ANSYS, Inc., MIT licence."), extra="flex:1"), align="start")
          + row(callout("Left: the field your Week 10 script would produce for that plate — hot boundary below, cooled boundary above, contours parallel to the edges.", "why", 26),
                callout("Right: no source and two fixed faces give a linear T. Every FE code must reproduce it exactly, because the four-node element contains 1, x and y: a quick check of any new model.", "ok", 26), align="stretch"),
          notes="Two independent codes, the same equation. The MAPDL example is a useful sanity check students can repeat in Week 14: with no heat generation and two faces at fixed temperature, "
                "the solution is linear and any mesh reproduces it to machine precision (a patch test). If it does not, the model is wrong, not the mesh.")
'''),
('D.divider("d6", "6",', '''
qr_lab(D, "qr-heat", 6, "Run the text’s plate on your phone",
       ["Keep the 2 × 2 mesh: do T at the bottom-right corner and at the bottom middle match (2.55)?",
        "Run the mesh study. From which mesh is the change below 1%? Which value would you report?",
        "Make all four edges insulated. What does the lab say, and what does it mean physically?"],
       [LABS["heat"]], "6 minutes, optional in class: if the block is running late, set it as homework. The energy-balance card shows the reaction check you will use in ANSYS (Week 14).",
       notes="Share the lab (Share menu, anyone with the link) before class and test the QR code on a phone that is not logged in. "
             "Answers: (1) 0.6214 and 0.4821 °C. (2) 8 × 8 changes by −0.95%, 16 × 16 by −0.23%: report 16 × 16, 0.5898 °C (software 0.5897). "
             "(3) No temperature is fixed, so [K] is singular; physically there is no steady state because the 600 W per metre of heat generated cannot leave.")
'''),
], [
('("2:15", "Post-processing", 25, "A6 · 8 min", False)', '("2:15", "Post-processing", 25, "A6 + QR lab", False)'),
])

# ------------------------------------------------------------------ Week 11
patch(11, '''
BMESH = "/_blob/1738fb86fb9372d10dcfe1130f9b24d7"; BVM = "/_blob/9ecac5841eb0f2be0f7c0e56b12decb9"
WRENCH = "/_blob/3177144d9485bdbb2aa22376528bd537"; BEAM3D = "/_blob/1a2e8befa876b3ec7d23856cb3ddb115"
''', [
('D.content("unknowns",', '''
D.content("w11-practice", "Block 1 · plane stress in practice", "A corner bracket in ANSYS, modelled as plane stress",
          col(row(webimg(BMESH, "Two-dimensional quadrilateral mesh of an L-shaped corner bracket with two pin holes", 520, 377),
                  webimg(BVM, "Von Mises stress on the corner bracket, highest around the constrained upper-left pin hole", 560, 386), align="center"),
              callout("“Because the bracket is thin in the z direction (½-inch thickness) compared to its x and y dimensions, and because the pressure load acts only in the x–y plane, assume plane stress.” — the tutorial’s own justification, word for word the test of this slide.", "why", 26),
              credit("Images and quotation: PyMAPDL documentation, “Static analysis of a corner bracket” (adapted from the classic Ansys APDL tutorial; PLANE183 elements), © ANSYS, Inc., MIT licence.")),
          notes="Read the quotation aloud and ask which two conditions it checks: thin compared with the in-plane size, and loads in the plane. Those are exactly the plane-stress conditions. "
                "The left image is the 2D mesh (quadrilaterals, with triangles where the geometry is awkward); the right image is the von Mises stress, highest next to the welded pin hole.")

D.content("w11-2d3d", "Block 1 · when is 2D enough?", "The same physics in 3D and in 2D",
          row(col(webimg(BEAM3D, "A clamped beam drawn in three dimensions, coloured by displacement, with arrows showing it sagging under its own weight", 640, 370),
                  credit("3D: a clamped beam sagging under its own weight (FEniCS). H. P. Langtangen and A. Logg, <i>Solving PDEs in Python</i> (Springer, 2016), CC BY 4.0."), extra="flex:1"),
              col(webimg(WRENCH, "A spanner modelled in two dimensions: displacement magnitude on the left and von Mises stress on the right", 820, 360),
                  credit("2D: a spanner in plane stress, displacement and von Mises stress. SolidsPy (J. Gómez and N. Guarín-Zapata), MIT licence."), extra="flex:1"), align="start")
          + row(callout("3D: three displacements u, v, w and six stresses at every point.", "why", 26),
                callout("2D plane stress: u and v, three stresses, σ<sub>zz</sub> = 0 because both faces are free. Valid when the body is thin and the loads act in its plane.", "ok", 26), align="stretch"),
          notes="Ask the class which of the two could be modelled in 2D. The spanner: yes, thin and loaded in its plane (plane stress). The beam: a slender bar is better modelled with beam theory, "
                "or in 2D only if it is a thin plate loaded in its plane. Our cantilever plate (4 m × 2 m × 10 mm) is the spanner case.")
'''),
('D.add("break"', '''
qr_lab(D, "qr-cant-w11", 5, "Plane stress or plane strain? Predict, then check",
       ["From the two [E] matrices, predict whether the plate is stiffer in plane strain, and by roughly how much.",
        "In the Cantilever FE Lab choose 8-node, 8 × 4. Read the tip deflection in plane stress, then in plane strain.",
        "Which idealisation suits our 10 mm plate, and which would suit a long dam?"],
       [LABS["cant"]], "5 minutes, optional in class: if the block is running late, set it as homework. Next week you will compute the 2 × 2 result in the lab by hand.",
       notes="Share the lab (Share menu, anyone with the link) before class and test the QR code on a phone that is not logged in. "
             "Answers: (1) Stiffer in plane strain: the plate cannot thin, so the bending modulus rises from E to E/(1 − ν²), about 12% stiffer; deflection ratio about 1 − ν² = 0.89. "
             "(2) 8-node 8 × 4: −0.1906 m in plane stress, about −0.171 m in plane strain (ratio 0.90). (3) Plane stress for the thin plate; plane strain for a long dam or retaining wall.")
'''),
], [
('("1:00", "Hooke + strain", 25, "A3 · 6 min", False)', '("1:00", "Hooke + strain", 25, "A3 + QR lab", False)'),
])

# ------------------------------------------------------------------ Week 12
patch(12, '''
GAUSS = "/_blob/d51d6a6c475a12f4b80d98e33490dc95"; SCONV = "/_blob/b3712586b064c47459d23e55ea25ebb4"
SM12 = "/_blob/3176d1b57be5f79a3b6178f8c7721bbf"; SM192 = "/_blob/66b84852111be594c932b7446b53373f"
''', [
('D.activity("act2", 2,', '''
D.content("w12-gauss", "Block 2 · how software integrates [k]", "Software adds [B]ᵀ[E][B] at four Gauss points",
          two_col(col(webimg(GAUSS, "A four-node element with corners at (1,2), (8,0), (9,4) and (4,5) and its four Gauss points marked inside it", 640, 408),
                      credit("Image: PyMAPDL documentation, “Build a finite element model” (how a finite element works), © ANSYS, Inc., MIT licence.")),
                  col(D.card(D.h3("What the program does") + D.ul(["Evaluate [B] at ξ, η = ±1/√3 (the orange points).", "Form t [B]ᵀ[E][B] × det J at each point; weights are 1.", "Add the four: that is [k], 8 × 8."], 27, gap=8), pad=26, gap=10),
                      callout("For our rectangle the four-point sum equals the closed form (3.42) to machine precision: we checked it for the cantilever element.", "ok", 26),
                      callout("For a distorted element like this one there is no closed form, so numerical integration in ξ, η is the only route. That is why software works on the square.", "why", 26)),
                  lw=700),
          notes="The element in the image is the textbook example from Logan’s book reproduced in the PyMAPDL documentation: nodes (1,2), (8,0), (9,4), (4,5). "
                "Its four Gauss points are the images of (±1/√3, ±1/√3). For the rectangle of the text the integrand is a quadratic in each direction, so two points per direction are exact.")
'''),
('D.activity("act6", 6,', '''
D.content("w12-conv-other", "Block 5 · the same experiment in another code", "Error falls with element size, then levels off near 0.7%",
          two_col(col(webimg(SCONV, "Log-log plot of relative displacement error against element size for a four-node cantilever model; the error falls from about 25 percent and levels off near 0.7 percent", 600, 416),
                      credit("Images: SolidsPy (J. Gómez and N. Guarín-Zapata), “Convergence analysis for a cantilever beam”, MIT licence, github.com/nicoguaro/SolidsPy.")),
                  col(row(webimg(SM12, "Coarse mesh of 12 square elements", 300, 109), webimg(SM192, "Fine mesh of 192 square elements", 300, 109), align="center"),
                      callout("Coarse meshes: each halving of h cuts the error about three times. Same lesson as our Table 3.1.", "ok", 26),
                      callout("Fine meshes: the error stops near 0.7%. The FE end load is spread uniformly; the exact elasticity solution assumes a parabolic end shear. That is a modelling difference, not a mesh error — as our converged 0.191 against Timoshenko’s 0.192 m.", "why", 26)),
                  lw=660),
          notes="Same experiment, different code, same story. The plateau is the key: refining further cannot remove a difference that comes from how the load was idealised. "
                "Students should be able to say which of the two errors (mesh, idealisation) a refinement study can remove.")
'''),
('D.divider("d6", "6",', '''
qr_lab(D, "qr-cant-w12", 8, "Your hand mesh, then better meshes, on your phone",
       ["4-node, 2 × 2: does the lab give the text’s −0.131 m? How far is it from beam theory?",
        "Same eight elements, two layouts: 4 × 2 and 8 × 1, then 2 × 4. Which is stiffest, and why?",
        "Find the coarsest mesh within 2% of −0.192 m with 4-node and with 8-node elements. Compare their dofs."],
       [LABS["cant"]], "8 minutes, optional in class: if the block is running late, set it as homework. The mesh study button builds the table of Activity 6 for you.",
       notes="Share the lab (Share menu, anyone with the link) before class and test the QR code on a phone that is not logged in. "
             "Answers: (1) −0.1306 m, 32% stiffer than Timoshenko’s −0.192 m. (2) 4 × 2: −0.164; 8 × 1: −0.166; 2 × 4: −0.133. Elements long in the bending direction lock; shape matters more than count. "
             "(3) 4-node 16 × 8 (−1.7%, 306 dofs) against 8-node 4 × 2 (−1.8%, 74 dofs).")
'''),
], [
('("2:15", "Solution & checks", 25, "A6 · 8 min", False)', '("2:15", "Solution & checks", 25, "A6 + QR lab", False)'),
])

# ------------------------------------------------------------------ Week 13
patch(13, '''
HOLEVM = "/_blob/d74c86901e76d1b79cf19a46ecdcb8c2"; ITSK = "/_blob/057abd4b2e6a2d1fed8ccecf15b6f8ee"; ITSQ = "/_blob/69e45d6775b237f3c514ab78ad2ac2fe"
''', [
('D.activity("act2", 2,', '''
D.content("w13-hole", "Block 2 · a concentration is not a singularity", "A hole concentrates stress, and the peak converges",
          two_col(col(webimg(HOLEVM, "Von Mises stress in a plate with a central hole under tension, highest at the top and bottom edges of the hole", 640, 454),
                      credit("Image: PyMAPDL documentation, “MAPDL 2D plane stress concentration analysis” (PLANE183, plane stress with thickness), © ANSYS, Inc., MIT licence.")),
                  col(D.card(D.h3("The MAPDL example") + D.ul(["Steel plate 0.4 m × 0.1 m in tension, hole d/W = 0.3, 50 elements around the hole.",
                                                             "Far field 10.0 MPa; peak von Mises 33.4 MPa at the edge of the hole.",
                                                             "On the net section K<sub>t</sub> = 2.34; Peterson’s formula gives 2.35."], 27, gap=8), pad=26, gap=10),
                      callout("A smooth hole has a finite peak: refine and it converges, so it can be reported once checked — here against Peterson.", "ok", 26),
                      callout("The fixed corner has no finite peak: it grows with every refinement (previous slide). Same plots, opposite verdicts.", "warn", 26)),
                  lw=700),
          notes="The example in the PyMAPDL documentation computes the stress concentration factor of a plate with a hole using PLANE183 and compares it with Peterson’s polynomial "
                "K_t = 3 − 3.14(d/h) + 3.667(d/h)² − 1.527(d/h)³ = 2.35 for d/h = 0.3; MAPDL gives 2.34. This is the gusset-plate check for the project.")
'''),
('D.divider("d3", "3",', '''
qr_lab(D, "qr-stress", 8, "Probe the Week 13 point, then refine",
       ["4-node 2 × 2, probe (3.5, 1.3). Compare with your Activity 1 numbers.",
        "Refine to 8-node 16 × 8 and 32 × 16 at the same point. Does σ<sub>xx</sub> approach beam theory’s 225? Then probe mid-span (2.0, 1.3).",
        "Run the corner study. Does the peak σ<sub>xx</sub> at the fixed corner converge?"],
       [LABS["stress"]], "8 minutes, optional in class: if the block is running late, set it as homework. The display options are the ones you will meet in ANSYS next week.",
       notes="Share the lab (Share menu, anyone with the link) before class and test the QR code on a phone that is not logged in. "
             "Answers: (1) 315.2, −44.9, −310.9 kN/m² (full precision). (2) It settles near 150, not 225: the point is 0.5 m from the loaded edge, where the uniform end traction differs from the parabolic shear of beam theory. "
             "At mid-span FE = beam theory = 900. (3) No: 4 134 → 5 372 → 6 400 → 7 467 kN/m².")
'''),
('D.activity("act5", 5,', '''
D.content("w13-symmetry", "Block 5 · two modelling tips for the project", "Use symmetry, and do not read stresses under a point load",
          two_col(row(webimg(ITSK, "Sketch of a disk squeezed by two point loads P at the top and bottom", 210, 292),
                      webimg(ITSQ, "Quarter of the disk meshed with triangles, with roller supports on the two cut edges and displacement shown as colour", 520, 365), align="center"),
                  col(D.card(D.h3("Indirect tensile (Brazilian) test") + D.ul(["A 150 mm disk squeezed across its diameter by two loads P; plane strain.",
                                                                              "Two lines of symmetry → model one quarter: rollers on the cut edges (no displacement normal to them).",
                                                                              "The load is a point force: the stress under it is singular. Read results away from it, or spread it over the real contact width."], 26, gap=8), pad=24, gap=10),
                      credit("Images: SfePy documentation, Primer (indirect tensile test in 2D), BSD-3-Clause licence, sfepy.org.")),
                  lw=780),
          notes="Two habits that save the project marks: exploit symmetry (a quarter model is four times smaller and the cut edges get rollers), and never report the stress under a concentrated load. "
                "The SfePy primer builds this quarter model in Gmsh and applies the symmetry conditions as zero normal displacement on the cut edges.")
'''),
], [
('("0:35", "Accuracy of stresses", 25, "A2 · 6 min", False)', '("0:35", "Accuracy of stresses", 25, "A2 + QR lab", False)'),
# --- Week 13 corrections: full-precision displacements ---
('callout("[B] is the Week 12 Activity 1 result; {û⁴} comes from the text\'s solution (3.49). Local order matters: nodes (1)(2)(3)(4) of element 4 are global 5, 6, 9, 8, each with u then v.", "warn", 26)',
 'callout("[B] is the Week 12 Activity 1 result. {û⁴} is the course MATLAB solution of the text’s (3.49) to six decimals: the text prints three, which is not enough here. Local order: nodes (1)(2)(3)(4) of element 4 are global 5, 6, 9, 8, each with u then v.", "warn", 26)'),
('notes="Answers: ε_xx = 0.15(0.042) − 0.15(0.031) = 0.00165; ε_yy = −0.25(−0.043) − 0.75(−0.130) + 0.75(−0.131) + 0.25(−0.046) = −0.00150; ε_xy = −0.00395. "\n                 "σ_xx = 224.44e6 × 0.00165 + 74.07e6 × (−0.00150) = 370 − 111 = 259 kN/m²; σ_yy = 74.07e6 × 0.00165 − 224.44e6 × 0.00150 = 122 − 337 = −214; σ_xy = 75.19e6 × (−0.00395) = −297. "\n                 "Largest in magnitude: σ_xy. σ_xx is tension, correct for a point above the neutral axis of a downward-loaded cantilever (top fibre in tension).")',
 'notes="Answers with the six-decimal displacements: ε_xx = 0.15(0.041967 − 0.030966) = 0.0016501; ε_yy = −0.0007445; ε_xy = −0.0041348. "\n                 "σ_xx = 224.44 × 1.6501 − 74.07 × 0.7445 = 370.4 − 55.1 = 315.2 kN/m²; σ_yy = 74.07 × 1.6501 − 224.44 × 0.7445 = −44.9; σ_xy = 75.19 × (−4.1348) = −310.9. "\n                 "σ_xx and σ_xy are about the same size; σ_yy is small, as beam theory assumes. σ_xx is tension, correct above the neutral axis of a downward-loaded cantilever. "\n                 "Trap: with the text’s three-decimal displacements ε_yy doubles (−0.0015) and σ_yy comes out as −214: v6 and v9 differ only in the fourth decimal.")'),
('D.content("act1-reveal", "Activity 1 · solution", "Tension above the neutral axis, as a cantilever should have",',
 'D.content("act1-reveal", "Activity 1 · solution", "Tension above the neutral axis; σ<sub>yy</sub> small, as beam theory assumes",'),
('callout("σ<sub>xx</sub> > 0 above mid-height: top fibre in tension for a downward tip load. σ<sub>yy</sub> ≠ 0 and the large σ<sub>xy</sub> are 2D effects a beam formula ignores.", "why", 26)),',
 'row(callout("σ<sub>xx</sub> > 0 above mid-height: top fibre in tension. σ<sub>xy</sub> carries the end shear; σ<sub>yy</sub> is small.", "why", 26), callout("Keep six decimals: v<sub>6</sub> and v<sub>9</sub> differ in the fourth. With three decimals ε<sub>yy</sub> doubles and σ<sub>yy</sub> becomes −214.", "warn", 26), align="stretch")),'),
('notes="Beam theory predicts σ_yy = 0 and a parabolic σ_xy; a coarse Q4 mesh gives a non-zero σ_yy as a by-product of its kinematics. Next slide: compare with beam theory.")',
 'notes="Strains are differences of nodal displacements, so rounding is amplified: ε_yy comes from v6 = −0.130421 and v9 = −0.130578. The lab (QR) computes at full precision and gives 315.2, −44.9, −310.9. Next slide: compare with beam theory.")'),
], )

# replace the whole beam-compare slide (multi-line) separately
p = HERE / "build_w13.py"; s = p.read_text()
a = s.index('D.content("beam-compare",'); b = s.index('D.content("sxx",')
if "Beam theory is a valid check only away from the ends" not in s:
    new = '''D.content("beam-compare", "Block 2 · beam theory as a check", "Beam theory is a valid check only away from the ends",
          two_col(D.eqpanel("t_beam_sig", None, colw=620, maxh=260, pad="12px 20px"),
                  col(table(["Point (m)", "2 × 2 FE", "Converged FE", "Beam theory"],
                            [["(1.0, 1.5) centroid of element 3", "1 645", "2 265", "2 250"], ["(2.0, 1.3) mid-span, edge of elements 3 | 4", "857 | 185", "900", "900"],
                             ["(3.0, 1.5) centroid of element 4", "519", "730", "750"], ["(3.5, 1.3) 0.5 m from the loaded end", "315", "153", "225"]], [46, 18, 18, 18], 25),
                      D.p("σ<sub>xx</sub> in kN m⁻²; converged = 8-node 64 × 32 from the course solver.", 24, MUTED)),
                  lw=620)
          + row(callout("2 × 2 → converged is the mesh error: up to 30% at centroids, and two different values on a shared edge.", "warn", 26),
                callout("Converged FE → beam theory: 0.03% at mid-span, 32% at x = 3.5 m. Near the end the model’s uniform traction is not the parabolic shear beam theory assumes (St-Venant).", "why", 26), align="stretch"),
          notes="Two errors are mixed in the 2 × 2 numbers. The mesh error (compare the first two columns) and, near the ends, the error of the check itself (compare the last two). "
                "Beam theory is exact for a parabolic end shear; the model applies a uniform traction, and the difference decays over about one depth from the end. "
                "Use centroid values at mid-span for checks. The 857 | 185 pair is the same point seen from two elements: unaveraged stresses jump across element edges on a coarse mesh.")

'''
    s = s[:a] + new + s[b:]; p.write_text(s); print("W13: beam-compare replaced")

# ------------------------------------------------------------------ Week 14
patch(14, '''
B1 = "/_blob/d8c9226261eecf74a1614dcf0f1770f4"; B2 = "/_blob/6693c19de0443fb785f34881efa131b2"; B3 = "/_blob/454cd3868335f396bb1405ce28ff40a6"; B4 = "/_blob/0a0931aa6f1852d9164d76567d86b3cc"
H1 = "/_blob/528e57bc6fa4ebfb90d0370ba59a2af2"; H2 = "/_blob/b93768ed4fdbc4b8e1a13e1f37dd8969"; H3 = "/_blob/1e6055863eaeaddd3f3d2ab4f56cce4f"
def panel(lab, src, alt, w, h):
    return col(D.p(lab, 26, DARK, 600), webimg(src, alt, w, h, pad=10), gap=10)
''', [
('D.content("vocab",', '''
D.content("w14-mapdl", "Block 1 · the same sequence in MAPDL", "Lines, area, mesh, solve: a corner bracket in ANSYS MAPDL",
          row(panel("1 · Lines", B1, "Numbered lines that outline an L-shaped bracket", 360, 263), panel("2 · Area", B2, "The bracket as a filled area", 360, 261),
              panel("3 · Mesh (PLANE183)", B3, "Quadrilateral mesh of the bracket", 360, 261), panel("4 · Solve: von Mises", B4, "Von Mises stress on the bracket", 380, 262), align="start", gap=20)
          + callout("Workbench hides these steps behind its cells; MAPDL and its Python interface expose them as commands. Same element, same plane-stress idealisation, same Weeks 9–13 mathematics.", "why", 26)
          + credit("Images: PyMAPDL documentation, “Static analysis of a corner bracket” (adapted from the classic Ansys APDL tutorial), © ANSYS, Inc., MIT licence, mapdl.docs.pyansys.com."),
          notes="Optional context for students who will meet MAPDL or PyMAPDL in industry or research. The four panels are the same stages as the Workbench cells on the previous slide: geometry, mesh, solution, results.")
'''),
('D.activity("act3", 3,', '''
qr_lab(D, "qr-predict", 6, "Before you press Solve: the expected numbers on your phone",
       ["Cantilever FE Lab: 8-node 2 × 1 and 8 × 4. Write both tip deflections in your prediction column.",
        "Stress Recovery Lab: 8-node 16 × 8, Elemental mean. Probe (2.0, 1.5): what σ<sub>xx</sub> should ANSYS show there?",
        "Cantilever FE Lab, “More to try”: produce each wrong-model signature before you see it in ANSYS."],
       [LABS["cant"], LABS["stress"]], "6 minutes. ANSYS’s PLANE183 is the 8-node element; expect agreement to about 1%, not to the last digit.",
       notes="Share both labs (Share menu, anyone with the link) before class and test the QR codes on a phone that is not logged in. "
             "Answers: (1) −0.178 m and −0.1906 m. (2) About 1500 kN/m² (beam theory 1500 at mid-span, 0.5 m above the neutral axis). "
             "(3) Plane strain −10%; point force +20% at the loaded node; vertical-only support refused; thickness 1 m → deflection ÷ 100.")
'''),
('D.activity("act5", 5,', '''
D.content("w14-verify", "Block 5 · what a verified result looks like", "Predict K<sub>t</sub>, resolve the hot spot, compare: 2.34 against 2.35",
          row(panel("1 · Geometry", H1, "Outline of a long plate with a central circular hole", 500, 155), panel("2 · Mesh refined at the hole", H2, "Mesh with many small elements around the hole", 520, 146),
              panel("3 · Von Mises", H3, "Von Mises stress highest at the edge of the hole", 480, 341), align="start", gap=20)
          + row(callout("Predicted before Solve: Peterson K<sub>t</sub> = 2.35 for d/W = 0.3. Computed: 2.34. Reported with the signed difference (−0.4%).", "ok", 26),
                callout("This is the standard for your project: a hand-check number, a mesh that resolves the hot spot, and the comparison in one sentence.", "why", 26), align="stretch")
          + credit("Images: PyMAPDL documentation, “MAPDL 2D plane stress concentration analysis”, © ANSYS, Inc., MIT licence."),
          notes="Use this as the model for the project's verification paragraph. A group with a gusset plate or a wall opening can use exactly this check (Peterson's chart for a hole or a notch).")
'''),
], [
('("1:00", "Demo 2: cantilever", 35, "A3 · 10 min", False)', '("1:00", "Demo 2: cantilever", 35, "A3 + QR lab", False)'),
])
