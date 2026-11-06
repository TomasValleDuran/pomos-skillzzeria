# Motion Libraries (snapshot Nov 2026)

Principle: **use the platform first, a library when you need springs, layout/shared transitions, gestures, timelines or exit animations.** For *how* to animate (easing, duration, purpose), use the `emil-design-eng`, `animate`, `animate-expo`, `choreograph`, `review-animations` and `apple-design` skills.

## Web

| Need | Use |
|---|---|
| Hover, focus, simple enter/exit, color/opacity | **CSS transitions** + `@starting-style` (enter from `display:none`), `transition-behavior: allow-discrete` |
| Route/page transitions, shared-element morphs | **View Transitions API** (same-document in all modern engines; cross-document `@view-transition` — check support), React `<ViewTransition>` |
| Scroll-linked effects (progress bars, reveal, parallax) | **CSS scroll-driven animations** (`animation-timeline: scroll()/view()`) — progressive enhancement where unsupported; otherwise Motion `useScroll` / GSAP ScrollTrigger |
| React springs, layout animations, `AnimatePresence` exits, gestures, drag | **Motion** (motion.dev, formerly Framer Motion; also vanilla JS + Vue) |
| Complex timelines, scroll storytelling, SVG morphing, text splitting | **GSAP** (100% free incl. all plugins: ScrollTrigger, SplitText, MorphSVG, Flip) |
| Physics springs in React (alternative) | React Spring |
| Zero-config list add/remove/reorder animation | **AutoAnimate** (`@formkit/auto-animate`) |
| Number transitions | **NumberFlow** |
| Designer-made vector animation, simple playback | **Lottie** (`lottie-web`, `@lottiefiles/dotlottie-web`) — prefer dotLottie format |
| Interactive, state-machine-driven vector animation (buttons, mascots, onboarding) | **Rive** — smaller files, runtime state machines |
| 3D | three.js / **React Three Fiber** + drei; Spline for designer-built scenes (heavy — lazy-load) |
| Programmatic CSS animation | Web Animations API (`element.animate()`) |
| Canvas/WebGL backgrounds, shaders | OGL, three.js, Paper Shaders, Unicorn Studio (export) — lazy-load, pause offscreen |
| Smooth scrolling | Lenis (only for scroll-storytelling sites; never on app UIs) |

## React Native

| Need | Use |
|---|---|
| Everything performant (UI thread) | **Reanimated 4** — includes a CSS-like `animation`/`transition` style API, layout animations, shared element transitions (4.2+); requires New Architecture |
| Gestures | **react-native-gesture-handler** (v3 Gesture API) |
| Declarative presets | Moti (built on Reanimated; check v4 compatibility), or Reanimated's CSS API |
| Custom drawing / shaders | React Native Skia |
| Vector animation | lottie-react-native, rive-react-native |
| Haptics | expo-haptics |
| Native transitions | Expo Router / native-stack transitions, iOS zoom transitions where supported |

## Flutter

Implicit animations (built-in) → explicit `AnimationController` → **flutter_animate** for chains → `animations` package (container transform, shared axis, fade through) → Rive/Lottie. Material 3 Expressive motion springs in recent Flutter versions (verify).

## SwiftUI / Compose

Use native APIs (see mobile.md). SwiftUI springs are the default animation; Compose uses `spring()` and the M3 motion scheme. Haptics: SwiftUI `sensoryFeedback`, Android `HapticFeedbackConstants`/`performHapticFeedback`.

## Non-negotiables on every platform

- Respect reduced motion (`prefers-reduced-motion`, iOS Reduce Motion / `accessibilityReduceMotion`, Android "Remove animations" / `ANIMATOR_DURATION_SCALE`). Replace movement with opacity, don't just disable feedback.
- Animate transform/opacity (web); keep animations on the UI thread (RN worklets).
- Interruptible: user input mid-animation must take over.
- UI animations mostly 150–300ms; frequent actions get less or none.
