"""Content of Part 1 — 2D Heat Transfer (Part 1): notes, exercises, lab tasks, glossary, short notes.

English is the primary text; Malay carries the explanation with technical terms left in English.
Numbers quoted in the notes are those of the deck (verified against fe_core and the text).
"""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, TRY, QC, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME

PART = {
    "n": 1, "slug": "01-heat-transfer-1", "deck": "deck_w9", "eqs": ["eqs_w9", "eqs_ex"], "figs": ["figs_w9", "figs_ex"],
    "topic": ("2D Heat Transfer", "2D Heat Transfer"), "part": "Part 1 of 2",
    "title": "2D Heat Transfer — Part 1",
    "sub": ("From the energy balance to the shape functions of the four-node element: the PDE, its boundary conditions, "
            "and how temperature is interpolated inside one element.",
            "Daripada energy balance kepada shape function bagi four-node element: PDE, boundary condition, "
            "dan cara temperature di-interpolate di dalam satu element."),
    "pdf": "pdf/heat-transfer-1-slides.pdf",
    "lab": {"id": "shape", "file": "../labs/shape.html", "name": "Shape Function Explorer", "inclass": "act4"},
    "minutes": {"n1": 6, "n2": 10, "n3": 7, "n4": 12, "n5": 7, "n6": 5},
    "target_min": 30,
    "code": "shape",
    "textref": "§2.1–§2.2.1",
    "covers": ("Heat conduction in a plate is the simplest two-dimensional field problem, and it carries every idea the rest of the course needs: a governing PDE, its boundary conditions, an element with shape functions, and the gradient of the interpolated field. Part 2 turns these into element matrices and a solved mesh.",
               "Heat conduction dalam plat ialah field problem dua dimensi yang paling mudah, dan ia membawa setiap idea yang diperlukan oleh baki kursus ini: PDE pentadbir, boundary condition-nya, element dengan shape function, dan gradient bagi field yang di-interpolate. Part 2 menukarkan semua ini kepada matrix element dan mesh yang diselesaikan."),
    "inclass_n": ("3 h · 5 activities", "3 jam · 5 aktiviti"),
    "inclass": [("A1 scalar or vector · A2 the y-direction balance", "A1 scalar atau vector · A2 keseimbangan arah y"),
                ("A3 boundary conditions of the plate", "A3 boundary condition bagi plat"),
                ("A4 + A5 shape functions and flux at (1.5, 0.3)", "A4 + A5 shape function dan flux pada (1.5, 0.3)")],
    "recall_title": ("Recall from the first half of the course", "Ingat semula separuh pertama kursus"),
}

OUTCOMES = [
    ("Derive the steady 2D heat-conduction PDE from an energy balance and Fourier’s law, and write it as {∂}[E]{∂}ᵀT = −q<sub>h</sub>.",
     "Menerbitkan steady 2D heat-conduction PDE daripada energy balance dan Fourier’s law, dan menulisnya sebagai {∂}[E]{∂}ᵀT = −q<sub>h</sub>."),
    ("Classify boundary conditions as Dirichlet (essential) or Neumann (natural) and write them for a rectangular domain.",
     "Mengelaskan boundary condition sebagai Dirichlet (essential) atau Neumann (natural) dan menulisnya untuk rectangular domain."),
    ("Derive the bilinear shape functions N<sub>1</sub>…N<sub>4</sub> of the four-node element and use them to interpolate T(x, y).",
     "Menerbitkan bilinear shape function N<sub>1</sub>…N<sub>4</sub> bagi four-node element dan menggunakannya untuk interpolate T(x, y)."),
    ("Differentiate the approximation to obtain the temperature gradient and the heat flux at any point of an element.",
     "Membezakan approximation tersebut untuk mendapatkan temperature gradient dan heat flux pada mana-mana titik dalam element."),
]

CANDO = [
    ("Write (2.11) from memory and say what each term means, with units.", "Menulis (2.11) tanpa melihat nota dan menyatakan maksud setiap term, dengan unit."),
    ("Label every edge of a rectangular plate: Dirichlet or Neumann, the equation with the outward normal, and what FEM does with it.", "Melabel setiap tepi plat segi empat: Dirichlet atau Neumann, persamaannya dengan outward normal, dan apa yang FEM buat dengannya."),
    ("Evaluate N<sub>1</sub>…N<sub>4</sub> at a point and interpolate T, and check the sum.", "Menilai N<sub>1</sub>…N<sub>4</sub> pada satu titik dan interpolate T, serta menyemak hasil tambahnya."),
    ("Compute ∂T/∂x, ∂T/∂y and the flux at a point from the nodal temperatures.", "Mengira ∂T/∂x, ∂T/∂y dan flux pada satu titik daripada nodal temperature."),
]


def notes(A):
    """A = Assets for eqs_w9 / figs_w9. Returns [(id, title_en, title_ms, html)]."""
    S = []

    # ---- n1 --------------------------------------------------------------
    body = (
        P("Everything in the first half of the course was one-dimensional: a bar, a beam, a truss, a frame. The unknowns sat on a line. "
          "From here on the unknown is a <i>field</i>: a temperature T(x, y) defined at every point of a plate. We cannot solve for infinitely many "
          "values, so we solve for a finite number of them at nodes and let the element interpolate in between. That is the whole idea of the method.",
          "Semua yang kita buat pada separuh pertama kursus ini bersifat satu dimensi: bar, beam, truss, frame. Unknown terletak pada satu garis. "
          "Mulai sekarang unknown ialah satu <i>field</i>: temperature T(x, y) yang wujud pada setiap titik plat. Kita tidak mampu menyelesaikan "
          "nilai yang tak terhingga banyaknya, jadi kita selesaikan nilai pada node sahaja dan biarkan element membuat interpolation di antaranya. Itulah keseluruhan idea kaedah ini.")
        + DEF("FEM is “nothing”, and FEM is “everything”", "FEM itu “tiada apa-apa”, dan FEM itu “segala-galanya”",
              "Nothing: FEM adds no new physics. It is only a way to turn a differential equation into simultaneous algebraic equations in matrix form. "
              "Everything: the same machinery solves heat, seepage, stress, vibration and fluid flow. Learn it once, on the simplest field problem, and reuse it.",
              "Tiada apa-apa: FEM tidak menambah fizik baharu. Ia hanya cara menukar differential equation kepada simultaneous algebraic equation dalam bentuk matrix. "
              "Segala-galanya: jentera yang sama menyelesaikan heat, seepage, stress, vibration dan fluid flow. Pelajari sekali pada field problem yang paling mudah, kemudian guna semula.")
        + H3("Scalar field first, vector field later", "Scalar field dahulu, vector field kemudian")
        + SB(P("Heat conduction is a <b>scalar</b> field problem: one unknown per node, the temperature T̂<sub>i</sub>. Plane stress, later in the course, is a <b>vector</b> field problem: "
               "two unknowns per node, the displacements u<sub>i</sub> and v<sub>i</sub>. Every idea of this part — shape functions, boundary conditions, assembly — appears in both; "
               "plane stress only has bigger matrices.",
               "Heat conduction ialah <b>scalar</b> field problem: satu unknown setiap node, iaitu temperature T̂<sub>i</sub>. Plane stress, kemudian dalam kursus ini, ialah <b>vector</b> field problem: "
               "dua unknown setiap node, iaitu displacement u<sub>i</sub> dan v<sub>i</sub>. Setiap idea dalam bahagian ini — shape function, boundary condition, assembly — muncul dalam kedua-duanya; "
               "plane stress cuma ada matrix yang lebih besar."))
        + A.fig("fig_scalar_vector", "Left: a scalar field, one number at each node. Right: a vector field, two numbers at each node.",
                "Kiri: scalar field, satu nombor pada setiap node. Kanan: vector field, dua nombor pada setiap node.", 560)
        + H3("Where civil engineers meet conduction", "Di mana jurutera awam bertemu conduction")
        + LI([("<b>Mass concrete.</b> Heat of hydration in dams, rafts and pile caps: the temperature rise and the gradient between core and surface drive early-age cracking.",
               "<b>Mass concrete.</b> Heat of hydration dalam empangan, raft dan pile cap: kenaikan temperature dan gradient antara teras dan permukaan menyebabkan early-age cracking."),
              ("<b>Fire engineering.</b> Temperature rise in steel sections and tunnel linings decides when strength is lost; the input is a 2D conduction model of the section.",
               "<b>Fire engineering.</b> Kenaikan temperature dalam keratan keluli dan tunnel lining menentukan bila kekuatan hilang; inputnya ialah model conduction 2D bagi keratan itu."),
              ("<b>Pavements and decks.</b> Daily thermal gradients through a bridge deck or a pavement slab produce stresses that design codes make us check.",
               "<b>Pavement dan deck.</b> Thermal gradient harian merentasi bridge deck atau pavement slab menghasilkan stress yang design code mewajibkan kita semak."),
              ("<b>Ground and geothermal.</b> Ground freezing, energy piles and buried pipelines are conduction problems in soil — and seepage uses the same equation.",
               "<b>Tanah dan geothermal.</b> Ground freezing, energy pile dan paip tertanam ialah masalah conduction dalam tanah — dan seepage menggunakan persamaan yang sama.")])
        + '<figure><img src="slides/img/w9_cht.png" alt="Temperature in a channel flow and in the solid plate below it, heated from its bottom face" class="figimg">'
        + '<figcaption>' + B("A heated plate under a channel flow. The solid plate obeys this part’s conduction PDE; at its interface with the fluid it receives a temperature and returns a heat flux — one Dirichlet and one Neumann condition (§3).",
                              "Plat panas di bawah channel flow. Plat pepejal mematuhi conduction PDE bahagian ini; pada interface dengan bendalir ia menerima temperature dan memulangkan heat flux — satu Dirichlet dan satu Neumann condition (§3).")
        + '<span class="credit"> Image: preCICE tutorials, “Flow over a heated plate”, LGPL-3.0, github.com/precice/tutorials.</span></figcaption></figure>'
        + KP([("The unknown is a field T(x, y); FEM solves for nodal values and interpolates between them.", "Unknown ialah field T(x, y); FEM menyelesaikan nilai pada node dan interpolate di antaranya."),
              ("FEM adds no physics; it turns a PDE into [K]{T̂} = {r}.", "FEM tidak menambah fizik; ia menukar PDE kepada [K]{T̂} = {r}."),
              ("Scalar field: one unknown per node. Plane stress will have two.", "Scalar field: satu unknown setiap node. Plane stress akan ada dua.")])
        + QC("q1", "What does the finite element method add to the physics of heat conduction?", "Apa yang finite element method tambah kepada fizik heat conduction?",
             [("a", "Fourier’s law", "Fourier’s law"), ("b", "Nothing — it only discretises the PDE", "Tiada apa-apa — ia hanya discretise PDE"), ("c", "A heat-generation term", "Satu term heat generation")],
             "b", "Nothing. The physics is the energy balance and Fourier’s law; FEM is a numerical method that turns the resulting PDE into algebraic equations.",
             "Tiada apa-apa. Fiziknya ialah energy balance dan Fourier’s law; FEM ialah kaedah berangka yang menukar PDE itu kepada algebraic equation.")
    )
    S.append(("n1", "Why a 2D field problem, and what FEM delivers", "Mengapa 2D field problem, dan apa yang FEM beri", body))

    # ---- n2 --------------------------------------------------------------
    body = (
        P("Take a small rectangle dx by dy inside the plate, of unit thickness. The dependent variables are the heat fluxes q<sub>x</sub> and q<sub>y</sub> "
          "(W m<sup>−2</sup>): energy per unit time per unit area crossing a face. Heat enters through the near faces and leaves through the far faces.",
          "Ambil satu segi empat kecil dx × dy di dalam plat, dengan ketebalan unit. Dependent variable ialah heat flux q<sub>x</sub> dan q<sub>y</sub> "
          "(W m<sup>−2</sup>): tenaga per unit masa per unit luas yang melintasi satu muka. Haba masuk melalui muka dekat dan keluar melalui muka jauh.")
        + A.fig("fig_diffelem", "The differential element: fluxes in and out, generation q<sub>h</sub> inside (text Fig. 2.1).",
                "Differential element: flux masuk dan keluar, generation q<sub>h</sub> di dalam (teks Rajah 2.1).", 520)
        + SB(P("The flux on the far face is the near-face flux plus its change across the element, a first-order Taylor expansion. The net inflow in the x-direction is therefore",
               "Flux pada muka jauh ialah flux muka dekat ditambah perubahannya merentasi element, iaitu first-order Taylor expansion. Jadi net inflow dalam arah x ialah"))
        + A.eq("e_Qx", "(2.2)")
        + SB(P("and by the same argument in the y-direction", "dan dengan hujah yang sama dalam arah y"))
        + A.eq("e_Qy", "(2.3)")
        + SB(P("Inside, heat is generated at a rate q<sub>h</sub> per unit volume (W m<sup>−3</sup>), for example the hydration of cement, and the element stores energy as its temperature rises:",
               "Di dalam, haba dijana pada kadar q<sub>h</sub> per unit isi padu (W m<sup>−3</sup>), contohnya hydration simen, dan element menyimpan tenaga apabila temperature-nya naik:"))
        + '<div class="eqrow">' + A.eq("e_Qh", "(2.5)") + A.eq("e_QE", "(2.1)") + '</div>'
        + H3("Conservation of energy", "Conservation of energy")
        + SB(P("Rate of change of stored energy = net conduction in + heat generated. Every term carries the factor dx dy, the volume of the element per unit thickness, so it cancels:",
               "Kadar perubahan tenaga tersimpan = net conduction masuk + haba dijana. Setiap term membawa faktor dx dy, iaitu isi padu element per unit ketebalan, jadi ia terbatal:"))
        + A.eq("e_balance", "(2.6)") + A.eq("e_balance2")
        + NOTE("Per unit thickness", "Per unit ketebalan",
               "Every quantity is multiplied by the same thickness t, which cancels, so we take t = 1. Nothing changes for a plate of any thickness as long as the faces are insulated.",
               "Setiap kuantiti didarab dengan ketebalan t yang sama, yang terbatal, jadi kita ambil t = 1. Tiada yang berubah untuk plat setebal mana pun selagi mukanya insulated.")
        + H3("Fourier’s law closes the system", "Fourier’s law melengkapkan sistem")
        + SB(P("The balance has three unknowns (T, q<sub>x</sub>, q<sub>y</sub>) and one equation. Fourier’s law supplies the other two: heat flows down the temperature gradient, "
               "in proportion to the conductivity k (W m<sup>−1</sup> K<sup>−1</sup>). The minus sign is the physics: flux points from hot to cold.",
               "Balance ini ada tiga unknown (T, q<sub>x</sub>, q<sub>y</sub>) dan satu persamaan. Fourier’s law membekalkan dua lagi: haba mengalir menuruni temperature gradient, "
               "berkadar dengan conductivity k (W m<sup>−1</sup> K<sup>−1</sup>). Tanda negatif itulah fiziknya: flux menghala dari panas ke sejuk."))
        + A.eq("e_fourier", "(2.7)")
        + A.fig("fig_fourier", "Flux points down the gradient: from the hot side to the cold side.", "Flux menghala menuruni gradient: dari sisi panas ke sisi sejuk.", 460)
        + SB(P("Substituting (2.7) into the balance gives one equation in T alone:", "Menggantikan (2.7) ke dalam balance memberi satu persamaan dalam T sahaja:"))
        + A.eq("e_pde_t", "(2.10)")
        + H3("Steady state: the PDE we discretise", "Steady state: PDE yang kita discretise")
        + SB(P("Drop the time derivative. This is the equation you must be able to write from memory: the divergence of the flux equals the source.",
               "Gugurkan time derivative. Inilah persamaan yang anda mesti boleh tulis tanpa melihat nota: divergence bagi flux sama dengan source."))
        + A.eq("e_pde", "(2.11)")
        + SB(P("Two special cases you have met before: with constant isotropic k it is Poisson’s equation, and with no source it is Laplace’s equation — the same equation as potential flow in fluid mechanics and seepage in soil mechanics.",
               "Dua kes khas yang anda pernah temui: dengan k yang constant dan isotropic ia menjadi Poisson’s equation, dan tanpa source ia menjadi Laplace’s equation — persamaan yang sama dengan potential flow dalam mekanik bendalir dan seepage dalam mekanik tanah."))
        + A.eq("e_poisson")
        + OK("Unit check", "Semakan unit", "Each term of (2.11) is W m<sup>−3</sup>: (W m<sup>−1</sup> K<sup>−1</sup>)(K m<sup>−2</sup>). The source q<sub>h</sub> sits on the right with a minus sign because we moved it across; a positive source makes the field concave, a hill.",
             "Setiap term dalam (2.11) ialah W m<sup>−3</sup>: (W m<sup>−1</sup> K<sup>−1</sup>)(K m<sup>−2</sup>). Source q<sub>h</sub> berada di kanan dengan tanda negatif kerana kita pindahkannya; source positif menjadikan field itu concave, seperti bukit.")
        + H3("The matrix form we will reuse", "Bentuk matrix yang akan kita guna semula")
        + SB(P("Write the operator as a row of derivatives, a material matrix and a column of derivatives. This is the slide that pays off in plane stress, where the same pattern appears with a 3 × 3 [E] and a 2 × 3 operator.",
               "Tulis operator sebagai satu baris derivative, satu material matrix dan satu lajur derivative. Inilah bentuk yang membuahkan hasil dalam plane stress, apabila pola yang sama muncul dengan [E] 3 × 3 dan operator 2 × 3."))
        + A.eq("e_matrix", "(2.12)") + A.eq("e_compact", "(2.13)") + A.eq("e_defs", "(2.14)")
        + NOTE("Order matters", "Susunan penting", "{∂} is a row of operators, not numbers: it acts on whatever stands to its right. You cannot commute it past a function.",
               "{∂} ialah satu baris operator, bukan nombor: ia bertindak ke atas apa sahaja di sebelah kanannya. Anda tidak boleh menukar susunannya melepasi sesuatu fungsi.")
        + STEP("Worked step · the y-direction balance (Activity 2)", "Langkah bekerja · balance arah y (Aktiviti 2)",
               P("In through y = 0: q<sub>y</sub> dx. Out through y = dy: (q<sub>y</sub> + ∂q<sub>y</sub>/∂y dy) dx. Net inflow Q<sub>y</sub> = −∂q<sub>y</sub>/∂y dx dy, equation (2.3). "
                 "Add Q<sub>x</sub>, Q<sub>y</sub> and Q<sub>h</sub>, set the sum equal to the stored-energy rate Q<sub>E</sub>, cancel dx dy, and (2.6) follows.",
                 "Masuk melalui y = 0: q<sub>y</sub> dx. Keluar melalui y = dy: (q<sub>y</sub> + ∂q<sub>y</sub>/∂y dy) dx. Net inflow Q<sub>y</sub> = −∂q<sub>y</sub>/∂y dx dy, persamaan (2.3). "
                 "Tambah Q<sub>x</sub>, Q<sub>y</sub> dan Q<sub>h</sub>, samakan hasil tambahnya dengan kadar tenaga tersimpan Q<sub>E</sub>, batalkan dx dy, dan (2.6) terhasil."))
        + KP([("Energy balance on dx × dy, then Fourier’s law, gives (2.11): divergence of flux = source.", "Energy balance pada dx × dy, kemudian Fourier’s law, memberi (2.11): divergence flux = source."),
              ("Every term of (2.11) is W m<sup>−3</sup>.", "Setiap term dalam (2.11) ialah W m<sup>−3</sup>."),
              ("Matrix form {∂}[E]{∂}ᵀT = −q<sub>h</sub>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>).", "Bentuk matrix {∂}[E]{∂}ᵀT = −q<sub>h</sub>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>).")])
        + QC("q2", "What are the units of the heat-generation term q<sub>h</sub> in (2.11)?", "Apakah unit bagi term heat generation q<sub>h</sub> dalam (2.11)?",
             [("a", "W m<sup>−2</sup>", "W m<sup>−2</sup>"), ("b", "W m<sup>−3</sup>", "W m<sup>−3</sup>"), ("c", "W m<sup>−1</sup> K<sup>−1</sup>", "W m<sup>−1</sup> K<sup>−1</sup>")],
             "b", "q<sub>h</sub> is heat generated per unit volume, W m<sup>−3</sup>, the same as k ∂²T/∂x². A flux (W m<sup>−2</sup>) is per unit area; conductivity is W m<sup>−1</sup> K<sup>−1</sup>.",
             "q<sub>h</sub> ialah haba dijana per unit isi padu, W m<sup>−3</sup>, sama dengan k ∂²T/∂x². Flux (W m<sup>−2</sup>) ialah per unit luas; conductivity ialah W m<sup>−1</sup> K<sup>−1</sup>.")
    )
    S.append(("n2", "From the energy balance to the PDE", "Daripada energy balance kepada PDE", body))

    # ---- n3 --------------------------------------------------------------
    body = (
        P("A PDE alone is not a problem. On every part of the boundary we must specify either the temperature or the flux. There are only two kinds of condition, and the whole of the finite element treatment depends on telling them apart.",
          "PDE sahaja bukan satu masalah. Pada setiap bahagian sempadan kita mesti tetapkan sama ada temperature atau flux. Hanya ada dua jenis condition, dan keseluruhan rawatan finite element bergantung pada kebolehan membezakannya.")
        + '<div class="eqrow">' + A.eq("e_dirichlet", "(2.16)") + A.eq("e_neumann", "(2.15)") + '</div>'
        + DEF("Dirichlet, or essential", "Dirichlet, atau essential", "The temperature T̄ is known on the edge. FEM must <i>impose</i> it on the unknowns: the corresponding rows and columns of the assembled system are modified.",
              "Temperature T̄ diketahui pada tepi itu. FEM mesti <i>mengenakannya</i> pada unknown: baris dan lajur yang sepadan dalam assembled system diubah suai.")
        + DEF("Neumann, or natural", "Neumann, atau natural", "The boundary flux q<sub>b</sub> is known, positive inward, and enters through the outward unit normal n = (n<sub>x</sub>, n<sub>y</sub>). "
              "FEM does not impose it: it appears by itself as a load, from the integration by parts in Part 2.",
              "Boundary flux q<sub>b</sub> diketahui, positif ke dalam, dan masuk melalui outward unit normal n = (n<sub>x</sub>, n<sub>y</sub>). "
              "FEM tidak mengenakannya: ia muncul dengan sendirinya sebagai load, daripada integration by parts dalam Part 2.")
        + A.fig("fig_bc", "The outward unit normal on each edge of a rectangular domain.", "Outward unit normal pada setiap tepi rectangular domain.", 420)
        + H3("Rectangular domains", "Rectangular domain")
        + SB(P("On a rectangle the normal is one of (±1, 0) or (0, ±1), so (2.15) loses one term on every edge:", "Pada segi empat tepat, normal ialah salah satu daripada (±1, 0) atau (0, ±1), jadi (2.15) kehilangan satu term pada setiap tepi:"))
        + A.eq("e_rect_v") + A.eq("e_rect_h") + A.eq("e_insul")
        + H3("What FEM does with each kind", "Apa yang FEM buat dengan setiap jenis")
        + '<div class="tbl"><table><tr><th>' + B("Condition", "Condition") + '</th><th>' + B("What is known", "Apa yang diketahui") + '</th><th>' + B("Where it enters the FEM", "Di mana ia masuk dalam FEM") + '</th><th>' + B("Action in Part 2", "Tindakan dalam Part 2") + '</th></tr>'
        + '<tr><td>Dirichlet · essential</td><td>T̄ ' + B("on the edge", "pada tepi") + '</td><td>' + B("imposed on the assembled system by modifying rows and columns of [K]", "dikenakan pada assembled system dengan mengubah baris dan lajur [K]") + '</td><td>' + B("row–column elimination", "row–column elimination") + '</td></tr>'
        + '<tr><td>Neumann · natural</td><td>q<sub>b</sub> ' + B("on the edge", "pada tepi") + '</td><td>' + B("appears in the boundary vector {b} produced by integration by parts", "muncul dalam boundary vector {b} hasil integration by parts") + '</td><td>{b} = ∫{N}ᵀq<sub>n</sub> ds</td></tr>'
        + '<tr><td>' + B("Insulated · natural, q<sub>b</sub> = 0", "Insulated · natural, q<sub>b</sub> = 0") + '</td><td>' + B("no flux", "tiada flux") + '</td><td>' + B("contributes nothing: the boundary integral is zero", "tiada sumbangan: boundary integral sifar") + '</td><td>' + B("do nothing", "tiada tindakan") + '</td></tr></table></div>'
        + NOTE("The most common error", "Kesilapan paling lazim", "Trying to “impose” an insulated edge. It needs no action at all. The names come from the integration by parts: the natural condition is the term that falls out of it; the essential one must be enforced on the unknowns.",
               "Cuba “mengenakan” tepi insulated. Ia tidak memerlukan apa-apa tindakan. Nama-namanya datang daripada integration by parts: natural condition ialah term yang terhasil daripadanya; essential condition mesti dikuatkuasakan pada unknown.")
        + STEP("Worked example · label the plate (Activity 3, text Exercise 2.5)", "Contoh bekerja · label plat (Aktiviti 3, teks Latihan 2.5)",
               A.fig("fig_plate_ex5", "Plate 0.15 m × 0.05 m, k = 450 W m<sup>−1</sup> K<sup>−1</sup>, q<sub>h</sub> = 1 × 10<sup>7</sup> W m<sup>−3</sup>, unit thickness.",
                     "Plat 0.15 m × 0.05 m, k = 450 W m<sup>−1</sup> K<sup>−1</sup>, q<sub>h</sub> = 1 × 10<sup>7</sup> W m<sup>−3</sup>, ketebalan unit.", 440)
               + '<div class="tbl"><table><tr><th>' + B("Edge", "Tepi") + '</th><th>' + B("Type", "Jenis") + '</th><th>' + B("Equation", "Persamaan") + '</th><th>' + B("FEM action", "Tindakan FEM") + '</th></tr>'
               + '<tr><td>' + B("top", "atas") + '</td><td>Dirichlet</td><td>T = 300 K</td><td>' + B("impose on the system", "kenakan pada sistem") + '</td></tr>'
               + '<tr><td>' + B("left", "kiri") + '</td><td>Dirichlet</td><td>T = 400 K</td><td>' + B("impose on the system", "kenakan pada sistem") + '</td></tr>'
               + '<tr><td>' + B("right", "kanan") + '</td><td>Neumann</td><td>n = (1, 0): k ∂T/∂x = q<sub>b</sub> = +1 × 10<sup>6</sup> W m<sup>−2</sup></td><td>' + B("load in {b}", "load dalam {b}") + '</td></tr>'
               + '<tr><td>' + B("bottom", "bawah") + '</td><td>Neumann, q<sub>b</sub> = 0</td><td>∂T/∂y = 0</td><td>' + B("nothing", "tiada") + '</td></tr></table></div>'
               + P("Well-posed: every edge has a condition and T is fixed on two edges, so the temperature level is pinned. The inward flux on the right edge is positive q<sub>b</sub>; the flux-vector component q<sub>x</sub> there points along −n and is negative, q<sub>x</sub> = −10<sup>6</sup> W m<sup>−2</sup>.",
                   "Well-posed: setiap tepi ada condition dan T ditetapkan pada dua tepi, jadi paras temperature terikat. Flux ke dalam pada tepi kanan ialah q<sub>b</sub> positif; komponen flux-vector q<sub>x</sub> di situ menghala sepanjang −n dan negatif, q<sub>x</sub> = −10<sup>6</sup> W m<sup>−2</sup>."))
        + KP([("Dirichlet = essential = imposed. Neumann = natural = appears from the integration by parts. Insulated = do nothing.", "Dirichlet = essential = dikenakan. Neumann = natural = muncul daripada integration by parts. Insulated = tiada tindakan."),
              ("q<sub>b</sub> is positive inward; on a rectangle only one derivative survives per edge.", "q<sub>b</sub> positif ke dalam; pada segi empat tepat hanya satu derivative kekal pada setiap tepi."),
              ("A problem is well-posed when every edge has a condition and T is pinned somewhere.", "Masalah itu well-posed apabila setiap tepi ada condition dan T terikat di suatu tempat.")])
        + QC("q3", "An edge of the plate is insulated. In the finite element model, what must you do about it?", "Satu tepi plat adalah insulated. Dalam model finite element, apa yang anda perlu buat?",
             [("a", "Impose ∂T/∂y = 0 on the nodes of that edge", "Kenakan ∂T/∂y = 0 pada node tepi itu"), ("b", "Nothing: its boundary integral is zero", "Tiada apa-apa: boundary integral-nya sifar"), ("c", "Set T = 0 on those nodes", "Tetapkan T = 0 pada node itu")],
             "b", "An insulated edge is a natural condition with q<sub>b</sub> = 0, so the boundary term {b} it would produce is zero. No action is needed.",
             "Tepi insulated ialah natural condition dengan q<sub>b</sub> = 0, jadi boundary term {b} yang bakal dihasilkannya ialah sifar. Tiada tindakan diperlukan.")
    )
    S.append(("n3", "Boundary conditions: essential and natural", "Boundary condition: essential dan natural", body))

    # ---- n4 --------------------------------------------------------------
    body = (
        P("The four-node rectangular element has one degree of freedom at each corner, the temperature T̂<sub>i</sub>, numbered anticlockwise from the bottom-left corner. "
          "We need a rule for T at any point inside the element in terms of these four numbers. The rule is a polynomial with four coefficients.",
          "Four-node rectangular element mempunyai satu degree of freedom pada setiap bucu, iaitu temperature T̂<sub>i</sub>, dinomborkan lawan jam dari bucu kiri bawah. "
          "Kita perlukan satu peraturan bagi T pada mana-mana titik di dalam element dalam sebutan empat nombor ini. Peraturannya ialah satu polynomial dengan empat coefficient.")
        + A.fig("fig_q4", "The element a × b, nodes 1 to 4 anticlockwise from the origin (text Fig. 2.2).", "Element a × b, node 1 hingga 4 lawan jam dari origin (teks Rajah 2.2).", 400)
        + STEP("Step 1 · assume a polynomial (2.17)", "Langkah 1 · andaikan satu polynomial (2.17)",
               A.eq("e_poly", "(2.17)") + SB(P("Four unknowns need four coefficients. The xy term, rather than x² or y², keeps the function linear along every edge, which is what makes neighbouring elements agree.",
                                                "Empat unknown memerlukan empat coefficient. Term xy, bukannya x² atau y², mengekalkan fungsi itu linear di sepanjang setiap tepi, dan itulah yang membuat element berjiran bersetuju.")))
        + STEP("Step 2 · evaluate at the nodes (2.18)", "Langkah 2 · nilaikan pada node (2.18)",
               A.eq("e_nodes", "(2.18)") + A.eq("e_nodes_matrix"))
        + STEP("Step 3 · solve for the coefficients (2.19)", "Langkah 3 · selesaikan coefficient (2.19)",
               A.eq("e_coeffs", "(2.19)") + SB(P("Check: if all four nodal values are equal to T<sub>0</sub>, then a<sub>1</sub> = T<sub>0</sub> and a<sub>2</sub> = a<sub>3</sub> = a<sub>4</sub> = 0, so T = T<sub>0</sub> everywhere. A uniform field is reproduced exactly.",
                                                   "Semak: jika keempat-empat nilai node sama dengan T<sub>0</sub>, maka a<sub>1</sub> = T<sub>0</sub> dan a<sub>2</sub> = a<sub>3</sub> = a<sub>4</sub> = 0, jadi T = T<sub>0</sub> di mana-mana. Field yang seragam dihasilkan semula dengan tepat.")))
        + STEP("Step 4 · collect by nodal value (2.20)–(2.22)", "Langkah 4 · kumpulkan mengikut nilai node (2.20)–(2.22)",
               A.eq("e_collect", "(2.20)") + A.eq("e_shape", "(2.21)") + A.eq("e_T_N", "(2.22)")
               + SB(P("Each nodal value is multiplied by its own function of position: its <b>shape function</b> N<sub>i</sub>(x, y). The row {N} and the column {T̂}ᵀ are the two objects the rest of the course is built from.",
                      "Setiap nilai node didarab dengan fungsi kedudukannya sendiri: <b>shape function</b> N<sub>i</sub>(x, y). Baris {N} dan lajur {T̂}ᵀ ialah dua objek yang menjadi asas keseluruhan kursus ini.")))
        + H3("What a shape function looks like", "Rupa sebuah shape function")
        + '<figure><div class="figrow"><img src="slides/img/fig_shape_tent.png" style="flex:0 1 300px" alt="Shape function N3 drawn as a surface over the element: a tent that rises to 1 at node 3 and is zero at the other three nodes" class="figimg">'
        + '<img src="slides/img/fig_shape_maps.png" alt="Colour maps of N1 to N4 over the element, each equal to 1 at its own node and 0 at the others" class="figimg" style="flex:1 1 340px"></div>'
        + '<figcaption>' + B("N<sub>3</sub> as a surface (left) and N<sub>1</sub>…N<sub>4</sub> as colour maps (right): each is 1 at its own node, 0 at the other three, and curved inside because of the xy term.",
                              "N<sub>3</sub> sebagai permukaan (kiri) dan N<sub>1</sub>…N<sub>4</sub> sebagai peta warna (kanan): setiap satu bernilai 1 pada node sendiri, 0 pada tiga node lain, dan melengkung di dalam kerana term xy.") + '</figcaption></figure>'
        + '<figure><img src="slides/img/w9_shapeN.png" alt="The four shape functions of a quadrilateral element plotted by PyMAPDL" class="figimg" style="width:min(520px,100%)">'
        + '<figcaption>' + B("The same four functions inside commercial code.", "Empat fungsi yang sama di dalam perisian komersial.") + '<span class="credit"> Image: PyMAPDL documentation, “Build a finite element model”, © ANSYS, Inc., MIT licence.</span></figcaption></figure>'
        + H3("Three properties you can check in 30 seconds", "Tiga sifat yang boleh disemak dalam 30 saat")
        + A.eq("e_kron") + SB(P("<b>Kronecker delta.</b> So T at node j equals T̂<sub>j</sub>: the nodal unknowns really are nodal temperatures. Check N<sub>2</sub> at node 3: N<sub>2</sub>(a, b) = a(b − b)/(ab) = 0.",
                                "<b>Kronecker delta.</b> Jadi T pada node j sama dengan T̂<sub>j</sub>: nodal unknown memang temperature pada node. Semak N<sub>2</sub> pada node 3: N<sub>2</sub>(a, b) = a(b − b)/(ab) = 0."))
        + A.eq("e_pou") + SB(P("<b>Partition of unity.</b> A uniform temperature is reproduced exactly, the test we did on the coefficients.",
                               "<b>Partition of unity.</b> Temperature yang seragam dihasilkan semula dengan tepat, ujian yang kita buat pada coefficient tadi."))
        + A.eq("e_edge") + SB(P("<b>Linear along each edge.</b> On y = 0 only nodes 1 and 2 matter, and T varies linearly between them. The neighbouring element shares those two nodes and the same straight line, so T is continuous across element boundaries (C<sup>0</sup>).",
                                "<b>Linear di sepanjang setiap tepi.</b> Pada y = 0 hanya node 1 dan 2 yang penting, dan T berubah secara linear antara keduanya. Element berjiran berkongsi dua node itu dan garis lurus yang sama, jadi T adalah continuous merentasi sempadan element (C<sup>0</sup>)."))
        + H3("From one element to the mesh", "Daripada satu element kepada mesh")
        + '<figure><div class="figrow"><img src="slides/img/w9_hat1d.png" style="flex:1 1 300px" alt="Two overlapping one-dimensional hat functions on a mesh of five elements" class="figimg">'
        + '<img src="slides/img/w9_tent2d.png" alt="A two-dimensional tent function rising to one at an interior node of a triangular mesh" class="figimg" style="flex:0 1 300px"></div>'
        + '<figcaption>' + B("One nodal value lifts one tent. In 1D the basis function of node i is a hat over the two elements that share it; in 2D it is a tent over every element around the node. That is why node i couples only to its neighbours and the global matrix is sparse (Part 2).",
                              "Satu nilai node mengangkat satu khemah. Dalam 1D, basis function bagi node i ialah topi (hat) merentasi dua element yang berkongsinya; dalam 2D ia khemah merentasi setiap element di sekeliling node. Sebab itulah node i hanya berkait dengan jirannya dan global matrix itu sparse (Part 2).")
        + '<span class="credit"> Images: Langtangen and Mardal, <i>Introduction to Numerical Methods for Variational Problems</i> (Springer, 2019), github.com/hplgit/fem-book, MIT licence.</span></figcaption></figure>'
        + STEP("Worked example · evaluate and interpolate (Activity 4)", "Contoh bekerja · nilaikan dan interpolate (Aktiviti 4)",
               P("a = 2 m, b = 1 m, point (x, y) = (1.5, 0.3) m, nodal temperatures T̂ = {100, 140, 160, 120} K.", "a = 2 m, b = 1 m, titik (x, y) = (1.5, 0.3) m, nodal temperature T̂ = {100, 140, 160, 120} K.")
               + A.fig("fig_q4_point", "The point (1.5, 0.3) in the 2 m × 1 m element.", "Titik (1.5, 0.3) dalam element 2 m × 1 m.", 380)
               + A.eq("e_act4_N") + A.eq("e_act4_sum") + A.eq("e_act4_T")
               + P("Node 2 carries half the weight because the point is nearest to it. The sum of the four weights is 1, as it must be.",
                   "Node 2 membawa separuh daripada weight kerana titik itu paling hampir dengannya. Hasil tambah empat weight ialah 1, sebagaimana sepatutnya."))
        + TRY("node3 diag")
        + KP([("T = {N}{T̂}ᵀ with the bilinear N<sub>i</sub> of (2.21).", "T = {N}{T̂}ᵀ dengan N<sub>i</sub> bilinear daripada (2.21)."),
              ("Kronecker delta, partition of unity, linear edges: three checks that catch most errors.", "Kronecker delta, partition of unity, tepi linear: tiga semakan yang menangkap kebanyakan kesilapan."),
              ("At (1.5, 0.3): N = 0.175, 0.525, 0.225, 0.075 and T = 136.0 K.", "Pada (1.5, 0.3): N = 0.175, 0.525, 0.225, 0.075 dan T = 136.0 K.")])
        + QC("q4", "At the centre of the element (a/2, b/2), what is the value of each shape function?", "Pada pusat element (a/2, b/2), apakah nilai setiap shape function?",
             [("a", "1", "1"), ("b", "1/2", "1/2"), ("c", "1/4", "1/4")],
             "c", "N<sub>i</sub>(a/2, b/2) = (a/2)(b/2)/(ab) = 1/4 for every i, and the four values sum to 1.",
             "N<sub>i</sub>(a/2, b/2) = (a/2)(b/2)/(ab) = 1/4 bagi setiap i, dan empat nilai itu berjumlah 1.")
    )
    S.append(("n4", "The four-node element and its shape functions", "Four-node element dan shape function-nya", body))

    # ---- n5 --------------------------------------------------------------
    body = (
        P("Differentiate the approximation T = {N}{T̂}ᵀ and the derivatives land on the shape functions, because the nodal values are constants. The gradient at any point is a 2 × 4 matrix of shape-function derivatives times the nodal vector:",
          "Bezakan approximation T = {N}{T̂}ᵀ dan derivative itu jatuh pada shape function, kerana nilai node ialah pemalar. Gradient pada mana-mana titik ialah matrix 2 × 4 bagi derivative shape function didarab dengan nodal vector:")
        + A.eq("e_grad", "(2.33)") + A.eq("e_dN")
        + SB(P("Read the matrix: ∂N<sub>i</sub>/∂x depends on y only and ∂N<sub>i</sub>/∂y on x only. Across an element edge the gradient, and therefore the flux, generally jumps — the approximation is continuous but its derivative is not.",
               "Baca matrix itu: ∂N<sub>i</sub>/∂x bergantung pada y sahaja dan ∂N<sub>i</sub>/∂y pada x sahaja. Merentasi tepi element, gradient dan seterusnya flux biasanya melompat — approximation itu continuous tetapi derivative-nya tidak."))
        + H3("From gradient to flux", "Daripada gradient kepada flux")
        + A.eq("e_flux_vec")
        + SB(P("Fourier’s law in matrix form: flux = −[E] × gradient. The same 2 × 4 matrix {∂}ᵀ{N} will be used twice: for the flux now, and for the conductance matrix in Part 2:",
               "Fourier’s law dalam bentuk matrix: flux = −[E] × gradient. Matrix 2 × 4 yang sama, {∂}ᵀ{N}, akan digunakan dua kali: untuk flux sekarang, dan untuk conductance matrix dalam Part 2:"))
        + A.eq("e_k_preview")
        + STEP("Worked example · gradient and flux at (1.5, 0.3) (Activity 5)", "Contoh bekerja · gradient dan flux pada (1.5, 0.3) (Aktiviti 5)",
               P("Same element and data as Activity 4, with k<sub>x</sub> = k<sub>y</sub> = 2 W m<sup>−1</sup> K<sup>−1</sup>.", "Element dan data yang sama dengan Aktiviti 4, dengan k<sub>x</sub> = k<sub>y</sub> = 2 W m<sup>−1</sup> K<sup>−1</sup>.")
               + A.eq("e_act5_dN") + A.eq("e_act5_grad") + A.eq("e_act5_q") + A.eq("e_act5_qy")
               + P("Both components of the flux are negative: heat flows towards decreasing x and y, away from the hottest node 3 at (a, b).",
                   "Kedua-dua komponen flux negatif: haba mengalir ke arah x dan y yang menyusut, menjauhi node 3 yang paling panas di (a, b)."))
        + H3("The eight-node element in one paragraph", "Eight-node element dalam satu perenggan")
        + A.fig("fig_q8", "Four corner nodes and four mid-side nodes (text Fig. 2.3).", "Empat node bucu dan empat node tengah sisi (teks Rajah 2.3).", 400)
        + SB(P("Add a node at the middle of each edge and the polynomial gains four terms, (2.31). The shape functions are quadratic along each edge, so they follow a curved temperature profile with fewer elements. "
               "The procedure is identical: evaluate at the eight nodes, invert, collect by nodal value. A corner function now dips below zero between its two mid-side neighbours, and the eight functions still sum to one.",
               "Tambah satu node di tengah setiap tepi dan polynomial itu mendapat empat term lagi, (2.31). Shape function-nya quadratic di sepanjang setiap tepi, jadi ia mengikut profil temperature yang melengkung dengan element yang lebih sedikit. "
               "Prosedurnya serupa: nilaikan pada lapan node, inverse, kumpulkan mengikut nilai node. Fungsi bucu kini jatuh di bawah sifar antara dua jiran tengah sisinya, dan lapan fungsi itu tetap berjumlah satu."))
        + A.eq("e_poly8", "(2.31)") + A.eq("e_N8")
        + TRY("act4 q8n1")
        + KP([("Gradient = {∂}ᵀ{N}{T̂}ᵀ, a 2 × 4 matrix times the nodal vector; flux = −[E] × gradient.", "Gradient = {∂}ᵀ{N}{T̂}ᵀ, matrix 2 × 4 didarab nodal vector; flux = −[E] × gradient."),
              ("At (1.5, 0.3) with k = 2: ∂T/∂x = ∂T/∂y = 20 K m<sup>−1</sup>, q<sub>x</sub> = q<sub>y</sub> = −40 W m<sup>−2</sup>.", "Pada (1.5, 0.3) dengan k = 2: ∂T/∂x = ∂T/∂y = 20 K m<sup>−1</sup>, q<sub>x</sub> = q<sub>y</sub> = −40 W m<sup>−2</sup>."),
              ("The eight-node element is the same procedure with quadratic edges.", "Eight-node element ialah prosedur yang sama dengan tepi quadratic.")])
        + QC("q5", "At a point the temperature increases in the +x direction. The flux component q<sub>x</sub> there is", "Pada satu titik, temperature meningkat dalam arah +x. Komponen flux q<sub>x</sub> di situ ialah",
             [("a", "positive", "positif"), ("b", "negative", "negatif"), ("c", "zero", "sifar")],
             "b", "q<sub>x</sub> = −k ∂T/∂x. A positive gradient gives a negative flux: heat flows from hot to cold, towards −x.",
             "q<sub>x</sub> = −k ∂T/∂x. Gradient positif memberi flux negatif: haba mengalir dari panas ke sejuk, ke arah −x.")
    )
    S.append(("n5", "Gradient and flux inside an element", "Gradient dan flux di dalam element", body))

    # ---- n6 --------------------------------------------------------------
    code = ["% Local conductance matrix (text §2.3.1)", "a = L/Nx; b = H/Ny;", "s1 = b*kx/(3*a) + a*ky/(3*b);", "s2 = -b*kx/(3*a) + a*ky/(6*b);",
            "s3 = -b*kx/(6*a) - a*ky/(6*b);", "s4 = b*kx/(6*a) - a*ky/(3*b);", "k = [s1 s2 s3 s4; s2 s1 s4 s3; s3 s4 s1 s2; s4 s3 s2 s1];",
            "fQ = a*b*Q/4*[1; 1; 1; 1];        % heat generation", "% Assembly by connectivity, element 1 = nodes [1 2 5 4]",
            "e1 = [1 2 5 4];  K(e1,e1) = K(e1,e1) + k;  F(e1) = F(e1) + fQ;", "% Essential conditions: rows and columns of known nodes removed",
            "free = setdiff(1:n, fixed);  T = zeros(n,1);  T(fixed) = Tbar;", "T(free) = K(free,free) \\ (F(free) - K(free,fixed)*T(fixed));"]
    steps = [("Governing PDE and boundary conditions", "PDE pentadbir dan boundary condition"), ("Element and shape functions", "Element dan shape function"),
             ("Galerkin weighted residual", "Galerkin weighted residual"), ("Integration by parts", "Integration by parts"),
             ("Element matrices [k], {q}, {b}", "Matrix element [k], {q}, {b}"), ("Assembly, then impose T̄", "Assembly, kemudian kenakan T̄"), ("Solve and post-process", "Selesaikan dan post-process")]
    body = (
        P("The method is a pipeline of seven steps. This part covered the first two; Part 2 does the other five on the text’s worked example and runs the MATLAB script.",
          "Kaedah ini ialah satu pipeline tujuh langkah. Bahagian ini merangkumi dua langkah pertama; Part 2 membuat lima lagi pada contoh bekerja dalam teks dan menjalankan skrip MATLAB.")
        + '<ol class="lo">' + "".join(f'<li>{B(e, m)}' + (' <span class="muted">· ' + B("this part", "bahagian ini") + '</span>' if i < 2 else "") + '</li>' for i, (e, m) in enumerate(steps)) + '</ol>'
        + H3("Part 2’s worked example (text §2.3)", "Contoh bekerja Part 2 (teks §2.3)")
        + A.fig("fig_plate_book", "A 1 m square plate with heat generation, two cold edges and two insulated edges, meshed with four elements.",
                "Plat segi empat sama 1 m dengan heat generation, dua tepi sejuk dan dua tepi insulated, di-mesh dengan empat element.", 300)
        + SB(P("Square plate 1 m × 1 m, q<sub>h</sub> = 600 W m<sup>−3</sup>, k<sub>x</sub> = k<sub>y</sub> = 300 W m<sup>−1</sup> K<sup>−1</sup>; top and left edges at 0 °C, right and bottom edges insulated. "
               "Four 4-node elements by hand, then 64 elements in MATLAB, then software.",
               "Plat segi empat sama 1 m × 1 m, q<sub>h</sub> = 600 W m<sup>−3</sup>, k<sub>x</sub> = k<sub>y</sub> = 300 W m<sup>−1</sup> K<sup>−1</sup>; tepi atas dan kiri pada 0 °C, tepi kanan dan bawah insulated. "
               "Empat 4-node element secara tangan, kemudian 64 element dalam MATLAB, kemudian perisian."))
        + NOTE("Before Part 2", "Sebelum Part 2", "Classify its four edges as in §3 and predict where the hottest point is. Write the prediction down; Part 2 checks it.",
               "Kelaskan empat tepinya seperti dalam §3 dan ramalkan di mana titik paling panas. Tulis ramalan itu; Part 2 menyemaknya.")
        + H3("The MATLAB skeleton follows the pipeline", "Rangka MATLAB mengikut pipeline")
        + '<pre class="paper" style="font:13px/1.5 var(--font-num);overflow-x:auto;white-space:pre">' + "\n".join(code) + '</pre>'
        + SB(LI([("Lines 2–8: step 5, the element matrix and load from closed-form integrals (s<sub>1</sub>…s<sub>4</sub> are derived in Part 2).", "Baris 2–8: langkah 5, matrix element dan load daripada closed-form integral (s<sub>1</sub>…s<sub>4</sub> diterbitkan dalam Part 2)."),
                 ("Line 10: step 6, assembly — the connectivity list [1 2 5 4] is the element’s global node numbers.", "Baris 10: langkah 6, assembly — senarai connectivity [1 2 5 4] ialah nombor node global bagi element itu."),
                 ("Lines 12–13: step 6, essential conditions by removing the rows and columns of the known nodes; step 7, solve with the backslash operator.", "Baris 12–13: langkah 6, essential condition dengan membuang baris dan lajur node yang diketahui; langkah 7, selesaikan dengan operator backslash.")]))
        + H3("To prepare", "Persediaan")
        + LI([("Read text §2.2.2 and §2.3 (the worked example), about 12 pages.", "Baca teks §2.2.2 dan §2.3 (contoh bekerja), kira-kira 12 muka surat."),
              ("Redo Activities 4 and 5 for the point (0.5, 0.8) m — or use the exercises tab, which gives you new numbers each time.", "Ulang Aktiviti 4 dan 5 untuk titik (0.5, 0.8) m — atau guna tab Latihan, yang memberi nombor baharu setiap kali."),
              ("Classify the edges of the §2.3 plate and predict the hottest point.", "Kelaskan tepi plat §2.3 dan ramalkan titik paling panas."),
              ("Bring MATLAB to the next session.", "Bawa MATLAB ke sesi seterusnya.")])
        + KP([("Seven steps: PDE + BCs, element, Galerkin, integration by parts, element matrices, assembly + impose, solve.", "Tujuh langkah: PDE + BC, element, Galerkin, integration by parts, matrix element, assembly + kenakan, selesaikan."),
              ("Part 2: steps 3–7 on the 1 m plate, by hand with four elements and in MATLAB with 64.", "Part 2: langkah 3–7 pada plat 1 m, secara tangan dengan empat element dan dalam MATLAB dengan 64.")])
        + QC("q6", "For the §2.3 plate (cold top and left edges, insulated right and bottom edges, uniform heat generation), where is the hottest point?", "Bagi plat §2.3 (tepi atas dan kiri sejuk, tepi kanan dan bawah insulated, heat generation seragam), di manakah titik paling panas?",
             [("a", "The centre of the plate", "Pusat plat"), ("b", "The bottom-right corner", "Bucu kanan bawah"), ("c", "The top-left corner", "Bucu kiri atas")],
             "b", "Heat can only leave through the two cold edges. The point farthest from both, where the two insulated edges meet, is the bottom-right corner.",
             "Haba hanya boleh keluar melalui dua tepi sejuk. Titik yang paling jauh daripada kedua-duanya, tempat dua tepi insulated bertemu, ialah bucu kanan bawah.")
    )
    S.append(("n6", "The pipeline: seven steps from PDE to answer", "Pipeline: tujuh langkah daripada PDE kepada jawapan", body))
    return S


# ---- recall questions on the Start tab (from the first half of the course) ----
RECALL = [
    QC("r1", "Recall · for the two-node bar element, the shape function N<sub>1</sub>(x) is", "Ingat semula · bagi two-node bar element, shape function N<sub>1</sub>(x) ialah",
       [("a", "1 at node 1, 0 at node 2, linear in between", "1 pada node 1, 0 pada node 2, linear di antaranya"), ("b", "1 everywhere in the element", "1 di mana-mana dalam element"), ("c", "quadratic in x", "quadratic dalam x")],
       "a", "N<sub>1</sub> = 1 − x/L: it is 1 at its own node and 0 at the other, and the displacement between the nodes is linear. The 2D element repeats this idea with four functions.",
       "N<sub>1</sub> = 1 − x/L: bernilai 1 pada node sendiri dan 0 pada node lain, dan displacement antara node adalah linear. Element 2D mengulang idea ini dengan empat fungsi."),
    QC("r2", "Recall · a fixed displacement at a support of a truss is, in the language of this part,", "Ingat semula · displacement tetap pada penyokong truss ialah, dalam bahasa bahagian ini,",
       [("a", "a natural condition", "satu natural condition"), ("b", "an essential condition", "satu essential condition"), ("c", "a load", "satu load")],
       "b", "A known value of the unknown field (displacement, or here temperature) is an essential condition, imposed on the system. A known force or flux is natural.",
       "Nilai yang diketahui bagi field yang tidak diketahui (displacement, atau di sini temperature) ialah essential condition, dikenakan pada sistem. Daya atau flux yang diketahui ialah natural."),
]


# ---- exercises: markup for the choice items, JS for the parameterised ones ----
def MCQ(qid, q_en, q_ms, options, ans, fb_en, fb_ms, marks=1):
    opts = "".join(f'<button class="opt" type="button" data-k="{k}">{B(e, m)}</button>' for k, e, m in options)
    conf = ('<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span>'
            '<button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>')
    return (f'<div class="q" data-q="{qid}" data-ans="{ans}" id="{qid}"><p><span class="qmeta">{qid.upper()} · {marks} ' + B("mark", "markah") + f'</span><br>{B(q_en, q_ms)}</p>{conf}'
            f'<div class="opts">{opts}</div><p class="fb" hidden><span class="meta"></span> {B(fb_en, fb_ms)}</p></div>')


QUICK = [
    MCQ("a1", "In the steady conduction equation (2.11), which combination has the units of q<sub>h</sub>?", "Dalam persamaan steady conduction (2.11), gabungan manakah yang mempunyai unit q<sub>h</sub>?",
        [("a", "k × ∂T/∂x", "k × ∂T/∂x"), ("b", "k × ∂²T/∂x²", "k × ∂²T/∂x²"), ("c", "ρC × T", "ρC × T")], "b",
        "k ∂²T/∂x² has units (W m<sup>−1</sup> K<sup>−1</sup>)(K m<sup>−2</sup>) = W m<sup>−3</sup>, the same as q<sub>h</sub>. The option k ∂T/∂x is a flux, W m<sup>−2</sup>.",
        "k ∂²T/∂x² berunit (W m<sup>−1</sup> K<sup>−1</sup>)(K m<sup>−2</sup>) = W m<sup>−3</sup>, sama dengan q<sub>h</sub>. Pilihan k ∂T/∂x ialah flux, W m<sup>−2</sup>."),
    MCQ("a2", "Which boundary condition must be <i>imposed</i> on the assembled equations rather than appearing by itself?", "Boundary condition manakah yang mesti <i>dikenakan</i> pada assembled equation dan bukannya muncul dengan sendiri?",
        [("a", "A known temperature on an edge", "Temperature yang diketahui pada satu tepi"), ("b", "A known inward flux on an edge", "Flux ke dalam yang diketahui pada satu tepi"), ("c", "An insulated edge", "Satu tepi insulated")], "a",
        "A known temperature is an essential (Dirichlet) condition: it constrains the unknowns themselves. A known flux, including zero flux, is natural and comes out of the integration by parts.",
        "Temperature yang diketahui ialah essential (Dirichlet) condition: ia mengekang unknown itu sendiri. Flux yang diketahui, termasuk flux sifar, adalah natural dan terhasil daripada integration by parts."),
    MCQ("a3", "On the right edge of a plate, n = (1, 0), an inward flux q<sub>b</sub> = +500 W m<sup>−2</sup> is applied. The flux-vector component q<sub>x</sub> at that edge is", "Pada tepi kanan plat, n = (1, 0), flux ke dalam q<sub>b</sub> = +500 W m<sup>−2</sup> dikenakan. Komponen flux-vector q<sub>x</sub> pada tepi itu ialah",
        [("a", "+500 W m<sup>−2</sup>", "+500 W m<sup>−2</sup>"), ("b", "−500 W m<sup>−2</sup>", "−500 W m<sup>−2</sup>"), ("c", "0, because the edge is a boundary", "0, kerana tepi itu sempadan")], "b",
        "q<sub>b</sub> is positive inward. On the right edge, inward means towards −x, so q<sub>x</sub> = −q<sub>b</sub> = −500 W m<sup>−2</sup>. Equivalently (2.15): k ∂T/∂x · n<sub>x</sub> = q<sub>b</sub>, so k ∂T/∂x = +500 and q<sub>x</sub> = −k ∂T/∂x = −500.",
        "q<sub>b</sub> positif ke dalam. Pada tepi kanan, ke dalam bermaksud ke arah −x, jadi q<sub>x</sub> = −q<sub>b</sub> = −500 W m<sup>−2</sup>. Setara dengan (2.15): k ∂T/∂x · n<sub>x</sub> = q<sub>b</sub>, jadi k ∂T/∂x = +500 dan q<sub>x</sub> = −k ∂T/∂x = −500."),
    MCQ("a4", "Why is the fourth term of the polynomial (2.17) chosen as xy rather than x²?", "Mengapa term keempat polynomial (2.17) dipilih sebagai xy dan bukannya x²?",
        [("a", "So that T is linear along every edge and neighbouring elements agree", "Supaya T linear di sepanjang setiap tepi dan element berjiran bersetuju"), ("b", "Because x² cannot be integrated", "Kerana x² tidak boleh di-integrate"), ("c", "Because the element is square", "Kerana element itu segi empat sama")], "a",
        "With xy, setting y = 0 (or x = 0, or y = b, or x = a) leaves a function that is linear in the remaining coordinate, fixed by the two nodes of that edge. Two elements sharing the edge share those nodes, so T is continuous. An x² term would make T along an edge depend on more than its two nodes.",
        "Dengan xy, menetapkan y = 0 (atau x = 0, y = b, x = a) meninggalkan fungsi yang linear dalam koordinat yang tinggal, ditentukan oleh dua node tepi itu. Dua element yang berkongsi tepi berkongsi node itu, jadi T continuous. Term x² akan menjadikan T sepanjang tepi bergantung pada lebih daripada dua node."),
    MCQ("a5", "The four nodal temperatures of an element are all 250 K. At a point inside the element, T is", "Keempat-empat nodal temperature sebuah element ialah 250 K. Pada satu titik di dalam element, T ialah",
        [("a", "exactly 250 K", "tepat 250 K"), ("b", "between 0 and 250 K, depending on position", "antara 0 dan 250 K, bergantung pada kedudukan"), ("c", "250 K only at the centre", "250 K hanya di pusat")], "a",
        "Partition of unity: Σ N<sub>i</sub> = 1 everywhere, so T = 250 × Σ N<sub>i</sub> = 250 K at every point. A uniform field is reproduced exactly.",
        "Partition of unity: Σ N<sub>i</sub> = 1 di mana-mana, jadi T = 250 × Σ N<sub>i</sub> = 250 K pada setiap titik. Field yang seragam dihasilkan semula dengan tepat."),
    MCQ("a6", "Inside a four-node element, ∂T/∂x of the interpolated field", "Di dalam four-node element, ∂T/∂x bagi field yang di-interpolate",
        [("a", "is the same at every point of the element", "adalah sama pada setiap titik dalam element"), ("b", "varies with y but not with x", "berubah dengan y tetapi tidak dengan x"), ("c", "varies with x but not with y", "berubah dengan x tetapi tidak dengan y")], "b",
        "From (2.17), ∂T/∂x = a<sub>2</sub> + a<sub>4</sub> y: it depends on y only. Equivalently, every ∂N<sub>i</sub>/∂x in the 2 × 4 matrix contains (b − y) or y.",
        "Daripada (2.17), ∂T/∂x = a<sub>2</sub> + a<sub>4</sub> y: ia bergantung pada y sahaja. Setara, setiap ∂N<sub>i</sub>/∂x dalam matrix 2 × 4 mengandungi (b − y) atau y."),
]

# error spotting: one wrong line
ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="4" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("A student evaluates the shape functions at (x, y) = (0.5, 0.8) m in a 2 m × 1 m element and interpolates T from T̂ = {100, 140, 160, 120} K. One line contains the slip. Which one?",
        "Seorang pelajar menilai shape function pada (x, y) = (0.5, 0.8) m dalam element 2 m × 1 m dan interpolate T daripada T̂ = {100, 140, 160, 120} K. Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>N<sub>1</sub> = (a − x)(b − y)/(ab) = (1.5)(0.2)/2 = 0.15</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>N<sub>2</sub> = x(b − y)/(ab) = (0.5)(0.2)/2 = 0.05</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>N<sub>3</sub> = xy/(ab) = (0.5)(0.8)/2 = 0.20</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>N<sub>4</sub> = x(a − y)/(ab) = (0.5)(1.2)/2 = 0.30</span></button>'
    + '<button type="button" data-k="5"><span class="ln">5</span><span>T = 0.15(100) + 0.05(140) + 0.20(160) + 0.30(120) = 90.0 K</span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 4: N<sub>4</sub> = y(a − x)/(ab) = (0.8)(1.5)/2 = 0.60, not x(a − y)/(ab). The check that should have caught it: the four values must sum to 1, and 0.15 + 0.05 + 0.20 + 0.30 = 0.70. With N<sub>4</sub> = 0.60 the sum is 1.00 and T = 15 + 7 + 32 + 72 = 126.0 K.",
        "Baris 4: N<sub>4</sub> = y(a − x)/(ab) = (0.8)(1.5)/2 = 0.60, bukan x(a − y)/(ab). Semakan yang sepatutnya menangkapnya: empat nilai mesti berjumlah 1, dan 0.15 + 0.05 + 0.20 + 0.30 = 0.70. Dengan N<sub>4</sub> = 0.60 jumlahnya 1.00 dan T = 15 + 7 + 32 + 72 = 126.0 K.")
    + '</p></div>'
)

# parameterised calculation exercises: specs in JS (FE from fe_core.js is available)
EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  function N4(a,b,x,y){ return [(a-x)*(b-y)/(a*b), x*(b-y)/(a*b), x*y/(a*b), y*(a-x)/(a*b)]; }
  function dN(a,b,x,y){ return {dx:[-(b-y)/(a*b),(b-y)/(a*b),y/(a*b),-y/(a*b)], dy:[-(a-x)/(a*b),-x/(a*b),x/(a*b),(a-x)/(a*b)]}; }
  function gen(r){
    var a = pick(r,[1.5,2,2.5,3,4]), b = pick(r,[0.5,1,1.5,2]); if (b >= a) b = a/2;
    var x = Math.round((0.1+0.8*r())*a*20)/20, y = Math.round((0.1+0.8*r())*b*20)/20;
    var T = [0,0,0,0].map(function(){ return 60 + 10*Math.floor(r()*12); });
    var k = pick(r,[1,1.5,2,3,5,10]);
    return {a:a,b:b,x:x,y:y,T:T,k:k};
  }
  function given(P, withK){
    return bi("Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m; point (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m; nodal temperatures T̂ = {"+P.T.join(", ")+"} K"+(withK?"; k<sub>x</sub> = k<sub>y</sub> = <span class=\"num\">"+P.k+"</span> W m<sup>−1</sup> K<sup>−1</sup>":"")+". Give 3 decimals for N and 1 decimal for the rest.",
              "Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m; titik (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m; nodal temperature T̂ = {"+P.T.join(", ")+"} K"+(withK?"; k<sub>x</sub> = k<sub>y</sub> = <span class=\"num\">"+P.k+"</span> W m<sup>−1</sup> K<sup>−1</sup>":"")+". Beri 3 tempat perpuluhan untuk N dan 1 tempat perpuluhan untuk yang lain.");
  }
  EX.define("b1", {
    gen: gen, text: function(P){ return given(P,false); },
    fields: [1,2,3,4].map(function(i){ return {id:"n"+i, label:["N<sub>"+i+"</sub>","N<sub>"+i+"</sub>"], fn:function(P){ return N4(P.a,P.b,P.x,P.y)[i-1]; }, atol:0.0015, rtol:0}; })
            .concat([{id:"t", label:["T(x, y)","T(x, y)"], unit:"K", fn:function(P){ var N=N4(P.a,P.b,P.x,P.y); return N[0]*P.T[0]+N[1]*P.T[1]+N[2]*P.T[2]+N[3]*P.T[3]; }, atol:0.15, rtol:0}]),
    hints: [function(P){ return bi("Use (2.21): N<sub>1</sub> = (a − x)(b − y)/(ab), N<sub>2</sub> = x(b − y)/(ab), N<sub>3</sub> = xy/(ab), N<sub>4</sub> = y(a − x)/(ab). Then T = Σ N<sub>i</sub> T̂<sub>i</sub>.",
                                      "Guna (2.21): N<sub>1</sub> = (a − x)(b − y)/(ab), N<sub>2</sub> = x(b − y)/(ab), N<sub>3</sub> = xy/(ab), N<sub>4</sub> = y(a − x)/(ab). Kemudian T = Σ N<sub>i</sub> T̂<sub>i</sub>."); },
            function(P){ return bi("ab = "+fmt(P.a*P.b,2)+"; a − x = "+fmt(P.a-P.x,2)+"; b − y = "+fmt(P.b-P.y,2)+". Check: the four N must sum to 1.",
                                      "ab = "+fmt(P.a*P.b,2)+"; a − x = "+fmt(P.a-P.x,2)+"; b − y = "+fmt(P.b-P.y,2)+". Semak: empat N mesti berjumlah 1."); },
            function(P){ var N=N4(P.a,P.b,P.x,P.y); return bi("N<sub>1</sub> = ("+fmt(P.a-P.x,2)+")("+fmt(P.b-P.y,2)+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[0],3)+". The others follow the same pattern.",
                                      "N<sub>1</sub> = ("+fmt(P.a-P.x,2)+")("+fmt(P.b-P.y,2)+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[0],3)+". Yang lain mengikut pola yang sama."); }],
    solution: function(P){ var N=N4(P.a,P.b,P.x,P.y), T=N[0]*P.T[0]+N[1]*P.T[1]+N[2]*P.T[2]+N[3]*P.T[3];
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">N<sub>1</sub> = ("+fmt(P.a-P.x,2)+")("+fmt(P.b-P.y,2)+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[0],3)+"<br>N<sub>2</sub> = ("+P.x+")("+fmt(P.b-P.y,2)+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[1],3)+"<br>N<sub>3</sub> = ("+P.x+")("+P.y+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[2],3)+"<br>N<sub>4</sub> = ("+P.y+")("+fmt(P.a-P.x,2)+")/"+fmt(P.a*P.b,2)+" = "+fmt(N[3],3)+"<br>Σ N<sub>i</sub> = "+fmt(N[0]+N[1]+N[2]+N[3],3)+"<br>T = "+fmt(N[0],3)+"("+P.T[0]+") + "+fmt(N[1],3)+"("+P.T[1]+") + "+fmt(N[2],3)+"("+P.T[2]+") + "+fmt(N[3],3)+"("+P.T[3]+") = "+fmt(T,1)+" K</p>"; }
  });
  EX.define("b2", {
    gen: gen, text: function(P){ return given(P,true); },
    fields: [{id:"gx", label:["∂T/∂x","∂T/∂x"], unit:"K m⁻¹", fn:function(P){ var d=dN(P.a,P.b,P.x,P.y); return d.dx[0]*P.T[0]+d.dx[1]*P.T[1]+d.dx[2]*P.T[2]+d.dx[3]*P.T[3]; }, atol:0.15, rtol:0.005},
             {id:"gy", label:["∂T/∂y","∂T/∂y"], unit:"K m⁻¹", fn:function(P){ var d=dN(P.a,P.b,P.x,P.y); return d.dy[0]*P.T[0]+d.dy[1]*P.T[1]+d.dy[2]*P.T[2]+d.dy[3]*P.T[3]; }, atol:0.15, rtol:0.005},
             {id:"qx", label:["q<sub>x</sub>","q<sub>x</sub>"], unit:"W m⁻²", fn:function(P){ var d=dN(P.a,P.b,P.x,P.y); return -P.k*(d.dx[0]*P.T[0]+d.dx[1]*P.T[1]+d.dx[2]*P.T[2]+d.dx[3]*P.T[3]); }, atol:0.3, rtol:0.005},
             {id:"qy", label:["q<sub>y</sub>","q<sub>y</sub>"], unit:"W m⁻²", fn:function(P){ var d=dN(P.a,P.b,P.x,P.y); return -P.k*(d.dy[0]*P.T[0]+d.dy[1]*P.T[1]+d.dy[2]*P.T[2]+d.dy[3]*P.T[3]); }, atol:0.3, rtol:0.005}],
    hints: [function(P){ return bi("(2.33): the gradient is the 2 × 4 matrix {∂}ᵀ{N} times {T̂}ᵀ. Row 1 holds ∂N<sub>i</sub>/∂x = {−(b − y), (b − y), y, −y}/(ab); row 2 holds ∂N<sub>i</sub>/∂y = {−(a − x), −x, x, (a − x)}/(ab).",
                                      "(2.33): gradient ialah matrix 2 × 4 {∂}ᵀ{N} didarab {T̂}ᵀ. Baris 1 memuatkan ∂N<sub>i</sub>/∂x = {−(b − y), (b − y), y, −y}/(ab); baris 2 memuatkan ∂N<sub>i</sub>/∂y = {−(a − x), −x, x, (a − x)}/(ab)."); },
            function(P){ var d=dN(P.a,P.b,P.x,P.y); return bi("∂N<sub>i</sub>/∂x = {"+d.dx.map(function(v){return fmt(v,3);}).join(", ")+"} m⁻¹. Multiply by the nodal temperatures and add. Then q = −k × gradient.",
                                      "∂N<sub>i</sub>/∂x = {"+d.dx.map(function(v){return fmt(v,3);}).join(", ")+"} m⁻¹. Darab dengan nodal temperature dan tambah. Kemudian q = −k × gradient."); },
            function(P){ var d=dN(P.a,P.b,P.x,P.y), gx=d.dx[0]*P.T[0]+d.dx[1]*P.T[1]+d.dx[2]*P.T[2]+d.dx[3]*P.T[3]; return bi("∂T/∂x = "+fmt(gx,1)+" K m⁻¹, so q<sub>x</sub> = −("+P.k+")("+fmt(gx,1)+"). Do the same with row 2 for y.",
                                      "∂T/∂x = "+fmt(gx,1)+" K m⁻¹, jadi q<sub>x</sub> = −("+P.k+")("+fmt(gx,1)+"). Buat yang sama dengan baris 2 untuk y."); }],
    solution: function(P){ var d=dN(P.a,P.b,P.x,P.y), gx=0, gy=0; for (var i=0;i<4;i++){ gx+=d.dx[i]*P.T[i]; gy+=d.dy[i]*P.T[i]; }
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">∂N<sub>i</sub>/∂x = {"+d.dx.map(function(v){return fmt(v,3);}).join(", ")+"}<br>∂N<sub>i</sub>/∂y = {"+d.dy.map(function(v){return fmt(v,3);}).join(", ")+"}<br>∂T/∂x = "+d.dx.map(function(v,i){return "("+fmt(v,3)+")("+P.T[i]+")";}).join(" + ")+" = "+fmt(gx,1)+" K m⁻¹<br>∂T/∂y = "+d.dy.map(function(v,i){return "("+fmt(v,3)+")("+P.T[i]+")";}).join(" + ")+" = "+fmt(gy,1)+" K m⁻¹<br>q<sub>x</sub> = −("+P.k+")("+fmt(gx,1)+") = "+fmt(-P.k*gx,1)+" W m⁻²; q<sub>y</sub> = −("+P.k+")("+fmt(gy,1)+") = "+fmt(-P.k*gy,1)+" W m⁻²</p>"; }
  });
  EX.define("b3", {
    gen: gen, text: function(P){ return bi("Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m; nodal temperatures T̂ = {"+P.T.join(", ")+"} K. Find the polynomial coefficients a<sub>1</sub>…a<sub>4</sub> of (2.17) from (2.19), to 2 decimals.",
                                        "Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m; nodal temperature T̂ = {"+P.T.join(", ")+"} K. Cari coefficient polynomial a<sub>1</sub>…a<sub>4</sub> bagi (2.17) daripada (2.19), kepada 2 tempat perpuluhan."); },
    fields: [{id:"a1", label:["a<sub>1</sub>","a<sub>1</sub>"], unit:"K", fn:function(P){ return P.T[0]; }, atol:0.01, rtol:0},
             {id:"a2", label:["a<sub>2</sub>","a<sub>2</sub>"], unit:"K m⁻¹", fn:function(P){ return (P.T[1]-P.T[0])/P.a; }, atol:0.015, rtol:0.002},
             {id:"a3", label:["a<sub>3</sub>","a<sub>3</sub>"], unit:"K m⁻¹", fn:function(P){ return (P.T[3]-P.T[0])/P.b; }, atol:0.015, rtol:0.002},
             {id:"a4", label:["a<sub>4</sub>","a<sub>4</sub>"], unit:"K m⁻²", fn:function(P){ return (P.T[0]-P.T[1]+P.T[2]-P.T[3])/(P.a*P.b); }, atol:0.015, rtol:0.002}],
    hints: [function(P){ return bi("(2.19): a<sub>1</sub> = T̂<sub>1</sub>; a<sub>2</sub> = (T̂<sub>2</sub> − T̂<sub>1</sub>)/a; a<sub>3</sub> = (T̂<sub>4</sub> − T̂<sub>1</sub>)/b; a<sub>4</sub> = (T̂<sub>1</sub> − T̂<sub>2</sub> + T̂<sub>3</sub> − T̂<sub>4</sub>)/(ab).",
                                      "(2.19): a<sub>1</sub> = T̂<sub>1</sub>; a<sub>2</sub> = (T̂<sub>2</sub> − T̂<sub>1</sub>)/a; a<sub>3</sub> = (T̂<sub>4</sub> − T̂<sub>1</sub>)/b; a<sub>4</sub> = (T̂<sub>1</sub> − T̂<sub>2</sub> + T̂<sub>3</sub> − T̂<sub>4</sub>)/(ab)."); },
            function(P){ return bi("Check your a<sub>4</sub> by evaluating T at node 3: a<sub>1</sub> + a<sub>2</sub>a + a<sub>3</sub>b + a<sub>4</sub>ab must equal T̂<sub>3</sub> = "+P.T[2]+".",
                                      "Semak a<sub>4</sub> anda dengan menilai T pada node 3: a<sub>1</sub> + a<sub>2</sub>a + a<sub>3</sub>b + a<sub>4</sub>ab mesti sama dengan T̂<sub>3</sub> = "+P.T[2]+"."); }],
    solution: function(P){ var a1=P.T[0], a2=(P.T[1]-P.T[0])/P.a, a3=(P.T[3]-P.T[0])/P.b, a4=(P.T[0]-P.T[1]+P.T[2]-P.T[3])/(P.a*P.b);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">a<sub>1</sub> = "+a1+"<br>a<sub>2</sub> = ("+P.T[1]+" − "+P.T[0]+")/"+P.a+" = "+fmt(a2,2)+"<br>a<sub>3</sub> = ("+P.T[3]+" − "+P.T[0]+")/"+P.b+" = "+fmt(a3,2)+"<br>a<sub>4</sub> = ("+P.T[0]+" − "+P.T[1]+" + "+P.T[2]+" − "+P.T[3]+")/"+fmt(P.a*P.b,2)+" = "+fmt(a4,2)+"<br>"+bi("Check at node 3: ","Semak pada node 3: ")+fmt(a1+a2*P.a+a3*P.b+a4*P.a*P.b,2)+" = T̂<sub>3</sub></p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("Shape functions at a point, and the interpolated temperature", "Shape function pada satu titik, dan temperature yang di-interpolate"), 5),
    ("b2", ("Gradient and flux at the point", "Gradient dan flux pada titik itu"), 5),
    ("b3", ("The polynomial coefficients from the nodal values", "Coefficient polynomial daripada nilai node"), 4),
]

LAB_TASKS = [
    ("node3", ("Drag P onto node 3 (or press “P on node 3”). Read N<sub>1</sub>…N<sub>4</sub>: the Kronecker property.", "Seret P ke node 3 (atau tekan “P on node 3”). Baca N<sub>1</sub>…N<sub>4</sub>: sifat Kronecker."),
              ("detected when P reaches node 3 on the 4-node element", "dikesan apabila P sampai ke node 3 pada 4-node element")),
    ("act4", ("Press “Activity 4 point”: P = (1.5, 0.3). Compare with your hand answers from Activity 4 and 5.", "Tekan “Activity 4 point”: P = (1.5, 0.3). Bandingkan dengan jawapan tangan anda daripada Aktiviti 4 dan 5."),
             ("detected when P = (1.5, 0.3) in the 2 × 1 element", "dikesan apabila P = (1.5, 0.3) dalam element 2 × 1")),
    ("diag", ("Find three points where N<sub>1</sub> = N<sub>3</sub>. What line joins them?", "Cari tiga titik di mana N<sub>1</sub> = N<sub>3</sub>. Garis apakah yang menghubungkannya?"),
             ("detected after three distinct points with |N<sub>1</sub> − N<sub>3</sub>| &lt; 0.01", "dikesan selepas tiga titik berbeza dengan |N<sub>1</sub> − N<sub>3</sub>| &lt; 0.01")),
    ("q8n1", ("Switch to the 8-node element and show N<sub>1</sub>. Where is it negative, and how can the weights still sum to 1?", "Tukar kepada 8-node element dan paparkan N<sub>1</sub>. Di mana ia negatif, dan bagaimana N<sub>i</sub> masih berjumlah 1?"),
             ("detected when the 8-node element shows N<sub>1</sub>", "dikesan apabila 8-node element memaparkan N<sub>1</sub>")),
]

GLOSSARY = [
    ("field problem", "An unknown defined at every point of a region, such as T(x, y), rather than at a few discrete locations.", "Unknown yang wujud pada setiap titik dalam satu kawasan, seperti T(x, y), bukannya pada beberapa lokasi diskret sahaja."),
    ("scalar field · vector field", "One number per point (temperature) versus two or more per point (displacement u, v).", "Satu nombor setiap titik (temperature) berbanding dua atau lebih setiap titik (displacement u, v)."),
    ("heat flux q", "Energy crossing a unit area per unit time, W m<sup>−2</sup>; a vector with components q<sub>x</sub>, q<sub>y</sub>.", "Tenaga yang melintasi unit luas per unit masa, W m<sup>−2</sup>; satu vector dengan komponen q<sub>x</sub>, q<sub>y</sub>."),
    ("Fourier’s law", "q = −k ∇T: flux is proportional to the temperature gradient and points from hot to cold.", "q = −k ∇T: flux berkadar dengan temperature gradient dan menghala dari panas ke sejuk."),
    ("conductivity k", "Material property, W m<sup>−1</sup> K<sup>−1</sup>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>) for an orthotropic material.", "Sifat bahan, W m<sup>−1</sup> K<sup>−1</sup>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>) bagi bahan orthotropic."),
    ("heat generation q<sub>h</sub>", "Heat produced per unit volume, W m<sup>−3</sup>, for example by cement hydration.", "Haba dihasilkan per unit isi padu, W m<sup>−3</sup>, contohnya oleh hydration simen."),
    ("steady state", "Nothing changes with time: ∂T/∂t = 0, so the stored-energy term disappears.", "Tiada yang berubah dengan masa: ∂T/∂t = 0, jadi term tenaga tersimpan hilang."),
    ("Poisson · Laplace", "Special cases of (2.11): constant isotropic k gives Poisson’s equation; no source gives Laplace’s equation.", "Kes khas (2.11): k constant dan isotropic memberi Poisson’s equation; tanpa source memberi Laplace’s equation."),
    ("boundary condition", "What is specified on the edge of the domain: the temperature or the flux. Needed on every part of the boundary.", "Apa yang ditetapkan pada tepi domain: temperature atau flux. Diperlukan pada setiap bahagian sempadan."),
    ("Dirichlet · essential", "A known value of the unknown field on the edge, T = T̄. Imposed on the assembled equations.", "Nilai yang diketahui bagi field pada tepi, T = T̄. Dikenakan pada assembled equation."),
    ("Neumann · natural", "A known flux on the edge, q<sub>b</sub>, positive inward. Appears by itself through the integration by parts.", "Flux yang diketahui pada tepi, q<sub>b</sub>, positif ke dalam. Muncul dengan sendiri melalui integration by parts."),
    ("outward normal n", "Unit vector pointing out of the domain at an edge; on a rectangle (±1, 0) or (0, ±1).", "Unit vector yang menghala keluar dari domain pada satu tepi; pada segi empat tepat (±1, 0) atau (0, ±1)."),
    ("insulated edge", "A natural condition with q<sub>b</sub> = 0. Requires no action in the finite element model.", "Natural condition dengan q<sub>b</sub> = 0. Tidak memerlukan apa-apa tindakan dalam model finite element."),
    ("well-posed", "Every edge has a condition and the temperature level is fixed somewhere, so the solution is unique.", "Setiap tepi ada condition dan paras temperature ditetapkan di suatu tempat, jadi penyelesaiannya unik."),
    ("element · node", "A small region (here a rectangle a × b) and the points on it where the unknowns live.", "Kawasan kecil (di sini segi empat tepat a × b) dan titik-titik padanya tempat unknown berada."),
    ("degree of freedom", "One unknown of the discrete system; one temperature per node for conduction.", "Satu unknown dalam sistem diskret; satu temperature setiap node bagi conduction."),
    ("shape function N<sub>i</sub>", "The function of position that multiplies nodal value i in the interpolation T = Σ N<sub>i</sub> T̂<sub>i</sub>.", "Fungsi kedudukan yang mendarab nilai node i dalam interpolation T = Σ N<sub>i</sub> T̂<sub>i</sub>."),
    ("bilinear", "Linear in x and in y separately, with an xy term: the four-node element’s polynomial (2.17).", "Linear dalam x dan dalam y secara berasingan, dengan term xy: polynomial four-node element (2.17)."),
    ("Kronecker delta", "N<sub>i</sub> = 1 at its own node and 0 at the others; so the nodal unknowns are nodal temperatures.", "N<sub>i</sub> = 1 pada node sendiri dan 0 pada node lain; jadi nodal unknown ialah temperature pada node."),
    ("partition of unity", "Σ N<sub>i</sub> = 1 at every point; a uniform field is reproduced exactly.", "Σ N<sub>i</sub> = 1 pada setiap titik; field yang seragam dihasilkan semula dengan tepat."),
    ("C<sup>0</sup> continuity", "T is continuous across element edges but its derivative generally jumps.", "T continuous merentasi tepi element tetapi derivative-nya biasanya melompat."),
    ("gradient matrix {∂}ᵀ{N}", "The 2 × 4 matrix of shape-function derivatives; gradient = {∂}ᵀ{N}{T̂}ᵀ.", "Matrix 2 × 4 bagi derivative shape function; gradient = {∂}ᵀ{N}{T̂}ᵀ."),
    ("conductance matrix [k]", "The element matrix of Part 2, [k] = ∫∫{N}ᵀ{∂}[E]{∂}ᵀ{N} dy dx; the heat analogue of stiffness.", "Matrix element dalam Part 2, [k] = ∫∫{N}ᵀ{∂}[E]{∂}ᵀ{N} dy dx; analog haba bagi stiffness."),
    ("assembly · connectivity", "Adding element matrices into the global system using each element’s list of global node numbers.", "Menambah matrix element ke dalam sistem global menggunakan senarai nombor node global setiap element."),
]


def short_notes(A):
    return (
        "<h3>§1 " + B("Field problem", "Field problem") + "</h3>" + P("One unknown per node, T̂<sub>i</sub>; the element interpolates between nodes. FEM adds no physics.", "Satu unknown setiap node, T̂<sub>i</sub>; element membuat interpolation antara node. FEM tidak menambah fizik.")
        + "<h3>§2 PDE</h3>" + A.eq("e_pde", "(2.11)", 0.5) + A.eq("e_compact", "(2.13)", 0.5) + P("Units W m<sup>−3</sup>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>).", "Unit W m<sup>−3</sup>; [E] = diag(k<sub>x</sub>, k<sub>y</sub>).")
        + "<h3>§3 " + B("Boundary conditions", "Boundary condition") + "</h3>" + A.eq("e_dirichlet", "(2.16)", 0.5) + A.eq("e_neumann", "(2.15)", 0.5)
        + LI([("Dirichlet = essential = imposed.", "Dirichlet = essential = dikenakan."), ("Neumann = natural = appears from integration by parts; q<sub>b</sub> positive inward.", "Neumann = natural = muncul daripada integration by parts; q<sub>b</sub> positif ke dalam."), ("Insulated: do nothing.", "Insulated: tiada tindakan.")])
        + "<h3>§4 " + B("Shape functions", "Shape function") + "</h3>" + A.eq("e_shape", "(2.21)", 0.5) + A.eq("e_T_N", "(2.22)", 0.5)
        + LI([("Kronecker delta · partition of unity · linear edges.", "Kronecker delta · partition of unity · tepi linear."), ("(1.5, 0.3): N = 0.175, 0.525, 0.225, 0.075; T = 136.0 K.", "(1.5, 0.3): N = 0.175, 0.525, 0.225, 0.075; T = 136.0 K.")])
        + "<h3>§5 " + B("Gradient and flux", "Gradient dan flux") + "</h3>" + A.eq("e_dN", None, 0.5) + A.eq("e_flux_vec", None, 0.5)
        + P("At (1.5, 0.3), k = 2: ∂T/∂x = ∂T/∂y = 20 K m<sup>−1</sup>; q<sub>x</sub> = q<sub>y</sub> = −40 W m<sup>−2</sup>.", "Pada (1.5, 0.3), k = 2: ∂T/∂x = ∂T/∂y = 20 K m<sup>−1</sup>; q<sub>x</sub> = q<sub>y</sub> = −40 W m<sup>−2</sup>.")
        + "<h3>§6 Pipeline</h3>" + P("1 PDE + BCs · 2 element · 3 Galerkin · 4 integration by parts · 5 [k], {q}, {b} · 6 assembly + impose T̄ · 7 solve.", "1 PDE + BC · 2 element · 3 Galerkin · 4 integration by parts · 5 [k], {q}, {b} · 6 assembly + kenakan T̄ · 7 selesaikan.")
    )


# ---- worked examples: answer-scheme style, from the course companion (FEM by Hand, Ch. 8) ----
EXAMPLES_INTRO = (
    '<div class="card" style="margin-bottom:18px"><h2 style="font-size:18px;margin:0 0 6px">' + B("How this topic is examined", "Bagaimana topik ini diuji") + '</h2>'
    + P("Model answers in the form the examiner expects: physical picture, plan, numbered steps with every substitution written out, checks, a boxed answer and an interpretation. "
        "The marks shown are a suggested scheme for a 20-mark question; the examiner’s own scheme may differ.",
        "Jawapan model dalam bentuk yang pemeriksa jangkakan: gambaran fizikal, pelan, langkah bernombor dengan setiap penggantian ditulis, semakan, jawapan berkotak dan tafsiran. "
        "Markah yang ditunjukkan ialah skema cadangan untuk soalan 20 markah; skema pemeriksa sendiri mungkin berbeza.", "lead")
    + '<div class="tbl"><table class="howex"><tr><th>' + B("Question type", "Jenis soalan") + '</th><th>' + B("Given and wanted", "Diberi dan dikehendaki") + '</th><th>' + B("Plan and the usual trap", "Pelan dan perangkap biasa") + '</th></tr>'
    + '<tr><td>' + B("Shape functions", "Shape function") + '</td><td>' + B("Node coordinates and the interpolation polynomial; wanted: N<sub>i</sub>.", "Koordinat node dan polynomial interpolation; dikehendaki: N<sub>i</sub>.") + '</td><td>' + B("Nodal conditions, solve for a<sub>i</sub>, collect the T<sub>i</sub>. Trap: no check of N<sub>i</sub> = 1 at node i and 0 at the others.", "Nodal condition, selesaikan a<sub>i</sub>, kumpulkan T<sub>i</sub>. Perangkap: tiada semakan N<sub>i</sub> = 1 pada node i dan 0 pada node lain.") + '</td></tr>'
    + '<tr><td>' + B("Temperature at a point", "Temperature pada satu titik") + '</td><td>' + B("Nodal temperatures; wanted: T(x, y), sometimes the flux.", "Nodal temperature; dikehendaki: T(x, y), kadang-kadang flux.") + '</td><td>' + B("Find the element, use its local coordinates in N<sub>i</sub>. Trap: global x, y in N<sub>i</sub>.", "Cari element, guna koordinat local dalam N<sub>i</sub>. Perangkap: x, y global dalam N<sub>i</sub>.") + '</td></tr>'
    + '<tr><td>' + B("Explain", "Terangkan") + '</td><td>' + B("Imposing T = T̄; insulated edges; why a row adds up to zero.", "Mengenakan T = T̄; tepi insulated; mengapa satu baris berjumlah sifar.") + '</td><td>' + B("Claim, reason, consequence — three sentences, in that order.", "Dakwaan, sebab, akibat — tiga ayat, mengikut urutan itu.") + '</td></tr></table></div>'
    + P("Notation follows the companion: Q is the heat generated per unit volume (the text’s q<sub>h</sub>), q<sub>n</sub> the inward boundary flux (the text’s q<sub>b</sub>), t the thickness.",
        "Notasi mengikut buku pendamping: Q ialah haba dijana per unit isi padu (q<sub>h</sub> dalam teks), q<sub>n</sub> boundary flux ke dalam (q<sub>b</sub> dalam teks), t ketebalan.", "lead")
    + '</div>')


def examples(A):
    X = []
    # ---- Example 1: three-node triangle (companion Example 8.1) ----
    head = ('<div class="xhead"><h2>' + B("Example 1 · Shape functions and conductance matrix of a triangle", "Contoh 1 · Shape function dan conductance matrix bagi segi tiga") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> derive N<sub>1</sub>, N<sub>2</sub>, N<sub>3</sub> from T = a<sub>1</sub> + a<sub>2</sub>x + a<sub>3</sub>y, then [k]</span><span><b>' + B("Units", "Unit") + '</b> symbolic</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 8.1</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>A three-node heat element has its nodes at (0, 0), (L, 0) and (L/2, L). With the interpolation T(x, y) = a<sub>1</sub> + a<sub>2</sub>x + a<sub>3</sub>y, '
         '(a) derive the shape functions by writing T = N<sub>1</sub>T<sub>1</sub> + N<sub>2</sub>T<sub>2</sub> + N<sub>3</sub>T<sub>3</sub>, (b) check them, and (c) find the conductance matrix for k<sub>x</sub> = k<sub>y</sub> = k and thickness t.</div>')
    body = (head + q + A.fig("fig_tri", "The triangle of Example 1.", "Segi tiga bagi Contoh 1.", 330)
            + PIC("A plane over a triangle is fixed by its three corner values, so the three nodal temperatures determine a<sub>1</sub>, a<sub>2</sub> and a<sub>3</sub>. Each shape function is the field obtained with its own node at 1 and the other two at 0: a plane that is 1 at that node and 0 along the opposite side. Side 1–2 lies on y = 0, so N<sub>3</sub> must depend on y only.",
                  "Satah di atas segi tiga ditentukan oleh tiga nilai bucunya, jadi tiga nodal temperature menentukan a<sub>1</sub>, a<sub>2</sub> dan a<sub>3</sub>. Setiap shape function ialah field yang diperoleh dengan node sendiri bernilai 1 dan dua node lain 0: satah yang bernilai 1 pada node itu dan 0 di sepanjang sisi bertentangan. Sisi 1–2 terletak pada y = 0, jadi N<sub>3</sub> mesti bergantung pada y sahaja.")
            + PLAN("Three nodal conditions → a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub> → collect T<sub>1</sub>, T<sub>2</sub>, T<sub>3</sub> → checks → derivatives → [k].")
            + XSTEP(1, "Nodal conditions", "Nodal condition", 3, A.eq("x1_cond"))
            + XSTEP(2, "(a) The coefficients", "(a) Coefficient", 3, P("From the first two, a<sub>1</sub> = T<sub>1</sub> and a<sub>2</sub> = (T<sub>2</sub> − T<sub>1</sub>)/L. The third then gives", "Daripada dua yang pertama, a<sub>1</sub> = T<sub>1</sub> dan a<sub>2</sub> = (T<sub>2</sub> − T<sub>1</sub>)/L. Yang ketiga kemudian memberi") + A.eq("x1_coef"))
            + XSTEP(3, "Collecting the nodal temperatures", "Mengumpul nodal temperature", 2, A.eq("x1_collect") + ANS("(a) " + A.eq("x1_N")))
            + XSTEP(4, "(b) Checks", "(b) Semakan", 3, A.eq("x1_checks") + P("Nodes 1 and 2 check in the same way. At the centroid (L/2, L/3) each function is 1/3.", "Node 1 dan 2 disemak dengan cara yang sama. Pada centroid (L/2, L/3) setiap fungsi bernilai 1/3.") + ANS("(b) N<sub>i</sub> = 1 at node i and 0 at the others; ΣN<sub>i</sub> = 1 everywhere."))
            + XSTEP(5, "(c) Derivatives and [k]", "(c) Derivative dan [k]", 9, A.eq("x1_dN")
                    + P("The derivatives are constant, so the integral k<sub>ij</sub> = t∫(k<sub>x</sub> N<sub>i,x</sub>N<sub>j,x</sub> + k<sub>y</sub> N<sub>i,y</sub>N<sub>j,y</sub>) dA is the area times the integrand (the conductance matrix of Part 2):",
                        "Derivative itu pemalar, jadi integral k<sub>ij</sub> = t∫(k<sub>x</sub> N<sub>i,x</sub>N<sub>j,x</sub> + k<sub>y</sub> N<sub>i,y</sub>N<sub>j,y</sub>) dA ialah luas didarab integrand (conductance matrix dalam Part 2):")
                    + A.eq("x1_kij") + ANS("(c) " + A.eq("x1_k") + "each row adds up to zero.") + CHK("Row 1: 5 − 3 − 2 = 0; row 3: −2 − 2 + 4 = 0. [k] is symmetric."))
            + INTERP("[k] does not contain L. Each entry is the thickness times the area, which grows as L², times a product of two gradients, each of which falls as 1/L; the two effects cancel, so a triangle of the same shape conducts the same heat per kelvin whatever its size. Every row adds up to zero because a uniform temperature, T<sub>1</sub> = T<sub>2</sub> = T<sub>3</sub>, produces no heat flow. The temperature inside the element is a plane, so its gradient, and with it the heat flux, is constant in each element and jumps from one element to the next; the temperature itself stays continuous, since along a shared side it varies linearly between the same two nodal values.",
                     "[k] tidak mengandungi L. Setiap entri ialah ketebalan didarab luas, yang membesar sebagai L², didarab hasil darab dua gradient yang masing-masing menyusut sebagai 1/L; dua kesan itu saling membatalkan, jadi segi tiga dengan bentuk yang sama mengalirkan haba yang sama per kelvin tanpa mengira saiznya. Setiap baris berjumlah sifar kerana temperature seragam, T<sub>1</sub> = T<sub>2</sub> = T<sub>3</sub>, tidak menghasilkan aliran haba. Temperature di dalam element ialah satah, jadi gradient-nya, dan seterusnya heat flux, adalah pemalar dalam setiap element dan melompat dari satu element ke element seterusnya; temperature itu sendiri kekal continuous, kerana di sepanjang sisi yang dikongsi ia berubah secara linear antara dua nilai node yang sama.")
            + SCHEME([("Three nodal conditions written correctly", "Tiga nodal condition ditulis dengan betul", 3), ("a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>", "a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>", 3), ("Collecting by nodal value → N<sub>1</sub>, N<sub>2</sub>, N<sub>3</sub>", "Mengumpul mengikut nilai node → N<sub>1</sub>, N<sub>2</sub>, N<sub>3</sub>", 2),
                      ("Kronecker and partition-of-unity checks", "Semakan Kronecker dan partition of unity", 3), ("Derivative vectors and the area", "Vektor derivative dan luas", 3), ("Three entries by integration, matrix by symmetry, row-sum check", "Tiga entri melalui integration, matrix melalui simetri, semakan jumlah baris", 6)], 20))
    X.append(("x1", "Shape functions and [k] of a triangle", "Shape function dan [k] bagi segi tiga", body))

    # ---- Example 2: temperature and flux at a point (companion Practice Problem 8.3, fully worked) ----
    head = ('<div class="xhead"><h2>' + B("Example 2 · Temperature and flux at a point of a four-node element", "Contoh 2 · Temperature dan flux pada satu titik four-node element") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> T(x, y), ∂T/∂x, ∂T/∂y and q from nodal temperatures</span><span><b>' + B("Units", "Unit") + '</b> m, °C, W</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Practice Problem 8.3 (worked in full here)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>A four-node element 0.4 m by 0.3 m has nodal temperatures 20, 40, 60 and 30 °C at nodes 1 to 4 (anticlockwise from the origin), and k = 15 W m<sup>−1</sup> K<sup>−1</sup>. '
         'Find T, q<sub>x</sub> and q<sub>y</sub> (a) at the centre and (b) at the local point (0.1, 0.2) m.</div>')
    body = (head + q + A.fig("fig_pp83", "The element of Example 2 with its nodal temperatures and the two points.", "Element bagi Contoh 2 dengan nodal temperature dan dua titiknya.", 380)
            + PIC("The nodal values rise from node 1 to node 3, so the temperature increases in both +x and +y; Fourier’s law then makes both flux components negative, pointing back towards node 1. The gradient of a bilinear field is not constant: ∂T/∂x changes with y and ∂T/∂y with x, so the two points will give different fluxes.",
                  "Nilai node meningkat dari node 1 ke node 3, jadi temperature bertambah dalam arah +x dan +y; Fourier’s law kemudian menjadikan kedua-dua komponen flux negatif, menghala kembali ke node 1. Gradient bagi field bilinear tidak malar: ∂T/∂x berubah dengan y dan ∂T/∂y dengan x, jadi dua titik itu akan memberi flux yang berbeza.")
            + PLAN("N<sub>i</sub> at the point → T = ΣN<sub>i</sub>T<sub>i</sub> → ∂N<sub>i</sub>/∂x, ∂N<sub>i</sub>/∂y from (2.33) → gradient → q = −k∇T. ab = 0.4 × 0.3 = 0.12 m² throughout.")
            + XSTEP(1, "(a) Shape functions and T at the centre", "(a) Shape function dan T pada pusat", 4, A.eq("x2_Nc"))
            + XSTEP(2, "(a) Derivatives at the centre (y = 0.15, x = 0.2)", "(a) Derivative pada pusat (y = 0.15, x = 0.2)", 3, A.eq("x2_dNc") + A.eq("x2_dNcy"))
            + XSTEP(3, "(a) Gradient and flux at the centre", "(a) Gradient dan flux pada pusat", 3, A.eq("x2_gradc") + ANS("(a) T = 37.5 °C; q<sub>x</sub> = −938 W m<sup>−2</sup>, q<sub>y</sub> = −750 W m<sup>−2</sup>.")
                    + CHK("ΣN<sub>i</sub> = 1. Both fluxes negative, as the physical picture predicted."))
            + XSTEP(4, "(b) Shape functions and T at (0.1, 0.2)", "(b) Shape function dan T pada (0.1, 0.2)", 5, P("With a − x = 0.3 and b − y = 0.1:", "Dengan a − x = 0.3 dan b − y = 0.1:") + A.eq("x2_Np"))
            + XSTEP(5, "(b) Gradient and flux at (0.1, 0.2)", "(b) Gradient dan flux pada (0.1, 0.2)", 5, A.eq("x2_gradp") + ANS("(b) T = 33.3 °C; q<sub>x</sub> = −1000 W m<sup>−2</sup>, q<sub>y</sub> = −625 W m<sup>−2</sup>."))
            + INTERP("The gradient changes between the two points because T<sub>1</sub> − T<sub>2</sub> + T<sub>3</sub> − T<sub>4</sub> = 20 − 40 + 60 − 30 = 10 ≠ 0: that combination is the coefficient a<sub>4</sub> of the xy term, and it is the only reason the field is not a plane. With four values that sum to zero in that pattern the flux would be the same everywhere in the element. The numbers also show the sign convention at work: a flux is negative when the temperature increases in that direction.",
                     "Gradient berubah antara dua titik itu kerana T<sub>1</sub> − T<sub>2</sub> + T<sub>3</sub> − T<sub>4</sub> = 20 − 40 + 60 − 30 = 10 ≠ 0: gabungan itu ialah coefficient a<sub>4</sub> bagi term xy, dan itulah satu-satunya sebab field itu bukan satah. Dengan empat nilai yang berjumlah sifar dalam pola itu, flux akan sama di seluruh element. Nombor-nombor itu juga menunjukkan tanda yang digunakan: flux negatif apabila temperature meningkat dalam arah itu.")
            + SCHEME([("N<sub>i</sub> = 1/4 at the centre and T", "N<sub>i</sub> = 1/4 pada pusat dan T", 4), ("Derivative rows at the centre", "Baris derivative pada pusat", 3), ("Gradient, then q = −k∇T with signs", "Gradient, kemudian q = −k∇T dengan tanda", 3),
                      ("N<sub>i</sub> at (0.1, 0.2), sum check, T", "N<sub>i</sub> pada (0.1, 0.2), semakan jumlah, T", 5), ("Gradient and flux at the point", "Gradient dan flux pada titik itu", 5)], 20))
    X.append(("x2", "Temperature and flux at a point", "Temperature dan flux pada satu titik", body))

    # ---- Example 3: explain-type questions (companion §8.4) ----
    head = ('<div class="xhead"><h2>' + B("Example 3 · Explain-type questions: model answers", "Contoh 3 · Soalan jenis terangkan: jawapan model") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> explain, three sentences each: claim, reason, consequence</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, §8.4</span><span><b>4 × 3 = 12 ' + B("marks", "markah") + '</b></span></div></div>')
    def qa(n, q_en, q_ms, a_en, a_ms):
        return XSTEP(n, q_en, q_ms, 3, '<p>' + B(a_en, a_ms) + '</p>')
    body = (head
            + '<div class="xq"><span class="qlabel">' + B("Questions", "Soalan") + '</span>' + B("Answer each in two or three sentences. State the claim, give the reason, and say what follows from it.", "Jawab setiap satu dalam dua atau tiga ayat. Nyatakan dakwaan, beri sebab, dan nyatakan apa yang terhasil daripadanya.") + '</div>'
            + qa(1, "Why is nothing done at an insulated edge?", "Mengapa tiada apa-apa dibuat pada tepi insulated?",
                 "An insulated edge is a natural condition with q<sub>n</sub> = 0, so its boundary term t∫{N}q<sub>n</sub> ds is zero. The Galerkin formulation satisfies it approximately without any action. A non-zero flux would instead enter {r} at the nodes of that edge.",
                 "Tepi insulated ialah natural condition dengan q<sub>n</sub> = 0, jadi boundary term-nya t∫{N}q<sub>n</sub> ds ialah sifar. Formulasi Galerkin memenuhinya secara anggaran tanpa sebarang tindakan. Flux bukan sifar pula akan masuk ke {r} pada node tepi itu.")
            + qa(2, "What is the difference between an essential and a natural boundary condition, and how is each imposed?", "Apakah perbezaan antara essential dan natural boundary condition, dan bagaimana setiap satu dikenakan?",
                 "An essential condition prescribes the primary variable, the temperature T = T̄; a natural condition prescribes the secondary variable, the flux q<sub>n</sub>. The essential condition is imposed on the assembled equations by striking the rows and columns of the known nodes, and the struck rows later give the heat flows there. The natural condition is never imposed: it appears by itself as a load through the boundary term of the integration by parts.",
                 "Essential condition menetapkan primary variable, iaitu temperature T = T̄; natural condition menetapkan secondary variable, iaitu flux q<sub>n</sub>. Essential condition dikenakan pada assembled equation dengan membuang baris dan lajur node yang diketahui, dan baris yang dibuang itu kemudian memberi aliran haba di situ. Natural condition tidak pernah dikenakan: ia muncul dengan sendirinya sebagai load melalui boundary term daripada integration by parts.")
            + qa(3, "Why does every row of [k] add up to zero, and how is that used?", "Mengapa setiap baris [k] berjumlah sifar, dan bagaimana ia digunakan?",
                 "Since ΣN<sub>i</sub> = 1, a uniform temperature makes every gradient zero and conducts no heat, so [k]{1, 1, …}ᵀ = {0}. Consequently [k], and an unrestrained [K], are singular, which is why at least one temperature must be prescribed. Every row of a computed matrix can be checked in a few seconds by adding it up." + A.eq("x3_rowsum", None, 0.5),
                 "Oleh kerana ΣN<sub>i</sub> = 1, temperature seragam menjadikan setiap gradient sifar dan tidak mengalirkan haba, jadi [k]{1, 1, …}ᵀ = {0}. Akibatnya [k], dan [K] yang tidak dikekang, adalah singular; sebab itulah sekurang-kurangnya satu temperature mesti ditetapkan. Setiap baris matrix yang dikira boleh disemak dalam beberapa saat dengan menjumlahkannya." + A.eq("x3_rowsum", None, 0.5))
            + qa(4, "How do the three-node and the four-node elements differ?", "Bagaimana three-node dan four-node element berbeza?",
                 "The T3 field is a plane, so its gradient and flux are constant in each element. The Q4 field contains xy, so ∂T/∂x varies with y and ∂T/∂y with x. Both fields vary linearly along every side, so the temperature is continuous between elements while the flux jumps; on the same nodes the Q4 is usually more accurate, but in this course it is limited to rectangles, whereas triangles fit any shape.",
                 "Field T3 ialah satah, jadi gradient dan flux-nya malar dalam setiap element. Field Q4 mengandungi xy, jadi ∂T/∂x berubah dengan y dan ∂T/∂y dengan x. Kedua-dua field berubah secara linear di sepanjang setiap sisi, jadi temperature continuous antara element manakala flux melompat; pada node yang sama Q4 biasanya lebih tepat, tetapi dalam kursus ini ia terhad kepada segi empat tepat, manakala segi tiga sesuai untuk apa jua bentuk.")
            + INTERP("The examiner looks for the three parts in order. “Insulated means do nothing” alone is a claim without a reason and earns one mark of three; naming the boundary term and its value earns the other two.",
                     "Pemeriksa mencari tiga bahagian mengikut urutan. “Insulated bermaksud tiada tindakan” sahaja ialah dakwaan tanpa sebab dan mendapat satu daripada tiga markah; menamakan boundary term dan nilainya mendapat dua markah lagi.")
            + SCHEME([("Claim stated correctly", "Dakwaan dinyatakan dengan betul", "1 each"), ("Reason: the term, the property or the equation behind it", "Sebab: term, sifat atau persamaan di sebaliknya", "1 each"), ("Consequence for the calculation", "Akibat kepada pengiraan", "1 each")], 12))
    X.append(("x3", "Explain-type questions", "Soalan jenis terangkan", body))
    return X
