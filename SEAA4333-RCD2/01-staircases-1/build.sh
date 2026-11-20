#!/bin/bash
# Build the SEAA 4333 Unit 1 page. Run from this folder: ./build.sh
#   web/build_page.py  web/src + ../shared/course.{css,js} -> index.html (equations as SVG, manifest generated)
#   web/add_tutor.py   Dr RJ guide panel -> index.html; tutor/ files for the rz-tutor Worker and the offline guide
# Occasional steps, run by hand when their sources change:
#   python3 web/make_figs.py <folder of PNG figures>     figures -> img/*.webp
#   python3 web/make_deck.py <claude.ai deck export>     Unit 1 deck -> slides/deck.html (no speaker notes)
#   python3 web/make_slides_pdf.py                       slides/deck.html -> pdf/staircases-1-slides.pdf
set -e
cd "$(dirname "$0")"
[ -d web/node_modules/mathjax-full ] || npm ci --prefix web --no-audit --no-fund
python3 web/build_page.py
python3 web/add_tutor.py
echo "built: index.html (open it through a local server, e.g. python3 -m http.server from My_Lectures/)"
