#!/bin/sh
# Build IEEE_ACCESS_FINAL.pdf with the official IEEE Access template files in ./ieeeaccess (template ACCESS_latex_template_20260513).
cd "$(dirname "$0")" || exit 1
export TEXINPUTS=./ieeeaccess//: TFMFONTS=./ieeeaccess//: T1FONTS=./ieeeaccess//: TEXFONTMAPS=./ieeeaccess//:
for i in 1 2 3; do pdflatex -interaction=nonstopmode IEEE_ACCESS_FINAL.tex >/dev/null || exit 1; done
rm -f IEEE_ACCESS_FINAL.aux IEEE_ACCESS_FINAL.log IEEE_ACCESS_FINAL.out
