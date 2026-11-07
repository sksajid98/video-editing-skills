---
name: cut-silences
description: Removes silences, dead air and long pauses from a talking-head, interview, podcast, vlog or reel recording, using a word-level transcript made locally with whisper.cpp (free, offline), and outputs an edit list (EDL), a re-timed transcript and optionally the cut video via ffmpeg. Use this whenever the user says cut the silences, trim pauses, remove dead air or gaps, tighten the pacing, make it snappier, or as the first cleanup pass of any talking-head edit, even if they just say clean up this video. Does not cut stutters, repeats or retakes (that is cut-mistakes).
license: MIT (adapted from nateherkai/herk-edit-kit)
---

# Cut Silences (edit pass 1)

First cleanup pass of a talking-head edit. Removes **only silence**: dead air before the first word, after the
last word, and pauses longer than a threshold (trimmed to a natural breath, never to zero). Words are untouched.
Stutters, false starts and retakes are the `cut-mistakes` skill (pass 2).

Scripts live in `~/.claude/skills/cut-silences/scripts/`. Keep every file in the project folder
`/Users/sajid.ali/Documents/Claude/<Project name>/` (source video copied in, original never overwritten).

## 1. Transcribe (word level, local, free)

```bash
python3 ~/.claude/skills/cut-silences/scripts/whisper_words.py "<project>/raw.mp4"
# Hindi / Hinglish or other languages: --model ~/whisper-models/ggml-medium.bin --lang auto
```

Writes `raw.json` next to the video: `{ words: [{text,start,end,type}], audio_duration_secs }`. Reuse an existing
word-level transcript if the user has one (ElevenLabs Scribe JSON works as is).

## 2. Plan, then cut

```bash
# plan only (EDL + re-timed transcript, video untouched)
node ~/.claude/skills/cut-silences/scripts/cut-silences.mjs "<project>/raw.json" --out-dir "<project>/edit"

# render the cut (local ffmpeg, re-encode, A/V in sync)
node ~/.claude/skills/cut-silences/scripts/cut-silences.mjs "<project>/raw.json" \
  --video "<project>/raw.mp4" --out-dir "<project>/edit" --output "<project>/edit/silenced.mp4" --apply
```

| Flag | Default | Meaning |
|---|---|---|
| `--video <path>` | none | Source video; enables the ffmpeg filter / render |
| `--out-dir <dir>` | next to transcript | Where outputs go |
| `--output <path>` | `<stem>.silenced.mp4` | Cut-video path |
| `--gap <s>` | `0.55` | Shortest pause treated as trimmable. Reels: 0.35–0.45. Corporate/interview: 0.7–0.9 |
| `--head-pad <s>` / `--tail-pad <s>` | `0.22` / `0.34` | Silence kept before the first / after the last word |
| `--apply` | off | Actually run ffmpeg |

How it decides: pauses under `--gap` stay. A trimmed pause keeps a breath (0.24 s after a long pause, 0.20 s after
`. ! ?`, 0.14 s otherwise). Cuts render in one ffmpeg `trim/atrim + concat` pass, so lip sync holds.

## 3. Outputs

| File | Use |
|---|---|
| `<stem>.silence-edl.json` | Keep/delete ranges in source seconds. Use it to rebuild the cut in Premiere |
| `<stem>.silence-transcript.json` | Words re-timed onto the cut timeline. Feed it to `cut-mistakes` |
| `<stem>.silence-decisions.md` | Readable summary and the biggest pauses removed |
| `silenced.mp4` | The cut video (only with `--apply`) |

## 4. Hand-off

- Next pass: `cut-mistakes` with `<stem>.silence-transcript.json` and `silenced.mp4`.
- To edit in Premiere instead of a flat MP4, the `video-studio` skill imports the raw clip and applies the EDL's
  `delete` ranges with `ripple_remove_timeline_ranges` on a new sequence, so the cuts stay editable.

## Gotchas

- **Cutting inside a phrase** clips words. Keep cuts between phrases; never speed up the voice.
- **Over-tight reels** sound breathless. Natural beats after a comma or "First," (0.2–0.4 s) should stay.
- **Wrong timeline**: the silence transcript matches `silenced.mp4`, not the raw file. Never mix the two.
- **base.en model on Hindi** returns garbage words. Use `ggml-medium.bin --lang auto` for Hindi/Hinglish.
- **Whisper word ends** run 40–80 ms early. If last syllables sound clipped, raise `--tail-pad` or `--gap`.
- A tool proposes cuts; the user's ear is the final check. Play the joins before calling it done.
