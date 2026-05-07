from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

SW, SH = 1920, 1080
W_IN, H_IN = 20.0, 11.25
EMU_PER_IN = 914400

def px(val, axis='x'):
    if axis == 'x':
        return int(val / SW * W_IN * EMU_PER_IN)
    else:
        return int(val / SH * H_IN * EMU_PER_IN)

def to_pt(pencil_px):
    return pencil_px * 72 / 96

# PowerPoint default internal textbox padding in source px (at 1920px canvas / 20" wide)
PPT_PAD_LEFT = 9.6   # px
PPT_PAD_TOP  = 4.8   # px

prs = Presentation()
prs.slide_width  = Emu(int(W_IN * EMU_PER_IN))
prs.slide_height = Emu(int(H_IN * EMU_PER_IN))
slide = prs.slides.add_slide(prs.slide_layouts[6])

def add_rect(slide, x, y, w, h, hex_color, opacity=1.0):
    shape = slide.shapes.add_shape(1, px(x,'x'), px(y,'y'), px(w,'x'), px(h,'y'))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(hex_color.lstrip('#'))
    shape.line.fill.background()
    if opacity < 1.0:
        spF = shape.fill._xPr.find(qn('a:solidFill'))
        clr = spF.find(qn('a:srgbClr'))
        a = etree.SubElement(clr, qn('a:alpha'))
        a.set('val', str(int(opacity * 100000)))
    return shape

def add_oval(slide, x, y, w, h, hex_color, opacity=1.0):
    shape = slide.shapes.add_shape(9, px(x,'x'), px(y,'y'), px(w,'x'), px(h,'y'))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(hex_color.lstrip('#'))
    shape.line.fill.background()
    if opacity < 1.0:
        spF = shape.fill._xPr.find(qn('a:solidFill'))
        clr = spF.find(qn('a:srgbClr'))
        a = etree.SubElement(clr, qn('a:alpha'))
        a.set('val', str(int(opacity * 100000)))
    return shape

def add_text(slide, text, x, y, w, h,
             font_name, font_size_px, font_weight,
             hex_color, letter_spacing_px=0, extra_nudge_y=0):
    """
    Compensates for PowerPoint's internal padding:
      - shifts textbox left by PPT_PAD_LEFT so glyphs land at x
      - shifts textbox up by PPT_PAD_TOP + extra_nudge_y so glyphs land at y
    """
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

# ── Background + chrome ─────────────────────────────────────────────────────
add_rect(slide, 0, 0, 1920, 1080, '000000')
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1072, 200, 8, 'FFFFFF')
for dx, dy, op in [(1780,200,1.0),(1820,200,0.4),(1860,200,0.2),
                   (1780,240,0.4),(1820,240,1.0),(1860,240,0.4)]:
    add_oval(slide, dx, dy, 16, 16, 'FFFFFF', op)

# ── TAG ROW ─────────────────────────────────────────────────────────────────
# Square rect at x=120, y=105 (no padding — it's a shape)
# Text glyphs should start at x=150, y=105
# extra_nudge_y=2 on top of PPT_PAD_TOP=4.8 → total 6.8px up, user said needs 5px higher
tag_y = 105
add_rect(slide, 120, tag_y, 14, 14, 'FFFFFF')
add_text(slide, 'TECHORAMA BELGIUM',
         x=150, y=tag_y, w=700, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4,
         extra_nudge_y=5)   # user said needs ~5px higher than before (v8 had nudge_y=7)

# ── TITLE ───────────────────────────────────────────────────────────────────
# v6 positions were working well. Keep same y values, just add left compensation.
title_y = 240
step_140 = int(140 * 0.88)  # 123px

add_text(slide, 'CLOUD NATIVE',
         x=120, y=title_y,              w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=-6)

add_text(slide, 'PLATFORM',
         x=120, y=title_y + step_140,   w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=-6)

add_text(slide, 'ENGINEERING',
         x=120, y=title_y + step_140*2, w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='666666', letter_spacing_px=-6)

# ON AZURE: user said needs ~10px lower than v8
add_text(slide, 'ON AZURE',
         x=120, y=title_y + step_140*3 + 10, w=900, h=int(72*1.2),
         font_name='Inter', font_size_px=72, font_weight=900,
         hex_color='444444', letter_spacing_px=-3)

# ── SPEAKER ─────────────────────────────────────────────────────────────────
# Bar is a rect (no padding). Name and role textboxes get left+top compensation.
# User said spacing between name and CEO line looks OK in v8 — keep same logic.
spk_y = 864
add_rect(slide, 120, spk_y, 80, 4, 'FFFFFF')

add_text(slide, 'Geert van der Cruijsen',
         x=120, y=spk_y + 14, w=900, h=46,
         font_name='Inter', font_size_px=42, font_weight=800,
         hex_color='FFFFFF', letter_spacing_px=-1,
         extra_nudge_y=3)

add_text(slide, 'CEO & Co-founder · Zure NL',
         x=120, y=spk_y + 64, w=900, h=28,
         font_name='Inter', font_size_px=24, font_weight=400,
         hex_color='888888', letter_spacing_px=1,
         extra_nudge_y=3)

out = '/Users/geertvdc/dev/github/geertvdc/platformengineering-talk/opening_slide.pptx'
prs.save(out)
print('Saved:', out)
