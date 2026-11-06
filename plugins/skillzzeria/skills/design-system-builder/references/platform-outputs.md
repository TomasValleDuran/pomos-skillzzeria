# Platform Outputs

## Web — CSS variables + Tailwind v4

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));

/* Primitives → utilities (bg-violet-600, p-4, rounded-lg …) */
@theme {
  --font-sans: "Inter Variable", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, monospace;
  --color-violet-600: oklch(49.1% 0.241 292.6);
  /* … ramps from palette.py --format tailwind … */
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --text-body: 1rem; --text-body--line-height: 1.5;
}

/* Semantic roles switch per theme */
:root { --bg: var(--color-neutral-50); --text: var(--color-neutral-950); --accent: var(--color-violet-600); }
.dark { --bg: var(--color-neutral-950); --text: var(--color-neutral-50); --accent: var(--color-violet-400); }

/* Expose semantic roles as utilities: bg-bg, text-text, bg-accent … */
@theme inline { --color-bg: var(--bg); --color-text: var(--text); --color-accent: var(--accent); }
```

To **restrict** the palette to your system (recommended for teams), reset namespaces: `--color-*: initial;` inside `@theme` before defining your own.

### shadcn/ui theming
shadcn components consume variables `--background, --foreground, --card, --popover, --primary, --primary-foreground, --secondary, --muted, --muted-foreground, --accent, --destructive, --border, --input, --ring, --chart-1..5, --sidebar-*, --radius`. Map your semantic tokens onto them in `:root` / `.dark` (e.g. `--primary: var(--accent)`, `--ring: var(--focus-ring)`), set `--radius`, and change the font. Note shadcn's `--accent` means "subtle hover background", not the brand color — map carefully. tweakcn can preview themes visually.

## React Native

**Plain/Unistyles** — a typed theme object:
```ts
export const light = {
  colors: { bg: '#faf9ff', text: '#0b0a0f', textMuted: '#54535a', accent: '#6d28d9', accentFg: '#fff', border: '#e4e3eb' },
  space: (n: number) => n * 4,
  radius: { sm: 6, md: 10, lg: 16, full: 999 },
  type: { body: { fontSize: 17, lineHeight: 22 }, title: { fontSize: 22, lineHeight: 28, fontWeight: '600' } },
} as const;
export const dark = { ...light, colors: { ...light.colors, bg: '#0b0a0f', text: '#faf9ff' /* … */ } };
```
Unistyles 3: `StyleSheet.configure({ themes: { light, dark }, settings: { adaptiveThemes: true } })`.
**NativeWind v5**: same Tailwind v4 CSS `@theme` + CSS variables as web (share the token CSS between web and native); use `vars()` / dark variants for theme switching.
**Tamagui**: `createTokens` + `createThemes` (themes are generated from palettes; sub-themes for components).
Hex output: `palette.py ... --notation hex` (RN doesn't parse `oklch()` everywhere — verify for your RN version; hex is safe).

## Flutter

```dart
final scheme = ColorScheme.fromSeed(seedColor: const Color(0xFF6D28D9), brightness: Brightness.light);
ThemeData(
  colorScheme: scheme,
  useMaterial3: true,
  textTheme: GoogleFonts.interTextTheme(),
  extensions: const [AppTokens(space: AppSpace(), radius: AppRadius())],
);

@immutable
class AppTokens extends ThemeExtension<AppTokens> { /* custom semantic tokens, copyWith + lerp */ }
```
Use `ColorScheme.fromSeed` for M3 roles, or construct `ColorScheme(...)` explicitly from your generated palette for exact brand control. Access: `Theme.of(context).extension<AppTokens>()!`.

## SwiftUI

- Colors: Asset Catalog color sets with Any/Dark (+ High Contrast) appearances → `Color("AccentSubtle")`, or a generated `extension Color { static let accentSubtle = Color("AccentSubtle") }`. Set the app's `AccentColor` asset.
- Prefer system semantic colors for neutrals (`.primary`, `.secondary`, `Color(.systemBackground)`) — they adapt to Liquid Glass, dark mode and accessibility settings for free.
- Type: Dynamic Type styles `.font(.body)`, custom fonts via `.custom("Inter", size: 17, relativeTo: .body)` so they scale.
- Spacing/radius: `enum Space { static let s2: CGFloat = 8 … }`; continuous corners.

## Jetpack Compose

```kotlin
private val LightColors = lightColorScheme(primary = Color(0xFF6D28D9), onPrimary = Color.White, surface = Color(0xFFFAF9FF) /* … */)
@Immutable data class Spacing(val xs: Dp = 4.dp, val sm: Dp = 8.dp, val md: Dp = 16.dp, val lg: Dp = 24.dp)
val LocalSpacing = staticCompositionLocalOf { Spacing() }

@Composable fun AppTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
  val colors = if (dynamicColorAvailable) dynamicLightColorScheme(LocalContext.current) else LightColors
  CompositionLocalProvider(LocalSpacing provides Spacing()) {
    MaterialTheme(colorScheme = colors, typography = AppTypography, shapes = AppShapes, content = content)
  }
}
```
Material Theme Builder exports M3 schemes from a seed. Decide whether dynamic color (Material You) overrides the brand — many brands use it only for neutral surfaces or not at all.

## One source → many platforms (pipelines)

**Style Dictionary v5** (Amazon; DTCG support; ESM config):
```js
// sd.config.mjs
export default {
  source: ['tokens/**/*.json'],
  platforms: {
    css:     { transformGroup: 'css',     buildPath: 'dist/css/',     files: [{ destination: 'tokens.css', format: 'css/variables' }] },
    js:      { transformGroup: 'js',      buildPath: 'dist/js/',      files: [{ destination: 'tokens.js',  format: 'javascript/es6' }] },
    ios:     { transformGroup: 'ios-swift', buildPath: 'dist/ios/',   files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift', options: { className: 'Tokens' } }] },
    compose: { transformGroup: 'compose', buildPath: 'dist/android/', files: [{ destination: 'Tokens.kt', format: 'compose/object', options: { className: 'Tokens', packageName: 'com.app.tokens' } }] },
  },
};
```
Some DTCG 2025.10 value shapes (structured dimensions/durations/colors) may need custom transforms depending on SD version — check its DTCG docs.

**Terrazzo** (DTCG-native, CLI + plugins): `@terrazzo/plugin-css`, `plugin-tailwind` (generates Tailwind v4 theme incl. modes), `plugin-js`, `plugin-swift`, `plugin-sass`. Good default for new DTCG-first setups.

**Figma**: Figma Variables ↔ tokens via Tokens Studio, Figma's variable export, or the Figma MCP (`get_variable_defs`). Keep **one** direction of truth (design→code or code→design), not both.
