# Kapiva style system (from 7 reference reels, 2026-11-03)

Source: /Users/sajid.ali/Documents/REF/Kapiva Style*.mp4. Full board + PDF:
/Users/sajid.ali/Documents/Claude/Kapiva Style Breakdown/board/ (Kapiva Style Breakdown.pdf).

## Rule: never reuse the last project's typography
For every new video: 1) name the format (who talks, where), 2) name the tone in one word, 3) pick type + accent below.
Only reuse a family when the format is the same.

| Format / topic | Tone | Type | Accent | Ref |
|---|---|---|---|---|
| Expert warning (doctor vox-pop, news proof) | Urgent | Montserrat Medium + ExtraBold Italic caps | Red box #E3232C on alarm words | v1 |
| Educator / home remedy / myth-buster | Friendly | Poppins ExtraBold + SemiBold, sentence case | Lime #C6F432 key word, word-by-word captions | v2 |
| Relatable symptom, moody lifestyle set | Dramatic | Anton (heavy condensed) + Inter Bold | Yellow #FFE600 + red #E10600, giant numerals | v3 |
| Podcast / case story | Conversational | Montserrat Light + SemiBold, size jumps | White only | v4 |
| Doctor authority, clinic | Clinical, premium | Outfit Medium/SemiBold caps in translucent olive boxes | Olive #5B6B2E | v5 |
| Celebrity, warm/witty | Trusted, minimal | Inter SemiBold captions on 60% dark pill, no supers | none | v6, v7 |

Topic hints: BP/heart → urgent red; cholesterol/digestion → friendly lime; sleep/stress → moody yellow;
sugar → clinical olive or warm celebrity; liver/detox → clean bright science.

## Constants across all 7
- Story spine: hook → problem → science → product → herbs → usage/safety → jungle end card (typing www.kapiva.in + marketplaces).
- Max 2 families (usually 1 family, 2 weights). Lockup = small setup line over a big punch line of the same width.
- One accent device per video (colour box OR colour word OR size jump).
- Captions 2–5 words Hinglish, centred at chest/table height (52–72%), above a legal micro-text band (92–98%).
- Supers in the headroom (12–28%) or across the chest; never on the eye line.
- Cuts follow speech, not the beat (only 20–35% of cuts land on a beat, about chance). Music is a low 94–117 BPM bed; avg shot 1.9–3.8 s.

## Layout devices
Split screen (50/50 stacked), PiP rounded card (top 60–65%, speaker cut-out bottom 35%), floating glass UI card
beside the head, herb-drop into a glass (one herb per beat), herb slide (lockup top, object centre).

## Transitions
Hard cut on speech (default), punch-in/out on emphasis, letter/word reveal, text slam with overshoot (dramatic tone),
zoom-blur whip, juice-splash wipe, card slide/PiP, article proof with red circle, glitch logo → end card.

## B-roll worlds (pick one per video) + Flow/Veo prompt pattern
3D medical CGI (artery, organs), studio herb hero on grey gradient, overhead herb flatlay around the bottle, warm AI
apothecary, practical herb drop in a glass, liquid splash, lifestyle drinking, lab scientist, petri-dish herb grid.
Prompt = camera + subject + action + context + style, 9:16, end with "No text, no subtitles." Example prompts are on
page 06 of the PDF.

# Part 2 – editor's playbook (deep breakdown, 2026-11-03)
PDF pages 08–19 and the matching Figma frames. Data: `Kapiva Style Breakdown/scripts/deep_data.py`; measurements in
`analysis/audio.json`, `analysis/colour.json`, `analysis/music.json`.

**House rules win over the references.** The references use letter-by-letter reveals and light wipes; the user's
house-style forbids fades/dissolves and "tuck tuck" letter staggers. Use the references for layout, type choice,
pacing and audio, and animate with the house entrances (whole line or word settles in from blur).

## Workflow order (do in this order)
1 Brief & topic → 2 Format & tone → 3 Storyboard beat sheet → 4 Colour & background theme (graphics/slides only, never
grade footage) → 5 Typography system → 6 Spacing grid → 7 Audio plan → 8 Rough cut & rhythm → 9 B-roll → 10 Motion
graphics → 11 Type motion → 12 Transitions → 13 Overlays → 14 Audio mix & vocal → 15 Storyboard sync & QC.

## Storyboard sync
Super starts on the first frame of its word, holds 1.5–3 s. Captions 2–5 words, swap on phrase ends, hidden under
supers. B-roll starts on the noun it proves (0.5–2 s, real speed). Product reveal at 30–66% of runtime (celebrity early,
case story late). One herb per spoken name. Count lockup on the number word. End card last 3–4 s.

## Rhythm
Voice drives the cut (cuts land on beats only at chance level). Average shot 1.9–3.8 s. Energy from punch-ins,
type slams and insert length. Podcast/expert = fast inserts; educator/clinical = long takes broken by cards.

## Spacing (1080×1920, approx.)
Side margin 60–80 px (cards 40–48). Headroom supers y 230–540. Chest supers y 860–1060. Captions y 1000–1380,
42–52 px. Legal micro-text y 1770–1880. PiP card top 60–65%, 24 px radius. Lockup ≤ 860 px wide. Punch line cap
≈ 110–160 px, setup line ≈ 60–80 px.

## Colour & backgrounds
Measured shoots: v1/v3/v4 dark (brightness 0.32–0.43), v2/v5 bright (0.53–0.56), v6/v7 warm olive (warmth +0.17,
sat 0.41–0.44). Slide backgrounds: studio grey gradient, white/pale-blue explainer, dark tabletop, warm wood & golden
light, overhead herb flatlay, glowing CGI void, jungle end card. One accent colour per video.

## Motion graphics & overlays
Lockup (setup + punch), highlight box, icon card + progress ring, glass data card with count-up, stacked split cards,
PiP explainer card, diamond grid, herb slide, count lockup, document proof, monitor counter, body infographic, end card.
Overlays: bottom gradient + 2-line legal text, translucent label box (60–70%), caption pill (black ~60%), glass card,
motion-blur whip, juice splash/particles, slide vignette.

## Audio (measured from the mixes)
References: -12.9 to -22.2 LUFS (inconsistent), voice 13–28 dB over the bed, voice mono/centred.
SFX on graphic entrances in graphic-heavy tones (v2 11/15 cuts, v3 13/15, v5 12/23); almost none in podcast/celebrity.
My mix: -14 LUFS, -1 dBTP. Voice: HPF 70–80 Hz, -2–3 dB at 250–350 Hz, +2–3 dB at 3–5 kHz, de-ess 6–8 kHz, 3:1
comp 4–6 dB GR, light NR outdoors. Bed under voice: urgent/dramatic -12 to -15 dB, friendly/clinical -15 to -18,
celebrity/podcast -18 to -22; duck 3–4 dB more under fast speech; +4–6 dB on the end card. SFX 6–10 dB under voice peaks.

## Recipes by tone
Urgent: Montserrat + red box, CGI medical + proof, dark cinematic bed. Friendly: Poppins + lime, icon cards, light pluck,
pops. Dramatic: Anton yellow/red slams, practical tabletop, punchy beat + hits. Conversational: Montserrat size jumps,
fast proof inserts, hidden lo-fi. Clinical: Outfit on olive boxes, PiP cards, warm AI organs, airy ambient + whooshes.
Warm celebrity: caption pill only, punch-ins, flatlay/warm product, acoustic bed, no SFX.
