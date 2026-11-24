import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from decklib import *

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "deck_w9"
eq_rep = {x["name"]: x for x in json.loads((HERE / "eqs_w9" / "_report.json").read_text())}
D = Deck(ROOT, "FEM — 2D Heat Transfer (Part 1)", "SEAA 4243 · 2D Heat Transfer — Part 1", HERE / "eqs_w9", HERE / "figs_w9", eq_rep)
TENT = "/_blob/bb25d245b036bf81d9b34464a33a9404"
MAPS = "/_blob/1be5a5fac93991bf225067078eb4e033"

def two_col(left, right, lw=None, rw=None, gap=48, align="start"):
    ls = f"width:{lw}px" if lw else "flex:1"
    rs = f"width:{rw}px" if rw else "flex:1"
    return (f'<div style="display:flex;flex-direction:row;gap:{gap}px;flex:1;align-items:{align}">'
            f'<div style="{ls};display:flex;flex-direction:column;gap:28px">{left}</div>'
            f'<div style="{rs};display:flex;flex-direction:column;gap:28px">{right}</div></div>')

def col(*parts, gap=28, extra=""):
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;{extra}">{"".join(parts)}</div>'

def row(*parts, gap=28, extra="", align="center"):
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:{align};{extra}">{"".join(parts)}</div>'

def figbox(svg, bg=WHITE):
    return f'<div style="background:{bg};border:1px solid {HAIR};border-radius:14px;padding:24px;display:flex;align-items:center;justify-content:center">{svg}</div>'

def callout(text, kind="why"):
    colr = {"why": TEAL, "warn": MAROON, "ok": GREEN}[kind]
    tag = {"why": "Why", "warn": "Watch out", "ok": "Check"}[kind]
    return (f'<div style="display:flex;flex-direction:row;gap:16px;align-items:start;background:{WHITE};border:1px solid {HAIR};border-radius:12px;padding:20px 24px">'
            f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{colr};white-space:nowrap">{tag}</p>'
            f'<p style="font-size:28px;line-height:1.35;color:{BODY}">{text}</p></div>')

# =============================================================================
# 0. Cover, map, outcomes, session map
# =============================================================================
# ==== extras: web images + QR labs ====
CHT = "/_blob/2df4ea670c559d53e9b66655a4c7f96e"; SHAPEN = "/_blob/7a67c37010a42bf8a488bcaeceaf2fc4"
TENT2D = "/_blob/4f57ba61e546d11d23d9eb6e2271dc3c"; HAT1D = "/_blob/64714eb9fe789ef11c1b805076358465"

D.add("cover",
      f'<div style="display:flex;flex-direction:column;gap:28px;flex:1;justify-content:center">'
      f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">SEAA 4243 Finite Element Method · 2L + 1T</p>'
      f'<h1 style="font-family:{SERIF};font-size:112px;font-weight:600;line-height:1.05;color:{LIGHT_ON_DARK}">2D Heat Transfer<br>Part 1 of 2</h1>'
      f'<p style="font-size:40px;line-height:1.3;color:{SOFT_ON_DARK};width:1400px">From the energy balance to the shape functions of the four-node scalar element</p>'
      f'</div>'
      f'<div style="display:flex;flex-direction:row;gap:64px;align-items:end">'
      f'<div style="display:flex;flex-direction:column;gap:6px"><p style="font-size:26px;color:{LIGHT_ON_DARK};font-weight:600">Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · Dr. Yip Bao Fang</p>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK}">Faculty of Civil Engineering, Universiti Teknologi Malaysia</p></div>'
      f'<div style="flex:1"></div>'
      f'<p style="font-size:24px;color:{SOFT_ON_DARK};text-align:right;width:620px">Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020 — Chapter 2</p></div>',
      notes="Welcome back after the mid-semester break. The first half of the course was one-dimensional elements: bar, beam, truss, frame, buckling and vibration. "
            "From today we move to two dimensions. The heat-transfer element is the simplest continuum element (one unknown per node) and it carries every idea "
            "we need for plane stress later: shape functions, Galerkin, integration by parts, assembly, boundary conditions. Today is Part 1: PDE, boundary conditions and shape functions. "
            "Next session: the element matrices, assembly, solution and MATLAB. Session is 3 hours with six short activities and a break at about 1h25.",
      bg=DARK, color=LIGHT_ON_DARK, transition="push", section="Opening: where this session sits, what students will be able to do, and the 3-hour plan")

# module map ------------------------------------------------------------------
weeks = [("1", "Heat transfer 1", "PDE · BCs · shape functions", True), ("2", "Heat transfer 2", "[k] · assembly · solve · Asg 4", False),
         ("3", "Plane stress 1", "PDE · [E] · [N]", False), ("4", "Plane stress 2", "[k] = ∫[B]ᵀ[E][B] · loads", False),
         ("5", "Plane stress 3", "stress recovery · Q8 · Project brief", False), ("6", "ANSYS demo", "hand calc vs software", False),
         ("7", "Practical FEM", "convergence · interpretation", False)]
cells = ""
for w, t, s, now in weeks:
    bg = AMBER if now else WHITE
    cells += (f'<div style="flex:1;background:{bg};border:1px solid {HAIR};border-radius:14px;padding:22px 18px;display:flex;flex-direction:column;gap:8px">'
              f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;color:{MAROON}">{w}</p>'
              f'<p style="font-size:28px;font-weight:600;line-height:1.2;color:{DARK}">{t}</p>'
              f'<p style="font-size:24px;line-height:1.3;color:{BODY}">{s}</p></div>')
D.content("map", "Course map · after the mid-semester break", "Two topics in five sessions, then one session with ANSYS",
          f'<div style="display:flex;flex-direction:row;gap:16px">{cells}</div>'
          + row(D.card(D.h3("CLO3 · the heat-transfer and plane-stress sessions") + D.p("Formulate 2D finite element problems and solve by hand calculation and computer software.", 28), extra="flex:1"),
                D.card(D.h3("CLO4 · project sessions") + D.p("Investigate and discuss complex structural problems using FEM with the aid of computer software (group project).", 28), extra="flex:1"),
                D.card(D.h3("Assessment on this block") + D.p("Assignment 4 (heat transfer) released in Heat Transfer Part 2 · Project briefing Plane Stress Part 3 · Final exam covers CLO3.", 28), extra="flex:1"), align="stretch"),
          notes="One minute on the map. Heat transfer takes two sessions because the 4-node element is small enough to do everything by hand. Plane stress takes three because the "
                "matrices are 8 by 8 and we add stress recovery. The last session is an ANSYS demo where we rebuild the hand-calculation examples in software and compare. "
                "Assignment 4 is released the next session and is a heat-transfer hand calculation of the type we start today.")

# outcomes --------------------------------------------------------------------
outs = ["Derive the steady 2D heat conduction PDE from an energy balance and Fourier’s law, and write it as {∂}[E]{∂}ᵀT = −q<sub>h</sub>.",
        "Classify boundary conditions as Dirichlet (essential) or Neumann (natural) and write them for a rectangular domain.",
        "Derive the bilinear shape functions N<sub>1</sub>…N<sub>4</sub> of the four-node element and use them to interpolate T(x, y).",
        "Differentiate the approximation to obtain the temperature gradient and the heat flux at any point of an element."]
D.content("outcomes", "Learning outcomes · today", "By the end of this session you should be able to",
          col(*[D.step(i + 1, o, 32) for i, o in enumerate(outs)], gap=22)
          + callout("Outcomes 1–3 are the first half of Chapter 2 of the text (§2.1 – §2.2.1). Outcome 4 prepares the next session’s conductance matrix [k].", "why"),
          notes="Read the four outcomes; they map onto the four lecture blocks after the warm-up. Point out that everything today is also in the book, sections 2.1 to 2.2.1, so students can read ahead.")

# session map -----------------------------------------------------------------
blocks = [("0:00", "Why 2D?", 25, "A1 · 5 min", False), ("0:25", "Governing PDE", 35, "A2 · 8 min", False), ("1:00", "Boundary conditions", 25, "A3 · 6 min", False),
          ("1:25", "Break", 10, "", True), ("1:35", "Shape functions", 35, "A4 + QR", False), ("2:10", "Gradient & flux", 25, "A5 · 8 min", False), ("2:35", "Pipeline & wrap-up", 25, "Exit ticket", False)]
segs = ""
for t0, name, mins, act, brk in blocks:
    bg = "#E6E2D8" if brk else WHITE
    chip = f'<p style="font-size:24px;font-weight:600;color:{DARK};background:{AMBER};padding:6px 14px;border-radius:999px;white-space:nowrap">{act}</p>' if act else '<p style="font-size:24px;color:#8A8F99">no activity</p>'
    segs += (f'<div style="flex:{mins};background:{bg};border:1px solid {HAIR};border-radius:12px;padding:20px 16px;display:flex;flex-direction:column;gap:10px;min-width:150px">'
             f'<p style="font-size:24px;font-weight:600;color:{MAROON}">{t0}</p><p style="font-size:26px;font-weight:600;line-height:1.2;color:{DARK}">{name}</p>'
             f'<p style="font-size:24px;color:{MUTED}">{mins} min</p>{chip}</div>')
D.content("session", "Session map · 180 minutes", "Six blocks, six short activities, one break",
          f'<div style="display:flex;flex-direction:row;gap:12px;align-items:stretch">{segs}</div>'
          + row(D.card(D.h3("How the activities work") + D.ul(["Amber slide = your turn. Work in pairs on paper, 5–8 minutes.", "A timer badge shows the time; the answer slide follows.", "Keep the answers — Activities 4 and 5 are the pattern for Assignment 4."], 28), extra="flex:1"),
                D.card(D.h3("What to have ready") + D.ul(["Calculator, pen and the formula sheet (shape functions).", "The text, Chapter 2, open at Fig. 2.2.", "Next session: laptop with MATLAB for code tracing."], 28), extra="flex:1"), align="stretch"),
          notes="Explain the rhythm: about 25 to 35 minutes of lecture, then an activity of 5 to 8 minutes, then the reveal. Students who finish early check the neighbouring pair. "
                "The break is at 1h25 for 10 minutes. Time stamps are from the start of the lecture, not clock time.")

# =============================================================================
# Block 1 — Why 2D?
# =============================================================================
D.divider("d1", "1", "Why two dimensions?", "FEM is a tool for solving a differential equation — so every topic starts from the PDE. Today’s PDE has one unknown: temperature.",
          "Block 1 · 0:00 – 0:25", section="Block 1: FEM as a PDE solver, scalar versus vector fields, where civil engineers meet heat conduction",
          notes="Five minutes of warm-up before this slide: ask the class to recall the 1D bar pipeline in pairs: what was the shape function, what did Galerkin do, where did the boundary terms come from. "
                "Then the key framing: FEM can be everything (it solves most engineering PDEs) and FEM can be nothing (it is just a tool to solve a DE). "
                "Because it is nothing, every topic must start from the first principle, the PDE. That is what we do today.")

pipe3 = ""
for i, (t, s) in enumerate([("1 · Get the DE", "Energy balance + Fourier’s law → a PDE in T(x, y)"), ("2 · Discretise with FEM", "Shape functions + Galerkin → [k]{T̂}ᵀ = {r}"), ("3 · Solve", "Assemble, impose T̄, solve, post-process")]):
    pipe3 += (f'<div style="flex:1;background:{WHITE};border:1px solid {HAIR};border-radius:14px;padding:32px;display:flex;flex-direction:column;gap:12px">'
              f'<p style="font-size:32px;font-weight:600;color:{DARK}">{t}</p><p style="font-size:28px;line-height:1.35;color:{BODY}">{s}</p></div>')
    if i < 2:
        pipe3 += f'<x-shape kind="arrow-right" style="width:72px;height:40px;background:{AMBER};align-self:center"></x-shape>'
D.content("fem-nothing", "Block 1 · the idea that organises the course", "FEM is “nothing”: a tool that solves a differential equation",
          f'<div style="display:flex;flex-direction:row;gap:20px;align-items:center">{pipe3}</div>'
          + row(D.card(D.h3("FEM can be “everything”") + D.p("Heat, seepage, stress, vibration, fluid flow — the same machinery solves all of them. That is why it is worth learning well.", 28), extra="flex:1"),
                D.card(D.h3("…and FEM can be “nothing”") + D.p("It is only a way to turn a continuous PDE into simultaneous algebraic equations in matrix form. Nothing is new in the physics.", 28), extra="flex:1"), align="stretch")
          + D.p("Finite difference, finite volume, meshless and isogeometric methods share the same goal; they differ in how the discretisation is done.", 28, MUTED),
          notes="The three cards are the whole course in one line. Step 1 is physics; step 2 is mathematics; step 3 is linear algebra. Students usually find step 2 hard because it is new; "
                "remind them the Galerkin steps are the same as for the bar element earlier in the course, only the integrals are now over an area.")

D.content("scalar-vector", "Block 1 · scalar versus vector fields", "Heat transfer has one unknown per node; plane stress has two",
          two_col(figbox(D.fig("fig_scalar_vector", width=860))
                  + D.p("Scalar element: each node carries one degree of freedom, the temperature T̂<sub>i</sub>. Vector element (Plane Stress Part 1): two, the displacements u<sub>i</sub> and v<sub>i</sub>.", 28),
                  D.card(D.h3("Problems governed by the same scalar PDE") +
                         f'<table style="font-size:26px;color:{BODY};border:1px solid {HAIR}"><tr><th style="width:36%">Field T</th><th style="width:34%">Property k</th><th style="width:30%">Flux q</th></tr>'
                         f'<tr><td>temperature</td><td>conductivity</td><td>heat flux</td></tr><tr><td>hydraulic head</td><td>permeability</td><td>seepage velocity</td></tr>'
                         f'<tr><td>electric potential</td><td>conductivity</td><td>current density</td></tr><tr><td>Prandtl stress function</td><td>1/G</td><td>shear stress</td></tr></table>')
                  + callout("Learn the scalar element once and you have also learnt seepage under a dam, groundwater flow and torsion of a shaft.", "why"),
                  lw=900, align="start"),
          notes="Make the DOF count concrete: a 4-node scalar element has a 4 by 4 matrix; a 4-node plane-stress element has an 8 by 8 matrix. "
                "The table shows why geotechnical students should care: seepage obeys Laplace’s equation with permeability in the role of conductivity.")

apps = [("Mass concrete", "Heat of hydration in dams, rafts and pile caps: the temperature rise and the gradient between core and surface drive early-age cracking."),
        ("Fire engineering", "Temperature rise in steel sections and tunnel linings decides when strength is lost; the input is a 2D conduction model of the section."),
        ("Pavements and decks", "Daily thermal gradients through a bridge deck or a pavement slab produce stresses that codes make us check."),
        ("Ground and geothermal", "Ground freezing, energy piles and buried pipelines are conduction problems in soil — and seepage uses the same equation.")]
D.content("civil", "Block 1 · where civil engineers meet conduction", "The same PDE appears across civil engineering",
          f'<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:28px">'
          + "".join(D.card(D.h3(t, 34) + D.p(s, 32), pad=40) for t, s in apps) + "</div>",
          notes="Keep this to two minutes; it is motivation, not content. Ask the class for one more example from their own field before moving to the activity. "
                "No numbers on this slide on purpose; the examples are qualitative.")

D.content("w9-practice", "Block 1 · the same PDE in a real simulation", "A heated plate under a channel flow",
          col(webimg(CHT, "Temperature in a channel flow and in the solid plate below it, heated from its bottom face, from the preCICE flow-over-a-heated-plate tutorial", 1240, 390),
              row(callout("The solid plate obeys today’s conduction PDE (with ∂T/∂t kept; at steady state it is exactly {∂}[E]{∂}ᵀT = −q<sub>h</sub>), with T fixed on its heated bottom face.", "why"),
                  callout("At the interface the solid receives a temperature from the fluid code and returns a heat flux: one Dirichlet and one Neumann condition, as in Block 3.", "ok"), align="stretch"),
              credit("Image: preCICE tutorials, “Flow over a heated plate”, t = 10 s; solid by FEniCS, Nutils or CalculiX (FE). LGPL-3.0, github.com/precice/tutorials.")),
          notes="Use this slide to show that the PDE of today is not a textbook toy: in a coupled heat-transfer analysis the solid side is exactly our 2D conduction problem, "
                "solved by an FE code, while a CFD code solves the fluid. Ask: which boundary of the plate is Dirichlet (the heated bottom, T fixed), which is Neumann "
                "(the interface, where the solid hands a heat flux to the fluid), and which edges are insulated (the two short sides).")

D.activity("act1", 1, 5, "pairs · no calculation", "Scalar or vector? Classify each field and count the unknowns per node",
           D.card(D.h3("Six fields — decide: scalar (1 dof) or vector (2 dof in 2D)?") +
                  D.ul(["Temperature in a concrete slab", "Pore-water pressure in an embankment", "Displacement of a shear wall", "Velocity of water in a pipe network", "Electric potential in a grounding grid", "Settlement of a strip footing (2D section)"], 30, gap=8),
                  extra="width:1000px"),
           D.card(D.h3("Then answer") + D.ul(["How many unknowns does a 4-node element have in each case?", "Which of the six could be solved with today’s element?"], 30, gap=8), extra="flex:1"),
           "Compare with the pair next to you. We reveal in 5 minutes.",
           notes="Answers: temperature = scalar (1 dof); pore pressure = scalar (1 dof); displacement = vector (2 dof: u, v); velocity = vector (2 dof: u, v); electric potential = scalar; "
                 "settlement of a footing = vector (2D plane-strain displacement; even if we only care about the vertical component, the element carries u and v). "
                 "A 4-node element therefore has 4 unknowns for a scalar field and 8 for a vector field. The first, second and fifth could be solved with today’s element, "
                 "with the property k reinterpreted (conductivity, permeability, electrical conductivity). Take one minute to collect answers by show of hands.")

# =============================================================================
# Block 2 — Governing PDE
# =============================================================================
D.divider("d2", "2", "The governing PDE", "Energy balance on a differential element, then Fourier’s law to close it in terms of temperature. Text §2.1.1 – §2.1.2.",
          "Block 2 · 0:25 – 1:00", section="Block 2: derivation of the steady heat conduction PDE from an energy balance and Fourier’s law, and its matrix form",
          notes="This block is a derivation. Go slowly on the x-direction balance, then hand the y-direction to the class (Activity 2). The target is equation 2.11 and its matrix form 2.13.")

D.content("diffelem", "Block 2 · the differential element · text Fig. 2.1", "Heat enters and leaves a small rectangle dx by dy",
          two_col(figbox(D.fig("fig_diffelem", width=800)),
                  col(D.p("Dependent variables: the heat fluxes q<sub>x</sub> and q<sub>y</sub> (W m<sup>−2</sup>), i.e. energy per unit time per unit area crossing a face.", 30),
                      D.p("The flux on the far face is the near-face flux plus its change across the element — a first-order Taylor expansion:", 30),
                      D.eqpanel("e_Qx", "(2.2)", colw=776, maxh=120),
                      D.p("Inside, heat is generated at a rate q<sub>h</sub> per unit volume (W m<sup>−3</sup>), e.g. hydration of cement.", 30),
                      callout("Per unit thickness: t multiplies every term and cancels, so we take t = 1.", "why")),
                  lw=840),
          notes="Same picture as the 1D bar earlier in the course, now with two directions. Stress the sign convention: positive flux points in the positive coordinate direction. "
                "The expression for Q_x is the net inflow in the x-direction: what comes in through the left face minus what leaves through the right face.")

D.content("balance", "Block 2 · conservation of energy", "Rate of change of stored energy = net conduction in + heat generated",
          col(row(D.card(D.h3("Stored (internal) energy") + D.eqpanel("e_QE", "(2.1)", colw=470, maxh=110, pad="16px 24px") + D.p("ρ density, C specific heat, T temperature", 26, MUTED), extra="flex:1"),
                  D.card(D.h3("Net conduction in") + D.p("Q<sub>x</sub> + Q<sub>y</sub>, the x- and y-direction net inflows (2.2)–(2.4)", 28), extra="flex:1"),
                  D.card(D.h3("Generated") + D.eqpanel("e_Qh", "(2.5)", colw=470, maxh=90, pad="16px 24px"), extra="flex:1"), align="stretch"),
              D.eqpanel("e_balance", "(2.6)", colw=1664, maxh=120),
              D.p("Every term carries the factor dx dy — the volume of the element per unit thickness — so it cancels (next slide).", 28, MUTED)),
          notes="Say the balance in words first, then point at the three cards, then the equation. The time-derivative term is kept for now; we drop it in the steady case, but "
                "it returns in Chapter 5 for fluids and in the unsteady worked example in the workshop notes.")

D.activity("act2", 2, 8, "pairs · derivation", "Your turn: the y-direction balance, then cancel dx dy",
           D.card(D.h3("Do") + D.ul(["Write Q<sub>y</sub> by the same argument as Q<sub>x</sub> (in through y = 0, out through y = dy).",
                                     "Put Q<sub>E</sub> = Q<sub>x</sub> + Q<sub>y</sub> + Q<sub>h</sub> and cancel the common factor dx dy.",
                                     "Check the units of every term in the result."], 30, gap=10), extra="width:960px"),
           col(D.eqpanel("e_Qx", "(2.2) — given", colw=656, maxh=110, pad="18px 32px"), D.eqpanel("e_QE", "(2.1) — given", colw=656, maxh=100, pad="18px 32px"),
               callout("Target: an equation with ∂T/∂t on the left and three terms on the right, none containing dx or dy.", "ok"), extra="flex:1"),
           "Reveal follows. If you finish early: what changes if q<sub>h</sub> depends on T?",
           notes="Walk around. Typical slip: writing the out-flux on the top face as q_y + (dq_y/dy) dx instead of dy. Another: forgetting that Q_y multiplies dx, not dy. "
                 "The unit check: rho C dT/dt is (kg/m3)(J/kg/K)(K/s) = W/m3; dq/dx is (W/m2)/m = W/m3; q_h is W/m3 by definition. "
                 "Early finishers: if q_h depends on T (e.g. Arrhenius hydration) the PDE becomes nonlinear; we keep q_h a given function of position.")

D.content("act2-reveal", "Activity 2 · solution", "The energy balance with dx dy cancelled",
          col(D.eqpanel("e_Qy", "(2.3)", maxw=1300, maxh=100, pad="18px 40px"), D.eqpanel("e_balance", "(2.6)", maxw=1500, maxh=100, pad="18px 40px"), D.eqpanel("e_balance2", "(2.7)", maxw=900, maxh=110, pad="18px 40px"),
              row(callout("Units of every term: W m<sup>−3</sup>. If one term disagrees, the derivation has a mistake.", "ok"),
                  callout("(2.7) still has three unknowns q<sub>x</sub>, q<sub>y</sub>, T. We need a law relating flux to temperature.", "why"), align="stretch")),
          notes="Show (2.3), then (2.6), then (2.7). Ask: how many unknowns, how many equations? Three unknowns and one equation, so we need Fourier’s law, two more equations.")

D.content("fourier", "Block 2 · Fourier’s law closes the system", "Heat flows down the temperature gradient",
          two_col(col(D.eqpanel("e_fourier", "(2.8), (2.9)", colw=980, maxh=120),
                      D.p("k<sub>x</sub>, k<sub>y</sub>: thermal conductivity in W m<sup>−1</sup> K<sup>−1</sup>. Isotropic material: k<sub>x</sub> = k<sub>y</sub> = k (concrete ≈ 1.5–2.5, steel ≈ 45–50).", 28),
                      D.p("Substituting (2.8)–(2.9) into (2.7) gives the general (unsteady) conduction equation:", 30),
                      D.eqpanel("e_pde_t", "(2.10)", colw=980, maxh=120)),
                  col(figbox(D.fig("fig_fourier", width=640)),
                      callout("The minus sign: where T falls with x (∂T/∂x < 0) the flux is positive, i.e. towards +x. Heat goes from hot to cold.", "why")),
                  lw=980, rw=640),
          notes="Fourier’s law is the constitutive law of this problem, the analogue of Hooke’s law for plane stress. The sign discussion matters later for boundary fluxes: "
                "an inward flux on the right edge of a plate is a negative q_x. The conductivity values are indicative only.")

D.content("pde-steady", "Block 2 · steady state · text §2.1.2", "Drop the time derivative: the PDE we discretise",
          col(D.eqpanel("e_pde", "(2.11)", colw=1664, maxh=140),
              row(D.card(D.h3("Special cases you already know") + D.eqpanel("e_poisson", "", colw=1598, maxh=160, bg=WHITE, pad="16px 32px"), extra="flex:1"), align="stretch"),
              row(callout("q<sub>h</sub> sits on the right with a minus sign because we moved it across; a source (q<sub>h</sub> > 0) makes the field concave — a hill.", "why"),
                  callout("Unit check of each term of (2.11): W m<sup>−3</sup>. The equation says: divergence of the flux = source.", "ok"), align="stretch")),
          notes="Equation 2.11 is the one students must be able to write from memory. Point out that with constant isotropic k it is Poisson’s equation and with no source it is Laplace’s equation, "
                "which they have met in fluid mechanics (potential flow) and soil mechanics (seepage).")

D.content("matrix-form", "Block 2 · the matrix form we will reuse · text (2.12)–(2.14)", "Write the operator as a row vector times [E] times a column vector",
          two_col(col(D.eqpanel("e_matrix", "(2.12)", colw=900, maxh=300), D.eqpanel("e_compact", "(2.13)", colw=900, maxh=90)),
                  col(D.eqpanel("e_defs", "(2.14)", colw=716, maxh=140),
                      callout("Why bother? In Plane Stress Part 1 plane stress will read [∂][E][∂]ᵀ{u}ᵀ = −{f}: the same shape with a 3 × 3 [E] and a 2 × 3 operator. Learn the pattern once.", "why"),
                      callout("{∂} is a row of operators, not numbers: it acts on whatever stands to its right. Order of multiplication matters.", "warn")),
                  lw=900),
          notes="This is the slide that pays off in Plane Stress. Multiply out (2.12) on the board to show it reproduces (2.11); students should see that [E] is diagonal because the material "
                "axes coincide with x and y. Warn that {∂} contains derivatives, so you cannot commute it past a function.")

# =============================================================================
# Block 3 — Boundary conditions
# =============================================================================
D.divider("d3", "3", "Boundary conditions", "A PDE alone is not a problem. Specify either the temperature or the flux on every part of the boundary. Text §2.1.3.",
          "Block 3 · 1:00 – 1:25", section="Block 3: Dirichlet and Neumann conditions, the rectangular-domain simplification, and what each type means for FEM",
          notes="Twenty-five minutes. The learning point is the distinction essential versus natural, because it decides what we do in the matrix system the next session.")

D.content("bc-types", "Block 3 · two kinds of condition · text (2.15)–(2.16)", "Either T or the normal flux is known at every boundary point",
          two_col(col(D.card(D.h3("Dirichlet · essential · temperature specified") + D.eqpanel("e_dirichlet", "(2.16)", maxw=400, maxh=80, bg=WHITE, pad="16px 40px")
                             + D.p("e.g. a face held at a fixed temperature by a fluid bath or the ground.", 26, MUTED)),
                      D.card(D.h3("Neumann · natural · normal flux specified") + D.eqpanel("e_neumann", "(2.15)", colw=1000, maxh=110, bg=WHITE, pad="16px 40px")
                             + D.p("q<sub>b</sub> known flux; (n<sub>x</sub>, n<sub>y</sub>) outward unit normal. Convection and radiation are Neumann-type too (not treated here).", 26, MUTED))),
                  col(figbox(D.fig("fig_bc", width=620)),
                      callout("Well-posed: the whole boundary is covered, and at least one point has T specified — otherwise T is only known up to a constant.", "warn")),
                  lw=1000, rw=620),
          notes="Dirichlet versus Neumann is the vocabulary; essential versus natural is the FEM meaning, which we explain two slides on. "
                "Ask what happens if the whole boundary is Neumann: the matrix system is singular because adding a constant to T changes nothing (the same as a free body in statics).")

D.content("bc-rect", "Block 3 · rectangular domains", "On a rectangle the normal is a coordinate axis, so (2.15) collapses to one term",
          col(row(D.eqpanel("e_rect_v", "vertical edges", colw=808, maxh=120), D.eqpanel("e_rect_h", "horizontal edges", colw=808, maxh=120), align="stretch"),
              D.eqpanel("e_insul", "insulated", colw=1664, maxh=120),
              row(callout("Sign: q<sub>b</sub> = k ∂T/∂n is positive when heat <b>enters</b>. On the right edge n = (+1, 0): an inward flux makes ∂T/∂x > 0 there, so q<sub>b</sub> > 0 — while the flux vector component q<sub>x</sub> = −k ∂T/∂x is negative. Two different symbols; keep them apart.", "warn"),
                  callout("Insulated = adiabatic = zero normal flux. It is a Neumann condition with q<sub>b</sub> = 0, not a Dirichlet condition.", "why"), align="stretch")),
          notes="Students lose marks on signs here. The rule: write the outward normal, then apply (2.15): q_b = k dT/dn. Heat entering through the right edge flows in the −x direction, so q_x = −k dT/dx < 0, hence dT/dx > 0 and q_b = k dT/dx × (+1) > 0. "
                "So q_b (the boundary flux of (2.15)) is positive for an inward flux; the flux-vector component q_x is negative. Next session this is why an inward flux is a positive load in {b}. "
                "Lecturer note: the text’s (2.41) writes the components with the opposite sign to (2.15); teach (2.15). The worked example avoids the issue by having only insulated and Dirichlet edges.")

D.content("bc-fem", "Block 3 · what FEM does with each kind", "Essential conditions are imposed; natural conditions appear by themselves",
          col(f'<table style="font-size:28px;color:{BODY};border:1px solid {HAIR}"><tr><th style="width:22%">Condition</th><th style="width:26%">What is known</th><th style="width:30%">Where it enters the FEM</th><th style="width:22%">Next session</th></tr>'
              f'<tr><td>Dirichlet · essential</td><td>T̄ on the edge</td><td>imposed on the assembled system by modifying rows and columns of [K]</td><td>row–column elimination</td></tr>'
              f'<tr><td>Neumann · natural</td><td>q<sub>b</sub> on the edge</td><td>appears in the boundary vector {{b}} produced by integration by parts</td><td>{{b}} = ∫{{N}}ᵀq<sub>n</sub> ds</td></tr>'
              f'<tr><td>Insulated · natural, q<sub>b</sub> = 0</td><td>no flux</td><td>contributes nothing: the boundary integral is zero</td><td>do nothing</td></tr></table>',
              row(callout("The most common error in Assignment 4: trying to “impose” an insulated edge. It needs no action at all.", "warn"),
                  callout("The names come from the integration by parts: the natural condition is the term that falls out of it; the essential one must be enforced on the unknowns.", "why"), align="stretch")),
          notes="This table is the bridge to the next session. Give the one-line reason: integration by parts produces a boundary integral containing the normal flux; where the flux is zero the "
                "integral vanishes, where it is known it becomes a load, and where it is unknown we must instead know T and remove that unknown from the system.")

D.activity("act3", 3, 6, "pairs · classification", "Label the plate: for each edge, type, equation and what FEM does",
           col(figbox(D.fig("fig_plate_ex5", width=760)), D.p("Text Exercise 2.5 geometry: k = 450 W m<sup>−1</sup> K<sup>−1</sup>, q<sub>h</sub> = 1 × 10<sup>7</sup> W m<sup>−3</sup>, unit thickness.", 26, MUTED), extra="width:820px"),
           D.card(D.h3("For each of the four edges write") + D.ul(["Dirichlet or Neumann?", "The equation, with the outward normal and the correct sign.", "Imposed, becomes a load, or do nothing?"], 30, gap=8)
                  + D.p("Then: is the problem well-posed? Why?", 30, DARK, 600), extra="flex:1"),
           "Reveal follows — then a 10-minute break.",
           notes="Answers: top edge T = 300 K, Dirichlet, imposed. Left edge T = 400 K, Dirichlet, imposed. Right edge: Neumann with inward flux 1e6 W/m2; outward normal (1, 0), "
                 "so (2.15) gives k dT/dx = q_b = +1e6 W/m2 (inward flux positive: the edge is hotter than the interior, dT/dx > 0); the flux-vector component is q_x = −1e6 W/m2. It becomes a load in {b}. "
                 "Bottom edge insulated: Neumann with q_b = 0, do nothing. Well-posed: yes, every edge has a condition and two edges fix T, so the solution is unique. "
                 "Common errors: calling the insulated edge Dirichlet, or mixing up q_b (boundary flux, inward positive) with q_x (flux-vector component).")

D.content("act3-reveal", "Activity 3 · solution", "Two essential edges, one flux load, one edge that needs nothing",
          col(f'<table style="font-size:28px;color:{BODY};border:1px solid {HAIR}"><tr><th style="width:14%">Edge</th><th style="width:20%">Type</th><th style="width:40%">Equation</th><th style="width:26%">FEM action</th></tr>'
              f'<tr><td>top</td><td>Dirichlet</td><td>T = 300 K</td><td>impose on the system</td></tr>'
              f'<tr><td>left</td><td>Dirichlet</td><td>T = 400 K</td><td>impose on the system</td></tr>'
              f'<tr><td>right</td><td>Neumann</td><td>n = (1, 0): k ∂T/∂x = q<sub>b</sub> = +1 × 10<sup>6</sup> W m<sup>−2</sup> (inward, so q<sub>x</sub> = −10<sup>6</sup>)</td><td>load in {{b}}</td></tr>'
              f'<tr><td>bottom</td><td>Neumann, q<sub>b</sub> = 0</td><td>∂T/∂y = 0</td><td>nothing</td></tr></table>',
              row(callout("Well-posed: every edge has a condition and T is fixed on two edges, so the temperature level is pinned.", "ok"),
                  callout("q<sub>b</sub> is the boundary flux of (2.15), positive inward; the flux-vector component q<sub>x</sub> points along −n and is negative.", "why"), align="stretch")),
          notes="Reveal row by row. Ask a pair to justify the sign on the right edge. Then break: 10 minutes.")

D.add("break", f'<div style="display:flex;flex-direction:column;gap:24px;flex:1;justify-content:center;align-items:center">'
               f'<p style="font-size:26px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:{AMBER}">1:25 – 1:35</p>'
               f'<h1 style="font-family:{SERIF};font-size:140px;font-weight:600;line-height:1;color:{LIGHT_ON_DARK}">Break</h1>'
               f'<p style="font-size:36px;color:{SOFT_ON_DARK};text-align:center;width:1200px">Back in 10 minutes. Second half: shape functions, gradients, and the pipeline for the next session.</p></div>'
               + D.footer(len(D.slides) + 1, dark=True),
      notes="Ten minutes. Put the slide up and start the second half on time.", bg=DARK, color=LIGHT_ON_DARK, transition="push")

# =============================================================================
# Block 4 — Shape functions
# =============================================================================
D.divider("d4", "4", "The four-node scalar element", "One unknown per node, a bilinear polynomial in between. Derive N₁…N₄ and learn the three properties you can always check. Text §2.2.1.",
          "Block 4 · 1:35 – 2:10", section="Block 4: degrees of freedom and derivation of the bilinear shape functions of the four-node rectangular element, with their properties",
          notes="Thirty-five minutes. This mirrors the bar element derivation from earlier in the course (assume a polynomial, evaluate at nodes, solve, collect), so keep reminding them of that.")

D.content("q4-dofs", "Block 4 · degrees of freedom · text Fig. 2.2", "A rectangle a × b, nodes numbered anticlockwise",
          two_col(figbox(D.fig("fig_q4", width=760)),
                  col(D.card(D.h3("Notation") + D.ul(["T̂<sub>i</sub> (hat): the nodal temperature at node i — a number, the unknown we solve for.",
                                                     "T(x, y): the temperature field inside the element — a function.",
                                                     "N<sub>i</sub>(x, y): the shape function that carries the influence of node i into the field.",
                                                     "Local coordinates: origin at node 1, x along the bottom edge, y along the left edge."], 28, gap=8)),
                      callout("Numbering is anticlockwise. Reverse it and the matrix entries the next session come out in the wrong places.", "warn")),
                  lw=800),
          notes="Insist on the hat. Students often write T_1 for both the nodal value and the field; from the next session the hat distinguishes {T̂}, the vector of unknowns, from T(x,y).")

D.content("poly", "Block 4 · assume a polynomial · text (2.17)", "Four nodes, four coefficients: 1, x, y and xy",
          two_col(col(D.eqpanel("e_poly", "(2.17)", colw=940, maxh=90),
                      D.card(D.h3("Why these four monomials?") + D.ul(["Four nodal values can fix exactly four coefficients.",
                                                                       "1, x, y give a plane; xy is the lowest-order term that is symmetric in x and y.",
                                                                       "x² without y² would favour one direction — the choice is geometrically balanced.",
                                                                       "Along any edge (x = const or y = const) the polynomial is linear in the other variable."], 28, gap=8))),
                  col(D.card(D.h3("Pascal triangle · text Fig. 2.4") +
                             f'<div style="display:flex;flex-direction:column;gap:6px;align-items:center;font-family:{SERIF}">'
                             f'<p style="font-size:34px;color:{MAROON};font-weight:600">1</p><p style="font-size:34px;color:{MAROON};font-weight:600">x&#160;&#160;&#160;&#160;&#160;&#160;y</p>'
                             f'<p style="font-size:34px;color:{BODY}">x²&#160;&#160;&#160;&#160;<span style="color:{MAROON}"><b>xy</b></span>&#160;&#160;&#160;&#160;y²</p>'
                             f'<p style="font-size:34px;color:{BODY}">x³&#160;&#160;&#160;x²y&#160;&#160;&#160;xy²&#160;&#160;&#160;y³</p></div>'
                             + D.p("4-node element: the four maroon terms. 8-node element: all terms down to x²y and xy² (Block 5).", 26, MUTED)),
                      callout("“Bilinear”: linear in x for fixed y and linear in y for fixed x — but not a plane, because of the xy term.", "why")),
                  lw=940),
          notes="Compare with the bar: there we assumed T = a1 + a2 x with two nodes. The pattern is the same. The xy term is what makes the element bilinear rather than planar; "
                "a plane would give only three coefficients for four nodes.")

D.content("nodes", "Block 4 · evaluate at the nodes · text (2.18)", "Each nodal value gives one equation in the coefficients",
          two_col(D.eqpanel("e_nodes", "(2.18)", colw=980, maxh=400),
                  col(D.eqpanel("e_nodes_matrix", "matrix form", colw=636, maxh=340),
                      callout("Lower-triangular after reordering, so it solves by forward substitution: a<sub>1</sub> first, then a<sub>2</sub>, a<sub>3</sub>, finally a<sub>4</sub>.", "why")),
                  lw=980),
          notes="Substitute the four node coordinates (0,0), (a,0), (a,b), (0,b). The matrix form is useful for the 8-node element where solving by hand is tedious and we let MATLAB invert it (text 2.26–2.30).")

D.content("coeffs", "Block 4 · solve for the coefficients · text (2.19)", "Four coefficients in terms of the four nodal temperatures",
          col(D.eqpanel("e_coeffs", "(2.19)", maxw=1600, maxh=140),
              row(D.card(D.h3("Read them physically") + D.ul(["a<sub>1</sub>: the value at the origin (node 1).", "a<sub>2</sub>: the slope along the bottom edge, (T̂<sub>2</sub> − T̂<sub>1</sub>)/a.",
                                                              "a<sub>3</sub>: the slope along the left edge, (T̂<sub>4</sub> − T̂<sub>1</sub>)/b.", "a<sub>4</sub>: the “twist” — how the x-slope changes with y."], 28, gap=8), extra="flex:1"),
                  D.card(D.h3("Check with a uniform field") + D.p("Put T̂<sub>1</sub> = T̂<sub>2</sub> = T̂<sub>3</sub> = T̂<sub>4</sub> = T<sub>0</sub>: then a<sub>1</sub> = T<sub>0</sub> and a<sub>2</sub> = a<sub>3</sub> = a<sub>4</sub> = 0, so T = T<sub>0</sub> everywhere. The element reproduces a constant exactly.", 28), extra="flex:1"), align="stretch")),
          notes="Do a_2 on the board: from the second equation a_2 = (T̂2 − T̂1)/a. The uniform-field check is the first sanity test of any element; it is the same idea as rigid-body motion for the bar element.")

D.content("shape", "Block 4 · collect by nodal value · text (2.20)–(2.22)", "The multiplier of each T̂ᵢ is its shape function Nᵢ",
          col(D.eqpanel("e_collect", "(2.20)", colw=1664, maxh=140), D.eqpanel("e_shape", "(2.21)", colw=1664, maxh=120),
              row(D.eqpanel("e_T_N", "(2.22)", colw=1100, maxh=80), callout("{N} is a 1 × 4 row; {T̂}ᵀ is a 4 × 1 column. Their product is the scalar T(x, y).", "why"), align="stretch")),
          notes="Insert (2.19) into (2.17) and collect the terms multiplying each T̂_i; this is the step students should do once by hand at home. "
                "The row-times-column form (2.22) is the one we will substitute into the PDE the next session; it is also (2.33) in the text, written for both the 4-node and the 8-node element.")

D.content("shape-pictures", "Block 4 · what a shape function looks like", "A tent: 1 at its own node, 0 at the other three, straight along every edge",
          two_col(f'<img src="{TENT}" alt="Shape function N3 drawn as a surface over the element: a tent that rises to 1 at node 3 and is zero at the other three nodes" style="width:620px;height:486px;object-fit:contain">',
                  col(f'<img src="{MAPS}" alt="Colour maps of N1 to N4 over the element, each equal to 1 at its own node and 0 at the others" style="width:980px;height:259px;object-fit:contain">',
                      D.p("Left: N<sub>3</sub> as a surface. Right: all four as colour maps (dark = 1). Each N<sub>i</sub> is the temperature field you get when node i is at 1 and the others at 0.", 28),
                      callout("Along an edge only the two nodes on that edge matter — the straight line of the bar element. That is what lets two neighbouring elements agree along their common edge.", "why")),
                  lw=640),
          notes="Point at the surface: a ridge line along each edge is straight, and the interior is a saddle-like bilinear surface. The colour maps show the symmetry: "
                "N2 is N1 mirrored in x, N4 is N1 mirrored in y, N3 is both. Students can plot these in MATLAB with meshgrid and surf in five lines.")

D.content("w9-ansys-N", "Block 4 · the same functions inside commercial code", "ANSYS’s four-node element uses these N₁ … N₄",
          two_col(webimg(SHAPEN, "Surface plots of the four bilinear shape functions N1 to N4 over the natural square from minus one to one", 560, 576),
                  col(D.card(D.h3("Same functions, new coordinates") + D.p("ξ = 2x/a − 1 and η = 2y/b − 1 map 0 ≤ x ≤ a, 0 ≤ y ≤ b onto −1 ≤ ξ, η ≤ 1, and", 27)
                             + D.p("N₁ = ¼(1 − ξ)(1 − η) = (a − x)(b − y)/ab", 30, DARK, 600) + D.p("which is the text’s (2.21). The other three follow by changing signs.", 27), pad=26, gap=10),
                      callout("Each surface is 1 at its own corner, 0 at the other three and straight along every edge: the three checks on the next slide.", "ok"),
                      callout("Plane Stress Part 2: the square lets one formula serve any four-sided element — the isoparametric idea behind PLANE182.", "why"),
                      credit("Image: PyMAPDL documentation, “Build a finite element model” (how a finite element works), © ANSYS, Inc., MIT licence, mapdl.docs.pyansys.com.")),
                  lw=616),
          notes="The plot comes from the PyMAPDL documentation example that builds a four-node element by hand and checks its stiffness against MAPDL. Point at N1: 1 at the corner "
                "(ξ, η) = (−1, −1), zero at the other corners, straight along every edge. Same functions as (2.21) after the change of variables on the slide.")

D.content("props", "Block 4 · three properties you can check in 30 seconds", "Kronecker delta, partition of unity, linear edges",
          col(row(D.card(D.h3("1 · Kronecker delta") + D.eqpanel("e_kron", "", colw=752, maxh=120, bg=WHITE, pad="16px 32px") + D.p("So T at node j equals T̂<sub>j</sub>: the nodal unknowns really are nodal temperatures.", 26, MUTED), extra="flex:1"),
                  D.card(D.h3("2 · Partition of unity") + D.eqpanel("e_pou", "", colw=752, maxh=120, bg=WHITE, pad="16px 32px") + D.p("A uniform temperature is reproduced exactly — the test we did on the coefficients.", 26, MUTED), extra="flex:1"), align="stretch"),
              D.card(D.h3("3 · Linear along each edge") + D.eqpanel("e_edge", "", colw=1598, maxh=100, bg=WHITE, pad="16px 32px")
                     + D.p("C⁰ continuity follows: the neighbouring element shares this edge’s two nodes and its straight line.", 26, MUTED))),
          notes="These three checks catch most errors in shape functions, including in the 8-node element and in plane stress. Ask students to verify the Kronecker property "
                "for N_2 at node 3 quickly on paper: N_2(a,b) = a(b−b)/(ab) = 0.")

D.content("w9-tent", "Block 4 · from one element to the mesh", "One nodal value lifts one tent",
          row(col(webimg(HAT1D, "Two overlapping one-dimensional hat functions phi 2 and phi 3 on a mesh of five elements", 700, 266),
                  D.p("1D: φᵢ is a hat over the two elements that share node i.", 26, MUTED), extra="flex:1"),
              col(webimg(TENT2D, "A two-dimensional tent function rising to one at an interior node of a triangular mesh and zero at all other nodes", 420, 287),
                  D.p("2D: a tent over every element sharing the node.", 26, MUTED), extra="width:560px"), align="start")
          + callout("Each element that touches node i adds one face of its tent. That is why T is continuous across element edges, and why node i couples only to its neighbours: the global matrix is sparse (Heat Transfer Part 2).", "why")
          + credit("Images: Langtangen and Mardal, <i>Introduction to Numerical Methods for Variational Problems</i> (Springer, 2019), github.com/hplgit/fem-book, MIT licence."),
          notes="Link the element view (four shape functions in one element) to the global view (one basis function per node, made of pieces from every element around it). "
                "This prepares assembly the next session: the global row of node i has entries only for nodes in the elements around i.")

D.activity("act4", 4, 8, "pairs · calculation", "Evaluate the shape functions at a point and interpolate the temperature",
           col(figbox(D.fig("fig_q4_point", width=700)), extra="width:760px"),
           col(D.card(D.h3("Given") + D.ul(["a = 2 m, b = 1 m; point (x, y) = (1.5, 0.3) m.", "Nodal temperatures T̂ = {100, 140, 160, 120} K."], 30, gap=8)
                      + D.h3("Find") + D.ul(["N<sub>1</sub>, N<sub>2</sub>, N<sub>3</sub>, N<sub>4</sub> at the point — and their sum.", "T(1.5, 0.3)."], 30, gap=8)),
               callout("Keep the sheet: Activity 5 uses the same element and data.", "ok"), extra="flex:1"),
           "8 minutes. Early finishers: which node has the most influence at this point, and why?",
           notes="Answers: N1 = (0.5)(0.7)/2 = 0.175; N2 = (1.5)(0.7)/2 = 0.525; N3 = (1.5)(0.3)/2 = 0.225; N4 = (0.3)(0.5)/2 = 0.075; sum = 1.000. "
                 "T = 0.175×100 + 0.525×140 + 0.225×160 + 0.075×120 = 17.5 + 73.5 + 36 + 9 = 136.0 K. "
                 "Node 2 dominates because the point is closest to it (x = 1.5 of 2, y = 0.3 of 1). This is exactly part (c) of the Assignment 4 type question (interpolate T at a given point).")

D.content("act4-reveal", "Activity 4 · solution", "Node 2 carries half the weight; the four weights sum to one",
          col(D.eqpanel("e_act4_N", "(2.21) at (1.5, 0.3)", colw=1664, maxh=210, pad="18px 40px"), D.eqpanel("e_act4_sum", "partition of unity", colw=1664, maxh=70, pad="14px 40px"), D.eqpanel("e_act4_T", "(2.22)", colw=1664, maxh=115, pad="18px 40px"),
              D.p("Assignment-type question: “after solving, T̂<sub>2</sub> and T̂<sub>6</sub> are 150 K … interpolate T at (1.4, 2.2)” — the same method, after converting the global point to local element coordinates.", 26, MUTED)),
          notes="Emphasise local coordinates: in a mesh the point must first be located in its element and its coordinates measured from that element’s node 1. We do this the next session in the post-processing slide.")

# =============================================================================
# Block 5 — Gradient and flux
# =============================================================================
qr_lab(D, "qr-shape", 6, "Check Activity 4 on your phone, then explore",
       ["Press “Activity 4 point”. Do N₁ … N₄, their sum and T = 136.0 K match your sheet?",
        "Drag P onto node 3 and read the four weights. Which property is this?",
        "Find three points where N₁ = N₃. What line joins them?"],
       [LABS["shape"]], "6 minutes, optional in class: if the block is running late, set it as homework. Answers are inside the Explorer under “Check answer”.",
       notes="Before class: the QR code opens the public copy on GitHub Pages (no login); open it once on a phone. "
             "Answers: (1) 0.175, 0.525, 0.225, 0.075; sum 1; T = 136.0 K. (2) N = (0, 0, 1, 0): the Kronecker delta property. (3) The diagonal from node 2 to node 4, x/a + y/b = 1. "
             "Extension in the Explorer: the 8-node N1 is negative over most of the element (−0.25 at the centre); the sum is still 1.")

D.divider("d5", "5", "Gradient, flux and a look ahead", "Differentiate the approximation: the 2 × 4 matrix {∂}ᵀ{N} gives the gradient, Fourier gives the flux — and the next session it builds [k].",
          "Block 5 · 2:10 – 2:35", section="Block 5: derivatives of the shape functions, the gradient and flux inside an element, and a one-slide preview of the eight-node element",
          notes="Twenty-five minutes. The derivatives are the ingredient of both post-processing and the conductance matrix, so this block saves time the next session.")

D.content("grad", "Block 5 · differentiate the approximation", "Gradient = derivative matrix × nodal temperatures",
          col(D.eqpanel("e_grad", "", colw=1664, maxh=270, pad="18px 40px"), D.eqpanel("e_dN", "from (2.21)", colw=1664, maxh=105, pad="14px 40px"),
              row(callout("∂N<sub>i</sub>/∂x depends on y only and ∂N<sub>i</sub>/∂y on x only — the gradient varies inside the element, though each component is constant along one direction.", "why"),
                  callout("Each row of {∂}ᵀ{N} sums to zero. A uniform T̂ therefore gives zero gradient, as it must.", "ok"), align="stretch")),
          notes="Derive one entry on the board: dN1/dx = −(b−y)/(ab). Then show the row-sum-zero property: −(b−y)+(b−y)+y−y = 0. "
                "Next session the same 2 by 4 matrix is sandwiched as {N}ᵀ{∂}[E]{∂}ᵀ{N} and integrated to give [k]; students who are comfortable with it now will find k_34 easy.")

D.content("flux", "Block 5 · from gradient to flux", "Fourier’s law in matrix form is the post-processing formula",
          two_col(col(D.eqpanel("e_flux_vec", "", colw=720, maxh=140),
                      D.p("Once the nodal temperatures are known, this gives the heat flux at any point (x, y) of the element — the quantity a designer usually wants (heat loss through a wall, flow under a dam).", 30)),
                  col(D.eqpanel("e_k_preview", "", colw=896, maxh=230), D.p("Next session: text (2.38) and (2.42).", 26, MUTED),
                      callout("The same {∂}ᵀ{N} appears twice in [k], once transposed: [k] is symmetric, and its row sums are zero for the same reason the gradient of a uniform field is zero.", "why")),
                  lw=720),
          notes="Two uses of one matrix. Flux now, conductance the next session. Mention that because the gradient is only piecewise constant-ish, the flux is discontinuous between elements; "
                "that is why software averages fluxes at nodes, which we will see in ANSYS in the ANSYS demo.")

D.activity("act5", 5, 8, "pairs · calculation", "Heat flux at the same point: evaluate the derivatives, then apply Fourier",
           col(figbox(D.fig("fig_q4_point", width=700)), extra="width:760px"),
           col(D.card(D.h3("Given (as Activity 4)") + D.ul(["a = 2 m, b = 1 m, point (1.5, 0.3) m, T̂ = {100, 140, 160, 120} K.", "k<sub>x</sub> = k<sub>y</sub> = 2 W m<sup>−1</sup> K<sup>−1</sup>."], 28, gap=6)
                      + D.h3("Find") + D.ul(["∂N<sub>i</sub>/∂x for i = 1…4, then ∂T/∂x.", "q<sub>x</sub> from Fourier’s law — sign and direction?", "If time: ∂T/∂y and q<sub>y</sub>."], 28, gap=6), pad=26, gap=10),
               callout("Check: the four derivatives must sum to zero.", "ok"), extra="flex:1"),
           "8 minutes. Reveal follows.",
           notes="Answers: dN/dx = (1/ab){−(b−y), (b−y), y, −y} = {−0.35, 0.35, 0.15, −0.15}; sum zero. dT/dx = −35 + 49 + 24 − 18 = 20 K/m. q_x = −2 × 20 = −40 W/m2, "
                 "i.e. 40 W/m2 flowing in the negative x direction (from the hotter right side towards the left). dN/dy = {−0.25, −0.75, 0.75, 0.25}; dT/dy = −25 − 105 + 120 + 30 = 20 K/m; q_y = −40 W/m2. "
                 "Ask: does the sign make sense? The right-hand nodes (140, 160) are hotter than the left (100, 120), so heat flows towards −x. Yes.")

D.content("act5-reveal", "Activity 5 · solution", "Heat flows from the hot side (nodes 2, 3) towards the cold side",
          col(D.eqpanel("e_act5_dN", "", colw=1664, maxh=92, pad="14px 40px"), D.eqpanel("e_act5_grad", "", colw=1664, maxh=165, pad="14px 40px"), D.eqpanel("e_act5_q", "", colw=1664, maxh=92, pad="14px 40px"), D.eqpanel("e_act5_qy", "", colw=1664, maxh=92, pad="14px 40px"), gap=20),
          notes="Walk through the four lines. The negative q_x means the flux vector points towards −x: from the hot nodes 2 and 3 towards nodes 1 and 4. Same for y by the symmetry of the data.")

D.content("q8", "Block 5 · the eight-node element in one slide · text §2.2.1, Fig. 2.3", "Mid-side nodes, eight monomials, quadratic along each edge",
          two_col(figbox(D.fig("fig_q8", width=560)),
                  col(D.eqpanel("e_poly8", "(2.23)", colw=1016, maxh=90), D.eqpanel("e_N8", "(2.30), (2.31e)", colw=1016, maxh=130),
                      D.ul(["Same recipe: evaluate at 8 nodes, invert the 8 × 8 matrix, collect — the text gives N<sub>1</sub>…N<sub>8</sub> in (2.31).",
                            "Three nodes per edge, so T is quadratic along an edge: fewer elements for curved fields.",
                            "Hand calculations here use the 4-node element; the 8-node one lives in the MATLAB code and in ANSYS (PLANE183-type)."], 28, gap=8)),
                  lw=600),
          notes="One slide only. The point is that nothing conceptually new happens: more nodes, more monomials from the Pascal triangle, the same three properties. "
                "In the worked example the next session the 8-node mesh with 2 elements gives a closer answer than the 4-node mesh with 4 elements; we will compare both to software.")

# =============================================================================
# Block 6 — Pipeline, MATLAB, wrap-up
# =============================================================================
D.divider("d6", "6", "The pipeline — where today fits", "Seven steps from PDE to answer. Today covered the first two; the next session we do the other five and run the MATLAB code.",
          "Block 6 · 2:35 – 3:00", section="Block 6: the seven-step FEM pipeline, the MATLAB skeleton that follows it, exit ticket and preparation for Heat Transfer Part 2",
          notes="Twenty-five minutes including the exit ticket. Keep the energy up: this block is about seeing the whole road.")

steps7 = [("1", "PDE + boundary conditions", "today"), ("2", "Shape functions {N}", "today"), ("3", "Galerkin weighted residual", "Heat Transfer Part 2"), ("4", "Integration by parts", "Heat Transfer Part 2"),
          ("5", "Element matrices [k], {q}, {b}", "Heat Transfer Part 2"), ("6", "Assembly + impose T̄", "Heat Transfer Part 2"), ("7", "Solve, then post-process", "Heat Transfer Part 2")]
cards7 = ""
for n, t, w in steps7:
    done = w == "today"
    cards7 += (f'<div style="background:{AMBER if done else WHITE};border:1px solid {HAIR};border-radius:14px;padding:14px 12px;display:flex;flex-direction:column;gap:6px;min-width:0">'
               f'<p style="font-family:{SERIF};font-size:48px;font-weight:600;line-height:1;color:{MAROON}">{n}</p><p style="font-size:26px;font-weight:600;line-height:1.2;color:{DARK}">{t}</p>'
               f'<p style="font-size:24px;color:{MUTED}">{w}</p></div>')
D.content("pipeline", "Block 6 · seven steps from PDE to answer", "Today: steps 1 and 2. Next session: steps 3 to 7 on the text’s worked example",
          f'<div style="display:grid;grid-template-columns:repeat(7, 1fr);gap:12px">{cards7}</div>'
          + two_col(figbox(D.fig("fig_plate_book", width=330)) ,
                    col(D.h3("The next session’s worked example · text §2.3"),
                        D.p("Square plate 1 m × 1 m, q<sub>h</sub> = 600 W m<sup>−3</sup>, k<sub>x</sub> = k<sub>y</sub> = 300 W m<sup>−1</sup> K<sup>−1</sup>; top and left edges at 0 °C, right and bottom edges insulated. Four 4-node elements by hand, then 64 elements in MATLAB, then software.", 28),
                        D.p("Before the next session, classify its four edges as in Activity 3 and predict where the hottest point is.", 28, DARK, 600)),
                    lw=380, align="center"),
          notes="Give the prediction task: hottest point is the bottom-right corner, where both insulated edges meet, farthest from the two cold edges. Students who predict this have understood the boundary conditions. "
                "Note for the lecturer: the text’s Fig. 2.5 caption says k = 400 but the numbers in (2.51) and the code use k = 300; use 300.")

code = ["% Local conductance matrix (text §2.3.1)", "a = L/Nx;  b = H/Ny;", "s1 =  b*kx/(3*a) + a*ky/(3*b);", "s2 = -b*kx/(3*a) + a*ky/(6*b);", "s3 = -b*kx/(6*a) - a*ky/(6*b);",
        "s4 =  b*kx/(6*a) - a*ky/(3*b);", "k  = [s1 s2 s3 s4; s2 s1 s4 s3; s3 s4 s1 s2; s4 s3 s2 s1];", "fQ = a*b*Q/4*[1; 1; 1; 1];          % heat generation",
        "% Assembly by connectivity, element 1 = nodes [1 2 5 4]", "K([1 2 5 4],[1 2 5 4]) = K([1 2 5 4],[1 2 5 4]) + k;", "F([1 2 5 4]) = F([1 2 5 4]) + fQ;",
        "% Impose T = To on known dofs, solve the rest", "dof_k = [1 4 7 8 9];  T(dof_k) = To;", "F = F - K(:,dof_k)*T(dof_k);", "dof_u = setdiff(1:ndof, dof_k);", "T(dof_u) = K(dof_u,dof_u) \\ F(dof_u);"]
D.content("matlab", "Block 6 · the MATLAB skeleton follows the pipeline", "Thirty lines: local matrix, assembly, boundary conditions, solve",
          two_col(D.code(code, 23),
                  col(D.card(D.h3("Read the code against the steps") + D.ul(["Lines 2–8: step 5, the element matrix and load from closed-form integrals (we derive s<sub>1</sub>…s<sub>4</sub> the next session).",
                                                                             "Lines 11–12: step 6, assembly — the connectivity list [1 2 5 4] is the element’s global node numbers.",
                                                                             "Lines 15–18: step 6, essential conditions by row–column elimination; step 7, solve with the backslash operator."], 26, gap=8)),
                      callout("Bring a laptop with MATLAB the next session; we trace this code line by line on the 2 × 2 mesh.", "ok")),
                  lw=1000),
          notes="Do not explain the formulas for s1 to s4 now; just show that the program is the pipeline. Students who can map code lines to pipeline steps will write Assignment 4 much faster.")

D.activity("exit", 6, 6, "individual · exit ticket", "Three questions before you leave — on paper, hand in at the door",
           D.card(D.h3("Questions") + D.ul(["Which boundary condition needs no action at all in the FEM, and why?",
                                            "For a square element (a = b), what is each N<sub>i</sub> at the centroid? What is their sum?",
                                            "Write {∂}[E]{∂}ᵀT = −q<sub>h</sub> out in full for k<sub>x</sub> = k<sub>y</sub> = k. Which classical equation is it?"], 30, gap=12), extra="width:1000px"),
           col(D.eqpanel("e_cent", "hint for Q2", colw=616, maxh=120, bg=WHITE), D.eqpanel("e_exit3", "Q3", colw=616, maxh=80, bg=WHITE), extra="flex:1"),
           "Six minutes. Name and matric number on the sheet; this is for feedback, not marks.",
           notes="Answers: (1) the insulated (zero-flux) edge: it is a natural condition with q_b = 0, so its boundary integral vanishes. "
                 "(2) each N_i = 1/4 at the centroid; sum = 1. (3) k(∂²T/∂x² + ∂²T/∂y²) = −q_h, Poisson’s equation (Laplace if q_h = 0). "
                 "Sort the tickets by question 1: those who answered “Dirichlet” need the essential/natural table again at the start of the next session.")

D.content("summary", "Wrap-up · what to take away and what to prepare", "Next session: Galerkin, integration by parts, [k], assembly and the worked example",
          two_col(D.card(D.h3("Today in four lines") + D.ul(["Energy balance + Fourier → (2.11): divergence of flux = source, written as {∂}[E]{∂}ᵀT = −q<sub>h</sub>.",
                                                              "Dirichlet = essential = imposed; Neumann = natural = appears from integration by parts; insulated = do nothing.",
                                                              "Four-node element: T = {N}{T̂}ᵀ with bilinear N<sub>i</sub>; Kronecker delta, partition of unity, linear edges.",
                                                              "{∂}ᵀ{N} (2 × 4) gives the gradient and, with −[E], the flux — and the next session, [k]."], 28, gap=10)),
                  col(D.card(D.h3("Before Heat Transfer Part 2") + D.ul(["Read text §2.2.2 and §2.3 (worked example) — 12 pages.", "Redo Activities 4 and 5 for the point (0.5, 0.8) m.",
                                                           "Classify the edges of the §2.3 plate and predict the hottest point.", "Bring MATLAB; Assignment 4 is released at the end of Heat Transfer Part 2."], 28, gap=10)),
                      D.p("Questions: arazin@utm.my · Office M50-02-29", 26, MUTED)),
                  lw=940),
          notes="Close on time. Collect exit tickets. Remind them that Assignment 4 is a hand calculation exactly along today’s and the next session’s steps.")

order = D.write("2026-10-26T14:30:00Z")
print(len(order), "slides:", order)
