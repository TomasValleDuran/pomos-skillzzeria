# UI/UX Skill Arsenal — inventory

Installed 2026-11-06 at user level (`~/.claude/skills/`, plugins via `claude plugin`), so they apply to every project. Our own skills live in the **pomos-skillzzeria** repo (`plugins/skillzzeria/skills/`) and are symlinked into `~/.claude/skills/` by its `scripts/install.sh`. Third-party skills were read in full before installing: all are plain Markdown (no scripts, no remote-instruction fetching), MIT licensed, each folder keeps its LICENSE.

## Our own (pomos-skillzzeria)

| Skill | Covers |
|---|---|
| `ui-ux-playbook` | Workflow, standards, routing, pre-ship checklist (this skill) |
| `ui-stack-advisor` | Component/animation/widget libraries for web + mobile, decision process |
| `design-system-builder` | Tokens, DTCG, theming, platform outputs, components, DESIGN.md |
| `color-theory` | Color theory + `palette.py` (OKLCH ramps, full light/dark systems, WCAG/APCA, CVD) |

## Third-party (vendored copies)

| Skill(s) | Source @ commit | Focus |
|---|---|---|
| `emil-design-eng`, `animate`, `review-animations`, `improve-animations`, `animation-performance`, `choreograph`, `animate-expo`, `mobile-native`, `apple-design` | github.com/emilkowalski/skills @ c8a7962 (2026-11-04) | Motion & interaction craft (Emil Kowalski — Sonner, Vaul; ex-Vercel/Linear) |
| `better-interface`, `better-colors`, `better-typography`, `better-accessibility`, `better-layout`, `better-ui`, `better-writing`, `interface-review`, `variant`, `state-machine`, `break` | github.com/jakubkrehel/skills @ 60bf140 (2026-11-01) | Precise review/fix rules per discipline; ranked reports. `variant`, `state-machine`, `break`, `interface-review` are user-invoked only |
| `mobile-design` | github.com/RubenGlez/mobile-design @ 97474ed | React Native/Expo mobile design, platform-aware |
| `interface-design` | github.com/Dammyjay93/interface-design @ 2f9be32 | Product UI (dashboards/SaaS) craft + design memory in `.interface-design/system.md` |
| Web Interface Guidelines (in `references/web-interface-guidelines.md`) | github.com/vercel-labs/web-interface-guidelines @ 434b7f9 | Code audit rules (vendored instead of fetched at runtime) |

## Plugins (official marketplace)

| Plugin | Gives |
|---|---|
| `frontend-design@claude-plugins-official` | `frontend-design` — aesthetic direction, anti-generic design |
| `expo@claude-plugins-official` | Official Expo skills: `expo-native-ui`, `expo-ui`, `expo-design-system`, `expo-animation`, `expo-router`, EAS, upgrades… |
| `vercel@claude-plugins-official` | `shadcn`, `nextjs`, `react-best-practices`, deployment skills |

## Considered, not installed (install if a project needs them)

| Skill | Why not by default | Install |
|---|---|---|
| **Impeccable** (pbakaus/impeccable, Apache-2.0) | Very popular all-in-one (24 commands: critique, audit, polish, bolder…) + deterministic anti-slop detector. Downloads a binary on first run and overlaps heavily with frontend-design/interface-design + the better-* set | `/plugin marketplace add pbakaus/impeccable` |
| **UI UX Pro Max** (nextlevelbuilder/ui-ux-pro-max-skill, MIT) | Searchable CSV database (styles, 192 palettes, 74 font pairings, UX rules) via Python; useful for style exploration, but overlaps color-theory/stack-advisor and tends to push "style catalog" looks | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` |
| **Taste Skill** (Leonxlnx/taste-skill, MIT) | Opinionated landing-page art direction with a browser checker (needs Node 22 + Chrome); great for marketing sites only | `/plugin marketplace add Leonxlnx/taste-skill` |
| Emil's `find-animation-opportunities`, `remove-animations`, `animation-vocabulary`, `break-ui`, `prototype`, `pick-ui-library`, `write-swift`, `ask-sonner` | Narrower; some overlap with installed ones | copy from the same repo |
| Jakub's `build-design`, `explain-interface`, `teardown` | Figma MCP covers build-design; teardown is illustration-specific | copy from the same repo |
| Apple-platform skills (e.g. rshankras/claude-code-apple-skills), AccessLint plugin | Add when doing native iOS or formal WCAG audits | see repos |

Avoid stacking several "aesthetic engines" (frontend-design + Impeccable + Taste + Pro Max) in one task — they give conflicting direction.

## Updating

`bash <skill-dir>/scripts/update-third-party.sh` (this skill's directory) clones the upstream repos into a temp folder and shows a diff against the installed copies. Nothing changes unless you re-run with `--apply`. Read the diff before applying — skills are instructions Claude follows. Plugins update via `claude plugin update <name>` / `/plugin`.
