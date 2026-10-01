"""Animated head tilt for the detailed portrait (02e).

The head (face, features, hairline) rotates about the top of the neck.
Hair can't simply rotate with it, because it hangs: the hair is instead
sheared (skewX) about the bottom of the picture, so its top travels with
the head while its ends stay put. The skew angle is chosen so the top of
the hair moves as far as the crown does:

    crown shift  = (470 - 170) * sin(a)   rotating about the neck at y = 470
    hair shift   = (750 - 170) * tan(s)   shearing about the bottom, y = 750
    so s ~= -0.517 * a                    (negative: skewX leans the other way)

The hair runs the same keyframes a fraction of a second late, which reads as
follow-through. CSS animations inside an SVG keep running when it's used as an
<img>, and everything holds still for prefers-reduced-motion.
"""
import re
import style_flat

OUT = "out"

# (percent of the loop, head angle in degrees)
KEYS = [(0, 0), (10, 0), (24, -8), (40, -8), (54, 7), (70, 7), (84, 0), (100, 0)]
SKEW = -0.517
LOOP = 11      # seconds
LAG = 0.22     # seconds the hair trails the head


def keyframes(name, fn):
    body = " ".join(f"{p}% {{ transform: {fn(a)}; }}" for p, a in KEYS)
    return f"@keyframes {name} {{ {body} }}"


CSS = f"""
  .head {{ transform-origin: 300px 470px; animation: tilt {LOOP}s cubic-bezier(.45,0,.25,1) infinite; }}
  .hang {{ transform-origin: 300px 750px; animation: hang {LOOP}s cubic-bezier(.45,0,.25,1) {LAG}s infinite; }}
  .hang-back {{ transform-origin: 300px 750px; animation: hang {LOOP}s cubic-bezier(.45,0,.25,1) {LAG + 0.08}s infinite; }}
  .stone {{ transform-origin: 303px 524px; animation: stone {LOOP}s cubic-bezier(.45,0,.25,1) {LAG + 0.15}s infinite; }}
  {keyframes('tilt', lambda a: f'rotate({a}deg)')}
  {keyframes('hang', lambda a: f'skewX({SKEW * a:.2f}deg)')}
  {keyframes('stone', lambda a: f'rotate({-0.35 * a:.2f}deg)')}
  @media (prefers-reduced-motion: reduce) {{ .head, .hang, .hang-back, .stone {{ animation: none; }} }}
"""


def build():
    svg = style_flat.detailed(animated=True)
    # the old gentle lock sway would fight the new motion
    svg = svg.replace('<g class="sway-l">', "<g>").replace('<g class="sway-r">', "<g>")
    svg = svg.replace("</style>", CSS + "</style>", 1)

    # back hair hangs
    svg = re.sub(r'(<path fill="url\(#hairBackG\)" d="[^"]+"/>)', r'<g class="hang-back">\1</g>', svg, count=1)

    # necklace sways a touch, opposite the head
    svg = svg.replace('  <g transform="translate(0,6)">', '  <g class="stone"><g transform="translate(0,6)">', 1)
    svg = svg.replace("  </g>\n\n  <!-- face -->", "  </g></g>\n\n  <!-- face -->", 1)

    # face and features rotate
    svg = svg.replace("  <!-- face -->", '  <g class="head">\n  <!-- face -->', 1)
    svg = svg.replace("  <!-- front locks with strand detail -->", "  </g>\n  <!-- front locks with strand detail -->\n  <g class=\"hang\">", 1)
    # locks end where the hairline starts; the hairline belongs to the head
    svg = svg.replace('  <path fill="#5E3A28" d=', '  </g>\n  <g class="head">\n  <path fill="#5E3A28" d=', 1)
    svg = svg.replace('  <rect width="600" height="750" filter="url(#grain)"', '  </g>\n  <rect width="600" height="750" filter="url(#grain)"', 1)
    svg = svg.replace("<title id=\"t\">Detailed illustrated portrait of Eileen Jubilee</title>",
                      "<title id=\"t\">Animated portrait of Eileen Jubilee tilting her head from side to side</title>")
    return svg


if __name__ == "__main__":
    s = build()
    open(f"{OUT}/02e-detailed-tilt-animated.svg", "w").write(s)
    print(len(s))
