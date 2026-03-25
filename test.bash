#!/bin/bash
export GREP_COLORS='ms=1;37;41'
cat -n bloodsugar.md | tac | awk '
  !seen["内"] && /内/      {print $0; seen["内"]=1}
  !seen["T"]  && /<T|>T/  {print $0; seen["T"]=1}
  !seen["A"]  && /<A|>A/  {print $0; seen["A"]=1}
  seen["内"] && seen["T"] && seen["A"] {exit}
'  | tac | egrep --color=always "((<|>)(内|T|A))"
