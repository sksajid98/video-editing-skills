# Pipeline specs (read at the start of every job)

## Project folder
`/Users/sajid.ali/Documents/Claude/<Project name>/`
```
source/      the user's videos (copied, never edited)
analysis/    per-source transcripts (tr_hi.srt, tr_en.srt), cuts.txt, sheet.png, a.wav
storyboard/  storyboard.md, frames v1/ (+ board.review.json from the Review Player), _old/
graphics/    HyperFrames project, overlay ProRes 4444, cut-outs
broll/       clips the user drops (keep their names)
audio/       music bed, SFX, stems, mix
renders/     every render (v1, v2…) + .changes.json
exports/     <Name> FINAL vN.mp4 (only QC-clean renders)
```

## Storyboard template (`storyboard/storyboard.md`)
```
# <Project> – storyboard v1
Topic: … | Format: … (ref vN) | Tone: … | Type: <family weights> | Accent: #… | Music: <pick> (−NN dB under voice)

| # | In–out | Spoken words (Hinglish) | Visual | Super / graphic | Transition | SFX | Frame |
|---|--------|------------------------|--------|-----------------|------------|-----|-------|
| 01 | 0.00–2.40 | "High BP at 30…" | A-roll MCU | HIGH BP / AT 30 lockup, headroom | cut | whoosh | 01 Hook - HIGH BP.png |

## B-roll needed
| # | Beat | Why | Tool | Prompt |
```
Beat lengths: hook ≤ 3 s; product reveal at 30–66% of runtime; end card 3–4 s.

## Render recipes
- Graphics: HyperFrames project in `graphics/`, at the source size and fps. Overlay = transparent ProRes 4444
  (`-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le`). Snapshot stills for the board with `npx hyperframes snapshot --at`.
- Composite: ffmpeg `overlay` of the ProRes on the source, with B-roll placed by `enable='between(t,a,b)'` or a
  concat list. Hard cuts only.
- Final: `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r <src fps> -c:a aac -b:a 320k`, then `finish_audio.sh`.

## Audio chain (ffmpeg, voice = source dialogue)
Voice:
```
highpass=f=75, equalizer=f=300:t=q:w=1.2:g=-2.5, equalizer=f=4000:t=q:w=1.0:g=2.5,
deesser=i=0.4:f=0.55, acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3
```
Add `afftdn=nf=-25` only for outdoor or handheld audio (the v1 type).
Music bed: set it so speech sits above the bed by the tone's gap. Urgent/dramatic 12–15 dB, friendly/clinical
15–18 dB, celebrity/podcast 18–22 dB. Then duck it under the voice:
```
[music][voice]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[bed]
```
Raise the bed 4–6 dB on the end card, ending on the music's natural end or a sting.
SFX: 6–10 dB under voice peaks, only in the friendly, dramatic and clinical tones, on graphic entrances.
Master: `amix` (normalize=0), then `finish_audio.sh` to -14 LUFS integrated, -1 dBTP.

## Stop summaries (what to post)
Stop 1:
```
Storyboard ready: <board link>
Topic · Format (ref) · Tone · Type · Accent · Music options (1–3)
B-roll I need (N): table with prompts
Decisions I made: …
```
Stop 2:
```
Final MP4: <Review Player link> · <path>
What I did: N supers, N graphics, N B-roll, captions, music −NN dB, -14 LUFS
QC: all PASS (or what's left, and why)
```
