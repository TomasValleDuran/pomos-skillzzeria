# Harmony, Brand Translation and Perception

## Harmony schemes (rotate hue in OKLCH, keep L and relative chroma)

| Scheme | Hue offsets | Character | UI use |
|---|---|---|---|
| Monochromatic | 0 (vary L/C only) | calm, cohesive, safest | product UIs: one accent ramp + neutrals |
| Analogous | ±30° | harmonious, low tension | gradients, illustrations, secondary accents |
| Complementary | 180° | maximum tension, vibrant | a single highlight against the brand (sale badge, CTA on brand-colored hero) — sparingly |
| Split-complementary | 150°, 210° | contrast with less clash | marketing pages with two supporting colors |
| Triadic | 120°, 240° | playful, balanced | kids/consumer apps, data categories |
| Tetradic | 90° steps | rich, hard to balance | illustration systems; rarely in UI chrome |

A harmony is a source of hues, not a mandate to use them equally. Dominant + supporting + accent proportions matter more than the scheme.

Hue rotation in HSL produces mismatched lightness (yellow is much brighter than blue at the same HSL L). `palette.py harmony` rotates in OKLCH so results sit at the same perceived lightness.

## Translating a brand palette to UI

Brand palettes are made for logos and marketing, not for interfaces. Common issues and fixes:

- **Brand color fails contrast as a button** → use a darker step of its ramp for fills/text; keep the exact brand color for large surfaces, illustrations, the logo.
- **Too many brand colors** → pick one as the interactive accent; others become illustration/marketing colors or chart colors. Interactive meaning must stay unambiguous.
- **Brand is red/green/yellow** → status colors must be shifted or differentiated (the tool nudges status hues ≥25° away; also differentiate by icon and copy).
- **Brand is very light (pastel)** → it becomes the subtle/tint color; derive a saturated mid-step for interactive elements.
- **Brand is near-black** → accent comes from a second color or from inverting (black buttons on light UI are fine and elegant; ensure focus rings remain visible).

## Temperature

Warm hues (red→yellow, ~0–110° in OKLCH) advance and energize; cool hues (cyan→violet, ~180–300°) recede and calm. Keep **neutral temperature consistent** with the accent: warm accent → stone/sand neutrals (slight positive hue tint ~60–90°); cool accent → slate/zinc neutrals (~250–270°). Mixing a warm accent with blue-gray neutrals is a frequent "something feels off" cause.

## Perception effects to design around

- **Simultaneous contrast**: the same gray looks lighter on dark backgrounds and darker on light ones; colors shift toward the complement of their surroundings. Check colors in context, never in isolation swatches.
- **Helmholtz–Kohlrausch**: saturated colors look brighter than their luminance suggests — saturated text can feel louder than its contrast ratio says. Use chroma for emphasis sparingly.
- **Bezold/assimilation**: thin lines/text take on the color of their surroundings; small colored text needs more chroma than you'd think, large areas need less.
- **Area effect**: a color looks more saturated over a large area. Pick big-surface colors (hero backgrounds) at lower chroma than the swatch suggests.
- **Vibrating edges**: two saturated complementary colors at similar lightness shimmer at the boundary (red text on blue). Separate them in lightness.

## Gradient craft

- Interpolate `in oklab` by default; `in oklch` for hue sweeps (shorter/longer hue interpolation keywords control the path).
- Add a mid stop to avoid dead gray middles when interpolating between complementary colors.
- Subtle beats loud: 10–20° hue shift with slight L change reads premium; rainbow gradients read template/AI.
- Add a touch of noise/grain (2–4% opacity) on large gradients to prevent banding.

## Palette inspiration sources (for exploration)

Coolors, Huemint (ML palette generation), Realtime Colors (preview a palette on a real page), Radix Colors (accessible scales), Tailwind palette, Material Theme Builder (M3 schemes from a seed), Leonardo by Adobe (contrast-targeted ramps), oklch.com (picker). Use them for ideas; generate the final system with the script so it's consistent and measured.
