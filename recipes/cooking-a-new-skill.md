# 📖 Recipe · Cooking a new skill (or agent, or command)

## When something deserves to be on the menu
You did the same multi-step thing twice, corrected Claude the same way twice, or found knowledge Claude keeps getting wrong. That's a skill.

| Dish | Use for | Lives in |
|---|---|---|
| **Skill** 🍕 | Knowledge + workflow Claude loads automatically when relevant | `plugins/skillzzeria/skills/<name>/SKILL.md` |
| **Agent** 👨‍🍳 | A focused worker with its own context (reviewers, researchers) | `plugins/skillzzeria/agents/<name>.md` |
| **Command** 🧾 | Something *you* trigger with `/name` | `plugins/skillzzeria/commands/<name>.md` |
| **Pantry item** 🥫 | Copy-paste code: workflows, configs, snippets | `pantry/…` |

## Steps
1. Scaffold: `scripts/new-skill.sh my-skill` (or `--agent` / `--command`). It copies from `templates/`.
2. Write the **description** first — it's the only part Claude sees before deciding to load the skill. Say what it does *and* when to use it, a bit pushy, with the phrases users actually type.
3. Write the body: point of view → workflow → output format → references. Explain *why*, not just MUST. Keep SKILL.md under ~300 lines; move depth to `references/`, deterministic work to `scripts/`.
4. Easy way: ask Claude "use skill-creator to help me build a skill for X" — it interviews you, drafts, and can run test prompts with/without the skill.
5. `scripts/install.sh` (symlinks it locally — new skills appear in Claude Code right away).
6. Try it on 2–3 real prompts. Fix what's off. Repeat.
7. `python3 scripts/validate.py` → bump `version` in `plugins/skillzzeria/.claude-plugin/plugin.json` and the marketplace entry → commit → push.
8. Add a line to the menu in `README.md` (`python3 scripts/validate.py --menu` prints the table).

## Kitchen rules
- One skill = one job. Two jobs → two skills that reference each other.
- No secrets, no personal data, no hardcoded absolute paths (use paths relative to the skill's directory).
- Third-party skills you like: credit + license in the folder, or list them under "Guest chefs" in the README instead of copying.
