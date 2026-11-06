# React / Next.js UI Libraries (snapshot Nov 2026)

## Layer model

```
Primitives (behavior + a11y, unstyled)  →  Styled kit / your design system  →  Blocks & templates
Base UI · Radix · React Aria · Ark UI       shadcn/ui · HeroUI · Mantine · MUI     shadcn blocks, registries
```

Pick primitives for correctness, a styled layer for speed, blocks for scaffolding.

## Headless primitives

| Library | Notes | Choose when |
|---|---|---|
| **Base UI** (`@base-ui/react`, MUI team; 1.0 stable early 2026) | ~35+ components, unstyled, render-prop composition, active team. shadcn's default since July 2026. | New design systems; long-term maintenance matters |
| **Radix Primitives** (`radix-ui` unified package) | Battle-tested, huge install base, slower development pace than Base UI | Existing Radix/shadcn projects; still fine for new ones |
| **React Aria Components** (Adobe) | Most rigorous a11y, i18n (RTL, calendars, number formatting), touch/keyboard normalization, drag & drop, virtualized collections | Accessibility-critical, international, complex widgets |
| **Ark UI** (Chakra team, Zag.js) | Same API across React/Vue/Solid/Svelte | Multi-framework design systems |
| **Headless UI** (Tailwind Labs) | Small set, Tailwind-native | Simple sites; Tailwind Plus users |

## Styled kits

| Kit | Style | Strengths | Trade-offs |
|---|---|---|---|
| **shadcn/ui** | Copy-in source, Tailwind v4, 8 visual styles, primitives selectable (Base UI / Radix / React Aria) | Ownership, registries ecosystem, CLI (`shadcn create`, presets, `apply`, `eject`), MCP server, AI Elements for chat/agent UIs | You maintain the code; defaults are recognizable — customize theme |
| **HeroUI v3** | Tailwind v4 + React Aria Components; also a React Native library | Polished look out of the box, strong a11y base | Opinionated look; check RN maturity |
| **Mantine** | CSS modules/vars, own styling | 100+ components, 70+ hooks, forms, dates, charts, notifications, Spotlight | Not Tailwind-native |
| **MUI v9 / Material UI** (+ MUI X v9) | Material Design, Emotion/Pigment CSS | Most complete; MUI X Data Grid, Date/Time pickers, Charts, Scheduler (alpha), Chat (alpha) | Heavy; looks Material unless deeply themed; advanced grid features are commercial |
| **Chakra UI v3** | Rewrite on Ark UI + Panda-style recipes | Good DX, theming with recipes/slots | v2→v3 migration churn |
| **Ant Design** | Enterprise | Huge set, data-dense patterns, pro components | Distinct look; bundle size |
| **Radix Themes** | Styled Radix | Beautiful defaults, Radix Colors | Less flexible than shadcn |
| **Park UI** | Styled Ark UI (Panda or Tailwind) | Multi-framework | Smaller community |
| **Tailwind Plus (ex Tailwind UI) / Catalyst** | Paid HTML/React templates + kit from Tailwind Labs | High craft | License cost |

## shadcn ecosystem (registries — install with `npx shadcn add <url or @registry/item>`)

Use selectively; each adds visual personality.

| Registry | Good for |
|---|---|
| shadcn blocks (official) | Dashboards, auth, sidebars, settings, charts (Recharts-based) |
| **Magic UI** | Marketing effects: marquees, number tickers, animated beams, globes, shimmer buttons |
| **Aceternity UI** | High-impact landing sections (spotlights, 3D cards, parallax). Heavy — use one or two |
| **Animate UI** | Animated versions of standard shadcn components (tabs, accordions, buttons) with Motion |
| **Motion Primitives** | Tasteful motion building blocks (text effects, morphing dialogs, in-view) |
| **React Bits** | 100+ animated text/background/interaction components (installs via jsrepo or shadcn) |
| **coss ui** (formerly Origin UI) | Large set of polished inputs, selects, buttons, primitives variations |
| **Kibo UI** | Composable advanced components (Gantt, kanban, editor, color picker) |
| **Cult UI**, **ReUI**, **Kokonut UI**, **Skiper UI** | More component/block variety |
| **tweakcn** | Visual theme editor that outputs shadcn CSS variables |
| **21st.dev** | Community marketplace of components; also an MCP ("magic") for generating components |

Rule: one "wow" effect per page section at most; respect `prefers-reduced-motion`; check bundle impact (many pull in Motion, three.js or canvas).

## Styling

- **Tailwind CSS v4**: CSS-first config (`@theme`, `@custom-variant`, `@utility`), OKLCH default palette, Lightning CSS engine, container queries built in. Default for new projects.
- **cva** (class-variance-authority) or **tailwind-variants** for typed variant APIs; `cn()` helper (shadcn now ships a `cn` package) for merging.
- Zero-runtime CSS-in-JS if not Tailwind: **vanilla-extract**, **Panda CSS**, **StyleX** (Meta), **Pigment CSS** (MUI).
- Avoid runtime CSS-in-JS (styled-components/Emotion) in React Server Components-heavy apps.

## Next.js specifics

- Prefer server components for layout; mark interactive leaves `"use client"`.
- Fonts via `next/font` (self-hosted, no CLS). Images via `next/image` with sizes.
- Theme switching without flash: `next-themes` (or an inline head script).
- View transitions: React `<ViewTransition>` / the View Transitions API for route changes (check current React/Next support before relying on it).
