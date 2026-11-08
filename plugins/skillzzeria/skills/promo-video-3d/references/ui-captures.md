# Showing the real app

Two honest routes. **Captures** (this file's first half) are fast and exact. **Rebuilt screens** (at the end) take longer but animate: taps, swipes, toasts, wizard steps. Pick rebuilt screens for an ad and captures for a quick intro.

## Screens
- Playwright with the installed Chrome (`chromium.launch({ channel: 'chrome' })`), mobile context: `viewport 390×844`, **`deviceScaleFactor: 4`**, `isMobile`, `hasTouch`, locale/timezone of the audience, `colorScheme: 'dark'` if the app is dark.
- Log in with a demo/QA account the user gives you; pass credentials via env vars, never write them to files or memory.
- **Use prod data** if that's what the audience will see in the demo, but look at it first: seeded or simulated users may have joke names (fictional characters) — pick records with plausible names. Empty states (no matches, no notifications) are not filmable: drop that feature from the video.
- Maps: set `geolocation` to where the data actually is (compute the median of record coordinates, then centre on the densest cluster); wait ~8 s for tiles; zoom out with `page.mouse.wheel(0, 300)` steps; never `waitUntil: 'networkidle'` on map pages (it never settles).
- Capture all screens **and** their pop-out elements in the **same session**, so element positions match the screenshots.

## Isolated elements (pop-outs)
`scripts/capture_element.mjs` (module or standalone). **Copy it into the project's `capture/` folder** — Node resolves `playwright` from the script's own location, so running it from the skill directory fails.
1. Locate the element (`getByRole('button', { name })`, or a text filter + walk up to the visual container; log candidate chains with bounding boxes and `border-radius` to pick the right ancestor).
2. Inject a style: `body * { visibility: hidden }` and `[data-pop], [data-pop] * { visibility: visible }`; transparent `html, body` background.
3. Glassy elements (`backdrop-filter`) lose their backdrop: force an opaque equivalent background on the element during capture.
4. `page.screenshot({ clip: box ± 2px, omitBackground: true })` → PNG with alpha, exact shape, shadows included.
5. Record the box in CSS px into a JSON (`{src, x0, y0, x1, y1, r}`) the scene imports to position the plane on the phone.

Result vs. cropping the screenshot: sharp text at any zoom, no background corners, no slivers of neighbouring UI.

## Rebuilding screens from the product's code
Read the repo; copy, don't invent. Keep a table of *element → source file* in the handoff, so anyone can check where each piece came from:

| Element | Where it came from (Next.js example) |
|---|---|
| Colors, radii, shadows, easing curves | design-system token files (`colors.css`, `effects.css`, `typography.css`) → `theme.ts`, `lib/anim.ts` |
| Font | the app's font file (e.g. Geist from the `geist` npm package) loaded with `FontFace` + `delayRender` |
| Logo / wordmark | the brand-mark SVG component (exact polygon points) and the logo component (weights, tracking) |
| Logo animation | the splash-screen CSS (keyframes, durations, curves) |
| Icons | the app's own icon components |
| Copy | the real strings in components ("Me sumo", "Solicitud enviada ⚡", "Publicar partido", wizard questions, tab labels) |
| Data | the demo seed (real place names, demo users), not prod bots |
| Photos | the app's `public/` images. **Confirm the licence covers advertising** before shipping |

- Build a small kit (`BrandMark`, `Wordmark`, `Chip`, `StatusBar`, `TabBar`, `Toast`, `Touch`) and one component per screen at the phone's CSS size (392×848). Each screen takes the frame and animates from it: pins pop with a spring, a card rises after a tap, a swipe stamps "ME SUMO" and the next card grows behind it, the wizard slides between steps.
- Key moments (`PH.map`, `PH.swipe`, tap frames…) live in `timeline.ts`, the same place the `tap()` SFX reads from.
- Recreating screens that don't exist yet, or showing numbers the product doesn't have, is not allowed. Rebuilt means "same as the app", not "a nicer app".
