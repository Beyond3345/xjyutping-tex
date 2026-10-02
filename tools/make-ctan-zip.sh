#!/bin/sh
# make-ctan-zip.sh [OUT]: build the archive to upload to CTAN (default
# ../xjyutping.zip, next to this repository).  It holds one folder,
# xjyutping/, with the package, its data, the manual (source and PDF),
# README, LICENSE, CHANGELOG, tools/ and tests/, and nothing else: no build
# files, no .DS_Store.  Files are 644, folders and scripts 755.
set -e
cd "$(dirname "$0")/.."
out=${1:-../xjyutping.zip}
case $out in /*) ;; *) out=$(pwd)/$out ;; esac

# the version must be the same everywhere (see CHANGELOG.md)
v=$(sed -n 's/^\\ProvidesExplPackage{xjyutping}{[^}]*}{\([^}]*\)}.*/\1/p' xjyutping.sty)
for f in xjyutping-chars.def xjyutping-words.def README.md xjyutping-doc.tex tools/build-data.py; do
  grep -q "$v" "$f" || { echo "$f does not mention version $v" >&2; exit 1; }
done
[ xjyutping-doc.pdf -nt xjyutping-doc.tex ] ||
  echo "warning: xjyutping-doc.pdf is older than xjyutping-doc.tex" >&2

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
d=$tmp/xjyutping
mkdir -p "$d/tools" "$d/tests"
cp README.md LICENSE CHANGELOG.md xjyutping.sty xjyutping.lua \
  xjyutping-chars.def xjyutping-words.def xjyutping-doc.tex xjyutping-doc.pdf "$d/"
cp tools/build-data.py tools/fetch-sources.sh tools/make-ctan-zip.sh \
  tools/wenetspeech-yue-counts.tsv "$d/tools/"
cp tests/run-tests.sh tests/render.sh tests/regression.tex tests/regression.expected \
  tests/layout-check.tex tests/fancy-check.tex tests/verse-check.tex "$d/tests/"
find "$d" -type d -exec chmod 755 {} +
find "$d" -type f -exec chmod 644 {} +
chmod 755 "$d"/tools/*.sh "$d"/tools/*.py "$d"/tests/*.sh
rm -f "$out"
(cd "$tmp" && zip -qrX "$out" xjyutping)
echo "$out (version $v)"
