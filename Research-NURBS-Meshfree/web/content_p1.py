# SPDX-License-Identifier: CC-BY-NC-SA-4.0 (text) AND MIT (code)
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Content of Part 1 of the NURBS-meshfree research primer: Foundations (B-splines, NURBS, reproducing kernels).

What: plain data read by build.py — page metadata, the Start plan, six notes sections, three worked examples,
five exercise generators (JavaScript), slides, Explorer tasks, glossary and the scripted guide steps. English and
Bahasa Melayu sit side by side (B(en, ms)); display equations are LaTeX, rendered to SVG by build.py.
Why: one source for the page, the search index, the guide and the tutor manifest. Every number quoted in the
examples is computed here by ../code/nmf_bspline_rk.py, so text and code cannot disagree.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
import nmf_bspline_rk as nm  # noqa: E402

EQS = {}          # equation id -> LaTeX


def B(en, ms):
    """Paired language spans."""
    return f'<span class="en">{en}</span><span class="ms">{ms}</span>'


def P(en, ms):
    return f"<p>{B(en, ms)}</p>"


def EQ(eid, tex, label=""):
    """Display equation placeholder; build.py swaps in the SVG and keeps the LaTeX as data-tex."""
    EQS[eid] = tex
    return f"%%EQ:{eid}:{label}%%"


def DEF(t_en, t_ms, en, ms, cls="def"):
    return f'<div class="{cls}"><b class="t">{B(t_en, t_ms)}</b>{B(en, ms)}</div>'


def KP(items):
    lis = "".join(f"<li>{B(en, ms)}</li>" for en, ms in items)
    return f'<details class="kp"><summary>{B("Key points", "Perkara utama")}</summary><ul>{lis}</ul></details>'


def QC(qid, q, opts, ans, fb):
    o = "".join(f'<button class="opt" type="button" data-k="{k}">{B(en, ms)}</button>' for k, en, ms in opts)
    return (f'<div class="qc" data-qc="{qid}" data-ans="{ans}" id="{qid}"><div class="h">{B("Quick check · not graded", "Semak cepat · tidak bergred")}</div>'
            f"<p>{B(*q)}</p><div class=\"opts\">{o}</div><p class=\"fb\" role=\"status\" hidden>{B(*fb)}</p></div>")


def STEP(t_en, t_ms, body):
    return f'<div class="step"><h4>{B(t_en, t_ms)}</h4><div class="bd">{body}</div></div>'


f6 = lambda v: f"{v:.6f}".rstrip("0").rstrip(".") if abs(v) > 1e-12 else "0"
f4 = lambda v: f"{v:.4f}"

# ------------------------------------------------------------------ numbers for the examples
T1 = [0, 0, 0, 0.5, 1, 1, 1]
TAB = nm.bspline_table(T1, 2, 0.75)
N1 = nm.bspline(T1, 2, 0.75)
GRV = nm.greville(T1, 2)
PSI2, D2 = nm.rk_standard(0.4, [0, 0.5, 1], 0.75, 1)
Q1 = nm.blossom(T1, 2)

META = {
    "app": "nmf", "part": "p1", "key": "nmf-p1-v1", "prefs": "nmf-prefs", "lab_key": "nmf-lab-rkbs-v1",
    "title": "NURBS–meshfree primer · Part 1 Foundations",
    "h1": B("Part 1 · Foundations: B-splines, NURBS and reproducing kernels", "Bahagian 1 · Asas: B-spline, NURBS dan reproducing kernel"),
    "kicker": B("RESEARCH PRIMER · FACULTY OF CIVIL ENGINEERING, UTM", "PRIMER PENYELIDIKAN · FAKULTI KEJURUTERAAN AWAM, UTM"),
    "desc": B("How a CAD curve is built from a knot vector, how a meshfree shape function is built from scattered nodes, "
              "and the exact point where the two meet: reproducing-kernel functions with blossom vectors are the B-splines. "
              "The map of the research area and how to read its papers close the part.",
              "Bagaimana CAD curve dibina daripada knot vector, bagaimana meshfree shape function dibina daripada node yang "
              "bertaburan, dan titik tepat pertemuan kedua-duanya: reproducing-kernel function dengan blossom vector ialah "
              "B-spline itu sendiri. Bahagian ini ditutup dengan peta bidang penyelidikan ini dan cara membaca artikelnya."),
    "crumb_topic": B("NURBS–meshfree primer", "Primer NURBS–meshfree"),
    "crumb_page": B("Part 1 of 4", "Bahagian 1 daripada 4"),
    "parts": [("01-foundations", B("Part 1", "Bhg. 1")), (None, B("Part 2", "Bhg. 2")), (None, B("Part 3", "Bhg. 3")), (None, B("Part 4", "Bhg. 4"))],
}

# ------------------------------------------------------------------ Start
START = {
    "who": B("For postgraduate research students and final-year project students joining the NURBS–meshfree work of the group. "
             "It assumes the finite element basics: weak form, shape functions, Gauss quadrature.",
             "Untuk pelajar penyelidikan pascasiswazah dan pelajar projek tahun akhir yang menyertai kerja NURBS–meshfree kumpulan ini. "
             "Ia menganggap asas finite element sudah dikuasai: weak form, shape function, Gauss quadrature."),
    "plan": {
        "before": {"min": 25, "items": [("read:n1", "notes/n1", "Read Notes §1 (6 min)", "Baca Nota §1 (6 min)"),
                                        ("read:n2", "notes/n2", "Read Notes §2 (10 min)", "Baca Nota §2 (10 min)"),
                                        ("recall:r1", "start/r1", "Recall question 1 (on this page)", "Soalan imbas kembali 1 (di page ini)")]},
        "in": {"label": B("Meeting · 2 h · 3 activities", "Perjumpaan · 2 j · 3 aktiviti"),
               "items": [(None, None, "A1 Cox–de Boor by hand at ξ = 0.75 (Example 1)", "A1 Cox–de Boor dengan tangan pada ξ = 0.75 (Contoh 1)"),
                         (None, None, "A2 an RK shape function at a point (Example 2)", "A2 RK shape function pada satu titik (Contoh 2)"),
                         ("ms:m2", "lab", "A3 Explorer task 2: the kernel does not matter", "A3 Tugasan Explorer 2: kernel tidak memberi kesan")]},
        "after": {"min": 110, "items": [("notes", "notes", "Notes §1–§6 (50 min)", "Nota §1–§6 (50 min)"),
                                         ("slides", "slides", "Slides, all 11", "Slides, kesemua 11"),
                                         ("examples", "examples", "Worked examples (3)", "Contoh berkerja (3)"),
                                         ("exercises", "exercises", "Exercises 1–5 (~35 min)", "Latihan 1–5 (~35 min)"),
                                         ("lab", "lab", "Explorer tasks 1–4", "Tugasan Explorer 1–4"),
                                         ("cando", "start/cando", "Can-do checklist", "Senarai semak boleh-buat")]},
    },
    "covers": B("Part 1 builds the two vocabularies the research area speaks — splines and reproducing kernels — and shows that they "
                "describe the same functions when the nodes carry blossom vectors. Parts 2–4 build on it: coupling IGA with meshfree "
                "regions, integration and boundary conditions that keep the methods consistent, and the group's own NURBS-based "
                "meshless methods (N-RPIM, NDM).",
                "Bahagian 1 membina dua perbendaharaan kata yang digunakan dalam bidang ini — spline dan reproducing kernel — dan "
                "menunjukkan bahawa kedua-duanya menggambarkan function yang sama apabila node membawa blossom vector. Bahagian 2–4 "
                "dibina di atasnya: coupling IGA dengan kawasan meshfree, integration dan boundary condition yang mengekalkan "
                "konsistensi kaedah, dan kaedah meshless berasaskan NURBS milik kumpulan ini (N-RPIM, NDM)."),
    "outcomes": [
        ("Evaluate B-spline basis functions and their derivatives from a knot vector by the Cox–de Boor recursion.",
         "Menilai B-spline basis function dan derivative-nya daripada knot vector dengan rekursi Cox–de Boor."),
        ("Explain what the weights of a NURBS curve do, and evaluate a point of the exact quarter circle.",
         "Menerangkan peranan weight dalam NURBS curve, dan menilai satu titik pada quarter circle yang tepat."),
        ("Derive the reproducing-kernel shape function from the reproducing conditions and compute it at a point.",
         "Menerbitkan reproducing-kernel shape function daripada reproducing condition dan mengiranya pada satu titik."),
        ("Show why RK functions with blossom vectors and B-spline supports are the B-splines, whatever the kernel.",
         "Menunjukkan mengapa RK function dengan blossom vector dan support B-spline ialah B-spline itu sendiri, apa pun kernel-nya."),
        ("List the hidden parameters to check before claiming to reproduce a NURBS–meshfree paper.",
         "Menyenaraikan hidden parameter yang perlu disemak sebelum mendakwa telah menghasilkan semula keputusan sesuatu artikel NURBS–meshfree."),
    ],
    "reference": B("Reference texts: Piegl & Tiller, <i>The NURBS Book</i> (2nd ed., Springer, 1997), Ch. 2; Cottrell, Hughes & Bazilevs, "
                   "<i>Isogeometric Analysis</i> (Wiley, 2009), Ch. 2; Liu, Jun & Zhang, IJNMF 20 (1995) 1081–1106 for RKPM.",
                   "Teks rujukan: Piegl & Tiller, <i>The NURBS Book</i> (ed. ke-2, Springer, 1997), Bab 2; Cottrell, Hughes & Bazilevs, "
                   "<i>Isogeometric Analysis</i> (Wiley, 2009), Bab 2; Liu, Jun & Zhang, IJNMF 20 (1995) 1081–1106 untuk RKPM."),
    "recall": [
        ("r1", ("State the Cox–de Boor recursion in words.", "Nyatakan rekursi Cox–de Boor dengan perkataan."),
         ("A degree-p B-spline is a blend of two degree-(p − 1) B-splines: the left one weighted by how far ξ has moved into its support, "
          "the right one by how far ξ still is from the end of the next support. Degree 0 is 1 on one knot span and 0 elsewhere.",
          "B-spline darjah p ialah campuran dua B-spline darjah (p − 1): yang kiri diberi weight mengikut sejauh mana ξ telah masuk ke "
          "dalam support-nya, yang kanan mengikut jarak ξ dari hujung support berikutnya. Darjah 0 bernilai 1 pada satu knot span dan 0 di tempat lain.")),
        ("r2", ("What do the reproducing conditions require of the shape functions?", "Apakah yang dituntut oleh reproducing condition terhadap shape function?"),
         ("That the approximation returns every polynomial up to degree p exactly: Σ Ψ<sub>I</sub>(x) {H(x<sub>I</sub>)} = {H(x)}. "
          "The first row is the partition of unity.",
          "Bahawa approximation memulangkan setiap polinomial sehingga darjah p dengan tepat: Σ Ψ<sub>I</sub>(x) {H(x<sub>I</sub>)} = {H(x)}. "
          "Baris pertama ialah partition of unity.")),
        ("r3", ("Write the blossom vector of a quadratic B-spline.", "Tulis blossom vector bagi quadratic B-spline."),
         ("{Q<sub>I</sub>} = {1, (t<sub>I+1</sub> + t<sub>I+2</sub>)/2, t<sub>I+1</sub> t<sub>I+2</sub>}<sup>T</sup>: one, the Greville abscissa, "
          "and the product of the two interior knots of the support.",
          "{Q<sub>I</sub>} = {1, (t<sub>I+1</sub> + t<sub>I+2</sub>)/2, t<sub>I+1</sub> t<sub>I+2</sub>}<sup>T</sup>: satu, Greville abscissa, "
          "dan hasil darab dua knot dalaman bagi support itu.")),
    ],
    "cando": [
        ("Evaluate N<sub>I,p</sub>(ξ) by hand on a short knot vector.", "Menilai N<sub>I,p</sub>(ξ) dengan tangan pada knot vector yang pendek."),
        ("Evaluate a NURBS curve point and check it lies on the circle.", "Menilai satu titik NURBS curve dan menyemak ia terletak pada bulatan."),
        ("Derive Ψ<sub>I</sub> from the reproducing conditions.", "Menerbitkan Ψ<sub>I</sub> daripada reproducing condition."),
        ("Explain why RK with blossom vectors equals the B-splines.", "Menerangkan mengapa RK dengan blossom vector sama dengan B-spline."),
        ("List the hidden parameters of a meshfree paper.", "Menyenaraikan hidden parameter dalam artikel meshfree."),
    ],
}

# ------------------------------------------------------------------ Notes
NOTES = []

NOTES.append({"id": "n1", "min": 6, "title": ("The research problem: exact geometry meets meshfree flexibility",
                                              "Masalah penyelidikan: geometri tepat bertemu fleksibiliti meshfree"), "html":
    P("A finite element mesh only approximates the geometry that a designer drew in CAD. The CAD model itself is made of "
      "NURBS: smooth, exact, and described by a handful of control points. Two families of methods try to close the gap "
      "between design and analysis, and this research area lives where they meet.",
      "Mesh finite element hanya menghampiri geometri yang dilukis oleh pereka dalam CAD. Model CAD itu sendiri dibina "
      "daripada NURBS: licin, tepat, dan diterangkan oleh beberapa control point sahaja. Dua keluarga kaedah cuba merapatkan "
      "jurang antara rekabentuk dan analisis, dan bidang penyelidikan ini terletak di tempat kedua-duanya bertemu.")
    + DEF("Isogeometric analysis (IGA)", "Isogeometric analysis (IGA)",
          "Use the NURBS basis that describes the CAD geometry as the basis of the analysis too (Hughes, Cottrell & Bazilevs, "
          "CMAME 194 (2005) 4135–4195). The geometry is exact at every refinement; the price is the tensor-product structure of "
          "the patches, which makes local refinement and complex topology awkward.",
          "Guna NURBS basis yang menerangkan geometri CAD sebagai basis analisis juga (Hughes, Cottrell & Bazilevs, CMAME 194 "
          "(2005) 4135–4195). Geometri kekal tepat pada setiap refinement; harganya ialah struktur tensor-product bagi patch, "
          "yang menyukarkan local refinement dan topologi yang kompleks.")
    + DEF("Meshfree methods", "Meshfree method",
          "Build the shape functions from scattered nodes and their supports, with no element connectivity: EFG (Belytschko, "
          "Lu & Gu 1994), RKPM (Liu, Jun & Zhang 1995), RPIM and others. Nodes can be added anywhere; the price is paid at the "
          "boundary (no Kronecker delta, so essential conditions need care), in the integration, and in the cost of each "
          "shape function.",
          "Bina shape function daripada node yang bertaburan dan support-nya, tanpa element connectivity: EFG (Belytschko, "
          "Lu & Gu 1994), RKPM (Liu, Jun & Zhang 1995), RPIM dan lain-lain. Node boleh ditambah di mana-mana; harganya dibayar "
          "di sempadan (tiada Kronecker delta, jadi essential condition perlu dikendalikan dengan teliti), dalam integration, "
          "dan dalam kos setiap shape function.")
    + f'<h3>{B("A map of the area", "Peta bidang ini")}</h3>'
    + P("The primer follows the papers the group has studied from first principles. They answer four questions, one per part:",
        "Primer ini mengikut artikel yang telah dikaji oleh kumpulan ini dari prinsip pertama. Kertas kerja itu menjawab "
        "empat soalan, satu bagi setiap bahagian:")
    + '<div class="tbl"><table><tr>' + "".join(f"<th>{B(a, b)}</th>" for a, b in [("Part", "Bahagian"), ("Question", "Soalan"), ("Papers", "Kertas kerja")]) + "</tr>"
    + "".join(f"<tr><td>{a}</td><td>{B(b, c)}</td><td>{d}</td></tr>" for a, b, c, d in [
        ("1", "Can a reproducing kernel produce the B-splines exactly?", "Bolehkah reproducing kernel menghasilkan B-spline dengan tepat?",
         "Zhang &amp; Wang (2017)"),
        ("2", "How do IGA and meshfree regions share one consistent approximation?", "Bagaimana kawasan IGA dan meshfree berkongsi satu approximation yang consistent?",
         "Wang &amp; Zhang (2014); Valizadeh et al. (2015); Shaw, Banerjee &amp; Roy (2008)"),
        ("3", "What integration and boundary treatment keeps the method exact for polynomials?", "Integration dan rawatan sempadan apakah yang mengekalkan ketepatan kaedah untuk polinomial?",
         "Chen, Hillman &amp; Rüter (2013); Chi &amp; Lin (2016)"),
        ("4", "What do NURBS-based meshless methods (N-RPIM, NDM) gain, and what must they prove?", "Apakah yang diperoleh kaedah meshless berasaskan NURBS (N-RPIM, NDM), dan apakah yang mesti dibuktikan?",
         "Mokhtaram et al. (2022); Rasin et al. (2025)")]) + "</table></div>"
    + DEF("Three things to keep apart", "Tiga perkara yang mesti dipisahkan",
          "The <i>geometry map</i> (how parameters become points), the <i>field approximation</i> (how the unknown is interpolated) "
          "and the <i>integration cells</i> (where the quadrature points sit). IGA uses one basis for the first two; the methods "
          "of this area deliberately separate them, and most of the difficulties come from forgetting which is which.",
          "<i>Geometry map</i> (bagaimana parameter menjadi titik), <i>field approximation</i> (bagaimana unknown di-interpolate) "
          "dan <i>integration cell</i> (tempat quadrature point terletak). IGA menggunakan satu basis untuk dua yang pertama; kaedah "
          "dalam bidang ini sengaja memisahkannya, dan kebanyakan kesukaran datang daripada terlupa yang mana satu.", "note")
    + KP([("IGA analyses with the CAD basis itself: exact geometry, rigid tensor-product structure.",
           "IGA menganalisis dengan CAD basis itu sendiri: geometri tepat, struktur tensor-product yang tegar."),
          ("Meshfree methods build shape functions from nodes: flexible refinement, harder boundaries and integration.",
           "Meshfree method membina shape function daripada node: refinement yang fleksibel, sempadan dan integration yang lebih sukar."),
          ("Keep geometry map, field approximation and integration cells apart.",
           "Pisahkan geometry map, field approximation dan integration cell.")])
    + QC("q1", ("What does isogeometric analysis use as the basis of the analysis?", "Apakah yang digunakan oleh isogeometric analysis sebagai basis analisis?"),
         [("a", "Lagrange polynomials on a mesh that approximates the CAD geometry", "Lagrange polynomial pada mesh yang menghampiri geometri CAD"),
          ("b", "The NURBS basis that describes the CAD geometry", "NURBS basis yang menerangkan geometri CAD"),
          ("c", "Radial basis functions centred on the control points", "Radial basis function yang berpusat pada control point")], "b",
         ("The NURBS basis of the CAD model, so the geometry is exact at every refinement.",
          "NURBS basis bagi model CAD, jadi geometri kekal tepat pada setiap refinement."))})

NOTES.append({"id": "n2", "min": 10, "title": ("B-splines from a knot vector", "B-spline daripada knot vector"), "html":
    P("A <b>knot vector</b> is a non-decreasing list of parameter values Ξ = {t<sub>1</sub>, t<sub>2</sub>, …, t<sub>n+p+1</sub>}. "
      "It defines n basis functions of degree p. An <b>open</b> knot vector repeats its first and last values p + 1 times, so the "
      "curve starts and ends at its first and last control points. The intervals [t<sub>i</sub>, t<sub>i+1</sub>) of non-zero length are the <b>knot spans</b>.",
      "<b>Knot vector</b> ialah senarai nilai parameter yang tidak menurun Ξ = {t<sub>1</sub>, t<sub>2</sub>, …, t<sub>n+p+1</sub>}. "
      "Ia mentakrifkan n basis function berdarjah p. Knot vector <b>open</b> mengulang nilai pertama dan terakhirnya sebanyak p + 1 kali, "
      "jadi curve bermula dan berakhir pada control point pertama dan terakhir. Selang [t<sub>i</sub>, t<sub>i+1</sub>) yang panjangnya bukan sifar ialah <b>knot span</b>.")
    + f'<h3>{B("The Cox–de Boor recursion", "Rekursi Cox–de Boor")}</h3>'
    + P("Start with piecewise constants, one per knot span, and raise the degree one step at a time:",
        "Mulakan dengan piecewise constant, satu bagi setiap knot span, dan naikkan darjah selangkah demi selangkah:")
    + EQ("e_cdb0", r"N_{I,0}(\xi)=\begin{cases}1, & t_I\le \xi< t_{I+1}\\ 0, & \text{otherwise}\end{cases}", "2.1")
    + EQ("e_cdb", r"N_{I,p}(\xi)=\frac{\xi-t_I}{t_{I+p}-t_I}\,N_{I,p-1}(\xi)+\frac{t_{I+p+1}-\xi}{t_{I+p+1}-t_{I+1}}\,N_{I+1,p-1}(\xi)", "2.2")
    + '<div class="sb">' + P("A fraction with a zero denominator (a repeated knot) is taken as zero. Each degree-p function is a blend of two "
                             "degree-(p − 1) neighbours, so N<sub>I,p</sub> is non-zero only on [t<sub>I</sub>, t<sub>I+p+1</sub>): p + 1 knot spans.",
                             "Pecahan dengan penyebut sifar (knot berulang) diambil sebagai sifar. Setiap function darjah p ialah campuran dua jiran "
                             "darjah (p − 1), jadi N<sub>I,p</sub> bukan sifar hanya pada [t<sub>I</sub>, t<sub>I+p+1</sub>): p + 1 knot span.") + "</div>"
    + P("The derivative follows from the same two neighbours, one degree lower:", "Derivative diperoleh daripada dua jiran yang sama, satu darjah lebih rendah:")
    + EQ("e_cdbd", r"\frac{dN_{I,p}}{d\xi}=\frac{p}{t_{I+p}-t_I}\,N_{I,p-1}(\xi)-\frac{p}{t_{I+p+1}-t_{I+1}}\,N_{I+1,p-1}(\xi)", "2.3")
    + f'<h3>{B("Properties used everywhere in this area", "Sifat yang digunakan di mana-mana dalam bidang ini")}</h3>'
    + EQ("e_pu", r"\sum_{I=1}^{n}N_{I,p}(\xi)=1,\qquad N_{I,p}(\xi)\ge 0", "2.4")
    + "<ul>" + "".join(f"<li>{B(a, b)}</li>" for a, b in [
        ("<b>Partition of unity</b> and non-negativity (2.4): a convex blend of control points.", "<b>Partition of unity</b> dan tidak negatif (2.4): campuran convex bagi control point."),
        ("<b>Local support</b>: on one knot span only p + 1 functions are non-zero.", "<b>Local support</b>: pada satu knot span hanya p + 1 function yang bukan sifar."),
        ("<b>Continuity</b> C<sup>p−m</sup> across a knot repeated m times; C<sup>∞</sup> inside a span.", "<b>Continuity</b> C<sup>p−m</sup> merentasi knot yang berulang m kali; C<sup>∞</sup> di dalam span."),
        ("<b>Linear reproduction</b> with the Greville abscissae (2.5): the B-splines can be read as functions attached to nodes ξ̄<sub>I</sub>.",
         "<b>Linear reproduction</b> dengan Greville abscissa (2.5): B-spline boleh dibaca sebagai function yang terikat pada node ξ̄<sub>I</sub>.")]) + "</ul>"
    + EQ("e_grev", r"\bar\xi_I=\frac{t_{I+1}+t_{I+2}+\dots+t_{I+p}}{p},\qquad \sum_{I=1}^{n}N_{I,p}(\xi)\,\bar\xi_I=\xi", "2.5")
    + STEP("Worked step · counting and the Greville points", "Langkah berkerja · mengira dan Greville point",
           P("Quadratic (p = 2), Ξ = {0, 0, 0, 0.5, 1, 1, 1}: seven knots, so n = 7 − 2 − 1 = 4 functions on two spans. The Greville points are "
             f"ξ̄ = {{{', '.join(f6(v) for v in GRV)}}}. At ξ = 0.75 (second span) the recursion gives N = {{{', '.join(f6(v) for v in N1)}}}; "
             f"the sum is 1 and Σ N<sub>I</sub> ξ̄<sub>I</sub> = {f6(float(N1 @ GRV))} = ξ. Example 1 shows every step.",
             "Quadratic (p = 2), Ξ = {0, 0, 0, 0.5, 1, 1, 1}: tujuh knot, jadi n = 7 − 2 − 1 = 4 function pada dua span. Greville point ialah "
             f"ξ̄ = {{{', '.join(f6(v) for v in GRV)}}}. Pada ξ = 0.75 (span kedua) rekursi memberi N = {{{', '.join(f6(v) for v in N1)}}}; "
             f"hasil tambahnya 1 dan Σ N<sub>I</sub> ξ̄<sub>I</sub> = {f6(float(N1 @ GRV))} = ξ. Contoh 1 menunjukkan setiap langkah."))
    + KP([("Cox–de Boor: degree 0 on spans, then blend two neighbours per degree (2.1)–(2.2).", "Cox–de Boor: darjah 0 pada span, kemudian campur dua jiran bagi setiap darjah (2.1)–(2.2)."),
          ("n = (number of knots) − p − 1; p + 1 non-zero functions per span.", "n = (bilangan knot) − p − 1; p + 1 function bukan sifar bagi setiap span."),
          ("Greville points make the B-splines reproduce ξ: they act as nodes.", "Greville point menjadikan B-spline reproduce ξ: ia bertindak sebagai node.")])
    + QC("q2", ("How many quadratic B-splines does Ξ = {0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 1} define?", "Berapakah bilangan quadratic B-spline yang ditakrifkan oleh Ξ = {0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 1}?"),
         [("a", "4", "4"), ("b", "6", "6"), ("c", "8", "8")], "b",
         ("Nine knots, p = 2: n = 9 − 2 − 1 = 6.", "Sembilan knot, p = 2: n = 9 − 2 − 1 = 6."))})

NOTES.append({"id": "n3", "min": 8, "title": ("NURBS and the geometry map", "NURBS dan geometry map"), "html":
    P("Polynomials cannot draw a circle exactly. Giving each B-spline a positive <b>weight</b> λ<sub>I</sub> and normalising makes the basis "
      "rational, and rational quadratics represent every conic section exactly.",
      "Polinomial tidak boleh melukis bulatan dengan tepat. Memberi setiap B-spline <b>weight</b> λ<sub>I</sub> yang positif dan menormalkannya "
      "menjadikan basis itu rasional, dan rational quadratic mewakili setiap conic section dengan tepat.")
    + EQ("e_nurbs", r"R_I(\xi)=\frac{\lambda_I\,N_{I,p}(\xi)}{\sum_{J=1}^{n}\lambda_J\,N_{J,p}(\xi)}", "3.1")
    + EQ("e_curve", r"\{x(\xi)\}=\sum_{I=1}^{n}R_I(\xi)\,\{P_I\}", "3.2")
    + P("With all weights equal, R<sub>I</sub> = N<sub>I,p</sub>. The R<sub>I</sub> keep the partition of unity and the local support, but "
        "they no longer reproduce ξ with the Greville points — a fact that matters in Part 2, when a meshfree correction must make up "
        "what the rational functions miss.",
        "Apabila semua weight sama, R<sub>I</sub> = N<sub>I,p</sub>. R<sub>I</sub> mengekalkan partition of unity dan local support, tetapi "
        "tidak lagi reproduce ξ dengan Greville point — fakta yang penting dalam Bahagian 2, apabila pembetulan meshfree mesti menampung "
        "apa yang tidak dicapai oleh function rasional itu.")
    + STEP("Worked step · the exact quarter circle", "Langkah berkerja · quarter circle yang tepat",
           P("Quadratic, Ξ = {0, 0, 0, 1, 1, 1}, control points (1, 0), (1, 1), (0, 1), weights 1, 1/√2, 1. At ξ = 0.5 the B-splines are "
             "¼, ½, ¼; the weighted values ¼, 0.3536, ¼ sum to 0.8536, so R = {0.2929, 0.4142, 0.2929} and x = y = 0.7071: radius exactly 1. "
             "Without the weight (λ<sub>2</sub> = 1) the same point lands at (0.75, 0.75), radius 1.0607.",
             "Quadratic, Ξ = {0, 0, 0, 1, 1, 1}, control point (1, 0), (1, 1), (0, 1), weight 1, 1/√2, 1. Pada ξ = 0.5 nilai B-spline ialah "
             "¼, ½, ¼; nilai berweight ¼, 0.3536, ¼ berjumlah 0.8536, jadi R = {0.2929, 0.4142, 0.2929} dan x = y = 0.7071: jejari tepat 1. "
             "Tanpa weight (λ<sub>2</sub> = 1) titik yang sama jatuh pada (0.75, 0.75), jejari 1.0607."))
    + f'<h3>{B("Surfaces, the map and its Jacobian", "Surface, map dan Jacobian-nya")}</h3>'
    + P("A NURBS surface is the tensor product of two curve bases, R<sub>IJ</sub>(ξ, η) = λ<sub>IJ</sub> N<sub>I</sub>(ξ) M<sub>J</sub>(η) / W(ξ, η), and the "
        "geometry map takes the parameter square to the physical patch. Derivatives in x and y come through the Jacobian, written in the "
        "row convention used throughout the primer:",
        "NURBS surface ialah tensor product bagi dua curve basis, R<sub>IJ</sub>(ξ, η) = λ<sub>IJ</sub> N<sub>I</sub>(ξ) M<sub>J</sub>(η) / W(ξ, η), dan "
        "geometry map membawa segi empat parameter kepada patch fizikal. Derivative dalam x dan y diperoleh melalui Jacobian, ditulis dalam "
        "row convention yang digunakan sepanjang primer ini:")
    + EQ("e_jac", r"\begin{Bmatrix}\partial f/\partial x\\ \partial f/\partial y\end{Bmatrix}=[J]^{-1}\begin{Bmatrix}\partial f/\partial\xi\\ \partial f/\partial\eta\end{Bmatrix},\qquad [J]=\begin{bmatrix}\partial x/\partial\xi & \partial y/\partial\xi\\ \partial x/\partial\eta & \partial y/\partial\eta\end{bmatrix}", "3.3")
    + DEF("Where meshfree methods enter", "Di mana meshfree method masuk",
          "Every method of Parts 2–4 keeps the NURBS map (3.2)–(3.3) for the geometry. What changes is the field: some or all of the "
          "unknown is interpolated by meshfree functions instead of R<sub>I</sub>, either in the parameter square or in physical space.",
          "Setiap kaedah dalam Bahagian 2–4 mengekalkan NURBS map (3.2)–(3.3) untuk geometri. Yang berubah ialah field: sebahagian atau "
          "keseluruhan unknown di-interpolate oleh meshfree function dan bukannya R<sub>I</sub>, sama ada dalam segi empat parameter atau dalam ruang fizikal.", "note")
    + KP([("Weights make the basis rational; rational quadratics draw conics exactly.", "Weight menjadikan basis rasional; rational quadratic melukis conic dengan tepat."),
          ("R<sub>I</sub> keep partition of unity and local support but not linear reproduction.", "R<sub>I</sub> mengekalkan partition of unity dan local support tetapi bukan linear reproduction."),
          ("Derivatives in x, y: {∂f/∂x} = [J]<sup>−1</sup>{∂f/∂ξ}, row convention.", "Derivative dalam x, y: {∂f/∂x} = [J]<sup>−1</sup>{∂f/∂ξ}, row convention.")])
    + QC("q3", ("Why does an exact circle need NURBS rather than B-splines?", "Mengapa bulatan yang tepat memerlukan NURBS dan bukannya B-spline?"),
         [("a", "Polynomial B-splines cannot represent conic sections exactly; rational weights can", "B-spline polinomial tidak dapat mewakili conic section dengan tepat; weight rasional boleh"),
          ("b", "B-splines are not smooth enough on a circle", "B-spline tidak cukup licin pada bulatan"),
          ("c", "NURBS need fewer control points than B-splines for any curve", "NURBS memerlukan lebih sedikit control point berbanding B-spline untuk sebarang curve")], "a",
         ("A circle is a conic; only a rational parametrisation draws it exactly. Smoothness is not the issue.",
          "Bulatan ialah conic; hanya parametrisation rasional yang melukisnya dengan tepat. Kelicinan bukan isunya."))})

NOTES.append({"id": "n4", "min": 10, "title": ("Reproducing kernel shape functions", "Reproducing kernel shape function"), "html":
    P("A meshfree method writes the unknown as a sum over nodes, with no elements:", "Meshfree method menulis unknown sebagai hasil tambah ke atas node, tanpa element:")
    + EQ("e_appr", r"u^h(x)=\sum_{I=1}^{n}\Psi_I(x)\,\hat u_I", "4.1")
    + P("Each node I carries a <b>kernel</b> (window) W<sub>I</sub>(x) of support radius a. The shape functions are required to reproduce every "
        "polynomial up to degree p — the <b>reproducing conditions</b>, with {H(x)} = {1, x, …, x<sup>p</sup>}<sup>T</sup>:",
        "Setiap node I membawa <b>kernel</b> (window) W<sub>I</sub>(x) dengan jejari support a. Shape function dituntut supaya reproduce setiap "
        "polinomial sehingga darjah p — <b>reproducing condition</b>, dengan {H(x)} = {1, x, …, x<sup>p</sup>}<sup>T</sup>:")
    + EQ("e_repr", r"\sum_{I=1}^{n}\Psi_I(x)\,\{H(x_I)\}=\{H(x)\}", "4.2")
    + f'<h3>{B("Derivation, step by step", "Terbitan, langkah demi langkah")}</h3>'
    + STEP("Step 1 · correct the kernel by a polynomial", "Langkah 1 · betulkan kernel dengan satu polinomial",
           P("Take the kernel and multiply it by a polynomial in the node position, with coefficients {b(x)} still unknown:",
             "Ambil kernel dan darabkan dengan satu polinomial dalam kedudukan node, dengan pekali {b(x)} yang belum diketahui:")
           + EQ("e_ansatz", r"\Psi_I(x)=\{H(x_I)\}^T\{b(x)\}\,W_I(x)", "4.3"))
    + STEP("Step 2 · impose the reproducing conditions", "Langkah 2 · kenakan reproducing condition",
           P("Substitute (4.3) into (4.2). The coefficients come out of the sum, which leaves a (p + 1) × (p + 1) <b>moment matrix</b>:",
             "Gantikan (4.3) ke dalam (4.2). Pekali keluar daripada hasil tambah, dan yang tinggal ialah <b>moment matrix</b> (p + 1) × (p + 1):")
           + EQ("e_mom", r"[M(x)]\{b(x)\}=\{H(x)\},\qquad [M(x)]=\sum_{J=1}^{n}\{H(x_J)\}\{H(x_J)\}^T W_J(x)", "4.4"))
    + STEP("Step 3 · solve and substitute back", "Langkah 3 · selesaikan dan gantikan semula",
           P("Solve for {b(x)} and put it back into (4.3):", "Selesaikan {b(x)} dan masukkan semula ke dalam (4.3):")
           + EQ("e_rk", r"\Psi_I(x)=\{H(x_I)\}^T[M(x)]^{-1}\{H(x)\}\,W_I(x)", "4.5"))
    + STEP("Step 4 · check the simplest case", "Langkah 4 · semak kes paling mudah",
           P("For p = 0, [M] = Σ W<sub>J</sub> and Ψ<sub>I</sub> = W<sub>I</sub> / Σ W<sub>J</sub>: the Shepard functions, a partition of unity. "
             "For p = 1 in 1D, one entry: M<sub>12</sub> = Σ x<sub>J</sub> W<sub>J</sub>(x); Example 2 computes all of them at x = 0.4.",
             "Untuk p = 0, [M] = Σ W<sub>J</sub> dan Ψ<sub>I</sub> = W<sub>I</sub> / Σ W<sub>J</sub>: Shepard function, satu partition of unity. "
             "Untuk p = 1 dalam 1D, satu entri: M<sub>12</sub> = Σ x<sub>J</sub> W<sub>J</sub>(x); Contoh 2 mengira semuanya pada x = 0.4."))
    + P("The kernel used in the primer is the cubic B-spline window, r = |x − x<sub>I</sub>| / a:",
        "Kernel yang digunakan dalam primer ini ialah cubic B-spline window, r = |x − x<sub>I</sub>| / a:")
    + EQ("e_kern", r"w(r)=\begin{cases}\tfrac23-4r^2+4r^3, & 0\le r\le\tfrac12\\[2pt] \tfrac43-4r+4r^2-\tfrac43 r^3, & \tfrac12<r\le 1\\[2pt] 0, & r>1\end{cases}", "4.6")
    + DEF("Two facts that drive the rest of the area", "Dua fakta yang menggerakkan seluruh bidang ini",
          "(1) [M(x)] must be invertible: at least p + 1 kernels must overlap x, so the support radius a cannot be too small. "
          "(2) Ψ<sub>I</sub>(x<sub>J</sub>) ≠ δ<sub>IJ</sub> in general: the functions do not interpolate, so essential boundary conditions "
          "need a transformation, Nitsche's method or a coupling with interpolating functions.",
          "(1) [M(x)] mesti invertible: sekurang-kurangnya p + 1 kernel mesti bertindih pada x, jadi jejari support a tidak boleh terlalu kecil. "
          "(2) Ψ<sub>I</sub>(x<sub>J</sub>) ≠ δ<sub>IJ</sub> secara umum: function itu tidak interpolate, jadi essential boundary condition "
          "memerlukan transformation, kaedah Nitsche atau coupling dengan function yang interpolate.")
    + '<div class="sb">' + P("Writing {H(x − x<sub>I</sub>)} instead of {H(x<sub>I</sub>)} (a shifted basis) gives the same Ψ<sub>I</sub> — the reproduced space "
                             "is the same — but a much better conditioned [M]; scale by the support as well, {H((x − x<sub>I</sub>)/a)}, and use it in code.",
                             "Menulis {H(x − x<sub>I</sub>)} dan bukannya {H(x<sub>I</sub>)} (shifted basis) memberi Ψ<sub>I</sub> yang sama — ruang yang di-reproduce "
                             "adalah sama — tetapi [M] yang jauh lebih baik conditioning-nya; skalakan juga dengan support, {H((x − x<sub>I</sub>)/a)}, dan guna itu dalam kod.") + "</div>"
    + KP([("Reproducing conditions (4.2) + kernel-times-polynomial ansatz (4.3) ⇒ Ψ<sub>I</sub> = {H(x<sub>I</sub>)}<sup>T</sup>[M]<sup>−1</sup>{H(x)} W<sub>I</sub>.",
           "Reproducing condition (4.2) + ansatz kernel-darab-polinomial (4.3) ⇒ Ψ<sub>I</sub> = {H(x<sub>I</sub>)}<sup>T</sup>[M]<sup>−1</sup>{H(x)} W<sub>I</sub>."),
          ("[M] invertible needs p + 1 overlapping kernels: support size matters.", "[M] invertible memerlukan p + 1 kernel yang bertindih: saiz support penting."),
          ("No Kronecker delta: essential conditions need special treatment.", "Tiada Kronecker delta: essential condition memerlukan rawatan khas.")])
    + QC("q4", ("Do RK shape functions satisfy Ψ<sub>I</sub>(x<sub>J</sub>) = δ<sub>IJ</sub>?", "Adakah RK shape function memenuhi Ψ<sub>I</sub>(x<sub>J</sub>) = δ<sub>IJ</sub>?"),
         [("a", "Yes, always", "Ya, sentiasa"), ("b", "No, not in general, so essential conditions need special treatment", "Tidak, secara umum tidak, jadi essential condition memerlukan rawatan khas"),
          ("c", "Only for p = 0", "Hanya untuk p = 0")], "b",
         ("They reproduce polynomials but do not interpolate; Example 2 shows Ψ at a node is not 1.", "Ia reproduce polinomial tetapi tidak interpolate; Contoh 2 menunjukkan Ψ pada node bukan 1."))})

NOTES.append({"id": "n5", "min": 10, "title": ("When RK becomes B-spline: blossom vectors", "Apabila RK menjadi B-spline: blossom vector"), "html":
    P("Compare (2.5) with (4.2): B-splines reproduce ξ with the Greville points in the role of node positions. They also reproduce ξ<sup>2</sup>, …, ξ<sup>p</sup>, "
      "but not with powers of ξ̄<sub>I</sub>. The right node vectors are the <b>blossom vectors</b> (Zhang &amp; Wang, CMAME 320 (2017) 474–508):",
      "Bandingkan (2.5) dengan (4.2): B-spline reproduce ξ dengan Greville point mengambil peranan kedudukan node. Ia juga reproduce ξ<sup>2</sup>, …, ξ<sup>p</sup>, "
      "tetapi bukan dengan kuasa bagi ξ̄<sub>I</sub>. Vector node yang betul ialah <b>blossom vector</b> (Zhang &amp; Wang, CMAME 320 (2017) 474–508):")
    + EQ("e_bloss", r"q_{I,l}=\frac{e_l(t_{I+1},\dots,t_{I+p})}{\binom{p}{l}},\qquad \{Q_I\}=\{1,\ q_{I,1},\ \dots,\ q_{I,p}\}^T", "5.1")
    + P("Here e<sub>l</sub> is the elementary symmetric polynomial of the p interior knots of the support (e<sub>1</sub> = sum, e<sub>p</sub> = product). "
        "q<sub>I,1</sub> is the Greville point. With these vectors the B-splines satisfy reproducing conditions of exactly the form (4.2) — Marsden's identity:",
        "Di sini e<sub>l</sub> ialah elementary symmetric polynomial bagi p knot dalaman support itu (e<sub>1</sub> = hasil tambah, e<sub>p</sub> = hasil darab). "
        "q<sub>I,1</sub> ialah Greville point. Dengan vector ini B-spline memenuhi reproducing condition yang bentuknya tepat seperti (4.2) — Marsden's identity:")
    + EQ("e_mars", r"\sum_{I=1}^{n}N_{I,p}(\xi)\,\{Q_I\}=\{H(\xi)\}", "5.2")
    + f'<h3>{B("The RK construction with blossom vectors", "Pembinaan RK dengan blossom vector")}</h3>'
    + P("Repeat Section 4 with {Q<sub>I</sub>} in place of {H(x<sub>I</sub>)}, and give node I a kernel whose support is the support of N<sub>I,p</sub>:",
        "Ulang Seksyen 4 dengan {Q<sub>I</sub>} menggantikan {H(x<sub>I</sub>)}, dan beri node I kernel yang support-nya ialah support bagi N<sub>I,p</sub>:")
    + EQ("e_rkq", r"\Psi_I(\xi)=\{Q_I\}^T[M(\xi)]^{-1}\{H(\xi)\}\,W_I(\xi),\qquad [M(\xi)]=\sum_{J}\{Q_J\}\{Q_J\}^T W_J(\xi)", "5.3")
    + STEP("Why the kernel cancels", "Mengapa kernel terbatal",
           P("On a knot span [t<sub>k</sub>, t<sub>k+1</sub>) exactly p + 1 supports are active, I = k − p, …, k. The reproducing conditions are p + 1 "
             "equations for these p + 1 values, and the vectors {Q<sub>I</sub>} are linearly independent, so the system is <b>square</b>:",
             "Pada satu knot span [t<sub>k</sub>, t<sub>k+1</sub>) tepat p + 1 support yang aktif, I = k − p, …, k. Reproducing condition ialah p + 1 "
             "persamaan bagi p + 1 nilai ini, dan vector {Q<sub>I</sub>} adalah linearly independent, jadi sistem itu <b>square</b>:")
           + EQ("e_sq", r"\left[\,\{Q_{k-p}\}\ \cdots\ \{Q_k\}\,\right]\begin{Bmatrix}\Psi_{k-p}\\ \vdots\\ \Psi_k\end{Bmatrix}=\{H(\xi)\}\quad\Longrightarrow\quad \Psi_I(\xi)=N_{I,p}(\xi)", "5.4")
           + P("Its unique solution is the B-splines, by (5.2). Any positive kernel W<sub>I</sub> leads to the same solution: (5.3) is just one way of "
               "solving (5.4). The kernel shape and the support radius inside the support no longer matter.",
               "Penyelesaian unik-nya ialah B-spline, berdasarkan (5.2). Sebarang kernel W<sub>I</sub> yang positif membawa kepada penyelesaian yang sama: (5.3) "
               "hanyalah satu cara menyelesaikan (5.4). Bentuk kernel dan jejari support tidak lagi penting."))
    + STEP("Worked step · the blossom vectors of Example 1", "Langkah berkerja · blossom vector bagi Contoh 1",
           P("For Ξ = {0, 0, 0, 0.5, 1, 1, 1}: " + ", ".join(f"{{Q<sub>{i + 1}</sub>}} = {{{', '.join(f6(v) for v in q)}}}" for i, q in enumerate(Q1))
             + ". At ξ = 0.75, Q<sub>2</sub>, Q<sub>3</sub>, Q<sub>4</sub> are active and the 3 × 3 system returns 0.125, 0.625, 0.25 — the B-splines of Example 1, "
               "for a constant, a cubic or a cosine kernel alike (Example 3).",
             "Untuk Ξ = {0, 0, 0, 0.5, 1, 1, 1}: " + ", ".join(f"{{Q<sub>{i + 1}</sub>}} = {{{', '.join(f6(v) for v in q)}}}" for i, q in enumerate(Q1))
             + ". Pada ξ = 0.75, Q<sub>2</sub>, Q<sub>3</sub>, Q<sub>4</sub> aktif dan sistem 3 × 3 memulangkan 0.125, 0.625, 0.25 — B-spline dalam Contoh 1, "
               "sama ada kernel malar, cubic atau cosine (Contoh 3)."))
    + DEF("What it buys, and what it does not", "Apa yang diperoleh, dan apa yang tidak",
          "Seen as RK functions, B-splines can be refined the meshfree way: insert nodes where needed and let the RK construction "
          "build the functions, while the square-system regions stay exact B-splines. The study of the 2017 paper found the catch: where "
          "nodes are inserted the system is no longer square, and linear exactness then depends on integration cells aligned with the knots — "
          "the theme of Part 3.",
          "Dilihat sebagai RK function, B-spline boleh di-refine secara meshfree: masukkan node di tempat yang perlu dan biarkan pembinaan RK "
          "membina function, sementara kawasan square-system kekal sebagai B-spline yang tepat. Kajian terhadap artikel 2017 itu menemui "
          "kekangannya: di kawasan node dimasukkan, sistem tidak lagi square, dan linear exactness kemudiannya bergantung pada integration cell "
          "yang sejajar dengan knot — tema Bahagian 3.", "note")
    + KP([("Blossom vectors (5.1) make the B-splines satisfy RK-type reproducing conditions (5.2).", "Blossom vector (5.1) menjadikan B-spline memenuhi reproducing condition jenis RK (5.2)."),
          ("With B-spline supports the system is square on each span: Ψ<sub>I</sub> = N<sub>I,p</sub> for any positive kernel.", "Dengan support B-spline sistem itu square pada setiap span: Ψ<sub>I</sub> = N<sub>I,p</sub> untuk sebarang kernel positif."),
          ("Inserted nodes break the square system; integration then decides exactness.", "Node yang dimasukkan memecahkan square system; integration kemudian menentukan ketepatan.")])
    + QC("q5", ("On one knot span of a degree-p space, how many blossom-RK functions are non-zero, and what does that make the reproducing system?",
                "Pada satu knot span dalam ruang darjah p, berapa banyak blossom-RK function yang bukan sifar, dan apakah kesannya pada sistem reproducing?"),
         [("a", "p + 1; a square system with a unique solution", "p + 1; square system dengan penyelesaian unik"),
          ("b", "p; an underdetermined system", "p; sistem yang underdetermined"),
          ("c", "all n; an overdetermined system solved by least squares", "kesemua n; sistem overdetermined yang diselesaikan dengan least squares")], "a",
         ("p + 1 functions, p + 1 conditions: square, so the solution is the B-splines whatever the kernel.",
          "p + 1 function, p + 1 condition: square, jadi penyelesaiannya ialah B-spline apa pun kernel-nya."))})

NOTES.append({"id": "n6", "min": 6, "title": ("Reading the literature like a reproducer", "Membaca literatur untuk menghasilkan semula keputusannya"), "html":
    P("Every paper of this area was studied by re-deriving it and repeating its figures. The same lessons came back in almost every one, and "
      "they are worth learning before your first literature review.",
      "Setiap artikel dalam bidang ini dikaji dengan menerbitkannya semula dan mengulang rajahnya. Pengajaran yang sama berulang dalam hampir "
      "setiap satu, dan ia berbaloi dipelajari sebelum ulasan literatur pertama anda.")
    + "<ol>" + "".join(f"<li>{B(a, b)}</li>" for a, b in [
        ("<b>Hidden parameters.</b> The support convention (radius in what spacing?), the error norm and its quadrature, the reading of a boundary "
         "condition, the integration cells. A plot can depend on each of them by a factor of 2 to 60.",
         "<b>Hidden parameter.</b> Konvensyen support (jejari dalam jarak yang mana?), error norm dan quadrature-nya, tafsiran sesuatu boundary "
         "condition, integration cell. Satu plot boleh bergantung pada setiap satu dengan faktor 2 hingga 60."),
        ("<b>The known-method limit.</b> Check whether, for the paper's own settings, the method reduces to FEM, IGA or plain RK. One studied method "
         "was exactly Q1 FEM at its settings; another gained only 2–10 % over plain RK.",
         "<b>Known-method limit.</b> Semak sama ada, dengan tetapan artikel itu sendiri, kaedah tersebut menjadi FEM, IGA atau RK biasa. Satu kaedah "
         "yang dikaji sebenarnya Q1 FEM pada tetapannya; satu lagi hanya memberi kelebihan 2–10 % berbanding RK biasa."),
        ("<b>The patch test first.</b> A method that cannot reproduce a linear field exactly with its own quadrature has an integration problem, "
         "whatever its convergence plot shows.",
         "<b>Patch test dahulu.</b> Kaedah yang tidak dapat reproduce linear field dengan tepat menggunakan quadrature-nya sendiri mempunyai masalah "
         "integration, apa pun yang ditunjukkan oleh convergence plot-nya."),
        ("<b>Bounded agreement.</b> Write MATCH or NEAR with the tolerance (e.g. within 2 % or 5 %), name every choice the paper did not state, and "
         "run the literal reading next to the one that matches.",
         "<b>Persetujuan bersempadan.</b> Tulis MATCH atau NEAR berserta toleransi (contohnya dalam 2 % atau 5 %), namakan setiap pilihan yang tidak "
         "dinyatakan oleh artikel, dan jalankan tafsiran literal di sebelah tafsiran yang sepadan."),
        ("<b>What a result does not show.</b> One mesh, one parameter set, one norm: say so.",
         "<b>Apa yang tidak ditunjukkan oleh sesuatu keputusan.</b> Satu mesh, satu set parameter, satu norm: nyatakannya.")]) + "</ol>"
    + DEF("A research habit", "Satu tabiat penyelidikan",
          "Before trusting a new method, implement the smallest case of it next to the method it claims to beat, with the same nodes, the same "
          "quadrature and the same boundary treatment. Most surprises in this area were found that way, in an afternoon.",
          "Sebelum mempercayai sesuatu kaedah baharu, laksanakan kes paling kecilnya di sebelah kaedah yang didakwa dikalahkannya, dengan node yang sama, "
          "quadrature yang sama dan rawatan sempadan yang sama. Kebanyakan kejutan dalam bidang ini ditemui dengan cara itu, dalam satu petang.", "ok")
    + KP([("List the unstated parameters before comparing numbers.", "Senaraikan parameter yang tidak dinyatakan sebelum membandingkan nombor."),
          ("Check the known-method limit and the patch test first.", "Semak known-method limit dan patch test dahulu."),
          ("Report agreement with a tolerance, and what the result does not show.", "Laporkan persetujuan dengan toleransi, dan apa yang tidak ditunjukkan oleh keputusan itu.")])
    + QC("q6", ("A paper reports “good agreement” but does not state the support size or the quadrature of its error norm. What should you do first when reproducing it?",
                "Satu artikel melaporkan “persetujuan yang baik” tetapi tidak menyatakan saiz support atau quadrature bagi error norm-nya. Apa yang patut anda buat dahulu apabila reproduce-nya?"),
         [("a", "Use the usual default values and report a match", "Guna nilai lalai yang biasa dan laporkan padanan"),
          ("b", "List the unstated parameters and run the literal reading and the plausible variants side by side", "Senaraikan parameter yang tidak dinyatakan dan jalankan tafsiran literal serta variasi yang munasabah secara bersebelahan"),
          ("c", "Tune the parameters until the plot matches, then report the match", "Laraskan parameter sehingga plot sepadan, kemudian laporkan padanan itu")], "b",
         ("Name every hidden choice and show what each reading gives; a fitted match is reported as a fit.", "Namakan setiap pilihan tersembunyi dan tunjukkan hasil setiap tafsiran; padanan yang dilaraskan dilaporkan sebagai fit."))})

# ------------------------------------------------------------------ Examples (answer-scheme form; numbers from nmf_bspline_rk.py)
def row(vals):
    return ", ".join(f6(v) for v in vals)


EXAMPLES = [
    {"id": "x1", "title": ("Quadratic B-splines at a point by Cox–de Boor", "Quadratic B-spline pada satu titik dengan Cox–de Boor"),
     "meta": ("evaluate N<sub>I,p</sub>(ξ) and check two properties", "nilai N<sub>I,p</sub>(ξ) dan semak dua sifat"),
     "q": ("Ξ = {0, 0, 0, 0.5, 1, 1, 1}, p = 2. Evaluate every basis function at ξ = 0.75 and check the partition of unity and the linear reproduction (2.5).",
           "Ξ = {0, 0, 0, 0.5, 1, 1, 1}, p = 2. Nilai setiap basis function pada ξ = 0.75 dan semak partition of unity serta linear reproduction (2.5)."),
     "plan": ("Find the span → degree 0 → degree 1 → degree 2 → checks.", "Cari span → darjah 0 → darjah 1 → darjah 2 → semakan."),
     "steps": [
         (("The knot span", "Knot span"),
          P(f"t<sub>4</sub> = 0.5 ≤ 0.75 < t<sub>5</sub> = 1, so ξ lies in span 4 and only N<sub>4,0</sub> = 1 at degree 0: {{{row(TAB[0])}}}.",
            f"t<sub>4</sub> = 0.5 ≤ 0.75 < t<sub>5</sub> = 1, jadi ξ terletak dalam span 4 dan hanya N<sub>4,0</sub> = 1 pada darjah 0: {{{row(TAB[0])}}}.")),
         (("Degree 1", "Darjah 1"),
          P("N<sub>3,1</sub> = (t<sub>5</sub> − ξ)/(t<sub>5</sub> − t<sub>4</sub>) N<sub>4,0</sub> = 0.25/0.5 = 0.5 and N<sub>4,1</sub> = (ξ − t<sub>4</sub>)/(t<sub>5</sub> − t<sub>4</sub>) N<sub>4,0</sub> = 0.5. "
            f"All degree-1 values: {{{row(TAB[1])}}}.",
            "N<sub>3,1</sub> = (t<sub>5</sub> − ξ)/(t<sub>5</sub> − t<sub>4</sub>) N<sub>4,0</sub> = 0.25/0.5 = 0.5 dan N<sub>4,1</sub> = (ξ − t<sub>4</sub>)/(t<sub>5</sub> − t<sub>4</sub>) N<sub>4,0</sub> = 0.5. "
            f"Semua nilai darjah 1: {{{row(TAB[1])}}}.")),
         (("Degree 2", "Darjah 2"),
          P("N<sub>2,2</sub> = (t<sub>5</sub> − ξ)/(t<sub>5</sub> − t<sub>3</sub>) N<sub>3,1</sub> = 0.25 × 0.5 = 0.125; "
            "N<sub>3,2</sub> = (ξ − t<sub>3</sub>)/(t<sub>5</sub> − t<sub>3</sub>) N<sub>3,1</sub> + (t<sub>6</sub> − ξ)/(t<sub>6</sub> − t<sub>4</sub>) N<sub>4,1</sub> = 0.75 × 0.5 + 0.5 × 0.5 = 0.625; "
            "N<sub>4,2</sub> = (ξ − t<sub>4</sub>)/(t<sub>6</sub> − t<sub>4</sub>) N<sub>4,1</sub> = 0.5 × 0.5 = 0.25 (the second term has t<sub>7</sub> − t<sub>5</sub> = 0, taken as 0). "
            f"Result: N = {{{row(TAB[2])}}}.",
            "N<sub>2,2</sub> = (t<sub>5</sub> − ξ)/(t<sub>5</sub> − t<sub>3</sub>) N<sub>3,1</sub> = 0.25 × 0.5 = 0.125; "
            "N<sub>3,2</sub> = (ξ − t<sub>3</sub>)/(t<sub>5</sub> − t<sub>3</sub>) N<sub>3,1</sub> + (t<sub>6</sub> − ξ)/(t<sub>6</sub> − t<sub>4</sub>) N<sub>4,1</sub> = 0.75 × 0.5 + 0.5 × 0.5 = 0.625; "
            "N<sub>4,2</sub> = (ξ − t<sub>4</sub>)/(t<sub>6</sub> − t<sub>4</sub>) N<sub>4,1</sub> = 0.5 × 0.5 = 0.25 (sebutan kedua ada t<sub>7</sub> − t<sub>5</sub> = 0, diambil sebagai 0). "
            f"Keputusan: N = {{{row(TAB[2])}}}.")),
         (("Checks", "Semakan"),
          P(f"Sum = {f6(float(N1.sum()))}. Greville points {{{row(GRV)}}}: Σ N<sub>I</sub> ξ̄<sub>I</sub> = 0.125 × 0.25 + 0.625 × 0.75 + 0.25 × 1 = {f6(float(N1 @ GRV))} = ξ. ✓",
            f"Hasil tambah = {f6(float(N1.sum()))}. Greville point {{{row(GRV)}}}: Σ N<sub>I</sub> ξ̄<sub>I</sub> = 0.125 × 0.25 + 0.625 × 0.75 + 0.25 × 1 = {f6(float(N1 @ GRV))} = ξ. ✓"))]},
    {"id": "x2", "title": ("Linear RK shape functions at a point", "Linear RK shape function pada satu titik"),
     "meta": ("moment matrix, coefficients, Ψ<sub>I</sub>, reproduction check", "moment matrix, pekali, Ψ<sub>I</sub>, semakan reproduction"),
     "q": ("Nodes x<sub>I</sub> = 0, 0.5, 1; cubic kernel (4.6) with a = 0.75; p = 1. Compute Ψ<sub>1</sub>, Ψ<sub>2</sub>, Ψ<sub>3</sub> at x = 0.4 and check (4.2).",
           "Node x<sub>I</sub> = 0, 0.5, 1; cubic kernel (4.6) dengan a = 0.75; p = 1. Kira Ψ<sub>1</sub>, Ψ<sub>2</sub>, Ψ<sub>3</sub> pada x = 0.4 dan semak (4.2)."),
     "plan": ("Kernel values → [M] → {b} → Ψ<sub>I</sub> → checks.", "Nilai kernel → [M] → {b} → Ψ<sub>I</sub> → semakan."),
     "steps": [
         (("Kernel values", "Nilai kernel"),
          P(f"r = 0.5333, 0.1333, 0.8: W = {{{', '.join(f4(v) for v in D2['W'])}}} (second, first and second branch of (4.6)).",
            f"r = 0.5333, 0.1333, 0.8: W = {{{', '.join(f4(v) for v in D2['W'])}}} (cabang kedua, pertama dan kedua bagi (4.6)).")),
         (("Moment matrix", "Moment matrix"),
          P(f"M<sub>11</sub> = Σ W<sub>J</sub> = {f4(D2['M'][0, 0])}, M<sub>12</sub> = Σ x<sub>J</sub> W<sub>J</sub> = {f4(D2['M'][0, 1])}, "
            f"M<sub>22</sub> = Σ x<sub>J</sub><sup>2</sup> W<sub>J</sub> = {f4(D2['M'][1, 1])}.",
            f"M<sub>11</sub> = Σ W<sub>J</sub> = {f4(D2['M'][0, 0])}, M<sub>12</sub> = Σ x<sub>J</sub> W<sub>J</sub> = {f4(D2['M'][0, 1])}, "
            f"M<sub>22</sub> = Σ x<sub>J</sub><sup>2</sup> W<sub>J</sub> = {f4(D2['M'][1, 1])}.")),
         (("Coefficients", "Pekali"),
          P(f"[M]{{b}} = {{1, 0.4}}<sup>T</sup> gives {{b}} = {{{', '.join(f4(v) for v in D2['b'])}}}.",
            f"[M]{{b}} = {{1, 0.4}}<sup>T</sup> memberi {{b}} = {{{', '.join(f4(v) for v in D2['b'])}}}.")),
         (("Shape functions", "Shape function"),
          P(f"Ψ<sub>I</sub> = (b<sub>1</sub> + b<sub>2</sub> x<sub>I</sub>) W<sub>I</sub>: Ψ = {{{', '.join(f4(v) for v in PSI2)}}}.",
            f"Ψ<sub>I</sub> = (b<sub>1</sub> + b<sub>2</sub> x<sub>I</sub>) W<sub>I</sub>: Ψ = {{{', '.join(f4(v) for v in PSI2)}}}.")),
         (("Checks", "Semakan"),
          P(f"Σ Ψ<sub>I</sub> = {f6(float(PSI2.sum()))} and Σ Ψ<sub>I</sub> x<sub>I</sub> = {f6(float(PSI2 @ [0, 0.5, 1]))} = x. ✓ Note Ψ<sub>2</sub> ≠ 1 even though x is close to node 2: no Kronecker delta.",
            f"Σ Ψ<sub>I</sub> = {f6(float(PSI2.sum()))} dan Σ Ψ<sub>I</sub> x<sub>I</sub> = {f6(float(PSI2 @ [0, 0.5, 1]))} = x. ✓ Perhatikan Ψ<sub>2</sub> ≠ 1 walaupun x dekat dengan node 2: tiada Kronecker delta."))]},
    {"id": "x3", "title": ("Blossom vectors make RK equal to B-splines", "Blossom vector menjadikan RK sama dengan B-spline"),
     "meta": ("blossom vectors, the square system, kernel independence", "blossom vector, square system, kebebasan daripada kernel"),
     "q": ("Same knots as Example 1. (a) Write the blossom vectors. (b) At ξ = 0.75, solve the reproducing conditions with the active vectors. "
           "(c) Show that (5.3) gives the same values for any positive kernel.",
           "Knot yang sama seperti Contoh 1. (a) Tulis blossom vector. (b) Pada ξ = 0.75, selesaikan reproducing condition dengan vector yang aktif. "
           "(c) Tunjukkan bahawa (5.3) memberi nilai yang sama untuk sebarang kernel positif."),
     "plan": ("Blossom vectors → active set → 3 × 3 system → compare with Example 1 → kernel argument.",
              "Blossom vector → set aktif → sistem 3 × 3 → banding dengan Contoh 1 → hujah kernel."),
     "steps": [
         (("(a) Blossom vectors", "(a) Blossom vector"),
          P("For p = 2, {Q<sub>I</sub>} = {1, (t<sub>I+1</sub> + t<sub>I+2</sub>)/2, t<sub>I+1</sub> t<sub>I+2</sub>}<sup>T</sup>: " + "; ".join(f"Q<sub>{i + 1}</sub> = {{{row(q)}}}" for i, q in enumerate(Q1)) + ".",
            "Untuk p = 2, {Q<sub>I</sub>} = {1, (t<sub>I+1</sub> + t<sub>I+2</sub>)/2, t<sub>I+1</sub> t<sub>I+2</sub>}<sup>T</sup>: " + "; ".join(f"Q<sub>{i + 1}</sub> = {{{row(q)}}}" for i, q in enumerate(Q1)) + ".")),
         (("(b) The square system", "(b) Square system"),
          P("ξ is in span [0.5, 1): supports of N<sub>2</sub>, N<sub>3</sub>, N<sub>4</sub> are active. Rows: Ψ<sub>2</sub> + Ψ<sub>3</sub> + Ψ<sub>4</sub> = 1; "
            "0.25Ψ<sub>2</sub> + 0.75Ψ<sub>3</sub> + Ψ<sub>4</sub> = 0.75; 0.5Ψ<sub>3</sub> + Ψ<sub>4</sub> = 0.5625. Solution: Ψ = {0.125, 0.625, 0.25} = N. ✓",
            "ξ dalam span [0.5, 1): support bagi N<sub>2</sub>, N<sub>3</sub>, N<sub>4</sub> aktif. Baris: Ψ<sub>2</sub> + Ψ<sub>3</sub> + Ψ<sub>4</sub> = 1; "
            "0.25Ψ<sub>2</sub> + 0.75Ψ<sub>3</sub> + Ψ<sub>4</sub> = 0.75; 0.5Ψ<sub>3</sub> + Ψ<sub>4</sub> = 0.5625. Penyelesaian: Ψ = {0.125, 0.625, 0.25} = N. ✓")),
         (("(c) Any kernel", "(c) Sebarang kernel"),
          P("With W<sub>I</sub> > 0 on the active supports, (5.3) solves the same three equations, so the weights cancel: a constant, a cubic and a cosine "
            "kernel all give {0.125, 0.625, 0.25} (run <code>code/nmf_bspline_rk.py</code>). The Explorer, task 2, shows it for every ξ.",
            "Dengan W<sub>I</sub> > 0 pada support yang aktif, (5.3) menyelesaikan tiga persamaan yang sama, jadi weight terbatal: kernel malar, cubic dan cosine "
            "semuanya memberi {0.125, 0.625, 0.25} (jalankan <code>code/nmf_bspline_rk.py</code>). Explorer, tugasan 2, menunjukkannya untuk setiap ξ."))]},
]

# ------------------------------------------------------------------ Exercises (generators run in the browser; answers never leave the page)
EXERCISES = [
    {"id": "e1", "title": ("Quadratic B-splines at a point", "Quadratic B-spline pada satu titik"), "marks": 4,
     "stmt": B("Open knot vector Ξ = {0, 0, 0, a, 1, 1, 1}, p = 2. Evaluate N<sub>1</sub> … N<sub>4</sub> at the given ξ (four decimals).",
               "Knot vector open Ξ = {0, 0, 0, a, 1, 1, 1}, p = 2. Nilai N<sub>1</sub> … N<sub>4</sub> pada ξ yang diberi (empat titik perpuluhan).")},
    {"id": "e2", "title": ("Greville points", "Greville point"), "marks": 3,
     "stmt": B("Compute the interior Greville points ξ̄<sub>2</sub> … ξ̄<sub>n−1</sub> of the given open knot vector.",
               "Kira Greville point dalaman ξ̄<sub>2</sub> … ξ̄<sub>n−1</sub> bagi knot vector open yang diberi.")},
    {"id": "e3", "title": ("Linear RK shape functions from given kernel values", "Linear RK shape function daripada nilai kernel yang diberi"), "marks": 5,
     "stmt": B("Nodes x<sub>I</sub> = 0, 1, 2; p = 1; the kernel values at the point x are given. Compute Ψ<sub>1</sub>, Ψ<sub>2</sub>, Ψ<sub>3</sub>.",
               "Node x<sub>I</sub> = 0, 1, 2; p = 1; nilai kernel pada titik x diberi. Kira Ψ<sub>1</sub>, Ψ<sub>2</sub>, Ψ<sub>3</sub>.")},
    {"id": "e4", "title": ("A point of a NURBS arc", "Satu titik pada NURBS arc"), "marks": 4,
     "stmt": B("Quadratic arc, Ξ = {0, 0, 0, 1, 1, 1}, control points (1, 0), (1, 1), (0, 1), weights 1, λ<sub>2</sub>, 1. Compute x and y at the given ξ, and the distance from the origin.",
               "Arc quadratic, Ξ = {0, 0, 0, 1, 1, 1}, control point (1, 0), (1, 1), (0, 1), weight 1, λ<sub>2</sub>, 1. Kira x dan y pada ξ yang diberi, dan jarak dari asalan.")},
    {"id": "e5", "title": ("A cubic blossom vector", "Blossom vector cubic"), "marks": 3,
     "stmt": B("For p = 3 and the three interior knots of one support given below, compute q<sub>1</sub>, q<sub>2</sub>, q<sub>3</sub> of (5.1).",
               "Untuk p = 3 dan tiga knot dalaman bagi satu support yang diberi di bawah, kira q<sub>1</sub>, q<sub>2</sub>, q<sub>3</sub> dalam (5.1).")},
]

# JavaScript: EX.specs[id] = {gen(rng) -> P, given(P) -> html, fields: [{id, label, ans(P), tol}], hints: [P -> html], solution(P) -> html}
EXERCISE_JS = r"""
var NM = {
  table: function (t, p, x) { var m = t.length, tab = [], row = [], i, k;
    for (i = 1; i < m; i++) row.push((t[i-1] <= x && x < t[i]) || (x === t[m-1] && t[i] === t[m-1] && t[i-1] < t[i]) ? 1 : 0); tab.push(row);
    for (k = 1; k <= p; k++) { var pr = tab[k-1], r = []; for (i = 1; i < m - k; i++) { var a = 0, b = 0, d1 = t[i+k-1] - t[i-1], d2 = t[i+k] - t[i];
      if (d1 > 0) a = (x - t[i-1]) / d1 * pr[i-1]; if (d2 > 0) b = (t[i+k] - x) / d2 * pr[i]; r.push(a + b); } tab.push(r); } return tab; },
  basis: function (t, p, x) { return NM.table(t, p, x)[p]; },
  f: function (v, d) { return (Math.abs(v) < 5e-13 ? 0 : v).toFixed(d === undefined ? 4 : d); }
};
var B2 = function (en, ms) { return '<span class="en">' + en + '</span><span class="ms">' + ms + '</span>'; };
EX.specs.e1 = {
  gen: function (r) { var a = 0.3 + 0.05 * Math.floor(r() * 9), x; do { x = Math.round((0.05 + 0.9 * r()) * 100) / 100; } while (Math.abs(x - a) < 0.04); return { a: a, x: x, t: [0, 0, 0, a, 1, 1, 1] }; },
  given: function (P) { return "a = " + P.a.toFixed(2) + ", ξ = " + P.x.toFixed(2); },
  fields: [0, 1, 2, 3].map(function (i) { return { id: "N" + (i + 1), label: "N<sub>" + (i + 1) + "</sub>", ans: function (P) { return NM.basis(P.t, 2, P.x)[i]; }, tol: 2e-3 }; }),
  hints: [
    function (P) { return B2("Find the span first: ξ = " + P.x.toFixed(2) + (P.x < P.a ? " lies in [0, a), so N<sub>4</sub> = 0." : " lies in [a, 1), so N<sub>1</sub> = 0."), "Cari span dahulu: ξ = " + P.x.toFixed(2) + (P.x < P.a ? " terletak dalam [0, a), jadi N<sub>4</sub> = 0." : " terletak dalam [a, 1), jadi N<sub>1</sub> = 0.")); },
    function (P) { var T = NM.table(P.t, 2, P.x)[1]; return B2("Degree-1 values: " + T.map(function (v) { return NM.f(v); }).join(", ") + ".", "Nilai darjah 1: " + T.map(function (v) { return NM.f(v); }).join(", ") + "."); },
    function (P) { return B2("Apply (2.2) once more; every fraction with a zero denominator is 0, and the four values must sum to 1.", "Guna (2.2) sekali lagi; setiap pecahan dengan penyebut sifar ialah 0, dan empat nilai itu mesti berjumlah 1."); }],
  solution: function (P) { var T = NM.table(P.t, 2, P.x); return B2("Degree 0: ", "Darjah 0: ") + T[0].join(", ") + "<br>" + B2("Degree 1: ", "Darjah 1: ") + T[1].map(function (v) { return NM.f(v); }).join(", ") + "<br>" + B2("Degree 2: ", "Darjah 2: ") + T[2].map(function (v) { return NM.f(v); }).join(", ") + B2(" (sum 1).", " (jumlah 1)."); }
};
EX.specs.e2 = {
  gen: function (r) { var p = 2 + Math.floor(r() * 2), k1 = Math.round((0.15 + 0.3 * r()) * 20) / 20, k2 = Math.round((0.55 + 0.3 * r()) * 20) / 20, t = [], i;
    for (i = 0; i <= p; i++) t.push(0); t.push(k1, k2); for (i = 0; i <= p; i++) t.push(1); return { p: p, t: t }; },
  given: function (P) { return "p = " + P.p + ", Ξ = {" + P.t.join(", ") + "}"; },
  fields: [0, 1, 2, 3].map(function (j) { return { id: "g" + (j + 2), label: "ξ̄<sub>" + (j + 2) + "</sub>", show: function (P) { return j < P.t.length - P.p - 3; },
    ans: function (P) { var i = j + 2, s = 0; for (var k = 0; k < P.p; k++) s += P.t[i + k]; return s / P.p; }, tol: 1e-3 }; }),
  hints: [
    function (P) { var n = P.t.length - P.p - 1; return B2("n = " + P.t.length + " − " + P.p + " − 1 = " + n + " functions; the interior ones are I = 2 … " + (n - 1) + ".", "n = " + P.t.length + " − " + P.p + " − 1 = " + n + " function; yang dalaman ialah I = 2 … " + (n - 1) + "."); },
    function (P) { return B2("ξ̄<sub>I</sub> is the average of the p knots t<sub>I+1</sub> … t<sub>I+p</sub>, Eq. (2.5).", "ξ̄<sub>I</sub> ialah purata p knot t<sub>I+1</sub> … t<sub>I+p</sub>, Pers. (2.5)."); }],
  solution: function (P) { var n = P.t.length - P.p - 1, out = []; for (var i = 1; i <= n; i++) { var s = 0; for (var k = 0; k < P.p; k++) s += P.t[i + k]; out.push(NM.f(s / P.p, 4)); } return "ξ̄ = {" + out.join(", ") + "}"; }
};
EX.specs.e3 = {
  gen: function (r) { var w = [0.05 + 0.4 * r(), 0.3 + 0.5 * r(), 0.05 + 0.4 * r()].map(function (v) { return Math.round(v * 100) / 100; }), x = Math.round((0.4 + 1.2 * r()) * 20) / 20; return { w: w, x: x }; },
  given: function (P) { return "x = " + P.x.toFixed(2) + ", W = {" + P.w.map(function (v) { return v.toFixed(2); }).join(", ") + "}"; },
  _psi: function (P) { var X = [0, 1, 2], m11 = 0, m12 = 0, m22 = 0; for (var j = 0; j < 3; j++) { m11 += P.w[j]; m12 += X[j] * P.w[j]; m22 += X[j] * X[j] * P.w[j]; }
    var d = m11 * m22 - m12 * m12, b1 = (m22 - m12 * P.x) / d, b2 = (m11 * P.x - m12) / d; return { psi: X.map(function (xi, j) { return (b1 + b2 * xi) * P.w[j]; }), m: [m11, m12, m22], b: [b1, b2] }; },
  fields: [0, 1, 2].map(function (i) { return { id: "P" + (i + 1), label: "Ψ<sub>" + (i + 1) + "</sub>", ans: function (P) { return EX.specs.e3._psi(P).psi[i]; }, tol: 2e-3 }; }),
  hints: [
    function (P) { var s = EX.specs.e3._psi(P); return B2("[M] = [[" + NM.f(s.m[0]) + ", " + NM.f(s.m[1]) + "], [" + NM.f(s.m[1]) + ", " + NM.f(s.m[2]) + "]], Eq. (4.4).", "[M] = [[" + NM.f(s.m[0]) + ", " + NM.f(s.m[1]) + "], [" + NM.f(s.m[1]) + ", " + NM.f(s.m[2]) + "]], Pers. (4.4)."); },
    function (P) { var s = EX.specs.e3._psi(P); return B2("Solve [M]{b} = {1, x}: b = {" + NM.f(s.b[0]) + ", " + NM.f(s.b[1]) + "}.", "Selesaikan [M]{b} = {1, x}: b = {" + NM.f(s.b[0]) + ", " + NM.f(s.b[1]) + "}."); },
    function (P) { return B2("Ψ<sub>I</sub> = (b<sub>1</sub> + b<sub>2</sub> x<sub>I</sub>) W<sub>I</sub>; check Σ Ψ = 1 and Σ Ψ x<sub>I</sub> = x.", "Ψ<sub>I</sub> = (b<sub>1</sub> + b<sub>2</sub> x<sub>I</sub>) W<sub>I</sub>; semak Σ Ψ = 1 dan Σ Ψ x<sub>I</sub> = x."); }],
  solution: function (P) { var s = EX.specs.e3._psi(P); return "M = [[" + s.m.map(function (v) { return NM.f(v); })[0] + ", " + NM.f(s.m[1]) + "], [" + NM.f(s.m[1]) + ", " + NM.f(s.m[2]) + "]]; b = {" + NM.f(s.b[0]) + ", " + NM.f(s.b[1]) + "}; Ψ = {" + s.psi.map(function (v) { return NM.f(v); }).join(", ") + "}"; }
};
EX.specs.e4 = {
  gen: function (r) { var circ = r() < 0.6, lam = circ ? Math.SQRT1_2 : Math.round((0.4 + 0.9 * r()) * 20) / 20, x = Math.round((0.1 + 0.8 * r()) * 20) / 20; return { lam: lam, x: x, circ: circ }; },
  given: function (P) { return "λ<sub>2</sub> = " + (P.circ ? "1/√2" : P.lam.toFixed(2)) + ", ξ = " + P.x.toFixed(2); },
  _pt: function (P) { var N = [(1 - P.x) * (1 - P.x), 2 * P.x * (1 - P.x), P.x * P.x], w = [N[0], P.lam * N[1], N[2]], s = w[0] + w[1] + w[2];
    var R = w.map(function (v) { return v / s; }); return { x: R[0] + R[1], y: R[1] + R[2], R: R, N: N }; },
  fields: [{ id: "x", label: "x", ans: function (P) { return EX.specs.e4._pt(P).x; }, tol: 2e-3 }, { id: "y", label: "y", ans: function (P) { return EX.specs.e4._pt(P).y; }, tol: 2e-3 },
           { id: "r", label: "√(x² + y²)", ans: function (P) { var q = EX.specs.e4._pt(P); return Math.sqrt(q.x * q.x + q.y * q.y); }, tol: 2e-3 }],
  hints: [
    function (P) { var q = EX.specs.e4._pt(P); return B2("Bernstein form on one span: N = {(1−ξ)², 2ξ(1−ξ), ξ²} = {" + q.N.map(function (v) { return NM.f(v); }).join(", ") + "}.", "Bentuk Bernstein pada satu span: N = {(1−ξ)², 2ξ(1−ξ), ξ²} = {" + q.N.map(function (v) { return NM.f(v); }).join(", ") + "}."); },
    function (P) { var q = EX.specs.e4._pt(P); return B2("R<sub>I</sub> = λ<sub>I</sub>N<sub>I</sub> / Σ λ<sub>J</sub>N<sub>J</sub> = {" + q.R.map(function (v) { return NM.f(v); }).join(", ") + "}.", "R<sub>I</sub> = λ<sub>I</sub>N<sub>I</sub> / Σ λ<sub>J</sub>N<sub>J</sub> = {" + q.R.map(function (v) { return NM.f(v); }).join(", ") + "}."); },
    function (P) { return B2("x = R<sub>1</sub> + R<sub>2</sub>, y = R<sub>2</sub> + R<sub>3</sub>. The distance is 1 only when λ<sub>2</sub> = 1/√2.", "x = R<sub>1</sub> + R<sub>2</sub>, y = R<sub>2</sub> + R<sub>3</sub>. Jaraknya 1 hanya apabila λ<sub>2</sub> = 1/√2."); }],
  solution: function (P) { var q = EX.specs.e4._pt(P); return "R = {" + q.R.map(function (v) { return NM.f(v); }).join(", ") + "}; x = " + NM.f(q.x) + ", y = " + NM.f(q.y) + ", r = " + NM.f(Math.sqrt(q.x * q.x + q.y * q.y)); }
};
EX.specs.e5 = {
  gen: function (r) { var k = []; while (k.length < 3) { var v = Math.round(r() * 20) / 20; k.push(v); } k.sort(function (a, b) { return a - b; }); return { k: k }; },
  given: function (P) { return "t<sub>I+1</sub>, t<sub>I+2</sub>, t<sub>I+3</sub> = " + P.k.map(function (v) { return v.toFixed(2); }).join(", "); },
  fields: [{ id: "q1", label: "q<sub>1</sub>", ans: function (P) { return (P.k[0] + P.k[1] + P.k[2]) / 3; }, tol: 1e-3 },
           { id: "q2", label: "q<sub>2</sub>", ans: function (P) { var k = P.k; return (k[0] * k[1] + k[0] * k[2] + k[1] * k[2]) / 3; }, tol: 1e-3 },
           { id: "q3", label: "q<sub>3</sub>", ans: function (P) { return P.k[0] * P.k[1] * P.k[2]; }, tol: 1e-3 }],
  hints: [
    function () { return B2("e<sub>1</sub> = sum, e<sub>2</sub> = sum of the pairwise products, e<sub>3</sub> = product of the three knots.", "e<sub>1</sub> = hasil tambah, e<sub>2</sub> = hasil tambah darab berpasangan, e<sub>3</sub> = hasil darab tiga knot."); },
    function () { return B2("Divide by C(3, l) = 3, 3, 1 for l = 1, 2, 3.", "Bahagi dengan C(3, l) = 3, 3, 1 untuk l = 1, 2, 3."); }],
  solution: function (P) { var k = P.k; return "q = {" + [(k[0] + k[1] + k[2]) / 3, (k[0] * k[1] + k[0] * k[2] + k[1] * k[2]) / 3, k[0] * k[1] * k[2]].map(function (v) { return NM.f(v); }).join(", ") + "}"; }
};
"""

QUICK = [  # quick concept questions in the Exercises tab (div.q)
    ("A knot repeated twice in a cubic B-spline space gives what continuity there?", "Knot yang berulang dua kali dalam ruang cubic B-spline memberi continuity apa di situ?",
     "C<sup>1</sup> (p − m = 3 − 2).", "C<sup>1</sup> (p − m = 3 − 2)."),
    ("Why must at least p + 1 kernels overlap every point?", "Mengapa sekurang-kurangnya p + 1 kernel mesti bertindih pada setiap titik?",
     "Otherwise [M] is singular and (4.4) has no solution.", "Jika tidak, [M] singular dan (4.4) tiada penyelesaian."),
    ("What is q<sub>I,1</sub> of a blossom vector?", "Apakah q<sub>I,1</sub> bagi blossom vector?",
     "The Greville abscissa ξ̄<sub>I</sub>.", "Greville abscissa ξ̄<sub>I</sub>."),
]

# ------------------------------------------------------------------ Slides (section.slide, 1600 × 900 stage)
def SL(t_en, t_ms, body):
    return (t_en, t_ms, body)


def UL(items):
    return "<ul>" + "".join(f"<li>{B(a, b)}</li>" for a, b in items) + "</ul>"


SLIDES = [
    SL("NURBS and meshfree methods · Part 1", "NURBS dan meshfree method · Bahagian 1",
       f'<p class="big">{B("Foundations: B-splines, NURBS and reproducing kernels", "Asas: B-spline, NURBS dan reproducing kernel")}</p>'
       f'<p>{B("Research primer · Faculty of Civil Engineering, UTM", "Primer penyelidikan · Fakulti Kejuruteraan Awam, UTM")}</p>'),
    SL("Why put NURBS and meshfree together?", "Mengapa gabungkan NURBS dan meshfree?",
       UL([("CAD geometry is NURBS; FE meshes only approximate it.", "Geometri CAD ialah NURBS; mesh FE hanya menghampirinya."),
           ("IGA: analyse with the CAD basis — exact geometry, rigid patches.", "IGA: analisis dengan CAD basis — geometri tepat, patch yang tegar."),
           ("Meshfree: shape functions from nodes — flexible refinement, harder boundaries.", "Meshfree: shape function daripada node — refinement fleksibel, sempadan lebih sukar."),
           ("This area: keep the exact geometry, borrow the meshfree flexibility.", "Bidang ini: kekalkan geometri tepat, pinjam fleksibiliti meshfree.")])),
    SL("Knot vectors and the Cox–de Boor recursion", "Knot vector dan rekursi Cox–de Boor", "%%EQ:e_cdb:2.2%%" + UL([
        ("Degree 0: one per knot span. Degree p: blend two degree-(p − 1) neighbours.", "Darjah 0: satu bagi setiap knot span. Darjah p: campur dua jiran darjah (p − 1)."),
        ("n = (number of knots) − p − 1.", "n = (bilangan knot) − p − 1.")])),
    SL("Properties you will use every day", "Sifat yang akan anda guna setiap hari", UL([
        ("Partition of unity, non-negative, local support of p + 1 spans.", "Partition of unity, tidak negatif, local support p + 1 span."),
        ("C<sup>p−m</sup> across a knot of multiplicity m.", "C<sup>p−m</sup> merentasi knot dengan multiplicity m."),
        ("Greville points ξ̄<sub>I</sub>: Σ N<sub>I</sub> ξ̄<sub>I</sub> = ξ — B-splines behave as nodal functions.", "Greville point ξ̄<sub>I</sub>: Σ N<sub>I</sub> ξ̄<sub>I</sub> = ξ — B-spline berkelakuan seperti nodal function.")])),
    SL("NURBS: weights draw the circle", "NURBS: weight melukis bulatan", "%%EQ:e_nurbs:3.1%%" + UL([
        ("Quarter circle: control points (1,0), (1,1), (0,1); weights 1, 1/√2, 1.", "Quarter circle: control point (1,0), (1,1), (0,1); weight 1, 1/√2, 1."),
        ("At ξ = 0.5: (0.7071, 0.7071), radius exactly 1. Without the weight: radius 1.0607.", "Pada ξ = 0.5: (0.7071, 0.7071), jejari tepat 1. Tanpa weight: jejari 1.0607.")])),
    SL("Reproducing kernel shape functions", "Reproducing kernel shape function", "%%EQ:e_rk:4.5%%" + UL([
        ("From the reproducing conditions Σ Ψ<sub>I</sub>{H(x<sub>I</sub>)} = {H(x)}.", "Daripada reproducing condition Σ Ψ<sub>I</sub>{H(x<sub>I</sub>)} = {H(x)}."),
        ("[M] needs p + 1 overlapping kernels. No Kronecker delta.", "[M] memerlukan p + 1 kernel yang bertindih. Tiada Kronecker delta.")])),
    SL("Example: linear RK at x = 0.4", "Contoh: linear RK pada x = 0.4", UL([
        ("Nodes 0, 0.5, 1; cubic kernel, a = 0.75.", "Node 0, 0.5, 1; cubic kernel, a = 0.75."),
        (f"W = {{{', '.join(f4(v) for v in D2['W'])}}} → Ψ = {{{', '.join(f4(v) for v in PSI2)}}}.", f"W = {{{', '.join(f4(v) for v in D2['W'])}}} → Ψ = {{{', '.join(f4(v) for v in PSI2)}}}."),
        ("Sums: 1 and 0.4. Ψ<sub>2</sub> ≠ 1 next to node 2.", "Jumlah: 1 dan 0.4. Ψ<sub>2</sub> ≠ 1 di sebelah node 2.")])),
    SL("Blossom vectors and Marsden's identity", "Blossom vector dan Marsden's identity", "%%EQ:e_bloss:5.1%%%%EQ:e_mars:5.2%%"),
    SL("RK with blossom vectors = B-splines", "RK dengan blossom vector = B-spline", "%%EQ:e_sq:5.4%%" + UL([
        ("p + 1 active supports, p + 1 conditions: a square system.", "p + 1 support aktif, p + 1 condition: square system."),
        ("The kernel cancels: any positive W gives the B-splines.", "Kernel terbatal: sebarang W positif memberi B-spline."),
        ("Inserted nodes break the square system → Part 3.", "Node yang dimasukkan memecahkan square system → Bahagian 3.")])),
    SL("Reading the literature like a reproducer", "Membaca literatur untuk menghasilkan semula keputusannya", UL([
        ("List the hidden parameters: support convention, norm and its quadrature, BC reading, cells.", "Senaraikan hidden parameter: konvensyen support, norm dan quadrature-nya, tafsiran BC, cell."),
        ("Check the known-method limit and the patch test first.", "Semak known-method limit dan patch test dahulu."),
        ("Report MATCH/NEAR with tolerances, and what the result does not show.", "Laporkan MATCH/NEAR dengan toleransi, dan apa yang tidak ditunjukkan oleh keputusan.")])),
    SL("Next: Parts 2–4", "Seterusnya: Bahagian 2–4", UL([
        ("Part 2 · Coupling IGA and meshfree regions (Wang &amp; Zhang 2014; Valizadeh et al. 2015; Shaw et al. 2008).", "Bahagian 2 · Coupling kawasan IGA dan meshfree (Wang &amp; Zhang 2014; Valizadeh et al. 2015; Shaw et al. 2008)."),
        ("Part 3 · Integration, boundaries and consistency (Chen, Hillman &amp; Rüter 2013; Chi &amp; Lin 2016).", "Bahagian 3 · Integration, sempadan dan konsistensi (Chen, Hillman &amp; Rüter 2013; Chi &amp; Lin 2016)."),
        ("Part 4 · NURBS-based meshless methods of the group (N-RPIM 2022; NDM 2025).", "Bahagian 4 · Kaedah meshless berasaskan NURBS milik kumpulan (N-RPIM 2022; NDM 2025).")])),
]

# ------------------------------------------------------------------ Explorer tasks (milestones reported by labs/rk-bspline.html)
LAB = {"src": "../labs/rk-bspline.html", "title": "B-spline and RK Explorer", "tasks": [
    ("m1", ("Set the degree to 3 and count the functions that are non-zero on one knot span.", "Tetapkan darjah kepada 3 dan kira function yang bukan sifar pada satu knot span."),
     ("Answer for yourself: p + 1 = 4.", "Jawab sendiri: p + 1 = 4.")),
    ("m2", ("Choose “RK with blossom vectors” and switch between at least two kernel shapes. Watch the error line.", "Pilih “RK dengan blossom vector” dan tukar antara sekurang-kurangnya dua bentuk kernel. Perhatikan garis ralat."),
     ("The curves do not move and max |Ψ − N| stays at round-off: Section 5.", "Curve tidak bergerak dan max |Ψ − N| kekal pada round-off: Seksyen 5.")),
    ("m3", ("Choose “RK with node monomials” (standard RK at the Greville points) and vary the support factor.", "Pilih “RK dengan node monomial” (RK biasa pada Greville point) dan ubah faktor support."),
     ("The functions now change with the support and differ from the B-splines, though they still reproduce ξ.", "Function kini berubah mengikut support dan berbeza daripada B-spline, walaupun masih reproduce ξ.")),
    ("m4", ("Move the interior knot slider with blossom RK on.", "Gerakkan slider knot dalaman dengan blossom RK dihidupkan."),
     ("The blossom vectors follow the knots, so RK and B-splines stay equal.", "Blossom vector mengikut knot, jadi RK dan B-spline kekal sama.")),
]}

# ------------------------------------------------------------------ Glossary (term, EN, BM)
GLOSSARY = [
    ("knot vector", "Non-decreasing list of parameter values that defines a B-spline basis.", "Senarai nilai parameter yang tidak menurun yang mentakrifkan B-spline basis."),
    ("open knot vector", "A knot vector whose end values are repeated p + 1 times; the curve then interpolates its end control points.", "Knot vector yang nilai hujungnya berulang p + 1 kali; curve kemudian interpolate control point di hujungnya."),
    ("knot span", "An interval [t<sub>i</sub>, t<sub>i+1</sub>) of non-zero length; p + 1 basis functions are non-zero on it.", "Selang [t<sub>i</sub>, t<sub>i+1</sub>) yang panjangnya bukan sifar; p + 1 basis function bukan sifar padanya."),
    ("B-spline basis function", "Piecewise polynomial N<sub>I,p</sub> built by the Cox–de Boor recursion; non-negative, local, a partition of unity.", "Polinomial cebis demi cebis N<sub>I,p</sub> yang dibina dengan rekursi Cox–de Boor; tidak negatif, setempat, satu partition of unity."),
    ("Cox–de Boor recursion", "Builds N<sub>I,p</sub> from two degree-(p − 1) neighbours, Eq. (2.2).", "Membina N<sub>I,p</sub> daripada dua jiran darjah (p − 1), Pers. (2.2)."),
    ("partition of unity", "The functions sum to one at every point.", "Function berjumlah satu pada setiap titik."),
    ("local support", "Each function is non-zero only on a small interval: p + 1 knot spans for a B-spline, radius a for a kernel.", "Setiap function bukan sifar hanya pada selang yang kecil: p + 1 knot span bagi B-spline, jejari a bagi kernel."),
    ("Greville abscissa", "Average of the p interior knots of a support, ξ̄<sub>I</sub>; with them the B-splines reproduce ξ.", "Purata p knot dalaman bagi satu support, ξ̄<sub>I</sub>; dengannya B-spline reproduce ξ."),
    ("NURBS", "Non-uniform rational B-splines: weighted, normalised B-splines; exact for conic sections.", "Non-uniform rational B-spline: B-spline yang diberi weight dan dinormalkan; tepat untuk conic section."),
    ("weight", "Positive factor λ<sub>I</sub> of a NURBS basis function; changes the shape without moving the control point.", "Faktor positif λ<sub>I</sub> bagi NURBS basis function; mengubah bentuk tanpa menggerakkan control point."),
    ("control point", "Coefficient of a spline geometry; the curve lies in the convex hull of its control points.", "Pekali bagi geometri spline; curve terletak dalam convex hull control point-nya."),
    ("geometry map", "The function x(ξ, η) that takes the parameter square to the physical patch.", "Function x(ξ, η) yang membawa segi empat parameter kepada patch fizikal."),
    ("Jacobian (row convention)", "[J] with rows ∂(x, y)/∂ξ and ∂(x, y)/∂η, so that {∂f/∂x} = [J]<sup>−1</sup>{∂f/∂ξ}.", "[J] dengan baris ∂(x, y)/∂ξ dan ∂(x, y)/∂η, supaya {∂f/∂x} = [J]<sup>−1</sup>{∂f/∂ξ}."),
    ("isogeometric analysis (IGA)", "Analysis with the NURBS basis of the CAD geometry.", "Analisis dengan NURBS basis bagi geometri CAD."),
    ("meshfree method", "A method whose shape functions are built from nodes and supports, without elements.", "Kaedah yang shape function-nya dibina daripada node dan support, tanpa element."),
    ("reproducing kernel (RK)", "Shape function Ψ<sub>I</sub> = kernel × polynomial correction that reproduces polynomials up to degree p.", "Shape function Ψ<sub>I</sub> = kernel × pembetulan polinomial yang reproduce polinomial sehingga darjah p."),
    ("reproducing conditions", "Σ Ψ<sub>I</sub>(x){H(x<sub>I</sub>)} = {H(x)}: polynomials up to degree p are returned exactly.", "Σ Ψ<sub>I</sub>(x){H(x<sub>I</sub>)} = {H(x)}: polinomial sehingga darjah p dipulangkan dengan tepat."),
    ("moment matrix", "[M(x)] = Σ {H(x<sub>J</sub>)}{H(x<sub>J</sub>)}<sup>T</sup> W<sub>J</sub>(x); must be invertible.", "[M(x)] = Σ {H(x<sub>J</sub>)}{H(x<sub>J</sub>)}<sup>T</sup> W<sub>J</sub>(x); mesti invertible."),
    ("kernel (window) function", "Non-negative bell-shaped function W<sub>I</sub> centred on node I with support radius a.", "Function berbentuk loceng yang tidak negatif W<sub>I</sub> berpusat pada node I dengan jejari support a."),
    ("support radius · dilation", "a = c<sub>a</sub> h: the reach of a kernel, as a multiple c<sub>a</sub> of a node spacing h.", "a = c<sub>a</sub> h: jangkauan kernel, sebagai gandaan c<sub>a</sub> bagi jarak node h."),
    ("Shepard function", "The p = 0 RK function W<sub>I</sub>/Σ W<sub>J</sub>.", "RK function bagi p = 0, iaitu W<sub>I</sub>/Σ W<sub>J</sub>."),
    ("shifted basis", "{H(x − x<sub>I</sub>)} instead of {H(x<sub>I</sub>)}: same functions, better-conditioned [M].", "{H(x − x<sub>I</sub>)} dan bukannya {H(x<sub>I</sub>)}: function yang sama, [M] dengan conditioning yang lebih baik."),
    ("blossom vector", "{Q<sub>I</sub>} = {1, q<sub>I,1</sub>, …, q<sub>I,p</sub>}, built from the interior knots of a support, Eq. (5.1).", "{Q<sub>I</sub>} = {1, q<sub>I,1</sub>, …, q<sub>I,p</sub>}, dibina daripada knot dalaman bagi satu support, Pers. (5.1)."),
    ("Marsden's identity", "Σ N<sub>I,p</sub>(ξ){Q<sub>I</sub>} = {H(ξ)}: B-splines reproduce polynomials with blossom vectors.", "Σ N<sub>I,p</sub>(ξ){Q<sub>I</sub>} = {H(ξ)}: B-spline reproduce polinomial dengan blossom vector."),
    ("elementary symmetric polynomial", "e<sub>l</sub>: sum of all products of l distinct numbers from a list.", "e<sub>l</sub>: hasil tambah semua hasil darab l nombor berbeza daripada satu senarai."),
    ("essential boundary condition", "A prescribed value of the unknown; needs special treatment when Ψ<sub>I</sub>(x<sub>J</sub>) ≠ δ<sub>IJ</sub>.", "Nilai unknown yang ditetapkan; memerlukan rawatan khas apabila Ψ<sub>I</sub>(x<sub>J</sub>) ≠ δ<sub>IJ</sub>."),
    ("patch test", "Check that a method reproduces a linear (or higher) field exactly with its own quadrature and boundary treatment.", "Semakan bahawa sesuatu kaedah reproduce linear field (atau lebih tinggi) dengan tepat menggunakan quadrature dan rawatan sempadannya sendiri."),
    ("known-method limit", "The settings at which a new method reduces to a known one (FEM, IGA, plain RK).", "Tetapan di mana kaedah baharu menjadi kaedah yang sudah dikenali (FEM, IGA, RK biasa)."),
    ("hidden parameter", "A choice a paper does not state but its results depend on (support convention, norm quadrature, BC reading).", "Pilihan yang tidak dinyatakan oleh artikel tetapi keputusannya bergantung padanya (konvensyen support, quadrature norm, tafsiran BC)."),
]

# ------------------------------------------------------------------ Scripted guide steps (= the Start plan, in order)
GUIDE = [
    {"id": "g1", "done": "visit:start", "goto": "start/plan", "pose": "welcome",
     "en": "Start with the plan: it lists everything in this part and ticks itself as you go.", "ms": "Mulakan dengan pelan: ia menyenaraikan semua dalam bahagian ini dan ditanda sendiri semasa awak maju.",
     "hen": "Continue always takes you to the first item not yet done.", "hms": "Butang Continue sentiasa membawa awak ke item pertama yang belum selesai."},
    {"id": "g2", "done": "read:n1", "goto": "notes/n1", "pose": "present",
     "en": "Read Notes §1: the research problem and the map of the area. Tick “Mark as read” at the end.", "ms": "Baca Nota §1: masalah penyelidikan dan peta bidang ini. Tanda “Tanda sudah dibaca” di hujung.",
     "hen": "Keep three things apart: geometry map, field approximation, integration cells.", "hms": "Pisahkan tiga perkara: geometry map, field approximation, integration cell."},
    {"id": "g3", "done": "read:n2", "goto": "notes/n2", "pose": "present",
     "en": "Read Notes §2 on B-splines, then try the quick check at its end.", "ms": "Baca Nota §2 tentang B-spline, kemudian cuba semak cepat di hujungnya.",
     "hen": "Count first: n = (number of knots) − p − 1.", "hms": "Kira dahulu: n = (bilangan knot) − p − 1."},
    {"id": "g4", "done": "recall:r1", "goto": "start/r1", "pose": "think",
     "en": "Recall question 1: say the Cox–de Boor recursion in your own words, then open the answer.", "ms": "Soalan imbas kembali 1: sebut rekursi Cox–de Boor dengan perkataan awak sendiri, kemudian buka jawapannya.",
     "hen": "Degree 0 lives on one span; each degree blends two neighbours.", "hms": "Darjah 0 hidup pada satu span; setiap darjah mencampurkan dua jiran."},
    {"id": "g5", "done": "xm:x1", "goto": "examples/x1", "pose": "explain",
     "en": "Work Example 1 with pen and paper before revealing each step.", "ms": "Selesaikan Contoh 1 dengan pen dan kertas sebelum membuka setiap langkah.",
     "hen": "Write the triangle: degree 0, then 1, then 2.", "hms": "Tulis segi tiga: darjah 0, kemudian 1, kemudian 2."},
    {"id": "g6", "done": "read:n3", "goto": "notes/n3", "pose": "present",
     "en": "Notes §3: weights and the exact circle, and the Jacobian convention.", "ms": "Nota §3: weight dan bulatan yang tepat, serta konvensyen Jacobian.",
     "hen": "Try the arc with λ₂ = 1 and see the radius grow.", "hms": "Cuba arc dengan λ₂ = 1 dan lihat jejari membesar."},
    {"id": "g7", "done": "read:n4", "goto": "notes/n4", "pose": "explain",
     "en": "Notes §4: derive the RK shape function step by step.", "ms": "Nota §4: terbitkan RK shape function langkah demi langkah.",
     "hen": "The whole derivation is one substitution: (4.3) into (4.2).", "hms": "Keseluruhan derivation ialah satu penggantian: (4.3) ke dalam (4.2)."},
    {"id": "g8", "done": "xm:x2", "goto": "examples/x2", "pose": "explain",
     "en": "Example 2 computes an RK function at a point. Check both sums at the end.", "ms": "Contoh 2 mengira RK function pada satu titik. Semak kedua-dua jumlah di hujung.",
     "hen": "[M] is 2 × 2 for p = 1.", "hms": "[M] bersaiz 2 × 2 untuk p = 1."},
    {"id": "g9", "done": "read:n5", "goto": "notes/n5", "pose": "present",
     "en": "Notes §5 is the heart of the part: RK with blossom vectors is the B-splines.", "ms": "Nota §5 ialah teras bahagian ini: RK dengan blossom vector ialah B-spline.",
     "hen": "Count unknowns and equations on one span.", "hms": "Kira unknown dan persamaan pada satu span."},
    {"id": "g10", "done": "ms:m2", "goto": "lab", "pose": "tablet",
     "en": "Explorer task 2: change the kernel and watch nothing move.", "ms": "Tugasan Explorer 2: tukar kernel dan lihat tiada apa yang bergerak.",
     "hen": "Look at the max |Ψ − N| readout.", "hms": "Lihat bacaan max |Ψ − N|."},
    {"id": "g11", "done": "read:n6", "goto": "notes/n6", "pose": "present",
     "en": "Notes §6: how to read and reproduce papers in this area.", "ms": "Nota §6: cara membaca artikel dalam bidang ini dan menghasilkan semula keputusannya.",
     "hen": "Hidden parameters first.", "hms": "Hidden parameter dahulu."},
    {"id": "g12", "done": "exercises", "goto": "exercises", "pose": "tablet",
     "en": "Exercises 1–5: new numbers each attempt. Use hints before the solution.", "ms": "Latihan 1–5: nombor baharu setiap cubaan. Guna petunjuk sebelum penyelesaian.",
     "hen": "Each exercise follows one example.", "hms": "Setiap latihan mengikut satu contoh."},
    {"id": "g13", "done": "cando", "goto": "start/cando", "pose": "thumbs-up",
     "en": "Finish with the can-do checklist: rate yourself honestly.", "ms": "Akhiri dengan senarai semak boleh-buat: nilai diri awak dengan jujur.",
     "hen": "“Not yet” is a fine answer; it tells you what to revisit.", "hms": "“Belum” ialah jawapan yang baik; ia memberitahu apa yang perlu diulang."},
]
