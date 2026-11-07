---
name: promo-video-3d
description: Build a short, catchy 3D promo / intro / teaser / launch video for a product entirely in code — Remotion + three.js (React Three Fiber) with bloom, real app screenshots on a 3D phone, kinetic type, a soundtrack synthesized on the beat grid, and a QR call-to-action — rendered to MP4 locally for free, no accounts. Use this whenever the user wants a video for a demo, pitch, steering committee, launch, app intro, reel or "something they'll remember", asks for 3D or motion-graphics video, mentions Remotion, DaVinci/After Effects-style animation done by Claude, "make a video of my app", or says a previous video "looks like a fancy PowerPoint".
---

# 3D promo video in code

A 30–45 s promo lives or dies on **one memorable image** and on **rhythm**. Text sliding over flat backgrounds reads as "a fancy PowerPoint" no matter how polished; real 3D space (lighting, depth, reflections, bloom) plus cuts locked to a beat grid is what makes it feel produced. Everything here runs locally and free: Remotion renders React frame by frame, three.js gives real 3D, numpy synthesizes the music on the same grid.

## When to use / not use
- Use for: product intros before a live demo, launch teasers, pitch openers, social reels of an app, animated logo reveals.
- Not for: editing existing footage (use a real NLE), long explainers with narration, UI micro-animations inside the app (use `animate` / `choreograph`).

## Workflow

1. **Brief in one line.** Audience, where it plays (projector? phone?), length, the single action you want after it (scan the QR, download, stay for the demo). Ask only what you can't infer.
2. **Find the concept in the brand, not in a template.** Look at the logo, the splash animation, the product's core verb. The concept that worked best: *the logo's parts are characters* — two halves of a mark that search for each other and collide to form the logo. Give the climax to that collision. See `references/storytelling.md` for the structure and copy rules.
3. **Storyboard on a beat grid before writing scenes.** 120 BPM at 30 fps → 1 beat = 15 frames, 1 bar = 60. Put every scene, cut, text slam and impact on beats in one `timing.ts`. Music, visuals and SFX all read from this grid, which is what makes it feel synced.
4. **Spike the 3D pipeline first** (5 minutes, one still): `ThreeCanvas` + one mesh + bloom, rendered with `--gl=angle`. The known traps (black frames from the composer, textures not ready, non-deterministic randomness) are in `references/remotion-three-pipeline.md` — read it before building scenes.
5. **Start from the starter kit** in `assets/starter/` (`cp -R` it, `npm i`, `npm run still` must show the example collision) (Stage with environment light + bloom + vignette + grain, camera rig, mirrored floor, additive glow sprites, warm-up, slam text, procedural sport-ball textures). Copy it into a new folder **outside** the product repo.
6. **Capture the real product** for any "show the app" beat: Playwright at 4x DPR, real data, and isolate pop-out elements with transparent backgrounds (copy `scripts/capture_element.mjs` into the project; see `references/ui-captures.md`). Never crop rectangles out of a screenshot for pop-outs: they blur and drag background corners along.
7. **Build scene by scene, review with contact sheets, not full renders.** `scripts/contact_sheet.sh` renders a handful of stills and tiles them into one image you can look at. Fix composition, then move on. Look specifically for the defects in `references/look-and-feel.md` (horizon cuts, grey floors, edge-on shapes, chunky bevels).
8. **Soundtrack on the same grid** with `scripts/synth.py` + an arrangement file (template: `scripts/music_example.py`): every visual event gets a sound (landing → thud, spin → whoosh, collision → impact + the product's own UI sound). Prefer no voice-over unless a human records it — see `references/audio.md`.
9. **Full render + automatic checks**: `scripts/check_render.py out.mp4` reports duration, isolated black frames and loudness/true peak. Then hand it over and iterate on the user's timestamps.

## Decisions that mattered (keep them)
- **3D over 2D.** The flat kinetic-type version was rejected as "a PowerPoint"; the 3D version was "almost perfect" on first view.
- **One hero moment** (the collision → logo) with flash, shockwave rings, particle burst, camera shake and the brand's real sound.
- **Real UI, honestly shown.** Real screenshots of prod; never fake screens or numbers. If the demo account has empty states, drop that feature from the video instead of inventing data. Check what real data looks like before filming it (seeded/bot users may have joke names).
- **Every visual beat has an audible beat**, and things land exactly on the beat (drop height computed so the fall takes one beat).
- **End on a frame you can pause on**: logo + one-line CTA + URL + big QR (dark on white, ≥450 px).

## Mistakes to avoid (they cost iterations)
- Text-to-speech voice-over: intelligible only with heavy ducking and still judged "pretty shitty". Music-only or a human recording.
- Glow sprites or background halos crossing a floor plane get clipped into a hard horizon line → no floor in scenes that don't need one, `depthTest={false}` on halos that must cross one, fog to dissolve horizons.
- Big extrusion bevels make a logo look like a framed pyramid → bevel ≈ 5% of depth, 8 segments.
- White materials read grey under one key light → give whites emissive ≈ 0.4.
- Shapes spinning on the axis of travel read as flat bars right before impact → ease the spin out (`fly²`) so they arrive face-on.
- Look at real objects before declaring textures done (a football's pentagons need the correct dual-polyhedron orientation; pádel balls look like tennis balls, so show the paddle).
- Claims in copy ("more sports coming") are promises to the audience — flag them to the user.

## Output
- A self-contained Remotion project (outside the product repo) with `src/timing.ts` as the single source of timing, `audio/` tools, `capture/` scripts.
- `out/<name>-vN.mp4` per iteration (H.264 CRF 17, AAC 256k). Report: what changed, what was checked (contact sheet, black-frame scan, LUFS) and what you could *not* check (you can't listen — say so).

## References
- `references/remotion-three-pipeline.md` — setup, versions, render flags, every pipeline bug hit and its fix. Read before step 4.
- `references/look-and-feel.md` — lighting, materials, bloom, floors, glows, camera, text over 3D, phone mockup with pop-outs, review checklist.
- `references/storytelling.md` — structure of a 40 s intro, concept patterns, copy rules, the feedback loop.
- `references/audio.md` — music in code on the grid, SFX mapping, loudness targets, voice-over findings.
- `references/ui-captures.md` — capturing real app screens and isolated UI elements with Playwright.
- `assets/starter/` — copyable project skeleton (kit, warm-up, slam text, ball textures, example scene).
- `scripts/contact_sheet.sh`, `scripts/check_render.py`, `scripts/synth.py`, `scripts/music_example.py`, `scripts/capture_element.mjs`.
