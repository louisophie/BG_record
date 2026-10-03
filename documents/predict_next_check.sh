#!/bin/bash
# predict_next_check.sh — one informative check time per dose, not hourly.
# Uses compressed PK: R peak ~1.5-2.5h, I peak ~2-4h, H peak ~0.5-1.5h
# Usage: bash predict_next_check.sh "<HH:MM dose-time> <units+insulin> <currentBG>"
# Example: bash predict_next_check.sh "23:02 14I 152"
# Prints: the single most informative next-check time + what to do.

dose_time="$1"; units="$2"; cur="$3"
ut="${units//[0-9.]/}"   # insulin letter
un="${units//[^0-9.]/}" # units number

# parse dose time to epoch today
dt=$(date -d "today $dose_time" +%s 2>/dev/null || date -d "$dose_time" +%s)

case "$ut" in
  H|h) peak_min=60;  end_min=240 ;;  # Humalog fast
  R|r) peak_min=150; end_min=300 ;;  # Regular ~1.5-2.5h peak
  I|i) peak_min=180; end_min=420 ;;  # NPH compressed 2-4h peak, tail ~7h
  *)   peak_min=150; end_min=300 ;;
esac

echo "Dose: $un $ut at $dose_time (BG $cur)"
echo "-------------------------"
echo "Peak check:  $(date -d @$((dt+peak_min*60)) '+%H:%M')  (primary — the one that matters)"
echo "Tail check:  $(date -d @$((dt+end_min*60)) '+%H:%M')  (only if dose was large, >6u, or night)"

echo ""
echo "Rule (post-hypo day / <90 / no meal): test at PEAK only, skip tail."
echo "Night heavy-dose: test at peak + keep glucose bedside; skip until morning."