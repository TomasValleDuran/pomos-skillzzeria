# 📖 Recipe · New project kickoff

Serves: any new web or mobile app. Prep time: ~30 min with Claude.

## Ingredients
- An idea + who it's for
- The Skillzzeria installed (`scripts/install.sh`) + the third-party UI arsenal (see `plugins/skillzzeria/skills/ui-ux-playbook/references/arsenal.md`)

## Steps
1. **Takeaway the starters**
   ```bash
   ~/projects/pomos-skillzzeria/scripts/takeaway.sh ~/projects/my-app --actions ci-node,claude-pr-review
   ```
   Copies CLAUDE.md, PR/issue templates, dependabot, .editorconfig and the chosen workflows (never overwrites).
2. **Brief** — tell Claude who it's for, the main job, and the feel in 3 concrete words. Ask it to use `ui-ux-playbook`.
3. **Pick the stack** — "use ui-stack-advisor to pick the UI stack for <platform>"; record the decision in DESIGN.md.
4. **Design system** — "use design-system-builder; brand color is #xxxxxx" → tokens + `DESIGN.md` (from the template).
5. **Fill CLAUDE.md** — commands, layout, conventions, gotchas. Keep it short and true.
6. **Build the first screen** end to end with all states; look at it at 390 and 1280, light and dark.
7. **`/ship-check`** before the first PR; let the `ui-critic` agent review bigger UI changes.
8. **GitHub** — `gh repo create`, add secrets (`CLAUDE_CODE_OAUTH_TOKEN`, `EXPO_TOKEN` if mobile), push.

## Chef's notes
- Decide once, write it down (DESIGN.md, CLAUDE.md). Future sessions read instead of re-deciding.
- If something here felt slow or repetitive, turn it into a skill (see `cooking-a-new-skill.md`).
