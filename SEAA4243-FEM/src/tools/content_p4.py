"""Content of Plane Stress Part 2 (site part 4): Galerkin for the vector field, [B], the 8 x 8 [k],
nodal loads, assembly with two dofs per node, the cantilever solved and checked.
Numbers are those of deck W12 and the text, recomputed with fe_plane_stress.py (see functest_p4.py)."""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME
from sitelib import QC as _QC
from content_p1 import MCQ as _MCQ

# where the right option sits (the authored lists put it first; spread it over a, b, c)
_POS = {"q1": "b", "q2": "c", "q3": "a", "q4": "b", "q5": "c", "q6": "a", "r1": "c", "r2": "b",
        "a1": "b", "a2": "c", "a3": "a", "a4": "c", "a5": "b", "a6": "a"}


def _place(qid, options, ans):
    pos = _POS.get(qid, ans); keys = "abcd"[:len(options)]
    right = [o for o in options if o[0] == ans]; rest = [o for o in options if o[0] != ans]
    i = keys.index(pos); seq = rest[:i] + right + rest[i:]
    return [(keys[j], e, m) for j, (_, e, m) in enumerate(seq)], pos


def QC(qid, q_en, q_ms, options, ans, fb_en, fb_ms):
    o, a = _place(qid, options, ans); return _QC(qid, q_en, q_ms, o, a, fb_en, fb_ms)


def MCQ(qid, q_en, q_ms, options, ans, fb_en, fb_ms):
    o, a = _place(qid, options, ans); return _MCQ(qid, q_en, q_ms, o, a, fb_en, fb_ms)

PART = {
    "n": 4, "slug": "04-plane-stress-2", "deck": "deck_w12", "eqs": ["eqs_w12", "eqs_w11", "eqs_ps2_ex"], "figs": ["figs_w12", "figs_w11", "figs_ps2_ex"],
    "topic": ("Plane Stress", "Plane Stress"), "part": "Part 2 of 3",
    "title": "Plane Stress — Part 2",
    "sub": ("[B] = [∂]ᵀ[N], the 8 × 8 stiffness matrix [k] = t∫[B]ᵀ[E][B] dA and its twelve closed-form values, nodal loads from tractions and self-weight, "
            "assembly with two dofs per node, and the text’s cantilever solved by hand and checked against beam theory and a refined mesh.",
            "[B] = [∂]ᵀ[N], stiffness matrix 8 × 8 [k] = t∫[B]ᵀ[E][B] dA dan dua belas nilai closed-form-nya, nodal load daripada traction dan self-weight, "
            "assembly dengan dua dof setiap node, dan cantilever dalam teks diselesaikan secara tangan dan disemak dengan beam theory serta mesh yang di-refine."),
    "pdf": "pdf/plane-stress-2-slides.pdf",
    "lab": {"id": "cant", "file": "../labs/cant.html", "name": "Cantilever Explorer", "inclass": "book22"},
    "minutes": {"n1": 8, "n2": 9, "n3": 11, "n4": 7, "n5": 10, "n6": 10},
    "target_min": 35,
    "code": "ps",
    "textref": "§3.2.2–§3.4",
    "covers": ("Plane Stress Part 1 gave the PDE in u and v, the boundary conditions and the 2 × 8 matrix [N]; this part turns them into numbers, exactly as Heat Transfer Part 2 did for temperature. "
               "Galerkin and integration by parts give [k]{û}ᵀ = {q} + {b}; the strain–displacement matrix [B] = [∂]ᵀ[N] puts [k] in the form t∫[B]ᵀ[E][B] dA, whose 64 entries reduce to twelve closed-form values for a rectangle. "
               "Edge tractions and self-weight become nodal loads, the elements are assembled through the dof map, the fixed edge is struck, and the text’s cantilever is solved and judged against beam theory and a refined mesh.",
               "Plane Stress Part 1 memberi PDE dalam u dan v, boundary condition dan matrix 2 × 8 [N]; bahagian ini menukarkannya kepada nombor, sama seperti Heat Transfer Part 2 lakukan untuk temperature. "
               "Galerkin dan integration by parts memberi [k]{û}ᵀ = {q} + {b}; strain–displacement matrix [B] = [∂]ᵀ[N] meletakkan [k] dalam bentuk t∫[B]ᵀ[E][B] dA, dan 64 entrinya menjadi dua belas nilai closed-form bagi segi empat tepat. "
               "Traction tepi dan self-weight menjadi nodal load, element di-assemble melalui dof map, tepi yang fixed dibuang, dan cantilever dalam teks diselesaikan serta dinilai berbanding beam theory dan mesh yang di-refine."),
    "inclass_n": ("3 h · 6 activities", "3 jam · 6 aktiviti"),
    "inclass": [("A1 [B] at a point · A2 s₁, s₂, s₃ of the cantilever element", "A1 [B] pada satu titik · A2 s₁, s₂, s₃ bagi element cantilever"),
                ("A3 the global load vector · A4 assembly entries · A5 reading the solution", "A3 global load vector · A4 entri assembly · A5 membaca penyelesaian"),
                ("A6 the coarse-mesh error and the mesh for 1%", "A6 ralat mesh kasar dan mesh untuk 1%")],
    "recall_title": ("Recall from Plane Stress Part 1", "Ingat semula Plane Stress Part 1"),
}

OUTCOMES = [
    ("Apply Galerkin and integration by parts to the plane-stress PDE, identify [k], {q} and {b}, and write [B] = [∂]ᵀ[N] and [k] = t∫[B]ᵀ[E][B] dA.",
     "Menggunakan Galerkin dan integration by parts pada PDE plane stress, mengenal pasti [k], {q} dan {b}, dan menulis [B] = [∂]ᵀ[N] serta [k] = t∫[B]ᵀ[E][B] dA."),
    ("Evaluate the 8 × 8 stiffness matrix of a four-node rectangular element from the closed-form entries s<sub>1</sub>…s<sub>12</sub>, and check it.",
     "Menilai stiffness matrix 8 × 8 bagi four-node rectangular element daripada entri closed-form s<sub>1</sub>…s<sub>12</sub>, dan menyemaknya."),
    ("Convert edge tractions and body forces into equivalent nodal loads, assemble the global system with two dofs per node and impose displacement conditions.",
     "Menukar traction tepi dan body force kepada nodal load yang setara, meng-assemble sistem global dengan dua dof setiap node dan mengenakan displacement condition."),
    ("Solve the 2 × 2 cantilever, check its reactions, compare it with beam theory and a refined mesh, and explain why the coarse mesh is too stiff.",
     "Menyelesaikan cantilever 2 × 2, menyemak reaction-nya, membandingkannya dengan beam theory dan mesh yang di-refine, dan menerangkan mengapa mesh kasar terlalu stiff."),
]

CANDO = [
    ("Write [B] for a rectangle and fill it with numbers at a point; say why each row adds up to zero.", "Menulis [B] bagi segi empat tepat dan mengisinya dengan nombor pada satu titik; menyatakan mengapa setiap baris berjumlah sifar."),
    ("Compute s<sub>1</sub>…s<sub>12</sub> for any a, b, E, ν, t, place them in [k] and check a row.", "Mengira s<sub>1</sub>…s<sub>12</sub> untuk sebarang a, b, E, ν, t, meletakkannya dalam [k] dan menyemak satu baris."),
    ("Turn a uniform or linearly varying edge load and a self-weight into nodal loads in the right dofs.", "Menukar edge load yang seragam atau berubah secara linear dan self-weight kepada nodal load pada dof yang betul."),
    ("Find any global entry K<sub>IJ</sub> from the dof map, and check a solution by its reactions and by beam theory.", "Mencari mana-mana entri global K<sub>IJ</sub> daripada dof map, dan menyemak penyelesaian melalui reaction-nya dan beam theory."),
]


def notes(A):
    S = []
    # ---- n1: Galerkin and integration by parts ----
    body = (
        P("Plane Stress Part 1 ended with two results: the PDE [∂][E][∂]ᵀ{u}ᵀ = −{f} and the interpolation {u}ᵀ = [N]{û}ᵀ with the 2 × 8 matrix [N]. Substitute the second into the first and, as in Heat Transfer Part 2, it does not balance: a bilinear displacement field cannot satisfy two second-order equations at every point.",
          "Plane Stress Part 1 berakhir dengan dua hasil: PDE [∂][E][∂]ᵀ{u}ᵀ = −{f} dan interpolation {u}ᵀ = [N]{û}ᵀ dengan matrix 2 × 8 [N]. Gantikan yang kedua ke dalam yang pertama dan, seperti dalam Heat Transfer Part 2, ia tidak seimbang: displacement field bilinear tidak mampu memenuhi dua persamaan peringkat kedua pada setiap titik.")
        + A.eq("r_subst", "(3.31)")
        + DEF("Galerkin, vector version", "Galerkin, versi vector",
              "Weight the residual with [N]ᵀ, the transpose of the interpolation matrix, and ask that each weighted average be zero. [N]ᵀ is 8 × 2, so one element gives eight equations, one per degree of freedom: u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.",
              "Weight residual itu dengan [N]ᵀ, iaitu transpose matrix interpolation, dan minta supaya setiap purata ber-weight itu sifar. [N]ᵀ ialah 8 × 2, jadi satu element memberi lapan persamaan, satu setiap degree of freedom: u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.")
        + A.eq("r_weighted", "(3.32)")
        + H3("Integration by parts, then name the terms", "Integration by parts, kemudian namakan term")
        + SB(P("Exactly as for heat, one [∂] moves from the displacements onto the weight [N]ᵀ (Green’s theorem, applied to each row). The derivative order falls to one, so a bilinear field is admissible, and a boundary integral appears that carries the traction, the natural condition of Plane Stress Part 1.",
               "Sama seperti haba, satu [∂] berpindah daripada displacement kepada weight [N]ᵀ (teorem Green, digunakan pada setiap baris). Peringkat derivative turun kepada satu, jadi field bilinear boleh diterima, dan satu integral sempadan muncul yang membawa traction, iaitu natural condition dalam Plane Stress Part 1."))
        + A.eq("r_rearr", "(3.34)–(3.38)") + A.eq("r_sys", "(3.38)")
        + '<div class="tbl"><table><tr><th>' + B("Term", "Term") + '</th><th>' + B("Name", "Nama") + '</th><th>' + B("What it holds", "Apa yang dikandunginya") + '</th><th>' + B("Heat analogue", "Analog haba") + '</th></tr>'
        + '<tr><td>[k]</td><td>stiffness matrix</td><td>' + B("material, geometry and thickness of the element; symmetric; 8 × 8", "bahan, geometri dan ketebalan element; simetri; 8 × 8") + '</td><td>' + B("conductance matrix, 4 × 4", "conductance matrix, 4 × 4") + '</td></tr>'
        + '<tr><td>{q}</td><td>' + B("body-force vector", "body-force vector") + '</td><td>' + B("forces per unit volume inside the element (self-weight), shared among its nodes", "daya per unit isi padu di dalam element (self-weight), dikongsi antara node-nya") + '</td><td>' + B("source vector", "source vector") + '</td></tr>'
        + '<tr><td>{b}</td><td>' + B("traction vector", "traction vector") + '</td><td>' + B("forces on edges with a known traction; zero on free edges; discarded with the equation on fixed edges", "daya pada tepi dengan traction diketahui; sifar pada tepi bebas; dibuang bersama persamaan pada tepi fixed") + '</td><td>' + B("boundary-flux vector", "boundary-flux vector") + '</td></tr></table></div>'
        + NOTE("Which edges of the cantilever contribute to {b}?", "Tepi cantilever mana yang menyumbang kepada {b}?",
               "Only the free end, x = 4 m, with its downward traction. The top and bottom edges are free (b<sub>x</sub> = b<sub>y</sub> = 0), so their boundary term vanishes. On the fixed edge the traction is unknown, but it multiplies the shape functions of nodes whose equations are struck when u = v = 0 is imposed; it comes back afterwards as the support reactions, just as the heat flow did at a prescribed temperature.",
               "Hanya hujung bebas, x = 4 m, dengan traction ke bawah. Tepi atas dan bawah bebas (b<sub>x</sub> = b<sub>y</sub> = 0), jadi boundary term-nya lenyap. Pada tepi fixed traction tidak diketahui, tetapi ia mendarab shape function bagi node yang persamaannya dibuang apabila u = v = 0 dikenakan; ia kembali kemudian sebagai support reaction, sama seperti aliran haba pada temperature yang ditetapkan.")
        + KP([("Weight the residual with [N]ᵀ: eight equations per four-node element.", "Weight residual dengan [N]ᵀ: lapan persamaan setiap four-node element."),
              ("Integration by parts lowers the derivative order and exposes the traction as the natural condition.", "Integration by parts merendahkan peringkat derivative dan mendedahkan traction sebagai natural condition."),
              ("[k]{û}ᵀ = {q} + {b} = {r}: stiffness, body force, traction; the same structure as heat with two unknowns per node.", "[k]{û}ᵀ = {q} + {b} = {r}: stiffness, body force, traction; struktur yang sama seperti haba dengan dua unknown setiap node.")])
        + QC("q1", "Weighting the plane-stress residual with [N]ᵀ gives, for one four-node element,", "Weight residual plane stress dengan [N]ᵀ memberi, bagi satu four-node element,",
             [("a", "eight equations, one per degree of freedom", "lapan persamaan, satu setiap degree of freedom"), ("b", "four equations, one per node", "empat persamaan, satu setiap node"), ("c", "two equations, one per direction", "dua persamaan, satu setiap arah")],
             "a", "[N]ᵀ is 8 × 2 and the residual is 2 × 1, so the weighted residual is an 8 × 1 vector: one equation for each of u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>. Heat transfer gave four, one per node, because it had one unknown per node.",
             "[N]ᵀ ialah 8 × 2 dan residual ialah 2 × 1, jadi weighted residual ialah vector 8 × 1: satu persamaan bagi setiap u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>. Heat transfer memberi empat, satu setiap node, kerana ia ada satu unknown setiap node.")
    )
    S.append(("n1", "Galerkin and integration by parts, two unknowns per node", "Galerkin dan integration by parts, dua unknown setiap node", body))

    # ---- n2: [B] and [k] = t∫[B]ᵀ[E][B] dA ----
    body = (
        P("In heat transfer the 2 × 4 matrix {∂}ᵀ{N} turned the nodal temperatures into the gradient. Its plane-stress counterpart turns the eight nodal displacements into the three strains, and it has a name of its own: the strain–displacement matrix [B].",
          "Dalam heat transfer, matrix 2 × 4 {∂}ᵀ{N} menukar nodal temperature kepada gradient. Padanannya dalam plane stress menukar lapan nodal displacement kepada tiga strain, dan ia ada nama sendiri: strain–displacement matrix [B].")
        + A.eq("r_B_def") + A.eq("r_B")
        + SB(LI([("Row 1 (ε<sub>xx</sub> = ∂u/∂x): ∂N<sub>i</sub>/∂x under each u<sub>i</sub>, zero under each v<sub>i</sub>.", "Baris 1 (ε<sub>xx</sub> = ∂u/∂x): ∂N<sub>i</sub>/∂x di bawah setiap u<sub>i</sub>, sifar di bawah setiap v<sub>i</sub>."),
                 ("Row 2 (ε<sub>yy</sub> = ∂v/∂y): ∂N<sub>i</sub>/∂y under each v<sub>i</sub>, zero under each u<sub>i</sub>.", "Baris 2 (ε<sub>yy</sub> = ∂v/∂y): ∂N<sub>i</sub>/∂y di bawah setiap v<sub>i</sub>, sifar di bawah setiap u<sub>i</sub>."),
                 ("Row 3 (ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x, the engineering shear strain): ∂N<sub>i</sub>/∂y under u<sub>i</sub> and ∂N<sub>i</sub>/∂x under v<sub>i</sub>.", "Baris 3 (ε<sub>xy</sub> = ∂u/∂y + ∂v/∂x, engineering shear strain): ∂N<sub>i</sub>/∂y di bawah u<sub>i</sub> dan ∂N<sub>i</sub>/∂x di bawah v<sub>i</sub>.")]))
        + NOTE("Nothing new is computed", "Tiada yang baharu dikira",
               "Every entry of [B] is a shape-function derivative from Heat Transfer Part 1: ∂N<sub>1</sub>/∂x = −(b − y)/(ab) = (y − b)/(ab), and so on. [B] only arranges them so that u and v are differentiated together.",
               "Setiap entri [B] ialah derivative shape function daripada Heat Transfer Part 1: ∂N<sub>1</sub>/∂x = −(b − y)/(ab) = (y − b)/(ab), dan seterusnya. [B] hanya menyusunnya supaya u dan v dibezakan serentak.")
        + STEP("Worked step · [B] at (1.5, 0.3) of a 2 m × 1 m element (Activity 1)", "Langkah bekerja · [B] pada (1.5, 0.3) bagi element 2 m × 1 m (Aktiviti 1)",
               P("The derivatives are those of the Heat Transfer Part 1 point: ∂N<sub>i</sub>/∂x = {−0.35, 0.35, 0.15, −0.15} and ∂N<sub>i</sub>/∂y = {−0.25, −0.75, 0.75, 0.25} m<sup>−1</sup>. Place them in the three rows:",
                 "Derivative-nya ialah derivative titik Heat Transfer Part 1: ∂N<sub>i</sub>/∂x = {−0.35, 0.35, 0.15, −0.15} dan ∂N<sub>i</sub>/∂y = {−0.25, −0.75, 0.75, 0.25} m<sup>−1</sup>. Letakkannya dalam tiga baris:")
               + A.eq("v0_Bnum")
               + P("Each row adds up to zero, and in row 3 the u-entries and the v-entries add up to zero separately. The reason is physical: a rigid translation (all u<sub>i</sub> equal, all v<sub>i</sub> equal) produces no strain. Keep this [B]; Plane Stress Part 3 multiplies it by the nodal displacements to get the stresses.",
                   "Setiap baris berjumlah sifar, dan dalam baris 3 entri u dan entri v masing-masing berjumlah sifar. Sebabnya fizikal: translation tegar (semua u<sub>i</sub> sama, semua v<sub>i</sub> sama) tidak menghasilkan strain. Simpan [B] ini; Plane Stress Part 3 mendarabnya dengan nodal displacement untuk mendapatkan stress."))
        + H3("The element stiffness matrix in [B] form", "Element stiffness matrix dalam bentuk [B]")
        + SB(P("Integration by parts left the product [N]ᵀ[∂] on the left and [∂]ᵀ[N] on the right of [E]. Both are [B] (the left one transposed), so the stiffness matrix is the same [B] twice with the material between:",
               "Integration by parts meninggalkan hasil darab [N]ᵀ[∂] di kiri dan [∂]ᵀ[N] di kanan [E]. Kedua-duanya ialah [B] (yang kiri di-transpose), jadi stiffness matrix ialah [B] yang sama dua kali dengan bahan di antaranya:"))
        + A.eq("r_kB")
        + LI([("<b>Thickness.</b> The integrals are per unit thickness; the element has thickness t, so every entry of [k] and every load is multiplied by t.", "<b>Ketebalan.</b> Integral itu per unit ketebalan; element mempunyai ketebalan t, jadi setiap entri [k] dan setiap load didarab dengan t."),
              ("<b>Symmetry.</b> [B]ᵀ[E][B] is symmetric whenever [E] is, and integration keeps it so: at most 36 distinct entries, and for a rectangle only twelve (§3).", "<b>Simetri.</b> [B]ᵀ[E][B] simetri apabila [E] simetri, dan integration mengekalkannya: paling banyak 36 entri berbeza, dan bagi segi empat tepat hanya dua belas (§3)."),
              ("<b>Meaning.</b> k<sub>ij</sub> is the force at dof i needed to give dof j a unit displacement with every other dof held: the stiffness influence coefficient of structural analysis.", "<b>Maksud.</b> k<sub>ij</sub> ialah daya pada dof i yang diperlukan untuk memberi dof j satu unit displacement dengan setiap dof lain ditahan: stiffness influence coefficient dalam analisis struktur.")])
        + H3("How software integrates [k]", "Bagaimana perisian meng-integrate [k]")
        + '<figure><img src="slides/img/w12_gauss.png" alt="A four-node element with corners at (1,2), (8,0), (9,4) and (4,5) and its four Gauss points marked inside it" class="figimg" style="width:min(460px,100%)"><figcaption>'
        + B("Software evaluates t[B]ᵀ[E][B] × det J at four Gauss points, ξ, η = ±1/√3, and adds them. For a rectangle the integrand is quadratic in each direction and the four-point sum equals the closed form of §3 exactly; for a distorted element like this one numerical integration is the only route.",
            "Perisian menilai t[B]ᵀ[E][B] × det J pada empat Gauss point, ξ, η = ±1/√3, dan menjumlahkannya. Bagi segi empat tepat integrand-nya quadratic dalam setiap arah dan jumlah empat titik itu sama dengan closed form §3 secara tepat; bagi element yang herot seperti ini, numerical integration ialah satu-satunya cara.")
        + '<span class="credit"> Image: PyMAPDL documentation, “Build a finite element model”, © ANSYS, Inc., MIT licence.</span></figcaption></figure>'
        + KP([("[B] = [∂]ᵀ[N], 3 × 8: strains from nodal displacements; every row adds up to zero.", "[B] = [∂]ᵀ[N], 3 × 8: strain daripada nodal displacement; setiap baris berjumlah sifar."),
              ("[k] = t∫[B]ᵀ[E][B] dA, 8 × 8, symmetric; k<sub>ij</sub> = force at i per unit displacement at j.", "[k] = t∫[B]ᵀ[E][B] dA, 8 × 8, simetri; k<sub>ij</sub> = daya pada i per unit displacement pada j."),
              ("Software integrates at 2 × 2 Gauss points; for a rectangle that is exact.", "Perisian meng-integrate pada 2 × 2 Gauss point; bagi segi empat tepat ia tepat.")])
        + QC("q2", "Why must every row of [B] add up to zero?", "Mengapa setiap baris [B] mesti berjumlah sifar?",
             [("a", "A rigid translation of the element produces no strain", "Translation tegar element tidak menghasilkan strain"), ("b", "Because [B] is symmetric", "Kerana [B] simetri"), ("c", "Because each shape function is 1 at its own node", "Kerana setiap shape function bernilai 1 pada node sendiri")],
             "a", "Giving every node the same u (or the same v) moves the element without deforming it, so [B]{û}ᵀ must be zero; that is a sum of the u-entries (or the v-entries) of each row. [B] is 3 × 8 and cannot be symmetric; the Kronecker property is true but is not the reason.",
             "Memberi setiap node u yang sama (atau v yang sama) menggerakkan element tanpa mengubah bentuknya, jadi [B]{û}ᵀ mesti sifar; itu ialah jumlah entri u (atau entri v) bagi setiap baris. [B] ialah 3 × 8 dan tidak boleh simetri; sifat Kronecker itu benar tetapi bukan sebabnya.")
    )
    S.append(("n2", "The strain–displacement matrix [B] and the stiffness matrix", "Strain–displacement matrix [B] dan stiffness matrix", body))

    # ---- n3: the 8 x 8 [k] ----
    body = (
        P("One entry in full is enough to see how all of them are made. Take k<sub>34</sub>: row 3 belongs to u<sub>2</sub> and column 4 to v<sub>2</sub>, so it couples the horizontal and the vertical displacement of the same node.",
          "Satu entri secara penuh sudah cukup untuk melihat bagaimana semuanya dibina. Ambil k<sub>34</sub>: baris 3 milik u<sub>2</sub> dan lajur 4 milik v<sub>2</sub>, jadi ia menggandingkan displacement mendatar dan menegak bagi node yang sama.")
        + STEP("k₃₄ in three steps (text (3.39)–(3.41))", "k₃₄ dalam tiga langkah (teks (3.39)–(3.41))",
               A.eq("r_s1", "(3.39)") + A.eq("r_s2", "(3.40)") + A.eq("r_s3", "(3.41)") + A.eq("r_s3b")
               + P("The integral of −x(b − y)/(a²b²) over the rectangle is −1/4, so k<sub>34</sub> does not depend on a or b: the coupling between u and v at a node is the same for every rectangle. The text writes the result as Et/(8(ν − 1)).",
                   "Integral −x(b − y)/(a²b²) atas segi empat tepat ialah −1/4, jadi k<sub>34</sub> tidak bergantung pada a atau b: gandingan antara u dan v pada satu node adalah sama bagi setiap segi empat tepat. Teks menulis hasilnya sebagai Et/(8(ν − 1))."))
        + H3("Twelve values, one pattern", "Dua belas nilai, satu pola")
        + SB(P("Repeating the integration for the other entries gives only twelve distinct values, arranged by the symmetry of the rectangle. Rows 1, 3, 5, 7 belong to u<sub>1</sub>…u<sub>4</sub> and rows 2, 4, 6, 8 to v<sub>1</sub>…v<sub>4</sub>; k<sub>34</sub> is s<sub>6</sub>. You do not memorise the pattern: you read it correctly from the text.",
               "Mengulang integration untuk entri lain hanya memberi dua belas nilai berbeza, disusun mengikut simetri segi empat tepat. Baris 1, 3, 5, 7 milik u<sub>1</sub>…u<sub>4</sub> dan baris 2, 4, 6, 8 milik v<sub>1</sub>…v<sub>4</sub>; k<sub>34</sub> ialah s<sub>6</sub>. Anda tidak perlu menghafal pola ini: anda membacanya dengan betul daripada teks."))
        + A.eq("r_kfull", "(3.42)") + A.eq("r_svals_a") + A.eq("r_svals_b")
        + NOTE("How to read the twelve values", "Cara membaca dua belas nilai itu",
               "s<sub>1</sub>, s<sub>3</sub>, s<sub>5</sub>, s<sub>7</sub> couple u with u: they are the heat conductance values with k<sub>x</sub> = Et/(1 − ν²) and k<sub>y</sub> = Gt (stretching along x, shearing along y). s<sub>9</sub>…s<sub>12</sub> couple v with v, the same with a and b swapped. s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> couple u with v and contain no a or b.",
               "s<sub>1</sub>, s<sub>3</sub>, s<sub>5</sub>, s<sub>7</sub> menggandingkan u dengan u: ia nilai conductance haba dengan k<sub>x</sub> = Et/(1 − ν²) dan k<sub>y</sub> = Gt (regangan sepanjang x, shear sepanjang y). s<sub>9</sub>…s<sub>12</sub> menggandingkan v dengan v, sama tetapi a dan b ditukar. s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> menggandingkan u dengan v dan tidak mengandungi a atau b.")
        + STEP("Worked example · the cantilever element (Activity 2, text (3.44))", "Contoh bekerja · element cantilever (Aktiviti 2, teks (3.44))",
               P("a = 2 m, b = 1 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, so 1 − ν² = 0.8911:", "a = 2 m, b = 1 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, jadi 1 − ν² = 0.8911:")
               + A.eq("r_act2") + _ktable(K344, "[k] of the cantilever element × 10⁶ N m<sup>−1</sup>, text (3.44); rows and columns in the dof order u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.", "[k] element cantilever × 10⁶ N m<sup>−1</sup>, teks (3.44); baris dan lajur mengikut susunan dof u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.")
               + P("All four elements of the 2 × 2 mesh have the same a, b and material, so this one matrix serves the whole mesh. The entries ±0.003 (s<sub>4</sub>, s<sub>8</sub>) are small because 1 − 3ν = 0.01 for ν = 0.33.",
                   "Keempat-empat element mesh 2 × 2 mempunyai a, b dan bahan yang sama, jadi satu matrix ini mencukupi untuk seluruh mesh. Entri ±0.003 (s<sub>4</sub>, s<sub>8</sub>) kecil kerana 1 − 3ν = 0.01 bagi ν = 0.33."))
        + OK("Checks on any [k] you compute", "Semakan pada mana-mana [k] yang anda kira",
             "Symmetric. In every row the u-entries add up to zero and so do the v-entries: a rigid translation in x or in y needs no force. A rigid rotation also gives [k]{d} = {0}. These three zero-energy modes make [k], and an unsupported [K], singular until the supports prevent them.",
             "Simetri. Dalam setiap baris entri u berjumlah sifar dan begitu juga entri v: translation tegar dalam x atau y tidak memerlukan daya. Rotation tegar juga memberi [k]{d} = {0}. Tiga zero-energy mode ini menjadikan [k], dan [K] tanpa support, singular sehingga support menghalangnya.")
        + A.eq("r_rowsum")
        + NOTE("The usual traps", "Perangkap biasa",
               "Plane strain [E] used where plane stress is asked (or the reverse); a and b swapped between s<sub>1</sub> and s<sub>9</sub>; a sign lost in s<sub>4</sub> = −s<sub>8</sub> or s<sub>6</sub> = −s<sub>2</sub>. The row-sum check catches only the lost sign: the other two give a matrix that is wrong but still balanced, so settle Ē = E/(1 − ν²) and which side is a before computing anything.",
               "[E] plane strain digunakan apabila plane stress diminta (atau sebaliknya); a dan b tertukar antara s<sub>1</sub> dan s<sub>9</sub>; tanda hilang dalam s<sub>4</sub> = −s<sub>8</sub> atau s<sub>6</sub> = −s<sub>2</sub>. Semakan jumlah baris hanya menangkap tanda yang hilang: dua yang lain memberi matrix yang salah tetapi masih seimbang, jadi tetapkan Ē = E/(1 − ν²) dan sisi mana a sebelum mengira apa-apa.")
        + KP([("Twelve values s<sub>1</sub>…s<sub>12</sub> in the pattern (3.42); the u–v couplings do not depend on a or b.", "Dua belas nilai s<sub>1</sub>…s<sub>12</sub> dalam pola (3.42); gandingan u–v tidak bergantung pada a atau b."),
              ("Cantilever element: k<sub>11</sub> = s<sub>1</sub> = 0.875 × 10⁶, s<sub>2</sub> = 0.373 × 10⁶, s<sub>9</sub> = 1.622 × 10⁶ N m<sup>−1</sup>.", "Element cantilever: k<sub>11</sub> = s<sub>1</sub> = 0.875 × 10⁶, s<sub>2</sub> = 0.373 × 10⁶, s<sub>9</sub> = 1.622 × 10⁶ N m<sup>−1</sup>."),
              ("u-entries and v-entries of every row sum to zero; three zero-energy modes.", "Entri u dan entri v setiap baris berjumlah sifar; tiga zero-energy mode.")])
        + QC("q3", "For ν = 1/3, the entries s<sub>4</sub> and s<sub>8</sub> of a rectangle are", "Bagi ν = 1/3, entri s<sub>4</sub> dan s<sub>8</sub> bagi segi empat tepat ialah",
             [("a", "zero", "sifar"), ("b", "equal to s<sub>2</sub>", "sama dengan s<sub>2</sub>"), ("c", "the largest entries of [k]", "entri terbesar dalam [k]")],
             "a", "s<sub>8</sub> = −s<sub>4</sub> = Et(1 − 3ν)/(8(1 − ν²)), and 1 − 3ν = 0 at ν = 1/3. That is why the cantilever element (ν = 0.33) shows only ±0.003 × 10⁶ there.",
             "s<sub>8</sub> = −s<sub>4</sub> = Et(1 − 3ν)/(8(1 − ν²)), dan 1 − 3ν = 0 pada ν = 1/3. Sebab itulah element cantilever (ν = 0.33) hanya menunjukkan ±0.003 × 10⁶ di situ.")
    )
    S.append(("n3", "The 8 × 8 stiffness matrix and its twelve values", "Stiffness matrix 8 × 8 dan dua belas nilainya", body))

    # ---- n4: loads ----
    body = (
        P("The load vector follows the same rule as in heat transfer, now in the plane-stress dof order: along an edge only the shape functions of its two nodes are non-zero, and along that edge they are the linear functions of a bar. A uniform load is therefore shared equally by the two nodes, in the direction it acts and nowhere else.",
          "Load vector mengikut peraturan yang sama seperti heat transfer, kini dalam susunan dof plane stress: di sepanjang satu tepi hanya shape function dua node-nya yang bukan sifar, dan di sepanjang tepi itu ia fungsi linear bar. Load yang seragam oleh itu dikongsi sama rata oleh dua node, dalam arah ia bertindak dan tidak di tempat lain.")
        + A.fig("fig_edge_traction", "A uniform downward traction on edge 2–3 loads v<sub>2</sub> and v<sub>3</sub> equally.", "Traction seragam ke bawah pada tepi 2–3 membebankan v<sub>2</sub> dan v<sub>3</sub> secara sama rata.", 440)
        + A.eq("r_bedge") + A.eq("r_r2", "(3.45)")
        + NOTE("Per length or per area?", "Per panjang atau per luas?",
               "The text gives q<sub>y</sub> = −5 kN m<sup>−1</sup>: a load per unit length of edge for the whole thickness. A traction in kN m<sup>−2</sup> must be multiplied by t first. In (3.45) the t of the integral cancels the 1/t of q<sub>y</sub>/t, which is why the thickness disappears from the result.",
               "Teks memberi q<sub>y</sub> = −5 kN m<sup>−1</sup>: load per unit panjang tepi untuk seluruh ketebalan. Traction dalam kN m<sup>−2</sup> mesti didarab dengan t dahulu. Dalam (3.45), t daripada integral membatalkan 1/t daripada q<sub>y</sub>/t, sebab itulah ketebalan hilang daripada hasilnya.")
        + H3("A linearly varying edge load", "Edge load yang berubah secara linear")
        + SB(P("If the load per unit length varies from p<sub>i</sub> at one node to p<sub>j</sub> at the other, the node at the heavier end takes more. The shares are those of the bar element, and their total and their moment about either node are the two checks:",
               "Jika load per unit panjang berubah daripada p<sub>i</sub> pada satu node kepada p<sub>j</sub> pada node yang lain, node di hujung yang lebih berat menerima lebih. Bahagiannya sama seperti bar element, dan jumlahnya serta momennya terhadap mana-mana node ialah dua semakan:"))
        + A.eq("v0_lin")
        + H3("Body force: self-weight", "Body force: self-weight")
        + SB(P("A uniform body force is shared by all four nodes, a quarter each, because every N<sub>i</sub> integrates to ab/4. Self-weight, f<sub>y</sub> = −ρg = −γ (unit weight γ), acts in −y, so it loads only the v-dofs:", "Body force yang seragam dikongsi oleh keempat-empat node, satu perempat setiap satu, kerana setiap N<sub>i</sub> ber-integral kepada ab/4. Self-weight, f<sub>y</sub> = −ρg = −γ (berat unit γ), bertindak dalam −y, jadi ia hanya membebankan dof v:"))
        + A.eq("r_body")
        + STEP("Worked example · the global load vector of the cantilever (Activity 3, text (3.47))", "Contoh bekerja · global load vector cantilever (Aktiviti 3, teks (3.47))",
               A.fig("fig_ps_mesh", "The 2 × 2 mesh: node n carries U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y).", "Mesh 2 × 2: node n membawa U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y).", 420)
               + P("Elements 2 (nodes 2, 3, 6, 5) and 4 (nodes 5, 6, 9, 8) have their side 2–3 on the free end. Each puts −2500 N on its local v<sub>2</sub> and v<sub>3</sub>, which are global U<sub>6</sub>, U<sub>12</sub> for element 2 and U<sub>12</sub>, U<sub>18</sub> for element 4. Node 6 is shared, so U<sub>12</sub> collects −5000 N: the full 5 kN m<sup>−1</sup> × 1 m of edge around it.",
                   "Element 2 (node 2, 3, 6, 5) dan 4 (node 5, 6, 9, 8) mempunyai sisi 2–3 pada hujung bebas. Setiap satu meletakkan −2500 N pada v<sub>2</sub> dan v<sub>3</sub> local-nya, iaitu U<sub>6</sub>, U<sub>12</sub> global bagi element 2 dan U<sub>12</sub>, U<sub>18</sub> bagi element 4. Node 6 dikongsi, jadi U<sub>12</sub> mengumpul −5000 N: keseluruhan 5 kN m<sup>−1</sup> × 1 m tepi di sekelilingnya.")
               + A.eq("r_R", "(3.47)")
               + P("The six entries B<sub>i</sub> at the fixed dofs 1, 2, 7, 8, 13 and 14 are the unknown support reactions. The total applied load is −10 000 N, which the reactions must balance.",
                   "Enam entri B<sub>i</sub> pada dof fixed 1, 2, 7, 8, 13 dan 14 ialah support reaction yang tidak diketahui. Jumlah load yang dikenakan ialah −10 000 N, yang mesti diimbangi oleh reaction."))
        + KP([("Uniform edge load: p ℓ/2 at each of the two edge nodes, only in the dofs of its direction.", "Edge load seragam: p ℓ/2 pada setiap satu daripada dua node tepi, hanya pada dof arahnya."),
              ("Linearly varying: ℓ(2p<sub>i</sub> + p<sub>j</sub>)/6 and ℓ(p<sub>i</sub> + 2p<sub>j</sub>)/6; self-weight: γtab/4 in each v-dof.", "Berubah secara linear: ℓ(2p<sub>i</sub> + p<sub>j</sub>)/6 dan ℓ(p<sub>i</sub> + 2p<sub>j</sub>)/6; self-weight: γtab/4 pada setiap dof v."),
              ("Cantilever: R<sub>6</sub> = R<sub>18</sub> = −2500 N, R<sub>12</sub> = −5000 N; six unknown reactions.", "Cantilever: R<sub>6</sub> = R<sub>18</sub> = −2500 N, R<sub>12</sub> = −5000 N; enam reaction yang tidak diketahui.")])
        + QC("q4", "The self-weight of an element a × b of thickness t and unit weight γ is shared as", "Self-weight bagi element a × b dengan ketebalan t dan berat unit γ dikongsi sebagai",
             [("a", "−γtab/4 in each of the four v-dofs", "−γtab/4 pada setiap satu daripada empat dof v"), ("b", "−γtab/2 at the two bottom nodes", "−γtab/2 pada dua node bawah"), ("c", "−γtab/8 in all eight dofs", "−γtab/8 pada kesemua lapan dof")],
             "a", "Each shape function integrates to ab/4, so each node carries a quarter of the weight γtab, and the weight acts in −y: only v<sub>1</sub>…v<sub>4</sub> are loaded. Putting it all on the bottom nodes, or into the u-dofs, changes the load the element feels.",
             "Setiap shape function ber-integral kepada ab/4, jadi setiap node membawa satu perempat berat γtab, dan berat itu bertindak dalam −y: hanya v<sub>1</sub>…v<sub>4</sub> dibebankan. Meletakkan semuanya pada node bawah, atau pada dof u, mengubah load yang dirasai element.")
    )
    S.append(("n4", "Loads: edge tractions and body forces", "Load: traction tepi dan body force", body))

    # ---- n5: assembly, supports, solution ----
    body = (
        P("Assembly is the heat-transfer scatter-add with one extra step: node numbers become dof numbers. Node n owns U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y), so each element’s four nodes give eight global dofs, in local order.",
          "Assembly ialah scatter-add heat transfer dengan satu langkah tambahan: nombor node menjadi nombor dof. Node n memiliki U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y), jadi empat node setiap element memberi lapan dof global, mengikut susunan local.")
        + A.eq("r_dofmap")
        + '<div class="tbl"><table><tr><th>' + B("Element", "Element") + '</th><th>' + B("Nodes (1)(2)(3)(4)", "Node (1)(2)(3)(4)") + '</th><th>' + B("Dofs in local order 1…8", "Dof mengikut susunan local 1…8") + '</th></tr>'
        + '<tr><td>1</td><td class="num">1, 2, 5, 4</td><td class="num">1 2 · 3 4 · 9 10 · 7 8</td></tr><tr><td>2</td><td class="num">2, 3, 6, 5</td><td class="num">3 4 · 5 6 · 11 12 · 9 10</td></tr>'
        + '<tr><td>3</td><td class="num">4, 5, 8, 7</td><td class="num">7 8 · 9 10 · 15 16 · 13 14</td></tr><tr><td>4</td><td class="num">5, 6, 9, 8</td><td class="num">9 10 · 11 12 · 17 18 · 15 16</td></tr></table></div>'
        + A.eq("r_scatter")
        + '<figure><img src="slides/img/fig_Kmap.png" alt="An 18 by 18 grid showing which element contributes to each entry of the assembled stiffness matrix; shared entries are marked with the number of contributing elements" class="figimg" style="width:min(420px,100%)"><figcaption>'
        + B("Which elements fill each entry of the 18 × 18 [K]. The rows of node 5 (U<sub>9</sub>, U<sub>10</sub>) are shared by all four elements; node 1 and node 9 never meet, so their entries stay zero.",
            "Element mana yang mengisi setiap entri [K] 18 × 18. Baris node 5 (U<sub>9</sub>, U<sub>10</sub>) dikongsi oleh keempat-empat element; node 1 dan node 9 tidak pernah bertemu, jadi entrinya kekal sifar.") + '</figcaption></figure>'
        + STEP("Worked step · entries of the assembled [K] (Activity 4)", "Langkah bekerja · entri [K] yang di-assemble (Aktiviti 4)",
               P("Local k<sub>11</sub> of element 2 (its local node 1 is global node 2) goes to K<sub>3,3</sub>; local k<sub>34</sub> = s<sub>6</sub> = −0.373 × 10⁶ goes to K<sub>5,6</sub>, the u–v coupling of node 3. The diagonals collect s<sub>1</sub> once for every element at the node:",
                 "k<sub>11</sub> local bagi element 2 (node local 1-nya ialah node global 2) pergi ke K<sub>3,3</sub>; k<sub>34</sub> local = s<sub>6</sub> = −0.373 × 10⁶ pergi ke K<sub>5,6</sub>, gandingan u–v bagi node 3. Pepenjuru mengumpul s<sub>1</sub> sekali bagi setiap element pada node itu:")
               + A.eq("v0_Kdiag") + A.eq("v0_K910")
               + P("K<sub>9,10</sub> is zero: at an interior node of a regular mesh the u–v couplings of the four elements cancel in pairs. K<sub>3,3</sub> = 1.751 and K<sub>9,9</sub> = 3.501 (× 10⁶) are visible in the text’s (3.46): a quick check of your dof map.",
                   "K<sub>9,10</sub> sifar: pada node dalaman mesh yang seragam, gandingan u–v empat element saling membatalkan secara berpasangan. K<sub>3,3</sub> = 1.751 dan K<sub>9,9</sub> = 3.501 (× 10⁶) kelihatan dalam (3.46) teks: semakan pantas untuk dof map anda."))
        + H3("Supports: strike the fixed dofs", "Support: buang dof yang fixed")
        + SB(P("The three nodes of the left edge are fixed in both directions: six known displacements, all zero. As for a prescribed temperature, their rows and columns are deleted; nothing moves to the right-hand side because the known values are zero. Twelve equations remain, text (3.48), which MATLAB solves.",
               "Tiga node pada tepi kiri fixed dalam kedua-dua arah: enam displacement yang diketahui, semuanya sifar. Seperti temperature yang ditetapkan, baris dan lajurnya dibuang; tiada yang berpindah ke sebelah kanan kerana nilai yang diketahui ialah sifar. Dua belas persamaan tinggal, teks (3.48), yang diselesaikan oleh MATLAB."))
        + A.eq("r_fixed")
        + '<div class="tbl"><table><tr><th>' + B("Node", "Node") + '</th><th class="r">u (m)</th><th class="r">v (m)</th><th>' + B("Where", "Di mana") + '</th></tr>'
        + '<tr><td>1, 4, 7</td><td class="r num">0</td><td class="r num">0</td><td>' + B("fixed edge", "tepi fixed") + '</td></tr>'
        + '<tr><td>2</td><td class="r num">−0.030966</td><td class="r num">−0.045520</td><td>' + B("bottom, mid-span", "bawah, tengah rentang") + '</td></tr>'
        + '<tr><td>5</td><td class="r num">0</td><td class="r num">−0.043013</td><td>' + B("centre", "pusat") + '</td></tr>'
        + '<tr><td>8</td><td class="r num">+0.030966</td><td class="r num">−0.045520</td><td>' + B("top, mid-span", "atas, tengah rentang") + '</td></tr>'
        + '<tr><td>3</td><td class="r num">−0.041967</td><td class="r num">−0.130578</td><td>' + B("free end, bottom", "hujung bebas, bawah") + '</td></tr>'
        + '<tr><td>6</td><td class="r num">0</td><td class="r num">−0.130421</td><td>' + B("free end, mid-height", "hujung bebas, tengah ketinggian") + '</td></tr>'
        + '<tr><td>9</td><td class="r num">+0.041967</td><td class="r num">−0.130578</td><td>' + B("free end, top", "hujung bebas, atas") + '</td></tr></table></div>'
        + STEP("Read the solution like a structural engineer (Activity 5)", "Baca penyelesaian seperti jurutera struktur (Aktiviti 5)",
               LI([("The bottom fibre shortens (u<sub>2</sub>, u<sub>3</sub> &lt; 0) and the top lengthens (u<sub>8</sub>, u<sub>9</sub> &gt; 0) by the same amounts: antisymmetric bending about mid-height, an exact property of this symmetric mesh and load.", "Gentian bawah memendek (u<sub>2</sub>, u<sub>3</sub> &lt; 0) dan gentian atas memanjang (u<sub>8</sub>, u<sub>9</sub> &gt; 0) dengan jumlah yang sama: lenturan antisimetri tentang tengah ketinggian, sifat tepat mesh dan load yang simetri ini."),
                   ("u = 0 at nodes 5 and 6: the mid-height line is the neutral axis.", "u = 0 pada node 5 dan 6: garis tengah ketinggian ialah neutral axis."),
                   ("v is almost the same across the depth of each section (−0.1306, −0.1304, −0.1306 m at the free end): the depth hardly changes, the usual beam assumption.", "v hampir sama merentasi kedalaman setiap keratan (−0.1306, −0.1304, −0.1306 m di hujung bebas): kedalaman hampir tidak berubah, andaian biasa beam.")]))
        + H3("Reactions: the first check of any solution", "Reaction: semakan pertama bagi mana-mana penyelesaian")
        + SB(P("Evaluate the struck rows, [K]{U} − {R}, at the six fixed dofs. Their sum must balance the applied load and their moment must balance its moment about the fixed edge. The 2 × 2 mesh gives exactly these values, as every correct model must, whatever its mesh:",
               "Nilaikan baris yang dibuang, [K]{U} − {R}, pada enam dof fixed. Jumlahnya mesti mengimbangi load yang dikenakan dan momennya mesti mengimbangi momen load itu terhadap tepi fixed. Mesh 2 × 2 memberi nilai ini dengan tepat, seperti yang mesti diberi oleh setiap model yang betul, tanpa mengira mesh-nya:"))
        + A.eq("v0_react")
        + KP([("Dof map: node n → 2n − 1, 2n; scatter-add 8 × 8 blocks; K<sub>ii</sub> collects s<sub>1</sub> (or s<sub>9</sub>) once per element at the node.", "Dof map: node n → 2n − 1, 2n; scatter-add blok 8 × 8; K<sub>ii</sub> mengumpul s<sub>1</sub> (atau s<sub>9</sub>) sekali bagi setiap element pada node itu."),
              ("Six fixed dofs struck → 12 × 12; tip v = −0.1306 m.", "Enam dof fixed dibuang → 12 × 12; v hujung = −0.1306 m."),
              ("Reactions: ΣR<sub>y</sub> = +10 kN, moment 40 kN·m about the fixed edge.", "Reaction: ΣR<sub>y</sub> = +10 kN, momen 40 kN·m terhadap tepi fixed.")])
        + QC("q5", "In the 2 × 2 cantilever, why is u = 0 at nodes 5 and 6?", "Dalam cantilever 2 × 2, mengapa u = 0 pada node 5 dan 6?",
             [("a", "They lie on the neutral axis of the bending plate", "Ia terletak pada neutral axis plat yang melentur"), ("b", "They are fixed by the supports", "Ia ditahan oleh support"), ("c", "Their rows were struck from [K]", "Barisnya telah dibuang daripada [K]")],
             "a", "Under bending the fibres above mid-height stretch and those below shorten by the same amount, so the mid-height line neither stretches nor shortens. Only nodes 1, 4 and 7 are supported, and only their rows were struck.",
             "Di bawah lenturan, gentian di atas tengah ketinggian meregang dan yang di bawah memendek dengan jumlah yang sama, jadi garis tengah ketinggian tidak meregang mahupun memendek. Hanya node 1, 4 dan 7 yang ditahan, dan hanya barisnya yang dibuang.")
    )
    S.append(("n5", "Assembly with two dofs per node, supports and the solution", "Assembly dengan dua dof setiap node, support dan penyelesaian", body))

    # ---- n6: is the answer right? ----
    code = ["% ---- changes from the heat script ----", "Lx = 4; Ly = 2;                 % plate 4 m x 2 m", "E = 200e6; nu = 0.33; t = 0.01;", "Nx = 2; Ny = 2; ndof = 18;      % 2 dofs per node", "a = Lx/Nx; b = Ly/Ny;",
            "% 12 closed-form values, text (3.42)", "s1 = E*t*((1-nu)*a^2 + 2*b^2)/(6*(1-nu^2)*a*b);", "s2 = E*t*((1-nu) + 2*nu)/(8*(1-nu^2));", "% ... s3 to s12 likewise ...",
            "k = [s1 s2 s3 s4 s5 s6 s7 s8; ...];  % 8 x 8 pattern of (3.42)", "% assembly with the dof map (node n -> 2n-1, 2n)", "K = zeros(ndof); F = zeros(ndof,1);",
            "d1 = [1 2 3 4 9 10 7 8];       K(d1,d1) = K(d1,d1) + k;", "d2 = [3 4 5 6 11 12 9 10];     K(d2,d2) = K(d2,d2) + k;", "d3 = [7 8 9 10 15 16 13 14];   K(d3,d3) = K(d3,d3) + k;",
            "d4 = [9 10 11 12 17 18 15 16]; K(d4,d4) = K(d4,d4) + k;", "F([6 12 18]) = [-2500 -5000 -2500];   % edge traction, (3.47)", "fixed = [1 2 7 8 13 14];  free = setdiff(1:ndof, fixed);",
            "U = zeros(ndof,1);  U(free) = K(free,free) \\ F(free);   % (3.49)"]
    body = (
        P("The computer will always return numbers. Whether they are right is the engineer’s question, and it has two independent answers: compare with a simpler theory, and refine the mesh until the answer stops moving.",
          "Komputer akan sentiasa memulangkan nombor. Sama ada nombor itu betul ialah soalan jurutera, dan ia ada dua jawapan yang bebas: bandingkan dengan teori yang lebih mudah, dan refine mesh sehingga jawapan berhenti berubah.")
        + H3("A hand check: Timoshenko beam theory", "Semakan tangan: Timoshenko beam theory")
        + SB(P("The plate is a deep cantilever (L/H = 2) carrying P = q<sub>y</sub>H = 10 kN at its end. Elementary bending gives PL³/(3EI); because the beam is deep, shear deformation adds PL/(κGA) with κ = 5/6:",
               "Plat ini ialah cantilever dalam (L/H = 2) yang membawa P = q<sub>y</sub>H = 10 kN di hujungnya. Lenturan asas memberi PL³/(3EI); kerana beam ini dalam, shear deformation menambah PL/(κGA) dengan κ = 5/6:"))
        + A.eq("r_beam") + A.eq("r_beam_num") + A.eq("v0_err")
        + NOTE("Keep four figures when the difference is small", "Kekalkan empat angka apabila perbezaannya kecil",
               "Rounded to three decimals, 0.189 against 0.192, the 16 × 16 error would look like −1.6%; with four figures, as on the Activity 6 slide, it is −1.4%. A percentage difference of two close numbers is only as good as the digits you keep.",
               "Dibundarkan kepada tiga tempat perpuluhan, 0.189 berbanding 0.192, ralat 16 × 16 akan kelihatan seperti −1.6%; dengan empat angka, seperti pada slide Aktiviti 6, ia −1.4%. Perbezaan peratus dua nombor yang hampir hanya setepat digit yang anda simpan.")
        + '<figure><img src="slides/img/fig_deflected.png" alt="Deflected shapes of the cantilever: the 2 by 2 hand mesh and a 32 by 16 converged mesh, displacements scaled" class="figimg" style="width:min(560px,100%)"><figcaption>'
        + B("The hand mesh deflects about two thirds as much as the converged mesh. Each bilinear element keeps straight edges, so it cannot curve; under bending it develops a spurious shear strain and resists with a shear stiffness it should not have. This is shear locking.",
            "Mesh tangan melentur kira-kira dua pertiga sahaja berbanding mesh yang converge. Setiap element bilinear mengekalkan tepi lurus, jadi ia tidak boleh melengkung; di bawah lenturan ia menghasilkan shear strain palsu dan menentang dengan shear stiffness yang tidak sepatutnya ada. Inilah shear locking.") + '</figcaption></figure>'
        + H3("Refine until the answer stops moving", "Refine sehingga jawapan berhenti berubah")
        + '<div class="tbl"><table><tr><th>' + B("Mesh", "Mesh") + '</th><th class="r">dofs</th><th class="r">' + B("tip v (m)", "v hujung (m)") + '</th><th class="r">' + B("vs beam theory", "berbanding beam theory") + '</th></tr>'
        + '<tr><td>Q4 2 × 2 (' + B("hand", "tangan") + ')</td><td class="r num">18</td><td class="r num">−0.1306</td><td class="r num">−32%</td></tr>'
        + '<tr><td>Q4 4 × 2</td><td class="r num">30</td><td class="r num">−0.1643</td><td class="r num">−14%</td></tr>'
        + '<tr><td>Q4 8 × 4</td><td class="r num">90</td><td class="r num">−0.1824</td><td class="r num">−5.0%</td></tr>'
        + '<tr><td>Q4 16 × 8</td><td class="r num">306</td><td class="r num">−0.1886</td><td class="r num">−1.7%</td></tr>'
        + '<tr><td>Q4 16 × 16</td><td class="r num">578</td><td class="r num">−0.1893</td><td class="r num">−1.4%</td></tr>'
        + '<tr><td>Q4 32 × 16</td><td class="r num">1122</td><td class="r num">−0.1906</td><td class="r num">−0.7%</td></tr>'
        + '<tr><td>Q4 80 × 80</td><td class="r num">13 122</td><td class="r num">−0.1915</td><td class="r num">−0.2%</td></tr>'
        + '<tr><td>' + B("Timoshenko beam", "Timoshenko beam") + '</td><td class="r">—</td><td class="r num">−0.1919</td><td class="r">—</td></tr></table></div>'
        + '<figure><img src="slides/img/fig_convergence.png" alt="Tip deflection against number of elements along the length, approaching 0.192 m, and relative error against element size on log-log axes" class="figimg" style="width:min(640px,100%)"><figcaption>'
        + B("Left: the tip deflection climbs towards the beam-theory line as the mesh is refined. Right: the error falls with the element size.", "Kiri: tip deflection meningkat ke arah garis beam theory apabila mesh di-refine. Kanan: ralat jatuh bersama saiz element.") + '</figcaption></figure>'
        + NOTE("Shape matters more than count", "Bentuk lebih penting daripada bilangan",
               "Eight elements in three layouts: 4 × 2 gives −0.164 m, 8 × 1 gives −0.166 m, but 2 × 4 gives only −0.133 m. Elements that are long in the bending direction (a/b = 4 in the 2 × 4 mesh) lock most. Refine along the length first.",
               "Lapan element dalam tiga susunan: 4 × 2 memberi −0.164 m, 8 × 1 memberi −0.166 m, tetapi 2 × 4 hanya memberi −0.133 m. Element yang panjang dalam arah lenturan (a/b = 4 dalam mesh 2 × 4) paling teruk locking. Refine sepanjang panjangnya dahulu.")
        + '<div class="figrow"><img src="slides/img/w12_conv.png" alt="Log-log plot of relative displacement error against element size for a four-node cantilever model; the error falls and then levels off" class="figimg" style="flex:1 1 280px;max-width:420px"><div style="flex:1 1 240px">'
        + '<img src="slides/img/w12_mesh12.png" alt="Coarse mesh of 12 square elements" class="figimg" style="margin-bottom:8px"><img src="slides/img/w12_mesh192.png" alt="Fine mesh of 192 square elements" class="figimg"></div></div>'
        + '<p class="credit">' + B("The same experiment in another code: the error falls with the element size, then levels off near 0.7%, because the load is applied as a uniform end traction while the exact solution assumes a parabolic end shear. Refining removes mesh error, not idealisation error. Images: SolidsPy (J. Gómez and N. Guarín-Zapata), MIT licence.",
                                   "Eksperimen yang sama dalam kod lain: ralat jatuh bersama saiz element, kemudian mendatar dekat 0.7%, kerana load dikenakan sebagai traction hujung yang seragam manakala penyelesaian tepat mengandaikan shear hujung parabolic. Refinement menghapuskan ralat mesh, bukan ralat idealisation. Imej: SolidsPy (J. Gómez dan N. Guarín-Zapata), lesen MIT.") + '</p>'
        + OK("The project rule", "Peraturan projek", "Three meshes, one table, one independent check (beam theory, the reactions, or a textbook solution). Then, and only then, a conclusion. Never report a single-mesh answer.",
             "Tiga mesh, satu jadual, satu semakan bebas (beam theory, reaction, atau penyelesaian buku teks). Kemudian, dan hanya kemudian, satu kesimpulan. Jangan sekali-kali melaporkan jawapan daripada satu mesh sahaja.")
        + H3("The script, as a diff against Heat Transfer Part 2", "Skrip, sebagai perbezaan daripada Heat Transfer Part 2")
        + '<pre class="paper" style="font:13px/1.5 var(--font-num);overflow-x:auto;white-space:pre">' + "\n".join(code) + '</pre>'
        + SB(LI([("Two dofs per node: ndof = 2 × nodes, and each element’s dof list replaces its node list.", "Dua dof setiap node: ndof = 2 × node, dan senarai dof setiap element menggantikan senarai node-nya."),
                 ("The 4 × 4 conductance pattern becomes the 8 × 8 pattern of (3.42).", "Pola conductance 4 × 4 menjadi pola 8 × 8 daripada (3.42)."),
                 ("Loads in the v-dofs of the loaded edge; six fixed dofs instead of fixed temperatures. The solve line is unchanged.", "Load pada dof v tepi yang dibebankan; enam dof fixed menggantikan temperature tetap. Baris penyelesaian tidak berubah.")]))
        + P("The Python version, fe_plane_stress.py, is in the Explorer tab; it builds [k] by Gauss quadrature, reproduces (3.49) and runs the convergence study above.",
            "Versi Python, fe_plane_stress.py, ada dalam tab Explorer; ia membina [k] melalui Gauss quadrature, menghasilkan semula (3.49) dan menjalankan kajian convergence di atas.")
        + KP([("Two independent checks: beam theory (0.192 m) and mesh refinement; plus the reactions.", "Dua semakan bebas: beam theory (0.192 m) dan mesh refinement; serta reaction."),
              ("The 2 × 2 Q4 mesh is 32% too stiff: straight-sided elements lock in bending.", "Mesh Q4 2 × 2 terlalu stiff sebanyak 32%: element bertepi lurus mengalami locking dalam lenturan."),
              ("About 32 elements along the length for 1%; elements long in the bending direction lock most.", "Kira-kira 32 element sepanjang panjangnya untuk 1%; element yang panjang dalam arah lenturan paling teruk locking.")])
        + QC("q6", "The same eight Q4 elements as a 4 × 2 mesh or as a 2 × 4 mesh. Which is stiffer?", "Lapan element Q4 yang sama sebagai mesh 4 × 2 atau sebagai mesh 2 × 4. Yang mana lebih stiff?",
             [("a", "2 × 4: its elements are four times longer than deep and lock in bending", "2 × 4: element-nya empat kali lebih panjang daripada dalam dan mengalami locking dalam lenturan"), ("b", "4 × 2: it has more elements along the length", "4 × 2: ia ada lebih banyak element sepanjang panjangnya"), ("c", "Neither: the same number of elements gives the same stiffness", "Tiada: bilangan element yang sama memberi stiffness yang sama")],
             "a", "2 × 4 gives −0.133 m against −0.164 m for 4 × 2: the 2 m × 0.5 m elements cannot curve along their length, so they develop most spurious shear. The count of elements is the same; their shape is not.",
             "2 × 4 memberi −0.133 m berbanding −0.164 m bagi 4 × 2: element 2 m × 0.5 m tidak boleh melengkung sepanjang panjangnya, jadi ia menghasilkan shear palsu paling banyak. Bilangan element sama; bentuknya tidak.")
    )
    S.append(("n6", "Is the answer right? Beam theory, refinement and shear locking", "Adakah jawapan betul? Beam theory, refinement dan shear locking", body))
    return S


RECALL = [
    QC("r1", "Recall · the text’s shear strain ε<sub>xy</sub> is", "Ingat semula · shear strain ε<sub>xy</sub> dalam teks ialah",
       [("a", "∂u/∂y + ∂v/∂x, the engineering shear strain", "∂u/∂y + ∂v/∂x, engineering shear strain"), ("b", "½(∂u/∂y + ∂v/∂x), the tensor shear strain", "½(∂u/∂y + ∂v/∂x), tensor shear strain"), ("c", "∂u/∂x + ∂v/∂y", "∂u/∂x + ∂v/∂y")],
       "a", "The text’s ε<sub>xy</sub> is the engineering shear strain γ<sub>xy</sub>, the sum of the two slopes; the (1 − ν)/2 entry of [E] is built for it. Row 3 of [B] comes straight from this definition.",
       "ε<sub>xy</sub> dalam teks ialah engineering shear strain γ<sub>xy</sub>, iaitu jumlah dua kecerunan; entri (1 − ν)/2 dalam [E] dibina untuknya. Baris 3 [B] terhasil terus daripada definisi ini."),
    QC("r2", "Recall · in the 2 × 2 cantilever mesh, global node 5 carries the dofs", "Ingat semula · dalam mesh cantilever 2 × 2, node global 5 membawa dof",
       [("a", "U<sub>5</sub> and U<sub>6</sub>", "U<sub>5</sub> dan U<sub>6</sub>"), ("b", "U<sub>9</sub> and U<sub>10</sub>", "U<sub>9</sub> dan U<sub>10</sub>"), ("c", "U<sub>10</sub> and U<sub>11</sub>", "U<sub>10</sub> dan U<sub>11</sub>")],
       "b", "Node n owns U<sub>2n−1</sub> (x) and U<sub>2n</sub> (y): node 5 → U<sub>9</sub>, U<sub>10</sub>. Taking the node number for the dof number is the commonest assembly slip.",
       "Node n memiliki U<sub>2n−1</sub> (x) dan U<sub>2n</sub> (y): node 5 → U<sub>9</sub>, U<sub>10</sub>. Mengambil nombor node sebagai nombor dof ialah kesilapan assembly yang paling biasa."),
]

QUICK = [
    MCQ("a1", "The strain–displacement matrix [B] of the four-node plane-stress element is", "Strain–displacement matrix [B] bagi four-node plane-stress element ialah",
        [("a", "3 × 8: three strains from eight nodal displacements", "3 × 8: tiga strain daripada lapan nodal displacement"), ("b", "2 × 8: two displacements from eight nodal displacements", "2 × 8: dua displacement daripada lapan nodal displacement"), ("c", "8 × 8, symmetric", "8 × 8, simetri")], "a",
        "[B] = [∂]ᵀ[N] = (3 × 2)(2 × 8) = 3 × 8. The 2 × 8 matrix is [N] itself; the 8 × 8 symmetric matrix is [k] = t∫[B]ᵀ[E][B] dA.",
        "[B] = [∂]ᵀ[N] = (3 × 2)(2 × 8) = 3 × 8. Matrix 2 × 8 ialah [N] itu sendiri; matrix simetri 8 × 8 ialah [k] = t∫[B]ᵀ[E][B] dA."),
    MCQ("a2", "Which entries of a rectangle’s [k] do not depend on the element’s sides a and b?", "Entri [k] segi empat tepat yang mana tidak bergantung pada sisi element a dan b?",
        [("a", "the u–v couplings s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub>", "gandingan u–v s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub>"), ("b", "the diagonal entries s<sub>1</sub> and s<sub>9</sub>", "entri pepenjuru s<sub>1</sub> dan s<sub>9</sub>"), ("c", "none: every entry contains a/b or b/a", "tiada: setiap entri mengandungi a/b atau b/a")], "a",
        "Each u–v coupling integrates the product of an x-derivative and a y-derivative, such as x(b − y)/(a²b²), whose integral over the element is ±1/4 whatever a and b are: s<sub>2</sub> = Et/(8(1 − ν)). The diagonals contain a/b and b/a.",
        "Setiap gandingan u–v meng-integrate hasil darab satu x-derivative dan satu y-derivative, seperti x(b − y)/(a²b²), yang integral-nya atas element ialah ±1/4 tanpa mengira a dan b: s<sub>2</sub> = Et/(8(1 − ν)). Pepenjuru mengandungi a/b dan b/a."),
    MCQ("a3", "A uniform traction acts in −y on side 2–3 of an element. Its nodal loads go to the local dofs", "Traction seragam bertindak dalam −y pada sisi 2–3 sesuatu element. Nodal load-nya pergi ke dof local",
        [("a", "4 and 6 (v<sub>2</sub>, v<sub>3</sub>), half each", "4 dan 6 (v<sub>2</sub>, v<sub>3</sub>), separuh setiap satu"), ("b", "3 and 5 (u<sub>2</sub>, u<sub>3</sub>), half each", "3 dan 5 (u<sub>2</sub>, u<sub>3</sub>), separuh setiap satu"), ("c", "all eight dofs, an eighth each", "kesemua lapan dof, satu perlapan setiap satu")], "a",
        "Along side 2–3 only N<sub>2</sub> and N<sub>3</sub> are non-zero, and the load acts in y, so it enters the v-dofs of nodes 2 and 3: local dofs 4 and 6, as in text (3.45).",
        "Di sepanjang sisi 2–3 hanya N<sub>2</sub> dan N<sub>3</sub> bukan sifar, dan load bertindak dalam y, jadi ia masuk ke dof v node 2 dan 3: dof local 4 dan 6, seperti dalam teks (3.45)."),
    MCQ("a4", "In the 2 × 2 cantilever mesh, the diagonal entry K<sub>9,9</sub> (u of the centre node 5) is", "Dalam mesh cantilever 2 × 2, entri pepenjuru K<sub>9,9</sub> (u bagi node pusat 5) ialah",
        [("a", "s<sub>1</sub>", "s<sub>1</sub>"), ("b", "2s<sub>1</sub>", "2s<sub>1</sub>"), ("c", "4s<sub>1</sub> = 3.501 × 10⁶ N m<sup>−1</sup>", "4s<sub>1</sub> = 3.501 × 10⁶ N m<sup>−1</sup>")], "c",
        "Node 5 belongs to all four elements, and each puts its u–u diagonal s<sub>1</sub> = 0.875 × 10⁶ there. K<sub>3,3</sub> (node 2, two elements) is 2s<sub>1</sub>.",
        "Node 5 dimiliki oleh keempat-empat element, dan setiap satu meletakkan pepenjuru u–u s<sub>1</sub> = 0.875 × 10⁶ di situ. K<sub>3,3</sub> (node 2, dua element) ialah 2s<sub>1</sub>."),
    MCQ("a5", "The 2 × 2 Q4 mesh gives a tip deflection of 0.131 m; beam theory with shear gives 0.192 m. The coarse mesh is", "Mesh Q4 2 × 2 memberi tip deflection 0.131 m; beam theory dengan shear memberi 0.192 m. Mesh kasar itu",
        [("a", "too stiff: straight-sided bilinear elements develop spurious shear in bending", "terlalu stiff: element bilinear bertepi lurus menghasilkan shear palsu dalam lenturan"), ("b", "too flexible: large elements are soft", "terlalu fleksibel: element besar itu lembut"), ("c", "more accurate than beam theory, which ignores the plate’s width", "lebih tepat daripada beam theory, yang mengabaikan lebar plat")], "a",
        "A smaller deflection under the same load means a stiffer model. Bilinear elements cannot curve, so they lock; refining the mesh brings the tip to −0.1906 m on 32 × 16, within 1% of beam theory.",
        "Deflection yang lebih kecil di bawah load yang sama bermaksud model yang lebih stiff. Element bilinear tidak boleh melengkung, jadi ia mengalami locking; refinement membawa hujung kepada −0.1906 m pada 32 × 16, dalam 1% daripada beam theory."),
    MCQ("a6", "After solving the text’s cantilever, the six reactions at the fixed edge must", "Selepas menyelesaikan cantilever dalam teks, enam reaction pada tepi fixed mesti",
        [("a", "add up to +10 kN in y and give 40 kN·m about the fixed edge", "berjumlah +10 kN dalam y dan memberi 40 kN·m terhadap tepi fixed"), ("b", "all be zero, because the edge does not move", "semuanya sifar, kerana tepi itu tidak bergerak"), ("c", "equal the nodal loads −2500, −5000, −2500 N", "sama dengan nodal load −2500, −5000, −2500 N")], "a",
        "Global equilibrium: the supports carry the whole 10 kN end load and its moment 10 × 4 = 40 kN·m. Zero displacement does not mean zero force; that is exactly where the force is.",
        "Keseimbangan global: support membawa keseluruhan load hujung 10 kN dan momennya 10 × 4 = 40 kN·m. Displacement sifar tidak bermaksud daya sifar; di situlah daya itu berada."),
]

ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="4" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("An element with a = 2 m, b = 1 m and t = 0.01 m carries a downward traction of 500 kN m<sup>−2</sup> (force per unit area) on its right side, 2–3. A student finds the nodal loads. One line contains the slip. Which one?",
        "Satu element dengan a = 2 m, b = 1 m dan t = 0.01 m membawa traction ke bawah 500 kN m<sup>−2</sup> (daya per unit luas) pada sisi kanannya, 2–3. Seorang pelajar mencari nodal load. Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>' + B("Load per unit length of the side: 500 × t = 500 × 0.01 = 5 kN m<sup>−1</sup>.", "Load per unit panjang sisi: 500 × t = 500 × 0.01 = 5 kN m<sup>−1</sup>.") + '</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>' + B("Total load on the side: 5 × b = 5 × 1 = 5 kN, downward.", "Jumlah load pada sisi: 5 × b = 5 × 1 = 5 kN, ke bawah.") + '</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>' + B("Each of the two nodes of side 2–3 takes half: 2.5 kN.", "Setiap satu daripada dua node sisi 2–3 menerima separuh: 2.5 kN.") + '</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>' + B("They go to local dofs 3 and 5 (u<sub>2</sub>, u<sub>3</sub>): r<sub>3</sub> = r<sub>5</sub> = −2.5 kN.", "Ia pergi ke dof local 3 dan 5 (u<sub>2</sub>, u<sub>3</sub>): r<sub>3</sub> = r<sub>5</sub> = −2.5 kN.") + '</span></button>'
    + '<button type="button" data-k="5"><span class="ln">5</span><span>' + B("Check: r<sub>3</sub> + r<sub>5</sub> = −5 kN = the total load ✓", "Semakan: r<sub>3</sub> + r<sub>5</sub> = −5 kN = jumlah load ✓") + '</span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 4: the traction acts in y, so the loads belong in the v-dofs of nodes 2 and 3, local dofs 4 and 6: r<sub>4</sub> = r<sub>6</sub> = −2.5 kN, and r<sub>3</sub> = r<sub>5</sub> = 0. The total in line 5 could not catch it, because the sum is the same whichever dofs receive the shares; the check that does is to ask which displacement the load does work on.",
        "Baris 4: traction bertindak dalam y, jadi load itu milik dof v node 2 dan 3, iaitu dof local 4 dan 6: r<sub>4</sub> = r<sub>6</sub> = −2.5 kN, dan r<sub>3</sub> = r<sub>5</sub> = 0. Jumlah pada baris 5 tidak dapat menangkapnya, kerana jumlahnya sama tidak kira dof mana yang menerima bahagian itu; semakan yang berkesan ialah bertanya displacement mana yang dikenakan kerja oleh load itu.")
    + '</p></div>'
)

EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  /* s1..s12 of text (3.42); E in kN/m2, t and a, b in m: values in kN/m */
  function sv(a,b,E,nu,t){ var c=E*t/(1-nu*nu), s={};
    s[1]=c*((1-nu)*a*a+2*b*b)/(6*a*b); s[2]=c*((1-nu)+2*nu)/8; s[3]=c*((1-nu)*a*a-4*b*b)/(12*a*b); s[4]=-c*((1-nu)-2*nu)/8;
    s[5]=-c*((1-nu)*a*a+2*b*b)/(12*a*b); s[6]=-c*((1-nu)+2*nu)/8; s[7]=-c*((1-nu)*a*a-b*b)/(6*a*b); s[8]=c*((1-nu)-2*nu)/8;
    s[9]=c*(2*a*a+(1-nu)*b*b)/(6*a*b); s[10]=-c*((1-nu)*b*b-a*a)/(6*a*b); s[11]=-c*(2*a*a+(1-nu)*b*b)/(12*a*b); s[12]=c*((1-nu)*b*b-4*a*a)/(12*a*b);
    s.c=c; return s; }
  var M = 1e6;
  function genK(r){ var a=pick(r,[0.25,0.5,1,1.5,2]), b=pick(r,[0.25,0.5,1,2]); while (a/b > 4 || b/a > 4) b=pick(r,[0.25,0.5,1,2]);
    return {a:a, b:b, E:pick(r,[2.0e7,2.5e7,3.0e7,7.0e7,2.0e8]), nu:pick(r,[0.15,0.2,0.25,0.3]), t:pick(r,[0.05,0.1,0.2,0.25])}; }
  function givenK(P){ return "a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, t = <span class=\"num\">"+P.t+"</span> m, E = <span class=\"num\">"+(P.E/1e6)+" × 10⁶</span> kN m<sup>−2</sup>, ν = <span class=\"num\">"+P.nu+"</span>"; }
  function f3(v){ return fmt(v/M,4); }
  function sg(v){ return String(v).replace("-", "−"); }
  EX.define("b1", {
    gen: genK,
    text: function(P){ return bi("Plane-stress element: "+givenK(P)+". Find s<sub>1</sub>, s<sub>2</sub>, s<sub>3</sub> and s<sub>7</sub> of (3.42) in 10⁶ kN m<sup>−1</sup>, to 3 decimals.",
                                   "Element plane stress: "+givenK(P)+". Cari s<sub>1</sub>, s<sub>2</sub>, s<sub>3</sub> dan s<sub>7</sub> daripada (3.42) dalam 10⁶ kN m<sup>−1</sup>, kepada 3 tempat perpuluhan."); },
    fields: [1,2,3,7].map(function(i){ return {id:"s"+i, label:["s<sub>"+i+"</sub>","s<sub>"+i+"</sub>"], unit:"10⁶ kN/m", fn:function(P){ return sv(P.a,P.b,P.E,P.nu,P.t)[i]/M; }, atol:0.0015, rtol:0.003}; }),
    hints: [function(P){ return bi("Start with the common factor Et/(1 − ν²). Then (3.42): s<sub>1</sub> = c((1 − ν)a² + 2b²)/(6ab), s<sub>2</sub> = c(1 + ν)/8, s<sub>3</sub> = c((1 − ν)a² − 4b²)/(12ab), s<sub>7</sub> = −c((1 − ν)a² − b²)/(6ab).",
                                      "Mulakan dengan faktor sepunya Et/(1 − ν²). Kemudian (3.42): s<sub>1</sub> = c((1 − ν)a² + 2b²)/(6ab), s<sub>2</sub> = c(1 + ν)/8, s<sub>3</sub> = c((1 − ν)a² − 4b²)/(12ab), s<sub>7</sub> = −c((1 − ν)a² − b²)/(6ab)."); },
            function(P){ var s=sv(P.a,P.b,P.E,P.nu,P.t); return bi("c = Et/(1 − ν²) = "+f3(s.c)+" × 10⁶ kN m<sup>−1</sup>; (1 − ν)a² = "+fmt((1-P.nu)*P.a*P.a,4)+", b² = "+fmt(P.b*P.b,4)+", ab = "+fmt(P.a*P.b,4)+".",
                                      "c = Et/(1 − ν²) = "+f3(s.c)+" × 10⁶ kN m<sup>−1</sup>; (1 − ν)a² = "+fmt((1-P.nu)*P.a*P.a,4)+", b² = "+fmt(P.b*P.b,4)+", ab = "+fmt(P.a*P.b,4)+"."); },
            function(P){ var s=sv(P.a,P.b,P.E,P.nu,P.t); return bi("Check with the row sum: s<sub>5</sub> = −s<sub>1</sub>/2 = "+f3(s[5])+", and s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub> + s<sub>7</sub> must be zero, so s<sub>7</sub> = −(s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub>).",
                                      "Semak dengan jumlah baris: s<sub>5</sub> = −s<sub>1</sub>/2 = "+f3(s[5])+", dan s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub> + s<sub>7</sub> mesti sifar, jadi s<sub>7</sub> = −(s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub>)."); }],
    solution: function(P){ var s=sv(P.a,P.b,P.E,P.nu,P.t), A2=(1-P.nu)*P.a*P.a, B2=P.b*P.b, ab=P.a*P.b;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">c = "+(P.E/1e6)+"×10⁶ × "+P.t+" / (1 − "+P.nu+"²) = "+f3(s.c)+" × 10⁶<br>s<sub>1</sub> = c("+fmt(A2,4)+" + "+fmt(2*B2,4)+")/(6 × "+fmt(ab,4)+") = "+fmt(s[1]/M,3)
        +"<br>s<sub>2</sub> = c(1 + "+P.nu+")/8 = "+fmt(s[2]/M,3)+"<br>s<sub>3</sub> = c("+fmt(A2,4)+" − "+fmt(4*B2,4)+")/(12 × "+fmt(ab,4)+") = "+fmt(s[3]/M,3)+"<br>s<sub>7</sub> = −c("+fmt(A2,4)+" − "+fmt(B2,4)+")/(6 × "+fmt(ab,4)+") = "+fmt(s[7]/M,3)
        +"<br>"+bi("Row check: ","Semakan baris: ")+"s<sub>1</sub> + s<sub>3</sub> + s<sub>5</sub> + s<sub>7</sub> = "+fmt((s[1]+s[3]+s[5]+s[7])/M,3)+" ("+bi("all in","semua dalam")+" 10⁶ kN m<sup>−1</sup>)</p>"; }
  });
  EX.define("b2", {
    gen: function(r){ var p2=pick(r,[0,-5,-10,-15,-20]), p3=pick(r,[-5,-10,-15,-20,-25]); if (p2===p3) p2=0;
      return {a:pick(r,[0.5,1,1.5,2]), b:pick(r,[0.5,1,1.5,2]), t:pick(r,[0.1,0.2,0.25,0.3]), g:pick(r,[24,25,78.5]), p2:p2, p3:p3}; },
    text: function(P){ return bi("Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, t = <span class=\"num\">"+P.t+"</span> m, unit weight γ = <span class=\"num\">"+P.g+"</span> kN m<sup>−3</sup>. Its right side 2–3 carries a load in y varying linearly from p<sub>2</sub> = <span class=\"num\">"+sg(P.p2)+"</span> kN m<sup>−1</sup> at node 2 to p<sub>3</sub> = <span class=\"num\">"+sg(P.p3)+"</span> kN m<sup>−1</sup> at node 3 (negative = downward). Find the total nodal loads r<sub>2</sub> (v<sub>1</sub>), r<sub>4</sub> (v<sub>2</sub>) and r<sub>6</sub> (v<sub>3</sub>) from the edge load and the self-weight, in kN, to 3 decimals.",
                                   "Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, t = <span class=\"num\">"+P.t+"</span> m, berat unit γ = <span class=\"num\">"+P.g+"</span> kN m<sup>−3</sup>. Sisi kanannya 2–3 membawa load dalam y yang berubah secara linear daripada p<sub>2</sub> = <span class=\"num\">"+sg(P.p2)+"</span> kN m<sup>−1</sup> pada node 2 kepada p<sub>3</sub> = <span class=\"num\">"+sg(P.p3)+"</span> kN m<sup>−1</sup> pada node 3 (negatif = ke bawah). Cari jumlah nodal load r<sub>2</sub> (v<sub>1</sub>), r<sub>4</sub> (v<sub>2</sub>) dan r<sub>6</sub> (v<sub>3</sub>) daripada edge load dan self-weight, dalam kN, kepada 3 tempat perpuluhan."); },
    fields: [{id:"r2", label:["r<sub>2</sub> (v<sub>1</sub>)","r<sub>2</sub> (v<sub>1</sub>)"], unit:"kN", fn:function(P){ return -P.g*P.t*P.a*P.b/4; }, atol:0.0015, rtol:0.002},
             {id:"r4", label:["r<sub>4</sub> (v<sub>2</sub>)","r<sub>4</sub> (v<sub>2</sub>)"], unit:"kN", fn:function(P){ return P.b*(2*P.p2+P.p3)/6 - P.g*P.t*P.a*P.b/4; }, atol:0.0015, rtol:0.002},
             {id:"r6", label:["r<sub>6</sub> (v<sub>3</sub>)","r<sub>6</sub> (v<sub>3</sub>)"], unit:"kN", fn:function(P){ return P.b*(P.p2+2*P.p3)/6 - P.g*P.t*P.a*P.b/4; }, atol:0.0015, rtol:0.002}],
    hints: [function(P){ return bi("Self-weight: W = γtab, a quarter in each v-dof, downward. Edge load on side 2–3 (length ℓ = b): r<sub>4</sub> = ℓ(2p<sub>2</sub> + p<sub>3</sub>)/6, r<sub>6</sub> = ℓ(p<sub>2</sub> + 2p<sub>3</sub>)/6. Add the two contributions dof by dof.",
                                      "Self-weight: W = γtab, satu perempat pada setiap dof v, ke bawah. Edge load pada sisi 2–3 (panjang ℓ = b): r<sub>4</sub> = ℓ(2p<sub>2</sub> + p<sub>3</sub>)/6, r<sub>6</sub> = ℓ(p<sub>2</sub> + 2p<sub>3</sub>)/6. Tambah dua sumbangan itu dof demi dof."); },
            function(P){ var W=P.g*P.t*P.a*P.b; return bi("W = "+fmt(W,4)+" kN, so −W/4 = "+fmt(-W/4,4)+" kN in each v-dof. Check the edge shares: their sum must be ℓ(p<sub>2</sub> + p<sub>3</sub>)/2 = "+fmt(P.b*(P.p2+P.p3)/2,4)+" kN.",
                                      "W = "+fmt(W,4)+" kN, jadi −W/4 = "+fmt(-W/4,4)+" kN pada setiap dof v. Semak bahagian tepi: jumlahnya mesti ℓ(p<sub>2</sub> + p<sub>3</sub>)/2 = "+fmt(P.b*(P.p2+P.p3)/2,4)+" kN."); }],
    solution: function(P){ var W=P.g*P.t*P.a*P.b, e4=P.b*(2*P.p2+P.p3)/6, e6=P.b*(P.p2+2*P.p3)/6;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">W = "+P.g+" × "+P.t+" × "+P.a+" × "+P.b+" = "+fmt(W,4)+" kN; −W/4 = "+fmt(-W/4,4)+" kN<br>"+bi("edge","tepi")+": r<sub>4</sub> = "+P.b+"(2("+sg(P.p2)+") + ("+sg(P.p3)+"))/6 = "+fmt(e4,4)+", r<sub>6</sub> = "+P.b+"(("+sg(P.p2)+") + 2("+sg(P.p3)+"))/6 = "+fmt(e6,4)+" kN<br>r<sub>2</sub> = "+fmt(-W/4,3)+" kN<br>r<sub>4</sub> = "+fmt(e4,4)+" + ("+fmt(-W/4,4)+") = "+fmt(e4-W/4,3)+" kN<br>r<sub>6</sub> = "+fmt(e6,4)+" + ("+fmt(-W/4,4)+") = "+fmt(e6-W/4,3)+" kN<br>"+bi("(r<sub>8</sub> = r<sub>2</sub>; the u-dofs get nothing.)","(r<sub>8</sub> = r<sub>2</sub>; dof u tidak menerima apa-apa.)")+"</p>"; }
  });
  EX.define("b3", {
    gen: genK,
    text: function(P){ return bi("The 2 × 2 cantilever mesh of the text (nodes 1–3 along the bottom, 4–6 at mid-height, 7–9 on top; elements [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]; node n owns dofs 2n − 1, 2n), with four identical elements: "+givenK(P)+". Find K<sub>3,3</sub>, K<sub>9,9</sub>, K<sub>5,6</sub> and K<sub>3,9</sub> in 10⁶ kN m<sup>−1</sup>, to 3 decimals.",
                                   "Mesh cantilever 2 × 2 dalam teks (node 1–3 di bawah, 4–6 di tengah ketinggian, 7–9 di atas; element [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]; node n memiliki dof 2n − 1, 2n), dengan empat element serupa: "+givenK(P)+". Cari K<sub>3,3</sub>, K<sub>9,9</sub>, K<sub>5,6</sub> dan K<sub>3,9</sub> dalam 10⁶ kN m<sup>−1</sup>, kepada 3 tempat perpuluhan."); },
    fields: [{id:"k33", label:["K<sub>3,3</sub>","K<sub>3,3</sub>"], unit:"10⁶ kN/m", fn:function(P){ return 2*sv(P.a,P.b,P.E,P.nu,P.t)[1]/M; }, atol:0.0015, rtol:0.003},
             {id:"k99", label:["K<sub>9,9</sub>","K<sub>9,9</sub>"], unit:"10⁶ kN/m", fn:function(P){ return 4*sv(P.a,P.b,P.E,P.nu,P.t)[1]/M; }, atol:0.0015, rtol:0.003},
             {id:"k56", label:["K<sub>5,6</sub>","K<sub>5,6</sub>"], unit:"10⁶ kN/m", fn:function(P){ return sv(P.a,P.b,P.E,P.nu,P.t)[6]/M; }, atol:0.0015, rtol:0.003},
             {id:"k39", label:["K<sub>3,9</sub>","K<sub>3,9</sub>"], unit:"10⁶ kN/m", fn:function(P){ return 2*sv(P.a,P.b,P.E,P.nu,P.t)[7]/M; }, atol:0.0015, rtol:0.003}],
    hints: [function(P){ return bi("Dof → node: 3 = U<sub>2</sub> (node 2), 5 and 6 = node 3, 9 = U<sub>5</sub> (node 5). An entry sums k<sub>ij</sub> over the elements that contain both nodes, at their local positions: local node m owns local dofs 2m − 1, 2m.",
                                      "Dof → node: 3 = U<sub>2</sub> (node 2), 5 dan 6 = node 3, 9 = U<sub>5</sub> (node 5). Satu entri menjumlahkan k<sub>ij</sub> atas element yang mengandungi kedua-dua node, pada kedudukan local-nya: node local m memiliki dof local 2m − 1, 2m."); },
            function(P){ return bi("Node 2 is local 2 of element 1 and local 1 of element 2; node 5 is in all four elements; node 3 is local 2 of element 2 only. In the pattern (3.42): every u–u diagonal is s<sub>1</sub>, k<sub>34</sub> = s<sub>6</sub>, k<sub>35</sub> = k<sub>17</sub> = s<sub>7</sub>.",
                                      "Node 2 ialah local 2 bagi element 1 dan local 1 bagi element 2; node 5 ada dalam keempat-empat element; node 3 ialah local 2 bagi element 2 sahaja. Dalam pola (3.42): setiap pepenjuru u–u ialah s<sub>1</sub>, k<sub>34</sub> = s<sub>6</sub>, k<sub>35</sub> = k<sub>17</sub> = s<sub>7</sub>."); },
            function(P){ return bi("K<sub>3,3</sub> = k¹<sub>33</sub> + k²<sub>11</sub> = 2s<sub>1</sub>; K<sub>9,9</sub> = 4s<sub>1</sub>; K<sub>5,6</sub> = k²<sub>34</sub> = s<sub>6</sub> = −s<sub>2</sub>; K<sub>3,9</sub> = k¹<sub>35</sub> + k²<sub>17</sub> = 2s<sub>7</sub>.",
                                      "K<sub>3,3</sub> = k¹<sub>33</sub> + k²<sub>11</sub> = 2s<sub>1</sub>; K<sub>9,9</sub> = 4s<sub>1</sub>; K<sub>5,6</sub> = k²<sub>34</sub> = s<sub>6</sub> = −s<sub>2</sub>; K<sub>3,9</sub> = k¹<sub>35</sub> + k²<sub>17</sub> = 2s<sub>7</sub>."); }],
    solution: function(P){ var s=sv(P.a,P.b,P.E,P.nu,P.t);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">s<sub>1</sub> = "+fmt(s[1]/M,4)+", s<sub>2</sub> = "+fmt(s[2]/M,4)+", s<sub>6</sub> = −s<sub>2</sub> = "+fmt(s[6]/M,4)+", s<sub>7</sub> = "+fmt(s[7]/M,4)+" (× 10⁶ kN m<sup>−1</sup>)<br>K<sub>3,3</sub> = k¹<sub>33</sub> + k²<sub>11</sub> = 2s<sub>1</sub> = "+fmt(2*s[1]/M,3)+"<br>K<sub>9,9</sub> = k¹<sub>55</sub> + k²<sub>77</sub> + k³<sub>33</sub> + k⁴<sub>11</sub> = 4s<sub>1</sub> = "+fmt(4*s[1]/M,3)+"<br>K<sub>5,6</sub> = k²<sub>34</sub> = s<sub>6</sub> = "+fmt(s[6]/M,3)+"<br>K<sub>3,9</sub> = k¹<sub>35</sub> + k²<sub>17</sub> = 2s<sub>7</sub> = "+fmt(2*s[7]/M,3)+"</p>"; }
  });
  EX.define("b4", {
    gen: function(r){ var L=pick(r,[3,4,5,6]), H=pick(r,[1,1.5,2]), t=pick(r,[0.15,0.2,0.25]), E=pick(r,[2.5e7,3.0e7]), nu=0.2, P=pick(r,[100,200,300,500]);
      var I=t*H*H*H/12, G=E/(2*(1+nu)), db=P*L*L*L/(3*E*I), ds=P*L/(5/6*G*t*H), f=pick(r,[0.68,0.75,0.86,0.93,0.97]);
      return {L:L,H:H,t:t,E:E,nu:nu,P:P,vfe:Number(((db+ds)*f*1000).toPrecision(3))}; },
    text: function(P){ return bi("A concrete wall acts as a cantilever: L = <span class=\"num\">"+P.L+"</span> m, H = <span class=\"num\">"+P.H+"</span> m, t = <span class=\"num\">"+P.t+"</span> m, E = <span class=\"num\">"+(P.E/1e6)+" × 10⁶</span> kN m<sup>−2</sup>, ν = 0.2, end load P = <span class=\"num\">"+P.P+"</span> kN spread over the free end. A Q4 model gives a tip deflection of <span class=\"num\">"+P.vfe+"</span> mm. Find the Timoshenko bending and shear deflections (κ = 5/6) in mm, to 3 decimals, and the error of the model relative to their sum, in %, to 1 decimal.",
                                   "Sebuah dinding konkrit bertindak sebagai cantilever: L = <span class=\"num\">"+P.L+"</span> m, H = <span class=\"num\">"+P.H+"</span> m, t = <span class=\"num\">"+P.t+"</span> m, E = <span class=\"num\">"+(P.E/1e6)+" × 10⁶</span> kN m<sup>−2</sup>, ν = 0.2, load hujung P = <span class=\"num\">"+P.P+"</span> kN tersebar pada hujung bebas. Model Q4 memberi tip deflection <span class=\"num\">"+P.vfe+"</span> mm. Cari deflection lenturan dan shear Timoshenko (κ = 5/6) dalam mm, kepada 3 tempat perpuluhan, dan ralat model berbanding jumlahnya, dalam %, kepada 1 tempat perpuluhan."); },
    fields: [{id:"db", label:["δ<sub>bending</sub>","δ<sub>lenturan</sub>"], unit:"mm", fn:function(P){ var I=P.t*P.H*P.H*P.H/12; return P.P*P.L*P.L*P.L/(3*P.E*I)*1000; }, atol:0.0015, rtol:0.003},
             {id:"ds", label:["δ<sub>shear</sub>","δ<sub>shear</sub>"], unit:"mm", fn:function(P){ var G=P.E/(2*(1+P.nu)); return P.P*P.L/(5/6*G*P.t*P.H)*1000; }, atol:0.0015, rtol:0.003},
             {id:"err", label:["error","ralat"], unit:"%", fn:function(P){ var I=P.t*P.H*P.H*P.H/12, G=P.E/(2*(1+P.nu)), d=(P.P*P.L*P.L*P.L/(3*P.E*I)+P.P*P.L/(5/6*G*P.t*P.H))*1000; return (P.vfe-d)/d*100; }, atol:0.15, rtol:0}],
    hints: [function(P){ return bi("δ = PL³/(3EI) + PL/(κGA) with I = tH³/12, A = tH, G = E/(2(1 + ν)), κ = 5/6. Plane stress: use E itself in the bending term. Keep kN and m, then convert to mm.",
                                      "δ = PL³/(3EI) + PL/(κGA) dengan I = tH³/12, A = tH, G = E/(2(1 + ν)), κ = 5/6. Plane stress: guna E itu sendiri dalam term lenturan. Kekalkan kN dan m, kemudian tukar kepada mm."); },
            function(P){ var I=P.t*P.H*P.H*P.H/12, G=P.E/(2*(1+P.nu)); return bi("I = "+fmt(I,5)+" m⁴, G = "+fmt(G/1e6,4)+" × 10⁶ kN m<sup>−2</sup>, A = "+fmt(P.t*P.H,3)+" m². Error = (δ<sub>FE</sub> − δ)/δ × 100; negative means the model is too stiff.",
                                      "I = "+fmt(I,5)+" m⁴, G = "+fmt(G/1e6,4)+" × 10⁶ kN m<sup>−2</sup>, A = "+fmt(P.t*P.H,3)+" m². Ralat = (δ<sub>FE</sub> − δ)/δ × 100; negatif bermaksud model terlalu stiff."); }],
    solution: function(P){ var I=P.t*P.H*P.H*P.H/12, G=P.E/(2*(1+P.nu)), db=P.P*P.L*P.L*P.L/(3*P.E*I)*1000, ds=P.P*P.L/(5/6*G*P.t*P.H)*1000, d=db+ds;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">I = "+P.t+" × "+P.H+"³/12 = "+fmt(I,5)+" m⁴; G = "+fmt(G/1e6,4)+" × 10⁶ kN m<sup>−2</sup><br>δ<sub>b</sub> = "+P.P+" × "+P.L+"³ / (3 × "+(P.E/1e6)+"×10⁶ × "+fmt(I,5)+") = "+fmt(db,3)+" mm<br>δ<sub>s</sub> = "+P.P+" × "+P.L+" / (5/6 × "+fmt(G/1e6,4)+"×10⁶ × "+fmt(P.t*P.H,3)+") = "+fmt(ds,3)+" mm<br>δ = "+fmt(d,3)+" mm; "+bi("error","ralat")+" = ("+P.vfe+" − "+fmt(d,3)+")/"+fmt(d,3)+" = "+fmt((P.vfe-d)/d*100,1)+"%</p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("Four values of the 8 × 8 stiffness matrix", "Empat nilai stiffness matrix 8 × 8"), 4),
    ("b2", ("Nodal loads from a varying edge load and self-weight", "Nodal load daripada edge load yang berubah dan self-weight"), 4),
    ("b3", ("Global entries of the 2 × 2 cantilever mesh", "Entri global mesh cantilever 2 × 2"), 4),
    ("b4", ("The beam-theory check of a cantilever wall", "Semakan beam theory bagi dinding cantilever"), 4),
]

LAB_TASKS = [
    ("book22", ("Press “Text example” (4-node, 2 × 2, the text’s data) and read the tip deflection. Does it match the text’s −0.1306 m, and how far is it from beam theory?", "Tekan “Text example” (4-node, 2 × 2, data teks) dan baca tip deflection. Adakah ia sepadan dengan −0.1306 m dalam teks, dan sejauh mana ia daripada beam theory?"),
               ("detected when the 4-node 2 × 2 mesh is solved with the text’s data", "dikesan apabila mesh 4-node 2 × 2 diselesaikan dengan data teks")),
    ("layouts", ("Same eight elements, three layouts: 4-node 4 × 2, 8 × 1 and 2 × 4. Which is stiffest, and why?", "Lapan element yang sama, tiga susunan: 4-node 4 × 2, 8 × 1 dan 2 × 4. Yang mana paling stiff, dan mengapa?"),
                ("detected when the 4-node 4 × 2, 8 × 1 and 2 × 4 meshes have all been solved with the text’s data", "dikesan apabila mesh 4-node 4 × 2, 8 × 1 dan 2 × 4 semuanya telah diselesaikan dengan data teks")),
    ("study", ("Run the mesh study. Find the coarsest 4-node and 8-node meshes within 2% of beam theory and compare their dofs.", "Jalankan kajian mesh. Cari mesh 4-node dan 8-node paling kasar dalam 2% daripada beam theory dan bandingkan dof-nya."),
              ("detected when the mesh study runs with the text’s data", "dikesan apabila kajian mesh dijalankan dengan data teks")),
    ("point", ("Replace the edge traction by a point force at the top corner (same total). What happens at the loaded node, and at mid-span?", "Gantikan traction tepi dengan point force pada bucu atas (jumlah yang sama). Apa yang berlaku pada node yang dibebankan, dan di tengah rentang?"),
              ("detected when the point force at the top corner is solved with the text’s data otherwise", "dikesan apabila point force pada bucu atas diselesaikan dengan data teks yang lain")),
]

GLOSSARY = [
    ("Galerkin, vector version", "Weighted residual with [N]ᵀ as the weight: eight equations per four-node element, one per dof.", "Weighted residual dengan [N]ᵀ sebagai weight: lapan persamaan setiap four-node element, satu setiap dof."),
    ("strain–displacement matrix [B]", "[B] = [∂]ᵀ[N], 3 × 8: the strains {ε} = [B]{û} at any point of the element; each row sums to zero.", "[B] = [∂]ᵀ[N], 3 × 8: strain {ε} = [B]{û} pada mana-mana titik element; setiap baris berjumlah sifar."),
    ("stiffness matrix [k]", "t∫[B]ᵀ[E][B] dA, 8 × 8, symmetric; units force per length (N m<sup>−1</sup> or kN m<sup>−1</sup>).", "t∫[B]ᵀ[E][B] dA, 8 × 8, simetri; unit daya per panjang (N m<sup>−1</sup> atau kN m<sup>−1</sup>)."),
    ("stiffness influence coefficient k<sub>ij</sub>", "Force at dof i needed to give dof j a unit displacement with every other dof held.", "Daya pada dof i yang diperlukan untuk memberi dof j satu unit displacement dengan setiap dof lain ditahan."),
    ("s<sub>1</sub>…s<sub>12</sub>", "The twelve distinct entries of a rectangle’s [k], text (3.42); s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> (u–v couplings) do not depend on a, b.", "Dua belas entri berbeza [k] segi empat tepat, teks (3.42); s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> (gandingan u–v) tidak bergantung pada a, b."),
    ("Ē = E/(1 − ν²)", "The plane-stress modulus that multiplies the normal terms of [E]; G = Ē(1 − ν)/2 is the shear modulus.", "Modulus plane stress yang mendarab term normal dalam [E]; G = Ē(1 − ν)/2 ialah shear modulus."),
    ("zero-energy (rigid-body) modes", "Two translations and one rotation that cause no strain; [k]{d} = 0 for each, so [k] is singular until supported.", "Dua translation dan satu rotation yang tidak menyebabkan strain; [k]{d} = 0 bagi setiap satu, jadi [k] singular sehingga ditahan."),
    ("row-sum check", "In every row of [k] the u-entries and the v-entries each add up to zero.", "Dalam setiap baris [k], entri u dan entri v masing-masing berjumlah sifar."),
    ("Gauss quadrature", "Numerical integration at chosen points; 2 × 2 points integrate the Q4 [k] of a rectangle exactly.", "Numerical integration pada titik terpilih; 2 × 2 titik meng-integrate [k] Q4 segi empat tepat dengan tepat."),
    ("consistent (equivalent) nodal loads", "Nodal forces that do the same work as a distributed load; a uniform edge load gives pℓ/2 to each edge node.", "Daya nod yang melakukan kerja yang sama seperti load teragih; edge load seragam memberi pℓ/2 kepada setiap node tepi."),
    ("traction · line load", "Traction is force per unit area of edge (kN m<sup>−2</sup>); a line load is per unit length for the whole thickness (kN m<sup>−1</sup>) = traction × t.", "Traction ialah daya per unit luas tepi (kN m<sup>−2</sup>); line load ialah per unit panjang untuk seluruh ketebalan (kN m<sup>−1</sup>) = traction × t."),
    ("body force · self-weight", "Force per unit volume; self-weight γ gives −γtab/4 in each v-dof of a Q4 element.", "Daya per unit isi padu; self-weight γ memberi −γtab/4 pada setiap dof v element Q4."),
    ("dof map", "Node n → dofs 2n − 1 (u) and 2n (v); an element’s eight global dofs in local order.", "Node n → dof 2n − 1 (u) dan 2n (v); lapan dof global sesuatu element mengikut susunan local."),
    ("scatter-add", "K<sub>IJ</sub> += k<sub>ij</sub> with I, J from the dof map; the same for {R}.", "K<sub>IJ</sub> += k<sub>ij</sub> dengan I, J daripada dof map; sama untuk {R}."),
    ("bandwidth", "How far the non-zeros of [K] spread from the diagonal; nodes numbered close together keep it narrow.", "Sejauh mana entri bukan sifar [K] tersebar dari pepenjuru; node yang dinomborkan berdekatan memastikannya sempit."),
    ("fixed dofs · reduced system", "Known displacements struck by row–column elimination; 18 − 6 = 12 equations for the 2 × 2 cantilever.", "Displacement yang diketahui dibuang melalui row–column elimination; 18 − 6 = 12 persamaan bagi cantilever 2 × 2."),
    ("reactions", "The struck rows [K]{U} − {R} at the supports; they must balance the applied loads and their moment.", "Baris yang dibuang [K]{U} − {R} pada support; ia mesti mengimbangi load yang dikenakan dan momennya."),
    ("neutral axis", "The line that neither stretches nor shortens in bending; mid-height of the cantilever (u = 0 at nodes 5 and 6).", "Garis yang tidak meregang mahupun memendek dalam lenturan; tengah ketinggian cantilever (u = 0 pada node 5 dan 6)."),
    ("Timoshenko beam", "Beam theory with shear deformation: δ = PL³/(3EI) + PL/(κGA), κ = 5/6 for a rectangle; 0.192 m for the text’s cantilever.", "Beam theory dengan shear deformation: δ = PL³/(3EI) + PL/(κGA), κ = 5/6 bagi segi empat tepat; 0.192 m bagi cantilever dalam teks."),
    ("shear locking", "Bilinear elements with straight edges cannot curve, develop spurious shear in bending and are too stiff; worst when long in the bending direction.", "Element bilinear bertepi lurus tidak boleh melengkung, menghasilkan shear palsu dalam lenturan dan terlalu stiff; paling teruk apabila panjang dalam arah lenturan."),
    ("convergence study", "The same model on at least three meshes, tabulated, until the result stops changing.", "Model yang sama pada sekurang-kurangnya tiga mesh, dijadualkan, sehingga hasilnya berhenti berubah."),
    ("patch test", "An element must reproduce a uniform state of stress exactly; one Q4 in uniform tension on rollers does.", "Element mesti menghasilkan semula keadaan stress seragam dengan tepat; satu Q4 dalam tegangan seragam di atas roller melakukannya."),
]


def short_notes(A):
    return (
        "<h3>§1 Galerkin</h3>" + A.eq("r_sys", "(3.38)", 0.5) + P("Weight with [N]ᵀ: 8 equations per element; integration by parts exposes the traction {b}.", "Weight dengan [N]ᵀ: 8 persamaan setiap element; integration by parts mendedahkan traction {b}.")
        + "<h3>§2 [B] " + B("and", "dan") + " [k]</h3>" + A.eq("r_B_def", None, 0.5) + A.eq("r_kB", None, 0.5)
        + P("Rows of [B] sum to zero. 2 × 2 Gauss points are exact for a rectangle.", "Baris [B] berjumlah sifar. 2 × 2 Gauss point tepat bagi segi empat tepat.")
        + "<h3>§3 s<sub>1</sub>…s<sub>12</sub></h3>" + A.eq("r_svals_a", None, 0.42)
        + LI([("u–v couplings s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> independent of a, b; s<sub>6</sub> = −s<sub>2</sub>, s<sub>4</sub> = −s<sub>8</sub>.", "Gandingan u–v s<sub>2</sub>, s<sub>4</sub>, s<sub>6</sub>, s<sub>8</sub> tidak bergantung pada a, b; s<sub>6</sub> = −s<sub>2</sub>, s<sub>4</sub> = −s<sub>8</sub>."),
              ("Cantilever element (× 10⁶ N m<sup>−1</sup>): s<sub>1</sub> = 0.875, s<sub>2</sub> = 0.373, s<sub>3</sub> = −0.123, s<sub>9</sub> = 1.622.", "Element cantilever (× 10⁶ N m<sup>−1</sup>): s<sub>1</sub> = 0.875, s<sub>2</sub> = 0.373, s<sub>3</sub> = −0.123, s<sub>9</sub> = 1.622.")])
        + "<h3>§4 " + B("Loads", "Load") + "</h3>" + LI([("Uniform edge: pℓ/2 each; linear: ℓ(2p<sub>i</sub> + p<sub>j</sub>)/6, ℓ(p<sub>i</sub> + 2p<sub>j</sub>)/6.", "Tepi seragam: pℓ/2 setiap satu; linear: ℓ(2p<sub>i</sub> + p<sub>j</sub>)/6, ℓ(p<sub>i</sub> + 2p<sub>j</sub>)/6."),
                                                         ("Self-weight: −γtab/4 in each v-dof. Traction × t = line load.", "Self-weight: −γtab/4 pada setiap dof v. Traction × t = line load."),
                                                         ("Cantilever: R<sub>6</sub> = R<sub>18</sub> = −2500, R<sub>12</sub> = −5000 N.", "Cantilever: R<sub>6</sub> = R<sub>18</sub> = −2500, R<sub>12</sub> = −5000 N.")])
        + "<h3>§5 Assembly</h3>" + A.eq("r_dofmap", None, 0.42)
        + P("K<sub>3,3</sub> = 2s<sub>1</sub>, K<sub>9,9</sub> = 4s<sub>1</sub>; strike dofs 1, 2, 7, 8, 13, 14 → 12 × 12; tip −0.1306 m; ΣR<sub>y</sub> = 10 kN, M = 40 kN·m.", "K<sub>3,3</sub> = 2s<sub>1</sub>, K<sub>9,9</sub> = 4s<sub>1</sub>; buang dof 1, 2, 7, 8, 13, 14 → 12 × 12; hujung −0.1306 m; ΣR<sub>y</sub> = 10 kN, M = 40 kN·m.")
        + "<h3>§6 " + B("Checks", "Semakan") + "</h3>" + A.eq("r_beam", None, 0.42)
        + P("Timoshenko 0.160 + 0.032 = 0.192 m; 2 × 2 is −32% (shear locking); 32 × 16 is −0.7%. Three meshes, one table, one check.", "Timoshenko 0.160 + 0.032 = 0.192 m; 2 × 2 ialah −32% (shear locking); 32 × 16 ialah −0.7%. Tiga mesh, satu jadual, satu semakan.")
    )


EXAMPLES_INTRO = (
    '<div class="card" style="margin-bottom:18px"><h2 style="font-size:18px;margin:0 0 6px">' + B("How plane stress is examined", "Bagaimana plane stress diuji") + '</h2>'
    + P("Model answers in the form the examiner expects: physical picture, plan, numbered steps with every substitution written out, checks, a boxed answer and an interpretation. The marks shown are a suggested scheme; the examiner’s own scheme may differ.",
        "Jawapan model dalam bentuk yang pemeriksa jangkakan: gambaran fizikal, pelan, langkah bernombor dengan setiap penggantian ditulis, semakan, jawapan berkotak dan tafsiran. Markah yang ditunjukkan ialah skema cadangan; skema pemeriksa sendiri mungkin berbeza.", "lead")
    + '<div class="tbl"><table class="howex"><tr><th>' + B("Question type", "Jenis soalan") + '</th><th>' + B("Given and wanted", "Diberi dan dikehendaki") + '</th><th>' + B("Plan and the usual trap", "Pelan dan perangkap biasa") + '</th></tr>'
    + '<tr><td>' + B("Element stiffness", "Element stiffness") + '</td><td>' + B("a, b, E, ν, t; wanted: entries of [k].", "a, b, E, ν, t; dikehendaki: entri [k].") + '</td><td>' + B("s<sub>1</sub> to s<sub>12</sub>, or two integrals. Trap: plane stress and plane strain mixed.", "s<sub>1</sub> hingga s<sub>12</sub>, atau dua integral. Perangkap: plane stress dan plane strain bercampur.") + '</td></tr>'
    + '<tr><td>' + B("Nodal loads", "Nodal load") + '</td><td>' + B("Edge load or body force; wanted: {r}.", "Edge load atau body force; dikehendaki: {r}.") + '</td><td>' + B("Equal shares for uniform loads; dofs of the load’s direction only. Trap: traction per area against load per length.", "Bahagian sama rata bagi load seragam; dof arah load sahaja. Perangkap: traction per luas berbanding load per panjang.") + '</td></tr>'
    + '<tr><td>' + B("Global stiffness entries", "Entri global stiffness") + '</td><td>' + B("Element [k] (often identical elements) and a numbered mesh; wanted: K<sub>IJ</sub>.", "[k] element (selalunya element serupa) dan mesh bernombor; dikehendaki: K<sub>IJ</sub>.") + '</td><td>' + B("Dof → node → elements containing both → local positions → sum. Trap: node number taken for dof number.", "Dof → node → element yang mengandungi kedua-duanya → kedudukan local → jumlah. Perangkap: nombor node diambil sebagai nombor dof.") + '</td></tr>'
    + '<tr><td>' + B("Small solution", "Penyelesaian kecil") + '</td><td>' + B("One or two elements, supports, loads; wanted: displacements and reactions.", "Satu atau dua element, support, load; dikehendaki: displacement dan reaction.") + '</td><td>' + B("Strike the restrained dofs, use symmetry, solve, check the reactions against the loads.", "Buang dof yang ditahan, guna simetri, selesaikan, semak reaction berbanding load.") + '</td></tr>'
    + '<tr><td>' + B("Explain", "Terangkan") + '</td><td>' + B("Plane stress against plane strain; why Q4 is stiff in bending; the patch test.", "Plane stress berbanding plane strain; mengapa Q4 stiff dalam lenturan; patch test.") + '</td><td>' + B("Claim, reason, consequence — three sentences, in that order.", "Dakwaan, sebab, akibat — tiga ayat, mengikut urutan itu.") + '</td></tr></table></div>'
    + P("Notation follows the companion: Ē = E/(1 − ν²), G = Ē(1 − ν)/2, s<sub>1</sub>…s<sub>12</sub> as in text (3.42), nodal loads r<sub>i</sub> numbered by local dof (u<sub>1</sub> = 1, v<sub>1</sub> = 2, …). Units kN and m unless stated.",
        "Notasi mengikut buku pendamping: Ē = E/(1 − ν²), G = Ē(1 − ν)/2, s<sub>1</sub>…s<sub>12</sub> seperti dalam teks (3.42), nodal load r<sub>i</sub> dinomborkan mengikut dof local (u<sub>1</sub> = 1, v<sub>1</sub> = 2, …). Unit kN dan m melainkan dinyatakan.", "lead")
    + '</div>')


def _ktable(rows, unit_en, unit_ms):
    """An 8 x 8 matrix as a scrollable table (an image of it would be unreadable on a phone)."""
    lab = [f"{'uv'[j % 2]}<sub>{j // 2 + 1}</sub>" for j in range(8)]
    head = "<tr><th></th>" + "".join(f'<th class="r" style="white-space:nowrap">{j + 1} · {lab[j]}</th>' for j in range(8)) + "</tr>"
    body = "".join(f'<tr><th style="white-space:nowrap">{i + 1} · {lab[i]}</th>'  + "".join(f'<td class="r num">{v}</td>' for v in r) + "</tr>" for i, r in enumerate(rows))
    return f'<div class="tbl"><table>{head}{body}</table></div><p class="lead" style="margin:4px 0 8px">{B(unit_en, unit_ms)}</p>'


K344 = [["0.875", "0.373", "−0.123", "−0.003", "−0.438", "−0.373", "−0.314", "0.003"], ["0.373", "1.622", "0.003", "0.623", "−0.373", "−0.811", "−0.003", "−1.434"],
        ["−0.123", "0.003", "0.875", "−0.373", "−0.314", "−0.003", "−0.438", "0.373"], ["−0.003", "0.623", "−0.373", "1.622", "0.003", "−1.434", "0.373", "−0.811"],
        ["−0.438", "−0.373", "−0.314", "0.003", "0.875", "0.373", "−0.123", "−0.003"], ["−0.373", "−0.811", "−0.003", "−1.434", "0.373", "1.622", "0.003", "0.623"],
        ["−0.314", "−0.003", "−0.438", "0.373", "−0.123", "0.003", "0.875", "−0.373"], ["0.003", "−1.434", "0.373", "−0.811", "−0.003", "0.623", "−0.373", "1.622"]]
K92 = [["5.069", "1.830", "−3.098", "−0.141", "−2.534", "−1.830", "0.563", "0.141"],
       ["1.830", "5.069", "0.141", "0.563", "−1.830", "−2.534", "−0.141", "−3.098"],
       ["−3.098", "0.141", "5.069", "−1.830", "0.563", "−0.141", "−2.534", "1.830"],
       ["−0.141", "0.563", "−1.830", "5.069", "0.141", "−3.098", "1.830", "−2.534"],
       ["−2.534", "−1.830", "0.563", "0.141", "5.069", "1.830", "−3.098", "−0.141"],
       ["−1.830", "−2.534", "−0.141", "−3.098", "1.830", "5.069", "0.141", "0.563"],
       ["0.563", "−0.141", "−2.534", "1.830", "−3.098", "0.141", "5.069", "−1.830"],
       ["0.141", "−3.098", "1.830", "−2.534", "−0.141", "0.563", "−1.830", "5.069"]]
K94 = [["2.44", "0.83", "−1.44", "−0.17", "−1.22", "−0.83", "0.22", "0.17"],
       ["0.83", "2.44", "0.17", "0.22", "−0.83", "−1.22", "−0.17", "−1.44"],
       ["−1.44", "0.17", "2.44", "−0.83", "0.22", "−0.17", "−1.22", "0.83"],
       ["−0.17", "0.22", "−0.83", "2.44", "0.17", "−1.44", "0.83", "−1.22"],
       ["−1.22", "−0.83", "0.22", "0.17", "2.44", "0.83", "−1.44", "−0.17"],
       ["−0.83", "−1.22", "−0.17", "−1.44", "0.83", "2.44", "0.17", "0.22"],
       ["0.22", "−0.17", "−1.22", "0.83", "−1.44", "0.17", "2.44", "−0.83"],
       ["0.17", "−1.44", "0.83", "−1.22", "−0.17", "0.22", "−0.83", "2.44"]]


def examples(A):
    X = []
    # ---- Example 1: stiffness matrix of a square element (companion 9.2) ----
    head = ('<div class="xhead"><h2>' + B("Example 1 · Stiffness matrix of a square element", "Contoh 1 · Stiffness matrix bagi element segi empat sama") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> entries of [k] by integration and by pattern</span><span><b>' + B("Units", "Unit") + '</b> kN, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 9.2 (textbook Exercise 3.1)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>' + B("A square plane-stress element of side 0.5 m and thickness 0.05 m has E = 2.05 × 10⁸ kN m<sup>−2</sup> and ν = 0.3. (a) Obtain k<sub>11</sub> and k<sub>12</sub> by integration, (b) write [k], and (c) check it.",
                                                                                              "Satu element plane stress segi empat sama bersisi 0.5 m dan tebal 0.05 m mempunyai E = 2.05 × 10⁸ kN m<sup>−2</sup> dan ν = 0.3. (a) Dapatkan k<sub>11</sub> dan k<sub>12</sub> melalui integration, (b) tulis [k], dan (c) semak.") + '</div>')
    body = (head + q + A.fig("fig_v1_square", "The element of Examples 1 and 2.", "Element bagi Contoh 1 dan 2.", 400)
            + PIC("k<sub>11</sub> is the force in x at node 1 that moves node 1 one unit in x with every other dof held. The movement shortens side 1–2, resisted by Ē = E/(1 − ν²), and shears the element, because node 1 moves while node 4 above it does not, resisted by G. k<sub>12</sub>, the force in y that comes with it, arises from the Poisson effect and from the same shear.",
                  "k<sub>11</sub> ialah daya dalam x pada node 1 yang menggerakkan node 1 satu unit dalam x dengan setiap dof lain ditahan. Pergerakan itu memendekkan sisi 1–2, ditentang oleh Ē = E/(1 − ν²), dan men-shear element, kerana node 1 bergerak manakala node 4 di atasnya tidak, ditentang oleh G. k<sub>12</sub>, daya dalam y yang menyertainya, timbul daripada kesan Poisson dan daripada shear yang sama.")
            + PLAN("Columns 1 and 2 of [B] → integrate k<sub>11</sub> and k<sub>12</sub> → s<sub>1</sub> to s<sub>12</sub> → [k] by the pattern (3.42) → row sums and a rigid rotation.")
            + XSTEP(1, "(a) Columns 1 and 2 of [B]", "(a) Lajur 1 dan 2 [B]", 2, A.eq("v1_Bcols") + P("with Ē = E/(1 − ν²) and G = Ē(1 − ν)/2 in [E].", "dengan Ē = E/(1 − ν²) dan G = Ē(1 − ν)/2 dalam [E]."))
            + XSTEP(2, "(a) k₁₁ by integration", "(a) k₁₁ melalui integration", 4, A.eq("v1_k11"))
            + XSTEP(3, "(a) k₁₂ by integration", "(a) k₁₂ melalui integration", 4, A.eq("v1_k12")
                    + P("The integral of (a − x)(b − y) over the element is a²b²/4, so k<sub>12</sub> contains neither a nor b.", "Integral (a − x)(b − y) atas element ialah a²b²/4, jadi k<sub>12</sub> tidak mengandungi a mahupun b."))
            + XSTEP(4, "(b) The twelve values and [k]", "(b) Dua belas nilai dan [k]", 4, A.eq("v1_nums") + A.eq("v1_sq")
                    + _ktable(K92, "[k] × 10⁶ kN m<sup>−1</sup>, in the pattern of (3.42); dof order u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.", "[k] × 10⁶ kN m<sup>−1</sup>, dalam pola (3.42); susunan dof u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>.")
                    + ANS("(b) s<sub>1</sub> = 5.069, s<sub>2</sub> = 1.830, s<sub>3</sub> = −3.098, s<sub>5</sub> = −2.534, s<sub>7</sub> = 0.563, s<sub>8</sub> = 0.141 (× 10⁶ kN m<sup>−1</sup>); [k] as tabulated."))
            + XSTEP(5, "(c) Checks", "(c) Semakan", 6, A.eq("v1_rows") + A.eq("v1_rot")
                    + CHK("Symmetric; u- and v-entries of row 1 each sum to zero; a rigid rotation gives zero force. The other rows check in the same way.")
                    + ANS("(c) [k] passes the three rigid-body checks."))
            + INTERP("The u–u entries are those of a heat element with k<sub>x</sub> = Et/(1 − ν²) and k<sub>y</sub> = Gt: moving u along x stretches the material, moving it along y shears it. As for a square heat element, the stiffness does not depend on the side: doubling a and b leaves [k] unchanged, so only E, ν and t matter. The coupling terms s<sub>2</sub> and s<sub>8</sub> are independent of the element’s size and shape; with ν = 1/3, s<sub>8</sub> would vanish.",
                     "Entri u–u ialah entri element haba dengan k<sub>x</sub> = Et/(1 − ν²) dan k<sub>y</sub> = Gt: menggerakkan u sepanjang x meregangkan bahan, menggerakkannya sepanjang y men-shear bahan. Seperti element haba segi empat sama, stiffness tidak bergantung pada sisinya: menggandakan a dan b tidak mengubah [k], jadi hanya E, ν dan t yang penting. Term gandingan s<sub>2</sub> dan s<sub>8</sub> tidak bergantung pada saiz dan bentuk element; dengan ν = 1/3, s<sub>8</sub> akan lenyap.")
            + SCHEME([("Columns of [B] with Ē and G identified", "Lajur [B] dengan Ē dan G dikenal pasti", 2), ("k<sub>11</sub>: integrand and integration", "k<sub>11</sub>: integrand dan integration", 4), ("k<sub>12</sub>: integrand and integration", "k<sub>12</sub>: integrand dan integration", 4),
                      ("Six distinct values and the square’s equalities", "Enam nilai berbeza dan kesamaan segi empat sama", 4), ("Row sums and the rigid rotation", "Jumlah baris dan rotation tegar", 6)], 20))
    X.append(("v1", "Stiffness matrix of a square element", "Stiffness matrix bagi element segi empat sama", body))

    # ---- Example 2: nodal loads (9.3) and global entries (9.4) ----
    head = ('<div class="xhead"><h2>' + B("Example 2 · Nodal loads, and global entries from a given element matrix", "Contoh 2 · Nodal load, dan entri global daripada matrix element yang diberi") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> edge load and body force; K<sub>IJ</sub> from [k] and the connectivity</span><span><b>' + B("Units", "Unit") + '</b> kN, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Examples 9.3 (textbook Exercise 3.2) and 9.4</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>' + B("For the element of Example 1, determine the nodal loads for (a) a load of −25 kN m<sup>−1</sup> in y on its right side, (b) the self-weight of steel, γ = 78.5 kN m<sup>−3</sup>, and (c) a load in y varying linearly along the right side from 0 at node 2 to −25 kN m<sup>−1</sup> at node 3. "
                                                                                              "(d) The structure in the figure below is modelled by four identical elements whose matrix, in the local dof order of Example 1, is given. Determine K<sub>9,11</sub>, K<sub>16,16</sub>, K<sub>8,7</sub> and K<sub>13,20</sub>.",
                                                                                              "Bagi element Contoh 1, tentukan nodal load untuk (a) load −25 kN m<sup>−1</sup> dalam y pada sisi kanannya, (b) self-weight keluli, γ = 78.5 kN m<sup>−3</sup>, dan (c) load dalam y yang berubah secara linear sepanjang sisi kanan daripada 0 pada node 2 kepada −25 kN m<sup>−1</sup> pada node 3. "
                                                                                              "(d) Struktur dalam rajah di bawah dimodelkan dengan empat element serupa yang matrix-nya, dalam susunan dof local Contoh 1, diberi. Tentukan K<sub>9,11</sub>, K<sub>16,16</sub>, K<sub>8,7</sub> dan K<sub>13,20</sub>.") + '</div>')
    body = (head + q
            + PIC("A uniform load is shared equally by the two nodes of its side, and a uniform body force by the four nodes of the element. A load that grows towards node 3 must put more on node 3, with its resultant at two thirds of the side from node 2. In (d) each global entry collects the stiffness every element contributes between its two dofs; only elements that contain both nodes contribute.",
                  "Load yang seragam dikongsi sama rata oleh dua node sisinya, dan body force yang seragam oleh empat node element. Load yang membesar ke arah node 3 mesti meletakkan lebih pada node 3, dengan paduannya pada dua pertiga sisi dari node 2. Dalam (d), setiap entri global mengumpul stiffness yang disumbangkan setiap element antara dua dof-nya; hanya element yang mengandungi kedua-dua node menyumbang.")
            + PLAN("(a) pℓ/2 → (b) γtab/4 → (c) ℓ(2p<sub>i</sub> + p<sub>j</sub>)/6 with total and moment checks → (d) dof → node → elements containing both → local positions → sum.")
            + XSTEP(1, "(a) Uniform edge load", "(a) Edge load seragam", 3, P("The right side runs from node 2 to node 3, ℓ = 0.5 m; the load is in y, so it enters v<sub>2</sub> and v<sub>3</sub> (local dofs 4 and 6).", "Sisi kanan berjalan dari node 2 ke node 3, ℓ = 0.5 m; load dalam y, jadi ia masuk ke v<sub>2</sub> dan v<sub>3</sub> (dof local 4 dan 6).") + A.eq("v2_edge"))
            + XSTEP(2, "(b) Self-weight", "(b) Self-weight", 3, A.eq("v2_self"))
            + XSTEP(3, "(c) Linearly varying load", "(c) Load yang berubah secara linear", 4, P("With p<sub>2</sub> = 0 and p<sub>3</sub> = −25 kN m<sup>−1</sup>:", "Dengan p<sub>2</sub> = 0 dan p<sub>3</sub> = −25 kN m<sup>−1</sup>:") + A.eq("v2_lin") + A.eq("v2_linchk")
                    + ANS("(a) −6.25 kN at v<sub>2</sub> and v<sub>3</sub>. (b) −0.245 kN at every v<sub>i</sub>. (c) −2.08 kN at v<sub>2</sub>, −4.17 kN at v<sub>3</sub>."))
            + XSTEP(4, "(d) Dofs and connectivity", "(d) Dof dan connectivity", 3,
                    A.fig("fig_v2_mesh", "The structure of (d): four identical elements, nodes 1–10.", "Struktur (d): empat element serupa, node 1–10.", 360)
                    + _ktable(K94, "The given element matrix (same local dof order as Example 1), in the units of the question.", "Matrix element yang diberi (susunan dof local yang sama seperti Contoh 1), dalam unit soalan.")
                    + '<div class="tbl"><table><tr><th>' + B("Element", "Element") + '</th><th>' + B("local 1", "local 1") + '</th><th>' + B("local 2", "local 2") + '</th><th>' + B("local 3", "local 3") + '</th><th>' + B("local 4", "local 4") + '</th></tr>'
                    + '<tr><td>1</td><td class="num">1</td><td class="num">2</td><td class="num">5</td><td class="num">4</td></tr><tr><td>2</td><td class="num">3</td><td class="num">4</td><td class="num">8</td><td class="num">7</td></tr>'
                    + '<tr><td>3</td><td class="num">4</td><td class="num">5</td><td class="num">9</td><td class="num">8</td></tr><tr><td>4</td><td class="num">5</td><td class="num">6</td><td class="num">10</td><td class="num">9</td></tr></table></div>'
                    + P("[K] is 20 × 20. Global dof 2i − 1 is U<sub>i</sub> and 2i is V<sub>i</sub>; local dof 2m − 1 is u of local node m and 2m is its v.", "[K] ialah 20 × 20. Dof global 2i − 1 ialah U<sub>i</sub> dan 2i ialah V<sub>i</sub>; dof local 2m − 1 ialah u bagi node local m dan 2m ialah v-nya."))
            + XSTEP(5, "(d) The four entries", "(d) Empat entri", 7,
                    LI([("K<sub>9,11</sub>: U<sub>5</sub> and U<sub>6</sub>. Only element 4 contains nodes 5 and 6, as its local nodes 1 and 2: local dofs 1 and 3.", "K<sub>9,11</sub>: U<sub>5</sub> dan U<sub>6</sub>. Hanya element 4 mengandungi node 5 dan 6, sebagai node local 1 dan 2: dof local 1 dan 3."),
                        ("K<sub>16,16</sub>: V<sub>8</sub>. Node 8 is local node 3 of element 2 (dof 6) and local node 4 of element 3 (dof 8).", "K<sub>16,16</sub>: V<sub>8</sub>. Node 8 ialah node local 3 bagi element 2 (dof 6) dan node local 4 bagi element 3 (dof 8)."),
                        ("K<sub>8,7</sub>: V<sub>4</sub> and U<sub>4</sub>. Node 4 is local 4 of element 1, local 2 of element 2 and local 1 of element 3.", "K<sub>8,7</sub>: V<sub>4</sub> dan U<sub>4</sub>. Node 4 ialah local 4 bagi element 1, local 2 bagi element 2 dan local 1 bagi element 3."),
                        ("K<sub>13,20</sub>: U<sub>7</sub> and V<sub>10</sub>. Nodes 7 and 10 share no element.", "K<sub>13,20</sub>: U<sub>7</sub> dan V<sub>10</sub>. Node 7 dan 10 tidak berkongsi element.")])
                    + A.eq("v2_K") + ANS("(d) K<sub>9,11</sub> = −1.44, K<sub>16,16</sub> = 4.88, K<sub>8,7</sub> = −0.83, K<sub>13,20</sub> = 0."))
            + INTERP("The loads go only to the dofs in the direction of the load; an edge load in y gives nothing to the u-dofs. The shares are the consistent loads of the bar element, because along a side the Q4 shape functions are the linear functions of a bar; the total and the moment are the two checks that catch a wrong share. In (d) the given matrix has the pattern of (3.42) for a square, with ν = 0.25 and Et = 5 in the units of the question, which reproduces every entry: "
                     + A.eq("v2_nu", None, 0.46) + " K<sub>8,7</sub> shows the u–v coupling at a node changing sign from one element to the next, so contributions from elements on different sides of a node partly cancel; at an interior node of a regular mesh they cancel completely.",
                     "Load hanya pergi ke dof dalam arah load itu; edge load dalam y tidak memberi apa-apa kepada dof u. Bahagian itu ialah consistent load bar element, kerana di sepanjang sisi shape function Q4 ialah fungsi linear bar; jumlah dan momen ialah dua semakan yang menangkap bahagian yang salah. Dalam (d), matrix yang diberi mempunyai pola (3.42) bagi segi empat sama, dengan ν = 0.25 dan Et = 5 dalam unit soalan, yang menghasilkan semula setiap entri: "
                     + A.eq("v2_nu", None, 0.46) + " K<sub>8,7</sub> menunjukkan gandingan u–v pada satu node bertukar tanda dari satu element ke element seterusnya, jadi sumbangan element di sisi berlainan sesuatu node sebahagiannya terbatal; pada node dalaman mesh yang seragam ia terbatal sepenuhnya.")
            + SCHEME([("(a) Shares and the dofs that receive them", "(a) Bahagian dan dof yang menerimanya", 3), ("(b) Weight and quarter shares", "(b) Berat dan bahagian satu perempat", 3), ("(c) Linear shares with total and moment checks", "(c) Bahagian linear dengan semakan jumlah dan momen", 4),
                      ("(d) Dof numbering and connectivity table", "(d) Penomboran dof dan connectivity table", 3), ("(d) Four entries with the local positions named", "(d) Empat entri dengan kedudukan local dinamakan", 7)], 20))
    X.append(("v2", "Nodal loads and global entries", "Nodal load dan entri global", body))

    # ---- Example 3: one element in tension (9.6) ----
    head = ('<div class="xhead"><h2>' + B("Example 3 · One element in tension: rollers and a clamped edge", "Contoh 3 · Satu element dalam tegangan: roller dan tepi clamped") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> supports, symmetry, comparison with the exact field</span><span><b>' + B("Units", "Unit") + '</b> kN, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 9.6</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>' + B("A square plate 1 m × 1 m and 0.01 m thick (E = 200 × 10⁶ kN m<sup>−2</sup>, ν = 0.3) is pulled by a uniform stress σ = 1000 kN m<sup>−2</sup> on its right side and modelled by one element. Find the nodal displacements (a) with rollers, u<sub>1</sub> = u<sub>4</sub> = 0 and v<sub>1</sub> = v<sub>2</sub> = 0, and (b) with the left side clamped, u<sub>1</sub> = v<sub>1</sub> = u<sub>4</sub> = v<sub>4</sub> = 0.",
                                                                                              "Satu plat segi empat sama 1 m × 1 m dan tebal 0.01 m (E = 200 × 10⁶ kN m<sup>−2</sup>, ν = 0.3) ditarik oleh stress seragam σ = 1000 kN m<sup>−2</sup> pada sisi kanannya dan dimodelkan dengan satu element. Cari nodal displacement (a) dengan roller, u<sub>1</sub> = u<sub>4</sub> = 0 dan v<sub>1</sub> = v<sub>2</sub> = 0, dan (b) dengan sisi kiri clamped, u<sub>1</sub> = v<sub>1</sub> = u<sub>4</sub> = v<sub>4</sub> = 0.") + '</div>')
    body = (head + q + A.fig("fig_v3_tension", "The plate of Example 3: (a) on rollers; (b) clamped on the left.", "Plat bagi Contoh 3: (a) di atas roller; (b) clamped di kiri.", 520)
            + PIC("On rollers the plate is free to contract sideways, so the stress is uniform: it stretches by σ/E = 5 × 10<sup>−6</sup> and contracts by νσ/E = 1.5 × 10<sup>−6</sup> per metre. That field is linear, and a Q4 contains linear fields, so (a) should come out exact. Clamped, the left side cannot contract, which stiffens the plate near the support: expect a slightly smaller stretch in (b), and the right-hand corners moving towards the centre line.",
                  "Di atas roller, plat bebas mengecut ke sisi, jadi stress-nya seragam: ia meregang sebanyak σ/E = 5 × 10<sup>−6</sup> dan mengecut sebanyak νσ/E = 1.5 × 10<sup>−6</sup> per meter. Field itu linear, dan Q4 mengandungi field linear, jadi (a) sepatutnya tepat. Apabila clamped, sisi kiri tidak dapat mengecut, yang menjadikan plat lebih stiff berhampiran support: jangkakan regangan yang sedikit lebih kecil dalam (b), dan bucu kanan bergerak ke arah garis tengah.")
            + PLAN("s<sub>1</sub> to s<sub>12</sub> → loads σtℓ/2 → (a) substitute the exact field into the reduced equations → (b) symmetry u<sub>3</sub> = u<sub>2</sub>, v<sub>3</sub> = −v<sub>2</sub> → a 2 × 2 system → reactions.")
            + XSTEP(1, "Element matrix and loads", "Matrix element dan load", 4, A.eq("v3_s") + P("For the unit square s<sub>9</sub> = s<sub>1</sub>, s<sub>10</sub> = s<sub>7</sub>, s<sub>11</sub> = s<sub>5</sub>, s<sub>12</sub> = s<sub>3</sub>, s<sub>6</sub> = −s<sub>2</sub>, s<sub>8</sub> = −s<sub>4</sub>.", "Bagi segi empat sama unit s<sub>9</sub> = s<sub>1</sub>, s<sub>10</sub> = s<sub>7</sub>, s<sub>11</sub> = s<sub>5</sub>, s<sub>12</sub> = s<sub>3</sub>, s<sub>6</sub> = −s<sub>2</sub>, s<sub>8</sub> = −s<sub>4</sub>.") + A.eq("v3_load"))
            + XSTEP(2, "(a) Rollers: the exact field satisfies the equations", "(a) Roller: field tepat memenuhi persamaan", 6,
                    P("The unknowns are u<sub>2</sub>, u<sub>3</sub>, v<sub>3</sub>, v<sub>4</sub>. Try the exact field:", "Unknown-nya ialah u<sub>2</sub>, u<sub>3</sub>, v<sub>3</sub>, v<sub>4</sub>. Cuba field tepat:") + A.eq("v3_exact")
                    + P("In row u<sub>2</sub> (row 3 of [k]) only four terms remain (s<sub>i</sub> in 10⁶ kN m<sup>−1</sup>, displacements in 10<sup>−6</sup> m):", "Dalam baris u<sub>2</sub> (baris 3 [k]) hanya empat term tinggal (s<sub>i</sub> dalam 10⁶ kN m<sup>−1</sup>, displacement dalam 10<sup>−6</sup> m):") + A.eq("v3_row3")
                    + P("Rows u<sub>3</sub>, v<sub>3</sub> and v<sub>4</sub> give 5, 0 and 0 in the same way, so the exact field is the solution.", "Baris u<sub>3</sub>, v<sub>3</sub> dan v<sub>4</sub> memberi 5, 0 dan 0 dengan cara yang sama, jadi field tepat itulah penyelesaiannya.")
                    + ANS("(a) u<sub>2</sub> = u<sub>3</sub> = 5.0 × 10<sup>−6</sup> m, v<sub>3</sub> = v<sub>4</sub> = −1.5 × 10<sup>−6</sup> m, exact."))
            + XSTEP(3, "(b) Clamped: symmetry gives a 2 × 2 system", "(b) Clamped: simetri memberi sistem 2 × 2", 6,
                    P("The unknowns are u<sub>2</sub>, v<sub>2</sub>, u<sub>3</sub>, v<sub>3</sub>. Plate and load are symmetric about mid-height, so u<sub>3</sub> = u<sub>2</sub> and v<sub>3</sub> = −v<sub>2</sub>; rows u<sub>2</sub> and v<sub>2</sub> (rows 3 and 4 of [k]) become",
                      "Unknown-nya ialah u<sub>2</sub>, v<sub>2</sub>, u<sub>3</sub>, v<sub>3</sub>. Plat dan load simetri tentang tengah ketinggian, jadi u<sub>3</sub> = u<sub>2</sub> dan v<sub>3</sub> = −v<sub>2</sub>; baris u<sub>2</sub> dan v<sub>2</sub> (baris 3 dan 4 [k]) menjadi")
                    + A.eq("v3_sym") + A.eq("v3_solve")
                    + ANS("(b) u<sub>2</sub> = u<sub>3</sub> = 4.85 × 10<sup>−6</sup> m (3.0% less than on rollers), v<sub>2</sub> = −v<sub>3</sub> = 1.00 × 10<sup>−6</sup> m."))
            + XSTEP(4, "Reactions as a check", "Reaction sebagai semakan", 4, P("From rows 1, 2, 7 and 8 of [k]{d} − {r}:", "Daripada baris 1, 2, 7 dan 8 bagi [k]{d} − {r}:") + A.eq("v3_react")
                    + CHK("The horizontal reactions balance the 10 kN pull; the vertical ones are equal and opposite, so they have no resultant."))
            + INTERP("(a) is the patch test: a uniform stress is reproduced exactly by one element, and therefore by any mesh of such elements; an element that failed it could not converge. (b) shows the effect of a support that prevents the Poisson contraction: the clamped side carries vertical reactions, −0.99 kN at node 1 and +0.99 kN at node 4, that hold its corners apart, and the resulting tension in y reduces the stretch in x by 3.0%. A fine mesh gives a mean stretch of the loaded side 1.2% below the free value, so one element overstates the restraint, because it spreads the effect of the clamped side over the whole plate.",
                     "(a) ialah patch test: stress yang seragam dihasilkan semula dengan tepat oleh satu element, dan oleh itu oleh mana-mana mesh element sedemikian; element yang gagal ujian ini tidak boleh converge. (b) menunjukkan kesan support yang menghalang pengecutan Poisson: sisi clamped membawa reaction menegak, −0.99 kN pada node 1 dan +0.99 kN pada node 4, yang menahan bucunya daripada mendekat, dan tegangan dalam y yang terhasil mengurangkan regangan dalam x sebanyak 3.0%. Mesh halus memberi regangan purata sisi yang dibebankan 1.2% di bawah nilai bebas, jadi satu element melebih-lebihkan kekangan itu, kerana ia menyebarkan kesan sisi clamped ke seluruh plat.")
            + SCHEME([("Element values and the two nodal loads", "Nilai element dan dua nodal load", 4), ("(a) Exact field shown to satisfy the reduced equations", "(a) Field tepat ditunjukkan memenuhi persamaan terkurang", 6),
                      ("(b) Symmetry, the 2 × 2 system and its solution", "(b) Simetri, sistem 2 × 2 dan penyelesaiannya", 6), ("Reactions and the equilibrium check", "Reaction dan semakan keseimbangan", 4)], 20))
    X.append(("v3", "One element in tension", "Satu element dalam tegangan", body))
    return X
