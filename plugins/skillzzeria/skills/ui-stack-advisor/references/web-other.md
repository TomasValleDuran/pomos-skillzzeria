# Vue, Svelte, Solid, Angular, Astro, plain HTML (snapshot Nov 2026)

## Vue / Nuxt

| Library | Notes |
|---|---|
| **Nuxt UI v4** | 125+ components, built on Reka UI + Tailwind v4 + Tailwind Variants. Nuxt UI and Nuxt UI Pro were unified and made fully free/open source. Works in plain Vue via a Vite plugin. Default pick. |
| **Reka UI** (formerly Radix Vue) | Headless primitives; foundation of Nuxt UI and shadcn-vue |
| **shadcn-vue** | shadcn port, copy-in |
| **PrimeVue** | Huge set, styled or unstyled ("pass-through") mode; good for enterprise |
| **Vuetify** | Material Design; mature |
| **Ark UI (Vue)** | Cross-framework primitives |
| **Naive UI**, **Element Plus** | Popular admin kits |

Motion: `@vueuse/motion`, Motion for Vue (`motion-v`), GSAP; `<Transition>`/`<TransitionGroup>` built-ins cover most UI needs.

## Svelte / SvelteKit (Svelte 5 runes)

| Library | Notes |
|---|---|
| **shadcn-svelte** | Community port, copy-in, built on Bits UI + Tailwind. Default pick. |
| **Bits UI** | Headless primitives for Svelte 5 |
| **Melt UI** | Builder-pattern headless primitives |
| **Skeleton** | Styled design system + Tailwind |
| **Flowbite Svelte** | Styled Tailwind components |
| **Ark UI (Svelte)** | Cross-framework primitives |

Motion: Svelte's built-in `transition:`, `animate:`, `svelte/motion` (springs/tweens) are excellent — reach for GSAP/Motion only for timelines/scroll.

## Solid

Kobalte (headless), Ark UI (Solid), solid-ui (shadcn port), Corvu (headless extras: drawer, resizable). Motion: `solid-motionone` / Motion's vanilla API.

## Angular

| Library | Notes |
|---|---|
| **Spartan UI** | shadcn-like: brain (headless) + helm (styled, copy-in) |
| **Angular Material / CDK** | Official; CDK is excellent for overlays, a11y, DnD, virtual scroll |
| **PrimeNG** | Huge, enterprise |
| **ng-zorro** | Ant Design for Angular |
| **Taiga UI** | Large, well-engineered kit |

## Astro / content sites

Astro islands with any of the above (React/Vue/Svelte). For mostly-static sites, prefer plain HTML + CSS + small islands. Starlight for docs.

## Plain HTML / framework-agnostic

- **Web components**: Shoelace → **Web Awesome** (successor), Lit-based design systems, Adobe Spectrum Web Components, Microsoft Fluent UI web components.
- **Native HTML is better than ever**: `<dialog>`, Popover API (`popover` attribute), `<details name>` exclusive accordions, CSS anchor positioning, `field-sizing: content`, customizable `<select>` (`appearance: base-select`, Chromium-first — progressive enhancement), `:has()`, container queries, `@starting-style`, View Transitions. Check support on caniuse/MDN; use them before adding JS libs for simple cases.
- **Pico CSS**, **Open Props** (design-token CSS variables), **daisyUI** (Tailwind plugin with themed component classes) for quick, framework-free styling.
