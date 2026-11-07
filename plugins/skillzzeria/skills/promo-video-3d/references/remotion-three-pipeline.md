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
