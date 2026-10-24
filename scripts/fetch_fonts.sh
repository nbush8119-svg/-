#!/usr/bin/env bash
# 下载画面和封面渲染用的 Noto CJK 字体（SIL OFL 1.1）到指定目录。
# 用法：scripts/fetch_fonts.sh episodes/02-philosophy/kit/fonts
set -euo pipefail
DEST="${1:-fonts}"; mkdir -p "$DEST"
BASE=https://github.com/notofonts/noto-cjk/raw/main
for f in Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Medium.otf \
         Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf \
         Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Black.otf \
         Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Black.otf; do
  out="$DEST/$(basename "$f")"
  [ -s "$out" ] && { echo "已有 $out"; continue; }
  echo "下载 $out"; curl -fL --retry 3 -o "$out" "$BASE/$f"
done
