import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w10"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w10" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — 2D Heat Transfer (Part 2)", "SEAA 4243 · 2D Heat Transfer — Part 2", HERE / "eqs_w10", HERE / "figs_w10", eq_rep)
D9 = Deck(ROOT, "", "", HERE / "eqs_w9", HERE / "figs_w9", {x["name"]: x for x in json.loads((HERE / "eqs_w9" / "_report.json").read_text())})
CONT = "/_blob/6e1ee3c16c5de7069f57f4c18dfb0b58"

# =============================================================================
# ==== extras: web images + QR labs ====
ASTER = "/_blob/15e4f769f19df6cd203c646cc3013c7c"; MTHERM = "/_blob/c133309344d3f4e9f43444105100e532"

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · 2L + 1T</p>'
      f'<h1 style="font-family:{SERIF};font-size:112px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">2D Heat Transfer<br>Part 2 of 2</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">From the weak form to the solution: [k], assembly, Dirichlet conditions, post-processing and the MATLAB code</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020 — §2.2.2 – §2.4</p></div>',
      notes="Part 2 of heat transfer. Last session: PDE, boundary conditions, shape functions, gradient. Today we finish the pipeline: Galerkin, integration by parts, the element matrices, "
            "assembly, Dirichlet conditions, solution, post-processing, and the MATLAB code. Assignment 4 is released at the end of the session. Start with the 5-minute retrieval warm-up.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: retrieval warm-up, outcomes and the 3-hour plan")

D.activity("warmup", "0", 5, "individual · retrieval warm-up", "Three questions from the last session — answer on paper before we start",
           D.card(D.h3("Write down") + D.ul(["The steady heat conduction PDE in matrix form, and the two matrices it contains.",
                                             "The name of the boundary condition that needs no action in FEM, and why.",
                                             "N<sub>2</sub> of the 4-node element and its value at node 3."], 30, gap=10), extra="width:1000px"),
           col(D9.eqpanel("e_T_N", "", colw=616, maxh=80, bg=WHITE), callout("No notes. Retrieval practice is the point: what you can recall is what you can use in the exam.", "why", 26), extra="flex:1"),
           "5 minutes. Then we compare with the slides.",
           notes="Answers: (1) {∂}[E]{∂}ᵀT = −q_h with {∂} = {∂/∂x ∂/∂y} and [E] = diag(k_x, k_y). (2) The insulated edge: a natural (Neumann) condition with q_b = 0, so its boundary integral vanishes. "
                 "(3) N_2 = x(b − y)/(ab); at node 3 (a, b) it is a(b − b)/(ab) = 0. Spend two minutes on answers, then the outcomes slide.")

outs = ["Apply the Galerkin weighted residual method and integration by parts to obtain [k]{T̂}ᵀ = {q} + {b} and explain what each term means.",
        "Evaluate the conductance matrix [k] and the load vectors {q} and {b} of a 4-node rectangular element in closed form.",
        "Assemble element matrices into the global system with a connectivity table and impose Dirichlet conditions by row–column elimination.",
        "Solve a small problem by hand, post-process temperature and flux at a point, and judge the result against a refined mesh."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("All four outcomes are examined by Assignment 4 (released today) and by the final exam under CLO3.", "ok"),
          notes="Four outcomes, four lecture blocks after the warm-up. Outcome 4 is the one students find hardest: converting a global point to local element coordinates.")

D.content("session", "Session map · 180 minutes", "Six blocks, seven short activities, one break",
          session_map([("0:00", "Weak form & IBP", 30, "A1 · 6 min", False), ("0:30", "Element matrices", 35, "A2 · 8 min", False), ("1:05", "Mesh & connectivity", 20, "A3 · 6 min", False),
                       ("1:25", "Break", 10, "", True), ("1:35", "Assembly & Dirichlet", 40, "A4 + A5", False), ("2:15", "Post-processing", 25, "A6 + QR", False), ("2:40", "MATLAB & Asg 4", 20, "Exit ticket", False)])
          + row(D.card(D.h3("Bring forward from the last session") + D.ul(["Your Activity 4–5 sheet: the same element, the same numbers.", "The formula sheet: N<sub>1</sub>…N<sub>4</sub> and their derivatives.", "A laptop with MATLAB for the code trace in Block 6."], 28), extra="flex:1"),
                D.card(D.h3("Today’s worked example") + D.ul(["Text §2.3: 1 m × 1 m plate, q<sub>h</sub> = 600 W m⁻³, k = 300 W m⁻¹ K⁻¹.", "Four 4-node elements by hand (2 × 2 mesh).", "Then 16 × 16 in MATLAB and a comparison with software."], 28), extra="flex:1"), align="stretch"),
          notes="Same rhythm as the last session. Block 4 is the longest because assembly and Dirichlet imposition are where Assignment 4 marks are lost; it has two activities.")

# =============================================================================
# Block 1 — Weak form
# =============================================================================
D.divider("d1", "1", "From residual to weak form", "Substitute T = {N}{T̂}ᵀ into the PDE, weight the residual with {N}ᵀ, integrate by parts. Text §2.2.2.",
          "Block 1 · 0:00 – 0:30", section="Block 1: Galerkin weighted residual, integration by parts in two dimensions, and the meaning of [k], {q} and {b}",
          notes="Thirty minutes. The logic mirrors the bar element exactly; keep saying so. The new element is Green’s theorem, the 2D form of integration by parts.")

D.content("residual", "Block 1 · substitute the approximation · text (2.34)", "Substituting the approximation leaves a residual",
          col(D.eqpanel("w_resid", "(2.34)", colw=1664, maxh=90),
              row(D.card(D.h3("Count") + D.p("Four unknowns T̂<sub>1</sub>…T̂<sub>4</sub>, but only one equation — and it holds nowhere exactly.", 30), extra="flex:1"),
                  D.card(D.h3("Idea") + D.p("Make the residual zero <i>on average</i>, weighted by each shape function: four weights, four equations.", 30), extra="flex:1"), align="stretch"),
              D.eqpanel("w_weighted", "(2.35) Galerkin: weights = shape functions", colw=1664, maxh=130),
              callout("Galerkin: the weights are the shape functions themselves, which makes [k] symmetric.", "why", 26)),
          notes="The ≠ sign is the honest statement: a bilinear field cannot satisfy a second-order PDE pointwise. Galerkin forces the weighted integral of the residual to zero for each N_i. "
                "Note the sign convention: the PDE is written as {∂}[E]{∂}ᵀT + q_h = 0, so the residual is the left-hand side.")

D.content("ibp-1d", "Block 1 · integration by parts: the 1D case you know", "Move one derivative from T onto the weight; a boundary term appears",
          col(D.eqpanel("w_ibp1d", "bar element, earlier in the course", colw=1664, maxh=130),
              row(D.card(D.h3("Purpose 1 · relax continuity") + D.p("After IBP only first derivatives of N and T appear, so a piecewise-linear (or bilinear) T is admissible. Second derivatives of a bilinear field would be zero or undefined at element edges.", 28), extra="flex:1"),
                  D.card(D.h3("Purpose 2 · expose the natural condition") + D.p("The boundary term contains k dT/dx, the flux. Where the flux is specified it becomes a load; where it is zero it vanishes; where T is specified the term is removed with the equation.", 28), extra="flex:1"), align="stretch")),
          notes="Students saw this earlier in the course for the bar. Re-derive the one line on the board. The two purposes are the same in 2D; only the boundary term changes from two end points to a line integral around the element.")

D.content("ibp-2d", "Block 1 · integration by parts in two dimensions · text (2.36)", "Green’s theorem turns the area integral of a derivative into a boundary integral",
          col(D.eqpanel("w_green", "Green’s theorem, x-direction (same for y)", colw=1664, maxh=130),
              D.eqpanel("w_ibp", "(2.36)", colw=1664, maxh=130),
              row(callout("n<sub>x</sub>, n<sub>y</sub> are the outward normal components and ds runs around the element boundary. Apply it to each row of {∂}[E]{∂}ᵀ.", "why"),
                  callout("q<sub>b</sub> = k ∂T/∂n is the boundary flux of (2.15), positive when heat <b>enters</b>. Text (2.41) writes the components with the opposite sign — use (2.15).", "warn"), align="stretch")),
          notes="Apply Green’s theorem with F = k_x ∂T/∂x and again with F = k_y ∂T/∂y; the two boundary terms combine into the normal flux k ∂T/∂n = q_b, exactly the quantity of the Neumann condition (2.15). "
                "Sign discipline: with q_b defined as inward-positive, the boundary term is +∫N q_b ds on the load side, so an inward flux adds heat, as it must. "
                "Lecturer note: the text’s (2.41) has the opposite sign to (2.15); we keep (2.15) throughout, and this also corrects the sign I gave in Heat Transfer Part 1’s Activity 3 answer: an inward flux has q_b > 0.")

D.content("terms", "Block 1 · rearrange and name the terms · text (2.37)–(2.42)", "Conductance matrix, heat-generation vector, boundary-flux vector",
          col(D.eqpanel("w_rearr", "(2.37)", colw=1664, maxh=220),
              D.eqpanel("w_qb", "(2.15)", colw=1664, maxh=110),
              row(D.eqpanel("w_sys", "(2.42)", colw=560, maxh=80),
              callout("Read [k]’s integrand left to right: {N}ᵀ{∂} means the derivative acts on the weight {N}ᵀ (moved there by the IBP). {∂}ᵀ{N} is the last session’s 2 × 4 gradient matrix.", "why", 26), align="stretch")),
          notes="Three names to learn: conductance matrix [k], heat-generation vector {q}, boundary-flux vector {b}; {r} is their sum. "
                "The “left to right” rule is the book’s convention: after IBP the operator acts on whatever is to its left in {N}ᵀ{∂}. Students who write {∂}{N}ᵀ get a 2 by 1 object and stall.")

D.activity("act1", 1, 6, "pairs · reasoning", "Which term, which edge? Trace the boundary term around the plate",
           col(figbox(D9.fig("fig_plate_book", width=380)), extra="width:440px"),
           D.card(D.h3("For the text’s plate (top and left at 0 °C, right and bottom insulated)") +
                  D.ul(["Which edges contribute to {b}? Write the value of q<sub>b</sub> on each.",
                        "On the two Dirichlet edges the flux is unknown — what happens to the boundary term there?",
                        "How many equations does the weighted residual give for one 4-node element, and for the 2 × 2 mesh before boundary conditions?"], 30, gap=10), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: (1) None: right and bottom are insulated (q_b = 0), so {b} = 0 for every element; the top and left edges are Dirichlet. (2) The unknown flux multiplies N_i of nodes on those edges; "
                 "when we impose T on those nodes we discard their equations, and the unknown flux disappears with them (it can be recovered afterwards as a reaction, like a support reaction). "
                 "(3) 4 equations per element; 9 for the 2 × 2 mesh with 9 nodes; after imposing T on 5 nodes, 4 remain.")

# =============================================================================
# Block 2 — Element matrices
# =============================================================================
D.divider("d2", "2", "The element matrices", "Integrate in closed form over the rectangle: k₃₄ step by step, then the whole [k], then {q} and {b}. Text (2.43)–(2.50).",
          "Block 2 · 0:30 – 1:05", section="Block 2: closed-form evaluation of the conductance matrix, the heat-generation vector and the boundary-flux vector",
          notes="Thirty-five minutes. k_34 is done slowly in five steps; the rest of [k] follows by the same recipe and by symmetry.")

D.content("k34-steps", "Block 2 · k₃₄ in four symbolic steps · text (2.43)–(2.46)", "Row 3 of {N}ᵀ, the operator, [E], the operator, column 4 of {N}",
          two_col(col(D.eqpanel("w_s1", "Step 1", colw=800, maxh=95, pad="16px 32px"), D.eqpanel("w_s2", "Step 2", colw=800, maxh=95, pad="16px 32px"), D.eqpanel("w_s3", "Step 3", colw=800, maxh=200, pad="16px 32px")),
                  col(D.eqpanel("w_s4", "Step 4", colw=816, maxh=95, pad="16px 32px"),
                      D.card(D.h3("What happened") + D.ul(["Step 1→2: the operator acts on N<sub>3</sub> to its left (IBP moved it there).", "Step 2→3: multiply by [E]; k<sub>x</sub> and k<sub>y</sub> attach to the two derivatives.",
                                                           "Step 3→4: the second operator acts to the right, on N<sub>4</sub>.", "Step 5: integrate over the rectangle (next slide)."], 28, gap=8))),
                  lw=800),
          notes="Walk through it with the two rules: left operator acts left, right operator acts right. Ask the class to write the analogous four steps for k_12 while you talk; it only changes the subscripts.")

D.content("k34-int", "Block 2 · k₃₄, step 5: the integrals · text (2.47)–(2.48)", "Two separable integrals over 0 ≤ x ≤ a, 0 ≤ y ≤ b",
          col(D.eqpanel("w_s5", "(2.47)", colw=1664, maxh=115, pad="16px 32px"), D.eqpanel("w_s5b", "", colw=1664, maxh=260, pad="16px 32px"), D.eqpanel("w_k34", "(2.48)", colw=1664, maxh=100, pad="16px 32px")),
          notes="Use the derivative table from the last session. ∫₀ᵇ y² dy = b³/3 and ∫₀ᵃ x(a − x) dx = a³/6. The result has the dimension of conductivity times thickness; with unit thickness, W/K.")

D.content("k-full", "Block 2 · the whole matrix · text (2.49)", "Four distinct values; symmetric; every row sums to zero",
          two_col(col(D.eqpanel("w_kfull", "(2.49)", colw=640, maxh=290), D.eqpanel("w_rowsum", "", colw=640, maxh=200)),
                  col(D.eqpanel("w_svals", "", colw=976, maxh=280),
                      callout("Row sums are zero because a uniform temperature produces no flux: [k]{1} = {0}. Use it as a check on every hand calculation.", "ok"),
                      callout("[k] is singular on its own (one zero eigenvalue). Only the Dirichlet conditions make the system solvable.", "warn")),
                  lw=640),
          notes="k_34 = s_2: check it against the previous slide. The zero row sum is the thermal analogue of rigid-body motion in a stiffness matrix. "
                "Symmetry comes from Galerkin (weights = shape functions) and from [E] being symmetric.")

D.content("loads", "Block 2 · the load vectors · text (2.39)–(2.40)", "Uniform generation splits equally; a uniform edge flux splits between the two edge nodes",
          col(row(D.eqpanel("w_qconst", "(2.39)", colw=700, maxh=230, pad="16px 32px"), D.eqpanel("w_bedge", "(2.40)", colw=964, maxh=230, pad="16px 32px"), align="stretch"),
              row(figbox(D.fig("fig_edge_flux", width=700)),
                  col(callout("{b} is assembled only on the elements whose edge lies on the flux boundary; interior edges never contribute.", "why"),
                      callout("Dimensions with unit thickness: q<sub>h</sub>ab/4 is W m⁻³ × m² = W per metre of thickness; q<sub>b</sub>b/2 likewise.", "ok"), extra="flex:1"), align="center")),
          notes="Along the edge x = a only N_2 and N_3 are non-zero and they reduce to the 1D linear shape functions; the integral of each over the edge is b/2. "
                "This is the same “half to each node” rule as a uniformly distributed load on a bar. For the 8-node element the split is 1/6, 2/3, 1/6 — the text’s (2.57) and the code show it.")

D.activity("act2", 2, 8, "pairs · calculation", "Evaluate [k] and {q} for the text’s element, then check the row sums",
           D.card(D.h3("Given (text §2.3)") + D.ul(["a = b = 0.5 m (2 × 2 mesh of a 1 m × 1 m plate), unit thickness.", "k<sub>x</sub> = k<sub>y</sub> = 300 W m⁻¹ K⁻¹, q<sub>h</sub> = 600 W m⁻³."], 30, gap=8)
                  + D.h3("Find") + D.ul(["s<sub>1</sub>, s<sub>2</sub>, s<sub>3</sub>, s<sub>4</sub> and hence [k].", "{q} for the element.", "Verify that each row of [k] sums to zero."], 30, gap=8), extra="width:960px"),
           col(D.eqpanel("w_svals", "", colw=656, maxh=220, bg=WHITE), callout("Units: W K⁻¹ for [k]; W for {q} (per metre of thickness).", "ok", 26), extra="flex:1"),
           "8 minutes. Early finishers: what changes in [k] if a is doubled and b kept?",
           notes="Answers: s1 = 100 + 100 = 200; s2 = −100 + 50 = −50; s3 = −50 − 50 = −100; s4 = 50 − 100 = −50. Row sum 200 − 50 − 100 − 50 = 0. "
                 "{q} = 600 × 0.5 × 0.5 / 4 = 37.5 W each. Early finishers: doubling a halves b k_x/a terms and doubles a k_y/b terms; the element conducts less in x per unit temperature difference because the path is longer.")

D.content("act2-reveal", "Activity 2 · solution · text (2.51)–(2.52)", "The same [k] and {r} for all four elements of the mesh",
          col(D.eqpanel("w_act2", "", colw=1664, maxh=190, pad="16px 32px"), row(D.eqpanel("w_k251", "(2.51)", colw=1040, maxh=250, pad="16px 32px"), D.eqpanel("w_r252", "", colw=576, maxh=250, pad="16px 24px"), align="stretch"), D.p("Right: (2.52), the heat-generation vector of every element.", 26, MUTED)),
          notes="Because the four elements are identical, one [k] and one {r} serve all. In a mesh with different element sizes you compute each; the MATLAB code does so in a loop.")

# =============================================================================
# Block 3 — Mesh and connectivity
# =============================================================================
D.divider("d3", "3", "Mesh and connectivity", "Number the global nodes, list each element’s nodes in local order, and you have the map from local to global. Text Fig. 2.6.",
          "Block 3 · 1:05 – 1:25", section="Block 3: the worked-example mesh, global numbering and the connectivity table that maps local to global degrees of freedom",
          notes="Twenty minutes, then the break. Connectivity is bookkeeping, but it is the bookkeeping that every FE program is built on.")

D.content("problem", "Block 3 · the worked example · text §2.3, Figs. 2.5–2.6", "A 1 m square plate meshed with four elements",
          two_col(col(figbox(D9.fig("fig_plate_book", width=430)), D.p("q<sub>h</sub> = 600 W m⁻³, k = 300 W m⁻¹ K⁻¹, unit thickness.", 26, MUTED)),
                  col(figbox(D.fig("fig_mesh_e1", width=410)), D.p("Four elements, nine global nodes. Element 1 shaded; its local nodes (1)…(4) sit at global nodes 1, 2, 5, 4.", 26, MUTED)),
                  lw=800, align="start")
          + callout("Heat source, two cold edges, two insulated edges. Coarse on purpose: the hand calculation must be traceable; Block 5 refines it.", "why", 26),
          notes="Predictions from the last session: hottest point at the bottom-right corner, node 3. Keep that prediction visible; we confirm it in Block 4. The numbering runs left to right, bottom to top, like the code’s loops.")

D.content("connectivity", "Block 3 · the connectivity table", "Element e, local node i → global node conn(e, i): always anticlockwise from the bottom-left",
          two_col(col(table(["Element", "(1)", "(2)", "(3)", "(4)"], [["1", "1", "2", "5", "4"], ["2", "2", "3", "6", "5"], ["3", "4", "5", "8", "7"], ["4", "5", "6", "9", "8"]], [24, 19, 19, 19, 19], 30),
                      callout("The MATLAB line K([1 2 5 4],[1 2 5 4]) = K([1 2 5 4],[1 2 5 4]) + k is this table’s first row.", "why")),
                  col(figbox(D.fig("fig_mesh_e2", width=440)), D.p("Element 2: local (1)…(4) = global 2, 3, 6, 5. Node 5 is local 4 here, local 3 in element 1: the same unknown T<sub>5</sub>.", 26)),
                  lw=1000, rw=500, align="start"),
          notes="Stress the anticlockwise start at the bottom-left corner: the [k] pattern (2.49) assumes it. A table row in the wrong order scrambles the entries, and the symptom is a result that looks plausible but is wrong.")

D.activity("act3", 3, 6, "pairs · bookkeeping", "Write the connectivity table for the Assignment 4 strip",
           col(figbox(D.fig("fig_assign", width=800)), extra="width:860px"),
           D.card(D.h3("Do") + D.ul(["List the global nodes of elements 1, 2 and 3 in local order (1)…(4).", "Mark which global nodes have a known temperature.", "How many equations remain after imposing them?"], 30, gap=10)
                  + D.p("Keep this table — you will need it for Assignment 4.", 28, DARK, 600), extra="flex:1"),
           "6 minutes, then a 10-minute break.",
           notes="Answers: element 1 → 1, 2, 6, 5; element 2 → 2, 3, 7, 6; element 3 → 3, 4, 8, 7. Known: T1 and T5 (left edge, 100 K). Remaining equations: 8 − 2 = 6. "
                 "Note the numbering here runs along the bottom (1–4) then the top (5–8), unlike the book’s 2 × 2 mesh; the recipe is the same.")

D.content("act3-reveal", "Activity 3 · solution", "Three rows, two known nodes, six unknowns",
          two_col(table(["Element", "(1)", "(2)", "(3)", "(4)"], [["1", "1", "2", "6", "5"], ["2", "2", "3", "7", "6"], ["3", "3", "4", "8", "7"]], [24, 19, 19, 19, 19], 30),
                  col(D.card(D.h3("Known and unknown") + D.ul(["Known: T<sub>1</sub> = T<sub>5</sub> = 100 K (left edge).", "Unknown: T<sub>2</sub>, T<sub>3</sub>, T<sub>4</sub>, T<sub>6</sub>, T<sub>7</sub>, T<sub>8</sub> — six equations.",
                                                              "Insulated edges: nothing to do. Heat source on element 1 only: {r¹} ≠ 0, {r²} = {r³} = 0."], 28, gap=8))),
                  lw=760),
          notes="Then break: 10 minutes.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:25 – 1:35</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: assembly, Dirichlet conditions, solution, post-processing and MATLAB.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True), notes="Ten minutes.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Assembly and Dirichlet
# =============================================================================
D.divider("d4", "4", "Assembly and Dirichlet conditions", "Scatter each [kᵉ] into [K] with the connectivity table, then remove the known temperatures. Text (2.53)–(2.55).",
          "Block 4 · 1:35 – 2:15", section="Block 4: assembly of the global system by scatter-add, imposition of Dirichlet conditions by row–column elimination, and the hand solution",
          notes="Forty minutes with two activities. Colour is used for the elements: maroon = element 1, teal = element 2, green = entries where both add.")

D.content("scatter", "Block 4 · the scatter-add rule", "Each local entry is added to the global position that the connectivity table names",
          col(D.eqpanel("w_scatter", "", colw=1664, maxh=80),
              row(D.card(D.h3("In words") + D.ul(["Start with [K] = 0 (9 × 9) and {R} = 0 (9 × 1).", "For each element: read its row of the table; add k<sub>ij</sub> to K<sub>IJ</sub> and r<sub>i</sub> to R<sub>I</sub>.",
                                                   "Shared nodes receive contributions from every element that touches them."], 28, gap=8), extra="flex:1"),
                  D.card(D.h3("Why ‘add’") + D.p("Each element’s weighted-residual equations are statements about its own area; the equation for a global node sums the statements of all elements around it — heat balance at that node.", 28), extra="flex:1"), align="stretch"),
              callout("Assembled [K] is symmetric, sparse (zeros where nodes are not connected) and still singular until Dirichlet conditions are imposed.", "ok")),
          notes="Make the analogy with truss assembly earlier in the course explicit; it is the same operation. The sparsity pattern follows the mesh: node 1 is connected only to nodes 2, 4, 5.")

D.content("asm-e1", "Block 4 · after element 1 · nodes [1 2 5 4]", "Sixteen entries land in rows and columns 1, 2, 4, 5",
          two_col(D.eqpanel("w_K_e1", "", colw=1100, maxh=600, pad="18px 32px"),
                  col(figbox(D.fig("fig_mesh_e1", width=400)), D.p("Maroon: element 1. Local (1)…(4) → global 1, 2, 5, 4: local k<sub>23</sub> = s<sub>4</sub> = −50 goes to K<sub>25</sub>; local k<sub>13</sub> = −100 goes to K<sub>15</sub>.", 26)),
                  lw=1100, rw=516, align="start"),
          notes="Do two entries aloud, then the activity assembles element 2. The rows 3, 6, 7, 8, 9 stay empty for now.")

D.activity("act4", 4, 8, "pairs · assembly", "Add element 2 (nodes [2 3 6 5]) to [K]",
           col(D.eqpanel("w_K_e1", "", colw=960, maxh=520, bg=WHITE, pad="14px 24px"), D.p("[K] after element 1 (maroon).", 26, MUTED), extra="width:960px"),
           col(D.card(D.h3("Do") + D.ul(["Write the 10 distinct entries that element 2 (nodes 2, 3, 6, 5) adds; its [k] equals element 1’s.", "Which four entries now have contributions from both elements? Give their totals.", "Check: row 2 of [K] must still sum to zero."], 28, gap=8)), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers (added by element 2): K22 +200 → 400; K33 +200; K66 +200; K55 +200 → 400; K23 −50; K26 −100; K25 −50 → −100 (with element 1’s −50); K36 −50; K35 −100; K65 −50. "
                 "Shared (both elements): K22 = 400, K55 = 400, K25 = K52 = −100. Row 2 after both: −50 + 400 − 50 − 100 − 100 − 100 = 0. Good.")

D.content("act4-reveal", "Activity 4 · solution · after elements 1 and 2", "Shared entries are sums; the rest come from one element",
          two_col(col(D.eqpanel("w_K_e12", "", colw=1100, maxh=560, pad="18px 32px"), D.p("Maroon: element 1 · teal: element 2 · green: both elements add.", 26, MUTED)),
                  col(D.card(D.h3("Totals at the shared nodes") + D.ul(["K<sub>22</sub> = 200 + 200 = 400", "K<sub>55</sub> = 200 + 200 = 400", "K<sub>25</sub> = K<sub>52</sub> = −50 − 50 = −100"], 28, gap=8)),
                      callout("Row 2: −50 + 400 − 50 − 100 − 100 − 100 = 0.", "ok")),
                  lw=1100, rw=516, align="start"),
          notes="Elements 3 and 4 follow the same way and fill rows 7–9. The complete matrix is the next slide, equation (2.53) of the text.")

D.content("K-full", "Block 4 · the complete global system · text (2.53)", "Nine equations, nine unknowns — but five temperatures are already known",
          col(D.eqpanel("w_K_full", "(2.53)", colw=1664, maxh=560, pad="16px 32px"),
              D.p("Load vector: 37.5 at corner nodes (one element), 75 at edge nodes (two elements), 150 at the centre node (four elements).", 28, MUTED)),
          notes="Point out the structure: diagonal 200/400/800 counts the elements at a node; the centre node 5 connects to all eight others. The load vector is the same count times 37.5.")

D.content("dirichlet", "Block 4 · impose the known temperatures", "Known T: delete the equation, move the value right",
          col(row(D.card(D.h3("Row–column elimination (T̄ = 0)") + D.ul(["Known: T<sub>1</sub> = T<sub>4</sub> = T<sub>7</sub> = T<sub>8</sub> = T<sub>9</sub> = 0 (top and left edges).", "Delete rows and columns 1, 4, 7, 8, 9 of [K] and rows of {R}.", "Keep rows and columns 2, 3, 5, 6: a 4 × 4 system."], 28, gap=8), extra="flex:1"),
                  D.card(D.h3("Non-zero T̄ (e.g. 100 K in Assignment 4)") + D.eqpanel("w_nonzero", "", colw=750, maxh=70, bg=PANEL, pad="12px 20px")
                         + D.p("The known column times T̄ is a known heat flow; it moves to the right-hand side before the row and column are deleted. MATLAB: F = F − K(:,dof_k)*To.", 26, MUTED), extra="flex:1"), align="stretch"),
              D.eqpanel("w_reduced", "(2.54) → (2.55)", colw=1664, maxh=280, pad="16px 32px")),
          notes="Why delete the row: the equation of a Dirichlet node contains the unknown boundary flux (reaction); we do not need it to find the temperatures. Why delete the column: the known T multiplies that column; "
                "with T̄ = 0 it contributes nothing; with T̄ ≠ 0 it is a known vector moved to the right. Solve the 4 × 4 by MATLAB backslash; by hand, Gaussian elimination takes about ten minutes.")

D.activity("act5", 5, 6, "pairs · verification", "Verify the solution and read it physically",
           D.card(D.h3("Do") + D.ul(["Substitute T<sub>2</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386, T<sub>6</sub> = 0.482 into row 1 of the reduced system (2.54). Does it give 75?",
                                     "Why is T<sub>3</sub> the largest and T<sub>5</sub> the smallest of the four?", "Why does T<sub>2</sub> equal T<sub>6</sub> exactly?"], 30, gap=10), extra="width:1000px"),
           col(figbox(D.fig("fig_mesh_T", width=560)), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: 400(0.482) − 50(0.621) − 100(0.386) − 100(0.482) = 74.95 ≈ 75 (rounding of T to 3 d.p.). T3 is the corner farthest from both cold edges, between the two insulated edges, so heat accumulates there; "
                 "T5 is the centre, closer to the cold edges than T3. T2 = T6 by the symmetry of the problem about the diagonal from node 1 to node 9 (swap x and y): the mesh, loads and boundary conditions are all symmetric.")

D.content("act5-reveal", "Activity 5 · solution", "Row 1 closes to within rounding; the pattern of the answer matches the physics",
          col(D.eqpanel("w_act5", "", colw=1664, maxh=130),
              row(D.card(D.h3("Hottest at node 3") + D.p("Farthest from the two cold edges, enclosed by the two insulated edges: the prediction from Heat Transfer Part 1 is confirmed.", 28), extra="flex:1"),
                  D.card(D.h3("T₂ = T₆") + D.p("Symmetry about the diagonal through nodes 1, 5, 9: swapping x and y maps the problem onto itself, so the solution must be symmetric too.", 28), extra="flex:1"),
                  D.card(D.h3("Use symmetry in exams") + D.p("If a problem is symmetric, equal temperatures are equal unknowns: fewer equations to solve by hand.", 28), extra="flex:1"), align="stretch")),
          notes="Symmetry is a legitimate exam-time trick: in (2.54) set T2 = T6 and the 4 × 4 reduces to 3 × 3. Mention that ANSYS users exploit symmetry by modelling half or a quarter of a structure.")

# =============================================================================
# Block 5 — Post-processing and validation
# =============================================================================
D.divider("d5", "5", "Post-processing and validation", "Temperature and flux anywhere in the plate, then the honest question: how wrong is a 2 × 2 mesh? Text Table 2.1, Fig. 2.8.",
          "Block 5 · 2:15 – 2:40", section="Block 5: interpolation at a point with local coordinates, flux recovery, mesh refinement and comparison with software",
          notes="Twenty-five minutes. Activity 6 is the Assignment 4 part (c) skill: global point → element → local coordinates → interpolate.")

D.content("interp", "Block 5 · temperature at any point: three steps", "Find the element, go local, interpolate with its own nodal values",
          two_col(col(D.step(1, "Locate the element that contains the point (from the mesh geometry).", 30),
                      D.step(2, "Local coordinates: subtract the coordinates of that element’s node 1.", 30),
                      D.eqpanel("w_local", "", colw=1000, maxh=70, pad="12px 24px"),
                      D.step(3, "Interpolate with the shape functions and the element’s four nodal temperatures, in local order.", 30),
                      D.eqpanel("w_interp", "", colw=1000, maxh=130, pad="12px 24px")),
                  col(figbox(D.fig("fig_mesh_point", width=360)), callout("Nodal values in the element’s local order (1)…(4) = its connectivity row, not global order.", "warn", 26)),
                  lw=1000, rw=516, align="start"),
          notes="The commonest Assignment error is using global coordinates in N_i. The element’s own origin is its node 1. Second commonest: listing the nodal temperatures in the wrong order.")

D.content("flux", "Block 5 · flux at a point", "Differentiate the same interpolation; the flux is constant along one direction in each element",
          col(D.eqpanel("w_fluxc", "", colw=1664, maxh=150),
              row(D.card(D.h3("Reading the sign") + D.p("At the centroid of element 2 (nodes 2, 3, 6, 5): q<sub>x</sub> < 0, heat flows towards −x, from the hot corner at node 3 towards node 2; q<sub>y</sub> > 0, towards the cold top edge.", 28), extra="flex:1"),
                  D.card(D.h3("Discontinuity") + D.p("The flux jumps across element edges because the gradient of a bilinear field is not continuous. Software averages nodal fluxes; the size of the jump is a free error indicator.", 28), extra="flex:1"), align="stretch")),
          notes="Compute it live if time allows: dN/dx at the centroid = (1/ab){−0.25, 0.25, 0.25, −0.25}·(1/1) with a = b = 0.5 gives (1/0.25)(…) — simpler: at the centroid dT/dx = (−T_2 + T_3 + T_6 − T_5)/(2a) = (−0.4821 + 0.6214 + 0.4821 − 0.3857)/1.0 = 0.2357 K/m; q_x = −300 × 0.2357 = −70.7 W/m2. Similarly dT/dy = (−T_2 − T_3 + T_6 + T_5)/(2b) = −0.2357, q_y = +70.7. Use four decimals for T: with three (0.482, 0.621, 0.386) the gradient comes out 0.235 and the flux −70.5, a rounding error in a difference of nearly equal numbers.")

D.content("validate", "Block 5 · how wrong is a 2 × 2 mesh? · text Table 2.1, Fig. 2.8", "The 2 × 2 mesh is about 5% high; 16 × 16 matches software",
          two_col(f'<img src="{CONT}" alt="Temperature contours of the plate for the 2 by 2 hand-calculation mesh and the 16 by 16 MATLAB mesh, same colour scale, hottest at the bottom-right corner" style="width:1000px;height:456px;object-fit:contain;border-radius:12px">',
                  col(table(["Mesh", "T(L/2, 0)", "T(L, 0)"], [["Q4 2 × 2 (hand)", "0.4821", "0.6214"], ["Q8 2 × 1 (hand)", "0.4448", "0.5836"], ["Q4 16 × 16", "0.4590", "0.5898"], ["Software (text)", "0.4589", "0.5897"]], [46, 27, 27], 26),
                      callout("Convergence check = the same problem on a finer mesh; refine until the answer stops moving. the ANSYS demo’s ANSYS exercise.", "ok", 24)),
                  lw=1000, rw=616, align="start")
          + D.eqpanel("w_err", "", colw=1664, maxh=120, pad="12px 32px"),
          notes="The 2 × 2 mesh overestimates by 5%; the 8-node mesh with two elements is within 3% and 1%. The contour on the left is faceted because each element is bilinear; the right is smooth. "
                "16 × 16 in MATLAB agrees with the text’s software value to the fourth decimal (0.4590 vs 0.4589). The lesson for the project: always show a mesh-refinement table.")

D.content("w10-practice", "Block 5 · the same steady conduction in other FE codes", "Same equations, same checks, other codes",
          row(col(webimg(ASTER, "Gmsh window showing the temperature in a solid plate computed with Code_Aster, from 302 kelvin at the top to 310 kelvin at the heated bottom", 695, 380),
                  credit("Code_Aster (open-source FE), solid plate heated from below, shown in Gmsh. preCICE tutorials, “Flow over a heated plate, steady state”, LGPL-3.0."), extra="flex:1"),
              col(webimg(MTHERM, "ANSYS MAPDL nodal temperature in a plate held at 5 and 100 degrees on two opposite faces, varying linearly between them", 665, 380),
                  credit("ANSYS MAPDL, plate with two faces at 5 and 100 °C. PyMAPDL documentation, “Basic thermal analysis”, © ANSYS, Inc., MIT licence."), extra="flex:1"), align="start")
          + row(callout("Left: the field your Heat Transfer Part 2 script would produce for that plate — hot boundary below, cooled boundary above, contours parallel to the edges.", "why", 26),
                callout("Right: no source and two fixed faces give a linear T. Every FE code must reproduce it exactly, because the four-node element contains 1, x and y: a quick check of any new model.", "ok", 26), align="stretch"),
          notes="Two independent codes, the same equation. The MAPDL example is a useful sanity check students can repeat in the ANSYS demo: with no heat generation and two faces at fixed temperature, "
                "the solution is linear and any mesh reproduces it to machine precision (a patch test). If it does not, the model is wrong, not the mesh.")

D.activity("act6", 6, 8, "pairs · calculation · Assignment pattern", "Interpolate the temperature at (0.3, 0.2) m in the solved plate",
           col(figbox(D.fig("fig_mesh_point", width=460)), extra="width:520px"),
           col(D.card(D.h3("Given") + D.ul(["Solution: T<sub>2</sub> = 0.482, T<sub>5</sub> = 0.386 °C; T<sub>1</sub> = T<sub>4</sub> = 0 (edge).", "Mesh: a = b = 0.5 m; element 1 has nodes [1 2 5 4]."], 28, gap=6)
                      + D.h3("Find") + D.ul(["Which element contains the point; its local coordinates.", "N<sub>1</sub>…N<sub>4</sub> at the point and their sum.", "T(0.3, 0.2)."], 28, gap=6), pad=26, gap=10),
               callout("Nodal order: {T̂¹} = {T<sub>1</sub>, T<sub>2</sub>, T<sub>5</sub>, T<sub>4</sub>}.", "warn", 26), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: element 1 (0 ≤ x ≤ 0.5, 0 ≤ y ≤ 0.5); node 1 is at (0, 0), so local = global = (0.3, 0.2). N = {0.24, 0.36, 0.24, 0.16}, sum 1. "
                 "T = 0.36 × 0.482 + 0.24 × 0.386 = 0.1735 + 0.0926 = 0.266 °C. Ask: what if the point were (0.8, 0.2)? Element 2, node 1 at (0.5, 0), local (0.3, 0.2) — same N, different nodal values {T2, T3, T6, T5}.")

D.content("act6-reveal", "Activity 6 · solution", "Element 1, local coordinates equal to global, T ≈ 0.266 °C",
          col(D.eqpanel("w_act6_N", "", colw=1664, maxh=320, pad="16px 32px"), D.eqpanel("w_act6_T", "", colw=1664, maxh=130, pad="16px 32px"),
              D.p("Same point shifted to (0.8, 0.2): element 2, local (0.3, 0.2), same N<sub>i</sub>, nodal values {T<sub>2</sub>, T<sub>3</sub>, T<sub>6</sub>, T<sub>5</sub>}.", 28, MUTED)),
          notes="Repeat the point: the shape functions depend only on local coordinates; the nodal values depend on the element.")

# =============================================================================
# Block 6 — MATLAB and Assignment 4
# =============================================================================
qr_lab(D, "qr-heat", 6, "Run the text’s plate on your phone",
       ["Keep the 2 × 2 mesh: do T at the bottom-right corner and at the bottom middle match (2.55)?",
        "Run the mesh study. From which mesh is the change below 1%? Which value would you report?",
        "Make all four edges insulated. What does the Explorer say, and what does it mean physically?"],
       [LABS["heat"]], "6 minutes, optional in class: if the block is running late, set it as homework. The energy-balance card shows the reaction check you will use in ANSYS (the ANSYS demo).",
       notes="The QR code opens the public copy on GitHub Pages (no login): open it once on a phone before class. "
             "Answers: (1) 0.6214 and 0.4821 °C. (2) 8 × 8 changes by −0.95%, 16 × 16 by −0.23%: report 16 × 16, 0.5898 °C (software 0.5897). "
             "(3) No temperature is fixed, so [K] is singular; physically there is no steady state because the 600 W per metre of heat generated cannot leave.")

D.divider("d6", "6", "The MATLAB code and Assignment 4", "Every line of the program is one of today’s steps. Then the assignment brief and the exit ticket.",
          "Block 6 · 2:40 – 3:00", section="Block 6: line-by-line trace of the text’s MATLAB script, Assignment 4 briefing, exit ticket and preparation for plane stress",
          notes="Twenty minutes. Students open the script on their laptops; you trace it against the pipeline.")

code1 = ["% ---- input (text §2.3.1) ----", "L = 1; H = 1; kx = 300; ky = 300; Q = 600;", "To = 0;            % Dirichlet value", "Nx = 2; Ny = 2; ndof = 9;", "a = L/Nx;  b = H/Ny;", "",
         "% ---- local conductance matrix: (2.49) ----", "s1 =  b*kx/(3*a) + a*ky/(3*b);", "s2 = -b*kx/(3*a) + a*ky/(6*b);", "s3 = -b*kx/(6*a) - a*ky/(6*b);", "s4 =  b*kx/(6*a) - a*ky/(3*b);",
         "k  = [s1 s2 s3 s4; s2 s1 s4 s3; s3 s4 s1 s2; s4 s3 s2 s1];", "fQ = a*b*Q/4*[1; 1; 1; 1];   % (2.39)"]
code2 = ["% ---- assembly by connectivity ----", "K = zeros(ndof); F = zeros(ndof,1);", "e1 = [1 2 5 4];  K(e1,e1) = K(e1,e1) + k;", "e2 = [2 3 6 5];  K(e2,e2) = K(e2,e2) + k;",
         "e3 = [4 5 8 7];  K(e3,e3) = K(e3,e3) + k;", "e4 = [5 6 9 8];  K(e4,e4) = K(e4,e4) + k;", "F(e1) = F(e1) + fQ;   % ... and e2, e3, e4", "",
         "% ---- Dirichlet: row-column elimination ----", "T = zeros(ndof,1);", "dof_k = [1 4 7 8 9];   T(dof_k) = To;", "F = F - K(:,dof_k)*T(dof_k);       % known -> RHS", "dof_u = setdiff(1:ndof, dof_k);", "T(dof_u) = K(dof_u,dof_u) \\ F(dof_u);  % solve"]
D.content("matlab", "Block 6 · the script, traced against the pipeline", "Left: input and [k]. Right: assembly, Dirichlet, solve",
          two_col(D.code(code1, 22), D.code(code2, 22), align="start")
          + D.p("Run it: T(dof_u) returns 0.4821, 0.6214, 0.3857, 0.4821 — equation (2.55). Change Nx = Ny = 16 and generalise the assembly loop to reproduce the 16 × 16 column of the table.", 26, MUTED),
          notes="Trace in this order: s1–s4 (Activity 2), k, fQ; the four K(...) lines (Activities 3–4); dof_k and the F update (Block 4); backslash. The 8-node script in §2.3.2 has the same structure with 8 × 8 blocks. "
                "Homework suggestion: write the loop version with a connectivity matrix conn(e,:) and the loop over e.")

D.content("assignment", "Block 6 · Assignment 4 · heat transfer · due [date]", "Three elements, a cold left edge, one heat source",
          two_col(figbox(D.fig("fig_assign", width=720)),
                  col(D.card(D.h3("Parts") + D.ul(["(a) Local load vector {r¹} for the heat source Q = 20 W m⁻² on element 1 (unit thickness).",
                                                   "(b) Global [K] in terms of k, with k<sub>x</sub> = k<sub>y</sub> = k, using your Activity 3 connectivity table.",
                                                   "(c) With T<sub>2</sub> = T<sub>6</sub> = 150 K from the solution, interpolate T at (x, y) = (1.4, 2.2) m."], 28, gap=8)),
                      D.eqpanel("w_asg_hint", "", colw=896, maxh=100, bg=WHITE, pad="12px 20px"),
                      callout("Show the connectivity table, s<sub>1</sub>…s<sub>4</sub> with a = 2 m, b = 3 m, and the local coordinates used in (c). Marks are for the method.", "ok", 24)),
                  lw=720),
          notes="Do not give numerical answers here. Hints only: (a) is the Qab/4 rule; (b) needs s1…s4 with a = 2, b = 3 and three scatter-adds into an 8 × 8 matrix; (c) is Activity 6 with the point in element 1, node 1 at the origin, and nodal values T1 = 100, T2 = 150, T6 = 150, T5 = 100. "
                 "Lecturer answer key is kept outside the deck. Due date: [date]; individual work; state the convention you use for the heat source (per unit area with unit thickness).")

D.activity("exit", 7, 5, "individual · exit ticket", "Three questions before you leave",
           D.card(D.h3("Questions") + D.ul(["In [k]{T̂}ᵀ = {q} + {b}, which vector does an insulated edge contribute to, and what is the contribution?",
                                            "Why must every row of [k] sum to zero, and what would a non-zero row sum tell you about your hand calculation?",
                                            "A 9-dof system has 5 Dirichlet nodes. How many equations do you solve, and what happens to the known values if they are not zero?"], 30, gap=12), extra="width:1000px"),
           col(D.eqpanel("w_sys", "", colw=616, maxh=80, bg=WHITE), D.eqpanel("w_rowsum", "", colw=616, maxh=180, bg=WHITE), extra="flex:1"),
           "Five minutes. Name and matric number; for feedback, not marks.",
           notes="Answers: (1) {b}, and the contribution is zero (q_b = 0). (2) A uniform temperature produces no heat flow, so [k]{1} = {0}; a non-zero row sum means an arithmetic or sign error in s1…s4. "
                 "(3) Four equations; non-zero known values are multiplied by their columns and moved to the right-hand side before the rows and columns are deleted.")

D.content("summary", "Wrap-up · heat transfer is done; plane stress starts the next session", "Same pipeline, two unknowns per node",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["Galerkin + IBP: [k]{T̂}ᵀ = {q} + {b}; the operator acts on the weight to its left.",
                                                              "[k] from four closed-form values s<sub>1</sub>…s<sub>4</sub>; rows sum to zero; {q} = q<sub>h</sub>ab/4; edge flux splits q<sub>b</sub>b/2.",
                                                              "Assembly = scatter-add by connectivity; Dirichlet = move known values right, delete rows and columns.",
                                                              "Post-process in local coordinates; refine the mesh before you believe a number."], 28, gap=10)),
                  col(D.card(D.h3("Before the next session") + D.ul(["Assignment 4: start now; due [date].", "Read text §3.1 (plane stress PDE) — 6 pages.", "Revise from solid mechanics: plane stress vs plane strain, Hooke’s law in 2D, strain–displacement relations.",
                                                            "Run the §2.3.1 script and change the mesh to 4 × 4."], 28, gap=10)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=940),
          notes="Close on time. Next session the unknown becomes the displacement vector {u, v}: [E] becomes 3 × 3, {∂} becomes a 2 × 3 operator matrix, and [k] becomes 8 × 8 — but every step today repeats.")

order = D.write("2026-10-26T15:10:00Z")
print(len(order), "slides:", order)
