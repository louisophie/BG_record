#!/bin/bash
termux-wake-lock                    # keep Termux alive

while true; do
    clear                           # optional: clean screen
    perl ./bloodsugar_duration_v2.pl
#    echo "------------------- $(date '+%H:%M:%S') -------------------"
    sleep 60
done
