#!/usr/bin/env bash
# Render a few stills of a Remotion composition and tile them into one image to review composition fast.
#   contact_sheet.sh <entry> <composition> <out.png> <frame> [frame...]
#   e.g. (from the project root)  contact_sheet.sh src/index.tsx Main out/sheet.png 30 120 300 450 600 900
# 3 columns, 640x360 tiles. Stills are rendered with --gl=angle and audio disabled.
set -euo pipefail
[[ $# -ge 4 ]] || { sed -n 2,5p "$0"; exit 1; }
ENTRY="$1"; COMP="$2"; OUT="$3"; shift 3
mkdir -p "$(dirname "$OUT")"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
inputs=(); i=0
for fr in "$@"; do
  npx remotion still "$ENTRY" "$COMP" "$TMP/f$i.png" --frame="$fr" --gl="${GL:-angle}" --props='{"audio":null}' --log=error
  inputs+=(-i "$TMP/f$i.png"); i=$((i + 1))
done
n=$i; cols=3; rows=$(( (n + cols - 1) / cols ))
filter=""; for ((k = 0; k < n; k++)); do filter+="[$k]scale=640:360[s$k];"; done
# pad the last row with black tiles
for ((k = n; k < rows * cols; k++)); do filter+="color=c=black:s=640x360:d=1[s$k];"; done
for ((r = 0; r < rows; r++)); do
  for ((c = 0; c < cols; c++)); do filter+="[s$((r * cols + c))]"; done
  filter+="hstack=$cols[r$r];"
done
if [[ $rows -gt 1 ]]; then for ((r = 0; r < rows; r++)); do filter+="[r$r]"; done; filter+="vstack=$rows[o]"; else filter+="[r0]null[o]"; fi
ffmpeg -y -loglevel error "${inputs[@]}" -filter_complex "$filter" -map "[o]" -frames:v 1 "$OUT"
echo "contact sheet → $OUT ($n frames)"
