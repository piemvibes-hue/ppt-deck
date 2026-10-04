#!/usr/bin/env python3
"""模板解剖：把官方 .pptx 的版式/主题色/字体/硬性内容要求全部抖出来。
用法：python3 inspect-template.py <模板.pptx>
关键看三样：
  ① slide_layouts 叫什么、占位符是什么——加页时用 prs.slide_layouts[i]
  ② theme 里的 accent 色与字体——整套 deck 的色板从模板取不自己造
  ③ slides 正文文本——「内容需包含…」「请替换…」这类模板要求是最高权威"""
import sys, zipfile, re
from xml.etree import ElementTree as ET

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'

def texts(xml):
    return [t.text or '' for t in ET.fromstring(xml).iter(f'{A}t')]

f = sys.argv[1]
z = zipfile.ZipFile(f)
names = z.namelist()

print('=== slide layouts ===')
for n in sorted(n for n in names if re.match(r'ppt/slideLayouts/slideLayout\d+\.xml$', n)):
    xml = z.read(n).decode('utf-8', 'ignore')
    name = re.search(r'name="([^"]*)"', xml)
    ph = re.findall(r'ph type="([^"]*)"', xml)
    txt = ' '.join(texts(xml))[:120]
    print(f'{n}: name={name.group(1) if name else "?"} ph={ph}')
    if txt.strip(): print(f'   text: {txt}')

print('\n=== theme ===')
for n in names:
    if 'theme' in n and n.endswith('.xml'):
        xml = z.read(n).decode('utf-8', 'ignore')
        colors = re.findall(r'<a:(\w+)>\s*<a:(?:srgbClr val="([0-9A-Fa-f]{6})"|sysClr[^/]*lastClr="([0-9A-Fa-f]{6})")', xml)[:16]
        fonts = re.findall(r'typeface="([^"]+)"', xml)[:8]
        print(f'{n}: colors={colors} fonts={fonts}')

print('\n=== slides（模板正文=硬性要求，逐字读）===')
for n in sorted(n for n in names if re.match(r'ppt/slides/slide\d+\.xml$', n)):
    t = ' | '.join(s for s in texts(z.read(n).decode('utf-8','ignore')) if s.strip())
    print(f'{n}: {t[:400]}')
