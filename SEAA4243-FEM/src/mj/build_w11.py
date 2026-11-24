import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w11"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w11" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — Plane Stress (Part 1)", "SEAA 4243 · Plane Stress — Part 1", HERE / "eqs_w11", HERE / "figs_w11", eq_rep)
D9 = Deck(ROOT, "", "", HERE / "eqs_w9", HERE / "figs_w9", {x["name"]: x for x in json.loads((HERE / "eqs_w9" / "_report.json").read_text())})

# =============================================================================
# ==== extras: web images + QR labs ====
BMESH = "/_blob/1738fb86fb9372d10dcfe1130f9b24d7"; BVM = "/_blob/9ecac5841eb0f2be0f7c0e56b12decb9"
WRENCH = "/_blob/3177144d9485bdbb2aa22376528bd537"; BEAM3D = "/_blob/1a2e8befa876b3ec7d23856cb3ddb115"

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · 2L + 1T</p>'
      f'<h1 style="font-family:{SERIF};font-size:112px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">Plane Stress<br>Part 1 of 3</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">Two unknowns per node: equilibrium, Hooke’s law and strain–displacement give [∂][E][∂]ᵀ{{u}}ᵀ = −{{f}}; then the boundary conditions and the element’s [N]</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020 — §3.1 – §3.2.1</p></div>',
      notes="Plane stress, part 1 of 3. The whole heat-transfer pipeline repeats; what changes is that the unknown is now a vector {u, v}. Today: the PDE from equilibrium, the constitutive law, "
            "the strain–displacement relation, boundary conditions, and the element’s shape-function matrix [N]. Assignment 4 is in progress; due the next session.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: retrieval warm-up, outcomes and the 3-hour plan")

D.activity("warmup", "0", 5, "individual · retrieval warm-up", "Three questions from heat transfer — on paper, no notes",
           D.card(D.h3("Write down") + D.ul(["The three steps that turn the PDE into [k]{T̂}ᵀ = {q} + {b} (name them).",
                                             "What a row of [k] must sum to, and why.",
                                             "The matrix form of the heat PDE: {∂}[E]{∂}ᵀT = −q<sub>h</sub>. What are the sizes of {∂} and [E]?"], 30, gap=10), extra="width:1000px"),
           col(callout("Keep question 3 in view: today the same pattern appears with a 2 × 3 operator and a 3 × 3 [E].", "why", 26), extra="flex:1"),
           "5 minutes. Then the outcomes.",
           notes="Answers: (1) substitute T = {N}{T̂}ᵀ, weight with {N}ᵀ and integrate (Galerkin), integrate by parts. (2) Zero: a uniform temperature produces no heat flow. "
                 "(3) {∂} is 1 × 2 and [E] is 2 × 2. Today: [∂] is 2 × 3 and [E] is 3 × 3.")

outs = ["Derive the plane-stress equilibrium equations from a differential element and write them as [∂]{σ}ᵀ = −{f}.",
        "State the plane-stress constitutive law {σ}ᵀ = [E]{ε}ᵀ and the strain–displacement relation {ε}ᵀ = [∂]ᵀ{u}ᵀ, and combine them into [∂][E][∂]ᵀ{u}ᵀ = −{f}.",
        "Classify traction (natural) and displacement (essential) boundary conditions and write them for a rectangular domain.",
        "Write the 2 × 8 shape-function matrix [N] of the four-node element and interpolate u and v at any point."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("Text §3.1 – §3.2.1. Next session: [B], [k] and the cantilever worked example; Plane Stress Part 3: stresses, convergence and the project.", "why"),
          notes="Four outcomes, four blocks after the warm-up. The derivation is longer than heat transfer because there are three ingredients (equilibrium, Hooke, strain–displacement) instead of two (balance, Fourier).")

D.content("session", "Session map · 180 minutes", "Six blocks, seven short activities, one break",
          session_map([("0:00", "Why plane stress?", 25, "A1 · 5 min", False), ("0:25", "Equilibrium → PDE", 35, "A2 · 8 min", False), ("1:00", "Hooke + strain", 25, "A3 + QR", False),
                       ("1:25", "Break", 10, "", True), ("1:35", "Boundary conditions", 30, "A4 · 6 min", False), ("2:05", "DOFs and [N]", 30, "A5 · 8 min", False), ("2:35", "What changes", 25, "Exit ticket", False)])
          + row(D.card(D.h3("Revise from solid mechanics") + D.ul(["Stress components σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub> and the sign convention.", "Hooke’s law in 2D; E and ν.", "Engineering shear strain ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x (the text’s symbol for γ<sub>xy</sub>)."], 28), extra="flex:1"),
                D.card(D.h3("The running example") + D.ul(["Text §3.4: cantilever plate 4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m⁻², ν = 0.33, 5 kN m⁻¹ on the free end.", "Today: its boundary conditions and its mesh.", "Next session: its 8 × 8 [k] and solution."], 28), extra="flex:1"), align="stretch"),
          notes="Note the text’s notation: ε_xy is the engineering shear strain (γ_xy in most solid-mechanics texts). Say it once now and once again at the strain slide, because the factor of 2 is where students lose marks.")

# =============================================================================
# Block 1 — Why plane stress
# =============================================================================
D.divider("d1", "1", "Why plane stress?", "Thin bodies loaded in their own plane: shear walls, deep beams, gusset plates, the web of a girder. Two unknowns at every point, u and v.",
          "Block 1 · 0:00 – 0:25", section="Block 1: what plane stress is, where civil engineers use it, and how it differs from plane strain",
          notes="Twenty-five minutes including the warm-up debrief. The learning point is the modelling decision: plane stress or plane strain, and the two-dof-per-node consequence.")

D.content("what", "Block 1 · the modelling assumption · text §3.1", "Thin and loaded in-plane: plane stress. Long with a constant section: plane strain",
          two_col(col(figbox(D.fig("fig_ps_vs_pe", width=900)),
                      D.p("Plane stress: the thickness t is small and nothing acts on the faces, so σ<sub>zz</sub> = σ<sub>xz</sub> = σ<sub>yz</sub> = 0. The body may thin or thicken freely (ε<sub>zz</sub> ≠ 0).", 28),
                      D.p("Plane strain: the body is long and every section is loaded the same way, so ε<sub>zz</sub> = 0 and a stress σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) develops to prevent it.", 28)),
                  col(D.card(D.h3("Plane stress in practice") + D.ul(["Shear walls, deep beams", "Gusset plates, connection plates", "Web of a plate girder, thin flanges", "Thin slabs loaded in their plane"], 28, gap=6)),
                      D.card(D.h3("Plane strain in practice") + D.ul(["Gravity dams, long embankments", "Tunnel linings, pipes, culverts", "Retaining walls (per metre run)", "Strip footings"], 28, gap=6))),
                  lw=940),
          notes="The two cases share everything except the 3 × 3 [E]. This course formulates plane stress (text Chapter 3); ANSYS in the ANSYS demo offers both and we will deliberately pick the wrong one once to see the difference.")

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

D.content("unknowns", "Block 1 · the unknowns", "Displacements u(x, y), v(x, y); from them strains, then stresses",
          two_col(col(figbox(D9.fig("fig_scalar_vector", width=860)), D.p("Heat transfer carried one unknown per node. Plane stress carries two: the nodal displacements u<sub>i</sub> and v<sub>i</sub>. A 4-node element has 8 degrees of freedom and an 8 × 8 stiffness matrix.", 28)),
                  col(table(["Quantity", "Heat transfer", "Plane stress"], [["primary field", "T (scalar)", "u, v (vector)"], ["derived field", "flux q<sub>x</sub>, q<sub>y</sub>", "strains ε, stresses σ"], ["material law", "Fourier: q = −k∇T", "Hooke: {σ} = [E]{ε}"], ["dof per node", "1", "2"], ["4-node [k]", "4 × 4", "8 × 8"]], [34, 33, 33], 26),
                      callout("Displacement-based FEM: we solve for u and v, then differentiate to get strains and stresses — so stresses are one order less accurate than displacements.", "why", 26)),
                  lw=900),
          notes="The last row of the table is the reason plane stress takes three sessions. The callout is the key idea for Plane Stress Part 3: stress recovery by differentiation loses accuracy, which is why we look at stresses at element centroids and refine the mesh.")

D.activity("act1", 1, 5, "pairs · no calculation", "Plane stress, plane strain, or neither? Decide and give the reason",
           D.card(D.h3("Six structures") + D.ul(["Steel gusset plate at a truss joint, 12 mm thick", "Concrete gravity dam, 300 m long", "Reinforced-concrete shear wall, 200 mm thick, 6 m high", "Circular tunnel lining, 2 km long",
                                                 "Square slab carrying a lateral floor load (bending)", "Strip footing of a long wall"], 30, gap=8), extra="width:1000px"),
           D.card(D.h3("For each") + D.ul(["Plane stress / plane strain / neither (and why).", "What is zero: σ<sub>zz</sub> or ε<sub>zz</sub>?"], 30, gap=8), extra="flex:1"),
           "Compare with the pair next to you. We reveal in 5 minutes.",
           notes="Answers: gusset plate → plane stress (thin, in-plane loads; σ_zz = 0). Gravity dam → plane strain (long, constant section; ε_zz = 0). Shear wall → plane stress (thin relative to height and length, loaded in its plane). "
                 "Tunnel lining → plane strain. Slab in bending → neither: loads are normal to the plane, so it is a plate-bending problem (not in this course). Strip footing → plane strain per metre run. "
                 "Two minutes for the reveal by show of hands.")

# =============================================================================
# Block 2 — Equilibrium → PDE
# =============================================================================
D.divider("d2", "2", "Equilibrium of a differential element", "Sum forces in x and in y; two PDEs in the stresses; write them with the 2 × 3 operator matrix [∂]. Text §3.1.1.",
          "Block 2 · 0:25 – 1:00", section="Block 2: derivation of the plane-stress equilibrium equations and their matrix form with the differential operator matrix",
          notes="Thirty-five minutes. Same method as Heat Transfer Part 1 (Taylor expansion on the far faces) with stresses instead of fluxes and force balance instead of energy balance.")

D.content("diffelem", "Block 2 · the differential element · text Fig. 3.1", "Normal stresses, shear stresses and body forces on a rectangle dx by dy",
          two_col(figbox(D.fig("fig_ps_diffelem", width=760)),
                  col(D.p("Dependent variables: σ<sub>xx</sub>, σ<sub>yy</sub> (normal) and σ<sub>xy</sub>, σ<sub>yx</sub> (shear). Body forces f<sub>x</sub>, f<sub>y</sub> per unit volume (self-weight: f<sub>y</sub> = −ρg).", 28),
                      D.p("Far faces carry the near-face stress plus its first-order change — the same Taylor expansion as for the heat flux.", 28),
                      D.eqpanel("p_sumF", "(3.1), (3.2)", colw=816, maxh=90),
                      callout("Sign convention: a stress component is positive when it acts in the positive coordinate direction on a face whose outward normal is positive (and vice versa).", "why", 26)),
                  lw=800),
          notes="Walk around the element naming each arrow. Shear stresses come in pairs: σ_xy acts on the x-faces in the y-direction; σ_yx on the y-faces in the x-direction; moment equilibrium makes them equal (next slides).")

D.content("eqx", "Block 2 · force balance in x · text (3.3)–(3.4)", "Forces are stresses times face areas; divide by dx dy",
          col(D.eqpanel("p_eqx_full", "(3.3)", colw=1664, maxh=120), D.eqpanel("p_eqx", "(3.4)", colw=1664, maxh=130),
              row(callout("σ<sub>xx</sub> acts on faces of area dy (times unit thickness); σ<sub>yx</sub> on faces of area dx. Expand, cancel the equal and opposite near-face terms, divide by dx dy.", "why", 26),
                  D.eqpanel("p_units", "", colw=820, maxh=100, bg=WHITE), align="stretch")),
          notes="Expand (3.3): the σ_xx terms cancel, leaving (∂σ_xx/∂x) dx dy; likewise for σ_yx; the body force is already per volume. Units: stress gradient in N/m³ equals body force in N/m³.")

D.activity("act2", 2, 8, "pairs · derivation", "Your turn: force balance in y, then the matrix form",
           D.card(D.h3("Do") + D.ul(["Write ΣF<sub>y</sub> = 0 for the element (which stresses act in y? on which faces?).", "Expand and cancel to get the second PDE.",
                                     "Put the two PDEs in matrix form: a 2 × 3 operator matrix times {σ<sub>xx</sub> σ<sub>yy</sub> σ<sub>xy</sub>}ᵀ, using σ<sub>yx</sub> = σ<sub>xy</sub>."], 30, gap=10), extra="width:960px"),
           col(D.eqpanel("p_eqx", "(3.4) — given", colw=656, maxh=120), callout("Why σ<sub>yx</sub> = σ<sub>xy</sub>? Moment equilibrium about the element centre.", "why", 26), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: σ_yy on the y-faces (area dx) and σ_xy on the x-faces (area dy) act in y: ∂σ_xy/∂x + ∂σ_yy/∂y + f_y = 0, equation (3.6). Matrix form: rows [∂/∂x 0 ∂/∂y] and [0 ∂/∂y ∂/∂x] acting on {σ_xx σ_yy σ_xy}ᵀ = −{f_x f_y}ᵀ. "
                 "Moment about the centre: σ_xy (dy)(dx/2)×2 = σ_yx (dx)(dy/2)×2, so they are equal (conservation of angular momentum).")

D.content("act2-reveal", "Activity 2 · solution · text (3.5)–(3.9)", "Two equilibrium equations, one operator matrix",
          col(D.eqpanel("p_eqy_full", "(3.5)", colw=1664, maxh=110, pad="16px 32px"), D.eqpanel("p_eqy", "(3.6)", colw=1664, maxh=110, pad="16px 32px"),
              row(D.eqpanel("p_matrix", "(3.8)", colw=960, maxh=280, pad="16px 32px"), col(D.eqpanel("p_compact", "(3.9)", colw=656, maxh=80), callout("[∂] is 2 × 3: two equations, three stress components. Its transpose will turn up in the strain–displacement relation.", "why", 24)), align="stretch")),
          notes="Compare with heat transfer: {∂} was a 1 × 2 row acting on a 2 × 1 flux vector; [∂] is a 2 × 3 matrix acting on the 3 × 1 stress vector. Same role, bigger size.")

# =============================================================================
# Block 3 — Hooke and strain-displacement
# =============================================================================
D.divider("d3", "3", "Hooke’s law and strain–displacement", "Three stresses in terms of three strains; three strains in terms of two displacements. Put together: a PDE in u and v. Text (3.10)–(3.17).",
          "Block 3 · 1:00 – 1:25", section="Block 3: plane-stress constitutive law, strain–displacement relation, and the displacement form of the PDE",
          notes="Twenty-five minutes. The constitutive law is the analogue of Fourier’s law; the strain–displacement relation has no analogue in heat transfer because T is the primary unknown there.")

D.content("hooke", "Block 3 · plane-stress Hooke’s law · text (3.10)–(3.12)", "Three stresses from three strains through the 3 × 3 matrix [E]",
          two_col(col(D.eqpanel("p_hooke", "(3.10)", colw=760, maxh=380, pad="16px 32px")),
                  col(D.eqpanel("p_E", "(3.11), (3.12)", colw=856, maxh=240, pad="16px 32px"),
                      callout("E: Young’s modulus; ν: Poisson’s ratio. The (1 − ν)/2 entry is G/(E/(1 − ν²)): the shear term uses the engineering shear strain ε<sub>xy</sub> = γ<sub>xy</sub>.", "why", 26),
                      callout("Plane strain changes only [E] (next slide). Everything else today is identical.", "ok", 26)),
                  lw=800),
          notes="Derive (3.10a) from 3D Hooke’s law with σ_zz = 0 if the class asks; otherwise state it. The shear entry: σ_xy = G γ_xy with G = E/(2(1+ν)); and E/(1−ν²) × (1−ν)/2 = E/(2(1+ν)) = G. Check it on the board — it is a nice 30-second verification.")

D.content("estrain", "Block 3 · the plane-strain matrix, for contrast", "Same shape, different constants — and ε₍zz₎ = 0 instead of σ₍zz₎ = 0",
          col(D.eqpanel("p_Estrain", "from 3D Hooke’s law with ε_zz = 0", colw=1664, maxh=230),
              row(D.card(D.h3("Why it matters") + D.p("Choosing plane stress for a dam (or plane strain for a thin plate) changes the stiffness by a factor of order 1/(1 − ν²): several percent for steel, more for rubber-like materials. ANSYS asks you which one; the FEM machinery does not care.", 28), extra="flex:1"),
                  D.card(D.h3("In this course") + D.p("We formulate and hand-calculate plane stress (text Chapter 3). Plane strain is the same [k] with this [E] substituted — one line in the MATLAB code.", 28), extra="flex:1"), align="stretch")),
          notes="Not in the text; included because the project and ANSYS will present the choice. For ν = 0.33, 1/(1 − ν²) = 1.12, so a 12% stiffness difference in the normal terms. For ν → 0.5 (rubber, undrained clay) the plane-strain matrix blows up: incompressibility, a topic for a later course.")

D.content("strain", "Block 3 · strain–displacement · text (3.13)–(3.15)", "Two displacements, three strains, the transpose of [∂]",
          col(row(figbox(D.fig("fig_strain", width=700)), D.eqpanel("p_strain", "(3.13)", colw=856, maxh=110), align="center"),
              row(D.eqpanel("p_strain_matrix", "(3.14), (3.15)", colw=1000, maxh=250, pad="12px 32px"),
                  col(callout("The 3 × 2 matrix in (3.14) is [∂]ᵀ, the transpose of the equilibrium operator: equilibrium and compatibility are dual.", "why", 24),
                      callout("ε<sub>xy</sub> is the engineering shear strain (sum of the two slopes), not the tensor strain (half of it). The text’s [E] is built for it.", "warn", 24)), align="stretch")),
          notes="Sketch the three deformation modes on the board as the figure shows. The transpose relation is worth a minute: in heat transfer the same thing happened ({∂} and {∂}ᵀ); here it gives the symmetric structure [∂][E][∂]ᵀ.")

D.content("pde", "Block 3 · assemble the PDE · text (3.16)–(3.17)", "Substitute strain into Hooke, Hooke into equilibrium: a PDE in u and v",
          col(row(D.eqpanel("p_sigma_u", "(3.16)", colw=700, maxh=80), D.eqpanel("p_pde", "(3.17)", colw=936, maxh=80), align="stretch"),
              D.eqpanel("p_compare", "heat transfer (2.13) ↔ plane stress (3.17)", colw=1664, maxh=90),
              row(D.card(D.h3("Read (3.17) from the inside out") + D.ul(["[∂]ᵀ{u}ᵀ: displacements → strains (3 × 1).", "[E][∂]ᵀ{u}ᵀ: strains → stresses (3 × 1).", "[∂][E][∂]ᵀ{u}ᵀ: stresses → equilibrium (2 × 1), balanced by the body force."], 28, gap=8), extra="flex:1"),
                  D.card(D.h3("What we will do with it") + D.p("Exactly what we did with (2.13): substitute {u}ᵀ = [N]{û}ᵀ, weight with [N]ᵀ, integrate by parts. The boundary term will be the traction (Block 4). Next session.", 28), extra="flex:1"), align="stretch")),
          notes="This slide is the payoff of Heat Transfer Part 1’s matrix-form slide: the pattern is identical. Students who see the correspondence will find the next session’s [k] derivation a repeat of k_34 with bigger matrices.")

D.activity("act3", 3, 6, "pairs · calculation", "Evaluate [E] for the cantilever’s material",
           D.card(D.h3("Given (text Fig. 3.4)") + D.ul(["E = 200 × 10⁶ N m⁻², ν = 0.33.", "Plane stress."], 30, gap=8) + D.h3("Find") + D.ul(["E/(1 − ν²) and the three distinct entries of [E].", "Then: G = E/(2(1 + ν)). Does it equal the (3,3) entry?"], 30, gap=8), extra="width:900px"),
           col(D.eqpanel("p_E", "", colw=716, maxh=200, bg=WHITE, pad="12px 20px"), callout("Keep four significant figures; the stiffness matrix the next session is built from these numbers.", "ok", 26), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: 1 − ν² = 0.8911; E/(1 − ν²) = 224.44 × 10⁶; ν × that = 74.07 × 10⁶; (1 − ν)/2 × that = 0.335 × 224.44 × 10⁶ = 75.19 × 10⁶. G = 200 × 10⁶/(2 × 1.33) = 75.19 × 10⁶: yes, equal to the (3,3) entry, as it must be.")

D.content("act3-reveal", "Activity 3 · solution", "The constitutive matrix of the cantilever, in N m⁻²",
          col(D.eqpanel("p_act3", "", colw=1664, maxh=120), D.eqpanel("p_act3_E", "", colw=1664, maxh=300, pad="16px 32px"),
              callout("G = E/(2(1 + ν)) = 200 × 10⁶ / 2.66 = 75.19 × 10⁶ N m⁻² — equal to the (3,3) entry, which confirms that ε<sub>xy</sub> is the engineering shear strain.", "ok")),
          notes="Then break: 10 minutes.")

qr_lab(D, "qr-cant-w11", 5, "Plane stress or plane strain? Predict, then check",
       ["From the two [E] matrices, predict whether the plate is stiffer in plane strain, and by roughly how much.",
        "In the Cantilever Explorer choose 8-node, 8 × 4. Read the tip deflection in plane stress, then in plane strain.",
        "Which idealisation suits our 10 mm plate, and which would suit a long dam?"],
       [LABS["cant"]], "5 minutes, optional in class: if the block is running late, set it as homework. Next session you will compute by hand the 2 × 2 result that the Explorer shows.",
       notes="The QR code opens the public copy on GitHub Pages (no login): open it once on a phone before class. "
             "Answers: (1) Stiffer in plane strain: the plate cannot thin, so the bending modulus rises from E to E/(1 − ν²), about 12% stiffer; deflection ratio about 1 − ν² = 0.89. "
             "(2) 8-node 8 × 4: −0.1906 m in plane stress, about −0.171 m in plane strain (ratio 0.90). (3) Plane stress for the thin plate; plane strain for a long dam or retaining wall.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:25 – 1:35</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: boundary conditions, degrees of freedom and the shape-function matrix.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True), notes="Ten minutes.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Boundary conditions
# =============================================================================
D.divider("d4", "4", "Boundary conditions", "Traction (natural) where forces are applied or absent; displacement (essential) where the structure is held. Text §3.1.2.",
          "Block 4 · 1:35 – 2:05", section="Block 4: traction and displacement boundary conditions, the rectangular-domain simplification, and the cantilever’s edges",
          notes="Thirty minutes. The analogy with heat transfer is exact: traction ↔ flux (natural), displacement ↔ temperature (essential), free edge ↔ insulated edge.")

D.content("bc-types", "Block 4 · two kinds of condition · text (3.18)–(3.23)", "On every boundary point, each direction has either a known traction or a known displacement",
          col(row(D.card(D.h3("Neumann · natural · traction specified") + D.eqpanel("p_bx", "(3.18a), (3.19a)", colw=1000, maxh=80, bg=PANEL, pad="12px 20px")
                         + D.p("b<sub>x</sub>, b<sub>y</sub>: force per unit area on the boundary (per unit thickness: force per unit length). A free edge has b<sub>x</sub> = b<sub>y</sub> = 0.", 26, MUTED), extra="flex:1"),
                  D.card(D.h3("Dirichlet · essential · displacement specified") + D.eqpanel("p_dirichlet", "(3.22), (3.23)", colw=560, maxh=80, bg=PANEL, pad="12px 20px")
                         + D.p("A fixed support: ū = v̄ = 0. A roller: one of them.", 26, MUTED), extra="flex:1"), align="stretch"),
              row(D.eqpanel("p_rect_v", "(3.20)", colw=820, maxh=90), D.eqpanel("p_rect_h", "(3.21)", colw=820, maxh=90), align="stretch"),
              callout("Each direction separately: on a roller edge u may be fixed (essential) while the traction in y is zero (natural). Count conditions per direction, not per edge.", "warn", 26)),
          notes="Two directions means two conditions per boundary point. (3.18b)/(3.19b) in the text write the traction in terms of displacement derivatives through Hooke and strain–displacement; we keep the stress form here. "
                "The rectangular simplification mirrors (2.15): on a vertical edge only σ_xx and σ_xy act as tractions.")

D.content("bc-fem", "Block 4 · what FEM does with each kind", "Same table as heat transfer, with forces in place of fluxes",
          col(table(["Condition", "What is known", "Where it enters the FEM", "Heat-transfer analogue"],
                    [["Displacement · essential", "ū, v̄ at nodes", "imposed on the assembled system by row–column elimination", "T̄ imposed"],
                     ["Traction · natural", "b<sub>x</sub>, b<sub>y</sub> on an edge", "equivalent nodal loads in {b} from the boundary integral", "flux load {b}"],
                     ["Free edge · natural, b = 0", "nothing acts", "contributes nothing: do nothing", "insulated edge"],
                     ["Body force", "f<sub>x</sub>, f<sub>y</sub> per volume", "equivalent nodal loads in {q} (e.g. self-weight)", "heat generation {q}"]], [24, 22, 32, 22], 27),
              row(callout("A free edge is not a support and not a load: it is the do-nothing condition, exactly like an insulated edge.", "warn", 26),
                  callout("Reactions at fixed nodes are recovered afterwards from the deleted equations, like boundary fluxes at Dirichlet nodes.", "why", 26), align="stretch")),
          notes="Make students say the analogy aloud: traction is to displacement as flux is to temperature. The free edge is the commonest source of a wrong model in ANSYS: students add a constraint where none exists.")

D.activity("act4", 4, 6, "pairs · classification", "Label the cantilever: each edge, each direction",
           col(figbox(D.fig("fig_cantilever", width=800)), extra="width:860px"),
           D.card(D.h3("For the four edges write") + D.ul(["Essential or natural, in x and in y.", "The equation (ū, v̄ or b<sub>x</sub>, b<sub>y</sub> with the outward normal).", "FEM action: impose / load / nothing."], 30, gap=8)
                  + D.p("Then: how many of the 18 dofs of the 2 × 2 mesh are known?", 30, DARK, 600), extra="flex:1"),
           "6 minutes. Reveal follows.",
           notes="Answers: left edge: u = v = 0, essential in both directions, imposed. Right edge: n = (1, 0); b_x = σ_xx = 0 and b_y = σ_xy = q_y (downward traction 5 kN/m; with unit-thickness bookkeeping, q_y/t per unit area), natural, load. "
                 "Top and bottom: free, b_x = b_y = 0, natural, nothing. Known dofs: the three left-edge nodes 1, 4, 7 → U1, U2, U7, U8, U13, U14 = 0: six known, twelve unknown. (Text (3.48) solves the 12 × 12 system.)")

D.content("act4-reveal", "Activity 4 · solution", "Six fixed dofs on the left edge, one loaded edge, two free edges",
          col(table(["Edge", "x-direction", "y-direction", "FEM action"],
                    [["left (x = 0)", "ū = 0, essential", "v̄ = 0, essential", "impose U<sub>1</sub>, U<sub>2</sub>, U<sub>7</sub>, U<sub>8</sub>, U<sub>13</sub>, U<sub>14</sub> = 0"],
                     ["right (x = 4)", "b<sub>x</sub> = σ<sub>xx</sub> = 0, natural", "b<sub>y</sub> = σ<sub>xy</sub> = −q<sub>y</sub>, natural", "nodal loads from the 5 kN m⁻¹ traction"],
                     ["top (y = 2)", "b<sub>x</sub> = σ<sub>yx</sub> = 0", "b<sub>y</sub> = σ<sub>yy</sub> = 0", "nothing"],
                     ["bottom (y = 0)", "b<sub>x</sub> = 0", "b<sub>y</sub> = 0", "nothing"]], [20, 26, 26, 28], 27),
              row(figbox(D.fig("fig_ps_mesh", width=430)), col(callout("18 dofs, 6 known, 12 unknown. Next session: the 12 × 12 reduced system (text (3.48)).", "ok", 26),
                                                                   callout("The traction acts downward: −q<sub>y</sub> in our sign convention, so the nodal loads come out negative (−2500, −5000, −2500 N in the text).", "why", 26)), align="center")),
          notes="Show the mesh with U_1…U_18: node n carries U_{2n−1} (x) and U_{2n} (y). The text’s load vector (3.47) has −2500 at U_6 and U_18 and −5000 at U_12: the edge traction split half to each end node of each edge element, with the middle node shared.")

# =============================================================================
# Block 5 — DOFs and [N]
# =============================================================================
D.divider("d5", "5", "Degrees of freedom and the shape-function matrix", "The same N₁…N₄ as heat transfer, arranged in a 2 × 8 matrix so that both u and v are interpolated at once. Text §3.2.1.",
          "Block 5 · 2:05 – 2:35", section="Block 5: nodal degrees of freedom of the plane-stress element and the 2-by-8 shape-function matrix",
          notes="Thirty minutes. Nothing new in the shape functions themselves; the new object is the matrix [N] and the ordering of the 8 dofs.")

D.content("dofs", "Block 5 · eight degrees of freedom · text Fig. 3.2", "Each node carries u (along x) and v (along y); the dof vector interleaves them",
          two_col(figbox(D.fig("fig_ps_q4", width=760)),
                  col(D.eqpanel("p_interp", "(3.24), (3.25)", colw=816, maxh=70, pad="14px 24px"),
                      D.card(D.h3("Ordering convention") + D.ul(["{û} = {u<sub>1</sub> v<sub>1</sub> u<sub>2</sub> v<sub>2</sub> u<sub>3</sub> v<sub>3</sub> u<sub>4</sub> v<sub>4</sub>}: node by node, u before v.",
                                                                 "Global: node n has dofs U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y).", "The same N<sub>i</sub>(x, y) as (2.21) interpolate both u and v."], 28, gap=8)),
                      callout("Keep this ordering everywhere: in [N], in [B], in [k] and in the connectivity. Mixing “all u then all v” with “node by node” is the classic assembly error.", "warn", 26)),
                  lw=800),
          notes="Interleaved ordering is what the text and the MATLAB code use: K([1 2 3 4 9 10 7 8],…) for element 1 — node 1 → dofs 1, 2; node 2 → 3, 4; node 5 → 9, 10; node 4 → 7, 8.")

D.content("Nmatrix", "Block 5 · the shape-function matrix · text (3.28)–(3.30)", "A 2 × 8 matrix: row 1 interpolates u, row 2 interpolates v",
          col(D.eqpanel("p_N", "(3.28)", colw=1664, maxh=470, pad="16px 32px"), D.eqpanel("p_general", "(3.30)", colw=1664, maxh=80, pad="12px 32px")),
          notes="Multiply out the first row to recover (3.24). The zeros matter: u does not depend on the v-dofs. The 8-node element gives a 2 × 16 matrix of the same pattern (text (3.29)).")

D.activity("act5", 5, 8, "pairs · calculation", "Interpolate u and v at a point of element 4 of the solved cantilever",
           col(figbox(D.fig("fig_ps_mesh_e4", width=760)), extra="width:820px"),
           col(D.card(D.h3("Given (text (3.49), element 4 = nodes 5, 6, 9, 8)") + D.ul(["(u, v) at node 5: (0, −0.043); node 6: (0, −0.130); node 9: (0.042, −0.131); node 8: (0.031, −0.046) m.",
                                                                                        "Element 4: a = 2 m, b = 1 m, its node 1 at global (2, 1)."], 28, gap=6)
                      + D.h3("Find") + D.ul(["Local coordinates of the point (3.5, 1.3) m.", "N<sub>1</sub>…N<sub>4</sub> there (you met these numbers in Heat Transfer Part 1).", "u and v at the point."], 28, gap=6), pad=26, gap=10), extra="flex:1"),
           "8 minutes. Reveal follows. Plane Stress Part 3 uses the same point for the stresses.",
           notes="Answers: local (1.5, 0.3); N = {0.175, 0.525, 0.225, 0.075}; u = 0.225 × 0.042 + 0.075 × 0.031 = 0.0118 m; v = 0.175(−0.043) + 0.525(−0.130) + 0.225(−0.131) + 0.075(−0.046) = −0.1087 m. "
                 "The downward deflection is about 0.11 m at 3.5 m along a 4 m cantilever with a very soft E of 200 MPa — the text’s numbers, chosen to make the displacements visible.")

D.content("act5-reveal", "Activity 5 · solution", "The heat-transfer shape functions, applied to two fields at once",
          col(figbox(D.fig("fig_ps_q4_point", width=720)) if False else "",
              D.eqpanel("p_act5_N", "", colw=1664, maxh=70, pad="12px 32px"), D.eqpanel("p_act5_u", "", colw=1664, maxh=160, pad="16px 32px"),
              row(figbox(D.fig("fig_ps_q4_point", width=560)), col(callout("Node 2 of the element (global node 6, the free end) dominates: half the weight, and the largest v.", "why", 26),
                                                                       callout("Plane Stress Part 3: differentiate the same interpolation with [B] to get ε and σ at this point.", "ok", 26)), align="center")),
          notes="The nodal values are listed in local order (1)(2)(3)(4) = global 5, 6, 9, 8. Point out that u is small and v large: bending, as expected for a cantilever.")

# =============================================================================
# Block 6 — What changes
# =============================================================================
D.divider("d6", "6", "The pipeline for plane stress — what changes", "Every step repeats; only the sizes grow. Preview of [B] and [k], then the exit ticket.",
          "Block 6 · 2:35 – 3:00", section="Block 6: side-by-side comparison of the heat-transfer and plane-stress pipelines, preview of [B] and [k], exit ticket and preparation",
          notes="Twenty-five minutes including the exit ticket.")

D.content("compare", "Block 6 · heat transfer and plane stress, side by side", "Same seven steps; the objects change size",
          col(table(["Step", "Heat transfer (Parts 1–2)", "Plane stress (Parts 1–3)"],
                    [["PDE", "{∂}[E]{∂}ᵀT = −q<sub>h</sub>", "[∂][E][∂]ᵀ{u}ᵀ = −{f}"], ["operator", "{∂}: 1 × 2", "[∂]: 2 × 3"], ["material", "[E] = diag(k<sub>x</sub>, k<sub>y</sub>): 2 × 2", "[E]: 3 × 3 (plane stress)"],
                     ["shape functions", "{N}: 1 × 4", "[N]: 2 × 8"], ["gradient / strain", "{∂}ᵀ{N}: 2 × 4", "[B] = [∂]ᵀ[N]: 3 × 8"], ["element matrix", "[k] = ∫{N}ᵀ{∂}[E]{∂}ᵀ{N} dA: 4 × 4", "[k] = t∫[B]ᵀ[E][B] dA: 8 × 8"],
                     ["natural BC", "flux q<sub>b</sub> → {b}", "traction b<sub>x</sub>, b<sub>y</sub> → {b}"], ["essential BC", "T̄ at nodes", "ū, v̄ at nodes"]], [22, 39, 39], 26),
              row(D.eqpanel("p_B_preview", "the next session", colw=900, maxh=80, pad="12px 24px"), D.eqpanel("p_k_preview", "the next session", colw=736, maxh=100, pad="12px 24px"), align="stretch")),
          notes="This table is the map for the next two sessions. [B] is the plane-stress version of the 2 × 4 gradient matrix; the attached image in the course notes ([σ] = [E][B]{u}, with [B] written out) is Plane Stress Part 2’s first slide after the derivation.")

D.activity("exit", 6, 5, "individual · exit ticket", "Three questions before you leave",
           D.card(D.h3("Questions") + D.ul(["A 10 m long culvert loaded uniformly along its length: plane stress or plane strain, and which quantity is zero?",
                                            "Write the strain–displacement relation in matrix form and name the matrix.",
                                            "For a square element (a = b), what are u and v at the centroid in terms of the nodal values?"], 30, gap=12), extra="width:1000px"),
           col(D.eqpanel("p_cent", "hint for Q3", colw=616, maxh=90, bg=WHITE, pad="12px 20px"), D.eqpanel("p_strain_matrix", "", colw=616, maxh=260, bg=WHITE, pad="12px 20px"), extra="flex:1"),
           "Five minutes. Name and matric number; for feedback, not marks.",
           notes="Answers: (1) plane strain, ε_zz = 0. (2) {ε}ᵀ = [∂]ᵀ{u}ᵀ, the transpose of the differential operator matrix. (3) u = (u1 + u2 + u3 + u4)/4 and v = (v1 + v2 + v3 + v4)/4, since every N_i = 1/4 at the centroid.")

D.content("summary", "Wrap-up · what to take away and what to prepare", "Next session: [B], the 8 × 8 [k] and the cantilever solved by hand",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["Equilibrium of the element: [∂]{σ}ᵀ = −{f} with the 2 × 3 operator [∂].",
                                                              "Hooke: {σ}ᵀ = [E]{ε}ᵀ (3 × 3, plane stress); strain–displacement: {ε}ᵀ = [∂]ᵀ{u}ᵀ. Together: [∂][E][∂]ᵀ{u}ᵀ = −{f}.",
                                                              "Traction = natural (load or nothing); displacement = essential (imposed). Count per direction.",
                                                              "{u}ᵀ = [N]{û}ᵀ with [N] 2 × 8, dofs ordered node by node, u before v."], 28, gap=10)),
                  col(D.card(D.h3("Before the next session") + D.ul(["Assignment 4 due the next session.", "Read text §3.2.2 – §3.3 (pages 89–96): the k₃₄ steps and s₁…s₁₂.", "Redo Activity 3 for plane strain with the matrix on the contrast slide.",
                                                            "Bring the heat-transfer MATLAB script: the next session we modify it for plane stress."], 28, gap=10)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=940),
          notes="Close on time. Collect exit tickets.")

order = D.write("2026-10-26T15:40:00Z")
print(len(order), "slides:", order)
