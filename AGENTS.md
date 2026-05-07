# AGENTS.md
## Platform Engineering Talk — Project Guide for AI Agents

This is a conference talk repository for **"Cloud Native Platform Engineering on Azure"** by Geert van der Cruijsen (CEO & Co-founder, Zure NL), presented at Techorama Belgium.

---

## Project Structure

```
design.pen           # Pencil design file — source of truth for all slide visuals
PPTX_NOTES.md        # Detailed technical notes for converting Pencil → PowerPoint
opening_slide.pptx   # Generated PPTX output (opening slide)
slides/              # Slide content and speaker notes
demos/               # Demo scripts and manifests (GitOps, Crossplane, Terranetes)
docs/                # Supporting notes, research, references
assets/              # Images, diagrams, logos
```

---

## Slide Content

The talk has 3 sections plus an opening slide:

| Slide | ID | Name |
|-------|----|------|
| 0 | `AfQre` | Opening |
| — | `mOXtk` | Slide 1 — The Chaos |
| — | `LzW2m` | Slide 2 — Day One |
| — | `4aGHE` | Slide 3 — Who Do You Call |
| — | `MbsRS` | Slide 4 — Ticket Queue |
| — | `5NOOU` | Slide 5 — Every Snowflake |
| — | `CK1vE` | Slide 6 — Cognitive Overload |
| — | `6gQPX` | Slide 7 — The Pivot |
| — | `5vJBq` | S2-01 DevOps Grew Up |
| — | `0O2Up` | S2-02 Not an Ops Team |
| — | `0IFZL` | S2-03 The IDP |
| — | `ZnXBD` | S2-04 The Golden Path |
| — | `7mmFP` | S2-05 Three Outcomes |
| — | `iG4kP` | S3-01 Why Kubernetes |
| — | `6oy8K` | S3-02 Declarative Everything |
| — | `kApwb` | S3-03 CNCF Toolkit |
| — | `YVj61` | S3-04 GitOps |
| — | `op0tz` | S3-05 Argo CD |
| — | `gjSv6` | S3-06 Azure / AKS |
| — | `o4NvXH` | S3-07 GitOps Architecture |
| — | `saIeA` | S3-08 Argo CD Patterns |

---

## Generating PowerPoint Slides

All PPTX generation uses **python-pptx** in a virtualenv:

```
/var/folders/dn/_590ldjj4cb4zygjhjm72mbh0000gn/T/opencode/pptx-venv/bin/python3
```

**Always read `PPTX_NOTES.md` before writing any PPTX generation code.** It contains all the hard-won conversion rules including:

- px → pt font size conversion (Pencil is 96dpi, PowerPoint is 72dpi — multiply by 0.75)
- PowerPoint internal textbox padding compensation (9.6px left, 4.8px top)
- Font weight via typeface name suffix (`Inter Black`, `Inter ExtraBold`, etc.)
- Letter spacing conversion (px → hundredths of a point)
- Line height stacking for separate textboxes
- Per-font-size `extra_nudge_y` values
- Reusable `add_text`, `add_rect`, `add_oval` helper functions

The working opening slide script (reference implementation) is:
`slides/slide_opening.py`

### Workflow for each new slide

1. Read the Pencil node using `pencil_batch_get` with the slide's node ID
2. Take a screenshot with `pencil_get_screenshot` to use as visual reference
3. Read `PPTX_NOTES.md` for all conversion rules
4. Write the generation script, reusing the helper functions from v9
5. Run with the venv python3
6. Compare output to the Pencil screenshot

---

## Design System

See `PPTX_NOTES.md` for full details. Key values:

- **Font**: Inter (must be installed)
- **Canvas**: 1920×1080px → 20"×11.25" in PowerPoint
- **Content area**: x=120, y=100, w=1680, h=880
- **Dark bg**: `#000000`, light bg: `#FFFFFF`, near-black: `#111111`
- **Accent bar**: 8px wide rect on left or right edge
- **Corner bar**: 200×8px rect at bottom corner
- **Footer color**: `#888888`
