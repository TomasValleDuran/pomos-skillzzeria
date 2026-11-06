# Dark Mode

## Principles

1. **Design it, don't invert it.** Same roles, different steps, re-measured.
2. **Background**: very dark, slightly tinted neutral (OKLCH L ≈ 0.13–0.18). Pure `#000` is acceptable for OLED-first media apps but causes smearing on scroll and harsh contrast for text-heavy UIs.
3. **Elevation = lighter.** Shadows are nearly invisible on dark; communicate depth with surface lightness: bg (L .15) → surface (L .19–.21) → raised/popover (L .23–.26). Add a subtle 1px border (white at 6–10% or neutral-800) to separate surfaces.
4. **Text**: primary ≈ neutral-50/100 (not pure white for long reading), muted ≈ neutral-400. Aim for 7:1+ on primary text; dark mode tolerates slightly lower contrast perceptually but WCAG still applies.
5. **Accents**: shift to a lighter step (400–500) and/or lower chroma by 10–20%. Fully saturated mid-lightness colors "vibrate" against dark backgrounds.
6. **Fills flip their label**: a light-ish dark-mode accent fill usually needs dark text (950 step). The tool picks by measured contrast.
7. **Images & illustrations**: reduce brightness slightly (`filter: brightness(.9)`) or provide dark variants; transparent PNG logos may need a dark-mode version.
8. **Shadows**: if used, make them darker and larger with lower opacity; pair with a light top border highlight for "lifted" glass/material feel.

## Switching mechanism (web)

Pick **one**:
- **Class/attribute strategy** (`.dark` / `[data-theme=dark]` on `<html>`): user-togglable, persist choice, set before paint to avoid flash (inline script in `<head>` or `next-themes`).
- **Media query** (`prefers-color-scheme`): zero JS, follows OS; can't be overridden by the user unless combined with a class.

Always also set `color-scheme: light dark` (or the active one) so native form controls and scrollbars match, and `<meta name="theme-color">` per scheme.

Tailwind v4: `@custom-variant dark (&:where(.dark, .dark *));` for class strategy.

## Native platforms

- **iOS/SwiftUI**: use semantic system colors (`.primary`, `.secondary`, `Color(.systemBackground)`, `.secondarySystemBackground`, `.label`, `.secondaryLabel`) — they adapt to dark mode, increased contrast and (on iOS 26) Liquid Glass materials automatically. Define brand colors in an Asset Catalog with Any/Dark (and High Contrast) appearances.
- **Android/Compose (Material 3)**: generate light and dark `ColorScheme`s (Material Theme Builder or `dynamicLightColorScheme`/`dynamicDarkColorScheme` on Android 12+). M3 uses tonal surface containers (`surfaceContainerLowest…Highest`) for elevation instead of shadows/overlays.
- **Flutter**: `ColorScheme.fromSeed(seedColor:, brightness:)` gives M3-correct light/dark schemes; for custom brand tokens use a `ThemeExtension`.
- **React Native**: `useColorScheme()`; with NativeWind use `dark:` variants; with Unistyles define `light`/`dark` themes and enable adaptive themes. Respect the OS setting by default.

## Testing

- Toggle both themes on every screen; look at empty states, charts, toasts, disabled states and modals specifically (they are most often forgotten).
- Run `palette.py system` report or `contrast` on every custom pair.
- Check "Increase Contrast" (iOS) / high-contrast text (Android) / `prefers-contrast: more` (web) if the product targets accessibility-sensitive audiences.
