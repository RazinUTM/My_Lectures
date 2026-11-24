"""matplotlib diagrams exported as SVG with all text converted to paths (no <text> elements)."""
import re, io, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon
import numpy as np

plt.rcParams.update({
    "svg.fonttype": "path",
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.size": 16,
    "axes.linewidth": 0,
})

NAVY = "#15223B"; MAROON = "#8C1D2F"; TEAL = "#1F6FA3"; AMBER = "#F4B942"
FILL = "#DCE6F0"; INK = "#1B2330"; GREY = "#8A94A6"; LIGHT = "#FBFAF6"


def save_svg(fig, path, name, alt=""):
    """save figure to SVG, strip metadata/style, prefix ids, set px size + aria-label"""
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.05, transparent=True)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index("<svg"):]
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    # size in px (matplotlib writes pt at 72 dpi -> 1pt = 1px here)
    m = re.search(r'width="([\d.]+)pt" height="([\d.]+)pt" viewBox="([^"]+)"', s)
    w, h, vb = float(m.group(1)), float(m.group(2)), m.group(3)
    pre = re.sub(r"[^A-Za-z0-9_-]", "", name)
    s = re.sub(r'id="([^"]+)"', lambda mm: f'id="{pre}-{mm.group(1)}"', s)
    s = re.sub(r'url\(#([^)]+)\)', lambda mm: f'url(#{pre}-{mm.group(1)})', s)
    s = re.sub(r'href="#([^"]+)"', lambda mm: f'href="#{pre}-{mm.group(1)}"', s)
    s = re.sub(r"<svg[^>]*>", f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w:.0f}" height="{h:.0f}" viewBox="{vb}" aria-label="{alt or name}">', s, count=1)
    s = re.sub(r'd="([^"]+)"', lambda mm: 'd="' + re.sub(r"(\d+\.\d{2})\d+", r"\1", mm.group(1)) + '"', s)
    s = re.sub(r"\s+\n", "\n", s)
    pathlib.Path(path).write_text(s)
    return dict(name=name, w=round(w), h=round(h), bytes=len(s.encode()))


def arrow(ax, p, q, color=TEAL, lw=2.2, ms=16, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, shrinkA=0, shrinkB=0))


def node(ax, x, y, label=None, r=0.11, dx=0, dy=0, color=MAROON, fontsize=15):
    ax.add_patch(Circle((x, y), r, facecolor=LIGHT, edgecolor=color, lw=2.2, zorder=5))
    if label is not None:
        ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, color=color, zorder=6, fontweight="bold")


def dim(ax, p, q, text, offset=0.0, side="below", color=INK, fontsize=16):
    """dimension line with ticks between p and q"""
    (x1, y1), (x2, y2) = p, q
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.2)
    ax.plot([x1, x1], [y1 - 0.06, y1 + 0.06] if y1 == y2 else [y1, y1], color=color, lw=1.2)
    if y1 == y2:
        ax.plot([x1, x1], [y1 - 0.06, y1 + 0.06], color=color, lw=1.2)
        ax.plot([x2, x2], [y2 - 0.06, y2 + 0.06], color=color, lw=1.2)
        ax.text((x1 + x2) / 2, y1 + (-0.14 if side == "below" else 0.14), text, ha="center",
                va="top" if side == "below" else "bottom", fontsize=fontsize, color=color)
    else:
        ax.plot([x1 - 0.06, x1 + 0.06], [y1, y1], color=color, lw=1.2)
        ax.plot([x2 - 0.06, x2 + 0.06], [y2, y2], color=color, lw=1.2)
        ax.text(x1 + (-0.14 if side == "left" else 0.14), (y1 + y2) / 2, text, ha="right" if side == "left" else "left",
                va="center", fontsize=fontsize, color=color, rotation=90)
