#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Write the SEAA 4333 perception survey (Week 7 and Week 15) in its two forms from one list of items.

What: the five agreement items and the open question below, in English and Malay, become
  perception_survey_moodle.xml   questions for a UTM eLearning (Moodle) Feedback activity:
                                 Feedback activity > Templates > Import questions
  perception_survey_slip.pdf     the paper version, two slips on each A4 page, for a class without Wi-Fi
The XML follows the import format documented by Moodle (docs.moodle.org/en/Feedback_Import): root
FEEDBACK VERSION="200701"; every ITEM carries ITEMID, ITEMTEXT, ITEMLABEL, PRESENTATION, OPTIONS,
DEPENDITEM and DEPENDVALUE; a rated multiple choice is "r>>>>>" then value####label lines joined by "|";
a long text answer is "columns|rows".

How to call it, from this folder:
  python3 make_survey.py            (needs Python's playwright and Chromium for the PDF)

Why it is like this: the items are written once, so the online form, the paper slip and the reading
guide (the Docs artifact "SEAA 4333 Perception Survey") cannot drift apart. The same items run in
Week 7 and Week 15, so the two runs can be compared.
"""
import html
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent

OPENING = ("Anonymous, about two minutes. Your answers help improve the rest of this course and its next offering. "
           "They do not affect your marks. Do not write your name.",
           "Tanpa nama, kira-kira dua minit. Jawapan anda membantu menambah baik baki kursus ini dan kursus ini pada "
           "semester akan datang. Jawapan anda tidak menjejaskan markah. Jangan tulis nama anda.")
SCALE = [("Strongly disagree", "Sangat tidak setuju"), ("Disagree", "Tidak setuju"), ("Neutral", "Neutral"),
         ("Agree", "Setuju"), ("Strongly agree", "Sangat setuju")]
ITEMS = [  # (label, English, Malay)
    ("Q1 engagement", "In the 3-hour sessions, I spend most of the time solving problems, on my own or with my team.",
     "Dalam sesi 3 jam, saya menghabiskan sebahagian besar masa dengan menyelesaikan masalah, sendiri atau bersama pasukan."),
    ("Q2 perceived learning", "I learn a great deal in these sessions.",
     "Saya belajar banyak dalam sesi ini."),
    ("Q3 hand solution", "I can write a full hand solution (Ref | Calculations | Output) to an exam-size problem without the app.",
     "Saya boleh menulis penyelesaian penuh dengan tangan (Ref | Calculations | Output) bagi masalah sebesar soalan "
     "peperiksaan tanpa app."),
    ("Q4 feedback", "The quick checks, the Labs and the app help me check my own working.",
     "Semak cepat, Lab dan app membantu saya memeriksa jalan kerja saya sendiri."),
    ("Q5 format", "For a course like this, I would choose this format over traditional lectures.",
     "Bagi kursus seperti ini, saya akan memilih format ini berbanding kuliah biasa."),
]
OPEN = ("Q6 one change", "What one change would help you learn more in this course?",
        "Apakah satu perubahan yang akan membantu anda belajar dengan lebih baik dalam kursus ini?")


def cdata(tag: str, text: str) -> str:
    assert "]]>" not in text
    return f"               <{tag}><![CDATA[{text}]]></{tag}>\n"


def moodle_xml() -> str:
    rated = "r>>>>>" + "\n|".join(f"{v}####{v} - {en} / {ms}" for v, (en, ms) in enumerate(SCALE, 1))
    out = ['<?xml version="1.0" encoding="UTF-8" ?>\n', '<FEEDBACK VERSION="200701" COMMENT="XML-Importfile for mod/feedback">\n',
           "     <ITEMS>\n"]
    for i, (label, en, ms) in enumerate(ITEMS + [OPEN], 1):
        is_open = (label, en, ms) == OPEN
        out.append(f'          <ITEM TYPE="{"textarea" if is_open else "multichoicerated"}" REQUIRED="{0 if is_open else 1}">\n')
        out.append(cdata("ITEMID", str(i)))
        out.append(cdata("ITEMTEXT", f"{en} / {ms}"))
        out.append(cdata("ITEMLABEL", label))
        out.append(cdata("PRESENTATION", "60|5" if is_open else rated))
        out.append(cdata("OPTIONS", "" if is_open else "h"))   # h: no "Not selected" choice on a required item
        out.append(cdata("DEPENDITEM", "0"))
        out.append(cdata("DEPENDVALUE", ""))
        out.append("          </ITEM>\n")
    out.append("     </ITEMS>\n</FEEDBACK>\n")
    return "".join(out)


def slip() -> str:
    e = html.escape
    rows = "".join(
        f'<tr><td class="q"><b>{e(label.split()[0])}</b></td><td class="it"><span class="en">{e(en)}</span>'
        f'<span class="ms">{e(ms)}</span></td>' + "".join(f'<td class="c"><span class="o">{v}</span></td>' for v in range(1, 6)) + "</tr>"
        for label, en, ms in ITEMS)
    head = "".join(f'<th class="c"><b>{v}</b><br>{e(en)}<br><i>{e(ms)}</i></th>' for v, (en, ms) in enumerate(SCALE, 1))
    one = f"""<section class="slip">
  <div class="top"><div><b>SEAA 4333 Reinforced Concrete Design II</b> · Perception survey / <i>Tinjauan persepsi</i></div>
    <div class="wk">Week / <i>Minggu</i>: <span class="box"></span> 7 &nbsp; <span class="box"></span> 15</div></div>
  <p class="open">{e(OPENING[0])}<br><i>{e(OPENING[1])}</i></p>
  <p class="how">Circle one number for each statement. / <i>Bulatkan satu nombor bagi setiap pernyataan.</i></p>
  <table><thead><tr><th></th><th></th>{head}</tr></thead><tbody>{rows}</tbody></table>
  <p class="q6"><b>Q6</b> {e(OPEN[1])} <i>{e(OPEN[2])}</i> <span class="opt">(optional / <i>tidak wajib</i>)</span></p>
  <div class="lines"></div>
  <p class="end">Hand it in at the door. Thank you. / <i>Serahkan di pintu. Terima kasih.</i></p>
</section>"""
    css = """@page { size: A4; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: Inter, 'DejaVu Sans', sans-serif; color: #1c1b19; font-size: 8.6pt; line-height: 1.28 }
.page { width: 210mm; height: 297mm; display: flex; flex-direction: column }
.slip { height: 148.5mm; padding: 7mm 11mm 5mm; display: flex; flex-direction: column; gap: 1.8mm }
.slip + .slip { border-top: 0.4mm dashed #8a857b }
.top { display: flex; justify-content: space-between; align-items: baseline; font-size: 9.6pt; border-bottom: 0.3mm solid #1c1b19; padding-bottom: 1.4mm }
.wk { white-space: nowrap }
.box { display: inline-block; width: 3.4mm; height: 3.4mm; border: 0.3mm solid #1c1b19; vertical-align: -0.5mm; margin-left: 1.5mm }
p { margin: 0 }
.open { color: #47443d; font-size: 7.8pt }
.how { font-size: 8.2pt }
table { width: 100%; border-collapse: collapse; table-layout: fixed }
col.q { width: 7mm } col.it { width: auto } col.c { width: 11.5mm }
th { font-weight: normal; font-size: 6.1pt; line-height: 1.15; color: #47443d; vertical-align: bottom; padding: 0 0.5mm 1mm }
th b { font-size: 8pt; color: #1c1b19 }
td { border-top: 0.25mm solid #c9c4b8; padding: 0.8mm 0.5mm; vertical-align: middle }
td.q { vertical-align: top; padding-top: 1.1mm }
td.it .en { display: block }
td.it .ms { display: block; font-style: italic; color: #47443d; font-size: 8.1pt }
td.c, th.c { text-align: center }
.o { display: inline-block; width: 5.4mm; height: 5.4mm; line-height: 5mm; border: 0.3mm solid #8a857b; border-radius: 50%; font-size: 8pt }
.q6 { border-top: 0.25mm solid #c9c4b8; padding-top: 1.6mm }
.q6 i { color: #47443d }
.opt { color: #8a857b; font-size: 7.6pt }
.lines { flex: 1; min-height: 11mm; background: repeating-linear-gradient(to bottom, transparent 0, transparent 5.3mm, #c9c4b8 5.3mm, #c9c4b8 5.55mm) }
.end { font-size: 8pt; color: #47443d; text-align: right }"""
    colg = '<colgroup><col class="q"><col class="it">' + '<col class="c">' * 5 + "</colgroup>"
    one = one.replace("<table>", "<table>" + colg)
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SEAA 4333 perception survey slip</title><style>{css}</style></head><body><div class="page">{one}{one}</div></body></html>'


def main() -> None:
    x = moodle_xml()
    ET.fromstring(x.encode("utf-8"))  # well-formed
    (HERE / "perception_survey_moodle.xml").write_text(x, encoding="utf-8")
    s = slip()
    (HERE / "perception_survey_slip.html").write_text(s, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto((HERE / "perception_survey_slip.html").as_uri()); pg.wait_for_timeout(300)
        over = pg.evaluate("() => [...document.querySelectorAll('.slip')].map(s => s.scrollHeight - s.clientHeight)")
        assert all(o <= 0 for o in over), f"slip overflows by {over} px"
        pg.pdf(path=str(HERE / "perception_survey_slip.pdf"), format="A4", print_background=True)
        b.close()
    print("perception_survey_moodle.xml: 5 rated items + 1 open; perception_survey_slip.pdf: 1 page, 2 slips")


if __name__ == "__main__":
    main()
