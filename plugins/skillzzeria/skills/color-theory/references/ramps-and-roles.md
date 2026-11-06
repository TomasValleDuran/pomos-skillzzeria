# Ramps and Roles

A ramp is not a gradient to pick from by eye. Every step exists because a role consumes it.

## Tailwind-style 50–950 → roles

| Step | Light theme role | Dark theme role |
|---|---|---|
| 50 | page background (neutral), subtle tint bg | primary text (neutral) |
| 100 | subtle surface, hover bg, accent-subtle (badges, selected rows) | — |
| 200 | borders, dividers, accent-subtle hover | — |
| 300 | strong borders, disabled fill | accent-text, status-text |
| 400 | placeholder icons (decorative), dark: accent fill | accent/status fills, focus ring, muted text (neutral) |
| 500 | focus ring, control borders (neutral) | accent fill, control borders |
| 600 | **primary fill** (accent), muted text (neutral) | — |
| 700 | fill hover/pressed, accent-text on light bg | strong borders (neutral) |
| 800 | — | borders, hover surfaces |
| 900 | headings in some systems | surfaces/cards, bg-subtle |
| 950 | primary text (neutral) | page background (neutral), accent-subtle (tinted bg) |

The exact step that works depends on the hue — that's why `palette.py system` searches and reports instead of hard-coding.

## Radix-style 1–12 (each step has a named job)

| Step | Use |
|---|---|
| 1 | App background |
| 2 | Subtle background (cards, sidebars, striped rows) |
| 3 | UI element background (normal) |
| 4 | UI element background (hover) |
| 5 | UI element background (active/selected) |
| 6 | Subtle borders, separators (non-interactive) |
| 7 | UI element border, focus ring |
| 8 | Hovered UI element border, strong borders |
| 9 | Solid backgrounds (the purest brand color — buttons, badges) |
| 10 | Hovered solid backgrounds |
| 11 | Low-contrast text (muted, accent text) |
| 12 | High-contrast text |

Radix designs separate light and dark scales (not reversed) — a good model: dark ramps should be generated, not the light ramp flipped.

## Semantic token set (minimum viable)

```
bg, bg-subtle, surface, surface-raised, overlay
border, border-strong, border-control
text, text-muted, text-subtle(placeholder), text-inverse
accent, accent-hover, accent-active, accent-fg, accent-subtle, accent-text
focus-ring
success|warning|danger|info  ×  {solid, solid-fg, subtle, text, border}
```

Names describe the **job**, never the hue (`--color-danger`, not `--color-red`) and never a single component (`--color-sidebar-bg` only if the sidebar truly needs a distinct role).

## Interaction states

| State | Recipe |
|---|---|
| Hover (solid) | one step further from the background (light: darker, dark: lighter) |
| Active/pressed | two steps, or hover + scale/translate feedback |
| Hover (ghost/neutral) | neutral-100 (light) / neutral-800–900 (dark) background |
| Selected | accent-subtle background + accent-text or a 2px accent indicator |
| Disabled | reduce contrast (neutral-300 fill / neutral-400 text) **and** remove pointer affordance; don't rely only on opacity over colored backgrounds |
| Focus | 2px+ ring in focus-ring color with ≥3:1 against adjacent colors, offset 2px from the component |
| Error | danger-text message + danger border on the control + icon; never color only |

## Ramp construction rules (what the script does)

1. Target lightness per step (finer at the light end).
2. Chroma = seed's relative vividness × gamut max at (L, H) × a shape that tapers at the dark end; absolute caps on tint steps so subtle backgrounds never go neon.
3. Constant hue (optional controlled drift for yellows/oranges whose shades go olive/brown).
4. Snap the step nearest the input to the exact input, so the brand color is literally in the ramp.

Hand-tuning after generation is fine — but re-measure.
