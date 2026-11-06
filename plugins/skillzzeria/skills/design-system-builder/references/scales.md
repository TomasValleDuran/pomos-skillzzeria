# Scales

## Typography

### Choosing type
- **≤2 families** + mono. A single great sans with weight/size contrast is enough for most product UIs. Pair a display face with a neutral text face for marketing.
- Product UI wants: large x-height, open apertures, tabular figures, good hinting at 12–14px (Inter, Geist, IBM Plex Sans, SF Pro, Roboto).
- Personality lives in headings: a serif or characterful grotesk for display, neutral sans for body.
- Variable fonts: one file, all weights; use optical sizing (`font-optical-sizing: auto`) where supported.
- Load ≤2–3 font files on critical path; `font-display: swap`; size-adjust fallback metrics to avoid layout shift (`next/font` does this).

### Scale
Modular ratios: 1.125 (dense apps), 1.2 (product UI), 1.25 (balanced), 1.333 (marketing), 1.5+ (editorial/landing). Round to whole pixels; snap to the 4px grid for line-heights.

Named roles (example product scale, 16px base):

| Role | Size / line-height | Weight | Tracking |
|---|---|---|---|
| display | 48–60 / 1.05–1.1 | 600–700 | −0.03em |
| h1 | 36 / 1.15 | 600 | −0.02em |
| h2 | 28–30 / 1.2 | 600 | −0.015em |
| h3 | 22–24 / 1.3 | 600 | −0.01em |
| title / h4 | 18–20 / 1.4 | 600 | 0 |
| body | 16 / 1.5 (14/1.45 for dense apps) | 400 | 0 |
| body-sm | 14 / 1.45 | 400 | 0 |
| label | 14 / 1.2 | 500 | 0 |
| caption | 12 / 1.35 | 400–500 | +0.01em |
| overline | 11–12 / 1.2, uppercase | 600 | +0.06em |
| code | 13–14 / 1.5 mono | 400 | 0 |

Rules: line length 45–75 characters (`max-width: 65ch`); hierarchy through weight and color before size; at most ~4 sizes visible on one screen; `text-wrap: balance` for headings, `pretty` for paragraphs; tabular numbers for data.

### Fluid type (web marketing)
`font-size: clamp(min, preferred-vw-expression, max)` — generate with Utopia. Don't use fluid type for dense product UI; use stepped sizes.

### Mobile
iOS: use Dynamic Type text styles (largeTitle 34, title1 28, title2 22, title3 20, headline 17 semibold, body 17, callout 16, subheadline 15, footnote 13, caption1 12, caption2 11) and let them scale. Android M3 type scale: display L/M/S (57/45/36), headline (32/28/24), title (22/16/14), body (16/14/12), label (14/12/11). React Native: respect `allowFontScaling`, test at the largest accessibility size, cap with `maxFontSizeMultiplier` only where layout truly breaks.

## Spacing

- 4px base; most used steps 4, 8, 12, 16, 24, 32, 48, 64.
- **Proximity = relationship**: space within a group < space between groups (e.g. label→input 6–8, field→field 16–24, section→section 48–64).
- Component padding ≈ 1:2 or 1:3 vertical:horizontal for buttons (e.g. 8×16, 10×20).
- Separate tokens for **inset** (padding), **stack** (vertical gaps), **inline** (horizontal gaps) only if the system is large; otherwise one numeric scale.
- Prefer `gap` over margins for layout.

## Radius

- Pick a personality and stick to it: sharp (0–4), soft (6–10), rounded (12–16), pill/round (20+/full).
- **Nested radius**: inner = outer − padding (a 16px card with 8px padding holds 8px-radius children). Mismatched nesting is one of the most visible "unpolished" tells.
- Small elements (badges, checkboxes) get smaller radii than containers; pill for chips/tags/toggles if the personality allows.
- iOS uses continuous ("squircle") corners — SwiftUI `.rect(cornerRadius:, style: .continuous)`; on web `corner-shape: squircle` is emerging (progressive enhancement).

## Elevation

Light mode shadow scale (layered shadows look more natural than one big blur):

```css
--shadow-xs: 0 1px 2px oklch(0% 0 0 / .05);
--shadow-sm: 0 1px 2px oklch(0% 0 0 / .06), 0 1px 3px oklch(0% 0 0 / .1);
--shadow-md: 0 2px 4px -1px oklch(0% 0 0 / .06), 0 4px 8px -2px oklch(0% 0 0 / .1);
--shadow-lg: 0 4px 6px -2px oklch(0% 0 0 / .05), 0 12px 24px -4px oklch(0% 0 0 / .12);
--shadow-xl: 0 8px 12px -4px oklch(0% 0 0 / .06), 0 24px 48px -8px oklch(0% 0 0 / .18);
```
Tint shadows with the neutral hue for warmth. Elevation meaning: 0 = flat content, 1 = cards, 2 = dropdowns/popovers, 3 = modals, 4 = toasts/drag. Dark mode: lighter surfaces + 1px subtle border, shadows only for overlays.

Borders vs shadows: a semi-transparent shadow ring (`0 0 0 1px oklch(0% 0 0 / .08)`) often looks crisper than a solid border on cards.

## Motion tokens

| Token | Value | Use |
|---|---|---|
| duration-instant | 100ms | press feedback, toggles |
| duration-fast | 150ms | hovers, small popovers, tooltips |
| duration-base | 200–250ms | dropdowns, accordions |
| duration-slow | 300–400ms | modals, drawers, page transitions |
| duration-deliberate | 500ms+ | marketing/onboarding only |
| ease-out | cubic-bezier(0.23, 1, 0.32, 1) | entering, responding to user |
| ease-in-out | cubic-bezier(0.77, 0, 0.175, 1) | moving on-screen |
| ease-drawer | cubic-bezier(0.32, 0.72, 0, 1) | sheets/drawers (iOS-like) |
| spring-default | stiffness ~300–400, damping ~30 (or SwiftUI `.smooth`/`.snappy`) | gestures, mobile |

Exits faster than entrances (~75%). Reduced motion: swap transforms for opacity, keep durations short.

## Density

Comfortable vs compact: scale control heights (40→32), paddings (one step down), and body size (16→14). Implement as a semantic-token mode, not per-component props.

## Breakpoints & layout

Mobile-first. Web: 640 / 768 / 1024 / 1280 / 1536. Prefer **container queries** for component responsiveness and breakpoints for page layout. Content max width ~1200–1440 for apps, 65–75ch for reading. Grid: 4 columns (mobile), 8 (tablet), 12 (desktop); gutters 16/24/32.

Mobile: design for 360–430pt widths, test 320 (small Android/SE) and large text. Tablets/foldables: adaptive layouts (list-detail), not stretched phone UIs. Safe areas: tokens or `env(safe-area-inset-*)`.
