#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze nights.csv: does a pre-bed R shot change next-morning outcomes?
Pure-stdlib statistics; prints report sections used for prebed_R_report.md
"""
import csv, math
from pathlib import Path

CSV = Path(__file__).resolve().parent / "nights.csv"
rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
for r in rows:
    for k in ("prebed_R", "evening_R", "prebed_H", "prebed_I", "basal_T",
              "rescue_RH", "bedtime_bg", "prev_bg", "morning_bg",
              "bolus_today", "bolus_yesterday", "R_uncertain"):
        r[k] = float(r[k]) if r.get(k) else None
    for k in ("noct_low70", "noct_low54", "gbts", "subj_neg", "subj_pos"):
        r[k] = int(r[k]) if r.get(k) else 0

def f(v, nd=1):
    return "-" if v is None else f"{v:.{nd}f}"

def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None

def median(xs):
    xs = sorted(x for x in xs if x is not None)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

def pct(num, den):
    den = [x for x in den]  # truthiness-safe list
    d = len(den)
    return f"{100 * num / d:.0f}% (n={d})" if d else "—"

def spearman(pairs):
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    n = len(pairs)
    if n < 10:
        return None, n

    def rank(v):
        s = sorted(range(n), key=lambda i: pairs[i][v])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and pairs[s[j + 1]][v] == pairs[s[i]][v]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r

    ra, rb = rank(0), rank(1)
    ma, mb = mean(ra), mean(rb)
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra)
                    * sum((y - mb) ** 2 for y in rb))
    return (num / den if den else None), n

print("=" * 72)
print("A. DATASET OVERVIEW")
print("=" * 72)
n_all = len(rows)
both_bg = [r for r in rows if r["bedtime_bg"] and r["morning_bg"]]
with_r = [r for r in rows if (r["prebed_R"] or 0) > 0]
no_r = [r for r in rows if not (r["prebed_R"] or 0) > 0]
rescued = [r for r in rows if (r["rescue_RH"] or 0) > 0]
print(f"nights extracted: {n_all}")
print(f"  with bedtime+morning BG : {len(both_bg)}")
print(f"  pre-bed R nights        : {len(with_r)}")
print(f"  basal-only nights       : {len(no_r)}")
print(f"  nights needing 02-06h rescue bolus: {len(rescued)}")
unc = [r for r in rows if (r['R_uncertain'] or 0) > 0]
print(f"  nights w/ approx-dose R : {len(unc)}")

print()
print("=" * 72)
print("B. MAIN COMPARISON: pre-bed R vs basal-only  (all nights)")
print("=" * 72)
hdr = f"{'metric':34}{'R nights':>18}{'no-R nights':>18}"
print(hdr)

def line(label, g1, g2, fn):
    print(f"{label:34}{fn(g1):>18}{fn(g2):>18}")

line("morning BG mean", with_r, no_r,
     lambda g: f"{f(mean([r['morning_bg'] for g2_ in [g] for r in g]))} mg/dL")
line("morning BG median", with_r, no_r,
     lambda g: f"{f(median([r['morning_bg'] for r in g]))} mg/dL")
line("bedtime BG mean", with_r, no_r,
     lambda g: f"{f(mean([r['bedtime_bg'] for r in g]))} mg/dL")

def rate(key, thr=0):
    def f_(g):
        n_pos = sum(1 for r in g if r[key] > thr)
        return pct(n_pos, g)
    return f_

line("回籠覺 nights (gbts>0)", with_r, no_r, rate("gbts"))
line("subjective NEG mornings", with_r, no_r, rate("subj_neg"))
line("subjective POS mornings", with_r, no_r, rate("subj_pos"))
line("any reading <70 at night", with_r, no_r, rate("noct_low70"))
line("any reading <54 at night", with_r, no_r, rate("noct_low54"))

def stable(r):
    return (r["bedtime_bg"] and 70 <= r["bedtime_bg"] <= 140
            and not r["noct_low70"]
            and r["morning_bg"] and 70 <= r["morning_bg"] <= 150)

line("'clean' nights (see def.)", with_r, no_r,
     lambda g: pct(sum(1 for r in g if stable(r)), g))

print()
print("=" * 72)
print("C. STRATIFIED BY BEDTIME BG  (controls the confounder: you dose R")
print("   BECAUSE bedtime BG is high -> raw comparison above is biased)")
print("=" * 72)
bands = [("70-109", lambda b: b < 110),
         ("110-149", lambda b: 110 <= b < 150),
         ("150+", lambda b: b >= 150)]
for name, cond in bands:
    grp = [r for r in both_bg if r["bedtime_bg"] and cond(r["bedtime_bg"])]
    g_r = [r for r in grp if (r["prebed_R"] or 0) > 0]
    g_n = [r for r in grp if not (r['prebed_R'] or 0) > 0]
    print(f"\n--- bedtime {name}: total={len(grp)}  (R:{len(g_r)} / noR:{len(g_n)})")
    if g_r and g_n:
        print(f"    morning BG mean      : {f(mean([r['morning_bg'] for r in g_r]),0)}"
              f"  vs  {f(mean([r['morning_bg'] for r in g_n]),0)}")
        print(f"    回籠覺 rate           : "
              f"{pct(sum(r['gbts']>0 for r in g_r), g_r)}  vs  "
              f"{pct(sum(r['gbts']>0 for r in g_n), g_n)}")
        print(f"    subjective NEG rate  : "
              f"{pct(sum(r['subj_neg']>0 for r in g_r), g_r)}  vs  "
              f"{pct(sum(r['subj_neg']>0 for r in g_n), g_n)}")
        print(f"    nocturnal <70 rate   : "
              f"{pct(sum(r['noct_low70'] for r in g_r), g_r)}  vs  "
              f"{pct(sum(r['noct_low70'] for r in g_n), g_n)}")
        print(f"    'clean' night rate   : "
              f"{pct(sum(stable(r) for r in g_r), g_r)}  vs  "
              f"{pct(sum(stable(r) for r in g_n), g_n)}")

print()
print("=" * 72)
print("D. FASTING DEPTH (previous-day bolus as proxy)")
print("=" * 72)
for name, cond in [("deep fast (<8u prev-day)", lambda v: v < 8),
                   ("eating/mixed (>=8u)", lambda v: v >= 8)]:
    grp = [r for r in both_bg if r["bolus_yesterday"] is not None
           and cond(r["bolus_yesterday"])]
    g_r = [r for r in grp if (r["prebed_R"] or 0) > 0]
    g_n = [r for r in grp if not (r['prebed_R'] or 0) > 0]
    print(f"\n--- {name}: total={len(grp)} (R:{len(g_r)}/noR:{len(g_n)})")
    if g_r and g_n:
        print(f"    morning BG mean : {f(mean([r['morning_bg'] for r in g_r]),0)}"
              f" vs {f(mean([r['morning_bg'] for r in g_n]),0)}")
        print(f"    回籠覺 rate      : {pct(sum(r['gbts']>0 for r in g_r), g_r)}"
              f" vs {pct(sum(r['gbts']>0 for r in g_n), g_n)}")
        print(f"    NEG rate        : {pct(sum(r['subj_neg']>0 for r in g_r), g_r)}"
              f" vs {pct(sum(r['subj_neg']>0 for r in g_n), g_n)}")

print()
print("=" * 72)
print("E. CORRELATIONS (Spearman)")
print("=" * 72)
for label, key in [("prebed_R vs morning_BG", "prebed_R"),
                   ("bedtime_BG vs morning_BG", "bedtime_bg"),
                   ("basal_T vs morning_BG", "basal_T")]:
    rho, n = spearman([(r[key], r["morning_bg"]) for r in rows])
    print(f"{label:30} rho={f(rho,2)}  (n={n})")
rho, n = spearman([(r["prebed_R"], -(r["gbts"])) for r in rows])
print(f"{'prebed_R vs -回籠覺count':30} rho={f(rho,2)}  (n={n})")

print()
print("=" * 72)
print("F. RESCUE NIGHTS (02:00-06:00 correction bolus needed)")
print("=" * 72)
ok = [r for r in rescued if r["morning_bg"]]
if ok:
    print(f"n={len(rescued)} | morning BG mean: {f(mean([r['morning_bg'] for r in ok]),0)}"
          f" | 回籠覺: {pct(sum(r['gbts']>0 for r in rescued), rescued)}"
          f" | NEG: {pct(sum(r['subj_neg']>0 for r in rescued), rescued)}")
