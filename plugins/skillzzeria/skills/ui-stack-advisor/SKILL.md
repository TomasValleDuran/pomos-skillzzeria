---
name: ui-stack-advisor
description: Curated, up-to-date knowledge of UI component libraries, animation libraries and building blocks (icons, charts, tables, forms, toasts, drag-and-drop, virtualization, rich text) for web (React, Next.js, Vue, Svelte, Solid, Angular) and mobile (React Native/Expo, Flutter, SwiftUI, Jetpack Compose), with a decision process for picking one. Use this whenever a project is being started or scaffolded, when the user asks "which UI library / component library / design kit should I use", compares libraries (shadcn vs MUI vs Mantine, Tamagui vs NativeWind, etc.), needs a specific widget (date picker, data table, command palette, carousel, bottom sheet, chart), wants "cool animated components", or when you are about to hand-roll a component that a mature library already solves well.
---

# UI Stack Advisor

Picking the stack is the highest-leverage UI decision in a project: it fixes accessibility quality, theming flexibility, bundle size and how "templated" the result looks. Make the pick deliberately, once, and write it down.

Knowledge snapshot: **November 2026**. Libraries move fast — before installing, confirm the current major version and API (see *Freshness check*). Prefer what's already in the project over anything listed here.

## Step 1 — Read the project first

Check `package.json` / `pubspec.yaml` / `Package.swift` / `build.gradle` for existing UI libs, styling (Tailwind version, CSS-in-JS), framework version, and any `components.json` (shadcn), `DESIGN.md`, or token files. **Don't introduce a second component library next to an existing one** — extend the existing one or wrap it. If the project already uses a competitor to a recommendation here, mention it but don't churn dependencies unasked.

## Step 2 — Answer five questions

1. **Platform(s)**: web only, mobile only, or both from one codebase?
2. **Ownership**: copy-in source you own and restyle freely (shadcn model) vs. a versioned dependency with a theme API (MUI/Mantine model)? Copy-in = maximum design freedom + you maintain it. Dependency = faster, consistent, upgrades for free, harder to make distinctive.
3. **Product type**: marketing/landing (expressive, motion-heavy), product UI/dashboard (dense, consistent, keyboard-friendly), content (typography-first), mobile consumer app (native feel, gestures).
4. **Accessibility bar**: public sector / enterprise / EU (European Accessibility Act) → choose primitives with proven a11y (React Aria, Base UI, Radix) and don't hand-roll interactive widgets.
5. **Styling system**: Tailwind v4 (default for new web projects), CSS Modules/vanilla-extract, or CSS-in-JS; on RN: NativeWind vs Unistyles vs Tamagui.

## Step 3 — Default picks (when nothing else constrains)

| Situation | Default | Why |
|---|---|---|
| React/Next.js product UI | **shadcn/ui** (Base UI primitives — the default since July 2026; Radix and React Aria also supported) + Tailwind v4 | You own the code, great a11y, huge ecosystem of registries, AI tooling knows it well |
| React, accessibility-critical / complex widgets (date ranges, comboboxes, drag & drop, i18n) | **React Aria Components** (or shadcn's React Aria variant / HeroUI v3, which is built on it) | Most rigorous a11y + i18n behavior |
| React, batteries-included, no Tailwind | **Mantine** | 100+ components + hooks + forms + dates, strong docs |
| React, enterprise/Material look or heavy data grids | **MUI v9** (+ MUI X Data Grid/Date Pickers/Charts) | Mature, complete; harder to make distinctive |
| Enterprise admin (esp. CN/APAC teams) | **Ant Design** | Huge component set, data-dense patterns |
| Vue / Nuxt | **Nuxt UI v4** (free, built on Reka UI + Tailwind v4) or **shadcn-vue** | |
| Svelte / SvelteKit | **shadcn-svelte** (on Bits UI) | |
| Solid | **Kobalte** / solid-ui (shadcn port) / Ark UI | |
| Angular | **Spartan UI** (shadcn-like) or Angular Material / PrimeNG | |
| Framework-agnostic primitives | **Ark UI** (Zag.js state machines; React/Vue/Solid/Svelte) | |
| Marketing / landing page flair | shadcn + **Motion** + selected pieces from Magic UI / Aceternity / Animate UI / React Bits | Use 1–3 signature effects, not a collage |
| React Native / Expo (new app) | **Expo** + Expo Router + **NativeWind v5** + **React Native Reusables** (shadcn for RN) or **HeroUI Native**; `@expo/ui` for truly native SwiftUI/Compose controls; Reanimated 4 + Gesture Handler for motion | |
| React Native, StyleSheet-style perf focus | **Unistyles 3** + your own components | |
| React Native + web from one codebase | **Tamagui** (compiler, universal) or Expo + NativeWind with react-native-web | |
| Flutter | Material 3 (built-in) / Cupertino; **forui** or **shadcn_ui** for a non-Material look | |
| iOS native | **SwiftUI** system components (Liquid Glass on iOS 26+ comes free with standard controls) | Fight the platform as little as possible |
| Android native | **Jetpack Compose Material 3** (Expressive APIs in material3 1.5 line) | |

Details, alternatives and trade-offs per platform live in the references — read the one that matches:

- `references/web-react.md` — React primitives, styled kits, shadcn ecosystem & registries, Tailwind tooling
- `references/web-other.md` — Vue, Svelte, Solid, Angular, Astro, plain HTML/web components
- `references/mobile.md` — React Native/Expo, Flutter, SwiftUI, Compose, Kotlin Multiplatform
- `references/motion.md` — animation libraries per platform and when CSS/native is enough
- `references/building-blocks.md` — icons, fonts, charts, tables, forms, toasts, dates, DnD, virtualization, editors, command menus, carousels, maps, 3D
- `references/inspiration.md` — where to look for references (Mobbin, Refero, etc.) and AI design tooling

## Step 4 — Record the decision

Write the choice into the project (`DESIGN.md` or README "UI stack" section): library + version, styling approach, icon set, motion library, font, and *why*. Future sessions (and other agents) will read it instead of re-deciding.

## Freshness check (do this before installing)

```bash
npm view <pkg> version time.modified repository.url   # current version + last publish
npm view <pkg> deprecated                               # deprecation notice, if any
# Flutter: https://pub.dev/packages/<pkg> (likes, pub points, last publish)
# Swift: check the repo's latest release tag
```

Signals to avoid a library: no release in 12+ months with open critical issues, README says "unmaintained/archived", peer deps pinned to old React/RN, no TypeScript types, a11y issues ignored. Known retired/at-risk examples: `react-beautiful-dnd` (deprecated → use `@atlaskit/pragmatic-drag-and-drop` or dnd kit), `@base-ui-components/react` (renamed → `@base-ui/react`), Chakra v2 APIs (v3 is a rewrite on Ark UI/Panda), Reanimated 2/3 gesture APIs (`useAnimatedGestureHandler` removed in v4).

If docs MCPs are available (e.g. Context7, shadcn MCP, the Figma MCP for design-system lookups), use them to read current docs instead of relying on memory.

## Anti-patterns

- Two component libraries in one app (MUI + shadcn) → inconsistent focus, spacing, theming.
- Hand-rolling dialogs, menus, comboboxes, date pickers, toasts, tooltips → accessibility bugs (focus trap, escape, aria, scroll lock, collision). Use primitives.
- Installing an "animated components" library wholesale → copy only the 1–3 pieces you need.
- Using a web UI kit inside React Native via webviews, or forcing Material components on iOS users.
- Leaving the library's default theme untouched → the "every shadcn app looks the same" problem. Change at minimum: font, radius, accent color, neutral temperature, and density (see design-system-builder and color-theory skills).
