"""Line-based portraits: pencil sketch, gestural ink, and one continuous line."""
import math
import random
from geo import (P, W, H, STRANDS_LIGHT, STRANDS_DARK, EYE_L, EYE_R, freckles, strands,
                 sample, resample, lock_edges, pts_to_d)

OUT = "out"


# ---------------------------------------------------------------- helpers

def normals(pts):
    out = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        out.append((-dy / L, dx / L))
    return out


def wobble(pts, rng, amp=1.5, freq=0.08):
    """Hand tremor: smooth low-frequency noise pushed along each point's normal."""
    ph1, ph2 = rng.uniform(0, 9), rng.uniform(0, 9)
    ns = normals(pts)
    out = []
    for i, ((x, y), (nx, ny)) in enumerate(zip(pts, ns)):
        o = amp * (0.6 * math.sin(i * freq + ph1) + 0.4 * math.sin(i * freq * 2.7 + ph2))
        out.append((x + nx * o, y + ny * o))
    return out


def trim(pts, rng, a=0.0, b=0.08):
    """Start late / stop early, as a quick hand does."""
    n = len(pts)
    i0 = int(n * rng.uniform(a, b)); i1 = n - int(n * rng.uniform(a, b))
    return pts[i0:max(i1, i0 + 2)]


def edge_between(d_left, name_lock, n=120):
    """Left/right edge of the back hair, top to bottom, for strands behind a lock."""
    pts = sample(d_left, step=2)
    return resample(pts, n)


def back_edges():
    """Outer silhouettes of the back hair (left and right), top to bottom."""
    pts = sample(P["hair_back"], step=2)
    bl = min(range(len(pts)), key=lambda i: math.dist(pts[i], (92, 750)))
    br = min(range(len(pts)), key=lambda i: math.dist(pts[i], (508, 750)))
    left = pts[: bl + 1]
    right = list(reversed(pts[br:]))
    return resample(left, 120), resample(right, 120)


def strands_between(a, b, count, seed, wobble_amp=2.0, start_max=0.25):
    rng = random.Random(seed)
    n = len(a) - 1
    out = []
    for k in range(count):
        f = (k + rng.uniform(0.1, 0.9)) / count
        s0 = int(rng.uniform(0.05, start_max) * n)
        e0 = n - int(rng.uniform(0, 0.1) * n)
        ph = rng.uniform(0, 6.28)
        out.append([(a[i][0] + (b[i][0] - a[i][0]) * f + wobble_amp * math.sin(i / 8 + ph),
                     a[i][1] + (b[i][1] - a[i][1]) * f) for i in range(s0, e0 + 1)])
    return out


def hatch(clip_id, bbox, angle, spacing, rng, width=0.7, opacity=0.6, color="#1d1b18", gap=0.12):
    """Parallel hand-drawn hatch lines over bbox, clipped by clip_id."""
    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2 + 10
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)        # along the line
    vx, vy = -uy, ux                          # across
    lines = []
    k = -R
    while k < R:
        px, py = cx + vx * k, cy + vy * k
        # break each line into 1-3 dashes for a pencil feel
        t = -R
        while t < R:
            seg = rng.uniform(R * 0.4, R * 1.4)
            j = rng.uniform(-0.8, 0.8)
            ax, ay = px + ux * t + vx * j, py + uy * t + vy * j
            bx, by = px + ux * (t + seg) + vx * j * 0.3, py + uy * (t + seg) + vy * j * 0.3
            lines.append(f"M{ax:.1f},{ay:.1f}L{bx:.1f},{by:.1f}")
            t += seg + rng.uniform(0, R * gap)
        k += spacing * rng.uniform(0.8, 1.2)
    return (f'<g clip-path="url(#{clip_id})" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" opacity="{opacity}" fill="none"><path d="{"".join(lines)}"/></g>')


# ---------------------------------------------------------------- pencil sketch

def sketch():
    rng = random.Random(5)
    G = "#1d1b18"

    def line(d, passes=2, amp=1.2, w=1.5, op=0.85, step=4, closed=False, trim_b=0.06):
        out = []
        base = sample(d, step=step)
        for p in range(passes):
            pts = wobble(base, rng, amp=amp * (1 + p * 0.4))
            if not closed:
                pts = trim(pts, rng, 0, trim_b)
            out.append(f'<path d="{pts_to_d(pts)}" stroke-width="{w*(1 - p*0.35):.2f}" opacity="{op*(1 - p*0.3):.2f}"/>')
        return "".join(out)

    parts = []
    # face and features
    parts.append(line(P["face"], passes=3, amp=1.4, w=1.3, closed=True))
    parts.append(line("M262,458 L260,548", passes=2)); parts.append(line("M338,458 L340,548", passes=2))
    for k in ["brow_l", "brow_r"]:
        for j in range(5):
            parts.append(line(P[k], passes=1, amp=1.6, w=1.4, op=0.6, step=3))
    for k in ["lid_l", "lid_r"]:
        parts.append(line(P[k], passes=3, amp=0.6, w=2.0, op=0.9, step=2))
    for k in ["crease_l", "crease_r", "lower_l", "lower_r"]:
        parts.append(line(P[k], passes=1, amp=0.5, w=0.9, op=0.55, step=2))
    parts.append(line(P["nose"], passes=2, amp=0.6, w=1.1, op=0.7, step=3))
    parts.append(line(P["nose_base"], passes=2, amp=0.5, w=1.2, op=0.75, step=2))
    parts.append(line("M268,424 Q284,416 300,420 Q316,416 332,424", passes=2, amp=0.5, w=1.0, op=0.6, step=2))
    parts.append(line(P["mouth"], passes=2, amp=0.4, w=1.6, op=0.85, step=2))
    parts.append(line("M276,429 Q300,446 324,429", passes=1, amp=0.5, w=0.9, op=0.5, step=2))
    # shirt, collar, necklace
    parts.append(line("M40,750 C52,640 125,588 232,556 L264,532", passes=2, amp=1.8, w=1.2))
    parts.append(line("M336,532 L368,556 C475,588 548,640 560,750", passes=2, amp=1.8, w=1.2))
    parts.append(line(P["collar_l"], passes=2, amp=1.0, w=1.2, closed=True))
    parts.append(line(P["collar_r"], passes=2, amp=1.0, w=1.2, closed=True))
    parts.append(line(P["placket"], passes=1))
    parts.append(line("M150,640 C170,670 180,710 178,750", passes=1, op=0.45))
    parts.append(line("M450,640 C432,672 424,710 426,750", passes=1, op=0.45))
    parts.append('<circle cx="300" cy="732" r="5" stroke-width="1" opacity="0.7"/>')
    chain = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.6" stroke-width="0.8" opacity="0.7"/>'
                    for d in [P["chain_l"], P["chain_r"]] for x, y in sample(d, step=5))
    parts.append(chain)
    parts.append('<circle cx="303" cy="645" r="5" stroke-width="1.3"/>')
    parts.append(line(P["pendant"], passes=2, amp=0.4, w=1.3, closed=True, step=2))

    # hair: outlines plus many strands
    for k in ["lock_l", "lock_r"]:
        parts.append(line(P[k], passes=1, amp=1.5, w=1.0, op=0.6, closed=True))
    parts.append(line(P["hair_back"], passes=1, amp=1.8, w=1.0, op=0.55, closed=True))
    strand_svg = []
    for name, seed in [("lock_l", 31), ("lock_r", 32)]:
        for s in strands(name, count=40, seed=seed, wobble=2.0):
            s = wobble(s[::2], rng, amp=0.8)
            strand_svg.append(f'<path d="{pts_to_d(s)}" stroke-width="{rng.uniform(0.6,1.5):.2f}" opacity="{rng.uniform(0.45,0.9):.2f}"/>')
    # strands in the back hair, between the silhouette and the front lock
    bl, br = back_edges()
    il, ol = lock_edges("lock_l", 120)
    ir, or_ = lock_edges("lock_r", 120)
    for a, b, seed in [(bl, ol, 41), (br, or_, 42)]:
        for s in strands_between(a, b, 22, seed, start_max=0.3):
            strand_svg.append(f'<path d="{pts_to_d(s[::2])}" stroke-width="{rng.uniform(0.5,1.0):.2f}" opacity="{rng.uniform(0.3,0.65):.2f}"/>')
    # crown: arcs from the top of the head out to each side
    for j in range(30):
        side = -1 if j % 2 else 1
        f = (j // 2 + 0.5) / 15
        x0 = 300 + side * (4 + 20 * f)
        x1 = 300 + side * (128 + 20 * f)
        y0 = 130 + 40 * f
        d = f"M{x0:.0f},{y0:.0f} C{300 + side*(70 + 30*f):.0f},{y0 - 4:.0f} {x1 - side*6:.0f},{y0 + 40:.0f} {x1:.0f},{y0 + 110:.0f}"
        strand_svg.append(f'<path d="{d}" stroke-width="{rng.uniform(0.6,1.2):.2f}" opacity="{rng.uniform(0.4,0.75):.2f}"/>')
    # crown: strands sweeping from the part
    for j in range(26):
        side = -1 if j % 2 else 1
        f = (j // 2 + 0.5) / 13
        x1 = 300 + side * (90 + 60 * f)
        d = f"M{300 + side*2},{176 + f*4} C{300 + side*40*(0.6+f)},{170 + f*6} {x1 - side*10},{205 + f*25} {x1},{260 + f*40}"
        strand_svg.append(f'<path d="{d}" stroke-width="{rng.uniform(0.5,1.1):.2f}" opacity="{rng.uniform(0.35,0.7):.2f}"/>')
    parts.append("".join(strand_svg))

    # eyes: iris drawn as a dark scribbled disc, pupil, highlight left as paper
    for (cx, cy), cid in [(EYE_L, "eyel"), (EYE_R, "eyer")]:
        scrib = []
        for i in range(36):
            a = i * 0.9
            r = 4 + (i % 6)
            scrib.append(f"{'M' if i == 0 else 'L'}{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
        parts.append(f'<g clip-path="url(#{cid})"><path d="{"".join(scrib)}" stroke-width="0.9" opacity="0.7"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="4.3" fill="{G}" stroke="none"/>'
                     f'<circle cx="{cx+3}" cy="{cy-3.5}" r="2" fill="#FAF9F5" stroke="none"/></g>')

    face_dots, chest_dots = freckles(seed=7, n=150)
    parts.append('<g fill="#4a443c" stroke="none">' + "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.6:.2f}" opacity="{o*0.8:.2f}"/>' for x, y, r, o in face_dots + chest_dots) + "</g>")

    # shading by hatching
    hatches = [
        hatch("faceShade", (296, 196, 400, 476), 62, 4.2, rng, opacity=0.4),
        hatch("neckShade", (258, 440, 342, 520), 160, 4.6, rng, opacity=0.32),
        "",
        hatch("backHair", (90, 125, 510, 750), 82, 3.6, rng, opacity=0.55),
        hatch("backHair", (90, 125, 510, 750), 102, 5.0, rng, opacity=0.35),
        hatch("shirtShade", (420, 595, 560, 750), 50, 5, rng, opacity=0.35),
        hatch("shirtShadeL", (40, 595, 185, 750), 130, 6, rng, opacity=0.25),
        hatch("sockets", (215, 290, 385, 330), 30, 3.5, rng, opacity=0.25),
        hatch("pendantC", (285, 648, 322, 708), 45, 2.2, rng, opacity=0.6),
    ]

    defs = f'''<defs>
    <clipPath id="eyel"><path d="{P['eye_l']}"/></clipPath>
    <clipPath id="eyer"><path d="{P['eye_r']}"/></clipPath>
    <clipPath id="faceShade"><path d="{P['face_shade']}"/></clipPath>
    <clipPath id="neckShade"><path d="M262,440 L338,440 L338,486 C318,500 282,500 262,486 Z"/></clipPath>
    <clipPath id="backHair"><path d="{P['hair_back']}"/></clipPath>
    <clipPath id="belowCrown"><rect x="0" y="235" width="{W}" height="{H}"/></clipPath>
    <clipPath id="shirtShade"><path d="{P['shirt_shade']}"/></clipPath>
    <clipPath id="shirtShadeL"><path d="{P['shirt_shade_l']}"/></clipPath>
    <clipPath id="pendantC"><path d="{P['pendant']}"/></clipPath>
    <clipPath id="sockets"><ellipse cx="255" cy="318" rx="32" ry="12"/><ellipse cx="345" cy="318" rx="32" ry="12"/></clipPath>
    <mask id="underJaw"><rect width="{W}" height="{H}" fill="#fff"/><path d="{P['face']}" fill="#000"/></mask>
    <mask id="notFace">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <path d="{P['face']}" fill="#000"/><path d="{P['neck']}" fill="#000"/><path d="{P['shirt']}" fill="#000"/>
      <path d="{P['lock_l']}" fill="#000"/><path d="{P['lock_r']}" fill="#000"/>
    </mask>
    <filter id="paper" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="2"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.43  0 0 0 0 0.4  0 0 0 0.09 0"/>
    </filter>
  </defs>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Pencil sketch portrait of Eileen Jubilee</title>
  {defs}
  <rect width="{W}" height="{H}" fill="#FAF9F5"/>
  <rect width="{W}" height="{H}" filter="url(#paper)"/>
  <g mask="url(#notFace)"><g clip-path="url(#belowCrown)">{hatches[3]}{hatches[4]}</g></g>
  {hatches[0]}<g mask="url(#underJaw)">{hatches[1]}{hatches[2]}</g>{hatches[5]}{hatches[6]}{hatches[7]}{hatches[8]}
  <g fill="none" stroke="{G}" stroke-linecap="round" stroke-linejoin="round">
    {"".join(parts)}
  </g>
</svg>
'''


# ---------------------------------------------------------------- gestural ink

def brush(pts, rng, wmax, taper=0.6, wobble_amp=1.5):
    """A filled brush stroke: width swells in the middle and tapers to fine ends."""
    pts = wobble(pts, rng, amp=wobble_amp, freq=0.12)
    ns = normals(pts)
    n = len(pts)
    ph = rng.uniform(0, 6)
    left, right = [], []
    for i, ((x, y), (nx, ny)) in enumerate(zip(pts, ns)):
        t = i / max(n - 1, 1)
        w = wmax * (math.sin(math.pi * t) ** taper) * (0.75 + 0.25 * math.sin(t * 7 + ph))
        w = max(w, 0.25)
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    poly = left + list(reversed(right))
    return pts_to_d(poly[::1], closed=True)


def gestural():
    rng = random.Random(9)
    INK = "#1B1714"
    strokes = []

    def add(d, wmax, step=5, part=(0, 1), amp=1.5, taper=0.6, op=0.92):
        wmax *= 1.5
        pts = sample(d, step=step)
        n = len(pts)
        pts = pts[int(n * part[0]): max(int(n * part[1]), int(n * part[0]) + 3)]
        strokes.append(f'<path d="{brush(pts, rng, wmax, taper, amp)}" opacity="{op}"/>')

    # face: two quick strokes that don't quite meet
    add(P["face"], 4.5, part=(0.02, 0.47), amp=2.5)
    add(P["face"], 4.0, part=(0.55, 0.97), amp=2.5)
    add("M264,440 L262,540", 3.0, amp=1.5); add("M336,440 L338,540", 3.0, amp=1.5)
    # features
    add(P["brow_l"], 6, step=3, amp=1.0, taper=0.4); add(P["brow_r"], 6, step=3, amp=1.0, taper=0.4)
    add(P["lid_l"], 4.2, step=2, amp=0.6, taper=0.5); add(P["lid_r"], 4.2, step=2, amp=0.6, taper=0.5)
    add(P["lower_l"], 1.6, step=2, amp=0.4, op=0.6); add(P["lower_r"], 1.6, step=2, amp=0.4, op=0.6)
    add("M304,334 C306,358 312,376 314,390 Q306,398 294,394", 2.6, step=3, amp=0.6)
    add(P["mouth"], 3.6, step=2, amp=0.6, taper=0.5)
    add("M282,442 Q300,449 318,442", 2.0, step=2, amp=0.5, op=0.6)
    # hair: long sweeping strokes
    for name, seed in [("lock_l", 51), ("lock_r", 52)]:
        for s in strands(name, count=9, seed=seed, wobble=3.0):
            strokes.append(f'<path d="{brush(s[::3], rng, rng.uniform(5, 13), 0.5, 2.5)}" opacity="{rng.uniform(0.75, 0.95):.2f}"/>')
    bl, br = back_edges()
    il, ol = lock_edges("lock_l", 120); ir, or_ = lock_edges("lock_r", 120)
    for a, b, seed in [(bl, ol, 61), (br, or_, 62)]:
        for s in strands_between(a, b, 4, seed, wobble_amp=3, start_max=0.35):
            strokes.append(f'<path d="{brush(s[::3], rng, rng.uniform(7, 15), 0.5, 3)}" opacity="0.85"/>')
    for side in (-1, 1):
        for j in range(4):
            f = j / 4
            x1 = 300 + side * (95 + 55 * f)
            d = f"M{300 + side*3},{177 + f*3} C{300 + side*45},{168 + f*8} {x1 - side*8},{205 + f*20} {x1},{265 + f*35}"
            add(d, rng.uniform(3, 6), step=4, amp=1.2, taper=0.5)
    # shoulders and collar: few confident strokes
    add("M48,750 C60,640 130,590 236,556", 5, amp=3)
    add("M364,556 C470,590 540,640 552,750", 5, amp=3)
    add("M266,528 L226,580 L266,606 L300,704", 2.8, step=3, amp=1.2, taper=0.4)
    add("M334,528 L374,580 L334,606 L300,704", 2.8, step=3, amp=1.2, taper=0.4)
    add("M268,522 Q284,600 303,642", 1.4, step=3, amp=0.6, op=0.7)
    add("M332,522 Q322,600 303,642", 1.4, step=3, amp=0.6, op=0.7)

    eyes = "".join(f'<circle cx="{cx}" cy="{cy}" r="5.4" fill="{INK}"/>' for cx, cy in [EYE_L, EYE_R])
    face_dots, _ = freckles(seed=7, n=60)
    fr = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.7:.2f}" opacity="{o*0.7:.2f}"/>' for x, y, r, o in face_dots)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Gestural ink portrait of Eileen Jubilee</title>
  <defs>
    <filter id="wash" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="8" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="38" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feGaussianBlur in="d" stdDeviation="1.2"/>
    </filter>
    <filter id="dry" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 1.35" result="holes"/>
      <feComposite in="SourceGraphic" in2="holes" operator="in"/>
    </filter>
    <filter id="paper" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="3" seed="5"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0.07 0"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="#FBF8F3"/>
  <rect width="{W}" height="{H}" filter="url(#paper)"/>
  <!-- colour washes, deliberately off-register -->
  <g filter="url(#wash)" style="mix-blend-mode:multiply">
    <circle cx="455" cy="170" r="70" fill="#C4552C" opacity="0.55"/>
    <path d="{P['face']}" fill="#EFBFA0" opacity="0.55" transform="translate(-14,8)"/>
    <path d="M70,750 C80,650 140,600 240,570 L360,570 C460,600 520,650 530,750 Z" fill="#9DB6CF" opacity="0.55" transform="translate(18,-6)"/>
    <path d="{P['lock_l']}" fill="#8A5634" opacity="0.4" transform="translate(-10,4)"/>
    <path d="{P['lock_r']}" fill="#8A5634" opacity="0.4" transform="translate(12,-4)"/>
    <ellipse cx="303" cy="680" rx="12" ry="20" fill="#2E5D4F" opacity="0.85"/>
  </g>
  <g fill="{INK}" filter="url(#dry)">
    {"".join(strokes)}
    {eyes}
  </g>
  <g fill="#6B3E26">{fr}</g>
</svg>
'''


# ---------------------------------------------------------------- one continuous line

def continuous_points():
    """Every feature, visited in an order where each one starts near where the last ended."""
    seq = []

    def take(d, step=5, reverse=False):
        pts = sample(d, step=step)
        seq.extend(reversed(pts) if reverse else pts)

    def loop_from(d, near, step=6, reverse=False):
        pts = sample(d, step=step)[:-1]
        i = min(range(len(pts)), key=lambda k: math.dist(pts[k], near))
        pts = pts[i:] + pts[:i] + [pts[i]]
        seq.extend(reversed(pts) if reverse else pts)

    def circle(cx, cy, r, turns=1.15, start=math.pi):
        k = int(28 * turns)
        seq.extend((cx + r * math.cos(start + 2 * math.pi * turns * i / k),
                    cy + r * math.sin(start + 2 * math.pi * turns * i / k)) for i in range(k + 1))

    take("M40,750 C52,640 125,588 232,556 L264,532")          # left shoulder, upward
    take("M264,532 L224,580 L266,606 L300,706", step=4)       # left collar down to the V
    loop_from(P["pendant"], (300, 706), step=3)               # around the stone
    take("M303,651 Q282,600 268,522", step=5)                  # chain, up the left
    take("M264,520 L264,452", step=5)                          # left side of the neck
    # face outline: from the left jaw, under the chin, up the right side, over the forehead
    face = sample(P["face"], step=5)
    i = min(range(len(face)), key=lambda k: math.dist(face[k], (256, 450)))
    j = min(range(len(face)), key=lambda k: math.dist(face[k], (206, 296)))
    # walk backwards from the left jaw: under the chin, up the right cheek, over the top, to the left temple
    seq.extend(face[i::-1] + face[len(face) - 2: j - 1: -1])
    take(P["brow_l"], step=4)
    take(P["lid_l"], step=3, reverse=True)
    circle(*EYE_L, 9.5, start=math.pi)
    take(P["lower_l"], step=3)
    take(P["nose"], step=4)
    take(P["nose_base"], step=3, reverse=True)
    take(P["mouth"], step=4)
    take("M329,425 Q300,446 271,425", step=4)                  # lower lip, back to the left
    take("M268,424 Q284,416 300,420 Q316,416 332,424", step=4)  # upper lip, to the right
    take("M332,424 C346,410 362,380 367,334", step=5)           # up the cheekbone
    take(P["lower_r"], step=3, reverse=True)                   # into the right eye
    circle(*EYE_R, 9.5, start=0)
    take(P["lid_r"], step=3)
    take(P["brow_r"], step=4)
    loop_from(P["lock_r"], seq[-1], step=6)                    # around the right lock
    back = sample(P["hair_back"], step=7)
    bl = min(range(len(back)), key=lambda k: math.dist(back[k], (92, 750)))
    br = min(range(len(back)), key=lambda k: math.dist(back[k], (508, 750)))
    right_up = back[br:]                                       # right silhouette, bottom to crown
    k = min(range(len(right_up)), key=lambda q: math.dist(right_up[q], seq[-1]))
    seq.extend(right_up[k:] + back[1: bl + 1])                 # over the crown, down the left
    loop_from(P["lock_l"], (112, 750), step=6)                 # around the left lock
    seq.extend([(330, 752), (560, 752)])                       # along the bottom edge
    take("M560,750 C548,640 475,588 368,556 L336,532")        # right shoulder, upward
    take("M336,532 L376,580 L334,606 L300,706", step=4)       # right collar to the V
    take("M304,640 Q322,600 332,522", step=5)                  # chain, up the right
    take("M336,520 L336,452", step=5)                          # right side of the neck
    return seq


def continuous(animated=False, color="#1d2a26"):
    pts = continuous_points()
    d = pts_to_d(pts[::1])
    anim = ""
    attrs = ""
    if animated:
        attrs = ' pathLength="1" class="draw"'
        anim = """<style>
  .draw { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 14s cubic-bezier(.45,.05,.55,.95) infinite }
  @keyframes draw { 0% { stroke-dashoffset: 1; opacity: 1 } 70% { stroke-dashoffset: 0; opacity: 1 }
                    92% { stroke-dashoffset: 0; opacity: 1 } 100% { stroke-dashoffset: 0; opacity: 0 } }
  .dot { animation: dot 14s infinite } @keyframes dot { 0%,68% { opacity: 0 } 72%,92% { opacity: 1 } 100% { opacity: 0 } }
  @media (prefers-reduced-motion: reduce) { .draw { animation: none; stroke-dashoffset: 0 } .dot { animation: none } }
</style>"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Single-line portrait of Eileen Jubilee</title>
  {anim}
  <rect width="{W}" height="{H}" fill="#FBF8F3"/>
  <circle class="{'dot' if animated else ''}" cx="470" cy="150" r="22" fill="#C4552C"/>
  <path d="{d}"{attrs} fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''


if __name__ == "__main__":
    for name, svg in [("03-pencil-sketch.svg", sketch()),
                      ("04-gestural-ink.svg", gestural()),
                      ("05-one-line.svg", continuous()),
                      ("05-one-line-animated.svg", continuous(animated=True))]:
        open(f"{OUT}/{name}", "w").write(svg)
        print(name, len(svg))
