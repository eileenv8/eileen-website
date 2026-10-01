"""Two flat-vector portraits: 'Golden Hour' (clean) and 'Golden Hour, detailed'."""
import math
import random
import os
from geo import P, W, H, STRANDS_LIGHT, STRANDS_DARK, EYE_L, EYE_R, freckles, strands, sample, pts_to_d

OUT = "out"
os.makedirs(OUT, exist_ok=True)

PAPER = "#FBF8F3"; GLOW = "#F3E2CC"; SUN = "#C4552C"
SKIN = "#F1CBAE"; SKIN_SHADE = "#E2AE8F"
HAIR_DARK = "#4E3122"; HAIR = "#6B4330"; HAIR_LIGHT = "#9A6440"
SHIRT = "#CBD8E6"; SHIRT_SHADE = "#B3C4D7"; SHIRT_LINE = "#9FB2C8"
GREEN = "#2E5D4F"; INK = "#2E2219"


def flyaway_paths(seed=11, n=6, spread=35, hmin=12, hmax=30):
    """Loose single hairs lifting off the crown and drifting outward."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        side = rng.choice([-1, 1])
        a = rng.uniform(0.15, 1.0)          # how far from the part
        x0 = 300 + side * a * 105
        y0 = 175 - 38 * (1 - a * a) + rng.uniform(0, 6)
        L = rng.uniform(hmin, hmax) * 1.6
        dx = side * (L * rng.uniform(0.5, 0.9) + spread * 0.2)
        dy = -L * rng.uniform(0.25, 0.6)
        out.append(f'M{x0:.0f},{y0:.0f} C{x0+dx*0.4:.0f},{y0+dy*0.9:.0f} {x0+dx*0.8:.0f},{y0+dy:.0f} {x0+dx:.0f},{y0+dy*0.6:.0f}')
    return out


def eyes_basic():
    s = []
    for (cx, cy), eye, lid, crease, lower in [
        (EYE_L, "eye_l", "lid_l", "crease_l", "lower_l"),
        (EYE_R, "eye_r", "lid_r", "crease_r", "lower_r"),
    ]:
        cid = eye.replace("_", "")
        s.append(f'<clipPath id="{cid}"><path d="{P[eye]}"/></clipPath>')
        s.append(f'<path d="{P[eye]}" fill="#FAF4EC"/>')
        s.append(f'<g clip-path="url(#{cid})" class="iris"><circle cx="{cx}" cy="{cy}" r="10" fill="#7C7140"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="4.2" fill="#22190F"/><circle cx="{cx+3}" cy="{cy-3.5}" r="1.8" fill="#FFF"/></g>')
        s.append(f'<path d="{P[lid]}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
        s.append(f'<path d="{P[crease]}" fill="none" stroke="#C99376" stroke-width="1.6" stroke-linecap="round"/>')
        s.append(f'<path d="{P[lower]}" fill="none" stroke="#D9A88C" stroke-width="1.4" stroke-linecap="round"/>')
    return "\n".join(s)


def golden_hour(animated=False):
    face_dots, chest_dots = freckles()
    fr = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" opacity="{o:.2f}"/>' for x, y, r, o in face_dots)
    frc = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" opacity="{o:.2f}"/>' for x, y, r, o in chest_dots)
    fly = "".join(f'<path d="{d}"/>' for d in flyaway_paths())
    light = "".join(f'<path d="{d}"/>' for d in STRANDS_LIGHT)
    dark = "".join(f'<path d="{d}"/>' for d in STRANDS_DARK)

    style = ""
    lids = ""
    if animated:
        # blink: closed-lid shapes fade in for a beat every 5.5s; hair sways; sun breathes
        style = """<style>
  .blink { animation: blink 5.5s infinite; opacity: 0 }
  @keyframes blink { 0%, 91%, 97%, 100% { opacity: 0 } 93%, 95% { opacity: 1 } }
  .sway-l { transform-origin: 300px 170px; animation: swayl 7s ease-in-out infinite }
  .sway-r { transform-origin: 300px 170px; animation: swayr 7s ease-in-out infinite }
  @keyframes swayl { 0%,100% { transform: rotate(0deg) } 50% { transform: rotate(0.9deg) } }
  @keyframes swayr { 0%,100% { transform: rotate(0deg) } 50% { transform: rotate(-0.7deg) } }
  .sun { transform-origin: 470px 150px; animation: sun 9s ease-in-out infinite }
  @keyframes sun { 0%,100% { transform: translateY(0) scale(1) } 50% { transform: translateY(-8px) scale(1.04) } }
  .fly { animation: fly 4s ease-in-out infinite alternate; transform-origin: 300px 170px }
  @keyframes fly { to { transform: translateY(-3px) rotate(1.5deg) } }
  @media (prefers-reduced-motion: reduce) { .blink, .sway-l, .sway-r, .sun, .fly { animation: none } }
</style>"""
        # closed eyes: skin-coloured lids covering the eye, with a soft lash line
        lids = f'''<g class="blink">
    <path d="M224,327 Q255,310 286,327 Q255,341 224,327 Z" fill="{SKIN}"/>
    <path d="M314,327 Q345,310 376,327 Q345,341 314,327 Z" fill="{SKIN}"/>
    <path d="M226,330 Q255,342 284,330" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M316,330 Q345,342 374,330" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Illustrated portrait of Eileen Jubilee</title>
  {style}
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <path d="M80,750 L80,300 A220,220 0 0 1 520,300 L520,750 Z" fill="{GLOW}"/>
  <circle class="sun" cx="470" cy="150" r="34" fill="{SUN}"/>
  <path fill="{HAIR_DARK}" d="{P['hair_back']}"/>
  <path fill="{SKIN}" d="{P['neck']}"/>
  <path fill="{SKIN_SHADE}" d="{P['chin_shadow']}" opacity="0.55"/>
  <path fill="{SHIRT}" d="{P['shirt']}"/>
  <path fill="{SHIRT_SHADE}" d="{P['shirt_shade']}" opacity="0.7"/>
  <path fill="{SKIN}" d="{P['v_skin']}"/>
  <g fill="#B5734C">{frc}</g>
  <g fill="#DDE6F0" stroke="{SHIRT_LINE}" stroke-width="2" stroke-linejoin="round">
    <path d="{P['collar_l']}"/><path d="{P['collar_r']}"/>
  </g>
  <path d="{P['placket']}" stroke="{SHIRT_LINE}" stroke-width="2"/>
  <circle cx="300" cy="732" r="5" fill="#F6F2EA" stroke="{SHIRT_LINE}" stroke-width="1.5"/>
  <g fill="none" stroke="#6F6A62" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="1 5">
    <path d="{P['chain_l']}"/><path d="{P['chain_r']}"/>
  </g>
  <circle cx="303" cy="645" r="5.5" fill="none" stroke="#6F6A62" stroke-width="2.4"/>
  <path fill="{GREEN}" d="{P['pendant']}"/>
  <path fill="#5E9A78" d="{P['pendant_hi']}" opacity="0.8"/>
  <path fill="{SKIN}" d="{P['face']}"/>
  <path fill="{SKIN_SHADE}" d="{P['face_shade']}" opacity="0.35"/>
  <ellipse cx="243" cy="382" rx="26" ry="15" fill="#EBA48C" opacity="0.28"/>
  <ellipse cx="357" cy="382" rx="26" ry="15" fill="#EBA48C" opacity="0.28"/>
  <g fill="#B5734C">{fr}</g>
  <g fill="none" stroke="#6E4A33" stroke-width="6" stroke-linecap="round">
    <path d="{P['brow_l']}"/><path d="{P['brow_r']}"/>
  </g>
  {eyes_basic()}
  {lids}
  <g fill="none" stroke="#C3896B" stroke-width="2.4" stroke-linecap="round">
    <path d="{P['nose']}"/><path d="{P['nose_base']}"/>
  </g>
  <path fill="#D9968A" d="{P['lip_upper']}"/>
  <path fill="#E4A69A" d="{P['lip_lower']}"/>
  <path d="{P['mouth']}" fill="none" stroke="#A9625A" stroke-width="2" stroke-linecap="round"/>
  <g class="sway-l"><path fill="{HAIR}" d="{P['lock_l']}"/></g>
  <g class="sway-r"><path fill="{HAIR}" d="{P['lock_r']}"/></g>
  <path fill="{HAIR}" d="{P['hairline']}"/>
  <g fill="none" stroke="{HAIR_LIGHT}" stroke-width="3" stroke-linecap="round" opacity="0.75">{light}</g>
  <g fill="none" stroke="{HAIR_DARK}" stroke-width="2.4" stroke-linecap="round" opacity="0.6">{dark}</g>
  <g class="fly" fill="none" stroke="{HAIR_LIGHT}" stroke-width="1.1" stroke-linecap="round" opacity="0.45">{fly}</g>
</svg>
'''


# ---------------------------------------------------------------- detailed

HAIR_BACK_LOW = P["hair_back"].replace("M300,128 C215,128 165,185 156,262", "M300,174 C236,168 170,190 156,262").replace(
    "C435,185 385,128 300,128 Z", "C430,190 364,168 300,174 Z")


def chain_links(d, every=5.2):
    pts = sample(d, step=every)
    out = []
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        rx = 3.3 if i % 2 == 0 else 2.6
        out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="1.9" transform="rotate({ang:.0f} {cx:.1f} {cy:.1f})"/>')
    return "".join(out)


def brow_hairs(d, seed, n=34):
    rng = random.Random(seed)
    pts = sample(d, n=n)
    out = []
    for i, (x, y) in enumerate(pts[:-1]):
        # hairs lean outward and up along the arch; thicker toward the inner end
        t = i / n
        nx, ny = pts[i + 1]
        ang = math.atan2(ny - y, nx - x) - 0.55
        L = 7 + 3 * math.sin(math.pi * t) + rng.uniform(-1.5, 1.5)
        x0 = x + rng.uniform(-1.5, 1.5); y0 = y + 2.6 * (1 - t) + rng.uniform(-1.2, 1.2)
        out.append(f'<path d="M{x0:.1f},{y0:.1f} l{L*math.cos(ang):.1f},{L*math.sin(ang):.1f}" stroke-width="{1.4 + 1.2*(1-t):.1f}"/>')
    return "".join(out)


def lashes(lid_d, side, n=12):
    pts = sample(lid_d, n=n)
    out = []
    for i, (x, y) in enumerate(pts[2:-1], start=2):
        t = i / n
        # outer lashes are longer and sweep outward
        outward = t if side == "r" else 1 - t
        L = 3 + 5 * outward
        ang = -math.pi / 2 + (0.9 * outward if side == "r" else -0.9 * outward)
        out.append(f'<path d="M{x:.1f},{y:.1f} q{L*0.3*math.cos(ang):.1f},{L*0.8*math.sin(ang):.1f} {L*math.cos(ang):.1f},{L*math.sin(ang):.1f}"/>')
    return "".join(out)


def detailed(animated=False):
    rng = random.Random(21)
    face_dots, chest_dots = freckles(seed=7, n=210)
    tones = ["#B5734C", "#A86644", "#C2875F"]
    fr = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.9:.2f}" fill="{tones[i%3]}" opacity="{o:.2f}"/>'
                 for i, (x, y, r, o) in enumerate(face_dots))
    frc = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{tones[i%3]}" opacity="{o:.2f}"/>'
                  for i, (x, y, r, o) in enumerate(chest_dots))

    def strand_svg(name, count, seed, colors, wmin, wmax):
        s = []
        for k, line in enumerate(strands(name, count=count, seed=seed)):
            c = colors[k % len(colors)]
            w = rng.uniform(wmin, wmax)
            o = rng.uniform(0.35, 0.8)
            s.append(f'<path d="{pts_to_d(line[::3])}" stroke="{c}" stroke-width="{w:.2f}" opacity="{o:.2f}"/>')
        return "".join(s)

    hair_cols = ["#3E2519", "#8C5A3A", "#A86E45", "#5A3826", "#B97C4E"]
    strands_l = strand_svg("lock_l", 46, 4, hair_cols, 0.7, 2.2)
    strands_r = strand_svg("lock_r", 46, 5, hair_cols, 0.7, 2.2)
    fly = "".join(f'<path d="{d}"/>' for d in flyaway_paths(seed=12, n=14, spread=45, hmin=10, hmax=38))

    # eye irises with radial fibres
    def iris(cx, cy, cid):
        fib = "".join(
            f'<path d="M{cx + 4.6*math.cos(a):.1f},{cy + 4.6*math.sin(a):.1f} L{cx + 9.4*math.cos(a):.1f},{cy + 9.4*math.sin(a):.1f}"/>'
            for a in [i * math.pi / 14 for i in range(28)])
        return (f'<g clip-path="url(#{cid})">'
                f'<circle cx="{cx}" cy="{cy}" r="10.4" fill="url(#irisG)"/>'
                f'<g stroke="#5C5A2E" stroke-width="0.6" opacity="0.55">{fib}</g>'
                f'<circle cx="{cx}" cy="{cy}" r="10.4" fill="none" stroke="#3B3420" stroke-width="1.3"/>'
                f'<circle cx="{cx}" cy="{cy}" r="4.3" fill="#1C140C"/>'
                f'<circle cx="{cx+3.2}" cy="{cy-3.6}" r="2" fill="#FFF"/>'
                f'<circle cx="{cx-3}" cy="{cy+3.4}" r="0.9" fill="#FFF" opacity="0.7"/>'
                f'<path d="M{cx-16},{cy-9} Q{cx},{cy-3} {cx+16},{cy-9} L{cx+16},{cy-16} L{cx-16},{cy-16} Z" fill="#6B4A36" opacity="0.18"/>'
                f'</g>')

    style = ""
    blink = ""
    sway_l = sway_r = fog_cls = ""
    if animated:
        style = """<style>
  .blink { animation: blink 6s infinite; opacity: 0 }
  @keyframes blink { 0%, 92%, 97%, 100% { opacity: 0 } 93.5%, 95.5% { opacity: 1 } }
  .sway-l { transform-origin: 300px 170px; animation: swayl 8s ease-in-out infinite }
  .sway-r { transform-origin: 300px 170px; animation: swayr 8s ease-in-out infinite }
  @keyframes swayl { 0%,100% { transform: rotate(0) } 50% { transform: rotate(0.8deg) } }
  @keyframes swayr { 0%,100% { transform: rotate(0) } 50% { transform: rotate(-0.6deg) } }
  .fog1 { animation: fog 26s linear infinite } .fog2 { animation: fog 38s linear infinite reverse }
  @keyframes fog { from { transform: translateX(-60px) } 50% { transform: translateX(60px) } to { transform: translateX(-60px) } }
  .fly { animation: fly 4s ease-in-out infinite alternate; transform-origin: 300px 170px }
  @keyframes fly { to { transform: translateY(-3px) rotate(1.4deg) } }
  @media (prefers-reduced-motion: reduce) { .blink, .sway-l, .sway-r, .fog1, .fog2, .fly { animation: none } }
</style>"""
        blink = f'''<g class="blink">
    <path d="M223,327 Q255,309 287,327 Q255,342 223,327 Z" fill="url(#skinG)"/>
    <path d="M313,327 Q345,309 377,327 Q345,342 313,327 Z" fill="url(#skinG)"/>
    <path d="M225,331 Q255,343 285,331" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M315,331 Q345,343 375,331" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  </g>'''
        sway_l, sway_r = ' class="sway-l"', ' class="sway-r"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Detailed illustrated portrait of Eileen Jubilee</title>
  {style}
  <defs>
    <linearGradient id="glowG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F6D9B4"/><stop offset="0.55" stop-color="#F3E2CC"/><stop offset="1" stop-color="#EFE6DA"/>
    </linearGradient>
    <radialGradient id="sunG" cx="0.4" cy="0.4" r="0.7">
      <stop offset="0" stop-color="#E07447"/><stop offset="1" stop-color="#B9481F"/>
    </radialGradient>
    <linearGradient id="hairBackG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3F2619"/><stop offset="0.6" stop-color="#4E3122"/><stop offset="1" stop-color="#6A4029"/>
    </linearGradient>
    <linearGradient id="lockG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5E3A28"/><stop offset="0.45" stop-color="#6E4531"/><stop offset="1" stop-color="#94603C"/>
    </linearGradient>
    <radialGradient id="skinG" cx="0.42" cy="0.42" r="0.65">
      <stop offset="0" stop-color="#F6D6BC"/><stop offset="0.7" stop-color="#F0C8AA"/><stop offset="1" stop-color="#E3B091"/>
    </radialGradient>
    <linearGradient id="neckG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#DDA685"/><stop offset="0.35" stop-color="#EEC4A6"/><stop offset="1" stop-color="#F1CBAE"/>
    </linearGradient>
    <linearGradient id="shirtG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#BFCEDF"/><stop offset="0.45" stop-color="#D3DEEA"/><stop offset="1" stop-color="#B5C6D9"/>
    </linearGradient>
    <radialGradient id="irisG" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#B49A4C"/><stop offset="0.45" stop-color="#857A42"/><stop offset="1" stop-color="#4E5530"/>
    </radialGradient>
    <linearGradient id="lipG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#CF8A80"/><stop offset="1" stop-color="#E4A79B"/>
    </linearGradient>
    <linearGradient id="stoneG" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#5FA07D"/><stop offset="0.5" stop-color="#2E6B52"/><stop offset="1" stop-color="#1D4537"/>
    </linearGradient>
    <clipPath id="archClip"><path d="M80,750 L80,300 A220,220 0 0 1 520,300 L520,750 Z"/></clipPath>
    <clipPath id="faceClip"><path d="{P['face']}"/></clipPath>
    <clipPath id="eyel"><path d="{P['eye_l']}"/></clipPath>
    <clipPath id="eyer"><path d="{P['eye_r']}"/></clipPath>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="table" tableValues="0 0.07"/></feComponentTransfer>
      <feComposite in2="SourceGraphic" operator="in"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <path d="M80,750 L80,300 A220,220 0 0 1 520,300 L520,750 Z" fill="url(#glowG)"/>
  <g clip-path="url(#archClip)"><g class="fog1" opacity="0.55">
    <path d="M80,250 C140,236 200,262 270,248 C320,238 360,256 420,246" stroke="#FFFFFF" stroke-width="10" fill="none" stroke-linecap="round"/>
  </g>
  <g class="fog2" opacity="0.4">
    <path d="M160,212 C220,200 280,222 350,208 C400,200 450,214 500,206" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linecap="round"/>
  </g></g>
  <circle cx="470" cy="150" r="34" fill="url(#sunG)"/>
  <circle cx="470" cy="150" r="44" fill="none" stroke="#C4552C" stroke-width="1.2" opacity="0.35" stroke-dasharray="2 6"/>

  <!-- hair behind -->
  <path fill="url(#hairBackG)" d="{HAIR_BACK_LOW}"/>

  <!-- neck and chest -->
  <path fill="url(#neckG)" d="{P['neck']}"/>
  <path fill="#D49D7E" d="{P['chin_shadow']}" opacity="0.45"/>
  <path d="M276,468 C278,500 280,520 278,548" stroke="#DCA486" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M324,468 C322,500 320,520 322,548" stroke="#DCA486" stroke-width="2" fill="none" opacity="0.5"/>

  <!-- shirt -->
  <path fill="url(#shirtG)" d="{P['shirt']}"/>
  <path fill="{SHIRT_SHADE}" d="{P['shirt_shade']}" opacity="0.6"/>
  <path fill="{SHIRT_SHADE}" d="{P['shirt_shade_l']}" opacity="0.35"/>
  <g fill="none" stroke="#A8BACE" stroke-width="1.6" stroke-linecap="round" opacity="0.8">
    <path d="M150,640 C170,670 180,710 178,750"/>
    <path d="M450,640 C432,672 424,710 426,750"/>
    <path d="M228,600 C236,640 240,690 236,750"/>
    <path d="M372,600 C366,640 362,690 366,750"/>
  </g>
  <path fill="url(#neckG)" d="{P['v_skin']}"/>
  <path d="M276,566 Q300,576 324,566" stroke="#DCA486" stroke-width="1.6" fill="none" opacity="0.6"/>
  <g>{frc}</g>
  <g fill="#E4ECF4" stroke="#94A8BF" stroke-width="1.8" stroke-linejoin="round">
    <path d="{P['collar_l']}"/><path d="{P['collar_r']}"/>
  </g>
  <g fill="none" stroke="#9FB2C8" stroke-width="0.9" stroke-dasharray="2.5 2.5">
    <path d="M266,534 L232,580 L268,601 L297,690"/>
    <path d="M334,534 L368,580 L332,601 L303,690"/>
  </g>
  <path d="M300,706 L300,750" stroke="#94A8BF" stroke-width="1.8"/>
  <path d="M306,706 L306,750" stroke="#A8BACE" stroke-width="1"/>
  <circle cx="300" cy="732" r="5.5" fill="#F6F2EA" stroke="#94A8BF" stroke-width="1.4"/>
  <circle cx="298.4" cy="732" r="0.9" fill="#94A8BF"/><circle cx="301.6" cy="732" r="0.9" fill="#94A8BF"/>

  <!-- necklace, sitting 6px lower -->
  <g transform="translate(0,6)">
  <g fill="none" stroke="#5F5A52" stroke-width="1.3">{chain_links(P['chain_l'])}{chain_links(P['chain_r'])}</g>
  <circle cx="303" cy="645" r="5.5" fill="none" stroke="#6F6A62" stroke-width="2.6"/>
  <circle cx="303" cy="645" r="5.5" fill="none" stroke="#C9C4BA" stroke-width="0.8"/>
  <path d="M303,649 C318,662 322,690 303,707 C284,690 288,662 303,649 Z" fill="#8F8A80"/>
  <path fill="url(#stoneG)" d="{P['pendant']}"/>
  <path d="M303,651 L303,704 M296,668 L310,668" stroke="#1D4537" stroke-width="0.7" opacity="0.5"/>
  <path fill="#A9D4BA" d="{P['pendant_hi']}" opacity="0.55"/>

  </g>

  <!-- face -->
  <path fill="url(#skinG)" d="{P['face']}"/>
  <g clip-path="url(#faceClip)">
    <path fill="#D9A283" d="{P['face_shade']}" opacity="0.28"/>
    <!-- temple shade under the hair -->
    <path d="M200,230 C230,215 260,205 300,203 C340,205 370,215 400,230 L400,200 L200,200 Z" fill="#C98E70" opacity="0.25"/>
    <!-- under-brow and socket shading -->
    <ellipse cx="255" cy="320" rx="34" ry="16" fill="#D9A283" opacity="0.22"/>
    <ellipse cx="345" cy="320" rx="34" ry="16" fill="#D9A283" opacity="0.22"/>
    <!-- nose side and tip -->
    <path d="M296,336 C294,360 288,378 286,390 C292,386 298,372 300,350 Z" fill="#D9A283" opacity="0.35"/>
    <ellipse cx="302" cy="383" rx="7" ry="5" fill="#FBE3D0" opacity="0.7"/>
    <!-- under-lip shadow and chin -->
    <ellipse cx="300" cy="452" rx="20" ry="6" fill="#D9A283" opacity="0.35"/>
    <ellipse cx="300" cy="461" rx="12" ry="4" fill="#FBE3D0" opacity="0.2"/>
    <!-- cheek warmth -->
    <ellipse cx="243" cy="382" rx="30" ry="17" fill="#EBA08A" opacity="0.3"/>
    <ellipse cx="357" cy="382" rx="30" ry="17" fill="#EBA08A" opacity="0.3"/>
    <!-- forehead light -->
    <ellipse cx="285" cy="252" rx="44" ry="24" fill="#FBE6D4" opacity="0.28"/>
  </g>
  <g>{fr}</g>

  <!-- brows, hair by hair -->
  <path d="{P['brow_l']}" stroke="#7A5038" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.45"/>
  <path d="{P['brow_r']}" stroke="#7A5038" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.45"/>
  <g stroke="#5E3C29" fill="none" stroke-linecap="round">{brow_hairs(P['brow_l'], 1)}{brow_hairs(P['brow_r'], 2)}</g>

  <!-- eyes -->
  <path d="{P['eye_l']}" fill="#F8F0E6"/><path d="{P['eye_r']}" fill="#F8F0E6"/>
  {iris(EYE_L[0], EYE_L[1], 'eyel')}
  {iris(EYE_R[0], EYE_R[1], 'eyer')}
  <g fill="none" stroke-linecap="round">
    <path d="{P['lid_l']}" stroke="{INK}" stroke-width="3.4"/><path d="{P['lid_r']}" stroke="{INK}" stroke-width="3.4"/>
    <path d="{P['crease_l']}" stroke="#BF8A6D" stroke-width="1.6"/><path d="{P['crease_r']}" stroke="#BF8A6D" stroke-width="1.6"/>
    <path d="{P['lower_l']}" stroke="#C8957A" stroke-width="1.3"/><path d="{P['lower_r']}" stroke="#C8957A" stroke-width="1.3"/>
  </g>
  <g fill="none" stroke="{INK}" stroke-width="1.2" stroke-linecap="round">{lashes(P['lid_l'], 'l')}{lashes(P['lid_r'], 'r')}</g>
  <circle cx="229" cy="329" r="1.6" fill="#E9B7A6"/><circle cx="371" cy="329" r="1.6" fill="#E9B7A6"/>
  {blink}

  <!-- nose -->
  <g fill="none" stroke="#C3896B" stroke-linecap="round">
    <path d="{P['nose']}" stroke-width="2.2"/>
    <path d="{P['nose_base']}" stroke-width="2.2"/>
  </g>
  <path d="M289,392 Q292,388 296,393 Q292,395 289,392 Z" fill="#B87A5E"/>
  <path d="M311,392 Q308,388 304,393 Q308,395 311,392 Z" fill="#B87A5E"/>

  <!-- mouth -->
  <path fill="url(#lipG)" d="{P['lip_upper']}"/>
  <path fill="#E6AA9E" d="{P['lip_lower']}"/>
  <ellipse cx="303" cy="433" rx="9" ry="2.4" fill="#F6CFC5" opacity="0.8"/>
  <path d="{P['mouth']}" fill="none" stroke="#A35C54" stroke-width="2" stroke-linecap="round"/>
  <path d="M294,410 Q300,414 306,410" fill="none" stroke="#D9A283" stroke-width="1.5" opacity="0.7"/>

  <!-- front locks with strand detail -->
  <g{sway_l}>
    <path fill="url(#lockG)" d="{P['lock_l']}"/>
    <g fill="none" stroke-linecap="round">{strands_l}</g>
  </g>
  <g{sway_r}>
    <path fill="url(#lockG)" d="{P['lock_r']}"/>
    <g fill="none" stroke-linecap="round">{strands_r}</g>
  </g>
  <path fill="#5E3A28" d="{P['hairline']}"/>
  <g fill="none" stroke="#A86E45" stroke-width="1.2" opacity="0.6" stroke-linecap="round">
    <path d="M298,178 C262,180 232,200 216,250"/><path d="M296,184 C270,188 244,206 226,244"/>
    <path d="M302,178 C338,180 368,200 384,250"/><path d="M304,184 C330,188 356,206 374,244"/>
  </g>

  <rect width="{W}" height="{H}" filter="url(#grain)" fill="#000"/>
</svg>
'''


if __name__ == "__main__":
    for name, svg in [
        ("01-golden-hour.svg", golden_hour()),
        ("01-golden-hour-animated.svg", golden_hour(animated=True)),
        ("02-golden-hour-detailed.svg", detailed()),
        ("02-golden-hour-detailed-animated.svg", detailed(animated=True)),
    ]:
        open(f"{OUT}/{name}", "w").write(svg)
        print(name, len(svg))
