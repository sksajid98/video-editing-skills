# Video types, editing workflow and commands

Read this when planning any edit. Find the video type, then follow its recipe inside the standard workflow.
`house-style.md` and the client brand skill (e.g. `brand-kapiva`) override everything here.

## 1. The standard editing workflow (every video)

| Stage | What happens | Tools here |
|---|---|---|
| 1. Brief | Goal, audience, platform, length, aspect ratio, brand, deadline, reference video | Ask once, in one round |
| 2. Ingest and organize | Project folder `/Users/sajid.ali/Documents/Claude/<Project>/`, copy media, bins (Footage, Audio, Music, Graphics, B-roll, Exports) | `import_media`, `create_bin`, `move_items_to_bin` |
| 3. Log and transcribe | Word-level transcript, mark good takes and key lines | `cut-silences` → `whisper_words.py`, `add_markers_batch` |
| 4. Paper edit / story | Write the structure from the transcript before touching the timeline (hook → body → payoff → CTA) | text plan, `create_editorial_plan` |
| 5. Assembly | All usable takes in story order on V1/A1 | `create_sequence_from_clips`, `add_to_timeline_batch` |
| 6. Rough cut | Remove silences, mistakes, retakes; get the story right | `cut-silences`, `cut-mistakes`, `ripple_remove_timeline_ranges` |
| 7. Fine cut | Pacing, J/L cuts, punch-ins, B-roll on V2+, cutaways | `split_clip`, `trim_clip`, `set_clip_scale`, `add_keyframe` |
| 8. Graphics | Titles, lower thirds, captions, motion graphics, logo, end card | AE via `video-studio` §4, `motion-broll`, `hyperframes`, `.mogrt` |
| 9. Sound | Dialogue level, music bed, ducking, SFX, loudness | `adjust_audio_levels`, `setup_ducking`, `analyze_loudness` |
| 10. Color | Correct (exposure, white balance, match shots), then grade (look/LUT) | `color_correct`, `apply_lut`, `read_video_scopes` |
| 11. Review | Export review frames, check sync, captions, safe zones, client notes | `export_sequence_review_frames`, `check_caption_safe_zone`, `plan_client_notes_checklist` |
| 12. Deliver | Export per platform, verify the file | `export_sequence`, `verify_delivery_file`, `plan_platform_delivery_matrix` |

Rule: story before polish. Never color or add graphics to a cut whose story isn't approved.

## 2. What a "command" is

- **Skill**: a written workflow I follow (`video-studio`, `cut-silences`, `brand-kapiva`…). Triggers by itself
  from your words, or by name: `/cut-silences`.
- **MCP tool call**: one action inside an app, e.g. `split_clip` in Premiere or `run-script createTextLayer`
  in After Effects. A skill is a recipe; tool calls are its steps.
- **Script / CLI command**: a terminal command such as `ffmpeg`, `whisper-cli` or `node cut-silences.mjs`.
  Used for work outside Premiere (transcripts, flat-file cuts, loudness checks).
- **ExtendScript**: code run inside AE/Premiere when no tool exists (AE `run-script`). Last resort in Premiere.

## 3. Video types and their recipes

| Type | Key traits | Edit recipe |
|---|---|---|
| **Talking head** (YouTube, vlog, educator) | One speaker to camera; story lives in the words | Transcribe → cut silences (gap 0.5) → cut mistakes → punch-ins (110–120 %) every 10–20 s on key lines → B-roll per noun → captions → light music −20 dB under voice |
| **Reel / Short / TikTok** (9:16) | Hook in 3 s, 15–90 s, sound-off viewing | Hook first frame; cut silences tight (gap 0.35–0.45); shots 1–3 s; split / full B-roll / punch-in layouts; 1–3-word captions in safe zone; every shot moves; music −11 dB; −14 LUFS. See `references/short-form-playbook.md` |
| **Motion graphics / explainer** | Animated type, shapes, icons; often voiceover-driven | Script + VO first, then a beat grid; animate to VO words; one visual idea per beat; 8–12-frame eases; build in AE (`ae-builder`, `motion-design-rules.md`) or `hyperframes`; link into Premiere |
| **Corporate video** (company profile, internal comms, CEO message) | Polished, calm, on-brand, legal/compliance aware | Interviews + B-roll; slower pacing (gap 0.7–0.9, shots 3–6 s); clean lower thirds with name/title; brand colors only; soft dissolves allowed; subtitles for accessibility; −16 LUFS for web/LinkedIn |
| **Testimonial / interview** | Real person, credibility | Pick the 3–5 strongest soundbites (paper edit); J/L cuts; cover jump cuts with B-roll or a 2nd angle; lower third on first appearance; keep natural pauses |
| **Product / ad / promo** (e.g. Kapiva) | Sell one product, 6–60 s, CTA | Hook → problem → product hero → benefits (safe claims) → proof → CTA + end card; packshot on clean bg; beat-synced cuts (`detect_beats`, `plan_beat_montage`); disclaimer; exports 9:16, 1:1, 16:9 |
| **Tutorial / screen recording** | Teach steps | Cut dead time; zoom 150–200 % into the clicked area with eased keyframes; cursor highlight; chapter markers (`plan_chapter_markers`); step titles |
| **Podcast / multicam** | 2+ speakers, long | Sync cameras/audio (`plan_media_synchronization`); switch to the active speaker (`plan_multicam_angle_switches`, `plan_speaker_checkerboard`); level each voice; clips for shorts (`rank_short_form_candidates`) |
| **Documentary / storytelling** | Narrative arc, emotion | Paper edit by story beats; establishing shots; music carries emotion; L-cuts; slow color grade; archival with credits |
| **Event / wedding / highlight** | Music-driven montage | Pick music first; cut on beats; best moments in story order (arrival → peak → ending); speed ramps; cross-dissolves for time passing; warm grade |
| **Music video** | Cut to the track | Beat/bar markers; performance + narrative intercut; effects synced to transients (`detect_audio_transients`) |
| **Slideshow / photo video** | Stills only | Ken Burns push (100→110 % over the shot), 2–4 s per photo, beat-timed, dissolves |

## 4. Universal quality checks before delivery

- Audio: dialogue clear, music ducked, no clicks at joins, −14 LUFS (social) / −16 LUFS (web), true peak ≤ −1 dBTP.
- Picture: no black or flash frames, no jump cut left uncovered, horizon and skin tones right.
- Text: spelled right, in the safe zone, readable on a phone, on-brand font and colors, never over the mouth.
- Sync: lips match after every cut.
- Export: right resolution, fps, aspect ratio and codec for each platform, file verified after export.
