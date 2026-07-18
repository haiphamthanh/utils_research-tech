#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 scripts/generate_figures.py
mkdir -p pdf

pandoc source/hieu_va_ung_dung_ai_trong_cong_viec.md \
  --from markdown+raw_tex \
  --pdf-engine=xelatex \
  --number-sections \
  --top-level-division=chapter \
  -V mainfont='DejaVu Sans' \
  -V monofont='DejaVu Sans' \
  -V sansfont='DejaVu Sans' \
  -V papersize=a4 \
  -o pdf/hieu_va_ung_dung_ai_trong_cong_viec.pdf

echo "Created pdf/hieu_va_ung_dung_ai_trong_cong_viec.pdf"
