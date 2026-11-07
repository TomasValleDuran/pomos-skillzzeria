// Capture real app UI for a promo video with Playwright (needs `playwright` installed in the project).
//
// As a module (inside your own logged-in script):
//   import { isolate } from '<skill-dir>/scripts/capture_element.mjs';
//   const box = await isolate(page, page.getByRole('button', { name: /Join/ }), 'public/screens/pop-join.png');
//   // box = { x0, y0, x1, y1, r } in CSS px → position the plane on the phone screen
//
// Standalone (public pages, no login):
//   node capture_element.mjs <url> "<css selector>" <out.png> [deviceScaleFactor=4] [opaque-bg]
//
// How it works: every other element gets visibility:hidden, html/body go transparent, and the screenshot is
// clipped to the element's box with omitBackground → PNG with alpha, exact shape (rounded corners, tails,
// shadows), sharp text. Cropping a full screenshot instead gives blur, background corners and neighbour slivers.

export async function isolate(page, locator, outPath, { opaqueBg = null, pad = 2 } = {}) {
  const el = locator.first();
  await el.scrollIntoViewIfNeeded().catch(() => {});
  const box = await el.boundingBox();
  if (!box) throw new Error('element not visible: ' + outPath);
  const radius = await el.evaluate((n) => parseFloat(getComputedStyle(n).borderRadius) || 0);
  await el.evaluate((n, bg) => {
    n.setAttribute('data-pop', '1');
    // glass elements lose their backdrop once everything else is hidden → give them an opaque equivalent
    if (bg) { n.style.setProperty('background', bg, 'important'); n.style.setProperty('backdrop-filter', 'none', 'important'); }
    const st = document.createElement('style');
    st.id = 'pop-style';
    st.textContent = 'html, body { background: transparent !important; } body * { visibility: hidden !important; } [data-pop], [data-pop] * { visibility: visible !important; }';
    document.head.appendChild(st);
  }, opaqueBg);
  await page.waitForTimeout(250);
  await page.screenshot({ path: outPath, omitBackground: true, clip: { x: box.x - pad, y: box.y - pad, width: box.width + pad * 2, height: box.height + pad * 2 } });
  await el.evaluate((n) => { n.removeAttribute('data-pop'); document.getElementById('pop-style')?.remove(); });
  return { x0: box.x - pad, y0: box.y - pad, x1: box.x + box.width + pad, y1: box.y + box.height + pad, r: Math.min(radius, box.height / 2) };
}

// Mobile context that matches the phone mockup (390×844 CSS px). 4x so pop-outs stay sharp when scaled up.
export async function mobileContext(browser, { scale = 4, ...extra } = {}) {
  return browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: scale, isMobile: true, hasTouch: true, ...extra });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [url, selector, out, scale = '4', bg] = process.argv.slice(2);
  if (!url || !selector || !out) {
    console.log('usage: node capture_element.mjs <url> "<css selector>" <out.png> [scale=4] [opaque-bg]');
    process.exit(1);
  }
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({ channel: 'chrome' }).catch(() => chromium.launch());
  const page = await (await mobileContext(browser, { scale: Number(scale) })).newPage();
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(2500);
  console.log(JSON.stringify(await isolate(page, page.locator(selector), out, { opaqueBg: bg ?? null })));
  await browser.close();
}
