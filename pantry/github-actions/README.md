# 🥫 Pantry · GitHub Actions

Copy-paste workflows. Drop them in a project's `.github/workflows/` (or run `scripts/takeaway.sh <project> --actions <names>`).

| Workflow | What it does | Secrets |
|---|---|---|
| `ci-node.yml` | Lint, typecheck, test, build for Node/TS; detects npm/pnpm/yarn; skips missing scripts | — |
| `ci-python.yml` | uv + ruff + pytest on 3.12/3.13 | — |
| `claude-pr-review.yml` | Claude reviews each PR with the Skillzzeria plugin loaded (UI checklist on UI changes) | `CLAUDE_CODE_OAUTH_TOKEN` |
| `claude-mention.yml` | `@claude` in issues/PRs → Claude answers or implements | `CLAUDE_CODE_OAUTH_TOKEN` |
| `expo-eas-preview.yml` | EAS Update per PR + QR comment | `EXPO_TOKEN` |

Also see `../project-starters/.github/dependabot.yml` (keeps actions + npm deps fresh).

Versions pinned as of 2026-11: `actions/checkout@v7`, `actions/setup-node@v7`, `pnpm/action-setup@v6`, `astral-sh/setup-uv@v10.3.3`, `anthropics/claude-code-action@v1`, `expo/expo-github-action@v8`. Dependabot will bump them.

Claude setup in a repo: run `/install-github-app` inside Claude Code (installs the app + secret), or install the app manually and add `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`.

Ideas to add next: release-please / changesets release, Vercel preview comments, Lighthouse CI budget, Playwright e2e with artifacts, EAS build on tag.
