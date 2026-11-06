# Mobile Standards — iOS HIG and Material 3

Verify specifics against the current Apple HIG and m3.material.io when it matters; both evolve yearly (Liquid Glass since iOS 26, Material 3 Expressive since 2025).

## Side by side

| Topic | iOS (HIG) | Android (Material 3) |
|---|---|---|
| Min touch target | 44×44 pt | 48×48 dp |
| Top-level navigation | Tab bar (bottom, ≤5; on iOS 26 a floating Liquid Glass bar that can minimize on scroll) | Navigation bar (compact), rail (medium), drawer (expanded) |
| Hierarchical navigation | Navigation stack, large titles collapsing, edge-swipe back | Top app bar + system/predictive back gesture |
| Back | Top-left back button with previous title; swipe from left edge | System back (gesture/button) — never rely on an in-app back alone |
| Primary action | Toolbar/navigation bar button; prominent button in content | FAB (or extended FAB / FAB menu in Expressive) |
| Modal tasks | Sheets with detents (medium/large), full-screen covers | Bottom sheets, full-screen dialogs |
| Alerts | Alert (2 buttons ideal), action sheet / confirmation dialog | Dialog; snackbar for lightweight feedback with action |
| Menus | Pull-down menus, context menus (long press, with preview) | Dropdown/exposed menus |
| Lists | Inset grouped lists, swipe actions | Lists with leading/trailing elements, swipe optional |
| Switch | Toggle | Switch |
| Typeface | SF Pro (system) with Dynamic Type styles | Roboto / Roboto Flex / Google Sans Flex, M3 type scale |
| Icons | SF Symbols (weights match text, symbol effects) | Material Symbols (variable: fill, weight, grade, optical size) |
| Color | Semantic system colors + app tint; vibrancy and materials | Dynamic color (Material You) + tonal palettes, surface containers |
| Materials/depth | Liquid Glass for controls/navigation floating over content; materials (blur) | Tonal elevation; M3 Expressive shapes & spring motion |
| Haptics | UIFeedbackGenerator / `sensoryFeedback`: selection, impact, notification | `performHapticFeedback` constants (CONFIRM, REJECT, etc.) |
| Text scaling | Dynamic Type (up to AX5 ≈ 3×) | Font scale up to 200% (non-linear scaling since Android 14) |
| Safe areas | Notch/Dynamic Island, home indicator | Edge-to-edge required on recent targets; handle `WindowInsets` (status, nav, IME, display cutout) |

## Rules that apply to both

- **Thumb zone**: primary actions in the bottom half; destructive actions away from frequent ones; avoid top-corner primary actions on large phones.
- **Gestures need visible alternatives** (swipe-to-delete also available in an edit mode or menu).
- **Don't override system gestures** (iOS edge swipe, Android back, home indicator area).
- **Keyboard**: correct keyboard type, return key label ("Next", "Go", "Search"), scroll focused field into view, dismiss on scroll/tap outside, autofill (`textContentType` / `autofillHints`).
- **Permissions**: ask in context with a pre-explanation; degrade gracefully when denied; link to settings.
- **Loading**: skeletons and progressive content; pull-to-refresh where content updates; offline-first states.
- **Feedback**: pressed states on every tappable element (highlight/scale ~0.97), haptics for confirmations and selections — not for every tap.
- **Text**: body ≥ 16–17 pt; test with the largest text size; never truncate critical info without a way to see it all.
- **Dark mode**: support it, test both; respect Reduce Motion, Reduce Transparency, Increase Contrast, Bold Text (iOS) and remove-animations / high-contrast text (Android).
- **Adaptive layouts**: tablets and foldables get list-detail / multi-pane layouts, not stretched phone UIs; support rotation where it adds value.
- **Performance**: 60/120 fps; no jank on scroll; images sized and cached; lists virtualized (FlashList, LazyColumn, List).

## Cross-platform apps (React Native, Flutter, KMP)

- Adapt per platform where users notice: navigation/back behavior, sheets, switches, date/time pickers, alerts, menus, typography, haptics. Shared: brand color, iconography style, content, illustrations.
- Prefer native controls when available (`@expo/ui`, platform-adaptive Flutter widgets, Zeego menus).
- Test on real devices: small (iPhone SE / 360dp Android), large, a mid-range Android for performance.

## Store-quality polish (common review/rating issues)

App icon and launch screen consistent with brand; no placeholder content; empty states designed; offline handling; account deletion available in-app if accounts exist (Apple requirement); privacy prompts honest; no broken layouts with large text; dark mode not broken; landscape either supported or locked deliberately.
