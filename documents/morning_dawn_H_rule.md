# Morning Dawn-Phenomenon H Rule — Dose Derivation 2026-09-21

*Source: bloodsugar.md Sept 2026 mornings · framework: Dr. Bernstein · personal compressed PK*

Rule: on waking, take fast insulin (H, or R if H unavailable) to cancel the dawn rise
and morning insulin resistance — never wake-and-wait.

## 1. Dawn rise rate (clean data)

- 09/13: 05:11 76 → 08:32 93, no insulin, fasting = **+17/3.4h ≈ +5/h**.
- Over the ~3h H action window the incoming rise is **+10–15**.

## 2. Morning-H empirical ISF ≈ 10–12 mg/dL/u (NOT the clean 40–45)

Morning resistance runs ~3–4× fasting-clean ISF:

| Morning | Dose | Landing | Per-unit |
|---|---|---|---|
| 09/07 (day-1 post-big-meal) | 7H @162 | 70 (−92/3.5h) | ~−13/u |
| 09/08 (day-2 post-big-meal) | 6H @168 | 112 (−56/3.8h) | ~−9.3/u |
| 09/10 | 5⁻H @132 (+7I mid-window) | 85 | confounded ✓ |
| 09/11 | 6H +8I @132 | 82 (−50/4h) | confounded ✓ |
| 09/15 | 2½H +8I @123 | 61 | over (I did most) |
| 09/20 | 3½H @168 (+NPH tail, rebound) | 144 (−24/4h) | rebound resisted |

Pure-H mornings center on **~−11/u** → use **10–12 mg/dL/u** for morning-H math.

## 3. Dose bands (H, wake BG, no active insulin, target ~85)

| Wake BG | H dose | Why |
|---|---|---|
| 70–100 | **1–2H** | already in target; cancels the incoming +10–15 dawn rise only |
| 100–120 | **2–3H** | −15–35 → ~85 |
| 120–150 | **4–5H** | −35–65 → ~85 |
| 150–180 | **6–7H** | −65–95 → ~85 |
| >180 | **(BG−85)/11, cap 8H** | e.g. 200 → 10 → cap 8H |

## 4. Modifiers

- **Post-hypo <24h (HAAF): halve every band** (44 was still biting at 23h on 09/19).
- **Clean fasting day (no carryover): lower end** of the band.
- **Carryover / rebound day (big-meal tail, Somogyi resolving): upper end** — the tail resists the drop (09/08 6H only −56 at −9.3/u).
- **R substitutes 1:1 when H unavailable** (HAAF ISF R ~50–60 ≈ H ~55–65, same scale) — but R peaks 1–3h, so shift the peak check later (`predict_next_check.sh`).
- Morning I (NPH basal for the day) is dosed **separately** per day-pattern/carryover — the bands above are the fast-insulin part only.
- Peak check at the H peak (~1h), tail per predictor. 鹽BC with the dose (food buffer).

## 5. Why not wait-and-see

Dawn rise is guaranteed (+5/h clean, more with carryover) and compounds hourly.
Waiting 2h at 130 → ~140, and the H window shifts into the daytime stack —
exactly how the midday crashes started (09/16, 09/17).
Correct on waking; the peak check (~1h) is the guardrail, not the decision point.
