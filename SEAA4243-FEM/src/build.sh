#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Rebuild the SEAA 4243 site from src/: Explorers, code packs, part pages, course home, then Dr RJ.
# Needs Python 3 with numpy, matplotlib, beautifulsoup4 and lxml. Decks and slide PDFs: see src/README.md.
set -euo pipefail
cd "$(dirname "$0")"
(cd mj/labs && python3 build_labs.py)
cd tools
python3 build_code.py
for p in content_p*.py; do python3 build_part.py "${p%.py}"; done
python3 build_home.py
python3 sync_labs.py
cd ../..
python3 tools/add_tutor.py          # Dr RJ panel and tutor files, always after the page build
echo "built; check with: git diff --stat"
