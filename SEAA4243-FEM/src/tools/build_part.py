"""Build one part page: python3 build_part.py content_p1"""
import importlib, json, pathlib, sys
from sitelib import *
from pyrun import run_card

mod = importlib.import_module(sys.argv[1])
PART = mod.PART
OUT = SITE / PART["slug"]; OUT.mkdir(parents=True, exist_ok=True)
A = Assets([MJ / d for d in PART["eqs"]] if isinstance(PART["eqs"], list) else MJ / PART["eqs"], [MJ / d for d in PART["figs"]] if isinstance(PART["figs"], list) else MJ / PART["figs"])

# blob -> local file map, by sha256 against the deck's uploaded assets (listed in mj/<deck>/_blobsha.json)
blobsha = json.loads((MJ / PART["deck"] / "_blobsha.json").read_text())
local = {}
figdirs = PART["figs"] if isinstance(PART["figs"], list) else [PART["figs"]]
for p in list((MJ / "web_img").glob("*.png")) + [q for d in figdirs for q in (MJ / d).glob("*.png")]:
    local[sha(p)] = str(p)
blob_map = {bid: local[h] for bid, h in blobsha.items() if h in local}
missing = [bid for bid in blobsha if bid not in blob_map]
if missing: raise SystemExit(f"no local file for blobs {missing}")
slides_html, nslides = slides_block(MJ / PART["deck"], blob_map, OUT / "slides/img")
(OUT / "slides/deck.html").write_text(slides_html)   # fetched by the viewer when the Slides tab opens

NOTES = mod.notes(A)
minutes = PART["minutes"]
EXAMPLES = mod.examples(A)
LAB = PART["lab"]
MAN = code_manifest(); CODE = MAN[PART["code"]]
marks_a, marks_b, marks_c = len(mod.QUICK), sum(c[2] for c in mod.CALC), 2
cfg = {"title": f"SEAA 4243 · {PART['title']}", "description": PART["sub"][0],
       "course": {"part": PART["n"], "key": f"seaa4243-p{PART['n']}-v1", "prefs": "seaa4243-prefs", "notes": [n[0] for n in NOTES], "slides": nslides,
                  "examples": [x[0] for x in EXAMPLES],
                  "lab": {"id": LAB["id"], "milestones": [{"id": t[0]} for t in mod.LAB_TASKS]}, "cando": len(mod.CANDO), "targetMin": PART["target_min"],
                  "prefix": "seaa4243", "lang": "en", "avatarBase": "../shared/avatar/", "regions": REGIONS,
                  "slideTitles": [html.unescape(t) for t in re.findall(r'<div class="sl" data-title="([^"]*)"', slides_html)]}}

# siblings in the same topic, and the previous / next built part
built = [p for p in COURSE_PARTS if p[5]]
topic = next(p[2] for p in COURSE_PARTS if p[0] == PART["n"])
sibs = [p for p in COURSE_PARTS if p[2] == topic]
idx = [p[0] for p in built].index(PART["n"])
prev_p = built[idx - 1] if idx > 0 else None
next_p = built[idx + 1] if idx + 1 < len(built) else None
next_soon = next((p for p in COURSE_PARTS if p[0] == PART["n"] + 1), None) if not next_p else None


def tab(view, en, ms, badge=True):
    return (f'<button class="tab" role="tab" data-view="{view}" id="t-{view}">{B(en, ms)}' + (f'<span class="bd" data-bd="{view}"></span>' if badge else "") + '</button>')


def partlabel(p):
    return p[3].split(" of ")[0].split(" ·")[0]


switch = "".join(
    (f'<a href="../{p[1]}/index.html"' + (' aria-current="page"' if p[0] == PART["n"] else "") + f'>{partlabel(p)}</a>') if p[5]
    else f'<span class="off" title="coming">{partlabel(p)}</span>' for p in sibs)

# ---- header + nav (T&L app template, as on the SEAA 4333 Units) -----------------
head = f'''
<div class="wrap">
<header class="top" id="hdr">
  <div class="hrow">
    {crumbs("../index.html", PART["topic"][0] + ", " + PART["part"].split(" ·")[0])}
    {CONTACT}
  </div>
  <div class="hmain">
    <div class="htitle">
      {KICKER}
      {fold_h1(PART["title"].replace(" — ", ' <span class="lab">— ') + "</span>" if " — " in PART["title"] else PART["title"])}
      <p class="sub" id="hsub">{B(*PART["sub"])}</p>
    </div>
    <div class="tools">
      {SEARCH}
      <div class="seg partsw" role="group" aria-label="{topic} parts">{switch}</div>
      <button class="toolbtn" id="snbtn" type="button" aria-controls="drawer" aria-expanded="false">{B("Short notes", "Nota ringkas")}</button>
      {PREFS_BTNS.format(info=INFO_BTN)}
    </div>
  </div>
</header>
<div class="navwrap" id="navwrap">
  <div class="navrow">
    <a class="homeicon" href="../index.html" title="SEAA 4243 course home" aria-label="SEAA 4243 course home"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M3 9.5 10 3.5l7 6"/><path d="M5 8.2V16.5h3.6v-4.2h2.8v4.2H15V8.2"/></svg></a>
    <nav class="tabs" role="tablist" aria-label="Sections">
      {tab("start", "Start", "Mula", False)}{tab("notes", "Notes", "Nota")}{tab("slides", "Slides", "Slides")}{tab("examples", "Examples", "Contoh")}{tab("exercises", "Exercises", "Latihan")}{tab("lab", "Explorer", "Explorer")}{tab("glossary", "Glossary", "Glosari", False)}{tab("feedback", "Feedback", "Maklum balas", False)}
    </nav>
  </div>
  <div class="prog"><span class="pct">{B("Progress", "Kemajuan")}</span><div class="bar" id="pbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Progress"><i></i></div><span class="pct" id="ppct">0 %</span></div>
</div>
{SCREEN_GUIDE}
<main>
'''

# ---- start -----------------------------------------------------------------
total_min = sum(minutes.values())


def item(key, go, en, ms):
    """A tracked plan item: a link to where it is done, with ○ / ✓ in front."""
    v, _, a = go.partition("/")
    href = f"#{v}-{a}" if a else f"#{v}"
    return f'<li data-stage-item="{key}"><a href="{href}" data-goto="{go}">{B(en, ms)}</a></li>'


def untracked(en, ms):
    return f'<li class="untracked">{B(en, ms)}</li>'


recall_items = "".join(item(f"qc:r{i+1}", f"start/r{i+1}", f"Recall question {i+1} (on this page)", f"Soalan ingat semula {i+1} (di halaman ini)") for i in range(len(mod.RECALL)))
stages = f'''
<div class="stages">
  <div class="stage" data-stage="before"><b>{B("Before class", "Sebelum kelas")}</b><em>≈ {minutes["n1"] + 4 * len(mod.RECALL)} min</em>
    <ul>{item("read:n1", "notes/n1", f"Read Notes §1 ({minutes['n1']} min)", f"Baca Nota §1 ({minutes['n1']} min)")}{recall_items}</ul><span class="st"></span></div>
  <div class="stage" data-stage="in"><b>{B("In class", "Dalam kelas")}</b><em>{B(*PART["inclass_n"])}</em>
    <ul>{"".join(untracked(e, m) for e, m in PART["inclass"])}{item("ms:" + LAB["inclass"], "lab", "QR Explorer: " + LAB["name"] + ", task " + str([t[0] for t in mod.LAB_TASKS].index(LAB["inclass"]) + 1), "Explorer QR: " + LAB["name"] + ", tugasan " + str([t[0] for t in mod.LAB_TASKS].index(LAB["inclass"]) + 1))}</ul><span class="st"></span></div>
  <div class="stage" data-stage="after"><b>{B("After class", "Selepas kelas")}</b><em>≈ {round((total_min + PART["target_min"] + 25) / 5) * 5} min</em>
    <ul>{item("notes", "notes", f"Notes §1–§{len(NOTES)} ({total_min} min)", f"Nota §1–§{len(NOTES)} ({total_min} min)")}{item("slides", "slides", f"Slides, all {nslides}", f"Slides, kesemua {nslides}")}{item("examples", "examples", f"Worked examples ({len(EXAMPLES)})", f"Contoh bekerja ({len(EXAMPLES)})")}{item("exercises", "exercises", f"Exercises A, B, C (~{PART['target_min']} min)", f"Latihan A, B, C (~{PART['target_min']} min)")}{item("lab", "lab", f"Explorer tasks 1–{len(mod.LAB_TASKS)}", f"Tugasan Explorer 1–{len(mod.LAB_TASKS)}")}{item("checklist", "start/cando", "Can-do checklist", "Senarai semak boleh-buat")}</ul><span class="st"></span></div>
</div>
<p class="legend">{B("○ to do · ✓ done · – done in class, not tracked. Click an item to go to it.", "○ belum · ✓ selesai · – dibuat dalam kelas, tidak dijejak. Klik item untuk pergi kepadanya.")}</p>'''
cando_rows = "".join(
    f'<div class="row" data-c="c{i+1}"><p>{B(e, m)}</p><div class="seg" role="group"><button type="button" data-v="0">{B("Not yet", "Belum")}</button><button type="button" data-v="1">{B("With notes", "Dengan nota")}</button><button type="button" data-v="2">{B("Without notes", "Tanpa nota")}</button></div></div>'
    for i, (e, m) in enumerate(mod.CANDO))
start = f'''
<section class="view" data-view="start" id="v-start" role="tabpanel" aria-labelledby="t-start">
  {vhead("Start", "Mula", "Follow the plan: before class, in class, after class. Each item links to where it is done and ticks itself when it is. Continue takes you to the first thing not yet done.", "Ikut pelan: sebelum kelas, dalam kelas, selepas kelas. Setiap item dipautkan ke tempat ia dibuat dan ditanda sendiri apabila selesai. Sambung membawa anda ke perkara pertama yang belum selesai.",
         "the bar averages six parts equally: Notes, Slides, Examples, Exercises, Explorer and the can-do checklist. Each tab’s badge shows its own count.", "bar ini purata enam bahagian secara sama rata: Nota, Slides, Contoh, Latihan, Explorer dan senarai semak boleh-buat. Lencana pada setiap tab menunjukkan kiraannya sendiri.")}
  <div class="start-hero">
    <div class="card">
      <h2>{B("Your plan", "Pelan anda")}</h2>
      {stages}
      <div class="contline"><button class="btn" id="contbtn" type="button" data-goto="notes/n1">{B("Continue", "Sambung")}</button><span class="when" id="contwhen"></span></div>
    </div>
    <div class="card">
      <h2>{B("What this part covers", "Apa yang bahagian ini liputi")}</h2>
      {P(*PART["covers"])}
      <h3>{B("After this part you should be able to", "Selepas bahagian ini, anda sepatutnya boleh")}</h3>
      {OL(mod.OUTCOMES, "lo")}
      <p class="lead" style="margin-top:12px">{B(f"Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020, {PART['textref']}.", f"Teks: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020, {PART['textref']}.")}</p>
    </div>
  </div>
  <div class="grid2" style="margin-top:18px">
    <div class="card" id="recall"><h2>{B(*PART["recall_title"])}</h2><p class="lead">{B("Two questions before class. Not graded; one try each.", "Dua soalan sebelum kelas. Tidak bergred; satu cubaan setiap satu.")}</p>{"".join(mod.RECALL)}</div>
    <div class="card" id="cando"><h2>{B("Can-do checklist", "Senarai semak boleh-buat")}</h2><p class="lead">{B("Rate yourself after the exercises. “Without notes” is the exam condition and counts in full; “With notes” counts half.", "Nilai diri anda selepas latihan. “Tanpa nota” ialah keadaan peperiksaan dan dikira penuh; “Dengan nota” dikira separuh.")}</p><div class="cando">{cando_rows}</div></div>
  </div>
  <div class="card" style="margin-top:18px" id="files">
    <h2>{B("Files and settings", "Fail dan tetapan")}</h2>
    <div class="recbar">{save_btn(PART["pdf"], pathlib.Path(PART["pdf"]).name, "Slides (PDF)", "Slides (PDF)", "btn ghost")}{zip_btn(PART["code"], "../code/", "Python code (.zip)", "Kod Python (.zip)", "btn ghost")}<a class="btn ghost" href="../labs/{LAB["id"]}.html" target="_blank" rel="noopener">{B("Open the Explorer in a new tab", "Buka Explorer dalam tab baharu")}</a><a class="btn ghost" href="../index.html">{B("Course home · export or import progress", "Laman kursus · export atau import kemajuan")}</a><span class="savemsg" aria-live="polite"></span></div>
    <p class="lead" style="margin:10px 0 0">{B("Progress is stored in this browser only. It is your own record, not a gradebook; graded work stays in eLearning.", "Kemajuan disimpan dalam pelayar ini sahaja. Ia rekod anda sendiri, bukan buku gred; kerja bergred kekal di eLearning.")} <button class="linkbtn" id="resetbtn" type="button">{B("Reset this part’s progress", "Set semula kemajuan bahagian ini")}</button></p>
  </div>
</section>'''

# ---- notes -------------------------------------------------------------------
toc = "".join(f'<li><a href="#notes-{sid}" data-toc="{sid}">{i+1}. {B(te, tm)}</a></li>' for i, (sid, te, tm, _) in enumerate(NOTES))
secs = ""
for i, (sid, te, tm, body) in enumerate(NOTES):
    secs += (f'<section class="nsec" id="{sid}"><h2>{i+1}. {B(te, tm)}</h2><div class="readtime">≈ {minutes[sid]} min</div>{body}'
             f'<div class="sfoot"><label class="readck"><input type="checkbox"><span class="rk-todo">{B("Mark this section as read", "Tanda seksyen ini sudah dibaca")}</span><span class="rk-done">{B("Read ✓ — untick to review again", "Sudah dibaca ✓ — nyahtanda untuk ulang")}</span></label></div></section>')
notes_v = f'''
<section class="view" data-view="notes" id="v-notes" role="tabpanel" aria-labelledby="t-notes" hidden>
  {vhead("Notes", "Nota", "Read each section, answer its Quick check (not graded, one try), then tick “Mark this section as read” at the end of the section. “Key points only” is the revision view.", "Baca setiap seksyen, jawab Semak cepat di dalamnya (tidak bergred, satu cubaan), kemudian tanda “Tanda seksyen ini sudah dibaca” di hujung seksyen. “Perkara utama sahaja” ialah paparan ulang kaji.",
         "sections ticked as read.", "seksyen yang ditanda sudah dibaca.")}
  <div class="notes">
    <aside class="toc"><div class="eyebrow">{B("Sections", "Seksyen")}</div><ol>{toc}</ol><div class="rt">≈ {total_min} min · ✓ = {B("read", "dibaca")}</div></aside>
    <div>
      <div class="ntools"><div class="seg" role="group" aria-label="Notes mode"><button type="button" data-nmode="full" aria-pressed="true">{B("Full notes", "Nota penuh")}</button><button type="button" data-nmode="key" aria-pressed="false">{B("Key points only", "Perkara utama sahaja")}</button></div><span class="muted">{B("Equation numbers follow the text.", "Nombor persamaan mengikut teks.")}</span></div>
      <div class="article">{secs}</div>
    </div>
  </div>
</section>'''

# ---- slides ------------------------------------------------------------------
slides_v = f'''
<section class="view" data-view="slides" id="v-slides" role="tabpanel" aria-labelledby="t-slides" hidden>
  {vhead("Slides", "Slides", "Step through with ◀ ▶ (⏮ ⏭ for the first and last), the ← → keys, the mouse wheel or a swipe on the slide, or drag the bar under the slide to any page; the list below jumps to any slide. Download the PDF for printing and offline reading.", "Gerak dengan ◀ ▶ (⏮ ⏭ untuk slide pertama dan terakhir), kekunci ← →, roda tetikus atau leret pada slide, atau seret bar di bawah slide ke mana-mana halaman; senarai di bawah melompat ke mana-mana slide. Muat turun PDF untuk cetakan dan bacaan luar talian.",
         "each slide you open, once.", "setiap slide yang anda buka, sekali.")}
  <div class="slidebar"><button class="btn ghost" id="svfirst" type="button" aria-label="First slide" title="First slide (Home)">⏮</button><button class="btn ghost" id="svprev" type="button" aria-label="Previous slide" title="Previous (←)">◀</button><span class="count" id="svcount">1 / {nslides}</span><button class="btn ghost" id="svnext" type="button" aria-label="Next slide" title="Next (→)">▶</button><button class="btn ghost" id="svlast" type="button" aria-label="Last slide" title="Last slide (End)">⏭</button><button class="btn ghost" id="svfull" type="button">{B("Full screen", "Skrin penuh")}</button>{save_btn(PART["pdf"], pathlib.Path(PART["pdf"]).name, "Download PDF", "Muat turun PDF", "btn ghost")}<span class="savemsg" aria-live="polite"></span></div>
  <div class="stage-sv" id="svstage"><div class="frame" id="svframe"><div class="cv" id="svcv" data-src="slides/deck.html"></div><p class="lead" id="svload" style="position:absolute;left:12px;top:8px">{B("Loading slides…", "Memuatkan slides…")}</p></div></div>
  <div class="sscrub"><input type="range" id="svscrub" min="1" max="{nslides}" value="1" step="1" aria-label="Slide"><span class="sstip" id="svtip" aria-hidden="true"></span></div>
  <div class="thumbs" id="thumbs"></div>
</section>'''

# ---- examples (answer schemes) -----------------------------------------------
xsecs = ""
for i, (xid, te, tm, body) in enumerate(EXAMPLES):
    xsecs += (f'<section class="xsec" id="{xid}">{body}'
              f'<div class="sfoot"><label class="readck"><input type="checkbox"><span class="rk-todo">{B("Mark this example as worked through", "Tanda contoh ini sudah diikuti")}</span><span class="rk-done">{B("Worked through ✓ — untick to revisit", "Sudah diikuti ✓ — nyahtanda untuk ulang")}</span></label></div></section>')
xtoc = "".join(f'<li><a href="#examples-{xid}" data-toc="{xid}">{i+1}. {B(te, tm)}</a></li>' for i, (xid, te, tm, _) in enumerate(EXAMPLES))
examples_v = f'''
<section class="view" data-view="examples" id="v-examples" role="tabpanel" aria-labelledby="t-examples" hidden>
  {vhead("Examples", "Contoh", "Model answers in exam form, with suggested marks. Try each question on paper first, then compare step by step; tick it at the end when you have worked through it.", "Jawapan model dalam bentuk peperiksaan, dengan markah cadangan. Cuba setiap soalan di atas kertas dahulu, kemudian bandingkan langkah demi langkah; tandanya di hujung apabila anda sudah mengikutinya.",
         "examples ticked as worked through.", "contoh yang ditanda sudah diikuti.")}
  <div class="notes">
    <aside class="toc"><div class="eyebrow">{B("Examples", "Contoh")}</div><ol>{xtoc}</ol></aside>
    <div>
      {mod.EXAMPLES_INTRO}
      <div class="xarticle">{xsecs}</div>
    </div>
  </div>
</section>'''

# ---- exercises ---------------------------------------------------------------
calc = "".join(f'<article class="qx" data-ex="{eid}" id="{eid}"><header><h4>{eid.upper()} · {B(*t)}</h4><span class="mk">{m} {B("marks", "markah")}</span></header><div class="exbody"></div></article>' for eid, t, m in mod.CALC)
timer = f'''<div class="timer"><span class="t" id="tmr">0:00</span><button class="btn" id="tstart" type="button">{B("Start timer", "Mula timer")}</button><button class="btn ghost" id="tpause" type="button" hidden>{B("Pause", "Jeda")}</button><button class="linkbtn" id="treset" type="button">{B("reset", "set semula")}</button><span class="sg">{B("target", "sasaran")} {PART["target_min"]} min · 1.5 min/{B("mark", "markah")}</span></div>'''


def parthead(letter, en, ms, marks, how_en, how_ms):
    return (f'<h3 class="part"><span class="pl">{letter}</span> {B(en, ms)} <span class="pm">· {marks}</span></h3>'
            f'<p class="parthow">{B(how_en, how_ms)}</p>')


ex_v = f'''
<section class="view" data-view="exercises" id="v-exercises" role="tabpanel" aria-labelledby="t-exercises" hidden>
  {vhead("Exercises", "Latihan", "Start the timer. For each question choose Sure or Not sure first, then answer. The summary at the end compares your confidence with your results.", "Mulakan timer. Untuk setiap soalan pilih Yakin atau Tak pasti dahulu, kemudian jawab. Ringkasan di hujung membandingkan keyakinan anda dengan keputusan.",
         "questions answered (B: checked, or solution viewed).", "soalan yang dijawab (B: disemak, atau penyelesaian dilihat).", timer)}
  {parthead("A", "Concept questions", "Soalan konsep", f"{marks_a} × 1 " + B("mark", "markah"), "Click one option. One try: the right answer is marked ✓ and explained.", "Klik satu pilihan. Satu cubaan: jawapan betul ditanda ✓ dan diterangkan.")}
  <div class="card">{"".join(mod.QUICK)}</div>
  {parthead("B", "Calculation, new numbers each time", "Pengiraan, nombor baharu setiap kali", f"{marks_b} " + B("marks", "markah"), "Type your numbers and press Check; each field is marked ✓ or ✗. Retry as often as you like, open hints one at a time, or show the solution. New numbers gives a fresh version.", "Taip nombor anda dan tekan Semak; setiap ruang ditanda ✓ atau ✗. Cuba semula seberapa kerap, buka petunjuk satu demi satu, atau tunjuk penyelesaian. Nombor baharu memberi versi baharu.")}
  <div class="card">{calc}</div>
  {parthead("C", "Find the slip", "Cari kesilapan", f"{marks_c} " + B("marks", "markah"), "Click the line that contains the error. One try.", "Klik baris yang mengandungi kesilapan. Satu cubaan.")}
  <div class="card">{mod.ERRSPOT}</div>
  <h3 class="part"><span class="pl">∑</span> {B("Summary", "Ringkasan")}</h3>
  <div class="card" id="exstats"></div>
</section>'''

# ---- explorer ------------------------------------------------------------------
tasks = "".join(f'<div class="tk" data-ms="{mid}"><header><h4><span class="tkn">{i+1}</span>{B(*t)}</h4><span class="tkok" aria-label="done">✓</span></header><p class="how">{B("Ticks itself: ", "Ditanda sendiri: ")}{B(*how)} · <button class="linkbtn tkself" type="button">{B("not ticked? mark done", "tidak ditanda? tanda selesai")}</button></p></div>' for i, (mid, t, how) in enumerate(mod.LAB_TASKS))
lab_v = f'''
<section class="view" data-view="lab" id="v-lab" role="tabpanel" aria-labelledby="t-lab" hidden>
  {vhead("Explorer", "Explorer", f"Work in the {LAB['name']} (on a phone, open it in its own tab). Do the {len(mod.LAB_TASKS)} tasks on the right; answers to the Explorer’s own questions are under “Check answer” inside it. Python code for assignments and projects, and a panel that runs short scripts in the browser, are at the bottom of this tab.", f"Bekerja dalam {LAB['name']} (di telefon, buka dalam tab sendiri). Buat {len(mod.LAB_TASKS)} tugasan di sebelah kanan; jawapan kepada soalan Explorer ada di bawah “Check answer” di dalamnya. Kod Python untuk assignment dan projek, dan panel untuk menjalankan skrip pendek dalam browser, ada di bahagian bawah tab ini.",
         "tasks done.", "tugasan yang selesai.", f'<a class="btn ghost vbtn" href="#lab-code" data-goto="lab/code">⤓ {B("Python code", "Kod Python")}</a>')}
  <div class="labgrid">
    <div><iframe class="labframe" id="labframe" src="{LAB["file"]}" title="{LAB["name"]}" loading="lazy"></iframe>
      <p class="lead" style="margin-top:8px">{B("Small screen? ", "Skrin kecil? ")}<a href="{LAB["file"]}" target="_blank" rel="noopener">{B("Open the Explorer in its own tab", "Buka Explorer dalam tab sendiri")}</a>. {B("Tasks done there are recorded here when you come back.", "Tugasan yang selesai di situ direkod di sini apabila anda kembali.")}</p></div>
    <div class="card"><h2>{B("Tasks", "Tugasan")} · {LAB["name"]}</h2><p class="lead">{B("Each task ticks itself when the Explorer sees it done. Tick by hand only if it does not.", "Setiap tugasan ditanda sendiri apabila Explorer melihatnya selesai. Tanda sendiri hanya jika ia tidak ditanda.")}</p>{tasks}</div>
  </div>
  {code_card(PART["code"])}
  {run_card(PART["n"], PART["slug"], PART["code"])}
</section>'''

# ---- glossary ----------------------------------------------------------------
grows = "".join(f'<tr><td class="g1">{t}</td><td>{B(e, m)}</td></tr>' for t, e, m in mod.GLOSSARY)
gl_v = f'''
<section class="view" data-view="glossary" id="v-glossary" role="tabpanel" aria-labelledby="t-glossary" hidden>
  {vhead("Glossary", "Glosari", "Look up a term; type in the box to filter. Terms stay in English in both languages; the explanation follows the language you chose.", "Cari istilah; taip dalam kotak untuk menapis. Istilah kekal dalam bahasa Inggeris dalam kedua-dua bahasa; penjelasan mengikut bahasa yang anda pilih.")}
  <div class="card"><input class="gfilter" id="gfilter" type="search" placeholder="filter…" aria-label="Filter">
  <div class="tbl"><table class="gloss"><tbody>{grows}</tbody></table></div></div>
</section>'''


# ---- feedback (the rz-tutor feedback module is mounted in #rzfeedback by tools/add_tutor.py) ---------
fb_v = f'''
<section class="view" data-view="feedback" id="v-feedback" role="tabpanel" aria-labelledby="t-feedback" hidden>
  {vhead("Feedback", "Maklum balas", "Tell the lecturer what works for you and what does not: rate this part, name the point that is still unclear, or report a mistake. The page is improved from time to time with what students say; the changes are listed under What’s new.", "Beritahu pensyarah apa yang membantu anda dan apa yang tidak: beri penilaian bahagian ini, nyatakan perkara yang masih kabur, atau laporkan kesilapan. Halaman ini ditambah baik dari semasa ke semasa berdasarkan maklum balas pelajar; perubahannya disenaraikan di bawah Apa yang baharu.")}
  <div id="rzfeedback"><p class="lead">{B("The feedback forms open on the course website, razinutm.github.io/My_Lectures.", "Borang maklum balas dibuka di laman web kursus, razinutm.github.io/My_Lectures.")}</p></div>
</section>'''

# ---- footer: home and neighbouring parts ----------------------------------------
def pnav(p, en, ms, cls):
    if not p: return f'<span class="{cls}"></span>'
    return f'<a class="{cls}" href="../{p[1]}/index.html"><span class="pk">{B(en, ms)}</span><b>{p[2]} — {partlabel(p)}</b></a>'


soon = (f'<span class="pnext soon"><span class="pk">{B("Next", "Seterusnya")}</span><b>{next_soon[2]} — {partlabel(next_soon)}</b><span class="pk">{B("coming", "akan datang")}</span></span>' if next_soon else "")
footnav = (f'<nav class="pagenav" aria-label="Parts">{pnav(prev_p, "← Previous", "← Sebelum", "pprev")}'
           f'<a class="phome" href="../index.html"><span aria-hidden="true">⌂</span> {B("Course home", "Laman kursus")}</a>'
           + (pnav(next_p, "Next →", "Seterusnya →", "pnext") if next_p else soon) + '</nav>')
drawer = f'''
{footnav}
</main>
<footer class="foot"><p class="lect"><img class="fava" data-avsrc="head" alt="" width="40" height="40" decoding="async">SEAA 4243 Finite Element Method · Faculty of Civil Engineering, Universiti Teknologi Malaysia. {B("Lecturer: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin.", "Pensyarah: Prof. Madya Ts. Dr. Ahmad Razin Zainal Abidin.")}</p>
<p>{B("Third-party images are credited where they appear (MIT, BSD, LGPL and CC BY licences).", "Imej pihak ketiga dikreditkan di tempat ia muncul (lesen MIT, BSD, LGPL dan CC BY).")}</p>
{TUTOR_LINE}
{copyright_line()}</footer>
</div>
<div class="scrim" id="scrim" hidden></div>
<aside class="drawer" id="drawer" aria-label="Short notes"><div class="dh"><h2>{B("Short notes", "Nota ringkas")}</h2><button class="iconbtn" id="drclose" type="button" aria-label="Close">✕</button></div>{mod.short_notes(A)}</aside>
<button class="tpill" id="tpill" type="button" hidden>0:00</button>
'''

body = head + start + notes_v + slides_v + examples_v + ex_v + lab_v + gl_v + fb_v + drawer
html_out = page(cfg, body, script_extra=f"<script>\n{mod.EX_JS}\n</script>")
(OUT / "index.html").write_text(html_out)
print(PART["slug"], "written:", len(html_out) // 1024, "KB,", nslides, "slides,", len(NOTES), "sections")
