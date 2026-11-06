#!/usr/bin/env bash
# 🔪 Prep a new dish from the templates.
#   scripts/new-skill.sh my-skill            -> plugins/skillzzeria/skills/my-skill/SKILL.md
#   scripts/new-skill.sh my-agent --agent    -> plugins/skillzzeria/agents/my-agent.md
#   scripts/new-skill.sh my-cmd --command    -> plugins/skillzzeria/commands/my-cmd.md
#   PLUGIN=other scripts/new-skill.sh x      -> into plugins/other/ instead
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:-}"; KIND="${2:---skill}"; PLUGIN="${PLUGIN:-skillzzeria}"
[[ "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "usage: $0 <kebab-case-name> [--agent|--command]"; exit 1; }

P="$REPO/plugins/$PLUGIN"
case "$KIND" in
  --skill)   dest="$P/skills/$NAME/SKILL.md"; src="$REPO/templates/skill/SKILL.md"; mkdir -p "$P/skills/$NAME" ;;
  --agent)   dest="$P/agents/$NAME.md";       src="$REPO/templates/agent.md";       mkdir -p "$P/agents" ;;
  --command) dest="$P/commands/$NAME.md";     src="$REPO/templates/command.md";     mkdir -p "$P/commands" ;;
  *) echo "unknown kind $KIND"; exit 1 ;;
esac
[[ -e "$dest" ]] && { echo "already on the menu: $dest"; exit 1; }

TITLE="$(echo "$NAME" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')"
sed -e "s/__NAME__/$NAME/g" -e "s/__TITLE__/$TITLE/g" "$src" > "$dest"
echo "🍳 Prepped $dest"
echo "Next: fill in the description (it decides when Claude uses it), then scripts/install.sh"
