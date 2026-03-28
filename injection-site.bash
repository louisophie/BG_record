#!/bin/bash
export GREP_COLORS='ms=1;37;41'
cat -n bloodsugar.md | tac | awk '
  /####/      && ++c <= 3   { print }
  /内/        && ++d <= 1   { print; }
  /<T|>T/     && ++e <= 1   { print; }
  /<A|>A/     && ++f <= 1   { print; }
  /<B|>B/     && ++g <= 1   { print; }

  c >= 3 && d >= 2 && e >= 1 && f >= 1 && g >= 1 { exit }
' | tac | perl -pne 's/^ +(\d+)\t/ $1 /;s/    - //;' | grep -E --color=always "((<|>)(内|T|A|B))|####"
