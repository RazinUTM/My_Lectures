import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w14"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w14" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — ANSYS Demo: Hand Calculation vs Software", "SEAA 4243 · ANSYS demo · hand calculation vs software", HERE / "eqs_w14", HERE / "figs_w14", eq_rep)
D11 = Deck(ROOT, "", "", HERE / "eqs_w11", HERE / "figs_w11", {x["name"]: x for x in json.loads((HERE / "eqs_w11" / "_report.json").read_text())})
WB = "/_blob/1cada4a4c7b95222761fbf6636d8015e"; PLATE = "/_blob/e0b47dd66681a36c53c16130a214cc68"; CANT = "/_blob/b1911d3845606732f87e754f688e77f4"
CONV = "/_blob/a3676e3c3cf26e744a495cdd3c4ab5ef"; WRONG = "/_blob/424772ab8b80e1aedff32d434a16416d"

def img(src, alt, w, h, bg=WHITE):
    return (f'<div style="background:{bg};border:1px solid {HAIR};border-radius:14px;padding:16px;display:flex;align-items:center;justify-content:center">'
            f'<img src="{src}" alt="{alt}" style="width:{w}px;height:{h}px;object-fit:contain"></div>')

# =============================================================================
# ==== extras: web images + QR labs ====
B1 = "/_blob/d8c9226261eecf74a1614dcf0f1770f4"; B2 = "/_blob/6693c19de0443fb785f34881efa131b2"; B3 = "/_blob/454cd3868335f396bb1405ce28ff40a6"; B4 = "/_blob/0a0931aa6f1852d9164d76567d86b3cc"
H1 = "/_blob/528e57bc6fa4ebfb90d0370ba59a2af2"; H2 = "/_blob/b93768ed4fdbc4b8e1a13e1f37dd8969"; H3 = "/_blob/1e6055863eaeaddd3f3d2ab4f56cce4f"
def panel(lab, src, alt, w, h):
    return col(D.p(lab, 26, DARK, 600), webimg(src, alt, w, h, pad=10), gap=10)

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · computer lab · 3 hours</p>'
      f'<h1 style="font-family:{SERIF};font-size:104px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">ANSYS demo:<br>hand calculation<br>versus software</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">The two textbook problems rebuilt in Workbench — predict, run, compare, explain — then your project model gets its first run</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., MSNM 2020 — §2.3 (plate) and §3.4 (cantilever) · ANSYS Mechanical (Workbench), Student edition is sufficient</p></div>',
      notes="Computer-lab session. Everything on screen is an ANSYS run of a problem the class has already solved by hand, so every number can be predicted before Solve is pressed. "
            "Menu names are those of recent Mechanical releases (2023–2025); check them against the lab version before class and run both models once yourself. Slides with [brackets] carry lecturer placeholders. "
            "Groups bring the model plan returned from Plane Stress Part 3.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: predictions on paper, outcomes and the 3-hour plan")

D.activity("warmup", "0", 5, "individual · predictions on paper", "Before any software: write down what the answers must be",
           D.card(D.h3("Write down") + D.ul(["The temperature at the bottom-right corner of the text’s plate (converged value).", "The tip deflection of the text’s cantilever (converged value) and its 2 × 2 hand value.",
                                             "The element that corresponds to the hand calculation (4-node or 8-node?) and the one ANSYS uses by default."], 30, gap=10), extra="width:1000px"),
           col(callout("Rule for today: no number from the screen is accepted until it has been predicted, or checked afterwards against something independent.", "why", 26), extra="flex:1"),
           "5 minutes. Keep the sheet: you will fill the ANSYS column later.",
           notes="Answers: 0.5897 °C (Heat Transfer Part 2, Table 2.1); 0.192 m and 0.131 m (Plane Stress Part 2); the hand calculation is the 4-node linear element; Mechanical’s default element order for solids is quadratic (8-node), ‘Program Controlled’.")

outs = ["Build a 2D steady-state thermal model and a 2D plane-stress model in ANSYS Workbench from a sketch, with units, material, mesh, supports and loads entered correctly.",
        "Map every ANSYS object to the hand calculation of the heat-transfer and plane-stress sessions (element order, consistent loads, essential and natural conditions, averaged versus element stresses, reactions).",
        "Run a mesh-refinement study, tabulate it, and check the model against one independent calculation before reading any contour plot.",
        "Recognise four classic modelling mistakes from their symptoms, and get your project model to a verified first run."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("CLO4 session: course information the ANSYS demo — computer-based modelling of 2D plane stress problems and interpretation of FEM results.", "why"),
          notes="Four outcomes. The third is the one the project is marked on.")

D.content("session", "Session map · 180 minutes", "Two demos, one mesh study, four mistakes, then your own model",
          session_map([("0:00", "Workbench & vocabulary", 30, "A1 · 8 min", False), ("0:30", "Demo 1: heat plate", 30, "A2 · 5 min", False), ("1:00", "Demo 2: cantilever", 35, "A3 + QR", False),
                       ("1:35", "Break", 10, "", True), ("1:45", "Stresses & wrong models", 30, "A4 · 8 min", False), ("2:15", "Project lab", 35, "A5 · 35 min", False), ("2:50", "Wrap-up", 10, "Exit ticket", False)])
          + row(D.card(D.h3("Bring forward") + D.ul(["Heat Transfer Part 2: plate results 0.6214 (2 × 2), 0.5898 (16 × 16), 0.5897 (software).", "Plane Stress Part 2: cantilever 0.131 (2 × 2), 0.192 (converged), Timoshenko check.", "Plane Stress Part 3: centroid vs nodal stress; the singular corner; Q4 vs Q8."], 28), extra="flex:1"),
                D.card(D.h3("Lab logistics") + D.ul(["One laptop per group with ANSYS Student / Workbench open before 0:30.", "Unit system: Metric (m, kg, N, s, V, A) — set it first.", "Save projects as [group]_W14.wbpj in [folder]."], 28), extra="flex:1"), align="stretch"),
          notes="Ask the groups to open Workbench during Block 1 so that no time is lost at 0:30. Confirm the save location and the lab’s ANSYS version beforehand.")

# =============================================================================
# Block 1 — Workbench & vocabulary
# =============================================================================
D.divider("d1", "1", "From the textbook to Workbench", "The six cells of a Workbench analysis are the six steps of the hand calculation. Same mathematics, different names.",
          "Block 1 · 0:00 – 0:30", section="Block 1: the Workbench workflow mapped onto the hand calculation, the ANSYS vocabulary and the unit conversions the inputs need",
          notes="Thirty minutes. The aim is that nothing in the software looks new: every object has a name from the heat-transfer and plane-stress sessions.")

D.content("wbflow", "Block 1 · the workflow", "Six Workbench cells, six steps you have already done by hand",
          col(img(WB, "The six Workbench cells, Engineering Data to Results, above the matching steps of the hand calculation: material matrix, domain, element matrices, boundary conditions, solve, post-processing", 1300, 450),
              callout("Engineering Data is [E] or k; Geometry is the domain; Mesh chooses the shape functions; Setup is {r} and the essential conditions; Solution solves [K]{U} = {R}; Results is [E][B]{û}.", "why", 25)),
          notes="Walk left to right. The dashed lines are the point of the slide: each cell is a step the class has done with pen and paper.")

D.content("w14-mapdl", "Block 1 · the same sequence in MAPDL", "Lines, area, mesh, solve: a corner bracket in ANSYS MAPDL",
          row(panel("1 · Lines", B1, "Numbered lines that outline an L-shaped bracket", 360, 263), panel("2 · Area", B2, "The bracket as a filled area", 360, 261),
              panel("3 · Mesh (PLANE183)", B3, "Quadrilateral mesh of the bracket", 360, 261), panel("4 · Solve: von Mises", B4, "Von Mises stress on the bracket", 380, 262), align="start", gap=20)
          + callout("Workbench hides these steps behind its cells; MAPDL and its Python interface expose them as commands. Same element, same plane-stress idealisation, same the heat-transfer and plane-stress sessions mathematics.", "why", 26)
          + credit("Images: PyMAPDL documentation, “Static analysis of a corner bracket” (adapted from the classic Ansys APDL tutorial), © ANSYS, Inc., MIT licence, mapdl.docs.pyansys.com."),
          notes="Optional context for students who will meet MAPDL or PyMAPDL in industry or research. The four panels are the same stages as the Workbench cells on the previous slide: geometry, mesh, solution, results.")

D.content("vocab", "Block 1 · vocabulary", "ANSYS object ↔ textbook quantity",
          col(table(["In Mechanical", "In the textbook (the heat-transfer and plane-stress sessions)", "Where it bit you by hand"],
                    [["Element order: Linear / Quadratic (PLANE182 / PLANE183; thermal PLANE55 / PLANE77)", "4-node Q4 (2.21) / 8-node Q8 (2.31)", "shear locking of Q4 in bending (Plane Stress Part 2)"],
                     ["Element Size, Edge Sizing (number of divisions), Face Meshing", "a, b and the structured mesh", "convergence table (heat transfer, plane stress)"],
                     ["Fixed Support · Displacement · Temperature", "essential (Dirichlet) conditions: rows deleted, Û known", "reduced system (Heat Transfer Part 2)"],
                     ["Force on an edge · Pressure · Heat Flux · Internal Heat Generation", "natural (Neumann) conditions and sources: {b}, {q}, {r}", "consistent nodal loads qb/2 and 1/6–2/3–1/6"],
                     ["No condition on an edge", "insulated / traction-free: q_b = 0, boundary integral vanishes", "Heat Transfer Part 1 Activity 3"],
                     ["Averaged · Unaveraged · Elemental Mean (stress display)", "nodal averaging · element values · centroid value", "Plane Stress Part 3 Block 2"],
                     ["Reaction probe", "[K]{U} − {R} at the fixed dofs", "equilibrium check (Plane Stress Part 3 report)"]], [38, 36, 26], 25)),
          notes="Keep this slide available during both demos; point at the row each time an object is created. The element names (PLANE182 etc.) appear in the solver output file and in the element-type legend.")

D.content("units", "Block 1 · inputs the software asks for", "Units first, then the five numbers of each problem",
          two_col(D.card(D.h3("Cantilever (text §3.4) · Static Structural") + D.ul(["Unit system: Metric (m, kg, N, s, V, A).", "Geometry: 4 m × 2 m surface body in XY; Analysis Type = 2D (Geometry cell properties) before importing or sketching.",
                                                                                   "2D Behavior = Plane Stress; Thickness = 0.01 m.", "Material: Isotropic Elasticity, E = 2 × 10⁸ Pa, ν = 0.33 — the textbook’s value, a thousand times softer than steel; keep it so the numbers match the book.",
                                                                                   "Fixed Support on the left edge; the load on the right edge — converted in Activity 1."], 26, gap=8)),
                  D.card(D.h3("Plate (text §2.3) · Steady-State Thermal") + D.ul(["Same unit system; 1 m × 1 m surface body, Analysis Type = 2D.", "Material: Isotropic Thermal Conductivity k = 300 W m⁻¹ K⁻¹ (the §2.3 figure says 400 — erratum).",
                                                                                 "Internal Heat Generation = 600 W m⁻³ on the body.", "Temperature = 0 °C on the top and left edges; nothing on the other two.",
                                                                                 "Thickness does not change the temperature field; it scales the heat-flow reactions."], 26, gap=8)),
                  align="stretch")
          + callout("A wrong unit system is the most common failure in student projects: a geometry drawn in mm with loads in N and E in Pa is a model of a different structure.", "warn", 26),
          notes="If the lab version shows ‘Analysis Type’ elsewhere, the rule is the same: the geometry must be declared 2D before Mechanical opens. Mention that Mechanical shows units on every input field — read them.")

D.activity("act1", 1, 8, "pairs · conversion", "Convert the textbook data for the dialog boxes",
           D.card(D.h3("Fill in") + table(["Textbook", "ANSYS input", "Value"],
                                          [["q<sub>y</sub> = 5 kN m⁻¹ down, right edge, t = 0.01 m", "Force on the edge, components", "F<sub>y</sub> = ?"], ["same load", "Pressure, components", "p<sub>y</sub> = ?"],
                                           ["E = 200 × 10⁶ N m⁻²", "Young’s Modulus", "? Pa"], ["2 × 2 hand mesh of the cantilever", "Edge Sizing, divisions (top/bottom, left/right)", "?, ?"],
                                           ["16 × 16 plate mesh", "Element Size (with Face Meshing)", "? m"], ["the hand element", "Element Order", "?"]], [40, 36, 24], 25), extra="width:1080px"),
           D.card(D.h3("Then check") + D.ul(["Multiply the pressure by the edge area (length × thickness): do you get the total load back?", "Why are the two edge-sizing numbers different for the cantilever?"], 28, gap=10), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: F_y = −10 000 N (5 kN/m × 2 m); p_y = −500 kPa (5000/0.01); E = 2e8 Pa; Edge Sizing 2 and 2 (gives 2 m × 1 m elements, the textbook mesh — Element Size 1 m would give 4 × 2); Element Size 0.0625 m; Linear. "
                 "Check: 500e3 × 2 × 0.01 = 10 000 N. The cantilever’s hand mesh has rectangular 2 × 1 m elements, so divisions by edge, not a single element size.")

D.content("act1-reveal", "Activity 1 · solution", "Total force or pressure: both put −10 kN on the edge, distributed consistently",
          col(D.eqpanel("t_load_conv", None, colw=1664, maxh=90, pad="12px 32px"), D.eqpanel("t_check_load", None, colw=1664, maxh=60, pad="12px 32px"),
              two_col(D.card(D.h3("The rest") + D.ul(["E = 2 × 10⁸ Pa; ν = 0.33.", "Edge Sizing: 2 divisions on every edge of the cantilever → the 2 m × 1 m elements of the text; Face Meshing for a mapped (structured) mesh.",
                                                     "Element Size 0.0625 m on the plate → 16 × 16.", "Element Order: Linear for the hand element; Quadratic is the default."], 26, gap=6)),
                      callout("Mechanical converts an edge Force into consistent nodal loads itself — the qb/2 (linear) or 1/6–2/3–1/6 (quadratic) of Plane Stress Parts 2–3. You never type nodal loads.", "ok", 26), lw=1000, align="start")),
          notes="Make the point that the software does the Plane Stress Part 2 load integration; the student’s job is the conversion of the physical load into the dialog’s quantity.")

# =============================================================================
# Block 2 — Demo 1: heat plate
# =============================================================================
D.divider("d2", "2", "Demo 1 · the heat plate", "Steady-State Thermal, 1 m square, two cold edges, two insulated edges, uniform heat source. Predicted before Solve: 0.6214 on the hand mesh, 0.5897 converged.",
          "Block 2 · 0:30 – 1:00", section="Block 2: live demonstration of the text §2.3 plate in Steady-State Thermal — set-up, prediction, run, comparison with the hand results",
          notes="Thirty minutes, live. Build the model from scratch on screen; students follow on their laptops. Do not skip the moment of writing the prediction on the board before pressing Solve.")

D.content("plate-setup", "Demo 1 · the model in ANSYS terms", "Every object on this sketch is a line of the Heat Transfer Part 2 hand calculation",
          two_col(img(PLATE, "The plate with its ANSYS boundary conditions: Temperature zero on the top and left edges, nothing on the other two edges, Internal Heat Generation on the body, and a temperature probe at the bottom-right corner", 760, 560),
                  col(D.card(D.h3("Build order (click path in the notes)") + D.ul(["Steady-State Thermal system → Engineering Data: new material, Isotropic Thermal Conductivity 300.", "Geometry (2D): sketch a 1 m square; one surface body.",
                                                                                   "Mesh: Face Meshing + Element Size 0.5 m, Element Order Linear → the hand mesh.", "Temperature 0 °C on top and left edges; Internal Heat Generation 600 W m⁻³ on the body.",
                                                                                   "Solve → Temperature contour; Probe at the bottom-right vertex; Total Heat Flux vectors."], 25, gap=6)),
                      callout("Nothing is applied on the right and bottom edges. In the weak form that is q<sub>b</sub> = 0 — insulated — exactly as in Heat Transfer Part 1 Activity 3.", "why", 24)),
                  lw=792, align="start"),
          notes="Script: (1) Toolbox → Steady-State Thermal, drag to the schematic. (2) Geometry cell → Properties → Advanced Geometry Options → Analysis Type: 2D. (3) Engineering Data: add material ‘plate’, Isotropic Thermal Conductivity = 300 W/m·K. "
                "(4) Geometry: new sketch on XY plane, rectangle 1 × 1 m, Surfaces From Sketches. (5) Model: assign material to the body. Mesh → insert Face Meshing on the face; Sizing → Element Size 0.5 m; Mesh details → Element Order: Linear. Generate: 4 elements, 9 nodes. "
                "(6) Steady-State Thermal → Temperature on the top edge and left edge (Ctrl-select), magnitude 0 °C; Internal Heat Generation on the body, 600 W/m³. (7) Solve. Insert Temperature result and a Temperature probe on the bottom-right vertex; insert Total Heat Flux (vector display). "
                "Expected nodal temperatures with 4 linear elements (Heat Transfer Part 2, text (2.55)): T2 = 0.4821 at the bottom mid-edge, T3 = 0.6214 at the bottom-right corner, T5 = 0.3857 at the centre, T6 = 0.4821 at the right mid-edge.")

D.activity("act2", 2, 5, "pairs · prediction", "Predict before Solve is pressed",
           D.card(D.h3("Fill the prediction column") + table(["Run", "Prediction (Heat Transfer Part 2)", "ANSYS (fill in live)"],
                                                            [["4 linear elements (0.5 m), T at the bottom-right corner", "?", ""], ["4 linear elements, T at the mid-point of the bottom edge", "?", ""],
                                                             ["256 linear elements (0.0625 m), corner", "?", ""], ["4 quadratic elements, corner", "?", ""]], [52, 24, 24], 26), extra="width:1060px"),
           D.card(D.h3("And sketch") + D.ul(["The direction of the heat-flux vectors on the insulated edges.", "Where the hottest point must be, and why."], 28, gap=10), extra="flex:1"),
           "5 minutes. Then we run the four cases.",
           notes="Answers: 0.6214; 0.4821; 0.5898; with 4 quadratic elements the text’s Q8 2 × 1 gives 0.5836 — with 4 quadratic elements (2 × 2) expect a value between that and 0.5897 (the course solver has no Q8 thermal element; record the ANSYS value: [___]). "
                 "Flux vectors run parallel to an insulated edge (no normal component); the hottest point is the corner farthest from both cold edges.")

D.content("plate-compare", "Demo 1 · compare and explain", "Linear 2 × 2 in ANSYS = the hand calculation; the difference should be in the fourth decimal",
          col(table(["Run", "Hand / text", "ANSYS [your run]", "Comment"],
                    [["4 linear elements, corner", "0.6214", "[ ]", "same element, same consistent {q}: should agree to 3–4 decimals"], ["4 linear elements, bottom mid-edge", "0.4821", "[ ]", "ditto"],
                     ["256 linear elements, corner", "0.5898", "[ ]", "Table 2.1"], ["4 quadratic elements, corner", "≈ 0.584–0.590", "[ ]", "Q8 2 × 1 gives 0.5836 (text)"], ["software, text Table 2.1", "0.5897", "—", "converged reference"]], [30, 22, 18, 30], 25),
              D.eqpanel("t_heat_check", None, colw=1664, maxh=100, pad="12px 32px"),
              callout("The reaction probe on the Temperature conditions is the independent check: heat out through the cold edges must equal the heat generated in the body.", "ok", 24)),
          notes="If the linear 2 × 2 run does not match 0.6214, the mesh is not the 2 × 2 one (check the node count: 9) or the element order is quadratic. Both are common and both are teachable. "
                "Reaction check: heat generated = 600 W/m³ × 1 m² × t; Mechanical reports the reaction on each Temperature condition in watts (per the model thickness).")

# =============================================================================
# Block 3 — Demo 2: cantilever
# =============================================================================
D.divider("d3", "3", "Demo 2 · the cantilever", "Static Structural, plane stress, 4 m × 2 m, t = 0.01 m. Predicted: 0.131 m on the hand mesh with linear elements, 0.192 m converged.",
          "Block 3 · 1:00 – 1:35", section="Block 3: live demonstration of the text §3.4 cantilever in Static Structural — linear versus quadratic elements, the mesh study and the convergence table",
          notes="Thirty-five minutes. Set the first model up live (ten minutes), then hand the mesh study to the groups (Activity 3).")

D.content("cant-setup", "Demo 2 · the model in ANSYS terms", "Fixed Support, an edge force, plane stress with thickness — then the mesh of Plane Stress Part 2",
          two_col(col(img(CANT, "The cantilever with its ANSYS inputs: Fixed Support on the left edge, a Force of minus ten kilonewtons in y on the right edge or an equivalent pressure, plane stress behaviour with thickness 0.01 metre, and a deflection probe at the tip", 900, 380),
                      callout("First number to read is not the deflection: it is the reaction. +10 000 N in Y, moment 40 000 N m, or something is wrong.", "warn", 24)),
                  D.card(D.h3("Build order (click path in the notes)") + D.ul(["Static Structural → Engineering Data: new material, Isotropic Elasticity E = 2 × 10⁸ Pa, ν = 0.33.", "Geometry (2D): 4 m × 2 m surface body; in Mechanical: 2D Behavior = Plane Stress, Thickness = 0.01 m.",
                                                                              "Mesh: Face Meshing; Edge Sizing 2 divisions on all edges; Element Order Linear.", "Fixed Support on the left edge; Force on the right edge, components, Y = −10 000 N.",
                                                                              "Solve → Directional Deformation (Y); probe at the top-right vertex; Force Reaction on the Fixed Support."], 24, gap=5)),
                  lw=932, align="start"),
          notes="Script: Toolbox → Static Structural; Geometry → Analysis Type 2D; sketch 4 × 2 m rectangle, Surfaces From Sketches; Mechanical → Geometry → 2D Behavior: Plane Stress; surface body → Thickness 0.01 m; assign material. "
                "Mesh → Face Meshing; Edge Sizing on the four edges: Number of Divisions 2 (set Behavior: Hard); Mesh details → Element Order: Linear; Generate → 4 elements, 9 nodes. "
                "Static Structural → Fixed Support (left edge); Force (right edge) → Define By: Components, Y = −10000 N. Solve. Insert Directional Deformation Y; Deformation Probe at the top-right vertex; Force Reaction probe (Boundary Condition: Fixed Support), and a Moment Reaction probe. "
                "Element Control note: Mechanical may apply an enhanced-strain formulation to linear elements (‘Program Controlled’). If the 2 × 2 linear result is much better than 0.131 m, say so and show Element Control: Manual with full integration for comparison; either way, discuss, do not hide.")

D.content("predict", "Demo 2 · predictions from the course solvers", "Linear elements lock; quadratic elements converge with a tenth of the dofs",
          two_col(img(CONV, "Tip deflection against degrees of freedom on a log axis for linear four-node and quadratic eight-node meshes, both converging to the Timoshenko value of 0.192 metres; the quadratic curve starts at 0.178 with 26 dofs, the linear curve at 0.131 with 18 dofs", 940, 520),
                  col(table(["Mesh (N<sub>x</sub> × N<sub>y</sub>)", "Linear (m)", "Quadratic (m)"], [["2 × 2 / 2 × 1", "0.131", "0.178"], ["8 × 4", "0.182", "0.191"], ["16 × 8", "0.189", "0.191"], ["32 × 16", "0.191", "0.192"], ["Timoshenko", "0.192", "0.192"]], [40, 30, 30], 26),
                      callout("ANSYS’s linear element (PLANE182) is not formulated exactly like the textbook Q4; expect the same trend and close numbers, not identical ones. Record what you get.", "why", 24)),
                  lw=972, align="start"),
          notes="The chart and table come from the course Python solvers (Q4 closed-form stiffness; Q8 with 3 × 3 Gauss) and reproduce the text’s Tables 3.1 and 3.2 (0.131, 0.178, 0.189). Lecturer: run the 2 × 2 linear and 2 × 1 quadratic cases before class and note the values here: linear [___], quadratic [___].")

qr_lab(D, "qr-predict", 6, "Before you press Solve: the expected numbers on your phone",
       ["Cantilever Explorer: 8-node 2 × 1 and 8 × 4. Write both tip deflections in your prediction column.",
        "Stress Recovery Explorer: 8-node 16 × 8, Elemental mean. Probe (2.0, 1.5): what σ<sub>xx</sub> should ANSYS show there?",
        "Cantilever Explorer, “More to try”: produce each wrong-model signature before you see it in ANSYS."],
       [LABS["cant"], LABS["stress"]], "6 minutes. ANSYS’s PLANE183 is the 8-node element; expect agreement to about 1%, not to the last digit.",
       notes="Both QR codes open the public copies on GitHub Pages (no login): open them once on a phone before class. "
             "Answers: (1) −0.178 m and −0.1906 m. (2) About 1500 kN/m² (beam theory 1500 at mid-span, 0.5 m above the neutral axis). "
             "(3) Plane strain −10%; point force +20% at the loaded node; vertical-only support refused; thickness 1 m → deflection ÷ 100.")

D.activity("act3", 3, 10, "groups · mesh study", "Run the mesh study and write the convergence table",
           D.card(D.h3("Do, in your group") + D.ul(["Quadratic elements, Edge Sizing (N<sub>x</sub>, N<sub>y</sub>) = (2, 1), (4, 2), (8, 4), (16, 8). Record nodes, tip deflection v at the top-right vertex, and the reaction.",
                                                    "Compute the change between successive meshes with the formula below.", "Switch the 8 × 4 case to Linear: how much stiffer?", "Decide which mesh you would report, and why."], 28, gap=8), extra="width:1060px"),
           col(D.card(D.h3("Change between meshes") + D.p("(v<sub>fine</sub> − v<sub>coarse</sub>) / v<sub>fine</sub> × 100%", 28) + D.p("Report the first mesh after which the change is below your tolerance (say 2%).", 24, MUTED)),
               callout("Mesh → Statistics shows nodes and elements. Dofs = 2 × nodes for plane stress.", "ok", 24), extra="flex:1"),
           "10 minutes. One group reads out its table.",
           notes="Expected (course solver, quadratic): 0.178, 0.1885, 0.1906, 0.1913 m; changes 5.6%, 1.1%, 0.35%. Linear 8 × 4: 0.182 (course solver). Report the 8 × 4 or 16 × 8 quadratic mesh: change below 1%. "
                 "Reaction must read +10 000 N on every mesh — it is independent of refinement.")

D.content("act3-reveal", "Activity 3 · solution", "Converged to within 0.35% at 8 × 4 quadratic; the linear element needs 16 × 8 for the same",
          col(table(["Quadratic mesh", "Nodes", "Dofs", "v<sub>tip</sub> (m)", "Change from previous", "Reaction R<sub>y</sub> (N)"],
                    [["2 × 1", "13", "26", "−0.178", "—", "+10 000"], ["4 × 2", "37", "74", "−0.189", "5.6%", "+10 000"], ["8 × 4", "121", "242", "−0.191", "1.1%", "+10 000"], ["16 × 8", "433", "866", "−0.191", "0.35%", "+10 000"]], [22, 12, 12, 18, 20, 16], 26),
              row(callout("Report the 8 × 4 quadratic mesh (or finer); say so in one sentence with the 0.35%. Timoshenko 0.192 m is the independent check: 0.7% away.", "ok", 26),
                  callout("The reaction never changes with the mesh: equilibrium is exact for any mesh. It checks the loads and supports, not the accuracy.", "why", 26), align="stretch")),
          notes="Values are from the course Q8 solver; the groups’ ANSYS values should be within about 1% of these. Then break.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:35 – 1:45</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: reading stresses, four wrong models, and your project model.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True), notes="Ten minutes. Groups keep their cantilever model open: it is reused after the break.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Stresses and wrong models
# =============================================================================
D.divider("d4", "4", "Stresses on screen, and four wrong models", "What the contour plot averages, where its maximum lies, and how a modelling mistake shows up in the numbers.",
          "Block 4 · 1:45 – 2:15", section="Block 4: reading stress results in Mechanical, the reaction check, and four deliberately wrong versions of the cantilever and their symptoms",
          notes="Thirty minutes. Use the groups’ 16 × 8 quadratic model for the stress plots, then build the four wrong models live (each is a one-field change).")

D.content("stress-read", "Block 4 · reading stresses in Mechanical", "Three display options, three things from Plane Stress Part 3",
          col(table(["Result object", "Display option", "Textbook meaning (Plane Stress Part 3)", "Use it for"],
                    [["Normal Stress (X axis)", "Averaged", "nodal average of element values", "contour plots away from boundaries"], ["Normal Stress (X axis)", "Unaveraged", "element values at the nodes", "seeing how rough the mesh still is"],
                     ["Normal Stress (X axis)", "Elemental Mean", "the centroid value", "the number to compare with M(y − 1)/I"], ["Equivalent (von Mises)", "any", "σ<sub>vM</sub> of (3 components)", "steel yield check"],
                     ["Maximum Principal", "any", "σ<sub>1</sub>", "concrete cracking, direction of reinforcement"], ["Stress Probe at a vertex", "—", "[E][B]{û} at a point", "a checkable number at a chosen location"]], [24, 18, 32, 26], 25),
              row(callout("The Max tag of every stress plot of this cantilever sits at the fixed corner. That is the singularity of Plane Stress Part 3: it grows with refinement and is not a design stress.", "warn", 25),
                  callout("Check: Elemental Mean σ<sub>x</sub> in an element at mid-span, mid-depth ± 0.5 m, against M(y − 1)/I. Within a few per cent on the 16 × 8 mesh.", "ok", 25), align="stretch")),
          notes="Show Averaged and Unaveraged side by side: jumps between elements are the discretisation error made visible. Then Elemental Mean and a probe at (2, 1.5): beam theory gives 10 000 × 2 × 0.5 / 6.667e-3 = 1500 kN/m². "
                "Display Option is in the result’s details under Integration Point Results.")

D.content("reaction", "Block 4 · the first check is always the reaction", "Before a single contour plot: do the supports carry what was applied?",
          col(D.eqpanel("t_reaction", None, colw=1664, maxh=130, pad="12px 32px"),
              row(D.card(D.h3("Force Reaction probe") + D.p("Boundary Condition: Fixed Support. Expect X = 0, Y = +10 000 N for any mesh and either element order.", 27), extra="flex:1"),
                  D.card(D.h3("Moment Reaction probe") + D.p("Summation about the support: 40 000 N m. Check the sign convention of the summation point before reading it.", 27), extra="flex:1"),
                  D.card(D.h3("What a wrong value means") + D.p("The load was entered in the wrong unit or direction, or a support is missing or doubled. Fix that before anything else.", 27), extra="flex:1"), align="stretch")),
          notes="Equilibrium holds exactly for every mesh, so a wrong reaction is never a mesh problem; it is an input problem. This is the single most useful habit for the project.")

D.content("wrong", "Block 4 · four wrong models, each a one-field change", "Four mistakes, four signatures (course-solver numbers, 32 × 16 mesh)",
          col(img(WRONG, "Four deliberately wrong versions of the cantilever model: plane strain instead of plane stress, a force on a single vertex, a support that fixes only the vertical direction, and a thickness left at its default", 1100, 250),
              table(["Mistake", "Symptom in the results", "Why"], [["(a) 2D Behavior: Plane Strain", "tip 0.172 m, not 0.191 m (−10%)", "stiffer [E]: ratio ≈ 1 − ν² = 0.89"], ["(b) Force on the top-right vertex", "tip node 0.230 m (+20%); von Mises under the load 10×; mid-span unchanged", "point load = singularity; St-Venant"],
                                                                 ["(c) Displacement Y = 0 only", "rigid-body warning; weak springs; huge x-displacement", "nothing stops translation in x"], ["(d) Thickness left at default", "tip 0.0019 m for t = 1 m: a clean factor of 100", "v ∝ 1/t"]], [28, 46, 26], 25)),
          notes="Numbers: plane strain 32 × 16: Q8 0.1722 m (Q4 0.1712 m); point load Q8 32 × 16: v = 0.2298 at the loaded node, 0.1874 at mid-depth, element under the load σ_vM 5353 vs 523 kN/m² with the edge traction, mid-span top element σ_x 2924 vs 2900. "
                "(c) Mechanical offers to add weak springs; the warning is the lesson. (d) If the thickness is not set, check what the lab version assumes; the scaling argument holds whatever the default.")

D.activity("act4", 4, 8, "pairs · diagnosis", "Spot the wrong model from its numbers",
           D.card(D.h3("Four runs of the cantilever, 32 × 16 quadratic") + table(["Run", "Reaction Y (N)", "Tip v (m)", "Max von Mises (kN m⁻²)", "Note"],
                                                                                  [["A", "+10 000", "−0.0019", "at the fixed corner", ""], ["B", "+10 000", "−0.230", "at the top-right vertex", "mid-span stresses normal"],
                                                                                   ["C", "+10 000", "−0.172", "at the fixed corner", "σ<sub>zz</sub> ≠ 0 in the results"], ["D", "+10 000", "−0.191", "at the fixed corner", "warning: 1 rigid-body mode"]], [10, 22, 18, 28, 22], 25), extra="width:1120px"),
           D.card(D.h3("For each run") + D.ul(["Which of the four mistakes (a)–(d), or none?", "One sentence of evidence.", "Is the corner maximum itself a mistake?"], 28, gap=10), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: A → (d) thickness (factor 100); B → (b) vertex force (deflection +20%, max at the loaded vertex); C → (a) plane strain (−10%, σ_zz present); D → (c) under-constrained (rigid-body warning; the deflection may still look right once weak springs are added — the warning is the evidence). "
                 "The corner maximum is not a mistake; it is the expected singularity of a fully fixed edge.")

D.content("act4-reveal", "Activity 4 · solution", "Every mistake leaves a signature: a factor, a location, a warning, or an extra stress component",
          col(table(["Run", "Mistake", "Signature"], [["A", "(d) thickness at default", "deflection off by a clean power of ten; reaction unchanged"], ["B", "(b) force on a vertex", "max stress at the loaded vertex; tip node deflects more than its neighbours; mid-span unchanged"],
                                                      ["C", "(a) plane strain", "deflection −10%; a σ<sub>zz</sub> appears in the results"], ["D", "(c) under-constrained", "rigid-body-mode warning; weak springs added by the solver"]], [10, 30, 60], 27),
              row(callout("The reaction was right in all four runs: equilibrium does not catch idealisation errors. Only a prediction or an independent check does.", "why", 26),
                  callout("For the project: a wrong reaction = input error; a right reaction with a wrong deflection = idealisation error. Different fixes.", "ok", 26), align="stretch")),
          notes="Transition to the lab block: the groups now apply exactly this sequence — reaction, hand estimate, then refinement — to their own model.")

# =============================================================================
# Block 5 — Project lab
# =============================================================================
D.divider("d5", "5", "Project lab · first verified run", "Your structure, your model plan from Plane Stress Part 3, one coarse mesh, one reaction check, one hand estimate. Lecturers circulate.",
          "Block 5 · 2:15 – 2:50", section="Block 5: groups build and run the first mesh of their project model with a verification checklist; lecturers review each group's plan",
          notes="Thirty-five minutes. Visit every group once; ask the two questions: what is your hand check, and what is free and what is fixed.")

D.content("checklist", "Block 5 · the first-run checklist", "In this order; stop at the first failure and fix it",
          f'<div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:16px">'
          + "".join(f'<div style="background:{WHITE};border:1px solid {HAIR};border-radius:14px;padding:18px 20px;display:flex;flex-direction:row;gap:16px;align-items:start">'
                    f'<p style="font-family:{SERIF};font-size:48px;font-weight:600;line-height:1;color:{MAROON}">{i+1}</p><div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:27px;font-weight:600;line-height:1.2;color:{DARK}">{t}</p><p style="font-size:24px;line-height:1.3;color:{BODY}">{s}</p></div></div>'
                    for i, (t, s) in enumerate([("Units & 2D", "Metric (m, kg, N); Analysis Type 2D; plane stress or strain stated"), ("Geometry", "dimensions checked against the sketch; thickness entered"), ("Material", "E, ν (or k) with units; source written down"),
                                                 ("Supports", "only what is really restrained; nothing free is fixed"), ("Loads", "tractions on edges, body force; no vertex forces"), ("Coarse mesh", "quadratic, a few elements; it must solve"),
                                                 ("Reaction", "equals the applied load, right sign"), ("Hand estimate", "deflection or stress within a factor of 2 — then refine")])) + "</div>"
          + row(callout("Deliverable at 2:50: a screenshot of the reaction probe and the coarse-mesh result, and the hand estimate written on the model plan. The refinement study is homework for the report.", "ok", 26),
                callout("A model that fails step 7 or 8 is not refined; it is fixed. Refinement never repairs an idealisation.", "warn", 26), align="stretch"),
          notes="Steps 7 and 8 are the gate. Groups that pass both in the lab can start the refinement study at once.")

D.content("w14-verify", "Block 5 · what a verified result looks like", "Predict K<sub>t</sub>, resolve the hot spot, compare: 2.34 against 2.35",
          row(panel("1 · Geometry", H1, "Outline of a long plate with a central circular hole", 500, 155), panel("2 · Mesh refined at the hole", H2, "Mesh with many small elements around the hole", 520, 146),
              panel("3 · Von Mises", H3, "Von Mises stress highest at the edge of the hole", 480, 341), align="start", gap=20)
          + row(callout("Predicted before Solve: Peterson K<sub>t</sub> = 2.35 for d/W = 0.3. Computed: 2.34. Reported with the signed difference (−0.4%).", "ok", 26),
                callout("This is the standard for your project: a hand-check number, a mesh that resolves the hot spot, and the comparison in one sentence.", "why", 26), align="stretch")
          + credit("Images: PyMAPDL documentation, “MAPDL 2D plane stress concentration analysis”, © ANSYS, Inc., MIT licence."),
          notes="Use this as the model for the project's verification paragraph. A group with a gusset plate or a wall opening can use exactly this check (Peterson's chart for a hole or a notch).")

D.activity("act5", 5, 35, "groups · project lab", "Build the first mesh of your project model and verify it",
           D.card(D.h3("Do") + D.ul(["Open the model plan returned from Plane Stress Part 3; build steps 1–6 of the checklist.", "Solve on the coarse mesh; read the reaction probe first; compare with the applied load.",
                                     "Write the hand estimate (beam theory, statics, or a stress-concentration factor) next to the FE value.", "If both agree within a factor of 2, run the second mesh; if not, find the input error before refining.",
                                     "Save as [group]_project.wbpj; screenshot the reaction probe and the result."], 28, gap=8), extra="width:1060px"),
           col(D.card(D.h3("Lecturer visits — be ready to answer") + D.ul(["What is free and what is fixed, and why?", "What is your hand check?", "Where will the stress maximum be, and is it a singularity?"], 27, gap=8)),
               figbox(D11.fig("fig_shearwall", height=180)), extra="flex:1"),
           "35 minutes. Hand in the screenshots and the annotated plan at 2:50.",
           notes="Common first-run problems: geometry in mm; thickness not set; a point force at a vertex; the whole bottom edge fixed when it should be a bearing; a missing BC in the in-plane direction (rigid-body warning).")

# =============================================================================
# Block 6 — Wrap-up
# =============================================================================
D.divider("d6", "6", "Wrap-up", "The habit of the course, the exit ticket, and what the last session adds.",
          "Block 6 · 2:50 – 3:00", section="Block 6: summary of the hand-versus-software comparison, exit ticket and the bridge to the last session’s practical issues",
          notes="Ten minutes. Collect the screenshots and the annotated plans.")

D.content("summary-hv", "Block 6 · hand calculation versus software, in one table", "The software is faster; it is not more right",
          col(table(["Question", "By hand (the heat-transfer and plane-stress sessions)", "In ANSYS (today)"], [["Which element?", "you derived Q4; you read about Q8", "Element Order: Linear / Quadratic — default quadratic"], ["Loads on nodes", "qb/2; 1/6–2/3–1/6", "automatic from Force / Pressure / Heat Generation"],
                                                                               ["Essential conditions", "rows deleted, Û = 0", "Fixed Support, Displacement, Temperature"], ["Insulated / free edge", "q<sub>b</sub> = 0: do nothing", "apply nothing"],
                                                                               ["Accuracy", "convergence table, Timoshenko", "the same table, from a mesh study you run"], ["Stresses", "[E][B]{û} at a point; centroid is honest", "Averaged / Unaveraged / Elemental Mean"],
                                                                               ["Equilibrium", "[K]{U} − {R}", "Reaction probe — the first check"]], [22, 38, 40], 26),
              D.eqpanel("t_predict", None, colw=1664, maxh=50, pad="10px 32px")),
          notes="One line to close: the software did the Plane Stress Part 2 integration and the Heat Transfer Part 2 assembly for you; the judgement — idealisation, convergence, checks — stayed with you.")

D.activity("exit", 6, 5, "individual · exit ticket", "Three questions before you leave",
           D.card(D.h3("Questions") + D.ul(["Your ANSYS reaction is +10 000 N but the tip deflection is 0.0019 m. What do you check first?",
                                            "Which display option gives the stress value closest to the centroid value you computed in Plane Stress Part 3?",
                                            "Your mesh study shows 0.35% change between the last two meshes, but the maximum stress still rises 18%. Explain."], 30, gap=12), extra="width:1300px"),
           None,
           "Five minutes. Name and matric number; for feedback, not marks.",
           notes="Answers: (1) thickness (and the unit system) — the reaction is right, so the load is right; a factor of 100 points at t. (2) Elemental Mean. (3) The deflection has converged; the maximum stress sits at the fixed corner, a singularity, and will keep rising — it is not a reportable value.")

D.content("summary", "Wrap-up · before the last session", "The last session closes the course: practical issues, then the project submission",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["Every Workbench cell is a step you did by hand; predict before Solve.", "Reaction first; then a hand estimate; then refine — in that order.",
                                                              "Quadratic elements converge with a tenth of the dofs; linear ones lock in bending.", "Four mistakes, four signatures: a factor, a location, a warning, an extra stress."], 28, gap=10)),
                  col(D.card(D.h3("Last session · practical issues in FEM (course information)") + D.ul(["Modelling considerations: symmetry, idealisation of supports and connections, when 2D is enough.",
                                                                                              "Convergence and accuracy: h-refinement, element order, singularities, what to report.", "Result interpretation for design; course wrap-up and exam guidance.",
                                                                                              "Project: report and presentation due [date]; bring the convergence table."], 27, gap=8)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=820),
          notes="Close on time. Remind the groups that the refinement study and the five-sentence results paragraph (Plane Stress Part 3) are the core of the report.")

order = D.write("2026-10-26T17:40:00Z")
print(len(order), "slides:", order)
