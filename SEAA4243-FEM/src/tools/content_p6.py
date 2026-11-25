"""Content of Part 6 — ANSYS demo: hand calculation versus software. The text's plate (§2.3) and cantilever (§3.4)
rebuilt in Workbench, the mesh study, reading stresses, four wrong models, the first verified run of the project
model, and verification against validation with the stage gates of the hybrid project (ANSYS + an own tool).
Every number was recomputed with SEAA4243-FEM/code/fe_heat_q4.py and fe_plane_stress.py; the patch test of Example 4
with a small independent assembly that calls fe_plane_stress.element_stiffness. ANSYS values are never quoted as
measured: the page gives the predictions a correct run must reproduce, and says where Mechanical may differ."""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, TRY, QC, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME
from content_p1 import MCQ
import re

PART = {
    "n": 6, "slug": "06-ansys-demo", "deck": "deck_w14",
    "eqs": ["eqs_ps4_ex", "eqs_ps3_ex"], "figs": ["figs_ps4_ex", "figs_w14"],
    "topic": ("ANSYS", "ANSYS"), "part": "Demo",
    "title": "ANSYS Demo — Hand Calculation versus Software",
    "sub": ("The two textbook problems rebuilt in ANSYS Workbench — predict, run, compare, explain: the heat plate and the cantilever, the mesh study, what a stress plot averages, four wrong models and their signatures, "
            "the first verified run of your project model, and how verification differs from validation in the hybrid project.",
            "Dua masalah buku teks dibina semula dalam ANSYS Workbench — ramal, run, banding, terangkan: plat haba dan cantilever, kajian mesh, apa yang dipuratakan oleh plot stress, empat model yang salah dan tanda-tandanya, "
            "run pertama yang disahkan bagi model projek anda, dan beza verification dengan validation dalam projek hibrid."),
    "pdf": "pdf/ansys-demo-slides.pdf",
    "lab": {"id": "cant", "file": "../labs/cant.html", "name": "Cantilever Explorer", "inclass": "study"},
    "minutes": {"n1": 9, "n2": 7, "n3": 9, "n4": 8, "n5": 6, "n6": 9, "n7": 10},
    "target_min": 30,
    "code": "ps",
    "textref": "§2.3 and §3.4",
    "covers": ("Five sessions of hand calculation end here, at the computer. Every object in ANSYS Workbench has a name from those sessions — element order is the choice of shape functions, a Fixed Support is an essential condition, a Force on an edge becomes the consistent loads you integrated by hand — "
               "so every number on the screen can be predicted before Solve is pressed. The habit this part builds is the one the project is marked on: reaction first, then a hand estimate, then refinement, and two independent tools that must agree.",
               "Lima sesi pengiraan tangan berakhir di sini, di hadapan komputer. Setiap objek dalam ANSYS Workbench mempunyai nama daripada sesi-sesi itu — element order ialah pilihan shape function, Fixed Support ialah essential condition, Force pada tepi menjadi consistent load yang anda integrate dengan tangan — "
               "jadi setiap nombor pada skrin boleh diramal sebelum butang Solve ditekan. Tabiat yang dibina di sini ialah tabiat yang dinilai dalam projek: reaction dahulu, kemudian anggaran tangan, kemudian refine, dan dua alat bebas yang mesti sepakat."),
    "inclass_n": ("3 h · computer lab · 5 activities", "3 jam · makmal komputer · 5 aktiviti"),
    "inclass": [("A1 convert the textbook data for the dialog boxes · A2 predict the plate before Solve", "A1 tukar data buku teks untuk kotak dialog · A2 ramal plat sebelum Solve"),
                ("A3 the cantilever mesh study and its convergence table · A4 spot the wrong model from its numbers", "A3 kajian mesh cantilever dan convergence table-nya · A4 kenal pasti model yang salah daripada nombornya"),
                ("A5 project lab: the first verified run of your group’s model", "A5 makmal projek: run pertama yang disahkan bagi model kumpulan anda")],
    "recall_title": ("Recall from Plane Stress Part 3", "Ingat semula Plane Stress Part 3"),
}

OUTCOMES = [
    ("Build a 2D steady-state thermal model and a 2D plane-stress model in ANSYS Workbench, with units, material, thickness, mesh, supports and loads entered correctly.",
     "Membina model 2D steady-state thermal dan model 2D plane stress dalam ANSYS Workbench, dengan unit, bahan, ketebalan, mesh, support dan load dimasukkan dengan betul."),
    ("Map every ANSYS object to the hand calculation: element order, consistent loads, essential and natural conditions, averaged and element stresses, reactions.",
     "Memadankan setiap objek ANSYS dengan pengiraan tangan: element order, consistent load, essential dan natural condition, stress averaged dan element, reaction."),
    ("Predict a result before running it, run a mesh study, and check the model against one independent calculation before reading any contour plot.",
     "Meramal keputusan sebelum run, menjalankan kajian mesh, dan menyemak model dengan satu pengiraan bebas sebelum membaca sebarang contour plot."),
    ("Distinguish verification from validation, recognise four classic modelling mistakes from their symptoms, and take a project model through the stage gates of the hybrid project.",
     "Membezakan verification dan validation, mengenal pasti empat kesilapan pemodelan klasik daripada simptomnya, dan membawa model projek melalui stage gate projek hibrid."),
]

CANDO = [
    ("Convert an edge load into the Force and the Pressure that ANSYS asks for, and check one against the other.", "Menukar edge load kepada Force dan Pressure yang diminta ANSYS, dan menyemak satu dengan yang lain."),
    ("Choose Edge Sizing or Element Size and the Element Order that reproduce a hand mesh, and predict the result of that run.", "Memilih Edge Sizing atau Element Size dan Element Order yang menghasilkan semula mesh tangan, dan meramal keputusan run itu."),
    ("Read the reaction first and say what a wrong reaction means; compare a stress with beam theory at an element centroid.", "Membaca reaction dahulu dan menyatakan maksud reaction yang salah; membandingkan stress dengan beam theory pada centroid element."),
    ("Tabulate a mesh study with the change between meshes, an extrapolated value and a signed difference from an independent check.", "Menjadualkan kajian mesh dengan perubahan antara mesh, nilai ekstrapolasi dan perbezaan bertanda daripada semakan bebas."),
    ("Name the wrong model from its signature: a factor, a location, a warning or an extra stress component.", "Menamakan model yang salah daripada tandanya: satu faktor, satu lokasi, satu amaran atau satu komponen stress tambahan."),
    ("Explain what each stage gate of the hybrid project proves, and what it cannot prove.", "Menerangkan apa yang dibuktikan oleh setiap stage gate projek hibrid, dan apa yang tidak dapat dibuktikannya."),
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
    # ---- n1: from the textbook to Workbench ----
    body = (
        P("Nothing in ANSYS Workbench is new mathematics. Its six cells are the six steps you have done with pen and paper: Engineering Data is [E] or k, Geometry is the domain, Mesh chooses the shape functions, Setup holds the loads and the essential conditions, Solution solves [K]{U} = {R}, and Results is [E][B]{û}. "
          "What is new is speed, and with speed the temptation to believe the first colour plot.",
          "Tiada matematik baharu dalam ANSYS Workbench. Enam sel-nya ialah enam langkah yang sudah anda buat dengan pen dan kertas: Engineering Data ialah [E] atau k, Geometry ialah domain, Mesh memilih shape function, Setup memegang load dan essential condition, Solution menyelesaikan [K]{U} = {R}, dan Results ialah [E][B]{û}. "
          "Yang baharu ialah kelajuan, dan bersama kelajuan datang godaan untuk mempercayai contour plot pertama.")
        + A.fig("fig_wb_flow", "The six Workbench cells above the matching steps of the hand calculation.", "Enam sel Workbench di atas langkah pengiraan tangan yang sepadan.", 640)
        + H3("ANSYS object ↔ textbook quantity", "Objek ANSYS ↔ kuantiti buku teks")
        + _tbl([B("In Mechanical", "Dalam Mechanical"), B("In the textbook", "Dalam buku teks"), B("Where you met it", "Di mana anda menemuinya")],
               [["Element Order: Linear / Quadratic (PLANE182 / PLANE183; thermal PLANE55 / PLANE77)", B("4-node Q4 / 8-node Q8", "4-node Q4 / 8-node Q8"), B("shear locking of Q4 in bending (Plane Stress Parts 2–3)", "shear locking Q4 dalam bending (Plane Stress Part 2–3)")],
                ["Element Size · Edge Sizing (divisions) · Face Meshing", B("a, b and the structured mesh", "a, b dan mesh berstruktur"), B("convergence tables", "convergence table")],
                ["Fixed Support · Displacement · Temperature", B("essential conditions: rows struck, Û known", "essential condition: baris dibuang, Û diketahui"), B("reduced system (Heat Transfer Part 2)", "sistem terturun (Heat Transfer Part 2)")],
                ["Force · Pressure · Heat Flux · Internal Heat Generation", B("natural conditions and sources: {b}, {q}, {r}", "natural condition dan sumber: {b}, {q}, {r}"), B("consistent loads qb/2 and 1/6 – 2/3 – 1/6", "consistent load qb/2 dan 1/6 – 2/3 – 1/6")],
                [B("nothing on an edge", "tiada apa pada tepi"), B("insulated or traction-free: the boundary integral vanishes", "insulated atau bebas traction: boundary integral hilang"), B("Heat Transfer Part 1", "Heat Transfer Part 1")],
                ["Averaged · Unaveraged · Elemental Mean", B("nodal average · element values · centroid value", "purata nodal · nilai element · nilai centroid"), B("Plane Stress Part 3", "Plane Stress Part 3")],
                ["Force Reaction · Moment Reaction (probes)", B("struck rows: [K]{U} − {R} at the fixed dofs", "baris yang dibuang: [K]{U} − {R} pada dof tetap"), B("equilibrium check", "semakan keseimbangan")]])
        + NOTE("Menu names vary by version", "Nama menu berbeza mengikut versi",
               "The names here are those of recent Mechanical releases (2023–2026), as on the slides; §7 collects the steps the demonstrations skip (curved edges, holes, varying loads, results along a line). In other versions an option may sit in a different panel (for example Analysis Type under the Geometry cell’s properties, or Display Option under Integration Point Results); the object and its meaning do not change. ANSYS Student is enough for every model on this page.",
               "Nama di sini ialah nama dalam keluaran Mechanical terkini (2023–2026), seperti dalam slides; §7 menghimpunkan langkah yang tidak ditunjukkan dalam demonstrasi (tepi melengkung, lubang, load yang berubah, keputusan sepanjang garisan). Dalam versi lain sesuatu pilihan mungkin berada di panel lain (contohnya Analysis Type di bawah properties sel Geometry, atau Display Option di bawah Integration Point Results); objek dan maknanya tidak berubah. ANSYS Student mencukupi untuk setiap model di halaman ini.")
        + H3("Units first, then the five numbers of each problem", "Unit dahulu, kemudian lima nombor bagi setiap masalah")
        + LI([("<b>Unit system:</b> Metric (m, kg, N, s, V, A), set before anything else. Mechanical prints the unit beside every input field: read it.", "<b>Unit system:</b> Metric (m, kg, N, s, V, A), ditetapkan sebelum perkara lain. Mechanical mencetak unit di sebelah setiap ruang input: bacalah."),
              ("<b>2D:</b> Analysis Type = 2D on the Geometry cell before the geometry is drawn; in Mechanical, 2D Behavior = Plane Stress and the Thickness (0.01 m for the cantilever).", "<b>2D:</b> Analysis Type = 2D pada sel Geometry sebelum geometri dilukis; dalam Mechanical, 2D Behavior = Plane Stress dan Thickness (0.01 m untuk cantilever)."),
              ("<b>Material:</b> the cantilever’s E = 2 × 10⁸ Pa and ν = 0.33 are the textbook’s, a thousand times softer than steel — keep them so that the numbers match the book. The plate’s k = 300 W m<sup>−1</sup> K<sup>−1</sup> (the §2.3 figure says 400: an erratum).", "<b>Bahan:</b> E = 2 × 10⁸ Pa dan ν = 0.33 bagi cantilever ialah nilai buku teks, seribu kali lebih lembut daripada keluli — kekalkan supaya nombor sepadan dengan buku. k plat = 300 W m<sup>−1</sup> K<sup>−1</sup> (rajah §2.3 menulis 400: erratum).")])
        + STEP("Worked conversion · the cantilever’s load and mesh (Activity 1)", "Penukaran bekerja · load dan mesh cantilever (Aktiviti 1)",
               P("The text gives q<sub>y</sub> = −5 kN m<sup>−1</sup> on the 2 m right edge of a 0.01 m plate: force per unit length of edge, thickness already included. The dialog wants either a total Force or a Pressure:",
                 "Teks memberi q<sub>y</sub> = −5 kN m<sup>−1</sup> pada tepi kanan 2 m bagi plat 0.01 m: daya per unit panjang tepi, ketebalan sudah termasuk. Kotak dialog mahukan sama ada jumlah Force atau Pressure:")
               + A.eq("p6_load") + A.eq("p6_load_chk")
               + P("The hand mesh has rectangular 2 m × 1 m elements, so it is set by divisions per edge, not by one element size (an Element Size of 1 m would give 4 × 2). The plate’s 16 × 16 mesh is a single size:",
                   "Mesh tangan mempunyai element segi empat tepat 2 m × 1 m, jadi ia ditetapkan dengan bilangan bahagian setiap tepi, bukan dengan satu saiz element (Element Size 1 m akan memberi 4 × 2). Mesh 16 × 16 plat ialah satu saiz:")
               + A.eq("p6_size")
               + P("Element Order: Linear for the hand element. Mechanical never asks for nodal loads: it integrates the Force or Pressure into the consistent loads of Plane Stress Parts 2–3 itself.",
                   "Element Order: Linear untuk element tangan. Mechanical tidak pernah meminta nodal load: ia sendiri meng-integrate Force atau Pressure menjadi consistent load seperti dalam Plane Stress Part 2–3."))
        + NOTE("The most common failure in student projects", "Kegagalan paling biasa dalam projek pelajar",
               "A wrong unit system: geometry drawn in mm with loads in N and E in Pa is a model of a different structure, and nothing in the solver objects. A wrong unit shows up as a factor of 10³ or 10⁶ somewhere — which is why every result is predicted first.",
               "Unit system yang salah: geometri dilukis dalam mm dengan load dalam N dan E dalam Pa ialah model struktur yang lain, dan solver tidak membantah langsung. Unit yang salah muncul sebagai faktor 10³ atau 10⁶ di suatu tempat — sebab itulah setiap keputusan diramal dahulu.")
        + KP([("Six Workbench cells = six hand steps; the software integrates and assembles, you decide the idealisation.", "Enam sel Workbench = enam langkah tangan; perisian meng-integrate dan assemble, anda menentukan idealisation."),
              ("q<sub>y</sub> = −5 kN m<sup>−1</sup> on a 2 m edge, t = 0.01 m: Force −10 000 N or Pressure −500 kPa; Pressure × edge area gives the Force back.", "q<sub>y</sub> = −5 kN m<sup>−1</sup> pada tepi 2 m, t = 0.01 m: Force −10 000 N atau Pressure −500 kPa; Pressure × luas tepi memberi semula Force."),
              ("Hand mesh: Edge Sizing 2 and 2, Linear. Plate 16 × 16: Element Size 0.0625 m.", "Mesh tangan: Edge Sizing 2 dan 2, Linear. Plat 16 × 16: Element Size 0.0625 m.")])
        + QC("q1", "A load of 3 kN m<sup>−1</sup> acts on a 1.5 m edge of a plate 0.02 m thick. The Pressure to enter is", "Load 3 kN m<sup>−1</sup> bertindak pada tepi 1.5 m bagi plat setebal 0.02 m. Pressure yang perlu dimasukkan ialah",
             [("a", "150 kPa", "150 kPa"), ("b", "4.5 kPa", "4.5 kPa"), ("c", "0.06 kPa", "0.06 kPa")],
             "a", "p = q/t = 3/0.02 = 150 kN m<sup>−2</sup> = 150 kPa. Check: 150 × (1.5 × 0.02) = 4.5 kN = q × 1.5, the total Force. 4.5 is that Force in kN, not a pressure; 0.06 is q × t.",
             "p = q/t = 3/0.02 = 150 kN m<sup>−2</sup> = 150 kPa. Semak: 150 × (1.5 × 0.02) = 4.5 kN = q × 1.5, iaitu jumlah Force. 4.5 ialah Force itu dalam kN, bukan pressure; 0.06 ialah q × t.")
    )
    S.append(("n1", "From the textbook to Workbench", "Dari buku teks ke Workbench", body))

    # ---- n2: demo 1, the heat plate ----
    body = (
        P("The first demonstration is the plate of Heat Transfer Part 2: 1 m square, k = 300 W m<sup>−1</sup> K<sup>−1</sup>, 600 W m<sup>−3</sup> generated inside, 0 °C on the top and left edges, nothing on the other two. Its answers are already known, so the run is a test of the model, not a source of new numbers.",
          "Demonstrasi pertama ialah plat Heat Transfer Part 2: segi empat sama 1 m, k = 300 W m<sup>−1</sup> K<sup>−1</sup>, 600 W m<sup>−3</sup> dijana di dalam, 0 °C pada tepi atas dan kiri, tiada apa pada dua tepi lagi. Jawapannya sudah diketahui, jadi run ini menguji model, bukan sumber nombor baharu.")
        + A.fig("fig_plate_ansys", "The plate in ANSYS terms: Temperature 0 °C on the top and left edges, nothing on the other two (insulated), Internal Heat Generation on the body, a probe at the bottom-right corner.",
                "Plat dalam istilah ANSYS: Temperature 0 °C pada tepi atas dan kiri, tiada apa pada dua tepi lagi (insulated), Internal Heat Generation pada jasad, probe di bucu kanan bawah.", 340)
        + H3("Build order", "Urutan membina")
        + OL([("Toolbox → <b>Steady-State Thermal</b>; Geometry cell properties → Analysis Type: 2D.", "Toolbox → <b>Steady-State Thermal</b>; properties sel Geometry → Analysis Type: 2D."),
              ("Engineering Data: new material, Isotropic Thermal Conductivity 300 W m<sup>−1</sup> K<sup>−1</sup>.", "Engineering Data: bahan baharu, Isotropic Thermal Conductivity 300 W m<sup>−1</sup> K<sup>−1</sup>."),
              ("Geometry: sketch a 1 m × 1 m rectangle on the XY plane; Surfaces From Sketches; assign the material.", "Geometry: lakar segi empat 1 m × 1 m pada satah XY; Surfaces From Sketches; tetapkan bahan."),
              ("Mesh: Face Meshing, Element Size 0.5 m, Element Order Linear → 4 elements, 9 nodes: the hand mesh.", "Mesh: Face Meshing, Element Size 0.5 m, Element Order Linear → 4 element, 9 node: mesh tangan."),
              ("Temperature 0 °C on the top and left edges; Internal Heat Generation 600 W m<sup>−3</sup> on the body.", "Temperature 0 °C pada tepi atas dan kiri; Internal Heat Generation 600 W m<sup>−3</sup> pada jasad."),
              ("Solve → Temperature; a probe at the bottom-right vertex; Total Heat Flux as vectors; a Reaction probe on the Temperature conditions.", "Solve → Temperature; probe di bucu kanan bawah; Total Heat Flux sebagai vektor; Reaction probe pada keadaan Temperature.")])
        + H3("Predict before Solve (Activity 2)", "Ramal sebelum Solve (Aktiviti 2)")
        + _tbl([B("Run", "Run"), B("Prediction", "Ramalan"), B("From", "Daripada")],
               [[B("4 linear elements, bottom-right corner", "4 linear element, bucu kanan bawah"), "0.6214", B("Heat Transfer Part 2, text (2.55)", "Heat Transfer Part 2, teks (2.55)")],
                [B("4 linear elements, mid-point of the bottom edge", "4 linear element, titik tengah tepi bawah"), "0.4821", B("same solution (symmetry: also the right mid-edge)", "penyelesaian yang sama (simetri: juga tengah tepi kanan)")],
                [B("256 linear elements (0.0625 m), corner", "256 linear element (0.0625 m), bucu"), "0.5898", B("text Table 2.1", "teks Jadual 2.1")],
                [B("4 quadratic elements, corner", "4 quadratic element, bucu"), "≈ 0.584 – 0.590", B("text Q8 2 × 1: 0.5836; record your value", "teks Q8 2 × 1: 0.5836; catat nilai anda")],
                [B("converged reference", "rujukan converge"), "0.5897", B("text Table 2.1 (software)", "teks Jadual 2.1 (perisian)")]])
        + P("The linear 2 × 2 run uses the same element and the same consistent {q} as the hand calculation, so it must agree to three or four decimals. The refined runs measure how far the hand mesh was from the answer:",
            "Run linear 2 × 2 menggunakan element dan {q} consistent yang sama seperti pengiraan tangan, jadi ia mesti sepakat hingga tiga atau empat tempat perpuluhan. Run yang di-refine mengukur sejauh mana mesh tangan daripada jawapan:")
        + A.eq("p6_plate_err")
        + H3("The independent check: heat in = heat out", "Semakan bebas: haba masuk = haba keluar")
        + A.eq("p6_heat")
        + SB(P("The reaction at a node with a prescribed temperature is the heat that must be removed there to hold it at 0 °C: the struck rows of [K]{T} − {R}, exactly as for the forces at a support. Their sum over both cold edges must equal what the body generates, on any mesh. Thickness does not change the temperatures; it scales every heat flow, so read the reaction with the model’s thickness in mind.",
               "Reaction pada node dengan suhu yang ditetapkan ialah haba yang mesti dikeluarkan di situ untuk mengekalkannya pada 0 °C: baris yang dibuang [K]{T} − {R}, sama seperti daya pada support. Jumlahnya pada kedua-dua tepi sejuk mesti sama dengan haba yang dijana oleh jasad, pada sebarang mesh. Ketebalan tidak mengubah suhu; ia menskala setiap aliran haba, jadi baca reaction dengan mengambil kira ketebalan model."))
        + NOTE("If the 2 × 2 run does not give 0.6214", "Jika run 2 × 2 tidak memberi 0.6214",
               "Check the node count first: 9 nodes means the hand mesh, 25 means a 4 × 4 mesh (corner 0.5968). Then the element order: Program Controlled gives quadratic elements. Both are common, and both are found in a minute because the answer was predicted.",
               "Semak bilangan node dahulu: 9 node bermaksud mesh tangan, 25 bermaksud mesh 4 × 4 (bucu 0.5968). Kemudian element order: Program Controlled memberi quadratic element. Kedua-duanya biasa, dan kedua-duanya ditemui dalam seminit kerana jawapannya sudah diramal.")
        + KP([("Linear 2 × 2: 0.6214 at the corner, 0.4821 at the mid-edges — the hand calculation, to four decimals.", "Linear 2 × 2: 0.6214 di bucu, 0.4821 di tengah tepi — pengiraan tangan, hingga empat tempat perpuluhan."),
              ("16 × 16: 0.5898, +0.02% from the converged 0.5897; the hand mesh is +5.4%.", "16 × 16: 0.5898, +0.02% daripada 0.5897 yang converge; mesh tangan +5.4%."),
              ("Reaction on the cold edges = −Q A t: heat out equals heat generated on every mesh.", "Reaction pada tepi sejuk = −Q A t: haba keluar sama dengan haba dijana pada setiap mesh.")])
        + QC("q2", "Your “linear 2 × 2” plate run shows 0.5968 °C at the corner instead of 0.6214. The most likely cause is", "Run plat “linear 2 × 2” anda menunjukkan 0.5968 °C di bucu dan bukannya 0.6214. Punca yang paling mungkin ialah",
             [("a", "the mesh is 4 × 4, not 2 × 2", "mesh ialah 4 × 4, bukan 2 × 2"), ("b", "the thickness is wrong", "ketebalan salah"), ("c", "the heat generation was entered per unit area", "penjanaan haba dimasukkan per unit luas")],
             "a", "0.5968 is exactly the 4 × 4 linear value: an Element Size of 0.25 m instead of 0.5 m. Thickness cannot change a temperature in this problem; a source in the wrong unit would change it by a large factor, not by 4%. Check Mesh → Statistics: 25 nodes.",
             "0.5968 ialah tepat nilai linear 4 × 4: Element Size 0.25 m dan bukannya 0.5 m. Ketebalan tidak boleh mengubah suhu dalam masalah ini; sumber dalam unit yang salah akan mengubahnya dengan faktor yang besar, bukan 4%. Semak Mesh → Statistics: 25 node.")
    )
    S.append(("n2", "Demo 1 · the heat plate", "Demo 1 · plat haba", body))

    # ---- n3: demo 2, the cantilever and the mesh study ----
    body = (
        P("The second demonstration is the cantilever of Plane Stress Part 2: 4 m × 2 m, t = 0.01 m, fixed on the left, −10 kN on the right edge. Two things are predicted: the 2 × 2 linear run must give the hand value, 0.1306 m, and a refined quadratic mesh must approach Timoshenko beam theory, 0.1919 m.",
          "Demonstrasi kedua ialah cantilever Plane Stress Part 2: 4 m × 2 m, t = 0.01 m, tetap di kiri, −10 kN pada tepi kanan. Dua perkara diramal: run linear 2 × 2 mesti memberi nilai tangan, 0.1306 m, dan mesh quadratic yang di-refine mesti menghampiri Timoshenko beam theory, 0.1919 m.")
        + A.fig("fig_cant_ansys", "The cantilever in ANSYS terms: Fixed Support on the left edge, a Force of −10 kN in y on the right edge (or −500 kPa), plane stress with t = 0.01 m, a deformation probe at the tip.",
                "Cantilever dalam istilah ANSYS: Fixed Support pada tepi kiri, Force −10 kN dalam y pada tepi kanan (atau −500 kPa), plane stress dengan t = 0.01 m, probe deformation di hujung.", 640)
        + H3("Build order", "Urutan membina")
        + OL([("Toolbox → <b>Static Structural</b>; Analysis Type 2D; Engineering Data: Isotropic Elasticity, E = 2 × 10⁸ Pa, ν = 0.33.", "Toolbox → <b>Static Structural</b>; Analysis Type 2D; Engineering Data: Isotropic Elasticity, E = 2 × 10⁸ Pa, ν = 0.33."),
              ("Geometry: 4 m × 2 m surface body. In Mechanical: Geometry → 2D Behavior: Plane Stress; the body’s Thickness 0.01 m.", "Geometry: surface body 4 m × 2 m. Dalam Mechanical: Geometry → 2D Behavior: Plane Stress; Thickness jasad 0.01 m."),
              ("Mesh: Face Meshing; Edge Sizing, 2 divisions on all four edges (Behavior: Hard); Element Order Linear → 4 elements, 9 nodes.", "Mesh: Face Meshing; Edge Sizing, 2 bahagian pada keempat-empat tepi (Behavior: Hard); Element Order Linear → 4 element, 9 node."),
              ("Fixed Support on the left edge; Force on the right edge, Define By: Components, Y = −10 000 N.", "Fixed Support pada tepi kiri; Force pada tepi kanan, Define By: Components, Y = −10 000 N."),
              ("Solve → <b>Force Reaction</b> and Moment Reaction probes on the Fixed Support first; then Directional Deformation (Y) and a probe at the top-right vertex.", "Solve → probe <b>Force Reaction</b> dan Moment Reaction pada Fixed Support dahulu; kemudian Directional Deformation (Y) dan probe di bucu kanan atas.")])
        + A.eq("p6_reaction")
        + NOTE("ANSYS’s linear element is not the textbook Q4", "Linear element ANSYS bukan Q4 buku teks",
               "With Element Control on Program Controlled, Mechanical may give PLANE182 an enhanced-strain formulation that bends far better than the textbook Q4. If your 2 × 2 linear run is much closer to 0.19 m than 0.1306 m, that is why: set Element Control to Manual with full integration to see the textbook element. Report which one you used; do not hide the difference — explaining it is the point.",
               "Dengan Element Control pada Program Controlled, Mechanical mungkin memberi PLANE182 formulasi enhanced strain yang melentur jauh lebih baik daripada Q4 buku teks. Jika run linear 2 × 2 anda jauh lebih dekat kepada 0.19 m berbanding 0.1306 m, itulah sebabnya: tetapkan Element Control kepada Manual dengan full integration untuk melihat element buku teks. Laporkan yang mana anda gunakan; jangan sembunyikan perbezaan itu — menerangkannya ialah tujuannya.")
        + H3("The mesh study (Activity 3)", "Kajian mesh (Aktiviti 3)")
        + P("The course solvers give the numbers a correct quadratic (PLANE183) study should come within about 1% of. Dofs are twice the nodes in plane stress; Mesh → Statistics shows the nodes.",
            "Solver kursus memberi nombor yang patut dihampiri dalam lingkungan kira-kira 1% oleh kajian quadratic (PLANE183) yang betul. Dof ialah dua kali bilangan node dalam plane stress; Mesh → Statistics menunjukkan bilangan node.")
        + _tbl([B("Quadratic mesh", "Mesh quadratic"), B("Nodes", "Node"), B("Dofs", "Dof"), "v<sub>tip</sub> (m)", B("Change from previous", "Perubahan dari sebelumnya"), "R<sub>y</sub> (N)"],
               [["2 × 1", "13", "26", "−0.1780", "—", "+10 000"], ["4 × 2", "37", "74", "−0.1885", "5.57%", "+10 000"], ["8 × 4", "121", "242", "−0.1906", "1.12%", "+10 000"], ["16 × 8", "433", "866", "−0.1913", "0.35%", "+10 000"]])
        + A.eq("p6_change")
        + P("Linear elements on the same meshes: 0.1306 (2 × 2), 0.1643 (4 × 2), 0.1824 (8 × 4), 0.1886 (16 × 8) m — the linear 8 × 4 is 4.3% stiffer than the quadratic 8 × 4, and the linear element needs 16 × 8 to come within 2% of beam theory. The independent check is Timoshenko:",
            "Linear element pada mesh yang sama: 0.1306 (2 × 2), 0.1643 (4 × 2), 0.1824 (8 × 4), 0.1886 (16 × 8) m — linear 8 × 4 4.3% lebih kaku daripada quadratic 8 × 4, dan linear element memerlukan 16 × 8 untuk berada dalam 2% daripada beam theory. Semakan bebasnya ialah Timoshenko:")
        + A.eq("p6_timo")
        + OK("Which mesh to report", "Mesh mana yang dilaporkan",
             "Report the first mesh after which the change falls below your tolerance. At 1%: the 8 × 4 quadratic mesh, because the next refinement changed the deflection by only 0.35%; it is 0.7% below Timoshenko, the 16 × 8 0.35% below. Say it in one sentence with both numbers.",
             "Laporkan mesh pertama yang selepasnya perubahan jatuh di bawah toleransi anda. Pada 1%: mesh quadratic 8 × 4, kerana refine seterusnya hanya mengubah deflection sebanyak 0.35%; ia 0.7% di bawah Timoshenko, dan 16 × 8 0.35% di bawah. Nyatakan dalam satu ayat dengan kedua-dua nombor.")
        + SB(P("The reaction column never changes: equilibrium holds exactly for every mesh, because the struck rows of [K]{U} − {R} balance the applied loads whatever the displacements. A reaction checks the loads and the supports; it says nothing about accuracy.",
               "Lajur reaction tidak pernah berubah: keseimbangan tepat bagi setiap mesh, kerana baris yang dibuang [K]{U} − {R} mengimbangi load yang dikenakan tanpa mengira displacement. Reaction menyemak load dan support; ia tidak memberitahu apa-apa tentang ketepatan."))
        + TRY("book22 study")
        + KP([("Linear 2 × 2 = the hand calculation (0.1306 m) when the element is the textbook Q4; quadratic 2 × 1 already gives 0.1780 m.", "Linear 2 × 2 = pengiraan tangan (0.1306 m) apabila element ialah Q4 buku teks; quadratic 2 × 1 sudah memberi 0.1780 m."),
              ("Quadratic study: changes 5.57%, 1.12%, 0.35%; report 8 × 4 or finer; Timoshenko 0.1919 m.", "Kajian quadratic: perubahan 5.57%, 1.12%, 0.35%; laporkan 8 × 4 atau lebih halus; Timoshenko 0.1919 m."),
              ("R<sub>y</sub> = +10 000 N and M = 40 000 N m on every mesh: the first number to read.", "R<sub>y</sub> = +10 000 N dan M = 40 000 N m pada setiap mesh: nombor pertama yang dibaca.")])
        + QC("q3", "A group’s quadratic study gives tip deflections whose changes are 5.6%, 1.1% and 0.35% (meshes 4 × 2, 8 × 4, 16 × 8). With a 1% tolerance they should report", "Kajian quadratic satu kumpulan memberi perubahan tip deflection 5.6%, 1.1% dan 0.35% (mesh 4 × 2, 8 × 4, 16 × 8). Dengan toleransi 1% mereka patut melaporkan",
             [("a", "the 4 × 2 mesh, because the change from 2 × 1 is the largest", "mesh 4 × 2, kerana perubahan dari 2 × 1 paling besar"), ("b", "the 8 × 4 mesh (or finer): the next refinement changed it by 0.35%", "mesh 8 × 4 (atau lebih halus): refine seterusnya mengubahnya sebanyak 0.35%"), ("c", "only a mesh with zero change", "hanya mesh dengan perubahan sifar")],
             "b", "The change attached to a mesh tells how much that refinement moved the result. After 8 × 4 the next step moved it 0.35%, below 1%, so 8 × 4 is converged to the tolerance; reporting 16 × 8 is also fine. A zero change never comes: each halving only shrinks the error.",
             "Perubahan yang dilekatkan pada sesuatu mesh menunjukkan sejauh mana refine itu menggerakkan keputusan. Selepas 8 × 4 langkah seterusnya menggerakkannya 0.35%, di bawah 1%, jadi 8 × 4 sudah converge mengikut toleransi; melaporkan 16 × 8 juga boleh. Perubahan sifar tidak akan berlaku: setiap pembahagian dua hanya mengecilkan ralat.")
    )
    S.append(("n3", "Demo 2 · the cantilever and the mesh study", "Demo 2 · cantilever dan kajian mesh", body))

    # ---- n4: stresses on screen and four wrong models ----
    body = (
        P("A stress contour is the most persuasive and the least reliable picture Mechanical draws. Three questions from Plane Stress Part 3 decide what it means: what is being averaged, where the maximum sits, and whether that maximum converges.",
          "Contour stress ialah gambar yang paling meyakinkan tetapi paling kurang boleh dipercayai yang dilukis oleh Mechanical. Tiga soalan daripada Plane Stress Part 3 menentukan maknanya: apa yang dipuratakan, di mana maksimum berada, dan sama ada maksimum itu converge.")
        + _tbl([B("Result object", "Objek keputusan"), "Display Option", B("Textbook meaning", "Makna dalam buku teks"), B("Use it for", "Gunakan untuk")],
               [["Normal Stress (X Axis)", "Averaged", B("nodal average of the element values", "purata nodal bagi nilai element"), B("contour plots away from boundaries", "contour plot jauh dari sempadan")],
                ["Normal Stress (X Axis)", "Unaveraged", B("each element’s own values at its nodes", "nilai setiap element sendiri pada node-nya"), B("seeing how rough the mesh still is", "melihat betapa kasarnya mesh lagi")],
                ["Normal Stress (X Axis)", "Elemental Mean", B("the centroid value", "nilai centroid"), B("the number to compare with M(y − H/2)/I", "nombor untuk dibandingkan dengan M(y − H/2)/I")],
                ["Equivalent (von Mises)", B("any", "mana-mana"), "σ<sub>vM</sub>", B("steel yield check", "semakan alah keluli")],
                ["Maximum Principal", B("any", "mana-mana"), "σ<sub>1</sub>", B("concrete cracking, direction of reinforcement", "keretakan konkrit, arah tetulang")],
                ["Stress probe", "—", B("[E][B]{û} at a chosen point", "[E][B]{û} pada titik yang dipilih"), B("a checkable number", "nombor yang boleh disemak")]])
        + NOTE("The Max tag of this cantilever", "Tag Max cantilever ini",
               "Every stress plot of the cantilever puts its Max tag at the fixed corner. That is the singularity of Plane Stress Part 3: it rises with every refinement and is not a design stress. Read stresses where they converge.",
               "Setiap plot stress cantilever meletakkan tag Max di bucu tetap. Itulah singularity Plane Stress Part 3: ia naik dengan setiap refine dan bukan design stress. Baca stress di tempat ia converge.")
        + STEP("Worked check · the bending stress at mid-span", "Semakan bekerja · bending stress di tengah rentang",
               A.eq("p6_beam_mid")
               + P("The course Q8 16 × 8 solution gives 1500.3 kN m<sup>−2</sup> at (2, 1.5), and 1757.8 at the centroid (2.125, 1.625) of the element above it, where beam theory also gives 1757.8. The Q4 16 × 8 mesh shows why Elemental Mean is the honest display for a linear element: its centroid value, 1744, is 0.8% low, but the stress its element evaluates at the corner node (2, 1.5) is 1338 — 10.8% low.",
                   "Penyelesaian Q8 16 × 8 kursus memberi 1500.3 kN m<sup>−2</sup> pada (2, 1.5), dan 1757.8 pada centroid (2.125, 1.625) element di atasnya, di mana beam theory juga memberi 1757.8. Mesh Q4 16 × 8 menunjukkan mengapa Elemental Mean ialah paparan yang jujur bagi linear element: nilai centroid-nya, 1744, rendah 0.8%, tetapi stress yang dinilai element itu pada node bucu (2, 1.5) ialah 1338 — rendah 10.8%."))
        + H3("Four wrong models, each a one-field change (Activity 4)", "Empat model yang salah, setiap satu perubahan satu ruang (Aktiviti 4)")
        + A.fig("fig_wrong", "Four deliberately wrong versions of the cantilever: plane strain, a force on one vertex, a support that fixes only v, and a thickness left at a default.",
                "Empat versi cantilever yang sengaja salah: plane strain, daya pada satu bucu, support yang hanya menetapkan v, dan ketebalan dibiarkan pada nilai default.", 640)
        + _tbl([B("Mistake", "Kesilapan"), B("Signature (course Q8 32 × 16; correct tip 0.1915 m)", "Tanda (Q8 32 × 16 kursus; tip betul 0.1915 m)"), B("Why", "Mengapa")],
               [[B("(a) 2D Behavior: Plane Strain", "(a) 2D Behavior: Plane Strain"), B("tip 0.1722 m (−10.1%); a σ<sub>zz</sub> appears in the results", "tip 0.1722 m (−10.1%); σ<sub>zz</sub> muncul dalam keputusan"), B("stiffer [E]: ratio ≈ 1 − ν²", "[E] lebih kaku: nisbah ≈ 1 − ν²")],
                [B("(b) Force on the top-right vertex", "(b) Force pada bucu kanan atas"), B("loaded node 0.2298 m (+20%); mid-depth 0.1875 m (−0.7%); von Mises under the load ×10", "node dibebankan 0.2298 m (+20%); tengah kedalaman 0.1875 m (−0.7%); von Mises di bawah load ×10"), B("a point load is a singularity; St-Venant", "point load ialah singularity; St-Venant")],
                [B("(c) Displacement Y = 0 only", "(c) Displacement Y = 0 sahaja"), B("rigid-body warning; weak springs added; large x-displacement", "amaran rigid-body; weak springs ditambah; x-displacement besar"), B("nothing stops translation in x", "tiada yang menghalang translasi dalam x")],
                [B("(d) Thickness 1 m instead of 0.01 m", "(d) Thickness 1 m dan bukannya 0.01 m"), B("tip 0.001915 m: a clean factor of 100", "tip 0.001915 m: faktor 100 yang tepat"), "v ∝ 1/t"]])
        + A.eq("p6_strain_ratio") + A.eq("p6_thick")
        + OK("The reaction was right in all four", "Reaction betul dalam keempat-empatnya",
             "R<sub>y</sub> = +10 000 N in every wrong model (the thickness one included): equilibrium does not catch idealisation errors. A wrong reaction means an input error — load, unit, direction, a missing or doubled support. A right reaction with a wrong deflection means an idealisation error. Different fixes.",
             "R<sub>y</sub> = +10 000 N dalam setiap model yang salah (termasuk model ketebalan): keseimbangan tidak menangkap ralat idealisation. Reaction yang salah bermaksud ralat input — load, unit, arah, support yang tertinggal atau berganda. Reaction yang betul dengan deflection yang salah bermaksud ralat idealisation. Pembetulan yang berbeza.")
        + TRY("pstrain point vonly thick")
        + KP([("Elemental Mean = centroid value: compare it with M(y − H/2)/I; ignore the Max tag at the fixed corner.", "Elemental Mean = nilai centroid: bandingkan dengan M(y − H/2)/I; abaikan tag Max di bucu tetap."),
              ("Plane strain −10%; vertex force +20% at the node; v-only support: warning; thickness: a power of ten.", "Plane strain −10%; daya bucu +20% pada node; support v sahaja: amaran; ketebalan: kuasa sepuluh."),
              ("Wrong reaction → input error; right reaction, wrong result → idealisation error.", "Reaction salah → ralat input; reaction betul, keputusan salah → ralat idealisation.")])
        + QC("q4", "A run of the cantilever reads R<sub>y</sub> = +10 000 N and a tip deflection of 0.0019 m. What do you check first?", "Satu run cantilever menunjukkan R<sub>y</sub> = +10 000 N dan tip deflection 0.0019 m. Apa yang anda semak dahulu?",
             [("a", "the load: it must be a hundred times too small", "load: ia mesti seratus kali terlalu kecil"), ("b", "the thickness (and the unit system): the deflection is off by exactly 100", "ketebalan (dan unit system): deflection tersasar tepat 100 kali"), ("c", "the mesh: refine until it reaches 0.19 m", "mesh: refine sehingga mencapai 0.19 m")],
             "b", "The reaction is right, so the load and supports are right. A clean factor of 100 in a linear model points at a scaling input: t = 1 m instead of 0.01 m gives exactly 0.0019 m. Refinement never repairs an idealisation.",
             "Reaction betul, jadi load dan support betul. Faktor 100 yang tepat dalam model linear menunjukkan input penskalaan: t = 1 m dan bukannya 0.01 m memberi tepat 0.0019 m. Refine tidak pernah membaiki idealisation.")
    )
    S.append(("n4", "Stresses on screen, and four wrong models", "Stress pada skrin, dan empat model yang salah", body))

    # ---- n5: the project model, first verified run ----
    body = (
        P("The last block of the session is your own structure, from the model plan of Plane Stress Part 3. The aim is not a refined answer; it is a coarse model you can trust enough to refine. That takes eight checks, in this order, stopping at the first failure.",
          "Blok terakhir sesi ialah struktur anda sendiri, daripada pelan model Plane Stress Part 3. Tujuannya bukan jawapan yang halus; tujuannya model kasar yang cukup dipercayai untuk di-refine. Itu memerlukan lapan semakan, mengikut urutan ini, berhenti pada kegagalan pertama.")
        + OL([("<b>Units and 2D.</b> Metric (m, kg, N); Analysis Type 2D; plane stress or plane strain stated, with the reason.", "<b>Unit dan 2D.</b> Metric (m, kg, N); Analysis Type 2D; plane stress atau plane strain dinyatakan, bersama sebabnya."),
              ("<b>Geometry.</b> Dimensions checked against the sketch; thickness entered.", "<b>Geometri.</b> Dimensi disemak dengan lakaran; ketebalan dimasukkan."),
              ("<b>Material.</b> E and ν (or k) with units, and where they came from.", "<b>Bahan.</b> E dan ν (atau k) dengan unit, dan dari mana nilainya."),
              ("<b>Supports.</b> Only what is really restrained; nothing that is free is fixed.", "<b>Support.</b> Hanya yang benar-benar dikekang; tiada yang bebas ditetapkan."),
              ("<b>Loads.</b> Tractions on edges and body forces; no forces on single vertices.", "<b>Load.</b> Traction pada tepi dan body force; tiada daya pada satu bucu."),
              ("<b>Coarse mesh.</b> Quadratic, a few elements; it must solve.", "<b>Mesh kasar.</b> Quadratic, beberapa element; ia mesti dapat diselesaikan."),
              ("<b>Reaction.</b> Equal to the applied load, with the right sign.", "<b>Reaction.</b> Sama dengan load yang dikenakan, dengan tanda yang betul."),
              ("<b>Hand estimate.</b> A deflection or a stress within a factor of 2 — then, and only then, refine.", "<b>Anggaran tangan.</b> Deflection atau stress dalam faktor 2 — kemudian, dan hanya kemudian, refine.")])
        + NOTE("Steps 7 and 8 are the gate", "Langkah 7 dan 8 ialah pintunya",
               "A model that fails step 7 or 8 is not refined; it is fixed. Refinement never repairs an idealisation: it converges, very precisely, to the answer of the wrong model.",
               "Model yang gagal langkah 7 atau 8 tidak di-refine; ia dibaiki. Refine tidak pernah membaiki idealisation: ia converge, dengan sangat tepat, kepada jawapan model yang salah.")
        + STEP("What a verified result looks like · a plate with a hole", "Rupa keputusan yang disahkan · plat berlubang",
               P("Predicted before Solve: Peterson’s K<sub>t</sub> for a central hole with d/W = 0.3. Computed with a mesh refined at the hole (MAPDL example on the slides): 2.34.",
                 "Diramal sebelum Solve: K<sub>t</sub> Peterson bagi lubang tengah dengan d/W = 0.3. Dikira dengan mesh yang di-refine di lubang (contoh MAPDL dalam slides): 2.34.")
               + A.eq("wn_peterson")
               + P("Reported as: “K<sub>t</sub> = 2.34 against Peterson’s 2.35 (−0.4%), on a mesh whose last refinement changed it by less than 1%.” A hand-check number, a mesh that resolves the hot spot, and the comparison in one sentence: that is the standard for the project.",
                   "Dilaporkan sebagai: “K<sub>t</sub> = 2.34 against Peterson’s 2.35 (−0.4%), on a mesh whose last refinement changed it by less than 1%.” Satu nombor semakan tangan, mesh yang menyelesaikan hot spot, dan perbandingan dalam satu ayat: itulah piawai projek."))
        + LI([("<b>Common first-run problems:</b> geometry in mm; thickness not set; a point force on a vertex; a whole edge fixed where the structure sits on a bearing; no restraint in one in-plane direction (rigid-body warning).",
               "<b>Masalah biasa run pertama:</b> geometri dalam mm; ketebalan tidak ditetapkan; point force pada bucu; seluruh tepi ditetapkan sedangkan struktur duduk di atas bearing; tiada kekangan dalam satu arah dalam satah (amaran rigid-body)."),
              ("<b>Deliverable at the end of the lab:</b> a screenshot of the reaction probe and of the coarse-mesh result, with the hand estimate written on the model plan.",
               "<b>Hasil di akhir makmal:</b> tangkapan skrin probe reaction dan keputusan mesh kasar, dengan anggaran tangan ditulis pada pelan model.")])
        + KP([("Eight checks in order; stop at the first failure.", "Lapan semakan mengikut urutan; berhenti pada kegagalan pertama."),
              ("Reaction = load, and a hand estimate within a factor of 2, before any refinement.", "Reaction = load, dan anggaran tangan dalam faktor 2, sebelum sebarang refine."),
              ("Report: number, check, signed difference, convergence — one sentence.", "Laporan: nombor, semakan, perbezaan bertanda, convergence — satu ayat.")])
        + QC("q5", "Your coarse project model has the right reaction, but its deflection is 3.1 mm where your hand estimate is 0.9 mm. Next step?", "Model projek kasar anda mempunyai reaction yang betul, tetapi deflection-nya 3.1 mm sedangkan anggaran tangan anda 0.9 mm. Langkah seterusnya?",
             [("a", "refine the mesh until the deflection settles", "refine mesh sehingga deflection stabil"), ("b", "look for an idealisation or input error (supports, thickness, E, plane strain/stress) before refining", "cari ralat idealisation atau input (support, ketebalan, E, plane strain/stress) sebelum refine"), ("c", "report 3.1 mm, since the software is more accurate than a hand estimate", "laporkan 3.1 mm, kerana perisian lebih tepat daripada anggaran tangan")],
             "b", "A factor of 3.4 is outside the factor-of-2 gate. The reaction is right, so the loads are; the difference lies in stiffness or restraint — or in the hand estimate itself, which then needs fixing too. Refinement would converge to the same wrong model.",
             "Faktor 3.4 berada di luar pintu faktor 2. Reaction betul, jadi load betul; perbezaan terletak pada kekakuan atau kekangan — atau pada anggaran tangan itu sendiri, yang kemudiannya perlu dibaiki juga. Refine akan converge kepada model salah yang sama.")
    )
    S.append(("n5", "Your project model: the first verified run", "Model projek anda: run pertama yang disahkan", body))

    # ---- n6: verification, validation and the hybrid project ----
    stages = _tbl([B("Gate", "Gate"), B("What must be shown", "Apa yang mesti ditunjukkan"), B("What it proves — and what it does not", "Apa yang dibuktikan — dan apa yang tidak")],
                  [["0", B("Specification and validation plan, written before any code: the problem, the idealisation, the quantities of interest, the checks and their tolerances.", "Spesifikasi dan pelan validation, ditulis sebelum sebarang kod: masalah, idealisation, kuantiti yang dikehendaki, semakan dan toleransinya."),
                    B("That the group knows what “right” will mean. Nothing about the code yet.", "Bahawa kumpulan tahu apa maksud “betul”. Belum ada apa-apa tentang kod.")],
                   ["1", B("Core solver: one element against a hand calculation (an entry of [k]); the patch test, exact to round-off; ΣR equal to the physical load.", "Core solver: satu element berbanding pengiraan tangan (satu entri [k]); patch test, tepat hingga round-off; ΣR sama dengan load fizikal."),
                    B("Element, assembly, loads and supports are consistent. Not that bending is right (Example 4).", "Element, assembly, load dan support konsisten. Bukan bahawa bending betul (Contoh 4).")],
                   ["2", B("Verification against a known solution: convergence to Timoshenko (cantilever) or Kirsch (plate with a hole, K<sub>t</sub> → 3) with the observed order.", "Verification berbanding penyelesaian yang diketahui: convergence kepada Timoshenko (cantilever) atau Kirsch (plat berlubang, K<sub>t</sub> → 3) dengan observed order."),
                    B("The equations are solved right. Not that they are the right equations.", "Persamaan diselesaikan dengan betul. Bukan bahawa ia persamaan yang betul.")],
                   ["3", B("ANSYS cross-check on the project structure: same idealisation, comparable mesh; every difference above the tolerance explained (element formulation, load application, averaging).", "Semakan silang ANSYS pada struktur projek: idealisation yang sama, mesh yang setanding; setiap perbezaan melebihi toleransi diterangkan (formulasi element, cara load dikenakan, averaging)."),
                    B("Two independent implementations agree. Not that the model matches the real structure.", "Dua pelaksanaan bebas sepakat. Bukan bahawa model sepadan dengan struktur sebenar.")],
                   ["4", B("UI and deployment: the tool runs from the group’s GitHub repository (GitHub Pages), with a README that states what it verifies and its limits.", "UI dan deployment: alat berjalan dari repository GitHub kumpulan (GitHub Pages), dengan README yang menyatakan apa yang disahkan dan hadnya."),
                    B("Others can run and check the tool.", "Orang lain boleh menjalankan dan menyemak alat itu.")],
                   ["5", B("Individual viva and demonstration: each member runs a gate live and explains the code and the numbers behind it.", "Viva dan demonstrasi individu: setiap ahli menjalankan satu gate secara langsung dan menerangkan kod serta nombor di sebaliknya."),
                    B("The understanding is the student’s, not the AI’s.", "Kefahaman itu milik pelajar, bukan AI.")]])
    rubric = _tbl([B("Component", "Komponen"), B("Marks", "Markah")],
                  [[B("Verification and ANSYS cross-check (Gates 1–3)", "Verification dan semakan silang ANSYS (Gate 1–3)"), "35"], [B("Interpretation of the results for design", "Tafsiran keputusan untuk reka bentuk"), "20"],
                   [B("Individual viva and demonstration (Gate 5)", "Viva dan demonstrasi individu (Gate 5)"), "25"], [B("UI, deployment and repository (Gate 4)", "UI, deployment dan repository (Gate 4)"), "10"],
                   [B("GenAI log and reflection", "Log GenAI dan refleksi"), "10"], [B("<b>Total</b>", "<b>Jumlah</b>"), "<b>100</b>"]])
    body = (
        P("Two different questions hide behind “is the model right?”. Asking them separately is what turns a colour plot into evidence.",
          "Dua soalan yang berbeza tersembunyi di sebalik “betulkah model ini?”. Bertanya kedua-duanya secara berasingan itulah yang menukar contour plot kepada bukti.")
        + DEF("Verification — solving the equations right", "Verification — menyelesaikan persamaan dengan betul",
              "Does the computer solve the mathematical model correctly? Checked against things that are exact for that model: a hand calculation on one element, a patch test, convergence to a known analytical solution, equilibrium of the reactions, an independent second code.",
              "Adakah komputer menyelesaikan model matematik dengan betul? Disemak dengan perkara yang tepat bagi model itu: pengiraan tangan pada satu element, patch test, convergence kepada penyelesaian analitikal yang diketahui, keseimbangan reaction, kod kedua yang bebas.")
        + DEF("Validation — solving the right equations", "Validation — menyelesaikan persamaan yang betul",
              "Does the mathematical model represent the real structure — plane stress or not, linear elastic or not, these supports or others? Only measurements can answer it: a load test, strain gauges, monitoring data. Without them, say plainly what the model cannot tell you.",
              "Adakah model matematik mewakili struktur sebenar — plane stress atau tidak, linear elastic atau tidak, support ini atau yang lain? Hanya pengukuran boleh menjawabnya: ujian beban, strain gauge, data pemantauan. Tanpanya, nyatakan dengan jelas apa yang model tidak dapat beritahu.")
        + P("The two demonstrations of this session were verification: ANSYS against hand calculations and textbook solutions. Agreement there says the software solves the idealised plate correctly; it cannot say that the idealisation was right — the four wrong models solved their own equations perfectly.",
            "Dua demonstrasi sesi ini ialah verification: ANSYS berbanding pengiraan tangan dan penyelesaian buku teks. Persetujuan di situ menunjukkan perisian menyelesaikan plat yang diidealkan dengan betul; ia tidak boleh menunjukkan bahawa idealisation itu betul — empat model yang salah menyelesaikan persamaan masing-masing dengan sempurna.")
        + H3("The hybrid project: ANSYS first, your own tool as the independent check", "Projek hibrid: ANSYS dahulu, alat anda sendiri sebagai semakan bebas")
        + P("In the project, ANSYS is the primary analysis. Each group also builds a small solver of its own — written with generative AI if you wish (“vibe coding”), deployed on GitHub — as an independent check of the ANSYS model. Two implementations that agree are stronger evidence than either alone; when they disagree, the difference is explained, never averaged away. "
            "The tool is only trusted after it passes the stage gates below, in order.",
            "Dalam projek, ANSYS ialah analisis utama. Setiap kumpulan juga membina solver kecil sendiri — ditulis dengan generative AI jika mahu (“vibe coding”), di-deploy di GitHub — sebagai semakan bebas bagi model ANSYS. Dua pelaksanaan yang sepakat ialah bukti yang lebih kuat daripada salah satunya sahaja; apabila tidak sepakat, perbezaannya diterangkan, tidak sekali-kali dipuratakan. "
            "Alat itu hanya dipercayai selepas melepasi stage gate di bawah, mengikut urutan.")
        + stages
        + NOTE("What the gates catch (Example 4)", "Apa yang ditangkap oleh gate (Contoh 4)",
               "A load bug that gives every edge node σ<sub>0</sub>tb instead of σ<sub>0</sub>tb/2 still balances its own load vector: ΣR must be compared with the <i>physical</i> load, σ<sub>0</sub>tH. A shear-modulus bug (Ē instead of Ē(1 − ν)/2) passes a tension patch test exactly, because the shear strain is zero there, and is caught only at Gate 2: the Q8 16 × 8 cantilever tip becomes 0.1696 m, 11.6% below Timoshenko.",
               "Pepijat load yang memberi setiap node tepi σ<sub>0</sub>tb dan bukannya σ<sub>0</sub>tb/2 masih mengimbangi vektor load-nya sendiri: ΣR mesti dibandingkan dengan load <i>fizikal</i>, σ<sub>0</sub>tH. Pepijat shear modulus (Ē dan bukannya Ē(1 − ν)/2) melepasi patch test tegangan dengan tepat, kerana shear strain sifar di situ, dan hanya ditangkap di Gate 2: tip cantilever Q8 16 × 8 menjadi 0.1696 m, 11.6% di bawah Timoshenko.")
        + H3("How the project is marked", "Bagaimana projek dinilai")
        + rubric
        + LI([("<b>GenAI log.</b> Keep the prompts, what you accepted and rejected, and which gate caught which AI error. The reflection says what you would check differently next time.",
               "<b>Log GenAI.</b> Simpan prompt, apa yang diterima dan ditolak, dan gate mana yang menangkap ralat AI yang mana. Refleksi menyatakan apa yang akan anda semak secara berbeza lain kali."),
              ("<b>Every line is yours to explain.</b> The viva asks each member to run a gate and explain the code behind it; a tool nobody in the group can explain earns no verification marks.",
               "<b>Setiap baris mesti boleh anda terangkan.</b> Viva meminta setiap ahli menjalankan satu gate dan menerangkan kod di sebaliknya; alat yang tiada ahli kumpulan boleh terangkan tidak mendapat markah verification.")])
        + SB(P("The brief, the group arrangement, the weight in the course and the dates are in Part 5, Notes §6, and are announced by the lecturer; this section adds the verification side.",
               "Taklimat, susunan kumpulan, wajaran dalam kursus dan tarikh ada dalam Part 5, Nota §6, dan diumumkan oleh pensyarah; bahagian ini menambah sisi verification."))
        + A.eq("p6_predict")
        + KP([("Verification: the equations solved right (hand check, patch test, convergence, a second code). Validation: the right equations (measurements).", "Verification: persamaan diselesaikan dengan betul (semakan tangan, patch test, convergence, kod kedua). Validation: persamaan yang betul (pengukuran)."),
              ("Gates 0–5: plan → core solver → known solution → ANSYS cross-check → deploy → viva. In order; no skipping.", "Gate 0–5: pelan → core solver → penyelesaian diketahui → semakan silang ANSYS → deploy → viva. Mengikut urutan; tiada lompatan."),
              ("Marks: 35 verification and cross-check · 20 interpretation · 25 viva and demo · 10 UI, deploy, repository · 10 GenAI log and reflection.", "Markah: 35 verification dan semakan silang · 20 tafsiran · 25 viva dan demo · 10 UI, deploy, repository · 10 log GenAI dan refleksi.")])
        + QC("q6", "Your group’s solver reproduces the tension patch test to 10<sup>−17</sup> m. Can you conclude that it is correct?", "Solver kumpulan anda menghasilkan semula patch test tegangan hingga 10<sup>−17</sup> m. Bolehkah anda simpulkan bahawa ia betul?",
             [("a", "yes: an exact patch test proves the element", "ya: patch test yang tepat membuktikan element itu"), ("b", "no: it proves consistency for that stress state only; a wrong shear term passes it, so Gate 2 (bending against Timoshenko) is still needed", "tidak: ia membuktikan konsistensi bagi keadaan stress itu sahaja; term shear yang salah melepasinya, jadi Gate 2 (bending berbanding Timoshenko) masih diperlukan"), ("c", "yes, if ANSYS gives the same displacement", "ya, jika ANSYS memberi displacement yang sama")],
             "b", "In uniform tension σ<sub>xy</sub> = 0, so the shear row of [E] is never exercised: with Ē in place of Ē(1 − ν)/2 the patch is still exact, while the cantilever comes out 11.6% stiff. Each gate proves something specific; together they build the case. ANSYS would agree on the patch too — for the same reason.",
             "Dalam tegangan seragam σ<sub>xy</sub> = 0, jadi baris shear [E] tidak pernah diuji: dengan Ē menggantikan Ē(1 − ν)/2 patch masih tepat, manakala cantilever menjadi 11.6% terlalu kaku. Setiap gate membuktikan sesuatu yang khusus; bersama-sama ia membina hujah. ANSYS juga akan sepakat pada patch itu — atas sebab yang sama.")
    )
    S.append(("n6", "Verification, validation and the hybrid project", "Verification, validation dan projek hibrid", body))

    # ---- n7: Workbench how-to (menu names checked against the Ansys Help, release 2026 R1, 24 Nov 2026) ----
    curves = _tbl([B("You mean", "Maksud anda"), B("Where", "Di mana"), B("Step", "Langkah")],
                  [[B("a curved edge of the structure: an arc, a fillet, a hole, a spline", "tepi struktur yang melengkung: arc, fillet, lubang, spline"), B("Geometry: a DesignModeler sketch", "Geometry: sketch DesignModeler"), "2"],
                   [B("a load that varies along an edge, such as water pressure on a wall", "load yang berubah sepanjang tepi, seperti tekanan air pada dinding"), B("Mechanical: Pressure → Magnitude → Function", "Mechanical: Pressure → Magnitude → Function"), "4"],
                   [B("a result plotted along a line: σ<sub>x</sub> across the depth, T along an edge", "keputusan diplot sepanjang garisan: σ<sub>x</sub> merentasi kedalaman, T sepanjang tepi"), B("Mechanical: Construction Geometry → Path", "Mechanical: Construction Geometry → Path"), "5"],
                   [B("a convergence curve: one result against the mesh", "lengkung convergence: satu keputusan berbanding mesh"), B("your mesh-study table, plotted; or a Convergence object", "jadual kajian mesh anda, diplot; atau objek Convergence"), "5"]])
    errors = _tbl([B("What you see", "Apa yang anda lihat"), B("Usual cause", "Punca biasa"), B("What to do", "Apa perlu dibuat")],
                  [[B("no 2D Behavior or Thickness under Geometry in Mechanical", "tiada 2D Behavior atau Thickness di bawah Geometry dalam Mechanical"), B("Analysis Type left at 3D: the surface became a shell", "Analysis Type kekal 3D: permukaan menjadi shell"), B("set Analysis Type = 2D on the Geometry cell (Step 1) and check the setup again", "tetapkan Analysis Type = 2D pada sel Geometry (Langkah 1) dan semak semula setup")],
                   [B("Surfaces From Sketches gives an error or no surface", "Surfaces From Sketches memberi ralat atau tiada permukaan"), B("the sketch is not closed, or it crosses itself", "sketch tidak tertutup, atau bersilang dengan dirinya"), B("close the gap (Coincident constraint), Trim the crossing parts", "tutup ruang (constraint Coincident), Trim bahagian yang bersilang")],
                   [B("the model is rejected as not planar, or sits in the wrong plane", "model ditolak kerana tidak satah, atau berada pada satah yang salah"), B("the sketch was drawn on a plane other than XY", "sketch dilukis pada satah selain XY"), B("draw on XYPlane: 2D models must lie in the x-y plane", "lukis pada XYPlane: model 2D mesti terletak pada satah x-y")],
                   [B("a warning about rigid-body motion or weak springs", "amaran tentang rigid-body motion atau weak springs"), B("the supports do not stop every rigid motion", "support tidak menghalang setiap rigid motion"), B("§4, wrong model (c): fix the support, do not accept the springs", "§4, model salah (c): betulkan support, jangan terima springs itu")],
                   [B("displacements wrong by a factor of 10³ or 10⁶", "displacement salah dengan faktor 10³ atau 10⁶"), B("mixed units: geometry in mm, E in Pa", "unit bercampur: geometri dalam mm, E dalam Pa"), B("§1: one unit system, set first; predict before Solve", "§1: satu unit system, ditetapkan dahulu; ramal sebelum Solve")],
                   [B("Face Meshing shows a warning on a face with a hole", "Face Meshing menunjukkan amaran pada muka berlubang"), B("a mapped mesh needs a four-sided face", "mesh berpeta memerlukan muka empat sisi"), B("delete Face Meshing and keep the free quadrilateral mesh, or split the face into four-sided pieces", "padam Face Meshing dan kekalkan mesh segi empat bebas, atau pecahkan muka kepada bahagian empat sisi")],
                   [B("the solve stops at the problem-size limit of the licence", "solve berhenti pada had saiz masalah lesen"), B("ANSYS Student solves structural models up to 128K nodes or elements", "ANSYS Student menyelesaikan model struktur sehingga 128K node atau element"), B("refine locally (Edge Sizing at the hole), not the whole face", "refine secara setempat (Edge Sizing di lubang), bukan seluruh muka")],
                   [B("the maximum stress keeps rising with every refinement", "stress maksimum terus naik setiap kali refine"), B("a singular point: a re-entrant corner, a point load, a fixed corner", "titik singular: bucu masuk ke dalam, point load, bucu tetap"), B("Plane Stress Part 3: report the stress away from the point; do not chase it", "Plane Stress Part 3: laporkan stress jauh dari titik itu; jangan kejar")]])
    body = (
        P("The demonstrations use rectangles. Your project structure will not: it has arcs, holes and fillets, loads that vary along an edge, and results you want as a curve rather than a colour plot. "
          "This section collects those steps for ANSYS Student, the free version downloaded from the Ansys website, which includes Workbench, DesignModeler, Discovery and Mechanical. The menu names were checked against the Ansys Help for release 2026 R1; if a menu sits elsewhere in your version, the object and its name are the same.",
          "Demonstrasi menggunakan segi empat tepat. Struktur projek anda tidak begitu: ia ada arc, lubang dan fillet, load yang berubah sepanjang tepi, dan keputusan yang anda mahu sebagai lengkung, bukan contour plot. "
          "Bahagian ini menghimpunkan langkah-langkah itu untuk ANSYS Student, versi percuma yang dimuat turun dari laman web Ansys, yang mengandungi Workbench, DesignModeler, Discovery dan Mechanical. Nama menu telah disemak dengan Ansys Help bagi release 2026 R1; jika sesuatu menu berada di tempat lain dalam versi anda, objek dan namanya tetap sama.")
        + H3("“A curve in ANSYS”: four different things", "“Curve dalam ANSYS”: empat perkara berbeza")
        + P("Students ask “how do I draw a curve in ANSYS?” and mean one of four things. Decide which first; the steps are in different places.",
            "Pelajar bertanya “macam mana nak lukis curve dalam ANSYS?” dan maksudnya salah satu daripada empat perkara. Tentukan yang mana dahulu; langkahnya berada di tempat berbeza.")
        + curves
        + STEP("Step 1 · Open DesignModeler, not the default editor", "Langkah 1 · Buka DesignModeler, bukan editor lalai",
               OL([("Toolbox → <b>Static Structural</b> (or <b>Steady-State Thermal</b>), dragged onto the Project Schematic.", "Toolbox → <b>Static Structural</b> (atau <b>Steady-State Thermal</b>), diseret ke Project Schematic."),
                   ("Select the Geometry cell and, in its Properties, set <b>Analysis Type = 2D</b>. Do it now: it can be switched later, but switching may invalidate settings already made.", "Pilih sel Geometry dan, dalam Properties-nya, tetapkan <b>Analysis Type = 2D</b>. Buat sekarang: ia boleh ditukar kemudian, tetapi pertukaran itu mungkin membatalkan tetapan yang sudah dibuat."),
                   ("Right-click the Geometry cell → <b>New DesignModeler Geometry</b>. A double-click opens the default editor, which in recent releases is Discovery; Surfaces From Sketches and the steps below are DesignModeler’s.", "Klik kanan sel Geometry → <b>New DesignModeler Geometry</b>. Klik dua kali membuka editor lalai, iaitu Discovery dalam release terkini; Surfaces From Sketches dan langkah di bawah ialah langkah DesignModeler."),
                   ("In DesignModeler, choose the length unit (Units → Meter) before drawing, so that the dimensions match the numbers on this page.", "Dalam DesignModeler, pilih unit panjang (Units → Meter) sebelum melukis, supaya dimensi sepadan dengan nombor di halaman ini.")]))
        + STEP("Step 2 · Draw a curved outline, a hole or a fillet", "Langkah 2 · Lukis garis luar melengkung, lubang atau fillet",
               OL([("Tree Outline → select <b>XYPlane</b> → <b>New Sketch</b>; then the <b>Sketching</b> tab under the Tree Outline. <b>Look At</b> turns the view normal to the plane.", "Tree Outline → pilih <b>XYPlane</b> → <b>New Sketch</b>; kemudian tab <b>Sketching</b> di bawah Tree Outline. <b>Look At</b> memusingkan pandangan supaya normal kepada satah."),
                   ("<b>Draw</b> toolbox: Line or Polyline for straight edges; <b>Arc by Center</b> — click the centre, click the start point (it sets the radius), click the end point; <b>Arc by 3 Points</b> — click the start, the end, then a third point that sets the side and the radius; <b>Arc by Tangent</b> — an arc that leaves an edge tangentially; <b>Circle</b> for a hole; <b>Spline</b> — click at least three points, then right-click → Open End or Closed End.",
                    "Toolbox <b>Draw</b>: Line atau Polyline untuk tepi lurus; <b>Arc by Center</b> — klik pusat, klik titik mula (ia menetapkan jejari), klik titik akhir; <b>Arc by 3 Points</b> — klik titik mula, titik akhir, kemudian titik ketiga yang menetapkan arah dan jejari; <b>Arc by Tangent</b> — arc yang keluar dari satu tepi secara tangen; <b>Circle</b> untuk lubang; <b>Spline</b> — klik sekurang-kurangnya tiga titik, kemudian klik kanan → Open End atau Closed End."),
                   ("<b>Modify</b> toolbox: <b>Fillet</b> — type the radius in the Radius box beside the tool, then click the corner point or the two edges; right-click offers Trim Both, Trim 1st, Trim 2nd or Trim None. <b>Trim</b> removes the unwanted part of an edge where two curves cross.",
                    "Toolbox <b>Modify</b>: <b>Fillet</b> — taip jejari dalam kotak Radius di sebelah alat itu, kemudian klik titik bucu atau dua tepi; klik kanan memberi Trim Both, Trim 1st, Trim 2nd atau Trim None. <b>Trim</b> membuang bahagian tepi yang tidak dikehendaki di tempat dua lengkung bersilang."),
                   ("<b>Dimensions</b> toolbox: General, click an edge, type the value in the Details View. <b>Constraints</b> toolbox: Tangent, Concentric or Equal Radius when a shape must stay smooth or symmetric.", "Toolbox <b>Dimensions</b>: General, klik satu tepi, taip nilai dalam Details View. Toolbox <b>Constraints</b>: Tangent, Concentric atau Equal Radius apabila sesuatu bentuk mesti kekal licin atau simetri."),
                   ("<b>Modeling</b> tab → <b>Concept → Surfaces From Sketches</b> → select the sketch → Apply → <b>Generate</b>. The sketch must be closed and must not cross itself.", "Tab <b>Modeling</b> → <b>Concept → Surfaces From Sketches</b> → pilih sketch → Apply → <b>Generate</b>. Sketch mesti tertutup dan tidak bersilang dengan dirinya."),
                   ("A hole: draw the circle in the same sketch as the outer boundary; the inner loop becomes the hole. Look at the surface before going on — a filled circle means the loop was not recognised as a hole.", "Lubang: lukis bulatan dalam sketch yang sama dengan sempadan luar; gelung dalam menjadi lubang. Lihat permukaan itu sebelum meneruskan — bulatan yang penuh bermaksud gelung itu tidak dikenali sebagai lubang."),
                   ("A quarter model of a plate with a hole (Plane Stress Part 3): the two outer edges, the two cut edges and an Arc by Center at the corner; the symmetry conditions go on the cut edges in Step 4.", "Model suku bagi plat berlubang (Plane Stress Part 3): dua tepi luar, dua tepi potongan dan Arc by Center di bucu; keadaan simetri diletakkan pada tepi potongan dalam Langkah 4.")]))
        + STEP("Step 3 · Mesh a curved shape", "Langkah 3 · Mesh bentuk melengkung",
               OL([("Mesh → Details: <b>Element Order</b> Linear or Quadratic. Quadratic elements follow a curved edge with curved sides; linear ones replace it with straight segments, so a hole needs more of them.", "Mesh → Details: <b>Element Order</b> Linear atau Quadratic. Quadratic element mengikut tepi melengkung dengan sisi melengkung; linear element menggantikannya dengan segmen lurus, jadi lubang memerlukan lebih banyak element."),
                   ("Mesh → Insert → <b>Sizing</b>: on an edge, Type = Number of Divisions (the divisions round a hole set how well its stress peak is resolved); on the face, an Element Size.", "Mesh → Insert → <b>Sizing</b>: pada satu tepi, Type = Number of Divisions (bilangan bahagian di sekeliling lubang menentukan sejauh mana puncak stress-nya dapat dikira); pada muka, satu Element Size."),
                   ("Face Meshing (mapped) works on four-sided faces; on a face with a hole, keep the free quadrilateral mesh or split the face.", "Face Meshing (berpeta) berfungsi pada muka empat sisi; pada muka berlubang, kekalkan mesh segi empat bebas atau pecahkan muka itu."),
                   ("Generate, then read Mesh → Details → Statistics (nodes and elements). For the mesh study, change one sizing at a time and halve it each run.", "Generate, kemudian baca Mesh → Details → Statistics (node dan element). Untuk kajian mesh, ubah satu sizing pada satu masa dan bahagi duanya setiap run.")]))
        + STEP("Step 4 · Supports and loads, including a load that varies along an edge", "Langkah 4 · Support dan load, termasuk load yang berubah sepanjang tepi",
               OL([("Choose the Edge selection filter, select the edge(s), then Insert → Fixed Support, Displacement, Force or Pressure. A symmetry edge: Displacement with the normal component 0 and the other Free.", "Pilih Edge selection filter, pilih tepi, kemudian Insert → Fixed Support, Displacement, Force atau Pressure. Tepi simetri: Displacement dengan komponen normal 0 dan komponen lain Free."),
                   ("Pressure, Define By = Normal To: a positive value pushes into the edge (compression). In 2D a Pressure acts on edges.", "Pressure, Define By = Normal To: nilai positif menolak ke dalam tepi (mampatan). Dalam 2D, Pressure bertindak pada tepi."),
                   ("A varying load: Magnitude → <b>Function</b>, then an expression that starts with “=” and uses x or y (one variable only). Set the unit system first: the function keeps the units active when Function was chosen.", "Load yang berubah: Magnitude → <b>Function</b>, kemudian ungkapan yang bermula dengan “=” dan menggunakan x atau y (satu pemboleh ubah sahaja). Tetapkan unit system dahulu: fungsi itu mengekalkan unit yang aktif ketika Function dipilih.")])
               + P("Example · water 5 m deep against a wall whose base is at y = 0 (m, N): the pressure is γ<sub>w</sub>(5 − y), entered as <code>=9810*(5-y)</code> in Pa. Check after Solve: the horizontal reaction must equal ½ γ<sub>w</sub> H² t = ½ × 9810 × 5² × t = 122.6 kN per metre of thickness.",
                   "Contoh · air sedalam 5 m menolak dinding yang tapaknya pada y = 0 (m, N): tekanannya γ<sub>w</sub>(5 − y), dimasukkan sebagai <code>=9810*(5-y)</code> dalam Pa. Semak selepas Solve: reaction mendatar mesti sama dengan ½ γ<sub>w</sub> H² t = ½ × 9810 × 5² × t = 122.6 kN bagi setiap meter ketebalan."))
        + STEP("Step 5 · A result as a curve: probes, paths and convergence", "Langkah 5 · Keputusan sebagai lengkung: probe, path dan convergence",
               OL([("A value at a point: Solution → Insert → Probe (Deformation, or Force Reaction on a support).", "Nilai pada satu titik: Solution → Insert → Probe (Deformation, atau Force Reaction pada support)."),
                   ("A result along a line: Model → Insert → <b>Construction Geometry</b>, then add a <b>Path</b>. Path Type = <b>Two Points</b>: Start and End coordinates (x, y, 0) and the Number of Sampling Points (up to 200, evenly spaced); or Path Type = <b>Edge</b> to follow an edge, a curved one included (the edge of a hole).",
                    "Keputusan sepanjang garisan: Model → Insert → <b>Construction Geometry</b>, kemudian tambah <b>Path</b>. Path Type = <b>Two Points</b>: koordinat Start dan End (x, y, 0) dan Number of Sampling Points (sehingga 200, berjarak sama); atau Path Type = <b>Edge</b> untuk mengikut satu tepi, termasuk tepi melengkung (tepi lubang)."),
                   ("Insert the result (for example Stress → Normal, Orientation X), set <b>Scoping Method = Path</b>, choose the path, and evaluate. The graph and its table appear under the plot; right-click the result → Export writes a tab-delimited text file that opens in Excel.",
                    "Masukkan keputusan (contohnya Stress → Normal, Orientation X), tetapkan <b>Scoping Method = Path</b>, pilih path itu, dan evaluate. Graf dan jadualnya muncul di bawah plot; klik kanan keputusan → Export menulis fail teks tab-delimited yang boleh dibuka dalam Excel."),
                   ("A convergence curve: the course way is your own table of three or four meshes (§3), plotted against the number of elements. Mechanical can also refine for you: right-click a result → Insert → <b>Convergence</b>, set the Allowable Change (20% by default) and the Refinement Depth in the Solution details. Never converge on a singular point: its value grows without limit.",
                    "Lengkung convergence: cara kursus ialah jadual anda sendiri bagi tiga atau empat mesh (§3), diplot berbanding bilangan element. Mechanical juga boleh refine untuk anda: klik kanan satu keputusan → Insert → <b>Convergence</b>, tetapkan Allowable Change (20% secara lalai) dan Refinement Depth dalam details Solution. Jangan sekali-kali converge pada titik singular: nilainya bertambah tanpa had.")])
               + P("Example · σ<sub>x</sub> across the depth of the cantilever at x = 2 m: a Two Points path from (2, 0, 0) to (2, 2, 0) with 41 points, then Normal Stress X on that path. Beam theory predicts a straight line through zero at mid-depth: M = 20 kN·m, so σ<sub>x</sub> = M(y − 1)/I = 1500 kN m<sup>−2</sup> at y = 1.5 m (§4) and ±3000 kN m<sup>−2</sup> at the top and bottom faces. A kink or an offset in the graph is a modelling error to explain.",
                   "Contoh · σ<sub>x</sub> merentasi kedalaman cantilever pada x = 2 m: path Two Points dari (2, 0, 0) ke (2, 2, 0) dengan 41 titik, kemudian Normal Stress X pada path itu. Beam theory meramalkan garis lurus melalui sifar di tengah kedalaman: M = 20 kN·m, jadi σ<sub>x</sub> = M(y − 1)/I = 1500 kN m<sup>−2</sup> pada y = 1.5 m (§4) dan ±3000 kN m<sup>−2</sup> di permukaan atas dan bawah. Bengkok atau anjakan dalam graf ialah ralat pemodelan yang perlu diterangkan."))
        + H3("When it goes wrong", "Apabila berlaku masalah")
        + errors
        + NOTE("Check these against your own screen", "Semak semua ini dengan skrin anda sendiri",
               "Menus move between releases, and videos online often use another release or another geometry editor. When a step here and a video disagree, follow the object names here and check the result against a prediction, as in §2–§5; ask the lecturer when a menu named here cannot be found.",
               "Menu berubah tempat antara release, dan video dalam talian sering menggunakan release lain atau editor geometri lain. Apabila satu langkah di sini dan sebuah video tidak sepadan, ikut nama objek di sini dan semak keputusan dengan ramalan, seperti dalam §2–§5; tanya pensyarah apabila menu yang dinamakan di sini tidak dapat dijumpai.")
        + KP([("“Curve” means a curved edge (Geometry), a varying load (Function), a result along a line (Path) or a convergence curve (your table).", "“Curve” bermaksud tepi melengkung (Geometry), load yang berubah (Function), keputusan sepanjang garisan (Path) atau lengkung convergence (jadual anda)."),
              ("Analysis Type 2D first; right-click Geometry → New DesignModeler Geometry; sketch on XYPlane; Surfaces From Sketches needs a closed sketch.", "Analysis Type 2D dahulu; klik kanan Geometry → New DesignModeler Geometry; sketch pada XYPlane; Surfaces From Sketches memerlukan sketch tertutup."),
              ("Path: Construction Geometry → Path (Two Points or Edge), then the result with Scoping Method = Path; Export for Excel.", "Path: Construction Geometry → Path (Two Points atau Edge), kemudian keputusan dengan Scoping Method = Path; Export untuk Excel."),
              ("A varying pressure: Magnitude → Function, =9810*(5-y); check the reaction against ½ γ H² t.", "Tekanan yang berubah: Magnitude → Function, =9810*(5-y); semak reaction dengan ½ γ H² t.")])
        + QC("q7", "You need σ<sub>x</sub> across the depth of the cantilever at x = 2 m as a graph for your report. What do you add in Mechanical?", "Anda perlukan σ<sub>x</sub> merentasi kedalaman cantilever pada x = 2 m sebagai graf untuk laporan. Apa yang anda tambah dalam Mechanical?",
             [("a", "a Path from (2, 0, 0) to (2, 2, 0), then Normal Stress X with Scoping Method = Path", "Path dari (2, 0, 0) ke (2, 2, 0), kemudian Normal Stress X dengan Scoping Method = Path"),
              ("b", "a Probe at (2, 1, 0)", "Probe pada (2, 1, 0)"),
              ("c", "a finer mesh, then read the colours of the contour plot", "mesh yang lebih halus, kemudian baca warna contour plot")],
             "a", "A path samples the result at evenly spaced points along the line and gives the graph and its table, ready to export. A probe gives one value (here σ<sub>x</sub> ≈ 0 at mid-depth); colours give a range, not a curve.",
             "Path mengambil sampel keputusan pada titik berjarak sama sepanjang garisan dan memberi graf serta jadualnya, sedia untuk di-export. Probe memberi satu nilai (di sini σ<sub>x</sub> ≈ 0 di tengah kedalaman); warna memberi julat, bukan lengkung.")
    )
    S.append(("n7", "Workbench how-to: the steps students ask about", "Panduan Workbench: langkah yang sering ditanya pelajar", body))
    return S


RECALL = [
    QC("r1", "Recall · which display option shows one stress value per element, at its centroid?", "Ingat semula · pilihan paparan mana yang menunjukkan satu nilai stress setiap element, pada centroid-nya?",
       [("a", "Averaged", "Averaged"), ("b", "Elemental mean", "Elemental mean"), ("c", "Unaveraged", "Unaveraged")],
       "b", "Elemental mean is the centroid value of each element — the most accurate point of a linear element and the number to compare with beam theory. Today it is the Display Option you set in Mechanical.",
       "Elemental mean ialah nilai centroid setiap element — titik paling tepat bagi linear element dan nombor untuk dibandingkan dengan beam theory. Hari ini ia ialah Display Option yang anda tetapkan dalam Mechanical."),
    QC("r2", "Recall · the reactions of the 2 × 2 cantilever sum to 10 kN and 40 kN m. On a 32 × 16 mesh they sum to", "Ingat semula · reaction cantilever 2 × 2 berjumlah 10 kN dan 40 kN m. Pada mesh 32 × 16 jumlahnya ialah",
       [("a", "a little more, because the finer mesh is more flexible", "sedikit lebih, kerana mesh yang lebih halus lebih fleksibel"), ("b", "the same 10 kN and 40 kN m", "10 kN dan 40 kN m yang sama"), ("c", "it depends on the element type", "bergantung pada jenis element")],
       "b", "Equilibrium of the whole plate fixes the totals on any mesh and for any element; only their split among the support nodes changes. Today the reaction is the first number you read in ANSYS.",
       "Keseimbangan seluruh plat menetapkan jumlahnya pada sebarang mesh dan bagi sebarang element; hanya pembahagiannya antara node support yang berubah. Hari ini reaction ialah nombor pertama yang anda baca dalam ANSYS."),
]

QUICK = [
    MCQ("a1", "Which Workbench cell decides the shape functions of the analysis?", "Sel Workbench mana yang menentukan shape function analisis?",
        [("a", "Engineering Data", "Engineering Data"), ("b", "Mesh (element order and size)", "Mesh (element order dan saiz)"), ("c", "Setup", "Setup")], "b",
        "Element Order (Linear or Quadratic) picks the 4-node or 8-node shape functions, and the sizing picks a and b. Engineering Data is [E] or k; Setup holds the loads and the essential conditions.",
        "Element Order (Linear atau Quadratic) memilih shape function 4-node atau 8-node, dan sizing memilih a dan b. Engineering Data ialah [E] atau k; Setup memegang load dan essential condition."),
    MCQ("a2", "In Steady-State Thermal, an edge with no condition applied is", "Dalam Steady-State Thermal, tepi tanpa sebarang keadaan dikenakan ialah",
        [("a", "held at 0 °C", "dikekalkan pada 0 °C"), ("b", "insulated: q<sub>b</sub> = 0, the boundary integral vanishes", "insulated: q<sub>b</sub> = 0, boundary integral hilang"), ("c", "cooled by convection to the ambient temperature", "disejukkan oleh convection kepada suhu ambien")], "b",
        "The weak form carries the boundary flux as a natural condition; applying nothing sets it to zero, exactly as on the plate’s bottom and right edges in Heat Transfer Part 1. A temperature or a convection must be applied explicitly.",
        "Weak form membawa flux sempadan sebagai natural condition; tidak mengenakan apa-apa menetapkannya kepada sifar, sama seperti pada tepi bawah dan kanan plat dalam Heat Transfer Part 1. Suhu atau convection mesti dikenakan secara eksplisit."),
    MCQ("a3", "To reproduce the text’s 2 × 2 cantilever mesh (2 m × 1 m elements, hand value 0.1306 m) you set", "Untuk menghasilkan semula mesh cantilever 2 × 2 teks (element 2 m × 1 m, nilai tangan 0.1306 m) anda tetapkan",
        [("a", "Element Order Quadratic, Element Size 1 m", "Element Order Quadratic, Element Size 1 m"), ("b", "Element Order Linear, Edge Sizing 2 divisions on every edge", "Element Order Linear, Edge Sizing 2 bahagian pada setiap tepi"), ("c", "Element Order Linear, Element Size 1 m", "Element Order Linear, Element Size 1 m")], "b",
        "Two divisions on each edge give 2 m × 1 m elements; an Element Size of 1 m gives 4 × 2 square elements. Linear is the hand element. Even then, check Element Control: an enhanced-strain PLANE182 bends better than the textbook Q4.",
        "Dua bahagian pada setiap tepi memberi element 2 m × 1 m; Element Size 1 m memberi 4 × 2 element segi empat sama. Linear ialah element tangan. Walaupun begitu, semak Element Control: PLANE182 dengan enhanced strain melentur lebih baik daripada Q4 buku teks."),
    MCQ("a4", "The textbook cantilever in ANSYS shows a Force Reaction of +20 000 N in Y. The most likely cause is", "Cantilever buku teks dalam ANSYS menunjukkan Force Reaction +20 000 N dalam Y. Punca yang paling mungkin ialah",
        [("a", "the mesh is too coarse", "mesh terlalu kasar"), ("b", "the load input: entered twice, on two edges, or with the wrong length", "input load: dimasukkan dua kali, pada dua tepi, atau dengan panjang yang salah"), ("c", "plane strain was chosen instead of plane stress", "plane strain dipilih dan bukannya plane stress")], "b",
        "The reactions balance the applied loads on every mesh and for every idealisation, so a wrong reaction can only come from the loads or the supports. Plane strain changes the deflection by −10%, not the reaction.",
        "Reaction mengimbangi load yang dikenakan pada setiap mesh dan bagi setiap idealisation, jadi reaction yang salah hanya boleh datang daripada load atau support. Plane strain mengubah deflection sebanyak −10%, bukan reaction."),
    MCQ("a5", "Refining the cantilever from 16 × 8 to 32 × 16 (quadratic) changes the tip deflection by 0.14% but raises the maximum von Mises stress from 7937 to 9358 kN m<sup>−2</sup> (+18%). Which statement is right?", "Refine cantilever dari 16 × 8 ke 32 × 16 (quadratic) mengubah tip deflection sebanyak 0.14% tetapi menaikkan von Mises maksimum dari 7937 ke 9358 kN m<sup>−2</sup> (+18%). Pernyataan mana yang betul?",
        [("a", "the mesh is not converged: refine again until the maximum stops rising", "mesh belum converge: refine lagi sehingga maksimum berhenti naik"), ("b", "the deflection has converged; the maximum sits at the fixed corner, a singularity, and is not reportable", "deflection sudah converge; maksimum berada di bucu tetap, satu singularity, dan tidak boleh dilaporkan"), ("c", "the software has an error", "perisian ada ralat")], "b",
        "A singular peak rises with every refinement and never settles, so “refine until it stops” never ends. Report the converged deflection and the stresses away from the corner, and model the support realistically if the corner matters.",
        "Puncak singular naik dengan setiap refine dan tidak pernah stabil, jadi “refine sehingga berhenti” tidak akan berakhir. Laporkan deflection yang converge dan stress jauh dari bucu, dan modelkan support secara realistik jika bucu itu penting."),
    MCQ("a6", "Comparing the FE deflection of a shear wall with a load test on the real wall is", "Membandingkan deflection FE sebuah shear wall dengan ujian beban pada dinding sebenar ialah",
        [("a", "verification", "verification"), ("b", "validation", "validation"), ("c", "a patch test", "patch test")], "b",
        "Validation asks whether the model represents reality, and only measurements on the real structure answer it. Verification compares the computer solution with things exact for the model: hand calculations, analytical solutions, a second code. A patch test is one verification check.",
        "Validation bertanya sama ada model mewakili realiti, dan hanya pengukuran pada struktur sebenar boleh menjawabnya. Verification membandingkan penyelesaian komputer dengan perkara yang tepat bagi model: pengiraan tangan, penyelesaian analitikal, kod kedua. Patch test ialah satu semakan verification."),
]

ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="4" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("A student writes the input sheet for the text’s cantilever (4 m × 2 m, t = 0.01 m, q<sub>y</sub> = −5 kN m<sup>−1</sup> on the right edge) before building it in Workbench. One line contains the slip. Which one?",
        "Seorang pelajar menulis helaian input bagi cantilever teks (4 m × 2 m, t = 0.01 m, q<sub>y</sub> = −5 kN m<sup>−1</sup> pada tepi kanan) sebelum membinanya dalam Workbench. Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>Unit system Metric (m, kg, N, s); Analysis Type 2D; 2D Behavior Plane Stress; Thickness 0.01 m.</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>Young’s Modulus 2 × 10⁸ Pa; Poisson’s Ratio 0.33.</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>Force on the right edge, components: Y = −5000 N m<sup>−1</sup> × 2 m = −10 000 N.</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>Expected Force Reaction Y = +10 000 N; expected Moment Reaction = 10 000 × 2 = 20 000 N m.</span></button>'
    + '<button type="button" data-k="5"><span class="ln">5</span><span>Edge Sizing 2 divisions on all four edges, Element Order Linear → 4 elements, 9 nodes.</span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 4: the lever arm of the end load about the support is the length, 4 m, not the depth: M = 10 000 × 4 = 40 000 N m. With 20 000 N m as the expectation, a correct run would look wrong — or a wrong one right. The check that catches it: the moment is P × L for a cantilever, the value the hand calculation of Plane Stress Part 2 gave.",
        "Baris 4: lengan momen load hujung terhadap support ialah panjang, 4 m, bukan kedalaman: M = 10 000 × 4 = 40 000 N m. Dengan 20 000 N m sebagai jangkaan, run yang betul akan kelihatan salah — atau yang salah kelihatan betul. Semakan yang menangkapnya: momen ialah P × L bagi cantilever, nilai yang diberi oleh pengiraan tangan Plane Stress Part 2.")
    + '</p></div>'
)

# parameterised calculation exercises
EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  /* b1: an edge traction converted for the ANSYS dialog: total Force, Pressure, consistent nodal force */
  EX.define("b1", {
    gen: function(r){ return {q:pick(r,[2,3,4,5,6,8,10,12,15]), H:pick(r,[0.5,0.8,1,1.2,1.5,2,2.5,3]), t:pick(r,[0.005,0.01,0.02,0.05,0.1,0.2]), n:pick(r,[2,3,4,5,8])}; },
    text: function(P){ return bi("A uniform load of <span class=\"num\">"+P.q+"</span> kN m<sup>−1</sup> (force per unit length of the edge, thickness included) acts on an edge of length H = <span class=\"num\">"+P.H+"</span> m of a plate of thickness t = <span class=\"num\">"+P.t+"</span> m. For the ANSYS dialog, find the total Force (kN, 3 decimals) and the Pressure (kPa, 1 decimal). Then, to check what the software does with it, find the consistent nodal force at an interior node of that edge when it is divided into <span class=\"num\">"+P.n+"</span> equal linear (4-node) element sides (kN, 3 decimals). Magnitudes only.",
                                   "Load seragam <span class=\"num\">"+P.q+"</span> kN m<sup>−1</sup> (daya per unit panjang tepi, termasuk ketebalan) bertindak pada tepi sepanjang H = <span class=\"num\">"+P.H+"</span> m bagi plat setebal t = <span class=\"num\">"+P.t+"</span> m. Untuk kotak dialog ANSYS, cari jumlah Force (kN, 3 tempat perpuluhan) dan Pressure (kPa, 1 tempat perpuluhan). Kemudian, untuk menyemak apa yang perisian lakukan dengannya, cari consistent nodal force pada node dalaman tepi itu apabila ia dibahagi kepada <span class=\"num\">"+P.n+"</span> sisi linear (4-node) element yang sama panjang (kN, 3 tempat perpuluhan). Magnitud sahaja."); },
    fields: [{id:"F", label:["Force","Force"], unit:"kN", fn:function(P){ return P.q*P.H; }, atol:0.002, rtol:0.001},
             {id:"p", label:["Pressure","Pressure"], unit:"kPa", fn:function(P){ return P.q/P.t; }, atol:0.06, rtol:0.001},
             {id:"fm", label:[bi("interior node","node dalaman"),bi("interior node","node dalaman")], unit:"kN", fn:function(P){ return P.q*P.H/P.n; }, atol:0.002, rtol:0.002}],
    hints: [function(P){ return bi("Force = q × H. Pressure is force per unit area of the edge face, (q × H)/(H × t) = q/t: kN m<sup>−2</sup> = kPa. Check: Pressure × H × t gives the Force back.",
                                   "Force = q × H. Pressure ialah daya per unit luas muka tepi, (q × H)/(H × t) = q/t: kN m<sup>−2</sup> = kPa. Semak: Pressure × H × t memberi semula Force."); },
            function(P){ return bi("Each side of length h = H/"+P.n+" = "+fmt(P.H/P.n,4)+" m gives qh/2 to each of its two nodes (text (3.45)); an interior node belongs to two sides.",
                                   "Setiap sisi sepanjang h = H/"+P.n+" = "+fmt(P.H/P.n,4)+" m memberi qh/2 kepada setiap satu daripada dua node-nya (teks (3.45)); node dalaman dimiliki dua sisi."); }],
    solution: function(P){ var F=P.q*P.H, h=P.H/P.n;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">Force = "+P.q+" × "+P.H+" = "+fmt(F,3)+" kN<br>Pressure = "+P.q+"/"+P.t+" = "+fmt(P.q/P.t,1)+" kPa ("+bi("check","semak")+": "+fmt(P.q/P.t,1)+" × "+P.H+" × "+P.t+" = "+fmt(F,3)+" kN)<br>h = "+P.H+"/"+P.n+" = "+fmt(h,4)+" m; "+bi("end node","node hujung")+" qh/2 = "+fmt(P.q*h/2,3)+" kN; "+bi("interior node","node dalaman")+" 2 × qh/2 = qh = "+fmt(P.q*h,3)+" kN<br>"+bi("Sum","Jumlah")+": 2 × "+fmt(P.q*h/2,3)+" + "+(P.n-1)+" × "+fmt(P.q*h,3)+" = "+fmt(F,3)+" kN</p>"; }
  });
  /* b2: the change between meshes, the observed order and the extrapolated value from three halvings */
  function rich(P){ var d1=P.q[1]-P.q[0], d2=P.q[2]-P.q[1], r=d1/d2, Q=P.q[2]+d2/(r-1); return {chg:d2/P.q[2]*100, r:r, p:Math.log(r)/Math.log(2), Q:Q}; }
  EX.define("b2", {
    gen: function(r){ var Qi=pick(r,[12.5,18,24,35,48,60]), p=pick(r,[1.5,2,2.5,3]), C=pick(r,[0.08,0.12,0.18,0.25]);
      var q=[1,0.5,0.25].map(function(h){ return Math.round(Qi*(1-C*Math.pow(h,p))*1000)/1000; }); return {q:q}; },
    text: function(P){ return bi("Three quadratic meshes in ANSYS, each with half the element size of the previous one, give tip deflections of "+P.q.map(function(v){return "<span class=\"num\">"+v.toFixed(3)+"</span>";}).join(", ")+" mm. Find the change produced by the last refinement (%, of the finest value), the ratio of successive changes (= 2<sup>p</sup>), the observed order p, and the extrapolated deflection. Change and ratio and p to 2 decimals, the deflection to 3 decimals.",
                                   "Tiga mesh quadratic dalam ANSYS, setiap satu dengan saiz element separuh daripada sebelumnya, memberi tip deflection "+P.q.map(function(v){return "<span class=\"num\">"+v.toFixed(3)+"</span>";}).join(", ")+" mm. Cari perubahan yang dihasilkan oleh refine terakhir (%, daripada nilai paling halus), nisbah perubahan berturut-turut (= 2<sup>p</sup>), observed order p, dan deflection yang diekstrapolasi. Perubahan, nisbah dan p kepada 2 tempat perpuluhan, deflection kepada 3 tempat perpuluhan."); },
    fields: [{id:"c", label:[bi("change","perubahan"),bi("change","perubahan")], unit:"%", fn:function(P){ return rich(P).chg; }, atol:0.01, rtol:0.003},
             {id:"r", label:["2<sup>p</sup>","2<sup>p</sup>"], fn:function(P){ return rich(P).r; }, atol:0.02, rtol:0.004},
             {id:"p", label:["p","p"], fn:function(P){ return rich(P).p; }, atol:0.02, rtol:0},
             {id:"q", label:[bi("extrapolated","diekstrapolasi"),bi("extrapolated","diekstrapolasi")], unit:"mm", fn:function(P){ return rich(P).Q; }, atol:0.003, rtol:0.0002}],
    hints: [function(P){ return bi("Change = (v<sub>fine</sub> − v<sub>coarse</sub>)/v<sub>fine</sub> × 100% for the last two meshes. FEM by Hand (10.1): 2<sup>p</sup> ≈ (Q<sub>h</sub> − Q<sub>h/2</sub>)/(Q<sub>h/2</sub> − Q<sub>h/4</sub>); Q ≈ Q<sub>h/4</sub> + (Q<sub>h/4</sub> − Q<sub>h/2</sub>)/(2<sup>p</sup> − 1).",
                                   "Perubahan = (v<sub>fine</sub> − v<sub>coarse</sub>)/v<sub>fine</sub> × 100% bagi dua mesh terakhir. FEM by Hand (10.1): 2<sup>p</sup> ≈ (Q<sub>h</sub> − Q<sub>h/2</sub>)/(Q<sub>h/2</sub> − Q<sub>h/4</sub>); Q ≈ Q<sub>h/4</sub> + (Q<sub>h/4</sub> − Q<sub>h/2</sub>)/(2<sup>p</sup> − 1)."); },
            function(P){ return bi("Changes: Δ<sub>1</sub> = "+fmt(P.q[1]-P.q[0],3)+", Δ<sub>2</sub> = "+fmt(P.q[2]-P.q[1],3)+" mm. p = ln(2<sup>p</sup>)/ln 2; a smooth problem with quadratic elements gives p near 2 or above, a singular corner less.",
                                   "Perubahan: Δ<sub>1</sub> = "+fmt(P.q[1]-P.q[0],3)+", Δ<sub>2</sub> = "+fmt(P.q[2]-P.q[1],3)+" mm. p = ln(2<sup>p</sup>)/ln 2; masalah licin dengan quadratic element memberi p sekitar 2 atau lebih, bucu singular kurang."); }],
    solution: function(P){ var s=rich(P);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">"+bi("change","perubahan")+" = ("+P.q[2].toFixed(3)+" − "+P.q[1].toFixed(3)+")/"+P.q[2].toFixed(3)+" × 100 = "+fmt(s.chg,2)+"%<br>Δ<sub>1</sub> = "+fmt(P.q[1]-P.q[0],3)+"; Δ<sub>2</sub> = "+fmt(P.q[2]-P.q[1],3)+"<br>2<sup>p</sup> ≈ "+fmt(P.q[1]-P.q[0],3)+"/"+fmt(P.q[2]-P.q[1],3)+" = "+fmt(s.r,2)+"; p = ln "+fmt(s.r,3)+"/ln 2 = "+fmt(s.p,2)+"<br>Q ≈ "+P.q[2].toFixed(3)+" + "+fmt(P.q[2]-P.q[1],3)+"/("+fmt(s.r,3)+" − 1) = "+fmt(s.Q,3)+" mm</p>"; }
  });
  /* b3: the reaction and the independent check of a cantilever run: R, M, Timoshenko, signed difference */
  function timo(P){ var Pl=P.q*P.H, I=P.t*Math.pow(P.H,3)/12, A=P.t*P.H, G=P.E/(2*(1+P.nu)); return {P:Pl, I:I, A:A, G:G, vb:Pl*Math.pow(P.L,3)/(3*P.E*I), vs:Pl*P.L/(5/6*G*A)}; }
  function b3v(P){ var T=timo(P), vt=(T.vb+T.vs)*1000; return {R:T.P/1000, M:T.P*P.L/1000, vt:vt, e:(P.fe-vt)/vt*100}; }
  EX.define("b3", {
    gen: function(r){ var P; for (var k=0;k<50;k++){ P={L:pick(r,[3,4,5,6]), H:pick(r,[0.8,1,1.5,2]), t:pick(r,[0.01,0.02,0.05]), E:pick(r,[200e6,500e6,1e9]), nu:pick(r,[0.25,0.3,0.33]), q:pick(r,[2000,4000,5000,8000])};
        if (P.L/P.H < 2) continue; var T=timo(P), vt=(T.vb+T.vs)*1000; if (vt < 2 || vt > 900) continue;
        P.fe=Math.round(vt*(1+pick(r,[-0.06,-0.04,-0.025,-0.015,-0.008,-0.004]))*1000)/1000; return P; }
      return P; },
    text: function(P){ return bi("A cantilever L = <span class=\"num\">"+P.L+"</span> m long, H = <span class=\"num\">"+P.H+"</span> m deep and t = <span class=\"num\">"+P.t+"</span> m thick (E = <span class=\"num\">"+fmt(P.E/1e6,0)+"</span> × 10⁶ N m<sup>−2</sup>, ν = <span class=\"num\">"+P.nu+"</span>, plane stress) is fixed at one end and carries a uniform downward traction of <span class=\"num\">"+P.q+"</span> N m<sup>−1</sup> on its free end. A quadratic ANSYS model reports a tip deflection of <span class=\"num\">"+P.fe.toFixed(3)+"</span> mm. Before trusting it, find the Force Reaction (kN, 3 decimals) and the Moment Reaction about the support (kN m, 3 decimals) that the run must show, the Timoshenko tip deflection PL³/3EI + PL/κGA with κ = 5/6 (mm, 3 decimals), and the signed difference of the ANSYS value from it (%, 2 decimals).",
                                   "Sebuah cantilever sepanjang L = <span class=\"num\">"+P.L+"</span> m, dalam H = <span class=\"num\">"+P.H+"</span> m dan tebal t = <span class=\"num\">"+P.t+"</span> m (E = <span class=\"num\">"+fmt(P.E/1e6,0)+"</span> × 10⁶ N m<sup>−2</sup>, ν = <span class=\"num\">"+P.nu+"</span>, plane stress) ditetapkan pada satu hujung dan membawa traction seragam ke bawah <span class=\"num\">"+P.q+"</span> N m<sup>−1</sup> pada hujung bebasnya. Model ANSYS quadratic melaporkan tip deflection <span class=\"num\">"+P.fe.toFixed(3)+"</span> mm. Sebelum mempercayainya, cari Force Reaction (kN, 3 tempat perpuluhan) dan Moment Reaction terhadap support (kN m, 3 tempat perpuluhan) yang mesti ditunjukkan oleh run, tip deflection Timoshenko PL³/3EI + PL/κGA dengan κ = 5/6 (mm, 3 tempat perpuluhan), dan perbezaan bertanda nilai ANSYS daripadanya (%, 2 tempat perpuluhan)."); },
    fields: [{id:"R", label:["R<sub>y</sub>","R<sub>y</sub>"], unit:"kN", fn:function(P){ return b3v(P).R; }, atol:0.002, rtol:0.001},
             {id:"M", label:["M","M"], unit:"kN m", fn:function(P){ return b3v(P).M; }, atol:0.002, rtol:0.001},
             {id:"vt", label:["Timoshenko","Timoshenko"], unit:"mm", fn:function(P){ return b3v(P).vt; }, atol:0.003, rtol:0.003},
             {id:"e", label:[bi("difference","perbezaan"),bi("difference","perbezaan")], unit:"%", fn:function(P){ return b3v(P).e; }, atol:0.06, rtol:0.02}],
    hints: [function(P){ return bi("P = q × H; the reactions balance it: R<sub>y</sub> = P upward and M = P × L, on any mesh. I = tH³/12, A = tH, G = E/[2(1 + ν)].",
                                   "P = q × H; reaction mengimbanginya: R<sub>y</sub> = P ke atas dan M = P × L, pada sebarang mesh. I = tH³/12, A = tH, G = E/[2(1 + ν)]."); },
            function(P){ var T=timo(P); return bi("P = "+fmt(T.P,0)+" N, I = "+fmt(T.I*1e6,3)+" × 10<sup>−6</sup> m⁴, A = "+fmt(T.A,4)+" m², G = "+fmt(T.G/1e6,2)+" × 10⁶ N m<sup>−2</sup>. Difference = (ANSYS − Timoshenko)/Timoshenko × 100, negative when the model is stiffer.",
                                                  "P = "+fmt(T.P,0)+" N, I = "+fmt(T.I*1e6,3)+" × 10<sup>−6</sup> m⁴, A = "+fmt(T.A,4)+" m², G = "+fmt(T.G/1e6,2)+" × 10⁶ N m<sup>−2</sup>. Perbezaan = (ANSYS − Timoshenko)/Timoshenko × 100, negatif apabila model lebih kaku."); }],
    solution: function(P){ var T=timo(P), s=b3v(P);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">P = "+P.q+" × "+P.H+" = "+fmt(T.P,0)+" N → R<sub>y</sub> = "+fmt(s.R,3)+" kN; M = "+fmt(T.P,0)+" × "+P.L+" = "+fmt(s.M,3)+" kN m<br>I = "+P.t+" × "+P.H+"³/12 = "+fmt(T.I*1e6,3)+" × 10<sup>−6</sup> m⁴; A = "+fmt(T.A,4)+" m²; G = "+fmt(T.G/1e6,2)+" × 10⁶ N m<sup>−2</sup><br>"
        +bi("bending","bending")+" PL³/3EI = "+fmt(T.vb*1000,3)+" mm; "+bi("shear","shear")+" PL/κGA = "+fmt(T.vs*1000,3)+" mm; Timoshenko = "+fmt(s.vt,3)+" mm<br>"+bi("difference","perbezaan")+" = ("+P.fe.toFixed(3)+" − "+fmt(s.vt,3)+")/"+fmt(s.vt,3)+" × 100 = "+fmt(s.e,2)+"%</p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("An edge load for the ANSYS dialog, and what the software does with it", "Edge load untuk kotak dialog ANSYS, dan apa yang perisian lakukan dengannya"), 3),
    ("b2", ("Change between meshes, observed order and the extrapolated value", "Perubahan antara mesh, observed order dan nilai ekstrapolasi"), 4),
    ("b3", ("Reactions and the independent check of a cantilever run", "Reaction dan semakan bebas bagi run cantilever"), 5),
]

LAB_TASKS = [
    ("book22", ("Press “Text example” (4-node, 2 × 2): −0.1306 m is your prediction for the ANSYS run with Element Order Linear and Edge Sizing 2 and 2. Write it in the prediction column.",
                "Tekan “Text example” (4-node, 2 × 2): −0.1306 m ialah ramalan anda bagi run ANSYS dengan Element Order Linear dan Edge Sizing 2 dan 2. Tulis dalam lajur ramalan."),
     ("detected when the 4-node 2 × 2 mesh is solved with the text’s data", "dikesan apabila mesh 4-node 2 × 2 diselesaikan dengan data teks")),
    ("study", ("Run the mesh study (in class, from the QR on your phone). Read the 8-node 2 × 1 and 8 × 4 tip deflections: the values ANSYS’s quadratic element should come within about 1% of.",
               "Jalankan kajian mesh (dalam kelas, dari QR pada telefon anda). Baca tip deflection 8-node 2 × 1 dan 8 × 4: nilai yang patut dihampiri dalam lingkungan kira-kira 1% oleh quadratic element ANSYS."),
     ("detected when the mesh study runs with the text’s data", "dikesan apabila kajian mesh dijalankan dengan data teks")),
    ("pstrain", ("Wrong model (a): on one mesh, switch from plane stress to plane strain. How much stiffer, and does the ratio match 1 − ν²?",
                 "Model salah (a): pada satu mesh, tukar dari plane stress ke plane strain. Berapa lebih kaku, dan adakah nisbahnya sepadan dengan 1 − ν²?"),
     ("detected when the same mesh has been solved in plane stress and in plane strain with the text’s data", "dikesan apabila mesh yang sama telah diselesaikan dalam plane stress dan plane strain dengan data teks")),
    ("point", ("Wrong model (b): replace the edge traction by a point force at the top corner (same total). Compare the loaded node with mid-depth.",
               "Model salah (b): gantikan traction tepi dengan point force pada bucu atas (jumlah yang sama). Bandingkan node yang dibebankan dengan tengah kedalaman."),
     ("detected when the point force at the top corner is solved with the text’s data otherwise", "dikesan apabila point force pada bucu atas diselesaikan dengan data teks yang lain")),
    ("vonly", ("Wrong model (c): change the support to “Vertical only: v = 0”. What does the Explorer report — and what would ANSYS do instead?",
               "Model salah (c): tukar support kepada “Vertical only: v = 0”. Apa yang dilaporkan oleh Explorer — dan apa yang akan dilakukan ANSYS?"),
     ("detected when the vertical-only support leaves the model unsolvable", "dikesan apabila support vertical-only menjadikan model tidak boleh diselesaikan")),
    ("thick", ("Wrong model (d): in “Model data”, change the thickness t. Check that the deflection scales exactly as 1/t while the reaction stays the same.",
               "Model salah (d): dalam “Model data”, tukar ketebalan t. Semak bahawa deflection berskala tepat sebagai 1/t manakala reaction kekal sama."),
     ("detected when t differs from 0.01 m with the text’s data otherwise", "dikesan apabila t berbeza daripada 0.01 m dengan data teks yang lain")),
]

GLOSSARY = [
    ("Workbench project schematic", "The chain of cells Engineering Data → Geometry → Model/Mesh → Setup → Solution → Results: the six steps of the hand calculation.", "Rantaian sel Engineering Data → Geometry → Model/Mesh → Setup → Solution → Results: enam langkah pengiraan tangan."),
    ("Analysis Type 2D · 2D Behavior", "Geometry-cell setting that makes the model two-dimensional; in Mechanical, the choice Plane Stress or Plane Strain, with a Thickness for plane stress.", "Tetapan sel Geometry yang menjadikan model dua dimensi; dalam Mechanical, pilihan Plane Stress atau Plane Strain, dengan Thickness bagi plane stress."),
    ("Element Order", "Linear (4-node: PLANE182, thermal PLANE55) or Quadratic (8-node: PLANE183, thermal PLANE77); Program Controlled gives quadratic for 2D solids.", "Linear (4-node: PLANE182, thermal PLANE55) atau Quadratic (8-node: PLANE183, thermal PLANE77); Program Controlled memberi quadratic bagi 2D solid."),
    ("Edge Sizing · Element Size · Face Meshing", "Number of divisions on an edge, one target size for the whole face, and the request for a mapped (structured) quadrilateral mesh.", "Bilangan bahagian pada satu tepi, satu saiz sasaran untuk seluruh muka, dan permintaan untuk mesh segi empat berpeta (berstruktur)."),
    ("enhanced strain · Element Control", "An option of the linear element that adds internal modes so it bends without locking; Element Control: Manual with full integration gives the textbook Q4.", "Pilihan linear element yang menambah mod dalaman supaya ia melentur tanpa locking; Element Control: Manual dengan full integration memberi Q4 buku teks."),
    ("Fixed Support · Displacement", "Essential conditions: all dofs, or chosen components, of an edge set to zero or a value.", "Essential condition: semua dof, atau komponen yang dipilih, pada satu tepi ditetapkan kepada sifar atau satu nilai."),
    ("Force · Pressure (on an edge)", "Natural conditions: a total force spread over the edge, or a force per unit area of the edge face; Mechanical turns either into consistent nodal loads.", "Natural condition: jumlah daya yang disebarkan pada tepi, atau daya per unit luas muka tepi; Mechanical menukar kedua-duanya menjadi consistent nodal load."),
    ("Internal Heat Generation", "The source q<sub>h</sub> in W m<sup>−3</sup> on a body; with thickness t its total is q<sub>h</sub> × area × t.", "Sumber q<sub>h</sub> dalam W m<sup>−3</sup> pada jasad; dengan ketebalan t jumlahnya q<sub>h</sub> × luas × t."),
    ("Reaction probe", "Force Reaction, Moment Reaction or heat reaction on a support or prescribed temperature: the struck rows of [K]{U} − {R}. The first check of every run.", "Force Reaction, Moment Reaction atau reaction haba pada support atau suhu yang ditetapkan: baris yang dibuang [K]{U} − {R}. Semakan pertama setiap run."),
    ("Averaged · Unaveraged · Elemental Mean", "Display Options of a stress result: nodal average, each element’s own nodal values, one centroid value per element.", "Display Option bagi keputusan stress: purata nodal, nilai node setiap element sendiri, satu nilai centroid setiap element."),
    ("rigid-body mode · weak springs", "A motion the supports do not stop (here, translation in x); the solver warns and may add weak springs to solve anyway — the warning is the evidence.", "Gerakan yang tidak dihalang oleh support (di sini, translasi dalam x); solver memberi amaran dan mungkin menambah weak springs untuk tetap menyelesaikan — amaran itulah buktinya."),
    ("input error · idealisation error", "A wrong load, unit or support (shows in the reaction) against a wrong modelling choice that equilibrium cannot catch (shows only against a prediction).", "Load, unit atau support yang salah (kelihatan pada reaction) berbanding pilihan pemodelan yang salah yang tidak dapat ditangkap oleh keseimbangan (hanya kelihatan berbanding ramalan)."),
    ("verification", "Solving the equations right: checks that are exact for the model — hand calculation, patch test, analytical solution, reactions, a second code.", "Menyelesaikan persamaan dengan betul: semakan yang tepat bagi model — pengiraan tangan, patch test, penyelesaian analitikal, reaction, kod kedua."),
    ("validation", "Solving the right equations: comparison of the model with measurements on the real structure.", "Menyelesaikan persamaan yang betul: perbandingan model dengan pengukuran pada struktur sebenar."),
    ("patch test", "A small mesh of unequal elements under a load whose exact solution is a constant stress; a consistent element reproduces it to round-off.", "Mesh kecil element yang tidak sama di bawah load yang penyelesaian tepatnya ialah stress malar; element yang konsisten menghasilkannya semula hingga round-off."),
    ("stage gate", "A check that must be passed, with evidence, before the next stage of the project starts.", "Semakan yang mesti dilepasi, dengan bukti, sebelum peringkat projek seterusnya bermula."),
    ("observed order p", "The rate measured from three meshes: successive changes shrink by 2<sup>p</sup> per halving of the element size.", "Kadar yang diukur daripada tiga mesh: perubahan berturut-turut mengecil sebanyak 2<sup>p</sup> bagi setiap pembahagian dua saiz element."),
    ("Kirsch solution", "The exact stresses around a circular hole in an infinite plate in tension: 3σ<sub>0</sub> at the edge of the hole (K<sub>t</sub> = 3).", "Stress tepat di sekeliling lubang bulat dalam plat tak terhingga dalam tegangan: 3σ<sub>0</sub> di tepi lubang (K<sub>t</sub> = 3)."),
    ("DesignModeler · Discovery", "Two geometry editors opened from the Geometry cell: right-click → New DesignModeler Geometry for the sketch-based editor used on this page; a double-click opens the default editor, Discovery in recent releases.", "Dua editor geometri yang dibuka dari sel Geometry: klik kanan → New DesignModeler Geometry untuk editor berasaskan sketch yang digunakan di halaman ini; klik dua kali membuka editor lalai, iaitu Discovery dalam release terkini."),
    ("Surfaces From Sketches", "DesignModeler’s Concept command that turns a closed sketch on the XY plane into the surface body of a 2D model; an inner loop becomes a hole.", "Arahan Concept dalam DesignModeler yang menukar sketch tertutup pada satah XY menjadi surface body bagi model 2D; gelung dalam menjadi lubang."),
    ("Path (Construction Geometry)", "A line (Two Points) or an edge along which a result is sampled; a result with Scoping Method = Path gives a graph and a table.", "Garisan (Two Points) atau tepi yang sepanjangnya keputusan diambil sampel; keputusan dengan Scoping Method = Path memberi graf dan jadual."),
    ("Function load", "A load magnitude given as an expression in x or y, starting with “=”, such as =9810*(5-y) for water pressure.", "Magnitud load yang diberi sebagai ungkapan dalam x atau y, bermula dengan “=”, seperti =9810*(5-y) bagi tekanan air."),
    ("GenAI log", "The record of prompts, accepted and rejected AI output, and the gate that caught each error; marked with the reflection.", "Rekod prompt, output AI yang diterima dan ditolak, dan gate yang menangkap setiap ralat; dinilai bersama refleksi."),
]


def short_notes(A):
    return (
        "<h3>§1 " + B("Workbench", "Workbench") + "</h3>" + A.eq("p6_load", None, 0.45)
        + P("Units first (Metric); Analysis Type 2D; Plane Stress + Thickness. Hand mesh: Edge Sizing 2 and 2, Linear. Plate 16 × 16: Element Size 0.0625 m.",
            "Unit dahulu (Metric); Analysis Type 2D; Plane Stress + Thickness. Mesh tangan: Edge Sizing 2 dan 2, Linear. Plat 16 × 16: Element Size 0.0625 m.")
        + "<h3>§2 " + B("Plate", "Plat") + "</h3>"
        + P("Linear 2 × 2: 0.6214 (corner), 0.4821 (mid-edges). 16 × 16: 0.5898; reference 0.5897. Heat reactions sum to −Q A t.",
            "Linear 2 × 2: 0.6214 (bucu), 0.4821 (tengah tepi). 16 × 16: 0.5898; rujukan 0.5897. Reaction haba berjumlah −Q A t.")
        + "<h3>§3 " + B("Cantilever", "Cantilever") + "</h3>" + A.eq("p6_reaction", None, 0.45)
        + P("Linear 2 × 2: 0.1306 m (textbook Q4). Quadratic 2 × 1 / 4 × 2 / 8 × 4 / 16 × 8: 0.1780 / 0.1885 / 0.1906 / 0.1913 m; changes 5.57, 1.12, 0.35%. Timoshenko 0.1919 m.",
            "Linear 2 × 2: 0.1306 m (Q4 buku teks). Quadratic 2 × 1 / 4 × 2 / 8 × 4 / 16 × 8: 0.1780 / 0.1885 / 0.1906 / 0.1913 m; perubahan 5.57, 1.12, 0.35%. Timoshenko 0.1919 m.")
        + "<h3>§4 " + B("Stresses and wrong models", "Stress dan model salah") + "</h3>"
        + P("Elemental Mean vs M(y − H/2)/I; ignore the corner Max. Plane strain −10%; vertex force +20% at the node; v-only: warning; thickness: ×1/100. Reaction right in all four.",
            "Elemental Mean berbanding M(y − H/2)/I; abaikan Max di bucu. Plane strain −10%; daya bucu +20% pada node; v sahaja: amaran; ketebalan: ×1/100. Reaction betul dalam keempat-empatnya.")
        + "<h3>§5 " + B("First run", "Run pertama") + "</h3>"
        + P("Units · geometry · material · supports · loads · coarse mesh · reaction · hand estimate (factor 2). Then refine.",
            "Unit · geometri · bahan · support · load · mesh kasar · reaction · anggaran tangan (faktor 2). Kemudian refine.")
        + "<h3>§6 " + B("V&amp;V and the project", "V&amp;V dan projek") + "</h3>"
        + P("Verification = equations solved right; validation = right equations. Gates 0 plan · 1 core solver · 2 known solution · 3 ANSYS cross-check · 4 deploy · 5 viva. Marks 35 · 20 · 25 · 10 · 10.",
            "Verification = persamaan diselesaikan dengan betul; validation = persamaan yang betul. Gate 0 pelan · 1 core solver · 2 penyelesaian diketahui · 3 semakan silang ANSYS · 4 deploy · 5 viva. Markah 35 · 20 · 25 · 10 · 10.")
        + "<h3>§7 " + B("Workbench how-to", "Panduan Workbench") + "</h3>"
        + P("Right-click Geometry → New DesignModeler Geometry; XYPlane sketch: Arc by Center, Fillet, Circle (hole), Spline; Surfaces From Sketches. Varying load: Magnitude → Function, =9810*(5-y). Curve of a result: Construction Geometry → Path, Scoping Method = Path.",
            "Klik kanan Geometry → New DesignModeler Geometry; sketch XYPlane: Arc by Center, Fillet, Circle (lubang), Spline; Surfaces From Sketches. Load berubah: Magnitude → Function, =9810*(5-y). Lengkung keputusan: Construction Geometry → Path, Scoping Method = Path.")
    )


# ---- worked examples: answer-scheme style ----
EXAMPLES_INTRO = (
    '<div class="card" style="margin-bottom:18px"><h2 style="font-size:18px;margin:0 0 6px">' + B("How this part is assessed", "Bagaimana bahagian ini dinilai") + '</h2>'
    + P("This part is mostly assessed through the project. In a test, software appears as given output to be judged: convert the inputs, predict what a correct run must show, check a reaction or a mesh study, name a wrong model from its numbers. "
        "The model answers below are in that form, with a suggested marking scheme; the examiner’s own scheme may differ.",
        "Bahagian ini kebanyakannya dinilai melalui projek. Dalam ujian, perisian muncul sebagai output yang diberi untuk dinilai: tukar input, ramal apa yang mesti ditunjukkan oleh run yang betul, semak reaction atau kajian mesh, namakan model yang salah daripada nombornya. "
        "Jawapan model di bawah dalam bentuk itu, dengan skema pemarkahan cadangan; skema pemeriksa sendiri mungkin berbeza.", "lead")
    + '<div class="tbl"><table class="howex"><tr><th>' + B("Question type", "Jenis soalan") + '</th><th>' + B("Given and wanted", "Diberi dan dikehendaki") + '</th><th>' + B("Plan and the usual trap", "Pelan dan perangkap biasa") + '</th></tr>'
    + '<tr><td>' + B("Predict a run", "Ramal satu run") + '</td><td>' + B("A textbook problem and an ANSYS set-up; wanted: the inputs and the numbers a correct run must give.", "Masalah buku teks dan set-up ANSYS; dikehendaki: input dan nombor yang mesti diberi oleh run yang betul.") + '</td><td>' + B("Convert, then solve the coarse mesh by hand; use symmetry. Trap: Pressure = q × t.", "Tukar, kemudian selesaikan mesh kasar dengan tangan; guna simetri. Perangkap: Pressure = q × t.") + '</td></tr>'
    + '<tr><td>' + B("Judge a mesh study", "Menilai kajian mesh") + '</td><td>' + B("Results of three or more meshes; wanted: changes, the mesh to report, a signed comparison.", "Keputusan tiga atau lebih mesh; dikehendaki: perubahan, mesh yang dilaporkan, perbandingan bertanda.") + '</td><td>' + B("Change formula; Richardson; Timoshenko. Trap: “converged” with no number.", "Formula perubahan; Richardson; Timoshenko. Perangkap: “converged” tanpa nombor.") + '</td></tr>'
    + '<tr><td>' + B("Diagnose", "Mendiagnosis") + '</td><td>' + B("Several runs with reactions, deflections and stresses; wanted: which mistake, and the evidence.", "Beberapa run dengan reaction, deflection dan stress; dikehendaki: kesilapan mana, dan buktinya.") + '</td><td>' + B("Reaction first; then factor, location, warning, extra component. Trap: blaming the mesh.", "Reaction dahulu; kemudian faktor, lokasi, amaran, komponen tambahan. Perangkap: menyalahkan mesh.") + '</td></tr>'
    + '<tr><td>' + B("Verify a code", "Mengesahkan kod") + '</td><td>' + B("A solver of your own; wanted: the gate checks and what each proves.", "Solver anda sendiri; dikehendaki: semakan gate dan apa yang dibuktikan setiap satu.") + '</td><td>' + B("One element, patch test, ΣR against the physical load, a known solution. Trap: one passed test taken as proof.", "Satu element, patch test, ΣR berbanding load fizikal, penyelesaian diketahui. Perangkap: satu ujian lulus dianggap bukti.") + '</td></tr></table></div>'
    + P("ANSYS values are not quoted as measured: the numbers below come from the course solvers and the text, and are what a correct run should reproduce (to the last digit for the textbook element, to about 1% for PLANE183).",
        "Nilai ANSYS tidak dipetik sebagai diukur: nombor di bawah datang daripada solver kursus dan teks, dan itulah yang patut dihasilkan semula oleh run yang betul (hingga digit terakhir bagi element buku teks, kira-kira 1% bagi PLANE183).", "lead")
    + '</div>')


def _head(n, t_en, t_ms, kind, units, src, marks):
    return ('<div class="xhead"><h2>' + B(f"Example {n} · {t_en}", f"Contoh {n} · {t_ms}") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + f'</b> {kind}</span><span><b>' + B("Units", "Unit") + f'</b> {units}</span><span><b>' + B("Source", "Sumber") + f'</b> {src}</span><span><b>{marks} ' + B("marks", "markah") + '</b></span></div></div>')


def examples(A):
    X = []
    # ---- Example 1: the plate in Steady-State Thermal ----
    head = _head(1, "The plate in Workbench: predict the hand mesh, check the heat balance, judge the refinement", "Plat dalam Workbench: ramal mesh tangan, semak keseimbangan haba, nilai refine",
                 "predict a software run; energy check", "W, m, °C", "text §2.3; Heat Transfer Part 2", 15)
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("The 1 m square plate of the text (k = 300 W m<sup>−1</sup> K<sup>−1</sup>, 600 W m<sup>−3</sup> generated, 0 °C on the top and left edges, the other edges insulated, t = 1 m) is set up in Steady-State Thermal with four linear elements (Element Size 0.5 m). "
             "(a) Predict, by hand, the temperatures the run must show at the free nodes. (b) What must the reactions on the two Temperature conditions add up to, and why? (c) Runs with 4 × 4, 8 × 8 and 16 × 16 elements give 0.5968, 0.5912 and 0.5898 °C at the corner; the converged value is 0.5897 °C. Judge the 2 × 2 run.",
             "Plat segi empat sama 1 m dalam teks (k = 300 W m<sup>−1</sup> K<sup>−1</sup>, 600 W m<sup>−3</sup> dijana, 0 °C pada tepi atas dan kiri, tepi lain insulated, t = 1 m) disediakan dalam Steady-State Thermal dengan empat linear element (Element Size 0.5 m). "
             "(a) Ramal, dengan tangan, suhu yang mesti ditunjukkan oleh run pada node bebas. (b) Berapakah jumlah reaction pada dua keadaan Temperature, dan mengapa? (c) Run dengan 4 × 4, 8 × 8 dan 16 × 16 element memberi 0.5968, 0.5912 dan 0.5898 °C di bucu; nilai converge ialah 0.5897 °C. Nilai run 2 × 2.")
         + '</div>')
    body = (head + q + A.fig("fig_plate_ansys", "The plate with its ANSYS conditions; nodes 1–3 along the bottom, 7–9 along the top.", "Plat dengan keadaan ANSYS-nya; node 1–3 di sepanjang bawah, 7–9 di sepanjang atas.", 300)
            + PIC("Heat is generated everywhere and can leave only through the cold top and left edges, so the hottest point is the corner farthest from both, the bottom-right. The plate is symmetric about the diagonal from (0, 1) to (1, 0): the bottom mid-edge and the right mid-edge must have the same temperature.",
                  "Haba dijana di semua tempat dan hanya boleh keluar melalui tepi atas dan kiri yang sejuk, jadi titik paling panas ialah bucu paling jauh dari kedua-duanya, iaitu kanan bawah. Plat simetri terhadap pepenjuru dari (0, 1) ke (1, 0): tengah tepi bawah dan tengah tepi kanan mesti mempunyai suhu yang sama.")
            + PLAN("[k] for a = b = 0.5 → {q} → assemble the free rows (nodes 2, 3, 5, 6) → T<sub>6</sub> = T<sub>2</sub> → solve → heat balance → percentages.")
            + XSTEP(1, "(a) Element matrix and loads", "(a) Matrix element dan load", 4, A.eq("x1_k") + A.eq("x1_q")
                    + CHK("Each row of [k] adds up to zero (a uniform temperature carries no heat), and the four element loads add up to Q a b t = 150 W."))
            + XSTEP(2, "(a) The free equations", "(a) Persamaan bebas", 4, P("Nodes 1, 4, 7, 8, 9 are at 0 °C, so only the rows and columns of nodes 2, 3, 5, 6 remain:", "Node 1, 4, 7, 8, 9 pada 0 °C, jadi hanya baris dan lajur node 2, 3, 5, 6 yang tinggal:")
                    + A.eq("x1_sys") + P("With T<sub>6</sub> = T<sub>2</sub> (symmetry), the first three rows become", "Dengan T<sub>6</sub> = T<sub>2</sub> (simetri), tiga baris pertama menjadi") + A.eq("x1_red") + A.eq("x1_T")
                    + CHK("Row 2: " + "300(0.48214) − 50(0.62143) − 100(0.38571) = 75.00.")
                    + ANS("(a) The run must show T<sub>3</sub> = 0.6214 °C at the corner, 0.4821 °C at both mid-edges and 0.3857 °C at the centre — the text’s (2.55), to four decimals."))
            + XSTEP(3, "(b) The heat balance", "(b) Keseimbangan haba", 3, P("The reactions are the struck rows [K]{T} − {R} at the fixed nodes, the heat removed there:", "Reaction ialah baris yang dibuang [K]{T} − {R} pada node tetap, haba yang dikeluarkan di situ:")
                    + A.eq("x1_heat")
                    + ANS("(b) −600 W in total (with t = 1 m): in a steady state all the heat generated, 600 × 1 × 1 W, must leave through the cold edges, on any mesh."))
            + XSTEP(4, "(c) The refinement", "(c) Refine", 4, A.eq("x1_err")
                    + ANS("(c) The 2 × 2 run over-predicts the peak by 5.4%; the error falls by about 4 to 5 times per halving, and 16 × 16 is within 0.02%."))
            + INTERP("The linear 2 × 2 run is a test of the model, not of the physics: it must reproduce the hand calculation exactly, because it is the same element with the same consistent loads. If it does not, the mesh or the element order is not what you think. The heat balance is the thermal version of the reaction check — exact on any mesh, so it checks the conditions and the source, not the accuracy. Accuracy comes only from the refinement, and here it is quick: the error drops roughly as h², so 8 × 8 is already within 0.3%.",
                     "Run linear 2 × 2 menguji model, bukan fizik: ia mesti menghasilkan semula pengiraan tangan dengan tepat, kerana ia element yang sama dengan consistent load yang sama. Jika tidak, mesh atau element order bukan seperti yang anda sangka. Keseimbangan haba ialah versi thermal bagi semakan reaction — tepat pada sebarang mesh, jadi ia menyemak keadaan sempadan dan sumber, bukan ketepatan. Ketepatan hanya datang daripada refine, dan di sini ia cepat: ralat menurun lebih kurang sebagai h², jadi 8 × 8 sudah dalam 0.3%.")
            + SCHEME([("Element matrix and the nodal loads", "Matrix element dan nodal load", 4), ("Free equations, symmetry, solution and a check", "Persamaan bebas, simetri, penyelesaian dan semakan", 4),
                      ("Heat balance with the reason", "Keseimbangan haba bersama sebabnya", 3), ("Percentages and the judgement", "Peratus dan penilaian", 4)], 15))
    X.append(("y1", "The plate in Workbench: predict and check", "Plat dalam Workbench: ramal dan semak", body))

    # ---- Example 2: the cantilever in Static Structural ----
    head = _head(2, "The cantilever in Workbench: inputs, reactions, the convergence table and the reported value", "Cantilever dalam Workbench: input, reaction, convergence table dan nilai yang dilaporkan",
                 "set up a run and judge a mesh study", "N, m", "text §3.4; Plane Stress Parts 2–3", 20)
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("The text’s cantilever (4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, fixed on the left, q<sub>y</sub> = −5 kN m<sup>−1</sup> on the right edge) is to be run in Static Structural. "
             "(a) Give the Force or Pressure, E and the Edge Sizing that reproduce the 2 × 2 hand mesh. (b) What must the Force and Moment Reaction probes show? (c) Quadratic meshes give the tip deflections below: compute the changes and choose the mesh to report at a 1% tolerance. "
             "(d) Compare with Timoshenko beam theory and estimate the converged value. (e) Linear elements give 0.1824 m (8 × 4) and 0.1886 m (16 × 8). Comment.",
             "Cantilever teks (4 m × 2 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, tetap di kiri, q<sub>y</sub> = −5 kN m<sup>−1</sup> pada tepi kanan) akan di-run dalam Static Structural. "
             "(a) Beri Force atau Pressure, E dan Edge Sizing yang menghasilkan semula mesh tangan 2 × 2. (b) Apa yang mesti ditunjukkan oleh probe Force dan Moment Reaction? (c) Mesh quadratic memberi tip deflection di bawah: kira perubahan dan pilih mesh untuk dilaporkan pada toleransi 1%. "
             "(d) Bandingkan dengan Timoshenko beam theory dan anggarkan nilai converge. (e) Linear element memberi 0.1824 m (8 × 4) dan 0.1886 m (16 × 8). Ulas.")
         + _tbl([B("quadratic mesh", "mesh quadratic"), "2 × 1", "4 × 2", "8 × 4", "16 × 8"], [["|v<sub>tip</sub>| (m)", "0.17796", "0.18846", "0.19059", "0.19125"]], "num")
         + B("Values from the course Q8 solver; a PLANE183 run should be within about 1% of them.", "Nilai daripada solver Q8 kursus; run PLANE183 patut berada dalam kira-kira 1% daripadanya.") + '</div>')
    body = (head + q + A.fig("fig_cant_ansys", "The cantilever with its ANSYS inputs.", "Cantilever dengan input ANSYS-nya.", 560)
            + PIC("The end load bends the cantilever down and every section carries 10 kN of shear. The supports must carry the load and its moment about the fixed edge whatever the mesh. The deflection rises towards the Timoshenko value as the mesh is refined, quickly with quadratic elements, slowly with linear ones.",
                  "Load hujung melentur cantilever ke bawah dan setiap keratan membawa shear 10 kN. Support mesti membawa load dan momennya terhadap tepi tetap tanpa mengira mesh. Deflection naik ke arah nilai Timoshenko apabila mesh di-refine, cepat dengan quadratic element, perlahan dengan linear element.")
            + PLAN("Convert → reactions from statics → changes → tolerance → Timoshenko → Richardson → linear against quadratic.")
            + XSTEP(1, "(a) Inputs", "(a) Input", 3, A.eq("x2_in") + CHK("−500 × 10³ × (2 × 0.01) = −10 000 N: the Pressure gives the Force back."))
            + XSTEP(2, "(b) Reactions", "(b) Reaction", 3, A.eq("p6_reaction")
                    + ANS("(b) Force Reaction X = 0, Y = +10 000 N; Moment Reaction 40 000 N m — on every mesh and for either element order."))
            + XSTEP(3, "(c) The convergence table", "(c) Convergence table", 4, A.eq("x2_chg")
                    + ANS("(c) Report the 8 × 4 mesh (or finer): the refinement after it changed the deflection by 0.35%, below 1%."))
            + XSTEP(4, "(d) Independent check and the converged value", "(d) Semakan bebas dan nilai converge", 6, A.eq("p6_timo") + A.eq("x2_diff") + A.eq("x2_rich")
                    + CHK("The course Q8 32 × 16 mesh gives 0.19151 m, 0.02% from the extrapolated 0.19155 m.")
                    + ANS("(d) 8 × 4 is 0.69% and 16 × 8 0.35% below Timoshenko’s 0.1919 m; the extrapolated plane-stress value is 0.1916 m, about 0.2% below beam theory, which is a different model (κ = 5/6, no restraint of the Poisson contraction at the support)."))
            + XSTEP(5, "(e) Linear elements", "(e) Linear element", 4, A.eq("x2_lin")
                    + ANS("(e) The linear element is 4.3% stiffer on the 8 × 4 mesh and needs 16 × 8 to come within 2% of beam theory: shear locking. Expect an enhanced-strain PLANE182 to do better than these textbook-Q4 values; say which formulation was used."))
            + INTERP("Three numbers carry the result: the reaction (inputs right), the change between the last two meshes (discretisation small enough) and the difference from Timoshenko (an independent model agrees). The report sentence follows directly: “The 8 × 4 quadratic mesh gives a tip deflection of 0.1906 m; the next refinement changed it by 0.35%, and it lies 0.7% below Timoshenko beam theory; the reactions are 10.0 kN and 40.0 kN m.” "
                     "Richardson adds an error estimate without a finer mesh, and the 32 × 16 result confirms it to 0.02%. The remaining 0.2% between the converged plate and beam theory is a modelling difference, not a mesh error — which is why beam theory is a check, not the truth.",
                     "Tiga nombor membawa keputusan: reaction (input betul), perubahan antara dua mesh terakhir (discretisation cukup kecil) dan perbezaan daripada Timoshenko (model bebas sepakat). Ayat laporan terus terhasil: “The 8 × 4 quadratic mesh gives a tip deflection of 0.1906 m; the next refinement changed it by 0.35%, and it lies 0.7% below Timoshenko beam theory; the reactions are 10.0 kN and 40.0 kN m.” "
                     "Richardson menambah anggaran ralat tanpa mesh yang lebih halus, dan keputusan 32 × 16 mengesahkannya hingga 0.02%. Baki 0.2% antara plat yang converge dan beam theory ialah perbezaan pemodelan, bukan ralat mesh — sebab itulah beam theory ialah semakan, bukan kebenaran.")
            + SCHEME([("Force or Pressure, E, Edge Sizing", "Force atau Pressure, E, Edge Sizing", 3), ("Both reactions with the reason they do not change", "Kedua-dua reaction bersama sebab ia tidak berubah", 3),
                      ("Three changes and the mesh to report", "Tiga perubahan dan mesh yang dilaporkan", 4), ("Timoshenko, signed differences, Richardson", "Timoshenko, perbezaan bertanda, Richardson", 6), ("Linear against quadratic, with the mechanism", "Linear berbanding quadratic, bersama mekanismenya", 4)], 20))
    X.append(("y2", "The cantilever in Workbench: inputs, reactions, mesh study", "Cantilever dalam Workbench: input, reaction, kajian mesh", body))

    # ---- Example 3: four wrong runs ----
    head = _head(3, "Four runs of the cantilever, three of them wrong: diagnose from the numbers", "Empat run cantilever, tiga daripadanya salah: diagnosis daripada nombor",
                 "diagnose software output", "N, m, kN m⁻²", "W14 Activity 4; Cantilever Explorer", 12)
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("Four quadratic 32 × 16 runs of the text’s cantilever give the results below; the correct model gives a tip deflection of 0.1915 m and, in the element under the right edge’s top corner, σ<sub>vM</sub> = 523 kN m<sup>−2</sup>. For each run, name the mistake (plane strain, a vertex force, a support that fixes only v, a wrong thickness) or say it is correct, and give the evidence.",
             "Empat run quadratic 32 × 16 bagi cantilever teks memberi keputusan di bawah; model yang betul memberi tip deflection 0.1915 m dan, dalam element di bawah bucu atas tepi kanan, σ<sub>vM</sub> = 523 kN m<sup>−2</sup>. Bagi setiap run, namakan kesilapannya (plane strain, daya pada bucu, support yang hanya menetapkan v, ketebalan yang salah) atau nyatakan ia betul, dan beri buktinya.")
         + _tbl([B("Run", "Run"), "R<sub>y</sub> (N)", B("tip v (m)", "tip v (m)"), B("other output", "output lain")],
                [["A", "+10 000", "−0.001915", B("—", "—")], ["B", "+10 000", "−0.2298", B("mid-depth of the free end −0.1875 m; σ<sub>vM</sub> 5353 kN m<sup>−2</sup> under the load", "tengah kedalaman hujung bebas −0.1875 m; σ<sub>vM</sub> 5353 kN m<sup>−2</sup> di bawah load")],
                 ["C", "+10 000", "−0.1722", B("σ<sub>zz</sub> listed among the results", "σ<sub>zz</sub> disenaraikan dalam keputusan")], ["D", "+10 000", "−0.1915", B("no warnings; σ<sub>vM</sub> 523 kN m<sup>−2</sup> in the corner element", "tiada amaran; σ<sub>vM</sub> 523 kN m<sup>−2</sup> dalam element bucu")]]) + '</div>')
    body = (head + q
            + PIC("Every run has the right reaction, so the loads and supports carry 10 kN: the differences are in the idealisation. Each idealisation error scales the response in its own way — the thickness divides everything, plane strain stiffens by about 1 − ν², a point load disturbs only its neighbourhood.",
                  "Setiap run mempunyai reaction yang betul, jadi load dan support membawa 10 kN: perbezaannya terletak pada idealisation. Setiap ralat idealisation menskala respons dengan caranya sendiri — ketebalan membahagi segalanya, plane strain mengakukan kira-kira 1 − ν², point load hanya mengganggu kawasan sekitarnya.")
            + PLAN("Reaction → ratio to the correct deflection → where the change is (everywhere or local) → the extra output.")
            + XSTEP(1, "Ratios to the correct model", "Nisbah kepada model yang betul", 4, A.eq("x3_ratio") + A.eq("x3_vm"))
            + XSTEP(2, "A and C", "A dan C", 3, P("A is a clean factor of 0.0100 everywhere: v ∝ 1/t, so the thickness is 1 m instead of 0.01 m. C is 10% stiffer, close to 1 − ν², and lists σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>), which exists only in plane strain.",
                                                       "A ialah faktor 0.0100 yang tepat di semua tempat: v ∝ 1/t, jadi ketebalan 1 m dan bukannya 0.01 m. C 10% lebih kaku, hampir 1 − ν², dan menyenaraikan σ<sub>zz</sub> = ν(σ<sub>xx</sub> + σ<sub>yy</sub>), yang hanya wujud dalam plane strain.")
                    + ANS("A: thickness. C: plane strain."))
            + XSTEP(3, "B and D", "B dan D", 3, P("B is 20% too flexible at the loaded vertex but within 0.7% at mid-depth, and the stress under the load is ten times the correct value: a local disturbance, the signature of a point force (St-Venant). D matches the correct model in deflection and stress, with no warning.",
                                                     "B 20% terlalu fleksibel pada bucu yang dibebankan tetapi dalam 0.7% di tengah kedalaman, dan stress di bawah load sepuluh kali nilai yang betul: gangguan setempat, tanda point force (St-Venant). D sepadan dengan model yang betul dalam deflection dan stress, tanpa amaran.")
                    + ANS("B: a force on the top-right vertex. D: correct. The fourth mistake, a support fixing only v, is not among them: it would have produced a rigid-body warning."))
            + XSTEP(4, "Why the reaction did not help", "Mengapa reaction tidak membantu", 2, P("Equilibrium of the whole plate fixes R<sub>y</sub> = 10 000 N for any stiffness, thickness or idealisation. It catches a wrong load or a missing support, never a wrong model.",
                                                                                                 "Keseimbangan seluruh plat menetapkan R<sub>y</sub> = 10 000 N bagi sebarang kekakuan, ketebalan atau idealisation. Ia menangkap load yang salah atau support yang tertinggal, tidak sekali-kali model yang salah."))
            + INTERP("A modelling mistake leaves a signature: a clean factor (thickness, units), a factor tied to a material constant (1 − ν² for plane strain), a local disturbance (a point load), or a warning (a mechanism). Reading it needs a prediction to compare against — the correct deflection here, a hand estimate in the project. That is why the reaction is the first check but never the last.",
                     "Kesilapan pemodelan meninggalkan tanda: faktor yang tepat (ketebalan, unit), faktor yang terikat pada pemalar bahan (1 − ν² bagi plane strain), gangguan setempat (point load), atau amaran (mekanisme). Membacanya memerlukan ramalan untuk dibandingkan — deflection yang betul di sini, anggaran tangan dalam projek. Sebab itulah reaction ialah semakan pertama tetapi tidak pernah yang terakhir.")
            + SCHEME([("Three ratios and the stress ratio", "Tiga nisbah dan nisbah stress", 4), ("A and C named with evidence", "A dan C dinamakan dengan bukti", 3), ("B and D named with evidence", "B dan D dinamakan dengan bukti", 3), ("Why equilibrium cannot catch them", "Mengapa keseimbangan tidak dapat menangkapnya", 2)], 12))
    X.append(("y3", "Four runs: diagnose the wrong models", "Empat run: diagnosis model yang salah", body))

    # ---- Example 4: Stage 1 gates for your own solver ----
    head = _head(4, "Gate 1 for your own solver: one element, the patch test and the reactions — and what they miss", "Gate 1 bagi solver anda sendiri: satu element, patch test dan reaction — dan apa yang terlepas",
                 "verify a code; explain what a check proves", "N, m", "hybrid project, Gates 1–2", 15)
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>'
         + B("A group’s plane-stress solver (4-node rectangles) is at Gate 1. (a) For one element with a = 2 m, b = 1 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, what must k<sub>11</sub> be? "
             "(b) The patch of the figure (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.3, t = 0.01 m) is pulled by σ<sub>0</sub> = 1000 kN m<sup>−2</sup> on its right edge. Give the nodal loads, the exact displacements, the stresses and the reaction that a correct solver must reproduce. "
             "(c) Two bugs are planted: the edge nodes receive σ<sub>0</sub>tb instead of σ<sub>0</sub>tb/2, and the shear entry of [E] is Ē instead of Ē(1 − ν)/2. Which Gate 1 check catches each, and what catches the other?",
             "Solver plane stress satu kumpulan (segi empat tepat 4-node) berada di Gate 1. (a) Bagi satu element dengan a = 2 m, b = 1 m, t = 0.01 m, E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.33, berapakah k<sub>11</sub> yang sepatutnya? "
             "(b) Patch dalam rajah (E = 200 × 10⁶ N m<sup>−2</sup>, ν = 0.3, t = 0.01 m) ditarik oleh σ<sub>0</sub> = 1000 kN m<sup>−2</sup> pada tepi kanannya. Beri nodal load, displacement tepat, stress dan reaction yang mesti dihasilkan semula oleh solver yang betul. "
             "(c) Dua pepijat ditanam: node tepi menerima σ<sub>0</sub>tb dan bukannya σ<sub>0</sub>tb/2, dan entri shear [E] ialah Ē dan bukannya Ē(1 − ν)/2. Semakan Gate 1 mana yang menangkap setiap satu, dan apa yang menangkap yang lain?") + '</div>')
    body = (head + q + A.fig("fig_patch", "The patch: four rectangles of unequal size, rollers on the left edge, a pin at node 1, uniform tension σ<sub>0</sub> on the right edge.",
                             "Patch: empat segi empat tepat yang tidak sama saiz, roller pada tepi kiri, pin di node 1, tegangan seragam σ<sub>0</sub> pada tepi kanan.", 520)
            + PIC("A uniform tension in a plate gives a constant stress, a displacement linear in x and y, and no shear. Bilinear elements contain linear fields exactly, so a consistent solver must reproduce that state on any mesh, however uneven — to round-off, not approximately. Anything else is a bug.",
                  "Tegangan seragam dalam plat memberi stress malar, displacement linear dalam x dan y, dan tiada shear. Element bilinear mengandungi field linear dengan tepat, jadi solver yang konsisten mesti menghasilkan semula keadaan itu pada sebarang mesh, betapa tidak sekata sekalipun — hingga round-off, bukan lebih kurang. Selain itu ialah pepijat.")
            + PLAN("k<sub>11</sub> closed form → edge loads → exact field → stresses → ΣR against σ<sub>0</sub>tH → each bug against each check.")
            + XSTEP(1, "(a) One element against the hand calculation", "(a) Satu element berbanding pengiraan tangan", 3, A.eq("p6_k11")
                    + ANS("(a) k<sub>11</sub> = 0.8753 × 10⁶ N m<sup>−1</sup> — the s<sub>1</sub> = 0.875 of the text’s cantilever. Compare the whole first row, not one entry: it must also add up to zero in u."))
            + XSTEP(2, "(b) Loads and the exact solution", "(b) Load dan penyelesaian tepat", 4, A.eq("x4_loads") + A.eq("x4_exact"))
            + XSTEP(3, "(b) Stresses and reactions", "(b) Stress dan reaction", 3, P("σ<sub>xx</sub> = 1000, σ<sub>yy</sub> = 0, σ<sub>xy</sub> = 0 kN m<sup>−2</sup> at every point of every element — centroid and corners alike. The course element routine, assembled on this patch, reproduces u and v to 10<sup>−17</sup> m and these stresses exactly.",
                                                                  "σ<sub>xx</sub> = 1000, σ<sub>yy</sub> = 0, σ<sub>xy</sub> = 0 kN m<sup>−2</sup> pada setiap titik setiap element — centroid dan bucu sama sahaja. Rutin element kursus, di-assemble pada patch ini, menghasilkan semula u dan v hingga 10<sup>−17</sup> m dan stress ini dengan tepat.")
                    + A.eq("x4_R") + ANS("(b) Loads 2000, 5000, 3000 N; u = 0.0100 m on the right edge, v = −0.0015 m on the top; σ = {1000, 0, 0} kN m<sup>−2</sup> everywhere; ΣR<sub>x</sub> = −10 000 N."))
            + XSTEP(4, "(c) The two bugs", "(c) Dua pepijat", 5, A.eq("x4_bug")
                    + P("The load bug doubles every displacement and its reactions still balance its own load vector, −20 000 N: ΣR catches it only when compared with the physical load σ<sub>0</sub>tH = 10 000 N, and the patch’s exact u catches it too. "
                        "The shear bug is invisible here, because σ<sub>xy</sub> = 0 in uniform tension; it is caught at Gate 2, where the cantilever, which carries shear, comes out 11.6% too stiff against Timoshenko.",
                        "Pepijat load menggandakan setiap displacement dan reaction-nya masih mengimbangi vektor load-nya sendiri, −20 000 N: ΣR hanya menangkapnya apabila dibandingkan dengan load fizikal σ<sub>0</sub>tH = 10 000 N, dan u tepat patch juga menangkapnya. "
                        "Pepijat shear tidak kelihatan di sini, kerana σ<sub>xy</sub> = 0 dalam tegangan seragam; ia ditangkap di Gate 2, di mana cantilever, yang membawa shear, menjadi 11.6% terlalu kaku berbanding Timoshenko.")
                    + ANS("(c) Load bug: the patch displacements and ΣR against σ<sub>0</sub>tH (Gate 1). Shear bug: passes Gate 1; caught by the Timoshenko convergence of Gate 2."))
            + INTERP("Each gate proves one thing. One element against the closed form checks the integration of [k]; the patch test checks that element, assembly, loads and supports reproduce a constant-stress state exactly; ΣR against the <i>physical</i> load checks the load bookkeeping. None of them exercises every term — a tension patch never touches the shear modulus — which is why the gates come in sequence and why a bending problem with a known answer follows. "
                     "With an AI-written solver this matters more, not less: the code can look right and pass the checks it happens to exercise. The GenAI log records which gate caught which error.",
                     "Setiap gate membuktikan satu perkara. Satu element berbanding closed form menyemak integration [k]; patch test menyemak bahawa element, assembly, load dan support menghasilkan semula keadaan stress malar dengan tepat; ΣR berbanding load <i>fizikal</i> menyemak catatan load. Tiada satu pun yang menguji setiap term — patch tegangan tidak pernah menyentuh shear modulus — sebab itulah gate datang secara berurutan dan masalah bending dengan jawapan yang diketahui menyusul. "
                     "Dengan solver yang ditulis oleh AI, ini lebih penting, bukan kurang: kod boleh kelihatan betul dan lulus semakan yang kebetulan diujinya. Log GenAI merekod gate mana yang menangkap ralat mana.")
            + SCHEME([("k<sub>11</sub> from the closed form", "k<sub>11</sub> daripada closed form", 3), ("Edge loads and the exact displacements", "Edge load dan displacement tepat", 4), ("Stresses and ΣR against σ<sub>0</sub>tH", "Stress dan ΣR berbanding σ<sub>0</sub>tH", 3), ("Each bug matched to the check that catches it, with the reason", "Setiap pepijat dipadankan dengan semakan yang menangkapnya, bersama sebabnya", 5)], 15))
    X.append(("y4", "Gate 1 for your own solver", "Gate 1 bagi solver anda sendiri", body))
    return X
