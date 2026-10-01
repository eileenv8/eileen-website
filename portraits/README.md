# Portraits

Ten illustrated portraits of Eileen, all drawn as code from one shared set of shapes
(`src/geo.py`), so the likeness holds across styles. See them side by side in the
"Eileen Portrait Studies" gallery.

| File | Style | Notes |
|---|---|---|
| `01-golden-hour.svg` | Flat vector | `-animated` blinks, sways, sun breathes |
| `02-golden-hour-detailed.svg` | Detailed flat vector | `-animated` adds drifting fog |
| `02a`–`02d` | Detailed, new angles | three-quarter (both sides), head tilt, turn and tilt; made by `src/angles.py` |
| `02e-detailed-tilt-animated.svg` | Detailed, head tilting side to side | 11-second loop; `02e-detailed-tilt.mp4` is the same loop as video, for social posts. Made by `src/tilt_anim.py` |
| `03-pencil-sketch.svg` | Pencil, black and white | |
| `04-gestural-ink.svg` | Brush ink + watercolor | |
| `05-one-line.svg` | Single continuous line | `-animated` draws itself |
| `06-riso.svg` | Two-ink risograph halftone | |
| `07-pixel.svg` | Pixel art | blinks (animation built in) |
| `08-polyculture.svg` | Botanical, hair as vines | `-animated` vines grow in |
| `09-cut-paper.svg` | Cut-paper collage | |
| `flowfield.html` | p5.js particle painting | live sketch, click to repaint |
| `00-first-draft.svg` | The first draft | with bag strap |

All animations stop for visitors who've asked their system for reduced motion.

## Use one on the site

```html
<img src="/portraits/01-golden-hour.svg" alt="Illustrated portrait of Eileen Jubilee" width="600" height="750">
```

CSS animations inside an SVG keep running when it's loaded with `<img>`.

## Regenerate

Needs Python 3 with `svgpathtools`, `numpy`, `pillow`, `scikit-image`, and Node with Playwright
(for rendering previews that the riso, pixel, and flow-field styles sample from).

```
cd src
python3 style_flat.py          # 01, 02 (writes to ./out)
node render.js out/01-golden-hour.svg out/p01.png
node render.js out/02-golden-hour-detailed.svg out/p02.png
python3 style_lines.py         # 03, 04, 05
python3 style_more.py          # 06, 07, 08
python3 style_paper.py         # 09
python3 style_gen.py           # 10
python3 angles.py              # 02a-02d: the detailed portrait at new angles
python3 tilt_anim.py           # 02e: animated head tilt
# video: node frames.js out/02e-detailed-tilt-animated.svg frames 24 11, then
# ffmpeg -framerate 24 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p out/02e-detailed-tilt.mp4
```

Edit a shape once in `geo.py` (say, the brow arch) and every style picks it up.
