#!/usr/bin/env bash
# 🛵 Delivery: symlink every skill, agent and command from this repo into ~/.claude so Claude Code
# picks them up in every project. Edits in the repo are live immediately (they're symlinks).
#
#   scripts/install.sh              install / refresh links
#   scripts/install.sh --uninstall  remove only the links that point into this repo
#
# On machines where you'd rather not clone, use the plugin instead (don't do both on one machine,
# or each skill shows up twice):
#   /plugin marketplace add TomasValleDuran/pomos-skillzzeria
#   /plugin install skillzzeria@pomos-skillzzeria
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MODE="${1:-install}"

link() { # src dest
  local src="$1" dest="$2"
  if [[ -L "$dest" ]]; then
    if [[ "$(readlink "$dest")" == "$src" ]]; then echo "  = $(basename "$dest")"; return; fi
    case "$(readlink "$dest")" in "$REPO"/*) rm "$dest";; *) echo "  ! $(basename "$dest") is linked elsewhere — skipped"; return;; esac
  elif [[ -e "$dest" ]]; then
    echo "  ! $(basename "$dest") already exists (not ours) — skipped"; return
  fi
  ln -s "$src" "$dest" && echo "  + $(basename "$dest")"
}

unlink_ours() { # dir
  for f in "$1"/*; do
    [[ -L "$f" ]] || continue
    case "$(readlink "$f")" in "$REPO"/*) rm "$f" && echo "  - $(basename "$f")";; esac
  done
}

mkdir -p "$CLAUDE/skills" "$CLAUDE/agents" "$CLAUDE/commands"

if [[ "$MODE" == "--uninstall" ]]; then
  echo "🧹 Clearing the table"
  unlink_ours "$CLAUDE/skills"; unlink_ours "$CLAUDE/agents"; unlink_ours "$CLAUDE/commands"
  exit 0
fi

echo "🍕 Skills";   for d in "$REPO"/plugins/*/skills/*/;  do [[ -f "$d/SKILL.md" ]] && link "${d%/}" "$CLAUDE/skills/$(basename "$d")"; done
echo "👨‍🍳 Agents";  for f in "$REPO"/plugins/*/agents/*.md;   do [[ -e "$f" ]] && link "$f" "$CLAUDE/agents/$(basename "$f")"; done
echo "🧾 Commands"; for f in "$REPO"/plugins/*/commands/*.md; do [[ -e "$f" ]] && link "$f" "$CLAUDE/commands/$(basename "$f")"; done
echo "Buon appetito. New skills show up in Claude Code right away; agents/commands may need a new session."
