"""Part 6, Notes §7 (Workbench how-to) as a supplementary file for Dr RJ on the other part pages.

The text is the same as on the Part 6 page: it is taken from 06-ansys-demo/tutor/blocks-p6.json (English) and
blocks-p6.ms.json (Malay headings), which tools/add_tutor.py writes from the built page. So run this after
add_tutor.py (src/build.sh does). Output: SEAA4243-FEM/tutor/extra/ansys-workbench-howto.json, wired in
rz-tutor-worker apps.json -> seaa4243 -> extra for parts p1-p5 (on Part 6 the section is already primary).

Each sub-heading of §7 becomes one block with a url, so Dr RJ can cite it and give a "Go to" button that opens
Part 6, Notes §7 from any part.
"""
import json
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = SITE / "06-ansys-demo" / "tutor"
OUT = SITE / "tutor" / "extra" / "ansys-workbench-howto.json"
URL = "https://razinutm.github.io/My_Lectures/SEAA4243-FEM/06-ansys-demo/index.html#notes-n7"
SECTION = "notes-n7"


def section(fname):
    blocks = json.loads((SRC / fname).read_text(encoding="utf-8"))["blocks"]
    text = next(b["text"] for b in blocks if b["id"] == SECTION)
    head, *parts = text.split("\n## ")
    first_line, _, intro = head.partition("\n")          # "[notes-n7] Notes 7. Workbench how-to: ..."
    return first_line.split("] ", 1)[1], intro.strip(), [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1].strip() if "\n" in p else "") for p in parts]


def main():
    title_en, intro_en, parts_en = section("blocks-p6.json")
    title_ms, _, parts_ms = section("blocks-p6.ms.json")
    assert len(parts_en) == len(parts_ms), "the English and Malay sections must have the same sub-headings"
    blocks = []
    rows = [("Introduction", "Pengenalan", intro_en)] + [(h, parts_ms[i][0], body) for i, (h, body) in enumerate(parts_en)]
    for k, (h_en, h_ms, body) in enumerate(rows):
        bid = f"p6-howto-{k}"
        blocks.append({
            "id": bid,
            "text": f"[{bid}] SEAA 4243 Part 6 · {title_en} · {h_en}\n{body}",
            "url": URL,
            "title_en": f"Part 6 · Notes §7 · {h_en}",
            "title_ms": f"Part 6 · Nota §7 · {h_ms}",
        })
    doc = {
        "title": "SUPPLEMENTARY — SEAA 4243 Part 6, Notes §7: Workbench how-to (ANSYS Student: DesignModeler and Mechanical), by the same lecturer",
        "context": ("The same text as Part 6, Notes §7 of this course, for questions on how to do something in ANSYS Workbench "
                    "(curved edges, holes, fillets, splines, meshing a curved shape, supports, varying loads, results along a path, "
                    "convergence, error messages). Its ids open Part 6, Notes §7. The menu names were checked against the Ansys Help "
                    "for release 2026 R1; if a student's screen differs, the object and its name are the same. Where it and the current "
                    "page differ, follow the current page."),
        "blocks": blocks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(SITE)}: {len(blocks)} blocks, {sum(len(b['text']) for b in blocks)} characters")


if __name__ == "__main__":
    main()
