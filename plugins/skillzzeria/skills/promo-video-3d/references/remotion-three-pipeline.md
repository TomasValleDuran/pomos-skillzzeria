# Remotion + three.js pipeline

## Versions that render correctly together (Nov 2026)

| Package | Version |
|---|---|
| `remotion`, `@remotion/cli`, `@remotion/three`, `@remotion/google-fonts` | 4.0.541 (all Remotion packages **must** share one exact version) |
| `three` / `@types/three` | 0.187.0 |
| `@react-three/fiber` | 9.8.2 (v9 = React 19) |
| `@react-three/drei` | 10.7.9 |
| `@react-three/postprocessing` / `postprocessing` | 3.2.2 / 6.39.6 |
| `react`, `react-dom` | 19.x |
| `playwright` (captures) | 1.65 |

`assets/starter/package.json` pins these. Install with `npm i`; a duplicate `three@0.170` pulled by `stats-gl` (drei dev dep) is harmless.

Typescript: with React 19 types there is no global `JSX` namespace — type R3F element props with `ThreeElements['group']` from `@react-three/fiber`. Add `"resolveJsonModule": true` to import shared JSON (e.g. a layout file read by both the scene and the music script).

## Rendering

```bash
npx remotion studio src/index.tsx                                  # live preview
npx remotion still  src/index.tsx Main out/f.png --frame=420 --gl=angle --props='{"audio":null}'
npx remotion render src/index.tsx Main out/v1.mp4 --codec h264 --crf 17 --audio-codec aac --audio-bitrate 256k --gl=angle
```

- `--gl=angle` on macOS (GPU). On Linux CI without GPU: `--gl=swangle` (slow but works).
- A 40 s 1080p30 scene with bloom + reflector renders in ~5–10 min on an M-series Mac with default concurrency.
- CRF 17 + film grain ≈ 4 MB/s (≈160 MB for 40 s). Fine for local playback; export a CRF 23 copy for messaging apps.
- Pass audio as a composition prop so stills can disable it (`audio: null`).
- 60 fps (ad) doubles render time; at 120 BPM a beat is then 30 frames. Decide fps in the brief, not later.

### Stills script for fast review
Bundle once, render many frames: `bundle()` from `@remotion/bundler` → `selectComposition` → loop `renderStill({ frame })`. Invocation like `node scripts/stills.mjs 60,180,700 [layer] [outDir]`. Much faster than one `npx remotion still` per frame, and feeds the contact sheet.

### Layered render + composite (for an ad you'll keep fixing)
- A composition prop `layer: 'all' | 'bg' | 'ui' | 'type' | 'fx'` and a tiny `<L name="ui">…</L>` wrapper that renders its children only in that layer or in `all`. A `useShows('bg')` hook skips mounting the three.js canvases in the other layers, so UI/type/fx renders take minutes instead of the 3D's ~20.
- Split used: `bg` = 3D + backgrounds · `ui` = phone, screens, map pins, QR · `type` = all typography, logo, wordmark · `fx` = flares, light fills, ripples, flashes, particles.
- Outside `all`/`bg` the page background is transparent. Render `bg` as `--codec=prores --prores-profile=hq`; the others as `--codec=prores --prores-profile=4444 --image-format=png --pixel-format=yuva444p10le` with props `{"layer":"ui","audio":false}`, `--muted`.
- Composite: ffmpeg `overlay` chain BG ← UI ← TYPE ← FX, then H.264 High CRF 15 preset slow + the audio mix.
- **Partial re-render**: ProRes is all-intra, so render `--frames=600-719` of one layer and splice it in with the concat demuxer and `-c copy`. A black cut at 624–696 was fixed this way without touching the rest.
- Payoff: changing the CTA URL = re-render `ui` + `type` and re-composite. Changing the music = re-mux only.

### Headless / cloud container (no GPU, restricted network)
- Remotion's Chrome download (`remotion.media`) may be blocked. Point it at Playwright's headless shell in `remotion.config.ts`: `Config.setBrowserExecutable('<pw-browsers>/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell')`.
- No GPU: `Config.setChromiumOpenGlRenderer('swangle')`. Expect ~1–1.5 s per 3D frame on 2 CPUs (bg layer of 2400 frames ≈ 22 min with `--concurrency=2`).
- **The project lives only in the container.** Copy the project (not just renders) to the user's machine before the session ends; copying may be limited per file size (400 MB seen), so send big files one by one.

## Bugs hit and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Every still is **pure black** once `<EffectComposer>` is added | The composer's render targets are not ready on the first frame a tab draws; each parallel render tab hits it once | `Warmup` component (in the starter): on mount `delayRender`, call `advance()` on 3 consecutive animation frames, then `continueRender`. Confirmed: 0 black frames over 1230-frame renders afterwards. |
| Still black after preserving the drawing buffer | Not the cause by itself | Keep `gl={{ preserveDrawingBuffer: true }}` anyway, but the real fix is the warm-up |
| Composer black with `multisampling={0}` | Same first-frame issue | `multisampling={4}` works once warmed up (needed for clean edges) |
| Textures pop in / frames render before an image loads | `TextureLoader` is async | `useImageTexture(src)` in the kit wraps the load in `delayRender`/`continueRender` |
| Particles / city / rain differ between frames or flicker | `Math.random()` per render, and each tab renders a different subset of frames | Seeded PRNG (`rand(seed)` in the kit) inside `useMemo`; everything is a pure function of `frame` |
| Trails or physics drift | Using `useFrame`/clock or accumulating state | Never use `useFrame` for animation. Compute positions analytically from `useCurrentFrame()` (e.g. the ball bounce: closed-form flights with restitution) |
| drei `<Trail>`, `<Text>` (troika loads fonts from the network) | Stateful / network | Build trails as a `TubeGeometry` over the last N% of a path each frame; put text in the 2D layer, not in 3D |
| `useCurrentFrame` inside the canvas | — | Works: `@remotion/three` bridges the context into `ThreeCanvas` |
| A random still errors once, passes on retry | First texture load timing | Re-run; if persistent, raise `delayRender` timeout |
| Physics too complex for closed form (dozens of balls colliding) | — | **Precompute** a deterministic sim once (seeded, fixed dt with 4 substeps, sphere–sphere impulses, rolling ω = up × v / r) into arrays per frame, then index by frame. Export contacts to JSON for the SFX |
| Post-processing with raw three (no R3F `EffectComposer`) | Needs a render loop | `UnrealBloomPass`/`BokehPass` in a three `EffectComposer` driven from `useFrame((_, dt) => composer.render(), 1)`. Priority 1 takes over rendering; animation values still come from the frame number, never from the clock |
| Scenes inside `<Sequence>` disagree about time | Local vs global frames mixed | Pick per scene and write it down: either local frames (subtract `SC.x.from` from global times) or wrap in `<Sequence from={-SC.x.from}>` to get global frames back |

## Structure that scales

```
src/
  timing.ts          BPM, BEAT, b(beats) → frames, SCENES (from/dur in beats), beatPulse()
  theme.ts           brand tokens + fonts (@remotion/google-fonts)
  config.ts          URL for the QR, screenshot paths, audio file
  three/kit.tsx      Stage, Cam, Floor, Glow, useImageTexture, roundedRect, rand
  three/Warmup.tsx   the composer fix
  components/Slam.tsx  kinetic text over 3D
  scenes/*.tsx       one file per scene, each its own <Stage> inside a <Sequence>
  Video.tsx          the Sequences
audio/tools/         synth.py + music.py (reads the same beats)
capture/             Playwright scripts
```

One `<Stage>` (ThreeCanvas) per scene is simpler than one global canvas: each scene has its own camera, lights and fog, and a Sequence boundary is a hard cut you control.

For seamless transitions, **overlap** the Sequences (e.g. world 0–696, phone 624–1488, balls 1428–1752, brand 1710–2400 at 60 fps) and hand off inside the overlap (camera dives into a light fill, the next scene emerges from it). Watch the overlap for one scene's opaque background covering the other too early.

The narrated ad's layout, for reference: `timeline.ts` (VO, SC, key frames, CTA_URL) · `theme.ts` (tokens copied from the product's design system) · `lib/anim.ts` (the product's Bézier curves, `prog()`, `keys()`, `seeded()`) · `lib/layers.tsx` (`<L>`, `MBlur`) · `ui/kit.tsx` + `ui/screens.tsx` + `ui/Phone.tsx` (rebuilt app) · `scenes/<Scene>.tsx` + `scenes/<scene>/*3D.tsx` (DOM part + three.js part per scene).
