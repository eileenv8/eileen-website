// Renders SVG/HTML files to PNG so each style can be checked by eye.
// usage: node render.js in.svg out.png [width height] [waitMs]
const { chromium } = require('playwright');
(async () => {
  const [inp, out, w = '600', h = '750', wait = '0'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + require('path').resolve(inp));
  if (+wait) await p.waitForTimeout(+wait);
  await p.screenshot({ path: out });
  await b.close();
})();
