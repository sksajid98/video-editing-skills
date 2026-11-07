---
name: brand-kapiva
description: Applies the Kapiva client brand (modern Ayurveda nutrition, with olive and leaf greens, terracotta accent, Jost type, and the black KAPIVA badge logo) to anything made for Kapiva, including product reels, ads, YouTube and Instagram videos, Premiere titles, lower thirds, captions, end cards, After Effects motion graphics, thumbnails, decks, PDFs and social posts. Use this whenever the user mentions Kapiva or a Kapiva product (Dia Free, Karela Jamun, Liver Care Juice, juices, atta mix, tablets), says Kapiva style or Kapiva brand, or is editing a video, project folder or file named for Kapiva, even if they don't say brand. Not for the user's own brand (use brand-book) or other clients.
---

# Brand: Kapiva (client)

Makes everything for Kapiva look and sound like Kapiva. This is a remix of the user's brand-book skill, so the
user's own brand stays separate. The brand values are in `references/brand.md` and the logo is in
`assets/kapiva-logo.png`.

## 1. Load the brand

Read `references/brand.md`. Its values came from Kapiva's live website CSS and the official logo, not from
guesses. If the user hands over an official Kapiva brand book later, update brand.md from it (the brand book
wins over the website).

## 2. Apply it, by output type

| Output | How to apply |
|---|---|
| Video titles / lower thirds (Premiere, AE) | Jost SemiBold/Medium, in Olive or Ink on a White/Sage plate, or White on Olive. Terracotta for a single highlight only. Build through the video-studio skill |
| Captions | Jost Bold, White with a thin Ink stroke or shadow. Highlight word in Leaf Green. Sentence case |
| End card / packshot | White or Sage background, black badge logo centered, product name in Olive, one CTA line, disclaimer in Grey |
| Thumbnail | Olive or Sage background, product hero shot, max 4–5 words in Jost Bold, one Terracotta accent (with Ink text) |
| Deck / PDF / doc | White background, Olive headings, Ink body, Sage callout boxes, Leaf for charts and data |
| HTML / artifact | Palette as CSS variables on `:root`, Jost from Google Fonts |
| Copy | Voice section of brand.md, plus the health-claim rules in Gotchas |

Use colors **by role** (background, text, primary, accent), never all at once.

## 3. Check before handing over

- Every color is from the palette in brand.md (Olive #506000, Leaf #80A03C, Ink #1E1E1E, Sage #EDEFE5,
  Terracotta #C97B5A…).
- Text contrast is at least 4.5:1 (brand.md lists the measured pairs). Leaf Green and Terracotta fail with
  small text, so use Olive or Ink for text.
- Jost is used, with Nunito/Arial as the fallback. Check that Jost is installed before building in AE/Premiere.
- The logo is the original black badge, never stretched, recolored, outlined or dropped on busy footage
  without clear space.
- Health claims use the safe wording (Gotchas).
- Files are saved in `/Users/sajid.ali/Documents/Claude/<Kapiva project name>/`.

## 4. Update the brand

When the user shares an official Kapiva brand book, new logo files or client feedback: update `references/brand.md`
(keep its layout), add the logo variants to `assets/`, and record the source and date in brand.md. Then run
`bash ~/.claude/skills/skill-forge/scripts/install_skill.sh ~/.claude/skills/brand-kapiva`.

## Gotchas

- **Health-claim wording.** Kapiva sells Ayurvedic health products, which are regulated in India (ASCI, AYUSH).
  Say "helps manage", "supports", "may help". Never "cures", "treats", "guaranteed", "replaces medicine". Never
  make before/after promises. Add "Consult your doctor before use." when copy talks about a condition (sugar,
  liver). A wrong claim can get an ad pulled.
- **Leaf Green or Terracotta for small text** fails contrast and looks washed out on phones. Use them for shapes and highlights.
- **Too much green** makes it look like a generic organic brand. Keep big areas White/Sage, and keep Olive for type and key blocks.
- **Jost missing in AE** silently falls back to Arial, and the geometric look is lost. Install it from Google Fonts first.
- **Logo on footage**: the badge is solid black. Put it on a clean area or end card, not over busy B-roll.
- **Mixing up brands**: never apply Kapiva colors to the user's own content, or brand-book values to Kapiva work.
- **Product names**: copy them exactly from the label or kapiva.in (e.g. "Dia Free Juice", "Karela Jamun Juice").
  If unsure, ask the user. Don't guess.
