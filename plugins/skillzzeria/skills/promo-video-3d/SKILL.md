---
name: promo-video-3d
description: Build a short, catchy 3D promo / intro / teaser / launch spot for a product entirely in code — Remotion + three.js with bloom, the real app on a 3D phone (screenshots or screens rebuilt from the product's own components), kinetic type, a narrator voice-over (ElevenLabs) cut phrase by phrase onto the timeline, music and SFX on the beat grid, and a scannable QR call-to-action — rendered to a finished MP4 master (optionally in alpha layers). Use this whenever the user wants a video for a demo, pitch, steering committee, launch, ad, app intro, reel or "something they'll remember", asks for 3D or motion-graphics video, mentions Remotion, ElevenLabs narration, DaVinci/After Effects-style animation done by Claude, "make a video of my app", or says a previous video "looks like a fancy PowerPoint".
---

# 3D promo video in code

A 30–45 s promo lives or dies on **one memorable image** and on **rhythm**. Text sliding over flat backgrounds reads as "a fancy PowerPoint" no matter how polished. Real 3D space (lighting, depth, reflections, bloom), with cuts and narration locked to one timeline, is what makes it feel produced. Remotion renders React frame by frame, three.js gives real 3D, and numpy synthesizes music and SFX on the same grid. Everything runs locally; the only paid piece worth paying for is the voice (ElevenLabs).

## When to use / not use
- Use for: product intros before a live demo, launch teasers, ads, pitch openers, social reels of an app, animated logo reveals.
- Not for: editing existing footage (use a real NLE), long explainers, UI micro-animations inside the app (use `animate` / `choreograph`).

## Workflow

1. **Brief in one line.** Audience, where it plays (projector? phone? ad?), length, fps (30 is enough for a projector; 60 for an ad), voice or no voice, and the single action you want after it (scan the QR, download, stay for the demo). If there is a voice, get the **exact script** now: it drives the whole timeline. Ask only what you can't infer.
2. **Find the concept in the brand, not in a template.** Look at the logo, the splash animation, the product's core verb. The concept that worked best: *the logo's parts are characters*, two halves of a mark that search for each other and collide to form the logo. Give the climax to that collision. See `references/storytelling.md` for structures and copy rules.
3. **One timeline file before any scene.** `timeline.ts` holds the BPM grid (120 BPM → 1 beat = 15 frames at 30 fps, 30 at 60 fps), the voice-over phrase starts (`VO[]`), scene ranges (`SC`), and every key moment (impact, the click, each tap). Scenes, music, SFX and VO all read from it. With narration, the **phrases are the skeleton**: place visuals under the words, then snap the hits to the beat.
4. **Spike the 3D pipeline first** (5 minutes, one still): `ThreeCanvas` + one mesh + bloom, rendered with `--gl=angle` (`swangle` without a GPU). The known traps (black frames from the composer, textures not ready, non-deterministic randomness, headless Chrome in a container) are in `references/remotion-three-pipeline.md`. Read it before building scenes.
5. **Start from the starter kit** in `assets/starter/` (`cp -R` it, `npm i`, `npm run still` must show the example collision): Stage with environment light + bloom + vignette + grain, camera rig, mirrored floor, glow sprites, warm-up, slam text, procedural sport-ball textures. Keep the project **outside** the product repo.
6. **Show the real product.** Use one of two routes, both honest:
   - **Screenshots on a 3D phone** (fast): Playwright at 4x DPR, real data, pop-outs captured as isolated transparent elements (`scripts/capture_element.mjs`; see `references/ui-captures.md`).
   - **Screens rebuilt in React from the product's own code** (best for ads): the repo's color/type tokens, the app font, real copy strings, real icons and seed data, at the phone's CSS size. They can animate: taps with a finger indicator, swipes, toasts, wizard steps. Chosen as "the best option" for the 40 s ad. Nothing invented: every string and token comes from a file you can name.
7. **Build scene by scene, review with contact sheets, not full renders.** `scripts/contact_sheet.sh` renders a handful of stills into one image. Fix composition, then move on. Check for the defects in `references/look-and-feel.md` (horizon cuts, grey floors, edge-on shapes, chunky bevels).
8. **Audio on the same timeline** (`references/audio.md`):
   - **Voice**: ElevenLabs, a native voice for the audience's accent, with direction tags. Cut the take into one file per phrase with `scripts/split_vo.py` (silence detection plus a slight speed-up), then place each phrase at its `VO[]` start.
   - **SFX**: short and dry (clicks, taps, bounces), one per visual event, read from the same data the scene uses.
   - **Music**: synthesize a temp track on the grid (`scripts/synth.py` + `scripts/music_example.py`) with a silence right before the hero hit. Swap in a licensed track later if the user has one.
   - **Mix**: stems → `loudnorm` to −14 LUFS / −1 dBTP.
9. **Render the master, then check it.** For one-pass work, render a single MP4. When fixes will be local (a URL, one scene), render **layers** (bg / ui / type / fx, ProRes with alpha) and composite with ffmpeg: changing the URL then means re-rendering two fast layers, not the 3D. Run `scripts/check_render.py out.mp4` (duration, isolated black frames, LUFS/true peak) and **decode the QR from a rendered frame** (it must resolve to the intended URL). Then hand it over and iterate on the user's timestamps.

## Decisions that mattered (keep them)
- **3D over 2D.** The flat kinetic-type version was rejected as "a PowerPoint". The 3D version was "almost perfect" on first view.
- **One hero moment** (the collision → logo) with flash, shockwave, particles, camera shake and the brand's real sound. In the narrated ad, a second hero beat: **the click**, a tap on the final object that cuts to the logo on a music hit after half a second of silence.
- **Real product, honestly shown.** Real screenshots or screens rebuilt from the real components and strings. Never fake numbers. If the demo account has empty states, drop that feature. Look at real data before filming it (seeded/bot users may have joke names).
- **A good neural voice works; cheap TTS doesn't.** The ElevenLabs narrator (rioplatense voice, direction tags, sped up 7%) shipped. Local Piper TTS was rejected as unclear.
- **Every visual beat has an audible beat**, and things land exactly on the beat (drop height computed so the fall takes one beat).
- **Seamless where the brief asks for it**: scenes overlap (one continuous camera dives into a light beam, and the phone emerges from it) instead of hard cuts. Hard cuts on beats are the high-energy alternative.
- **End on a frame you can pause on**: logo + one-line CTA + URL + big QR (dark on white, ≥450 px, error level H if a logo sits in the middle).
- **The agent delivers the finished master.** Don't assume the user has DaVinci/Premiere. Music swaps, URL changes and copy fixes are re-rendered or re-muxed by you, not handed back as "edit this in your NLE".

## Mistakes to avoid (they cost iterations)
- Local/robotic TTS: intelligible only with heavy ducking and still judged "pretty shitty". Use ElevenLabs-class voices or a human.
- Glow sprites or background halos crossing a floor plane get clipped into a hard horizon line → no floor in scenes that don't need one, `depthTest={false}` on halos that must cross one, fog to dissolve horizons.
- Big extrusion bevels make a logo look like a framed pyramid → bevel ≈ 5% of depth, 8 segments.
- White materials read grey under one key light → give whites emissive ≈ 0.4.
- Shapes spinning on the axis of travel read as flat bars right before impact → ease the spin out (`fly²`) so they arrive face-on.
- Look at real objects before declaring textures done (a football's pentagons need the correct dual-polyhedron orientation; pádel balls look like tennis balls, so show the paddle).
- A phone that copies Apple's (Dynamic Island, the exact iPhone frame) is a trade-dress risk in an ad → generic frame, punch-hole camera.
- The QR pointing to a preview/dev URL. Confirm the **production** URL before the final render and keep it in one constant.
- Claims in copy ("more sports coming"), and product photos whose **licence for advertising** is unknown: flag both to the user.

## Output
- A self-contained Remotion project (outside the product repo) with `src/timeline.ts` as the single source of timing, `public/vo/` phrase WAVs + `durations.json`, `audio/` tools, `capture/` scripts, `scripts/` for stills and layer renders.
- `out/<name>-vN.mp4` per iteration (H.264; CRF 15–17 for the master, AAC 256–320k). Report what changed, what was checked (contact sheet, black-frame scan, LUFS, QR decode) and what you could *not* check (you can't listen, so say so).
- A handoff `.md` when the work may continue in another session: brief, sources of every brand element, timeline table, render commands, pending items. Projects in a cloud container vanish with the session; copy the project, not just the renders, to the user's machine.

## References
- `references/remotion-three-pipeline.md`: setup, versions, render flags, layered render + composite, partial re-renders, headless/container setup, every pipeline bug hit and its fix. Read before step 4.
- `references/look-and-feel.md`: lighting, materials, bloom, floors, glows, camera (continuous paths + projecting 3D points to 2D), motion blur, depth of field, text over 3D, phone mockups, review checklist.
- `references/storytelling.md`: structure of a 40 s intro (music-only) and a 40 s narrated ad, concept patterns, copy rules, the feedback loop.
- `references/audio.md`: ElevenLabs voice-over pipeline, music on the grid, SFX mapping, swapping in a licensed track, loudness targets.
- `references/ui-captures.md`: capturing real screens and isolated UI elements, or rebuilding screens from the product's components.
- `assets/starter/`: copyable project skeleton (kit, warm-up, slam text, ball textures, example scene).
- `scripts/contact_sheet.sh`, `scripts/check_render.py`, `scripts/split_vo.py`, `scripts/synth.py`, `scripts/music_example.py`, `scripts/capture_element.mjs`.
