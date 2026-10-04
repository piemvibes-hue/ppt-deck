#!/usr/bin/env bash
# 逐页渲染 QA：LibreOffice → PDF → 每页 PNG（120dpi，用 pdftoppm）
# 用法：./render.sh out.pptx renders/
# 渲染页必看：脚本没报错≠页面上没炸——重点看文字溢出/贴底条/图层叠压/拉伸
set -euo pipefail
PPTX="$1"; OUT="${2:-renders}"
mkdir -p "$OUT"
soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
pdftoppm -png -r 120 "$PDF" "$OUT/page"
ls "$OUT"/page-*.png | wc -l | xargs echo "rendered pages:"
