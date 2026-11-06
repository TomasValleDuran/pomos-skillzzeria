---
name: design-system-builder
description: Create, extend, or audit a design system for any project and platform — design tokens (color, typography, spacing, radius, elevation, motion, breakpoints), token architecture (primitive → semantic → component), the W3C DTCG token format, theming (light/dark, brands, density), multi-platform output (CSS variables, Tailwind v4 @theme, React Native, Flutter, SwiftUI, Compose), component API conventions, documentation (DESIGN.md, Storybook) and governance. Use this whenever the user starts a new app and needs a visual foundation, says "design system", "design tokens", "theme", "style guide", "UI kit", "make it consistent", "set up Tailwind theme", wants to unify inconsistent UI, extract tokens from existing code or Figma, support dark mode or multiple brands, or share styles between web and mobile.
---

# Design System Builder

A design system is a set of **decisions made once** so that every screen doesn't re-decide them. Tokens hold the decisions, components apply them, documentation explains them. Scale the effort to the project: a weekend app needs a 40-line token file and a DESIGN.md; a multi-team product needs pipelines and governance. Start small, grow by extraction.

## Process

### 0. Read what exists
Look for: tokens/theme files, `tailwind` config or `@theme` blocks, `components.json`, CSS variables, a `theme/` module, Figma links (use the Figma MCP `get_variable_defs`/`search_design_system` if connected), `DESIGN.md`/`.interface-design/system.md`. In existing codebases, **extract before inventing**: grep the actual colors, font sizes, spacings and radii in use, cluster them, and propose the consolidated scale. Show the user the before→after mapping.

### 1. Define the direction (one paragraph)
Who uses it, what it should feel like (in concrete words: "dense like a trading terminal", "calm like a reading app"), platform(s), brand constraints, density, light/dark. This drives every scale choice below. If `interface-design` or `frontend-design` skills are in play, they own this aesthetic step; this skill turns the direction into a system.

### 2. Foundations (tokens)
Build in this order — each depends on the previous:

1. **Color** → run the `color-theory` skill's tool: `python3 <skills-dir>/color-theory/scripts/palette.py system <brand-hex> --format tailwind|css|json` (`color-theory` is a sibling of this skill's directory). It produces primitive ramps + verified light/dark semantic roles.
2. **Typography** → font families (≤2, plus mono), a type scale with named roles, line-heights, weights, tracking. See `references/scales.md`.
3. **Space** → 4px base grid; t-shirt or numeric scale; layout spacing separate from component padding.
4. **Shape** → radius scale (and a rule for nesting: inner radius = outer − padding), border widths.
5. **Elevation** → shadow scale (light) and surface-lightness steps (dark), z-index layers.
6. **Motion** → durations + easings as tokens (and reduced-motion behavior).
7. **Layout** → breakpoints, container widths, grid columns, safe areas (mobile).
8. **Sizing** → control heights (sm/md/lg), icon sizes, minimum touch target.

### 3. Token architecture
Three tiers — components must only consume the semantic (or component) tier:

```
primitive   --blue-600, --space-4, --radius-2          raw values, named by what they ARE
semantic    --color-accent, --space-inset-md, --radius-control   named by JOB, aliases primitives, switch per theme
component   --button-bg, --card-padding                 optional; only for components with real theming needs
```

Theme switching (dark mode, brands, density, high contrast) = repointing semantic tokens. Components never change. Full naming rules, DTCG format, modes: `references/token-architecture.md`.

### 4. Ship to the platform(s)
- Single web app: hand-written CSS variables + Tailwind v4 `@theme` is enough.
- Web + mobile, or multiple apps: author tokens in **DTCG JSON** (one source), build with **Style Dictionary v5** or **Terrazzo** to CSS, Tailwind, TS, Swift, Kotlin/Compose, Flutter, RN.
Recipes and output examples per platform: `references/platform-outputs.md`. Starter DTCG file: `assets/tokens.example.json`.

### 5. Components
Build on accessible primitives (see `ui-stack-advisor`). Consistent API: `variant` (visual intent), `size`, `tone`/`color` only if needed, states via data attributes, composition over configuration. Every component documents all states: default, hover, active, focus-visible, disabled, loading, error, empty, selected, read-only. Conventions and checklist: `references/components.md`.

### 6. Document & govern
Write `DESIGN.md` at the project root from `assets/DESIGN.template.md` — direction, tokens table, component inventory, do/don't, and the *why* behind decisions. This file is what future sessions read to stay consistent; keep it short and current. Larger systems add Storybook (or Ladle/Histoire), visual regression, a changelog with semver, and a contribution process (`references/components.md#governance`).

## Defaults that work (when the user has no preference)

| Foundation | Default |
|---|---|
| Base unit | 4px; spacing scale 0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96 px |
| Type scale | 12, 14, 16 (body), 18, 20, 24, 30, 36, 48, 60 px (≈1.2–1.25 ratio); product UIs can use 14px body |
| Line height | 1.5 body, 1.2–1.3 headings, 1.1 display; tighten tracking on large sizes (−0.01 to −0.03em) |
| Radius | 0, 4, 6, 8, 12, 16, 24, full — pick a *personality*: sharp (2–4), soft (8–12), round (16+) and apply consistently |
| Controls | heights 32 / 36–40 / 44–48 px; touch targets ≥ 44pt (iOS) / 48dp (Android) / 24px min WCAG 2.2 (aim 44) |
| Motion | 100 / 150 / 200 / 300 / 500 ms; ease-out `cubic-bezier(0.23,1,0.32,1)` for enter, ease-in-out for move, springs on mobile |
| Breakpoints | 640, 768, 1024, 1280, 1536 (Tailwind); prefer container queries for components |
| Elevation | 4–5 shadow levels; dark mode uses lighter surfaces + subtle borders instead |
| Z-index | base 0, dropdown 1000, sticky 1100, overlay 1300, modal 1400, popover 1500, toast 1600, tooltip 1700 |

Defaults are a floor, not a style. The distinctiveness comes from the choices that vary: typeface, accent hue, neutral temperature, radius personality, density, and motion character.

## Quality bar (check before calling it done)
- [ ] No raw values in components (hex, px font sizes, arbitrary spacing) — grep for them
- [ ] Semantic names describe jobs, not values or hues
- [ ] Light + dark both designed and contrast-verified (WCAG 2.2 AA)
- [ ] Every interactive component has visible focus, disabled, loading, error states
- [ ] Type scale has named roles (display, h1–h3, body, label, caption, code), not just sizes
- [ ] Spacing consistent: same relationship → same token
- [ ] Reduced-motion variant for motion tokens
- [ ] DESIGN.md written and accurate
- [ ] Mobile: Dynamic Type / font scaling respected, safe areas tokenized, touch targets ≥ 44/48

## References
- `references/token-architecture.md` — tiers, naming grammar, DTCG 2025.10 format, modes/themes, aliasing rules
- `references/scales.md` — typography (scales, fluid type, pairing), spacing, radius, elevation, motion, density, breakpoints
- `references/platform-outputs.md` — CSS, Tailwind v4, shadcn theming, React Native (NativeWind/Unistyles/Tamagui), Flutter, SwiftUI, Compose, Style Dictionary/Terrazzo pipeline
- `references/components.md` — component API conventions, anatomy, states matrix, composition, docs, testing, governance
- `assets/tokens.example.json` — starter DTCG token file
- `assets/DESIGN.template.md` — DESIGN.md template
