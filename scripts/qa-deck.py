#!/usr/bin/env python3
"""deck 口径门禁：必检术语在位 + 禁用在场即挂 + 页数断言。
用法：python3 qa-deck.py out.pptx --slides 18 --require '95.7%' '风险召回' --ban 'TODO' '占位'
把评审会追问的数字/术语写进 --require（附口径注释）；占位词/乱码写进 --ban。"""
import re, sys, zipfile, argparse

ap = argparse.ArgumentParser()
ap.add_argument('pptx')
ap.add_argument('--slides', type=int, default=0)
ap.add_argument('--require', nargs='*', default=[])
ap.add_argument('--ban', nargs='*', default=['�', 'lorem', 'TODO', 'XX%', '占位', 'placeholder'])
a = ap.parse_args()

z = zipfile.ZipFile(a.pptx)
slide_names = sorted(n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n))
xml = ''.join(z.read(n).decode('utf-8', 'ignore') for n in slide_names)

missing = [t for t in a.require if t not in xml]
banned = [t for t in a.ban if t in xml]
print(f'页数: {len(slide_names)} | 必检 {len(a.require)} 缺 {len(missing)} | 禁用命中 {len(banned)}')
if missing: print('缺失:', missing)
if banned: print('命中禁用:', banned)
if a.slides and len(slide_names) != a.slides:
    print(f'页数不符：期望 {a.slides}')
ok = not missing and not banned and (not a.slides or len(slide_names) == a.slides)
sys.exit(0 if ok else 1)
