---
name: cut-mistakes
description: Finds and removes spoken mistakes (stutters, repeated words, false starts and retakes, keeping the last clean take) from a talking-head, interview, podcast or reel recording, review-gated so every cut is shown with context and approved before ffmpeg renders it. Use this after cut-silences, or whenever the user says cut the mistakes, remove stutters or repeats, clean up flubs, remove retakes, keep the best take, or fix the bad takes, even if they just say clean up my talking. Needs a word-level transcript.
license: MIT (adapted from nateherkai/herk-edit-kit)
---

# Cut Mistakes and Retakes (edit pass 2)

Second cleanup pass, run after `cut-silences`. Removes stutters ("the the", "I- I-"), repeated words, false starts
and retakes (keeps the clean take). What counts as a mistake is **judgment**: "never, never" for emphasis looks
like a stutter to a script. So every cut is reviewed before rendering.

Scripts: `~/.claude/skills/kapiva-style-editing/modules/cut-mistakes/scripts/`. Files stay in `/Users/sajid.ali/Documents/Claude/<Project name>/edit/`.

## 1. Find candidates (mechanical)

```bash
node ~/.claude/skills/kapiva-style-editing/modules/cut-mistakes/scripts/find-cut-candidates.mjs \
  "<project>/edit/raw.silence-transcript.json" --out-dir "<project>/edit"
```

Writes `<stem>.cut-candidates.json` (type, confidence, cut range, removes/keeps text, context) and a readable
`<stem>.cut-candidates.md`. Types: `stutter`, `retake` (near-duplicate line), `false_start`.

## 2. Review (required gate)

Read every candidate's `removes` and `context`. Show the user a short table (time, what goes, what stays, your
recommendation) and collect approvals. Write the approved cuts (seconds on the **silenced** timeline):

```json
{ "cuts": [ { "start": 100.93, "end": 101.06, "reason": "I- false start" } ] }
```

For a retake, widen the cut from the start of the botched take to the clean restart. Zero cuts is a valid result.

## 3. Apply

```bash
node ~/.claude/skills/kapiva-style-editing/modules/cut-mistakes/scripts/apply-cuts.mjs \
  "<project>/edit/raw.silence-transcript.json" --cuts "<project>/edit/approved-cuts.json" \
  --video "<project>/edit/silenced.mp4" --out-dir "<project>/edit" --output "<project>/edit/clean.mp4" --apply
```

Writes the EDL, `<stem>.mistakes-transcript.json` (re-timed for captions and graphics), a decisions log and, with
`--apply`, `clean.mp4`. Drop `--apply` for a dry run. Then hand `clean.mp4` + the mistakes transcript to
`video-studio` (Premiere/AE graphics, captions) or `motion-broll`.

## Gotchas

- **Emphasis is not a stutter.** "It's never, never hands-off", "the piece is, is this…" and lists are false positives.
- **Fillers glued to the next word** ("what it does is it…") stay. Cutting them clips the neighbouring word.
- **Join takes only where both sides are silent.** If takes run together, keep one take whole.
- **Timeline mix-ups**: approved cut times are on the silenced timeline. Captions must use the mistakes
  transcript, never the raw one.
- Hard joins between words can click. Listen to every join; add a 20–30 ms audio crossfade in Premiere if needed.
