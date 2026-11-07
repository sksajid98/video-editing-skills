---
name: video-idea-finder
description: Finds the user's next video idea before any script is written, in 3 steps. First it researches outlier videos in their niche from the last 30 days, grouped into repeating patterns. Then it interviews the user one question at a time to find 3 ideas only they could make. Finally it tries to kill the chosen idea and gives 10 hooks. Works for Reels, Shorts, TikTok and YouTube. Use this whenever the user asks for video ideas, content ideas, what to post next, what's working or trending in their niche, viral or outlier videos, a content angle, or ideas for a client like Kapiva. Also use for "stress-test my idea", "will this go viral", "roast my video idea" or "give me hooks for this idea", even if they don't say the word idea. Not for writing the script itself (hand off to reel-script-writer) or editing footage (video-studio).
license: Method credited to Ikjot Juneja (Substack, 29 Oct 2026). Wording and script written for this skill.
---

# Video Idea Finder

Asking Claude "give me video ideas" gets generic ideas. This skill flips the order: study what already won,
add what only the user knows, then try to break the idea before anyone films it. The output is one tested idea
with 10 hooks, ready for `reel-script-writer`. The method's source and prompt wording are in `references/method.md`.

## Inputs
- **Niche and platform.** The user's own channel, or a client (e.g. Kapiva: Ayurveda, health juices, India).
  If missing, ask once in one line. Platform default: Instagram Reels + YouTube Shorts.
- **An idea already in hand?** Skip to step 3. **Only want trends?** Stop after step 1.

## Step 1: Find what already won (outliers)
An outlier is a video far above its *own channel's* normal views. Big accounts get big views on everything,
so "most viewed" teaches nothing. A small channel doing 10x its median shows a topic or hook that pulls by itself.

1. Research the last 30 days with WebSearch (`mode: "extended"`, several searches in one turn: niche + "reel",
   "shorts", "viral", competitor names, hashtags). For view counts, open the channel or video pages with the
   built-in browser (`get_page_text`). Never invent a number.
2. For each candidate, record the channel, title, url, views, publish date and the channel's typical views (the
   median of its last ~10 videos, or 5+ rows in the CSV). Save them to
   `/Users/sajid.ali/Documents/Claude/<Project>/ideas/videos.csv`.
3. Rank: `python3 ~/.claude/skills/video-idea-finder/scripts/outlier_score.py <csv> --days 30 --top 10`.
4. Tag each of the top 10 by hook type, topic and format, using the labels in `references/method.md`. Then
   name the **3 patterns** that repeat (e.g. "myth vs fact + doctor talking head + one ingredient").

If fewer than 10 can be verified, show the ones you have and say how many. Don't pad with guesses.

## Step 2: Interview the user
The patterns are the skeleton. The user's experience makes the idea theirs, and nobody can copy it.

- Ask **one question at a time** (plain chat, not AskUserQuestion), then wait. Build each question on the last
  answer: a story, a mistake, a customer question, a number, a strong opinion, something they do differently.
- Tell them once to answer casually, like talking to a friend. Good ideas often show up around question 4–5.
- Stop after 5–8 questions, or as soon as you can name 3 ideas that each (a) follow one of the 3 patterns and
  (b) use a detail only they gave you. For each idea give: title, pattern used, the personal detail, and one line
  on why it should pull. Ask which one to test.

## Step 3: Try to kill the idea
Being harsh is the point. Weak ideas should die here, before a filming day is spent on them.

1. **Weakest part**: the one thing most likely to make people scroll (too broad, already done, no stakes, slow
   payoff), and how to fix it.
2. **Comment pushback**: the 3–5 objections viewers will post, and which one to answer inside the video.
3. **10 hooks**, each from a different angle (shock number, contrarian claim, question with stakes, I tried X,
   warning, before→after, list, named-person story, myth vs fact, insider secret). Each one names a specific
   thing, number or person, in 15 words or fewer.
4. **Verdict**: film it, fix it (one change), or kill it. If it's killed, go back to the next idea from step 2.

## Output format
Save to `/Users/sajid.ali/Documents/Claude/<Project>/ideas/<YYYY-MM-DD>-ideas.md` and show it in chat:

```
# Video ideas: <niche>, <date>
## 1. Outliers (last 30 days)
<table from outlier_score.py, plus Hook type | Topic | Format columns>
**Patterns:** 1) … 2) … 3) …
## 2. Ideas
1. <title> · pattern <n> · only-you detail: … · why it pulls: …
## 3. Stress test: <chosen idea>
Weakest part: … → fix: …
Pushback: …
Hooks: 1. … 10. …
Verdict: FILM / FIX / KILL
```

Worked example (Kapiva, step 3 only). Idea: "I drank Karela Jamun juice for 30 days". Weakest part: a 30-day
diary is common, and a sugar result would be a health claim. Fix: make it a habit story with no results promise.
Pushback: "paid ad", "tastes awful", "does it actually work?". Hook 3: "Everyone said it tastes like punishment.
Day 1 was worse." Verdict: FIX.

## Hand-off
When the verdict is FILM, offer `reel-script-writer` with the idea, the pattern and the best 3 hooks. For Kapiva,
`brand-kapiva` rules apply to every hook and idea.

## Scripts
| Script | What it does | When |
|---|---|---|
| `scripts/outlier_score.py` | Views ÷ channel median, filters to the last N days, ranks, prints a Markdown table, lists skipped rows | Step 1, after the CSV is filled |

## Gotchas
- **Invented view counts** make the whole analysis worthless, and the user can't tell. Only use numbers you saw on
  a page. Mark the rest "unverified" and leave them out of the ranking.
- **Ranking by raw views** surfaces celebrity accounts. Always rank by multiple of the channel median.
- **Old videos**: search results often show viral videos from past years. Check each publish date against the 30 days.
- **Asking all interview questions at once** gets short, generic answers. One question, wait, then follow up on
  the answer.
- **Ideas with no only-you detail** are just the trend again. If you can't point to the user's own words in
  an idea, keep interviewing.
- **Soft stress tests** defeat step 3. Name the real weakness even if the user loves the idea.
- **Kapiva / health niches**: hooks like "cured my sugar" break ASCI/AYUSH rules. Use "helps manage" or
  "supports", with no before/after promises (see `brand-kapiva`).
- **Instagram and TikTok pages** often hide counts without sign-in. Use YouTube Shorts data plus the counts
  that are visible, say which platform the numbers came from, and never sign in for the user.

## Done checklist
- [ ] Every ranked video has a real url, a date within 30 days and seen view counts
- [ ] 3 patterns named, each backed by 2+ of the outliers
- [ ] Every idea names its pattern and a detail from the user's answers
- [ ] 10 hooks with 10 different angles, each 15 words or fewer
- [ ] File saved under Documents/Claude/<Project>/ideas/
