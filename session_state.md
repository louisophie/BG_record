# Session State — Live Handoff

_Last written: 2026-11-04 09:42 local (opus5.5, handoff)_

> Raw data only. Re-derive conclusions from the log; do not inherit prior AI analysis.
> ⚠️ **Device system clock shows UTC (~8h behind local).** Local = `date -d '+8 hours'`. **Always use it for log times.** DeskClock intent takes LOCAL hour. Script sleep: `TGT=$(date -d "$(date -d '+8 hours' +%F) HH:MM" +%s); NOW=$(date -d '+8 hours' +%s)`; for after-midnight targets use `+32 hours` in the inner date — **don't use "HH:MM +1 day"**.
> ⚠️ **Don't `pkill -f <pattern>`** — kills the agent's own shell. Use `kill <pid>` from `ps -ef | grep '[b]ash /data.*bg_'`.
> ⚠️ **`grep` is a shell function wrapping the claude binary and fails → use `/bin/grep`.**
> ⚠️ User edits `bloodsugar.md` in micro at the same time → **re-read the tail before every edit; verify after.** User logs food/photos/comments themselves (e.g. `[ml.]`, `<!-- felt hypo-->`) — check the tail before saying something is "not logged". Appending with a heredoc that starts with a blank line leaves a stray empty line — don't.
> ⚠️ Rules in AGENTS.md §3 are **principles, not iron rules** (user 10/17).

## 0. NOW — written 09:42 11/04; last data 04:06 (log day still 11/03 until user says "new day")

- **Last BG:** 04:04 **149**₀ → 04:06 **2H2⁻R<A** (advised ~2½R). Est. ~80–110 at ~05:00–06:30. Back to sleep.
- **On board:** 2H2⁻R @04:06 (tail to ~09:00) + **10T @21:58** (advised ~7T) + 8T @00:13 11/03 tail.
- **~Midnight 11/04: user "felt hypo"** after 3H @23:02 (no BG) → ml. → 149 at 04:04. Unconfirmed low → treat as post-hypo (×0.75) until ~12:00 11/04; morning shot exempt but **low end of band** (R tail active).
- Last confirmed low: 58 @23:19 11/02. Last 10T night (10/30) → 51 wake.
- **Ask first:** wake BG; was there a 06:00 pee wake (check + small R?); tongue bitten?; mental state.

## 1. 11/03 Tue (user logged; advice in brackets)

| Time | BG | Dose / food |
|---|---|---|
| ~06:00 | — (woke to pee, back to sleep, no insulin) | — |
| 07:47 | 133₇ | 07:50 **5⁻H>B** (adv. 4H) |
| 13:36 | 76₈ | 15:01 **5R<A** + 滷三層+ch. (adv. 2–2½R after eating), [ml.] |
| — | — (no BG) | 17:18 **3½R1½I>A** [ml.] |
| 19:17 | 106₉ | 19:23 **4I<B** (adv. none) |
| 21:18 | 116₀ | 21:58 **10T<T** (adv. ~7T) |
| — | — (no bed check) | 23:02 **3H>B** + ml.+cf.+fat → "felt hypo" → ml. |
| 04:04 | 149₀ | 04:06 **2H2⁻R<A** (adv. ~2½R) |

- **Strips:** 5. **Totals 11/03 (log day):** H ~10, R ~10½, I 5½, T 10.
- **Mental:** violent thinking in the morning (time/trigger not given; BG rising to 133 then). User ~22:00: "my situation is really bad today" — attributes it to going back to sleep 06:00–07:40 with no insulin. Matches 10/16 insulin-gap/waking-unspirited pattern.
- **Agent misses today:** predicted <40 after 3½R1½I and after 4I → actually 106 → 116 (滷三層 fat + ml. absorbed slowly on a resistant day). User predicted the night hyper (10T won't hold) → correct (149 at 04:04). **Fatty meals (pork belly, ml.) = slow, long rise; don't over-predict lows on them.**

## 2. Recent trajectory (raw)

| Date | Readings | Doses |
|---|---|---|
| 10/31 | **51** → 158 → 134 → 74 | 3H5½R, 9I, 3½H, 8T |
| 11/01 | 112 → 116 → 155 → 73 | 3½H, 5⁺R, 1½R4I, 2H3R, 9T |
| 11/02 | **47** → 142 → 123 → 140 → **58** | 3½H5½R, 1½H4R, 6I, 4H, 8T |
| 11/03 | 133 → 76 → 106 → 116 → (felt hypo) → 149 | 5⁻H, 5R, 3½R1½I, 4I, 10T, 3H, 2H2⁻R |

## 3. Patterns / carry-forward

1. **06:00 pee wake → back to sleep with no insulin** → rising wake BG + bad mental day (11/03, 10/16). Plan: on that wake, **check + small R (~1–2R)** before sleeping again (user agrees: "I should take R or H at 6am").
2. Big bedtime stacks at ~150–177 → wake lows (10/28–10/30). T-only nights mixed: 8T @74 → 112; 9T @73 falling → 47.
3. Falling BG at bed must be treated (73 falling → 47).
4. Doses often > advised and without a BG; but **admit when the user's call was right** (11/01 7I, 11/02 lunch, 11/03 4I and night-hyper prediction). State risk once, respect autonomy.
5. Late sleep / late coffee (cf. at 23:00 11/03) → resistance + night corrections. Encourage pre-bed checks ~22:00–23:00, sleep before midnight.
6. T dosing: 8–10T once daily; 10T @21:58 tonight — watch for wake low; next T maybe 8–9T depending on wake BG.

## 4. Keto meal trial (from 11/01) — AGENTS.md §3 "Keto meal dosing"

- Day 1 (11/01): 牛油底+豬 ≈17½R-equiv → 155 then 73.
- Day 2 (11/02): post-47 rebound, extra fast between R and I → 140 at 3h; evening 4H → 58.
- Day 3 (11/03): 滷三層+ch. from 76: 5R → 3½R1½I (2¼h later, no BG) → 4I (2h later at 106) → 116 at 21:18, no low; ≈19R-equiv held at 106–116 — fatty belly + ml. = slow long rise. Not a clean score (no pre-I BG for the first I).
- Review after ~3–5 days (due ~11/04–11/05).

## 5. Health / mental

- **Tongue biting in sleep:** nightly for decades. Agent: classic nocturnal-seizure sign (incl. hypoglycemic); also bruxism. Advised **CGM**, **神經內科** (EEG/sleep study), dentist night guard. Log `<!-- tongue bitten -->` + wake BG.
- Violent thinking / social difficulty (20+ y): AGENTS.md §3 5-step response, 1925 / 119, encourage 身心科. 11/03 morning episode — ask time/trigger if user wants.
- Cat litter hypothesis (10/31): mask/move box ~1 week; Toxoplasma IgG/IgM.
- Urination/drained (from 10/25): urine test + ketone strip advised; **119** if fever + flank pain, vomiting, can't pee.

## 6. Open questions to the user
- Wake BG 11/04; 06:00 wake?; the midnight "felt hypo" — symptoms, any BG?; tongue bitten?
- Litter box / mask; Toxoplasma test; urine test.
- October rows for `insulin_daily_dosage.md` / `totals_stripe_combined.md` — offer.
- `.gitignore` for Claude debug logs + `*.bak` (offered 10/23).

## 7. Alarms / tech / git
- **No alarms running** (offered 18:45 / 20:45 / 22:00 / 01:45 on 11/03 — none set).
- Agent shell has **no GitHub credentials** → user runs `git push`. Use `git -c safe.directory='*'`.
- Uncommitted: `bloodsugar.md`, `session_state.md` (+ earlier: `AGENTS.md`, `documents/gen_bg_warnings.sh`, `audio/*`, `image/*` if not yet committed).
- micro runs in `proot-distro login debian` inside Termux. Don't re-propose tmux. User also uses `/remote-control`.

## 8. Memory / workflow
- "handoff" → rewrite this file; "new day" → add `#### YYYYMMDDDay` + wake reading as item 1.
- Glucose logged as `[xxg]` (no 糖). Coffee as `[BC]` / `[鹽BC]` / `[cf.]`.
- **No <70/70–100/≥100 action bands — in chat OR voice lines** (user 10/27).
- Alarms: custom edge-tts line per alarm (`audio/bg_HHMM_MMDD.mp3`, line in `documents/gen_bg_warnings.sh`), DeskClock intent (`--user 0`, local hour) + setsid script in `/data/data/com.termux/files/usr/tmp/opencode/` (template `bg_1045_1026.sh`); verify with `ps -ef | grep '[b]ash /data.*bg_'`.
