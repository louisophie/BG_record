# BG & Insulin Alarm Playbook (Termux, reusable)

*Last updated: 2026-09-17 · tested on RedmiNote10s + Termux + Termux:API + Google TTS (cmn-TW downloaded)*

## 1. Two alarm layers (use both)

| Layer | What | Covers |
|---|---|---|
| DeskClock (`com.android.deskclock`) via intent | Loud system alarm + message text | Wakes you even if Termux sleeps |
| Background bash script | `bg_warn*.mp3` + vibration + Taiwan TTS voice, 3 rounds | Tells you *what to do* (check BG, eat glucose, dose rule) |

## 2. DeskClock alarm (system clock)

```bash
# 20:30 hypo-watch
am start -a android.intent.action.SET_ALARM \
  --ei android.intent.extra.alarm.HOUR 20 \
  --ei android.intent.extra.alarm.MINUTES 30 \
  --es android.intent.extra.alarm.MESSAGE "量血糖！5I高峰 hypo watch" \
  --ez android.intent.extra.alarm.SKIP_UI true
```

- First use per ROM may need DeskClock opened once to confirm.
- Verify verbally with user ("it is set correctly") — no reliable CLI readback.

## 3. Voice warning script (template — use this, not the old ones)

```bash
#!/bin/bash
# hypo_2130_0917_fix.sh — TEMPLATE
# Uses PRE-GENERATED MP3 (no network, no live TTS). Voice = edge-tts zh-TW-HsiaoChenNeural.
sleep 3375   # = target_epoch - now_epoch; compute: $(date -d "21:30 today" +%s) - $(date +%s)
termux-wake-lock 2>&1
for i in 1 2 3; do
  termux-vibrate -d 1000 2>&1
  termux-media-player play /storage/emulated/0/Documents/github/BG_record/audio/bg_warn5.mp3 2>&1
  sleep 60
done
```

Launch detached + verify:

```bash
chmod +x script.sh
setsid bash script.sh < /dev/null > script.log 2>&1 & echo ok-$!
sleep 3; ls /proc/<pid>/cmdline   # exists = running
```

Kill a stuck loop:

```bash
kill <bash_pid> <sleep_pid>
```

## 4. TTS: use edge-tts (Taiwan neural voice) — NOT Google TTS

**Default voice: `zh-TW-HsiaoChenNeural`** (Microsoft Taiwan female, neural, near-human). Verified 2026-09-18 — far better than Google's TTS fallback (which gave a China accent).

**Voices available (edge-tts):**
| Voice | Gender |
|---|---|
| `zh-TW-HsiaoChenNeural` | Female (DEFAULT) |
| `zh-TW-HsiaoYuNeural` | Female |
| `zh-TW-YunJheNeural` | Male |

**Generate an MP3 (needs network ONLY at generation time):**
```bash
edge-tts --voice zh-TW-HsiaoChenNeural --text "請量血糖" --write-media audio/bg_warn1.mp3
```

**Regenerate ALL standard warnings:** run `/data/data/com.termux/files/usr/tmp/opencode/gen_bg_warnings.sh`.

**Best practice:** pre-generate warning MP3s ahead of time (as done), so alarm scripts only `termux-media-player play` the file — **no network, no live TTS, no termux-tts-speak** needed at alarm time.

> Fallback if edge-tts unavailable: `termux-tts-speak -e com.google.android.tts -l zh-TW -s ALARM` (Google, may be China accent).

## 5. Ready-made warning lines (these are pre-generated in `audio/`; for custom text, re-run edge-tts)

| Situation | Chinese (TW) line | File |
|---|---|---|
| Plain prompt | 請量血糖。 | bg_warn1 |
| Hypo-watch peak (default) | 量血糖，胰島素高峰到了，低血糖風險最高。低於九十馬上吃葡萄糖粉，開燈坐著量。 | bg_warn5 |
| NPH window, must eat first | 下午兩點半，先量血糖再打NPH，空腹不可打。 | nph_1430 |
| Wake check | 六點半，量血糖，記錄晨起狀態。 | bg_0630 |

## 6. Audio files (`audio/` — ALL now edge-tts HsiaoChenNeural)

- `bg_warn1–5.mp3` — BG check warnings (warn5 = default for hypo-watch)
- `bg_0630/1400/1500.mp3` — time-based BG reminders
- `nph_0900/1250/1430/1836/2045.mp3` — NPH-slot reminders (pick nearest slot: 13:30 window → `nph_1430.mp3`)

## 7. Bugs found 2026-09-17 (do NOT regress)

1. **`termux-vibrate -d 1000,500,...` FAILS** — this termux-api build accepts one integer only (`Error: For input string`). Use `-d 1000` and loop if needed.
2. **`termux-notification` HANGS (~2 min block)** in this Termux — any script calling it stalls *before* mp3/TTS. Voice scripts must NOT call it (DeskClock covers the visual). Order: vibrate → mp3 → TTS.
3. **Stuck loops accumulate** (`bash` + `sleep` + `sh/termux-api` stay in `ps`) — kill old `<pid>`s after they fire; check `ps` before launching a same-slot replacement.
4. **`setsid ... &` + `echo ok-$!` is the launch pattern that returns fast**; `nohup` and chained `termux-notification` in the same one-liner block the tool call to timeout.

## 8. New-session checklist

1. `date '+%H:%M'` + `tail -n 8 bloodsugar.md` (current BG, active insulin, now-time)
2. Compute `sleep = target_epoch − now_epoch`
3. Send DeskClock intent (section 2)
4. Write script from template (section 3) with warning line (section 5) + mp3 (section 6)
5. Launch + verify via `/proc/<pid>` (section 3)
6. Tell user: DeskClock message + voice rounds + what to do at ring (BG first, dose rule, glucose bedside)
