---
name: ui-ux-playbook
description: The entry point for any UI/UX work on web or mobile — the end-to-end workflow (brief → direction → system → stack → build → motion → verify), industry standards and best practices (WCAG 2.2, Apple HIG, Material 3, Nielsen heuristics, Laws of UX, Core Web Vitals, forms, navigation, states, i18n), a pre-ship UI checklist, and a routing map telling you which specialized design/animation/color/library skill to load for each sub-task. Use this whenever you start or plan a frontend or mobile app, build or redesign screens, review UI/UX quality, answer "what's the best practice for X" in interface design, or when several design skills could apply and you need to decide which.
---

# UI/UX Playbook

Great interfaces come from three things done together: **a clear point of view** (who, what job, what feel), **a consistent system** (tokens + components), and **hundreds of correct details** (states, motion, accessibility, copy). This playbook orchestrates the arsenal of skills that cover each part.

## Workflow for any UI task

Scale it: a button tweak needs steps 5–7; a new app needs all of them.

1. **Brief** — Who is the person, what's the job (verb), what context/device, what should it feel like (concrete words). Infer from the codebase and request; ask one question only if a critical constraint is unknowable (platform, existing brand, audience).
2. **Direction** — choose the aesthetic and interaction character *before* code. Look at 2–4 real references for this screen type (`ui-stack-advisor/references/inspiration.md`).
3. **System** — tokens and DESIGN.md (`design-system-builder`; colors via `color-theory`). Existing project? Read and follow its system; extend it, don't fork it.
4. **Stack** — component/motion libraries (`ui-stack-advisor`). Use accessible primitives; don't hand-roll dialogs, menus, comboboxes, date pickers, toasts.
5. **Build** — structure and hierarchy first (layout, type, spacing), then color, then detail. Real content, not lorem ipsum. All states: loading, empty, error, partial, success, disabled, long content.
6. **Motion** — only where it has a purpose (feedback, continuity, state change); see motion skills.
7. **Verify by looking** — render it (dev server + Playwright/Chrome MCP/simulator), check at real sizes (390, 768, 1280+; small phone, tablet), both themes, keyboard-only, 200% zoom / largest Dynamic Type. Fix what you see in batches.
8. **Review** — run the pre-ship checklist below or a review skill.

## Which skill for what (routing)

| Need | Load |
|---|---|
| Aesthetic direction for landing pages, marketing, distinctive visual design | `frontend-design` |
| Product UI (dashboards, SaaS, admin, tools) with persistent design memory | `interface-design` |
| Design system, tokens, theming, multi-platform tokens, DESIGN.md | `design-system-builder` |
| Picking/deriving colors, palettes, dark-mode colors, contrast, color-blind safety | `color-theory` (generates) · `better-colors` (audits) |
| Typography: scale, wrapping, font features, truncation | `better-typography` |
| Layout: grouping, alignment, responsive, i18n room | `better-layout` |
| Polish: radius, shadows, icons, optical alignment | `better-ui` |
| Accessibility review/fix (WCAG 2.2) | `better-accessibility` |
| UX copy, labels, errors, empty states | `better-writing` |
| Whole-screen ranked review across all of the above | `better-interface` · branch/PR review: `interface-review` |
| Choosing component/animation/widget libraries | `ui-stack-advisor` |
| Animation philosophy, easing, durations, springs, component feel | `emil-design-eng` |
| Build a web animation | `animate` · several elements together: `choreograph` |
| Review / audit / fix janky animations | `review-animations` · `improve-animations` · `animation-performance` |
| Apple-style fluid motion, gestures, materials (web or native) | `apple-design` |
| Mobile web feeling native (PWA, touch, 100vh, safe areas) | `mobile-native` |
| React Native / Expo design & review | `mobile-design` · animation: `animate-expo` · Expo plugin skills: `expo-native-ui`, `expo-ui`, `expo-design-system`, `expo-animation`, `expo-router` |
| shadcn/ui specifics | `shadcn` (Vercel plugin) |
| Component variants / state gallery / stress test | `variant` · `state-machine` · `break` (user-invoked) |
| Charts and dashboards data viz | `dataviz` |
| Figma ↔ code | Figma MCP skills (`figma-design-to-code`, `figma-generate-library`, …) |

Conflict rule: when two skills disagree, **the project's existing DESIGN.md/system wins**, then the user's brief, then the more specific skill (e.g. `animate-expo` over `emil-design-eng` in an Expo app). Don't stack multiple aesthetic-direction skills on one task — pick one (`frontend-design` *or* `interface-design`).

## Standards cheat sheet

**Accessibility (WCAG 2.2 AA — legal baseline in the US (ADA/508), EU (European Accessibility Act, in force since June 2025), and many others)**
- Contrast 4.5:1 text, 3:1 large text & UI components/meaningful graphics
- Everything operable by keyboard; visible focus (2.4.7) not hidden by sticky UI (2.4.11); logical order
- Target size ≥ 24×24 CSS px (2.5.8) — design for 44×44
- Dragging has a single-pointer alternative (2.5.7)
- Labels for every input, errors identified in text, no info by color alone
- Text resizes to 200% / reflows at 320px width without horizontal scroll (1.4.10)
- Respect reduced motion; no flashing > 3/s; auto-moving content > 5s can be paused
- Consistent help location (3.2.6), no redundant re-entry (3.3.7), accessible authentication — no cognitive tests, allow paste/password managers (3.3.8)
- Semantic HTML first; ARIA only to fill gaps. Native: accessibility labels/traits (iOS), contentDescription/semantics (Android/Compose), `accessibilityLabel`/`accessibilityRole` (RN)

**Platforms**
- iOS (HIG): 44×44pt targets, tab bar for top-level nav (≤5), navigation stack with back swipe, sheets with detents, SF Symbols, Dynamic Type, semantic colors, Liquid Glass for the control layer (iOS 26+), haptics for meaningful events
- Android (Material 3 / Expressive): 48×48dp targets, navigation bar/rail/drawer by width class, predictive back, edge-to-edge with insets, dynamic color, M3 type scale
- Details and differences: `references/mobile-standards.md`

**Performance (Core Web Vitals, 75th percentile)**: LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1. Respond to input within ~100ms; show progress for anything > 400ms (Doherty threshold); skeletons for content, spinners for actions; optimistic UI where safe. Mobile: 60/120fps, keep JS thread free (Reanimated worklets), lists virtualized.

**UX principles**: Nielsen's 10 heuristics + Laws of UX (Fitts, Hick, Jakob, Miller/chunking, Tesler, Doherty, peak-end, aesthetic-usability, Von Restorff, Gestalt). Pattern guidance for forms, navigation, search, tables, onboarding, empty/error/loading states, notifications, settings, destructive actions: `references/ux-principles-and-patterns.md`.

**Ethics**: no dark patterns (confirmshaming, roach-motel cancellation, pre-checked consent, fake urgency, hidden costs, nagging). They're increasingly illegal (EU DSA/DMA, FTC click-to-cancel rules, GDPR consent rules) and they erode trust.

## Pre-ship UI checklist

- [ ] Purpose of each screen obvious in 5 seconds; one primary action per view
- [ ] Hierarchy readable when squinting (size/weight/contrast, not just color)
- [ ] Spacing, radius, type, color from tokens only; consistent with DESIGN.md
- [ ] Loading, empty, error, partial, offline, and long-content states designed
- [ ] Forms: labels, correct input types/autocomplete, inline errors, preserved input on error, no paste blocking
- [ ] Keyboard: tab order, visible focus, Escape closes overlays, focus returns to trigger
- [ ] Screen reader: names/roles/states, live regions for async updates, headings structure
- [ ] Contrast measured both themes; nothing conveyed by color alone
- [ ] Responsive at 320 / 390 / 768 / 1024 / 1440; touch targets ≥ 44; no hover-only affordances
- [ ] Motion purposeful, ≤ 300ms for UI, interruptible, reduced-motion respected
- [ ] Copy: specific verbs on buttons, errors explain fix, consistent terminology, i18n-ready (no concatenated strings, room for +30–40% text, RTL-safe logical properties)
- [ ] Performance: images sized/lazy, fonts preloaded/swapped, no layout shift, long lists virtualized
- [ ] Looked at the rendered result (screenshots at real sizes), not just the code

Web code audit with the full rule set (focus, forms, animation, typography, content, images, performance, navigation, touch, theming, i18n, hydration, copy, anti-patterns): read `references/web-interface-guidelines.md` and report as `file:line - issue`.

## References
- `references/web-interface-guidelines.md` — Vercel's Web Interface Guidelines (vendored, MIT) for code audits
- `references/ux-principles-and-patterns.md` — heuristics, Laws of UX, and pattern-level best practices
- `references/mobile-standards.md` — iOS HIG + Material 3 essentials and platform differences
- `references/arsenal.md` — every installed UI skill: source, license, what it's for, how to update; optional extras
