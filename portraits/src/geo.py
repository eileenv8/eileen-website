"""Shared geometry for every portrait style.

All shapes live on a 600 x 750 canvas: front-facing, neutral pose, no bag strap.
Each style module imports these path strings so the likeness stays the same
from one style to the next. `sample()` turns any path into evenly spaced points,
which the sketchy and gestural styles redraw by hand-wobbled lines.
"""
import random
from svgpathtools import parse_path

W, H = 600, 750

P = {
    # hair behind the head and shoulders
    "hair_back": "M300,128 C215,128 165,185 156,262 C148,330 128,360 132,420 "
                 "C136,470 104,500 108,560 C112,610 90,650 100,700 C104,725 96,740 92,750 L508,750 "
                 "C504,740 496,725 500,700 C510,650 488,610 492,560 C496,500 464,470 468,420 "
                 "C472,360 452,330 444,262 C435,185 385,128 300,128 Z",
    "neck": "M264,425 L260,560 L340,560 L336,425 Z",
    "chin_shadow": "M263,430 C282,476 318,476 337,430 L337,470 C318,492 282,492 263,470 Z",
    "shirt": "M40,750 C52,640 125,588 232,556 L264,532 L336,532 L368,556 C475,588 548,640 560,750 Z",
    "shirt_shade": "M420,600 C490,630 540,680 552,750 L470,750 C468,690 450,640 420,600 Z",
    "shirt_shade_l": "M180,600 C110,630 60,680 48,750 L130,750 C132,690 150,640 180,600 Z",
    "v_skin": "M262,530 L300,705 L338,530 Z",
    "collar_l": "M266,526 L224,580 L266,606 L300,706 Z",
    "collar_r": "M334,526 L376,580 L334,606 L300,706 Z",
    "placket": "M300,706 L300,750",
    "chain_l": "M268,520 Q282,600 302,640",
    "chain_r": "M332,520 Q322,600 304,640",
    "pendant": "M303,651 C316,664 320,688 303,704 C286,688 290,664 303,651 Z",
    "pendant_hi": "M298,664 C301,672 301,684 299,692 C294,684 294,672 298,664 Z",
    "face": "M300,198 C352,198 393,228 395,300 C397,362 380,410 346,448 "
            "C329,465 314,472 300,472 C286,472 271,465 254,448 C220,410 203,362 205,300 "
            "C207,228 248,198 300,198 Z",
    "face_shade": "M300,198 C352,198 393,228 395,300 C397,362 380,410 346,448 "
                  "C329,465 314,472 300,472 C330,440 352,400 356,340 C360,270 340,215 300,198 Z",
    "brow_l": "M221,301 Q248,289 282,296",
    "brow_r": "M318,296 Q352,289 379,301",
    "eye_l": "M227,328 Q255,311 283,328 Q255,340 227,328 Z",
    "eye_r": "M317,328 Q345,311 373,328 Q345,340 317,328 Z",
    "lid_l": "M225,329 Q255,309 285,327",
    "lid_r": "M315,327 Q345,309 375,329",
    "crease_l": "M231,316 Q255,304 281,315",
    "crease_r": "M319,315 Q345,304 369,316",
    "lower_l": "M233,334 Q255,341 279,333",
    "lower_r": "M321,333 Q345,341 367,334",
    "nose": "M304,334 C306,358 312,376 314,388",
    "nose_base": "M286,392 Q300,401 314,392",
    "lip_upper": "M268,424 Q284,416 300,420 Q316,416 332,424 Q300,431 268,424 Z",
    "lip_lower": "M271,425 Q300,446 329,425 Q300,432 271,425 Z",
    # neutral mouth: a level line, only the faintest lift at the corners
    "mouth": "M268,424 Q300,431 332,424",
    "lock_l": "M300,170 C246,168 200,196 192,262 C186,312 202,350 194,398 "
              "C186,446 160,470 168,524 C176,578 150,606 156,660 C160,700 146,724 160,750 L112,750 "
              "C98,716 120,690 112,648 C104,598 132,566 124,512 C116,458 148,430 144,380 "
              "C140,330 132,290 152,238 C174,184 236,162 300,170 Z",
    "lock_r": "M300,170 C356,166 404,196 410,262 C416,312 398,350 408,398 "
              "C418,446 444,470 434,524 C424,578 452,606 444,660 C438,700 456,724 440,750 L492,750 "
              "C506,716 482,690 490,648 C498,598 470,566 478,512 C486,458 454,430 458,380 "
              "C462,330 470,290 448,238 C426,184 362,162 300,170 Z",
    "hairline": "M300,170 C258,168 218,190 206,258 L214,266 C226,222 258,200 298,196 "
                "L300,186 L302,196 C342,200 374,222 386,266 L394,258 C382,190 342,168 300,170 Z",
}

# flowing strands through the hair (open paths), used for highlights and line styles
STRANDS_LIGHT = [
    "M172,262 C166,320 180,350 170,400 C160,450 136,476 146,526 C156,576 130,604 136,656 C140,696 128,716 138,742",
    "M198,250 C192,300 206,340 198,392 C190,440 166,466 174,516",
    "M428,262 C434,320 420,350 430,400 C440,450 464,476 454,526 C444,576 470,604 464,656 C460,696 472,716 462,742",
    "M402,250 C408,300 394,340 402,392 C410,440 434,466 426,516",
]
STRANDS_DARK = [
    "M156,300 C148,350 162,390 150,440 C138,490 112,520 120,570 C126,620 104,650 112,700",
    "M444,300 C452,350 438,390 450,440 C462,490 488,520 480,570 C474,620 496,650 488,700",
]

EYE_L = (256, 327)
EYE_R = (344, 327)
IRIS_R = 10


def sample(d, n=None, step=6.0):
    """Evenly spaced points along path `d` (by arc length)."""
    path = parse_path(d)
    length = path.length()
    if n is None:
        n = max(2, int(length / step))
    pts = []
    for i in range(n + 1):
        t = path.ilength(length * i / n) if 0 < i < n else (0 if i == 0 else 1)
        z = path.point(t)
        pts.append((z.real, z.imag))
    return pts


def freckles(seed=7, n=140):
    """Seeded freckle positions (x, y, r, opacity) across nose, cheeks and forehead."""
    rng = random.Random(seed)
    dots = []
    tries = 0
    while len(dots) < n and tries < 6000:
        tries += 1
        x = rng.uniform(215, 385)
        y = rng.uniform(250, 420)
        if ((x - 300) / 92) ** 2 + ((y - 345) / 110) ** 2 > 1:
            continue
        if abs(y - 327) < 14 and (225 < x < 287 or 313 < x < 375):
            continue
        if abs(y - 296) < 8 and (219 < x < 284 or 316 < x < 381):
            continue
        if 412 < y and 262 < x < 338:
            continue
        weight = 1.0 if 340 < y < 405 else 0.45
        if rng.random() > weight:
            continue
        dots.append((x, y, rng.uniform(0.9, 2.1), rng.uniform(0.45, 0.85)))
    chest = []
    for _ in range(30):
        x = rng.uniform(272, 328)
        y = rng.uniform(550, 650)
        if abs(x - 300) > (700 - y) * 0.22:
            continue
        chest.append((x, y, rng.uniform(0.8, 1.6), rng.uniform(0.35, 0.6)))
    return dots, chest


def resample(pts, n):
    """Re-space a polyline to n+1 points by arc length."""
    import math
    seg = [0.0]
    for a, b in zip(pts, pts[1:]):
        seg.append(seg[-1] + math.dist(a, b))
    total = seg[-1]
    out, j = [], 0
    for i in range(n + 1):
        s = total * i / n
        while j < len(seg) - 2 and seg[j + 1] < s:
            j += 1
        a, b = pts[j], pts[j + 1]
        span = seg[j + 1] - seg[j] or 1
        t = (s - seg[j]) / span
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def lock_edges(name, n=120):
    """Split a hair lock outline into its inner and outer edges, both top-to-bottom."""
    pts = sample(P[name], step=2)
    # the two bottom corners sit on y=750; split there
    bottom = [i for i, p in enumerate(pts) if p[1] > 749.5]
    i0, i1 = bottom[0], bottom[-1]
    inner = pts[: i0 + 1]
    outer = list(reversed(pts[i1:]))
    return resample(inner, n), resample(outer, n)


def strands(name, count=24, seed=3, n=120, wobble=2.5):
    """Hair strands interpolated across a lock, top to bottom."""
    rng = random.Random(seed)
    inner, outer = lock_edges(name, n)
    out = []
    for k in range(count):
        f = (k + rng.uniform(0.2, 0.8)) / count
        start = int(rng.uniform(0, 0.15) * n)
        end = n - int(rng.uniform(0, 0.12) * n)
        ph = rng.uniform(0, 6.28)
        line = []
        for i in range(start, end + 1):
            a, b = inner[i], outer[i]
            import math
            w = wobble * math.sin(i / 9 + ph)
            line.append((a[0] + (b[0] - a[0]) * f + w, a[1] + (b[1] - a[1]) * f))
        out.append(line)
    return out


def pts_to_d(pts, closed=False):
    """Smooth path through points (Catmull-Rom converted to cubic Beziers)."""
    if len(pts) < 2:
        return ""
    if closed:
        pts = pts + pts[:3]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")
