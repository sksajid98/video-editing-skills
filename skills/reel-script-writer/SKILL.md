---
name: reel-script-writer
description: Writes ready-to-record 60-second Instagram Reel, YouTube Shorts and TikTok scripts in the user's own voice, with a catchy hook, a plain-language body and their fixed call to action, from an article, link, topic, video transcript or notes. Use this whenever the user asks for a reel script, a short script, a 60-second script, a voiceover script for a short, or a hook for a reel. Also use when they paste or link an article and just invoke this skill with no other instructions, or say "turn this into a reel", even if they don't say the word script. Not for long-form YouTube scripts or captions on finished videos.
---

# Reel Script Writer

Writes one 60-second short-form script that sounds like the user wrote it, ready to read on camera or as a
voiceover. The structure is fixed and the voice comes from their real scripts.

## 1. Before writing

1. Read `references/voice-profile.md`. If it says `NOT SET YET`, run the setup (section 5) first. Without their
   real scripts the output is generic, and generic is the one thing this skill exists to avoid.
2. Read `references/examples.md` and study 5+ of their scripts: hook openers, sentence length, slang,
   how they explain, and how they land the CTA.
3. Get the source. With a link, fetch it. With a topic only, research the key facts first. Pull out the one
   surprising fact or stake that makes it worth 60 seconds.

## 2. Structure (always)

| Part | Length | Job |
|---|---|---|
| Hook | 2–3 lines, about 10–15 s (30–40 words) | Stop the scroll: a surprising fact, a bold claim, stakes, or "this just happened" |
| Body | about 40 s (100–110 words) | Explain it simply, one idea per line, a concrete detail or number, and why it matters to the viewer |
| CTA | the fixed line from voice-profile.md, word for word | Same every time. Viewers learn it |

Total: about 150–165 spoken words (about 2.6 words per second). Count before handing over.

## 3. Hooks (where most scripts fail)

Draft 3 hooks using different angles (shock fact, bold claim, question with stakes, a named person in a story).
Keep the one that is the most specific and creates the most open curiosity. Then cut its first line to its
strongest 8–12 words. Hooks that win name a thing, a number or a person. "AI is changing everything" names nothing.

## 4. Output

Give the script only, unless the user asks for more (no B-roll notes, on-screen text or emojis):

```
HOOK
<2–3 lines>

BODY
<short lines, one idea each>

CTA
<fixed CTA>

(~158 words · ~60 s)
```

After the script, offer 2 alternative hooks in one line each, so the user can swap.

Hand-off: ideas come from `video-idea-finder`. Once the reel is recorded, offer `video-studio` to edit it (it runs
`cut-silences` and `cut-mistakes` first). For Kapiva, `brand-kapiva` rules apply to the script too.

## 5. Setup (first run)

Ask in one round: (1) paste or attach 10+ of their past scripts (more is better, ideally 50–100); (2) their exact CTA
line; (3) the page or channel name and its niche; (4) platform(s). Save the scripts into `references/examples.md` and
fill in `references/voice-profile.md`: the CTA, the niche, and a voice summary you write from the scripts (tone,
typical openers, sentence length, words they use, words they never use). Set the status to `SET <date>`. Then write
3 test scripts from 3 different articles. Ask specific questions ("are the hooks catchy enough?", "is the diction
right?") and fold the answers into Gotchas as general rules. Finish with
`bash ~/.claude/skills/skill-forge/scripts/install_skill.sh ~/.claude/skills/reel-script-writer`.

## Gotchas

- **Generic hooks** are the main failure. If a hook would fit any video on the topic, rewrite it with the
  specific name, number or event.
- **Unsure of a name** (tool, model, person, company)? Ask the user for the real one. Don't write around it with
  "a new AI tool". A vague noun kills credibility.
- **Over 165 words** gets rushed on camera. Cut adjectives and repeated ideas first, never the CTA.
- **Changing the CTA wording** breaks the brand habit. Copy it exactly.
- **Copying source sentences**: rewrite in the user's voice. Never paste the article's lines.
- **Jargon**: if a 15-year-old wouldn't get a word, swap it or explain it in five words.

## Done checklist
- [ ] Hook names something specific and is 3 lines at most
- [ ] 150–165 words, one idea per body line
- [ ] CTA matches voice-profile.md exactly
- [ ] Reads like examples.md (read the first line aloud next to one of theirs)
