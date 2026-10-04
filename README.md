# ppt-deck

用官方 .pptx 模板做评审导向的路演/比赛/答辩 PPT 的可复用管线。从 L'Oréal BEAUTY TECHATHON 参赛作品（[EmpathyDesk](https://github.com/piemvibes-hue/empathy-desk)，18 页官方模板版）沉淀——8 版迭代 + 4 次评分表审查的完整教训。

```
模板解剖        素材拍摄          逐页构建            QA 双门禁
inspect-   ──▶ shoot.cjs ──▶ python-pptx ──▶ render.sh + qa-deck.py ──▶ deck.pptx
template.py    dsf=3 裁切     deck-helpers.py   每页 PNG + 口径断言
```

## 四步

```bash
# 1. 读模板：版式/主题色/字体/正文硬性要求（模板原文是最高权威）
python3 scripts/inspect-template.py "官方模板.pptx"

# 2. 拍素材：全景 dsf=2 + 组件裁切 dsf=3（折叠卡先点开）
BASE=http://localhost:5173 OUT=./shots node scripts/shoot.cjs

# 3. 构建：import deck-helpers 写 build.py
#    Presentation('模板.pptx') 直接加页；browser() 读图原比例 contain-fit 永不拉伸

# 4. QA：逐页渲染亲眼看 + 口径门禁强制
scripts/render.sh out.pptx renders/
python3 scripts/qa-deck.py out.pptx --slides 18 --require '95.7%' --ban '占位'
```

## 核心原则

| 原则 | 为什么 |
|---|---|
| `Presentation(模板)` 直接加页 | 自绘版式仿得像也会被判「没用官方模板」 |
| 页面表先行：每页=一个评审问题 | 功能目录评委记不住，评分点对齐页评委给得了分 |
| 截图 dsf=3 + contain-fit | 拉伸变形是最低级失分点，糊图救不回来 |
| 数字带口径+诚实标注栏 | 打平项也写——报喜不报忧的表反而降低可信度 |
| 渲染页逐张亲眼看 | 脚本没报错≠页面上没炸，每版都能修出 4-6 处 |

详版方法论+坑位全清单：[docs/method.md](docs/method.md)。Agent 端到端版：[SKILL.md](SKILL.md)。

## License

MIT
