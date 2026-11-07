# House style (the user's standing editing rules)

These are the user's own rules from their notes in chat. They override the generic defaults in
`motion-design-rules.md`. When the user gives a new standing rule in chat, add it here.

## Workflow
- Frames first, every video and every change round (user rule, 2026-11-03): before rendering any video, render each changed
  moment as a still frame (plus 2–3 design options for any new motion graphic), lay them out as a storyboard, and post them to the
  Review Player image board (`/board?dir=...`) for comments. Render the video only after the user approves the frames.
- Review notes in the Review Player or chat are standing rules: save each one here so it applies to every future video.
- Change only what the note asks for (user rule, 2026-11-03). Never add anything the user didn't ask for: no extra subtext,
  Latin names, disclaimers, halos or captions. Never touch finished or approved parts while fixing another note. After every
  render, run the change tracker (`Review Player/change_tracker.py old.mp4 new.mp4 --expect ranges`) and confirm the
  only frames that changed are inside the requested ranges.
- Never speed up or fast-forward B-roll. Use the part of the clip that fits the line, at its real speed, even if
  that leaves part of the clip unused.
- Herb/item cards appear exactly on the spoken word, and no camera zoom snaps happen during a full-screen graphic slide.
- Approved frames are locked: never re-render or redesign them. Next round, only frames with comments get a new version, shown
  first on the board. Superseded images move to `_old/` and their comments are marked done.
- Work in the sequence the user gives. Never create a new sequence, and never cut, trim or retime their edit.
- Approval first: before creating anything in Premiere, show every transition, super, subtitle and motion
  graphic on a real frame of their footage (an approval page with rendered frames, plus a full preview
  MP4). Build in Premiere only after they confirm.
- Where things are built (user rule, 2026-11-04): supers, all text, background boxes and shape layers are Premiere text/shape
  layers, editable in Premiere. Never build supers in After Effects. Use AE only for animated graphs, charts and bar animations
  (Dynamic Linked). Flashes are a white still with Opacity keys in Premiere; zooms use Motion Scale keys in Premiere.
- Music for a hook runs long past the hook's end (the full track) so the user can lay the Common Body after it; duck it only
  under the hook's voice.
- Build graphics with HyperFrames (local CLI). Render one transparent ProRes 4444 overlay at the
  sequence's size and fps, and put it on a new track above the B-roll. For text behind the person, render
  a person cutout (`npx hyperframes remove-background`) and place it on the track above the text.
- Build the review preview from the source clips with hard cuts, so it matches the final edit.
- Raw iPhone footage is HDR (HLG, BT.2020). Every ffmpeg preview or render made from it must be tagged SDR at the end
  (`setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv`, yuv420p), or browsers and players switch to
  HDR and the video flashes. Also cut each segment to an exact frame count (`-frames:v`), never only `-t`. (2026-11-04)
- Preview builds (2026-11-05): give every segment `setsar=1` and join them with the concat *filter* (not concat-demuxer copy),
  or cuts can drop or freeze frames. Blend 24 fps AI B-rolls to 25 fps (`framerate=fps=25`) instead of repeating a frame
  every second; in Premiere turn on Frame Blending for them. Supers must never sit on a face: if the next shot's face is
  high, move the group below the chin for that shot.

## Colour
- Colours change per project. Never carry a palette over from an earlier video; use the palette the user
  gives for this project, or ask for one before designing. The colours named below are from past jobs.
- Build each palette as a calm base (cream, warm grey, off-white or near-black) plus one or two loud
  accents. On dark scenes, let the accent glow (soft bloom, light leaks, coloured halos behind cards).

## Look (from the user's reference board, 2026-11-02)
Reference files: `/Users/sajid.ali/Documents/REF/Reference/` (14 videos) plus 5 images (palette room,
galaxy, Brutalism poster, manga sketch, VaultBank app UI).
- Mix both sides: clean premium (glass and rounded UI cards, soft shadows, hatched fills, real UI mockups)
  with gritty editorial (film grain, halftone dots, photocopy contrast, B&W photos with accent overlays).
  Every frame should hold up as a designed poster, not a template caption.
- Type: huge condensed heavy display type that fills or crops off the frame, often behind the speaker.
  Pair a bold sans with an elegant italic serif in the same line. In each phrase, give one key word the
  accent colour, a highlight box or a size jump. Add small editorial details (tiny uppercase micro-text,
  vertical side text, barcodes, labels) and faint grid paper behind type.
- Captions: small clean words beside or below the speaker that pop in word by word; on punch lines, a
  full-screen word slam with motion blur, or a hard cut to a white/colour type card and back.
- Motion: snappy, eased (overshoot and settle, never linear), motion blur on big moves. Use depth: 3D card
  carousels, floating and orbiting objects, parallax layers, and camera pushes that flow between graphics
  (no fades or dissolves, per Transitions below).
- Text entrances are smooth and whole: a line or word block settles in from blur (about 16–22 px → 0) with a
  small rise and a long ease-out (power3.out, 0.8–1.0 s). No letter-by-letter "tuck tuck tuck" staggers, no
  sliding/whip-in cards, no bounce. Leave a little breathing space between beats; a slow, smooth camera push
  and parallax keep it alive. (User note, 2026-11-02.)
- Explaining a concept: glass UI cards, chat bubbles stacking, a cursor clicking, text typing into a
  prompt box, numbers counting up.
- Reactions: emojis and cut-out 3D objects (bulb, briefcase, chess pieces); occasional illustrated or
  comic-style accents.

## The user's own edit style (from Hook 3 Copy 01_1.mp4, Kapiva LCJ, 2026-11-03)
- Supers: white or accent heavy grotesk, italic for the accent word (AYURVEDIC HERBS, BEAUTIFULLY), one line above the head.
- A big numeral beside stacked lines ("5 AYURVEDIC HERBS"); count-ups in big bold numerals (500+).
- Lists as a dark rounded checklist card with green tick circles and a small header line; herbs as app-icon style
  rounded-square glass tiles with the image and a bold label, popping beside the subject.
- Bottom-of-frame dark gradient under bold geometric subtitles; claim lines as a bold headline over a light condensed line.

## Transitions
- No fades, cross dissolves or wipes anywhere. Remove existing ones (cuts stay unchanged).
- At cuts use instant zoom-in / instant zoom-out (a 1–2 frame snap, about 100↔115%). At section changes (cut to a new
  setup, to the product, to B-roll) a short white flash (peak ~85% on the cut frame, gone in ~0.2 s) is wanted too, with a
  swish/hit SFX (user note, 2026-11-03).
- No zooms (push-ins or snap zooms) in a stretch with many quick cuts, e.g. the first 20 s of a myth-buster hook: on top of the
  cuts they look abrupt (user note, Sonia Hook 1, 2026-11-05). Checklist boxes: plain white, no tick marks, no highlight colour.
  Music for these hooks should be energetic (e.g. BalloonPlanet – Peak Performance), not soft pizzicato.
- Slow push-in (about 100→108% over the phrase) while the speaker says an intense line; snap zoom (~112%) on punch words.
- On intense or emphasised words (for example "fatty liver"), add an instant zoom-in on the word.

## Supers (big highlight text)
- Thick and on one line (user note, 2026-11-03): a heavy sans (Inter Black) for each super, the phrase on a single line
  ("FATTY LIVER", not FATTY / LIVER stacked), never a condensed face like League Gothic.
- Supers are white (review notes, 2026-11-03): don't use green or lime for type. Keep supers modest in size with room on the
  sides (FATTY LIVER at about 620 px wide on 1080), not edge to edge. Lockups too (5 AYURVEDIC HERBS at about 600 px wide).
- White type must always pop: bright white (#FFFFFF) with a proper drop shadow behind the text, offset down and right like
  Premiere's Drop Shadow: about 40% opacity, small distance, softness about 5. No dark halos, blobs or glows above or around
  text (rejected 2026-11-03: "looks odd", "like the top of the text"). Check every white super against its actual frame.
- Centre CTAs (ORDER NOW) on the frame axis; don't push them to one side.
- Boxes and their spacing are a standing rule for every video: even gaps, boxes placed precisely on a grid or axis, and
  text that never touches or crosses a box edge (measure the longest label and size the box from it).
- Motion graphics for items (herbs, features, ingredients) should look premium, not like flat boxes. Follow the SaaS motion
  references in `REF/Reference/Saas motion*.mp4`: frosted glass cards with glowing gradient edges, orbit rings with icon
  bubbles around a glowing core, 3D card carousels with depth, soft gradient light backgrounds, light shafts and grids.
- Brand/claim lockups follow the user's edit: a heavy white line over a light (Inter 300) white line of the same width,
  with the light line's words landing as they're spoken (KAPIVA / LIVER CARE JUICE, REDUCE FAT / INFLAMMATION FROM LIVER).
- Kinetic word runs (simply, ayurvedically, beautifully) use one font size, weight and position for every word, so it
  reads as one continuous frame; don't resize words to fit a width.
- Text in a box must always fit inside it with padding: size the box to the text, never the text to a fixed box.
  Stack list boxes one per row (BURPING / FARTING / PET DARD) with space between them.
- Never put a person cutout over B-roll: a cutout starts only after the B-roll cut.
- CTA (ORDER NOW): one line, not split and not at the bottom. A white rounded pill on the side with a 3D cart icon
  (Fluent 3D emoji works) and black text; rises in like the supers, then a clean press (scale dip + ripple), with no cursor.
- Counts like 30 ML: no flat cartoon cups or glasses. Use a real 3D asset or type alone: heavy count-up numerals plus a thin unit,
  tipping in from 3D.
- Screen replacements (phones) are tracked: corner-track the green screen each frame and perspective-warp the new
  screen onto it, never a static overlay.
- Precise alignment: lockups share exact edges (same width, centred on the frame axis), and stacked lines line up to a big
  numeral's cap height and baseline ("5 | HERBS / KAPIVA LIVER CARE JUICE"). Solve sizes from measured glyph widths; never
  stretch glyphs to fit. Grids, pills and cards are centred on the frame axis too.
- Formation: one thick line in the project accent plus one medium line (white, bold sans, smaller), like "5 HERBS / KAPIVA LIVER CARE JUICE".
  Keep brand lines together on one line (KAPIVA on top, LIVER CARE JUICE directly under it).
- Big, reference-sized type, and placed behind the person's head (cutout on top), about 30–55% covered.
- Animation: pop out and come back (overshoot scale, then settle); medium line slides in from the left.
- CTA split: ORDER behind the head at the top, NOW in front at the bottom.
- Use the speaker's exact words; never invent numbers or rephrase.
- On talking heads, supers rise from behind the person into the empty space above their head.
- When the line is only the key phrase (e.g. "FATTY LIVER"), the super is that phrase alone, with no medium line.
- A spoken list (e.g. burp, fart, pet dard) becomes parallel boxes that appear one by one as each word is said.
- Instagram videos: the Reels safe zone applies only to supers, highlighted words and animated graphics, not to
  subtitles, inserts, screen recordings or end cards. Margins for 1080×1920: about 220 px top, 420 px bottom,
  60 px left and 120 px right (the like/comment rail). Mark them as edge bands on storyboards, not a big box.
- Never put text on the face line or eye line. Supers, cards and numbers (e.g. 500+ studies) go above the head
  or in clear space beside it; a front-of-person CTA word (e.g. NOW) goes below the chin. (User notes, 2026-11-03.)

## Lists, numbers and kinetic words
- Ingredient/herb lists (approved, Kapiva LCJ 2026-11-03): a SaaS slide. Cut to a full-screen soft white-on-white gradient
  background with slow abstract animation (drifting gradient blobs, light shaft, faint grid). Frosted herb cards (photo, name,
  Latin name) slide in one by one as each is named. The herb being named is highlighted front and centre, and earlier cards
  slide left, turn away and blur. The rest arrive on "etcetera". Never wrap herbs around the product or bottle.
  The ending to reuse (user: "remember this for future reference"): every card settles into a centred grid at half size
  (3 + 2 for five items) with even gaps, nothing overlapping, and every name and Latin name fully readable.
- Motion library, keep for later: the orbit path (glass bubbles on a tilted glowing ring) was liked. Offer it when a
  "many things around one core" moment comes up or when stuck for an idea.
- Older option, items that arrive one by one (herbs, features) each sit in their own tile, laid out as a grid (2 columns for 5
  herbs), with the item's image in a gold-ringed circle that gently hovers.
- Three words said in one frame (e.g. burp, fart, pet dard) use flat 60–70% white pill boxes side by side.
- Don't stack two ideas in one graphic: if the line lists 5 herbs, the "500+ studies" proof gets its own frame.
- A measured amount (e.g. 30 ml) is a count-up motion graphic with a measuring scale, tracked to the glass or
  bottle whenever it is on screen.
- A run of words like "simply, ayurvedically, beautifully" plays one word at a time near the head: each comes in,
  then fades out before the next. Never all at once.
- Images for real things (herbs, ingredients): ask the user which images they have before sourcing from
  Pinterest or the web.

## AI B-roll
- When a shot needs AI-generated B-roll, list it with why it is needed, ask which tool or website the user will
  use, then write a prompt tailored to that tool. The user generates it and drops the result in chat.

## Subtitles
- Text overlay, not a Premiere caption track.
- Hindi speech is written in Hinglish (Hindi in English letters); English words stay as spoken.
- White Montserrat Bold, about 72 px at 1080×1920, 2–3 words per group, in the lower third below the chin,
  never over the face (move them lower on close framings).
- Always put a dark gradient across the bottom of the frame (clear at ~55% height to ~70% black at the bottom) so the
  subtitles pop; fade it out while a graphic sits low in frame. Poppins Bold ~66 px matches the user's own edits. (2026-11-03)
- Hidden while a super or motion graphic is on screen.

## Motion graphics
- TV/broadcast style, and each one a different kind (badges, document stacks, cups, meters), not more text.
- No tagline bars or extra brand strips unless asked.

## Typography per video (user rule, 2026-11-03)
- Never use the same typography on every video. For each new video, pick the topic, the format and the tone, then choose
  the type family and accent from `references/kapiva-style-system.md` (learned from the 7 Kapiva reference reels).
- Work in the editor order from `references/kapiva-style-system.md` (Part 2): tone → storyboard → colour/backgrounds →
  typography → spacing → audio plan → cut → B-roll → motion graphics → type motion → transitions → overlays → mix → sync QC.
  Improvise the look per video within that order (user, 2026-11-03).
- Before exporting a video, ask the user which folder to export it to, once for every project (never reuse another project's folder). Same project, later versions: same folder (user rule, 2026-11-03).

## Approved super typography (user rule, 2026-11-04) — use this family for every super
The user said earlier typography was "very poor". Supers must come from THIS family (copied from their REF/Talking Head
videos + REF/Kapiva Style reels). Pick the style that fits each super, improvise within it, and change colours to suit the
topic (e.g. trading green #089981 / red #F23645). Library + generators: `Documents/Claude/Typography Library/`
(`gen_v2.py`, `gen_supers.py`; approved stills on the Frame Board, `screens_v2/` and `screens/`).
- **Caps lead + red italic box** (KP 01): Inter Tight SemiBold caps line, then Inter Tight Black Italic caps in a solid red box; optional line icons under it.
- **Caps lead + half-bar (+ script)** (MIX 01): caps lead, then Montserrat ExtraBold word on a red bar that covers the lower
  ~60 % of the letters (tops stay ink on white / white on video), optional Mrs Saint Delafield script tail and icons.
- **Light lead + heavy word + brush stroke** (MIX 06): Montserrat Regular lead, Montserrat ExtraBold word (tight -0.045em), a thick yellow/accent brush stroke under it.
- **Caps tag + bold word + coloured italic** (MIX 07): tracked grey caps tag, Montserrat Bold word, Montserrat Italic line in an accent colour.
- **Lead + skewed highlight bar (+ script tail)** (Type 03 / MIX 08): Inter SemiBold lead, Inter Tight Black Italic word in white on a skewed red bar, optional script tail.
- **Mixed weight lines** (Type 08): small setup line, big red payoff line, small line, big ink line.
- Herb lockup (KP 04 notes): herb name Montserrat Bold caps; benefit line in two caps sizes, scaled so it is exactly the name's width, one line.
- KP 03 number lockup copy is "5 AYURVEDIC HERBS".
- Use only the exact super text from the script; split it across the style's roles (lead / hero / tail) instead of adding words.
- Show supers as stills on the Frame Board first: one in an approved style + one improvised version per super.
- Approved improvised styles (Onkar supers, 2026-11-04), also part of the family:
  - **Lead + coloured half-bar word + script tail** (B2): small Montserrat lead, Montserrat ExtraBold word on a half-bar in an accent colour (e.g. trading green), Mrs Saint Delafield script word overlapping under it.
  - **Bold word + coloured script + skewed ink bar** (B3): Montserrat ExtraBold line, red script line under it, then Inter Tight Black Italic caps in white on a skewed black bar with the key word in red.
  - **Ghost word + caps lead + red italic box** (B5): huge light-grey ghost of the key word behind, Inter Tight SemiBold caps lead, Inter Tight Black Italic caps in the red box.
- Onkar Hook 3 frame notes (2026-11-04): supers in ALL CAPS (THE FATTY LIVER, STRATEGY); a half-bar sits flush to the bottom of
  the caps; tail lines use a normal font's italic, not a script font. When the text grows, keep the background bar/box the same
  size and let the text run past it. Trading/stock beats get a real candlestick chart (candles, wicks, volume, price line),
  not a plain line.
- Not picked (avoid unless asked): MIX 07 for "QUICK Exit strategy", dashed stop-loss line with SL chip, grid + green 3D extruded word.

## From the Onkar LCJ storyboard notes (2026-11-03)
- Sublines under a headline are big and premium: about 42 px caps with wide tracking, on a glass chip with a soft accent
  tint and a fine light border, sized up so it reads at a glance. Every piece of text gets the drop shadow, always.
- No home-made illustrations ("I don't want Claude's design"). Use real imagery: the user's B-roll, assets from past
  projects, or images from the internet, cut out (still frame → remove background). Generic drawn shapes are rejected.
- When the speaker gestures "this → this", show each item in a premium glass box that tracks the hand that presents it,
  appearing on the word (first item, then the second on the next hand).
- Don't put themed decoration (e.g. trading bars/candles) on every frame.
- Negating an item (junk food, etc.): the item pops up in the middle inside a white rounded box that slides up, with a
  red overlay blink and a clean, well-drawn cross. No cartoon/childish crosses. Hide brand names on props.
- When the speaker names a habit or action (walk, eating chips…), show the headline on the speaker first, then cut to a
  B-roll of that action; write prompts for the B-roll the user will generate.

- SFX: pick them from the user's Artlist account (search_sfx → download_track as WAV) when the project folders don't have
  the right sound: swish on flashes, deep hit on big section changes, impact swell on snap zooms (user note, 2026-11-03).

## From the Onkar Body storyboard notes (2026-11-03)
- B-roll always plays full frame, never inside a box or card.
- Herb/ingredient beats use the user's own herb B-roll videos (they open on the herb itself, then show the benefit): show the
  herb part on its name, then the benefit part. Don't swap in stock herb cut-out cards when the user has videos.
- Big claim lines: two lines, big, a script/elegant italic word paired with a thick heavy line (not one plain line of caps).
- A follow-up "pop" chip for a positive claim (e.g. MAXIMUM EFFICACY): bluish gradient box with white, not black.
- Dosage: the number + unit huge (30 ML), the rest on a smaller regular white line under it, plus the frequency (TWICE DAILY).
- Duration claims (30 / 60 / 90 days): a premium animated chart/graph that marks each milestone, not just a headline.
- Labels/supers on B-roll: ALL CAPS, centre-aligned text in a box centred on the frame axis; light (white/frosted) gradient
  boxes over bright lab B-roll, not dark green glass. A herb's label stays on through its benefit B-roll (Onkar Body v2 notes).
- Sonia BPXJ Hook 1 storyboard notes (2026-11-05): no emoji/icons on symptom B-roll frames (label box only); stacked
  checklist boxes are centred on the frame axis at one width, one line each; herb names are typography only (no box);
  in a claim like "Aloevera pulp is visible" only the key noun phrase goes in the green box. Storyboard stills carry no
  VO/notes box: put notes in chat, not on the image.
- Keep claim type simple when asked ("just simple"): plain thick caps over two lines, no script word.

## "Bold and slimmer / bold and light" text combo (approved 2026-11-05)
When the user asks for "bold and slimmer" or "bold and light": two lines, all caps, white, centred, tight leading.
Top: Jost Bold 700 (~124 px at 1080 wide, -0.01em). Bottom: Jost Light 300 (~70 px). Soft drop shadow.
Optional: top line in Kapiva lime #C6F23A, or left-aligned. Use only when asked; don't replace approved supers.
Reference: `Documents/Claude/Kapiva BPXJ – Sonia/hook1/two-line options/` (option A).
