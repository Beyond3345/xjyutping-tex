#!/bin/sh
# Compile tests/regression.tex twice with the package in ../, with XeLaTeX
# and LuaLaTeX, each as it is and with the fancy option, and compare each
# debug log with tests/regression.expected.  Exit status 0 means all is well.
cd "$(dirname "$0")" || exit 1
status=0
for engine in xelatex lualatex; do
  for fancy in '' fancy; do
    job=regression-$engine${fancy:+-$fancy}
    pre=${fancy:+'\PassOptionsToPackage{fancy}{xjyutping}'}
    for i in 1 2; do
      TEXINPUTS=..: LUAINPUTS=..: max_print_line=10000 $engine \
        -interaction=nonstopmode -jobname "$job" "$pre\\input{regression}" \
        > /dev/null 2>&1
    done
    if grep -q '^!' "$job.log"; then
      echo "$job: TeX errors:"; grep -A3 '^!' "$job.log"; status=1
    fi
    grep -a '^xjyutping>' "$job.log" > "$job.readings"
    if diff -u regression.expected "$job.readings"; then
      echo "$job: readings ok"
    else
      status=1
    fi
  done
done
exit $status
