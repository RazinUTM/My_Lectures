"""Builder for the SEAA 4243 course pages.

A part page = shared engine (inlined) + content authored in Python (bilingual pairs) +
the slide sections of the matching deck (same source as the claude.ai deck, notes stripped)
+ the lab iframe. Everything the page needs is inlined except images, the PDF and the lab,
which sit beside it at relative paths; the folder works on GitHub Pages and as a multi-file
artifact alike.
"""
import hashlib, html, json, pathlib, re, shutil

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent          # src/tools -> SEAA4243-FEM
MJ = HERE.parent / "mj"
SHARED = SITE / "shared"
FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500;600&display=swap")


# ---- bilingual helpers -------------------------------------------------------
def B(en, ms):
    """Inline pair: both languages in the DOM, the root attribute shows one."""
    return f'<span class="en">{en}</span><span class="ms">{ms}</span>'

def P(en, ms, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c}>{B(en, ms)}</p>'

LICENCE_URL = "https://github.com/RazinUTM/My_Lectures/blob/main/SEAA4243-FEM/LICENSE.md"
COPY_EN = ("© 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia (Faculty of Civil Engineering). "
           "Free to share and adapt for non-commercial teaching and learning, with credit (CC BY-NC-SA 4.0); the code is MIT-licensed. "
           "The lecturer's avatar and some other items are excepted: see the ")
COPY_MS = ("© 2026 Ahmad Razin Zainal Abidin dan Universiti Teknologi Malaysia (Fakulti Kejuruteraan Awam). "
           "Bebas dikongsi dan diubah suai untuk pengajaran dan pembelajaran bukan komersial, dengan kredit (CC BY-NC-SA 4.0); kod di bawah lesen MIT. "
           "Avatar pensyarah dan beberapa item lain dikecualikan: lihat ")


# ---- T&L app template header (rz-tnl-app-template, rz-settings-buttons), as on the SEAA 4333 Units ----------
HOST = "https://people.utm.my/arazin/for-my-students/"
PAGES = "https://razinutm.github.io/My_Lectures/"
EMAIL = "arazin@utm.my"


def crumbs(home_href, cur):
    """Host chain For My Students › My Lectures › SEAA 4243 (› current part)."""
    sep = '<span class="sep" aria-hidden="true">›</span>'
    c = (f'<a href="{HOST}">{B("For My Students", "Untuk Pelajar Saya")}</a>{sep}<a href="{PAGES}">My Lectures</a>{sep}')
    c += (f'<a href="{home_href}">SEAA 4243</a>{sep}<span aria-current="page">{cur}</span>' if cur
          else '<span aria-current="page">SEAA 4243</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{c}</nav>'


CONTACT = (f'<p class="contact" id="hcontact"><img data-avsrc="badge" alt="" aria-hidden="true" width="26" height="26">'
           f'<span class="who">Ahmad Razin Zainal Abidin</span><a href="mailto:{EMAIL}"><svg viewBox="0 0 24 24" aria-hidden="true">'
           f'<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></svg>{EMAIL}</a></p>')
KICKER = f'<div class="kicker">SEAA 4243 · {B("Faculty of Civil Engineering, UTM", "Fakulti Kejuruteraan Awam, UTM")}</div>'
SEARCH = ('<div class="hsearch" id="hsearch" role="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>'
          '<input id="hq" type="search" autocomplete="off" spellcheck="false" data-ph-en="Search" data-ph-ms="Cari" placeholder="Search" aria-label="Search this page" aria-controls="hres" aria-expanded="false">'
          '<div class="hres" id="hres" role="listbox" hidden></div></div>')
PREFS_BTNS = ('<div class="prefs">'
              '<button type="button" id="btn-lang" class="iconbtn langbtn" title="Bahasa">BM</button>'
              '<button type="button" id="btn-theme" class="iconbtn" title="Theme"></button>'
              '<button type="button" id="btn-font" class="iconbtn fontbtn" title="Text size"><span class="aa" aria-hidden="true">A<small>A</small></span><span class="lvl" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>'
              '{info}</div>')
INFO_BTN = ('<button type="button" id="btn-info" class="iconbtn" data-tt-en="About this screen" data-tt-ms="Tentang skrin ini" aria-label="About this screen" title="About this screen" aria-controls="sguide" aria-expanded="false">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.6h.01"/></svg></button>')


def fold_h1(title_html):
    return (f'<div class="h1row"><h1>{title_html}</h1><button class="foldbtn" id="foldbtn" type="button" aria-controls="hsub" aria-expanded="true">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg><span class="vh">Hide description</span></button></div>')


SCREEN_GUIDE = f"""
<div class="sgscrim" id="sgscrim" hidden></div>
<div class="sguide" id="sguide" role="dialog" aria-modal="true" aria-labelledby="sgtitle" hidden>
  <div class="sghead"><h2 id="sgtitle"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.6h.01"/></svg>{B("About this screen", "Tentang skrin ini")}</h2><button class="iconbtn" type="button" id="sgclose" aria-label="Close">✕</button></div>
  <p class="sglead">{B("Click an area to see where it is on the page, or take the tour (← → to move, Esc to close).", "Klik satu kawasan untuk melihat kedudukannya pada halaman, atau ikut tour (← → untuk bergerak, Esc untuk tutup).")}</p>
  <ol class="sglist" id="sglist"></ol>
  <h3>{B("Symbols", "Simbol")}</h3>
  <ul class="sgsym">
    <li><b class="bdx">2/6</b> {B("done out of the total in that tab; it turns green when complete.", "selesai daripada jumlah dalam tab itu; bertukar hijau apabila lengkap.")}</li>
    <li><b>○ ✓ –</b> {B("in the plan on Start: to do, done, and done in class (not tracked here).", "dalam pelan di Mula: belum, selesai, dan dibuat dalam kelas (tidak dijejak di sini).")}</li>
    <li><b>✓ ✗</b> {B("your answer is right or not yet right. Exercises in Part B can be tried again with new numbers.", "jawapan anda betul atau belum betul. Latihan Bahagian B boleh dicuba semula dengan nombor baharu.")}</li>
    <li><b>← →</b> {B("previous or next slide in the Slides tab.", "slide sebelum atau seterusnya dalam tab Slides.")}</li>
    <li><b>/</b> {B("jumps to the search box.", "terus ke kotak carian.")}</li>
    <li><b>Esc</b> {B("closes this guide, the tour and the Short notes drawer.", "menutup panduan ini, tour dan laci Nota ringkas.")}</li>
  </ul>
  <div class="sgfoot"><button class="btn" type="button" id="sgtour">{B("Take the tour", "Ikut tour")}</button></div>
</div>
<div class="tourring" id="tourring" hidden></div>
<div class="tourcard" id="tourcard" role="dialog" aria-live="polite" hidden>
  <div class="tch"><b id="tctitle"></b><span class="tcn" id="tcn"></span></div>
  <p id="tctext"></p>
  <div class="tcbar"><button class="btn ghost" type="button" id="tcprev">{B("Back", "Kembali")}</button><button class="btn" type="button" id="tcnext">{B("Next", "Seterusnya")}</button><button class="linkbtn" type="button" id="tcclose">{B("Close", "Tutup")}</button></div>
</div>
"""

# [selector, title EN, title MS, text EN, text MS]: the screen guide (ⓘ) and its tour
REGIONS = [
    [".crumbs", "Where you are", "Di mana anda berada", "The way back: For My Students, My Lectures, the SEAA 4243 course home, this part.", "Jalan kembali: For My Students, My Lectures, laman kursus SEAA 4243, bahagian ini."],
    ["#hcontact", "Your lecturer", "Pensyarah anda", "Questions about the course go to this email.", "Soalan tentang kursus dihantar ke e-mel ini."],
    [".htitle", "This part", "Bahagian ini", "The title and what the part covers. The arrow folds the description away.", "Tajuk dan apa yang bahagian ini liputi. Anak panah melipat penerangan."],
    ["#hsearch", "Search", "Carian", "Finds sections, slides, examples, exercises, Explorer tasks and glossary terms on this page. Press / to jump here.", "Mencari seksyen, slide, contoh, latihan, tugasan Explorer dan istilah glosari dalam halaman ini. Tekan / untuk terus ke sini."],
    [".partsw", "Parts of this topic", "Bahagian topik ini", "Moves to the other parts of the same topic. Each part keeps its own progress.", "Bertukar ke bahagian lain dalam topik yang sama. Setiap bahagian menyimpan kemajuannya sendiri."],
    ["#snbtn", "Short notes", "Nota ringkas", "The formulas and steps of the part on one sheet, for revision.", "Formula dan langkah bahagian ini pada satu helaian, untuk ulang kaji."],
    [".prefs", "Settings", "Tetapan", "Language (BM/EN), light or dark theme, text size (AA: four sizes in turn), and this guide. The choice is kept for every part of the course.", "Bahasa (BM/EN), tema cerah atau gelap, saiz teks (AA: empat saiz bergilir), dan panduan ini. Pilihan disimpan untuk setiap bahagian kursus."],
    [".navrow", "Tabs", "Tab", "Start, Notes, Slides, Examples, Exercises, Explorer, Glossary and Feedback. A badge shows done out of total.", "Mula, Nota, Slides, Contoh, Latihan, Explorer, Glosari dan Maklum balas. Lencana menunjukkan selesai daripada jumlah."],
    [".prog", "Progress", "Kemajuan", "The mean over the tabs that count. It is your own record, kept in this browser, not a gradebook.", "Purata tab yang dikira. Ia rekod anda sendiri, disimpan dalam pelayar ini, bukan buku gred."],
    ["main", "Contents", "Kandungan", "The tab you chose. On Start, the plan shows what to do before, in and after class.", "Tab yang anda pilih. Di Mula, pelan menunjukkan apa perlu dibuat sebelum, semasa dan selepas kelas."],
    ["#rzguide", "Dr RJ, your guide", "Dr RJ, panduan anda", "Ask a question in your own words; Dr RJ points to the matching sections of this page. When the AI tutor is on, a notice in his panel says what is sent.", "Tanya soalan dengan perkataan anda sendiri; Dr RJ menunjukkan bahagian yang berkaitan dalam halaman ini. Apabila tutor AI dihidupkan, notis dalam panelnya menyatakan apa yang dihantar."],
    ["footer.foot", "Credits and licence", "Kredit dan lesen", "Who made the page, what you may reuse, and what stays in your browser.", "Siapa yang menghasilkan halaman ini, apa yang boleh digunakan semula, dan apa yang kekal dalam pelayar anda."],
]

# preferences applied before first paint, so the page never flashes in the wrong language, theme or size
# (the old A−/A+ value "ts" is read as the text size)
PREPAINT = ('<script>(function(){try{var r=document.documentElement,p=JSON.parse(localStorage.getItem("seaa4243-prefs")||"null")||{};'
            'if(p.lang==="ms"){r.setAttribute("data-lang","ms");r.lang="ms"}if(p.theme==="light"||p.theme==="dark")r.setAttribute("data-theme",p.theme);'
            'var f=+p.font||+p.ts||1;r.style.setProperty("--font-scale",String(f));r.style.setProperty("--ts",String(f));'
            'if(p.fold)r.classList.add("subfold")}catch(e){}})();</script>')


# the footer line on the Dr RJ guide panel (added with the panel on 23 Nov 2026)
TUTOR_LINE = '<p><span class="en">Dr RJ, the guide beside the contents, points to the matching sections of this page. When the AI tutor is switched on, his panel shows a notice first; the questions you then type to him go through the course server to an AI service (Anthropic) to be answered, and the server keeps counts only, not the questions. He can be wrong: check against the notes. Only what you type to Dr RJ and what you send from the Feedback tab leaves the browser; answers and progress are stored in this browser only.</span><span class="ms">Dr RJ, panduan di sebelah kandungan, menunjukkan bahagian yang berkaitan dalam halaman ini. Apabila tutor AI dihidupkan, panelnya memaparkan notis terlebih dahulu; soalan yang anda taip kepadanya selepas itu dihantar melalui pelayan kursus kepada perkhidmatan AI (Anthropic) untuk dijawab, dan pelayan hanya menyimpan kiraan, bukan soalan. Beliau boleh tersilap: semak dengan nota. Hanya apa yang anda taip kepada Dr RJ dan apa yang anda hantar dari tab Maklum balas keluar dari pelayar; jawapan dan kemajuan disimpan dalam pelayar ini sahaja.</span></p>'


def copyright_line():
    """The general copyright and licence line at the foot of every page."""
    a = f'<a href="{LICENCE_URL}" target="_blank" rel="noopener">'
    return f'<p class="copy">{B(COPY_EN + a + "licence</a>.", COPY_MS + a + "lesen</a>.")}</p>'


def LI(pairs, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<ul{c}>' + "".join(f"<li>{B(e, m)}</li>" for e, m in pairs) + "</ul>"

def OL(pairs, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<ol{c}>' + "".join(f"<li>{B(e, m)}</li>" for e, m in pairs) + "</ol>"

def H3(en, ms):
    return f"<h3>{B(en, ms)}</h3>"

def DEF(t_en, t_ms, b_en, b_ms):
    return f'<div class="def"><b class="t">{B(t_en, t_ms)}</b>{B(b_en, b_ms)}</div>'

def NOTE(t_en, t_ms, b_en, b_ms):
    return f'<div class="note"><b class="t">{B(t_en, t_ms)}</b>{B(b_en, b_ms)}</div>'

def OK(t_en, t_ms, b_en, b_ms):
    return f'<div class="ok"><b class="t">{B(t_en, t_ms)}</b>{B(b_en, b_ms)}</div>'

def STEP(t_en, t_ms, body):
    return f'<div class="step"><h4>{B(t_en, t_ms)}</h4><div class="bd">{body}</div></div>'

def KP(pairs):
    return ('<details class="kp"><summary>' + B("Key points", "Perkara utama") + "</summary>"
            + "<ul>" + "".join(f"<li>{B(e, m)}</li>" for e, m in pairs) + "</ul></details>")

def TRY(ids):
    """Marker for a "Try it yourself" box, placed just before the section's KP(): the ids of the Explorer tasks
    (LAB_TASKS) that the section prepares, separated by spaces. The marker is empty on purpose: shared/course.js
    fills the box from the task cards of the Explorer view at load, so the task text is written once.
    Every task of a part is placed in exactly one box (build_part.py checks this)."""
    return f'<aside class="try" data-tasks="{ids}"></aside>'

def QC(qid, q_en, q_ms, options, ans, fb_en, fb_ms):
    """Ungraded one-try question inside the notes (\"Quick check\") or on the Start tab (ids r1, r2: \"Recall\")."""
    opts = "".join(f'<button class="opt" type="button" data-k="{k}">{B(e, m)}</button>' for k, e, m in options)
    if qid.startswith("r"):
        label = B(f"Recall {qid[1:]}", f"Ingat semula {qid[1:]}")
        q_en = re.sub(r"^Recall · ", "", q_en); q_ms = re.sub(r"^Ingat semula · ", "", q_ms)
        q_en, q_ms = q_en[:1].upper() + q_en[1:], q_ms[:1].upper() + q_ms[1:]
    else:
        label = B("Quick check · not graded", "Semak cepat · tidak bergred")
    return (f'<div class="qc" data-qc="{qid}" data-ans="{ans}" id="{qid}"><div class="h">{label}</div>'
            f'<p>{B(q_en, q_ms)}</p><div class="opts">{opts}</div><p class="fb" role="status" hidden>{B(fb_en, fb_ms)}</p></div>')

def SB(inner):
    """Supporting prose, hidden in key-points mode."""
    return f'<div class="sb">{inner}</div>'


# ---- worked examples (answer-scheme style) ----
def XSTEP(n, t_en, t_ms, marks, body):
    """One numbered step of a model answer with its marks."""
    mk = f'<span class="mk-badge">[{marks}]</span>' if marks else ""
    return f'<div class="xstep"><h4><span class="xn">Step {n}</span> {B(t_en, t_ms)}{mk}</h4><div class="bd">{body}</div></div>'

def ANS(inner):
    return f'<div class="ans"><b>Answer.</b> {inner}</div>'

def CHK(inner):
    return f'<p class="chk"><b>Check.</b> {inner}</p>'

def PLAN(inner):
    return f'<p class="plan"><b>Plan.</b> {inner}</p>'

def PIC(en, ms):
    return f'<p class="pic"><b>{B("Physical picture.", "Gambaran fizikal.")}</b> {B(en, ms)}</p>'

def INTERP(en, ms):
    return f'<div class="interp"><b>{B("Interpretation", "Tafsiran")}</b>{B(en, ms)}</div>'

def SCHEME(rows, total):
    """rows: [(what_en, what_ms, marks)] -> marking-scheme table."""
    body = "".join(f'<tr><td>{B(e, m)}</td><td class="r num">{mk}</td></tr>' for e, m, mk in rows)
    return (f'<details class="scheme"><summary>{B("Marking scheme (suggested)", "Skema pemarkahan (cadangan)")} · {total}</summary>'
            f'<div class="tbl"><table><tr><th>{B("What earns the marks", "Apa yang diberi markah")}</th><th class="r">{B("Marks", "Markah")}</th></tr>{body}'
            f'<tr><td><b>{B("Total", "Jumlah")}</b></td><td class="r num"><b>{total}</b></td></tr></table></div></details>')


# ---- course structure (shared by the home page and the part pages) -------------
# (n, slug, topic, part label, description pair, built)
COURSE_PARTS = [
    (1, "01-heat-transfer-1", "2D Heat Transfer", "Part 1 of 2", ("PDE, boundary conditions, the four-node element and its shape functions, gradient and flux.", "PDE, boundary condition, four-node element dan shape function-nya, gradient dan flux."), True),
    (2, "02-heat-transfer-2", "2D Heat Transfer", "Part 2 of 2", ("Galerkin, integration by parts, [k], assembly, essential conditions, the worked example in MATLAB.", "Galerkin, integration by parts, [k], assembly, essential condition, contoh bekerja dalam MATLAB."), True),
    (3, "03-plane-stress-1", "Plane Stress", "Part 1 of 3", ("Equilibrium, Hooke, strain–displacement, the PDE in matrix form, boundary conditions, [N] with two dofs per node.", "Equilibrium, Hooke, strain–displacement, PDE dalam bentuk matrix, boundary condition, [N] dengan dua dof setiap node."), True),
    (4, "04-plane-stress-2", "Plane Stress", "Part 2 of 3", ("[B], the 8 × 8 [k], consistent loads, assembly by dof map, the cantilever solved and refined.", "[B], [k] 8 × 8, consistent load, assembly mengikut dof map, cantilever diselesaikan dan di-refine."), True),
    (5, "05-plane-stress-3", "Plane Stress", "Part 3 of 3 · Project", ("Stress recovery, principal stresses, convergence and singularities, the 8-node element, reporting; project briefing.", "Stress recovery, principal stress, convergence dan singularity, 8-node element, pelaporan; taklimat projek."), True),
    (6, "06-ansys-demo", "ANSYS", "Demo", ("Hand calculation versus software: the plate and the cantilever rebuilt in Workbench, reaction checks, wrong models.", "Pengiraan tangan berbanding perisian: plat dan cantilever dibina semula dalam Workbench, semakan reaction, model yang salah."),True),
]
# (id, name, home blurb pair, where it is used pair, code pack id)
EXPLORERS = [
    ("shape", "Shape Function Explorer", ("N<sub>1</sub>…N<sub>8</sub> as colour maps; drag a point and read the weights.", "N<sub>1</sub>…N<sub>8</sub> sebagai peta warna; seret satu titik dan baca nilai N<sub>i</sub>."), ("Heat Transfer · Part 1", "Heat Transfer · Part 1"), "shape"),
    ("heat", "Heat Conduction Explorer", ("The 1 m plate solved live: edit edges and mesh, probe, energy balance, mesh study.", "Plat 1 m diselesaikan secara langsung: ubah tepi dan mesh, probe, energy balance, kajian mesh."), ("Heat Transfer · Part 2", "Heat Transfer · Part 2"), "heat"),
    ("cant", "Cantilever Explorer", ("Q4 and Q8 meshes of the cantilever: tip deflection, reactions, convergence.", "Mesh Q4 dan Q8 bagi cantilever: tip deflection, reaction, convergence."), ("Plane Stress · Parts 1–2 · ANSYS demo", "Plane Stress · Part 1–2 · Demo ANSYS"), "ps"),
    ("stress", "Stress Recovery Explorer", ("Stresses from displacements: unaveraged, averaged, principal, Mohr’s circle, the corner singularity.", "Stress daripada displacement: unaveraged, averaged, principal, Mohr’s circle, singularity di bucu."), ("Plane Stress · Part 3", "Plane Stress · Part 3"), "ps"),
]


def code_manifest():
    return json.loads((SITE / "code" / "manifest.json").read_text())


def kb(n):
    return f"{max(1, round(n / 1024))} kB"


def save_btn(href, name, label_en, label_ms, cls="btn"):
    """A download button: the engine fetches href and offers it through the viewer's downloads
    capability, or as an ordinary download where that is not available (GitHub Pages)."""
    return (f'<button class="{cls}" type="button" data-save="{href}" data-name="{name}">'
            f'<span class="dl" aria-hidden="true">⤓</span> {B(label_en, label_ms)}</button>')


def zip_btn(pack_id, rel, label_en, label_ms, cls="btn"):
    """Download a code pack: the engine fetches the .py files and the README (served as text) and
    builds the zip in the browser, then offers it like any other download."""
    p = code_manifest()[pack_id]
    return (f'<button class="{cls}" type="button" data-zip="{p["zip"][:-4]}" data-base="{rel}" '
            f'data-files="{",".join(p["files"])}" data-readme="{p["readme"]}">'
            f'<span class="dl" aria-hidden="true">⤓</span> {B(label_en, label_ms)}</button>')


# the lecturer's avatar is filled in by the engine (img[data-avsrc], shared/avatar/); Dr RJ's panel carries the poses


def vhead(t_en, t_ms, todo_en, todo_ms, counts_en=None, counts_ms=None, aside=""):
    """The same head on every tab: what the tab is for, what to do, and what counts toward progress."""
    c = (f'<p class="counts"><span class="cl">{B("Counts toward progress:", "Dikira dalam kemajuan:")}</span> {B(counts_en, counts_ms)}</p>'
         if counts_en else f'<p class="counts muted">{B("Not counted toward progress.", "Tidak dikira dalam kemajuan.")}</p>')
    return (f'<div class="vhead"><div class="vtxt"><h2>{B(t_en, t_ms)}</h2>'
            f'<p class="todo"><b>{B("What to do", "Apa perlu dibuat")}</b> {B(todo_en, todo_ms)}</p>{c}</div>{aside}</div>')


def code_card(pack_id, rel="../code/"):
    """Explorer tab: download the companion code, read what it does, show and copy it."""
    man = code_manifest(); p = man[pack_id]; allp = man["all"]
    blocks = ""
    for f in p["files"]:
        src = (SITE / "code" / f).read_text()
        cid = "code-" + f.replace(".py", "").replace("_", "-")
        blocks += (f'<details class="codeview"><summary>{B("Show the code", "Tunjuk kod")} · <span class="num">{f}</span> · {src.count(chr(10))} {B("lines", "baris")}</summary>'
                   f'<div class="codebar"><button class="btn ghost sm" type="button" data-copy="{cid}">{B("Copy", "Salin")}</button><span class="copymsg" aria-live="polite"></span></div>'
                   f'<pre class="code" id="{cid}"><code>{html.escape(src)}</code></pre></details>')
    return (f'<div class="card codecard" id="code"><h2>{B("Python code for assignments and projects", "Kod Python untuk assignment dan projek")}</h2>'
            + P("The same steps and notation as the notes, written out in plain Python. Use it to check every matrix and number of a hand calculation, and to run what is impractical by hand: mesh studies, contour plots, your own geometry and loads.",
                "Langkah dan notasi yang sama seperti nota, ditulis dalam Python biasa. Guna untuk menyemak setiap matrix dan nombor dalam pengiraan tangan, dan untuk menjalankan apa yang tidak praktikal dibuat dengan tangan: kajian mesh, contour plot, geometri dan beban anda sendiri.", "lead")
            + f'<div class="recbar">{zip_btn(pack_id, rel, "Download " + ", ".join(p["files"]) + " (.zip, " + kb(p["bytes"]) + ")", "Muat turun " + ", ".join(p["files"]) + " (.zip, " + kb(p["bytes"]) + ")")}'
            f'{zip_btn("all", rel, "All course code (.zip, " + kb(allp["bytes"]) + ")", "Semua kod kursus (.zip, " + kb(allp["bytes"]) + ")", "btn ghost")}<span class="savemsg" aria-live="polite"></span></div>'
            + '<ol class="howrun">'
            + f'<li>{B("Unzip, then install Python 3.8 or newer and run <code>pip install numpy matplotlib</code> (matplotlib only for the plots).", "Unzip, kemudian pasang Python 3.8 atau lebih baharu dan jalankan <code>pip install numpy matplotlib</code> (matplotlib hanya untuk plot).")}</li>'
            + f'<li>{B("Run <code>python " + p["files"][0] + "</code>. It reproduces the course example; README.txt lists the output you should see.", "Jalankan <code>python " + p["files"][0] + "</code>. Ia menghasilkan semula contoh kursus; README.txt menyenaraikan output yang sepatutnya keluar.")}</li>'
            + f'<li>{B("Read the docstring at the top of the file for the notation, numbering and units, and how to call it for your own problem.", "Baca docstring di bahagian atas fail untuk notasi, penomboran dan unit, dan cara memanggilnya untuk masalah anda sendiri.")}</li></ol>'
            + f'<p class="lead" style="margin:6px 0 10px">{B("A hand calculation is still a hand calculation: in a test or an assignment that asks for the steps, show them yourself.", "Pengiraan tangan tetap pengiraan tangan: dalam ujian atau assignment yang meminta langkah, tunjukkan sendiri.")}</p>'
            + blocks + '</div>')


# ---- assets ------------------------------------------------------------------
class Assets:
    """Equations and figures from one or more rendered directories (lists are searched in order)."""
    def __init__(self, eq_dirs, fig_dirs):
        self.eq_dirs = [pathlib.Path(d) for d in (eq_dirs if isinstance(eq_dirs, (list, tuple)) else [eq_dirs])]
        self.fig_dirs = [pathlib.Path(d) for d in (fig_dirs if isinstance(fig_dirs, (list, tuple)) else [fig_dirs])]
        self.rep = {}
        for d in self.eq_dirs:
            for r in json.loads((d / "_report.json").read_text()): self.rep.setdefault(r["name"], (r, d))

    def _find(self, dirs, name):
        for d in dirs:
            if (d / f"{name}.svg").exists(): return d / f"{name}.svg"
        raise FileNotFoundError(name)

    def eq(self, name, label=None, scale=0.52, maxw=None):
        r, d = self.rep[name]; s = (d / f"{name}.svg").read_text()
        w, h = r["w"] * scale, r["h"] * scale
        if maxw and w > maxw: h = h * maxw / w; w = maxw
        s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w:.0f}" height="{h:.0f}"', s, count=1)
        s = s.replace('fill="#1B2330"', 'fill="currentColor"').replace('fill="#1b2330"', 'fill="currentColor"')
        lab = f'<span class="lbl">{label}</span>' if label else ""
        # never shrink below 62 % on a narrow screen: scroll sideways instead, so the symbols stay legible
        s = s.replace("<svg ", f'<svg style="min-width:{0.62 * w:.0f}px" ', 1)
        return f'<div class="eqrow"><div class="eqwrap" style="width:{w:.0f}px">{s}</div>{lab}</div>'

    def fig(self, name, cap_en, cap_ms, width=None):
        s = self._find(self.fig_dirs, name).read_text()
        m = re.search(r'width="([\d.]+)" height="([\d.]+)"', s); w0, h0 = float(m.group(1)), float(m.group(2))
        w = width or w0; h = h0 * w / w0
        s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w:.0f}" height="{h:.0f}"', s, count=1)
        return f'<figure><div class="paper">{s}</div><figcaption>{B(cap_en, cap_ms)}</figcaption></figure>'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def slides_block(deck_dir, blob_map, img_out, img_rel="slides/img"):
    """Return (html, count): the deck's sections wrapped for the viewer, notes stripped, blobs mapped."""
    deck_dir = pathlib.Path(deck_dir); order = json.loads((deck_dir / "project/deck.json").read_text())["order"]
    img_out = pathlib.Path(img_out); img_out.mkdir(parents=True, exist_ok=True)
    out = []
    for sid in order:
        s = (deck_dir / f"project/slides/{sid}.html").read_text()
        s = re.sub(r"<aside>.*?</aside>", "", s, flags=re.S).strip()
        def rep(m):
            bid = m.group(1); src = blob_map.get(bid)
            if not src: raise KeyError(f"no local file for blob {bid} in {sid}")
            dst = img_out / pathlib.Path(src).name
            if not dst.exists() or sha(dst) != sha(src): shutil.copy(src, dst)
            return f"{img_rel}/{dst.name}"
        s = re.sub(r"/_blob/([0-9a-f]{32})", rep, s)
        # title for the thumbnail list: eyebrow + heading text
        t = ""
        m = re.search(r"<h2[^>]*>(.*?)</h2>", s, flags=re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S)
        if m: t = re.sub(r"<[^>]+>", " ", m.group(1)); t = re.sub(r"\s+", " ", t).strip()
        out.append(f'<div class="sl" data-title="{html.escape(t[:90])}">{s}</div>')
    return "\n".join(out), len(order)


# ---- page --------------------------------------------------------------------
def page(cfg, body, head_extra="", script_extra=""):
    css = (SHARED / "course.css").read_text(); js = (SHARED / "course.js").read_text()
    annot = (SHARED / "annotate.js").read_text()        # the annotation toolbar: its own script, after the engine
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(cfg['title'])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{PREPAINT}
<meta name="description" content="{html.escape(cfg.get('description', ''))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>
{css}
</style>
{head_extra}
</head>
<body>
{body}
<script>window.COURSE = {json.dumps(cfg['course'], ensure_ascii=False).replace('</', '<\\/')};</script>
<script>
{js}
</script>
{script_extra}
<script>
{annot}</script>
</body>
</html>
"""
