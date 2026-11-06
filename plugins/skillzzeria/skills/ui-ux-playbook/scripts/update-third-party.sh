#!/usr/bin/env bash
# Show (and optionally apply) upstream changes to the vendored third-party UI skills.
# Usage: update-third-party.sh            -> diff only (safe, changes nothing)
#        update-third-party.sh --apply    -> overwrite installed copies with upstream
set -euo pipefail

APPLY=0; [[ "${1:-}" == "--apply" ]] && APPLY=1
DEST="$HOME/.claude/skills"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# repo | path-in-repo-containing-skill-dirs | skills...
SOURCES=(
  "emilkowalski/skills|skills|emil-design-eng animate review-animations improve-animations animation-performance choreograph animate-expo mobile-native apple-design"
  "jakubkrehel/skills|skills|better-interface better-colors better-typography better-accessibility better-layout better-ui better-writing interface-review variant state-machine break"
  "Dammyjay93/interface-design|.claude/skills|interface-design"
)

changed=0
for entry in "${SOURCES[@]}"; do
  IFS='|' read -r repo base skills <<<"$entry"
  dir="$TMP/${repo//\//_}"
  git clone -q --depth 1 "https://github.com/$repo.git" "$dir"
  echo "== $repo @ $(git -C "$dir" rev-parse --short HEAD)"
  for s in $skills; do
    src="$dir/$base/$s"
    [[ -d "$src" ]] || { echo "  !! $s no longer exists upstream"; continue; }
    if diff -rq -x agents -x LICENSE "$src" "$DEST/$s" >/dev/null 2>&1; then
      echo "  = $s"
    else
      changed=1; echo "  ~ $s changed:"
      diff -ru -x agents -x LICENSE "$DEST/$s" "$src" | sed 's/^/      /' | head -80 || true
      if (( APPLY )); then
        rm -rf "$DEST/$s"; cp -R "$src" "$DEST/$s"; rm -rf "$DEST/$s/agents"
        cp "$dir/LICENSE" "$DEST/$s/LICENSE" 2>/dev/null || true
        echo "    -> applied"
      fi
    fi
  done
done

# mobile-design lives at the repo root
dir="$TMP/mobile-design"; git clone -q --depth 1 https://github.com/RubenGlez/mobile-design.git "$dir"
echo "== RubenGlez/mobile-design @ $(git -C "$dir" rev-parse --short HEAD)"
if diff -rq "$dir/SKILL.md" "$DEST/mobile-design/SKILL.md" >/dev/null && diff -rq "$dir/references" "$DEST/mobile-design/references" >/dev/null; then
  echo "  = mobile-design"
else
  changed=1; echo "  ~ mobile-design changed"
  diff -ru "$DEST/mobile-design/references" "$dir/references" | sed 's/^/      /' | head -60 || true
  diff -u "$DEST/mobile-design/SKILL.md" "$dir/SKILL.md" | sed 's/^/      /' | head -60 || true
  if (( APPLY )); then
    rm -rf "$DEST/mobile-design"; mkdir -p "$DEST/mobile-design"
    cp -R "$dir/SKILL.md" "$dir/references" "$dir/LICENSE" "$DEST/mobile-design/"; echo "    -> applied"
  fi
fi

echo
(( changed )) && (( ! APPLY )) && echo "Review the diffs above, then re-run with --apply to update." || true
echo "Web Interface Guidelines are vendored in ui-ux-playbook/references; compare manually with"
echo "https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md"
