#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Convert the Unit 1 figures (PNG) to the WebP files the page and the slides use, in img/.

What: for every name in FIGS, reads <source folder>/<name>.png and writes img/<name>.webp, at most 1400 px
wide (enough for a sharp figure in a 700 px column on a high-density screen), quality 90; the QR code is
written lossless so that it stays scannable. Prints the size of each file.

How to call it, from this topic folder:
  python3 web/make_figs.py <folder with the PNG figures>

Why it is like this: one set of WebP figures serves the notes, the examples and the slide deck, so nothing is
stored twice. The PNG originals were drawn for this course in October 2026 (Workbook Ch. 1 and the Unit 1
deck on claude.ai); they are kept with the lecturer, not in this repository.
"""
import sys
from pathlib import Path

from PIL import Image

topic = Path(__file__).resolve().parent.parent
FIGS = ["anatomy", "hook", "section", "model_we11", "model_fe12", "elev_we11", "elev_fe12", "elev_s1", "elev_d1",
        "detail_we11", "detail_fe12", "detail_fe12_q", "kinkA", "kinkB", "kinkA_ans", "kinkB_ans", "qr_explorer"]
MAXW = 1400


def main(src: Path) -> int:
    out = topic / "img"
    out.mkdir(exist_ok=True)
    total = 0
    for name in FIGS:
        im = Image.open(src / f"{name}.png").convert("RGB")
        if name == "qr_explorer":
            im.save(out / f"{name}.webp", "WEBP", lossless=True, method=6)
        else:
            if im.width > MAXW:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            im.save(out / f"{name}.webp", "WEBP", quality=90, method=6)
        size = (out / f"{name}.webp").stat().st_size
        total += size
        print(f"img/{name}.webp  {im.width}×{im.height}  {size / 1024:.0f} kB")
    print(f"{len(FIGS)} figures, {total / 1024:.0f} kB")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
