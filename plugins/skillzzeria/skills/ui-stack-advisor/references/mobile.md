# Mobile UI Stacks (snapshot Nov 2026)

First principle: **mobile users expect their platform's conventions** (navigation, gestures, controls, typography, haptics). Cross-platform frameworks should adapt per platform rather than impose one look. See the `mobile-design` and `apple-design` skills for design guidance; Expo's official skills (`expo-native-ui`, `expo-ui`, `expo-design-system`, `expo-animation`, `expo-router`) for implementation.

## React Native / Expo

Baseline (2026): Expo SDK (New Architecture only), Expo Router (file-based navigation built on React Navigation), Hermes, Reanimated 4 (+ `react-native-worklets`), Gesture Handler (v3 API), `expo-image`, `expo-haptics`, `expo-symbols` (SF Symbols), FlashList v2 for lists, `react-native-keyboard-controller` for keyboard handling, `react-native-safe-area-context`.

### Styling engines
| Engine | Model | Choose when |
|---|---|---|
| **NativeWind v5** | Tailwind v4 classes compiled for RN (RN 0.81+) | Team knows Tailwind; sharing tokens with a web app; using RN Reusables/gluestack |
| **Unistyles 3** | StyleSheet-compatible API, C++ core, themes + breakpoints, no re-renders on theme change | Performance-sensitive apps; teams that prefer StyleSheet |
| **Tamagui** | Compiler-optimized styled system + full component kit; web + native | Universal (web+native) apps wanting one design system; accept higher setup/lock-in |
| Plain `StyleSheet` + tokens module | Zero deps | Small apps; maximum control |

### Component kits
| Kit | Notes |
|---|---|
| **React Native Reusables** | shadcn/ui for RN: copy-in, NativeWind, accessible primitives (rn-primitives). Default pick for a shadcn-like workflow. |
| **HeroUI Native** | Built from scratch as part of HeroUI v3 (2026), ~37 components; newer — verify maturity |
| **gluestack-ui (v3+)** | Copy-in, NativeWind-based (big rewrite from v1/v2; beware stale tutorials) |
| **Tamagui UI** | Comes with Tamagui |
| **@expo/ui** | Real **SwiftUI** (iOS) and **Jetpack Compose** (Android) components from JS: sheets, pickers, sliders, toggles, menus, grouped forms. Use for the most native feel. |
| **React Native Paper** | Material Design 3 for RN; good for Android-first or Material brands |
| **Zeego** | Native menus/context menus |
| **@gorhom/bottom-sheet** | Mature JS bottom sheet (consider native sheets via Expo Router `presentation: 'formSheet'` or @expo/ui first) |

### Mobile building blocks
Lists: FlashList, LegendList. Images: expo-image. Icons: `expo-symbols` (SF Symbols on iOS), `@expo/vector-icons`, Lucide RN, Phosphor RN. Lottie: `lottie-react-native`. Rive: `rive-react-native`. Charts: Victory Native XL (Skia), `react-native-gifted-charts`. Skia: `@shopify/react-native-skia` for custom drawing/shaders. Toasts: `sonner-native`, Burnt (native toasts). Forms: React Hook Form / TanStack Form.

## Flutter

- **Material 3** is the default in Flutter (`useMaterial3: true`); `ColorScheme.fromSeed` for theming; dynamic color via `dynamic_color`.
- **Cupertino** widgets for iOS-styled UI; consider adaptive widgets (`Switch.adaptive`, platform checks) or packages that render Liquid Glass on iOS 26+ with Material fallback elsewhere (several exist; verify maintenance).
- Non-Material looks: **forui** (minimalistic, shadcn-inspired, actively released), **shadcn_ui** (`shad`, maintained by Serverpod), `shadcn_flutter` (84 components, New York style).
- Motion: built-in implicit animations (`AnimatedContainer`, `AnimatedSwitcher`), Hero, **flutter_animate** (chainable effects), `animations` package (Material motion patterns), Rive, Lottie.
- Theming: `ThemeData` + `ThemeExtension` for custom tokens; keep tokens in one `theme/` module.

## iOS — SwiftUI

- Use system components and semantic styles first: `NavigationStack`, `TabView`, `List`, `Form`, `.sheet` with detents, `.toolbar`, `Menu`, `ContentUnavailableView`, SF Symbols (with symbol effects), Dynamic Type text styles, semantic colors.
- **Liquid Glass** (iOS 26+): standard bars, tab bars, toolbars, sheets and controls adopt it automatically when built with current SDK. Custom: `.glassEffect()`, `GlassEffectContainer`, `.buttonStyle(.glass/.glassProminent)`. Use glass for the navigation/control layer floating above content — not for content itself. iOS 27 adds a user-facing glass intensity setting; respect accessibility settings (Reduce Transparency, Increase Contrast).
- Wrap iOS-26-only APIs in `if #available(iOS 26, *)` when supporting older versions.
- Animation: `withAnimation(.spring(...))`, `.animation(_, value:)`, `matchedGeometryEffect`, `PhaseAnimator`, `KeyframeAnimator`, `.contentTransition(.numericText())`, navigation zoom transitions, `sensoryFeedback` for haptics.
- Libraries are rarely needed; popular extras: Pow (effects), Lottie/Rive, SwiftUI-Introspect (escape hatch).

## Android — Jetpack Compose

- **Material 3** (`androidx.compose.material3`); **M3 Expressive** (new motion physics, shapes & shape morphing, button groups, FAB menus, loading indicators, flexible toolbars) lives in the material3 1.5 line — most APIs graduated from experimental; check whether 1.5.0 is stable in your Compose BOM.
- Dynamic color (Material You) on Android 12+; tonal surface containers for elevation.
- Edge-to-edge is enforced on recent Android targets — handle `WindowInsets`.
- Adaptive layouts: `material3-adaptive` (list-detail, supporting pane, navigation suite) for foldables/tablets.
- Motion: `animate*AsState`, `AnimatedVisibility`, `AnimatedContent`, shared element transitions (`SharedTransitionLayout`), `spring()` specs; M3 motion scheme tokens.
- Non-Material looks: build on `foundation` + your own components, or Compose Unstyled.

## Kotlin Multiplatform

Compose Multiplatform shares Compose UI to iOS (stable for iOS since 2025); consider native SwiftUI for iOS-critical screens to keep platform feel.
