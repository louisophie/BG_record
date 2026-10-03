# Strip-Reduction Protocol

*From BG log analysis 2026-09-18 · saves ~2 strips/day on calm days*

## Why it works

- 1088 readings over the log: **24% <70, 13% <54** — but the dangerous lows cluster almost entirely **night 22:00–08:00** (26, 30, 36, 40, 51, 59).
- Daytime fasting readings (09:00, 14:00, etc.) repeat the same pattern daily → low information.
- Only the **two pre-bed checks** and the **one peak check after a heavy dose** actually change a dose decision.

## Calm-day schedule (5.2 → 3/day)

| # | When | What it decides |
|---|------|-----------------|
| 1 | Pre-bed −2h | sets the evening R/I dose |
| 2 | At bed moment | trajectory (rising/falling) → final dose |
| 3 | Morning wake | carry-over state, morning correction |

## Heavy-dose night (add 1)

| # | When | What it decides |
|---|------|-----------------|
| 4 | Dose peak (see predictor) | catches the <54 danger window |

Only add #4 when a large/stacked dose ran (e.g. >6I, or I + bolus together). Otherwise skip straight to morning.

## The peak-check predictor

`documents/predict_next_check.sh`

```bash
bash predict_next_check.sh "<HH:MM dose-time>" "<units+insulin>" "<currentBG>"
```

- Uses compressed PK: H peak ~0.5–1.5h, R ~1.5–2.5h, **I ~2–4h** (your NPH).
- Prints the **one peak check** — test there, not hourly.
- Tail check only printed for large (>6u) or night doses.
- Validated: `14:11 4I → peak 17:11` (real crash 17:07); `23:02 14I → peak 02:02` (real hypo 02:36).

## Non-negotiables (do NOT strip these)

- **The 2 pre-bed checks** — they set the evening basal. Worst place to save strips.
- **Peak check on any heavy-dose night** — your 26/30/36/40 cluster all came from stacks; the peak is where a rescue matters.
- **Any symptom** (shake, sweat, confusion, "not right") overrides the schedule — check immediately.

## Rule of thumb

> Test at the **peak**, not the pattern. Daytime fasting trend is predictable; night stacks are not.