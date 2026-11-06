---
description: Run the pre-ship UI checklist on a screen, component or the current branch, and fix what's safe to fix.
argument-hint: "[file, route or component — defaults to UI files changed on this branch]"
---

Run a pre-ship UI pass on: $ARGUMENTS (if empty, the UI files changed on the current branch).

1. Load the `ui-ux-playbook` skill and use its **Pre-ship UI checklist** as the rubric; for web code also apply `references/web-interface-guidelines.md`.
2. Read the project's `DESIGN.md` / token files first — the project's system wins over generic advice.
3. If a dev server is running or can be started, render the target at 390px and 1280px in light and dark and look at it.
4. Report a table: `| Severity | Location | Issue | Fix |`, most severe first.
5. Apply fixes that are mechanical and low-risk (missing labels, `transition: all`, missing `type`/`autocomplete`, reduced-motion guards, raw values that map 1:1 to an existing token). List design-judgment fixes for the user instead of applying them.
6. Finish with what was verified, what wasn't, and a one-line verdict.
