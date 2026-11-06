# Contrast and Color-Vision Deficiency

## WCAG 2.2 success criteria involving color

| SC | Level | Requirement |
|---|---|---|
| 1.4.1 Use of Color | A | Color is not the only visual means of conveying information, indicating an action, prompting a response, or distinguishing an element. Links inside body text need a non-color cue (underline) unless they have 3:1 against surrounding text **and** a non-color cue on hover/focus. |
| 1.4.3 Contrast (Minimum) | AA | Text 4.5:1; large text (≥24px regular or ≥18.66px bold) 3:1. |
| 1.4.6 Contrast (Enhanced) | AAA | 7:1 / 4.5:1. |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI component boundaries/states needed to identify them (input borders, checkbox outlines, toggle states) and meaningful graphics (icons without text, chart elements). |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator is visible. |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element not entirely hidden by sticky headers/overlays. |
| 2.4.13 Focus Appearance | AAA | Focus indicator area ≥ 2px perimeter and 3:1 change of contrast. |

Exempt: disabled components, pure decoration, logos/brand names, incidental text in photos.

## Practical rules

- **Measure the rendered pair.** Text on a card measures against the card, not the page. Text over alpha/gradient/image: measure the worst spot.
- **Placeholder text** isn't required to meet 4.5:1 by many readings, but if it's the only hint it should; prefer visible labels anyway.
- **Focus ring**: 2px solid ring, 2px offset, focus-ring color ≥3:1 against both the component and the background. A two-tone ring (inner light/outer dark) works on any background.
- **Fixing a failing pair**: change **lightness**, not hue. Moving one step along the ramp is usually enough.
- **Thin and small text** needs more contrast than the ratio implies — APCA accounts for font weight and size; WCAG doesn't.

## APCA quick levels (advisory; WCAG 3 not final)

| |Lc| | Use |
|---|---|
| 90 | Preferred for body text (≥14–16px regular) |
| 75 | Minimum for body text columns |
| 60 | Minimum for other content text: large/medium (≥24px or ≥16px bold), UI labels |
| 45 | Large headlines (≥36px), meaningful icons and non-text elements |
| 30 | Absolute minimum for any text: placeholders, disabled, copyright fine print |
| 15 | Invisible threshold for non-text: dividers below this are invisible to many |

APCA is polarity-aware: light text on dark (negative Lc) needs a slightly larger |Lc| for the same perceived legibility at small sizes.

## Color-vision deficiency (CVD)

| Type | Prevalence (approx.) | Confuses |
|---|---|---|
| Deuteranomaly/-opia (green-weak) | ~6% of men | red–green, brown–green, blue–purple |
| Protanomaly/-opia (red-weak) | ~2% of men | red–green, red looks darker/black |
| Tritanomaly/-opia (blue-weak) | <0.01% | blue–green, yellow–pink |
| Achromatopsia | very rare | everything except lightness |

Design rules:
- Red/green pairs (success/error, gain/loss) must differ in **lightness** and carry an icon/sign (+/−, ✓/✕, ▲/▼).
- Charts: differentiate series by lightness and position, add direct labels instead of legends, use patterns/dashes for lines. Run `palette.py cvd` on the series.
- Status badges: always text + icon, color third.
- Test with OS simulators: macOS Accessibility → Display → Color Filters; Chrome DevTools → Rendering → Emulate vision deficiencies; Xcode Accessibility Inspector; Android Developer options → Simulate color space.

## Non-color cues checklist

- Links in paragraphs: underline (or 3:1 + underline on hover/focus)
- Form errors: icon + message + border, not just a red border
- Required fields: asterisk + "required" in label/aria
- Selected tabs/nav: weight, indicator bar, or background — not only text color
- Charts: labels, shapes, patterns
- Online/offline dots: tooltip or text label
