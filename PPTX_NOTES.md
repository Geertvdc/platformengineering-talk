# PowerPoint Generation Notes
## Platform Engineering Talk — Pencil → PPTX

---

## Slide Dimensions

- Source canvas: **1920 × 1080 px**
- PowerPoint size: **20" × 11.25"** (widescreen, matches 1920/1080 ratio)
- EMU per inch: 914400

```python
SW, SH = 1920, 1080
W_IN, H_IN = 20.0, 11.25
EMU_PER_IN = 914400

def px(val, axis='x'):
    if axis == 'x':
        return int(val / SW * W_IN * EMU_PER_IN)
    else:
        return int(val / SH * H_IN * EMU_PER_IN)
```

---

## Font Size Conversion

Pencil uses **px at 96dpi**. PowerPoint uses **pt at 72dpi**.

```python
def to_pt(pencil_px):
    return pencil_px * 72 / 96
```

| Pencil px | PowerPoint pt |
|-----------|--------------|
| 140px | 105pt |
| 72px | 54pt |
| 42px | 31.5pt |
| 24px | 18pt |
| 20px | 15pt |

---

## Letter Spacing Conversion

Pencil letter spacing is in px. PowerPoint stores it in **hundredths of a point**.

```python
# In rPr XML:
rPr.set('spc', str(int(to_pt(letter_spacing_px) * 100)))
```

| Pencil px | PowerPoint (hundredths pt) |
|-----------|--------------------------|
| -6px | -450 |
| -3px | -225 |
| -1px | -75 |
| +1px | +75 |
| +4px | +300 |

---

## Font Weight

Use the **typeface name suffix** — do NOT rely on `font.bold = True` (that only gives 700).

```python
weight_map = {
    400: '',            # Inter
    500: ' Medium',     # Inter Medium
    600: ' SemiBold',   # Inter SemiBold
    700: ' Bold',       # Inter Bold
    800: ' ExtraBold',  # Inter ExtraBold
    900: ' Black',      # Inter Black
}
latin.set('typeface', 'Inter' + weight_map[font_weight])
```

- Set `rPr.set('b', '1')` for weight >= 700 as well (belt and braces)

---

## PowerPoint Textbox Internal Padding

PowerPoint adds default internal padding to every textbox:

- **Left: 9.6px** (91440 EMU = 0.1")
- **Top: 4.8px** (45720 EMU = 0.05")

This means glyphs do NOT start at the textbox x/y — they start 9.6px to the right and 4.8px down.

**Fix: subtract padding from placement coords so glyphs land where you want them:**

```python
PPT_PAD_LEFT = 9.6   # px
PPT_PAD_TOP  = 4.8   # px

adj_x = x - PPT_PAD_LEFT
adj_y = y - PPT_PAD_TOP - extra_nudge_y
txBox = slide.shapes.add_textbox(px(adj_x,'x'), px(adj_y,'y'), ...)
```

- `extra_nudge_y` is a per-font-size tweak (larger fonts need a bit more due to ascender height)
- Shapes (rects, ovals) have NO padding — place them at exact x/y

---

## Line Height / Vertical Stacking

Pencil's `lineHeight` is a multiplier. For **separate textboxes stacked vertically**, use:

```
step = fontSize_px * lineHeight
```

as the vertical distance between textbox tops (not as pptx line spacing).

```python
step_140 = int(140 * 0.88)  # = 123px  for 140px font at lineHeight 0.88
step_72  = int(72  * 1.2)   # = 86px   for 72px font at lineHeight 1.2
```

Remove paragraph spacing inside each textbox to avoid extra gaps:

```python
pPr = p._p.get_or_add_pPr()
spcBef = etree.SubElement(pPr, qn('a:spcBef'))
etree.SubElement(spcBef, qn('a:spcPts')).set('val', '0')
spcAft = etree.SubElement(pPr, qn('a:spcAft'))
etree.SubElement(spcAft, qn('a:spcPts')).set('val', '0')
```

---

## Shapes

- **Rectangles**: `add_shape(1, ...)` — exact x/y, no padding
- **Ovals/Ellipses**: `add_shape(9, ...)` — exact x/y, no padding
- **Opacity**: set via XML alpha on solidFill (0–100000 scale)

```python
if opacity < 1.0:
    spF = shape.fill._xPr.find(qn('a:solidFill'))
    clr = spF.find(qn('a:srgbClr'))
    a = etree.SubElement(clr, qn('a:alpha'))
    a.set('val', str(int(opacity * 100000)))
```

---

## Reusable add_text Function

```python
def add_text(slide, text, x, y, w, h,
             font_name, font_size_px, font_weight,
             hex_color, letter_spacing_px=0, extra_nudge_y=0):
    adj_x = x - PPT_PAD_LEFT
    adj_y = y - PPT_PAD_TOP - extra_nudge_y
    txBox = slide.shapes.add_textbox(px(adj_x,'x'), px(adj_y,'y'), px(w,'x'), px(h,'y'))
    tf = txBox.text_frame
    tf.word_wrap = False
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    pPr = p._p.get_or_add_pPr()
    spcBef = etree.SubElement(pPr, qn('a:spcBef'))
    etree.SubElement(spcBef, qn('a:spcPts')).set('val', '0')
    spcAft = etree.SubElement(pPr, qn('a:spcAft'))
    etree.SubElement(spcAft, qn('a:spcPts')).set('val', '0')
    run = p.add_run()
    run.text = text
    rPr = run._r.get_or_add_rPr()
    rPr.set('sz', str(int(to_pt(font_size_px) * 100)))
    rPr.set('b', '1' if font_weight >= 700 else '0')
    if letter_spacing_px != 0:
        rPr.set('spc', str(int(to_pt(letter_spacing_px) * 100)))
    solidFill = etree.SubElement(rPr, qn('a:solidFill'))
    srgbClr = etree.SubElement(solidFill, qn('a:srgbClr'))
    srgbClr.set('val', hex_color.lstrip('#'))
    weight_map = {400: '', 500: ' Medium', 600: ' SemiBold',
                  700: ' Bold', 800: ' ExtraBold', 900: ' Black'}
    latin = etree.SubElement(rPr, qn('a:latin'))
    latin.set('typeface', font_name + weight_map.get(font_weight, ''))
    return txBox
```

---

## Design System — Common Values

| Token | Value |
|-------|-------|
| Font | Inter |
| Slide bg (dark) | `#000000` |
| Slide bg (light) | `#FFFFFF` |
| Slide bg (near-black) | `#111111` |
| Accent bar | 8px wide rect, left or right edge |
| Corner bar | 200×8px rect, bottom corner |
| Footer text color | `#888888` |
| Dimmed title color | `#666666` |
| More dimmed | `#444444` |
| Content area | x=120, y=100, w=1680, h=880 |
| Footer y | y=1020 |

---

## Per-slide Extra Nudge Y Values (empirical)

These compensate for PowerPoint ascender space above cap-height at each font size:

| Font size (px) | extra_nudge_y |
|---------------|---------------|
| 140px (105pt) | 0 (default PPT_PAD_TOP=4.8 is enough) |
| 72px (54pt)   | 0 |
| 42px (31.5pt) | 3 |
| 24px (18pt)   | 3 |
| 20px (15pt)   | 5 |

---

## Working Script

The final working script for the opening slide is:
`slides/slide_opening.py`

Run it with:
```
/var/folders/dn/_590ldjj4cb4zygjhjm72mbh0000gn/T/opencode/pptx-venv/bin/python3 slides/slide_opening.py
```
