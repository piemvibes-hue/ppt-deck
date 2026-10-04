---
name: ppt-deck
description: 用官方 .pptx 模板做一份评审导向的路演/比赛/答辩 PPT——模板解析→产品截图管线（高清不拉伸）→python-pptx 逐页构建→LibreOffice 逐页渲染 QA→口径门禁。用户要求「做 PPT/做 deck/做路演稿/套官方模板/答辩演示」且要求真实截图、正式交付时使用；不用于随手一版草稿。
---

# ppt-deck：模板级 PPT 制作管线

把「一份官方 .pptx 模板 + 一个真实产品 + 一套评审口径」变成一份逐页渲染 QA 过的演示文档。核心思想：**评审每个打分点对应一页，每页只讲一件事，每张图都是真机截图原比例缩放**。

## 流程（严格按序）

### 1. 读模板，不是看缩略图——解析 XML

```bash
python3 scripts/inspect-template.py <官方模板.pptx>
```

产出：版式清单（slide_layouts 各叫什么名字、占位符有什么）、主题色/字体、以及**正文里写着的硬性要求**（比如「内容需包含 A/B/C/D 四大板块」——模板原文是最高权威，比你的偏好和习惯排版都优先）。把四大板块逐字抄进工作笔记，后面每页归属一个板块。

### 2. 定页面表：每页只答一个评审问题

先写「页 → 评审问题 → 证据（哪张图哪组数）」三列对齐的页面表，**给用户过目再动手**。反例：按功能目录排页（评委记不住）；正解：按评审打分点排页。页数控制在模板要求±2 页内；四板块每块至少 1 页且标题带板块名。

### 3. 拍素材：dsf≥2 全景 + dsf=3 裁切

```bash
BASE=<产品地址> OUT=./shots node scripts/shoot.cjs
```

- 全景页 `deviceScaleFactor: 2`；关键组件单独裁切用 `deviceScaleFactor: 3`——投到 4-5 英寸宽槽位时约 390dpi，糊不了
- 折叠卡片/异步面板**先点开再截**；带交互证据的状态（填入的话术、拦截警告）先制造状态再截
- 命名即语义：`assist_card.png` 不是 `crop3.png`——构建脚本里看到名字就知道该放哪页

### 4. 构建：继承模板版式，不仿版式

```python
from pptx import Presentation
prs = Presentation('官方模板.pptx')   # 直接改模板文件：保留母版/主题/封面/尾页
s = prs.slides.add_slide(prs.slide_layouts[内容页索引])
```

- 用模板自带的 slide_layout 加页，别新建空白页自己画背景——评审认的是「用了官方模板」
- 封面按模板占位符要求填（作品名/赛道/队伍名），删掉模板自带的「请替换此处」注释块
- 统一 helper 只写一次（`scripts/deck-helpers.py`）：`tx()`（段内多 run 混排+字距）、`panel()`（圆角卡）、`browser()`（见下）、`page_title()`（板块标签+页题+分隔线）、`feat()`（编号卡）。每页 = `page_title` + 一种布局套路（demo_slide 左图右点 / duo_slide 双图 / 卡阵）
- **字体只指定一次**（模板推荐字体，如思源黑体 CN），`_ea` 把 latin/ea/cs 三个 typeface 全设了——中文漏设 ea 会渲染成宋体

### 5. 图片铁律：原比例缩放，永不拉伸

`browser(slide, x, y, w, img, url='', max_h=None)` 是资产级 helper——读 PNG 真实宽高比 contain-fit：框宽内放不下就缩高，细长卡（a>1）放宽框也不拉。长截图裁切比例从 0.34 到 10.0 都正确入框。**绝不要把图塞进固定 16:9 框**——那是拉伸变形的根源。

### 6. QA 双门禁：渲染 + 口径

```bash
scripts/render.sh out.pptx renders/   # LibreOffice → 每页 PNG
python3 scripts/qa-deck.py out.pptx --require '95.7%' '风险召回' --ban 'TODO' '占位' --slides 18
```

- **渲染页必看**——脚本层面没报错≠页面上没炸：重点看文字溢出卡片、图片贴住底条、长标题换行撞下一行、图层叠压
- 口径清单在脚本启动前从最新评测数据抄：数字写到 REQUIRED 数组时附带口径注释（哪个文件哪天复核），评审追问时讲得出
- 每页备注栏写讲稿口径（主张/数字来源/追问应答）——演示时点击幻灯片视图能看到

## 踩过的坑（全部真实）

| 症状 | 根因 | 解法 |
|---|---|---|
| 截图糊 | dsf=1 拍小卡片放大投屏 | 裁切一律 dsf=3 |
| 图变形 | 硬塞 16:9 框 | 读 PNG 真实比例 contain-fit |
| 中文变宋体 | 只设 latin typeface | `_ea` 三处 typeface 全设 |
| 长标题撞行 | 两栏标题各自换行重叠 | 标题截 6 字内+固定行距 |
| 页脚贴底条 | 内容高度顶满 | 槽高留 0.3in 余量，渲染后逐页核 |
| 「用了模板」不认账 | 自绘版式仿得像 | 直接 `Presentation(模板)` 加页 |
| 评委问数字口径 | 抄自旧稿未复核 | REQUIRED 数组+来源注释，QA 门禁强制 |

详版方法论与检查表：`docs/method.md`。
