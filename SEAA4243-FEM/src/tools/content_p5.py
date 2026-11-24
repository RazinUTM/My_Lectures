"""Content of Part 5 — Plane Stress (Part 3): stresses from the nodal displacements, principal and von Mises stresses,
accuracy of stresses and singularities, the 8-node element, reporting an FE result, and the project brief.
Every number was recomputed with SEAA4243-FEM/code/fe_plane_stress.py (and a sparse copy of it for the 64 x 32 and
128 x 64 meshes); the worked examples follow FEM by Hand, Examples 9.7, 10.5 and 10.6."""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, QC, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME
from content_p1 import MCQ
import re

PART = {
    "n": 5, "slug": "05-plane-stress-3", "deck": "deck_w13",
    "eqs": ["eqs_w13", "eqs_w12", "eqs_w11", "eqs_ps3_ex"], "figs": ["figs_w13", "figs_w12", "figs_w11", "figs_ps3_ex"],
    "topic": ("Plane Stress", "Plane Stress"), "part": "Part 3 of 3",
    "title": "Plane Stress — Part 3",
    "sub": ("Stresses from the solved nodal displacements, {σ} = [E][B]{û}; principal and von Mises stresses; how far a computed stress can be trusted, and where it cannot; "
            "the 8-node element; and the standard for reporting a finite element result, with the group project brief.",
            "Stress daripada nodal displacement yang telah diselesaikan, {σ} = [E][B]{û}; principal stress dan von Mises stress; sejauh mana stress yang dikira boleh dipercayai, dan di mana tidak; "
            "8-node element; dan piawai melaporkan keputusan finite element, bersama taklimat projek kumpulan."),
    "pdf": "pdf/plane-stress-3-slides.pdf",
    "lab": {"id": "stress", "file": "../labs/stress.html", "name": "Stress Recovery Explorer", "inclass": "p13"},
    "minutes": {"n1": 10, "n2": 6, "n3": 9, "n4": 9, "n5": 8, "n6": 8},
    "target_min": 37,
    "code": "ps",
    "textref": "§3.4–§3.5",
    "covers": ("Parts 1 and 2 ended with the nodal displacements. This part turns them into what a design needs — strains, stresses, principal and von Mises stresses at any point — and asks how far each can be trusted: "
               "centroid values against beam theory, the jumps between elements, the fixed corner that never converges, and the 8-node element that bends without locking. "
               "It closes with the four things every FE results section needs and the brief of the group project.",
               "Part 1 dan 2 berakhir dengan nodal displacement. Bahagian ini menukarkannya kepada apa yang diperlukan dalam reka bentuk — strain, stress, principal stress dan von Mises stress pada mana-mana titik — dan bertanya sejauh mana setiap satu boleh dipercayai: "
               "nilai centroid berbanding beam theory, lompatan antara element, bucu tetap yang tidak pernah converge, dan 8-node element yang melentur tanpa locking. "
               "Ia ditutup dengan empat perkara yang wajib ada dalam setiap bahagian keputusan FE dan taklimat projek kumpulan."),
    "inclass_n": ("3 h · 5 activities", "3 jam · 5 aktiviti"),
    "inclass": [("A1 strains and stresses at (3.5, 1.3) · A2 which stresses would you report?", "A1 strain dan stress pada (3.5, 1.3) · A2 stress mana yang akan anda laporkan?"),
                ("A3 Q4 against Q8 on the cantilever · A4 the plate written up in three sentences", "A3 Q4 berbanding Q8 pada cantilever · A4 plat ditulis dalam tiga ayat"),
                ("A5 project briefing: Gate 0, your group’s one-page plan", "A5 taklimat projek: Gate 0, pelan satu halaman kumpulan anda")],
    "recall_title": ("Recall from Plane Stress Part 2", "Ingat semula Plane Stress Part 2"),
}

OUTCOMES = [
    ("Recover strains and stresses at a point of an element from its nodal displacements, {ε} = [B]{û} and {σ} = [E][B]{û}, and compute the principal and von Mises stresses.",
     "Mendapatkan semula strain dan stress pada satu titik dalam element daripada nodal displacement-nya, {ε} = [B]{û} dan {σ} = [E][B]{û}, dan mengira principal stress serta von Mises stress."),
    ("Explain where computed stresses are accurate (element centroids, away from supports and loads) and where they are not (element edges, re-entrant corners, point loads).",
     "Menerangkan di mana stress yang dikira tepat (centroid element, jauh dari support dan load) dan di mana tidak (tepi element, re-entrant corner, point load)."),
    ("Describe the 8-node element, convert an edge load into its 1/6 – 2/3 – 1/6 nodal loads, and explain why it needs far fewer elements than the 4-node element in bending.",
     "Menerangkan 8-node element, menukar edge load kepada nodal load 1/6 – 2/3 – 1/6, dan menerangkan mengapa ia memerlukan jauh lebih sedikit element berbanding 4-node element dalam bending."),
    ("Report an FE study to the project standard: idealisation, a convergence table with an error estimate, one independent check, and quantified conclusions.",
     "Melaporkan kajian FE mengikut piawai projek: idealisation, convergence table dengan anggaran ralat, satu semakan bebas, dan kesimpulan yang dikuantifikasi."),
]

CANDO = [
    ("Recover σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub> at a point from an element’s nodal displacements, keeping enough decimals.", "Mendapatkan σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub> pada satu titik daripada nodal displacement sesuatu element, dengan tempat perpuluhan yang mencukupi."),
    ("Compute σ<sub>1</sub>, σ<sub>2</sub>, the principal direction and the von Mises stress, and say which one governs concrete and which steel.", "Mengira σ<sub>1</sub>, σ<sub>2</sub>, arah principal dan von Mises stress, dan menyatakan yang mana menguasai konkrit dan yang mana keluli."),
    ("Judge a reported stress: centroid or node, converged or not, at a singularity or not; check it against beam theory away from the ends.", "Menilai stress yang dilaporkan: centroid atau node, converge atau tidak, pada singularity atau tidak; menyemaknya dengan beam theory jauh dari hujung."),
    ("Share an edge load among the nodes of an 8-node side, and explain shear locking of the 4-node element.", "Membahagikan edge load antara node sisi 8-node, dan menerangkan shear locking bagi 4-node element."),
    ("Estimate the converged value and the error of the finest mesh from three meshes.", "Menganggar nilai converge dan ralat mesh paling halus daripada tiga mesh."),
]


_NUMCELL = re.compile(r"^[\s\d.,−\-+%|×()]+$")


def _tbl(head, rows, cls=""):
    """Small HTML table; head and cells are already bilingual where needed. Columns whose body cells are all numbers are right-aligned."""
    numcol = [all(_NUMCELL.match(r[j]) for r in rows) for j in range(len(head))]
    rc = lambda j: ' class="r"' if numcol[j] else ""
    h = "".join(f"<th{rc(j)}>{c}</th>" for j, c in enumerate(head))
    b = "".join("<tr>" + "".join(f"<td{rc(j)}>{c}</td>" for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tbl"><table{(" class=" + chr(34) + cls + chr(34)) if cls else ""}><tr>{h}</tr>{b}</table></div>'


def notes(A):
    S = []
    # ---- n1: stress recovery ----
    body = (
        P("Plane Stress Part 2 ended with the nodal displacements of the cantilever. They are the primary result: the method solved for them. Everything a designer reads afterwards — strains, stresses, principal stresses, von Mises — is <i>derived</i> from them by differentiating the interpolation inside each element. "
          "The tool for that is the matrix [B] that already built [k].",
          "Plane Stress Part 2 berakhir dengan nodal displacement bagi cantilever. Itulah primary result: kaedah ini menyelesaikan nilai itu. Segala yang dibaca oleh pereka selepas itu — strain, stress, principal stress, von Mises — <i>diterbitkan</i> daripadanya dengan membezakan interpolation di dalam setiap element. "
          "Alat untuknya ialah matrix [B] yang sudah membina [k].")
        + A.eq("wn_recover")
        + H3("Three steps", "Tiga langkah")
        + OL([("<b>Locate.</b> Find the element that contains the point, take its local coordinates x, y from its local node 1 (the rule from Heat Transfer Part 2), and list its eight nodal displacements in local order, u before v at each node.",
               "<b>Cari.</b> Kenal pasti element yang mengandungi titik itu, ambil koordinat local x, y dari node local 1-nya (peraturan dari Heat Transfer Part 2), dan senaraikan lapan nodal displacement-nya mengikut susunan local, u sebelum v pada setiap node."),
              ("<b>Strains.</b> Evaluate [B] (3 × 8) at the point and multiply by {û} (8 × 1).", "<b>Strain.</b> Nilai [B] (3 × 8) pada titik itu dan darab dengan {û} (8 × 1)."),
              ("<b>Stresses.</b> Multiply by [E] (3 × 3). Then, if the design needs them, the principal and von Mises stresses (§2).", "<b>Stress.</b> Darab dengan [E] (3 × 3). Kemudian, jika reka bentuk memerlukannya, principal stress dan von Mises stress (§2).")])
        + SB(P("Column by column, [B] holds the derivatives of the four shape functions of Heat Transfer Part 1, each used twice: once for u and once for v. Written out, its three rows are the three strains:",
               "Lajur demi lajur, [B] memuatkan derivative empat shape function dari Heat Transfer Part 1, setiap satu digunakan dua kali: sekali untuk u dan sekali untuk v. Apabila ditulis penuh, tiga barisnya ialah tiga strain:"))
        + A.eq("wn_B") + A.eq("wn_rows")
        + NOTE("The usual trap", "Perangkap biasa",
               "Global coordinates in [B]. The point (3.5, 1.3) of the cantilever lies in element 4, whose node 1 is at (2, 1): [B] is evaluated at x = 1.5, y = 0.3. With the global values the shape-function derivatives are wrong, and nothing in the arithmetic warns you.",
               "Koordinat global dalam [B]. Titik (3.5, 1.3) pada cantilever terletak dalam element 4, yang node 1-nya di (2, 1): [B] dinilai pada x = 1.5, y = 0.3. Dengan nilai global, derivative shape function menjadi salah, dan tiada apa dalam aritmetik yang memberi amaran.")
        + STEP("Worked point · the cantilever at (3.5, 1.3) m (Activity 1)", "Titik bekerja · cantilever pada (3.5, 1.3) m (Aktiviti 1)",
               A.eq("wn_pt")
               + P("The nodal displacements of element 4 in local order (global nodes 5, 6, 9, 8), from the course solution of the text’s (3.49) to six decimals:",
                   "Nodal displacement element 4 mengikut susunan local (node global 5, 6, 9, 8), daripada penyelesaian kursus bagi (3.49) teks kepada enam tempat perpuluhan:")
               + _tbl([B("local node", "node local"), "1 (5)", "2 (6)", "3 (9)", "4 (8)"],
                      [["u (m)", "0", "0", "0.041967", "0.030966"], ["v (m)", "−0.043013", "−0.130421", "−0.130578", "−0.045520"]], "num")
               + P("With b − y = 0.7, y = 0.3, a − x = 0.5 and x = 1.5:", "Dengan b − y = 0.7, y = 0.3, a − x = 0.5 dan x = 1.5:")
               + A.eq("wn_eps") + A.eq("wn_E") + A.eq("wn_sig")
               + P("σ<sub>xx</sub> is tension, as it should be above the neutral axis of a cantilever loaded downwards; σ<sub>xy</sub> carries the end shear and is as large as σ<sub>xx</sub> here; σ<sub>yy</sub> is small, as beam theory assumes.",
                   "σ<sub>xx</sub> ialah tension, seperti yang sepatutnya di atas neutral axis bagi cantilever yang dibebani ke bawah; σ<sub>xy</sub> membawa shear di hujung dan sebesar σ<sub>xx</sub> di sini; σ<sub>yy</sub> kecil, seperti yang diandaikan oleh beam theory."))
        + NOTE("Keep the decimals", "Kekalkan tempat perpuluhan",
               "Strains are differences of nodal displacements, so rounding is amplified. v<sub>6</sub> = −0.130421 and v<sub>9</sub> = −0.130578 differ only in the fourth decimal; with the three decimals the text prints, ε<sub>yy</sub> doubles and σ<sub>yy</sub> becomes −214 instead of −45:",
               "Strain ialah beza antara nodal displacement, jadi pembundaran diperbesarkan. v<sub>6</sub> = −0.130421 dan v<sub>9</sub> = −0.130578 hanya berbeza pada tempat perpuluhan keempat; dengan tiga tempat perpuluhan yang dicetak dalam teks, ε<sub>yy</sub> berganda dan σ<sub>yy</sub> menjadi −214 dan bukannya −45:")
        + A.eq("wn_round")
        + SB(P("Software does exactly this at the Gauss points of every element, and then averages to the nodes for the contour plot (§4). A hand calculation lets you see what is being averaged.",
               "Perisian membuat perkara yang sama pada Gauss point setiap element, kemudian membuat purata ke node untuk contour plot (§4). Pengiraan tangan membolehkan anda melihat apa yang dipuratakan."))
        + KP([("{ε} = [B]{û}, {σ} = [E][B]{û}, from the nodal displacements of the element that contains the point, at its local coordinates.", "{ε} = [B]{û}, {σ} = [E][B]{û}, daripada nodal displacement element yang mengandungi titik itu, pada koordinat local-nya."),
              ("Cantilever at (3.5, 1.3): ε = {0.00165, −0.000745, −0.00413}; σ = {315.2, −44.9, −310.9} kN m<sup>−2</sup>.", "Cantilever pada (3.5, 1.3): ε = {0.00165, −0.000745, −0.00413}; σ = {315.2, −44.9, −310.9} kN m<sup>−2</sup>."),
              ("Keep five or six decimals in the displacements: strains are their differences.", "Kekalkan lima atau enam tempat perpuluhan dalam displacement: strain ialah beza antaranya.")])
        + QC("q1", "To find the stress at a point of a solved mesh you need", "Untuk mencari stress pada satu titik dalam mesh yang telah diselesaikan, anda memerlukan",
             [("a", "the nodal displacements of the element that contains the point, and [B] at its local coordinates", "nodal displacement element yang mengandungi titik itu, dan [B] pada koordinat local-nya"),
              ("b", "the whole global displacement vector multiplied by [K]", "keseluruhan global displacement vector didarab dengan [K]"),
              ("c", "the nodal forces of the element divided by its area", "nodal force element itu dibahagi dengan luasnya")],
             "a", "Only that element’s eight displacements enter, through [B] evaluated at the point’s local coordinates and then [E]. [K]{U} gives nodal forces (reactions), not stresses.",
             "Hanya lapan displacement element itu yang terlibat, melalui [B] yang dinilai pada koordinat local titik itu dan kemudian [E]. [K]{U} memberi nodal force (reaction), bukan stress.")
    )
    S.append(("n1", "Stresses from the nodal displacements", "Stress daripada nodal displacement", body))

    # ---- n2: principal and von Mises ----
    body = (
        P("Three stress components describe the state at a point, but a design check needs one or two numbers that do not depend on the x and y axes you happened to choose. Rotating the axes until the shear vanishes gives the principal stresses; combining the components into an equivalent uniaxial stress gives von Mises.",
          "Tiga komponen stress menerangkan keadaan pada satu titik, tetapi semakan reka bentuk memerlukan satu atau dua nombor yang tidak bergantung pada paksi x dan y yang kebetulan dipilih. Memutar paksi sehingga shear hilang memberi principal stress; menggabungkan komponen menjadi satu stress uniaxial yang setara memberi von Mises.")
        + H3("Principal stresses and their direction", "Principal stress dan arahnya")
        + A.eq("wn_principal")
        + SB(P("θ<sub>p</sub> is measured from the x-axis to the direction of σ<sub>1</sub>; −30° means 30° clockwise. On Mohr’s circle the centre is at (σ<sub>xx</sub> + σ<sub>yy</sub>)/2 = 135.1 and the radius is 359.3 kN m<sup>−2</sup>; the Stress Recovery Explorer draws it for every probe.",
               "θ<sub>p</sub> diukur dari paksi x ke arah σ<sub>1</sub>; −30° bermaksud 30° ikut arah jam. Pada Mohr’s circle, pusatnya di (σ<sub>xx</sub> + σ<sub>yy</sub>)/2 = 135.1 dan jejarinya 359.3 kN m<sup>−2</sup>; Stress Recovery Explorer melukisnya untuk setiap probe."))
        + H3("Von Mises", "Von Mises")
        + A.eq("wn_vm")
        + SB(P("In plane stress the third principal stress, σ<sub>zz</sub>, is zero, which is why von Mises can be written with σ<sub>1</sub> and σ<sub>2</sub> alone. In plane strain σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) and the formula changes.",
               "Dalam plane stress, principal stress ketiga, σ<sub>zz</sub>, ialah sifar, sebab itulah von Mises boleh ditulis dengan σ<sub>1</sub> dan σ<sub>2</sub> sahaja. Dalam plane strain σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>) dan formulanya berubah."))
        + LI([("<b>Concrete</b> cracks in tension: σ<sub>1</sub> and its direction decide where cracks open and how the reinforcement should run in a wall or a deep beam.",
               "<b>Konkrit</b> retak dalam tension: σ<sub>1</sub> dan arahnya menentukan di mana retak terbuka dan bagaimana tetulang patut disusun dalam dinding atau deep beam."),
              ("<b>Steel</b> yields when σ<sub>vM</sub> reaches f<sub>y</sub>. ANSYS plots von Mises by default; know what it is before you read the colours.",
               "<b>Keluli</b> alah apabila σ<sub>vM</sub> mencapai f<sub>y</sub>. ANSYS memplot von Mises secara default; fahami maksudnya sebelum membaca warna.")])
        + OK("Invariant check", "Semakan invariant",
             "σ<sub>1</sub> + σ<sub>2</sub> = σ<sub>xx</sub> + σ<sub>yy</sub> for any rotation: 494.4 − 224.1 = 270.3 = 315.2 − 44.9. A slip in the square root fails this check at once.",
             "σ<sub>1</sub> + σ<sub>2</sub> = σ<sub>xx</sub> + σ<sub>yy</sub> bagi sebarang putaran: 494.4 − 224.1 = 270.3 = 315.2 − 44.9. Kesilapan dalam punca kuasa dua akan gagal semakan ini serta-merta.")
        + KP([("σ<sub>1,2</sub> = centre ± radius of Mohr’s circle; θ<sub>p</sub> = ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)].", "σ<sub>1,2</sub> = pusat ± jejari Mohr’s circle; θ<sub>p</sub> = ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)]."),
              ("Cantilever at (3.5, 1.3): σ<sub>1</sub> = 494.4, σ<sub>2</sub> = −224.1 at −30.0°; σ<sub>vM</sub> = 636.8 kN m<sup>−2</sup>.", "Cantilever pada (3.5, 1.3): σ<sub>1</sub> = 494.4, σ<sub>2</sub> = −224.1 pada −30.0°; σ<sub>vM</sub> = 636.8 kN m<sup>−2</sup>."),
              ("Concrete: σ<sub>1</sub> and its direction. Steel: σ<sub>vM</sub> against f<sub>y</sub>.", "Konkrit: σ<sub>1</sub> dan arahnya. Keluli: σ<sub>vM</sub> berbanding f<sub>y</sub>.")])
        + QC("q2", "A point carries pure shear: σ<sub>xx</sub> = σ<sub>yy</sub> = 0, σ<sub>xy</sub> = 100 kN m<sup>−2</sup>. Its principal stresses are", "Satu titik mengalami pure shear: σ<sub>xx</sub> = σ<sub>yy</sub> = 0, σ<sub>xy</sub> = 100 kN m<sup>−2</sup>. Principal stress-nya ialah",
             [("a", "+100 and −100 kN m<sup>−2</sup>, at 45° to the axes", "+100 dan −100 kN m<sup>−2</sup>, pada 45° kepada paksi"), ("b", "100 and 0 kN m<sup>−2</sup>, along the axes", "100 dan 0 kN m<sup>−2</sup>, di sepanjang paksi"), ("c", "+141 and −141 kN m<sup>−2</sup>, at 45°", "+141 dan −141 kN m<sup>−2</sup>, pada 45°")],
             "a", "The centre of Mohr’s circle is 0 and its radius is √(0 + 100²) = 100, so σ<sub>1,2</sub> = ±100; tan 2θ<sub>p</sub> is infinite, so θ<sub>p</sub> = 45°. Von Mises is √3 × 100 = 173 kN m<sup>−2</sup>.",
             "Pusat Mohr’s circle ialah 0 dan jejarinya √(0 + 100²) = 100, jadi σ<sub>1,2</sub> = ±100; tan 2θ<sub>p</sub> infiniti, jadi θ<sub>p</sub> = 45°. Von Mises ialah √3 × 100 = 173 kN m<sup>−2</sup>.")
    )
    S.append(("n2", "Principal and von Mises stresses", "Principal stress dan von Mises stress", body))

    # ---- n3: accuracy of stresses ----
    body = (
        P("The method solves for displacements; stresses come one differentiation later. A bilinear displacement field has strains that are only linear at best, and each element computes them from its own nodes, so stresses are one order less accurate than displacements and they jump from one element to the next. "
          "On the 2 × 2 cantilever the tip deflection is 32% low; some of the stresses are worse.",
          "Kaedah ini menyelesaikan displacement; stress datang selepas satu pembezaan. Displacement field bilinear mempunyai strain yang paling baik pun hanya linear, dan setiap element mengiranya daripada node sendiri, jadi stress kurang tepat satu peringkat berbanding displacement dan ia melompat dari satu element ke element seterusnya. "
          "Pada cantilever 2 × 2, tip deflection rendah 32%; sesetengah stress lebih teruk.")
        + H3("Beam theory as the check", "Beam theory sebagai semakan")
        + A.eq("wn_beam") + A.eq("wn_beam_pt")
        + _tbl([B("Point (m)", "Titik (m)"), "2 × 2 Q4", B("converged", "converge"), B("beam theory", "beam theory")],
               [[B("(1.0, 1.5) centroid of element 3", "(1.0, 1.5) centroid element 3"), "1645", "2265", "2250"],
                [B("(2.0, 1.3) mid-span, on the side shared by elements 3 | 4", "(2.0, 1.3) tengah rentang, pada sisi dikongsi element 3 | 4"), "857 | 185", "900", "900"],
                [B("(3.0, 1.5) centroid of element 4", "(3.0, 1.5) centroid element 4"), "519", "730", "750"],
                [B("(3.5, 1.3) the Activity 1 point, 0.5 m from the loaded end", "(3.5, 1.3) titik Aktiviti 1, 0.5 m dari hujung berbeban"), "315", "153", "225"]], "num")
        + P("σ<sub>xx</sub> in kN m<sup>−2</sup>; converged = 8-node 64 × 32 mesh of the course solver. Two different errors are mixed in this table.",
            "σ<sub>xx</sub> dalam kN m<sup>−2</sup>; converge = mesh 8-node 64 × 32 daripada solver kursus. Dua ralat yang berbeza bercampur dalam jadual ini.", "lead")
        + LI([("<b>The mesh error</b> (first column against the second): up to 30% at the centroids of the 2 × 2 mesh, and two different values, 857 and 185, at one point on a shared side.",
               "<b>Ralat mesh</b> (lajur pertama berbanding kedua): sehingga 30% pada centroid mesh 2 × 2, dan dua nilai berbeza, 857 dan 185, pada satu titik di sisi yang dikongsi."),
              ("<b>The error of the check itself</b> (second column against the third): 0.03% at mid-span but 32% at x = 3.5 m. Near the loaded end the model applies a uniform traction, not the parabolic shear that beam theory assumes; by St-Venant’s principle the difference fades within about one depth of the end.",
               "<b>Ralat semakan itu sendiri</b> (lajur kedua berbanding ketiga): 0.03% di tengah rentang tetapi 32% pada x = 3.5 m. Berhampiran hujung berbeban, model mengenakan traction seragam, bukan shear parabola yang diandaikan oleh beam theory; menurut St-Venant’s principle, perbezaan itu pudar dalam kira-kira satu kedalaman dari hujung.")])
        + '<figure><img src="slides/img/fig_sxx.png" alt="Left: contour of sigma xx at element centroids on a 32 by 16 mesh, tension at the top and compression at the bottom, largest at the fixed end. Right: sigma xx through the depth at x of about 2 m from the element centroids, lying on the straight line of beam theory" class="figimg" style="width:min(760px,100%)">'
        + '<figcaption>' + B("σ<sub>xx</sub> at the element centroids of a 32 × 16 Q4 mesh. Right: through the depth at x ≈ 2 m the centroid values sit on the beam-theory line, within 0.25% at every depth.",
                              "σ<sub>xx</sub> pada centroid element mesh Q4 32 × 16. Kanan: merentasi kedalaman pada x ≈ 2 m, nilai centroid terletak pada garis beam theory, dalam lingkungan 0.25% pada setiap kedalaman.") + '</figcaption></figure>'
        + OK("Where to read a stress", "Di mana membaca stress",
             "At element centroids, on a mesh that has converged, at least one depth away from supports and concentrated loads. Use beam theory there as the check, and quote the difference with its sign.",
             "Pada centroid element, pada mesh yang telah converge, sekurang-kurangnya satu kedalaman jauh dari support dan load tertumpu. Gunakan beam theory di situ sebagai semakan, dan nyatakan perbezaannya bersama tandanya.")
        + KP([("Stresses are derivatives of the displacements: less accurate, and discontinuous between elements.", "Stress ialah derivative displacement: kurang tepat, dan tidak continuous antara element."),
              ("2 × 2 centroids: 73% of the converged bending stress; 32 × 16 centroids at mid-span: within 0.25% of beam theory.", "Centroid 2 × 2: 73% daripada bending stress yang converge; centroid 32 × 16 di tengah rentang: dalam 0.25% daripada beam theory."),
              ("Beam theory is a valid check only away from the ends (St-Venant).", "Beam theory ialah semakan yang sah hanya jauh dari hujung (St-Venant).")])
        + QC("q3", "On the converged mesh σ<sub>xx</sub> at (3.5, 1.3) is 153 kN m<sup>−2</sup>, while beam theory gives 225. The best explanation is", "Pada mesh yang converge, σ<sub>xx</sub> pada (3.5, 1.3) ialah 153 kN m<sup>−2</sup>, manakala beam theory memberi 225. Penjelasan terbaik ialah",
             [("a", "the mesh is still too coarse", "mesh masih terlalu kasar"), ("b", "near the loaded end the uniform traction is not the parabolic shear beam theory assumes (St-Venant)", "berhampiran hujung berbeban, traction seragam bukan shear parabola yang diandaikan beam theory (St-Venant)"), ("c", "plane stress is the wrong idealisation", "plane stress ialah idealisation yang salah")],
             "b", "The FE value has converged (64 × 32 Q8), and at mid-span the same model matches beam theory to 0.03%. The 0.5 m point is inside the end zone where the way the load is applied still matters; it is the check that is wrong there, not the model.",
             "Nilai FE telah converge (64 × 32 Q8), dan di tengah rentang model yang sama sepadan dengan beam theory hingga 0.03%. Titik 0.5 m berada dalam zon hujung di mana cara load dikenakan masih penting; semakan itulah yang salah di situ, bukan model.")
    )
    S.append(("n3", "How far can a computed stress be trusted?", "Sejauh mana stress yang dikira boleh dipercayai?", body))

    # ---- n4: display options, singularities, concentrations ----
    body = (
        P("Each element produces its own stress field. A contour plot has to decide what to show where two or more elements meet, and ANSYS offers the same three choices as the Stress Recovery Explorer.",
          "Setiap element menghasilkan stress field sendiri. Contour plot perlu memutuskan apa yang dipaparkan di tempat dua atau lebih element bertemu, dan ANSYS menawarkan tiga pilihan yang sama seperti Stress Recovery Explorer.")
        + _tbl([B("Display option", "Pilihan paparan"), B("What is shown", "Apa yang dipaparkan"), B("Use it for", "Gunakan untuk")],
               [[B("Elemental mean", "Elemental mean"), B("one value per element, at its centroid", "satu nilai setiap element, pada centroid-nya"), B("the most reliable value per element; checks against beam theory", "nilai paling boleh dipercayai setiap element; semakan dengan beam theory")],
                [B("Unaveraged", "Unaveraged"), B("each element’s own values at its nodes: jumps visible at shared sides", "nilai element sendiri pada node-nya: lompatan kelihatan pada sisi dikongsi"), B("seeing where the mesh is too coarse: large jumps, large local error", "melihat di mana mesh terlalu kasar: lompatan besar, ralat setempat besar")],
                [B("Averaged", "Averaged"), B("the mean of all elements at each node: a smooth picture", "purata semua element pada setiap node: gambaran yang licin"), B("reporting, once the unaveraged jumps are small", "pelaporan, setelah lompatan unaveraged kecil")]])
        + NOTE("A smooth plot is not an accurate plot", "Plot yang licin bukan plot yang tepat",
               "Averaging hides the jumps; it does not remove the error. Look at the unaveraged plot first: the size of the jump between neighbours is a free estimate of the local error.",
               "Purata menyembunyikan lompatan; ia tidak menghapuskan ralat. Lihat plot unaveraged dahulu: saiz lompatan antara jiran ialah anggaran percuma bagi ralat setempat.")
        + H3("The fixed corner never converges", "Bucu tetap tidak pernah converge")
        + _tbl([B("4-node mesh", "Mesh 4-node"), B("centroid of the top-left element (m)", "centroid element kiri atas (m)"), "FE σ<sub>xx</sub>", B("beam theory there", "beam theory di situ"), "FE / beam"],
               [["8 × 4", "(0.25, 1.75)", "4134", "4219", "0.98"], ["16 × 8", "(0.125, 1.875)", "5372", "5086", "1.06"], ["32 × 16", "(0.0625, 1.9375)", "6400", "5537", "1.16"], ["64 × 32", "(0.031, 1.969)", "7467", "5767", "1.30"]], "num")
        + P("Every halving of the elements raises the peak, and it passes beam theory, which itself tends to 6000 kN m<sup>−2</sup> at the corner. The elastic solution at the re-entrant corner of a fully fixed edge is infinite: refining chases infinity. A point load produces the same kind of singularity under it.",
            "Setiap kali saiz element dibahagi dua, puncaknya meningkat, dan ia melepasi beam theory, yang sendiri menghampiri 6000 kN m<sup>−2</sup> di bucu itu. Penyelesaian elastic pada re-entrant corner bagi tepi yang tetap sepenuhnya ialah infiniti: refine bermakna mengejar infiniti. Point load menghasilkan singularity yang sama di bawahnya.")
        + DEF("Singularity or concentration?", "Singularity atau concentration?",
              "A <b>singularity</b> (a fully fixed corner, a point load, a sharp re-entrant corner) has no finite peak: the peak grows with every refinement and must not be reported. A <b>stress concentration</b> (a smooth hole, a fillet) has a finite peak: it converges, and once checked it is the number the design needs.",
              "<b>Singularity</b> (bucu yang tetap sepenuhnya, point load, re-entrant corner yang tajam) tiada puncak terhingga: puncaknya meningkat dengan setiap refine dan tidak boleh dilaporkan. <b>Stress concentration</b> (lubang yang licin, fillet) mempunyai puncak terhingga: ia converge, dan setelah disemak, itulah nombor yang diperlukan reka bentuk.")
        + '<figure><img src="slides/img/w13_hole_vm.png" alt="Von Mises stress in a plate with a central hole under tension, highest at the top and bottom edges of the hole" class="figimg" style="width:min(520px,100%)">'
        + '<figcaption>' + B("A concentration that converges: a steel plate 0.4 m × 0.1 m in tension with a hole of d/W = 0.3, PLANE183. Far field 10.0 MPa, peak von Mises 33.4 MPa at the edge of the hole, K<sub>t</sub> = 2.34 on the net section against Peterson’s 2.35.",
                              "Concentration yang converge: plat keluli 0.4 m × 0.1 m dalam tension dengan lubang d/W = 0.3, PLANE183. Medan jauh 10.0 MPa, puncak von Mises 33.4 MPa di tepi lubang, K<sub>t</sub> = 2.34 pada keratan bersih berbanding 2.35 Peterson.")
        + '<span class="credit"> ' + B("Image: PyMAPDL documentation, “MAPDL 2D plane stress concentration analysis”, © ANSYS, Inc., MIT licence.", "Imej: dokumentasi PyMAPDL, “MAPDL 2D plane stress concentration analysis”, © ANSYS, Inc., lesen MIT.") + '</span></figcaption></figure>'
        + A.eq("wn_peterson")
        + SB(P("The net-section check: the nominal stress across the remaining width is 10.0/(1 − 0.3) = 14.3 MPa, and 33.4/14.3 = 2.34. That is the kind of independent check the project asks for.",
               "Semakan keratan bersih: stress nominal merentasi lebar yang tinggal ialah 10.0/(1 − 0.3) = 14.3 MPa, dan 33.4/14.3 = 2.34. Itulah jenis semakan bebas yang diminta dalam projek."))
        + KP([("Elemental mean = centroids; Unaveraged shows the jumps; Averaged is smooth but not more accurate.", "Elemental mean = centroid; Unaveraged menunjukkan lompatan; Averaged licin tetapi tidak lebih tepat."),
              ("Fixed corner: 4134 → 5372 → 6400 → 7467 kN m<sup>−2</sup>, no limit. Never report a peak at a singularity.", "Bucu tetap: 4134 → 5372 → 6400 → 7467 kN m<sup>−2</sup>, tiada had. Jangan sekali-kali laporkan puncak pada singularity."),
              ("A smooth hole converges: K<sub>t</sub> = 2.34 against Peterson’s 2.35.", "Lubang yang licin converge: K<sub>t</sub> = 2.34 berbanding 2.35 Peterson.")])
        + QC("q4", "Your model shows its highest von Mises stress right at a fully fixed corner, and the value grows when you refine. You", "Model anda menunjukkan von Mises stress tertinggi tepat pada bucu yang tetap sepenuhnya, dan nilainya meningkat apabila anda refine. Anda",
             [("a", "report the finest-mesh value as the design stress", "melaporkan nilai mesh paling halus sebagai design stress"), ("b", "treat it as a singularity: report stresses a short distance away, or model the support realistically", "menganggapnya sebagai singularity: melaporkan stress sedikit jauh dari situ, atau memodelkan support secara realistik"), ("c", "switch to plane strain", "menukar kepada plane strain")],
             "b", "A peak that grows without limit is a singularity of the idealised support, not a property of the structure. Show the divergence in the mesh study, then report values outside the corner zone, or model the real support (a bearing, a flexible wall) so the peak becomes finite.",
             "Puncak yang meningkat tanpa had ialah singularity bagi support yang diidealkan, bukan sifat struktur. Tunjukkan divergence dalam kajian mesh, kemudian laporkan nilai di luar zon bucu, atau modelkan support sebenar (bearing, dinding fleksibel) supaya puncak menjadi terhingga.")
    )
    S.append(("n4", "Display options, singularities and concentrations", "Pilihan paparan, singularity dan concentration", body))

    # ---- n5: the 8-node element ----
    body = (
        P("The 8-node (serendipity) element adds a node at the middle of each side. Its displacement field is quadratic along every side, so the sides can curve, and that is its whole advantage in bending: a bent beam has curved fibres, and an element whose sides must stay straight can only imitate them by shearing (Example 3).",
          "8-node (serendipity) element menambah satu node di tengah setiap sisi. Displacement field-nya quadratic di sepanjang setiap sisi, jadi sisinya boleh melengkung, dan itulah keseluruhan kelebihannya dalam bending: beam yang melentur mempunyai fibre melengkung, dan element yang sisinya mesti kekal lurus hanya boleh meniru lengkungan itu dengan shear (Contoh 3).")
        + A.eq("t_q8_sizes") + A.eq("t_q8_N")
        + A.fig("fig_q8_mesh", "The text’s 2 × 1 mesh of 8-node elements: 13 nodes, 26 dofs (text Fig. 3.6).", "Mesh 2 × 1 8-node element dalam teks: 13 node, 26 dof (teks Rajah 3.6).", 460)
        + SB(P("The recipe is unchanged: [B] = [∂]ᵀ[N] and [k] = t∫[B]ᵀ[E][B] dA, now 16 × 16 with 3 × 3 Gauss points. Nobody computes it by hand; the text lists it in its MATLAB code (§3.4.2).",
               "Resipinya tidak berubah: [B] = [∂]ᵀ[N] dan [k] = t∫[B]ᵀ[E][B] dA, kini 16 × 16 dengan 3 × 3 Gauss point. Tiada siapa mengiranya dengan tangan; teks menyenaraikannya dalam kod MATLAB-nya (§3.4.2)."))
        + H3("Edge loads on a three-node side", "Edge load pada sisi tiga node")
        + SB(P("Along a side the quadratic shape functions integrate to ℓ/6, 2ℓ/3 and ℓ/6, so a uniform edge load is no longer shared half and half: the mid-side node takes two thirds.",
               "Di sepanjang sisi, shape function quadratic ber-integral kepada ℓ/6, 2ℓ/3 dan ℓ/6, jadi edge load seragam tidak lagi dibahagi separuh-separuh: node tengah sisi mengambil dua pertiga."))
        + A.eq("wn_q8load", "(3.51)")
        + A.fig("fig_edge_loads", "The same uniform load q on a side of length ℓ: one 8-node side (left) against two 4-node sides (right). The totals are equal; the shares are not.",
                "Load seragam q yang sama pada sisi sepanjang ℓ: satu sisi 8-node (kiri) berbanding dua sisi 4-node (kanan). Jumlahnya sama; bahagiannya tidak.", 460)
        + H3("What it buys", "Apa yang diperoleh")
        + _tbl([B("Mesh", "Mesh"), B("dofs", "dof"), B("tip deflection (m)", "tip deflection (m)"), B("against 0.1915", "berbanding 0.1915")],
               [["Q4 2 × 2", "18", "0.1306", "−31.8%"], ["Q8 2 × 1", "26", "0.1780", "−7.1%"], ["Q8 4 × 2", "74", "0.1885", "−1.6%"], ["Q4 16 × 8", "306", "0.1886", "−1.5%"],
                ["Q8 4 × 4", "130", "0.1896", "−1.0%"], ["Q4 16 × 16", "578", "0.1893", "−1.1%"], ["Q8 8 × 4", "242", "0.1906", "−0.5%"], ["Q4 32 × 16", "1122", "0.1906", "−0.5%"]], "num")
        + P("Reference: the converged plane-stress value, 0.1915 m (Q4 128 × 64). Timoshenko beam theory gives 0.1919 m, a different model 0.2% stiffer in shear. Text Table 3.2 lists the same comparison to three decimals.",
            "Rujukan: nilai plane stress yang converge, 0.1915 m (Q4 128 × 64). Timoshenko beam theory memberi 0.1919 m, model berbeza yang 0.2% lebih kaku dalam shear. Jadual 3.2 teks menyenaraikan perbandingan yang sama kepada tiga tempat perpuluhan.", "lead")
        + OK("Cost is degrees of freedom, not elements", "Kos ialah degree of freedom, bukan element",
             "For the same 0.5% error the Q8 8 × 4 mesh needs 242 dofs and the Q4 32 × 16 mesh 1122. In ANSYS, PLANE183 is the 8-node element and PLANE182 the 4-node one; Workbench meshes 2D solids with the quadratic element by default — now you know why.",
             "Untuk ralat 0.5% yang sama, mesh Q8 8 × 4 memerlukan 242 dof dan mesh Q4 32 × 16 memerlukan 1122. Dalam ANSYS, PLANE183 ialah 8-node element dan PLANE182 ialah 4-node; Workbench menggunakan element quadratic untuk 2D solid secara default — kini anda tahu sebabnya.")
        + KP([("Q8: 16 dofs, quadratic sides that can curve; no parasitic shear in bending.", "Q8: 16 dof, sisi quadratic yang boleh melengkung; tiada parasitic shear dalam bending."),
              ("Uniform edge load: qℓ/6, 2qℓ/3, qℓ/6. Cantilever 2 × 1: −1667, −6667, −1667 N.", "Edge load seragam: qℓ/6, 2qℓ/3, qℓ/6. Cantilever 2 × 1: −1667, −6667, −1667 N."),
              ("Two Q8 elements: −7%; four Q4: −32%. Compare meshes by dofs.", "Dua Q8 element: −7%; empat Q4: −32%. Bandingkan mesh mengikut dof.")])
        + QC("q5", "A uniform edge load q acts on the side of length ℓ of an 8-node element. The mid-side node receives", "Edge load seragam q bertindak pada sisi sepanjang ℓ bagi 8-node element. Node tengah sisi menerima",
             [("a", "qℓ/2", "qℓ/2"), ("b", "2qℓ/3", "2qℓ/3"), ("c", "qℓ/3", "qℓ/3")],
             "b", "The quadratic edge shape functions integrate to ℓ/6, 2ℓ/3 and ℓ/6, so the mid-side node takes two thirds and each corner one sixth; the total is qℓ. qℓ/2 is the share of the middle node of two 4-node sides.",
             "Shape function tepi quadratic ber-integral kepada ℓ/6, 2ℓ/3 dan ℓ/6, jadi node tengah sisi mengambil dua pertiga dan setiap bucu satu perenam; jumlahnya qℓ. qℓ/2 ialah bahagian node tengah bagi dua sisi 4-node.")
    )
    S.append(("n5", "The 8-node element", "8-node element", body))

    # ---- n6: reporting and the project ----
    body = (
        P("A number without a mesh study and a check is an opinion. The project is marked on whether your numbers can be defended, and so is any FE result you will sign in practice.",
          "Nombor tanpa kajian mesh dan semakan hanyalah pendapat. Projek dinilai berdasarkan sama ada nombor anda boleh dipertahankan, dan begitu juga mana-mana keputusan FE yang akan anda tandatangani dalam amalan.")
        + H3("Four things every results section needs", "Empat perkara yang wajib ada dalam setiap bahagian keputusan")
        + OL([("<b>Idealisation stated.</b> Plane stress or plane strain and why; thickness; E and ν with units; supports and loads with a sketch; what was left out (self-weight, openings, reinforcement).",
               "<b>Idealisation dinyatakan.</b> Plane stress atau plane strain dan sebabnya; ketebalan; E dan ν dengan unit; support dan load dengan lakaran; apa yang ditinggalkan (berat sendiri, bukaan, tetulang)."),
              ("<b>A convergence table.</b> At least three meshes, the quantity of interest for each, the change between the last two in per cent, and which mesh the results come from. Three meshes also give an error estimate (Example 2).",
               "<b>Convergence table.</b> Sekurang-kurangnya tiga mesh, kuantiti yang dikehendaki bagi setiap satu, perubahan antara dua yang terakhir dalam peratus, dan mesh mana yang menjadi sumber keputusan. Tiga mesh juga memberi anggaran ralat (Contoh 2)."),
              ("<b>One independent check.</b> Beam theory away from the ends, equilibrium of the reactions against the loads, a textbook stress-concentration factor, or a hand calculation on a coarse mesh. Quote the difference with its sign.",
               "<b>Satu semakan bebas.</b> Beam theory jauh dari hujung, keseimbangan reaction berbanding load, stress-concentration factor dari buku teks, atau pengiraan tangan pada mesh kasar. Nyatakan perbezaan bersama tandanya."),
              ("<b>Quantified conclusions.</b> “The tip deflection is 0.191 m, within 0.7% of beam theory”, not “the results agree well”. Say where the maximum is, what it means for the design, and what the model cannot tell you.",
               "<b>Kesimpulan yang dikuantifikasi.</b> “Tip deflection ialah 0.191 m, dalam 0.7% daripada beam theory”, bukan “keputusan sepadan dengan baik”. Nyatakan di mana maksimum, apa maksudnya untuk reka bentuk, dan apa yang model tidak dapat beritahu.")])
        + STEP("Model paragraph · the cantilever in five sentences", "Perenggan model · cantilever dalam lima ayat",
               P("The cantilever (4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33) was idealised as plane stress with the left edge fully fixed and the 5 kN m<sup>−1</sup> end load applied as an edge traction. "
                 "Four-node meshes of 2 × 2, 8 × 4, 16 × 8 and 32 × 16 elements gave tip deflections of 0.131, 0.182, 0.189 and 0.191 m; the change between the last two meshes is 1.0%, so the 32 × 16 results are reported. "
                 "Timoshenko beam theory gives 0.192 m (0.160 m bending, 0.032 m shear), 0.7% above the FE value. "
                 "The bending stress at element centroids at mid-span agrees with M(y − 1)/I to within 0.25%; the stress at the fixed corner increases without bound under refinement and is not reported. "
                 "The reactions sum to 10.0 kN upward and 40.0 kN m, equal to the applied load and its moment.",
                 "(Ditulis dalam bahasa Inggeris kerana laporan projek ditulis dalam bahasa Inggeris.) The cantilever (4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33) was idealised as plane stress with the left edge fully fixed and the 5 kN m<sup>−1</sup> end load applied as an edge traction. "
                 "Four-node meshes of 2 × 2, 8 × 4, 16 × 8 and 32 × 16 elements gave tip deflections of 0.131, 0.182, 0.189 and 0.191 m; the change between the last two meshes is 1.0%, so the 32 × 16 results are reported. "
                 "Timoshenko beam theory gives 0.192 m (0.160 m bending, 0.032 m shear), 0.7% above the FE value. "
                 "The bending stress at element centroids at mid-span agrees with M(y − 1)/I to within 0.25%; the stress at the fixed corner increases without bound under refinement and is not reported. "
                 "The reactions sum to 10.0 kN upward and 40.0 kN m, equal to the applied load and its moment.")
               + P("Every sentence carries a number, a comparison or a decision. No adjectives.", "Setiap ayat membawa nombor, perbandingan atau keputusan. Tiada kata sifat."))
        + H3("The group project: ANSYS first, your own tool as the independent check", "Projek kumpulan: ANSYS dahulu, alat anda sendiri sebagai semakan bebas")
        + SB(P("CLO4: investigate a 2D structural problem with FEM, in a group, with software, and defend the numbers. ANSYS is the primary analysis. Each group also builds a small plane-stress solver of its own, written with generative AI if you wish (“vibe coding”) and deployed on GitHub Pages, as an independent check of the ANSYS model. Items in square brackets are announced by the lecturer.",
               "CLO4: mengkaji masalah struktur 2D dengan FEM, secara berkumpulan, menggunakan perisian, dan mempertahankan nombor-nombornya. ANSYS ialah analisis utama. Setiap kumpulan juga membina solver plane stress kecil sendiri, ditulis dengan generative AI jika mahu (“vibe coding”) dan di-deploy di GitHub Pages, sebagai semakan bebas bagi model ANSYS. Item dalam kurungan segi empat akan diumumkan oleh pensyarah."))
        + _tbl([B("Item", "Perkara"), B("Brief", "Ringkasan")],
               [[B("Task", "Tugasan"), B("Choose a 2D structural problem, idealise it, model it in ANSYS (plane stress or plane strain), verify your own solver step by step, cross-check the ANSYS model with it, and interpret the results for design.", "Pilih masalah struktur 2D, idealkan, modelkan dalam ANSYS (plane stress atau plane strain), sahkan solver anda sendiri langkah demi langkah, semak silang model ANSYS dengannya, dan tafsirkan keputusan untuk reka bentuk.")],
                [B("Team and weight", "Kumpulan dan wajaran"), B("Groups of [4–5]; 15% of the course (CLO4). One repository and one report per group, with a line on who did what.", "Kumpulan [4–5] orang; 15% daripada kursus (CLO4). Satu repository dan satu laporan bagi setiap kumpulan, dengan satu baris tentang siapa buat apa.")],
                [B("Deliverables", "Hasil"), B("(1) Report, at most 15 pages: idealisation, ANSYS convergence table, the evidence of Gates 1–3, interpretation, limitations. (2) The tool: public GitHub repository, GitHub Pages link, README with the verification table, the limits and a licence. (3) GenAI log and a one-page reflection. (4) ANSYS files (.wbpj archive) and the hand-check sheet. (5) Demonstration and individual viva, about 20 minutes per group, on [date].",
                                                          "(1) Laporan, paling banyak 15 halaman: idealisation, convergence table ANSYS, bukti Gate 1–3, tafsiran, had. (2) Alat: repository GitHub awam, pautan GitHub Pages, README dengan jadual verification, had dan lesen. (3) Log GenAI dan refleksi satu halaman. (4) Fail ANSYS (arkib .wbpj) dan helaian semakan tangan. (5) Demonstrasi dan viva individu, kira-kira 20 minit bagi setiap kumpulan, pada [tarikh].")],
                [B("Candidates", "Calon struktur"), B("Shear wall with openings (text Exercise 3.4) · deep beam or transfer girder · gusset or connection plate · dam or retaining-wall section (plane strain).", "Shear wall dengan bukaan (Latihan 3.4 teks) · deep beam atau transfer girder · gusset atau connection plate · keratan empangan atau tembok penahan (plane strain).")],
                [B("Starting point", "Titik mula"), B("You may start from the course Python code (MIT licence) or from code an AI writes for you; say which in the README. The marks are for what you verify and can explain, not for writing every line from scratch.", "Anda boleh bermula daripada kod Python kursus (lesen MIT) atau kod yang ditulis oleh AI; nyatakan yang mana dalam README. Markah diberi untuk apa yang anda sahkan dan boleh terangkan, bukan untuk menulis setiap baris dari kosong.")]])
        + H3("Stage gates, in order", "Stage gate, mengikut urutan")
        + _tbl([B("Gate", "Gate"), B("What must be shown", "Apa yang mesti ditunjukkan"), B("When", "Bila")],
               [["0", B("Plan, before any code: the structure and its sketch, the idealisation, the quantities you will report, the checks and their tolerances, the repository name.", "Pelan, sebelum sebarang kod: struktur dan lakarannya, idealisation, kuantiti yang akan dilaporkan, semakan dan toleransinya, nama repository."), B("end of this session", "hujung sesi ini")],
                ["1", B("Core solver: one element against a hand value of [k]; the patch test exact to round-off; ΣR equal to the physical load.", "Core solver: satu element berbanding nilai tangan [k]; patch test tepat hingga round-off; ΣR sama dengan load fizikal."), B("ANSYS demo session", "sesi demo ANSYS")],
                ["2", B("Known solution: convergence of your solver to Timoshenko (the course cantilever) or Kirsch (a plate with a hole), with the observed order.", "Penyelesaian diketahui: convergence solver anda kepada Timoshenko (cantilever kursus) atau Kirsch (plat berlubang), dengan observed order."), "[date]"],
                ["3", B("ANSYS cross-check on your structure: same idealisation, comparable mesh and element; every difference above your tolerance explained, never averaged away.", "Semakan silang ANSYS pada struktur anda: idealisation yang sama, mesh dan element yang setanding; setiap perbezaan melebihi toleransi anda diterangkan, tidak sekali-kali dipuratakan."), "[date]"],
                ["4", B("UI and deployment: the tool runs from GitHub Pages; the README states what it verifies and its limits.", "UI dan deployment: alat berjalan dari GitHub Pages; README menyatakan apa yang disahkan dan hadnya."), "[date]"],
                ["5", B("Demonstration and individual viva: each member runs one gate live and explains the code and the numbers behind it.", "Demonstrasi dan viva individu: setiap ahli menjalankan satu gate secara langsung dan menerangkan kod serta nombor di sebaliknya."), "[date]"]])
        + _tbl([B("Marked component", "Komponen dinilai"), B("Marks", "Markah")],
               [[B("Verification and ANSYS cross-check (Gates 1–3)", "Verification dan semakan silang ANSYS (Gate 1–3)"), "35"],
                [B("Interpretation of the results for design", "Tafsiran keputusan untuk reka bentuk"), "20"],
                [B("Demonstration and individual viva (Gate 5)", "Demonstrasi dan viva individu (Gate 5)"), "25"],
                [B("UI, deployment and repository (Gate 4)", "UI, deployment dan repository (Gate 4)"), "10"],
                [B("GenAI log and reflection", "Log GenAI dan refleksi"), "10"],
                [B("<b>Total</b>", "<b>Jumlah</b>"), "<b>100</b>"]])
        + NOTE("Where the marks are lost", "Di mana markah hilang",
               "Fixing edges that are free; a single point load at a node; one mesh only; “results agree well” with no number; quoting the corner peak as the design stress; a tool checked only against itself, or tuned until it matches ANSYS; a tool nobody in the group can explain, which earns no verification marks. Part 6, Notes §6, shows what each gate proves and what it misses.",
               "Menetapkan tepi yang sepatutnya bebas; satu point load pada satu node; satu mesh sahaja; “keputusan sepadan dengan baik” tanpa nombor; memetik puncak di bucu sebagai design stress; alat yang disemak dengan dirinya sendiri sahaja, atau dilaraskan sehingga sama dengan ANSYS; alat yang tiada ahli kumpulan boleh terangkan, yang tidak mendapat markah verification. Part 6, Nota §6, menunjukkan apa yang dibuktikan oleh setiap gate dan apa yang terlepas.")
        + H3("Two habits that save marks", "Dua tabiat yang menyelamatkan markah")
        + '<figure><div class="figrow"><img src="slides/img/w13_its_sketch.png" alt="Sketch of a disk squeezed by two point loads P at the top and bottom" class="figimg" style="flex:0 1 150px">'
        + '<img src="slides/img/w13_its_quarter.png" alt="Quarter of the disk meshed with triangles, with roller supports on the two cut edges" class="figimg" style="flex:1 1 320px"></div>'
        + '<figcaption>' + B("Indirect tensile (Brazilian) test of a 150 mm disk, plane strain: two lines of symmetry, so one quarter is modelled with rollers on the cut edges. The loads are point forces: read the stresses away from them.",
                              "Ujian indirect tensile (Brazilian) bagi cakera 150 mm, plane strain: dua garis simetri, jadi satu perempat dimodelkan dengan roller pada tepi yang dipotong. Load ialah point force: baca stress jauh daripadanya.")
        + '<span class="credit"> ' + B("Images: SfePy documentation, Primer, BSD-3-Clause licence.", "Imej: dokumentasi SfePy, Primer, lesen BSD-3-Clause.") + '</span></figcaption></figure>'
        + LI([("<b>Use symmetry.</b> A quarter model is four times smaller; the cut edges get rollers (no displacement normal to them).", "<b>Gunakan simetri.</b> Model satu perempat empat kali lebih kecil; tepi yang dipotong diberi roller (tiada displacement normal kepadanya)."),
              ("<b>Spread concentrated loads.</b> A point force is a singularity; apply it over the real contact width, or read the stresses away from it.", "<b>Sebarkan load tertumpu.</b> Point force ialah singularity; kenakan pada lebar sentuhan sebenar, atau baca stress jauh daripadanya.")])
        + KP([("Idealisation · convergence table · one check · quantified conclusions.", "Idealisation · convergence table · satu semakan · kesimpulan yang dikuantifikasi."),
              ("Every sentence of a results section carries a number.", "Setiap ayat dalam bahagian keputusan membawa nombor."),
              ("Project: ANSYS first, your own tool as the independent check, Gates 0–5 in order; 35 marks for verification and cross-check, 25 for the viva.", "Projek: ANSYS dahulu, alat anda sendiri sebagai semakan bebas, Gate 0–5 mengikut urutan; 35 markah untuk verification dan semakan silang, 25 untuk viva.")])
        + QC("q6", "Which sentence meets the reporting standard?", "Ayat mana yang memenuhi piawai pelaporan?",
             [("a", "“The FE results agree well with beam theory.”", "“The FE results agree well with beam theory.”"),
              ("b", "“The 32 × 16 tip deflection, 0.191 m, is 0.7% below Timoshenko beam theory; the last refinement changed it by 1.0%.”", "“The 32 × 16 tip deflection, 0.191 m, is 0.7% below Timoshenko beam theory; the last refinement changed it by 1.0%.”"),
              ("c", "“The maximum bending stress is 7467 kN m<sup>−2</sup>, at the fixed corner.”", "“The maximum bending stress is 7467 kN m<sup>−2</sup>, at the fixed corner.”")],
             "b", "(b) gives the number, the comparison with its sign and the convergence. (a) has no number. (c) quotes a singular peak: 7467 kN m<sup>−2</sup> is σ<sub>xx</sub> at the corner centroid of the 64 × 32 mesh, and it would rise again on the next mesh.",
             "(b) memberi nombor, perbandingan bersama tandanya dan convergence. (a) tiada nombor. (c) memetik puncak singular: 7467 kN m<sup>−2</sup> ialah σ<sub>xx</sub> pada centroid bucu mesh 64 × 32, dan ia akan naik lagi pada mesh seterusnya.")
    )
    S.append(("n6", "Reporting an FE result, and the project", "Melaporkan keputusan FE, dan projek", body))
    return S


RECALL = [
    QC("r1", "Recall · for a four-node plane-stress element, the size of [B] is", "Ingat semula · bagi four-node plane-stress element, saiz [B] ialah",
       [("a", "2 × 8", "2 × 8"), ("b", "3 × 8", "3 × 8"), ("c", "8 × 8", "8 × 8")],
       "b", "Three strains (ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub>) from eight nodal displacements: [B] = [∂]ᵀ[N] is 3 × 8. [N] is 2 × 8 and [k] = t∫[B]ᵀ[E][B] dA is 8 × 8. Today [B] turns the solved displacements into strains.",
       "Tiga strain (ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub>) daripada lapan nodal displacement: [B] = [∂]ᵀ[N] bersaiz 3 × 8. [N] bersaiz 2 × 8 dan [k] = t∫[B]ᵀ[E][B] dA bersaiz 8 × 8. Hari ini [B] menukar displacement yang diselesaikan kepada strain."),
    QC("r2", "Recall · the 2 × 2 Q4 mesh gives a tip deflection of 0.131 m against 0.192 m from beam theory. The coarse mesh is", "Ingat semula · mesh Q4 2 × 2 memberi tip deflection 0.131 m berbanding 0.192 m daripada beam theory. Mesh kasar itu",
       [("a", "too flexible", "terlalu fleksibel"), ("b", "too stiff, by about a third", "terlalu kaku, kira-kira satu pertiga"), ("c", "exact at the nodes", "tepat pada node")],
       "b", "0.131/0.192 = 0.68: the bilinear elements cannot bend without a spurious shear strain, which resists the bending (shear locking). Refining, or using 8-node elements, removes most of it. Today: what that means for the stresses.",
       "0.131/0.192 = 0.68: element bilinear tidak dapat melentur tanpa shear strain palsu, yang menentang bending (shear locking). Refine, atau menggunakan 8-node element, menghapuskan sebahagian besarnya. Hari ini: apa maksudnya untuk stress."),
]

QUICK = [
    MCQ("a1", "Order the operations that take the solved nodal displacements to a stress at a point.", "Susun operasi yang membawa nodal displacement yang diselesaikan kepada stress pada satu titik.",
        [("a", "[E]{û}, then [B], then locate the element", "[E]{û}, kemudian [B], kemudian cari element"),
         ("b", "locate the element and the local coordinates → {ε} = [B]{û} → {σ} = [E]{ε}", "cari element dan koordinat local → {ε} = [B]{û} → {σ} = [E]{ε}"),
         ("c", "average the nodal displacements → multiply by [k] → divide by the area", "purata nodal displacement → darab dengan [k] → bahagi dengan luas")], "b",
        "Locate first, because [B] must be evaluated at the local coordinates of the point in the element that contains it; then strains, then stresses. [k]{û} gives nodal forces, not stresses.",
        "Cari dahulu, kerana [B] mesti dinilai pada koordinat local titik itu dalam element yang mengandunginya; kemudian strain, kemudian stress. [k]{û} memberi nodal force, bukan stress."),
    MCQ("a2", "In a displacement-based model, why are the stresses less accurate than the displacements?", "Dalam model berasaskan displacement, mengapa stress kurang tepat berbanding displacement?",
        [("a", "[E] is only approximate", "[E] hanya anggaran"), ("b", "they are derivatives of the interpolated displacements: one order lower, and discontinuous between elements", "ia derivative bagi displacement yang di-interpolate: satu peringkat lebih rendah, dan tidak continuous antara element"), ("c", "the loads are lumped at the nodes", "load dikumpulkan pada node")], "b",
        "The method solves for nodal displacements; strains come from differentiating the shape functions, which loses one order of accuracy, and each element differentiates its own field, so the stresses jump at shared sides. [E] is exact for the idealisation; consistent loads are not lumped.",
        "Kaedah ini menyelesaikan nodal displacement; strain datang daripada membezakan shape function, yang kehilangan satu peringkat ketepatan, dan setiap element membezakan field sendiri, jadi stress melompat pada sisi yang dikongsi. [E] tepat bagi idealisation itu; consistent load tidak dikumpulkan."),
    MCQ("a3", "Which display option shows the jumps of stress between neighbouring elements?", "Pilihan paparan mana yang menunjukkan lompatan stress antara element yang berjiran?",
        [("a", "Elemental mean", "Elemental mean"), ("b", "Unaveraged", "Unaveraged"), ("c", "Averaged", "Averaged")], "b",
        "Unaveraged shows each element’s own values at its nodes, so two values meet at every shared node and the jump is visible. Elemental mean shows one value per element; Averaged smooths the jumps away without removing the error.",
        "Unaveraged menunjukkan nilai setiap element sendiri pada node-nya, jadi dua nilai bertemu pada setiap node yang dikongsi dan lompatannya kelihatan. Elemental mean menunjukkan satu nilai setiap element; Averaged melicinkan lompatan tanpa menghapuskan ralat."),
    MCQ("a4", "σ<sub>xx</sub> next to the fully fixed corner rises 4134 → 5372 → 6400 → 7467 kN m<sup>−2</sup> as the elements are halved. What do you report?", "σ<sub>xx</sub> bersebelahan bucu yang tetap sepenuhnya meningkat 4134 → 5372 → 6400 → 7467 kN m<sup>−2</sup> apabila element dibahagi dua. Apa yang anda laporkan?",
        [("a", "7467 kN m<sup>−2</sup>, the finest mesh", "7467 kN m<sup>−2</sup>, mesh paling halus"), ("b", "an extrapolated limit from the three finest meshes", "had yang diekstrapolasi daripada tiga mesh paling halus"), ("c", "none of them: it is a singularity; report stresses away from the corner", "tiada satu pun: ia singularity; laporkan stress jauh dari bucu")], "c",
        "The steps do not shrink (1238, 1028, 1067), so there is no limit to extrapolate to: the elastic stress at a fully fixed re-entrant corner is infinite. Report values outside the corner zone or model the support realistically.",
        "Langkahnya tidak mengecil (1238, 1028, 1067), jadi tiada had untuk diekstrapolasi: stress elastic pada re-entrant corner yang tetap sepenuhnya ialah infiniti. Laporkan nilai di luar zon bucu atau modelkan support secara realistik."),
    MCQ("a5", "Two meshes of 8-node elements, 2 × 1 and 4 × 2, give tip deflections of 0.1780 and 0.1885 m (converged 0.1915). Four 4-node elements give 0.1306 m. The main reason the Q8 does better per element is that", "Dua mesh 8-node element, 2 × 1 dan 4 × 2, memberi tip deflection 0.1780 dan 0.1885 m (converge 0.1915). Empat 4-node element memberi 0.1306 m. Sebab utama Q8 lebih baik bagi setiap element ialah",
        [("a", "it has more Gauss points", "ia mempunyai lebih banyak Gauss point"), ("b", "its sides can curve, so bending does not create a spurious shear strain", "sisinya boleh melengkung, jadi bending tidak menghasilkan shear strain palsu"), ("c", "its loads are lumped more evenly", "load-nya dikumpulkan dengan lebih sekata")], "b",
        "A Q4 keeps its sides straight and can rotate a section only by shearing; the parasitic shear stores energy and resists bending (Example 3). The quadratic sides of a Q8 take the curved shape of a bent beam. More Gauss points are a consequence of the higher order, not the cause.",
        "Q4 mengekalkan sisinya lurus dan hanya boleh memutar keratan dengan shear; parasitic shear menyimpan tenaga dan menentang bending (Contoh 3). Sisi quadratic Q8 mengambil bentuk melengkung beam yang melentur. Lebih banyak Gauss point ialah akibat order yang lebih tinggi, bukan sebabnya."),
    MCQ("a6", "A results section reads: “Four meshes were run and the results agree well with theory.” What is missing?", "Satu bahagian keputusan berbunyi: “Four meshes were run and the results agree well with theory.” Apa yang tiada?",
        [("a", "nothing: four meshes is enough", "tiada: empat mesh sudah mencukupi"), ("b", "the numbers: the quantity for each mesh, the change between the last two, and the difference from the check with its sign", "nombor: kuantiti bagi setiap mesh, perubahan antara dua yang terakhir, dan perbezaan daripada semakan bersama tandanya"), ("c", "a colour contour plot", "contour plot berwarna")], "b",
        "The standard is a convergence table plus a signed, quantified comparison with an independent check. “Agree well” is an opinion; a contour plot without numbers does not verify anything.",
        "Piawainya ialah convergence table serta perbandingan yang dikuantifikasi dan bertanda dengan semakan bebas. “Agree well” ialah pendapat; contour plot tanpa nombor tidak mengesahkan apa-apa."),
]

ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="4" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("A student recovers the stresses at (3.5, 1.3) m of the 2 × 2 cantilever (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, Ē = 224.44 × 10⁶ N m<sup>−2</sup>). One line contains the slip. Which one?",
        "Seorang pelajar mendapatkan semula stress pada (3.5, 1.3) m bagi cantilever 2 × 2 (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, Ē = 224.44 × 10⁶ N m<sup>−2</sup>). Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>The point lies in element 4 (nodes 5, 6, 9, 8), whose node 1 is at (2, 1): local (1.5, 0.3).</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>{ε} = [B]{û<sup>4</sup>} = {0.0016501, −0.0007445, −0.0041348}.</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>σ<sub>xx</sub> = 224.44(1.6501) − 74.07(0.7445) = 315.2 kN m<sup>−2</sup>; σ<sub>yy</sub> = 74.07(1.6501) − 224.44(0.7445) = −44.9 kN m<sup>−2</sup>.</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>σ<sub>xy</sub> = Ē ε<sub>xy</sub> = 224.44(−4.1348) = −928.0 kN m<sup>−2</sup>.</span></button>'
    + '<button type="button" data-k="5"><span class="ln">5</span><span>σ<sub>vM</sub> = √(315.2² + 315.2 × 44.9 + 44.9² + 3 × 928.0²) = 1643 kN m<sup>−2</sup>.</span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 4: the shear row of [E] for plane stress is Ē(1 − ν)/2 = 75.19 × 10⁶ N m<sup>−2</sup>, which equals G = E/(2(1 + ν)). So σ<sub>xy</sub> = 75.19(−4.1348) = −310.9 kN m<sup>−2</sup>, and line 5 becomes σ<sub>vM</sub> = 636.8 kN m<sup>−2</sup>. The check that catches it: the shear entry must equal G, and a shear stress three times σ<sub>xx</sub> near a free end is implausible.",
        "Baris 4: baris shear [E] bagi plane stress ialah Ē(1 − ν)/2 = 75.19 × 10⁶ N m<sup>−2</sup>, yang sama dengan G = E/(2(1 + ν)). Jadi σ<sub>xy</sub> = 75.19(−4.1348) = −310.9 kN m<sup>−2</sup>, dan baris 5 menjadi σ<sub>vM</sub> = 636.8 kN m<sup>−2</sup>. Semakan yang menangkapnya: entri shear mesti sama dengan G, dan shear stress tiga kali σ<sub>xx</sub> berhampiran hujung bebas tidak munasabah.")
    + '</p></div>'
)

# parameterised calculation exercises
EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  function strains(P){ var a=P.a, b=P.b, x=P.x, y=P.y, u=P.u, v=P.v, ab=a*b;
    return [((b-y)*(u[1]-u[0]) + y*(u[2]-u[3]))/ab, ((a-x)*(v[3]-v[0]) + x*(v[2]-v[1]))/ab,
            ((a-x)*(u[3]-u[0]) + x*(u[2]-u[1]))/ab + ((b-y)*(v[1]-v[0]) + y*(v[2]-v[3]))/ab]; }
  function stresses(P){ var e=strains(P), Eb=P.E/(1-P.nu*P.nu);   /* kN/m2, strains in 1 */
    return [Eb*(e[0]+P.nu*e[1]), Eb*(P.nu*e[0]+e[1]), Eb*(1-P.nu)/2*e[2]]; }
  /* b1: stresses at a point from the nodal displacements of one element */
  EX.define("b1", {
    gen: function(r){ for (var k=0;k<50;k++){ var a=pick(r,[0.4,0.5,0.6,0.8,1]), b=pick(r,[0.2,0.3,0.4,0.5]);
        var P={a:a,b:b,E:200e6,nu:pick(r,[0.25,0.3]),x:Math.round(a*(1+Math.floor(r()*9))/10*100)/100,y:Math.round(b*(1+Math.floor(r()*9))/10*100)/100,
               u:[0,0,0,0].map(function(){return Math.floor(r()*7)-3;}), v:[0,0,0,0].map(function(){return Math.floor(r()*5)-2;})};
        P.u=P.u.map(function(q){return q*1e-5;}); P.v=P.v.map(function(q){return q*1e-5;});
        var s=stresses(P); if (Math.min(Math.abs(s[0]),Math.abs(s[1]),Math.abs(s[2]))>=100) return P; }
      return P; },
    text: function(P){ var d=[]; for (var i=0;i<4;i++){ d.push(fmt(P.u[i]*1e5,0)); d.push(fmt(P.v[i]*1e5,0)); }
      return bi("A four-node element, a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, E = 200 × 10⁶ kN m<sup>−2</sup>, ν = <span class=\"num\">"+P.nu+"</span>, plane stress, has the nodal displacements {u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>} = {"+d.join(", ")+"} × 10<sup>−5</sup> m. Find the stresses at the local point (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m, in kN m<sup>−2</sup>, to the nearest whole number.",
                "Satu four-node element, a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, E = 200 × 10⁶ kN m<sup>−2</sup>, ν = <span class=\"num\">"+P.nu+"</span>, plane stress, mempunyai nodal displacement {u<sub>1</sub>, v<sub>1</sub>, …, u<sub>4</sub>, v<sub>4</sub>} = {"+d.join(", ")+"} × 10<sup>−5</sup> m. Cari stress pada titik local (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m, dalam kN m<sup>−2</sup>, kepada nombor bulat terdekat."); },
    fields: [{id:"sxx", label:["σ<sub>xx</sub>","σ<sub>xx</sub>"], unit:"kN m⁻²", fn:function(P){ return stresses(P)[0]; }, atol:3, rtol:0.006},
             {id:"syy", label:["σ<sub>yy</sub>","σ<sub>yy</sub>"], unit:"kN m⁻²", fn:function(P){ return stresses(P)[1]; }, atol:3, rtol:0.006},
             {id:"sxy", label:["σ<sub>xy</sub>","σ<sub>xy</sub>"], unit:"kN m⁻²", fn:function(P){ return stresses(P)[2]; }, atol:3, rtol:0.006}],
    hints: [function(P){ return bi("Strains from the rows of [B]: ε<sub>xx</sub> = [(b − y)(u<sub>2</sub> − u<sub>1</sub>) + y(u<sub>3</sub> − u<sub>4</sub>)]/ab; ε<sub>yy</sub> = [(a − x)(v<sub>4</sub> − v<sub>1</sub>) + x(v<sub>3</sub> − v<sub>2</sub>)]/ab; ε<sub>xy</sub> = [(a − x)(u<sub>4</sub> − u<sub>1</sub>) + x(u<sub>3</sub> − u<sub>2</sub>) + (b − y)(v<sub>2</sub> − v<sub>1</sub>) + y(v<sub>3</sub> − v<sub>4</sub>)]/ab.",
                                      "Strain daripada baris [B]: ε<sub>xx</sub> = [(b − y)(u<sub>2</sub> − u<sub>1</sub>) + y(u<sub>3</sub> − u<sub>4</sub>)]/ab; ε<sub>yy</sub> = [(a − x)(v<sub>4</sub> − v<sub>1</sub>) + x(v<sub>3</sub> − v<sub>2</sub>)]/ab; ε<sub>xy</sub> = [(a − x)(u<sub>4</sub> − u<sub>1</sub>) + x(u<sub>3</sub> − u<sub>2</sub>) + (b − y)(v<sub>2</sub> − v<sub>1</sub>) + y(v<sub>3</sub> − v<sub>4</sub>)]/ab."); },
            function(P){ var e=strains(P); return bi("ab = "+fmt(P.a*P.b,3)+", b − y = "+fmt(P.b-P.y,2)+", a − x = "+fmt(P.a-P.x,2)+". Strains: ε = {"+e.map(function(q){return fmt(q*1e6,2);}).join(", ")+"} × 10<sup>−6</sup>.",
                                      "ab = "+fmt(P.a*P.b,3)+", b − y = "+fmt(P.b-P.y,2)+", a − x = "+fmt(P.a-P.x,2)+". Strain: ε = {"+e.map(function(q){return fmt(q*1e6,2);}).join(", ")+"} × 10<sup>−6</sup>."); },
            function(P){ var Eb=P.E/(1-P.nu*P.nu); return bi("[E]: Ē = E/(1 − ν²) = "+fmt(Eb/1e6,3)+" × 10⁶; νĒ = "+fmt(P.nu*Eb/1e6,3)+" × 10⁶; Ē(1 − ν)/2 = "+fmt(Eb*(1-P.nu)/2/1e6,3)+" × 10⁶ kN m<sup>−2</sup>. σ<sub>xx</sub> = Ē(ε<sub>xx</sub> + νε<sub>yy</sub>), σ<sub>yy</sub> = Ē(νε<sub>xx</sub> + ε<sub>yy</sub>), σ<sub>xy</sub> = Ē(1 − ν)ε<sub>xy</sub>/2.",
                                      "[E]: Ē = E/(1 − ν²) = "+fmt(Eb/1e6,3)+" × 10⁶; νĒ = "+fmt(P.nu*Eb/1e6,3)+" × 10⁶; Ē(1 − ν)/2 = "+fmt(Eb*(1-P.nu)/2/1e6,3)+" × 10⁶ kN m<sup>−2</sup>. σ<sub>xx</sub> = Ē(ε<sub>xx</sub> + νε<sub>yy</sub>), σ<sub>yy</sub> = Ē(νε<sub>xx</sub> + ε<sub>yy</sub>), σ<sub>xy</sub> = Ē(1 − ν)ε<sub>xy</sub>/2."); }],
    solution: function(P){ var e=strains(P), s=stresses(P), Eb=P.E/(1-P.nu*P.nu), a=P.a, b=P.b, x=P.x, y=P.y, u=P.u.map(function(q){return q*1e5;}), v=P.v.map(function(q){return q*1e5;});
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">"+bi("Displacements below in 10<sup>−5</sup> m; ab = ","Displacement di bawah dalam 10<sup>−5</sup> m; ab = ")+fmt(a*b,3)+"<br>"
        +"ε<sub>xx</sub> = ["+fmt(b-y,2)+"("+fmt(u[1]-u[0],0)+") + "+fmt(y,2)+"("+fmt(u[2]-u[3],0)+")] × 10<sup>−5</sup>/"+fmt(a*b,3)+" = "+fmt(e[0]*1e6,2)+" × 10<sup>−6</sup><br>"
        +"ε<sub>yy</sub> = ["+fmt(a-x,2)+"("+fmt(v[3]-v[0],0)+") + "+fmt(x,2)+"("+fmt(v[2]-v[1],0)+")] × 10<sup>−5</sup>/"+fmt(a*b,3)+" = "+fmt(e[1]*1e6,2)+" × 10<sup>−6</sup><br>"
        +"ε<sub>xy</sub> = ["+fmt(a-x,2)+"("+fmt(u[3]-u[0],0)+") + "+fmt(x,2)+"("+fmt(u[2]-u[1],0)+") + "+fmt(b-y,2)+"("+fmt(v[1]-v[0],0)+") + "+fmt(y,2)+"("+fmt(v[2]-v[3],0)+")] × 10<sup>−5</sup>/"+fmt(a*b,3)+" = "+fmt(e[2]*1e6,2)+" × 10<sup>−6</sup><br>"
        +"Ē = "+fmt(Eb/1e6,3)+" × 10⁶ kN m<sup>−2</sup><br>σ<sub>xx</sub> = "+fmt(Eb/1e6,3)+"("+fmt(e[0]*1e6,2)+" + "+P.nu+" × "+fmt(e[1]*1e6,2)+") = "+fmt(s[0],0)+" kN m<sup>−2</sup><br>"
        +"σ<sub>yy</sub> = "+fmt(Eb/1e6,3)+"("+P.nu+" × "+fmt(e[0]*1e6,2)+" + "+fmt(e[1]*1e6,2)+") = "+fmt(s[1],0)+" kN m<sup>−2</sup><br>"
        +"σ<sub>xy</sub> = "+fmt(Eb*(1-P.nu)/2/1e6,3)+" × "+fmt(e[2]*1e6,2)+" = "+fmt(s[2],0)+" kN m<sup>−2</sup></p>"; }
  });
  /* b2: principal stresses, direction and von Mises from a given state */
  function principal(P){ var c=(P.sx+P.sy)/2, R=Math.sqrt(Math.pow((P.sx-P.sy)/2,2)+P.sxy*P.sxy), th=0.5*Math.atan2(2*P.sxy,P.sx-P.sy)*180/Math.PI;
    return {s1:c+R, s2:c-R, th:th, vm:Math.sqrt(P.sx*P.sx-P.sx*P.sy+P.sy*P.sy+3*P.sxy*P.sxy), c:c, R:R}; }
  EX.define("b2", {
    gen: function(r){ var P; for (var k=0;k<50;k++){ P={sx:10*(Math.floor(r()*61)-30), sy:10*(Math.floor(r()*41)-20), sxy:10*(Math.floor(r()*41)-20)}; if (Math.abs(P.sxy)>=20 && Math.abs(P.sx-P.sy)>=20) break; } return P; },
    text: function(P){ return bi("At a point of a plate in plane stress, σ<sub>xx</sub> = <span class=\"num\">"+fmt(P.sx,0)+"</span>, σ<sub>yy</sub> = <span class=\"num\">"+fmt(P.sy,0)+"</span>, σ<sub>xy</sub> = <span class=\"num\">"+fmt(P.sxy,0)+"</span> kN m<sup>−2</sup>. Find σ<sub>1</sub>, σ<sub>2</sub>, the angle θ<sub>p</sub> from the x-axis to the direction of σ<sub>1</sub> (degrees, between −90° and 90°) and the von Mises stress; stresses to 1 decimal, the angle to 1 decimal.",
                                   "Pada satu titik plat dalam plane stress, σ<sub>xx</sub> = <span class=\"num\">"+fmt(P.sx,0)+"</span>, σ<sub>yy</sub> = <span class=\"num\">"+fmt(P.sy,0)+"</span>, σ<sub>xy</sub> = <span class=\"num\">"+fmt(P.sxy,0)+"</span> kN m<sup>−2</sup>. Cari σ<sub>1</sub>, σ<sub>2</sub>, sudut θ<sub>p</sub> dari paksi x ke arah σ<sub>1</sub> (darjah, antara −90° dan 90°) dan von Mises stress; stress kepada 1 tempat perpuluhan, sudut kepada 1 tempat perpuluhan."); },
    fields: [{id:"s1", label:["σ<sub>1</sub>","σ<sub>1</sub>"], unit:"kN m⁻²", fn:function(P){ return principal(P).s1; }, atol:0.15, rtol:0.002},
             {id:"s2", label:["σ<sub>2</sub>","σ<sub>2</sub>"], unit:"kN m⁻²", fn:function(P){ return principal(P).s2; }, atol:0.15, rtol:0.002},
             {id:"th", label:["θ<sub>p</sub>","θ<sub>p</sub>"], unit:"°", fn:function(P){ return principal(P).th; }, atol:0.15, rtol:0},
             {id:"vm", label:["σ<sub>vM</sub>","σ<sub>vM</sub>"], unit:"kN m⁻²", fn:function(P){ return principal(P).vm; }, atol:0.15, rtol:0.002}],
    hints: [function(P){ return bi("Mohr’s circle: centre c = (σ<sub>xx</sub> + σ<sub>yy</sub>)/2, radius R = √[((σ<sub>xx</sub> − σ<sub>yy</sub>)/2)² + σ<sub>xy</sub>²]; σ<sub>1,2</sub> = c ± R. Von Mises: √(σ<sub>xx</sub>² − σ<sub>xx</sub>σ<sub>yy</sub> + σ<sub>yy</sub>² + 3σ<sub>xy</sub>²).",
                                      "Mohr’s circle: pusat c = (σ<sub>xx</sub> + σ<sub>yy</sub>)/2, jejari R = √[((σ<sub>xx</sub> − σ<sub>yy</sub>)/2)² + σ<sub>xy</sub>²]; σ<sub>1,2</sub> = c ± R. Von Mises: √(σ<sub>xx</sub>² − σ<sub>xx</sub>σ<sub>yy</sub> + σ<sub>yy</sub>² + 3σ<sub>xy</sub>²)."); },
            function(P){ var q=principal(P); return bi("c = "+fmt(q.c,1)+", R = "+fmt(q.R,1)+". For the angle use tan 2θ<sub>p</sub> = 2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>); if σ<sub>xx</sub> − σ<sub>yy</sub> < 0, add 180° to 2θ<sub>p</sub> (or subtract it, to stay within ±90° for θ<sub>p</sub>) so that θ<sub>p</sub> points to σ<sub>1</sub>.",
                                      "c = "+fmt(q.c,1)+", R = "+fmt(q.R,1)+". Untuk sudut guna tan 2θ<sub>p</sub> = 2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>); jika σ<sub>xx</sub> − σ<sub>yy</sub> < 0, tambah 180° kepada 2θ<sub>p</sub> (atau tolak, supaya θ<sub>p</sub> kekal dalam ±90°) supaya θ<sub>p</sub> menghala ke σ<sub>1</sub>."); },
            function(P){ return bi("Checks: σ<sub>1</sub> + σ<sub>2</sub> = σ<sub>xx</sub> + σ<sub>yy</sub> = "+fmt(P.sx+P.sy,0)+"; σ<sub>vM</sub> = √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²) gives the same number.",
                                      "Semakan: σ<sub>1</sub> + σ<sub>2</sub> = σ<sub>xx</sub> + σ<sub>yy</sub> = "+fmt(P.sx+P.sy,0)+"; σ<sub>vM</sub> = √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²) memberi nombor yang sama."); }],
    solution: function(P){ var q=principal(P);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">c = ("+fmt(P.sx,0)+" + "+fmt(P.sy,0)+")/2 = "+fmt(q.c,1)+"<br>R = √[("+fmt((P.sx-P.sy)/2,1)+")² + ("+fmt(P.sxy,0)+")²] = "+fmt(q.R,1)+"<br>σ<sub>1</sub> = "+fmt(q.s1,1)+", σ<sub>2</sub> = "+fmt(q.s2,1)+" kN m<sup>−2</sup><br>2θ<sub>p</sub> = atan2("+fmt(2*P.sxy,0)+", "+fmt(P.sx-P.sy,0)+") = "+fmt(2*q.th,1)+"°, θ<sub>p</sub> = "+fmt(q.th,1)+"°<br>σ<sub>vM</sub> = √("+fmt(P.sx,0)+"² − ("+fmt(P.sx,0)+")("+fmt(P.sy,0)+") + "+fmt(P.sy,0)+"² + 3 × "+fmt(P.sxy,0)+"²) = "+fmt(q.vm,1)+" kN m<sup>−2</sup></p>"; }
  });
  /* b3: rate, extrapolation and error from three meshes, Richardson as in FEM by Hand (10.1) */
  function rich(P){ var d1=P.q[1]-P.q[0], d2=P.q[2]-P.q[1], r=d1/d2, Q=P.q[2]+d2/(r-1); return {r:r, p:Math.log(r)/Math.log(2), Q:Q, err:(P.q[2]-Q)/Q*100}; }
  EX.define("b3", {
    gen: function(r){ var Qi=pick(r,[12.5,18,24,35,48,60]), p=pick(r,[1.5,2]), C=pick(r,[0.12,0.18,0.25,0.3]);
      var q=[1,0.5,0.25].map(function(h){ return Math.round(Qi*(1-C*Math.pow(h,p))*1000)/1000; }); return {q:q, what:pick(r,[["tip deflection","tip deflection"],["deflection at mid-span","deflection di tengah rentang"]])}; },
    text: function(P){ return bi("Three meshes, each with half the element size of the previous one, give the "+P.what[0]+" "+P.q.map(function(v){return "<span class=\"num\">"+v.toFixed(3)+"</span>";}).join(", ")+" mm. Find the ratio of successive changes (= 2<sup>p</sup>), the rate p, the extrapolated value and the error of the finest mesh against it (%, with sign). Ratio and p to 2 decimals, the value to 3 decimals, the error to 2 decimals.",
                                   "Tiga mesh, setiap satu dengan saiz element separuh daripada sebelumnya, memberi "+P.what[1]+" "+P.q.map(function(v){return "<span class=\"num\">"+v.toFixed(3)+"</span>";}).join(", ")+" mm. Cari nisbah perubahan berturut-turut (= 2<sup>p</sup>), kadar p, nilai yang diekstrapolasi dan ralat mesh paling halus berbanding nilai itu (%, dengan tanda). Nisbah dan p kepada 2 tempat perpuluhan, nilai kepada 3 tempat perpuluhan, ralat kepada 2 tempat perpuluhan."); },
    fields: [{id:"r", label:["2<sup>p</sup>","2<sup>p</sup>"], fn:function(P){ return rich(P).r; }, atol:0.02, rtol:0.004},
             {id:"p", label:["p","p"], fn:function(P){ return rich(P).p; }, atol:0.02, rtol:0},
             {id:"q", label:[bi("extrapolated","diekstrapolasi"),bi("extrapolated","diekstrapolasi")], unit:"mm", fn:function(P){ return rich(P).Q; }, atol:0.003, rtol:0.0002},
             {id:"e", label:[bi("error of finest","ralat paling halus"),bi("error of finest","ralat paling halus")], unit:"%", fn:function(P){ return rich(P).err; }, atol:0.02, rtol:0.01}],
    hints: [function(P){ return bi("FEM by Hand (10.1): 2<sup>p</sup> ≈ (Q<sub>h</sub> − Q<sub>h/2</sub>)/(Q<sub>h/2</sub> − Q<sub>h/4</sub>); Q ≈ Q<sub>h/4</sub> + (Q<sub>h/4</sub> − Q<sub>h/2</sub>)/(2<sup>p</sup> − 1).",
                                      "FEM by Hand (10.1): 2<sup>p</sup> ≈ (Q<sub>h</sub> − Q<sub>h/2</sub>)/(Q<sub>h/2</sub> − Q<sub>h/4</sub>); Q ≈ Q<sub>h/4</sub> + (Q<sub>h/4</sub> − Q<sub>h/2</sub>)/(2<sup>p</sup> − 1)."); },
            function(P){ return bi("Changes: Δ<sub>1</sub> = "+fmt(P.q[1]-P.q[0],3)+", Δ<sub>2</sub> = "+fmt(P.q[2]-P.q[1],3)+" mm. p = ln(2<sup>p</sup>)/ln 2. The error of the finest mesh is (Q<sub>h/4</sub> − Q)/Q, negative when it is below the limit.",
                                      "Perubahan: Δ<sub>1</sub> = "+fmt(P.q[1]-P.q[0],3)+", Δ<sub>2</sub> = "+fmt(P.q[2]-P.q[1],3)+" mm. p = ln(2<sup>p</sup>)/ln 2. Ralat mesh paling halus ialah (Q<sub>h/4</sub> − Q)/Q, negatif apabila ia di bawah had."); }],
    solution: function(P){ var s=rich(P);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">Δ<sub>1</sub> = "+P.q[1].toFixed(3)+" − "+P.q[0].toFixed(3)+" = "+fmt(P.q[1]-P.q[0],3)+"; Δ<sub>2</sub> = "+P.q[2].toFixed(3)+" − "+P.q[1].toFixed(3)+" = "+fmt(P.q[2]-P.q[1],3)+"<br>2<sup>p</sup> ≈ "+fmt(P.q[1]-P.q[0],3)+"/"+fmt(P.q[2]-P.q[1],3)+" = "+fmt(s.r,2)+"; p = ln "+fmt(s.r,3)+"/ln 2 = "+fmt(s.p,2)+"<br>Q ≈ "+P.q[2].toFixed(3)+" + "+fmt(P.q[2]-P.q[1],3)+"/("+fmt(s.r,3)+" − 1) = "+fmt(s.Q,3)+" mm<br>"+bi("error of the finest mesh","ralat mesh paling halus")+" = ("+P.q[2].toFixed(3)+" − "+fmt(s.Q,3)+")/"+fmt(s.Q,3)+" = "+fmt(s.err,2)+"%</p>"; }
  });
  /* b4: a uniform edge load on an 8-node side, and on two 4-node sides */
  EX.define("b4", {
    gen: function(r){ return {q:pick(r,[5,8,10,12,15,20,25,30,40]), L:pick(r,[0.5,0.8,1,1.2,1.5,2,2.5,3])}; },
    text: function(P){ return bi("A uniform load of <span class=\"num\">"+P.q+"</span> kN m<sup>−1</sup> (force per unit length of the edge, thickness included) acts along a side of length ℓ = <span class=\"num\">"+P.L+"</span> m. Find the nodal loads (magnitudes, kN, 3 decimals) at a corner and at the mid-side node when the side belongs to one 8-node element, and at the middle node when the same side is made of two 4-node sides.",
                                   "Load seragam <span class=\"num\">"+P.q+"</span> kN m<sup>−1</sup> (daya per unit panjang tepi, termasuk ketebalan) bertindak di sepanjang sisi sepanjang ℓ = <span class=\"num\">"+P.L+"</span> m. Cari nodal load (magnitud, kN, 3 tempat perpuluhan) pada bucu dan pada node tengah sisi apabila sisi itu milik satu 8-node element, dan pada node tengah apabila sisi yang sama terdiri daripada dua sisi 4-node."); },
    fields: [{id:"fc", label:[bi("Q8 corner","Q8 bucu"),bi("Q8 corner","Q8 bucu")], unit:"kN", fn:function(P){ return P.q*P.L/6; }, atol:0.002, rtol:0.002},
             {id:"fm", label:[bi("Q8 mid-side","Q8 tengah sisi"),bi("Q8 mid-side","Q8 tengah sisi")], unit:"kN", fn:function(P){ return 2*P.q*P.L/3; }, atol:0.002, rtol:0.002},
             {id:"f4", label:[bi("Q4 middle node","Q4 node tengah"),bi("Q4 middle node","Q4 node tengah")], unit:"kN", fn:function(P){ return P.q*P.L/2; }, atol:0.002, rtol:0.002}],
    hints: [function(P){ return bi("Text (3.51): along an 8-node side the shape functions integrate to ℓ/6, 2ℓ/3, ℓ/6. A 4-node side of length ℓ/2 gives (q × ℓ/2)/2 to each of its two nodes, and the middle node belongs to both sides.",
                                      "Teks (3.51): di sepanjang sisi 8-node, shape function ber-integral kepada ℓ/6, 2ℓ/3, ℓ/6. Sisi 4-node sepanjang ℓ/2 memberi (q × ℓ/2)/2 kepada setiap satu daripada dua node-nya, dan node tengah dimiliki kedua-dua sisi."); },
            function(P){ return bi("Total qℓ = "+fmt(P.q*P.L,3)+" kN in both cases: check that your shares add up to it.", "Jumlah qℓ = "+fmt(P.q*P.L,3)+" kN dalam kedua-dua kes: semak bahawa bahagian anda berjumlah sebanyak itu."); }],
    solution: function(P){ var T=P.q*P.L;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">qℓ = "+P.q+" × "+P.L+" = "+fmt(T,3)+" kN<br>Q8: "+bi("corners","bucu")+" qℓ/6 = "+fmt(T/6,3)+" kN; "+bi("mid-side","tengah sisi")+" 2qℓ/3 = "+fmt(2*T/3,3)+" kN ("+fmt(T/6,3)+" + "+fmt(2*T/3,3)+" + "+fmt(T/6,3)+" = "+fmt(T,3)+")<br>"+bi("Two Q4 sides: ends ","Dua sisi Q4: hujung ")+"qℓ/4 = "+fmt(T/4,3)+" kN; "+bi("middle node","node tengah")+" 2 × qℓ/4 = "+fmt(T/2,3)+" kN</p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("Stresses at a point from the nodal displacements", "Stress pada satu titik daripada nodal displacement"), 6),
    ("b2", ("Principal stresses, their direction and von Mises", "Principal stress, arahnya dan von Mises"), 4),
    ("b3", ("Rate, converged value and error from three meshes", "Kadar, nilai converge dan ralat daripada tiga mesh"), 4),
    ("b4", ("Edge loads on an 8-node side and on two 4-node sides", "Edge load pada sisi 8-node dan pada dua sisi 4-node"), 3),
]

LAB_TASKS = [
    ("p13", ("4-node, 2 × 2 mesh: press “lecture point (3.5, 1.3)” and read σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub>, σ<sub>1</sub>, σ<sub>2</sub> and von Mises. Compare with your Activity 1 hand calculation.",
             "4-node, mesh 2 × 2: tekan “lecture point (3.5, 1.3)” dan baca σ<sub>xx</sub>, σ<sub>yy</sub>, σ<sub>xy</sub>, σ<sub>1</sub>, σ<sub>2</sub> dan von Mises. Bandingkan dengan pengiraan tangan Aktiviti 1 anda."),
            ("detected when the 4-node 2 × 2 mesh shows the probe at (3.5, 1.3) after you have acted", "dikesan apabila mesh 4-node 2 × 2 memaparkan probe pada (3.5, 1.3) selepas anda bertindak")),
    ("refine", ("Keep the point and refine: 8-node 16 × 8, then 32 × 16. Does σ<sub>xx</sub> approach beam theory’s 225 kN m<sup>−2</sup>? Then probe mid-span, (2.0, 1.3).",
                "Kekalkan titik itu dan refine: 8-node 16 × 8, kemudian 32 × 16. Adakah σ<sub>xx</sub> menghampiri 225 kN m<sup>−2</sup> beam theory? Kemudian probe tengah rentang, (2.0, 1.3)."),
               ("detected when 8-node 16 × 8 and 32 × 16 have both been shown with the probe at (3.5, 1.3)", "dikesan apabila 8-node 16 × 8 dan 32 × 16 kedua-duanya dipaparkan dengan probe pada (3.5, 1.3)")),
    ("corner", ("Run the corner study. Does the peak σ<sub>xx</sub> next to the fixed corner converge?", "Jalankan corner study. Adakah puncak σ<sub>xx</sub> bersebelahan bucu tetap converge?"),
               ("detected when the corner study runs", "dikesan apabila corner study dijalankan")),
    ("disp3", ("On the 4-node 4 × 2 mesh compare Elemental mean, Unaveraged and Averaged. Where do neighbouring elements disagree most?", "Pada mesh 4-node 4 × 2, bandingkan Elemental mean, Unaveraged dan Averaged. Di mana element berjiran paling tidak sepakat?"),
              ("detected when the 4-node 4 × 2 mesh has been shown with all three display options", "dikesan apabila mesh 4-node 4 × 2 dipaparkan dengan ketiga-tiga pilihan paparan")),
]

GLOSSARY = [
    ("stress recovery · post-processing", "Computing strains and stresses from the solved nodal displacements, {σ} = [E][B]{û}.", "Mengira strain dan stress daripada nodal displacement yang diselesaikan, {σ} = [E][B]{û}."),
    ("strain–displacement matrix [B]", "[∂]ᵀ[N], 3 × 8 for a four-node element: its rows give ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub> from the eight nodal displacements.", "[∂]ᵀ[N], 3 × 8 bagi four-node element: barisnya memberi ε<sub>xx</sub>, ε<sub>yy</sub>, ε<sub>xy</sub> daripada lapan nodal displacement."),
    ("primary · derived result", "Displacements are solved for; strains and stresses are derived by differentiation and are less accurate.", "Displacement diselesaikan secara langsung; strain dan stress diterbitkan melalui pembezaan dan kurang tepat."),
    ("principal stresses σ<sub>1</sub>, σ<sub>2</sub>", "The normal stresses on the planes where the shear is zero; the largest and smallest normal stress at the point.", "Normal stress pada satah di mana shear sifar; normal stress terbesar dan terkecil pada titik itu."),
    ("principal direction θ<sub>p</sub>", "Angle from the x-axis to σ<sub>1</sub>: ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)], taken in the right quadrant.", "Sudut dari paksi x ke σ<sub>1</sub>: ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)], diambil dalam sukuan yang betul."),
    ("Mohr’s circle", "The stress state drawn as a circle: centre (σ<sub>xx</sub> + σ<sub>yy</sub>)/2, radius √[((σ<sub>xx</sub> − σ<sub>yy</sub>)/2)² + σ<sub>xy</sub>²].", "Keadaan stress dilukis sebagai bulatan: pusat (σ<sub>xx</sub> + σ<sub>yy</sub>)/2, jejari √[((σ<sub>xx</sub> − σ<sub>yy</sub>)/2)² + σ<sub>xy</sub>²]."),
    ("von Mises stress", "An equivalent uniaxial stress for yielding of ductile metals: √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²) in plane stress.", "Stress uniaxial setara untuk alah logam mulur: √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²) dalam plane stress."),
    ("Elemental mean", "Display option: one value per element, at its centroid.", "Pilihan paparan: satu nilai setiap element, pada centroid-nya."),
    ("Unaveraged", "Display option: each element’s own nodal values; the jumps between elements stay visible.", "Pilihan paparan: nilai node setiap element sendiri; lompatan antara element kekal kelihatan."),
    ("Averaged · nodal averaging", "Display option: the mean of all elements at a node; smooth, but no more accurate.", "Pilihan paparan: purata semua element pada satu node; licin, tetapi tidak lebih tepat."),
    ("stress jump", "The difference between neighbouring elements’ stresses at a shared side; a free indicator of the local mesh error.", "Perbezaan stress element berjiran pada sisi yang dikongsi; penunjuk percuma bagi ralat mesh setempat."),
    ("St-Venant’s principle", "How a load is applied matters only within about one depth of where it acts; beyond that only its resultant counts.", "Cara load dikenakan hanya penting dalam kira-kira satu kedalaman dari tempat ia bertindak; selepas itu hanya resultant-nya yang dikira."),
    ("singularity", "A point where the elastic stress is infinite (fully fixed re-entrant corner, point load): the computed peak grows with every refinement.", "Titik di mana stress elastic infiniti (re-entrant corner tetap sepenuhnya, point load): puncak yang dikira meningkat dengan setiap refine."),
    ("stress concentration · K<sub>t</sub>", "A finite local rise of stress at a smooth hole or fillet; K<sub>t</sub> = peak/nominal; it converges under refinement.", "Kenaikan stress setempat yang terhingga pada lubang licin atau fillet; K<sub>t</sub> = puncak/nominal; ia converge apabila di-refine."),
    ("8-node (serendipity) element · Q8", "Rectangle with corner and mid-side nodes, 16 dofs, quadratic along every side; PLANE183 in ANSYS.", "Segi empat tepat dengan node bucu dan tengah sisi, 16 dof, quadratic di sepanjang setiap sisi; PLANE183 dalam ANSYS."),
    ("consistent edge loads", "Nodal shares of an edge load from ∫N<sub>i</sub>q ds: ½, ½ on a 4-node side; ⅙, ⅔, ⅙ on an 8-node side.", "Bahagian nodal bagi edge load daripada ∫N<sub>i</sub>q ds: ½, ½ pada sisi 4-node; ⅙, ⅔, ⅙ pada sisi 8-node."),
    ("shear locking · parasitic shear", "A 4-node element bent by a moment shears because its sides stay straight; the spurious shear energy makes it too stiff.", "4-node element yang dilentur oleh momen mengalami shear kerana sisinya kekal lurus; tenaga shear palsu menjadikannya terlalu kaku."),
    ("rate of convergence p", "The error falls as h<sup>p</sup>; halving h divides it by 2<sup>p</sup>. About 2 for Q4 displacements of smooth problems, lower at a clamped corner.", "Ralat menurun sebagai h<sup>p</sup>; membahagi dua h membahagikannya dengan 2<sup>p</sup>. Kira-kira 2 bagi displacement Q4 masalah licin, lebih rendah pada bucu terkapit."),
    ("Richardson extrapolation", "An estimate of the converged value from two or three meshes: Q ≈ Q<sub>h/2</sub> + (Q<sub>h/2</sub> − Q<sub>h</sub>)/(2<sup>p</sup> − 1).", "Anggaran nilai converge daripada dua atau tiga mesh: Q ≈ Q<sub>h/2</sub> + (Q<sub>h/2</sub> − Q<sub>h</sub>)/(2<sup>p</sup> − 1)."),
    ("convergence table", "Three or more meshes, the quantity of interest on each, and the change between the last two in per cent.", "Tiga atau lebih mesh, kuantiti yang dikehendaki pada setiap satu, dan perubahan antara dua yang terakhir dalam peratus."),
    ("independent check", "A comparison with something not computed by the same model: beam theory, equilibrium of reactions, a textbook K<sub>t</sub>, a hand calculation.", "Perbandingan dengan sesuatu yang tidak dikira oleh model yang sama: beam theory, keseimbangan reaction, K<sub>t</sub> buku teks, pengiraan tangan."),
    ("idealisation", "The modelling decisions: 2D or not, plane stress or plane strain, thickness, material, supports, loads, what is left out.", "Keputusan pemodelan: 2D atau tidak, plane stress atau plane strain, ketebalan, bahan, support, load, apa yang ditinggalkan."),
    ("symmetry model", "Modelling a half or a quarter of a symmetric structure under a symmetric load, with rollers on the cut edges.", "Memodelkan separuh atau satu perempat struktur simetri di bawah load simetri, dengan roller pada tepi yang dipotong."),
]


def short_notes(A):
    return (
        "<h3>§1 " + B("Stress recovery", "Stress recovery") + "</h3>" + A.eq("wn_recover", None, 0.5) + A.eq("wn_rows", None, 0.45)
        + P("Use local x, y of the element that contains the point. Cantilever (3.5, 1.3): σ = {315.2, −44.9, −310.9} kN m<sup>−2</sup>. Keep 5–6 decimals in û.",
            "Guna x, y local bagi element yang mengandungi titik itu. Cantilever (3.5, 1.3): σ = {315.2, −44.9, −310.9} kN m<sup>−2</sup>. Kekalkan 5–6 tempat perpuluhan dalam û.")
        + "<h3>§2 " + B("Principal and von Mises", "Principal dan von Mises") + "</h3>"
        + P("σ<sub>1,2</sub> = c ± R; θ<sub>p</sub> = ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)]; σ<sub>vM</sub> = √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²). Cantilever: 494.4, −224.1, −30.0°, 636.8.",
            "σ<sub>1,2</sub> = c ± R; θ<sub>p</sub> = ½ tan<sup>−1</sup>[2σ<sub>xy</sub>/(σ<sub>xx</sub> − σ<sub>yy</sub>)]; σ<sub>vM</sub> = √(σ<sub>1</sub>² − σ<sub>1</sub>σ<sub>2</sub> + σ<sub>2</sub>²). Cantilever: 494.4, −224.1, −30.0°, 636.8.")
        + "<h3>§3 " + B("Accuracy", "Ketepatan") + "</h3>"
        + LI([("Read stresses at centroids, on converged meshes, away from supports and point loads.", "Baca stress pada centroid, pada mesh yang converge, jauh dari support dan point load."),
              ("Beam check M(y − H/2)/I only away from the ends: (3.5, 1.3) converged 153 vs beam 225.", "Semakan beam M(y − H/2)/I hanya jauh dari hujung: (3.5, 1.3) converge 153 berbanding beam 225.")])
        + "<h3>§4 " + B("Display options and singularities", "Pilihan paparan dan singularity") + "</h3>"
        + P("Elemental mean · Unaveraged (jumps) · Averaged (smooth). Fixed corner 4134 → 7467 kN m<sup>−2</sup>: singular, never report. Hole: K<sub>t</sub> 2.34, converges.",
            "Elemental mean · Unaveraged (lompatan) · Averaged (licin). Bucu tetap 4134 → 7467 kN m<sup>−2</sup>: singular, jangan laporkan. Lubang: K<sub>t</sub> 2.34, converge.")
        + "<h3>§5 Q8</h3>" + A.eq("wn_q8load", None, 0.45)
        + P("Q8 2 × 1: −7%; Q4 2 × 2: −32% (against 0.1915 m). Compare by dofs.", "Q8 2 × 1: −7%; Q4 2 × 2: −32% (berbanding 0.1915 m). Bandingkan mengikut dof.")
        + "<h3>§6 " + B("Report", "Laporan") + "</h3>" + A.eq("wn_rich", None, 0.45)
        + P("Idealisation · convergence table · one check · numbers in every sentence.", "Idealisation · convergence table · satu semakan · nombor dalam setiap ayat.")
    )


# ---- worked examples: answer-scheme style, from the course companion (FEM by Hand, Ch. 9 and 10) ----
EXAMPLES_INTRO = (
    '<div class="card" style="margin-bottom:18px"><h2 style="font-size:18px;margin:0 0 6px">' + B("How this topic is examined", "Bagaimana topik ini diuji") + '</h2>'
    + P("Model answers in the form the examiner expects: physical picture, plan, numbered steps with every substitution written out, checks, a boxed answer and an interpretation. "
        "The marks shown are a suggested scheme; the examiner’s own scheme may differ. Expect one hand calculation on a single element and one judgement question.",
        "Jawapan model dalam bentuk yang pemeriksa jangkakan: gambaran fizikal, pelan, langkah bernombor dengan setiap penggantian ditulis, semakan, jawapan berkotak dan tafsiran. "
        "Markah yang ditunjukkan ialah skema cadangan; skema pemeriksa sendiri mungkin berbeza. Jangkakan satu pengiraan tangan pada satu element dan satu soalan penilaian.", "lead")
    + '<div class="tbl"><table class="howex"><tr><th>' + B("Question type", "Jenis soalan") + '</th><th>' + B("Given and wanted", "Diberi dan dikehendaki") + '</th><th>' + B("Plan and the usual trap", "Pelan dan perangkap biasa") + '</th></tr>'
    + '<tr><td>' + B("Displacement and stress at a point", "Displacement dan stress pada satu titik") + '</td><td>' + B("Nodal displacements of an element; wanted: u, v, σ at (x<sub>1</sub>, y<sub>1</sub>).", "Nodal displacement satu element; dikehendaki: u, v, σ pada (x<sub>1</sub>, y<sub>1</sub>).") + '</td><td>' + B("N<sub>i</sub> and [B] at the point, then [E]. Trap: global coordinates in N<sub>i</sub>; the factor (1 − ν)/2.", "N<sub>i</sub> dan [B] pada titik itu, kemudian [E]. Perangkap: koordinat global dalam N<sub>i</sub>; faktor (1 − ν)/2.") + '</td></tr>'
    + '<tr><td>' + B("Stresses and reactions from a computer solution", "Stress dan reaction daripada penyelesaian komputer") + '</td><td>' + B("{U} of a small mesh; wanted: stresses at element centres, reactions, a comparison.", "{U} bagi mesh kecil; dikehendaki: stress pada pusat element, reaction, perbandingan.") + '</td><td>' + B("Centre formulas; struck rows of [K]{U} − {R}; beam theory. Trap: rounded displacements in a difference.", "Formula pusat; baris yang dibuang [K]{U} − {R}; beam theory. Perangkap: displacement yang dibundarkan dalam beza.") + '</td></tr>'
    + '<tr><td>' + B("Judge the accuracy", "Menilai ketepatan") + '</td><td>' + B("Results of two or three meshes, sometimes an exact value; wanted: the error and its cause.", "Keputusan dua atau tiga mesh, kadang-kadang nilai tepat; dikehendaki: ralat dan puncanya.") + '</td><td>' + B("Signed percentage; rate from three meshes; (10.1). Trap: “more elements are better” without saying what improves.", "Peratus bertanda; kadar daripada tiga mesh; (10.1). Perangkap: “lebih banyak element lebih baik” tanpa menyatakan apa yang bertambah baik.") + '</td></tr>'
    + '<tr><td>' + B("Explain", "Terangkan") + '</td><td>' + B("Why a Q4 is stiff in bending; why stresses jump; what a singularity is.", "Mengapa Q4 kaku dalam bending; mengapa stress melompat; apa itu singularity.") + '</td><td>' + B("Claim, reason (the mechanism), consequence for the mesh — in that order.", "Dakwaan, sebab (mekanisme), akibat kepada mesh — mengikut urutan itu.") + '</td></tr></table></div>'
    + P("Notation follows the companion: {d} the element displacements, Ē = E/(1 − ν²), G = Ē(1 − ν)/2; node i owns the global dofs U<sub>i</sub> (2i − 1) and V<sub>i</sub> (2i).",
        "Notasi mengikut buku pendamping: {d} displacement element, Ē = E/(1 − ν²), G = Ē(1 − ν)/2; node i memiliki dof global U<sub>i</sub> (2i − 1) dan V<sub>i</sub> (2i).", "lead")
    + '</div>')


def examples(A):
    X = []
    # ---- Example 1: the text's cantilever (FEM by Hand, Example 9.7) ----
    head = ('<div class="xhead"><h2>' + B("Example 1 · The text’s cantilever: stresses at the element centres, reactions and accuracy", "Contoh 1 · Cantilever dalam teks: stress pada pusat element, reaction dan ketepatan") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> given {U} from a computer: stresses, reactions, accuracy of Q4 in bending</span><span><b>' + B("Units", "Unit") + '</b> N, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 9.7 (text §3.4)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("The cantilever of the figure, 4 m long, 2 m deep and 0.01 m thick (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33), carries q<sub>y</sub> = 5 kN m<sup>−1</sup> downward on its free end. With four equal Q4 elements, "
             "(a) give the element constants and the loads, (b) take the computed displacements below, (c) find the stresses at the centres of elements 1 and 3 and compare them with beam theory, (d) check the reactions, and (e) judge the accuracy.",
             "Cantilever dalam rajah, panjang 4 m, dalam 2 m dan tebal 0.01 m (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33), membawa q<sub>y</sub> = 5 kN m<sup>−1</sup> ke bawah pada hujung bebasnya. Dengan empat Q4 element yang sama, "
             "(a) beri pemalar element dan load, (b) ambil displacement yang dikira di bawah, (c) cari stress pada pusat element 1 dan 3 dan bandingkan dengan beam theory, (d) semak reaction, dan (e) nilai ketepatan.")
         + _tbl([B("node", "node"), "2", "3", "5", "6", "8", "9"],
                [["U<sub>i</sub> (m)", "−0.03097", "−0.04197", "0", "0", "0.03097", "0.04197"], ["V<sub>i</sub> (m)", "−0.04552", "−0.13058", "−0.04301", "−0.13042", "−0.04552", "−0.13058"]], "num")
         + B("Nodes 1, 4 and 7 on the fixed edge have U = V = 0.", "Node 1, 4 dan 7 pada tepi tetap mempunyai U = V = 0.") + '</div>')
    body = (head + q + A.fig("fig_ps_mesh", "The 2 × 2 mesh: nodes 1–3 along the bottom, element 1 = nodes 1, 2, 5, 4 and element 3 = nodes 4, 5, 8, 7; node i carries U<sub>2i−1</sub> and U<sub>2i</sub>.",
                             "Mesh 2 × 2: node 1–3 di sepanjang bawah, element 1 = node 1, 2, 5, 4 dan element 3 = node 4, 5, 8, 7; node i membawa U<sub>2i−1</sub> dan U<sub>2i</sub>.", 420)
            + PIC("The end load bends the cantilever downward: the top fibres stretch, the bottom ones shorten, and every section carries a 10 kN shear. Element 1 is in the bottom half, so expect σ<sub>xx</sub> in compression, element 3 the same in tension, and both with the same shear. Beam theory gives the tip deflection PL³/3EI + PL/κGA = 0.160 + 0.032 = 0.192 m; four Q4 elements are a coarse model of bending, so expect less.",
                  "End load melentur cantilever ke bawah: fibre atas meregang, yang bawah memendek, dan setiap keratan membawa shear 10 kN. Element 1 di separuh bawah, jadi jangkakan σ<sub>xx</sub> dalam compression, element 3 sama dalam tension, dan kedua-duanya dengan shear yang sama. Beam theory memberi tip deflection PL³/3EI + PL/κGA = 0.160 + 0.032 = 0.192 m; empat Q4 element ialah model bending yang kasar, jadi jangkakan kurang.")
            + PLAN("s<sub>1</sub>–s<sub>12</sub> for a = 2, b = 1 → loads → {d} of elements 1 and 3 → strains at the centres → [E] → beam theory → struck rows for the reactions → finer meshes.")
            + XSTEP(1, "(a) Element constants and loads", "(a) Pemalar element dan load", 3, A.eq("w1_s") + A.eq("w1_r")
                    + CHK("The u entries of row 1 add up to zero: 0.875 − 0.123 − 0.438 − 0.314 = 0.000. The three loads add up to −10 kN."))
            + XSTEP(2, "(b) Element displacements", "(b) Displacement element", 2, P("Element 1 has the nodes 1, 2, 5, 4 in local order, so", "Element 1 mempunyai node 1, 2, 5, 4 mengikut susunan local, jadi") + A.eq("w1_d1")
                    + P("and element 3, nodes 4, 5, 8, 7, has the mirror image: {0, 0, 0, −0.04301, 0.03097, −0.04552, 0, 0}ᵀ m.", "dan element 3, node 4, 5, 8, 7, mempunyai imej cerminnya: {0, 0, 0, −0.04301, 0.03097, −0.04552, 0, 0}ᵀ m."))
            + XSTEP(3, "(c) Strains at the centre of element 1", "(c) Strain pada pusat element 1", 4, P("At (a/2, b/2) the rows of [B] reduce to averages of the side differences:", "Pada (a/2, b/2) baris [B] menjadi purata beza sisi:") + A.eq("w1_eps")
                    + NOTE("Rounding", "Pembundaran", "Differences of rounded displacements lose a digit: the unrounded solution gives ε<sub>yy</sub> = 1.253 × 10<sup>−3</sup> and ε<sub>xy</sub> = −6.650 × 10<sup>−3</sup>, which leaves the stresses below unchanged to three figures.",
                           "Beza antara displacement yang dibundarkan kehilangan satu digit: penyelesaian tanpa pembundaran memberi ε<sub>yy</sub> = 1.253 × 10<sup>−3</sup> dan ε<sub>xy</sub> = −6.650 × 10<sup>−3</sup>, yang tidak mengubah stress di bawah kepada tiga angka bererti."))
            + XSTEP(4, "(c) Stresses and beam theory", "(c) Stress dan beam theory", 4, P("With Ē = 224.44 × 10⁶ N m<sup>−2</sup> (strains in 10<sup>−3</sup>):", "Dengan Ē = 224.44 × 10⁶ N m<sup>−2</sup> (strain dalam 10<sup>−3</sup>):") + A.eq("w1_sig")
                    + P("Element 3, above it, has σ<sub>xx</sub> = +1645 kN m<sup>−2</sup> and the same shear. Beam theory at x = 1 m, 0.5 m from the neutral axis:", "Element 3, di atasnya, mempunyai σ<sub>xx</sub> = +1645 kN m<sup>−2</sup> dan shear yang sama. Beam theory pada x = 1 m, 0.5 m dari neutral axis:")
                    + A.eq("w1_beam") + ANS("(c) σ<sub>xx</sub> = ∓1.65 MPa in elements 1 and 3 (beam theory ∓2.25 MPa); σ<sub>xy</sub> = −0.50 MPa (average V/tH = 0.50 MPa)."))
            + XSTEP(5, "(d) Reactions", "(d) Reaction", 3, P("The struck rows of [K]{U} − {R} at the fixed nodes (no load acts there) give the reactions (R<sub>x</sub>, R<sub>y</sub>):", "Baris yang dibuang [K]{U} − {R} pada node tetap (tiada load bertindak di situ) memberi reaction (R<sub>x</sub>, R<sub>y</sub>):") + A.eq("w1_R")
                    + CHK("They balance the 10 kN load and its 40 kN m moment about the support."))
            + XSTEP(6, "(e) Accuracy", "(e) Ketepatan", 4, P("The tip deflection, at the corners of the free end, is 0.1306 m. Finer meshes of the course solver:", "Tip deflection, pada bucu hujung bebas, ialah 0.1306 m. Mesh lebih halus daripada solver kursus:")
                    + _tbl(["mesh", "2 × 2", "4 × 2", "8 × 4", "16 × 8", "32 × 16", "128 × 64", "beam"], [[B("tip (m)", "tip (m)"), "0.1306", "0.1643", "0.1824", "0.1886", "0.1906", "0.1915", "0.1919"]], "num")
                    + A.eq("w1_acc") + ANS("(e) The 2 × 2 mesh gives 68% of the deflection and 73% of the bending stress; about 16 × 8 elements are needed to come within 2%."))
            + INTERP("A Q4 element is too stiff in bending. Its sides stay straight, so it can rotate a section only by shearing, and the spurious shear stores energy that resists the bending (Example 3). That is why the 2 × 2 mesh deflects a third less than it should and its centroid stresses are a quarter low; it improves only as the elements become short compared with the depth, or with Q8 elements, whose two-element mesh is 7% low. The reactions, by contrast, are exact in total: the 10 kN and the 40 kN m follow from equilibrium of the whole plate whatever the mesh, although their split among nodes 1, 4 and 7 is not.",
                     "Q4 element terlalu kaku dalam bending. Sisinya kekal lurus, jadi ia hanya boleh memutar keratan dengan shear, dan shear palsu itu menyimpan tenaga yang menentang bending (Contoh 3). Itulah sebabnya mesh 2 × 2 melendut satu pertiga kurang daripada sepatutnya dan stress centroid-nya rendah satu perempat; ia bertambah baik hanya apabila element menjadi pendek berbanding kedalaman, atau dengan Q8 element, yang mesh dua element-nya rendah 7%. Reaction pula tepat secara jumlah: 10 kN dan 40 kN m terhasil daripada keseimbangan seluruh plat tanpa mengira mesh, walaupun pembahagiannya antara node 1, 4 dan 7 tidak tepat.")
            + SCHEME([("Element constants and the three nodal loads", "Pemalar element dan tiga nodal load", 3), ("Element displacements in local order", "Displacement element mengikut susunan local", 2), ("Three strains at the centre", "Tiga strain pada pusat", 4),
                      ("Stresses with [E]; beam theory and V/tH", "Stress dengan [E]; beam theory dan V/tH", 4), ("Reactions and the equilibrium check", "Reaction dan semakan keseimbangan", 3), ("Percentages and the mesh needed", "Peratus dan mesh yang diperlukan", 4)], 20))
    X.append(("z1", "The text’s cantilever: stresses, reactions, accuracy", "Cantilever dalam teks: stress, reaction, ketepatan", body))

    # ---- Example 2: error estimate from three meshes (FEM by Hand, Example 10.5 method; Example 9.7 data) ----
    head = ('<div class="xhead"><h2>' + B("Example 2 · How far is the finest mesh from the answer? An error estimate from three meshes", "Contoh 2 · Sejauh mana mesh paling halus dari jawapan? Anggaran ralat daripada tiga mesh") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> interpret computer results without an exact solution</span><span><b>' + B("Units", "Unit") + '</b> m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 10.5 (method), with the cantilever results of Example 9.7</span><span><b>15 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("The cantilever of Example 1, modelled with Q4 meshes of 8 × 4, 16 × 8 and 32 × 16 elements, gives tip deflections of 0.1824, 0.1886 and 0.1906 m. (a) Estimate the rate of convergence. (b) Estimate the converged deflection with the measured rate, and with the rate p = 2 of smooth problems. "
             "(c) Estimate the error of the 32 × 16 result. (d) A 128 × 64 mesh gives 0.1915 m and Timoshenko beam theory 0.1919 m. Comment.",
             "Cantilever dalam Contoh 1, dimodelkan dengan mesh Q4 8 × 4, 16 × 8 dan 32 × 16 element, memberi tip deflection 0.1824, 0.1886 dan 0.1906 m. (a) Anggarkan kadar convergence. (b) Anggarkan deflection yang converge dengan kadar yang diukur, dan dengan kadar p = 2 bagi masalah licin. "
             "(c) Anggarkan ralat keputusan 32 × 16. (d) Mesh 128 × 64 memberi 0.1915 m dan Timoshenko beam theory 0.1919 m. Ulas.") + '</div>')
    body = (head + q
            + PIC("Each halving of the elements moves the deflection up by a smaller step. If the steps shrink by a fixed factor 2<sup>p</sup>, the remaining distance to the converged value is a fixed multiple of the last step, which is what (10.1) uses. For a smooth problem a Q4 nodal value has p = 2; the clamped corner of the cantilever, where the elastic stress is singular, should lower it.",
                  "Setiap kali saiz element dibahagi dua, deflection naik dengan langkah yang lebih kecil. Jika langkah mengecil dengan faktor tetap 2<sup>p</sup>, jarak yang tinggal ke nilai converge ialah gandaan tetap bagi langkah terakhir, dan itulah yang digunakan oleh (10.1). Bagi masalah licin, nilai node Q4 mempunyai p = 2; bucu terkapit cantilever, di mana stress elastic singular, sepatutnya merendahkannya.")
            + PLAN("Successive changes → 2<sup>p</sup> and p → (10.1) with the measured p and with p = 2 → error of the finest mesh → compare with the 128 × 64 result and with beam theory.")
            + A.eq("wn_rich", "(10.1)")
            + XSTEP(1, "(a) The rate", "(a) Kadar", 4, A.eq("w2_rate") + ANS("(a) The changes shrink by 3.1 per halving: p ≈ 1.6, below the 2 of a smooth problem."))
            + XSTEP(2, "(b) The converged value", "(b) Nilai converge", 4, A.eq("w2_ext") + ANS("(b) About 0.1916 m with the measured rate; 0.1913 m if p = 2 is assumed."))
            + XSTEP(3, "(c) Error of the finest mesh", "(c) Ralat mesh paling halus", 3, A.eq("w2_err") + ANS("(c) The 32 × 16 deflection is about 0.5% below the converged value; assuming p = 2 would understate that error by about a third."))
            + XSTEP(4, "(d) Comment", "(d) Ulasan", 4, A.eq("w2_chk")
                    + P("The extrapolation from three meshes lands within 0.03% of a mesh with sixteen times as many elements as the finest of them, at a fraction of its cost. The assumed p = 2 falls short because the clamped corner slows the convergence; a third mesh is what reveals that. Beam theory is not the reference for the mesh error: it is a different model (a shear coefficient of 5/6 and no restraint of the Poisson contraction at the support), and its 0.2% difference from the converged plane-stress answer is a modelling difference, not a mesh error.",
                        "Ekstrapolasi daripada tiga mesh mendarat dalam 0.03% daripada mesh yang mempunyai enam belas kali ganda bilangan element mesh paling halus antaranya, dengan kos yang jauh lebih rendah. Andaian p = 2 tidak mencukupi kerana bucu terkapit melambatkan convergence; mesh ketiga yang mendedahkannya. Beam theory bukan rujukan untuk ralat mesh: ia model yang berbeza (shear coefficient 5/6 dan tiada kekangan Poisson contraction pada support), dan perbezaan 0.2% daripada jawapan plane stress yang converge ialah perbezaan pemodelan, bukan ralat mesh."))
            + INTERP("Three meshes turn computer results into an answer with an error estimate, without an exact solution, which is the normal situation in practice and the convergence table the project asks for. The estimate is only as good as the assumption that the error follows h<sup>p</sup>: check the rate with the third mesh, and distrust an extrapolation whose steps do not shrink by a steady factor. At the fixed corner itself the stresses do not shrink at all (Notes §4), so no extrapolation is possible there.",
                     "Tiga mesh menukar keputusan komputer kepada jawapan dengan anggaran ralat, tanpa penyelesaian tepat, iaitu keadaan biasa dalam amalan dan convergence table yang diminta dalam projek. Anggaran itu hanya sebaik andaian bahawa ralat mengikut h<sup>p</sup>: semak kadarnya dengan mesh ketiga, dan jangan percaya ekstrapolasi yang langkahnya tidak mengecil dengan faktor yang tetap. Pada bucu tetap itu sendiri stress langsung tidak mengecil (Nota §4), jadi ekstrapolasi tidak mungkin di situ.")
            + SCHEME([("Successive changes, 2<sup>p</sup> and p", "Perubahan berturut-turut, 2<sup>p</sup> dan p", 4), ("Extrapolated value, both rates", "Nilai ekstrapolasi, kedua-dua kadar", 4), ("Signed error of the finest mesh", "Ralat bertanda mesh paling halus", 3), ("Comparison with the fine mesh and with beam theory, with reasons", "Perbandingan dengan mesh halus dan beam theory, dengan sebab", 4)], 15))
    X.append(("z2", "Error estimate from three meshes", "Anggaran ralat daripada tiga mesh", body))

    # ---- Example 3: why a Q4 is too stiff in bending (FEM by Hand, Example 10.6) ----
    head = ('<div class="xhead"><h2>' + B("Example 3 · Why a Q4 element is too stiff in bending, and which refinement helps", "Contoh 3 · Mengapa Q4 element terlalu kaku dalam bending, dan refine mana yang membantu") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> explain an inaccurate result; choose a mesh</span><span><b>' + B("Units", "Unit") + '</b> N, m</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 10.6</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("(a) A Q4 element in plane stress, of length a and depth b, is bent by equal and opposite couples on its two ends, which stay straight. Show where its strain field departs from pure bending, and find the ratio of its end rotation to the exact one. "
             "(b) The cantilever of Example 1 gives these tip deflections, as percentages of a 128 × 64 mesh (0.1915 m). Which refinement helps, and why? (c) What does an 8-node element change?",
             "(a) Satu Q4 element dalam plane stress, panjang a dan dalam b, dilentur oleh couple yang sama dan bertentangan pada dua hujungnya, yang kekal lurus. Tunjukkan di mana strain field-nya berbeza daripada pure bending, dan cari nisbah putaran hujungnya kepada nilai tepat. "
             "(b) Cantilever dalam Contoh 1 memberi tip deflection berikut, sebagai peratus mesh 128 × 64 (0.1915 m). Refine mana yang membantu, dan mengapa? (c) Apa yang diubah oleh 8-node element?")
         + _tbl([B("mesh (along × through)", "mesh (sepanjang × merentas)"), "2 × 2", "2 × 4", "2 × 8", "4 × 2", "8 × 2", "8 × 4", "16 × 8"], [["%", "68.2", "69.6", "70.1", "85.8", "91.9", "95.2", "98.5"]], "num") + '</div>')
    body = (head + q + A.fig("fig_bend", "Pure bending of a block: (a) exact; (b) one Q4 element.", "Pure bending sebuah blok: (a) tepat; (b) satu Q4 element.", 560)
            + PIC("In pure bending the top and bottom fibres curve while the ends stay plane and square to them. The sides of a Q4 element stay straight, so its ends can rotate only by shearing the element. That shear stores energy which the real block does not have, and the element resists bending more than it should.",
                  "Dalam pure bending, fibre atas dan bawah melengkung manakala hujung kekal rata dan tegak kepadanya. Sisi Q4 element kekal lurus, jadi hujungnya hanya boleh berputar dengan meng-shear element itu. Shear itu menyimpan tenaga yang tiada pada blok sebenar, dan element itu menentang bending lebih daripada sepatutnya.")
            + PLAN("Bilinear bending field → its strains → strain energy → moment–rotation → ratio → the cantilever table → Q8.")
            + XSTEP(1, "(a) The strain field", "(a) Strain field", 4, P("Let the element bend to a curvature κ′, with the origin at its centre, so that its ends turn by ±κ′a/2. The bilinear field that does this is", "Biarkan element melentur kepada kelengkungan κ′, dengan origin di pusatnya, supaya hujungnya berputar ±κ′a/2. Field bilinear yang melakukannya ialah") + A.eq("w3_field")
                    + P("The exact field has γ<sub>xy</sub> = 0 and ε<sub>yy</sub> = −νε<sub>xx</sub>. The element has a shear strain that grows towards its ends — the parasitic shear — and no lateral strain, because v would need a y² term.",
                        "Field tepat mempunyai γ<sub>xy</sub> = 0 dan ε<sub>yy</sub> = −νε<sub>xx</sub>. Element itu mempunyai shear strain yang bertambah ke arah hujungnya — parasitic shear — dan tiada lateral strain, kerana v memerlukan term y²."))
            + XSTEP(2, "(a) Strain energy", "(a) Tenaga strain", 4, P("With ε<sub>yy</sub> = 0, σ<sub>xx</sub> = Ēε<sub>xx</sub>, and per unit thickness", "Dengan ε<sub>yy</sub> = 0, σ<sub>xx</sub> = Ēε<sub>xx</sub>, dan per unit ketebalan") + A.eq("w3_U"))
            + XSTEP(3, "(a) Moment and the ratio of rotations", "(a) Momen dan nisbah putaran", 5, A.eq("w3_M") + A.eq("w3_ratio") + A.eq("w3_nums")
                    + ANS("(a) γ<sub>xy</sub> = −κ′x ≠ 0 and ε<sub>yy</sub> = 0; θ<sub>Q4</sub>/θ<sub>exact</sub> = (1 − ν²)/[1 + (1 − ν)(a/b)²/2], 0.67 for a square element with ν = 0.3.")
                    + CHK("A one-element computation with the course solver, end couples applied as consistent loads, gives 0.837, 0.674, 0.379 and 0.138: the same four ratios."))
            + XSTEP(4, "(b) The cantilever", "(b) Cantilever", 4, P("Refining through the depth only, 2 × 2 → 2 × 4 → 2 × 8, moves the deflection from 68.2 to 70.1%. Every layer of elements carries the same parasitic shear, whatever its depth: what governs is the element length over the depth of the member, a/B, which stays 1. "
                                                                    "Refining along the length, 2 × 2 → 4 × 2 → 8 × 2, raises it to 85.8 and 91.9%, because a/B falls to 0.5 and 0.25. With both, 8 × 4 and 16 × 8 reach 95.2 and 98.5% at a/B = 0.25 and 0.125.",
                                                                    "Refine merentas kedalaman sahaja, 2 × 2 → 2 × 4 → 2 × 8, mengubah deflection dari 68.2 kepada 70.1%. Setiap lapisan element membawa parasitic shear yang sama, tanpa mengira kedalamannya: yang menentukan ialah panjang element berbanding kedalaman anggota, a/B, yang kekal 1. "
                                                                    "Refine di sepanjang panjang, 2 × 2 → 4 × 2 → 8 × 2, menaikkannya kepada 85.8 dan 91.9%, kerana a/B turun kepada 0.5 dan 0.25. Dengan kedua-duanya, 8 × 4 dan 16 × 8 mencapai 95.2 dan 98.5% pada a/B = 0.25 dan 0.125.")
                    + ANS("(b) Refine along the length, so that the elements are short compared with the depth of the member; refining through the depth alone gains less than 2 points."))
            + XSTEP(5, "(c) The 8-node element", "(c) 8-node element", 3, P("Its sides are quadratic, so they can curve and pure bending needs no shear. Two Q8 elements give 0.1780 m (92.9%) and a 4 × 2 Q8 mesh 0.1885 m (98.4%), against 68.2% for four Q4 elements.",
                                                                          "Sisinya quadratic, jadi ia boleh melengkung dan pure bending tidak memerlukan shear. Dua Q8 element memberi 0.1780 m (92.9%) dan mesh Q8 4 × 2 memberi 0.1885 m (98.4%), berbanding 68.2% bagi empat Q4 element.")
                    + ANS("(c) Q8 removes the parasitic shear: two elements are 7% low where four Q4 are 32% low."))
            + INTERP("The Q4 fails in bending for a reason that can be seen in one element: its straight sides force a shear strain that pure bending does not have, and relative to the bending energy that shear energy grows with (a/b)². The error therefore depends on how the elements are arranged, not only on how many there are, and an analyst can control it: where a member bends, refine along its length until the elements are short compared with its depth, or use an element whose sides can bend. That is the reason Workbench meshes 2D solids with PLANE183, the 8-node element.",
                     "Q4 gagal dalam bending atas sebab yang boleh dilihat dalam satu element: sisinya yang lurus memaksa shear strain yang tiada dalam pure bending, dan berbanding tenaga bending, tenaga shear itu bertambah dengan (a/b)². Jadi ralat bergantung pada susunan element, bukan hanya bilangannya, dan penganalisis boleh mengawalnya: di mana anggota melentur, refine di sepanjang panjangnya sehingga element pendek berbanding kedalamannya, atau gunakan element yang sisinya boleh melentur. Itulah sebab Workbench menggunakan PLANE183, iaitu 8-node element, untuk 2D solid.")
            + SCHEME([("Bilinear field and its three strains", "Field bilinear dan tiga strain-nya", 4), ("Strain energy with both terms", "Tenaga strain dengan kedua-dua term", 4), ("Moment, exact moment, ratio and its values", "Momen, momen tepat, nisbah dan nilainya", 5),
                      ("Which refinement helps, with a/B", "Refine mana yang membantu, dengan a/B", 4), ("What Q8 changes, with numbers", "Apa yang diubah oleh Q8, dengan nombor", 3)], 20))
    X.append(("z3", "Why a Q4 is too stiff in bending", "Mengapa Q4 terlalu kaku dalam bending", body))
    return X
