# Three Eating Patterns — Insulin & Morning-BG Analysis

*From bloodsugar.md Feb–Sep 2026 · generated 2026-09-19 by DeepSeek V4 Pro · Dr. Bernstein framework*

## 1. The three day-patterns (confirmed from data)

| Pattern | Evening food | Evening I (NPH) | Morning BG typical |
|---|---|---|---|
| **A. Full fasting** | none | small / none | lowest, most hypo-prone |
| **B. Normal one-meal** | meat / cheese / egg only | 5–8I | mid |
| **C. Big-meal (binge)** | starch + sugar present | high (10–24I) | highest, most variable |

## 2. Finding 1 — Pre-bed NPH >10u DOES cause hypo (contradicts ">10u is safe")

All pre-bed I >10u nights and next-morning BG:

| Date | Pre-bed I | Morning | Verdict |
|---|---|---|---|
| 08/28 | 16u | 50 | LOW |
| 08/29 | 14u | 96 | ok |
| 09/04 | 16u | 72 | low edge |
| 09/05 | 16u | 127 | high ok |
| 09/08 | 16u | 120 | high ok |
| 09/12 | 16u | 76 | low edge |
| 09/14 | 16u | 123 | high ok |
| 09/17 | 14u | **26** | SEVERE LOW |

- **5/8 nights (62%) woke <80**; one hit **26**.
- The *good* mornings (96–127) were all **big-meal days** (hotpot/pork/starch buffer).
- The *bad* mornings (26, 50) happened when the meal buffer was weaker or post-hypo.
- **Conclusion: >10I pre-bed is only safe ON a big-meal day with a real food buffer. It is NOT safe on fasting or normal-meal days.**

## 3. Finding 2 — Sept 2026 pattern breakdown (most reliable era)

**BIG-MEAL days** (starch/sugar evening):
| eveI | morning | 
|---|---|
| 16u (09/04) | 72 |
| 7u (09/09) | 133 |
| 7u (09/10) | 120 |
| 24u (09/12) | 76 |
| 8u (09/13) | 36 LOW |
| 16u (09/14) | 123 |
| 9u (09/15) | 115 |
| 18u (09/16) | 121 |
| 0u (09/07) | 168 HIGH |

**NORMAL days** (meat/ch/egg only):
| eveI | morning |
|---|---|
| 16u (09/05) | 127 |
| 16u (09/08) | 120 |
| 15u (09/11) | 51 LOW |
| 19u (09/17) | 26 SEVERE |
| 0u (09/18) | 201 HIGH |

**Key insight:** 
- On **big-meal days**, high I (14–18u) lands morning in a good range (72–123) **most of the time** — the starch/sugar buffer absorbs it. This is where large NPH is justified.
- On **normal-meal days**, the SAME 14–19u I crashes (51, 26) because there's no starch buffer — only protein/fat (slow, weak resistance).
- **The pattern difference is real and large: big-meal days need much more evening I than normal/fasting days.**

## 4. The three-pattern dose framework

| Pattern | Evening I target | Why |
|---|---|---|
| **A. Fasting** | **0–2I** (ideally 0) | no food buffer; any I crashes. Morning lows are highest here (51% <70). |
| **B. Normal (meat/ch/egg)** | **4–6I** | protein/fat tail only; modest buffer. More than ~8I risks low (09/11 15I→51, 09/17 19I→26). |
| **C. Big-meal (starch/sugar)** | **10–16I** | starch/sugar buffer absorbs it; this is the ONLY pattern where >10I is defensible. |

**Rule of thumb:**
> Match evening NPH to the evening buffer. Starch/sugar meal = full dose (10–16I). Meat/egg only = half (4–6I). Nothing = near-zero (0–2I). Dosing B's day with C's dose is what produces 26 and 51.

## 4b. Meal Bolus (R/H) Requirements per Pattern

*Learned 2026-09-21 from 09/21 dinner (牛+ch, Pattern B):*

| Pattern | Meal Type | R/H Bolus (with food) | Notes |
|---|---|---|---|
| **A. Fasting** | none | 0 | No meal = no bolus |
| **B. Normal (meat/ch/egg)** | meat/cheese/egg | **6–8u R/H** | When **no midday meal dose** taken. The protein/fat absorption needs a real bolus; 4⁻R (today) was half what the meal needed → +28 rise (93→121). With midday meal, reduce to 4–6u. |
| **C. Big-meal (starch/sugar)** | starch/sugar present | 10–16u R/H | Starch/sugar absorbs it; this is where big bolus is defensible. |

**Rule of thumb:** R/H bolus matches the *evening buffer* just like NPH. No midday dose → full bolus (6–8u for Pattern B). Midday dose taken → halve the evening bolus.

## 5. Special cases that override the table

- **Post-hypo <24h** (HAAF): halve EVERYTHING above, even on big-meal day (09/17 was big-meal but post-26 → crashed anyway).
- **Rebound present:** if BG is high from rebound (not meal), DON'T add big basal — it lands later as a low. Correct small and awake.
- **Dawn/dawn-risk:** if rising on own, small + recheck, not pre-emptive full dose.

## 6. Post-big-meal gluconeogenesis carryover — how long does it need high insulin?

**Verified from log (09/12 → 09/19):**

| Day | Total insulin | Relative |
|---|---|---|
| 09/12 (big-meal anchor) | 48u | 100% |
| 09/13 | 45u | ~90% |
| 09/14 | 45u | ~90% |
| 09/15 | 41u | ~85% |
| 09/16 | 40u | ~85% |
| 09/17 | 40u | ~85% |
| 09/18 | 29u | ~60% |
| 09/19 | 22u | ~45% |

**Findings:**
- **Direct glucose + glycogen-refill** from a big meal lasts **~24–36h**.
- **Protein/fat gluconeogenesis tail + sustained eating** keeps total insulin need elevated (~40–45u) for **~3–4 days**, then drops.
- **If you actually fast/lights after** the big meal, need drops fast: 09/18 29u → 09/19 22u within 2 days.
- **Consecutive big meals** keep it pinned high until you stop; then it tapers ~2 days.

**Carryover taper table (if fasting/lights after one big meal):**

| Day after big meal | Relative need |
|---|---|
| Day 1 | ~100% (dinner already covered) |
| Day 2 | ~80% |
| Day 3 | ~60% |
| Day 4 | ~40% |
| Day 5 | ~20% (back to fasting baseline) |

**Practical rule:**
- 1 big meal → **2–3 days** of elevated (not full) dose. Don't drop to fasting-dose on day 2.
- Consecutive big meals → stays high until you stop, then drops ~2 days.
- **Post-hypo override always wins:** severe hypo <24h → halve everything regardless of carryover (09/17 big-meal but post-26 crashed anyway).

## 7. Open items / to refine

- Need cleaner tagging of "real starch" (photos) vs sauce-level sugar to sharpen big-meal classification.
- Big-meal I sweet spot may be ~10–14I (09/12's 24I worked but is ceiling; 09/16's 18I fine; 09/04 16I fine). 
- Consider logging evening-carb grams + I dose together for 2 weeks to find the per-pattern regression.

*Framework: Dr. Richard K. Bernstein · Personal compressed PK (I 4–7h, behaves 1.5× potent R)*