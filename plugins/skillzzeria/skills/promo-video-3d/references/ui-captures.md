# Capturing the real app

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
