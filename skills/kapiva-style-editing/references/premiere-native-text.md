# Native Premiere text (no After Effects for supers)

The user wants every super, text and box as an editable Premiere graphic, one element per layer. AE only for
animated graphs/bars (Dynamic Link). The bridge has no "new text" call, so build `.mogrt` files from Premiere's
stock templates with `scripts/make_pr_text.py`, then place them with `import_mogrt`.

## The tool
```python
import sys; sys.path.insert(0, "/Users/sajid.ali/.claude/skills/kapiva-style-editing/scripts")
from make_pr_text import make, make_box
make(out, "WARM WATER", "InterTight-Black", 84*1.778, "#FFFFFF", tracking=-10)          # plain text (Basic Title)
make_box(out, "HEADACHES", "InterTight-Black", 84, "#121212", "#FFFFFF", box_op=90,
         box_vs=65.1, box_dy=(46.2-94*0.651)/1080)                                        # text + auto-width box
```
- **Text (`make`)**: stock templates are 1920×1080, so font size = CSS px × 1.778. Text centre lands at about
  y 980 px with default Motion → Position y = 0.5 + (target_cy − 980)/1920, x = 0.5 + (cx − 540)/1080.
- **Box (`make_box`)**: keep the template font at 84 and size the whole graphic with Motion Scale
  (scale = target_font_px / 47.25 × 100). Box height = `box_vs` % (ratio wanted ÷ 2.24 × 100); `box_dy` keeps it centred.
  Box centre ≈ (537, 1757) px → set Anchor Point (0.4972, 0.9154), then Position = (cx/1080, cy/1920).
- Tracking is in 1/1000 em (CSS -.01em → -10). Colours are "#RRGGBB". Rotation/opacity via Motion/Opacity.

## Gotchas (all learned the hard way on Sonia Hook 1)
- **BinaryHash**: every edited blob needs a fresh hash ending in len+12 (`_rehash`, built in). Without it Premiere's
  cache mixes graphics up and they render blank or wrong.
- **Never edit the box Path** (rounded corners, skew): any change renders nothing. Boxes are square; a red bar is straight.
- The caption template has a fade-in/out and bounce: the tool strips them (house rule: no fades).
- **import_mogrt drops the clip at default length first**, so it overwrites later clips on the same track. Place in
  time order, or on a free track, and check neighbours after.
- Removing an audio partner with `remove_from_timeline` also removes the linked video. Mute the track instead.
- Always pass `expected_cep_target {"backend":"cep","sequence_id":…}`; the user edits other sequences at the same time.
  On HOST_RECOVERY_REQUIRED: inspect, acknowledge, then ask before switching the active sequence back.
- Save tokens: use `set_clip_properties_batch` / `add_to_timeline_batch`, read single tracks (`get_track_info`), never
  `get_full_sequence_info` on big timelines.
