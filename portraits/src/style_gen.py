"""Generative portraits built from a render of the detailed flat portrait (out/p02.png):
- 09-topographic.svg: the face as a contour map, isolines of brightness
- 10-flowfield.html: a p5.js sketch that paints the portrait with particles on a noise field
"""
import base64
import io
import math
import numpy as np
from PIL import Image, ImageFilter
from skimage import measure
from geo import W, H, pts_to_d

OUT = "out"


def topographic(src="out/p02.png", levels=26):
    img = Image.open(src).convert("L").filter(ImageFilter.GaussianBlur(6.5))
    a = np.asarray(img, dtype=float) / 255
    # stretch contrast so the face and hair spread over the whole range
    lo, hi = np.percentile(a, 2), np.percentile(a, 98)
    a = np.clip((a - lo) / (hi - lo), 0, 1)
    ramp = ["#1F3A33", "#2E5D4F", "#4F7F5F", "#7FA27A", "#B6A36A", "#D48A55", "#C4552C"]

    def col(t):
        x = t * (len(ramp) - 1)
        i = min(int(x), len(ramp) - 2)
        f = x - i
        c0 = [int(ramp[i][k:k + 2], 16) for k in (1, 3, 5)]
        c1 = [int(ramp[i + 1][k:k + 2], 16) for k in (1, 3, 5)]
        return "#%02X%02X%02X" % tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))

    paths = []
    for li in range(1, levels):
        lv = li / levels
        for c in measure.find_contours(a, lv):
            if len(c) < 30:
                continue
            pts = [(round(p[1], 1), round(p[0], 1)) for p in c[::5]]
            w = 1.6 if li % 5 == 0 else 0.9          # every fifth line is an index contour
            paths.append(f'<path d="{pts_to_d(pts)}" stroke="{col(lv)}" stroke-width="{w}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Topographic contour-map portrait of Eileen Jubilee</title>
  <rect width="{W}" height="{H}" fill="#FBF8F3"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">{"".join(paths)}</g>
</svg>
'''


def image_b64(src="out/p02.png", size=(300, 375)):
    im = Image.open(src).convert("RGB").resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


SKETCH_JS = r"""
// Paints the portrait with particles that drift along a Perlin-noise flow field.
// Each particle carries the colour of the pixel beneath it. Strokes start broad
// and get finer, so the face resolves out of loose marks. Click to repaint.
function flowPortrait(holderId, dataUrl) {
  return new p5(function (p) {
    let img, parts = [], t = 0;
    const N = 900, W = 600, H = 750, DURATION = 1500;
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    p.preload = function () { img = p.loadImage(dataUrl); };
    function seed() {
      p.background(251, 248, 243);
      parts = [];
      for (let i = 0; i < N; i++) parts.push({ x: p.random(W), y: p.random(H), life: p.random(40, 140) });
      t = 0;
      p.loop();
    }
    p.setup = function () {
      const c = p.createCanvas(W, H);
      c.parent(holderId);
      c.elt.style.width = '100%'; c.elt.style.height = 'auto';
      img.loadPixels();
      p.noiseSeed(7); p.randomSeed(7);
      seed();
      c.mousePressed(seed);
      p.repaint = seed;
      if (reduce) { for (let k = 0; k < DURATION; k++) step(); p.noLoop(); }
    };
    function colourAt(x, y) {
      const ix = p.constrain(Math.floor(x / 2), 0, img.width - 1);
      const iy = p.constrain(Math.floor(y / 2), 0, img.height - 1);
      const k = 4 * (iy * img.width + ix);
      return [img.pixels[k], img.pixels[k + 1], img.pixels[k + 2]];
    }
    function step() {
      const prog = Math.min(t / DURATION, 1);
      const len = p.lerp(9, 1.6, prog);           // stroke length shrinks: loose -> fine
      const wgt = p.lerp(7, 1.1, Math.pow(prog, 0.7));
      for (const q of parts) {
        const a = p.noise(q.x * 0.006, q.y * 0.006, t * 0.0015) * p.TWO_PI * 2.2;
        const nx = q.x + Math.cos(a) * len, ny = q.y + Math.sin(a) * len;
        const c = colourAt(q.x, q.y);
        p.stroke(c[0], c[1], c[2], p.lerp(70, 150, prog));
        p.strokeWeight(wgt);
        p.line(q.x, q.y, nx, ny);
        q.x = nx; q.y = ny; q.life--;
        if (q.life < 0 || q.x < 0 || q.x > W || q.y < 0 || q.y > H) {
          q.x = p.random(W); q.y = p.random(H); q.life = p.random(40, 140);
        }
      }
      t++;
    }
    p.draw = function () {
      for (let k = 0; k < 3; k++) step();
      if (t >= DURATION) p.noLoop();
    };
  });
}
"""


def flowfield_html():
    data = image_b64()
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eileen — flow field portrait</title>
<style>
  body {{ margin: 0; background: #FBF8F3; display: grid; place-items: center; min-height: 100vh; font: 14px/1.5 Inter, system-ui, sans-serif; color: #4C4739 }}
  #flow {{ width: min(92vw, 480px); cursor: pointer }}
  p {{ text-align: center; margin: 12px 16px 24px }}
</style></head>
<body>
<main>
  <div id="flow" role="img" aria-label="Portrait of Eileen Jubilee painted by drifting particles"></div>
  <p>Click to repaint.</p>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js"></script>
<script>{SKETCH_JS}
flowPortrait('flow', '{data}');
</script>
</body></html>
'''


if __name__ == "__main__":
    svg = topographic()
    open(f"{OUT}/09-topographic.svg", "w").write(svg)
    print("09", len(svg))
    html = flowfield_html()
    open(f"{OUT}/10-flowfield.html", "w").write(html)
    open(f"{OUT}/flow_data_url.txt", "w").write(image_b64())
    print("10", len(html))
