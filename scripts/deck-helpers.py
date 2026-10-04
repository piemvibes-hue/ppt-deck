#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deck-helpers —— python-pptx 页面构建原语集（与产品无关，import 即用）
用法：from deck_helpers import *
  prs = Presentation('模板.pptx'); s = prs.slides.add_slide(prs.slide_layouts[1])
  page_title(s, '板块二 · 技术实现', '页题')
  browser(s, x, y, w, 'shots/card.png', url='app.example.com', max_h=4.3)
"""
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

EMU = 914400
def IN(v): return Emu(int(v * EMU))

# ---- 色板：改成模板 theme 取到的色系（inspect-template.py 会列出来）----
FONT = '思源黑体 CN'   # 模板推荐字体；漏设 ea 中文会渲染成宋体
INK = RGBColor(0x24, 0x1F, 0x35)
BODY = RGBColor(0x4C, 0x46, 0x63)
MUTE = RGBColor(0x8C, 0x86, 0x99)
PANEL = RGBColor(0xF7, 0xF5, 0xFB)
LINE = RGBColor(0xDD, 0xD4, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xEF, 0xE9, 0xF5)
ACC = RGBColor(0xA0, 0x2B, 0x93)
ACC_D = RGBColor(0x6B, 0x1E, 0x78)
ML, MR = 0.91, 12.42   # 左右边距（16:9，按模板标题位校准）


def _ea(run, name=FONT):
    """中文字体必须 latin/ea/cs 三处 typeface 全设——漏 ea 中文渲染成宋体。"""
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:latin', 'a:ea', 'a:cs'):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {})
            rPr.append(e)
        e.set('typeface', name)


def tx(slide, runs, x, y, w, h, size=12, color=INK, bold=False, align='l', valign='t', lh=None, spacing=None):
    """多 run 混排文本：runs=[(text,{size,bold,color,align,space_after,spacing}),...]；text 里 \n 分自然段。"""
    box = slide.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[valign]
    if not isinstance(runs, list): runs = [(runs, {})]
    first = True
    for text, opt in runs:
        for li, t in enumerate(str(text).split('\n')):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[opt.get('align', align)]
            if lh: p.line_spacing = lh
            if opt.get('space_after'): p.space_after = Pt(opt['space_after'])
            r = p.add_run(); r.text = t
            r.font.size = Pt(opt.get('size', size)); r.font.bold = opt.get('bold', bold)
            r.font.italic = opt.get('italic', False)
            r.font.color.rgb = opt.get('color', color)
            r.font.name = FONT; _ea(r)
            if opt.get('spacing') or spacing:
                r._r.get_or_add_rPr().set('spc', str(int((opt.get('spacing') or spacing) * 100)))
    return box


def hr(slide, y, x0=ML, x1=MR, color=LINE):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, IN(x0), IN(y), IN(x1 - x0), IN(0.012))
    ln.fill.solid(); ln.fill.fore_color.rgb = color; ln.line.fill.background()
    ln.shadow.inherit = False
    return ln


def panel(slide, x, y, w, h, fill=PANEL, line=LINE, r=0.07):
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, IN(x), IN(y), IN(w), IN(h))
    sp.adjustments[0] = r / min(w, h) if min(w, h) else r
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    return sp


def rect(slide, x, y, w, h, fill, line=None):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, IN(x), IN(y), IN(w), IN(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    return sp


def img_dims(p):
    with Image.open(p) as im: return im.size


def browser(slide, x, y, w, img, url='', max_h=None):
    """浏览器框装截图：读图真实比例 contain-fit，永不拉伸。返回图底 y 坐标。"""
    bar = 0.30
    mh = max_h or w * 9 / 16
    iw, ih = img_dims(img); a = iw / ih
    fw = w - 0.024; fh = fw / a
    if fh > mh - 0.024: fh = mh - 0.024; fw = fh * a
    fx = x + (w - fw) / 2
    panel(slide, fx - 0.012, y, fw + 0.024, bar + fh + 0.024, fill=WHITE, line=LINE, r=0.05)
    rect(slide, fx, y + 0.012, fw, bar - 0.02, SOFT)
    for i in range(3):
        d = slide.shapes.add_shape(MSO_SHAPE.OVAL, IN(fx + 0.13 + i * 0.13), IN(y + 0.10), IN(0.08), IN(0.08))
        d.fill.solid(); d.fill.fore_color.rgb = RGBColor(0xC9, 0xC2, 0xD2); d.line.fill.background(); d.shadow.inherit = False
    if url:
        tx(slide, url, fx + 0.52, y, fw - 0.7, bar, size=7, color=MUTE, valign='m')
    slide.shapes.add_picture(img, IN(fx), IN(y + bar + 0.012), IN(fw), IN(fh))
    return y + bar + fh


def ink_strip(slide, x, y, w, h, runs):
    rect(slide, x, y, w, h, INK)
    tx(slide, runs, x + 0.3, y, w - 0.6, h, size=12.5, color=WHITE, valign='m', lh=1.15)


def page_title(slide, tag, title):
    """板块标签 + 页题 + 分隔线；每页统一从这里开始。"""
    tx(slide, tag, ML, 0.62, 11.5, 0.3, size=11.5, bold=True, color=ACC, spacing=1.5)
    tx(slide, [(title, {'size': 27, 'bold': True, 'color': INK})], ML, 0.95, 11.6, 0.62)
    hr(slide, 1.72)


def feat(slide, x, y, w, head, desc, accent=False, num=None):
    """要点卡：可选 01/02 序号 + 标题 + 描述。"""
    dx = 0
    if num:
        tx(slide, num, x, y - 0.06, 0.5, 0.5, size=20, bold=True, color=ACC)
        dx = 0.55
    tx(slide, head, x + dx, y, w - dx, 0.35, size=13.5, bold=True, color=ACC_D if accent else INK)
    tx(slide, desc, x + dx, y + 0.38, w - dx, 0.85, size=10.5, color=BODY, lh=1.4)


def demo_slide(prs, tag, title, img, url, feats, img_left=False, note=''):
    """套路页 1：大图 + 右列要点（每页只讲一件事）。"""
    s = prs.slides.add_slide(prs.slide_layouts[1])
    page_title(s, tag, title)
    bw, by = 6.35, 2.05
    bx = ML if img_left else MR - bw
    browser(s, bx, by, bw, img, url, max_h=4.3)
    fx = bx + bw + 0.5 if img_left else ML
    fw = MR - fx if img_left else bx - ML - 0.5
    for i, f in enumerate(feats):
        fy = by + 0.12 + i * 1.42
        if i: hr(s, fy - 0.24, fx, fx + fw)
        feat(s, fx, fy, fw, f[0], f[1], accent=f[2] if len(f) > 2 else False)
    if note: s.notes_slide.notes_text_frame.text = note
    return s


def duo_slide(prs, tag, title, imgL, urlL, imgR, urlR, feats, note=''):
    """套路页 2：双图 + 右列要点。"""
    s = prs.slides.add_slide(prs.slide_layouts[1])
    page_title(s, tag, title)
    bw, by = 4.62, 2.05
    browser(s, ML, by, bw, imgL, urlL, max_h=4.3)
    browser(s, ML + bw + 0.4, by, bw, imgR, urlR, max_h=4.3)
    fx = ML + bw * 2 + 0.8; fw = MR - fx
    for i, f in enumerate(feats):
        fy = by + 0.1 + i * 1.52
        if i: hr(s, fy - 0.24, fx, fx + fw)
        feat(s, fx, fy, fw, f[0], f[1], accent=f[2] if len(f) > 2 else False)
    if note: s.notes_slide.notes_text_frame.text = note
    return s
