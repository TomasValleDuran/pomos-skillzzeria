# 🍕 Pomo's Skillzzeria

> *Homemade skills, agents & workflows for Claude Code. Wood-fired since 2026. Not the biggest menu in town — but every dish is ours.*

```
        (  )   (   )  )
         ) (   )  (  (
         ( )  (    ) )
         _____________
        <_____________> ___
        |             |/ _ \
        |  SKILLZZERIA  | | |
        |             |_| |
     ___|             |\___/
    /    \___________/    \
    \_____________________/
```

## 🛵 Delivery (install)

**On this machine (live edits):**
```bash
git clone https://github.com/TomasValleDuran/pomos-skillzzeria ~/projects/pomos-skillzzeria
~/projects/pomos-skillzzeria/scripts/install.sh      # symlinks skills/agents/commands into ~/.claude
```

**Anywhere else (as a Claude Code plugin):**
```
/plugin marketplace add TomasValleDuran/pomos-skillzzeria
/plugin install skillzzeria@pomos-skillzzeria
```
Pick one method per machine, or every skill shows up twice.

## 📜 The Menu

### 🍕 Pizzas (skills): Claude grabs these automatically when they're relevant

| Skill | What it does |
|---|---|
| `ui-ux-playbook` | 🍕 **Margherita della casa.** The place to start for any UI/UX work: the workflow, the standards (WCAG 2.2, HIG, Material 3, Core Web Vitals), a pre-ship checklist, and which skill to use for what |
| `ui-stack-advisor` | 🍕 **Quattro Stagioni.** Component, animation and widget libraries for web (React/Vue/Svelte/Angular) and mobile (RN/Expo, Flutter, SwiftUI, Compose), plus how to pick one |
| `design-system-builder` | 🍕 **Capricciosa.** Tokens, the W3C DTCG format, theming, multi-platform outputs, component conventions, and a DESIGN.md template |
| `promo-video-3d` | 🍕 **Calzone.** A 30–45 s 3D promo/intro video in code: Remotion + three.js with bloom, the real app on a 3D phone, a soundtrack synthesized on the beat grid, QR call-to-action. Starter kit, render checks, lessons learned |
| `color-theory` | 🍕 **Diavola.** Color theory plus `palette.py`: one hex → full OKLCH light/dark system with every contrast pair checked (WCAG + APCA) and a color-blindness check |

### 👨‍🍳 Chefs (agents): workers with their own context

| Agent | What it does |
|---|---|
| `ui-critic` | Read-only reviewer that gives a ranked UI/UX critique against the project's design system |

### 🧾 Orders (slash commands): you call them

| Command | What it does |
|---|---|
| `/ship-check` | Pre-ship UI checklist on a screen or branch; fixes the safe stuff and reports the rest |

### 🥫 Pantry: copy-paste ingredients

| Shelf | Contents |
|---|---|
| [`pantry/github-actions/`](pantry/github-actions/) | CI for Node and Python, Claude PR review (with this menu loaded), `@claude` mentions, Expo EAS previews |
| [`pantry/project-starters/`](pantry/project-starters/) | `CLAUDE.md` template, PR and issue templates, dependabot, `.editorconfig` |
| [`pantry/snippets/`](pantry/snippets/) | UI baseline CSS, no-flash theme script, React media-query hooks |

🥡 **Takeaway** packs the starters (plus any workflows you pick) into a project. It never overwrites existing files:
```bash
scripts/takeaway.sh ~/projects/my-app --actions ci-node,claude-pr-review --snippets
scripts/takeaway.sh --list
```

### 📖 Recipes: how we do things

- [New project kickoff](recipes/new-project-kickoff.md)
- [Cooking a new skill, agent or command](recipes/cooking-a-new-skill.md)

### 🍷 Guest chefs: third-party skills we love (not ours, installed separately)

Emil Kowalski's motion skills · Jakub Krehel's `better-*` skills · `mobile-design` · `interface-design` · Anthropic's `frontend-design` · the official Expo plugin. Full list, sources and update script: [`arsenal.md`](plugins/skillzzeria/skills/ui-ux-playbook/references/arsenal.md).

## 🔪 Kitchen tools

| Script | Does |
|---|---|
| `scripts/install.sh [--uninstall]` | Symlink everything into `~/.claude` (or remove only our links) |
| `scripts/new-skill.sh <name> [--agent\|--command]` | Start a new dish from `templates/` |
| `scripts/takeaway.sh <dir> [--actions …] [--snippets]` | Copy starters and workflows into a project |
| `python3 scripts/validate.py [--menu]` | Health inspection (runs in CI too), or print the menu tables |

## 🏗️ Floor plan

```
.claude-plugin/marketplace.json      ← makes this repo installable with /plugin
plugins/skillzzeria/                 ← the house plugin (add more plugins next to it)
  ├── .claude-plugin/plugin.json
  ├── skills/<name>/SKILL.md         ← 🍕
  ├── agents/<name>.md               ← 👨‍🍳
  └── commands/<name>.md             ← 🧾
pantry/                              ← 🥫 workflows, starters, snippets
recipes/                             ← 📖 playbooks
templates/                           ← blank recipe cards
scripts/                             ← 🔪 kitchen tools
```

## 🧾 House rules
1. One skill, one job.
2. The description decides when a skill gets used. Write it like a menu: what's in it and when to order it.
3. No secrets and no absolute paths. Validate before you serve (`python3 scripts/validate.py`).
4. Bump the plugin `version` when the menu changes.

MIT © pomo
