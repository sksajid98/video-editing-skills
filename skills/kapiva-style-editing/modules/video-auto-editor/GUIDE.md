---
name: video-auto-editor
description: The user's hands-off video editor. When the user drops one or more videos (a talking head, a stitched raw edit, a reel, a Kapiva or other client ad), it runs the whole edit on its own in the user's house style. It picks the topic, format, tone and typography, writes and renders the storyboard and lists the B-roll it needs with prompts. After the storyboard is approved it builds the titles, motion graphics, captions, B-roll and audio mix, checks its own work, and delivers the final MP4. Then it takes revision notes until final approval and hands over the editable Premiere project. Use this whenever the user attaches or points to video files and says edit this, make the video, do your thing, here's the footage, auto edit, make it like the Kapiva references, or just drops videos with little or no instruction, even if they don't say "agent" or "auto". Not for a single small change to an existing timeline (use video-studio) or for idea/script work (video-idea-finder, reel-script-writer).
---

# Video auto-editor

The user wants to drop footage and get a finished, on-brand MP4 with as few stops as possible. This skill drives
the whole job end to end. It stops only at the three points the user asked for: the **storyboard**, the **final MP4**
and the **final project approval**. Everything between those stops runs on its own, including fixing its own
mistakes before the user sees anything.

It is a conductor. The how-to for each craft lives in other files, so read them; don't re-invent them here:
- `~/.claude/skills/kapiva-style-editing/modules/video-studio/house-style.md`: the user's standing rules. They override everything, including the references.
- `~/.claude/skills/kapiva-style-editing/modules/video-studio/references/kapiva-style-system.md`: the typography picker, tones, the 15-step order, sync, spacing, audio and recipes.
- `~/.claude/skills/kapiva-style-editing/modules/video-studio/motion-design-rules.md`: timing, easing and QC for graphics.
- `references/pipeline-specs.md` (this skill): the storyboard template, render recipes, the audio chain and folder layout. Read it at the start of every job.

## Stops (the only times you wait for the user)

| Stop | What you show | What you wait for |
|---|---|---|
| 1. Storyboard | Frame Board link plus a one-screen summary: topic, tone, type, palette, music pick, missing B-roll with prompts | Approval or comments on frames, plus the B-roll files |
| 2. Final MP4 | First ask where to export it. Then the MP4 opened in the Review Player, plus a short "what I did" list and the QC result | Review comments, or "approved" |
| 3. Project file | Only after the MP4 is approved: build the editable Premiere project (video-studio §3–4) | The user's OK to save over project files |

Between stops, don't ask small questions. Decide with the references and say in the stop summary what you decided.
Ask early only when you are truly blocked (no usable audio, wrong aspect ratio, the brand is unknown and the choice changes everything).

## Phase A: intake → storyboard (automatic)

1. **Intake.** Run `scripts/intake.sh <videos…> --project "<Name>"`. Name the project after the product and topic
   (e.g. `Kapiva Dia Free – Doctor reel`). It builds the folder, transcripts, cuts and contact sheets.
2. **Read the footage.** Look at the contact sheet(s) and read `tr_hi.srt` (Hinglish source) and `tr_en.srt` (meaning).
   Note who is talking, where, the framing, and whether it is already a stitched edit. A stitched edit is never re-cut
   or retimed (house rule): you only add on top.
3. **Topic, format, tone.** Name them in one line each, and pick the matching reference (v1–v7) from the picker.
   Never reuse the last project's typography unless the format is the same. Check the memory or the last project
   folder for what was used last.
4. **Design system for this video.**
   - One accent colour plus white plus a dark.
   - Slide backgrounds.
   - Type family and weights (max 2 families).
   - Lockup style and caption style.
   - Spacing bands.
   - Music bed brief and SFX plan.

   Brand rules come first: for Kapiva, apply `brand-kapiva` and its health-claim wording.
5. **Beat sheet.** Map the transcript onto the spine: hook → problem → science → product → herbs → usage/safety →
   end card. Every row gets these columns:
   - time in–out;
   - the spoken words;
   - visual (A-roll, B-roll, card or slide);
   - super text, using the speaker's exact words;
   - graphic type;
   - transition;
   - SFX.

   Use the template in `references/pipeline-specs.md`.
6. **Storyboard stills.** Render one still per beat on the real frame of the footage, with the actual type and
   graphics, the way `hyperframes` snapshot works. For any new motion graphic, render 2–3 design options. Save them
   to `storyboard/frames v1/` named `NN <beat> - <what>.png`. Write `storyboard/storyboard.md`.
7. **B-roll needs.** For each B-roll beat with no footage, write why it is needed plus a Flow/Veo prompt (the
   `google-flow` skill and the prompts page of the breakdown). Ask which tool the user will use if you don't know yet.
8. **Music.** Pick 2–3 bed options by tone: from the user's music folders first, otherwise suggest Artlist catalog
   tracks with `search_music`. Never generate or license anything without the user saying so.
9. **STOP 1.**
   - Start the Review Player (`preview_start review-player`).
   - Post `http://localhost:4777/board?dir=<frames folder>`.
   - Give the summary.

## Phase B: build → self-QC → final MP4 (automatic)

Start when the storyboard is approved. Approved frames are locked: build them exactly as approved.

1. **Read the board comments** (`board.review.txt`). If any frame has a comment, re-render only that frame and show
   it again. That counts as a short Stop 1 again; don't build the video on an unapproved frame.
2. **Assemble.** Place the B-roll the user dropped on the beats, at real speed and never sped up. Take the part of
   the clip that fits.
3. **Graphics.** Use HyperFrames (local CLI) as in house-style:
   - Render one transparent ProRes 4444 overlay at the source size and fps.
   - Make person cut-outs with `npx hyperframes remove-background` for text-behind-head.
   - Supers start on the first frame of their word.
   - Entrances follow house-style: a whole line or word settles in from blur. No letter-by-letter stagger, no fades or dissolves.
4. **Captions.** Use text layers in the overlay, not a caption track. Write them in Hinglish, 2–5 words, in the
   chosen caption style. Hide them under supers.
5. **Audio.** Build the mix with the chain in `references/pipeline-specs.md`:
   - voice clean-up;
   - music bed at the tone's level, ducked under speech;
   - SFX only where the tone uses them;
   - end-card swell;
   - `scripts/finish_audio.sh` to reach -14 LUFS / -1 dBTP.
6. **Render** H.264 1080×1920 at the source fps to `renders/<name> v1.mp4`.
7. **Self-QC loop.** Repeat until clean, at most 3 passes:
   - Run `scripts/qc_final.py <mp4> --fps <src fps>`.
   - Snapshot every super and graphic moment and check each one against the Done checklist below.
   - Fix what fails and re-render.

   Fix the generator (HTML, timing, mix settings), not the frame. Record what you fixed.
8. **Ask where to export (every project).** Before the first export of each project, ask the user which folder the
   MP4 should go to, so they can show it from there. Offer the project's `exports/` folder as the default. Never
   carry the folder over from another project. Within the same project, later versions go to the same folder unless
   the user names a new one.
9. **STOP 2.**
   - Copy the clean render to `<chosen folder>/<Name> FINAL v1.mp4`.
   - Open it in the Review Player (`/?file=…`).
   - Give a "what I did" list (tone, type, palette, music, graphics count, QC results).

## Phase C: revisions (until approved)

- Read the user's comments from `<video>.review.json` / `.txt` or the chat. Change only what the notes ask for.
- Re-render, then run `Review Player/change_tracker.py OLD NEW --expect "<ranges>"`. Anything UNEXPECTED is a bug,
  so fix it before showing.
- Re-run `qc_final.py`. Deliver `<chosen folder>/<Name> FINAL v2.mp4`, v3 and so on (ask again only if the user wants a new place). Every new standing rule from the notes
  goes into `video-studio/house-style.md` and is synced to `Skils/`.

## Phase D: final project (after "approved")

Build the editable Premiere sequence with After Effects Dynamic Link graphics, adjustment layer, gradient and subtitle
text layers, following video-studio §3–4 and the Hook 3 v8 build. Ask before saving over any existing project file.

## Delegating to the agent

Don't delegate. Run every phase yourself in the main chat (user rule, 2026-11-04). Use the `video-auto-editor` agent
(`~/.claude/agents/video-auto-editor.md`) only when the user explicitly says to use an agent for that task.

## Scripts

| Script | What it does | When |
|---|---|---|
| `scripts/intake.sh <videos…> --project "<Name>"` | Project folders, copies sources, transcripts (hi + en), cuts, contact sheets, JSON summary | Phase A step 1 |
| `scripts/finish_audio.sh in.mp4 out.mp4` | Two-pass loudnorm to -14 LUFS / -1 dBTP, video copied untouched | Last step of every render |
| `scripts/qc_final.py final.mp4 --fps N` | Size, fps, codecs, loudness, true peak, black/frozen frames | Every render before showing |
| `Review Player/change_tracker.py OLD NEW --expect "a-b,…"` | Proves only the requested ranges changed | Every revision |

## Gotchas

- **Stopping too often.** The user asked for automation between stops. Asking "should the super be white?" midway
  breaks that. Decide from house-style and the picker, and list the decision in the stop summary.
- **Skipping Stop 1.** Rendering the video before the storyboard is approved breaks the frames-first rule. Only the
  storyboard stop gates the build.
- **Copying the references' animation.** The Kapiva references use letter-by-letter reveals and light wipes, which
  house-style bans. Copy their layout, type choice, pacing and audio, not those entrances.
- **Same look every video.** Re-using the last project's family is the exact thing the user wants to avoid. Check what was used last.
- **Inventing claims or numbers.** Supers use the speaker's exact words. Kapiva health claims follow brand-kapiva wording.
- **Unrequested extras.** Never add disclaimers, Latin names, halos, tagline bars or a colour grade that nobody
  asked for. That was a rejected round on Hook 3.
- **Retiming the user's edit.** A stitched source is final picture. Only overlay on top of it.
- **Speeding up B-roll** to fit a beat is banned. Use a shorter section of the clip instead.
- **Silent failures in background renders.** HyperFrames and ffmpeg can exit 0 with a wrong-length file. Always check
  the duration against the source, and run `qc_final.py`.
- **Hinglish captions.** whisper `-l hi` writes Devanagari. Transliterate it into Hinglish (Roman letters, English words
  as spoken) using `tr_en.srt` for meaning; never put Devanagari or the English gloss on screen.
- **Loudness.** References swing from -13 to -22 LUFS. Always finish at -14 LUFS / -1 dBTP so Instagram doesn't turn it down or distort it.
- **Text on the eye line**, or a box narrower than its text: check every graphic still at full size before Stop 2.

## Done checklist (before Stop 2)

- [ ] Every beat in the approved storyboard is in the video, in order, and approved frames match pixel for pixel.
- [ ] Supers land on their word (±2 frames) and use the speaker's exact words.
- [ ] Nothing on the face or eye line; text fits its boxes with padding; lockups centred on the frame axis.
- [ ] White type has the house drop shadow (40% opacity, softness 5), no halos.
- [ ] Captions in Hinglish, 2–5 words, hidden under supers.
- [ ] No fades, dissolves or letter staggers; B-roll at real speed.
- [ ] `qc_final.py` all PASS (1080×1920, fps, -14 LUFS, ≤ -1 dBTP, no black frames).
- [ ] End card present and complete if the brand uses one.
