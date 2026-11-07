# Motion design, typography and asset rules

Use this when building titles, lower thirds, kinetic type, logo stings or any graphic asset in AE.
Numbers are tested conventions for 1920x1080 at 24–30 fps. Scale them for other sizes, and break a rule
only when there's a reason to.

## 1. Purpose and restraint
- Every move needs a job: draw attention, show a relationship, give feedback, or set a mood. Cut motion that does none of these.
- One hero move per moment. Animate at most 2–3 elements at once and keep the rest still.
- Pick one motion language per project (one easing family, one duration scale, one entrance direction) and stick to it.

## 2. Timing (at 30 fps)
| Use | Duration |
|---|---|
| Small UI-style pops, icon bumps | 6–10 frames (0.2–0.33 s) |
| Text or element entrances | 10–18 frames (0.33–0.6 s) |
| Large moves, panel slides, scene transitions | 18–30 frames (0.6–1 s) |
| Exits | about 70–80% of the entrance duration |
| Stagger between letters / words / lines | 1–2 f / 2–4 f / 4–6 f |

- **Reading time:** text must hold still and be fully legible for at least 2 s, or about 0.3 s per word plus 1 s, whichever is longer. Lower thirds hold 4–6 s.
- Cut motion to the music. Land key poses on beats (use `detect_beats` in Premiere) and put big hits on downbeats.
- Leave 6–12 frames of stillness before the next move so the eye can settle.

## 3. Easing
- Never use linear motion for position or scale. Linear is fine only for opacity, color, and constant drifts or loops.
- **Entrances: ease out** (fast start, slow settle). **Exits: ease in** (slow start, fast leave). **Moves inside the frame: ease in-out.**
- AE easy ease (33%) is a starting point. For a premium look, open the speed graph and push the influence to 70–90% so the move has a sharp start and a long tail.
- Use overshoot and bounce (`inertia`/`elastic` expressions) sparingly: playful brands only, and at most once per graphic.
- Follow-through: secondary elements (underline, subtitle, icon) start 2–4 frames after the main element and settle after it.
- Anticipation: a tiny 2–3 frame counter-move before a big move makes it feel intentional.

## 4. Typography for video
**Typefaces**
- Use at most 2 families (one display, one text). Prefer weight changes within one family over adding a third.
- Pick sturdy sans-serifs with open counters and a large x-height (e.g. Inter, Montserrat, Proxima Nova, Helvetica Now, SF Pro). Thin hairline serifs shimmer and break up when compressed or moving.
- Use Medium to Black weights for on-screen text. Light weights only at large sizes on clean backgrounds.

**Size at 1080p** (scale ×2 for 4K, and use larger sizes for vertical 1080x1920)
| Role | Size | Notes |
|---|---|---|
| Hero title | 90–160 px | Tight tracking (−10 to −30), line height about 0.9–1.0 |
| Section title | 60–90 px | |
| Lower third name | 44–60 px | Bold/Black, Title Case |
| Lower third role | 28–36 px | Regular/Medium, about 60–70% of the name size |
| Captions / subtitles | 42–56 px | Max 2 lines, about 32–42 characters per line |
| Absolute minimum | about 24 px (cap height ≥ 18 px) | Nothing smaller, ever |

**Setting**
- Hierarchy has 3 levels: size, then weight, then color/opacity. Use at most 2 levers at once.
- Line length: 3–7 words per line for kinetic type. Break lines on meaning, not at a fixed width.
- Tracking: tighten large display text and loosen ALL CAPS and small text (+50 to +100).
- Leading: 1.0–1.2× for multi-line titles. Avoid widows (one word alone on the last line).
- Contrast: aim for at least 4.5:1, and 7:1 for small text. Over busy footage, add a bar or plate, a 20–40% black gradient, or a soft shadow (distance 0–4, blur 10–30, opacity 30–60%). Avoid hard 1990s drop shadows.
- Avoid pure #FFFFFF on pure #000000 in big areas; off-white (#F5F5F5) and near-black (#111) look better on screen. Keep graphics whites at about 90–100 IRE (`read_video_scopes`).

**Kinetic type techniques** (from subtle to loud)
1. Fade + 20–40 px rise, per line (the safe default)
2. Mask or track-matte reveal: text slides out from behind an invisible edge (the classic premium look)
3. Per-word or per-character stagger with Text Animators (Range Selector, offset by index)
4. Scale punch on the key word (100 → 110 → 100%) or a color or weight swap on emphasis
5. Camera moves through 3D text layers, plus motion blur (always turn motion blur on for fast moves: shutter 180°)
- Animate the words the voice says, timed to the transcript. The key word gets the biggest move.

## 5. Composition and layout
- **Safe zones:** title-safe is the inner 90% (≈96 px side and 54 px top/bottom margins at 1080p). Action-safe is 93–95%. For social vertical video, keep the top 14% and bottom 20–25% clear of key text (UI overlays), and keep text off the right edge where the button column sits.
- **Grid:** set up a 12-column grid, or at minimum rule-of-thirds guides, and snap every element to it. Keep the same margins on every graphic in a project.
- **Rule of thirds:** put focal elements on the lines and intersections. Lead room: leave space in the direction a subject faces or moves. Center only for symmetric, formal or hero moments.
- **Lower thirds:** left-aligned in the bottom third, inside title-safe. Never over faces or necks. Place them on the side opposite where the subject looks.
- **Hierarchy:** one focal point per frame. Guide the eye through scale, contrast, color, motion, and isolation (negative space).
- **Negative space** is a design element; don't fill it. Group related items close together (proximity) and separate unrelated ones.
- **Direction:** use a consistent motion direction for the whole piece, e.g. in from the left or bottom and out to the right or top. Reversing direction signals "back" or "undo".
- **Continuity:** the end of one shot's motion should lead into the next (match cuts, shape or color carry-over, matching velocity at cuts).

## 6. Designing assets (shapes, icons, logos, plates)
- Build vector shape layers rather than raster. Keep the stroke width the same across a set (e.g. 4 px at 1080p), and use the same corner radius everywhere (e.g. 8–16 px).
- **Color:** a 60/30/10 split (base / secondary / accent). Use one accent color for emphasis only. Pull colors from the footage or the brand kit (`validate_mogrt_brand_kit`).
- Build assets with hierarchy in mind. Plates and bars sit behind type at 70–90% opacity or as blurred glass. Never let an asset compete with the text it supports.
- Parent sub-elements to one null for the whole graphic so it can be moved, scaled and animated as a unit. Name every layer.
- Make it reusable: expose text, color and position as Essential Graphics properties (so it can become a .mogrt), and set the comp to the sequence's size and fps.
- Logo stings: 2–4 s total; the logo resolves by 60–70% of the duration and holds clean for at least 1 s. Respect the logo's clear space; don't distort, recolor or skew it.
- Polish: motion blur on, anti-aliasing high, no sub-pixel jitter (round position on still holds), and check the frame at 100% and at phone size.

## 7. Accessibility and QC checklist
- [ ] Every line readable for ≥ 2 s at phone size
- [ ] Contrast ≥ 4.5:1 against the actual footage frame (`capture_frame` to check)
- [ ] Inside title-safe / platform safe zones (`check_caption_safe_zone`)
- [ ] No flashing more than 3 times per second; avoid large, fast full-frame strobes
- [ ] One easing / timing system used throughout
- [ ] Fonts: ≤ 2 families, nothing under 24 px at 1080p
- [ ] Graphics whites within broadcast range; no clipped colors
- [ ] Motion supports the voiceover/music; nothing moves without a reason
