#!/bin/sh
# Compile tests/regression.tex twice with the package in ../, with XeLaTeX
# and LuaLaTeX, each as it is, with the fancy option and with the
# traditional option (which leaves out the data for simplified text), and
# compare each debug log with tests/regression.expected; then compile
# tests/pad-check.tex with both engines, which logs a FAIL for every
# character that loses its padding at a group end, and tests/lazy-check.tex
# and tests/simp-check.tex, whose debug logs are compared with
# tests/lazy-check.expected and tests/simp-check.expected.  Exit status 0
# means all is well.
cd "$(dirname "$0")" || exit 1
status=0
for engine in xelatex lualatex; do
  for opt in '' fancy traditional; do
    job=regression-$engine${opt:+-$opt}
    pre=${opt:+"\\PassOptionsToPackage{$opt}{xjyutping}"}
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
  job=pad-check-$engine
  TEXINPUTS=..: LUAINPUTS=..: max_print_line=10000 $engine \
    -interaction=nonstopmode -jobname "$job" pad-check.tex > /dev/null 2>&1
  if grep -q '^!' "$job.log"; then
    echo "$job: TeX errors:"; grep -A3 '^!' "$job.log"; status=1
  fi
  if grep -a '^pad-check: FAIL' "$job.log"; then
    status=1
  else
    echo "$job: padding ok"
  fi
  job=lazy-check-$engine
  TEXINPUTS=..: LUAINPUTS=..: max_print_line=10000 $engine \
    -interaction=nonstopmode -jobname "$job" lazy-check.tex > /dev/null 2>&1
  if grep -q '^!' "$job.log"; then
    echo "$job: TeX errors:"; grep -A3 '^!' "$job.log"; status=1
  fi
  grep -a '^xjyutping>' "$job.log" > "$job.readings"
  if grep -a '^lazy-check: FAIL' "$job.log" || ! diff -u lazy-check.expected "$job.readings"; then
    status=1
  else
    echo "$job: lazy sounds ok"
  fi
  job=simp-check-$engine
  TEXINPUTS=..: LUAINPUTS=..: max_print_line=10000 $engine \
    -interaction=nonstopmode -jobname "$job" simp-check.tex > /dev/null 2>&1
  if grep -q '^!' "$job.log"; then
    echo "$job: TeX errors:"; grep -A3 '^!' "$job.log"; status=1
  fi
  grep -a '^xjyutping>' "$job.log" > "$job.readings"
  if diff -u simp-check.expected "$job.readings"; then
    echo "$job: simplified input ok"
  else
    status=1
  fi
done
exit $status
