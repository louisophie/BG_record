#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract nightly features from bloodsugar.md (Bernstein-style free-text log)
to test: does pre-bed R correlate with next-morning refreshment?

Outputs (in ./analysis/):
  nights.csv        - one row per night
  unparsed.txt      - lines worth manual review
Run from repo root:  python3 analysis/extract_bg.py
"""
import re, csv, sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "bloodsugar.md"
OUT = ROOT / "analysis"
OUT.mkdir(exist_ok=True)

SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
       "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}
FRAC = {"½": .5, "¼": .25, "¾": .75}

def sup(s):
    return "".join(SUP.get(c, c) for c in s)

def num(tok):
    """'6' '6½' '½' '2.5' -> float ; None if empty"""
    tok = tok.strip()
    if not tok:
        return None
    v = 0.0
    m = re.match(r"^(\d+(?:\.\d+)?)", tok)
    if m:
        v += float(m.group(1))
        rest = tok[m.end():]
    else:
        rest = tok
    for c in rest:
        if c in FRAC:
            v += FRAC[c]
    return v if v > 0 else None

DATE_RE = re.compile(r"^#{3,4}\s*(\d{8})")
ENTRY_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])?\s*(\d{1,2}):(\d{2})(?!\d)")
BG_RE = re.compile(r"(\d{1,3})\s*mg/dL")
BRA_RE = re.compile(r"\{([^{}]*)\}")
CMT_RE = re.compile(r"<!--(.*?)-->", re.S)
SLEEP_RE = re.compile(r"〘睡([^〙]*)〙")
IN_TIME_RE = re.compile(r"^\s*(\d{1,2})\s*[:：]\s*(\d{2}|[⁰¹²³⁴⁵⁶⁷⁸⁹]{1,2})\s*[:：]?\s+(.*)$")
COMB_RE = re.compile(
    r"\((\d+)\s*\+\s*(\d+)\)\s*([½¼¾]?)[^A-Za-z0-9]{0,3}(II|I|T|R|H|N)\b")
# token grammar: [num][frac][mods] DRUG   e.g. '6R' '3⁺R' '2½I' '3½⁺R'
#               or [frac][mods] DRUG      e.g. '½⁻I' '½+T'
UNIT_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)?([½¼¾])?([⁺⁻+\-]*)\s*(II|I|T|R|H|N)(?![A-Za-z])")

def resolve_dt(cur_date, hh, mm, last_dt):
    """anchor hh:mm to cur_date; if that looks like going backwards
    vs last seen entry (crossing midnight), roll forward one day."""
    cand = cur_date.replace(hour=hh % 24, minute=mm)
    if last_dt and cand < last_dt - timedelta(hours=4):
        cand += timedelta(days=1)
    return cand

NEG_KW = ["不舒服", "累", "疲", "tired", "exhaust", "miserable", "unpleasant",
          "violent", "weak", "very bad", "腦霧", "霧", "頭暈", "dizzy", "foggy",
          "unrefresh", "睡不飽"]
POS_KW = ["much better", "way better", "feel better", "睡飽", "清爽", "精神",
          "尚可", "good"]

records = []      # dicts: dt, bg, insulins[(time,drug,units,approx)], sleep_tags, comments
cur_date = None
last_dt = None
unparsed = []

for raw in SRC.read_text(encoding="utf-8").splitlines():
    line = raw.rstrip()
    if not line.strip():
        continue
    m = DATE_RE.match(line)
    if m:
        cur_date = datetime.strptime(m.group(1), "%Y%m%d")
        continue
    if cur_date is None:
        continue

    comments = "; ".join(x.strip() for x in CMT.findall(line)) if False else \
               "; ".join(x.strip() for x in CMT_RE.findall(line))
    work = CMT_RE.sub(" ", line)

    # entry leading time?
    em = ENTRY_RE.match(work)
    if em:
        last_dt = resolve_dt(cur_date, int(em.group(1)), int(em.group(2)), last_dt)

    # BG value?
    bgm = BG_RE.search(work)
    bg = int(bgm.group(1)) if bgm else None

    # sleep tags (search original incl. comments)
    sleeps = SLEEP_RE.findall(line)

    # insulin blocks
    insulins = []
    for blk in BRA_RE.findall(work):
        body = blk
        t_here = None
        im = IN_TIME_RE.match(body)
        if im:
            t_here = resolve_dt(cur_date, int(im.group(1)) % 24,
                                int(sup(im.group(2))), last_dt)
            body = im.group(3)
        for part in re.split(r"[,，]", body):
            part = part.strip()
            if not part:
                continue
            cm = COMB_RE.search(part)
            if cm:
                u = float(cm.group(1)) + float(cm.group(2))
                if cm.group(3):
                    u += FRAC.get(cm.group(3), 0)
                insulins.append((t_here or last_dt, cm.group(4), u, False))
                continue
            matched_any = False
            pos = 0
            while True:
                um = UNIT_RE.search(part, pos)
                if not um:
                    break
                num_s, frac_c, mods, drug = um.groups()
                if not (num_s or frac_c or mods):     # bare letter = site junk
                    pos = um.end()
                    continue
                matched_any = True
                approx = bool(mods)
                u = (float(num_s.replace(",", ".")) if num_s else 0.0) \
                    + FRAC.get(frac_c or "", 0)
                insulins.append((t_here or last_dt, drug, u, approx))
                pos = um.end()
            if not matched_any:
                bm = re.match(r"^(\d+(?:[.,]\d+)?[½¼¾]?|[½¼¾])\s*[⁺⁻+\-]*\s*[<>]", part)
                if bm:                                # bare '2½>B' -> default R
                    u = num(bm.group(1)) or 0
                    if u:
                        insulins.append((t_here or last_dt, "R", u, True))
                        matched_any = True
            if not matched_any and re.match(r"^\d", part):
                unparsed.append(f"{line}   ## token? '{part}'")

    if bg is not None or insulins or sleeps or comments:
        records.append({
            "dt": last_dt,
            "bg": bg,
            "insulins": insulins,
            "sleeps": len(sleeps),
            "comment": comments,
        })

# ---------------- group into nights ----------------
def dnum(dt):
    return dt.date() if dt else None

dates = sorted({d for r in records if (d := dnum(r["dt"]))})
nights = []
for i in range(len(dates) - 1):
    D = dates[i]
    nxt = dates[i + 1]
    win_lo = datetime.combine(D, datetime.min.time()) + timedelta(hours=17)
    win_hi = datetime.combine(nxt, datetime.min.time()) + timedelta(hours=11, minutes=59)

    def in_win(r):
        return r["dt"] and win_lo <= r["dt"] <= win_hi

    recs = [r for r in records if in_win(r)]
    if not recs:
        continue

    bed_end = datetime.combine(nxt, datetime.min.time()) + timedelta(hours=3)
    dinner_cut = datetime.combine(D, datetime.min.time()) \
        + timedelta(hours=20, minutes=30)
    expo_end = datetime.combine(nxt, datetime.min.time()) + timedelta(hours=2)
    rescue_end = datetime.combine(nxt, datetime.min.time()) \
        + timedelta(hours=5, minutes=59)

    pre = [r for r in records
           if r["dt"] and win_lo <= r["dt"] <= bed_end]

    def units(drug, lo=None, hi=None):
        tot = unc = 0.0
        for r in pre:
            for (t, dg, u, ap) in r["insulins"]:
                if t and dg == drug and (lo is None or t >= lo) \
                        and (hi is None or t <= hi):
                    tot += u
                    unc += u if ap else 0
        return round(tot, 2), round(unc, 2)

    evening_R, _ = units("R", lo=win_lo, hi=dinner_cut)   # dinner bolus
    prebed_R, R_unc = units("R", lo=dinner_cut, hi=expo_end)
    prebed_H, _ = units("H", lo=dinner_cut, hi=expo_end)
    prebed_I, _ = units("I", lo=dinner_cut, hi=expo_end)
    basal_T, T_unc = units("T")
    rescue_R, _ = units("R", lo=expo_end, hi=rescue_end)
    rescue_H, _ = units("H", lo=expo_end, hi=rescue_end)
    rescue_RH = round(rescue_R + rescue_H, 2)

    pre_bgs = [(r["dt"], r["bg"]) for r in pre if r["bg"]]
    bedtime_bg, prev_bg = None, None
    if pre_bgs:
        bedtime_bg = pre_bgs[-1][1]
        if len(pre_bgs) >= 2:
            prev_bg = pre_bgs[-2][1]

    # overnight/morning outcomes
    am_recs = [r for r in recs if r["dt"] and r["dt"].date() == nxt]
    am_bgs = [(r["dt"], r["bg"]) for r in am_recs if r["bg"]
              and r["dt"].hour >= 3]
    morning_t, morning_bg = am_bgs[0] if am_bgs else (None, None)

    night_readings = [(r["dt"], r["bg"]) for r in recs if r["bg"]
                      and (r["dt"].hour >= 21 or r["dt"].hour <= 7)]
    lo70 = any(b < 70 for _, b in night_readings)
    lo54 = any(b < 54 for _, b in night_readings)

    gbts = sum(r["sleeps"] for r in recs
               if r["dt"] and (datetime.combine(D, datetime.min.time())
                               + timedelta(hours=21)) <= r["dt"] <= win_hi)

    LEGEND_RE = re.compile(r"=[^;|~]*(left|right|thumb|finger|nail|buttock|belly|arm|units|coffee powder)", re.I)
    cmts = [r["comment"] for r in records
            if r["comment"] and in_win(r) and not LEGEND_RE.search(r["comment"])]
    joined = " | ".join(cmts).lower()
    neg = any(k.lower() in joined for k in NEG_KW)
    pos = any(k.lower() in joined for k in POS_KW)

    # eating-load proxies (bolus units logged on day D and D-1, calendar basis)
    def bolus_on(day):
        tot = 0.0
        for r in records:
            if dnum(r["dt"]) == day:
                for (t, dg, u, ap) in r["insulins"]:
                    if dg in ("R", "H", "N"):
                        tot += u
        return round(tot, 2)

    bolus_today = bolus_on(D)
    bolus_yest = bolus_on(D - timedelta(days=1))

    nights.append(dict(
        night=str(D), prebed_R=prebed_R, R_uncertain=R_unc,
        evening_R=evening_R, prebed_H=prebed_H, prebed_I=prebed_I,
        basal_T=basal_T, T_uncertain=T_unc, rescue_RH=rescue_RH,
        bedtime_bg=bedtime_bg, prev_bg=prev_bg,
        morning_bg=morning_bg, morning_time=morning_t.strftime("%H:%M") if morning_t else "",
        noct_low70=int(lo70), noct_low54=int(lo54),
        gbts=gbts, subj_neg=int(neg), subj_pos=int(pos),
        bolus_today=bolus_today, bolus_yesterday=bolus_yest,
        comments=" ~ ".join(cmts)[:300],
    ))

cols = ["night", "prebed_R", "R_uncertain", "evening_R", "prebed_H",
        "prebed_I", "basal_T", "T_uncertain", "rescue_RH",
        "bedtime_bg", "prev_bg", "morning_bg", "morning_time",
        "noct_low70", "noct_low54", "gbts", "subj_neg", "subj_pos",
        "bolus_today", "bolus_yesterday", "comments"]

with open(OUT / "nights.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(nights)

(OUT / "unparsed.txt").write_text("\n".join(unparsed), encoding="utf-8")
print(f"records={len(records)}  nights={len(nights)}  unparsed_lines={len(unparsed)}")
print(f"wrote {OUT/'nights.csv'}")
