// Capture frames of an SVG's CSS animations at exact times by seeking every animation.
const { chromium } = require('playwright');
(async () => {
  const [inp, outdir, fps = '12', secs = '11', w = '600', h = '750'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + require('path').resolve(inp));
  await p.waitForTimeout(300);
  const n = Math.round(+fps * +secs);
  for (let i = 0; i < n; i++) {
    const t = i * 1000 / +fps;
    await p.evaluate((t) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; } }, t);
    await p.screenshot({ path: `${outdir}/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
