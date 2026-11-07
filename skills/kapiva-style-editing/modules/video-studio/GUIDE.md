---
name: video-studio
description: Edit the user's real videos end to end in Adobe Premiere Pro through the premiere-pro MCP, and build motion graphics in After Effects through the after-effects MCP, Dynamic Linked back into the Premiere timeline. Use whenever the user asks to edit, cut, trim, assemble, caption, color, add titles/lower thirds/animated text/logo stings/motion graphics to, or export a video in Premiere or After Effects.
---

# Video studio: Premiere Pro + After Effects

**Read `house-style.md` first.** It holds the user's standing rules (approval-first frames, no fades,
super formation, Hinglish subtitles) and overrides the defaults below. Add each new standing rule the
user gives in chat to that file.

Before planning, read `references/video-types.md`: the 12-stage workflow and the recipe for this video type
(talking head, reel, motion graphics, corporate, testimonial, product ad, tutorial, podcast, event…). For reels and
Shorts also read `references/short-form-playbook.md`.

## 0. The video skill chain

video-studio is the hub. Load the skill for each stage the job needs, in this order, and skip the stages it doesn't:

| Stage | Skill | Hands on |
|---|---|---|
| Idea | `video-idea-finder` | chosen idea + 3 hooks |
| Script | `reel-script-writer` | script to record |
| AI shots (optional) | `google-flow` | generated clips to import |
| Silence pass | `cut-silences` | EDL + re-timed transcript |
| Mistake pass | `cut-mistakes` | EDL / `clean.mp4` |
| Edit in Premiere | `video-studio` (this skill), `premiere-pro-mcp` for bridge trouble | sequence |
| Motion graphics | `motion-broll` (word-timed B-roll), AE via §4, `ae-builder` (rebuild an animation as an editable AE project), `hyperframes` / `remotion-best-practices` (code-rendered graphics) | clips / Dynamic Linked comps |
| Brand | `brand-kapiva` for Kapiva work, else `brand-book` | styles for titles, captions, end cards |

Brand rules and `house-style.md` apply at every stage. When a stage finishes, offer the next one in one line.

Two MCP servers are registered in the Claude app: `premiere-pro` and `after-effects`. Their tools are
deferred, so load them with ToolSearch before the first call:

- `select:mcp__premiere-pro__verify_premiere_connection,mcp__premiere-pro__get_capabilities,mcp__premiere-pro__get_full_sequence_info,mcp__premiere-pro__export_frame,mcp__premiere-pro__export_sequence`
  (the Premiere tools are called directly by name; use `get_capabilities` with `tool_query` to find more)
- When motion graphics are needed: `select:mcp__after-effects__run-script,mcp__after-effects__get-results,mcp__after-effects__setLayerKeyframe,mcp__after-effects__setLayerExpression,mcp__after-effects__apply-effect,mcp__after-effects__apply-effect-template,mcp__after-effects__create-composition`

## 1. Connect (always first)

1. `verify_premiere_connection`. It launches Premiere if it is closed and waits for the MCP Bridge panel.
   If it returns `userActionRequired: true`, give the user `nextStep` word for word and stop.
2. Only when the edit needs motion graphics, connect After Effects:
   - If it is not running: `open -a "Adobe After Effects 2026"` (Bash), then wait ~30–60 s.
     The Startup script `zz_mcp-bridge-autostart.jsx` opens the "MCP Bridge Auto" palette on its own.
   - Probe: `run-script` `getProjectInfo`, wait 3 s, `get-results`. A fresh `_responseTimestamp` means connected.
     A stale or missing result: ask the user to open Window > mcp-bridge-auto.jsx and tick "Auto-run commands".
   - If the panel was never installed or the probe keeps failing, tell the user to run
     `bash setup-video-studio.sh` in the Adobe_Premiere_Pro_MCP-main folder.

## 2. Understand the footage before cutting

- Inspect first: `list_sequences`, then `search_tools` → `list_project_items`, `get_active_sequence`, `list_sequence_tracks`.
- For talking-head or interview footage, transcribe locally to choose cuts:
  `ffmpeg -i in.mp4 -ar 16000 -ac 1 /tmp/a.wav && whisper-cli -m ~/whisper-models/ggml-base.en.bin -f /tmp/a.wav -osrt`.
- Use `detect_silence` (ffmpeg-based) to find dead air.
- For a full cleanup pass, use the `cut-silences` skill (local whisper word transcript + EDL), then `cut-mistakes`
  (review-gated stutters/retakes). Apply their EDL delete ranges in Premiere with `ripple_remove_timeline_ranges`
  on a new sequence, or import their `clean.mp4`.
- If the Premiere bridge misbehaves, follow the `premiere-pro-mcp` skill's troubleshooting.
- Check that every media path exists before `import_media`. Never invent paths, clip ids or .mogrt files.

## 3. Edit in Premiere

- Find tools with `search_tools` (natural-language `query`, or regex `pattern` like `^trim|split|ripple`), read
  arguments with `get_tool_schema`, run with `invoke_tool`.
- Make a new, clearly named sequence (e.g. `<name> – Claude edit v1`) instead of changing the user's sequence,
  unless they ask you to edit it in place.
- Typical order: import → assemble on V1/A1 → trim/split/ripple-delete silences → b-roll on V2 → audio levels and
  ducking (`setup_ducking`) → transitions → color/effects → graphics (step 4) → markers → export.
- Every project gets its own folder in `/Users/sajid.ali/Documents/Claude/<Project name>/`: move/copy the
  source video there, and keep the Premiere project, AE .aep, transcripts, renders and exports in it.
- Ask before deleting media, closing projects, saving over the project file, or overwriting an export.
- If a tool returns `success: false`, report the exact error; don't retry blindly.

## 4. Motion graphics → After Effects → Dynamic Link

Use AE when the user wants animated titles, lower thirds, kinetic type, logo animations, shape animation,
or anything beyond a static .mogrt.

Before designing any graphic, read `motion-design-rules.md` (in this skill folder) and follow its timing,
easing, typography, safe-zone and composition rules. Run its QC checklist before linking into Premiere.

1. Build in AE: `create-composition` (match the Premiere sequence's width/height/fps/duration), then
   `run-script` with `createTextLayer` / `createShapeLayer` / `createSolidLayer` / `setLayerProperties`,
   plus `setLayerKeyframe`, `setLayerExpression`, `apply-effect`, `apply-effect-template`.
   Call `get-results` after each `run-script` to confirm it worked.
2. Save the AE project: `run-script` `saveProject` with
   `{ "path": "<project folder>/<name>_motion.aep" }`. Keep the .aep next to the Premiere project.
   `get-results` returns the path and the comp names.
3. Link it into Premiere: `invoke_tool` `import_ae_composition` with
   `{ aepPath, compName, sequenceId, time, videoTrackIndex }` (default V2, above the footage).
   The comp lands in the "AE Dynamic Link" bin as a live-linked clip.
4. To revise the graphic: change it in AE, `saveProject` again (no path), and Premiere updates the
   linked clip. There is no need to re-import.

If the user only needs a simple title and has a .mogrt, `add_text_overlay` / `import_mogrt` in Premiere is faster.
For fully generated HTML-based graphics, the `hyperframes` skill renders a video file that can be imported instead.
For word-timed UI-style B-roll on a talking-head video (one morphing shape, cursor-driven), use the
`motion-broll` skill. It renders MP4 cutaways and transparent ProRes 4444 `.mov` panels named by their
in-point (`04-name_0m32s40.mov`). Then `import_media` them and place each one on V2 at its in-point with
`add_to_timeline`. Its `preview.mp4` is for review only.

## 5. Finish

- Save the Premiere project only with the user's OK. Export with the export tools (`search_tools` "export").
- Report what changed: the sequence name, cuts made, graphics added (AE project path + comp names), and the export path.

## Gotchas

- Story before polish: don't grade or add graphics until the cut is approved.
- EDL/transcript times from `cut-silences` are on the silenced timeline; don't apply them to the raw clip twice.
- A brand skill (e.g. `brand-kapiva`) overrides default title/caption styles.
