#!/bin/sh
# render.sh file.tex [dpi]: compile with the package in ../ and render every page to PNG
set -e
cd "$(dirname "$1")"
f=$(basename "$1" .tex)
TEXINPUTS=..: xelatex -interaction=nonstopmode -halt-on-error "$f.tex" > /dev/null 2>&1 || { grep -A8 '^!' "$f.log" | head -30; exit 1; }
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r${2:-200} -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -sOutputFile="$f-%d.png" "$f.pdf"
ls "$f"-*.png
