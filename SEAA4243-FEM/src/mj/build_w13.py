import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w13"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w13" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — Plane Stress (Part 3) & Project Briefing", "SEAA 4243 · Plane Stress — Part 3 · Project", HERE / "eqs_w13", HERE / "figs_w13", eq_rep)
D11 = Deck(ROOT, "", "", HERE / "eqs_w11", HERE / "figs_w11", {x["name"]: x for x in json.loads((HERE / "eqs_w11" / "_report.json").read_text())})
D12 = Deck(ROOT, "", "", HERE / "eqs_w12", HERE / "figs_w12", {x["name"]: x for x in json.loads((HERE / "eqs_w12" / "_report.json").read_text())})
SXX = "/_blob/b57e367be5c050a8fe7ef4470acc72d2"

# =============================================================================
# ==== extras: web images + QR labs ====
HOLEVM = "/_blob/d74c86901e76d1b79cf19a46ecdcb8c2"; ITSK = "/_blob/057abd4b2e6a2d1fed8ccecf15b6f8ee"; ITSQ = "/_blob/69e45d6775b237f3c514ab78ad2ac2fe"

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · 2L + 1T</p>'
      f'<h1 style="font-family:{SERIF};font-size:112px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">Plane Stress<br>Part 3 of 3</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">Stresses from displacements, how far to trust them, the 8-node element, how to report FE results — and the project briefing</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020 — §3.4 – §3.5</p></div>',
      notes="Last theory session. Two halves: the first finishes plane stress (stress recovery, accuracy, the 8-node element, reporting); the second is the project briefing under CLO4. "
            "Assignment 4 should have been collected the last session; return feedback today if marked.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: retrieval warm-up, outcomes and the 3-hour plan")

D.activity("warmup", "0", 5, "individual · retrieval warm-up", "Three questions from the last session — on paper",
           D.card(D.h3("Write down") + D.ul(["[k] = t∫[B]ᵀ[E][B] dA — the size of each factor.", "The tip deflection of the 2 × 2 cantilever and of the converged mesh, and the percentage error.",
                                             "Why the coarse bilinear mesh is too stiff in bending (one sentence)."], 30, gap=10), extra="width:1000px"),
           col(callout("Today we compute the stresses that go with those displacements, and ask the same question: how far can they be trusted?", "why", 26), extra="flex:1"),
           "5 minutes. Then the outcomes.",
           notes="Answers: (1) 8 × 3, 3 × 3, 3 × 8 → 8 × 8. (2) 0.131 m and 0.192 m, −32%. (3) Straight element edges cannot curve, so bending produces spurious shear strain (shear locking).")

outs = ["Recover strains and stresses at a point of an element from the nodal displacements, {ε} = [B]{û}, {σ} = [E][B]{û}, and compute principal and von Mises stresses.",
        "Explain where stresses are accurate (element centroids, away from supports) and where they are not (element edges, re-entrant corners, point loads).",
        "Describe the 8-node element and its advantage per element; convert an edge traction into its 1/6 – 2/3 – 1/6 nodal loads.",
        "Plan and report an FE study: idealisation, mesh refinement table, one independent check, quantified conclusions — the project standard."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("Outcomes 1–3 complete CLO3. Outcome 4 is CLO4: the project (15%) and the ANSYS demo assess it.", "why"),
          notes="Four outcomes; the fourth belongs to the project. Keep the first half tight so the briefing gets its full forty minutes.")

D.content("session", "Session map · 180 minutes", "Six blocks, six activities, one break, the project briefing",
          session_map([("0:00", "Stress recovery", 35, "A1 · 8 min", False), ("0:35", "Accuracy of stresses", 25, "A2 + QR", False), ("1:00", "The 8-node element", 25, "A3 · 6 min", False),
                       ("1:25", "Break", 10, "", True), ("1:35", "Reporting results", 25, "A4 · 8 min", False), ("2:00", "Project briefing", 40, "A5 · 12 min", False), ("2:40", "Wrap-up", 20, "Exit ticket", False)])
          + row(D.card(D.h3("Bring forward") + D.ul(["Plane Stress Part 2 Activity 1: [B] at (1.5, 0.3) with a = 2, b = 1.", "Plane Stress Part 1 Activity 5: the nodal displacements of element 4.", "Plane Stress Part 1 Activity 3: [E] = 224.44, 74.07, 75.19 (× 10⁶)."], 28), extra="flex:1"),
                D.card(D.h3("Project") + D.ul(["Groups of [4–5] — lecturer to confirm.", "Brief, deliverables, rubric and dates in Block 5.", "Model plan (one page) drafted in class today."], 28), extra="flex:1"), align="stretch"),
          notes="Items in square brackets on the project slides are for the lecturer to confirm before the session: group size, due date, presentation slot.")

# =============================================================================
# Block 1 — Stress recovery
# =============================================================================
D.divider("d1", "1", "Stresses from displacements", "The same [B] that built [k] now turns the solved nodal displacements into strains and stresses at any point. Text §3.4, Fig. 3.7.",
          "Block 1 · 0:00 – 0:35", section="Block 1: strain and stress recovery at a point from the nodal displacements, principal and von Mises stresses",
          notes="Thirty-five minutes. The whole calculation uses numbers the class already has from three earlier activities; the new step is the matrix product and the interpretation.")

D.content("recover", "Block 1 · the post-processing formula", "Two matrix products: [B] gives strains, [E] gives stresses",
          col(D.eqpanel("t_recover", "", colw=1664, maxh=80),
              row(D.card(D.h3("Step 1 · locate") + D.p("Find the element, convert to local coordinates (the local-coordinate rule from heat transfer), take its eight nodal displacements in local order.", 28), extra="flex:1"),
                  D.card(D.h3("Step 2 · strains") + D.p("Evaluate [B] at the point (3 × 8) and multiply by {û}ᵀ (8 × 1): three strains.", 28), extra="flex:1"),
                  D.card(D.h3("Step 3 · stresses") + D.p("Multiply by [E] (3 × 3): σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub>. Then principal and von Mises if the design needs them.", 28), extra="flex:1"), align="stretch"),
              callout("Software does exactly this at the Gauss points of every element and then averages to the nodes for the contour plot. Hand calculation lets you see what is averaged.", "why", 26)),
          notes="Emphasise the chain: nodal displacements are the primary result; everything else is derived by differentiation, which is why stresses are less accurate than displacements.")

D.content("point", "Block 1 · the worked point · element 4 at (3.5, 1.3) m", "Local (1.5, 0.3): the [B] of Plane Stress Part 2 and the nodal displacements of Plane Stress Part 1",
          col(D.eqpanel("t_Bnum", None, colw=1664, maxh=170, pad="12px 32px"),
              D.eqpanel("t_u4", None, colw=1664, maxh=110, pad="12px 32px"),
              callout("[B] is the Plane Stress Part 2 Activity 1 result. {û⁴} is the course MATLAB solution of the text’s (3.49) to six decimals: the text prints three, which is not enough here. Local order: nodes (1)(2)(3)(4) of element 4 are global 5, 6, 9, 8, each with u then v.", "warn", 26)),
          notes="Everything on this slide was computed in earlier activities. Point at where each number came from before multiplying.")

D.activity("act1", 1, 8, "pairs · calculation", "Strains and stresses at (3.5, 1.3) m",
           D.card(D.h3("Do") + D.ul(["Multiply row by row: ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub> = [B]{û⁴}.", "Multiply by [E] (224.44, 74.07, 75.19 × 10⁶ N m⁻²) to get σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub> in kN m⁻².",
                                     "Which stress is largest? Is σ<sub>xx</sub> tension or compression at this point, and should it be (the point is above the mid-height)?"], 30, gap=10), extra="width:1000px"),
           col(D.card(D.h3("Formula") + D.p("{ε}ᵀ = [B]{û}ᵀ &nbsp;(3 × 8)(8 × 1)", 28) + D.p("{σ}ᵀ = [E]{ε}ᵀ &nbsp;(3 × 3)(3 × 1)", 28)),
               callout("Only the non-zero products matter: row 1 has two, row 2 four, row 3 six.", "ok", 26), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers with the six-decimal displacements: ε_xx = 0.15(0.041967 − 0.030966) = 0.0016501; ε_yy = −0.0007445; ε_xy = −0.0041348. "
                 "σ_xx = 224.44 × 1.6501 − 74.07 × 0.7445 = 370.4 − 55.1 = 315.2 kN/m²; σ_yy = 74.07 × 1.6501 − 224.44 × 0.7445 = −44.9; σ_xy = 75.19 × (−4.1348) = −310.9. "
                 "σ_xx and σ_xy are about the same size; σ_yy is small, as beam theory assumes. σ_xx is tension, correct above the neutral axis of a downward-loaded cantilever. "
                 "Trap: with the text’s three-decimal displacements ε_yy doubles (−0.0015) and σ_yy comes out as −214: v6 and v9 differ only in the fourth decimal.")

D.content("act1-reveal", "Activity 1 · solution", "Tension above the neutral axis; σ<sub>yy</sub> small, as beam theory assumes",
          col(D.eqpanel("t_eps_num", "", colw=1664, maxh=240, pad="12px 32px"), D.eqpanel("t_sig_num", "", colw=1664, maxh=200, pad="12px 32px"),
              row(callout("σ<sub>xx</sub> > 0 above mid-height: top fibre in tension. σ<sub>xy</sub> carries the end shear; σ<sub>yy</sub> is small.", "why", 26), callout("Keep six decimals: v<sub>6</sub> and v<sub>9</sub> differ in the fourth. With three decimals ε<sub>yy</sub> doubles and σ<sub>yy</sub> becomes −214.", "warn", 26), align="stretch")),
          notes="Strains are differences of nodal displacements, so rounding is amplified: ε_yy comes from v6 = −0.130421 and v9 = −0.130578. The Explorer (QR) computes at full precision and gives 315.2, −44.9, −310.9. Next slide: compare with beam theory.")

D.content("principal", "Block 1 · principal and von Mises stresses", "From three components to the two numbers a design check uses",
          col(D.eqpanel("t_principal", "", colw=1664, maxh=200, pad="12px 32px"), D.eqpanel("t_vm", "", colw=1664, maxh=100, pad="12px 32px"),
              row(D.card(D.h3("Principal stresses") + D.p("The largest tension (σ<sub>1</sub>) governs cracking in concrete; the direction is at ½·atan(2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)) from the x-axis.", 28), extra="flex:1"),
                  D.card(D.h3("Von Mises") + D.p("The yield check for steel: σ<sub>vM</sub> against f<sub>y</sub>. ANSYS plots it by default — know what it is before you read the colour.", 28), extra="flex:1"), align="stretch")),
          notes="Both are standard in solid mechanics; included so that the ANSYS contour plots the next session mean something. For concrete walls the principal tension and its direction decide the reinforcement.")

# =============================================================================
# Block 2 — Accuracy of stresses
# =============================================================================
D.divider("d2", "2", "How far can a stress be trusted?", "Compare with beam theory at the point, at the centroid, across the depth and at the fixed corner. Text Fig. 3.7.",
          "Block 2 · 0:35 – 1:00", section="Block 2: accuracy of recovered stresses, centroid versus point values, mesh convergence of stresses, and the singularity at the fixed corner",
          notes="Twenty-five minutes. The message: stresses converge more slowly than displacements, and at a re-entrant corner they do not converge at all.")

D.content("beam-compare", "Block 2 · beam theory as a check", "Beam theory is a valid check only away from the ends",
          col(D.eqpanel("t_beam_line", None, colw=1664, maxh=96, pad="12px 32px"),
              table(["Point (m)", "2 × 2 FE", "Converged FE", "Beam theory"],
                    [["(1.0, 1.5) centroid of element 3", "1 645", "2 265", "2 250"], ["(2.0, 1.3) mid-span, on the edge between elements 3 and 4", "857 | 185", "900", "900"],
                     ["(3.0, 1.5) centroid of element 4", "519", "730", "750"], ["(3.5, 1.3) the Activity 1 point, 0.5 m from the loaded end", "315", "153", "225"]], [52, 16, 16, 16], 26),
              D.p("σ<sub>xx</sub> in kN m⁻²; converged = 8-node 64 × 32 from the course solver; at (3.5, 1.3) beam theory gives 5 000 × 0.3 / 6.667 × 10⁻³ = 225.", 24, MUTED),
              row(callout("2 × 2 → converged is the mesh error: up to 30% at centroids, and two different values on a shared edge.", "warn", 26),
                  callout("Converged FE → beam theory: 0.03% at mid-span, 32% at x = 3.5 m. Near the end the uniform traction of the model is not the parabolic shear beam theory assumes (St-Venant).", "why", 26), align="stretch")),
          notes="Two errors are mixed in the 2 × 2 numbers. The mesh error (compare the first two columns) and, near the ends, the error of the check itself (compare the last two). "
                "Beam theory is exact for a parabolic end shear; the model applies a uniform traction, and the difference decays over about one depth from the end. "
                "Use centroid values at mid-span for checks. The 857 | 185 pair is the same point seen from two elements: unaveraged stresses jump across element edges on a coarse mesh.")

D.content("sxx", "Block 2 · stresses on a fine mesh", "At element centroids, away from the support, a 32 × 16 mesh matches beam theory",
          two_col(f'<img src="{SXX}" alt="Left: contour of sigma xx at element centroids on a 32 by 16 mesh, positive at the top fibre and negative at the bottom, largest at the fixed end. Right: sigma xx through the depth at x of 2 m from the finite element centroids compared with the straight line of beam theory" style="width:1100px;height:400px;object-fit:contain;border-radius:12px">',
                  col(D.card(D.h3("Reading the plot") + D.ul(["Linear through the depth; zero at mid-height: beam theory holds away from the ends.", "Largest at the fixed end, zero at the free end: M = P(L − x).", "Each element has one centroid value; the contour is piecewise constant."], 26, gap=6)),
                      callout("Centroid values of a 32 × 16 mesh at x ≈ 2 m: within 0.25% of beam theory at every depth.", "ok", 24)),
                  lw=1100, rw=516, align="start"),
          notes="The right-hand plot is the one to remember: FE centroid stresses on a fine mesh sit on the beam-theory line. The left-hand contour is clipped at ±3000 kN/m² so the colours are readable; the fixed corner goes higher — next slide.")

D.content("singular", "Block 2 · the fixed corner never converges", "A re-entrant corner of a fully fixed edge is a stress singularity in the elastic model",
          col(table(["Mesh", "Centroid of the top-left element (m)", "FE σ<sub>xx</sub> there (kN m⁻²)", "Beam theory at the same point", "FE / beam"],
                    [["8 × 4", "(0.25, 1.75)", "4 134", "4 219", "0.98"], ["16 × 8", "(0.125, 1.875)", "5 372", "5 086", "1.06"], ["32 × 16", "(0.0625, 1.9375)", "6 400", "5 537", "1.16"], ["64 × 32", "(0.031, 1.969)", "7 467", "5 767", "1.30"]], [14, 30, 22, 22, 12], 27),
              row(callout("Beam theory at the corner tends to 6 000; the FE value passes it and keeps rising with every refinement. The elastic solution is infinite there — refining chases infinity.", "warn", 26),
                  callout("Design practice: do not read a peak at a modelled corner. Report stresses a short distance away (St-Venant), or model the support realistically, or use a stress linearisation.", "why", 26), align="stretch")),
          notes="This is why ANSYS users see “hot spots” at supports and point loads. The numbers are from the course MATLAB solver with centroid evaluation. The same happens at a concentrated nodal force.")

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

D.activity("act2", 2, 6, "pairs · judgement", "Which of these stresses would you put in a design report?",
           D.card(D.h3("Six candidates") + D.ul(["σ<sub>xx</sub> at the centroid of an element in the middle of a 32 × 16 mesh.", "Peak von Mises at the fixed corner of the same mesh.", "σ<sub>xx</sub> at the top-right node of the 2 × 2 hand mesh.",
                                                 "Nodal-averaged σ<sub>xx</sub> at mid-span from a mesh-converged model.", "Stress under a single nodal point load.", "σ<sub>xy</sub> averaged over the depth at a section 1 m from the support."], 29, gap=6), extra="width:1060px"),
           D.card(D.h3("For each") + D.ul(["Trust / use with care / do not report.", "One reason."], 30, gap=8), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: (1) trust — centroid of a converged mesh, away from boundaries. (2) do not report — singularity. (3) do not report — coarse mesh and a nodal value (extrapolated). (4) trust if the mesh study shows convergence. "
                 "(5) do not report — a point load is a singularity too; distribute it over a realistic area. (6) use with care — averaged shear is fine; near the support it is still within the St-Venant zone.")

D.content("act2-reveal", "Activity 2 · solution", "Trust converged centroid values away from singularities; distribute point loads; never report a corner peak",
          col(table(["Candidate", "Verdict", "Reason"], [["centroid, fine mesh, mid-span", "trust", "converged, interior point, element-level value"], ["von Mises at the fixed corner", "do not report", "stress singularity: grows without bound with refinement"],
                                                        ["nodal σ<sub>xx</sub> on the 2 × 2 mesh", "do not report", "coarse mesh, extrapolated to a node"], ["nodal-averaged, converged mesh", "trust", "averaging is the standard post-processing"],
                                                        ["under a nodal point load", "do not report", "another singularity; spread the load over a patch"], ["depth-averaged σ<sub>xy</sub> 1 m from support", "use with care", "fine for shear resultant; local values still disturbed by the support"]], [34, 18, 48], 26)),
          notes="The verdicts carry over directly to the project rubric: a report that quotes a corner peak as the design stress loses the interpretation marks.")

# =============================================================================
# Block 3 — The 8-node element
# =============================================================================
qr_lab(D, "qr-stress", 8, "Probe the lecture point, then refine",
       ["4-node 2 × 2, probe (3.5, 1.3). Compare with your Activity 1 numbers.",
        "Refine to 8-node 16 × 8 and 32 × 16 at the same point. Does σ<sub>xx</sub> approach beam theory’s 225? Then probe mid-span (2.0, 1.3).",
        "Run the corner study. Does the peak σ<sub>xx</sub> at the fixed corner converge?"],
       [LABS["stress"]], "8 minutes, optional in class: if the block is running late, set it as homework. The display options are the ones you will meet in ANSYS the next session.",
       notes="The QR code opens the public copy on GitHub Pages (no login): open it once on a phone before class. "
             "Answers: (1) 315.2, −44.9, −310.9 kN/m² (full precision). (2) It settles near 150, not 225: the point is 0.5 m from the loaded edge, where the uniform end traction differs from the parabolic shear of beam theory. "
             "At mid-span FE = beam theory = 900. (3) No: 4 134 → 5 372 → 6 400 → 7 467 kN/m².")

D.divider("d3", "3", "The 8-node element", "Mid-side nodes, quadratic edges, 16 dofs: fewer elements for the same accuracy in bending. Text Fig. 3.6, (3.50)–(3.53), Table 3.2.",
          "Block 3 · 1:00 – 1:25", section="Block 3: the eight-node serendipity element, its load distribution and its accuracy compared with the four-node element",
          notes="Twenty-five minutes, then the break. No hand derivation of the 16 × 16 matrix; the point is to read the text’s results and understand why the element is better in bending.")

D.content("q8", "Block 3 · the element · text Fig. 3.3, Fig. 3.6", "Two elements, 13 nodes, 26 dofs for the whole cantilever",
          col(D.eqpanel("t_q8_sizes", None, colw=1664, maxh=90, pad="12px 32px"),
              two_col(figbox(D.fig("fig_q8_mesh", width=700)),
                      col(D.eqpanel("t_q8_N", None, colw=868, maxh=200, pad="12px 24px"), D.p("Shape functions of the text's (2.31): corner nodes and mid-side nodes have different forms.", 24, MUTED),
                          callout("Quadratic along each edge: the element can curve, so bending no longer forces spurious shear. That is the whole advantage.", "why", 24)),
                      lw=748)),
          notes="Same recipe as Q4 with the eight shape functions of (2.31). The 16 × 16 [k] is in the text’s MATLAB listing §3.4.2 (38 distinct values); nobody computes it by hand.")

D.content("q8-loads", "Block 3 · edge loads on a three-node edge · text (3.51)", "One sixth to each corner, two thirds to the mid-side node",
          col(D.eqpanel("t_q8_loads", None, colw=1664, maxh=165, pad="12px 32px"),
              row(figbox(D.fig("fig_q8_loads", width=620)),
                  col(callout("Not half-and-half any more: the quadratic edge shape functions integrate to b/6, 2b/3, b/6. The total is still q<sub>y</sub>b.", "why", 26),
                      callout("For the 2 × 1 mesh the loaded edge belongs to element 2 only: U<sub>10</sub>, U<sub>16</sub>, U<sub>26</sub> receive −1667, −6667, −1667 N — the text’s (3.52).", "ok", 26), extra="flex:1"), align="center")),
          notes="Check the total: 1667 + 6667 + 1667 = 10 000 N = 5 kN/m × 2 m. The mid-side node carries most of it because its shape function is the bubble along the edge.")

D.activity("act3", 3, 6, "pairs · comparison", "Which mesh for the money? Compare Q4 and Q8 on the cantilever",
           D.card(D.h3("Given · text Tables 3.1 and 3.2") + table(["Model", "Elements", "Dofs", "U₁₈ (m)"], [["Q4 2 × 2", "4", "18", "−0.131"], ["Q8 2 × 1", "2", "26", "−0.178"], ["Q8 4 × 4", "16", "—", "−0.189"], ["Q4 16 × 16", "256", "578", "−0.189"], ["converged", "—", "—", "−0.192"]], [34, 22, 20, 24], 26), extra="width:900px"),
           D.card(D.h3("Find") + D.ul(["The error of each model.", "Elements needed by Q4 and by Q8 for about 1.6% error.", "Why Q8 wins per element — one sentence."], 30, gap=8), extra="flex:1"),
           "6 minutes. Reveal follows, then the break.",
           notes="Answers: Q4 2×2 −32%; Q8 2×1 −7%; Q8 4×4 −1.6%; Q4 16×16 −1.6%. For 1.6%: Q8 needs 16 elements, Q4 needs 256. Q8 wins because its edges can curve (quadratic), so bending does not generate spurious shear strain. "
                 "Dofs are the fairer cost measure: Q8 4×4 has 25 corner + 40 mid-side = 65 nodes = 130 dofs, versus 17 × 17 = 289 nodes = 578 dofs for Q4 16×16.")

D.content("act3-reveal", "Activity 3 · solution · text Table 3.2", "Two 8-node elements beat four 4-node elements; sixteen match 256",
          col(D.eqpanel("t_err", "", colw=1664, maxh=330, pad="12px 32px"),
              row(callout("ANSYS: PLANE182 ≈ Q4, PLANE183 ≈ Q8. The default for 2D solids is the quadratic one — now you know why.", "ok", 26),
                  callout("Cost is dofs, not elements: Q8 4 × 4 has about 130 dofs; Q4 16 × 16 has 578 for the same error.", "why", 26), align="stretch")),
          notes="Then break: 10 minutes.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:25 – 1:35</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: how to report FE results, and the project briefing.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True), notes="Ten minutes. Ask groups to sit together after the break.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Reporting results
# =============================================================================
D.divider("d4", "4", "Reporting an FE result", "A number without a mesh study and a check is an opinion. The four things every results section needs.",
          "Block 4 · 1:35 – 2:00", section="Block 4: the standard for reporting finite element results — idealisation, convergence table, independent check, quantified conclusion",
          notes="Twenty-five minutes. This block sets the standard the project is marked against.")

D.content("report", "Block 4 · four things every FE results section needs", "Idealisation, convergence, an independent check, quantified conclusions",
          f'<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:28px">'
          + D.card(D.h3("1 · Idealisation stated") + D.p("Plane stress or plane strain and why; thickness; material constants with units; supports and loads with a sketch; what was left out (self-weight? openings? reinforcement?).", 27), pad=30)
          + D.card(D.h3("2 · Convergence table") + D.p("At least three meshes; the quantity of interest for each; the change between the last two as a percentage. One table, one sentence saying which mesh the results come from.", 27), pad=30)
          + D.card(D.h3("3 · One independent check") + D.p("Beam theory, equilibrium of reactions against applied loads, a textbook stress-concentration factor, or a hand calculation on a coarse mesh. Report the difference with its sign.", 27), pad=30)
          + D.card(D.h3("4 · Quantified conclusions") + D.p("“The tip deflection is 0.191 m, within 0.7% of beam theory” — not “the results agree well”. Say where the maximum is, what it means for the design, and what the model cannot tell you.", 27), pad=30)
          + "</div>",
          notes="Read the four cards as a checklist. Point 4 is the one students resist: they write “good agreement” instead of a number with a direction.")

D.content("report-ex", "Block 4 · the cantilever written up in five sentences", "A model paragraph for the project report",
          col(D.card(D.p("The cantilever (4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m⁻², ν = 0.33) was idealised as plane stress with the left edge fully fixed and the 5 kN m⁻¹ end load applied as an edge traction. "
                         "Four-node meshes of 2 × 2, 8 × 4, 16 × 8 and 32 × 16 elements gave tip deflections of 0.131, 0.182, 0.189 and 0.191 m; the change between the last two meshes is 1.0%, so the 32 × 16 results are reported. "
                         "Timoshenko beam theory gives 0.192 m (0.160 m bending, 0.032 m shear), 0.7% above the FE value. "
                         "The bending stress at element centroids at mid-span agrees with M(y − 1)/I to within 0.25%; the stress at the fixed corner increases without bound under refinement and is not reported. "
                         "The reactions sum to 10.0 kN upward and 40.0 kN m, equal to the applied load and its moment.", 29, BODY, lh=1.45), pad=36),
              row(callout("Every sentence carries a number, a comparison or a decision. No adjectives.", "ok", 26), callout("Five sentences, one table, two figures: that is the whole results section of a good project report.", "why", 26), align="stretch")),
          notes="Students can use this paragraph as a template: replace the structure, the numbers and the check. The reaction check is from the course solver; in ANSYS it is the Reaction Probe.")

D.activity("act4", 4, 8, "pairs · writing", "Write the heat-transfer plate up in three sentences",
           D.card(D.h3("Data · Heat Transfer Part 2") + table(["Mesh", "T(L, 0) (°C)"], [["Q4 2 × 2", "0.6214"], ["Q4 16 × 16", "0.5898"], ["Software", "0.5897"]], [50, 50], 26)
                  + D.p("Plate 1 m × 1 m, k = 300 W m⁻¹ K⁻¹, q<sub>h</sub> = 600 W m⁻³, two edges at 0 °C, two insulated.", 26, MUTED), extra="width:860px"),
           D.card(D.h3("Write") + D.ul(["Sentence 1: the idealisation.", "Sentence 2: the convergence, with the percentage change.", "Sentence 3: the check against software, with the signed difference."], 30, gap=8)
                  + D.p("Rule: every sentence has at least one number.", 28, DARK, 600), extra="flex:1"),
           "8 minutes. Two pairs read theirs out.",
           notes="A model answer: “The plate was idealised as 2D steady conduction with T = 0 °C on the top and left edges and the other two edges insulated. The maximum temperature at the bottom-right corner was 0.6214 °C on the 2 × 2 mesh and 0.5898 °C on the 16 × 16 mesh, a change of −5.1%, so the finer mesh is reported. The commercial-software value of 0.5897 °C is 0.02% below the FE result.”")

# =============================================================================
# Block 5 — Project briefing
# =============================================================================
D.divider("d5", "5", "Project briefing", "CLO4: investigate a structural problem with FEM, in a group, with software — and defend the numbers. 15% of the course.",
          "Block 5 · 2:00 – 2:40", section="Block 5: the group project brief, candidate structures, deliverables, rubric, timeline and the in-class model plan",
          notes="Forty minutes. Items in square brackets are to be confirmed by the lecturer before the session. Walk through the brief, the candidates, the rubric, then give the groups twelve minutes to draft a model plan.")

D.content("brief", "Block 5 · the brief", "One real structure, one FE model, one verified answer, one report, one presentation",
          col(row(D.card(D.h3("Task") + D.p("Choose a 2D structural problem, idealise it, model it in ANSYS (plane stress or plane strain), verify the model, and interpret the results for design.", 28), extra="flex:1"),
                  D.card(D.h3("Team") + D.p("Groups of [4–5]. One submission per group; a one-line statement of who did what.", 28), extra="flex:1"),
                  D.card(D.h3("Weight") + D.p("15% of the course (CLO4). Report [70%] · presentation [30%] — lecturer to confirm.", 28), extra="flex:1"), align="stretch"),
              row(D.card(D.h3("Deliverables") + D.ul(["Technical report, [10–15] pages: idealisation, mesh study, check, results, interpretation, limitations.", "Presentation, [10] minutes + questions, [date].", "Model files (.wbpj or archive) and the hand-check sheet."], 28, gap=6), extra="flex:1"),
                  D.card(D.h3("Dates") + D.ul(["Today: groups formed, model plan drafted.", "ANSYS demo: bring your plan and start the model in the lab.", "[date]: report and presentation."], 28, gap=6), extra="flex:1"), align="stretch")),
          notes="Confirm the bracketed items. The course information lists Project as 15% with project-based learning in groups on a truss, frame or 2D plane-stress case; 2D is required here because that is what the 2D sessions teach.")

cands = [("Shear wall with openings", "Text Exercise 3.4: 5 m × 6 m, t = 0.2 m, 125 kN m⁻¹ on top, two openings. Plane stress. Check: cantilever beam + stress concentration at opening corners."),
         ("Deep beam or transfer girder", "Span-to-depth about 2; point or distributed load; supports on bearing pads. Plane stress. Check: beam theory for deflection, strut-and-tie for the stress path."),
         ("Gusset or connection plate", "Steel plate with bolt-hole or weld loads; t = 10–20 mm. Plane stress. Check: net-section stress, stress-concentration factor at the hole (≈ 3)."),
         ("Dam or retaining wall section", "Per metre run with hydrostatic pressure and self-weight. Plane strain. Check: overturning and base stress from statics.")]
D.content("candidates", "Block 5 · candidate structures", "Four families that fit the course; propose your own if it is 2D and checkable",
          f'<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:20px">' + "".join(D.card(D.h3(t, 30) + D.p(s, 26), pad=22, gap=8) for t, s in cands) + "</div>"
          + row(figbox(D11.fig("fig_shearwall", height=110)), col(callout("Choose something with a known hand check. A structure you cannot check is a structure you cannot defend in the presentation.", "warn", 26), extra="flex:1"), align="center"),
          notes="Steer groups toward the first two: they map directly onto what was taught, and the checks are in this course. The dam needs plane strain — a good choice for a strong group.")

D.content("rubric", "Block 5 · how it is marked", "Proposed rubric — lecturer to confirm weights",
          col(table(["Criterion", "Weight", "Full marks look like", "Common failure"],
                    [["Idealisation and modelling", "30%", "plane stress/strain justified; supports and loads realistic; units consistent; sketch of the model", "fixing edges that are free; point loads at a node; wrong thickness"],
                     ["Verification", "30%", "three-mesh convergence table; one independent hand check with a signed difference", "single mesh; “results agree well” with no number"],
                     ["Interpretation", "20%", "where the maximum is and why; what it means for the design; singularities identified and excluded", "quoting the corner peak as the design stress"],
                     ["Report and presentation", "20%", "five-sentence results paragraph; labelled figures with units; questions answered with numbers", "screenshots without scales; reading slides aloud"]], [22, 10, 38, 30], 28),
              callout("Sixty per cent of the marks are for modelling decisions and verification — not for the colour plots. A plain model that is checked beats an elaborate one that is not.", "why", 26)),
          notes="The rubric is proposed; adjust the weights to the faculty template. The right-hand column tells students exactly what loses marks.")

D.content("workflow", "Block 5 · the modelling workflow", "Eight steps; the project report follows the same order",
          f'<div style="display:grid;grid-template-columns:repeat(8, 1fr);gap:12px">'
          + "".join(f'<div style="background:{WHITE};border:1px solid {HAIR};border-radius:14px;padding:16px 10px;display:flex;flex-direction:column;gap:8px;min-width:0">'
                    f'<p style="font-family:{SERIF};font-size:48px;font-weight:600;line-height:1;color:{MAROON}">{i+1}</p><p style="font-size:26px;font-weight:600;line-height:1.2;color:{DARK}">{t}</p><p style="font-size:24px;line-height:1.3;color:{BODY}">{s}</p></div>'
                    for i, (t, s) in enumerate([("Idealise", "2D? stress or strain? what is left out"), ("Geometry", "dimensions, thickness, openings"), ("Material", "E, ν, units"), ("Mesh", "element type, size, three levels"),
                                                 ("Supports", "fixed, roller, symmetry"), ("Loads", "tractions, body force, not point loads"), ("Solve & verify", "reactions, convergence, hand check"), ("Interpret", "where, why, what it means")])) + "</div>"
          + callout("the ANSYS demo runs exactly this sequence in ANSYS on the cantilever and the plate, then on your structure.", "ok", 26),
          notes="This is also the agenda of the ANSYS demo. Groups should arrive at the ANSYS demo with steps 1–3 and 5–6 decided on paper.")

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

D.activity("act5", 5, 12, "groups · planning", "Draft your model plan on one page",
           D.card(D.h3("Write, as a group") + D.ul(["The structure, with a sketch and dimensions; the source of the geometry and loads.", "Idealisation: plane stress or plane strain, thickness, material (E, ν, units).",
                                                    "Supports and loads, each one justified in a few words.", "The quantity you will report (deflection? stress where?) and the hand check you will use.", "Three mesh sizes you will run."], 29, gap=8), extra="width:1060px"),
           col(callout("Lecturers circulate. A plan with a fixed edge that should be free, or no hand check, is sent back now rather than in the report.", "warn", 26),
               callout("Hand in the plan at the end; it comes back with comments at the ANSYS session.", "ok", 26), extra="flex:1"),
           "12 minutes. Hand in before you leave.",
           notes="Use the time to visit every group once. The two questions to ask: what is your hand check, and what is free and what is fixed.")

# =============================================================================
# Block 6 — Wrap-up
# =============================================================================
D.divider("d6", "6", "Wrap-up", "Three sessions of plane stress in one page, the exit ticket, and what to bring to the ANSYS session.",
          "Block 6 · 2:40 – 3:00", section="Block 6: summary of the plane-stress sessions, exit ticket and preparation for the ANSYS demonstration",
          notes="Twenty minutes.")

D.content("summary-ps", "Block 6 · plane stress in one page", "From equilibrium to a verified stress",
          col(table(["Part", "Step", "Result"], [["1", "equilibrium + Hooke + strain–displacement", "[∂][E][∂]ᵀ{u}ᵀ = −{f}; traction natural, displacement essential; [N] 2 × 8"],
                                                  ["2", "Galerkin + IBP; [B] = [∂]ᵀ[N]", "[k] = t∫[B]ᵀ[E][B] dA, s₁…s₁₂; loads qb/2; assembly by dof map; 2 × 2 cantilever 32% too stiff"],
                                                  ["3", "post-processing and judgement", "{σ} = [E][B]{û}; trust centroids on converged meshes; corners are singular; Q8 curves"]], [10, 36, 54], 27),
              row(callout("The heat-transfer pipeline, with two unknowns per node. Nothing else changed.", "why", 26), callout("Exam: expect one hand calculation on a single element (k entry, load vector or stress at a point) and one interpretation question.", "ok", 26), align="stretch")),
          notes="One-page summary for revision. The exam hint reflects the CLO3 assessment: formulate and solve by hand for simple cases.")

D.activity("exit", 6, 5, "individual · exit ticket", "Three questions before you leave",
           D.card(D.h3("Questions") + D.ul(["Order the three operations that take nodal displacements to a stress at a point.",
                                            "Your model shows its highest stress at a fixed corner. What do you do?",
                                            "Which element would you choose for a wall in bending with a limited number of elements, Q4 or Q8, and why?"], 30, gap=12), extra="width:1300px"),
           None,
           "Five minutes. Name and matric number; for feedback, not marks.",
           notes="Answers: (1) locate and take local nodal displacements → [B]{û} → [E]{ε}. (2) Do not report it; it is a singularity — refine to show it diverges, report stresses away from the corner or model the support realistically. (3) Q8: quadratic edges avoid shear locking; fewer elements for the same accuracy.")

D.content("summary", "Wrap-up · before the ANSYS session", "Bring the model plan, the two textbook examples and a laptop with ANSYS access",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["{σ} = [E][B]{û}: two products; use centroid values on converged meshes.", "Stresses converge slower than displacements; fixed corners and point loads are singular.",
                                                              "Q8: quadratic edges, 1/6–2/3–1/6 loads, far fewer elements for the same error.", "A results section = idealisation + convergence table + one check + numbers."], 28, gap=10)),
                  col(D.card(D.h3("Before the ANSYS demo") + D.ul(["Install or confirm access to ANSYS Student / Workbench; bring a laptop.", "Re-read Heat Transfer Part 2 §2.3 and Plane Stress Part 2 §3.4: we rebuild both in ANSYS and compare.",
                                                            "Finish the group model plan if it was returned with comments."], 28, gap=10)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=940),
          notes="Close on time. Collect the model plans and the exit tickets.")

order = D.write("2026-10-26T16:55:00Z")
print(len(order), "slides:", order)
