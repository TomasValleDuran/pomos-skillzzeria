# Look and feel

The target look: dark stage, one accent color, glossy objects, soft bloom, film grain. Premium comes from **restraint** (black background, few objects, one accent) and **light** (environment reflections + bloom), not from detail.

## The Stage (in the starter kit)
- Background `#000`, **fog** to black (`[near, far]` ≈ 2× and 4× the camera distance) — it dissolves floors and city edges into the void instead of a visible horizon.
- `Environment` built only from `Lightformer`s (no HDR download): a white top strip, a brand-accent side strip, a dim white fill. Intensity 0.25–0.8 per scene.
- Post: `Bloom` (intensity 0.9–1.3, `luminanceThreshold` 0.55–0.85, `mipmapBlur`), `Vignette` (0.65), `Noise` (0.035). Raise bloom briefly on the hero impact.
- Material defaults: `meshPhysicalMaterial` with `clearcoat 1`, roughness 0.15–0.3; accent objects get emissive ≈ 0.45 of their own color, **white objects emissive ≈ 0.4** (otherwise they read grey).

## Floors
- `MeshReflectorMaterial` floor sells "real space" (reflections of balls, triangles). Keep it **near-black** and set `envMapIntensity ≈ 0.12`, or the environment turns it into a grey band.
- **Only add a floor when something touches it** (balls bouncing, objects standing). Scenes with floating objects (phone, logo, CTA) look better with no floor: no horizon line to clip halos.

## Glows / halos
- Additive sprites with a radial-gradient canvas texture (`Glow` in the kit). Cheap, controllable, and they bloom.
- A halo whose lower half sits behind a floor is **clipped into a hard horizontal line** — the most visible defect in review. Fix: no floor, or `depthTest={false}` on that sprite, or move it in front.
- Background halo behind a hero object: big (scale ≈ 10) and low opacity (≈ 0.4) so its edge never reads as a disc.

## Shapes
- Extrude logos with `ExtrudeGeometry`: depth ≈ 0.2 of the height, **bevel ≈ 0.01 (5% of depth) with 8 segments**. A 0.025 bevel produced an "inner triangle inside a frame" look.
- Logo pieces that spin while flying: ease the spin to zero before contact (`rotation = fly² · 4π`) so they arrive face-on; spinning on the travel axis shows them edge-on as bars.
- Procedural textures are fine and license-free; check them against reality: football = Voronoi of the 12 icosahedron vertices (black) + 20 vertices of the **dual** dodecahedron (white) with the right permutation; tennis/baseball seam = `lat = 0.42·sin(2·lon)`; volleyball = 3 stripe groups per dominant axis. Where real objects look alike (pádel vs tennis ball), show the distinguishing object (the paddle).

## Fake volumetric light
- Open cylinder (top radius 0.25, bottom 1.4) with a shader: alpha = `pow(|dot(N,V)|, 2.5) · mix(0.25, 1, uv.y)`, additive, no depth write. Plus a soft glow plane on the floor and a real `spotLight` (penumbra 1). A flat-opacity cone looks like a solid grey lampshade — don't.

## Camera
- Drive the camera from props every frame (`Cam` in the kit). Moves that worked: slow push-in on a hero (5–10%), crane up to reveal distance ("they're far apart"), drone descending onto a city following a character, push into an object to transition, 8–12 frames of decaying shake on impact.
- Hard cuts on beats are better than long camera transitions for energy.

## Text over 3D
- Text stays in the 2D layer (crisp, fast, real fonts). Big display weight (800–900), negative tracking, **slam in on the beat** (scale 1.35→1 spring + blur 16→0), out in 5 frames.
- Put text **at the bottom third** when the object is the subject; centered when the text is the subject. Left-aligned big words + phone on the right for feature beats.

## Phone with the real app
- `RoundedBox` body (dark titanium, metalness 0.85), screen = `MeshBasicMaterial` with the screenshot (`toneMapped={false}` so UI colors stay true), dynamic-island pill, brand mark on the back.
- Screen change = 360° spin centered on the beat; swap the texture exactly at 180° (back facing camera).
- **Pop-out**: one UI element per screen flies out 0.4 units toward camera with a spring, a halo behind, then retracts before the next spin. Use an *isolated* capture of the element (transparent PNG at 4x) on a plane of the element's CSS size; small elements get a minimum on-screen size (`max(1.28, 0.42 / width)`).

## Hero collision recipe
White flash (2D, 0→0.9→0 in 6 frames) · two shockwave rings (white, then accent 4 frames later) scaling 0.2→9 · 900-point additive burst flattened toward the screen plane with `1 - exp(-t/9)` expansion · emissive spike decaying `exp(-t/8)` · spring overshoot 1.35→1 · shake · then the wordmark clip-reveal underneath.

## Review checklist (run on every contact sheet)
- [ ] Any hard horizontal line behind a glow? (floor clipping)
- [ ] Any grey band where floor meets background? (env on floor / missing fog)
- [ ] Whites actually white? Accent used once per frame?
- [ ] Objects facing camera at their key moment (not edge-on)?
- [ ] Bevels thin; no "frame" artefacts on the logo?
- [ ] Pop-outs sharp at 200% zoom, no background corners?
- [ ] Text readable against everything behind it, not covering the hero?
- [ ] Last frame pausable: logo, CTA, URL, QR all visible and static?
