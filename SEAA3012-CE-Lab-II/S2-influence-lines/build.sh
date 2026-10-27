#!/bin/bash
# Build the Lab S2 teaching package (XeLaTeX). Run from this folder.
set -e
cd "$(dirname "$0")"
python3 shared/s2_numbers.py > /dev/null          # reference numbers -> shared/s2_numbers.json
( cd notes     && xelatex -interaction=nonstopmode s2_lecture_notes.tex >/dev/null && xelatex -interaction=nonstopmode s2_lecture_notes.tex >/dev/null )
( cd exercises && xelatex -interaction=nonstopmode -jobname=s2_exercises_student s2_exercises.tex >/dev/null \
               && xelatex -interaction=nonstopmode -jobname=s2_exercises_key "\def\showkey{1}\input{s2_exercises.tex}" >/dev/null )
( cd slides    && xelatex -interaction=nonstopmode s2_slides.tex >/dev/null && xelatex -interaction=nonstopmode s2_slides.tex >/dev/null )
( cd activity  && xelatex -interaction=nonstopmode s2_activity_sheet.tex >/dev/null )
python3 web/build_web.py                          # course page -> index.html and activity/influence-line-explorer.html
mkdir -p pdf
cp notes/s2_lecture_notes.pdf exercises/s2_exercises_student.pdf exercises/s2_exercises_key.pdf slides/s2_slides.pdf activity/s2_activity_sheet.pdf pdf/
echo "built: pdf/s2_lecture_notes.pdf  pdf/s2_slides.pdf  pdf/s2_exercises_student.pdf  pdf/s2_exercises_key.pdf  pdf/s2_activity_sheet.pdf"
