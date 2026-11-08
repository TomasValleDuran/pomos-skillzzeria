# Storytelling for a 40-second intro

## Structure that worked (82 beats at 120 BPM ≈ 41 s)

| Beats | Scene | Job |
|---|---|---|
| 0–12 | **Pain** — each half of the logo alone under a spotlight; 3–5 short slams ("Saturday, 7 pm." · "Two players short.") then a crane reveals how far apart they are; lights out | Recognition: everyone in the room has lived it |
| 12–24 | **World** — the problem space as a 3D place (dark city like the app's map; beacons light up on beats; the hero character crosses it with a light trail) | Show the product's promise without UI yet |
| 24–44 | **Product** — 3D phone, 4 real screens × 4 beats, one UI element pops out per screen; one-word headlines ("Find." "Join." "Create." "Discover.") | Proof it exists and is real |
| 44–58 | **Breadth / fun** — objects of the domain land one per beat, then a rain of more ("And more coming."), then everything spirals into a point of light | Energy peak before the climax |
| 58–66 | **Climax** — the two halves fly in and collide → logo, wordmark, tagline, the app's own splash sound | The image people remember |
| 66–82 | **CTA** — two-beat punchline ("Stop looking for players." → "Start playing."), then the end card: 3D logo, CTA line, URL pill, big QR | The action; pausable while the live demo starts |

Shorter (30 s): drop the World scene and use 3 product screens.

## Narrated 40 s ad (1080p60, ElevenLabs voice, "Apple-style")
Script (14 phrases): *Sábado, 19 h. · Faltan dos. · ¿Cómo se encuentran? · Partidos cerca tuyo. · Encontrá. · Sumate. · Armá el tuyo. · Descubrí. · Todo en una app. · Y vienen más. · Elegí el tuyo. · SportMatch. · Dejá de buscar jugadores. · Empezá a jugar.*

| Seconds | Scene | What's on screen |
|---|---|---|
| 0–5.9 | **Hook** | The logo's two halves as 3D prisms, apart and rotating among shards, with hook text between them; they attract and **collide** (5.9 s) into the logo: flare, anamorphic streak, and a wave that lights up the city |
| 6–11.6 | **City** | One continuous camera descends over a procedural neon version of the real town; volumetric beams rise at each match; real map pins projected onto 3D; the camera dives into the main beam (the "2 spots left" match) and a light fill covers the screen |
| 10.6–24.8 | **Product** | A phone emerges from the light. Four rebuilt screens (map → swipe → create wizard → profile) with real taps, toasts and transitions; one action word per screen on the left ("Encontrá." "Sumate." "Armá el tuyo." "Descubrí.", numbered 01–04); then "Todo en una app": phone centred, screens fan out in 3D; phone falls out with motion blur |
| 23.8–29.2 | **Breadth** | A rain of balls of every sport (physics, reflections, depth of field), rack focus onto the hero ball ("Y vienen más." "Elegí el tuyo.") |
| 28.5 | **The click** | Half a second of silence, then a tap on the hero ball → ripple, flash, music hit |
| 28.5–40 | **Brand + CTA** | The app's splash animation, big: halves fly in, flare, wordmark reveal, particles; the logo compacts upward; "Dejá de buscar jugadores." → "Empezá a jugar."; QR + URL + "ESCANEÁ Y SUMATE" |

The voice carries the story, so the visuals can be more abstract (prisms, city of light) than in a music-only cut, where the slams have to carry it.

## Concept patterns
- **Brand mark as characters**: logo pieces = the two sides of the marketplace (player ↔ match, buyer ↔ seller, mentor ↔ student). Their meeting is the product. Strongest pattern found.
- **Reuse the product's own motion**: if the app has a splash animation and sound, recreate it big for the reveal — continuity between video and app when the demo starts.
- **Domain objects as rhythm**: balls, tools, ingredients… landing on beats is cheap to build and reads instantly.

## Copy rules
- Write in the product's voice and language (rioplatense Spanish here: "Sumate", "Armá el tuyo", "Empezá a jugar").
- 2–5 words per slam. One idea per beat. Subtitles only on product beats, one line.
- **No invented numbers** (user counts, ratings). If metrics are inflated by test/bot data, leave them out entirely.
- Every promise is a claim to the audience ("more sports coming", "free", "in seconds"): flag it to the user before shipping.

## What did not work
- **Flat 2D kinetic type + phone mockup**: competent but "looks like a fancy PowerPoint".
- **Cheap TTS voice-over**: a local model (Piper `es_AR`) was "not easy to understand" and cheapened it. An ElevenLabs native voice with direction tags did work (see `audio.md`).
- Cropped screenshot pop-outs (blurry, background corners).

## Feedback loop
- Show a contact sheet early (6–12 frames) before any full render; full renders only for the user's review.
- Ask the user for **timestamps + screenshots** of what bothers them; they spot real defects (horizon cuts, blurry pop-outs, bevels) that are easy to miss in thumbnails.
- Version every render (`-v1`, `-v2`…), never overwrite the file the user is watching.
- Work in batches and leave recoverable state (a handoff `.md`, the timeline table, render commands): long sessions get cut by usage limits, and another agent may pick it up.
- Ask early whether the user has an editor (DaVinci, Premiere). If not, deliver only the finished master and make every change yourself; don't ship layer/stem packages they can't use.
