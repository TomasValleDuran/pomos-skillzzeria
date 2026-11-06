# CLAUDE.md — <project name>

<One sentence: what this is and who it's for.>

## Stack
- <framework + version>, <language>, <package manager>
- UI: <component library>, <styling>, <icons>, <motion lib> — design decisions live in `DESIGN.md`
- Data: <db / API / auth>
- Deploy: <Vercel / EAS / Fly / …>

## Commands
```bash
<pm> install        # setup
<pm> run dev        # local dev server (port <n>)
<pm> run lint       # lint
<pm> run typecheck  # types
<pm> run test       # tests (single file: <pm> run test -- path)
```

## Layout
- `src/app/` — <routes/screens>
- `src/components/ui/` — design-system components (don't fork; extend)
- `src/lib/` — <utilities>
- <anything non-obvious about where things go>

## Conventions
- <naming, file structure, state management, data fetching patterns>
- UI: use semantic tokens only (no raw hex/px); every list/form has loading, empty and error states; check `DESIGN.md` before adding a component.
- Tests: <where, what style, what must be tested>
- Commits: <conventional commits? branch naming?>

## Gotchas
- <things that bit us: env vars needed, flaky services, generated files not to edit, platform quirks>

## Definition of done
- [ ] lint + typecheck + tests pass
- [ ] UI changes looked at in the browser/simulator (light + dark, mobile + desktop)
- [ ] `/ship-check` run for UI-heavy changes
