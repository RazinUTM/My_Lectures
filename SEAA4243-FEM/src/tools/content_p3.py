"""Content of Plane Stress Part 1 (site part 3): equilibrium, Hooke's law, strain-displacement, boundary
conditions and the shape-function matrix [N]. Numbers are those of deck W11 and the text (Mohd Yassin et al.,
MSNM 2020, Ch. 3); every value in the examples and exercises was recomputed in Python before it was written."""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, QC, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME
from content_p1 import MCQ

PART = {
    "n": 3, "slug": "03-plane-stress-1", "deck": "deck_w11", "eqs": ["eqs_w11", "eqs_ps1_ex"], "figs": ["figs_w11", "figs_w9", "figs_ps1_ex"],
    "topic": ("Plane Stress", "Plane Stress"), "part": "Part 1 of 3",
    "title": "Plane Stress — Part 1",
    "sub": ("Two unknowns at every point: equilibrium, Hooke’s law and strain–displacement give [∂][E][∂]ᵀ{u}ᵀ = −{f}; then the boundary conditions and the element’s 2 × 8 shape-function matrix [N].",
            "Dua unknown pada setiap titik: equilibrium, Hooke’s law dan strain–displacement memberi [∂][E][∂]ᵀ{u}ᵀ = −{f}; kemudian boundary condition dan shape-function matrix [N] 2 × 8 bagi element."),
    "pdf": "pdf/plane-stress-1-slides.pdf",
    "lab": {"id": "cant", "file": "../labs/cant.html", "name": "Cantilever Explorer", "inclass": "pstrain"},
    "minutes": {"n1": 7, "n2": 10, "n3": 8, "n4": 7, "n5": 9, "n6": 8},
    "target_min": 33,
    "code": "ps",
    "textref": "§3.1–§3.2.1",
    "covers": ("Heat transfer had one unknown per node; plane stress has two, the displacements u and v. The governing equation needs three ingredients instead of two: equilibrium of a small element, Hooke’s law, and the relation between strains and displacements. Together they give the same pattern as heat transfer, [∂][E][∂]ᵀ{u}ᵀ = −{f}, with bigger matrices. This part also sets up the boundary conditions and the shape-function matrix [N]; Part 2 builds [k] and solves the cantilever, and Part 3 recovers the stresses.",
               "Heat transfer ada satu unknown setiap node; plane stress ada dua, iaitu displacement u dan v. Persamaan pentadbir memerlukan tiga bahan, bukan dua: equilibrium bagi element kecil, Hooke’s law, dan hubungan antara strain dan displacement. Bersama-sama ia memberi pola yang sama dengan heat transfer, [∂][E][∂]ᵀ{u}ᵀ = −{f}, dengan matrix yang lebih besar. Bahagian ini juga menyediakan boundary condition dan shape-function matrix [N]; Part 2 membina [k] dan menyelesaikan cantilever, dan Part 3 mendapatkan semula stress."),
    "inclass_n": ("3 h · 5 activities", "3 jam · 5 aktiviti"),
    "inclass": [("A1 plane stress, plane strain or neither · A2 the y-direction balance", "A1 plane stress, plane strain atau bukan kedua-duanya · A2 keseimbangan arah y"),
                ("A3 [E] of the cantilever · A4 its boundary conditions", "A3 [E] bagi cantilever · A4 boundary condition-nya"),
                ("A5 u and v at (3.5, 1.3) in element 4", "A5 u dan v pada (3.5, 1.3) dalam element 4")],
    "recall_title": ("Recall from Heat Transfer", "Ingat semula Heat Transfer"),
}

OUTCOMES = [
    ("Derive the plane-stress equilibrium equations from a differential element and write them as [∂]{σ}ᵀ = −{f}.",
     "Menerbitkan equilibrium equation plane stress daripada differential element dan menulisnya sebagai [∂]{σ}ᵀ = −{f}."),
    ("State the plane-stress constitutive law {σ}ᵀ = [E]{ε}ᵀ and the strain–displacement relation {ε}ᵀ = [∂]ᵀ{u}ᵀ, contrast plane stress with plane strain, and combine them into [∂][E][∂]ᵀ{u}ᵀ = −{f}.",
     "Menyatakan constitutive law plane stress {σ}ᵀ = [E]{ε}ᵀ dan hubungan strain–displacement {ε}ᵀ = [∂]ᵀ{u}ᵀ, membezakan plane stress dengan plane strain, dan menggabungkannya menjadi [∂][E][∂]ᵀ{u}ᵀ = −{f}."),
    ("Classify traction (natural) and displacement (essential) boundary conditions in each direction and write them for a rectangular domain.",
     "Mengelaskan boundary condition traction (natural) dan displacement (essential) dalam setiap arah dan menulisnya untuk rectangular domain."),
    ("Write the 2 × 8 shape-function matrix [N] of the four-node element, number its degrees of freedom, and interpolate u and v at any point.",
     "Menulis shape-function matrix [N] 2 × 8 bagi four-node element, menomborkan degree of freedom-nya, dan interpolate u dan v pada mana-mana titik."),
]

CANDO = [
    ("Decide plane stress, plane strain or neither for a structure, and say which quantity is zero.", "Menentukan plane stress, plane strain atau bukan kedua-duanya bagi sesuatu struktur, dan menyatakan kuantiti yang sifar."),
    ("Write [E] for plane stress and for plane strain from E and ν, and check the shear entry against G.", "Menulis [E] untuk plane stress dan plane strain daripada E dan ν, dan menyemak entri shear dengan G."),
    ("Label every edge of a plate in x and in y: essential or natural, the equation, and what FEM does with it.", "Melabel setiap tepi plat dalam arah x dan y: essential atau natural, persamaannya, dan apa yang FEM buat dengannya."),
    ("Number the dofs of a mesh and interpolate u and v at a point from the nodal displacements.", "Menomborkan dof bagi satu mesh dan interpolate u dan v pada satu titik daripada nodal displacement."),
]

CREDIT_BRACKET = "Images: PyMAPDL documentation, “Static analysis of a corner bracket” (adapted from the classic Ansys APDL tutorial), © ANSYS, Inc., MIT licence."
CREDIT_2D3D = ("3D beam: H. P. Langtangen and A. Logg, <i>Solving PDEs in Python</i> (Springer, 2016), CC BY 4.0. "
               "2D spanner: SolidsPy (J. Gómez and N. Guarín-Zapata), MIT licence.")


def img(src, alt, cap_en, cap_ms, credit, width=520):
    return (f'<figure><img src="slides/img/{src}" alt="{alt}" class="figimg" style="width:min({width}px,100%)">'
            f'<figcaption>{B(cap_en, cap_ms)}<span class="credit"> {credit}</span></figcaption></figure>')


def notes(A):
    """A = Assets for eqs_w11 / figs_w11 (+ figs_w9 for the scalar–vector picture). Returns [(id, title_en, title_ms, html)]."""
    S = []

    # ---- n1 --------------------------------------------------------------
    body = (
        P("Heat transfer gave a scalar field: one temperature at every point and one unknown at every node. Plane stress gives a <i>vector</i> field: "
          "every point of a plate moves by a displacement with two components, u(x, y) along x and v(x, y) along y. From the displacements we get "
          "strains, and from the strains stresses. The finite element method solves for u and v at the nodes; strains and stresses come afterwards, by differentiation.",
          "Heat transfer memberi scalar field: satu temperature pada setiap titik dan satu unknown pada setiap node. Plane stress memberi <i>vector</i> field: "
          "setiap titik plat bergerak dengan displacement yang ada dua komponen, u(x, y) dalam arah x dan v(x, y) dalam arah y. Daripada displacement kita dapat "
          "strain, dan daripada strain kita dapat stress. Finite element method menyelesaikan u dan v pada node; strain dan stress dikira kemudian, melalui pembezaan.")
        + A.fig("fig_scalar_vector", "Left: heat transfer, one number per node. Right: plane stress, two numbers per node, u and v.",
                "Kiri: heat transfer, satu nombor setiap node. Kanan: plane stress, dua nombor setiap node, u dan v.", 560)
        + DEF("Plane stress and plane strain", "Plane stress dan plane strain",
              "Plane stress: the body is thin (thickness t small) and loaded only in its own plane, so its faces are free: σ<sub>zz</sub> = σ<sub>xz</sub> = σ<sub>yz</sub> = 0, while the plate may thin or thicken (ε<sub>zz</sub> ≠ 0). "
              "Plane strain: the body is long in z and every section is loaded alike, so each slice is held by its neighbours: ε<sub>zz</sub> = 0, and a stress σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) develops to keep it so.",
              "Plane stress: badan itu nipis (ketebalan t kecil) dan dibebankan hanya dalam satahnya sendiri, jadi mukanya bebas: σ<sub>zz</sub> = σ<sub>xz</sub> = σ<sub>yz</sub> = 0, manakala plat boleh menipis atau menebal (ε<sub>zz</sub> ≠ 0). "
              "Plane strain: badan itu panjang dalam arah z dan setiap keratan dibebankan sama, jadi setiap kepingan ditahan oleh jirannya: ε<sub>zz</sub> = 0, dan stress σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) terbentuk untuk mengekalkannya.")
        + A.fig("fig_ps_vs_pe", "Plane stress (thin plate, free faces) and plane strain (long body, every slice alike).",
                "Plane stress (plat nipis, muka bebas) dan plane strain (badan panjang, setiap kepingan sama).", 620)
        + H3("Where civil engineers use each", "Di mana jurutera awam menggunakan setiap satu")
        + SB('<div class="tbl"><table><tr><th>' + B("Plane stress", "Plane stress") + '</th><th>' + B("Plane strain", "Plane strain") + '</th></tr>'
             + '<tr><td>' + B("shear walls, deep beams", "shear wall, deep beam") + '</td><td>' + B("gravity dams, long embankments", "empangan graviti, tambak panjang") + '</td></tr>'
             + '<tr><td>' + B("gusset and connection plates", "gusset plate dan connection plate") + '</td><td>' + B("tunnel linings, pipes, culverts", "tunnel lining, paip, pembetung") + '</td></tr>'
             + '<tr><td>' + B("webs of plate girders", "web bagi plate girder") + '</td><td>' + B("retaining walls, per metre run", "dinding penahan, per meter panjang") + '</td></tr>'
             + '<tr><td>' + B("slabs loaded in their own plane", "slab yang dibebankan dalam satahnya sendiri") + '</td><td>' + B("strip footings", "strip footing") + '</td></tr></table></div>'
             + P("A slab carrying a floor load is neither: the load acts normal to its plane, so it bends as a plate, a different problem. The test for plane stress is always the same two questions: is the body thin compared with its in-plane size, and do the loads act in its plane?",
                 "Slab yang menanggung beban lantai bukan kedua-duanya: beban bertindak normal kepada satahnya, jadi ia melentur sebagai plate, masalah yang berbeza. Ujian untuk plane stress sentiasa dua soalan yang sama: adakah badan itu nipis berbanding saiz dalam satahnya, dan adakah beban bertindak dalam satahnya?"))
        + '<div class="figrow">'
        + img("w11_bracket_mesh.png", "Two-dimensional quadrilateral mesh of an L-shaped corner bracket with two pin holes",
              "A corner bracket meshed in 2D, “because the bracket is thin compared to its x and y dimensions, and the load acts only in the x–y plane”: the two plane-stress questions, answered.",
              "Corner bracket di-mesh dalam 2D, “kerana bracket itu nipis berbanding dimensi x dan y, dan beban bertindak hanya dalam satah x–y”: dua soalan plane stress, dijawab.", "", 300)
        + img("w11_bracket_vm.png", "Von Mises stress on the corner bracket, highest around the constrained pin hole",
              "Its von Mises stress, highest next to the held pin hole. Part 3 explains how such a plot is computed and read.",
              "Von Mises stress-nya, paling tinggi bersebelahan lubang pin yang ditahan. Part 3 menerangkan cara plot sebegini dikira dan dibaca.", CREDIT_BRACKET, 330)
        + '</div>'
        + H3("What the finite element model solves for", "Apa yang diselesaikan oleh model finite element")
        + SB('<div class="tbl"><table><tr><th></th><th>' + B("Heat transfer", "Heat transfer") + '</th><th>' + B("Plane stress", "Plane stress") + '</th></tr>'
             + '<tr><td>' + B("primary field", "primary field") + '</td><td>T (scalar)</td><td>u, v (vector)</td></tr>'
             + '<tr><td>' + B("derived field", "derived field") + '</td><td>flux q<sub>x</sub>, q<sub>y</sub></td><td>strains ε, stresses σ</td></tr>'
             + '<tr><td>' + B("material law", "material law") + '</td><td>Fourier: q = −k∇T</td><td>Hooke: {σ} = [E]{ε}</td></tr>'
             + '<tr><td>' + B("dofs per node", "dof setiap node") + '</td><td>1</td><td>2</td></tr>'
             + '<tr><td>4-node [k]</td><td>4 × 4</td><td>8 × 8</td></tr></table></div>')
        + NOTE("Displacement-based FEM", "FEM berasaskan displacement",
               "We solve for u and v and differentiate them to get strains and stresses. Each differentiation costs accuracy, so stresses are always less accurate than displacements, and they jump between elements. Part 3 is about exactly that.",
               "Kita selesaikan u dan v dan bezakannya untuk mendapatkan strain dan stress. Setiap pembezaan mengurangkan ketepatan, jadi stress sentiasa kurang tepat berbanding displacement, dan ia melompat antara element. Part 3 membincangkan perkara itu.")
        + KP([("Plane stress: thin, loaded in plane, σ<sub>zz</sub> = 0. Plane strain: long, uniform section, ε<sub>zz</sub> = 0.", "Plane stress: nipis, dibebankan dalam satah, σ<sub>zz</sub> = 0. Plane strain: panjang, keratan seragam, ε<sub>zz</sub> = 0."),
              ("Two unknowns per node, u and v; a 4-node element has 8 dofs and an 8 × 8 [k].", "Dua unknown setiap node, u dan v; 4-node element ada 8 dof dan [k] 8 × 8."),
              ("Strains and stresses come from derivatives of the displacements: less accurate.", "Strain dan stress diperoleh daripada derivative displacement: kurang tepat.")])
        + QC("q1", "A concrete gravity dam 300 m long carries water pressure that is the same at every section. Which idealisation, and which quantity is zero?",
             "Empangan graviti konkrit sepanjang 300 m menanggung tekanan air yang sama pada setiap keratan. Idealisation yang mana, dan kuantiti apa yang sifar?",
             [("a", "Plane stress; σ<sub>zz</sub> = 0", "Plane stress; σ<sub>zz</sub> = 0"), ("b", "Plane strain; ε<sub>zz</sub> = 0", "Plane strain; ε<sub>zz</sub> = 0"), ("c", "Neither: it is a plate in bending", "Bukan kedua-duanya: ia plate yang melentur")],
             "b", "The dam is long and every section is loaded alike, so each slice is held by its neighbours and cannot strain along the axis: ε<sub>zz</sub> = 0. A stress σ<sub>zz</sub> develops instead.",
             "Empangan itu panjang dan setiap keratan dibebankan sama, jadi setiap kepingan ditahan oleh jirannya dan tidak boleh ber-strain di sepanjang paksinya: ε<sub>zz</sub> = 0. Sebaliknya stress σ<sub>zz</sub> terbentuk.")
    )
    S.append(("n1", "Why plane stress: two unknowns at every point", "Mengapa plane stress: dua unknown pada setiap titik", body))

    # ---- n2 --------------------------------------------------------------
    body = (
        P("Take a small rectangle dx by dy of unit thickness inside the plate. On its faces act the normal stresses σ<sub>xx</sub> and σ<sub>yy</sub> and the shear stresses σ<sub>xy</sub> and σ<sub>yx</sub> (N m<sup>−2</sup>); "
          "inside acts a body force f<sub>x</sub>, f<sub>y</sub> per unit volume (N m<sup>−3</sup>), for example self-weight f<sub>y</sub> = −ρg. "
          "The method is the one used for the heat flux in Heat Transfer Part 1: the stress on a far face is the near-face stress plus its first-order change.",
          "Ambil satu segi empat kecil dx × dy dengan ketebalan unit di dalam plat. Pada mukanya bertindak normal stress σ<sub>xx</sub> dan σ<sub>yy</sub> serta shear stress σ<sub>xy</sub> dan σ<sub>yx</sub> (N m<sup>−2</sup>); "
          "di dalamnya bertindak body force f<sub>x</sub>, f<sub>y</sub> per unit isi padu (N m<sup>−3</sup>), contohnya berat sendiri f<sub>y</sub> = −ρg. "
          "Kaedahnya sama seperti heat flux dalam Heat Transfer Part 1: stress pada muka jauh ialah stress muka dekat ditambah perubahan first-order-nya.")
        + A.fig("fig_ps_diffelem", "The differential element: normal and shear stresses on the faces, body force inside (text Fig. 3.1).",
                "Differential element: normal stress dan shear stress pada muka, body force di dalam (teks Rajah 3.1).", 520)
        + NOTE("Sign convention", "Konvensyen tanda",
               "A stress component is positive when it acts in the positive coordinate direction on a face whose outward normal points in a positive direction, and in the negative direction on a face whose outward normal is negative.",
               "Satu komponen stress positif apabila ia bertindak dalam arah koordinat positif pada muka yang outward normal-nya menghala ke arah positif, dan dalam arah negatif pada muka yang outward normal-nya negatif.")
        + H3("Force balance in x", "Keseimbangan daya dalam arah x")
        + SB(P("Static equilibrium requires the forces in x and in y to sum to zero. Forces are stresses times face areas: σ<sub>xx</sub> acts on the faces of area dy, σ<sub>yx</sub> on the faces of area dx (each times the unit thickness):",
               "Static equilibrium memerlukan jumlah daya dalam arah x dan y bersamaan sifar. Daya ialah stress didarab luas muka: σ<sub>xx</sub> bertindak pada muka seluas dy, σ<sub>yx</sub> pada muka seluas dx (setiap satu didarab ketebalan unit):"))
        + A.eq("p_sumF", "(3.1), (3.2)") + A.eq("p_eqx_full", "(3.3)")
        + SB(P("The near-face terms cancel against the first part of the far-face terms, every remaining term carries dx dy, and dividing by it leaves the first equilibrium equation:",
               "Term muka dekat terbatal dengan bahagian pertama term muka jauh, setiap term yang tinggal membawa dx dy, dan membahagi dengannya meninggalkan equilibrium equation pertama:"))
        + A.eq("p_eqx", "(3.4)")
        + OK("Unit check", "Semakan unit", "A stress gradient is (N m<sup>−2</sup>)/m = N m<sup>−3</sup>, a force per unit volume, the same as the body force.",
             "Stress gradient ialah (N m<sup>−2</sup>)/m = N m<sup>−3</sup>, daya per unit isi padu, sama dengan body force.")
        + H3("Force balance in y (Activity 2)", "Keseimbangan daya dalam arah y (Aktiviti 2)")
        + SB(P("In y, σ<sub>yy</sub> acts on the faces of area dx and σ<sub>xy</sub> on the faces of area dy. The same expansion gives",
               "Dalam arah y, σ<sub>yy</sub> bertindak pada muka seluas dx dan σ<sub>xy</sub> pada muka seluas dy. Pengembangan yang sama memberi"))
        + A.eq("p_eqy_full", "(3.5)") + A.eq("p_eqy", "(3.6)")
        + NOTE("Why σ<sub>yx</sub> = σ<sub>xy</sub>", "Mengapa σ<sub>yx</sub> = σ<sub>xy</sub>",
               "Take moments about the centre of the element: the pair σ<sub>xy</sub> dy on the x-faces and the pair σ<sub>yx</sub> dx on the y-faces each make a couple with arm dx or dy. Equilibrium of moments makes the two couples equal, σ<sub>xy</sub> dy dx = σ<sub>yx</sub> dx dy, so the shear stresses are equal. Only three stress components remain.",
               "Ambil momen terhadap pusat element: pasangan σ<sub>xy</sub> dy pada muka-x dan pasangan σ<sub>yx</sub> dx pada muka-y masing-masing membentuk couple dengan lengan dx atau dy. Keseimbangan momen menjadikan dua couple itu sama, σ<sub>xy</sub> dy dx = σ<sub>yx</sub> dx dy, jadi shear stress itu sama. Hanya tiga komponen stress tinggal.")
        + H3("The matrix form", "Bentuk matrix")
        + SB(P("Collect the two equations with a 2 × 3 matrix of derivative operators acting on the stress vector {σ<sub>xx</sub> σ<sub>yy</sub> σ<sub>xy</sub>}ᵀ. "
               "This is the plane-stress version of {∂}{q} in heat transfer: there a 1 × 2 row acted on a 2 × 1 flux; here a 2 × 3 matrix acts on a 3 × 1 stress.",
               "Kumpulkan dua persamaan itu dengan matrix 2 × 3 bagi derivative operator yang bertindak ke atas stress vector {σ<sub>xx</sub> σ<sub>yy</sub> σ<sub>xy</sub>}ᵀ. "
               "Ini versi plane stress bagi {∂}{q} dalam heat transfer: di sana satu baris 1 × 2 bertindak ke atas flux 2 × 1; di sini matrix 2 × 3 bertindak ke atas stress 3 × 1."))
        + A.eq("p_matrix", "(3.8)") + A.eq("p_compact", "(3.9)") + A.eq("p_dop")
        + STEP("Worked step · Activity 2 in words", "Langkah bekerja · Aktiviti 2 dalam ayat",
               P("Forces in y: σ<sub>yy</sub> on the bottom face (area dx) acts downward, σ<sub>yy</sub> + ∂σ<sub>yy</sub>/∂y dy on the top face acts upward; σ<sub>xy</sub> on the left face (area dy) acts downward, σ<sub>xy</sub> + ∂σ<sub>xy</sub>/∂x dx on the right face acts upward; f<sub>y</sub> dx dy acts on the volume. "
                 "Sum, cancel, divide by dx dy: ∂σ<sub>xy</sub>/∂x + ∂σ<sub>yy</sub>/∂y + f<sub>y</sub> = 0. Row 2 of [∂] is therefore [0 ∂/∂y ∂/∂x].",
                 "Daya dalam arah y: σ<sub>yy</sub> pada muka bawah (luas dx) bertindak ke bawah, σ<sub>yy</sub> + ∂σ<sub>yy</sub>/∂y dy pada muka atas bertindak ke atas; σ<sub>xy</sub> pada muka kiri (luas dy) bertindak ke bawah, σ<sub>xy</sub> + ∂σ<sub>xy</sub>/∂x dx pada muka kanan bertindak ke atas; f<sub>y</sub> dx dy bertindak pada isi padu. "
                 "Jumlahkan, batalkan, bahagi dengan dx dy: ∂σ<sub>xy</sub>/∂x + ∂σ<sub>yy</sub>/∂y + f<sub>y</sub> = 0. Jadi baris 2 bagi [∂] ialah [0 ∂/∂y ∂/∂x]."))
        + KP([("Force balance in x and y on dx × dy gives (3.4) and (3.6); moment balance gives σ<sub>yx</sub> = σ<sub>xy</sub>.", "Keseimbangan daya dalam x dan y pada dx × dy memberi (3.4) dan (3.6); keseimbangan momen memberi σ<sub>yx</sub> = σ<sub>xy</sub>."),
              ("Matrix form [∂]{σ}ᵀ = −{f} with the 2 × 3 operator [∂].", "Bentuk matrix [∂]{σ}ᵀ = −{f} dengan operator [∂] 2 × 3."),
              ("Every term is a force per unit volume, N m<sup>−3</sup>.", "Setiap term ialah daya per unit isi padu, N m<sup>−3</sup>.")])
        + QC("q2", "What is the size of the operator matrix [∂] in [∂]{σ}ᵀ = −{f}?", "Apakah saiz operator matrix [∂] dalam [∂]{σ}ᵀ = −{f}?",
             [("a", "2 × 3: two equations, three stress components", "2 × 3: dua persamaan, tiga komponen stress"), ("b", "3 × 2: three stresses, two displacements", "3 × 2: tiga stress, dua displacement"), ("c", "1 × 2, as in heat transfer", "1 × 2, seperti dalam heat transfer")],
             "a", "Two equilibrium equations (x and y) act on the three stress components σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub>. Its transpose, 3 × 2, appears in the strain–displacement relation (§4).",
             "Dua equilibrium equation (x dan y) bertindak ke atas tiga komponen stress σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub>. Transpose-nya, 3 × 2, muncul dalam hubungan strain–displacement (§4).")
    )
    S.append(("n2", "Equilibrium of a differential element", "Equilibrium bagi differential element", body))

    # ---- n3 --------------------------------------------------------------
    body = (
        P("Equilibrium gives two equations in three unknown stresses. Hooke’s law, the analogue of Fourier’s law, relates the stresses to the strains through the material. For plane stress (σ<sub>zz</sub> = 0) it reads",
          "Equilibrium memberi dua persamaan dalam tiga stress yang tidak diketahui. Hooke’s law, analog bagi Fourier’s law, menghubungkan stress dengan strain melalui bahan. Untuk plane stress (σ<sub>zz</sub> = 0) ia berbunyi")
        + A.eq("p_hooke", "(3.10)")
        + SB(P("or, with the 3 × 3 constitutive matrix [E],", "atau, dengan constitutive matrix [E] 3 × 3,"))
        + A.eq("p_E", "(3.11), (3.12)")
        + DEF("Engineering shear strain", "Engineering shear strain",
              "The text’s ε<sub>xy</sub> is the engineering shear strain, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x (written γ<sub>xy</sub> in most solid-mechanics books), not the tensor strain, which is half of it. The (3,3) entry of [E] is built for it: (E/(1 − ν²))·(1 − ν)/2 = E/(2(1 + ν)) = G, the shear modulus.",
              "ε<sub>xy</sub> dalam teks ialah engineering shear strain, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x (ditulis γ<sub>xy</sub> dalam kebanyakan buku mekanik pepejal), bukan tensor strain, yang separuh daripadanya. Entri (3,3) bagi [E] dibina untuknya: (E/(1 − ν²))·(1 − ν)/2 = E/(2(1 + ν)) = G, iaitu shear modulus.")
        + H3("The cantilever’s material (Activity 3)", "Bahan cantilever (Aktiviti 3)")
        + SB(P("For the text’s cantilever, E = 200 × 10⁶ N m<sup>−2</sup> and ν = 0.33. Keep four significant figures: Part 2 builds [k] from these numbers.",
               "Untuk cantilever dalam teks, E = 200 × 10⁶ N m<sup>−2</sup> dan ν = 0.33. Simpan empat angka bererti: Part 2 membina [k] daripada nombor ini."))
        + A.eq("p_act3") + A.eq("p_act3_E")
        + OK("Check", "Semakan", "G = E/(2(1 + ν)) = 200 × 10⁶/2.66 = 75.19 × 10⁶ N m<sup>−2</sup>, equal to the (3,3) entry. If your (3,3) entry is twice this, you used (1 − ν) instead of (1 − ν)/2.",
             "G = E/(2(1 + ν)) = 200 × 10⁶/2.66 = 75.19 × 10⁶ N m<sup>−2</sup>, sama dengan entri (3,3). Jika entri (3,3) anda dua kali ganda nilai ini, anda telah guna (1 − ν) dan bukan (1 − ν)/2.")
        + H3("Plane strain changes only [E]", "Plane strain hanya mengubah [E]")
        + SB(P("Setting ε<sub>zz</sub> = 0 instead of σ<sub>zz</sub> = 0 in three-dimensional Hooke’s law gives a matrix with the same shape and different constants:",
               "Menetapkan ε<sub>zz</sub> = 0 dan bukan σ<sub>zz</sub> = 0 dalam Hooke’s law tiga dimensi memberi matrix dengan bentuk yang sama tetapi pemalar yang berbeza:"))
        + A.eq("p_Estrain")
        + SB(P("The shear entry is G in both. The normal entries are larger in plane strain, because a slice that cannot thin resists in-plane stretching more. "
               "For ν = 0.33 the bending stiffness of the cantilever rises by the factor 1/(1 − ν²) = 1.12, so its tip deflection falls to about 0.89 of the plane-stress value; the Explorer shows 0.90 on a fine mesh. "
               "As ν approaches 0.5 (rubber, undrained clay) the plane-strain constants grow without bound: the material becomes incompressible, a topic for later courses.",
               "Entri shear ialah G dalam kedua-duanya. Entri normal lebih besar dalam plane strain, kerana kepingan yang tidak boleh menipis lebih menahan regangan dalam satah. "
               "Untuk ν = 0.33, bending stiffness cantilever meningkat dengan faktor 1/(1 − ν²) = 1.12, jadi tip deflection-nya turun kepada kira-kira 0.89 daripada nilai plane stress; Explorer menunjukkan 0.90 pada mesh halus. "
               "Apabila ν menghampiri 0.5 (getah, undrained clay), pemalar plane strain membesar tanpa had: bahan itu menjadi incompressible, topik untuk kursus kemudian."))
        + NOTE("In this course", "Dalam kursus ini", "We formulate and calculate by hand in plane stress (text Chapter 3). Plane strain is the same [k] with the other [E]: one line in the code, one option in ANSYS.",
               "Kita memformulasi dan mengira dengan tangan dalam plane stress (teks Bab 3). Plane strain ialah [k] yang sama dengan [E] yang lain: satu baris dalam kod, satu pilihan dalam ANSYS.")
        + KP([("{σ}ᵀ = [E]{ε}ᵀ; plane stress [E] = E/(1 − ν²)·[1 ν 0; ν 1 0; 0 0 (1 − ν)/2].", "{σ}ᵀ = [E]{ε}ᵀ; plane stress [E] = E/(1 − ν²)·[1 ν 0; ν 1 0; 0 0 (1 − ν)/2]."),
              ("ε<sub>xy</sub> is the engineering shear strain; the (3,3) entry equals G.", "ε<sub>xy</sub> ialah engineering shear strain; entri (3,3) sama dengan G."),
              ("Plane strain: only [E] changes; stiffer in the normal entries, same G.", "Plane strain: hanya [E] berubah; lebih kaku dalam entri normal, G sama.")])
        + QC("q3", "For E = 200 × 10⁶ N m<sup>−2</sup> and ν = 0.33, which value is the (3,3) entry of the plane-stress [E]?", "Untuk E = 200 × 10⁶ N m<sup>−2</sup> dan ν = 0.33, nilai manakah entri (3,3) bagi [E] plane stress?",
             [("a", "150.4 × 10⁶ N m<sup>−2</sup>", "150.4 × 10⁶ N m<sup>−2</sup>"), ("b", "75.19 × 10⁶ N m<sup>−2</sup>", "75.19 × 10⁶ N m<sup>−2</sup>"), ("c", "74.07 × 10⁶ N m<sup>−2</sup>", "74.07 × 10⁶ N m<sup>−2</sup>")],
             "b", "(1 − ν)/2 × E/(1 − ν²) = 0.335 × 224.44 × 10⁶ = 75.19 × 10⁶ = G. Option (a) forgets the half; (c) is the (1,2) entry, ν E/(1 − ν²).",
             "(1 − ν)/2 × E/(1 − ν²) = 0.335 × 224.44 × 10⁶ = 75.19 × 10⁶ = G. Pilihan (a) terlupa separuh; (c) ialah entri (1,2), ν E/(1 − ν²).")
    )
    S.append(("n3", "Hooke’s law: plane stress and plane strain", "Hooke’s law: plane stress dan plane strain", body))

    # ---- n4 --------------------------------------------------------------
    body = (
        P("Heat transfer had no step like this one, because T was itself the unknown. Here the unknowns are displacements, and the strains are their derivatives: ε<sub>xx</sub> measures stretching along x, ε<sub>yy</sub> along y, and ε<sub>xy</sub> the change of a right angle.",
          "Heat transfer tiada langkah seperti ini, kerana T sendiri ialah unknown. Di sini unknown ialah displacement, dan strain ialah derivative-nya: ε<sub>xx</sub> mengukur regangan dalam arah x, ε<sub>yy</sub> dalam arah y, dan ε<sub>xy</sub> perubahan sudut tegak.")
        + A.fig("fig_strain", "The three strains: stretching along x and along y, and the shear that closes a right angle by ∂u/∂y + ∂v/∂x.",
                "Tiga strain: regangan dalam arah x dan y, dan shear yang menutup sudut tegak sebanyak ∂u/∂y + ∂v/∂x.", 560)
        + A.eq("p_strain", "(3.13)")
        + SB(P("In matrix form the 3 × 2 operator is exactly the transpose of the equilibrium operator [∂]. That is not a coincidence: equilibrium and compatibility are dual, and it is why the final matrix [k] comes out symmetric.",
               "Dalam bentuk matrix, operator 3 × 2 itu tepat transpose bagi equilibrium operator [∂]. Itu bukan kebetulan: equilibrium dan compatibility adalah dual, dan itulah sebab matrix akhir [k] keluar simetri."))
        + A.eq("p_strain_matrix", "(3.14), (3.15)")
        + NOTE("The factor that loses marks", "Faktor yang menghilangkan markah",
               "ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x, the sum of the two slopes. Halving it, or using the tensor shear strain with the text’s [E], halves the shear stress.",
               "ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x, hasil tambah dua cerun. Membahagi dua nilainya, atau menggunakan tensor shear strain dengan [E] dalam teks, menjadikan shear stress separuh.")
        + H3("Assemble the PDE", "Bina PDE")
        + SB(P("Substitute the strains into Hooke’s law and Hooke’s law into equilibrium. The result is two PDEs in the two displacements, written once with the three matrices:",
               "Gantikan strain ke dalam Hooke’s law dan Hooke’s law ke dalam equilibrium. Hasilnya dua PDE dalam dua displacement, ditulis sekali dengan tiga matrix:"))
        + A.eq("p_sigma_u", "(3.16)") + A.eq("p_pde", "(3.17)")
        + SB(P("Read (3.17) from the inside out: [∂]ᵀ{u}ᵀ turns displacements into strains (3 × 1); [E] turns strains into stresses (3 × 1); [∂] turns stresses into the two equilibrium equations, balanced by the body force. Compare it with the heat PDE:",
               "Baca (3.17) dari dalam ke luar: [∂]ᵀ{u}ᵀ menukar displacement kepada strain (3 × 1); [E] menukar strain kepada stress (3 × 1); [∂] menukar stress kepada dua equilibrium equation, diimbangi oleh body force. Bandingkan dengan PDE heat:"))
        + A.eq("p_compare")
        + OK("Same pattern, bigger matrices", "Pola yang sama, matrix lebih besar",
             "Part 2 does with (3.17) exactly what Heat Transfer Part 2 did with (2.13): substitute {u}ᵀ = [N]{û}ᵀ, weight with [N]ᵀ (Galerkin), integrate by parts. The boundary term that appears is the traction of §5.",
             "Part 2 membuat dengan (3.17) tepat apa yang Heat Transfer Part 2 buat dengan (2.13): gantikan {u}ᵀ = [N]{û}ᵀ, beri weight dengan [N]ᵀ (Galerkin), integrate by parts. Boundary term yang muncul ialah traction dalam §5.")
        + KP([("{ε}ᵀ = [∂]ᵀ{u}ᵀ: ε<sub>xx</sub> = ∂u/∂x, ε<sub>yy</sub> = ∂v/∂y, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x.", "{ε}ᵀ = [∂]ᵀ{u}ᵀ: ε<sub>xx</sub> = ∂u/∂x, ε<sub>yy</sub> = ∂v/∂y, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x."),
              ("The strain operator is the transpose of the equilibrium operator.", "Strain operator ialah transpose bagi equilibrium operator."),
              ("[∂][E][∂]ᵀ{u}ᵀ = −{f}: two PDEs in u and v, the analogue of {∂}[E]{∂}ᵀT = −q<sub>h</sub>.", "[∂][E][∂]ᵀ{u}ᵀ = −{f}: dua PDE dalam u dan v, analog bagi {∂}[E]{∂}ᵀT = −q<sub>h</sub>.")])
        + QC("q4", "A displacement field is u = 0.002y, v = 0. Which strains does it produce?", "Satu displacement field ialah u = 0.002y, v = 0. Strain apa yang dihasilkan?",
             [("a", "ε<sub>xx</sub> = 0.002, the others zero", "ε<sub>xx</sub> = 0.002, yang lain sifar"), ("b", "ε<sub>xy</sub> = 0.002, the others zero", "ε<sub>xy</sub> = 0.002, yang lain sifar"), ("c", "ε<sub>xy</sub> = 0.001, the others zero", "ε<sub>xy</sub> = 0.001, yang lain sifar")],
             "b", "ε<sub>xx</sub> = ∂u/∂x = 0, ε<sub>yy</sub> = ∂v/∂y = 0, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x = 0.002 + 0. This is simple shear; 0.001 would be the tensor strain, which the text’s [E] does not use.",
             "ε<sub>xx</sub> = ∂u/∂x = 0, ε<sub>yy</sub> = ∂v/∂y = 0, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x = 0.002 + 0. Ini simple shear; 0.001 ialah tensor strain, yang tidak digunakan oleh [E] dalam teks.")
    )
    S.append(("n4", "Strain–displacement, and the PDE in u and v", "Strain–displacement, dan PDE dalam u dan v", body))

    # ---- n5 --------------------------------------------------------------
    body = (
        P("Every point of the boundary needs one condition in x and one in y. In each direction either the force on the boundary is known or the displacement is: never both, never neither.",
          "Setiap titik pada sempadan memerlukan satu condition dalam arah x dan satu dalam arah y. Dalam setiap arah sama ada daya pada sempadan diketahui atau displacement diketahui: tidak pernah kedua-duanya, tidak pernah tiada.")
        + DEF("Traction · natural", "Traction · natural",
              "The traction {b<sub>x</sub>, b<sub>y</sub>} is the force per unit area acting on the boundary (per unit thickness: force per unit length). With the outward normal (n<sub>x</sub>, n<sub>y</sub>) it is related to the stresses by (3.18)–(3.19). A free edge has b<sub>x</sub> = b<sub>y</sub> = 0.",
              "Traction {b<sub>x</sub>, b<sub>y</sub>} ialah daya per unit luas yang bertindak pada sempadan (per unit ketebalan: daya per unit panjang). Dengan outward normal (n<sub>x</sub>, n<sub>y</sub>) ia dihubungkan dengan stress melalui (3.18)–(3.19). Tepi bebas ada b<sub>x</sub> = b<sub>y</sub> = 0.")
        + A.eq("p_bx", "(3.18a), (3.19a)")
        + SB(P("On a rectangle the normals are (±1, 0) on the vertical edges and (0, ±1) on the horizontal ones, so only two stresses act as tractions on each edge:",
               "Pada segi empat tepat, normal ialah (±1, 0) pada tepi menegak dan (0, ±1) pada tepi mendatar, jadi hanya dua stress bertindak sebagai traction pada setiap tepi:"))
        + A.eq("p_rect_v", "(3.20)") + A.eq("p_rect_h", "(3.21)")
        + DEF("Displacement · essential", "Displacement · essential",
              "A known displacement: a fixed support ū = v̄ = 0, a roller one of them, a settlement a non-zero value.",
              "Displacement yang diketahui: fixed support ū = v̄ = 0, roller salah satu daripadanya, settlement nilai bukan sifar.")
        + A.eq("p_dirichlet", "(3.22), (3.23)")
        + H3("What FEM does with each kind", "Apa yang FEM buat dengan setiap jenis")
        + SB('<div class="tbl"><table><tr><th>' + B("Condition", "Condition") + '</th><th>' + B("Known", "Diketahui") + '</th><th>' + B("In the FEM", "Dalam FEM") + '</th><th>' + B("Heat analogue", "Analog heat") + '</th></tr>'
             + '<tr><td>' + B("displacement · essential", "displacement · essential") + '</td><td>ū, v̄</td><td>' + B("imposed on the assembled system (row–column elimination)", "dikenakan pada assembled system (row–column elimination)") + '</td><td>T̄</td></tr>'
             + '<tr><td>' + B("traction · natural", "traction · natural") + '</td><td>b<sub>x</sub>, b<sub>y</sub></td><td>' + B("equivalent nodal loads {b} from the boundary integral", "equivalent nodal load {b} daripada boundary integral") + '</td><td>' + B("flux load", "flux load") + '</td></tr>'
             + '<tr><td>' + B("free edge · natural, b = 0", "tepi bebas · natural, b = 0") + '</td><td>' + B("nothing acts", "tiada yang bertindak") + '</td><td>' + B("nothing to do", "tiada tindakan") + '</td><td>' + B("insulated edge", "tepi insulated") + '</td></tr>'
             + '<tr><td>' + B("body force", "body force") + '</td><td>f<sub>x</sub>, f<sub>y</sub></td><td>' + B("equivalent nodal loads {q}, e.g. self-weight", "equivalent nodal load {q}, contohnya berat sendiri") + '</td><td>' + B("heat generation", "heat generation") + '</td></tr></table></div>')
        + NOTE("Count per direction, not per edge", "Kira mengikut arah, bukan mengikut tepi",
               "A roller edge is essential in one direction and natural in the other. A free edge is not a support and not a load: it is the do-nothing condition, exactly like an insulated edge. Adding a support where none exists is the commonest wrong model in ANSYS.",
               "Tepi roller adalah essential dalam satu arah dan natural dalam arah yang lain. Tepi bebas bukan support dan bukan beban: ia condition tanpa tindakan, sama seperti tepi insulated. Menambah support yang tidak wujud ialah model salah yang paling kerap dalam ANSYS.")
        + H3("The cantilever (Activity 4)", "Cantilever (Aktiviti 4)")
        + A.fig("fig_cantilever", "The text’s cantilever: 4 m × 2 m, t = 0.01 m, fixed on the left, 5 kN m<sup>−1</sup> downward on the right.",
                "Cantilever dalam teks: 4 m × 2 m, t = 0.01 m, fixed di kiri, 5 kN m<sup>−1</sup> ke bawah di kanan.", 560)
        + SB('<div class="tbl"><table><tr><th>' + B("Edge", "Tepi") + '</th><th>x</th><th>y</th><th>' + B("FEM action", "Tindakan FEM") + '</th></tr>'
             + '<tr><td>' + B("left, x = 0", "kiri, x = 0") + '</td><td>ū = 0, essential</td><td>v̄ = 0, essential</td><td>' + B("impose U<sub>1</sub>, U<sub>2</sub>, U<sub>7</sub>, U<sub>8</sub>, U<sub>13</sub>, U<sub>14</sub> = 0", "kenakan U<sub>1</sub>, U<sub>2</sub>, U<sub>7</sub>, U<sub>8</sub>, U<sub>13</sub>, U<sub>14</sub> = 0") + '</td></tr>'
             + '<tr><td>' + B("right, x = 4", "kanan, x = 4") + '</td><td>b<sub>x</sub> = σ<sub>xx</sub> = 0</td><td>b<sub>y</sub> = σ<sub>xy</sub>, ' + B("downward", "ke bawah") + '</td><td>' + B("nodal loads from the traction", "nodal load daripada traction") + '</td></tr>'
             + '<tr><td>' + B("top, bottom", "atas, bawah") + '</td><td>b<sub>x</sub> = 0</td><td>b<sub>y</sub> = 0</td><td>' + B("nothing", "tiada") + '</td></tr></table></div>')
        + A.fig("fig_ps_mesh", "The 2 × 2 mesh: node n owns dofs U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y); 18 dofs, 6 known, 12 unknown.",
                "Mesh 2 × 2: node n memiliki dof U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y); 18 dof, 6 diketahui, 12 tidak diketahui.", 420)
        + H3("Why the supports must stop every rigid motion", "Mengapa support mesti menghalang setiap rigid motion")
        + SB(P("A plate can translate in x, translate in y and rotate in its plane without straining at all: for a small rotation θ, u = −θy and v = θx give ε<sub>xx</sub> = ε<sub>yy</sub> = 0 and ε<sub>xy</sub> = −θ + θ = 0. "
               "Such a motion needs no force, so [K] is singular until the supports remove all three. Holding v alone along the left edge stops the y-translation but not the x-translation, nor a rotation about a point of that edge (its points move in x, not in y); "
               "the Explorer’s “vertical only” support shows the solver refusing. Holding u alone along the edge stops x-translation and rotation but leaves the plate free to slide in y.",
               "Plat boleh translate dalam arah x, translate dalam arah y dan berputar dalam satahnya tanpa sebarang strain: untuk putaran kecil θ, u = −θy dan v = θx memberi ε<sub>xx</sub> = ε<sub>yy</sub> = 0 dan ε<sub>xy</sub> = −θ + θ = 0. "
               "Pergerakan sebegini tidak memerlukan daya, jadi [K] singular sehingga support menghapuskan ketiga-tiganya. Menahan v sahaja di sepanjang tepi kiri menghalang translation y tetapi tidak menghalang translation x, mahupun putaran terhadap satu titik pada tepi itu (titik-titiknya bergerak dalam arah x, bukan y); "
               "support “vertical only” dalam Explorer menunjukkan solver menolak. Menahan u sahaja di sepanjang tepi itu menghalang translation x dan putaran tetapi membiarkan plat bebas menggelongsor dalam arah y."))
        + KP([("Traction known → natural → load (or nothing on a free edge). Displacement known → essential → imposed.", "Traction diketahui → natural → beban (atau tiada pada tepi bebas). Displacement diketahui → essential → dikenakan."),
              ("One condition per direction at every boundary point.", "Satu condition setiap arah pada setiap titik sempadan."),
              ("Supports must remove two translations and one rotation, or [K] is singular.", "Support mesti menghapuskan dua translation dan satu putaran, jika tidak [K] singular.")])
        + QC("q5", "The top edge of the cantilever carries nothing. What does the finite element model do there?", "Tepi atas cantilever tidak menanggung apa-apa. Apa yang model finite element buat di situ?",
             [("a", "Fix v = 0, because nothing acts", "Tetapkan v = 0, kerana tiada yang bertindak"), ("b", "Nothing: b<sub>x</sub> = b<sub>y</sub> = 0 is a natural condition", "Tiada: b<sub>x</sub> = b<sub>y</sub> = 0 ialah natural condition"), ("c", "Add a small spring to keep it stable", "Tambah spring kecil supaya stabil")],
             "b", "A free edge is a natural condition with zero traction; its boundary term is zero, so it needs no action, exactly like an insulated edge. Fixing v there would add a support the structure does not have.",
             "Tepi bebas ialah natural condition dengan traction sifar; boundary term-nya sifar, jadi ia tidak memerlukan tindakan, sama seperti tepi insulated. Menetapkan v di situ menambah support yang tiada pada struktur itu.")
    )
    S.append(("n5", "Boundary conditions: traction and displacement", "Boundary condition: traction dan displacement", body))

    # ---- n6 --------------------------------------------------------------
    body = (
        P("The element is the four-node rectangle of heat transfer, with the same shape functions N<sub>1</sub>…N<sub>4</sub> of (2.21). What is new is that each node carries two degrees of freedom, so both u and v are interpolated, with the same functions:",
          "Element ialah four-node rectangle dalam heat transfer, dengan shape function N<sub>1</sub>…N<sub>4</sub> yang sama daripada (2.21). Yang baharu ialah setiap node membawa dua degree of freedom, jadi kedua-dua u dan v di-interpolate, dengan fungsi yang sama:")
        + A.fig("fig_ps_q4", "The plane-stress element: eight dofs, u along x and v along y at each node (text Fig. 3.2).",
                "Element plane stress: lapan dof, u dalam arah x dan v dalam arah y pada setiap node (teks Rajah 3.2).", 460)
        + A.eq("p_interp", "(3.24), (3.25)")
        + H3("The 2 × 8 shape-function matrix", "Shape-function matrix 2 × 8")
        + SB(P("Both interpolations are one matrix product. Row 1 picks the u-dofs and row 2 the v-dofs; the zeros say that u does not depend on any v. The 8-node element gives a 2 × 16 matrix of the same pattern (3.29).",
               "Kedua-dua interpolation ialah satu hasil darab matrix. Baris 1 memilih dof-u dan baris 2 dof-v; sifar menunjukkan bahawa u tidak bergantung pada mana-mana v. 8-node element memberi matrix 2 × 16 dengan pola yang sama (3.29)."))
        + A.eq("p_N", "(3.28)") + A.eq("p_general", "(3.30)")
        + NOTE("One ordering, everywhere", "Satu susunan, di mana-mana",
               "Node by node, u before v: {û} = {u<sub>1</sub> v<sub>1</sub> u<sub>2</sub> v<sub>2</sub> … u<sub>4</sub> v<sub>4</sub>}. In the mesh, node n owns global dofs U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y). Keep it in [N], in [B], in [k] and in the connectivity; mixing it with “all u then all v” is the classic assembly error.",
               "Node demi node, u sebelum v: {û} = {u<sub>1</sub> v<sub>1</sub> u<sub>2</sub> v<sub>2</sub> … u<sub>4</sub> v<sub>4</sub>}. Dalam mesh, node n memiliki dof global U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y). Kekalkan susunan ini dalam [N], [B], [k] dan connectivity; mencampurkannya dengan “semua u kemudian semua v” ialah kesilapan assembly yang klasik.")
        + H3("Activity 5: u and v at (3.5, 1.3) m", "Aktiviti 5: u dan v pada (3.5, 1.3) m")
        + A.fig("fig_ps_mesh_e4", "Element 4 of the solved cantilever (nodes 5, 6, 9, 8) and the point (3.5, 1.3).",
                "Element 4 bagi cantilever yang diselesaikan (node 5, 6, 9, 8) dan titik (3.5, 1.3).", 520)
        + SB(P("The point lies in element 4, whose local node 1 is global node 5 at (2, 1). Its local coordinates are (1.5, 0.3): the Activity 4 point of Heat Transfer Part 1, with the same shape functions. The nodal displacements come from the text’s solution (3.49), in local order 5, 6, 9, 8:",
               "Titik itu terletak dalam element 4, yang local node 1-nya ialah global node 5 pada (2, 1). Koordinat local-nya (1.5, 0.3): titik Aktiviti 4 dalam Heat Transfer Part 1, dengan shape function yang sama. Nodal displacement diambil daripada penyelesaian teks (3.49), dalam susunan local 5, 6, 9, 8:"))
        + A.eq("p_act5_N") + A.eq("p_act5_u")
        + SB(P("Node 6, the free-end node of the element, carries half the weight and the largest v. The plate sags by 0.11 m and hardly moves along x: bending, as expected of a cantilever (the text chose a very soft E so that the displacements are visible). At the centroid every N<sub>i</sub> = 1/4:",
               "Node 6, node hujung bebas bagi element itu, membawa separuh weight dan v yang terbesar. Plat itu melendut 0.11 m dan hampir tidak bergerak dalam arah x: lenturan, seperti yang dijangka bagi cantilever (teks memilih E yang sangat lembut supaya displacement kelihatan). Pada centroid setiap N<sub>i</sub> = 1/4:"))
        + A.eq("p_cent")
        + H3("What comes next", "Apa seterusnya")
        + SB(P("Differentiating u and v gives the strains. Packed into a matrix, the derivatives of [N] become [B] = [∂]ᵀ[N], a 3 × 8 matrix, and Galerkin turns (3.17) into the element stiffness matrix:",
               "Membezakan u dan v memberi strain. Apabila dibungkus dalam matrix, derivative bagi [N] menjadi [B] = [∂]ᵀ[N], matrix 3 × 8, dan Galerkin menukar (3.17) kepada element stiffness matrix:"))
        + A.eq("p_B_preview") + A.eq("p_k_preview")
        + SB('<div class="tbl"><table><tr><th>' + B("Step", "Langkah") + '</th><th>' + B("Heat transfer", "Heat transfer") + '</th><th>' + B("Plane stress", "Plane stress") + '</th></tr>'
             + '<tr><td>PDE</td><td>{∂}[E]{∂}ᵀT = −q<sub>h</sub></td><td>[∂][E][∂]ᵀ{u}ᵀ = −{f}</td></tr>'
             + '<tr><td>' + B("operator", "operator") + '</td><td>{∂}: 1 × 2</td><td>[∂]: 2 × 3</td></tr>'
             + '<tr><td>' + B("material", "bahan") + '</td><td>[E]: 2 × 2</td><td>[E]: 3 × 3</td></tr>'
             + '<tr><td>' + B("shape functions", "shape function") + '</td><td>{N}: 1 × 4</td><td>[N]: 2 × 8</td></tr>'
             + '<tr><td>' + B("gradient / strain", "gradient / strain") + '</td><td>{∂}ᵀ{N}: 2 × 4</td><td>[B] = [∂]ᵀ[N]: 3 × 8</td></tr>'
             + '<tr><td>' + B("element matrix", "matrix element") + '</td><td>[k]: 4 × 4</td><td>[k] = t∫[B]ᵀ[E][B] dA: 8 × 8</td></tr>'
             + '<tr><td>' + B("natural BC", "natural BC") + '</td><td>' + B("flux → {b}", "flux → {b}") + '</td><td>' + B("traction → {b}", "traction → {b}") + '</td></tr>'
             + '<tr><td>' + B("essential BC", "essential BC") + '</td><td>T̄</td><td>ū, v̄</td></tr></table></div>')
        + KP([("Same N<sub>i</sub> as heat transfer, for u and for v: {u}ᵀ = [N]{û}ᵀ with [N] 2 × 8.", "N<sub>i</sub> yang sama seperti heat transfer, untuk u dan v: {u}ᵀ = [N]{û}ᵀ dengan [N] 2 × 8."),
              ("Dofs node by node, u before v; node n owns U<sub>2n−1</sub>, U<sub>2n</sub>.", "Dof node demi node, u sebelum v; node n memiliki U<sub>2n−1</sub>, U<sub>2n</sub>."),
              ("At (3.5, 1.3) in element 4: u = 0.0118 m, v = −0.1087 m.", "Pada (3.5, 1.3) dalam element 4: u = 0.0118 m, v = −0.1087 m.")])
        + QC("q6", "In the 2 × 2 cantilever mesh, which global dofs belong to node 5?", "Dalam mesh cantilever 2 × 2, dof global manakah milik node 5?",
             [("a", "U<sub>5</sub> and U<sub>6</sub>", "U<sub>5</sub> dan U<sub>6</sub>"), ("b", "U<sub>9</sub> and U<sub>10</sub>", "U<sub>9</sub> dan U<sub>10</sub>"), ("c", "U<sub>10</sub> and U<sub>11</sub>", "U<sub>10</sub> dan U<sub>11</sub>")],
             "b", "Node n owns U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y): for n = 5, U<sub>9</sub> and U<sub>10</sub>. Option (a) takes the node number for a dof number, the commonest numbering slip.",
             "Node n memiliki U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y): untuk n = 5, U<sub>9</sub> dan U<sub>10</sub>. Pilihan (a) mengambil nombor node sebagai nombor dof, kesilapan penomboran yang paling kerap.")
    )
    S.append(("n6", "Degrees of freedom and the shape-function matrix [N]", "Degree of freedom dan shape-function matrix [N]", body))
    return S


# ---- start-tab recall (from heat transfer) -------------------------------------------
RECALL = [
    QC("r1", "Recall · in the heat PDE {∂}[E]{∂}ᵀT = −q<sub>h</sub>, what is [E]?", "Ingat semula · dalam PDE heat {∂}[E]{∂}ᵀT = −q<sub>h</sub>, apakah [E]?",
       [("a", "diag(k<sub>x</sub>, k<sub>y</sub>), 2 × 2", "diag(k<sub>x</sub>, k<sub>y</sub>), 2 × 2"), ("b", "Young’s modulus", "Young’s modulus"), ("c", "the 4 × 4 conductance matrix", "conductance matrix 4 × 4")],
       "a", "[E] holds the conductivities, 2 × 2. Plane stress keeps the same pattern with a 3 × 3 [E] built from E and ν.",
       "[E] memuatkan conductivity, 2 × 2. Plane stress mengekalkan pola yang sama dengan [E] 3 × 3 yang dibina daripada E dan ν."),
    QC("r2", "Recall · in heat transfer, how is a known temperature T̄ put into the assembled equations?", "Ingat semula · dalam heat transfer, bagaimana temperature yang diketahui T̄ dimasukkan ke dalam assembled equation?",
       [("a", "As a nodal load in {b}", "Sebagai nodal load dalam {b}"), ("b", "By striking its row and column (row–column elimination)", "Dengan membuang baris dan lajurnya (row–column elimination)"), ("c", "It appears by itself through integration by parts", "Ia muncul dengan sendiri melalui integration by parts")],
       "b", "T̄ is essential: it is imposed on the assembled system, and the struck row later gives the heat flow there. A known displacement ū is treated in exactly the same way.",
       "T̄ adalah essential: ia dikenakan pada assembled system, dan baris yang dibuang kemudian memberi aliran haba di situ. Displacement yang diketahui ū dirawat dengan cara yang sama."),
]


QUICK = [
    MCQ("a1", "Which structure is best modelled in plane stress?", "Struktur manakah paling sesuai dimodelkan dalam plane stress?",
        [("a", "A 2 km tunnel lining under ground pressure", "Tunnel lining 2 km di bawah tekanan tanah"), ("b", "A 12 mm gusset plate loaded by its truss members", "Gusset plate 12 mm yang dibebankan oleh anggota truss"), ("c", "A floor slab carrying its live load", "Slab lantai yang menanggung beban hidup")], "b",
        "The gusset plate is thin and every member force acts in its plane: plane stress. The tunnel lining is long with a constant section (plane strain); the slab carries load normal to its plane (plate bending).",
        "Gusset plate itu nipis dan setiap daya anggota bertindak dalam satahnya: plane stress. Tunnel lining panjang dengan keratan seragam (plane strain); slab menanggung beban normal kepada satahnya (plate bending)."),
    MCQ("a2", "The (3,3) entry of the plane-stress [E] equals", "Entri (3,3) bagi [E] plane stress sama dengan",
        [("a", "E/(1 − ν²)", "E/(1 − ν²)"), ("b", "G = E/(2(1 + ν))", "G = E/(2(1 + ν))"), ("c", "νE/(1 − ν²)", "νE/(1 − ν²)")], "b",
        "E/(1 − ν²) × (1 − ν)/2 = E/(2(1 + ν)) = G, because ε<sub>xy</sub> is the engineering shear strain.",
        "E/(1 − ν²) × (1 − ν)/2 = E/(2(1 + ν)) = G, kerana ε<sub>xy</sub> ialah engineering shear strain."),
    MCQ("a3", "Compared with plane stress, the plane-strain [E] for the same E and ν is", "Berbanding plane stress, [E] plane strain untuk E dan ν yang sama adalah",
        [("a", "larger in the normal entries, with the same shear entry", "lebih besar dalam entri normal, dengan entri shear yang sama"), ("b", "smaller in every entry", "lebih kecil dalam setiap entri"), ("c", "identical", "sama sekali")], "a",
        "A slice that cannot strain through its thickness resists in-plane stretching more, so the normal entries grow (by 1/(1 − ν²) in bending); the shear modulus G is the same. With ν = 0 the two coincide.",
        "Kepingan yang tidak boleh ber-strain merentasi ketebalannya lebih menahan regangan dalam satah, jadi entri normal membesar (sebanyak 1/(1 − ν²) dalam lenturan); shear modulus G sama. Dengan ν = 0 kedua-duanya sama."),
    MCQ("a4", "u = 0.001x and v = −0.0003y everywhere in a plate. What is ε<sub>xy</sub>?", "u = 0.001x dan v = −0.0003y di seluruh plat. Apakah ε<sub>xy</sub>?",
        [("a", "0.0007", "0.0007"), ("b", "0", "0"), ("c", "0.00035", "0.00035")], "b",
        "ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x = 0 + 0: a stretch along x with a Poisson contraction along y, and no shear.",
        "ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x = 0 + 0: regangan dalam arah x dengan pengecutan Poisson dalam arah y, tanpa shear."),
    MCQ("a5", "A plate is held only by v = 0 along its left edge and loaded on the right. Why does the solver fail?", "Satu plat ditahan hanya dengan v = 0 di sepanjang tepi kirinya dan dibebankan di kanan. Mengapa solver gagal?",
        [("a", "The load is too large", "Beban terlalu besar"), ("b", "Nothing stops a rigid translation in x (or a rotation about the edge), so [K] is singular", "Tiada yang menghalang rigid translation dalam x (atau putaran terhadap tepi itu), jadi [K] singular"), ("c", "The mesh is too coarse", "Mesh terlalu kasar")], "b",
        "Rigid motions produce no strain and need no force; unless the supports remove both translations and the rotation, [K] is singular. v = 0 on a vertical line leaves u free everywhere.",
        "Rigid motion tidak menghasilkan strain dan tidak memerlukan daya; melainkan support menghapuskan kedua-dua translation dan putaran, [K] singular. v = 0 pada garis menegak membiarkan u bebas di mana-mana."),
    MCQ("a6", "What is the size of [N] for the four-node plane-stress element?", "Apakah saiz [N] bagi four-node element plane stress?",
        [("a", "1 × 4", "1 × 4"), ("b", "2 × 8", "2 × 8"), ("c", "3 × 8", "3 × 8")], "b",
        "Two fields (u, v) from eight dofs: 2 × 8. 1 × 4 is the heat-transfer {N}; 3 × 8 is [B] of Part 2.",
        "Dua field (u, v) daripada lapan dof: 2 × 8. 1 × 4 ialah {N} heat transfer; 3 × 8 ialah [B] dalam Part 2."),
]

ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="3" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("A student builds the plane-stress [E] for E = 200 × 10⁶ kN m<sup>−2</sup> and ν = 0.25, and uses it for a shear strain ε<sub>xy</sub> = 1 × 10<sup>−5</sup>. One line contains the slip. Which one?",
        "Seorang pelajar membina [E] plane stress untuk E = 200 × 10⁶ kN m<sup>−2</sup> dan ν = 0.25, dan menggunakannya untuk shear strain ε<sub>xy</sub> = 1 × 10<sup>−5</sup>. Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>E/(1 − ν²) = 200 × 10⁶/(1 − 0.0625) = 213.33 × 10⁶</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>E<sub>11</sub> = E<sub>22</sub> = 213.33 × 10⁶; E<sub>12</sub> = 0.25 × 213.33 × 10⁶ = 53.33 × 10⁶</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>E<sub>33</sub> = (1 − ν) × 213.33 × 10⁶ = 160.00 × 10⁶</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>σ<sub>xy</sub> = E<sub>33</sub> ε<sub>xy</sub> = 160.00 × 10⁶ × 1 × 10<sup>−5</sup> = 1600 kN m<sup>−2</sup></span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 3: the shear entry is (1 − ν)/2 × E/(1 − ν²) = 0.375 × 213.33 × 10⁶ = 80.00 × 10⁶ kN m<sup>−2</sup>. The check that catches it: it must equal G = E/(2(1 + ν)) = 200 × 10⁶/2.5 = 80.00 × 10⁶. Line 4 then follows the slip; the correct shear stress is 800 kN m<sup>−2</sup>.",
        "Baris 3: entri shear ialah (1 − ν)/2 × E/(1 − ν²) = 0.375 × 213.33 × 10⁶ = 80.00 × 10⁶ kN m<sup>−2</sup>. Semakan yang menangkapnya: ia mesti sama dengan G = E/(2(1 + ν)) = 200 × 10⁶/2.5 = 80.00 × 10⁶. Baris 4 hanya mengikut kesilapan itu; shear stress yang betul ialah 800 kN m<sup>−2</sup>.")
    + '</p></div>'
)

# parameterised calculation exercises
EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  var MATS = [["steel", 200, [0.25, 0.3]], ["aluminium", 70, [0.33]], ["concrete", 30, [0.15, 0.2]], ["timber", 10, [0.3]], ["soft rubber-like plastic", 3, [0.4, 0.45]]];
  function Emat(E, nu, strain){
    if (!strain) { var c = E/(1-nu*nu); return [c, nu*c, c*(1-nu)/2]; }
    var d = E/((1+nu)*(1-2*nu)); return [d*(1-nu), d*nu, d*(1-2*nu)/2];
  }
  // b1: [E] for plane stress or plane strain
  EX.define("b1", {
    gen: function(r){ var m = pick(r, MATS); return {name:m[0], E:m[1], nu:pick(r, m[2]), strain: r() < 0.5}; },
    text: function(P){ var k = P.strain ? ["plane strain","plane strain"] : ["plane stress","plane stress"];
      return bi("A "+P.name+" with E = <span class=\"num\">"+P.E+"</span> GPa and ν = <span class=\"num\">"+P.nu+"</span>, in <b>"+k[0]+"</b>. Find the three distinct entries of [E] in GPa, to 3 significant figures.",
                "Satu "+({"steel":"keluli","aluminium":"aluminium","concrete":"konkrit","timber":"kayu","soft rubber-like plastic":"plastik lembut seperti getah"}[P.name])+" dengan E = <span class=\"num\">"+P.E+"</span> GPa dan ν = <span class=\"num\">"+P.nu+"</span>, dalam <b>"+k[1]+"</b>. Cari tiga entri berbeza bagi [E] dalam GPa, kepada 3 angka bererti."); },
    fields: [{id:"e11", label:["E<sub>11</sub> = E<sub>22</sub>","E<sub>11</sub> = E<sub>22</sub>"], unit:"GPa", fn:function(P){ return Emat(P.E,P.nu,P.strain)[0]; }, rtol:0.005, atol:0},
             {id:"e12", label:["E<sub>12</sub>","E<sub>12</sub>"], unit:"GPa", fn:function(P){ return Emat(P.E,P.nu,P.strain)[1]; }, rtol:0.005, atol:0},
             {id:"e33", label:["E<sub>33</sub>","E<sub>33</sub>"], unit:"GPa", fn:function(P){ return Emat(P.E,P.nu,P.strain)[2]; }, rtol:0.005, atol:0}],
    hints: [function(P){ return P.strain ? bi("Plane strain: [E] = E/((1 + ν)(1 − 2ν)) × [1 − ν, ν, 0; ν, 1 − ν, 0; 0, 0, (1 − 2ν)/2].","Plane strain: [E] = E/((1 + ν)(1 − 2ν)) × [1 − ν, ν, 0; ν, 1 − ν, 0; 0, 0, (1 − 2ν)/2].")
                                     : bi("Plane stress (3.11): [E] = E/(1 − ν²) × [1, ν, 0; ν, 1, 0; 0, 0, (1 − ν)/2].","Plane stress (3.11): [E] = E/(1 − ν²) × [1, ν, 0; ν, 1, 0; 0, 0, (1 − ν)/2]."); },
            function(P){ return bi("Check E<sub>33</sub>: in both idealisations it equals G = E/(2(1 + ν)) = "+fmt(P.E/(2*(1+P.nu)),3)+" GPa.","Semak E<sub>33</sub>: dalam kedua-dua idealisation ia sama dengan G = E/(2(1 + ν)) = "+fmt(P.E/(2*(1+P.nu)),3)+" GPa."); }],
    solution: function(P){ var e = Emat(P.E,P.nu,P.strain), c = P.strain ? P.E/((1+P.nu)*(1-2*P.nu)) : P.E/(1-P.nu*P.nu);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">"+(P.strain
        ? "E/((1 + ν)(1 − 2ν)) = "+P.E+"/("+fmt(1+P.nu,2)+" × "+fmt(1-2*P.nu,2)+") = "+fmt(c,3)+" GPa<br>E<sub>11</sub> = (1 − ν)("+fmt(c,3)+") = "+fmt(e[0],3)+"<br>E<sub>12</sub> = ν("+fmt(c,3)+") = "+fmt(e[1],3)+"<br>E<sub>33</sub> = (1 − 2ν)/2 ("+fmt(c,3)+") = "+fmt(e[2],3)
        : "E/(1 − ν²) = "+P.E+"/"+fmt(1-P.nu*P.nu,4)+" = "+fmt(c,3)+" GPa<br>E<sub>11</sub> = "+fmt(e[0],3)+"<br>E<sub>12</sub> = ν("+fmt(c,3)+") = "+fmt(e[1],3)+"<br>E<sub>33</sub> = (1 − ν)/2 ("+fmt(c,3)+") = "+fmt(e[2],3))
        +" GPa<br>"+bi("Check: G = E/(2(1 + ν)) = ","Semak: G = E/(2(1 + ν)) = ")+fmt(P.E/(2*(1+P.nu)),3)+" GPa = E<sub>33</sub></p>"; }
  });
  // b2: u and v at a point of an element from its nodal displacements
  function N4(a,b,x,y){ return [(a-x)*(b-y)/(a*b), x*(b-y)/(a*b), x*y/(a*b), y*(a-x)/(a*b)]; }
  EX.define("b2", {
    gen: function(r){ var a = pick(r,[0.4,0.5,0.6,0.8,1.0,2.0]), b = pick(r,[0.2,0.3,0.4,0.5,1.0]);
      var x = Math.round((0.1+0.8*r())*a*20)/20, y = Math.round((0.1+0.8*r())*b*20)/20;
      var u = [0,0,0,0].map(function(){ return Math.round((r()*4-1)*10)/10; }), v = [0,0,0,0].map(function(){ return Math.round((r()*4-3)*10)/10; });
      return {a:a,b:b,x:x,y:y,u:u,v:v}; },
    text: function(P){ return bi("Element a = <span class=\"num\">"+P.a+"</span> m by b = <span class=\"num\">"+P.b+"</span> m, local nodes 1–4 anticlockwise from the origin. Nodal displacements (× 10<sup>−3</sup> m): u = {"+P.u.join(", ")+"}, v = {"+P.v.join(", ")+"}. Find u and v at the local point (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m, in 10<sup>−3</sup> m to 3 decimals.",
                                 "Element a = <span class=\"num\">"+P.a+"</span> m × b = <span class=\"num\">"+P.b+"</span> m, local node 1–4 lawan arah jam dari asalan. Nodal displacement (× 10<sup>−3</sup> m): u = {"+P.u.join(", ")+"}, v = {"+P.v.join(", ")+"}. Cari u dan v pada titik local (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m, dalam 10<sup>−3</sup> m kepada 3 tempat perpuluhan."); },
    fields: [{id:"u", label:["u","u"], unit:"10⁻³ m", fn:function(P){ var N=N4(P.a,P.b,P.x,P.y); return N[0]*P.u[0]+N[1]*P.u[1]+N[2]*P.u[2]+N[3]*P.u[3]; }, atol:0.0015, rtol:0},
             {id:"v", label:["v","v"], unit:"10⁻³ m", fn:function(P){ var N=N4(P.a,P.b,P.x,P.y); return N[0]*P.v[0]+N[1]*P.v[1]+N[2]*P.v[2]+N[3]*P.v[3]; }, atol:0.0015, rtol:0}],
    hints: [function(P){ return bi("(3.24)–(3.25): u = Σ N<sub>i</sub> u<sub>i</sub> and v = Σ N<sub>i</sub> v<sub>i</sub>, with the N<sub>i</sub> of (2.21): N<sub>1</sub> = (a − x)(b − y)/(ab), N<sub>2</sub> = x(b − y)/(ab), N<sub>3</sub> = xy/(ab), N<sub>4</sub> = y(a − x)/(ab).",
                                      "(3.24)–(3.25): u = Σ N<sub>i</sub> u<sub>i</sub> dan v = Σ N<sub>i</sub> v<sub>i</sub>, dengan N<sub>i</sub> daripada (2.21): N<sub>1</sub> = (a − x)(b − y)/(ab), N<sub>2</sub> = x(b − y)/(ab), N<sub>3</sub> = xy/(ab), N<sub>4</sub> = y(a − x)/(ab)."); },
            function(P){ var N=N4(P.a,P.b,P.x,P.y); return bi("N = {"+N.map(function(n){return fmt(n,4);}).join(", ")+"}; they sum to 1. The same four numbers multiply the u-values and the v-values.",
                                      "N = {"+N.map(function(n){return fmt(n,4);}).join(", ")+"}; jumlahnya 1. Empat nombor yang sama mendarab nilai-u dan nilai-v."); }],
    solution: function(P){ var N=N4(P.a,P.b,P.x,P.y), u=0, v=0; for (var i=0;i<4;i++){ u+=N[i]*P.u[i]; v+=N[i]*P.v[i]; }
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">N = {"+N.map(function(n){return fmt(n,4);}).join(", ")+"}, Σ = "+fmt(N[0]+N[1]+N[2]+N[3],4)+"<br>u = "+N.map(function(n,i){return fmt(n,4)+"("+P.u[i]+")";}).join(" + ")+" = "+fmt(u,3)+" × 10<sup>−3</sup> m<br>v = "+N.map(function(n,i){return fmt(n,4)+"("+P.v[i]+")";}).join(" + ")+" = "+fmt(v,3)+" × 10<sup>−3</sup> m</p>"; }
  });
  // b3: strains from a displacement field, then stresses by Hooke (plane stress)
  function lin(c1, c2){ var t = "<span class=\"num\">"+fmt(c1,1)+"</span>x " + (c2 < 0 ? "− " : "+ ") + "<span class=\"num\">"+fmt(Math.abs(c2),1)+"</span>y"; return t; }
  EX.define("b3", {
    gen: function(r){ var c = function(){ return Math.round((r()*6-3)*10)/10 || 0.5; };
      return {a2:c(), a3:c(), b2:c(), b3:c(), E:pick(r,[70,200,210]), nu:pick(r,[0.25,0.3,0.33])}; },
    text: function(P){ return bi("In a plate the displacements are u = ("+lin(P.a2,P.a3)+") × 10<sup>−4</sup> and v = ("+lin(P.b2,P.b3)+") × 10<sup>−4</sup> (x, y in m). E = <span class=\"num\">"+P.E+"</span> GPa, ν = <span class=\"num\">"+P.nu+"</span>, plane stress. Find the strains (× 10<sup>−4</sup>) and σ<sub>xx</sub>, σ<sub>xy</sub> in MPa, to 3 significant figures.",
                                 "Dalam satu plat, displacement ialah u = ("+lin(P.a2,P.a3)+") × 10<sup>−4</sup> dan v = ("+lin(P.b2,P.b3)+") × 10<sup>−4</sup> (x, y dalam m). E = <span class=\"num\">"+P.E+"</span> GPa, ν = <span class=\"num\">"+P.nu+"</span>, plane stress. Cari strain (× 10<sup>−4</sup>) serta σ<sub>xx</sub>, σ<sub>xy</sub> dalam MPa, kepada 3 angka bererti."); },
    fields: [{id:"exx", label:["ε<sub>xx</sub>","ε<sub>xx</sub>"], unit:"10⁻⁴", fn:function(P){ return P.a2; }, atol:0.001, rtol:0},
             {id:"eyy", label:["ε<sub>yy</sub>","ε<sub>yy</sub>"], unit:"10⁻⁴", fn:function(P){ return P.b3; }, atol:0.001, rtol:0},
             {id:"exy", label:["ε<sub>xy</sub>","ε<sub>xy</sub>"], unit:"10⁻⁴", fn:function(P){ return P.a3+P.b2; }, atol:0.001, rtol:0},
             {id:"sxx", label:["σ<sub>xx</sub>","σ<sub>xx</sub>"], unit:"MPa", fn:function(P){ return P.E*1e3/(1-P.nu*P.nu)*(P.a2+P.nu*P.b3)*1e-4; }, rtol:0.005, atol:0.05},
             {id:"sxy", label:["σ<sub>xy</sub>","σ<sub>xy</sub>"], unit:"MPa", fn:function(P){ return P.E*1e3/(2*(1+P.nu))*(P.a3+P.b2)*1e-4; }, rtol:0.005, atol:0.05}],
    hints: [function(P){ return bi("(3.13): ε<sub>xx</sub> = ∂u/∂x, ε<sub>yy</sub> = ∂v/∂y, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x (the engineering shear strain, both slopes added).",
                                      "(3.13): ε<sub>xx</sub> = ∂u/∂x, ε<sub>yy</sub> = ∂v/∂y, ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x (engineering shear strain, kedua-dua cerun ditambah)."); },
            function(P){ return bi("(3.10): σ<sub>xx</sub> = E/(1 − ν²)(ε<sub>xx</sub> + ν ε<sub>yy</sub>); σ<sub>xy</sub> = G ε<sub>xy</sub> with G = E/(2(1 + ν)). 1 GPa × 10<sup>−4</sup> = 0.1 MPa.",
                                      "(3.10): σ<sub>xx</sub> = E/(1 − ν²)(ε<sub>xx</sub> + ν ε<sub>yy</sub>); σ<sub>xy</sub> = G ε<sub>xy</sub> dengan G = E/(2(1 + ν)). 1 GPa × 10<sup>−4</sup> = 0.1 MPa."); },
            function(P){ return bi("E/(1 − ν²) = "+fmt(P.E/(1-P.nu*P.nu),2)+" GPa; G = "+fmt(P.E/(2*(1+P.nu)),2)+" GPa.","E/(1 − ν²) = "+fmt(P.E/(1-P.nu*P.nu),2)+" GPa; G = "+fmt(P.E/(2*(1+P.nu)),2)+" GPa."); }],
    solution: function(P){ var c=P.E/(1-P.nu*P.nu), G=P.E/(2*(1+P.nu)), exy=P.a3+P.b2;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">ε<sub>xx</sub> = ∂u/∂x = "+P.a2+" × 10<sup>−4</sup>; ε<sub>yy</sub> = ∂v/∂y = "+P.b3+" × 10<sup>−4</sup><br>ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x = "+P.a3+" + "+P.b2+" = "+fmt(exy,1)+" × 10<sup>−4</sup><br>σ<sub>xx</sub> = "+fmt(c,2)+" GPa × ("+P.a2+" + "+P.nu+" × "+P.b3+") × 10<sup>−4</sup> = "+fmt(c*1e3*(P.a2+P.nu*P.b3)*1e-4,2)+" MPa<br>σ<sub>xy</sub> = "+fmt(G,2)+" GPa × "+fmt(exy,1)+" × 10<sup>−4</sup> = "+fmt(G*1e3*exy*1e-4,2)+" MPa</p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("The constitutive matrix [E], plane stress or plane strain", "Constitutive matrix [E], plane stress atau plane strain"), 4),
    ("b2", ("Displacements at a point of an element", "Displacement pada satu titik dalam element"), 4),
    ("b3", ("Strains from a displacement field, then stresses", "Strain daripada displacement field, kemudian stress"), 6),
]

LAB_TASKS = [
    ("pstrain", ("Choose a mesh (in class: 8-node, 8 × 4), read the tip deflection in plane stress, then switch to plane strain. By how much does it change, and why?",
                 "Pilih satu mesh (dalam kelas: 8-node, 8 × 4), baca tip deflection dalam plane stress, kemudian tukar kepada plane strain. Berapa banyak ia berubah, dan mengapa?"),
     ("detected when the same mesh has been solved in plane stress and in plane strain with the text’s data", "dikesan apabila mesh yang sama telah diselesaikan dalam plane stress dan plane strain dengan data teks")),
    ("vonly", ("Change the support on the left edge to “Vertical only: v = 0”. What does the Explorer report, and which rigid motions are left free?",
               "Tukar support pada tepi kiri kepada “Vertical only: v = 0”. Apa yang dilaporkan oleh Explorer, dan rigid motion manakah yang dibiarkan bebas?"),
     ("detected when the vertical-only support leaves the model unsolvable", "dikesan apabila support vertical-only menjadikan model tidak boleh diselesaikan")),
    ("thick", ("Open “Model data” and change the thickness t (for example to 0.02 m). How does the tip deflection change, and where does t enter the equations?",
               "Buka “Model data” dan tukar ketebalan t (contohnya kepada 0.02 m). Bagaimana tip deflection berubah, dan di mana t masuk ke dalam persamaan?"),
     ("detected when t differs from 0.01 m with the text’s data otherwise", "dikesan apabila t berbeza daripada 0.01 m dengan data teks yang lain")),
    ("nu0", ("Set ν = 0 in “Model data” and compare plane stress with plane strain on the same mesh. Why are they now identical?",
             "Tetapkan ν = 0 dalam “Model data” dan bandingkan plane stress dengan plane strain pada mesh yang sama. Mengapa kedua-duanya kini sama?"),
     ("detected when ν = 0 has been solved in both idealisations on the same mesh", "dikesan apabila ν = 0 telah diselesaikan dalam kedua-dua idealisation pada mesh yang sama")),
]

GLOSSARY = [
    ("plane stress", "A thin body loaded in its own plane: σ<sub>zz</sub> = σ<sub>xz</sub> = σ<sub>yz</sub> = 0, while ε<sub>zz</sub> may be non-zero.", "Badan nipis yang dibebankan dalam satahnya sendiri: σ<sub>zz</sub> = σ<sub>xz</sub> = σ<sub>yz</sub> = 0, manakala ε<sub>zz</sub> boleh bukan sifar."),
    ("plane strain", "A long body with every section loaded alike: ε<sub>zz</sub> = 0, and σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) develops.", "Badan panjang dengan setiap keratan dibebankan sama: ε<sub>zz</sub> = 0, dan σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) terbentuk."),
    ("displacement u, v", "The movement of a point along x and along y; the primary unknowns of plane stress.", "Pergerakan satu titik dalam arah x dan y; primary unknown bagi plane stress."),
    ("normal stress · shear stress", "σ<sub>xx</sub>, σ<sub>yy</sub> act normal to a face; σ<sub>xy</sub> = σ<sub>yx</sub> act along it (N m<sup>−2</sup>).", "σ<sub>xx</sub>, σ<sub>yy</sub> bertindak normal kepada muka; σ<sub>xy</sub> = σ<sub>yx</sub> bertindak di sepanjangnya (N m<sup>−2</sup>)."),
    ("body force f", "Force per unit volume acting inside the body, N m<sup>−3</sup>; self-weight f<sub>y</sub> = −ρg.", "Daya per unit isi padu yang bertindak di dalam badan, N m<sup>−3</sup>; berat sendiri f<sub>y</sub> = −ρg."),
    ("differential element", "A small rectangle dx × dy on which equilibrium is written before the size goes to zero.", "Segi empat kecil dx × dy tempat equilibrium ditulis sebelum saiznya menghampiri sifar."),
    ("equilibrium equations", "(3.4) and (3.6): the stress gradients balance the body force in x and in y.", "(3.4) dan (3.6): stress gradient mengimbangi body force dalam arah x dan y."),
    ("operator matrix [∂]", "The 2 × 3 matrix of derivatives in [∂]{σ}ᵀ = −{f}; its transpose gives the strains.", "Matrix derivative 2 × 3 dalam [∂]{σ}ᵀ = −{f}; transpose-nya memberi strain."),
    ("constitutive matrix [E]", "The 3 × 3 matrix of Hooke’s law, {σ}ᵀ = [E]{ε}ᵀ; different for plane stress and plane strain.", "Matrix 3 × 3 bagi Hooke’s law, {σ}ᵀ = [E]{ε}ᵀ; berbeza untuk plane stress dan plane strain."),
    ("Young’s modulus E · Poisson’s ratio ν", "Stiffness in uniaxial tension; lateral contraction per unit axial strain.", "Kekakuan dalam tegangan uniaxial; pengecutan sisi per unit axial strain."),
    ("shear modulus G", "G = E/(2(1 + ν)); the (3,3) entry of [E] in both idealisations.", "G = E/(2(1 + ν)); entri (3,3) bagi [E] dalam kedua-dua idealisation."),
    ("engineering shear strain ε<sub>xy</sub>", "∂u/∂y + ∂v/∂x, the change of a right angle (γ<sub>xy</sub> in many books); twice the tensor shear strain.", "∂u/∂y + ∂v/∂x, perubahan sudut tegak (γ<sub>xy</sub> dalam banyak buku); dua kali tensor shear strain."),
    ("strain–displacement relation", "{ε}ᵀ = [∂]ᵀ{u}ᵀ: three strains from two displacements.", "{ε}ᵀ = [∂]ᵀ{u}ᵀ: tiga strain daripada dua displacement."),
    ("traction b", "Force per unit area on the boundary, b<sub>x</sub> = σ<sub>xx</sub>n<sub>x</sub> + σ<sub>xy</sub>n<sub>y</sub>, b<sub>y</sub> = σ<sub>xy</sub>n<sub>x</sub> + σ<sub>yy</sub>n<sub>y</sub>.", "Daya per unit luas pada sempadan, b<sub>x</sub> = σ<sub>xx</sub>n<sub>x</sub> + σ<sub>xy</sub>n<sub>y</sub>, b<sub>y</sub> = σ<sub>xy</sub>n<sub>x</sub> + σ<sub>yy</sub>n<sub>y</sub>."),
    ("natural · essential", "Natural: a known traction, entered as a load. Essential: a known displacement, imposed on the assembled system.", "Natural: traction yang diketahui, dimasukkan sebagai beban. Essential: displacement yang diketahui, dikenakan pada assembled system."),
    ("free edge", "A natural condition with zero traction; the finite element model does nothing there.", "Natural condition dengan traction sifar; model finite element tidak buat apa-apa di situ."),
    ("rigid-body motion", "Translation or rotation without strain; supports must remove all three in 2D or [K] is singular.", "Translation atau putaran tanpa strain; support mesti menghapuskan ketiga-tiganya dalam 2D, jika tidak [K] singular."),
    ("reaction", "Force at a support, recovered after solving from the struck rows of the system.", "Daya pada support, diperoleh selepas menyelesaikan daripada baris sistem yang dibuang."),
    ("degree of freedom (dof)", "One nodal unknown; node n owns U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y).", "Satu nodal unknown; node n memiliki U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y)."),
    ("shape-function matrix [N]", "The 2 × 8 matrix with {u v}ᵀ = [N]{û}ᵀ; the same N<sub>i</sub> for u and for v.", "Matrix 2 × 8 dengan {u v}ᵀ = [N]{û}ᵀ; N<sub>i</sub> yang sama untuk u dan v."),
    ("strain-displacement matrix [B]", "[B] = [∂]ᵀ[N], 3 × 8, so that {ε}ᵀ = [B]{û}ᵀ; built in Part 2.", "[B] = [∂]ᵀ[N], 3 × 8, supaya {ε}ᵀ = [B]{û}ᵀ; dibina dalam Part 2."),
    ("stiffness matrix [k]", "[k] = t∫[B]ᵀ[E][B] dA, 8 × 8 for the four-node element; the analogue of the conductance matrix.", "[k] = t∫[B]ᵀ[E][B] dA, 8 × 8 bagi four-node element; analog bagi conductance matrix."),
]


def short_notes(A):
    return (
        "<h3>§1 " + B("Idealisation", "Idealisation") + "</h3>" + LI([("Plane stress: thin, in-plane loads, σ<sub>zz</sub> = 0.", "Plane stress: nipis, beban dalam satah, σ<sub>zz</sub> = 0."), ("Plane strain: long, uniform section, ε<sub>zz</sub> = 0.", "Plane strain: panjang, keratan seragam, ε<sub>zz</sub> = 0."), ("Unknowns u, v: two dofs per node.", "Unknown u, v: dua dof setiap node.")])
        + "<h3>§2 " + B("Equilibrium", "Equilibrium") + "</h3>" + A.eq("p_matrix", "(3.8)", 0.45) + A.eq("p_compact", "(3.9)", 0.5)
        + "<h3>§3 Hooke</h3>" + A.eq("p_E", "(3.11)", 0.45) + P("(3,3) entry = G = E/(2(1 + ν)). Cantilever: 224.44, 74.07, 75.19 × 10⁶ N m<sup>−2</sup>.", "Entri (3,3) = G = E/(2(1 + ν)). Cantilever: 224.44, 74.07, 75.19 × 10⁶ N m<sup>−2</sup>.")
        + "<h3>§4 " + B("Strain and the PDE", "Strain dan PDE") + "</h3>" + A.eq("p_strain", "(3.13)", 0.45) + A.eq("p_pde", "(3.17)", 0.5)
        + "<h3>§5 " + B("Boundary conditions", "Boundary condition") + "</h3>" + A.eq("p_bx", None, 0.42)
        + LI([("Traction = natural = load (free edge: nothing).", "Traction = natural = beban (tepi bebas: tiada)."), ("Displacement = essential = imposed.", "Displacement = essential = dikenakan."), ("Supports must stop 2 translations + 1 rotation.", "Support mesti menghalang 2 translation + 1 putaran.")])
        + "<h3>§6 [N]</h3>" + A.eq("p_interp", None, 0.45) + P("Node n: U<sub>2n−1</sub>, U<sub>2n</sub>. At (3.5, 1.3): u = 0.0118 m, v = −0.1087 m.", "Node n: U<sub>2n−1</sub>, U<sub>2n</sub>. Pada (3.5, 1.3): u = 0.0118 m, v = −0.1087 m.")
    )


# ---- worked examples: answer-scheme style, from the course companion (FEM by Hand, Ch. 9) ----
EXAMPLES_INTRO = (
    '<div class="card" style="margin-bottom:18px"><h2 style="font-size:18px;margin:0 0 6px">' + B("How plane stress is examined", "Bagaimana plane stress diuji") + '</h2>'
    + P("Model answers in the form the examiner expects: physical picture, plan, numbered steps with every substitution written out, checks, a boxed answer and an interpretation. "
        "The marks are a suggested scheme; the examiner’s own scheme may differ. Part 2 adds [k], loads and assembly; Part 3 adds stresses and accuracy.",
        "Jawapan model dalam bentuk yang pemeriksa jangkakan: gambaran fizikal, pelan, langkah bernombor dengan setiap penggantian ditulis, semakan, jawapan berkotak dan tafsiran. "
        "Markah ialah skema cadangan; skema pemeriksa sendiri mungkin berbeza. Part 2 menambah [k], beban dan assembly; Part 3 menambah stress dan ketepatan.", "lead")
    + '<div class="tbl"><table class="howex"><tr><th>' + B("Question type", "Jenis soalan") + '</th><th>' + B("Given and wanted", "Diberi dan dikehendaki") + '</th><th>' + B("Plan and the usual trap", "Pelan dan perangkap biasa") + '</th></tr>'
    + '<tr><td>' + B("Displacement and stress at a point", "Displacement dan stress pada satu titik") + '</td><td>' + B("Nodal displacements of an element; wanted: u, v, ε, σ at (x<sub>1</sub>, y<sub>1</sub>).", "Nodal displacement bagi satu element; dikehendaki: u, v, ε, σ pada (x<sub>1</sub>, y<sub>1</sub>).") + '</td><td>' + B("N<sub>i</sub> and their derivatives at the point, then [E]. Trap: global coordinates in N<sub>i</sub>; the factor (1 − ν)/2.", "N<sub>i</sub> dan derivative-nya pada titik itu, kemudian [E]. Perangkap: koordinat global dalam N<sub>i</sub>; faktor (1 − ν)/2.") + '</td></tr>'
    + '<tr><td>' + B("Plane stress or plane strain", "Plane stress atau plane strain") + '</td><td>' + B("E, ν; wanted: [E], sometimes σ for given strains.", "E, ν; dikehendaki: [E], kadang-kadang σ untuk strain yang diberi.") + '</td><td>' + B("Pick the idealisation from the geometry first. Trap: the two [E] mixed.", "Pilih idealisation daripada geometri dahulu. Perangkap: dua [E] bercampur.") + '</td></tr>'
    + '<tr><td>' + B("Numbering and supports", "Penomboran dan support") + '</td><td>' + B("A mesh without numbers; wanted: node, element and dof numbers, known dofs, nodal loads.", "Mesh tanpa nombor; dikehendaki: nombor node, element dan dof, dof yang diketahui, nodal load.") + '</td><td>' + B("Row by row; nodes of each element anticlockwise from the lower left. Trap: node number taken for dof number.", "Baris demi baris; node setiap element lawan arah jam dari kiri bawah. Perangkap: nombor node diambil sebagai nombor dof.") + '</td></tr></table></div>'
    + P("Notation follows the companion: {d} = {u<sub>1</sub> v<sub>1</sub> … u<sub>4</sub> v<sub>4</sub>}ᵀ for an element’s nodal displacements, Ē = E/(1 − ν²), units kN and m (stresses in kN/m²).",
        "Notasi mengikut buku pendamping: {d} = {u<sub>1</sub> v<sub>1</sub> … u<sub>4</sub> v<sub>4</sub>}ᵀ bagi nodal displacement satu element, Ē = E/(1 − ν²), unit kN dan m (stress dalam kN/m²).", "lead")
    + '</div>')


def examples(A):
    X = []
    # ---- Example 1: displacements, strains and stresses at a point (book Example 9.1) ----
    head = ('<div class="xhead"><h2>' + B("Example 1 · Displacements, strains and stresses at a point", "Contoh 1 · Displacement, strain dan stress pada satu titik") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> given {d} of an element, find u, v, ε and σ at a point</span><span><b>' + B("Units", "Unit") + '</b> kN, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 9.1</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>An element 0.6 m by 0.4 m, with E = 200 × 10⁶ kN/m² and ν = 0.3 (plane stress), has the nodal displacements '
         '{d} = {u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>}ᵀ = {1, 0.1, 2, 0.1, 2, 0, 1, 0}ᵀ × 10<sup>−5</sup> m. (a) Explain how the displacements and stresses at a point (x<sub>1</sub>, y<sub>1</sub>) of the element are obtained. '
         '(b) Calculate the stresses at the centre. (c) With u<sub>3</sub> = 3 × 10<sup>−5</sup> m instead, find u, v and the stresses at (0.15, 0.3) m.</div>')
    body = (head + q + A.fig("fig_ps1_el", "The element of Example 1, its eight dofs, the centre and the point (0.15, 0.3).", "Element bagi Contoh 1, lapan dof-nya, pusat dan titik (0.15, 0.3).", 460)
            + PIC("Nodes 2 and 3 move 1 × 10<sup>−5</sup> m further right than nodes 1 and 4, so the element is stretched along x by 10<sup>−5</sup>/0.6 = 1.67 × 10<sup>−5</sup>. The top moves down by 10<sup>−6</sup> relative to the bottom: a contraction in y. Nothing shears it. Expect σ<sub>xx</sub> near Eε<sub>xx</sub> ≈ 3.3 × 10³ kN/m², a little more because the element contracts in y less than a free bar would.",
                  "Node 2 dan 3 bergerak 1 × 10<sup>−5</sup> m lebih ke kanan berbanding node 1 dan 4, jadi element itu diregang dalam arah x sebanyak 10<sup>−5</sup>/0.6 = 1.67 × 10<sup>−5</sup>. Bahagian atas bergerak ke bawah 10<sup>−6</sup> relatif kepada bahagian bawah: pengecutan dalam arah y. Tiada yang meng-shear-nya. Jangka σ<sub>xx</sub> sekitar Eε<sub>xx</sub> ≈ 3.3 × 10³ kN/m², sedikit lebih kerana element itu mengecut dalam arah y kurang daripada bar bebas.")
            + PLAN("(a) local coordinates → N<sub>i</sub> → u, v → derivatives → {ε} → {σ}; (b) the centre; (c) the point (0.15, 0.3), then the centre as a check.")
            + XSTEP(1, "(a) The procedure", "(a) Prosedur", 4, A.eq("u1_proc")
                    + P("Only the nodal displacements of the element that contains the point are used. In Part 2 the derivatives of step (3) are packed into the matrix [B], so that {ε}ᵀ = [B]{d}.",
                        "Hanya nodal displacement bagi element yang mengandungi titik itu digunakan. Dalam Part 2, derivative dalam langkah (3) dibungkus ke dalam matrix [B], supaya {ε}ᵀ = [B]{d}."))
            + XSTEP(2, "The derivatives of u and v", "Derivative bagi u dan v", 2, P("Differentiating u = Σ N<sub>i</sub>u<sub>i</sub> with the N<sub>i</sub> of (2.21) gives, at any local point (x, y),", "Membezakan u = Σ N<sub>i</sub>u<sub>i</sub> dengan N<sub>i</sub> daripada (2.21) memberi, pada mana-mana titik local (x, y),") + A.eq("u1_deriv"))
            + XSTEP(3, "(b) Strains at the centre", "(b) Strain pada pusat", 3, P("At (a/2, b/2) each derivative becomes the average of two side differences:", "Pada (a/2, b/2) setiap derivative menjadi purata dua beza sisi:") + A.eq("u1_epsc"))
            + XSTEP(4, "(b) Stresses at the centre", "(b) Stress pada pusat", 3, A.eq("u1_sigc") + ANS("(b) σ<sub>xx</sub> = 3.50 × 10³ kN/m² (3.50 MPa), σ<sub>yy</sub> = 549 kN/m², σ<sub>xy</sub> = 0.")
                    + CHK("σ<sub>xx</sub> is a little above Eε<sub>xx</sub> = 3333 kN/m², as the physical picture predicted."))
            + XSTEP(5, "(c) Displacements at (0.15, 0.3)", "(c) Displacement pada (0.15, 0.3)", 3, A.eq("u1_Np") + A.eq("u1_uvp"))
            + XSTEP(6, "(c) Strains and stresses at (0.15, 0.3)", "(c) Strain dan stress pada (0.15, 0.3)", 5, A.eq("u1_epsp") + A.eq("u1_sigp")
                    + ANS("(c) u = 1.44 × 10<sup>−5</sup> m, v = 2.5 × 10<sup>−7</sup> m; σ = {6245, 1374, 481} kN/m² at (0.15, 0.3).")
                    + P("At the centre the same steps give", "Pada pusat langkah yang sama memberi") + A.eq("u1_centre_c"))
            + INTERP("In (b) the displacements are a uniform stretch, so the strains, and the stresses, are the same at every point of the element: the centre is not special there. In (c) the extra movement of node 3 alone makes ε<sub>xx</sub> grow with y and adds a shear strain that grows with x, so the stresses vary inside the element. The element next to it, computed from its own nodes, will give different stresses on the shared side; that is why finite element stresses are usually reported at element centres or averaged at the nodes (Part 3).",
                     "Dalam (b), displacement ialah regangan seragam, jadi strain, dan stress, sama pada setiap titik dalam element: pusat tidak istimewa di situ. Dalam (c), pergerakan tambahan node 3 sahaja menjadikan ε<sub>xx</sub> bertambah dengan y dan menambah shear strain yang bertambah dengan x, jadi stress berubah di dalam element. Element di sebelahnya, yang dikira daripada node sendiri, akan memberi stress yang berbeza pada sisi yang dikongsi; sebab itulah stress finite element biasanya dilaporkan pada pusat element atau dipuratakan pada node (Part 3).")
            + SCHEME([("Procedure in the right order, element and local coordinates first", "Prosedur dalam urutan yang betul, element dan koordinat local dahulu", 4), ("Derivatives of u and v", "Derivative bagi u dan v", 2),
                      ("Strains at the centre", "Strain pada pusat", 3), ("Ē, [E] and the stresses at the centre", "Ē, [E] dan stress pada pusat", 3), ("N<sub>i</sub> with the sum check, u and v", "N<sub>i</sub> dengan semakan jumlah, u dan v", 3),
                      ("Strains with the engineering shear, stresses", "Strain dengan engineering shear, stress", 5)], 20))
    X.append(("x1", "Displacements, strains and stresses at a point", "Displacement, strain dan stress pada satu titik", body))

    # ---- Example 2: [E] for plane stress and plane strain (book Practice Problem 9.1, worked in full and extended) ----
    head = ('<div class="xhead"><h2>' + B("Example 2 · Plane stress or plane strain: [E] and what it does", "Contoh 2 · Plane stress atau plane strain: [E] dan kesannya") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> constitutive matrices; stresses for a given strain; the out-of-plane quantity</span><span><b>' + B("Units", "Unit") + '</b> kN, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Practice Problem 9.1 (worked in full and extended)</span><span><b>15 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>For concrete with E = 30 × 10⁶ kN/m² and ν = 0.2: (a) calculate [E] for plane stress and for plane strain and compare their entries. '
         '(b) A strain state ε<sub>xx</sub> = 2 × 10<sup>−4</sup>, ε<sub>yy</sub> = ε<sub>xy</sub> = 0 is imposed. Find σ<sub>xx</sub> and σ<sub>yy</sub> in each idealisation, and (c) the out-of-plane stress or strain that each one implies. '
         '(d) Which idealisation suits a 200 mm shear wall, and which a long retaining wall?</div>')
    body = (head + q
            + PIC("Plane stress leaves the faces free, so the material may contract through the thickness; plane strain forbids that, and the slice must be squeezed by a stress σ<sub>zz</sub>. A material that is held in z resists in-plane stretching more, so expect larger normal entries in plane strain. Shear does not change the volume, so the shear entry should be G in both.",
                  "Plane stress membiarkan muka bebas, jadi bahan boleh mengecut merentasi ketebalan; plane strain melarangnya, dan kepingan itu mesti dihimpit oleh stress σ<sub>zz</sub>. Bahan yang ditahan dalam arah z lebih menahan regangan dalam satah, jadi jangka entri normal lebih besar dalam plane strain. Shear tidak mengubah isi padu, jadi entri shear sepatutnya G dalam kedua-duanya.")
            + PLAN("(a) the two factors → the entries → G as a check; (b) {σ} = [E]{ε}; (c) σ<sub>zz</sub> = 0 with ε<sub>zz</sub> from 3D Hooke, or ε<sub>zz</sub> = 0 with σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>); (d) geometry.")
            + XSTEP(1, "(a) Plane stress", "(a) Plane stress", 3, A.eq("u2_ps"))
            + XSTEP(2, "(a) Plane strain", "(a) Plane strain", 3, A.eq("u2_pe") + A.eq("u2_G")
                    + ANS("(a) Plane stress: 31.25, 6.25, 12.5 × 10⁶; plane strain: 33.33, 8.33, 12.5 × 10⁶ kN/m². Plane strain is stiffer in the normal entries; the shear entry G is the same."))
            + XSTEP(3, "(b) Stresses for the imposed strain", "(b) Stress untuk strain yang dikenakan", 3, A.eq("u2_sig"))
            + XSTEP(4, "(c) The out-of-plane quantity", "(c) Kuantiti luar satah", 4, A.eq("u2_zz")
                    + ANS("(c) Plane stress: σ<sub>zz</sub> = 0 and the plate thins, ε<sub>zz</sub> = −5.0 × 10<sup>−5</sup>. Plane strain: ε<sub>zz</sub> = 0 and σ<sub>zz</sub> = 1667 kN/m² holds the slice at its thickness.")
                    + CHK("Plane-stress ε<sub>zz</sub> equals −ν/(1 − ν)(ε<sub>xx</sub> + ε<sub>yy</sub>) = −0.25 × 2 × 10<sup>−4</sup> = −5.0 × 10<sup>−5</sup>, the same number by a second route."))
            + XSTEP(5, "(d) Choosing the idealisation", "(d) Memilih idealisation", 2, P("The shear wall is thin and loaded in its own plane: plane stress. The retaining wall is long with the same section and the same soil pressure along it: plane strain, per metre run.",
                                                                                  "Shear wall itu nipis dan dibebankan dalam satahnya sendiri: plane stress. Dinding penahan panjang dengan keratan dan tekanan tanah yang sama di sepanjangnya: plane strain, per meter panjang."))
            + INTERP("The two matrices differ only where the thickness direction matters. A strain along x alone makes the plane-strain material push back harder (6667 against 6250 kN/m²), and it also produces a larger lateral stress σ<sub>yy</sub>, because the slice can relieve its Poisson effect neither through the thickness nor sideways. For ν = 0.2 the difference is about 7%; for ν = 0.33 it is 12% in bending, and as ν approaches 0.5 the plane-strain entries grow without bound. Choosing the wrong idealisation is therefore a modelling error of known size, not a numerical one: no mesh refinement removes it.",
                     "Dua matrix itu berbeza hanya di tempat arah ketebalan penting. Strain dalam arah x sahaja menjadikan bahan plane strain menolak balik lebih kuat (6667 berbanding 6250 kN/m²), dan ia juga menghasilkan lateral stress σ<sub>yy</sub> yang lebih besar, kerana kepingan itu tidak dapat melepaskan kesan Poisson-nya sama ada merentasi ketebalan atau ke sisi. Untuk ν = 0.2 perbezaannya kira-kira 7%; untuk ν = 0.33 ia 12% dalam lenturan, dan apabila ν menghampiri 0.5 entri plane strain membesar tanpa had. Memilih idealisation yang salah ialah ralat pemodelan yang saiznya diketahui, bukan ralat berangka: tiada mesh refinement yang dapat menghapuskannya.")
            + SCHEME([("Plane-stress factor and entries", "Faktor dan entri plane stress", 3), ("Plane-strain factor, entries, G check", "Faktor plane strain, entri, semakan G", 3), ("Stresses in both idealisations", "Stress dalam kedua-dua idealisation", 3),
                      ("ε<sub>zz</sub> and σ<sub>zz</sub> with the second-route check", "ε<sub>zz</sub> dan σ<sub>zz</sub> dengan semakan cara kedua", 4), ("Idealisation with its reason", "Idealisation dengan sebabnya", 2)], 15))
    X.append(("x2", "Plane stress or plane strain: [E]", "Plane stress atau plane strain: [E]", body))

    # ---- Example 3: numbering, supports and loads of a plate with a hole (book Example 9.5 a, extended) ----
    head = ('<div class="xhead"><h2>' + B("Example 3 · Numbering, supports and loads of a plate with a hole", "Contoh 3 · Penomboran, support dan beban bagi plat berlubang") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> node, element and dof numbers; connectivity; known dofs; nodal loads; rigid motions</span><span><b>' + B("Units", "Unit") + '</b> symbolic</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 9.5 (a), extended</span><span><b>15 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>The plate of the figure, fixed on its left side and pulled by a uniform traction q (force per unit length, thickness included) on its right side, has a rectangular hole and is modelled by eight four-node elements in three rows of equal height h. '
         '(a) Number the nodes, elements and dofs, and give the connectivity of all elements. (b) Which dofs are known, and how many unknowns remain? (c) Write the non-zero entries of the load vector. '
         '(d) Show that a small rigid rotation produces no strain, and explain what this requires of the supports.</div>')
    body = (head + q + A.fig("fig_ps1_hole", "The plate of Example 3, with the numbering of the answer.", "Plat bagi Contoh 3, dengan penomboran jawapan.", 480)
            + PIC("The numbering is a choice, but a good one keeps the nodes of each element close in number, so that [K] stays narrow: rows of four nodes from the bottom left do that. The hole only means that some nodes belong to fewer elements and that no element spans it. The left side is held in both directions; the right side is a natural boundary loaded in x; top, bottom and the edges of the hole are free.",
                  "Penomboran ialah pilihan, tetapi pilihan yang baik mengekalkan nombor node setiap element berdekatan, supaya [K] kekal sempit: baris empat node dari kiri bawah memenuhinya. Lubang itu hanya bermaksud sesetengah node tergolong dalam lebih sedikit element dan tiada element merentasinya. Sisi kiri ditahan dalam kedua-dua arah; sisi kanan ialah sempadan natural yang dibebankan dalam arah x; atas, bawah dan tepi lubang bebas.")
            + PLAN("Nodes row by row → elements row by row, skipping the hole → connectivity anticlockwise from the lower left → dofs 2i − 1, 2i → supports → edge loads → rigid motions.")
            + XSTEP(1, "(a) Nodes, elements and dofs", "(a) Node, element dan dof", 3, P("Nodes 1–4 along the bottom, then 5–8, 9–12 and 13–16 above them. Elements 1–3 form the bottom row, 4 and 5 lie beside the hole, 6–8 form the top row.",
                                                                                    "Node 1–4 di sepanjang bawah, kemudian 5–8, 9–12 dan 13–16 di atasnya. Element 1–3 membentuk baris bawah, 4 dan 5 terletak di sebelah lubang, 6–8 membentuk baris atas.") + A.eq("u3_dofs"))
            + XSTEP(2, "(a) Connectivity", "(a) Connectivity", 4, '<div class="tbl"><table><tr><th>' + B("element", "element") + '</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th></tr>'
                    + '<tr><td>' + B("local 1", "local 1") + '</td><td>1</td><td>2</td><td>3</td><td>5</td><td>7</td><td>9</td><td>10</td><td>11</td></tr>'
                    + '<tr><td>' + B("local 2", "local 2") + '</td><td>2</td><td>3</td><td>4</td><td>6</td><td>8</td><td>10</td><td>11</td><td>12</td></tr>'
                    + '<tr><td>' + B("local 3", "local 3") + '</td><td>6</td><td>7</td><td>8</td><td>10</td><td>12</td><td>14</td><td>15</td><td>16</td></tr>'
                    + '<tr><td>' + B("local 4", "local 4") + '</td><td>5</td><td>6</td><td>7</td><td>9</td><td>11</td><td>13</td><td>14</td><td>15</td></tr></table></div>'
                    + CHK("Every element lists four distinct nodes anticlockwise from its lower left; nodes 6, 7, 10 and 11 at the corners of the hole each belong to three elements, not four, because the hole takes the fourth place."))
            + XSTEP(3, "(b) Known dofs", "(b) Dof yang diketahui", 3, A.eq("u3_known")
                    + ANS("(b) Dofs 1, 2, 9, 10, 17, 18, 25 and 26 are zero; 24 unknowns remain."))
            + XSTEP(4, "(c) Nodal loads from the traction", "(c) Nodal load daripada traction", 3, P("Each right-hand edge of height h carries qh, shared equally by its two end nodes in the x-direction; nodes 8 and 12 collect a share from two edges:",
                                                                                                  "Setiap tepi kanan setinggi h menanggung qh, dikongsi sama rata oleh dua node hujungnya dalam arah x; node 8 dan 12 mengumpul bahagian daripada dua tepi:") + A.eq("u3_loads")
                    + ANS("(c) r<sub>7</sub> = r<sub>31</sub> = qh/2, r<sub>15</sub> = r<sub>23</sub> = qh, all in x; nothing in y and nothing elsewhere."))
            + XSTEP(5, "(d) Rigid rotation and the supports", "(d) Rigid rotation dan support", 2, A.eq("u3_rigid")
                    + P("A rigid motion needs no force, so [K] is singular unless the supports prevent both translations and the rotation. Here the fixed left side prevents all three; a support of v alone along it would leave the x-translation and a rotation about the edge free.",
                        "Rigid motion tidak memerlukan daya, jadi [K] singular melainkan support menghalang kedua-dua translation dan putaran. Di sini sisi kiri yang fixed menghalang ketiga-tiganya; support v sahaja di sepanjangnya akan membiarkan translation x dan putaran terhadap tepi itu bebas."))
            + INTERP("The hole changes nothing in the procedure: its corner nodes simply belong to fewer elements, no element contributes across it, and its edges are free. With rows of four, the node numbers inside any element differ by at most 5, so in [K] (32 × 32) every non-zero entry K<sub>IJ</sub> has |I − J| ≤ 2 × 5 + 1 = 11: a half-bandwidth of 12 instead of 32. Numbering column by column instead (four columns of four) would give the same here, but on a long plate the rule is to number across the short direction.",
                     "Lubang itu tidak mengubah apa-apa dalam prosedur: node bucunya hanya tergolong dalam lebih sedikit element, tiada element menyumbang merentasinya, dan tepinya bebas. Dengan baris empat node, nombor node dalam mana-mana element berbeza paling banyak 5, jadi dalam [K] (32 × 32) setiap entri bukan sifar K<sub>IJ</sub> ada |I − J| ≤ 2 × 5 + 1 = 11: half-bandwidth 12 dan bukan 32. Menomborkan lajur demi lajur (empat lajur empat node) memberi hasil yang sama di sini, tetapi pada plat panjang peraturannya ialah menomborkan merentasi arah yang pendek.")
            + SCHEME([("Node, element and dof numbering", "Penomboran node, element dan dof", 3), ("Connectivity table", "Connectivity table", 4), ("Known dofs and the count", "Dof yang diketahui dan kiraannya", 3),
                      ("Load shares with the total", "Bahagian beban dengan jumlahnya", 3), ("Rigid rotation and what it requires", "Rigid rotation dan apa yang diperlukannya", 2)], 15))
    X.append(("x3", "Numbering, supports and loads: plate with a hole", "Penomboran, support dan beban: plat berlubang", body))
    return X
