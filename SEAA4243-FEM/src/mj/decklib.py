"""Slide-building helpers for the SEAA 4243 decks (Slides artifact format: inline styles only)."""
import json, re, pathlib, html as _html

# ---- tokens ---------------------------------------------------------------
BG = "#FBFAF6"; PANEL = "#EEF2F7"; PANEL_B = "#D6DEE8"; DARK = "#15223B"; INK = "#1B2330"; BODY = "#3C4454"
MUTED = "#6B7280"; MAROON = "#8C1D2F"; TEAL = "#1F6FA3"; AMBER = "#F4B942"; AMBER_PALE = "#FBF1D6"; GREEN = "#2E7D5B"
HAIR = "#E1E4EA"; WHITE = "#FFFFFE"; LIGHT_ON_DARK = "#FBFAF6"; SOFT_ON_DARK = "#BFD0E6"; CODE_BG = "#1E2633"

SERIF = "'Source Serif 4', Georgia, serif"
SANS = "'IBM Plex Sans', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Courier New', monospace"

FACES = {
    "source-serif-4": {"family": "Source Serif 4", "href": "https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&display=swap"},
    "ibm-plex-sans": {"family": "IBM Plex Sans", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap"},
    "jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap"},
}


def esc(t):
    return _html.escape(t, quote=False)


class Deck:
    def __init__(self, root, title, footer_text, eq_dir, fig_dir, eq_report):
        self.root = pathlib.Path(root); self.title = title; self.footer_text = footer_text
        self.eq_dir = pathlib.Path(eq_dir); self.fig_dir = pathlib.Path(fig_dir); self.eq_report = eq_report
        self.slides = []  # (id, html)
        self.sections = {}
        # the lecturer's avatar, uploaded to this deck's asset store (ids per deck in _avatar.json)
        av = self.root / "_avatar.json"
        self.av = json.loads(av.read_text()) if av.exists() else {}

    # ---- assets ------------------------------------------------------------
    def eq(self, name, maxw=None, scale=1.0, maxh=None):
        s = (self.eq_dir / f"{name}.svg").read_text()
        r = self.eq_report[name]; w, h = r["w"] * scale, r["h"] * scale
        if maxw and w > maxw:
            h = h * maxw / w; w = maxw
        if maxh and h > maxh:
            w = w * maxh / h; h = maxh
        s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w:.0f}" height="{h:.0f}"', s, count=1)
        return s

    def fig(self, name, width=None, height=None):
        s = (self.fig_dir / f"{name}.svg").read_text()
        m = re.search(r'width="([\d.]+)" height="([\d.]+)"', s)
        w0, h0 = float(m.group(1)), float(m.group(2))
        if width and not height:
            width, height = width, h0 * width / w0
        elif height and not width:
            width, height = w0 * height / h0, height
        elif not width and not height:
            width, height = w0, h0
        s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{width:.0f}" height="{height:.0f}"', s, count=1)
        return s

    # ---- fragments ---------------------------------------------------------
    def header(self, eyebrow, title, title_size=52):
        return (f'<div style="display:flex;flex-direction:column;gap:10px">'
                f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{MAROON}">{eyebrow}</p>'
                f'<h2 style="font-family:{SERIF};font-size:{title_size}px;font-weight:600;line-height:1.1;color:{DARK}">{title}</h2></div>')

    def footer(self, n, dark=False):
        c = SOFT_ON_DARK if dark else MUTED
        badge = (f'<img src="{self.av["head"]}" alt="" style="position:absolute;left:128px;bottom:52px;width:52px;height:52px;border-radius:50%">'
                 if self.av.get("head") else "")
        left = 196 if badge else 128
        return (badge + f'<p style="position:absolute;left:{left}px;bottom:64px;font-size:24px;color:{c}">{self.footer_text}</p>'
                f'<p style="position:absolute;right:128px;bottom:64px;width:240px;text-align:right;font-size:24px;color:{c}">{n}</p>')

    def panel(self, inner, label=None, bg=PANEL, pad="28px 40px", gap=24, border=PANEL_B):
        lab = f'<p style="font-size:26px;color:{MUTED};white-space:nowrap">{label}</p>' if label else ""
        return (f'<div style="background:{bg};border:1px solid {border};border-radius:12px;padding:{pad};display:flex;flex-direction:row;'
                f'align-items:center;justify-content:center;gap:{gap}px">{inner}{lab}</div>')

    def eqpanel(self, name, label=None, maxw=1500, scale=1.0, bg=PANEL, maxh=None, colw=None, pad="28px 40px"):
        if colw:
            labw = (len(label) * 13 + 24) if label else 0
            maxw = min(maxw, colw - 84 - labw)
        return self.panel(self.eq(name, maxw=maxw, scale=scale, maxh=maxh), label, bg=bg, pad=pad)

    def p(self, text, size=34, color=BODY, weight=400, lh=1.35, extra=""):
        return f'<p style="font-size:{size}px;line-height:{lh};color:{color};font-weight:{weight};{extra}">{text}</p>'

    def ul(self, items, size=32, color=BODY, lh=1.4, gap=10):
        lis = "".join(f'<li>{i}</li>' for i in items)
        return f'<ul style="font-size:{size}px;line-height:{lh};color:{color};display:flex;flex-direction:column;gap:{gap}px">{lis}</ul>'

    def card(self, inner, bg=WHITE, pad=32, gap=14, border=HAIR, extra=""):
        return f'<div style="background:{bg};border:1px solid {border};border-radius:14px;padding:{pad}px;display:flex;flex-direction:column;gap:{gap}px;{extra}">{inner}</div>'

    def h3(self, text, size=30, color=DARK):
        return f'<h3 style="font-size:{size}px;font-weight:600;line-height:1.2;color:{color}">{text}</h3>'

    def pill(self, text, bg=AMBER, color=DARK, size=24):
        return f'<p style="font-size:{size}px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{color};background:{bg};padding:8px 18px;border-radius:999px;white-space:nowrap">{text}</p>'

    def step(self, n, text, size=30):
        return (f'<div style="display:flex;flex-direction:row;gap:18px;align-items:start">'
                f'<p style="font-size:24px;font-weight:600;color:{LIGHT_ON_DARK};background:{DARK};border-radius:999px;padding:4px 16px;white-space:nowrap">{n}</p>'
                f'<p style="font-size:{size}px;line-height:1.35;color:{BODY}">{text}</p></div>')

    def code(self, lines, size=26):
        ps = "".join(f'<p style="font-size:{size}px;line-height:1.5;color:#E8ECF2;white-space:nowrap">{esc(l) if l.strip() else "&#160;"}</p>' for l in lines)
        return f'<div style="background:{CODE_BG};border-radius:12px;padding:28px 36px;display:flex;flex-direction:column;gap:0px;font-family:{MONO}">{ps}</div>'

    # ---- slide kinds -------------------------------------------------------
    def add(self, sid, body, notes="", bg=BG, color=BODY, transition="fade", pad="104px 128px 150px", layout="display:flex;flex-direction:column;gap:36px", section=None):
        if sid == "cover" and self.av.get("wave"):
            body += f'<img src="{self.av["wave"]}" alt="The lecturer, waving" style="position:absolute;right:96px;top:96px;width:280px;height:500px">'
        aside = f"<aside>{esc(notes.strip())}</aside>" if notes else ""
        sec = (f'<section id="{sid}" data-transition="{transition}" style="background:{bg};color:{color};font-family:{SANS};padding:{pad};{layout}">'
               f'{body}{aside}</section>')
        self.slides.append((sid, sec))
        if section:
            self.sections[f"s{len(self.sections)+1}"] = {"description": section, "start": sid}

    def content(self, sid, eyebrow, title, body, notes="", section=None, title_size=52):
        n = len(self.slides) + 1
        self.add(sid, self.header(eyebrow, title, title_size) + body + self.footer(n), notes, section=section)

    def divider(self, sid, number, title, subtitle, timing, notes="", section=None):
        n = len(self.slides) + 1
        body = (f'<div style="display:flex;flex-direction:row;gap:64px;align-items:center;flex:1">'
                f'<p style="font-family:{SERIF};font-size:260px;font-weight:600;line-height:1;color:{AMBER};width:300px">{number}</p>'
                f'<div style="display:flex;flex-direction:column;gap:22px;flex:1">'
                f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{AMBER}">{timing}</p>'
                f'<h2 style="font-family:{SERIF};font-size:84px;font-weight:600;line-height:1.08;color:{LIGHT_ON_DARK}">{title}</h2>'
                f'<p style="font-size:36px;line-height:1.35;color:{SOFT_ON_DARK}">{subtitle}</p></div>'
                + (f'<img src="{self.av["explain"]}" alt="The lecturer, explaining" style="height:470px;width:331px;flex:none;align-self:flex-end">' if self.av.get("explain") else "")
                + '</div>')
        self.add(sid, body + self.footer(n, dark=True), notes, bg=DARK, color=LIGHT_ON_DARK, transition="push", section=section)

    def activity(self, sid, number, minutes, mode, title, left, right=None, done_line=None, notes="", section=None):
        n = len(self.slides) + 1
        badge = (f'<div style="position:absolute;right:128px;top:80px;width:160px;height:160px;border-radius:50%;background:{AMBER};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0px">'
                 f'<p style="font-size:64px;font-weight:600;line-height:1;color:{DARK}">{minutes}</p><p style="font-size:24px;font-weight:600;letter-spacing:2px;color:{DARK}">MIN</p></div>')
        head = (f'<div style="display:flex;flex-direction:column;gap:10px;width:1380px">'
                f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{MAROON}">Activity {number} · {mode}</p>'
                f'<h2 style="font-family:{SERIF};font-size:52px;font-weight:600;line-height:1.1;color:{DARK}">{title}</h2></div>')
        cols = f'<div style="display:flex;flex-direction:row;gap:44px;flex:1;align-items:start">{left}{right or ""}</div>'
        done = self.p(done_line, 26, MUTED) if done_line else ""
        self.add(sid, badge + head + cols + done + self.footer(n), notes, bg=AMBER_PALE, section=section)

    # ---- files -------------------------------------------------------------
    def write(self, created_at):
        (self.root / "project" / "slides").mkdir(parents=True, exist_ok=True)
        order = [sid for sid, _ in self.slides]
        deck = {"v": 4, "createdOnFiles": {"v": 1, "at": created_at}, "lists": "css", "title": self.title, "order": order,
                "sections": self.sections, "faces": FACES, "designSystems": []}
        (self.root / "project" / "deck.json").write_text(json.dumps(deck, indent=1))
        for sid, sec in self.slides:
            (self.root / "project" / "slides" / f"{sid}.html").write_text(sec)
        return order


# ---- shared layout helpers --------------------------------------------------
def two_col(left, right, lw=None, rw=None, gap=48, align="start"):
    ls = f"width:{lw}px" if lw else "flex:1"
    rs = f"width:{rw}px" if rw else "flex:1"
    return (f'<div style="display:flex;flex-direction:row;gap:{gap}px;flex:1;align-items:{align}">'
            f'<div style="{ls};display:flex;flex-direction:column;gap:28px">{left}</div>'
            f'<div style="{rs};display:flex;flex-direction:column;gap:28px">{right}</div></div>')

def col(*parts, gap=28, extra=""):
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;{extra}">{"".join(parts)}</div>'

def row(*parts, gap=28, extra="", align="center"):
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;align-items:{align};{extra}">{"".join(parts)}</div>'

def figbox(svg, bg=WHITE):
    return f'<div style="background:{bg};border:1px solid {HAIR};border-radius:14px;padding:24px;display:flex;align-items:center;justify-content:center">{svg}</div>'

def callout(text, kind="why", size=28):
    colr = {"why": TEAL, "warn": MAROON, "ok": GREEN}[kind]
    tag = {"why": "Why", "warn": "Watch out", "ok": "Check"}[kind]
    return (f'<div style="display:flex;flex-direction:row;gap:16px;align-items:start;background:{WHITE};border:1px solid {HAIR};border-radius:12px;padding:20px 24px">'
            f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{colr};white-space:nowrap">{tag}</p>'
            f'<p style="font-size:{size}px;line-height:1.35;color:{BODY}">{text}</p></div>')

def table(headers, rows, widths, size=28):
    th = "".join(f'<th style="width:{w}%">{h}</th>' for h, w in zip(headers, widths))
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table style="font-size:{size}px;color:{BODY};border:1px solid {HAIR}"><tr>{th}</tr>{trs}</table>'

def session_map(blocks):
    """blocks: list of (t0, name, mins, act_label, is_break)"""
    segs = ""
    for t0, name, mins, act, brk in blocks:
        bg = "#E6E2D8" if brk else WHITE
        chip = f'<p style="font-size:24px;font-weight:600;color:{DARK};background:{AMBER};padding:6px 14px;border-radius:999px;white-space:nowrap">{act}</p>' if act else '<p style="font-size:24px;color:#8A8F99">no activity</p>'
        segs += (f'<div style="flex:{mins};background:{bg};border:1px solid {HAIR};border-radius:12px;padding:20px 16px;display:flex;flex-direction:column;gap:10px;min-width:150px">'
                 f'<p style="font-size:24px;font-weight:600;color:{MAROON}">{t0}</p><p style="font-size:26px;font-weight:600;line-height:1.2;color:{DARK}">{name}</p>'
                 f'<p style="font-size:24px;color:{MUTED}">{mins} min</p>{chip}</div>')
    return f'<div style="display:flex;flex-direction:row;gap:12px;align-items:stretch">{segs}</div>'

def week_map(weeks, now):
    cells = ""
    for w, t, s in weeks:
        bg = AMBER if w == now else WHITE
        cells += (f'<div style="flex:1;background:{bg};border:1px solid {HAIR};border-radius:14px;padding:22px 18px;display:flex;flex-direction:column;gap:8px">'
                  f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;color:{MAROON}">{w}</p>'
                  f'<p style="font-size:28px;font-weight:600;line-height:1.2;color:{DARK}">{t}</p>'
                  f'<p style="font-size:24px;line-height:1.3;color:{BODY}">{s}</p></div>')
    return f'<div style="display:flex;flex-direction:row;gap:16px">{cells}</div>'

WEEKS = [("1", "Heat transfer 1", "PDE · BCs · shape functions"), ("2", "Heat transfer 2", "[k] · assembly · solve · Asg 4"),
         ("3", "Plane stress 1", "PDE · [E] · [N]"), ("4", "Plane stress 2", "[k] = ∫[B]ᵀ[E][B] · loads"),
         ("5", "Plane stress 3", "stress recovery · Q8 · Project brief"), ("6", "ANSYS demo", "hand calc vs software"),
         ("7", "Practical FEM", "convergence · interpretation")]


# ---- QR codes, web images and credits (added for the QR labs and image slides) ----
def qr_svg(url, px=340, label="QR code"):
    """Inline SVG of a QR code built from filled module runs (no strokes, no classes)."""
    import segno
    q = segno.make(url, error="m", micro=False)
    rows = [list(r) for r in q.matrix]; n = len(rows); b = 2; N = n + 2 * b; d = []
    for y, r in enumerate(rows):
        x = 0
        while x < n:
            if r[x]:
                x0 = x
                while x < n and r[x]: x += 1
                d.append(f"M{x0 + b} {y + b}h{x - x0}v1h-{x - x0}z")
            else:
                x += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {N} {N}" aria-label="{label}" shape-rendering="crispEdges">'
            f'<rect x="0" y="0" width="{N}" height="{N}" fill="#FFFFFE"/><path fill="#15223B" d="{"".join(d)}"/></svg>')


def webimg(src, alt, w, h, pad=12, bg=WHITE):
    return (f'<div style="background:{bg};border:1px solid {HAIR};border-radius:14px;padding:{pad}px;display:flex;align-items:center;justify-content:center">'
            f'<img src="{src}" alt="{alt}" style="width:{w}px;height:{h}px;object-fit:contain"></div>')


def credit(text, size=24):
    return f'<p style="font-size:{size}px;line-height:1.35;color:{MUTED}">{text}</p>'


def qr_card(url, name, px=300):
    """QR card: the code, the Explorer's name, and the address broken at its slashes so a student can type it."""
    rest = url.replace("https://", "")
    if "github.io/" in rest:   # razinutm.github.io/ · My_Lectures/SEAA4243-FEM/ · labs/x.html
        host, _, path = rest.partition("/")
        head, _, tail = path.rpartition("/labs/")
        lines = [host + "/", head + "/", "labs/" + tail]
    else:
        host, _, ident = rest.rpartition("/"); lines = [host + "/", ident]
    return (f'<div style="background:{WHITE};border:1px solid {HAIR};border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:10px;align-items:center;width:360px">'
            f'{qr_svg(url, px, "QR code that opens the " + name)}'
            f'<p style="font-size:28px;font-weight:600;line-height:1.2;color:{DARK};text-align:center">{name}</p>'
            f'<p style="font-family:{MONO};font-size:20px;line-height:1.3;color:{BODY};text-align:center">{"<br>".join(lines)}</p></div>')


def qr_lab(D, sid, minutes, title, tasks, labs, done_line, notes, section=None, size=24):
    """Amber QR activity slide: numbered tasks on the left, one or two QR cards on the right."""
    n = len(D.slides) + 1
    badge = (f'<div style="position:absolute;right:128px;top:80px;width:160px;height:160px;border-radius:50%;background:{AMBER};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0px">'
             f'<p style="font-size:64px;font-weight:600;line-height:1;color:{DARK}">{minutes}</p><p style="font-size:24px;font-weight:600;letter-spacing:2px;color:{DARK}">MIN</p></div>')
    head = (f'<div style="display:flex;flex-direction:column;gap:10px;width:1380px">'
            f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:{MAROON}">QR Explorer · pairs, one phone</p>'
            f'<h2 style="font-family:{SERIF};font-size:52px;font-weight:600;line-height:1.1;color:{DARK}">{title}</h2></div>')
    px = 300 if len(labs) == 1 else 250
    left = D.card(D.h3("Scan, then do") + "".join(D.step(i + 1, t, 28) for i, t in enumerate(tasks)), extra="flex:1", gap=16)
    right = f'<div style="display:flex;flex-direction:row;gap:20px;align-items:start">{"".join(qr_card(u, nm, px) for u, nm in labs)}</div>'
    cols = f'<div style="display:flex;flex-direction:row;gap:40px;flex:1;align-items:start">{left}{right}</div>'
    done = D.p(done_line, 26, MUTED) if done_line else ""
    D.add(sid, badge + head + cols + done + D.footer(n), notes, bg=AMBER_PALE, section=section)


PAGES = "https://razinutm.github.io/My_Lectures/SEAA4243-FEM/labs/"
LABS = {"shape": (PAGES + "shape.html", "Shape Function Explorer"),
        "heat": (PAGES + "heat.html", "Heat Conduction Explorer"),
        "cant": (PAGES + "cant.html", "Cantilever Explorer"),
        "stress": (PAGES + "stress.html", "Stress Recovery Explorer")}
