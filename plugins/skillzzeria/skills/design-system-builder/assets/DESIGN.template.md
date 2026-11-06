# DESIGN.md — <Product name>

> Source of truth for how this product looks, feels and behaves. Read before building UI; update when a decision changes. Keep it short.

## Direction
- **Who**: <the actual person + context, e.g. "ops lead triaging incidents on a laptop between meetings">
- **Job**: <the main verb(s) the UI serves>
- **Feel**: <3 concrete words, e.g. "dense, calm, precise"> — and what it is NOT: <e.g. "not playful, not glossy">
- **Platforms**: <web / iOS / Android / RN / Flutter> · **Themes**: <light, dark> · **Density**: <comfortable/compact>
- **References**: <2–4 real products or screens that capture the bar>

## Stack
| Layer | Choice | Why |
|---|---|---|
| Components | <e.g. shadcn/ui (Base UI) + Tailwind v4> | |
| Icons | <e.g. Lucide, 1.5px stroke> | |
| Motion | <e.g. CSS + Motion for layout/exit> | |
| Fonts | <e.g. Inter Variable (UI), Geist Mono (code)> | |
| Charts | <e.g. Recharts> | |

## Tokens
Source: `<path to tokens file>` — never use raw values in components.

**Color roles** (light / dark)
| Role | Light | Dark | Use |
|---|---|---|---|
| bg | neutral-50 | neutral-950 | page |
| surface | white | neutral-900 | cards, panels |
| text / text-muted | neutral-950 / 600 | neutral-50 / 400 | |
| border / border-control | neutral-200 / 500 | neutral-800 / 500 | dividers / inputs (3:1) |
| accent / accent-fg | accent-600 / white | accent-400 / accent-950 | primary actions only |
| danger / success / warning / info | … | … | status, always with icon + text |

**Type**: <family>, scale <ratio>; roles: display, h1, h2, h3, body (<size>/<lh>), label, caption, code.
**Space**: 4px grid; <common steps>. **Radius**: <personality + values; nested rule>. **Elevation**: <levels>. **Motion**: <durations, easings, reduced-motion behavior>.

## Components
| Component | Status | Notes |
|---|---|---|
| Button | ✅ | variants: solid, soft, outline, ghost; sizes sm/md/lg |
| … | | |

## Rules
- One filled primary action per view.
- Every list/table has designed empty, loading and error states.
- Focus visible on every interactive element; never remove outlines without replacement.
- <product-specific rules: e.g. "numbers right-aligned, tabular", "destructive actions require undo or confirm">

## Decisions log
| Date | Decision | Why |
|---|---|---|
| <YYYY-MM-DD> | <e.g. accent moved from 500 to 600> | <contrast 4.5:1 on white> |
