#!/bin/sh
# Compile tests/regression.tex twice with the package in ../, once as it is
# and once with the fancy option, and compare each debug log with
# tests/regression.expected.  Exit status 0 means all is well.
cd "$(dirname "$0")" || exit 1
status=0
for job in regression regression-fancy; do
  pre=''
  [ "$job" = regression-fancy ] && pre='\PassOptionsToPackage{fancy}{xjyutping}'
  for i in 1 2; do
    TEXINPUTS=..: max_print_line=10000 xelatex -interaction=nonstopmode \
      -jobname "$job" "$pre\\input{regression}" > /dev/null 2>&1
  done
  if grep -q '^!' "$job.log"; then echo "$job: TeX errors:"; grep -A3 '^!' "$job.log"; status=1; fi
  grep -a '^xjyutping>' "$job.log" > "$job.readings"
  if diff -u regression.expected "$job.readings"; then echo "$job: readings ok"; else status=1; fi
done
exit $status
