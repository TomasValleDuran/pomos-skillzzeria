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
- **TTS voice-over**: even a good local model (Piper `es_AR`) was "not easy to understand" and cheapened it.
- Cropped screenshot pop-outs (blurry, background corners).

## Feedback loop
- Show a contact sheet early (6–12 frames) before any full render; full renders only for the user's review.
- Ask the user for **timestamps + screenshots** of what bothers them; they spot real defects (horizon cuts, blurry pop-outs, bevels) that are easy to miss in thumbnails.
- Version every render (`-v1`, `-v2`…), never overwrite the file the user is watching.
