---
name: color-theory
description: Color theory and palette engineering for UI on any platform (web, iOS, Android, Flutter, React Native). Choose and derive brand palettes, build tonal ramps, tinted neutrals and status colors, map them to light/dark semantic tokens, and verify contrast (WCAG 2.2 + APCA) and color-blind safety with a bundled zero-dependency OKLCH tool. Use this whenever the user picks, generates, critiques or fixes colors — "what colors should I use", brand color, palette, color scheme, theme, dark mode colors, accent, gradient, "this looks dull/garish", contrast problems, color-blind friendliness, or turning one hex into a full system — even if they don't say "color theory".
---

# Color Theory for Interfaces

Color in UI is mostly a **lightness** problem wearing a hue costume. Hierarchy, contrast, legibility and dark mode are all decided by lightness; hue carries identity and meaning; chroma (saturation) carries emphasis. Work in that order.

## The toolkit — use it instead of guessing

`scripts/palette.py` (Python 3, no deps) computes everything in OKLCH and gamut-maps to sRGB. Never eyeball a contrast ratio or invent a ramp by hand when you can compute it.

```bash
S=<skill-dir>/scripts/palette.py   # <skill-dir> = the base directory shown when this skill loads
python3 $S system "#6d28d9"                    # full system: ramps + light/dark roles, all pairs verified
python3 $S system "#6d28d9" --format tailwind  # Tailwind v4 @theme + semantic vars (also: css, json = DTCG)
python3 $S ramp "#0f766e" --format css         # one 50–950 ramp (input snapped to its nearest step)
python3 $S neutral "#0f766e" --tint 0.01       # gray ramp tinted toward the brand hue
python3 $S contrast "#fff" "#7c3aed"           # WCAG ratio + levels + APCA Lc
python3 $S cvd "#16a34a" "#dc2626" "#2563eb"   # color-blind simulation + confusable pairs
python3 $S harmony "#6d28d9" --scheme split    # hue relationships in OKLCH
python3 $S convert "hsl(...)/#hex/oklch(...)"  # notation conversion + how vivid it is
```

`system` auto-walks steps along a ramp when a pair fails (e.g. moves `text-muted` darker until 4.5:1) and prints every adjustment — relay those to the user, they are design decisions.

## Workflow: from "I need colors" to shipped tokens

1. **Find the anchor.** Existing brand color? Use it. None? Derive from the product's personality (see *Choosing a hue* below) and propose 2–3 seeds with a one-line rationale each, rather than a single arbitrary pick.
2. **Generate the system** with `palette.py system <seed>`. One accent ramp, one neutral ramp, and only the status ramps the product renders.
3. **Map to semantic roles**, never use primitives in components (`--color-accent`, `--color-text-muted`, not `--violet-600`). The design-system-builder skill covers token architecture in depth.
4. **Verify**: contrast on the *rendered* pair (text on its actual surface, including alpha/overlays), both themes, CVD check for any color-coded meaning (charts, status, tags).
5. **Apply with restraint** (below), then look at it rendered.

## How much color: distribution

- **Neutrals do ~90% of the work.** Backgrounds, surfaces, text, borders. A UI built on good neutrals with one accent almost always looks more professional than a multi-hue one.
- **60-30-10** is a useful sanity check: ~60% dominant neutral, ~30% secondary surface/neutral variation, ~10% accent. If the accent exceeds ~10–15% of pixels, it stops meaning "act here".
- **One filled primary action per view.** Color on a button's background reads as primary from across the room; colored text reads as a link.
- **One color, one meaning.** If violet means "brand/interactive", don't also use it for a category tag. Status hues must sit clearly apart from the accent (the tool keeps ≥25° in OKLCH hue).
- **Color is never the only signal.** ~8% of men and ~0.5% of women have a color-vision deficiency; pair color with an icon, label, pattern or position.

## Choosing a hue (when there is no brand)

Associations are culture-dependent and weak compared to execution — a well-built palette in any hue beats a "psychologically correct" hue used badly. Use them as tie-breakers:

| Hue family | Common UI reading | Typical products | Watch out |
|---|---|---|---|
| Blue / indigo | trust, calm, competence | fintech, SaaS, health, enterprise | the most generic choice; push chroma or shift toward indigo/cyan to stand out |
| Violet | creative, premium, "AI" | creative tools, AI products | very saturated violet is now an "AI slop" tell |
| Green / teal | growth, money, health, success | finance, sustainability, wellness | conflicts with "success" status — nudge status hue |
| Red / rose | energy, urgency, passion | food, media, entertainment | conflicts with "danger"; use for brand moments, keep destructive actions distinct |
| Orange / amber | warmth, friendliness, action | consumer, food, marketplaces | dark oranges go brown; check light-mode fills |
| Yellow / lime | optimism, attention | consumer, playful | can't carry white text; use dark text on yellow fills, or use the brand as accent-subtle and pick a darker step for fills (`--hue-shift -15` keeps shades golden instead of olive) |
| Near-neutral (black/stone/sand) | luxury, editorial, tooling | dev tools, fashion, portfolios | needs typographic and spatial craft to not feel empty |

Regional notes worth knowing: red is lucky/celebratory in China but means loss in Western finance (and gain in Chinese/Japanese stock tickers); white is associated with mourning in parts of East Asia. For finance UIs, make up/down colors configurable.

## Perceptual color — why OKLCH

HSL lightness lies: `hsl(60 100% 50%)` (yellow) and `hsl(240 100% 50%)` (blue) share "L=50%" but differ enormously in perceived brightness. That's why HSL ramps have uneven contrast and dark/light steps that don't line up across hues.

OKLCH = **L** (perceived lightness 0–1) · **C** (chroma, ~0–0.37) · **H** (hue angle). Equal L ≈ equal perceived lightness across hues, so:
- the same step across ramps (all `-600`s) has similar contrast against white,
- you can rotate hue without changing lightness (harmonies, status colors that "match"),
- dark mode can be derived by reasoning about L.

Caveats: the sRGB gamut is irregular — each hue has a different max chroma at each L (yellow peaks near L≈0.95, blue near L≈0.45). The tool gamut-maps by reducing chroma, keeping L and H. Wide-gamut (Display-P3) colors are an enhancement: declare the sRGB value first, then the P3/`oklch()` vivid one in `@media (color-gamut: p3)`.

CSS supports `oklch()` in all modern browsers; use it in new web projects. On native platforms convert to the platform's notation (hex/sRGB, `Color(red:green:blue:)`, `Color(0xFF…)`) — the tool's `--notation hex` helps.

## Ramps, neutrals and tints

- **Ramps hold one hue end to end**, step finer at the light end (that's where backgrounds live and the eye is most sensitive), and peak in chroma mid-ramp. 11 steps (50–950, Tailwind convention) or 12 (Radix convention, each step has a named job) — see `references/ramps-and-roles.md` for the role map.
- **Tinted neutrals**: mix a little of the brand hue into grays (chroma ≈ 0.005–0.02). It makes the whole UI feel coherent; pure #808080 grays feel dead next to a saturated accent. Warm brand → warm grays; cool → cool.
- **Never pure black on pure white for long text** in branded UIs; near-black (neutral-950) on near-white reduces glare. Pure black backgrounds in dark mode cause smearing on OLED during scroll; use L ≈ 0.13–0.18.

## Dark mode is not inversion

- Elevation goes **lighter**, not shadow-darker: surface > background by ~0.03–0.06 L.
- **Desaturate accents** slightly and **raise their lightness**; saturated mid-tones vibrate on dark backgrounds.
- Body text slightly off-white (neutral-50/100), muted text around neutral-400.
- Fills often flip their label to dark text (the tool decides by contrast).
- Re-measure every pair; contrast does not survive reversal. See `references/dark-mode.md`.

## Contrast — the standards

| Pair | WCAG 2.2 AA | AAA | APCA guidance (advisory) |
|---|---|---|---|
| Body text (<24px / <18.66px bold) | 4.5:1 | 7:1 | Lc 75+ (90 preferred) |
| Large text (≥24px or ≥18.66px bold) | 3:1 | 4.5:1 | Lc 60+ |
| UI components & graphical objects needed to understand them (input borders, icons, focus rings, chart marks) | 3:1 (SC 1.4.11) | — | Lc 45+ |
| Disabled controls, decorative elements, logos | exempt | — | — |

WCAG 2.x is the legal/compliance baseline (ADA, EN 301 549 / European Accessibility Act). APCA (the WCAG 3 candidate) models perception better, especially for dark mode and light text, but WCAG 3 is not final — meet WCAG 2.2 AA and use APCA as a second opinion. Details, focus-ring rules and gotchas in `references/contrast-and-cvd.md`.

## Gradients, overlays, and alpha

- Interpolate gradients `in oklab` (smooth, no muddy middle); use `in oklch` for multi-hue sweeps that would go gray through the middle. Keep stops close in lightness for backgrounds behind text.
- Text over images: a scrim (gradient overlay) or a solid backing; measure the worst-case region.
- Alpha colors (`/50`, `rgba`) change contrast depending on what's underneath. Prefer solid tokens for text; reserve alpha for overlays, hovers and shadows.

## Data visualization

Categorical palettes need equal-ish lightness and max hue separation; sequential palettes vary lightness monotonically; diverging palettes share a neutral midpoint. Use the `dataviz` skill if available — it has a validated palette method. Always run `palette.py cvd` on chart series colors.

## Reviewing someone's colors — quick checklist

- [ ] Every text/background pair measured in both themes (not estimated)
- [ ] Input borders, focus rings, icons that convey meaning ≥ 3:1
- [ ] No raw hex/rgb in components; semantic tokens only
- [ ] One accent, used for interactive/primary meaning only
- [ ] Status colors distinct from accent and from each other under CVD simulation
- [ ] Neutrals tinted consistently (not a mix of cool and warm grays)
- [ ] Dark mode designed (lighter surfaces for elevation, adjusted accents), not inverted
- [ ] Meaning never carried by color alone

For a full color-system audit with severity-ranked findings, the `better-colors` skill is excellent; for picking/deriving/generating, stay here.

## References
- `references/ramps-and-roles.md` — step-by-step role mapping (Tailwind 50–950 and Radix 1–12), state colors (hover/active/disabled/selected)
- `references/dark-mode.md` — dark theme construction, elevation, platform specifics (iOS semantic colors, Material tonal surfaces)
- `references/contrast-and-cvd.md` — WCAG 2.2 details, APCA levels, focus indicators, CVD design rules
- `references/harmony-and-brand.md` — harmony schemes, deriving secondary colors, brand-to-UI translation, temperature, simultaneous contrast
