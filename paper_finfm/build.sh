#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
out="${1:-../plans/paper-build}"
mkdir -p "$out"
out="$(realpath "$out")"
source_dir="$PWD"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$out" main.tex
(
  cd "$out"
  BIBINPUTS="$source_dir:" BSTINPUTS="$source_dir:" bibtex main
)
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$out" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$out" main.tex
if rg -q 'undefined references|Citation .* undefined|Overfull' "$out/main.log"; then
  echo "Resolve reference or layout warnings in $out/main.log" >&2
  exit 1
fi
echo "PDF: $out/main.pdf"
