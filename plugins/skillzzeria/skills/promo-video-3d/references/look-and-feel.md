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
- Hard cuts on beats are better than long camera transitions for energy. For a "seamless" brief, use **one continuous camera** per world: a slow push, then a Catmull-Rom path (`CatmullRomCurve3`, eased) descending over the city and diving into the main light beam, with a white-blue light fill covering the hand-off to the next scene.
- **2D elements tracked on 3D**: write a `project(frame, Vector3)` that rebuilds the same camera for that frame and returns screen x/y + depth. Use it to place DOM elements (the app's real map pins, a click ripple on a 3D ball) with scale by depth. Text and UI stay crisp and still follow the 3D.

## Motion blur and depth of field
- **Directional motion blur** for DOM elements: an SVG filter with `feGaussianBlur stdDeviation="x y"` proportional to velocity in px/frame (`pos(f) − pos(f−1)`), capped at ~24 px. Use on kinetic words (vertical), the phone (x/y from its pose function) and logo pieces flying in (horizontal). Velocity comes from the same pure pose function, so it's deterministic.
- **Rack focus** in 3D: `BokehPass` with the focus distance animated from the crowd to the hero object and the aperture opening. Sells the "macro" look on the ball rain.

## Light as a wave
- An impact that "turns the city on": a uniform `uWave` radius (0→125 over ~190 frames at 60 fps) in the building shader. Windows (procedural per-cell hash) light up inside the radius, edges get a bright ring that travels with the wave, and the court markings light up when their beam rises. Average window detail with distance to avoid moiré, and use manual exponential fog in the shader.

## Text over 3D
- Text stays in the 2D layer (crisp, fast, real fonts). Big display weight (800–900), negative tracking, **slam in on the beat** (scale 1.35→1 spring + blur 16→0), out in 5 frames.
- Put text **at the bottom third** when the object is the subject; centered when the text is the subject. Left-aligned big words + phone on the right for feature beats.

## Phone with the real app
- **Generic phone, not an iPhone**: no Dynamic Island, no exact Apple frame (trade dress in an ad). Punch-hole camera, side buttons, dark titanium gradient.
- Two builds that worked:
  - **three.js**: `RoundedBox` body (metalness 0.85), screen = `MeshBasicMaterial` with the screenshot (`toneMapped={false}` so UI colors stay true), brand mark on the back.
  - **CSS 3D** (when the screens are React components): the screen is live DOM at the phone's CSS size (392×848), the frame gets real thickness from ~11 stacked layers in Z, plus a glass reflection that slides with `rotY`. One `pose(f)` function drives entry (rotX 48°→0, scale 0.72→1, rising), side shift, float, small rotY "flicks" on each screen change, centering, and exit; its derivative feeds the motion blur.
- Taps: a finger circle with press + ripple at the tapped element, with a `tap()` SFX on the same frame.
- "All in one app" beat: the phone centers and 3–4 other screens fan out around it as 3D panels.
- Screen change = 360° spin centered on the beat; swap the texture exactly at 180° (back facing camera).
- **Pop-out**: one UI element per screen flies out 0.4 units toward camera with a spring, a halo behind, then retracts before the next spin. Use an *isolated* capture of the element (transparent PNG at 4x) on a plane of the element's CSS size; small elements get a minimum on-screen size (`max(1.28, 0.42 / width)`).

## Hero collision recipe
Copy the app's **splash animation** if it has one (read its CSS: fly-in from the sides, settle with overshoot 1.10 → 0.995 → 1, flare on contact, glow bloom 0 → 0.85 → 0.38, wordmark reveal by `clip-path`). Recreating it big makes the video and the live app feel like one piece. Then layer on: white flash (2D, 0→0.9→0 in 6 frames) · two shockwave rings (white, then accent 4 frames later) scaling 0.2→9 · 900-point additive burst flattened toward the screen plane with `1 - exp(-t/9)` expansion · emissive spike decaying `exp(-t/8)` · spring overshoot 1.35→1 · shake · then the wordmark clip-reveal underneath.

## Review checklist (run on every contact sheet)
- [ ] Any hard horizontal line behind a glow? (floor clipping)
- [ ] Any grey band where floor meets background? (env on floor / missing fog)
- [ ] Whites actually white? Accent used once per frame?
- [ ] Objects facing camera at their key moment (not edge-on)?
- [ ] Bevels thin; no "frame" artefacts on the logo?
- [ ] Pop-outs sharp at 200% zoom, no background corners?
- [ ] Text readable against everything behind it, not covering the hero?
- [ ] Last frame pausable: logo, CTA, URL, QR all visible and static?
- [ ] QR decodes from a rendered frame to the **production** URL? (`cv2.QRCodeDetector().detectAndDecode(cv2.imread('f.png'))`; error level H if a logo covers the centre)
- [ ] Phone generic (no Dynamic Island)? Photos cleared for advertising use?
- [ ] Scene overlaps: no opaque background appearing before the previous scene has handed off?

## End card QR
Generate with the `qrcode` package (error correction `H`), dark modules on a white card, the brand mark in the centre, revealed with a radial wipe from the centre, plus a short line ("ESCANEÁ Y SUMATE") and the URL in text. The URL lives in one constant (`CTA_URL`, `CTA_URL_LABEL`).
