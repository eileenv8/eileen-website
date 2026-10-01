"""New angles for the detailed portrait.

Instead of redrawing, the head is treated as a rounded form and turned
mathematically. Every point on the face, features, and front hair is moved:

- Turn (yaw): a point at horizontal offset x from the face's centre line sits at
  angle a = asin(x / R) on a cylinder of radius R. Turning the head moves it to
  a + turn * cos(a), so the outline stays put while the features slide toward
  the far side and bunch up there, the way they do in a three-quarter view.
  The nose sticks out from the face, so points near it move a little further.
- Tilt (roll): the head rotates about the top of the neck. Hair below the jaw
  rotates less and less, because it hangs.

The body (neck, shirt, necklace) is left as it was, so the head turns on the body.
"""
import math
import re
from lxml import etree
from svgpathtools import parse_path
from geo import pts_to_d
import style_flat

OUT = "out"
SVG = "http://www.w3.org/2000/svg"
CX, R = 300.0, 118.0
PIVOT = (300.0, 470.0)


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def make_warp(turn=0.0, tilt_deg=0.0):
    tilt = math.radians(tilt_deg)

    def yaw(x, y):
        xr = (x - CX) / R
        if abs(xr) >= 1:
            return x, y
        w = 1 - smoothstep(470, 540, y)            # only the head turns
        a = math.asin(xr)
        nx = CX + R * math.sin(a + turn * w * math.cos(a))
        # the nose stands proud of the face, so it travels further
        bump = 0.30 * R * math.exp(-((x - 303) / 13) ** 2) * smoothstep(326, 392, y) * (1 - smoothstep(398, 412, y))
        nx += bump * math.sin(turn * w)
        return nx, y

    def roll(x, y):
        w = 1 - smoothstep(430, 650, y)            # hair hanging below the jaw rotates less
        a = tilt * w
        dx, dy = x - PIVOT[0], y - PIVOT[1]
        return (PIVOT[0] + dx * math.cos(a) - dy * math.sin(a),
                PIVOT[1] + dx * math.sin(a) + dy * math.cos(a))

    def f(x, y):
        return roll(*yaw(x, y))

    def eye(x, y, centre):
        # irises keep looking at the viewer: they follow the head only part way
        cx, cy = centre
        tx, _ = yaw(cx, cy)
        return roll(x + 0.86 * (tx - cx), y)

    return f, eye, tilt_deg


def warp_path(d, f):
    path = parse_path(d)
    out = []
    for sub in path.continuous_subpaths():
        L = sub.length()
        if L < 0.5:
            continue
        step = 1.8 if L < 60 else (4 if L < 300 else 7)
        n = max(2, int(L / step))
        pts = []
        for i in range(n + 1):
            if 0 < i < n:
                try:
                    t = sub.ilength(min(L * i / n, L * 0.999999))
                except ValueError:          # rare rounding at a segment boundary
                    t = i / n
            else:
                t = 0 if i == 0 else 1
            z = sub.point(t)
            pts.append(f(z.real, z.imag))
        closed = abs(sub.start - sub.end) < 0.6
        if closed:
            pts = pts[:-1]
        out.append(pts_to_d(pts, closed=closed))
    return " ".join(out)


def local_scale(f, x, y):
    (a, _), (b, _) = f(x - 1, y), f(x + 1, y)
    return max(0.35, (b - a) / 2)


def warp_tree(root, f, eye, tilt_deg):
    eye_groups = {"eyel": (256, 327), "eyer": (344, 327)}

    def fn_for(el):
        p = el
        while p is not None:
            cp = p.get("clip-path") or ""
            for k, c in eye_groups.items():
                if f"#{k})" in cp:
                    return lambda x, y, c=c: eye(x, y, c)
            p = p.getparent()
        return f

    targets = []
    for gid in ("head", "headback", "faceClip", "eyel", "eyer"):
        node = root.find(f".//{{{SVG}}}*[@id='{gid}']")
        if node is not None:
            targets.append(node)
    for node in targets:
        for el in node.iter():
            if not isinstance(el.tag, str):        # skip comments
                continue
            tag = etree.QName(el).localname
            g = fn_for(el)
            if tag == "path" and el.get("d"):
                el.set("d", warp_path(el.get("d"), g))
            elif tag in ("circle", "ellipse"):
                cx, cy = float(el.get("cx")), float(el.get("cy"))
                nx, ny = g(cx, cy)
                el.set("cx", f"{nx:.1f}"); el.set("cy", f"{ny:.1f}")
                if tag == "ellipse":
                    s = local_scale(g, cx, cy)
                    el.set("rx", f"{float(el.get('rx')) * s:.1f}")
                    if tilt_deg:
                        el.set("transform", f"rotate({tilt_deg:.1f} {nx:.1f} {ny:.1f})")


def render(turn=0.0, tilt=0.0, mirror=False, title="Detailed illustrated portrait of Eileen Jubilee"):
    svg = style_flat.detailed()
    # mark the head so only it moves
    svg = svg.replace("  <!-- face -->", '  <g id="head">\n  <!-- face -->', 1)
    svg = svg.replace('  <rect width="600" height="750" filter="url(#grain)"', '  </g>\n  <rect width="600" height="750" filter="url(#grain)"', 1)
    svg = re.sub(r'(<path fill="url\(#hairBackG\)" d="[^"]+"/>)', r'<g id="headback">\1</g>', svg, count=1)
    root = etree.fromstring(svg.encode())
    f, eye, tdeg = make_warp(turn, tilt)
    warp_tree(root, f, eye, tdeg)
    if mirror:
        # the other direction: flip the whole picture, then put the sun back on the right
        kids = [k for k in root if isinstance(k.tag, str) and etree.QName(k).localname not in ("defs", "title", "style")]
        g = etree.SubElement(root, f"{{{SVG}}}g", transform="translate(600,0) scale(-1,1)")
        for k in kids:
            g.append(k)
        for c in g.iter(f"{{{SVG}}}circle"):
            if c.get("fill") == "url(#sunG)" or c.get("stroke") == "#C4552C":
                c.set("cx", "130")
    t = root.find(f"{{{SVG}}}title")
    if t is not None:
        t.text = title
    return etree.tostring(root, encoding="unicode")


if __name__ == "__main__":
    jobs = [
        ("02a-detailed-three-quarter-right.svg", dict(turn=0.34, title="Detailed portrait of Eileen Jubilee, head turned three-quarters")),
        ("02b-detailed-three-quarter-left.svg", dict(turn=0.34, mirror=True, title="Detailed portrait of Eileen Jubilee, head turned three-quarters the other way")),
        ("02c-detailed-tilt.svg", dict(turn=0.08, tilt=-7, title="Detailed portrait of Eileen Jubilee, head tilted")),
        ("02d-detailed-turn-and-tilt.svg", dict(turn=0.26, tilt=6, title="Detailed portrait of Eileen Jubilee, head turned and tilted")),
    ]
    for name, kw in jobs:
        s = render(**kw)
        open(f"{OUT}/{name}", "w").write(s)
        print(name, len(s))
