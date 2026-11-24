import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w12"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w12" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — Plane Stress (Part 2)", "SEAA 4243 · Plane Stress — Part 2", HERE / "eqs_w12", HERE / "figs_w12", eq_rep)
D11 = Deck(ROOT, "", "", HERE / "eqs_w11", HERE / "figs_w11", {x["name"]: x for x in json.loads((HERE / "eqs_w11" / "_report.json").read_text())})
DEFL = "/_blob/40eed239f8fcab51e29f8ed62cf2aaae"; CONV = "/_blob/8970169a0142d5c27a82177663abf946"; KMAP = "/_blob/c53c1eee4ca4cee9d7659e7372bde797"

# =============================================================================
# ==== extras: web images + QR labs ====
GAUSS = "/_blob/d51d6a6c475a12f4b80d98e33490dc95"; SCONV = "/_blob/b3712586b064c47459d23e55ea25ebb4"
SM12 = "/_blob/3176d1b57be5f79a3b6178f8c7721bbf"; SM192 = "/_blob/66b84852111be594c932b7446b53373f"

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · 2L + 1T</p>'
      f'<h1 style="font-family:{SERIF};font-size:112px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">Plane Stress<br>Part 2 of 3</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">[B] = [∂]ᵀ[N], the 8 × 8 stiffness matrix [k] = t∫[B]ᵀ[E][B] dA, nodal loads, assembly with two dofs per node, and the cantilever solved by hand</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020 — §3.2.2 – §3.4</p></div>',
      notes="Plane stress part 2. Collect Assignment 4 at the start. Today repeats Heat Transfer Part 2 with bigger matrices: Galerkin and IBP give [k] = t∫[B]ᵀ[E][B] dA, then the cantilever is assembled and solved by hand "
            "(2 × 2 mesh) and checked against a fine mesh and against beam theory.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: retrieval warm-up, outcomes and the 3-hour plan")

D.activity("warmup", "0", 5, "individual · retrieval warm-up", "Three questions from the last session — on paper",
           D.card(D.h3("Write down") + D.ul(["The plane-stress PDE in matrix form and the sizes of [∂] and [E].", "The three strain components in terms of u and v.",
                                             "The dof numbers of global node 5 in the 2 × 2 cantilever mesh, and the dof list of element 1."], 30, gap=10), extra="width:1000px"),
           col(callout("Question 3 is the bookkeeping that today’s assembly runs on.", "why", 26), extra="flex:1"),
           "5 minutes. Then the outcomes.",
           notes="Answers: (1) [∂][E][∂]ᵀ{u}ᵀ = −{f}; [∂] is 2 × 3, [E] is 3 × 3. (2) ε_xx = ∂u/∂x, ε_yy = ∂v/∂y, ε_xy = ∂u/∂y + ∂v/∂x. (3) Node 5 → U9, U10; element 1 (nodes 1, 2, 5, 4) → dofs [1 2 3 4 9 10 7 8].")

outs = ["Apply Galerkin and integration by parts to the plane-stress PDE and identify [k], {q} and {b}; write [B] = [∂]ᵀ[N] and [k] = t∫[B]ᵀ[E][B] dA.",
        "Evaluate the 8 × 8 stiffness matrix of a four-node rectangular element from the closed-form entries s₁…s₁₂.",
        "Convert an edge traction into equivalent nodal loads, assemble the global system with two dofs per node and impose displacement conditions.",
        "Solve the 2 × 2 cantilever, compare with a refined mesh and with beam theory, and explain why the coarse mesh is too stiff."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("Text §3.2.2 – §3.4. Outcome 4 is the lesson the project depends on: a coarse Q4 mesh underestimates bending deflection badly.", "why"),
          notes="Four outcomes, four blocks. Outcome 4 introduces the idea that an FE answer is only as good as its mesh, which Plane Stress Part 3 and the ANSYS week develop.")

D.content("session", "Session map · 180 minutes", "Six blocks, seven short activities, one break",
          session_map([("0:00", "Weak form and [B]", 30, "A1 · 8 min", False), ("0:30", "The 8 × 8 [k]", 35, "A2 · 8 min", False), ("1:05", "Load vectors", 20, "A3 · 6 min", False),
                       ("1:25", "Break", 10, "", True), ("1:35", "Assembly & supports", 40, "A4 + A5", False), ("2:15", "Solution & checks", 25, "A6 + QR", False), ("2:40", "MATLAB & wrap-up", 20, "Exit ticket", False)])
          + row(D.card(D.h3("Bring forward") + D.ul(["Plane Stress Part 1 Activity 3: [E] = 224.44, 74.07, 75.19 (× 10⁶ N m⁻²).", "Plane Stress Part 1 Activity 4: which dofs are fixed (U<sub>1</sub>, U<sub>2</sub>, U<sub>7</sub>, U<sub>8</sub>, U<sub>13</sub>, U<sub>14</sub>).", "The Heat Transfer Part 2 MATLAB script."], 28), extra="flex:1"),
                D.card(D.h3("The running example") + D.ul(["Cantilever 4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m⁻², ν = 0.33, q<sub>y</sub> = 5 kN m⁻¹ downward on the free end.", "2 × 2 mesh: a = 2 m, b = 1 m, 18 dofs.", "Text §3.4, equations (3.44)–(3.49), Table 3.1."], 28), extra="flex:1"), align="stretch"),
          notes="Same rhythm. Block 4 is the longest; Block 5 holds the most important engineering lesson of the plane-stress sessions.")

# =============================================================================
# Block 1 — Weak form and [B]
# =============================================================================
D.divider("d1", "1", "Weak form and the matrix [B]", "Substitute {u}ᵀ = [N]{û}ᵀ, weight with [N]ᵀ, integrate by parts. The strain–displacement matrix [B] appears twice in [k]. Text §3.2.2 – §3.3.",
          "Block 1 · 0:00 – 0:30", section="Block 1: Galerkin weighted residual and integration by parts for the vector problem, and the strain–displacement matrix B",
          notes="Thirty minutes. Keep the derivation parallel to Heat Transfer Part 2, slide for slide; the class should be able to predict each step.")

D.content("galerkin", "Block 1 · Galerkin and IBP, vector version · text (3.31)–(3.38)", "Eight unknowns per element, eight weighted equations, one boundary term",
          col(row(D.eqpanel("r_subst", "(3.31)", colw=700, maxh=80), D.eqpanel("r_weighted", "(3.32)", colw=936, maxh=120), align="stretch"),
              D.eqpanel("r_rearr", "(3.34)–(3.38)", colw=1664, maxh=220),
              row(D.eqpanel("r_sys", "(3.38)", colw=560, maxh=80), callout("[N]ᵀ is 8 × 2, so weighting gives 8 equations. Integration by parts moves one [∂] onto [N]ᵀ (left to right rule) and produces the traction boundary term {b}.", "why", 26), align="stretch")),
          notes="The structure is identical to (2.35)–(2.42). The boundary term is the traction vector {b} = {b_x b_y} integrated against [N]ᵀ along the edge: exactly the natural condition of Plane Stress Part 1.")

D.content("B", "Block 1 · the strain–displacement matrix [B] · text §3.3", "[B] = [∂]ᵀ[N]: strains from the nodal displacements",
          col(D.eqpanel("r_B_def", "", colw=1664, maxh=70, pad="12px 32px"), D.eqpanel("r_B", "", colw=1664, maxh=360, pad="12px 32px"),
              row(callout("Row 1: ∂N<sub>i</sub>/∂x under each u<sub>i</sub>. Row 2: ∂N<sub>i</sub>/∂y under each v<sub>i</sub>. Row 3: ∂N<sub>i</sub>/∂y under u<sub>i</sub>, ∂N<sub>i</sub>/∂x under v<sub>i</sub>.", "why", 24),
                  callout("Each entry is a Heat Transfer Part 1 derivative: ∂N<sub>1</sub>/∂x = −(b − y)/ab = (y − b)/ab, and so on. Nothing new is computed.", "ok", 24), align="stretch")),
          notes="This is the matrix in the course notes’ figure ({σ}ᵀ = [E][B]{u}ᵀ). Derive the first column aloud: ∂N_1/∂x = (y − b)/ab in row 1, zero in row 2, ∂N_1/∂y = (x − a)/ab in row 3. "
                "Then the same for column 2 (v_1): zero, (x − a)/ab, (y − b)/ab.")

D.content("kB", "Block 1 · the stiffness matrix in [B] form", "The same [B] twice, with [E] between them, integrated over the element and multiplied by the thickness",
          col(D.eqpanel("r_kB", "", colw=1664, maxh=130),
              row(D.card(D.h3("Why the thickness appears") + D.p("The integrals of (3.35) are per unit thickness; the physical element has thickness t, so every entry of [k] and every load is multiplied by t. The text keeps t inside s<sub>1</sub>…s<sub>12</sub>.", 28), extra="flex:1"),
                  D.card(D.h3("Why it is symmetric") + D.p("[B]ᵀ[E][B] is symmetric whenever [E] is. Integration preserves symmetry. The 8 × 8 matrix therefore has at most 36 distinct entries — and by the rectangle’s symmetry only 12.", 28), extra="flex:1"),
                  D.card(D.h3("What is being computed") + D.p("k<sub>ij</sub> = force at dof i per unit displacement of dof j, all others held. It is the virtual-work pairing of the strain patterns of dofs i and j through Hooke’s law.", 28), extra="flex:1"), align="stretch")),
          notes="Students who have met stiffness influence coefficients in structural analysis should hear that k_ij has the same meaning. The 12 distinct values come next.")

D.activity("act1", 1, 8, "pairs · derivation", "Build [B] at a point and check it",
           D.card(D.h3("Do") + D.ul(["a = 2 m, b = 1 m, point (1.5, 0.3) — the Heat Transfer Part 1 point. Write ∂N<sub>i</sub>/∂x and ∂N<sub>i</sub>/∂y for i = 1…4 (you have them: −0.35, 0.35, 0.15, −0.15 and −0.25, −0.75, 0.75, 0.25).",
                                     "Fill the 3 × 8 matrix [B] with these numbers.", "Check: the sum of each row is zero. Why must it be?"], 30, gap=10), extra="width:1000px"),
           col(D.eqpanel("r_B", "", colw=616, maxh=200, bg=WHITE, pad="10px 16px"), callout("Row sums zero: a rigid translation (all u<sub>i</sub> equal, all v<sub>i</sub> equal) produces no strain.", "ok", 26), extra="flex:1"),
           "8 minutes. Keep the sheet: Plane Stress Part 3 multiplies this [B] by the nodal displacements.",
           notes="Answer: row 1 = [−0.35 0 0.35 0 0.15 0 −0.15 0]; row 2 = [0 −0.25 0 −0.75 0 0.75 0 0.25]; row 3 = [−0.25 −0.35 −0.75 0.35 0.75 0.15 0.25 −0.15]. "
                 "Row sums: 0, 0, 0 (in row 3 the u-entries sum to zero and the v-entries sum to zero separately). Physical reason: rigid-body translation gives zero strain; this is the plane-stress analogue of [k]{1} = 0.")

# =============================================================================
# Block 2 — the 8x8 [k]
# =============================================================================
D.divider("d2", "2", "The 8 × 8 stiffness matrix", "k₃₄ in three steps, then the pattern of twelve closed-form values, then the numbers for the cantilever element. Text (3.39)–(3.44).",
          "Block 2 · 0:30 – 1:05", section="Block 2: the k34 derivation in three steps, the twelve closed-form entries and the numerical stiffness matrix of the cantilever element",
          notes="Thirty-five minutes. The derivation of one entry is shown in full; the other eleven are read from the text and evaluated numerically in the activity.")

D.content("k34-1", "Block 2 · k₃₄, step 1 · text (3.39)", "Row 3 of [N]ᵀ[∂] (dof u₂) times [E]",
          col(D.eqpanel("r_s1", "(3.39)", colw=1664, maxh=470, pad="16px 32px"),
              callout("Row 3 of the 8 × 3 matrix [N]ᵀ[∂] belongs to u<sub>2</sub>: the derivatives of N<sub>2</sub> sit in columns 1 and 3 (ε<sub>xx</sub> and ε<sub>xy</sub>). Multiplying by [E] attaches a material constant to each.", "why", 26)),
          notes="Compare with Heat Transfer Part 2 Steps 1–2: there the row was {∂N_3/∂x ∂N_3/∂y} times a 2 × 2 [E]; here it is a 1 × 3 row times a 3 × 3 [E]. The zero in the middle is the v-column: u_2 does not produce ε_yy.")

D.content("k34-2", "Block 2 · k₃₄, step 2 · text (3.40)", "Times column 4 of [∂]ᵀ[N] (dof v₂): two products survive",
          col(D.eqpanel("r_s2", "(3.40)", colw=1664, maxh=490, pad="16px 32px"),
              callout("Column 4 belongs to v<sub>2</sub>: ∂N<sub>2</sub>/∂y in row 2 and ∂N<sub>2</sub>/∂x in row 3, zero in row 1. The first product vanishes; the ν-term and the shear term remain.", "why", 26)),
          notes="k_34 couples u_2 and v_2 at the same node: a horizontal displacement of node 2 produces a vertical force there through Poisson’s ratio and through shear. That is why the entry carries both ν and (1 − ν)/2.")

D.content("k34-3", "Block 2 · k₃₄, step 3 · text (3.41)", "Integrate over the rectangle and multiply by t",
          col(D.eqpanel("r_s3", "(3.41)", colw=1664, maxh=130), D.eqpanel("r_s3b", "", colw=1664, maxh=300, pad="16px 32px"),
              callout("Independent of a and b: the coupling between u and v at a node does not depend on the element’s proportions. Entries on the diagonal do (next slide).", "ok", 26)),
          notes="The integral of −x(b − y)/(a²b²) over the rectangle is −(a²/2)(b²/2)/(a²b²) = −1/4. Then ν + (1 − ν)/2 = (1 + ν)/2 and (1 + ν)/(1 − ν²) = 1/(1 − ν). The text writes the result as E t/(8(ν − 1)).")

D.content("k-pattern", "Block 2 · the whole matrix · text (3.42)", "Twelve distinct values arranged by the symmetry of the rectangle",
          two_col(D.eqpanel("r_kfull", "(3.42)", colw=1100, maxh=600, pad="14px 24px"),
                  col(D.card(D.h3("Read the pattern") + D.ul(["Rows 1, 3, 5, 7 belong to u<sub>1</sub>…u<sub>4</sub>; rows 2, 4, 6, 8 to v<sub>1</sub>…v<sub>4</sub>.", "k<sub>34</sub> = s<sub>6</sub>: the entry just derived.", "Symmetric: s<sub>2</sub> at (1,2) and (2,1), and so on.", "Each s pairs the x- and y-derivatives of two shape functions through one entry of [E]."], 28, gap=8)),
                      callout("You do not memorise this; you read it correctly from the text. The twelve formulas follow.", "why", 24)),
                  lw=1100),
          notes="Read the pattern: rows 1, 3, 5, 7 (the u-dofs) and rows 2, 4, 6, 8 (the v-dofs) have the same structure with s_1…s_8 and s_9…s_12. Students do not need to memorise the pattern; they need to be able to read it correctly from the text in an open-book exam.")

D.content("k-vals-a", "Block 2 · the first six values · text (3.42)", "s₁ … s₆: diagonal and nearest-neighbour entries",
          col(D.eqpanel("r_svals_a", "", colw=1664, maxh=400, pad="12px 32px"),
              row(callout("k<sub>34</sub> = s<sub>6</sub> = −E t(1 + ν)/(8(1 − ν²)) — compare with step 3.", "ok", 26),
                  callout("s<sub>1</sub> depends on a/b: a long, thin element is stiffer against u-displacement along its length than across it.", "why", 26), align="stretch")),
          notes="s_1 and s_9 are the two diagonal values (u-dof and v-dof); the others are couplings. Note the common factor E t/(1 − ν²), which the activity evaluates first.")

D.content("k-vals", "Block 2 · the remaining six values · text (3.42)", "s₇ … s₁₂, and the row-sum check",
          col(D.eqpanel("r_svals_b", "", colw=1664, maxh=400, pad="12px 32px"),
              row(callout("Rigid translation in x (all u<sub>i</sub> = 1, all v<sub>i</sub> = 0) gives zero force, so the u-entries of every row sum to zero: s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub> + s<sub>7</sub> = 0.", "ok", 26),
                  callout("[k] has three zero-energy modes (two translations, one rotation): singular until the supports prevent them.", "warn", 26), align="stretch")),
          notes="Check s_1 + s_3 + s_5 + s_7 = Et/((1−ν²)ab) × [((1−ν)a² + 2b²)/6 + ((1−ν)a² − 4b²)/12 − ((1−ν)a² + 2b²)/12 − ((1−ν)a² − b²)/6] = 0. Students can verify with the numbers in the next activity.")

D.content("w12-gauss", "Block 2 · how software integrates [k]", "Software adds [B]ᵀ[E][B] at four Gauss points",
          two_col(col(webimg(GAUSS, "A four-node element with corners at (1,2), (8,0), (9,4) and (4,5) and its four Gauss points marked inside it", 640, 408),
                      credit("Image: PyMAPDL documentation, “Build a finite element model” (how a finite element works), © ANSYS, Inc., MIT licence.")),
                  col(D.card(D.h3("What the program does") + D.ul(["Evaluate [B] at ξ, η = ±1/√3 (the orange points).", "Form t [B]ᵀ[E][B] × det J at each point; weights are 1.", "Add the four: that is [k], 8 × 8."], 27, gap=8), pad=26, gap=10),
                      callout("For our rectangle the four-point sum equals the closed form (3.42) to machine precision: we checked it for the cantilever element.", "ok", 26),
                      callout("For a distorted element like this one there is no closed form, so numerical integration in ξ, η is the only route. That is why software works on the square.", "why", 26)),
                  lw=700),
          notes="The element in the image is the textbook example from Logan’s book reproduced in the PyMAPDL documentation: nodes (1,2), (8,0), (9,4), (4,5). "
                "Its four Gauss points are the images of (±1/√3, ±1/√3). For the rectangle of the text the integrand is a quadratic in each direction, so two points per direction are exact.")

D.activity("act2", 2, 8, "pairs · calculation", "Evaluate s₁, s₂, s₃ for the cantilever element and check against the text",
           D.card(D.h3("Given") + D.ul(["a = 2 m, b = 1 m, t = 0.01 m, E = 200 × 10⁶ N m⁻², ν = 0.33 (so 1 − ν² = 0.8911).", "s<sub>1</sub>, s<sub>2</sub>, s<sub>3</sub> from the formulas on the previous slides."], 30, gap=8)
                  + D.h3("Find") + D.ul(["E t/(1 − ν²), then s<sub>1</sub>, s<sub>2</sub>, s<sub>3</sub> in N m⁻¹.", "Compare with row 1 of the text’s (3.44): 0.875, 0.373, −0.123 (× 10⁶).", "If time: s<sub>5</sub> and s<sub>7</sub>, and check s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub> + s<sub>7</sub> = 0."], 30, gap=8), extra="width:1000px"),
           col(D.eqpanel("r_svals_a", "", colw=616, maxh=240, bg=WHITE, pad="10px 16px"), callout("Units: N m⁻² × m = N m⁻¹ (force per unit displacement).", "ok", 26), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: Et/(1−ν²) = 2.2444 × 10⁶; s1 = 2.2444e6 × (0.67 × 4 + 2)/(6 × 2) = 2.2444e6 × 4.68/12 = 0.8753e6; s2 = 2.2444e6 × (0.67 + 0.66)/8 = 0.3731e6; s3 = 2.2444e6 × (2.68 − 4)/24 = −0.1234e6. "
                 "s5 = −2.2444e6 × 4.68/24 = −0.4377e6; s7 = −2.2444e6 × (2.68 − 1)/12 = −0.3142e6; sum 0.8753 − 0.1234 − 0.4377 − 0.3142 = 0.0000. All match (3.44).")

D.content("act2-reveal", "Activity 2 · solution · text (3.44)", "The element stiffness matrix of the cantilever, × 10⁶ N m⁻¹",
          col(D.eqpanel("r_act2", "", colw=1664, maxh=285, pad="12px 32px"), D.eqpanel("r_k344", "(3.44)", colw=1664, maxh=315, pad="12px 32px")),
          notes="All four elements share this matrix (same a, b, material). Row 1 sum: 0.875 + 0.373 − 0.123 − 0.003 − 0.438 − 0.373 − 0.314 + 0.003 = 0.000. Note the symmetry and the ±0.003 entries (s_4 and s_8), which are tiny because (1 − ν) − 2ν = 0.01 for ν = 0.33.")

# =============================================================================
# Block 3 — Load vectors
# =============================================================================
D.divider("d3", "3", "Load vectors", "A distributed traction on an edge becomes two nodal forces; a body force becomes four. Text (3.36)–(3.37), (3.45)–(3.47).",
          "Block 3 · 1:05 – 1:25", section="Block 3: equivalent nodal loads from edge tractions and body forces, and the global load vector of the cantilever",
          notes="Twenty minutes. The half-to-each-node rule again, now in the dof ordering of plane stress.")

D.content("loads", "Block 3 · edge traction → nodal loads · text (3.37), (3.45)", "A uniform traction on edge 2–3 loads v₂ and v₃ equally",
          col(row(figbox(D.fig("fig_edge_traction", width=720)), col(D.eqpanel("r_bedge", "", colw=896, maxh=120, pad="12px 24px"), callout("Q<sub>y</sub> = −5000 N m⁻¹ (downward), b = 1 m: −2500 N at v<sub>2</sub> (dof 4) and v<sub>3</sub> (dof 6) of elements 2 and 4. Only elements with an edge on the loaded boundary get a {b}.", "why", 24)), align="center"),
              D.eqpanel("r_r2", "(3.45)", colw=1664, maxh=80, pad="12px 32px"),
              D.eqpanel("r_body", "", colw=1664, maxh=110, pad="12px 32px"), D.p("Body force, e.g. self-weight: a quarter of the element weight at each node, in the v-dofs.", 26, MUTED)),
          notes="The text gives q_y as a line load in kN/m along the edge (force per unit length of the edge for the whole thickness). Per unit area it would be q_y/t; multiplied by t in the integral it returns to q_y. "
                "Self-weight is ignored in the text’s example; the formula is shown so students can add it in the project.")

D.activity("act3", 3, 6, "pairs · bookkeeping", "Assemble the global load vector of the cantilever",
           col(figbox(D11.fig("fig_ps_mesh", width=760)), extra="width:820px"),
           D.card(D.h3("Do") + D.ul(["Which elements carry the edge traction? Which of their local dofs?", "Map those local dofs to global dofs with the node numbering (node n → U<sub>2n−1</sub>, U<sub>2n</sub>).",
                                     "Write the 18 × 1 global load vector {R}. Which entries are unknown reactions?"], 30, gap=10), extra="flex:1"),
           "6 minutes. Reveal follows, then the break.",
           notes="Answers: elements 2 (nodes 2, 3, 6, 5) and 4 (nodes 5, 6, 9, 8) have their edge 2–3 on x = 4: element 2 local v_2, v_3 → global nodes 3, 6 → U6, U12; element 4 local v_2, v_3 → nodes 6, 9 → U12, U18. "
                 "So R6 = −2500, R12 = −2500 − 2500 = −5000, R18 = −2500; all other known entries zero; the six entries at fixed dofs (1, 2, 7, 8, 13, 14) are unknown reactions B_i. Equation (3.47).")

D.content("act3-reveal", "Activity 3 · solution · text (3.47)", "Three loaded dofs, six reactions, nine zeros",
          col(D.eqpanel("r_R", "(3.47)", colw=1664, maxh=70, pad="12px 32px"),
              row(table(["Element", "Local loaded dofs", "Global nodes", "Global dofs", "Load (N)"], [["2", "v<sub>2</sub>, v<sub>3</sub> (local 4, 6)", "3, 6", "U<sub>6</sub>, U<sub>12</sub>", "−2500 each"], ["4", "v<sub>2</sub>, v<sub>3</sub> (local 4, 6)", "6, 9", "U<sub>12</sub>, U<sub>18</sub>", "−2500 each"]], [14, 30, 18, 20, 18], 27),
                  callout("Node 6 is shared by both loaded elements, so U<sub>12</sub> receives −5000: the full 5 kN m⁻¹ × 1 m of edge around it.", "why", 26), align="stretch")),
          notes="Then break: 10 minutes.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:25 – 1:35</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: assembly with two dofs per node, supports, the solution and its checks.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True), notes="Ten minutes.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Assembly and supports
# =============================================================================
D.divider("d4", "4", "Assembly and supports", "Scatter-add 8 × 8 blocks with the dof map, then delete the six fixed dofs. Text (3.46)–(3.48).",
          "Block 4 · 1:35 – 2:15", section="Block 4: the dof map, scatter-add assembly of the 18-by-18 system, imposition of the fixed-edge conditions and the reduced system",
          notes="Forty minutes with two activities. The only new thing compared with Heat Transfer Part 2 is the dof map: node → two dofs.")

D.content("dofmap", "Block 4 · the dof map", "Connectivity in node numbers becomes connectivity in dof numbers",
          col(D.eqpanel("r_dofmap", "", colw=1664, maxh=150, pad="12px 32px"),
              row(table(["Element", "Nodes (1)(2)(3)(4)", "Dofs, in local order 1…8"], [["1", "1, 2, 5, 4", "1 2 · 3 4 · 9 10 · 7 8"], ["2", "2, 3, 6, 5", "3 4 · 5 6 · 11 12 · 9 10"], ["3", "4, 5, 8, 7", "7 8 · 9 10 · 15 16 · 13 14"], ["4", "5, 6, 9, 8", "9 10 · 11 12 · 17 18 · 15 16"]], [18, 34, 48], 28),
                  col(D.eqpanel("r_scatter", "", colw=700, maxh=70, pad="12px 20px"), callout("MATLAB: K([1 2 3 4 9 10 7 8],[1 2 3 4 9 10 7 8]) += k — the text’s §3.4.1 lines.", "why", 26)), align="stretch")),
          notes="Students should write the dof lists themselves before seeing the table (Activity 4). The pattern is mechanical: for each node n in the connectivity row, write 2n − 1 and 2n.")

D.content("Kmap", "Block 4 · the assembled [K], 18 × 18 · text (3.46)", "Each entry is filled by the elements that share both its dofs",
          two_col(f'<img src="{KMAP}" alt="An 18 by 18 grid showing which element contributes to each entry of the assembled stiffness matrix; shared entries are marked with the number of contributing elements" style="width:600px;height:620px;object-fit:contain">',
                  col(D.card(D.h3("Read the map") + D.ul(["Diagonal blocks of node 5 (U<sub>9</sub>, U<sub>10</sub>) are shared by all four elements: the number 4.", "Edge nodes are shared by two elements; corner nodes by one.", "Zero where the two dofs belong to nodes that no element has in common: node 1 and node 9 never meet."], 28, gap=8)),
                      callout("Bandwidth: the non-zeros stay close to the diagonal because neighbouring nodes have nearby numbers. Numbering across the short side first keeps the band narrow — software renumbers for you.", "why", 26)),
                  lw=620),
          notes="The text prints (3.46) with dots; this map is the structure behind it. Ask: which entries of row 9 are non-zero? All of them, because node 5 touches every node of the mesh.")

D.activity("act4", 4, 8, "pairs · assembly", "Place two entries of element 2 into [K], then find the fixed dofs",
           D.card(D.h3("Do") + D.ul(["Element 2 has nodes 2, 3, 6, 5. Write its dof list in local order 1…8.", "Its local k<sub>11</sub> = 0.875 × 10⁶ and local k<sub>34</sub> = −0.373 × 10⁶. To which global entries K<sub>IJ</sub> do they go?",
                                     "Which global diagonal entries receive s<sub>1</sub> = 0.875 × 10⁶ from more than one element? Give K<sub>9,9</sub>.", "List the six fixed dofs and the size of the reduced system."], 30, gap=10), extra="width:1060px"),
           col(D.eqpanel("r_k344", "", colw=556, maxh=260, bg=WHITE, pad="8px 12px"), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: dofs [3 4 5 6 11 12 9 10]. Local k_11 → K_33 (u_2 global = U3); local k_34 → K_{5,6} (local 3 = U5, local 4 = U6). K_99 receives s_1 from elements 1, 2, 3, 4: K_99 = 4 × 0.875 = 3.5 × 10⁶ (the text’s (3.46)/(3.48) row 9 diagonal is 3.500 — consistent with the map showing ‘4’). "
                 "Fixed: U1, U2, U7, U8, U13, U14; reduced system 12 × 12.")

D.content("act4-reveal", "Activity 4 · solution · text (3.48)", "Six fixed dofs; twelve equations remain",
          col(D.eqpanel("r_fixed", "", colw=1664, maxh=150, pad="12px 32px"),
              row(table(["Local entry of element 2", "Global entry", "Value (× 10⁶)"], [["k<sub>11</sub> (u<sub>2</sub>–u<sub>2</sub>)", "K<sub>3,3</sub>", "+0.875 (plus element 1’s k<sub>33</sub> = 0.875 → 1.751)"], ["k<sub>34</sub> (u<sub>2</sub>–v<sub>2</sub> coupling)", "K<sub>5,6</sub>", "−0.373"], ["k<sub>77</sub> (u<sub>4</sub>–u<sub>4</sub>, node 5)", "K<sub>9,9</sub>", "+0.875 (× 4 elements → 3.500)"]], [40, 20, 40], 26),
                  callout("K<sub>3,3</sub> = 1.751 and K<sub>9,9</sub> = 3.500 are visible in the text’s (3.46) and (3.48): a good place to check your dof map.", "ok", 26), align="stretch")),
          notes="Then the reduced system (3.48): rows and columns 3, 4, 5, 6, 9, 10, 11, 12, 15, 16, 17, 18 of [K] and {R}. Solving by hand is not feasible; MATLAB backslash gives (3.49).")

D.content("solution", "Block 4 · the solution · text (3.49)", "Nodal displacements of the 2 × 2 mesh, in metres",
          col(table(["Node", "x-dof", "u (m)", "y-dof", "v (m)"], [["1 (fixed)", "U<sub>1</sub>", "0", "U<sub>2</sub>", "0"], ["2", "U<sub>3</sub>", "−0.031", "U<sub>4</sub>", "−0.046"], ["3 (free end, bottom)", "U<sub>5</sub>", "−0.042", "U<sub>6</sub>", "−0.131"],
                                                                  ["4 (fixed)", "U<sub>7</sub>", "0", "U<sub>8</sub>", "0"], ["5 (centre)", "U<sub>9</sub>", "0.000", "U<sub>10</sub>", "−0.043"], ["6 (free end, mid)", "U<sub>11</sub>", "0.000", "U<sub>12</sub>", "−0.130"],
                                                                  ["7 (fixed)", "U<sub>13</sub>", "0", "U<sub>14</sub>", "0"], ["8", "U<sub>15</sub>", "0.031", "U<sub>16</sub>", "−0.046"], ["9 (free end, top)", "U<sub>17</sub>", "0.042", "U<sub>18</sub>", "−0.131"]], [30, 14, 21, 14, 21], 25),
              callout("Bending signature: the bottom fibre shortens (u<sub>3</sub>, u<sub>5</sub> < 0), the top lengthens (u<sub>15</sub>, u<sub>17</sub> > 0), and mid-height u = 0.", "why", 26)),
          notes="Nine rows at 25 px is the limit for one slide; the table is the content of (3.49) rearranged by node. Activity 5 asks the class to read it physically. Also point out that v is almost the same across the depth of a section (free end: −0.131, −0.130, −0.131 m): the depth barely changes (ε_yy ≈ 0), the usual beam assumption.")

D.activity("act5", 5, 6, "pairs · interpretation", "Read the solution like a structural engineer",
           D.card(D.h3("From the table") + D.ul(["Why is U<sub>5</sub> = −U<sub>17</sub> and U<sub>6</sub> = U<sub>18</sub> exactly?", "Why is U<sub>9</sub> = U<sub>11</sub> = 0?", "The free end moves down 0.131 m. Estimate the tip deflection of the same cantilever with elementary beam theory, δ = PL³/(3EI), with P = 10 kN, L = 4 m, I = t h³/12. Compare."], 30, gap=10), extra="width:1060px"),
           col(figbox(D11.fig("fig_cantilever", width=520)), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: (1) antisymmetry of bending about the mid-height axis: the top and bottom fibres stretch and shorten equally, and both deflect the same; (2) the mid-height line is the neutral axis, no axial displacement. "
                 "(3) I = 0.01 × 8/12 = 6.667e−3 m⁴; δ = 10⁴ × 64/(3 × 2e8 × 6.667e−3) = 0.160 m (bending only). The FE mesh gives 0.131: 18% below even the bending-only value, and shear deformation would add more. The coarse mesh is too stiff.")

D.content("act5-reveal", "Activity 5 · solution", "Antisymmetric bending, a neutral axis, and a mesh that is too stiff",
          col(D.eqpanel("r_beam", "Timoshenko beam: bending + shear", colw=1664, maxh=120, pad="12px 32px"), D.eqpanel("r_beam_num", "", colw=1664, maxh=140, pad="12px 32px"),
              row(callout("Shear adds 0.032 m to the 0.160 m of bending: 17% for a beam this deep (L/h = 2). The 2 × 2 FE answer, 0.131 m, is 32% below the beam estimate.", "warn", 26),
                  callout("Both symmetries are exact properties of the discrete system, not approximations: the mesh, the loads and the supports are symmetric about y = 1 m.", "ok", 26), align="stretch")),
          notes="Block 5 explains the 32%: mesh refinement and the bending behaviour of the bilinear element. The beam estimate includes shear via the Timoshenko correction with κ = 5/6.")

# =============================================================================
# Block 5 — Solution and checks
# =============================================================================
D.divider("d5", "5", "Is the answer right? Refinement and a hand check", "Refine the mesh until the deflection stops moving, and compare with beam theory. Text Table 3.1, Fig. 3.7.",
          "Block 5 · 2:15 – 2:40", section="Block 5: mesh convergence of the tip deflection, the beam-theory check, and why the bilinear element is too stiff in bending",
          notes="Twenty-five minutes. The most important engineering lesson of the plane-stress sessions.")

D.content("deflected", "Block 5 · deflected shapes", "The hand mesh deflects two thirds as much as the converged mesh",
          two_col(f'<img src="{DEFL}" alt="Deflected shapes of the cantilever: the 2 by 2 hand mesh in maroon and a 32 by 16 converged mesh in light blue, displacements scaled four times" style="width:1000px;height:430px;object-fit:contain;border-radius:12px">',
                  col(D.card(D.h3("What the picture shows") + D.ul(["Both meshes bend; the coarse one bends less.", "The bilinear element cannot curve: each element’s edges stay straight, so bending is represented by a kink pattern.", "Straight edges force spurious shear strain under bending — the element resists with shear stiffness it should not have: <b>shear locking</b>."], 28, gap=8)),
                      callout("More elements → smaller kinks → less spurious shear. The 8-node element (Plane Stress Part 3) curves instead.", "why", 26)),
                  lw=1000, rw=616, align="start"),
          notes="Shear locking is the name; the mechanism is that a single bilinear element under pure bending develops parasitic shear strain because its edges cannot curve. Draw it on the board: a rectangle bent into a trapezoid has sheared corners.")

D.content("convergence", "Block 5 · mesh convergence · text Table 3.1", "Refine until the tip deflection stops moving; the limit agrees with beam theory",
          two_col(f'<img src="{CONV}" alt="Tip deflection against number of elements along the length, approaching 0.192 m, and relative error against element size on log-log axes" style="width:1060px;height:408px;object-fit:contain;border-radius:12px">',
                  col(table(["Mesh", "U₆ (m)", "U₁₈ (m)"], [["Q4 2 × 2", "−0.131", "−0.131"], ["Q4 16 × 16", "−0.1893", "−0.1893"], ["Q4 80 × 80", "−0.192", "−0.192"], ["Software (text)", "−0.192", "−0.192"], ["Beam theory", "—", "−0.192"]], [40, 30, 30], 26),
                      D.eqpanel("r_err", "", colw=556, maxh=110, bg=WHITE, pad="10px 16px")),
                  lw=1060, rw=556, align="start"),
          notes="Panel (a): deflection versus elements along the length on a log axis; it climbs to the beam-theory line. Panel (b): the error falls roughly in proportion to the element size (observed rate about 1.4 in this range). "
                "Table 3.1 of the text and the course’s own MATLAB runs agree to three decimals. The lesson for the project: show a table like this, and never report a single-mesh answer.")

D.content("w12-conv-other", "Block 5 · the same experiment in another code", "Error falls with element size, then levels off near 0.7%",
          two_col(col(webimg(SCONV, "Log-log plot of relative displacement error against element size for a four-node cantilever model; the error falls from about 25 percent and levels off near 0.7 percent", 600, 416),
                      credit("Images: SolidsPy (J. Gómez and N. Guarín-Zapata), “Convergence analysis for a cantilever beam”, MIT licence, github.com/nicoguaro/SolidsPy.")),
                  col(row(webimg(SM12, "Coarse mesh of 12 square elements", 300, 109), webimg(SM192, "Fine mesh of 192 square elements", 300, 109), align="center"),
                      callout("Coarse meshes: each halving of h cuts the error about three times. Same lesson as our Table 3.1.", "ok", 26),
                      callout("Fine meshes: the error stops near 0.7%. The FE end load is spread uniformly; the exact elasticity solution assumes a parabolic end shear. That is a modelling difference, not a mesh error — as our converged 0.191 against Timoshenko’s 0.192 m.", "why", 26)),
                  lw=660),
          notes="Same experiment, different code, same story. The plateau is the key: refining further cannot remove a difference that comes from how the load was idealised. "
                "Students should be able to say which of the two errors (mesh, idealisation) a refinement study can remove.")

D.activity("act6", 6, 8, "pairs · calculation", "Quantify the coarse-mesh error and decide on a mesh",
           D.card(D.h3("Do") + D.ul(["Percentage error of the 2 × 2 and the 16 × 16 tip deflections relative to the converged 0.192 m.", "If the error roughly halves when the element size halves, how many elements along the length are needed for 1%?",
                                     "A project team reports a shear-wall deflection from a single 4 × 6 mesh. What do you ask them to add?"], 30, gap=10), extra="width:1000px"),
           col(D.eqpanel("r_err", "", colw=616, maxh=110, bg=WHITE, pad="10px 16px"), callout("Use the table and the plot; no new theory needed.", "ok", 26), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: 2 × 2: −32%; 16 × 16: −1.4% (keep four figures: rounded to 0.189 it would look like −1.6%). From −1.4% at 16 elements, halving the error needs twice the elements: about 32 along the length for 1%, consistent with the 32 × 16 run (−0.7%). "
                 "Ask the team for a mesh-refinement table (at least three meshes) and, if possible, a hand or beam-theory check of one number.")

D.content("act6-reveal", "Activity 6 · solution", "Report the error, refine until it is below the tolerance, and check one number by hand",
          col(row(D.card(D.h3("Errors") + D.ul(["2 × 2: (0.131 − 0.192)/0.192 = −32%", "16 × 16: (0.1893 − 0.192)/0.192 = −1.4%", "32 × 16: (0.191 − 0.192)/0.192 = −0.7%"], 28, gap=8), extra="flex:1"),
                  D.card(D.h3("Mesh for 1%") + D.p("About 32 elements along the length (element size 0.125 m). Finer than that costs time and buys nothing a designer can use.", 28), extra="flex:1"),
                  D.card(D.h3("The project rule") + D.p("Three meshes, one table, one independent check (beam theory, equilibrium of reactions, or a textbook solution). Then — and only then — a conclusion.", 28), extra="flex:1"), align="stretch"),
              callout("Reactions check: the six reactions at the fixed edge must sum to +10 kN upward and give the moment 10 × 4 = 40 kN m. Software prints them; use them.", "ok", 26)),
          notes="The reaction check is a second independent test available in any software: global equilibrium of the model.")

# =============================================================================
# Block 6 — MATLAB and wrap-up
# =============================================================================
qr_lab(D, "qr-cant-w12", 8, "Your hand mesh, then better meshes, on your phone",
       ["4-node, 2 × 2: does the Explorer give the text’s −0.131 m? How far is it from beam theory?",
        "Same eight elements, two layouts: 4 × 2 and 8 × 1, then 2 × 4. Which is stiffest, and why?",
        "Find the coarsest mesh within 2% of −0.192 m with 4-node and with 8-node elements. Compare their dofs."],
       [LABS["cant"]], "8 minutes, optional in class: if the block is running late, set it as homework. The mesh study button builds the table of Activity 6 for you.",
       notes="The QR code opens the public copy on GitHub Pages (no login): open it once on a phone before class. "
             "Answers: (1) −0.1306 m, 32% stiffer than Timoshenko’s −0.192 m. (2) 4 × 2: −0.164; 8 × 1: −0.166; 2 × 4: −0.133. Elements long in the bending direction lock; shape matters more than count. "
             "(3) 4-node 16 × 8 (−1.7%, 306 dofs) against 8-node 4 × 2 (−1.8%, 74 dofs).")

D.divider("d6", "6", "The MATLAB script and what comes next", "Four changes turn the heat-transfer script into the plane-stress script. Then the exit ticket.",
          "Block 6 · 2:40 – 3:00", section="Block 6: the plane-stress MATLAB script by diff against the heat-transfer script, exit ticket and preparation for Plane Stress Part 3",
          notes="Twenty minutes. Students compare the two scripts side by side; the structure is identical.")

code1 = ["% ---- changes from the heat script ----", "E = 200e6; nu = 0.33; t = 0.01;  qy = 5000;", "Nx = 2; Ny = 2; ndof = 18;   % 2 dofs per node", "a = Lx/Nx; b = Ly/Ny;", "",
         "% 12 closed-form values, text (3.42)", "s1 =  (E*t*((1-nu)*a^2 + 2*b^2))/(6*(1-nu^2)*a*b);", "s2 =  (E*t*((1-nu) + 2*nu))/(8*(1-nu^2));", "s3 =  (E*t*((1-nu)*a^2 - 4*b^2))/(12*(1-nu^2)*a*b);", "% ... s4 to s12 likewise ...",
         "k = [s1 s2 s3 s4 s5 s6 s7 s8; ...];   % 8 x 8, (3.42)"]
code2 = ["% assembly with the dof map (node n -> 2n-1, 2n)", "K = zeros(ndof); F = zeros(ndof,1);", "d1 = [1 2 3 4 9 10 7 8];      K(d1,d1) = K(d1,d1) + k;", "d2 = [3 4 5 6 11 12 9 10];    K(d2,d2) = K(d2,d2) + k;",
         "d3 = [7 8 9 10 15 16 13 14];  K(d3,d3) = K(d3,d3) + k;", "d4 = [9 10 11 12 17 18 15 16]; K(d4,d4) = K(d4,d4) + k;", "",
         "% edge traction -> nodal loads, text (3.47)", "F([6 12 18]) = [-2500 -5000 -2500];", "% fixed edge, then solve", "dof_k = [1 2 7 8 13 14];", "dof_u = setdiff(1:ndof, dof_k);", "U = zeros(ndof,1);", "U(dof_u) = K(dof_u,dof_u) \\ F(dof_u);"]
D.content("matlab", "Block 6 · the script, as a diff against Heat Transfer Part 2", "Four changes turn the heat-transfer script into the plane-stress script",
          two_col(D.code(code1, 22), D.code(code2, 22), align="start")
          + D.p("Run it: U(dof_u) reproduces (3.49). Text §3.4.1 is the full listing; §3.4.2 is the 8-node version with 16 × 16 blocks.", 26, MUTED),
          notes="Walk through the four differences. Homework: generalise with a connectivity matrix and a loop, then run 4 × 2, 8 × 4, 16 × 8 and reproduce the convergence table.")

D.activity("exit", 7, 5, "individual · exit ticket", "Three questions before you leave",
           D.card(D.h3("Questions") + D.ul(["What are the sizes of [B], [E] and [k] for the 4-node plane-stress element, and what does t multiply?",
                                            "An edge of length b carries a uniform traction q. What does each of its two nodes receive?",
                                            "Your 2 × 2 model gives 0.131 m and the converged answer is 0.192 m. Is the coarse model too stiff or too flexible, and why?"], 30, gap=12), extra="width:1000px"),
           col(D.eqpanel("r_kB", "", colw=616, maxh=100, bg=WHITE, pad="10px 16px"), extra="flex:1"),
           "Five minutes. Name and matric number; for feedback, not marks.",
           notes="Answers: (1) 3 × 8, 3 × 3, 8 × 8; t multiplies the area integral (every entry of [k] and the loads). (2) qb/2 each. (3) Too stiff: bilinear elements cannot curve, so they develop spurious shear under bending (shear locking); refining the mesh removes it.")

D.content("summary", "Wrap-up · what to take away and what to prepare", "Next session: stresses from displacements, the 8-node element, and the project briefing",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["[B] = [∂]ᵀ[N] (3 × 8); [k] = t∫[B]ᵀ[E][B] dA (8 × 8), symmetric, three zero-energy modes.",
                                                              "Twelve closed-form values s<sub>1</sub>…s<sub>12</sub>; for the cantilever element k<sub>11</sub> = 0.875 × 10⁶ N m⁻¹.",
                                                              "Edge traction → qb/2 at each edge node (dofs v); assembly by the dof map; six fixed dofs → 12 × 12.",
                                                              "2 × 2 mesh: tip deflection 0.131 m, 32% too stiff; converged 0.192 m = beam theory with shear."], 28, gap=10)),
                  col(D.card(D.h3("Before Plane Stress Part 3") + D.ul(["Read text §3.4 (pages 97–107) and Table 3.2 (8-node results).", "Compute [E][B] at the Heat Transfer Part 1 point with the Activity 1 [B]: Plane Stress Part 3 starts there.",
                                                            "Form project groups; bring one candidate structure (shear wall, deep beam, gusset) for the briefing."], 28, gap=10)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=940),
          notes="Close on time. Collect exit tickets.")

order = D.write("2026-10-26T16:20:00Z")
print(len(order), "slides:", order)
