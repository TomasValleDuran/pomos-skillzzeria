#!/usr/bin/env bash
# 🥡 Takeaway: copy project starters (+ chosen GitHub Actions) into a project. Never overwrites.
#   scripts/takeaway.sh <project-dir> [--actions ci-node,claude-pr-review,...] [--snippets]
#   scripts/takeaway.sh --list
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PANTRY="$REPO/pantry"

if [[ "${1:-}" == "--list" || -z "${1:-}" ]]; then
  echo "usage: $0 <project-dir> [--actions a,b] [--snippets]"
  echo "actions:"; for f in "$PANTRY"/github-actions/*.yml; do echo "  - $(basename "$f" .yml)"; done
  exit 0
fi

TARGET="$1"; shift
[[ -d "$TARGET" ]] || { echo "no such directory: $TARGET"; exit 1; }
ACTIONS=""; SNIPPETS=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --actions) ACTIONS="$2"; shift 2 ;;
    --snippets) SNIPPETS=1; shift ;;
    *) echo "unknown option $1"; exit 1 ;;
  esac
done

put() { # src dest
  if [[ -e "$2" ]]; then echo "  = ${2#"$TARGET"/} exists, kept"; return; fi
  mkdir -p "$(dirname "$2")"; cp "$1" "$2"; echo "  + ${2#"$TARGET"/}"
}

echo "🥡 Packing starters into $TARGET"
( cd "$PANTRY/project-starters" && find . -type f ) | while read -r f; do
  put "$PANTRY/project-starters/${f#./}" "$TARGET/${f#./}"
done

if [[ -n "$ACTIONS" ]]; then
  IFS=',' read -ra list <<<"$ACTIONS"
  for a in "${list[@]}"; do
    src="$PANTRY/github-actions/$a.yml"
    [[ -f "$src" ]] || { echo "  ! unknown action $a (see --list)"; continue; }
    name="$a"; [[ "$a" == ci-* ]] && name="ci"; [[ "$a" == "claude-mention" ]] && name="claude"
    put "$src" "$TARGET/.github/workflows/$name.yml"
  done
fi

if (( SNIPPETS )); then
  ( cd "$PANTRY/snippets" && find . -type f ) | while read -r f; do
    put "$PANTRY/snippets/${f#./}" "$TARGET/snippets-from-skillzzeria/${f#./}"
  done
fi
echo "Done. Fill in CLAUDE.md, and add any secrets the workflows need (see pantry/github-actions/README.md)."
