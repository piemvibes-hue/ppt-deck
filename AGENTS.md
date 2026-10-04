# AGENTS.md — 给所有编程智能体的使用说明

本仓库是一个**可直接被 agent 执行的技能包**。你的任务是把「官方 .pptx 模板 + 真实产品 + 评审口径」做成一份逐页 QA 过的演示文档。

## 入口

读 `SKILL.md`——6 步执行规范。`docs/method.md` 是完整方法论与坑位清单。

## 目录即技能

仓库根目录本身就是合法 skill 目录（SKILL.md + scripts/ + docs/）。装载方式：

| 工具 | 装法 |
|---|---|
| Claude Code | 复制为 `<项目>/.claude/skills/ppt-deck/` 或 `~/.claude/skills/ppt-deck/` |
| Codex | 复制为 `<项目>/.codex/skills/ppt-deck/` |
| Devin | 复制为 `<项目>/.devin/skills/ppt-deck/` |
| 其他 agent | 把 `SKILL.md` 作为上下文喂给它，脚本按相对路径调用 |

## 执行契约

- `scripts/inspect-template.py <模板.pptx>`：必须先跑——模板正文里的硬性要求（板块名/封面要素/推荐字体）是最高权威
- `scripts/deck_helpers.py`：import 使用（`from deck_helpers import *`），`browser()` 保原比例
- `scripts/shoot.cjs`：截图模板，改 BASE 与登录路径后跑
- `scripts/render.sh out.pptx renders/`：LibreOffice 逐页 PNG——**每张亲眼看**，不许只跑脚本不渲染
- `scripts/qa-deck.py`：数字口径门禁——必检术语缺位/占位词命中即失败

## 不要做

- 不要 `Presentation()` 空白起稿仿模板——`Presentation(模板.pptx)` 直接加页
- 不要把图塞进固定宽高比的框——`browser()` 读图原比例 contain-fit
- 不要写完不渲染就交付——脚本没报错≠页面没炸
