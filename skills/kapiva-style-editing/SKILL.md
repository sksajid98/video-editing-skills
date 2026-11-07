---
name: kapiva-style-editing
description: The user's all-in-one video editing skill in their Kapiva house style. It merges video-studio and house style, Kapiva brand, approved typography (incl. "bold and light" Jost combo), Premiere Pro MCP editing with native Premiere text layers, motion graphics in After Effects, motion B-roll, AE rebuilds, Google Flow AI B-roll prompts, silence and mistake cutting, and the hands-off auto-editor. Use it for any edit of a reel, ad, hook or body (Kapiva BP Xpert Juice, Liver Care Juice, Dia Free and others), storyboards and frames-first approvals, supers and typography, B-roll, zooms, flashes, music and SFX, Premiere timelines, Review Player previews and exports. Trigger on /kapiva-style-editing, "edit this video", "make the hook", "storyboard", "supers", "Kapiva style", "bold and light", "build it in Premiere", even if they don't name a skill.
---

# Kapiva-style editing (all video skills in one)

One skill for the whole job. Read only the parts the task needs; each part lives in `modules/` or `references/`.
The older skills (video-studio, brand-kapiva, premiere-pro-mcp, …) still exist; this one supersedes them for the
user's edits.

## 0. First, always
1. Read `modules/video-studio/house-style.md` (the user's standing rules). It overrides everything else here.
2. Short replies. Do the work; report results, links and what's left in a few lines.
3. Save every new rule the user gives to `modules/video-studio/house-style.md` (and to `~/.claude/skills/video-studio/house-style.md`),
   then re-sync with `install_skill.sh`.

## 1. The workflow (never skip a gate)
1. **Script** → take only the on-screen supers; list them per hook; **wait until the user names the hook/film**.
2. **Storyboard / frames first** → stills with 2–3 options for anything new, on the Review Player board
   (`http://localhost:4777/board?dir=<folder>`). Wait for approval. Approved frames are locked.
3. **Preview video** (ffmpeg) → open in the Review Player (`http://localhost:4777/?file=<abs path>`; start it with
   preview_start "review-player"). Read notes from `<video>.review.txt`.
4. **Notes round** → change only what was asked; run `change_tracker.py` to prove nothing else moved.
5. **Premiere build** → duplicate the user's sequence ("<name> – Claude edit vN"); never edit theirs; native text layers.
6. **Export** → draft to the project's `5. EXPORT/DRAFTS` (ask the location once per project), loudness -14 LUFS, open in Review Player.
   The user saves the Premiere project.

## 2. Where everything is

| Need | Read |
|---|---|
| Standing rules, look, supers, transitions, subtitles | `modules/video-studio/house-style.md` |
| Workflow per video type, 12 stages | `modules/video-studio/references/video-types.md` |
| Reels / Shorts pacing | `modules/video-studio/references/short-form-playbook.md` |
| Pick type + tone per video (7 Kapiva reels) | `modules/video-studio/references/kapiva-style-system.md` |
| Typography (approved family, bold+light) | `references/typography.md` |
| Kapiva colours, logo, health-claim wording | `modules/brand-kapiva/GUIDE.md`, `modules/brand-kapiva/references/brand.md` |
| Premiere MCP: connect, safe tool order, troubleshooting | `modules/premiere-pro-mcp/GUIDE.md`, `modules/video-studio/GUIDE.md` |
| Supers/boxes as native Premiere graphics | `references/premiere-native-text.md` + `scripts/make_pr_text.py` |
| Motion graphics in AE, Dynamic Link, timing rules | `modules/video-studio/GUIDE.md` §4, `modules/video-studio/motion-design-rules.md` |
| Rebuild an animation as an editable AE project | `modules/ae-builder/GUIDE.md` |
| Word-timed UI B-roll on a talking head | `modules/motion-broll/GUIDE.md` |
| AI B-roll prompts (Google Flow / Veo) | `modules/google-flow/GUIDE.md` |
| Cut silences / cut mistakes | `modules/cut-silences/GUIDE.md`, `modules/cut-mistakes/GUIDE.md` |
| Hands-off full edit (drop videos → final MP4) | `modules/video-auto-editor/GUIDE.md` |

## 3. Look (quick list; details in house style)
- No colour grade. No fades. Never speed up B-roll; B-roll full frame. Drop shadow on all text.
- No zooms in multi-cut stretches (e.g. first 20 s of a hook); slow pushes only on longer shots.
- Flash + swish SFX on big section changes; pops on supers; energetic music ducked under VO, long enough for the Body.
- No home-made illustrations: real or AI B-roll (write Flow prompts), 3D emoji icons only where approved.
- Typography per video from the approved family; "bold and light" = Jost Bold + Jost Light caps (see typography.md).
- iPhone HDR footage: tag previews SDR (`setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709`).

## 4. Preview build rules (ffmpeg)
Render each segment with an exact `-frames:v` count, `setsar=1`, join with the concat **filter**, blend 24 fps clips
(`framerate=fps=25`), overlay transparent PNG supers per time window, flashes with a geq white layer, audio:
sidechain-duck music under VO, loudnorm -14. A working example: `/Users/sajid.ali/Documents/Claude/Kapiva BPXJ – Sonia/hook1/build_preview.py`.

## 5. Premiere build rules
- Guard every edit with `expected_cep_target {"backend":"cep","sequence_id":…}`.
- Supers: one element per layer via `make_pr_text.py` (see references). Icons as PNG layers. Flashes = white PNG on a
  top track with opacity keys 0 → 85 → 0 over 0.2 s.
- B-roll: set source in/out, overwrite on V2; 24 fps clips get frame blending; their audio on a muted track.
- Music as a pre-ducked WAV on its own track; SFX on separate tracks with the preview's gains.
- Name tracks (Icons, Supers 0–4, Flashes, Music (ducked), SFX). Export check frames and compare with the approved preview.

## Scripts

| Script | What it does |
|---|---|
| `scripts/make_pr_text.py` | Makes native Premiere text / text+box `.mogrt` files from the stock templates |
| `modules/video-auto-editor/scripts/intake.sh`, `qc_final.py`, `finish_audio.sh` | Auto-editor intake, QC and final audio |
| `modules/cut-silences/scripts/*`, `modules/cut-mistakes/scripts/*` | Whisper word timings, silence/mistake EDLs, apply cuts |
| `modules/motion-broll/scripts/*`, `modules/motion-broll/engine/*` | Motion B-roll pages, render and composite |
| `modules/ae-builder/scripts/*`, `modules/ae-builder/assets/*` | AE rebuild library, easing fit, curve checks |
| Review Player change tracker | `~/Developer/video-use/.venv/bin/python …/change_tracker.py` (see house style) |

## Gotchas
- **Running ahead.** Don't process footage before the user names the hook; don't render video before frames are approved.
- **Adding unrequested things** (extra lines, disclaimers, effects, speed-ups) — the user rejects them every time.
- **Editing the user's sequence** or switching the active sequence while they work: duplicate, guard, and ask before switching back.
- **AE for supers.** Never; supers are native Premiere graphics. AE only for graph/bar animation.
- **Custom box shapes** (rounded/skewed) break native Premiere graphics; use the template box and say so.
- **MOGRT default length** overwrites later clips on a track: place in time order or on a free track.
- **Tokens.** Batch Premiere calls, read single tracks, small check frames, a new session per hook, short replies.
- **Agents.** Don't spawn agents unless the user says so.
- **Two copies of the house style.** After saving a rule, sync both `modules/video-studio/house-style.md` here and
  `~/.claude/skills/video-studio/house-style.md`, then run `install_skill.sh` for each skill.
