"""Riso two-colour halftone, pixel art (with blink), and the botanical 'Polyculture' portrait.

Riso and pixel art are derived from a render of the clean flat portrait, so run
style_flat.py and render out/01-golden-hour.svg to out/p01.png first.
"""
import math
import random
from collections import Counter
from PIL import Image
import numpy as np
from geo import P, W, H, EYE_L, EYE_R, freckles, strands, sample, resample, lock_edges, pts_to_d
from style_lines import back_edges, strands_between

OUT = "out"


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float) / 255


# ---------------------------------------------------------------- riso

def riso(src="out/p01.png", ink_a="#D9532B", ink_b="#2E5D4F", cell=7.0):
    img = np.asarray(Image.open(src).convert("RGB"), dtype=float) / 255
    paper = hex2rgb("#F7F2E8")
    A, B = hex2rgb(ink_a), hex2rgb(ink_b)
    # every combination of the two ink densities, and the colour it prints
    steps = np.linspace(0, 1, 21)
    combos = np.array([(a, b) for a in steps for b in steps])
    printed = paper * (1 - combos[:, :1] * (1 - A)) * (1 - combos[:, 1:] * (1 - B))

    def density(x, y):
        x0, y0 = int(max(0, min(W - 1, x))), int(max(0, min(H - 1, y)))
        x1, y1 = min(W, x0 + 4), min(H, y0 + 4)
        c = img[max(0, y0 - 3):y1, max(0, x0 - 3):x1].reshape(-1, 3).mean(axis=0)
        # weight luminance more than hue so the faces read
        err = ((printed - c) ** 2 * np.array([1.0, 1.4, 0.8])).sum(axis=1)
        return combos[int(np.argmin(err))]

    def layer(angle, which, dx=0.0, dy=0.0):
        a = math.radians(angle)
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        R = int(math.hypot(W, H) / cell) + 2
        dots = []
        for i in range(-R, R):
            for j in range(-R, R):
                x = W / 2 + (i * ux + j * vx) * cell
                y = H / 2 + (i * uy + j * vy) * cell
                if not (-cell < x < W + cell and -cell < y < H + cell):
                    continue
                dens = density(x, y)[which]
                if dens < 0.04:
                    continue
                r = cell * 0.62 * math.sqrt(dens)
                dots.append(f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="{r:.2f}"/>')
        return "".join(dots)

    la = layer(15, 0)
    lb = layer(75, 1, dx=1.6, dy=-1.2)   # slightly off-register, like a real riso pass
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Two-colour risograph portrait of Eileen Jubilee</title>
  <defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.4  0 0 0 0 0.38  0 0 0 0 0.33  0 0 0 0.08 0"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="#F7F2E8"/>
  <g fill="{ink_a}" style="mix-blend-mode:multiply" opacity="0.92">{la}</g>
  <g fill="{ink_b}" style="mix-blend-mode:multiply" opacity="0.9">{lb}</g>
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
</svg>
'''


# ---------------------------------------------------------------- pixel art

PIX = 10  # canvas px per art pixel -> 60 x 75 grid


def pixel_grid(src="out/p01.png"):
    img = Image.open(src).convert("RGB")
    gw, gh = W // PIX, H // PIX
    grid = [[None] * gw for _ in range(gh)]
    px = img.load()
    for gy in range(gh):
        for gx in range(gw):
            cnt = Counter()
            for yy in range(gy * PIX + 1, gy * PIX + PIX - 1, 2):
                for xx in range(gx * PIX + 1, gx * PIX + PIX - 1, 2):
                    cnt[px[xx, yy]] += 1
            grid[gy][gx] = cnt.most_common(1)[0][0]
    return grid


def snap_palette(grid, palette):
    pal = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in palette]
    out = []
    for row in grid:
        r = []
        for c in row:
            best = min(pal, key=lambda p: sum((p[k] - c[k]) ** 2 for k in range(3)))
            r.append("#%02X%02X%02X" % best)
        out.append(r)
    return out


def pixel_art():
    palette = ["#FBF8F3", "#F3E2CC", "#C4552C", "#4E3122", "#6B4330", "#9A6440",
               "#F1CBAE", "#E2AE8F", "#CBD8E6", "#B3C4D7", "#9FB2C8", "#DDE6F0",
               "#2E5D4F", "#2E2219", "#D9968A", "#FAF4EC", "#7C7140", "#6E4A33", "#B5734C", "#C99070"]
    g = snap_palette(pixel_grid(), palette)
    gh, gw = len(g), len(g[0])
    SK, INK = "#F1CBAE", "#2E2219"

    def put(x, y, c):
        if 0 <= y < gh and 0 <= x < gw:
            g[y][x] = c

    # hand-placed eyes, 5 cells wide: white, iris, pupil, iris, white under a lash line
    open_eye, closed_eye = {}, {}
    for cx in (25, 34):                       # EYE_L / EYE_R at 10px cells
        cy = 32
        for dx in range(-3, 4):
            put(cx + dx, cy - 1, g[cy - 1][cx + dx] if abs(dx) == 3 else INK)
            put(cx + dx, cy, SK)
            put(cx + dx, cy + 1, SK)
        put(cx + (-3 if cx < 30 else 3), cy - 1, INK)          # outer lash flick
        for dx, c in zip(range(-2, 3), ["#FAF4EC", "#7C7140", "#22190F", "#7C7140", "#FAF4EC"]):
            put(cx + dx, cy, c)
        for dx in range(-3, 4):
            closed_eye[(cx + dx, cy - 1)] = SK
            closed_eye[(cx + dx, cy)] = INK if abs(dx) < 3 else SK
    # brows
    for cx in (25, 34):
        for dx in range(-3, 3):
            put(cx + dx + (0 if cx < 30 else 1), 29, SK)
            put(cx + dx + (0 if cx < 30 else 1), 30, SK)
        for dx in range(-2, 3):
            put(cx + dx, 29, "#6E4A33")
        put(cx + (-3 if cx < 30 else 3), 30, "#6E4A33")
    # nose and mouth
    put(31, 35, "#E2AE8F"); put(31, 36, "#E2AE8F"); put(31, 37, "#E2AE8F"); put(30, 38, "#E2AE8F")
    for dx in range(-2, 3):
        put(30 + dx, 42, "#D9968A")
    for dx in range(-1, 2):
        put(30 + dx, 43, "#E4A69A" if False else "#D9968A")
    # freckles: a sprinkle of darker skin pixels across nose and cheeks
    rng = random.Random(3)
    for _ in range(16):
        x = rng.randint(23, 37); y = rng.randint(34, 37)
        if g[y][x] == SK and not (29 <= x <= 31):
            put(x, y, "#E2AE8F" if rng.random() < 0.75 else "#C99070")

    def rects(grid, skip=None):
        out = []
        for y, row in enumerate(grid):
            x = 0
            while x < gw:
                c = row[x]
                x0 = x
                while x < gw and row[x] == c:
                    x += 1
                if c != skip:
                    out.append(f'<rect x="{x0*PIX}" y="{y*PIX}" width="{(x-x0)*PIX}" height="{PIX}" fill="{c}"/>')
        return "".join(out)

    base = rects(g)
    blink = "".join(f'<rect x="{x*PIX}" y="{y*PIX}" width="{PIX}" height="{PIX}" fill="{c}"/>' for (x, y), c in closed_eye.items())
    # sun twinkle frame: two pixels that pop on and off
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" aria-labelledby="t">
  <title id="t">Pixel-art portrait of Eileen Jubilee</title>
  <style>
    .blink {{ animation: blink 4.8s steps(1) infinite; opacity: 0 }}
    @keyframes blink {{ 0% {{ opacity: 0 }} 90% {{ opacity: 1 }} 93% {{ opacity: 0 }} 96% {{ opacity: 1 }} 98% {{ opacity: 0 }} }}
    .tw {{ animation: tw 1.6s steps(1) infinite }}
    @keyframes tw {{ 0% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink, .tw {{ animation: none }} .blink {{ opacity: 0 }} }}
  </style>
  {base}
  <g class="blink">{blink}</g>
  <g class="tw" fill="#C4552C"><rect x="510" y="110" width="10" height="10"/><rect x="420" y="180" width="10" height="10"/><rect x="520" y="190" width="10" height="10"/></g>
</svg>
'''


# ---------------------------------------------------------------- botanical

def leaf(x, y, ang, L, wdt, fill):
    """Almond leaf from (x,y) pointing along ang."""
    ex, ey = x + L * math.cos(ang), y + L * math.sin(ang)
    nx, ny = -math.sin(ang), math.cos(ang)
    mx, my = x + L * 0.5 * math.cos(ang), y + L * 0.5 * math.sin(ang)
    return (f'<path d="M{x:.1f},{y:.1f} Q{mx + nx*wdt:.1f},{my + ny*wdt:.1f} {ex:.1f},{ey:.1f} '
            f'Q{mx - nx*wdt:.1f},{my - ny*wdt:.1f} {x:.1f},{y:.1f} Z" fill="{fill}"/>')


def flower(x, y, r, petal, centre, rot):
    ps = "".join(
        f'<ellipse cx="{x + r*math.cos(rot + k*1.2566):.1f}" cy="{y + r*math.sin(rot + k*1.2566):.1f}" rx="{r*0.75:.1f}" ry="{r*0.45:.1f}" '
        f'transform="rotate({math.degrees(rot + k*1.2566):.0f} {x + r*math.cos(rot + k*1.2566):.1f} {y + r*math.sin(rot + k*1.2566):.1f})" fill="{petal}"/>'
        for k in range(5))
    return ps + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.45:.1f}" fill="{centre}"/>'


def polyculture(animated=False):
    rng = random.Random(14)
    INKC = "#1F3A33"
    greens = ["#2E5D4F", "#4F7F5F", "#7FA27A", "#A7B98A", "#3D6B4E"]
    stems, leaves, blooms = [], [], []

    vines = []
    for name, seed in [("lock_l", 71), ("lock_r", 72)]:
        vines += strands(name, count=14, seed=seed, wobble=3.0)
    bl, br = back_edges()
    _, ol = lock_edges("lock_l", 120); _, or_ = lock_edges("lock_r", 120)
    vines += strands_between(bl, ol, 6, 81, wobble_amp=3, start_max=0.3)
    vines += strands_between(br, or_, 6, 82, wobble_amp=3, start_max=0.3)
    # crown vines from the part
    for side in (-1, 1):
        for j in range(6):
            f = (j + 0.5) / 6
            x1 = 300 + side * (100 + 50 * f)
            vines.append(sample(f"M{300 + side*3},{150 + f*24} C{300 + side*55},{140 + f*20} {x1 - side*12},{190 + f*20} {x1},{262 + f*30}", step=4))

    for k, v in enumerate(vines):
        v = v[::2] if len(v) > 60 else v
        delay = rng.uniform(0, 2.5)
        cls = f' class="grow" style="animation-delay:{delay:.2f}s"' if animated else ""
        plen = ' pathLength="1"' if animated else ""
        stems.append(f'<path d="{pts_to_d(v)}" stroke="{INKC}" stroke-width="{rng.uniform(1.1, 1.8):.2f}"{plen}{cls}/>')
        side = 1
        i = rng.randint(2, 6)
        while i < len(v) - 2:
            x, y = v[i]
            x2, y2 = v[i + 1]
            ang = math.atan2(y2 - y, x2 - x) + side * rng.uniform(0.6, 1.1)
            L = rng.uniform(11, 20)
            lcls = f' class="pop" style="animation-delay:{delay + 0.8 + i/len(v)*2.2:.2f}s;transform-origin:{x:.0f}px {y:.0f}px"' if animated else ""
            leaves.append(f'<g{lcls}>' + leaf(x, y, ang, L, L * 0.32, rng.choice(greens)) + "</g>")
            side *= -1
            i += rng.randint(2, 4)
        if rng.random() < 0.55:
            j = rng.randint(len(v) // 4, len(v) - 3)
            x, y = v[j]
            fcls = f' class="pop" style="animation-delay:{delay + 2.6:.2f}s;transform-origin:{x:.0f}px {y:.0f}px"' if animated else ""
            blooms.append(f'<g{fcls}>' + flower(x, y, rng.uniform(4.5, 7), rng.choice(["#C4552C", "#E08A5A", "#E6B54A", "#F2D7C2"]), "#F6E7C8", rng.uniform(0, 6)) + "</g>")

    face_dots, chest_dots = freckles(seed=7, n=90)
    fr = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.7:.2f}" opacity="{o:.2f}"/>' for x, y, r, o in face_dots + chest_dots)

    style = ""
    if animated:
        style = """<style>
  .grow { stroke-dasharray: 1; stroke-dashoffset: 1; animation: grow 3.2s ease-out forwards }
  @keyframes grow { to { stroke-dashoffset: 0 } }
  .pop { transform: scale(0); animation: pop .7s cubic-bezier(.3,1.6,.5,1) forwards }
  @keyframes pop { to { transform: scale(1) } }
  .sway { transform-origin: 300px 160px; animation: sway 9s ease-in-out 6s infinite }
  @keyframes sway { 0%,100% { transform: rotate(0) } 50% { transform: rotate(.6deg) } }
  @media (prefers-reduced-motion: reduce) { .grow { animation: none; stroke-dashoffset: 0 } .pop { animation: none; transform: none } .sway { animation: none } }
</style>"""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Botanical portrait of Eileen Jubilee, her hair drawn as a polyculture of vines</title>
  {style}
  <defs><mask id="notBody"><rect width="{W}" height="{H}" fill="#fff"/><path d="{P['face']}" fill="#000"/><path d="{P['neck']}" fill="#000"/><path d="{P['shirt']}" fill="#000"/></mask></defs>
  <rect width="{W}" height="{H}" fill="#FBF8F3"/>
  <circle cx="300" cy="330" r="245" fill="#F1EADB"/>
  <path d="{P['shirt']}" fill="#E3EBF2"/>
  <path d="{P['v_skin']}" fill="#F7E3D2"/>
  <path d="{P['neck']}" fill="#F7E3D2"/>
  <path d="{P['face']}" fill="#F7E3D2"/>
  <g fill="none" stroke="{INKC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="{P['face']}"/>
    <path d="M262,458 L260,546"/><path d="M338,458 L340,546"/>
    <path d="M40,750 C52,640 125,588 232,556 L264,532"/><path d="M336,532 L368,556 C475,588 548,640 560,750"/>
    <path d="{P['collar_l']}"/><path d="{P['collar_r']}"/><path d="{P['placket']}"/>
    <path d="{P['brow_l']}" stroke-width="3"/><path d="{P['brow_r']}" stroke-width="3"/>
    <path d="{P['lid_l']}" stroke-width="2.6"/><path d="{P['lid_r']}" stroke-width="2.6"/>
    <path d="{P['lower_l']}" stroke-width="1.2"/><path d="{P['lower_r']}" stroke-width="1.2"/>
    <path d="{P['nose']}"/><path d="{P['nose_base']}"/>
    <path d="{P['mouth']}"/><path d="M276,430 Q300,444 324,430" stroke-width="1.3"/>
    <path d="{P['chain_l']}" stroke-width="1.2" stroke-dasharray="1 4"/><path d="{P['chain_r']}" stroke-width="1.2" stroke-dasharray="1 4"/>
  </g>
  <circle cx="{EYE_L[0]}" cy="{EYE_L[1]}" r="5" fill="{INKC}"/><circle cx="{EYE_R[0]}" cy="{EYE_R[1]}" r="5" fill="{INKC}"/>
  <!-- the pendant becomes a seed -->
  <path d="{P['pendant']}" fill="#2E5D4F" stroke="{INKC}" stroke-width="1.5"/>
  <path d="M303,654 C306,670 306,688 303,700" stroke="#A7B98A" stroke-width="1.2" fill="none"/>
  <g fill="#C4552C">{fr}</g>
  <g fill="#B98A62" opacity="0.22">
    <path d="{P['hair_back']}" mask="url(#notBody)"/>
    <path d="{P['lock_l']}"/><path d="{P['lock_r']}"/><path d="{P['hairline']}"/>
  </g>
  <g class="sway">
    <g fill="none" stroke-linecap="round">{"".join(stems)}</g>
    <g>{"".join(leaves)}</g>
    <g>{"".join(blooms)}</g>
  </g>
</svg>
'''


if __name__ == "__main__":
    for name, svg in [("06-riso.svg", riso()),
                      ("07-pixel.svg", pixel_art()),
                      ("08-polyculture.svg", polyculture()),
                      ("08-polyculture-animated.svg", polyculture(animated=True))]:
        open(f"{OUT}/{name}", "w").write(svg)
        print(name, len(svg))
