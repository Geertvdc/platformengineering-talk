"""
generate_presentation.py
Builds the full Platform Engineering talk PPTX — all slides in one file.
"""
from pptx import Presentation
from pptx.util import Emu
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

PPT_PAD_LEFT = 9.6
PPT_PAD_TOP  = 4.8

prs = Presentation()
prs.slide_width  = Emu(int(W_IN * EMU_PER_IN))
prs.slide_height = Emu(int(H_IN * EMU_PER_IN))

def new_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])

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

def add_rect_outlined(slide, x, y, w, h, stroke_hex, stroke_opacity=1.0, fill_hex=None):
    """Rectangle with a semi-transparent stroke border (used for diagram boxes)."""
    shape = slide.shapes.add_shape(1, px(x,'x'), px(y,'y'), px(w,'x'), px(h,'y'))
    if fill_hex:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(fill_hex.lstrip('#'))
    else:
        shape.fill.background()
    shape.line.width = 9525  # 1px → 0.75pt → 9525 EMU
    shape.line.color.rgb = RGBColor.from_string(stroke_hex.lstrip('#'))
    if stroke_opacity < 1.0:
        ln = shape.line._ln
        solidFill = ln.find(qn('a:solidFill'))
        if solidFill is not None:
            srgbClr = solidFill.find(qn('a:srgbClr'))
            if srgbClr is not None:
                alpha = etree.SubElement(srgbClr, qn('a:alpha'))
                alpha.set('val', str(int(stroke_opacity * 100000)))
    return shape

def add_text(slide, text, x, y, w, h,
             font_name, font_size_px, font_weight,
             hex_color, letter_spacing_px=0, extra_nudge_y=0, opacity=1.0, word_wrap=False):
    adj_x = x - PPT_PAD_LEFT
    adj_y = y - PPT_PAD_TOP - extra_nudge_y
    txBox = slide.shapes.add_textbox(px(adj_x,'x'), px(adj_y,'y'), px(w,'x'), px(h,'y'))
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
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
    if opacity < 1.0:
        alpha = etree.SubElement(srgbClr, qn('a:alpha'))
        alpha.set('val', str(int(opacity * 100000)))
    weight_map = {400: '', 500: ' Medium', 600: ' SemiBold',
                  700: ' Bold', 800: ' ExtraBold', 900: ' Black'}
    latin = etree.SubElement(rPr, qn('a:latin'))
    latin.set('typeface', font_name + weight_map.get(font_weight, ''))
    return txBox


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 0 — Opening
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1072, 200, 8, 'FFFFFF')
for dx, dy, op in [(1780,200,1.0),(1820,200,0.4),(1860,200,0.2),
                   (1780,240,0.4),(1820,240,1.0),(1860,240,0.4)]:
    add_oval(slide, dx, dy, 16, 16, 'FFFFFF', op)

tag_y = 120
add_rect(slide, 120, tag_y, 14, 14, 'FFFFFF')
add_text(slide, 'TECHORAMA BELGIUM',
         x=150, y=tag_y, w=700, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

title_y = 240
step_140 = int(140 * 0.88)  # 123px

add_text(slide, 'CLOUD NATIVE',
         x=120, y=title_y,              w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'PLATFORM',
         x=120, y=title_y + step_140,   w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'ENGINEERING',
         x=120, y=title_y + step_140*2, w=1500, h=step_140,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='666666', letter_spacing_px=0)
add_text(slide, 'ON AZURE',
         x=120, y=title_y + step_140*3 + 10, w=900, h=int(72*1.2),
         font_name='Inter', font_size_px=72, font_weight=900,
         hex_color='444444', letter_spacing_px=0)

spk_y = 864
add_rect(slide, 120, spk_y, 80, 4, 'FFFFFF')
add_text(slide, 'Geert van der Cruijsen',
         x=120, y=spk_y + 14, w=900, h=46,
         font_name='Inter', font_size_px=42, font_weight=800,
         hex_color='FFFFFF', letter_spacing_px=0, extra_nudge_y=3)
add_text(slide, 'CEO & Co-founder \u00b7 Zure NL',
         x=120, y=spk_y + 64, w=900, h=28,
         font_name='Inter', font_size_px=24, font_weight=400,
         hex_color='888888', letter_spacing_px=1, extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — The Chaos
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, '!',
         x=1400, y=-180, w=400, h=968,
         font_name='Inter', font_size_px=800, font_weight=900,
         hex_color='FFFFFF', opacity=0.04)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')

for dx, dy, op in [
    (1780, 160, 1.0), (1820, 160, 1.0), (1860, 160, 1.0),
    (1780, 200, 0.4), (1820, 200, 1.0), (1860, 200, 0.4),
    (1780, 240, 0.2), (1820, 240, 0.4), (1860, 240, 1.0),
]:
    add_oval(slide, dx, dy, 16, 16, 'FFFFFF', op)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '01 / THE CHAOS',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'THE CHAOS.',
         x=120, y=389, w=1600, h=198,
         font_name='Inter', font_size_px=220, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
# +20px to compensate: PPTX renders 220px font with less visual gap to next text
add_text(slide, 'BEFORE THE PLATFORM.',
         x=120, y=607, w=1600, h=72,
         font_name='Inter', font_size_px=72, font_weight=900,
         hex_color='666666', letter_spacing_px=0)

add_rect(slide, 120, 903, 120, 6, 'FFFFFF')
add_text(slide, 'What happens when platform teams become the bottleneck \u2014 and how to think differently.',
         x=120, y=929, w=1680, h=31,
         font_name='Inter', font_size_px=26, font_weight=400,
         hex_color='AAAAAA', extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Day One
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, '01',
         x=1000, y=-120, w=800, h=847,
         font_name='Inter', font_size_px=700, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.03)
add_rect(slide, 0, 0, 8, 1080, '000000')

add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '02 / DAY ONE',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'DAY ONE.',
         x=120, y=354, w=1600, h=211,
         font_name='Inter', font_size_px=240, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
# +15px to compensate: PPTX renders 240px font with less visual gap to next text
add_text(slide, 'Three things. Zero answers.',
         x=120, y=594, w=800, h=36,
         font_name='Inter', font_size_px=30, font_weight=400,
         hex_color='AAAAAA', extra_nudge_y=3)

for cx, num, label in zip([120, 700, 1280],
                           ['01', '02', '03'],
                           ['NAMESPACE.', 'DATABASE.', 'PIPELINE.']):
    add_text(slide, num,
             x=cx, y=844, w=520, h=87,
             font_name='Inter', font_size_px=72, font_weight=900,
             hex_color='DDDDDD', letter_spacing_px=0)
    add_rect(slide, cx, 941, 520, 2, '000000')
    add_text(slide, label,
             x=cx, y=953, w=520, h=27,
             font_name='Inter', font_size_px=22, font_weight=800,
             hex_color='000000', letter_spacing_px=2, extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Who Do You Call
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, '?',
         x=1280, y=-60, w=500, h=847,
         font_name='Inter', font_size_px=700, font_weight=900,
         hex_color='FFFFFF', opacity=0.05)
add_rect(slide, 1912, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 0, 1060, 200, 8, 'FFFFFF')

add_oval(slide, 60, 160, 16, 16, 'FFFFFF', 0.2)
add_oval(slide, 60, 200, 16, 16, 'FFFFFF', 0.4)
add_oval(slide, 60, 240, 16, 16, 'FFFFFF', 1.0)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '03 / WHO DO YOU CALL',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'WHO DO',
         x=120, y=254, w=1600, h=180,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'YOU',
         x=120, y=434, w=1600, h=180,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='666666', letter_spacing_px=0)
add_text(slide, 'CALL?',
         x=120, y=614, w=1600, h=180,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_rect(slide, 120, 903, 120, 6, 'FFFFFF')
add_text(slide, 'When your team needs infrastructure. Today. Not next week.',
         x=120, y=929, w=1680, h=31,
         font_name='Inter', font_size_px=26, font_weight=400,
         hex_color='AAAAAA', extra_nudge_y=3)



# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Ticket Queue
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '111111')
add_text(slide, 'QUEUE',
         x=560, y=80, w=1200, h=500,
         font_name='Inter', font_size_px=480, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1072, 200, 8, 'FFFFFF')

for dx, dy, op in [(1780,160,0.3),(1820,160,0.15),(1780,200,0.15),(1820,200,0.3)]:
    add_oval(slide, dx, dy, 14, 14, 'FFFFFF', op)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '01 / THE CHAOS',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'THE TICKET QUEUE.',
         x=120, y=308, w=900, h=80,
         font_name='Inter', font_size_px=44, font_weight=800,
         hex_color='444444', letter_spacing_px=0, extra_nudge_y=3)
add_text(slide, 'SLOW.',
         x=120, y=378, w=800, h=180,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'INCONSISTENT.',
         x=120, y=564, w=1200, h=90,
         font_name='Inter', font_size_px=96, font_weight=900,
         hex_color='444444', letter_spacing_px=0)
add_text(slide, 'BOTTLENECK.',
         x=120, y=648, w=1200, h=120,
         font_name='Inter', font_size_px=128, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_rect(slide, 120, 935, 80, 4, 'FFFFFF')
add_text(slide, 'The ticket queue is where developer velocity goes to die.',
         x=120, y=953, w=1400, h=30,
         font_name='Inter', font_size_px=22, font_weight=400,
         hex_color='555555', extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Every Snowflake
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, '*',
         x=1520, y=750, w=250, h=300,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', opacity=0.05)
add_text(slide, '*',
         x=1780, y=480, w=120, h=140,
         font_name='Inter', font_size_px=80, font_weight=900,
         hex_color='FFFFFF', opacity=0.07)
add_text(slide, '*',
         x=1650, y=650, w=180, h=220,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='FFFFFF', opacity=0.10)
add_rect(slide, 1912, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 0, 1060, 200, 8, 'FFFFFF')

add_oval(slide, 60, 160, 16, 16, 'FFFFFF', 0.2)
add_oval(slide, 60, 200, 16, 16, 'FFFFFF', 0.4)
add_oval(slide, 60, 240, 16, 16, 'FFFFFF', 1.0)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '01 / THE CHAOS',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'EVERY TEAM.',
         x=120, y=280, w=1500, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'EVERY',
         x=120, y=452, w=900, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='666666', letter_spacing_px=0)
add_text(slide, 'SNOWFLAKE.',
         x=120, y=624, w=1500, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_rect(slide, 120, 903, 120, 6, 'FFFFFF')
add_text(slide, 'No two teams build their infrastructure the same way. The platform team inherits the chaos.',
         x=120, y=929, w=1680, h=34,
         font_name='Inter', font_size_px=26, font_weight=400,
         hex_color='AAAAAA', extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Cognitive Overload
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
for txt, fx, fy, fsz, fop in [
    ('FEATURES',       80,   200, 50, 0.11),
    ('SECURITY',       1280, 140, 42, 0.09),
    ('INFRASTRUCTURE', 560,  870, 34, 0.08),
    ('COMPLIANCE',     1380, 700, 44, 0.10),
    ('MONITORING',     80,   820, 38, 0.09),
    ('NETWORKING',     1120, 940, 32, 0.07),
    ('COST',           1620, 280, 62, 0.12),
    ('OBSERVABILITY',  1050, 580, 30, 0.08),
]:
    add_text(slide, txt,
             x=fx, y=fy, w=500, h=int(fsz*1.3),
             font_name='Inter', font_size_px=fsz, font_weight=800,
             hex_color='FFFFFF', opacity=fop)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1072, 200, 8, 'FFFFFF')

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '01 / THE CHAOS',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'TOO MUCH',
         x=120, y=271, w=1500, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'TO',
         x=120, y=441, w=500, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='555555', letter_spacing_px=0)
add_text(slide, 'HOLD.',
         x=120, y=611, w=900, h=165,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_rect(slide, 120, 904, 120, 4, 'FFFFFF')
add_text(slide, 'Developers are asked to master features, security, and infrastructure simultaneously. '
               'Cognitive overload isn\u2019t a weakness \u2014 it\u2019s an architectural problem.',
         x=120, y=922, w=1680, h=62,
         font_name='Inter', font_size_px=24, font_weight=400,
         hex_color='666666', extra_nudge_y=3, word_wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — The Pivot
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_oval(slide, 900, -300, 1400, 1400, 'FFFFFF', 0.03)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 0, 1072, 200, 8, 'FFFFFF')

for dx, dy, op in [
    (1780,820,0.30),(1820,820,0.15),(1860,820,0.08),
    (1780,860,0.15),(1820,860,0.30),(1860,860,0.15),
]:
    add_oval(slide, dx, dy, 14, 14, 'FFFFFF', op)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '01 / THE CHAOS',
         x=150, y=120, w=500, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'WHAT IF THEY',
         x=120, y=315, w=1400, h=145,
         font_name='Inter', font_size_px=158, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'NEVER NEEDED',
         x=120, y=460, w=1400, h=145,
         font_name='Inter', font_size_px=158, font_weight=900,
         hex_color='404040', letter_spacing_px=0)
add_text(slide, 'TO CALL YOU?',
         x=120, y=605, w=1400, h=145,
         font_name='Inter', font_size_px=158, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_rect(slide, 120, 933, 120, 4, 'FFFFFF')
add_text(slide, 'The platform team\u2019s job isn\u2019t to say no. It\u2019s to make yes the default.',
         x=120, y=951, w=1200, h=34,
         font_name='Inter', font_size_px=24, font_weight=400,
         hex_color='555555', extra_nudge_y=3)




# ═══════════════════════════════════════════════════════════════════════════════
# S2-01 — DevOps Grew Up
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'SCALE',
         x=580, y=240, w=1400, h=650,
         font_name='Inter', font_size_px=500, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, '000000')
add_rect(slide, 1720, 1060, 200, 8, '000000')

for dx, dy, op in [(1780,100,0.15),(1820,100,0.15),(1860,100,0.15),
                   (1780,140,0.08),(1820,140,0.08),(1860,140,0.04)]:
    add_oval(slide, dx, dy, 14, 14, '000000', op)

add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '02 / PLATFORM ENGINEERING',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'YOU BUILD IT. YOU RUN IT.',
         x=120, y=391, w=900, h=75,
         font_name='Inter', font_size_px=56, font_weight=900,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=3)
add_rect(slide, 120, 479, 160, 8, '000000')
add_text(slide, 'AT SCALE.',
         x=120, y=507, w=1200, h=180,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='000000', letter_spacing_px=0)

add_text(slide, 'Platform engineering is DevOps that scales \u2014 built for large teams and large organisations.',
         x=120, y=956, w=1400, h=28,
         font_name='Inter', font_size_px=20, font_weight=500,
         hex_color='888888', extra_nudge_y=5)


# ═══════════════════════════════════════════════════════════════════════════════
# S2-02 — Not an Ops Team
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '111111')
add_text(slide, 'TICKET',
         x=900, y=350, w=1100, h=380,
         font_name='Inter', font_size_px=300, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.06)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, '333333')

add_rect(slide, 1380, 450, 500, 5, '333333', opacity=0.5)
add_rect(slide, 1500, 480, 360, 5, '333333', opacity=0.3)
add_rect(slide, 1600, 510, 220, 5, '333333', opacity=0.15)

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '02 / PLATFORM ENGINEERING',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='666666', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'A PRODUCT.',
         x=120, y=420, w=1200, h=162,
         font_name='Inter', font_size_px=180, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'NOT A TICKET QUEUE.',
         x=120, y=596, w=1200, h=75,
         font_name='Inter', font_size_px=56, font_weight=900,
         hex_color='444444', letter_spacing_px=0, extra_nudge_y=3)

add_text(slide, 'The platform team ships. Developers self-serve.',
         x=120, y=956, w=900, h=28,
         font_name='Inter', font_size_px=20, font_weight=500,
         hex_color='555555', letter_spacing_px=1, extra_nudge_y=5)


# ═══════════════════════════════════════════════════════════════════════════════
# S2-03 — The IDP
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, 'IDP',
         x=1000, y=250, w=1100, h=760,
         font_name='Inter', font_size_px=600, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.04)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '02 / PLATFORM ENGINEERING',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='666666', letter_spacing_px=4, extra_nudge_y=5)

# "THE\nPLATFORM." split into 2 lines (160px * 0.88 = 141px step)
add_text(slide, 'THE',
         x=120, y=373, w=600, h=145,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'PLATFORM.',
         x=120, y=514, w=1100, h=145,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)

add_text(slide, 'A product your developers consume \u2014 not a system they wait for.',
         x=120, y=910, w=1400, h=30,
         font_name='Inter', font_size_px=22, font_weight=400,
         hex_color='AAAAAA', extra_nudge_y=3)
add_text(slide, 'Abstractions, golden path, self-service \u2014 built once, used by every team.',
         x=120, y=953, w=1400, h=30,
         font_name='Inter', font_size_px=22, font_weight=400,
         hex_color='666666', extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# S2-04 — The Golden Path
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'PATH',
         x=820, y=300, w=1300, h=650,
         font_name='Inter', font_size_px=500, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, '000000')
add_rect(slide, 1720, 1060, 200, 8, '000000')

add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '02 / PLATFORM ENGINEERING',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'OPINIONATED.',
         x=120, y=427, w=1300, h=145,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
add_text(slide, 'NOT MANDATORY.',
         x=120, y=580, w=1000, h=78,
         font_name='Inter', font_size_px=80, font_weight=900,
         hex_color='CCCCCC', letter_spacing_px=0)

add_text(slide, 'Make the right thing easy. Make the wrong thing intentional.',
         x=120, y=953, w=1000, h=30,
         font_name='Inter', font_size_px=22, font_weight=400,
         hex_color='888888', extra_nudge_y=3)


# ═══════════════════════════════════════════════════════════════════════════════
# S2-05 — Three Outcomes
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()

add_rect(slide, 0, 0, 1920, 1080, '111111')
add_text(slide, '03',
         x=1200, y=50, w=1000, h=880,
         font_name='Inter', font_size_px=700, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')

add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '02 / PLATFORM ENGINEERING',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='666666', letter_spacing_px=4, extra_nudge_y=5)

add_text(slide, 'SELF-SERVICE.',
         x=120, y=167, w=900, h=92,
         font_name='Inter', font_size_px=100, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'Developers provision what they need \u2014 on demand.',
         x=120, y=284, w=800, h=26,
         font_name='Inter', font_size_px=18, font_weight=400,
         hex_color='666666', extra_nudge_y=5)
add_rect(slide, 120, 338, 718, 2, '333333')

add_text(slide, 'CONSISTENCY.',
         x=120, y=372, w=1000, h=92,
         font_name='Inter', font_size_px=100, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'Every team\u2019s infrastructure follows the same platform standards.',
         x=120, y=489, w=900, h=26,
         font_name='Inter', font_size_px=18, font_weight=400,
         hex_color='666666', extra_nudge_y=5)
add_rect(slide, 120, 543, 718, 2, '333333')

add_text(slide, 'BOUNDARIES.',
         x=120, y=577, w=900, h=92,
         font_name='Inter', font_size_px=100, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'Clear ownership between platform team and product team.',
         x=120, y=694, w=800, h=26,
         font_name='Inter', font_size_px=18, font_weight=400,
         hex_color='555555', extra_nudge_y=5)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-01 — Why Kubernetes
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, 'API',
         x=1100, y=50, w=1400, h=800,
         font_name='Inter', font_size_px=700, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')
for dx, dy, op in [(1780,160,1.0),(1820,160,0.4),(1860,160,0.2),
                   (1780,200,0.4),(1820,200,1.0),(1860,200,0.4)]:
    add_oval(slide, dx, dy, 14, 14, 'FFFFFF', op)
add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '03 / CLOUD NATIVE + GITOPS',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='888888', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'KUBERNETES.',
         x=120, y=710, w=1700, h=176,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'AN API. NOT A SCHEDULER.',
         x=120, y=894, w=1700, h=86,
         font_name='Inter', font_size_px=96, font_weight=900,
         hex_color='666666', letter_spacing_px=0)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-02 — Declarative Everything
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'INTENT',
         x=560, y=300, w=1400, h=500,
         font_name='Inter', font_size_px=380, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 1912, 0, 8, 1080, '000000')
add_rect(slide, 0, 1060, 200, 8, '000000')
for dx, dy, op in [(1780,160,0.15),(1820,160,0.15),(1860,160,0.08),
                   (1780,200,0.08),(1820,200,0.08)]:
    add_oval(slide, dx, dy, 14, 14, '000000', op)
add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '03 / CLOUD NATIVE + GITOPS',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'YOU DECLARE IT.',
         x=120, y=721, w=1700, h=141,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
add_text(slide, 'KUBERNETES CONVERGES IT.',
         x=120, y=884, w=1700, h=106,
         font_name='Inter', font_size_px=120, font_weight=900,
         hex_color='CCCCCC', letter_spacing_px=0)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-03 — CNCF Toolkit
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, '111111')
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')
for wm_text, wm_size, wm_x, wm_y, wm_op in [
    ('ARGO',          48, 1280, 140,  0.10),
    ('PROMETHEUS',    32,   80, 200,  0.08),
    ('ISTIO',         54, 1620, 260,  0.10),
    ('FLUX',          62,  140, 820,  0.10),
    ('CROSSPLANE',    36, 1260, 880,  0.08),
    ('OPENTELEMETRY', 30,  560, 920,  0.07),
    ('CILIUM',        38, 1500, 560,  0.09),
    ('OPA',           44, 1100, 580,  0.10),
    ('KEDA',          30,   60, 560,  0.07),
    ('BACKSTAGE',     34, 1680, 780,  0.08),
]:
    add_text(slide, wm_text,
             x=wm_x, y=wm_y, w=800, h=200,
             font_name='Inter', font_size_px=wm_size, font_weight=800,
             hex_color='FFFFFF', letter_spacing_px=0, opacity=wm_op)
add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '03 / CLOUD NATIVE + GITOPS',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='888888', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'CNCF TOOLKIT.',
         x=120, y=710, w=1700, h=176,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'BUILD ON KUBERNETES.',
         x=120, y=894, w=1700, h=86,
         font_name='Inter', font_size_px=96, font_weight=900,
         hex_color='555555', letter_spacing_px=0)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-04 — GitOps
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'GITOPS',
         x=540, y=340, w=1400, h=600,
         font_name='Inter', font_size_px=340, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 1912, 0, 8, 1080, '000000')
add_rect(slide, 0, 1060, 200, 8, '000000')
add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '03 / CLOUD NATIVE + GITOPS',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'GIT IS',
         x=120, y=151, w=1700, h=141,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
add_text(slide, 'THE TRUTH.',
         x=120, y=306, w=1700, h=141,
         font_name='Inter', font_size_px=160, font_weight=900,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=15)
# 4-column list
cols = [
    (120, '01', 'DECLARATIVE',  'Desired state as data, not steps.'),
    (524, '02', 'VERSIONED',    'Every change is a Git commit.'),
    (928, '03', 'PULLED',       'The cluster fetches; CI never pushes.'),
    (1332, '04', 'RECONCILED',  'Drift heals itself, continuously.'),
]
for cx, num, title, desc in cols:
    add_text(slide, num,
             x=cx, y=469, w=380, h=44,
             font_name='Inter', font_size_px=36, font_weight=900,
             hex_color='000000', letter_spacing_px=0)
    add_text(slide, title,
             x=cx, y=519, w=380, h=27,
             font_name='Inter', font_size_px=22, font_weight=800,
             hex_color='000000', letter_spacing_px=0, extra_nudge_y=3)
    add_text(slide, desc,
             x=cx, y=552, w=380, h=40,
             font_name='Inter', font_size_px=16, font_weight=500,
             hex_color='666666', letter_spacing_px=0, extra_nudge_y=5, word_wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-05 — Argo CD (DEMO)
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, '000000')
add_text(slide, 'ARGO',
         x=560, y=240, w=1400, h=700,
         font_name='Inter', font_size_px=520, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.05)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1720, 1060, 200, 8, 'FFFFFF')
for dx, dy, op in [(1780,160,1.0),(1820,160,0.4),(1860,160,0.2)]:
    add_oval(slide, dx, dy, 14, 14, 'FFFFFF', op)
add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, '03 / CLOUD NATIVE + GITOPS  \u00b7  DEMO',
         x=150, y=120, w=700, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='888888', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'ARGO CD.',
         x=120, y=720, w=1700, h=176,
         font_name='Inter', font_size_px=200, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0)
add_text(slide, 'DRIFT? RECONCILE.',
         x=120, y=904, w=1700, h=76,
         font_name='Inter', font_size_px=84, font_weight=900,
         hex_color='666666', letter_spacing_px=0)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-06 — Azure / AKS
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'AZURE',
         x=600, y=280, w=1400, h=600,
         font_name='Inter', font_size_px=460, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.05)
add_oval(slide, 1200, -200, 1200, 1200, '000000', 0.04)
add_rect(slide, 1912, 0, 8, 1080, '000000')
add_rect(slide, 0, 1060, 200, 8, '000000')
for dx, dy, op in [(1780,160,0.15),(1820,160,0.15),(1860,160,0.08)]:
    add_oval(slide, dx, dy, 14, 14, '000000', op)
add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, '03 / CLOUD NATIVE + GITOPS',
         x=150, y=120, w=600, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'AKS IS WHERE',
         x=120, y=646, w=1700, h=123,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
add_text(slide, 'IT RUNS.',
         x=120, y=777, w=1700, h=123,
         font_name='Inter', font_size_px=140, font_weight=900,
         hex_color='000000', letter_spacing_px=0, extra_nudge_y=10)
add_text(slide, 'NOT WHERE IT STOPS.',
         x=120, y=908, w=1700, h=72,
         font_name='Inter', font_size_px=80, font_weight=900,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=10)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-07 — GitOps Architecture
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, '0D0D0D')
add_text(slide, 'LOOP',
         x=150, y=-60, w=1400, h=700,
         font_name='Inter', font_size_px=480, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.04)
add_rect(slide, 0, 0, 8, 1080, 'FFFFFF')
add_rect(slide, 1712, 1064, 200, 8, 'FFFFFF')
add_rect(slide, 120, 120, 14, 14, 'FFFFFF')
add_text(slide, 'SECTION 3  \u00b7  GITOPS ARCHITECTURE',
         x=150, y=120, w=700, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='FFFFFF', letter_spacing_px=4, extra_nudge_y=5)
add_text(slide, 'HOW GITOPS WORKS',
         x=120, y=117, w=900, h=92,
         font_name='Inter', font_size_px=76, font_weight=900,
         hex_color='FFFFFF', letter_spacing_px=0, extra_nudge_y=0)

# Step labels (above arrows)
add_text(slide, '1  git push',
         x=330, y=335, w=220, h=20,
         font_name='Inter', font_size_px=13, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.47, extra_nudge_y=5)
add_text(slide, '2  argo pulls',
         x=678, y=335, w=220, h=20,
         font_name='Inter', font_size_px=13, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.47, extra_nudge_y=5)
add_text(slide, '3  apply',
         x=1114, y=335, w=180, h=20,
         font_name='Inter', font_size_px=13, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.47, extra_nudge_y=5)

# Arrows between boxes
add_text(slide, '\u2192',
         x=346, y=367, w=80, h=60,
         font_name='Inter', font_size_px=48, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.33, extra_nudge_y=0)
add_text(slide, '\u2190',
         x=706, y=367, w=80, h=60,
         font_name='Inter', font_size_px=48, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.33, extra_nudge_y=0)
add_text(slide, '\u2192',
         x=1127, y=367, w=80, h=60,
         font_name='Inter', font_size_px=48, font_weight=400,
         hex_color='FFFFFF', letter_spacing_px=0, opacity=0.33, extra_nudge_y=0)

# Diagram boxes
add_rect_outlined(slide, 120, 309, 220, 160, 'FFFFFF', stroke_opacity=0.27)
add_rect_outlined(slide, 430, 309, 260, 160, 'FFFFFF', stroke_opacity=0.27)
add_rect(slide, 800, 289, 300, 200, 'FFFFFF')
add_rect_outlined(slide, 1220, 269, 560, 240, 'FFFFFF', stroke_opacity=0.27)

# Box labels
add_text(slide, 'DEVELOPER',
         x=163, y=380, w=140, h=20,
         font_name='Inter', font_size_px=16, font_weight=700,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=5)
add_text(slide, 'GIT REPO',
         x=493, y=380, w=120, h=20,
         font_name='Inter', font_size_px=16, font_weight=700,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=5)
add_text(slide, 'ARGO CD',
         x=869, y=375, w=160, h=28,
         font_name='Inter', font_size_px=22, font_weight=700,
         hex_color='0D0D0D', letter_spacing_px=0, extra_nudge_y=3)
add_text(slide, 'KUBERNETES CLUSTER',
         x=1286, y=378, w=340, h=24,
         font_name='Inter', font_size_px=18, font_weight=700,
         hex_color='CCCCCC', letter_spacing_px=0, extra_nudge_y=5)

# Insight row
for ix, label in [(120, 'PULL NOT PUSH'), (690, 'GIT = SOURCE OF TRUTH'), (1260, 'ALWAYS CONVERGING')]:
    add_rect(slide, ix, 729, 540, 70, '141414')
    add_text(slide, label,
             x=ix+24, y=753, w=492, h=24,
             font_name='Inter', font_size_px=18, font_weight=800,
             hex_color='FFFFFF', letter_spacing_px=0, extra_nudge_y=5)


# ═══════════════════════════════════════════════════════════════════════════════
# S3-08 — Argo CD Patterns
# ═══════════════════════════════════════════════════════════════════════════════
slide = new_slide()
add_rect(slide, 0, 0, 1920, 1080, 'FFFFFF')
add_text(slide, 'ARGO',
         x=80, y=-20, w=1400, h=700,
         font_name='Inter', font_size_px=420, font_weight=900,
         hex_color='000000', letter_spacing_px=0, opacity=0.04)
add_rect(slide, 1912, 0, 8, 1080, '000000')
add_rect(slide, 1712, 1064, 200, 8, '000000')
add_rect(slide, 120, 120, 14, 14, '000000')
add_text(slide, 'SECTION 3  \u00b7  ARGO CD PATTERNS',
         x=150, y=120, w=700, h=24,
         font_name='Inter', font_size_px=20, font_weight=600,
         hex_color='000000', letter_spacing_px=4, extra_nudge_y=5)

# Two-line headline
add_text(slide, 'APP OF APPS.',
         x=120, y=117, w=1200, h=75,
         font_name='Inter', font_size_px=62, font_weight=900,
         hex_color='000000', letter_spacing_px=0)
add_text(slide, 'APPLICATIONSETS.',
         x=120, y=192, w=1200, h=75,
         font_name='Inter', font_size_px=62, font_weight=900,
         hex_color='000000', letter_spacing_px=0)

# ── Left column: App of Apps tree ──
add_text(slide, 'APP OF APPS',
         x=120, y=287, w=400, h=27,
         font_name='Inter', font_size_px=22, font_weight=800,
         hex_color='000000', letter_spacing_px=0, extra_nudge_y=3)

# ROOT-APP box
add_rect(slide, 393, 328, 280, 70, '111111')
add_text(slide, 'ROOT-APP',
         x=446, y=354, w=174, h=19,
         font_name='Inter', font_size_px=16, font_weight=800,
         hex_color='FFFFFF', letter_spacing_px=0, extra_nudge_y=5)

# Tree connector lines
add_rect(slide, 532, 398, 2, 50, 'AAAAAA')
add_rect(slide, 215, 448, 636, 2, 'AAAAAA')
add_rect(slide, 215, 450, 2, 28, 'AAAAAA')
add_rect(slide, 532, 450, 2, 28, 'AAAAAA')
add_rect(slide, 849, 450, 2, 28, 'AAAAAA')

# Child boxes
add_rect_outlined(slide, 120, 478, 192, 60, '000000', stroke_opacity=0.2)
add_rect_outlined(slide, 436, 478, 192, 60, '000000', stroke_opacity=0.2)
add_rect_outlined(slide, 754, 478, 192, 60, '000000', stroke_opacity=0.2)
add_text(slide, 'INFRA-APP',
         x=144, y=500, w=144, h=17,
         font_name='Inter', font_size_px=13, font_weight=700,
         hex_color='333333', letter_spacing_px=0, extra_nudge_y=5)
add_text(slide, 'PLATFORM-APP',
         x=444, y=500, w=176, h=17,
         font_name='Inter', font_size_px=13, font_weight=700,
         hex_color='333333', letter_spacing_px=0, extra_nudge_y=5)
add_text(slide, 'APPS-APP',
         x=778, y=500, w=144, h=17,
         font_name='Inter', font_size_px=13, font_weight=700,
         hex_color='333333', letter_spacing_px=0, extra_nudge_y=5)

# Column divider
add_rect(slide, 956, 287, 2, 260, 'CCCCCC')

# ── Right column: ApplicationSets fan ──
add_text(slide, 'APPLICATIONSETS',
         x=982, y=287, w=600, h=27,
         font_name='Inter', font_size_px=22, font_weight=800,
         hex_color='000000', letter_spacing_px=0, extra_nudge_y=3)

# APPSET TEMPLATE box
add_rect(slide, 982, 432, 280, 80, '111111')
add_text(slide, 'APPSET TEMPLATE',
         x=1006, y=462, w=232, h=19,
         font_name='Inter', font_size_px=13, font_weight=800,
         hex_color='FFFFFF', letter_spacing_px=1, extra_nudge_y=5)

# Arrow
add_text(slide, '\u2192',
         x=1267, y=452, w=60, h=50,
         font_name='Inter', font_size_px=40, font_weight=400,
         hex_color='444444', letter_spacing_px=0, extra_nudge_y=0)

# Generated cluster boxes
for gi, (gy, label) in enumerate([(352, 'dev-cluster'), (432, 'staging-cluster'), (512, 'prod-cluster')]):
    add_rect_outlined(slide, 1342, gy, 200, 70, '000000', stroke_opacity=0.2)
    add_text(slide, label,
             x=1366, y=gy+26, w=152, h=17,
             font_name='Inter', font_size_px=13, font_weight=700,
             hex_color='333333', letter_spacing_px=0, extra_nudge_y=5)

# Footer strip
add_rect(slide, 120, 787, 1680, 50, '111111')
add_text(slide, 'DRIFT DETECTED  \u2192  ARGO RECONCILES WITHIN SECONDS',
         x=354, y=807, w=1213, h=19,
         font_name='Inter', font_size_px=16, font_weight=700,
         hex_color='FFFFFF', letter_spacing_px=3, extra_nudge_y=5)


# ═══════════════════════════════════════════════════════════════════════════════
out = '/Users/geertvdc/dev/github/geertvdc/platformengineering-talk/presentation.pptx'
prs.save(out)
print(f'Saved {len(prs.slides)} slides to: {out}')
