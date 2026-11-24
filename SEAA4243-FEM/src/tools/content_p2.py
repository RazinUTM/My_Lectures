"""Content of Part 2 — 2D Heat Transfer (Part 2): Galerkin, element matrices, assembly, solution,
post-processing. Numbers are those of the deck and the companion (verified against fe_core/fe_heat)."""
from sitelib import B, P, LI, OL, H3, DEF, NOTE, OK, STEP, KP, QC, SB, XSTEP, ANS, CHK, PLAN, PIC, INTERP, SCHEME
from content_p1 import MCQ, EXAMPLES_INTRO as _INTRO1

PART = {
    "n": 2, "slug": "02-heat-transfer-2", "deck": "deck_w10", "eqs": ["eqs_w10", "eqs_w9", "eqs_ex"], "figs": ["figs_w10", "figs_w9", "figs_ex"],
    "topic": ("2D Heat Transfer", "2D Heat Transfer"), "part": "Part 2 of 2",
    "title": "2D Heat Transfer — Part 2",
    "sub": ("Galerkin and integration by parts turn the PDE into [k]{T̂}ᵀ = {q} + {b}; the element matrices in closed form, assembly by connectivity, "
            "the known temperatures imposed, and the text’s plate solved by hand and checked against a fine mesh.",
            "Galerkin dan integration by parts menukar PDE kepada [k]{T̂}ᵀ = {q} + {b}; matrix element dalam closed form, assembly mengikut connectivity, "
            "temperature yang diketahui dikenakan, dan plat dalam teks diselesaikan secara tangan dan disemak dengan mesh halus."),
    "pdf": "pdf/heat-transfer-2-slides.pdf",
    "lab": {"id": "heat", "file": "../labs/heat.html", "name": "Heat Conduction Explorer", "inclass": "book2"},
    "minutes": {"n1": 9, "n2": 10, "n3": 6, "n4": 11, "n5": 9, "n6": 5},
    "target_min": 35,
    "code": "heat",
    "textref": "§2.2.2–§2.4",
    "covers": ("Part 1 gave the PDE and the element; this part turns them into numbers. The Galerkin weighted residual and integration by parts give [k]{T̂}ᵀ = {q} + {b}; the element matrices are evaluated in closed form, assembled through a connectivity table, the known temperatures are imposed, and the text’s plate is solved by hand and checked against a refined mesh. Plane stress reuses every one of these steps with two unknowns per node.",
               "Part 1 memberi PDE dan element; bahagian ini menukarkannya kepada nombor. Galerkin weighted residual dan integration by parts memberi [k]{T̂}ᵀ = {q} + {b}; matrix element dinilai dalam closed form, di-assemble melalui connectivity table, temperature yang diketahui dikenakan, dan plat dalam teks diselesaikan secara tangan dan disemak dengan mesh yang di-refine. Plane stress menggunakan semula setiap langkah ini dengan dua unknown setiap node."),
    "inclass_n": ("3 h · 6 activities", "3 jam · 6 aktiviti"),
    "inclass": [("A1 the boundary term · A2 [k] and {q}", "A1 boundary term · A2 [k] dan {q}"),
                ("A3 connectivity · A4 assembly · A5 verification", "A3 connectivity · A4 assembly · A5 pengesahan"),
                ("A6 temperature at (0.3, 0.2) m", "A6 temperature pada (0.3, 0.2) m")],
    "recall_title": ("Recall from Part 1", "Ingat semula Part 1"),
}

OUTCOMES = [
    ("Apply the Galerkin weighted residual method and integration by parts to obtain [k]{T̂}ᵀ = {q} + {b} and explain what each term means.",
     "Menggunakan Galerkin weighted residual method dan integration by parts untuk memperoleh [k]{T̂}ᵀ = {q} + {b} dan menerangkan maksud setiap term."),
    ("Evaluate the conductance matrix [k] and the load vectors {q} and {b} of a 4-node rectangular element in closed form.",
     "Menilai conductance matrix [k] dan load vector {q} dan {b} bagi 4-node rectangular element dalam closed form."),
    ("Assemble element matrices into the global system with a connectivity table and impose Dirichlet conditions by row–column elimination.",
     "Meng-assemble matrix element ke dalam sistem global dengan connectivity table dan mengenakan Dirichlet condition melalui row–column elimination."),
    ("Solve a small problem by hand, post-process temperature and flux at a point, and judge the result against a refined mesh.",
     "Menyelesaikan masalah kecil secara tangan, post-process temperature dan flux pada satu titik, dan menilai hasilnya berbanding mesh yang di-refine."),
]

CANDO = [
    ("Write the weighted residual, integrate by parts, and name [k], {q} and {b}.", "Menulis weighted residual, integrate by parts, dan menamakan [k], {q} dan {b}."),
    ("Compute s<sub>1</sub>…s<sub>4</sub> for any a, b, k<sub>x</sub>, k<sub>y</sub> and check a row.", "Mengira s<sub>1</sub>…s<sub>4</sub> untuk sebarang a, b, k<sub>x</sub>, k<sub>y</sub> dan menyemak satu baris."),
    ("Assemble a small mesh from a connectivity table and impose known temperatures.", "Meng-assemble mesh kecil daripada connectivity table dan mengenakan temperature yang diketahui."),
    ("Convert a global point to local coordinates and interpolate T and the flux.", "Menukar titik global kepada koordinat local dan interpolate T serta flux."),
]


def notes(A):
    S = []
    # ---- n1: Galerkin and integration by parts ----
    body = (
        P("Substitute the approximation T = {N}{T̂}ᵀ of Part 1 into the PDE and it does not balance: a bilinear field cannot satisfy a second-order equation at every point. "
          "The residual is what is left over. Four unknowns T̂<sub>1</sub>…T̂<sub>4</sub>, one equation, and it holds nowhere exactly.",
          "Gantikan approximation T = {N}{T̂}ᵀ dari Part 1 ke dalam PDE dan ia tidak seimbang: field bilinear tidak mampu memenuhi persamaan peringkat kedua pada setiap titik. "
          "Residual ialah apa yang tinggal. Empat unknown T̂<sub>1</sub>…T̂<sub>4</sub>, satu persamaan, dan ia tidak dipenuhi dengan tepat di mana-mana.")
        + A.eq("w_resid", "(2.34)")
        + DEF("Galerkin’s idea", "Idea Galerkin", "Ask instead that the residual be zero <i>on average</i>, weighted by each shape function in turn. Four weights, four equations. Galerkin chooses the weights equal to the shape functions, which makes [k] symmetric.",
              "Minta pula supaya residual itu sifar <i>secara purata</i>, di-weight oleh setiap shape function bergilir-gilir. Empat weight function, empat persamaan. Galerkin memilih weight function sama dengan shape function, dan itulah yang menjadikan [k] simetri.")
        + A.eq("w_weighted", "(2.35)")
        + H3("Integration by parts: the 1D case you know", "Integration by parts: kes 1D yang anda kenal")
        + SB(P("For the bar element earlier in the course, one derivative moved from T onto the weight and a boundary term appeared:", "Bagi bar element pada awal kursus, satu derivative berpindah dari T kepada weight function dan satu boundary term muncul:"))
        + A.eq("w_ibp1d")
        + SB(LI([("<b>Purpose 1 · relax continuity.</b> After the integration by parts only first derivatives of N and T appear, so a bilinear T is admissible. Its second derivatives would be zero or undefined at element edges.",
                  "<b>Tujuan 1 · melonggarkan continuity.</b> Selepas integration by parts hanya derivative pertama N dan T yang muncul, jadi T bilinear boleh diterima. Derivative keduanya akan sifar atau tak tertakrif di tepi element."),
                 ("<b>Purpose 2 · expose the natural condition.</b> The boundary term contains k ∂T/∂n, the flux. Where the flux is specified it becomes a load; where it is zero it vanishes; where T is specified the term is removed with the equation.",
                  "<b>Tujuan 2 · mendedahkan natural condition.</b> Boundary term mengandungi k ∂T/∂n, iaitu flux. Di mana flux ditetapkan ia menjadi load; di mana ia sifar ia lenyap; di mana T ditetapkan term itu dibuang bersama persamaannya.")]))
        + H3("Two dimensions: Green’s theorem", "Dua dimensi: teorem Green")
        + SB(P("The same move in two dimensions is Green’s theorem: the area integral of a derivative becomes a boundary integral minus an area integral with the derivative on the weight.",
               "Langkah yang sama dalam dua dimensi ialah teorem Green: integral luas bagi satu derivative menjadi integral sempadan tolak integral luas dengan derivative pada weight function."))
        + A.eq("w_green") + A.eq("w_ibp", "(2.36)")
        + H3("Rearrange and name the terms", "Susun semula dan namakan term")
        + A.eq("w_rearr", "(2.37)")
        + A.eq("w_qb") + A.eq("w_sys", "(2.42)")
        + '<div class="tbl"><table><tr><th>' + B("Term", "Term") + '</th><th>' + B("Name", "Nama") + '</th><th>' + B("What it holds", "Apa yang dikandunginya") + '</th></tr>'
        + '<tr><td>[k]</td><td>' + B("conductance matrix", "conductance matrix") + '</td><td>' + B("the material and the geometry of the element; symmetric; 4 × 4", "bahan dan geometri element; simetri; 4 × 4") + '</td></tr>'
        + '<tr><td>{q}</td><td>' + B("source vector", "source vector") + '</td><td>' + B("the heat generated inside the element, shared among its nodes", "haba yang dijana di dalam element, dikongsi antara node-nya") + '</td></tr>'
        + '<tr><td>{b}</td><td>' + B("boundary vector", "boundary vector") + '</td><td>' + B("the heat entering through edges with a known flux; zero on insulated edges; discarded with the equation on Dirichlet edges", "haba yang masuk melalui tepi dengan flux diketahui; sifar pada tepi insulated; dibuang bersama persamaan pada tepi Dirichlet") + '</td></tr></table></div>'
        + NOTE("Which edges contribute to {b}?", "Tepi mana yang menyumbang kepada {b}?",
               "For the text’s plate (top and left at 0 °C, right and bottom insulated): none. The insulated edges have q<sub>b</sub> = 0, and on the two Dirichlet edges the unknown flux multiplies the N<sub>i</sub> of nodes whose equations we discard when T is imposed. The flux there can be recovered afterwards, like a support reaction.",
               "Bagi plat dalam teks (atas dan kiri pada 0 °C, kanan dan bawah insulated): tiada. Tepi insulated ada q<sub>b</sub> = 0, dan pada dua tepi Dirichlet flux yang tidak diketahui mendarab N<sub>i</sub> bagi node yang persamaannya kita buang apabila T dikenakan. Flux di situ boleh diperoleh semula kemudian, seperti support reaction.")
        + KP([("Galerkin: weighted residual with the shape functions as weights; integration by parts lowers the derivative order and exposes the natural condition.", "Galerkin: weighted residual dengan shape function sebagai weight function; integration by parts merendahkan peringkat derivative dan mendedahkan natural condition."),
              ("[k]{T̂}ᵀ = {q} + {b} = {r}: conductance matrix, source vector, boundary vector.", "[k]{T̂}ᵀ = {q} + {b} = {r}: conductance matrix, source vector, boundary vector."),
              ("One 4-node element gives 4 equations; the 2 × 2 mesh gives 9, and 4 remain after T is imposed on 5 nodes.", "Satu 4-node element memberi 4 persamaan; mesh 2 × 2 memberi 9, dan 4 tinggal selepas T dikenakan pada 5 node.")])
        + QC("q1", "In the Galerkin method the weighting functions are", "Dalam kaedah Galerkin, weighting function ialah",
             [("a", "the shape functions themselves", "shape function itu sendiri"), ("b", "the constants 1, x, x²", "pemalar 1, x, x²"), ("c", "the nodal temperatures", "nodal temperature")],
             "a", "Galerkin takes the weights equal to the trial functions, so the equations come out symmetric. Weights 1, x, x² give a Petrov–Galerkin (basic WRM) system that is not symmetric.",
             "Galerkin mengambil weight function sama dengan trial function, jadi persamaannya simetri. Pemberat 1, x, x² memberi sistem Petrov–Galerkin (WRM asas) yang tidak simetri.")
    )
    S.append(("n1", "Galerkin and integration by parts", "Galerkin dan integration by parts", body))

    # ---- n2: the element matrix and loads ----
    body = (
        P("The matrix product inside [k] is best read from the inside out. Take the entry k<sub>34</sub>: shape function 3 on the left, shape function 4 on the right, and the operator acting on each.",
          "Hasil darab matrix di dalam [k] paling mudah dibaca dari dalam ke luar. Ambil entri k<sub>34</sub>: shape function 3 di kiri, shape function 4 di kanan, dan operator bertindak ke atas setiap satu.")
        + STEP("k₃₄ in four symbolic steps (text (2.43)–(2.46))", "k₃₄ dalam empat langkah simbolik (teks (2.43)–(2.46))",
               A.eq("w_s1") + A.eq("w_s2") + A.eq("w_s3") + A.eq("w_s4")
               + P("Each operator acts on the shape function to its left (from the integration by parts) or to its right. The result is a sum of two products of derivatives, one weighted by k<sub>x</sub> and one by k<sub>y</sub>.",
                   "Setiap operator bertindak ke atas shape function di kirinya (daripada integration by parts) atau di kanannya. Hasilnya ialah hasil tambah dua hasil darab derivative, satu di-weight oleh k<sub>x</sub> dan satu lagi oleh k<sub>y</sub>."))
        + STEP("Step 5: the integrals (text (2.47)–(2.48))", "Langkah 5: integral (teks (2.47)–(2.48))", A.eq("w_s5") + A.eq("w_s5b") + A.eq("w_k34", "(2.48)"))
        + H3("The whole matrix in four numbers", "Keseluruhan matrix dalam empat nombor")
        + SB(P("Repeat the same integration for the other entries and only four distinct values appear. [k] is symmetric and has the pattern below.",
               "Ulang integration yang sama untuk entri lain dan hanya empat nilai berbeza yang muncul. [k] simetri dan mempunyai pola di bawah."))
        + A.eq("w_kfull", "(2.49)") + A.eq("w_svals")
        + OK("Row-sum check", "Semakan jumlah baris", "s<sub>1</sub> + s<sub>2</sub> + s<sub>3</sub> + s<sub>4</sub> = 0 for every a, b, k<sub>x</sub>, k<sub>y</sub>: a uniform temperature conducts no heat. Add up any row of a matrix you compute; if it is not zero, look for the slip.",
             "s<sub>1</sub> + s<sub>2</sub> + s<sub>3</sub> + s<sub>4</sub> = 0 bagi setiap a, b, k<sub>x</sub>, k<sub>y</sub>: temperature seragam tidak mengalirkan haba. Jumlahkan mana-mana baris matrix yang anda kira; jika bukan sifar, cari kesilapannya.")
        + A.eq("w_rowsum")
        + NOTE("The usual trap", "Perangkap biasa", "b/a and a/b swapped. In s<sub>2</sub> and s<sub>4</sub> the k<sub>x</sub> term carries b/a (the two nodes of a horizontal side) and the k<sub>y</sub> term a/b. For a square the matrix depends only on k, not on the side.",
               "b/a dan a/b tertukar. Dalam s<sub>2</sub> dan s<sub>4</sub>, term k<sub>x</sub> membawa b/a (dua node pada sisi mendatar) dan term k<sub>y</sub> membawa a/b. Bagi segi empat sama, matrix bergantung pada k sahaja, bukan pada sisinya.")
        + H3("The load vectors", "Load vector")
        + SB(P("A uniform source is shared equally among the four nodes, because every N<sub>i</sub> has the same integral ab/4 over the element. A uniform inward flux on an edge is shared equally by the two nodes of that edge, because along the edge only their shape functions are non-zero and each integrates to half the length.",
               "Source yang seragam dikongsi sama rata antara empat node, kerana setiap N<sub>i</sub> mempunyai integral yang sama ab/4 di atas element. Flux ke dalam yang seragam pada satu tepi dikongsi sama rata oleh dua node tepi itu, kerana di sepanjang tepi hanya shape function mereka yang bukan sifar dan setiap satu ber-integral kepada separuh panjang."))
        + A.eq("w_qconst", "(2.39)") + A.eq("w_bedge", "(2.40)")
        + A.fig("fig_edge_flux", "A uniform inward flux on the right edge becomes two equal nodal loads q<sub>b</sub>b/2 at nodes 2 and 3.", "Flux ke dalam yang seragam pada tepi kanan menjadi dua nodal load yang sama q<sub>b</sub>b/2 pada node 2 dan 3.", 420)
        + STEP("Worked example · the text’s element (Activity 2)", "Contoh bekerja · element dalam teks (Aktiviti 2)",
               P("a = b = 0.5 m, k<sub>x</sub> = k<sub>y</sub> = 300 W m<sup>−1</sup> K<sup>−1</sup>, q<sub>h</sub> = 600 W m<sup>−3</sup>, unit thickness.", "a = b = 0.5 m, k<sub>x</sub> = k<sub>y</sub> = 300 W m<sup>−1</sup> K<sup>−1</sup>, q<sub>h</sub> = 600 W m<sup>−3</sup>, ketebalan unit.")
               + A.eq("w_act2") + A.eq("w_k251", "(2.51)") + A.eq("w_r252", "(2.52)")
               + P("All four elements of the 2 × 2 mesh are identical, so one [k] and one {r} serve the whole mesh. Row check: 200 − 50 − 100 − 50 = 0.", "Keempat-empat element mesh 2 × 2 serupa, jadi satu [k] dan satu {r} mencukupi untuk seluruh mesh. Semakan baris: 200 − 50 − 100 − 50 = 0."))
        + KP([("[k] = t[s<sub>1</sub> s<sub>2</sub> s<sub>3</sub> s<sub>4</sub>; …] with s<sub>1</sub> = bk<sub>x</sub>/3a + ak<sub>y</sub>/3b and the three others of (2.49); rows sum to zero.", "[k] = t[s<sub>1</sub> s<sub>2</sub> s<sub>3</sub> s<sub>4</sub>; …] dengan s<sub>1</sub> = bk<sub>x</sub>/3a + ak<sub>y</sub>/3b dan tiga yang lain daripada (2.49); baris berjumlah sifar."),
              ("{q} = q<sub>h</sub>ab/4 at each node; an edge flux gives q<sub>b</sub>b/2 at each of its two nodes.", "{q} = q<sub>h</sub>ab/4 pada setiap node; flux tepi memberi q<sub>b</sub>b/2 pada setiap satu daripada dua node-nya."),
              ("Text element: s = 200, −50, −100, −50 W K<sup>−1</sup>; r<sub>i</sub> = 37.5 W.", "Element dalam teks: s = 200, −50, −100, −50 W K<sup>−1</sup>; r<sub>i</sub> = 37.5 W.")])
        + QC("q2", "For a square element with k<sub>x</sub> = k<sub>y</sub> = k, the coupling between the two nodes of one side, s<sub>2</sub>, is", "Bagi element segi empat sama dengan k<sub>x</sub> = k<sub>y</sub> = k, gandingan antara dua node satu sisi, s<sub>2</sub>, ialah",
             [("a", "−k/6", "−k/6"), ("b", "−k/3", "−k/3"), ("c", "+k/6", "+k/6")],
             "a", "s<sub>2</sub> = −bk/3a + ak/6b = −k/3 + k/6 = −k/6. The diagonal pair is s<sub>3</sub> = −k/3, twice as strong, and s<sub>1</sub> = 2k/3.",
             "s<sub>2</sub> = −bk/3a + ak/6b = −k/3 + k/6 = −k/6. Pasangan pepenjuru ialah s<sub>3</sub> = −k/3, dua kali lebih kuat, dan s<sub>1</sub> = 2k/3.")
    )
    S.append(("n2", "The element matrix and the load vectors", "Matrix element dan load vector", body))

    # ---- n3: the worked example and connectivity ----
    body = (
        P("The text’s plate: 1 m square, q<sub>h</sub> = 600 W m<sup>−3</sup>, k = 300 W m<sup>−1</sup> K<sup>−1</sup>, top and left edges at 0 °C, right and bottom insulated. Four elements, nine global nodes, numbered left to right and bottom to top like the loops of the code. Coarse on purpose: the hand calculation must be traceable.",
          "Plat dalam teks: segi empat sama 1 m, q<sub>h</sub> = 600 W m<sup>−3</sup>, k = 300 W m<sup>−1</sup> K<sup>−1</sup>, tepi atas dan kiri pada 0 °C, kanan dan bawah insulated. Empat element, sembilan node global, dinomborkan dari kiri ke kanan dan bawah ke atas seperti gelung dalam kod. Kasar dengan sengaja: pengiraan tangan mesti boleh dijejak.")
        + '<div class="figrow">' + A.fig("fig_plate_book", "The plate (text Fig. 2.5).", "Plat (teks Rajah 2.5).", 300) + A.fig("fig_mesh_e1", "Element 1 shaded; its local nodes (1)…(4) sit at global nodes 1, 2, 5, 4.", "Element 1 berlorek; node local-nya (1)…(4) berada pada node global 1, 2, 5, 4.", 330) + '</div>'
        + H3("The connectivity table", "Connectivity table")
        + SB(P("Each element lists its global node numbers in local order, anticlockwise from its bottom-left corner. This table is the whole bookkeeping of the method.",
               "Setiap element menyenaraikan nombor node global-nya mengikut susunan local, lawan jam dari bucu kiri bawah. Jadual inilah keseluruhan rekod kaedah ini."))
        + '<div class="tbl"><table><tr><th>' + B("Element", "Element") + '</th><th>(1)</th><th>(2)</th><th>(3)</th><th>(4)</th></tr>'
        + '<tr><td>1</td><td>1</td><td>2</td><td>5</td><td>4</td></tr><tr><td>2</td><td>2</td><td>3</td><td>6</td><td>5</td></tr><tr><td>3</td><td>4</td><td>5</td><td>8</td><td>7</td></tr><tr><td>4</td><td>5</td><td>6</td><td>9</td><td>8</td></tr></table></div>'
        + A.fig("fig_mesh_e2", "Element 2 shaded: local (1)…(4) at global 2, 3, 6, 5.", "Element 2 berlorek: local (1)…(4) pada global 2, 3, 6, 5.", 330)
        + NOTE("Reading the table", "Membaca jadual", "Node 5 appears in all four elements, so four element matrices add into row 5 of [K]: K<sub>55</sub> = 4s<sub>1</sub>. Node 2 appears in elements 1 and 2: K<sub>22</sub> = 2s<sub>1</sub>. A corner node appears once: K<sub>11</sub> = s<sub>1</sub>.",
               "Node 5 muncul dalam keempat-empat element, jadi empat matrix element ditambah ke dalam baris 5 [K]: K<sub>55</sub> = 4s<sub>1</sub>. Node 2 muncul dalam element 1 dan 2: K<sub>22</sub> = 2s<sub>1</sub>. Node bucu muncul sekali: K<sub>11</sub> = s<sub>1</sub>.")
        + STEP("Counting the equations", "Mengira persamaan", P("Nine nodes give nine equations. The top edge (nodes 7, 8, 9) and the left edge (nodes 1, 4, 7) are at 0 °C: five known temperatures, so four equations remain, for T<sub>2</sub>, T<sub>3</sub>, T<sub>5</sub>, T<sub>6</sub>.",
                                                              "Sembilan node memberi sembilan persamaan. Tepi atas (node 7, 8, 9) dan tepi kiri (node 1, 4, 7) berada pada 0 °C: lima temperature diketahui, jadi empat persamaan tinggal, bagi T<sub>2</sub>, T<sub>3</sub>, T<sub>5</sub>, T<sub>6</sub>."))
        + KP([("Connectivity: global node numbers of each element in local anticlockwise order.", "Connectivity: nombor node global setiap element mengikut susunan local lawan jam."),
              ("K<sub>ii</sub> = s<sub>1</sub> × (number of elements at node i); a shared side adds twice.", "K<sub>ii</sub> = s<sub>1</sub> × (bilangan element pada node i); sisi yang dikongsi menambah dua kali."),
              ("Text plate: 9 equations, 5 known temperatures, 4 unknowns.", "Plat teks: 9 persamaan, 5 temperature diketahui, 4 unknown.")])
        + QC("q3", "In the 2 × 2 mesh, how many element matrices contribute to K<sub>25</sub> (nodes 2 and 5)?", "Dalam mesh 2 × 2, berapa banyak matrix element yang menyumbang kepada K<sub>25</sub> (node 2 dan 5)?",
             [("a", "one", "satu"), ("b", "two", "dua"), ("c", "four", "empat")],
             "b", "Nodes 2 and 5 are both in elements 1 and 2 (they share the side 2–5), so two matrices add: K<sub>25</sub> = k<sub>23</sub> + k<sub>14</sub> = 2s<sub>4</sub>. Node 5 alone is in four elements, but a coupling counts only the elements that contain both nodes.",
             "Node 2 dan 5 kedua-duanya dalam element 1 dan 2 (berkongsi sisi 2–5), jadi dua matrix ditambah: K<sub>25</sub> = k<sub>23</sub> + k<sub>14</sub> = 2s<sub>4</sub>. Node 5 sahaja berada dalam empat element, tetapi gandingan hanya mengira element yang mengandungi kedua-dua node.")
    )
    S.append(("n3", "The worked example and its connectivity table", "Contoh bekerja dan connectivity table-nya", body))

    # ---- n4: assembly and Dirichlet ----
    body = (
        P("Assembly is one rule applied many times: every entry of an element matrix is added into the global matrix at the row and column given by the connectivity table. The same scatter-add builds {R} from the element load vectors.",
          "Assembly ialah satu peraturan yang digunakan berkali-kali: setiap entri matrix element ditambah ke dalam matrix global pada baris dan lajur yang diberi oleh connectivity table. Scatter-add yang sama membina {R} daripada load vector element.")
        + A.eq("w_scatter")
        + STEP("After element 1 (nodes 1, 2, 5, 4)", "Selepas element 1 (node 1, 2, 5, 4)", A.eq("w_K_e1") + P("Sixteen entries land in rows and columns 1, 2, 4, 5. Everything else is still zero.", "Enam belas entri mendarat di baris dan lajur 1, 2, 4, 5. Yang lain masih sifar."))
        + STEP("After elements 1 and 2 (Activity 4)", "Selepas element 1 dan 2 (Aktiviti 4)", A.eq("w_K_e12") + P("Element 2 adds into rows and columns 2, 3, 6, 5. Where the two overlap (nodes 2 and 5, shown in green) the entries add: K<sub>22</sub> = 400, K<sub>55</sub> = 400 so far, K<sub>25</sub> = −100.",
                                                                                                                "Element 2 ditambah ke dalam baris dan lajur 2, 3, 6, 5. Di mana kedua-duanya bertindih (node 2 dan 5, ditunjukkan hijau) entri bertambah: K<sub>22</sub> = 400, K<sub>55</sub> = 400 setakat ini, K<sub>25</sub> = −100."))
        + STEP("The complete system (text (2.53))", "Sistem lengkap (teks (2.53))", A.eq("w_K_full", "(2.53)") + P("K<sub>55</sub> = 800 (four elements), the side nodes 400, the corners 200; {R} = 37.5 × (1, 2, 1, 2, 4, 2, 1, 2, 1) W.",
                                                                                                "K<sub>55</sub> = 800 (empat element), node sisi 400, bucu 200; {R} = 37.5 × (1, 2, 1, 2, 4, 2, 1, 2, 1) W."))
        + H3("Impose the known temperatures", "Kenakan temperature yang diketahui")
        + SB(P("A known T̄<sub>k</sub> is not an unknown, so its equation is not needed and its column multiplies a known number. Move that column times T̄<sub>k</sub> to the right-hand side, then delete the row and the column. Here all five known values are zero, so nothing moves to the right and the reduced system is simply rows and columns 2, 3, 5, 6.",
               "T̄<sub>k</sub> yang diketahui bukan unknown, jadi persamaannya tidak diperlukan dan lajurnya mendarab nombor yang diketahui. Pindahkan lajur itu kali T̄<sub>k</sub> ke sebelah kanan, kemudian buang baris dan lajur itu. Di sini kelima-lima nilai yang diketahui ialah sifar, jadi tiada yang berpindah ke kanan dan sistem terkurang hanyalah baris dan lajur 2, 3, 5, 6."))
        + A.eq("w_nonzero") + A.eq("w_reduced", "(2.54)–(2.55)")
        + A.fig("fig_mesh_T", "The solved nodal temperatures at the free nodes 2, 3, 5 and 6.", "Nodal temperature yang diselesaikan pada node bebas 2, 3, 5 dan 6.", 360)
        + STEP("Verify and read the solution (Activity 5)", "Sahkan dan baca penyelesaian (Aktiviti 5)",
               A.eq("w_act5") + LI([("T<sub>3</sub> is the largest: the corner farthest from both cold edges, between the two insulated edges, where heat accumulates.", "T<sub>3</sub> paling besar: bucu paling jauh daripada kedua-dua tepi sejuk, antara dua tepi insulated, tempat haba terkumpul."),
                                    ("T<sub>5</sub> is the smallest of the four: the centre is closer to the cold edges than node 3.", "T<sub>5</sub> paling kecil antara empat: pusat lebih hampir dengan tepi sejuk berbanding node 3."),
                                    ("T<sub>2</sub> = T<sub>6</sub> exactly: the mesh, loads and boundary conditions are symmetric about the diagonal from node 1 to node 9.", "T<sub>2</sub> = T<sub>6</sub> dengan tepat: mesh, load dan boundary condition simetri tentang pepenjuru dari node 1 ke node 9.")]))
        + KP([("Scatter-add: K<sub>IJ</sub> += k<sub>ij</sub> with I, J from the connectivity table; same for {R}.", "Scatter-add: K<sub>IJ</sub> += k<sub>ij</sub> dengan I, J daripada connectivity table; sama untuk {R}."),
              ("Known T: move its column × T̄ to the right, delete row and column; the struck rows later give the heat flows.", "T yang diketahui: pindahkan lajurnya × T̄ ke kanan, buang baris dan lajur; baris yang dibuang kemudian memberi aliran haba."),
              ("Text plate: T<sub>2</sub> = T<sub>6</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386 °C.", "Plat teks: T<sub>2</sub> = T<sub>6</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386 °C.")])
        + QC("q4", "A node has a prescribed temperature of 100 K. When the system is reduced, the column of that node", "Satu node mempunyai temperature yang ditetapkan 100 K. Apabila sistem dikurangkan, lajur node itu",
             [("a", "is deleted and nothing else changes", "dibuang dan tiada yang lain berubah"), ("b", "times 100 is subtracted from the right-hand side of every remaining equation, then deleted", "kali 100 ditolak daripada sebelah kanan setiap persamaan yang tinggal, kemudian dibuang"), ("c", "is replaced by zeros and the diagonal set to 1", "digantikan dengan sifar dan pepenjuru ditetapkan 1")],
             "b", "The column multiplies a known value, so its product K<sub>ik</sub> × 100 is a known number in every remaining equation and moves to the right-hand side. Only when the prescribed value is zero does nothing move. Option (c) is a valid computer trick but is not the hand method of this course.",
             "Lajur itu mendarab nilai yang diketahui, jadi hasil darabnya K<sub>ik</sub> × 100 ialah nombor yang diketahui dalam setiap persamaan yang tinggal dan berpindah ke sebelah kanan. Hanya apabila nilai yang ditetapkan ialah sifar, tiada yang berpindah. Pilihan (c) ialah helah komputer yang sah tetapi bukan kaedah tangan kursus ini.")
    )
    S.append(("n4", "Assembly and the known temperatures", "Assembly dan temperature yang diketahui", body))

    # ---- n5: post-processing and accuracy ----
    body = (
        P("The solution is a list of nodal values. Everything else — the temperature at a point, the flux, the hottest spot — is post-processing with the shape functions of Part 1, done one element at a time in that element’s local coordinates.",
          "Penyelesaian ialah senarai nilai node. Segala yang lain — temperature pada satu titik, flux, titik paling panas — ialah post-processing dengan shape function Part 1, dibuat satu element pada satu masa dalam koordinat local element itu.")
        + STEP("Temperature at any point: three steps", "Temperature pada mana-mana titik: tiga langkah",
               OL([("Find the element that contains the point.", "Cari element yang mengandungi titik itu."), ("Convert to local coordinates: subtract the element’s origin (its local node 1).", "Tukar kepada koordinat local: tolak origin element (node local 1-nya)."), ("Evaluate N<sub>1</sub>…N<sub>4</sub> there and multiply by the element’s nodal temperatures, in local order from the connectivity table.", "Nilaikan N<sub>1</sub>…N<sub>4</sub> di situ dan darab dengan nodal temperature element itu, mengikut susunan local daripada connectivity table.")])
               + A.eq("w_local") + A.eq("w_interp"))
        + A.fig("fig_mesh_point", "The point (0.3, 0.2) m lies in element 1.", "Titik (0.3, 0.2) m terletak dalam element 1.", 330)
        + STEP("Worked example · T at (0.3, 0.2) (Activity 6, the assignment pattern)", "Contoh bekerja · T pada (0.3, 0.2) (Aktiviti 6, pola tugasan)",
               A.eq("w_act6_N") + A.eq("w_act6_T")
               + P("Element 1 has node 1 at the origin, so local = global here. For the point (0.8, 0.2) the element would be 2, with local (0.3, 0.2) — the same N — but the nodal values {T<sub>2</sub>, T<sub>3</sub>, T<sub>6</sub>, T<sub>5</sub>}.",
                   "Element 1 mempunyai node 1 pada origin, jadi local = global di sini. Bagi titik (0.8, 0.2) element-nya ialah 2, dengan local (0.3, 0.2) — N yang sama — tetapi nilai node {T<sub>2</sub>, T<sub>3</sub>, T<sub>6</sub>, T<sub>5</sub>}."))
        + H3("Flux at a point", "Flux pada satu titik")
        + A.eq("w_fluxc")
        + SB(P("At the centroid of element 2 the flux has equal and opposite components: heat flows towards −x (the cold left edge) and +y (the cold top edge). Evaluate the flux at centroids or Gauss points; it is least accurate at nodes and jumps across element edges.",
               "Pada centroid element 2, flux mempunyai komponen yang sama dan bertentangan: haba mengalir ke arah −x (tepi kiri sejuk) dan +y (tepi atas sejuk). Nilaikan flux pada centroid atau titik Gauss; ia paling kurang tepat pada node dan melompat merentasi tepi element."))
        + H3("How wrong is a 2 × 2 mesh?", "Berapa salah mesh 2 × 2?")
        + '<div class="tbl"><table><tr><th>' + B("Mesh", "Mesh") + '</th><th class="r">T(L/2, 0)</th><th class="r">T(L, 0)</th></tr>'
        + '<tr><td>Q4 2 × 2 (' + B("hand", "tangan") + ')</td><td class="r num">0.4821</td><td class="r num">0.6214</td></tr><tr><td>Q8 2 × 1 (' + B("hand", "tangan") + ')</td><td class="r num">0.4448</td><td class="r num">0.5836</td></tr>'
        + '<tr><td>Q4 16 × 16</td><td class="r num">0.4590</td><td class="r num">0.5898</td></tr><tr><td>' + B("Software (text Table 2.1)", "Perisian (teks Jadual 2.1)") + '</td><td class="r num">0.4589</td><td class="r num">0.5897</td></tr></table></div>'
        + A.eq("w_err")
        + '<figure><img src="slides/img/fig_contours.png" alt="Temperature contours of the plate on the 2 by 2 mesh, faceted, and on a 16 by 16 mesh, smooth" class="figimg" style="width:min(640px,100%)"><figcaption>' + B("Left: the 2 × 2 solution is faceted because each element is bilinear. Right: 16 × 16 is smooth and matches the text’s software value to the fourth decimal.", "Kiri: penyelesaian 2 × 2 berfaset kerana setiap element bilinear. Kanan: 16 × 16 licin dan sepadan dengan nilai perisian dalam teks hingga tempat perpuluhan keempat.") + '</figcaption></figure>'
        + OK("The habit of the course", "Tabiat kursus ini", "A convergence check is the same problem on a finer mesh; refine until the answer stops moving, and show the table. The error of bilinear elements falls about four times each time the mesh is halved.",
             "Semakan convergence ialah masalah yang sama pada mesh yang lebih halus; refine sehingga jawapan berhenti berubah, dan tunjukkan jadualnya. Ralat element bilinear jatuh kira-kira empat kali setiap kali mesh dibahagi dua.")
        + '<div class="figrow"><img src="slides/img/w10_aster.png" alt="Temperature in a solid plate computed with Code_Aster, shown in Gmsh" class="figimg" style="flex:1 1 300px"><img src="slides/img/w10_mapdl_thermal.png" alt="ANSYS MAPDL nodal temperature in a plate held at 5 and 100 degrees on two opposite faces" class="figimg" style="flex:1 1 300px"></div>'
        + '<p class="credit">' + B("Other codes, the same equations. Left: Code_Aster, preCICE tutorials “Flow over a heated plate, steady state”, LGPL-3.0. Right: ANSYS MAPDL, PyMAPDL documentation “Basic thermal analysis”, © ANSYS, Inc., MIT licence. With no source and two fixed faces the solution is linear and any mesh reproduces it exactly: a quick check of any new model.",
                                   "Kod lain, persamaan yang sama. Kiri: Code_Aster, tutorial preCICE “Flow over a heated plate, steady state”, LGPL-3.0. Kanan: ANSYS MAPDL, dokumentasi PyMAPDL “Basic thermal analysis”, © ANSYS, Inc., lesen MIT. Tanpa source dan dengan dua muka tetap, penyelesaiannya linear dan mana-mana mesh menghasilkannya dengan tepat: semakan pantas untuk mana-mana model baharu.") + '</p>'
        + KP([("Post-process per element: locate, convert to local coordinates, interpolate with the nodal values in local order.", "Post-process setiap element: cari, tukar kepada koordinat local, interpolate dengan nilai node mengikut susunan local."),
              ("T(0.3, 0.2) = 0.266 °C; flux at the centroid of element 2 = (−70.7, +70.7) W m<sup>−2</sup>.", "T(0.3, 0.2) = 0.266 °C; flux pada centroid element 2 = (−70.7, +70.7) W m<sup>−2</sup>."),
              ("The 2 × 2 mesh is about 5% high; 16 × 16 matches software. Refine before you believe a number.", "Mesh 2 × 2 kira-kira 5% tinggi; 16 × 16 sepadan dengan perisian. Refine sebelum anda percaya sesuatu nombor.")])
        + QC("q5", "The point (0.8, 0.2) m in the text’s 2 × 2 mesh (a = b = 0.5 m) lies in element 2. Its local coordinates are", "Titik (0.8, 0.2) m dalam mesh 2 × 2 teks (a = b = 0.5 m) terletak dalam element 2. Koordinat local-nya ialah",
             [("a", "(0.8, 0.2)", "(0.8, 0.2)"), ("b", "(0.3, 0.2)", "(0.3, 0.2)"), ("c", "(0.3, 0.7)", "(0.3, 0.7)")],
             "b", "Element 2 has its local node 1 at global (0.5, 0), so x<sub>loc</sub> = 0.8 − 0.5 = 0.3 and y<sub>loc</sub> = 0.2 − 0 = 0.2. Using (0.8, 0.2) in N<sub>i</sub> gives negative shape functions, the usual sign that the coordinates were not converted.",
             "Element 2 mempunyai node local 1 pada global (0.5, 0), jadi x<sub>loc</sub> = 0.8 − 0.5 = 0.3 dan y<sub>loc</sub> = 0.2 − 0 = 0.2. Menggunakan (0.8, 0.2) dalam N<sub>i</sub> memberi shape function negatif, tanda biasa bahawa koordinat tidak ditukar.")
    )
    S.append(("n5", "Post-processing and accuracy", "Post-processing dan ketepatan", body))

    # ---- n6: the script, the assignment and what comes next ----
    code = ["% Local conductance matrix (text §2.3.1)", "a = L/Nx; b = H/Ny;", "s1 = b*kx/(3*a) + a*ky/(3*b);", "s2 = -b*kx/(3*a) + a*ky/(6*b);",
            "s3 = -b*kx/(6*a) - a*ky/(6*b);", "s4 = b*kx/(6*a) - a*ky/(3*b);", "k = [s1 s2 s3 s4; s2 s1 s4 s3; s3 s4 s1 s2; s4 s3 s2 s1];",
            "fQ = a*b*Q/4*[1; 1; 1; 1];        % heat generation", "% Assembly by connectivity (conn(e,:) = global nodes of element e)",
            "for e = 1:Ne,  c = conn(e,:);  K(c,c) = K(c,c) + k;  F(c) = F(c) + fQ;  end", "% Essential conditions: known nodes removed, their columns moved to the right",
            "free = setdiff(1:n, fixed);  T = zeros(n,1);  T(fixed) = Tbar;", "T(free) = K(free,free) \\ (F(free) - K(free,fixed)*T(fixed));",
            "% Post-processing: element, local coordinates, interpolation", "e = find_element(x, y);  xl = x - X(conn(e,1));  yl = y - Y(conn(e,1));",
            "N = [(a-xl)*(b-yl), xl*(b-yl), xl*yl, yl*(a-xl)]/(a*b);  Tp = N*T(conn(e,:));"]
    body = (
        P("The script is the pipeline in thirty lines. Read it against the seven steps and every block has a name.", "Skrip ini ialah pipeline dalam tiga puluh baris. Baca ia berpandukan tujuh langkah dan setiap blok ada namanya.")
        + '<pre class="paper" style="font:13px/1.5 var(--font-num);overflow-x:auto;white-space:pre">' + "\n".join(code) + '</pre>'
        + SB(LI([("Lines 2–8: step 5, the element matrix and load from the closed-form s<sub>1</sub>…s<sub>4</sub> of §2.", "Baris 2–8: langkah 5, matrix element dan load daripada s<sub>1</sub>…s<sub>4</sub> closed-form dalam §2."),
                 ("Line 10: step 6, assembly, one scatter-add per element.", "Baris 10: langkah 6, assembly, satu scatter-add setiap element."),
                 ("Lines 12–13: step 6, the known temperatures moved to the right and struck; step 7, the backslash solve.", "Baris 12–13: langkah 6, temperature yang diketahui dipindahkan ke kanan dan dibuang; langkah 7, penyelesaian backslash."),
                 ("Lines 15–16: §5, interpolation in local coordinates.", "Baris 15–16: §5, interpolation dalam koordinat local.")]))
        + NOTE("Try it", "Cuba", "Change the mesh to 4 × 4 and compare T(1, 0) with the table of §5. Then set Q = 0 and T = 5 on the left and 100 on the right edge: every mesh must return a straight line.",
               "Tukar mesh kepada 4 × 4 dan bandingkan T(1, 0) dengan jadual §5. Kemudian tetapkan Q = 0 dan T = 5 di kiri dan 100 di tepi kanan: setiap mesh mesti memulangkan garis lurus.")
        + H3("Assignment 4 · what is asked", "Tugasan 4 · apa yang diminta")
        + A.fig("fig_assign", "Three identical 2 m × 3 m elements, T = 100 K on the left edge, zero flux elsewhere, a heat source on element 1.", "Tiga element 2 m × 3 m yang serupa, T = 100 K pada tepi kiri, flux sifar di tempat lain, satu heat source pada element 1.", 460)
        + LI([("(a) The local load vector {r¹} for the heat source Q = 20 W m<sup>−2</sup> on element 1 (unit thickness).", "(a) Load vector local {r¹} bagi heat source Q = 20 W m<sup>−2</sup> pada element 1 (ketebalan unit)."),
              ("(b) The global [K] in terms of k, with k<sub>x</sub> = k<sub>y</sub> = k, using the connectivity table of Activity 3.", "(b) [K] global dalam sebutan k, dengan k<sub>x</sub> = k<sub>y</sub> = k, menggunakan connectivity table Aktiviti 3."),
              ("(c) With T<sub>2</sub> = T<sub>6</sub> = 150 K from the solution, interpolate T at (x, y) = (1.4, 2.2) m.", "(c) Dengan T<sub>2</sub> = T<sub>6</sub> = 150 K daripada penyelesaian, interpolate T pada (x, y) = (1.4, 2.2) m.")])
        + A.eq("w_asg_hint")
        + P("Show the connectivity table, s<sub>1</sub>…s<sub>4</sub> with a = 2 m, b = 3 m, and the local coordinates used in (c). Marks are for the method; state the convention you use for the source (per unit area, unit thickness). Individual work.",
            "Tunjukkan connectivity table, s<sub>1</sub>…s<sub>4</sub> dengan a = 2 m, b = 3 m, dan koordinat local yang digunakan dalam (c). Markah diberi untuk kaedah; nyatakan konvensyen yang anda guna untuk source (per unit luas, ketebalan unit). Kerja individu.")
        + H3("What comes next", "Apa yang seterusnya")
        + SB(P("Plane stress repeats every step of this part with two unknowns per node: [E] becomes 3 × 3, {∂} a 2 × 3 operator matrix, and [k] 8 × 8. Before that session, read text §3.1 and revise plane stress versus plane strain, Hooke’s law in 2D and the strain–displacement relations.",
               "Plane stress mengulang setiap langkah bahagian ini dengan dua unknown setiap node: [E] menjadi 3 × 3, {∂} matrix operator 2 × 3, dan [k] 8 × 8. Sebelum sesi itu, baca teks §3.1 dan ulang kaji plane stress berbanding plane strain, hukum Hooke dalam 2D dan hubungan strain–displacement."))
        + KP([("Seven steps, thirty lines: element matrix, scatter-add assembly, strike the known nodes, backslash, interpolate in local coordinates.", "Tujuh langkah, tiga puluh baris: matrix element, assembly scatter-add, buang node yang diketahui, backslash, interpolate dalam koordinat local."),
              ("Assignment 4: {r¹}, [K] in terms of k, T at (1.4, 2.2) — method marks; show the bookkeeping.", "Tugasan 4: {r¹}, [K] dalam sebutan k, T pada (1.4, 2.2) — markah kaedah; tunjukkan rekod.")])
        + QC("q6", "With no heat source and two opposite edges held at fixed temperatures, a 1 × 1 mesh of one bilinear element gives", "Tanpa heat source dan dua tepi bertentangan ditetapkan pada temperature tetap, mesh 1 × 1 dengan satu element bilinear memberi",
             [("a", "the exact linear field", "field linear yang tepat"), ("b", "an answer about 5% high", "jawapan kira-kira 5% tinggi"), ("c", "a singular matrix", "matrix singular")],
             "a", "The exact field is linear in x, and the bilinear element contains 1, x and y, so it reproduces that field exactly on any mesh. This is the patch-test check of §5; the 5% error belongs to the curved field of the plate with a source.",
             "Field tepat adalah linear dalam x, dan element bilinear mengandungi 1, x dan y, jadi ia menghasilkan semula field itu dengan tepat pada mana-mana mesh. Inilah semakan patch-test dalam §5; ralat 5% itu milik field melengkung bagi plat dengan source.")
    )
    S.append(("n6", "The script, the assignment and what comes next", "Skrip, tugasan dan apa yang seterusnya", body))
    return S


RECALL = [
    QC("r1", "Recall · the boundary condition that needs no action in the finite element model is", "Ingat semula · boundary condition yang tidak memerlukan tindakan dalam model finite element ialah",
       [("a", "a prescribed temperature", "temperature yang ditetapkan"), ("b", "an insulated edge", "tepi insulated"), ("c", "a prescribed inward flux", "flux ke dalam yang ditetapkan")],
       "b", "Insulated means q<sub>b</sub> = 0: a natural condition whose boundary term is zero. A prescribed temperature is imposed; a non-zero flux becomes a load in {b}.",
       "Insulated bermaksud q<sub>b</sub> = 0: natural condition yang boundary term-nya sifar. Temperature yang ditetapkan dikenakan; flux bukan sifar menjadi load dalam {b}."),
    QC("r2", "Recall · N<sub>2</sub> = x(b − y)/(ab) at node 3, (a, b), equals", "Ingat semula · N<sub>2</sub> = x(b − y)/(ab) pada node 3, (a, b), bersamaan",
       [("a", "1", "1"), ("b", "0", "0"), ("c", "1/2", "1/2")],
       "b", "N<sub>2</sub>(a, b) = a(b − b)/(ab) = 0: each shape function is 1 at its own node and 0 at the others (Kronecker delta).",
       "N<sub>2</sub>(a, b) = a(b − b)/(ab) = 0: setiap shape function bernilai 1 pada node sendiri dan 0 pada node lain (Kronecker delta)."),
]

QUICK = [
    MCQ("a1", "Integration by parts is applied to the weighted residual mainly in order to", "Integration by parts digunakan pada weighted residual terutamanya untuk",
        [("a", "lower the derivative order so a bilinear T is admissible, and expose the flux boundary term", "merendahkan peringkat derivative supaya T bilinear boleh diterima, dan mendedahkan boundary term flux"), ("b", "make the integrals easier to evaluate numerically", "memudahkan integral dinilai secara berangka"), ("c", "remove the heat-generation term", "membuang term heat generation")], "a",
        "After integration by parts only first derivatives of N and T appear, and the boundary term k ∂T/∂n ds carries the natural condition. Neither the ease of integration nor the source term is the reason.",
        "Selepas integration by parts hanya derivative pertama N dan T yang muncul, dan boundary term k ∂T/∂n ds membawa natural condition. Bukan kemudahan integration mahupun term source yang menjadi sebabnya."),
    MCQ("a2", "For the text’s plate (top and left edges at 0 °C, right and bottom insulated), the boundary vector {b} of every element is", "Bagi plat dalam teks (tepi atas dan kiri pada 0 °C, kanan dan bawah insulated), boundary vector {b} setiap element ialah",
        [("a", "zero", "sifar"), ("b", "q<sub>b</sub>b/2 at the nodes of the cold edges", "q<sub>b</sub>b/2 pada node tepi sejuk"), ("c", "unknown until the system is solved", "tidak diketahui sehingga sistem diselesaikan")], "a",
        "The insulated edges have q<sub>b</sub> = 0. On the cold edges the flux is unknown, but it multiplies the shape functions of nodes whose equations are discarded when T is imposed, so {b} contributes nothing to the equations that are solved.",
        "Tepi insulated mempunyai q<sub>b</sub> = 0. Pada tepi sejuk flux tidak diketahui, tetapi ia mendarab shape function node yang persamaannya dibuang apabila T dikenakan, jadi {b} tidak menyumbang kepada persamaan yang diselesaikan."),
    MCQ("a3", "For an element with a = 2 m, b = 1 m and k<sub>x</sub> = k<sub>y</sub> = k, the entry s<sub>2</sub> is", "Bagi element dengan a = 2 m, b = 1 m dan k<sub>x</sub> = k<sub>y</sub> = k, entri s<sub>2</sub> ialah",
        [("a", "−k/6 + k/3 = +k/6", "−k/6 + k/3 = +k/6"), ("b", "−k/3 + k/6 = −k/6", "−k/3 + k/6 = −k/6"), ("c", "−2k/3 + k/12 = −7k/12", "−2k/3 + k/12 = −7k/12")], "a",
        "s<sub>2</sub> = −bk/(3a) + ak/(6b) = −k/6 + 2k/6 = +k/6. The b/a factor goes with k<sub>x</sub>. An elongated element can have a positive side coupling; a square never does.",
        "s<sub>2</sub> = −bk/(3a) + ak/(6b) = −k/6 + 2k/6 = +k/6. Faktor b/a mengiringi k<sub>x</sub>. Element memanjang boleh mempunyai gandingan sisi positif; segi empat sama tidak pernah."),
    MCQ("a4", "In the 2 × 2 mesh the diagonal entry K<sub>55</sub> of the centre node equals", "Dalam mesh 2 × 2, entri pepenjuru K<sub>55</sub> bagi node pusat bersamaan",
        [("a", "s<sub>1</sub>", "s<sub>1</sub>"), ("b", "2s<sub>1</sub>", "2s<sub>1</sub>"), ("c", "4s<sub>1</sub>", "4s<sub>1</sub>")], "c",
        "Node 5 belongs to all four elements and each adds its own s<sub>1</sub> at that position: 4 × 200 = 800 W K<sup>−1</sup> for the text’s plate.",
        "Node 5 dimiliki oleh keempat-empat element dan setiap satu menambah s<sub>1</sub>-nya sendiri pada kedudukan itu: 4 × 200 = 800 W K<sup>−1</sup> bagi plat dalam teks."),
    MCQ("a5", "The struck rows of a node with a prescribed temperature are useful because they give", "Baris yang dibuang bagi node dengan temperature yang ditetapkan berguna kerana ia memberi",
        [("a", "the heat flowing in or out at that node, for the energy balance", "haba yang mengalir masuk atau keluar pada node itu, untuk energy balance"), ("b", "a second estimate of the unknown temperatures", "anggaran kedua bagi temperature yang tidak diketahui"), ("c", "the error of the mesh", "ralat mesh")], "a",
        "[K]{T} − {R} evaluated in a struck row is the heat the boundary must supply or remove at that node, like a support reaction. Summed over the cold nodes it must balance the heat generated: −600 W for the text’s plate.",
        "[K]{T} − {R} yang dinilai pada baris yang dibuang ialah haba yang mesti dibekalkan atau dikeluarkan oleh sempadan pada node itu, seperti support reaction. Dijumlahkan atas node sejuk ia mesti mengimbangi haba yang dijana: −600 W bagi plat dalam teks."),
    MCQ("a6", "Refining the text’s mesh from 2 × 2 to 4 × 4 changes T(1, 0) from 0.6214 to 0.5968 °C (exact 0.5894). Halving the mesh again should leave an error of about", "Menghalusi mesh teks dari 2 × 2 kepada 4 × 4 mengubah T(1, 0) dari 0.6214 kepada 0.5968 °C (tepat 0.5894). Membahagi dua mesh sekali lagi sepatutnya meninggalkan ralat kira-kira",
        [("a", "0.0037 °C, a quarter of the current 0.0074", "0.0037 °C, separuh daripada 0.0074 semasa"), ("b", "0.0018 °C, a quarter of the current 0.0074", "0.0018 °C, satu perempat daripada 0.0074 semasa"), ("c", "the same 0.0074 °C", "0.0074 °C yang sama")], "b",
        "Bilinear elements converge as h²: halving h divides the error by about four. 0.0074/4 ≈ 0.0018, and the 8 × 8 value 0.5912 has an error of 0.0018. (Option (a) halves instead of quartering.)",
        "Element bilinear converge sebagai h²: membahagi dua h membahagikan ralat kira-kira empat. 0.0074/4 ≈ 0.0018, dan nilai 8 × 8 iaitu 0.5912 mempunyai ralat 0.0018. (Pilihan (a) membahagi dua, bukan empat.)"),
]

ERRSPOT = (
    '<div class="q" data-q="c1" data-ans="2" id="c1"><p><span class="qmeta">C1 · 2 ' + B("marks", "markah") + '</span><br>'
    + B("A student interpolates T at (0.8, 0.2) m in the text’s solved 2 × 2 mesh (a = b = 0.5 m; T<sub>2</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386, T<sub>6</sub> = 0.482 °C). One line contains the slip. Which one?",
        "Seorang pelajar interpolate T pada (0.8, 0.2) m dalam mesh 2 × 2 teks yang telah diselesaikan (a = b = 0.5 m; T<sub>2</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386, T<sub>6</sub> = 0.482 °C). Satu baris mengandungi kesilapan. Yang mana?") + '</p>'
    + '<div class="conf"><span>' + B("Before you answer:", "Sebelum menjawab:") + '</span><button type="button" data-c="sure">' + B("Sure", "Yakin") + '</button><button type="button" data-c="unsure">' + B("Not sure", "Tak pasti") + '</button></div>'
    + '<div class="errline">'
    + '<button type="button" data-k="1"><span class="ln">1</span><span>0.5 ≤ x ≤ 1, 0 ≤ y ≤ 0.5: the point is in element 2, nodes [2 3 6 5].</span></button>'
    + '<button type="button" data-k="2"><span class="ln">2</span><span>Local coordinates: x<sub>loc</sub> = 0.8, y<sub>loc</sub> = 0.2 (element 2 has the same a and b as element 1).</span></button>'
    + '<button type="button" data-k="3"><span class="ln">3</span><span>N<sub>1</sub> = (0.5 − 0.8)(0.3)/0.25 = −0.36, N<sub>2</sub> = (0.8)(0.3)/0.25 = 0.96, N<sub>3</sub> = (0.8)(0.2)/0.25 = 0.64, N<sub>4</sub> = (0.2)(−0.3)/0.25 = −0.24.</span></button>'
    + '<button type="button" data-k="4"><span class="ln">4</span><span>ΣN<sub>i</sub> = −0.36 + 0.96 + 0.64 − 0.24 = 1.00 ✓</span></button>'
    + '<button type="button" data-k="5"><span class="ln">5</span><span>T = −0.36(0.482) + 0.96(0.621) + 0.64(0.482) − 0.24(0.386) = 0.639 °C.</span></button>'
    + '</div><p class="fb" hidden><span class="meta"></span> '
    + B("Line 2: the global coordinates were used. Element 2 has its local node 1 at (0.5, 0), so x<sub>loc</sub> = 0.3, y<sub>loc</sub> = 0.2 and N = {0.24, 0.36, 0.24, 0.16}, T = 0.24(0.482) + 0.36(0.621) + 0.24(0.482) + 0.16(0.386) = 0.517 °C. The sum check in line 4 did not catch it, because ΣN<sub>i</sub> = 1 holds for any x, y; the negative N<sub>1</sub> and N<sub>4</sub> in line 3 were the warning, and 0.639 above T<sub>3</sub> = 0.621, the hottest node, was the second.",
        "Baris 2: koordinat global digunakan. Element 2 mempunyai node local 1 pada (0.5, 0), jadi x<sub>loc</sub> = 0.3, y<sub>loc</sub> = 0.2 dan N = {0.24, 0.36, 0.24, 0.16}, T = 0.24(0.482) + 0.36(0.621) + 0.24(0.482) + 0.16(0.386) = 0.517 °C. Semakan jumlah pada baris 4 tidak menangkapnya, kerana ΣN<sub>i</sub> = 1 berlaku untuk sebarang x, y; N<sub>1</sub> dan N<sub>4</sub> yang negatif pada baris 3 ialah amarannya, dan 0.639 yang melebihi T<sub>3</sub> = 0.621, node paling panas, ialah amaran kedua.")
    + '</p></div>'
)

EX_JS = r"""
(function(){
  var bi = window.COURSE_API.bi, fmt = window.COURSE_API.fmt;
  function pick(r, arr){ return arr[Math.floor(r()*arr.length)]; }
  function svals(a,b,kx,ky){ return {s1:b*kx/(3*a)+a*ky/(3*b), s2:-b*kx/(3*a)+a*ky/(6*b), s3:-b*kx/(6*a)-a*ky/(6*b), s4:b*kx/(6*a)-a*ky/(3*b)}; }
  function N4(a,b,x,y){ return [(a-x)*(b-y)/(a*b), x*(b-y)/(a*b), x*y/(a*b), y*(a-x)/(a*b)]; }
  function dN(a,b,x,y){ return {dx:[-(b-y)/(a*b),(b-y)/(a*b),y/(a*b),-y/(a*b)], dy:[-(a-x)/(a*b),-x/(a*b),x/(a*b),(a-x)/(a*b)]}; }
  function genK(r){ var a=pick(r,[0.5,1,1.5,2,2.5]), b=pick(r,[0.5,1,1.5,2,3]); return {a:a,b:b,kx:pick(r,[1,2,5,10,20,45,300]),ky:pick(r,[1,2,5,10,20,45,300])}; }
  EX.define("b1", {
    gen: genK,
    text: function(P){ return bi("Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, k<sub>x</sub> = <span class=\"num\">"+P.kx+"</span>, k<sub>y</sub> = <span class=\"num\">"+P.ky+"</span> W m<sup>−1</sup> K<sup>−1</sup>, unit thickness. Find s<sub>1</sub>…s<sub>4</sub> of (2.49) in W K<sup>−1</sup>, to 3 decimals.",
                                   "Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, k<sub>x</sub> = <span class=\"num\">"+P.kx+"</span>, k<sub>y</sub> = <span class=\"num\">"+P.ky+"</span> W m<sup>−1</sup> K<sup>−1</sup>, ketebalan unit. Cari s<sub>1</sub>…s<sub>4</sub> daripada (2.49) dalam W K<sup>−1</sup>, kepada 3 tempat perpuluhan."); },
    fields: ["s1","s2","s3","s4"].map(function(k){ return {id:k, label:[k.replace(/(\d)/,"<sub>$1</sub>"),k.replace(/(\d)/,"<sub>$1</sub>")], unit:"W/K", fn:function(P){ return svals(P.a,P.b,P.kx,P.ky)[k]; }, atol:0.0015, rtol:0.002}; }),
    hints: [function(P){ return bi("(2.49): s<sub>1</sub> = bk<sub>x</sub>/3a + ak<sub>y</sub>/3b, s<sub>2</sub> = −bk<sub>x</sub>/3a + ak<sub>y</sub>/6b, s<sub>3</sub> = −bk<sub>x</sub>/6a − ak<sub>y</sub>/6b, s<sub>4</sub> = bk<sub>x</sub>/6a − ak<sub>y</sub>/3b.",
                                      "(2.49): s<sub>1</sub> = bk<sub>x</sub>/3a + ak<sub>y</sub>/3b, s<sub>2</sub> = −bk<sub>x</sub>/3a + ak<sub>y</sub>/6b, s<sub>3</sub> = −bk<sub>x</sub>/6a − ak<sub>y</sub>/6b, s<sub>4</sub> = bk<sub>x</sub>/6a − ak<sub>y</sub>/3b."); },
            function(P){ return bi("bk<sub>x</sub>/3a = "+fmt(P.b*P.kx/(3*P.a),3)+", ak<sub>y</sub>/3b = "+fmt(P.a*P.ky/(3*P.b),3)+"; the /6 terms are half of these. Check: the four values must sum to zero.",
                                      "bk<sub>x</sub>/3a = "+fmt(P.b*P.kx/(3*P.a),3)+", ak<sub>y</sub>/3b = "+fmt(P.a*P.ky/(3*P.b),3)+"; term /6 ialah separuh daripada ini. Semak: empat nilai mesti berjumlah sifar."); },
            function(P){ var s=svals(P.a,P.b,P.kx,P.ky); return bi("s<sub>1</sub> = "+fmt(s.s1,3)+". The others follow; s<sub>2</sub> + s<sub>3</sub> + s<sub>4</sub> must equal −s<sub>1</sub>.", "s<sub>1</sub> = "+fmt(s.s1,3)+". Yang lain menyusul; s<sub>2</sub> + s<sub>3</sub> + s<sub>4</sub> mesti sama dengan −s<sub>1</sub>."); }],
    solution: function(P){ var s=svals(P.a,P.b,P.kx,P.ky), A=P.b*P.kx/(3*P.a), Bb=P.a*P.ky/(3*P.b);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">bk<sub>x</sub>/3a = "+fmt(A,4)+", ak<sub>y</sub>/3b = "+fmt(Bb,4)+"<br>s<sub>1</sub> = "+fmt(A,4)+" + "+fmt(Bb,4)+" = "+fmt(s.s1,3)+"<br>s<sub>2</sub> = −"+fmt(A,4)+" + "+fmt(Bb/2,4)+" = "+fmt(s.s2,3)+"<br>s<sub>3</sub> = −"+fmt(A/2,4)+" − "+fmt(Bb/2,4)+" = "+fmt(s.s3,3)+"<br>s<sub>4</sub> = "+fmt(A/2,4)+" − "+fmt(Bb,4)+" = "+fmt(s.s4,3)+"<br>"+bi("Row sum: ","Jumlah baris: ")+fmt(s.s1+s.s2+s.s3+s.s4,3)+"</p>"; }
  });
  EX.define("b2", {
    gen: function(r){ var a=pick(r,[0.5,1,2,2.5]), b=pick(r,[0.5,1,1.5,3]); return {a:a,b:b,Q:pick(r,[20,50,100,600,1000]),qb:pick(r,[50,100,200,500,1000]),edge:pick(r,["right (2–3)","top (3–4)","left (4–1)","bottom (1–2)"])}; },
    text: function(P){ var len = (P.edge.indexOf("right")===0||P.edge.indexOf("left")===0)?"b = "+P.b:"a = "+P.a;
      return bi("Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, unit thickness. A uniform source q<sub>h</sub> = <span class=\"num\">"+P.Q+"</span> W m<sup>−3</sup> acts in the element and a uniform inward flux q<sub>b</sub> = <span class=\"num\">"+P.qb+"</span> W m<sup>−2</sup> on its "+P.edge+" edge (length "+len+" m). Find the source load at each node, q<sub>i</sub>, and the boundary load at each of the two nodes of that edge, b<sub>j</sub>, in W, to 2 decimals.",
                "Element a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, ketebalan unit. Source seragam q<sub>h</sub> = <span class=\"num\">"+P.Q+"</span> W m<sup>−3</sup> bertindak dalam element dan flux ke dalam yang seragam q<sub>b</sub> = <span class=\"num\">"+P.qb+"</span> W m<sup>−2</sup> pada tepi "+P.edge+" (panjang "+len+" m). Cari load source pada setiap node, q<sub>i</sub>, dan load sempadan pada setiap satu daripada dua node tepi itu, b<sub>j</sub>, dalam W, kepada 2 tempat perpuluhan."); },
    fields: [{id:"qi", label:["q<sub>i</sub> (each node)","q<sub>i</sub> (setiap node)"], unit:"W", fn:function(P){ return P.Q*P.a*P.b/4; }, atol:0.006, rtol:0.002},
             {id:"bj", label:["b<sub>j</sub> (each edge node)","b<sub>j</sub> (setiap node tepi)"], unit:"W", fn:function(P){ var L=(P.edge.indexOf("right")===0||P.edge.indexOf("left")===0)?P.b:P.a; return P.qb*L/2; }, atol:0.006, rtol:0.002}],
    hints: [function(P){ return bi("(2.39): a uniform source is shared equally, q<sub>i</sub> = q<sub>h</sub>ab/4. (2.40): a uniform edge flux is shared equally by the two nodes of that edge, b<sub>j</sub> = q<sub>b</sub> × (edge length)/2.",
                                      "(2.39): source seragam dikongsi sama rata, q<sub>i</sub> = q<sub>h</sub>ab/4. (2.40): flux tepi seragam dikongsi sama rata oleh dua node tepi itu, b<sub>j</sub> = q<sub>b</sub> × (panjang tepi)/2."); },
            function(P){ return bi("Totals as checks: the four q<sub>i</sub> add up to q<sub>h</sub>ab = "+fmt(P.Q*P.a*P.b,2)+" W; the two b<sub>j</sub> add up to q<sub>b</sub> × length.", "Jumlah sebagai semakan: empat q<sub>i</sub> berjumlah q<sub>h</sub>ab = "+fmt(P.Q*P.a*P.b,2)+" W; dua b<sub>j</sub> berjumlah q<sub>b</sub> × panjang."); }],
    solution: function(P){ var L=(P.edge.indexOf("right")===0||P.edge.indexOf("left")===0)?P.b:P.a;
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">q<sub>i</sub> = "+P.Q+" × "+P.a+" × "+P.b+" / 4 = "+fmt(P.Q*P.a*P.b/4,2)+" W "+bi("at each of the four nodes (total ","pada setiap satu daripada empat node (jumlah ")+fmt(P.Q*P.a*P.b,2)+" W)<br>b<sub>j</sub> = "+P.qb+" × "+L+" / 2 = "+fmt(P.qb*L/2,2)+" W "+bi("at each of the two nodes of the "+P.edge+" edge; the other two nodes get nothing.","pada setiap satu daripada dua node tepi "+P.edge+"; dua node lain tidak menerima apa-apa.")+"</p>"; }
  });
  EX.define("b3", {
    gen: function(r){ var a=pick(r,[0.5,1,2]), b=pick(r,[0.5,1,1.5]); return {a:a,b:b,k:pick(r,[1,2,10,45,300])}; },
    text: function(P){ return bi("Two identical elements a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, k<sub>x</sub> = k<sub>y</sub> = <span class=\"num\">"+P.k+"</span> W m<sup>−1</sup> K<sup>−1</sup>, side by side: nodes 1, 2, 3 along the bottom and 4, 5, 6 along the top; element 1 = [1 2 5 4], element 2 = [2 3 6 5]. Find the global entries K<sub>22</sub>, K<sub>25</sub>, K<sub>12</sub> and K<sub>15</sub> in W K<sup>−1</sup>, to 3 decimals.",
                                   "Dua element serupa a = <span class=\"num\">"+P.a+"</span> m, b = <span class=\"num\">"+P.b+"</span> m, k<sub>x</sub> = k<sub>y</sub> = <span class=\"num\">"+P.k+"</span> W m<sup>−1</sup> K<sup>−1</sup>, bersebelahan: node 1, 2, 3 di sepanjang bawah dan 4, 5, 6 di sepanjang atas; element 1 = [1 2 5 4], element 2 = [2 3 6 5]. Cari entri global K<sub>22</sub>, K<sub>25</sub>, K<sub>12</sub> dan K<sub>15</sub> dalam W K<sup>−1</sup>, kepada 3 tempat perpuluhan."); },
    fields: [{id:"k22", label:["K<sub>22</sub>","K<sub>22</sub>"], unit:"W/K", fn:function(P){ return 2*svals(P.a,P.b,P.k,P.k).s1; }, atol:0.0015, rtol:0.002},
             {id:"k25", label:["K<sub>25</sub>","K<sub>25</sub>"], unit:"W/K", fn:function(P){ return 2*svals(P.a,P.b,P.k,P.k).s4; }, atol:0.0015, rtol:0.002},
             {id:"k12", label:["K<sub>12</sub>","K<sub>12</sub>"], unit:"W/K", fn:function(P){ return svals(P.a,P.b,P.k,P.k).s2; }, atol:0.0015, rtol:0.002},
             {id:"k15", label:["K<sub>15</sub>","K<sub>15</sub>"], unit:"W/K", fn:function(P){ return svals(P.a,P.b,P.k,P.k).s3; }, atol:0.0015, rtol:0.002}],
    hints: [function(P){ return bi("Write the connectivity: node 2 is local 2 of element 1 and local 1 of element 2; node 5 is local 3 of element 1 and local 4 of element 2. An entry K<sub>IJ</sub> is the sum of k<sub>ij</sub> over every element that contains both I and J.",
                                      "Tulis connectivity: node 2 ialah local 2 bagi element 1 dan local 1 bagi element 2; node 5 ialah local 3 bagi element 1 dan local 4 bagi element 2. Entri K<sub>IJ</sub> ialah jumlah k<sub>ij</sub> atas setiap element yang mengandungi kedua-dua I dan J."); },
            function(P){ var s=svals(P.a,P.b,P.k,P.k); return bi("s<sub>1</sub> = "+fmt(s.s1,3)+", s<sub>2</sub> = "+fmt(s.s2,3)+", s<sub>3</sub> = "+fmt(s.s3,3)+", s<sub>4</sub> = "+fmt(s.s4,3)+". In the pattern of (2.49): k<sub>12</sub> = s<sub>2</sub>, k<sub>13</sub> = s<sub>3</sub>, k<sub>23</sub> = k<sub>14</sub> = s<sub>4</sub>.",
                                      "s<sub>1</sub> = "+fmt(s.s1,3)+", s<sub>2</sub> = "+fmt(s.s2,3)+", s<sub>3</sub> = "+fmt(s.s3,3)+", s<sub>4</sub> = "+fmt(s.s4,3)+". Dalam pola (2.49): k<sub>12</sub> = s<sub>2</sub>, k<sub>13</sub> = s<sub>3</sub>, k<sub>23</sub> = k<sub>14</sub> = s<sub>4</sub>."); },
            function(P){ return bi("K<sub>22</sub> = s<sub>1</sub> + s<sub>1</sub> (two elements). K<sub>25</sub> = k¹<sub>23</sub> + k²<sub>14</sub> = 2s<sub>4</sub>. K<sub>12</sub> = k¹<sub>12</sub> = s<sub>2</sub> (element 1 only). K<sub>15</sub> = k¹<sub>13</sub> = s<sub>3</sub>.",
                                      "K<sub>22</sub> = s<sub>1</sub> + s<sub>1</sub> (dua element). K<sub>25</sub> = k¹<sub>23</sub> + k²<sub>14</sub> = 2s<sub>4</sub>. K<sub>12</sub> = k¹<sub>12</sub> = s<sub>2</sub> (element 1 sahaja). K<sub>15</sub> = k¹<sub>13</sub> = s<sub>3</sub>."); }],
    solution: function(P){ var s=svals(P.a,P.b,P.k,P.k);
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">s = {"+fmt(s.s1,3)+", "+fmt(s.s2,3)+", "+fmt(s.s3,3)+", "+fmt(s.s4,3)+"}<br>K<sub>22</sub> = 2s<sub>1</sub> = "+fmt(2*s.s1,3)+"<br>K<sub>25</sub> = k¹<sub>23</sub> + k²<sub>14</sub> = 2s<sub>4</sub> = "+fmt(2*s.s4,3)+"<br>K<sub>12</sub> = k¹<sub>12</sub> = s<sub>2</sub> = "+fmt(s.s2,3)+"<br>K<sub>15</sub> = k¹<sub>13</sub> = s<sub>3</sub> = "+fmt(s.s3,3)+"</p>"; }
  });
  /* b4: the text's solved 2 x 2 mesh; nodes 1-3 bottom, 4-6 middle, 7-9 top; a = b = 0.5, k = 300 */
  var TN = [0, 0.4821, 0.6214, 0, 0.3857, 0.4821, 0, 0, 0], CONN = [[1,2,5,4],[2,3,6,5],[4,5,8,7],[5,6,9,8]], ORG = [[0,0],[0.5,0],[0,0.5],[0.5,0.5]];
  EX.define("b4", {
    gen: function(r){ var e=Math.floor(r()*4), xl=Math.round((0.05+0.4*r())*20)/20, yl=Math.round((0.05+0.4*r())*20)/20; return {e:e, x:Math.round((ORG[e][0]+xl)*100)/100, y:Math.round((ORG[e][1]+yl)*100)/100}; },
    text: function(P){ return bi("The text’s plate (a = b = 0.5 m, k = 300 W m<sup>−1</sup> K<sup>−1</sup>) solved on the 2 × 2 mesh: T<sub>2</sub> = T<sub>6</sub> = 0.4821, T<sub>3</sub> = 0.6214, T<sub>5</sub> = 0.3857 °C and 0 on the cold edges; elements [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]. For the point (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m give the element number, T to 4 decimals and q<sub>x</sub> to 1 decimal.",
                                   "Plat dalam teks (a = b = 0.5 m, k = 300 W m<sup>−1</sup> K<sup>−1</sup>) diselesaikan pada mesh 2 × 2: T<sub>2</sub> = T<sub>6</sub> = 0.4821, T<sub>3</sub> = 0.6214, T<sub>5</sub> = 0.3857 °C dan 0 pada tepi sejuk; element [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]. Bagi titik (x, y) = (<span class=\"num\">"+P.x+"</span>, <span class=\"num\">"+P.y+"</span>) m, beri nombor element, T kepada 4 tempat perpuluhan dan q<sub>x</sub> kepada 1 tempat perpuluhan."); },
    fields: [{id:"e", label:["element","element"], fn:function(P){ return P.e+1; }, atol:0.01, rtol:0},
             {id:"t", label:["T","T"], unit:"°C", fn:function(P){ var N=N4(0.5,0.5,P.x-ORG[P.e][0],P.y-ORG[P.e][1]), c=CONN[P.e]; return N[0]*TN[c[0]-1]+N[1]*TN[c[1]-1]+N[2]*TN[c[2]-1]+N[3]*TN[c[3]-1]; }, atol:0.0006, rtol:0.002},
             {id:"qx", label:["q<sub>x</sub>","q<sub>x</sub>"], unit:"W m⁻²", fn:function(P){ var d=dN(0.5,0.5,P.x-ORG[P.e][0],P.y-ORG[P.e][1]), c=CONN[P.e], g=0; for(var i=0;i<4;i++) g+=d.dx[i]*TN[c[i]-1]; return -300*g; }, atol:0.3, rtol:0.005}],
    hints: [function(P){ return bi("Element = the square that contains the point (x < 0.5 → left column; y < 0.5 → bottom row). Local coordinates: subtract the element’s origin, its local node 1.", "Element = segi empat yang mengandungi titik itu (x < 0.5 → lajur kiri; y < 0.5 → baris bawah). Koordinat local: tolak origin element, iaitu node local 1-nya."); },
            function(P){ var c=CONN[P.e]; return bi("Element "+(P.e+1)+", nodes ["+c.join(" ")+"], origin ("+ORG[P.e][0]+", "+ORG[P.e][1]+"): local ("+fmt(P.x-ORG[P.e][0],2)+", "+fmt(P.y-ORG[P.e][1],2)+"). Nodal values in local order: {"+c.map(function(n){return TN[n-1];}).join(", ")+"}.",
                                      "Element "+(P.e+1)+", node ["+c.join(" ")+"], origin ("+ORG[P.e][0]+", "+ORG[P.e][1]+"): local ("+fmt(P.x-ORG[P.e][0],2)+", "+fmt(P.y-ORG[P.e][1],2)+"). Nilai node mengikut susunan local: {"+c.map(function(n){return TN[n-1];}).join(", ")+"}."); },
            function(P){ var xl=P.x-ORG[P.e][0], yl=P.y-ORG[P.e][1], N=N4(0.5,0.5,xl,yl); return bi("N = {"+N.map(function(v){return fmt(v,3);}).join(", ")+"}. T = ΣN<sub>i</sub>T<sub>i</sub>; q<sub>x</sub> = −300 Σ(∂N<sub>i</sub>/∂x)T<sub>i</sub> with ∂N<sub>i</sub>/∂x = {−(b − y), b − y, y, −y}/(ab) at the local y.",
                                      "N = {"+N.map(function(v){return fmt(v,3);}).join(", ")+"}. T = ΣN<sub>i</sub>T<sub>i</sub>; q<sub>x</sub> = −300 Σ(∂N<sub>i</sub>/∂x)T<sub>i</sub> dengan ∂N<sub>i</sub>/∂x = {−(b − y), b − y, y, −y}/(ab) pada y local."); }],
    solution: function(P){ var xl=P.x-ORG[P.e][0], yl=P.y-ORG[P.e][1], N=N4(0.5,0.5,xl,yl), d=dN(0.5,0.5,xl,yl), c=CONN[P.e], T=0, g=0; for(var i=0;i<4;i++){ T+=N[i]*TN[c[i]-1]; g+=d.dx[i]*TN[c[i]-1]; }
      return "<h5>"+bi("Solution with these numbers","Penyelesaian dengan nombor ini")+"</h5><p class=\"num\">"+bi("Element ","Element ")+(P.e+1)+", "+bi("nodes","node")+" ["+c.join(" ")+"], local ("+fmt(xl,2)+", "+fmt(yl,2)+")<br>N = {"+N.map(function(v){return fmt(v,4);}).join(", ")+"}, ΣN = "+fmt(N[0]+N[1]+N[2]+N[3],3)+"<br>T = "+N.map(function(v,i){return fmt(v,4)+"("+TN[c[i]-1]+")";}).join(" + ")+" = "+fmt(T,4)+" °C<br>∂T/∂x = "+d.dx.map(function(v,i){return "("+fmt(v,3)+")("+TN[c[i]-1]+")";}).join(" + ")+" = "+fmt(g,4)+" K m⁻¹; q<sub>x</sub> = −300 × "+fmt(g,4)+" = "+fmt(-300*g,1)+" W m⁻²</p>"; }
  });
  EX.ready();
})();
"""

CALC = [
    ("b1", ("The four values of the conductance matrix", "Empat nilai conductance matrix"), 4),
    ("b2", ("Source and edge-flux loads", "Load source dan flux tepi"), 3),
    ("b3", ("Assembly entries of a two-element strip", "Entri assembly bagi jalur dua element"), 4),
    ("b4", ("Temperature and flux at a point of the solved mesh", "Temperature dan flux pada satu titik mesh yang diselesaikan"), 5),
]

LAB_TASKS = [
    ("book2", ("Keep the text’s example on the 2 × 2 mesh. Read T at the bottom-right corner and at the middle of the bottom edge; tap the plate to probe.", "Kekalkan contoh teks pada mesh 2 × 2. Baca T pada bucu kanan bawah dan di tengah tepi bawah; ketik plat untuk probe."),
              ("detected on the first probe with the text’s settings on 2 × 2", "dikesan pada probe pertama dengan tetapan teks pada 2 × 2")),
    ("study", ("Run the mesh study. From which mesh does the maximum temperature change by less than 1%? Which value would you report?", "Jalankan kajian mesh. Dari mesh manakah temperature maksimum berubah kurang daripada 1%? Nilai mana yang akan anda laporkan?"),
              ("detected when the mesh study runs with the text’s settings", "dikesan apabila kajian mesh dijalankan dengan tetapan teks")),
    ("right0", ("Set the right edge to 0 °C as well. Where is the hottest point now, and why there?", "Tetapkan tepi kanan kepada 0 °C juga. Di mana titik paling panas sekarang, dan mengapa di situ?"),
               ("detected when three edges are at the same temperature and the bottom is insulated", "dikesan apabila tiga tepi berada pada temperature yang sama dan bawah insulated")),
    ("allins", ("Make all four edges insulated. What does the Explorer report, and what does it mean physically?", "Jadikan keempat-empat tepi insulated. Apa yang dilaporkan oleh Explorer, dan apa maksudnya secara fizikal?"),
               ("detected when all four edges are insulated", "dikesan apabila keempat-empat tepi insulated")),
]

GLOSSARY = [
    ("residual", "What is left when the approximation is substituted into the PDE; zero only for the exact solution.", "Apa yang tinggal apabila approximation digantikan ke dalam PDE; sifar hanya untuk penyelesaian tepat."),
    ("weighted residual", "The residual multiplied by a weight and integrated; set to zero to get one equation per weight.", "Residual didarab dengan weight function dan di-integrate; disamakan dengan sifar untuk mendapat satu persamaan setiap weight function."),
    ("Galerkin method", "Weighted residual with the shape functions as weights; gives a symmetric [k].", "Weighted residual dengan shape function sebagai weight function; memberi [k] yang simetri."),
    ("integration by parts · Green’s theorem", "Moves one derivative from T onto the weight and produces a boundary term; in 2D the area integral trades with a boundary integral.", "Memindahkan satu derivative dari T kepada weight function dan menghasilkan boundary term; dalam 2D integral luas ditukar dengan integral sempadan."),
    ("weak form", "The integrated, lower-derivative statement that the finite element equations come from.", "Pernyataan ter-integrate dengan derivative lebih rendah yang menjadi asal persamaan finite element."),
    ("conductance matrix [k]", "4 × 4, symmetric, from ∫{N}ᵀ{∂}[E]{∂}ᵀ{N} dA; the heat analogue of stiffness. Units W K<sup>−1</sup> per unit thickness.", "4 × 4, simetri, daripada ∫{N}ᵀ{∂}[E]{∂}ᵀ{N} dA; analog haba bagi stiffness. Unit W K<sup>−1</sup> per unit ketebalan."),
    ("s<sub>1</sub>…s<sub>4</sub>", "The four distinct entries of [k] for a rectangle, (2.49); s<sub>1</sub> diagonal, s<sub>2</sub> horizontal side, s<sub>4</sub> vertical side, s<sub>3</sub> diagonal pairs.", "Empat entri berbeza [k] bagi segi empat tepat, (2.49); s<sub>1</sub> pepenjuru, s<sub>2</sub> sisi mendatar, s<sub>4</sub> sisi menegak, s<sub>3</sub> pasangan pepenjuru."),
    ("source vector {q}", "Nodal loads from the heat generated inside the element, q<sub>h</sub>ab/4 each for a uniform source.", "Nodal load daripada haba yang dijana di dalam element, q<sub>h</sub>ab/4 setiap satu bagi source seragam."),
    ("boundary vector {b}", "Nodal loads from a known flux on an edge, q<sub>b</sub>ℓ/2 at each of the two nodes of that edge.", "Nodal load daripada flux yang diketahui pada satu tepi, q<sub>b</sub>ℓ/2 pada setiap satu daripada dua node tepi itu."),
    ("row-sum check", "Every row of [k] adds to zero because a uniform temperature conducts no heat.", "Setiap baris [k] berjumlah sifar kerana temperature seragam tidak mengalirkan haba."),
    ("connectivity table", "For each element, its global node numbers in local anticlockwise order.", "Bagi setiap element, nombor node global-nya mengikut susunan local lawan jam."),
    ("assembly · scatter-add", "K<sub>IJ</sub> += k<sub>ij</sub> with I, J read from the connectivity table; the same for {R}.", "K<sub>IJ</sub> += k<sub>ij</sub> dengan I, J dibaca daripada connectivity table; sama untuk {R}."),
    ("global system [K]{T} = {R}", "All elements assembled; singular until at least one temperature is prescribed.", "Semua element di-assemble; singular sehingga sekurang-kurangnya satu temperature ditetapkan."),
    ("row–column elimination", "Imposing a known T̄: move its column × T̄ to the right-hand side, delete the row and the column.", "Mengenakan T̄ yang diketahui: pindahkan lajurnya × T̄ ke sebelah kanan, buang baris dan lajur itu."),
    ("reduced system", "The equations that remain for the unknown temperatures after the known ones are struck.", "Persamaan yang tinggal untuk temperature yang tidak diketahui selepas yang diketahui dibuang."),
    ("struck rows · energy balance", "Rows of the known nodes, evaluated afterwards, give the heat flows there; their sum balances the heat put in.", "Baris node yang diketahui, dinilai selepas itu, memberi aliran haba di situ; jumlahnya mengimbangi haba yang dimasukkan."),
    ("local coordinates", "Position measured from an element’s local node 1; what N<sub>i</sub> must be evaluated with.", "Kedudukan diukur dari node local 1 sesuatu element; itulah yang mesti digunakan untuk menilai N<sub>i</sub>."),
    ("post-processing", "Everything computed from the nodal solution: T at a point, flux, hottest point, heat flows.", "Segala yang dikira daripada penyelesaian node: T pada satu titik, flux, titik paling panas, aliran haba."),
    ("mesh refinement · convergence", "Repeating the solution on finer meshes until the answer stops changing; bilinear elements converge as h².", "Mengulang penyelesaian pada mesh yang lebih halus sehingga jawapan berhenti berubah; element bilinear converge sebagai h²."),
    ("relative error", "(T<sub>mesh</sub> − T<sub>ref</sub>)/T<sub>ref</sub>; about +5% for the 2 × 2 mesh of the text’s plate.", "(T<sub>mesh</sub> − T<sub>ref</sub>)/T<sub>ref</sub>; kira-kira +5% bagi mesh 2 × 2 plat dalam teks."),
    ("patch test", "A field the element can represent exactly (here a linear T) must be reproduced exactly on any mesh.", "Field yang mampu diwakili element dengan tepat (di sini T linear) mesti dihasilkan semula dengan tepat pada mana-mana mesh."),
    ("symmetry", "Equal geometry, material, loads and boundary conditions about a line give equal temperatures at mirror nodes; a line of symmetry carries no heat across it.", "Geometri, bahan, load dan boundary condition yang sama tentang satu garis memberi temperature yang sama pada node cermin; garis simetri tidak membawa haba merentasinya."),
]


def short_notes(A):
    return (
        "<h3>§1 Galerkin</h3>" + A.eq("w_sys", "(2.42)", 0.5) + P("Weights = shape functions; integration by parts lowers the derivative order and exposes q<sub>b</sub>.", "Pemberat = shape function; integration by parts merendahkan peringkat derivative dan mendedahkan q<sub>b</sub>.")
        + "<h3>§2 [k], {q}, {b}</h3>" + A.eq("w_svals", "(2.49)", 0.5) + A.eq("w_qconst", "(2.39)", 0.5)
        + LI([("Edge flux: q<sub>b</sub>ℓ/2 at each of the two edge nodes.", "Flux tepi: q<sub>b</sub>ℓ/2 pada setiap satu daripada dua node tepi."), ("Rows sum to zero. Text element: 200, −50, −100, −50; r<sub>i</sub> = 37.5 W.", "Baris berjumlah sifar. Element teks: 200, −50, −100, −50; r<sub>i</sub> = 37.5 W.")])
        + "<h3>§3–§4 " + B("Assembly", "Assembly") + "</h3>" + A.eq("w_scatter", None, 0.5) + A.eq("w_nonzero", None, 0.5)
        + LI([("Text plate: elements [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]; K<sub>55</sub> = 800.", "Plat teks: element [1 2 5 4], [2 3 6 5], [4 5 8 7], [5 6 9 8]; K<sub>55</sub> = 800."), ("T<sub>2</sub> = T<sub>6</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386 °C.", "T<sub>2</sub> = T<sub>6</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386 °C.")])
        + "<h3>§5 Post-processing</h3>" + A.eq("w_local", None, 0.5) + A.eq("w_interp", None, 0.5)
        + P("T(0.3, 0.2) = 0.266 °C. 2 × 2 is ≈ 5% high; 16 × 16 = 0.5898 vs software 0.5897.", "T(0.3, 0.2) = 0.266 °C. 2 × 2 ≈ 5% tinggi; 16 × 16 = 0.5898 berbanding perisian 0.5897.")
    )


EXAMPLES_INTRO = _INTRO1.replace(
    '<tr><td>' + B("Explain", "Terangkan") + '</td>',
    '<tr><td>' + B("Conductance matrix", "Conductance matrix") + '</td><td>' + B("a, b, k<sub>x</sub>, k<sub>y</sub> (and t); wanted: [k], often in terms of k.", "a, b, k<sub>x</sub>, k<sub>y</sub> (dan t); dikehendaki: [k], selalunya dalam sebutan k.") + '</td><td>' + B("s<sub>1</sub> to s<sub>4</sub> and the pattern of (2.49). Trap: b/a and a/b swapped.", "s<sub>1</sub> hingga s<sub>4</sub> dan pola (2.49). Perangkap: b/a dan a/b tertukar.") + '</td></tr>'
    + '<tr><td>' + B("Heat loads", "Load haba") + '</td><td>' + B("Q or q<sub>n</sub> on an element; wanted: {r}.", "Q atau q<sub>n</sub> pada satu element; dikehendaki: {r}.") + '</td><td>' + B("Equal shares. Trap: Q in W/m² against W/m³.", "Bahagian sama rata. Perangkap: Q dalam W/m² berbanding W/m³.") + '</td></tr>'
    + '<tr><td>' + B("Assembly and solution", "Assembly dan penyelesaian") + '</td><td>' + B("Identical elements, prescribed temperatures, insulated edges; wanted: the free nodal temperatures.", "Element serupa, temperature ditetapkan, tepi insulated; dikehendaki: temperature node bebas.") + '</td><td>' + B("K<sub>ii</sub> is s<sub>1</sub> times the number of elements at node i; strike the fixed nodes; use symmetry.", "K<sub>ii</sub> ialah s<sub>1</sub> kali bilangan element pada node i; buang node tetap; guna simetri.") + '</td></tr>'
    + '<tr><td>' + B("Explain", "Terangkan") + '</td>')


def examples(A):
    X = []
    # ---- Example 1: [k] and loads of a square element (companion 8.2 + 8.3) ----
    head = ('<div class="xhead"><h2>' + B("Example 1 · Conductance matrix and nodal loads of a square element", "Contoh 1 · Conductance matrix dan nodal load bagi element segi empat sama") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> [k] of a Q4 element, two entries by integration, the rest by pattern; {b} for a boundary flux, {q} for a source</span><span><b>' + B("Units", "Unit") + '</b> W, m, K</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Examples 8.2 and 8.3 (textbook Exercises 2.1–2.3)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>A square element of side 0.025 m and thickness 0.005 m has k = 450 W m<sup>−1</sup> K<sup>−1</sup>. (a) Show the integration for k<sub>12</sub> and k<sub>13</sub> and complete [k] by the pattern of (2.49). '
         '(b) Determine the nodal loads for an inward heat flux of 10<sup>6</sup> W m<sup>−2</sup> on its right side, 2–3, and (c) for an internal heat generation of 10<sup>7</sup> W m<sup>−3</sup>. '
         '(d) In an examination plate of unit thickness, an element 2 m wide and 3 m high carries a heat source Q = 20 W m<sup>−2</sup>; determine its load vector.</div>')
    body = (head + q + A.fig("fig_sq_flux", "The element of Example 1.", "Element bagi Contoh 1.", 380)
            + PIC("k<sub>ij</sub> is the heat that must be supplied at node i when node j is held 1 K above the others, all at 0 K. In a square it is negative for i ≠ j, because a hotter node j pushes heat towards node i and the supply at i must take it away. For a square with k<sub>x</sub> = k<sub>y</sub> the matrix depends only on k and t, not on the side. The heat entering or generated is shared by the nodes in proportion to how much each shape function covers: every N<sub>i</sub> integrates to ab/4 over the element, and along a side only its two nodes have non-zero shape functions, each taking half.",
                  "k<sub>ij</sub> ialah haba yang mesti dibekalkan pada node i apabila node j ditahan 1 K lebih tinggi daripada yang lain, semuanya pada 0 K. Dalam segi empat sama ia negatif untuk i ≠ j, kerana node j yang lebih panas menolak haba ke arah node i dan bekalan di i mesti membawanya pergi. Bagi segi empat sama dengan k<sub>x</sub> = k<sub>y</sub>, matrix itu bergantung pada k dan t sahaja, bukan pada sisi. Haba yang masuk atau dijana dikongsi oleh node mengikut kadar liputan setiap shape function: setiap N<sub>i</sub> ber-integral kepada ab/4 di atas element, dan di sepanjang satu sisi hanya dua node-nya mempunyai shape function bukan sifar, setiap satu mengambil separuh.")
            + PLAN("Derivatives of N<sub>1</sub>, N<sub>2</sub>, N<sub>3</sub> → integrate k<sub>12</sub>, k<sub>13</sub> → s<sub>1</sub> to s<sub>4</sub> → the pattern → row-sum check → (b) {b} on side 2–3 → (c) {q} → (d) the same with Q per unit area → totals as checks.")
            + XSTEP(1, "Derivatives", "Derivative", 2, P("From (8.5), the shape functions of Part 1:", "Daripada (8.5), shape function Part 1:") + A.eq("y1_dN"))
            + XSTEP(2, "(a) Two entries by integration", "(a) Dua entri melalui integration", 5, A.eq("y1_k12") + A.eq("y1_k13"))
            + XSTEP(3, "(a) Numbers", "(a) Nombor", 3, P("With a = b and k<sub>x</sub> = k<sub>y</sub> = 450, multiplied by t = 0.005 m:", "Dengan a = b dan k<sub>x</sub> = k<sub>y</sub> = 450, didarab dengan t = 0.005 m:") + A.eq("y1_nums"))
            + XSTEP(4, "(a) The matrix", "(a) Matrix", 2, A.eq("y1_k") + CHK("Every row: 1.5 − 0.375 − 0.75 − 0.375 = 0.") + ANS("(a) [k] as above: s<sub>1</sub> = 1.5, s<sub>2</sub> = s<sub>4</sub> = −0.375, s<sub>3</sub> = −0.75 W K<sup>−1</sup>."))
            + XSTEP(5, "(b) Flux on side 2–3", "(b) Flux pada sisi 2–3", 3, P("On x = a: N<sub>1</sub> = N<sub>4</sub> = 0, N<sub>2</sub> = (b − y)/b, N<sub>3</sub> = y/b. Each integrates to b/2 along the side:", "Pada x = a: N<sub>1</sub> = N<sub>4</sub> = 0, N<sub>2</sub> = (b − y)/b, N<sub>3</sub> = y/b. Setiap satu ber-integral kepada b/2 di sepanjang sisi:") + A.eq("y1_b") + CHK("Total 125 W = q<sub>n</sub> t b = 10<sup>6</sup>(0.005)(0.025), the heat crossing the side."))
            + XSTEP(6, "(c) Heat generation", "(c) Heat generation", 3, P("∫N<sub>i</sub> dA = ab/4 for each node, so", "∫N<sub>i</sub> dA = ab/4 bagi setiap node, jadi") + A.eq("y1_q") + CHK("Total 31.25 W = Q t ab."))
            + XSTEP(7, "(d) A source given per unit area", "(d) Source yang diberi per unit luas", 2, P("Q = 20 W m<sup>−2</sup> is heat per unit area of the plate and already contains the thickness, so it is not multiplied by t:", "Q = 20 W m<sup>−2</sup> ialah haba per unit luas plat dan sudah mengandungi ketebalan, jadi ia tidak didarab dengan t:") + A.eq("y1_qc")
                    + ANS("(b) 62.5 W at nodes 2 and 3. (c) 7.81 W at each node. (d) {r}<sup>1</sup> = {30, 30, 30, 30}ᵀ W."))
            + NOTE("Pitfall · W m<sup>−2</sup> or W m<sup>−3</sup>", "Perangkap · W m<sup>−2</sup> atau W m<sup>−3</sup>", "A source per unit volume (W m<sup>−3</sup>) is multiplied by t. A source per unit area of the plate (W m<sup>−2</sup>), as in part (d), already contains the thickness: do not multiply again.",
                   "Source per unit isi padu (W m<sup>−3</sup>) didarab dengan t. Source per unit luas plat (W m<sup>−2</sup>), seperti dalam bahagian (d), sudah mengandungi ketebalan: jangan darab lagi.")
            + INTERP("The diagonal pair (1–3) is coupled twice as strongly as each side pair, −0.75 against −0.375 W K<sup>−1</sup>. For a side pair the two directions work against each other: in k<sub>12</sub> the k<sub>x</sub> term is negative and the k<sub>y</sub> term positive; for a diagonal pair both are negative. Doubling the side of the square leaves [k] unchanged: the longer conduction path and the wider section cancel. Equal shares are a property of uniform loads; whatever the distribution, the loads must add up to the total heat, and that check catches a forgotten thickness or a misplaced factor of 2.",
                     "Pasangan pepenjuru (1–3) digandingkan dua kali lebih kuat daripada setiap pasangan sisi, −0.75 berbanding −0.375 W K<sup>−1</sup>. Bagi pasangan sisi, dua arah itu bertentangan: dalam k<sub>12</sub> term k<sub>x</sub> negatif dan term k<sub>y</sub> positif; bagi pasangan pepenjuru kedua-duanya negatif. Menggandakan sisi segi empat sama tidak mengubah [k]: laluan conduction yang lebih panjang dan keratan yang lebih lebar saling membatalkan. Bahagian sama rata ialah sifat load seragam; apa jua taburannya, load mesti berjumlah kepada jumlah haba, dan semakan itu menangkap ketebalan yang terlupa atau faktor 2 yang tersalah letak.")
            + SCHEME([("Derivatives of the shape functions", "Derivative shape function", 2), ("k<sub>12</sub> and k<sub>13</sub> by integration, with the integrals evaluated", "k<sub>12</sub> dan k<sub>13</sub> melalui integration, dengan integral dinilai", 5), ("Numerical s<sub>1</sub>…s<sub>4</sub> with t", "s<sub>1</sub>…s<sub>4</sub> berangka dengan t", 3), ("Matrix by the pattern, row-sum check", "Matrix mengikut pola, semakan jumlah baris", 2),
                      ("{b}: half the flux × length × t at each of the two nodes, total check", "{b}: separuh flux × panjang × t pada setiap dua node, semakan jumlah", 3), ("{q}: tQab/4 at each node, total check", "{q}: tQab/4 pada setiap node, semakan jumlah", 3), ("Per-unit-area source not multiplied by t", "Source per unit luas tidak didarab dengan t", 2)], 20))
    X.append(("y1", "[k] and loads of a square element", "[k] dan load bagi element segi empat sama", body))

    # ---- Example 2: 2 x 2 mesh with a prescribed temperature and an inward flux (companion 8.6) ----
    head = ('<div class="xhead"><h2>' + B("Example 2 · Four elements with a prescribed temperature and an inward flux", "Contoh 2 · Empat element dengan temperature ditetapkan dan flux ke dalam") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> assembly of a 2 × 2 mesh, essential and natural conditions, solution by symmetry, energy balance</span><span><b>' + B("Units", "Unit") + '</b> W, m, K</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 8.6 (textbook Exercise 2.4)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>The square plate of the figure, 0.05 m by 0.05 m and 0.005 m thick, is divided into four equal elements. Its top and bottom are insulated, its left side is held at 400 K, and its right side receives an inward heat flux of 10<sup>6</sup> W m<sup>−2</sup>. '
         'With k = 450 W m<sup>−1</sup> K<sup>−1</sup>, determine the temperature at node 5.</div>')
    body = (head + q + A.fig("fig_mesh_flux", "The plate of Example 2 with the global node numbers.", "Plat bagi Contoh 2 dengan nombor node global.", 440)
            + PIC("The heat entering at the right side, 10<sup>6</sup>(0.005)(0.05) = 250 W, must all leave through the left side; with the top and bottom insulated it flows straight across, so T depends on x only. With no source the gradient is constant, q<sub>n</sub>/k = 2222 K m<sup>−1</sup>, so expect T = 400 + 2222x: 455.6 K at the middle column and 511.1 K at the right side. A bilinear element contains this linear field, so the finite element solution should reproduce it.",
                  "Haba yang masuk pada sisi kanan, 10<sup>6</sup>(0.005)(0.05) = 250 W, mesti semuanya keluar melalui sisi kiri; dengan atas dan bawah insulated ia mengalir terus melintang, jadi T bergantung pada x sahaja. Tanpa source, gradient-nya malar, q<sub>n</sub>/k = 2222 K m<sup>−1</sup>, jadi jangkakan T = 400 + 2222x: 455.6 K pada lajur tengah dan 511.1 K pada sisi kanan. Element bilinear mengandungi field linear ini, jadi penyelesaian finite element sepatutnya menghasilkannya semula.")
            + PLAN("[k] of Example 1 → assemble 9 × 9 → flux loads at nodes 3, 6, 9 → strike nodes 1, 4, 7 → solve by columns → check a full row → energy balance.")
            + XSTEP(1, "Element matrices and assembly", "Matrix element dan assembly", 5, P("The four elements are identical to that of Example 1. With element 1 on nodes 1, 2, 5, 4 (local 1, 2, 3, 4), element 2 on 2, 3, 6, 5, element 3 on 4, 5, 8, 7 and element 4 on 5, 6, 9, 8:", "Keempat-empat element serupa dengan element Contoh 1. Dengan element 1 pada node 1, 2, 5, 4 (local 1, 2, 3, 4), element 2 pada 2, 3, 6, 5, element 3 pada 4, 5, 8, 7 dan element 4 pada 5, 6, 9, 8:")
                    + A.eq("y2_K") + P("Corner nodes have ts<sub>1</sub> = 1.5, side nodes 2ts<sub>1</sub> = 3, the centre 4ts<sub>1</sub> = 6 W K<sup>−1</sup>.", "Node bucu mempunyai ts<sub>1</sub> = 1.5, node sisi 2ts<sub>1</sub> = 3, pusat 4ts<sub>1</sub> = 6 W K<sup>−1</sup>."))
            + XSTEP(2, "Loads", "Load", 3, P("The flux enters through sides 3–6 and 6–9, each giving 62.5 W to each of its nodes (Example 1):", "Flux masuk melalui sisi 3–6 dan 6–9, setiap satu memberi 62.5 W kepada setiap node-nya (Contoh 1):") + A.eq("y2_loads"))
            + XSTEP(3, "Boundary conditions", "Boundary condition", 3, P("T<sub>1</sub> = T<sub>4</sub> = T<sub>7</sub> = 400 K: strike rows and columns 1, 4, 7 and subtract K<sub>i1</sub>(400) + K<sub>i4</sub>(400) + K<sub>i7</sub>(400) from the right-hand side. Six unknowns remain.", "T<sub>1</sub> = T<sub>4</sub> = T<sub>7</sub> = 400 K: buang baris dan lajur 1, 4, 7 dan tolak K<sub>i1</sub>(400) + K<sub>i4</sub>(400) + K<sub>i7</sub>(400) daripada sebelah kanan. Enam unknown tinggal."))
            + XSTEP(4, "Solution by columns", "Penyelesaian mengikut lajur", 5, P("Since T does not vary with y, the middle column shares one value and the right column another. Adding the three equations of the middle column (rows 2, 5, 8) and the three of the right column (rows 3, 6, 9):", "Oleh kerana T tidak berubah dengan y, lajur tengah berkongsi satu nilai dan lajur kanan satu nilai lain. Menambah tiga persamaan lajur tengah (baris 2, 5, 8) dan tiga persamaan lajur kanan (baris 3, 6, 9):")
                    + A.eq("y2_cols") + A.eq("y2_sol") + CHK(A.eq("y2_check", None, 0.5)) + ANS("T<sub>5</sub> = 455.6 K (and T<sub>2</sub> = T<sub>8</sub> = 455.6, T<sub>3</sub> = T<sub>6</sub> = T<sub>9</sub> = 511.1 K)."))
            + XSTEP(5, "Energy balance", "Energy balance", 4, A.eq("y2_bal"))
            + INTERP("The finite element temperatures equal the exact 400 + q<sub>n</sub>x/k at every node, as expected: the exact field is linear, and a bilinear element represents a linear field exactly. Two features of the data make the column shortcut valid, the insulated top and bottom and the uniform conditions on the left and right; with a flux on part of a side only, or a hole, T would vary with y and the six equations would have to be solved together. Doubling the thickness doubles both [K] and {R} and leaves the temperatures unchanged." + A.eq("y2_exact", None, 0.5),
                     "Temperature finite element sama dengan 400 + q<sub>n</sub>x/k yang tepat pada setiap node, seperti dijangka: field tepat adalah linear, dan element bilinear mewakili field linear dengan tepat. Dua ciri data menjadikan jalan pintas lajur itu sah, iaitu atas dan bawah yang insulated dan keadaan seragam di kiri dan kanan; dengan flux pada sebahagian sisi sahaja, atau satu lubang, T akan berubah dengan y dan enam persamaan itu perlu diselesaikan bersama. Menggandakan ketebalan menggandakan [K] dan {R} dan tidak mengubah temperature." + A.eq("y2_exact", None, 0.5))
            + SCHEME([("[K] assembled with the right multiplicities (1.5, 3, 6 on the diagonal)", "[K] di-assemble dengan gandaan yang betul (1.5, 3, 6 pada pepenjuru)", 5), ("Flux loads at nodes 3, 6, 9", "Load flux pada node 3, 6, 9", 3), ("Rows and columns 1, 4, 7 struck, 400 K moved to the right", "Baris dan lajur 1, 4, 7 dibuang, 400 K dipindahkan ke kanan", 3),
                      ("Column equations and T<sub>5</sub>; a full-row check", "Persamaan lajur dan T<sub>5</sub>; semakan satu baris penuh", 5), ("Struck rows give 250 W out = 250 W in", "Baris yang dibuang memberi 250 W keluar = 250 W masuk", 4)], 20))
    X.append(("y2", "A 2 × 2 mesh with a prescribed temperature and an inward flux", "Mesh 2 × 2 dengan temperature ditetapkan dan flux ke dalam", body))

    # ---- Example 3: the textbook's worked example (companion 8.7) ----
    head = ('<div class="xhead"><h2>' + B("Example 3 · Plate with a heat source: the textbook’s worked example", "Contoh 3 · Plat dengan heat source: contoh bekerja dalam teks") + '</h2>'
            '<div class="xmeta"><span><b>' + B("Exam type", "Jenis soalan") + '</b> 2 × 2 mesh, assembly, symmetry, energy balance, accuracy</span><span><b>' + B("Units", "Unit") + '</b> W, m, °C</span><span><b>' + B("Source", "Sumber") + '</b> FEM by Hand, Example 8.7 (textbook §2.3)</span><span><b>20 ' + B("marks", "markah") + '</b></span></div></div>')
    q = ('<div class="xq"><span class="qlabel">' + B("Question", "Soalan") + '</span>The square plate of the figure, 1 m by 1 m and of unit thickness, generates Q = 600 W m<sup>−3</sup> and has k = 300 W m<sup>−1</sup> °C<sup>−1</sup>. Its left and top edges are held at 0 °C; its bottom and right edges are insulated. '
         'With four equal Q4 elements, (a) form [k] and {r} of an element, (b) assemble, apply the boundary conditions and solve, and (c) check the energy balance and compare with the exact solution.</div>')
    body = (head + q + '<div class="figrow">' + A.fig("fig_plate_book", "The plate (textbook Figs. 2.5 and 2.6).", "Plat (teks Rajah 2.5 dan 2.6).", 300) + A.fig("fig_mesh_e1", "The mesh with its global node numbers.", "Mesh dengan nombor node global-nya.", 330) + '</div>'
            + PIC("The heat generated everywhere flows to the cold left and top edges, so the hottest point is the corner farthest from both, node 3 at (1, 0). The problem is symmetric about the diagonal through (0, 1) and (1, 0), so T<sub>2</sub> = T<sub>6</sub>. The insulated edges are lines of symmetry: the plate is one quarter of a 2 m square with all edges at 0 °C, whose centre temperature is 0.07367 Q(2)²/k = 0.589 °C.",
                  "Haba yang dijana di mana-mana mengalir ke tepi kiri dan atas yang sejuk, jadi titik paling panas ialah bucu paling jauh daripada kedua-duanya, node 3 pada (1, 0). Masalah ini simetri tentang pepenjuru melalui (0, 1) dan (1, 0), jadi T<sub>2</sub> = T<sub>6</sub>. Tepi insulated ialah garis simetri: plat ini ialah satu perempat daripada segi empat sama 2 m dengan semua tepi pada 0 °C, yang temperature pusatnya 0.07367 Q(2)²/k = 0.589 °C.")
            + PLAN("s<sub>1</sub> to s<sub>4</sub>, Qab/4 → assemble 9 × 9 → strike nodes 1, 4, 7, 8, 9 → T<sub>6</sub> = T<sub>2</sub> → 3 × 3 → heat flows → exact solution and convergence.")
            + XSTEP(1, "(a) Element matrices", "(a) Matrix element", 3, A.eq("y3_k"))
            + XSTEP(2, "(b) Assembly", "(b) Assembly", 4, P("Corner nodes belong to one element, side nodes to two and node 5 to four:", "Node bucu dimiliki satu element, node sisi dua dan node 5 empat:") + A.eq("y3_K")
                    + P("The complete 9 × 9 is (2.53) of the textbook; its rows for the free nodes, after striking T<sub>1</sub> = T<sub>4</sub> = T<sub>7</sub> = T<sub>8</sub> = T<sub>9</sub> = 0 (nothing moves to the right, since the prescribed temperatures are zero):", "9 × 9 yang lengkap ialah (2.53) dalam teks; barisnya bagi node bebas, selepas membuang T<sub>1</sub> = T<sub>4</sub> = T<sub>7</sub> = T<sub>8</sub> = T<sub>9</sub> = 0 (tiada yang berpindah ke kanan, kerana temperature yang ditetapkan ialah sifar):") + A.eq("y3_red"))
            + XSTEP(3, "(b) Solution with T₆ = T₂", "(b) Penyelesaian dengan T₆ = T₂", 5, P("Row 6 then repeats row 2, and the other three rows become", "Baris 6 kemudian mengulang baris 2, dan tiga baris yang lain menjadi") + A.eq("y3_sym")
                    + P("The second gives T<sub>3</sub> = 0.1875 + 0.5T<sub>2</sub> + 0.5T<sub>5</sub>. Substituting into the first and the third:", "Yang kedua memberi T<sub>3</sub> = 0.1875 + 0.5T<sub>2</sub> + 0.5T<sub>5</sub>. Menggantikan ke dalam yang pertama dan ketiga:") + A.eq("y3_solve") + A.eq("y3_T")
                    + CHK("Row 1 of the reduced system: 400(0.4821) − 50(0.6214) − 100(0.3857) − 100(0.4821) = 75.0 ✓") + ANS("(b) T<sub>2</sub> = T<sub>6</sub> = 0.482, T<sub>3</sub> = 0.621, T<sub>5</sub> = 0.386 °C, the textbook’s (2.55)."))
            + XSTEP(4, "(c) Energy balance", "(c) Energy balance", 4, A.eq("y3_bal") + P("All the heat generated, Q × area = 600 W, leaves through the cold edges.", "Semua haba yang dijana, Q × luas = 600 W, keluar melalui tepi sejuk."))
            + XSTEP(5, "(c) Comparison with the exact solution", "(c) Perbandingan dengan penyelesaian tepat", 4, A.eq("y3_exact")
                    + P("At nodes 2, 3 and 5 the 2 × 2 mesh is 5.1%, 5.4% and 6.5% high. For the corner temperature:", "Pada node 2, 3 dan 5, mesh 2 × 2 adalah 5.1%, 5.4% dan 6.5% tinggi. Bagi temperature bucu:")
                    + '<div class="tbl"><table><tr><th>' + B("mesh", "mesh") + '</th><th class="r">1 × 1</th><th class="r">2 × 2</th><th class="r">4 × 4</th><th class="r">8 × 8</th><th class="r">16 × 16</th><th class="r">' + B("exact", "tepat") + '</th></tr>'
                    + '<tr><td>T<sub>3</sub> (°C)</td><td class="r num">0.7500</td><td class="r num">0.6214</td><td class="r num">0.5968</td><td class="r num">0.5912</td><td class="r num">0.5898</td><td class="r num">0.5894</td></tr>'
                    + '<tr><td>' + B("error", "ralat") + '</td><td class="r num">+27.3%</td><td class="r num">+5.4%</td><td class="r num">+1.26%</td><td class="r num">+0.31%</td><td class="r num">+0.08%</td><td class="r num">–</td></tr></table></div>'
                    + ANS("(c) Energy balance 600 W in and out; the 2 × 2 mesh is 5–7% high at its nodes, and the error falls about four times each time the mesh is halved."))
            + INTERP("The error falls as h², the rate of bilinear elements for a smooth field, about four times for each halving of the mesh. Finite element temperatures are not bounds: the 2 × 2 Q4 mesh is above the exact values, while the textbook’s two eight-node elements give 0.4448 and 0.5836 °C, below them. The nodal temperatures are not exact here, as they were in Example 2, because the exact field is curved in both directions. Node 5 shows the averaging property of square meshes: 800T<sub>5</sub> = 100(T<sub>1</sub> + … + T<sub>9</sub> without T<sub>5</sub>) + 150, the mean of its eight neighbours plus the effect of the source.",
                     "Ralat jatuh sebagai h², kadar element bilinear bagi field yang licin, kira-kira empat kali bagi setiap pembahagian dua mesh. Temperature finite element bukan sempadan: mesh Q4 2 × 2 berada di atas nilai tepat, manakala dua element lapan node dalam teks memberi 0.4448 dan 0.5836 °C, di bawahnya. Nodal temperature tidak tepat di sini, tidak seperti dalam Contoh 2, kerana field tepat melengkung dalam kedua-dua arah. Node 5 menunjukkan sifat purata mesh segi empat sama: 800T<sub>5</sub> = 100(T<sub>1</sub> + … + T<sub>9</sub> tanpa T<sub>5</sub>) + 150, min lapan jirannya ditambah kesan source.")
            + SCHEME([("s<sub>1</sub>…s<sub>4</sub> and Qab/4", "s<sub>1</sub>…s<sub>4</sub> dan Qab/4", 3), ("Diagonal multiplicities and the reduced 4 × 4", "Gandaan pepenjuru dan 4 × 4 terkurang", 4), ("Symmetry used, 3 × 3 solved, a row check", "Simetri digunakan, 3 × 3 diselesaikan, semakan satu baris", 5),
                      ("Heat flows at the cold nodes summing to −600 W", "Aliran haba pada node sejuk berjumlah −600 W", 4), ("Comparison with the exact values and the h² rate", "Perbandingan dengan nilai tepat dan kadar h²", 4)], 20))
    X.append(("y3", "Plate with a heat source: the textbook’s example", "Plat dengan heat source: contoh dalam teks", body))
    return X
