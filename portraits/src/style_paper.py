"""Cut-paper collage portrait: every shape is a layer of paper casting a soft shadow."""
import random
from geo import P, W, H, EYE_L, EYE_R, freckles

OUT = "out"


def papercut():
    face_dots, chest_dots = freckles(seed=7, n=70)
    fr = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(r, 1.3):.2f}"/>' for x, y, r, o in face_dots + chest_dots)

    def cut(d, fill, depth=1, extra=""):
        return f'<path d="{d}" fill="{fill}" filter="url(#s{depth})"{extra}/>'

    def stroke_cut(d, w, fill, depth=1):
        # a strip of paper: draw the stroke as a thick line with the shadow filter
        return f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round" filter="url(#s{depth})"/>'

    arches = "".join(
        f'<path d="M{80 + i*34},750 L{80 + i*34},{300 + i*10} A{220 - i*34},{220 - i*34} 0 0 1 {520 - i*34},{300 + i*10} L{520 - i*34},750 Z" fill="{c}" filter="url(#s2)"/>'
        for i, c in enumerate(["#F0D6B8", "#EBC39D", "#E5AE84", "#DD9A6E"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Cut-paper collage portrait of Eileen Jubilee</title>
  <defs>
    <filter id="s1" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="1.5" stdDeviation="1.4" flood-color="#3A2618" flood-opacity="0.35"/></filter>
    <filter id="s2" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#3A2618" flood-opacity="0.3"/></filter>
    <filter id="s3" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="1" dy="5" stdDeviation="5" flood-color="#2A1A10" flood-opacity="0.38"/></filter>
    <filter id="fibre" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04 0.9" numOctaves="2" seed="6"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0.07 0"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="#F6EFE4"/>
  {arches}
  <circle cx="470" cy="150" r="34" fill="#C4552C" filter="url(#s2)"/>
  {cut(P['hair_back'], '#4A2E20', 3)}
  {cut(P['neck'], '#EDC3A4', 1)}
  {cut(P['shirt'], '#C6D4E3', 3)}
  {cut(P['shirt_shade'], '#B0C1D5', 1)}
  {cut(P['v_skin'], '#F1CBAE', 1)}
  <g fill="#C98663">{"".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.15"/>' for x, y, r, o in chest_dots)}</g>
  {cut(P['collar_l'], '#E3EAF2', 2)}{cut(P['collar_r'], '#E3EAF2', 2)}
  {stroke_cut(P['chain_l'], 2.2, '#8C877E', 1)}{stroke_cut(P['chain_r'], 2.2, '#8C877E', 1)}
  {cut(P['pendant'], '#2E5D4F', 2)}
  {cut(P['pendant_hi'], '#5E9A78', 1)}
  {cut(P['face'], '#F1CBAE', 3)}
  {cut(P['face_shade'], '#E8B796', 1)}
  <ellipse cx="243" cy="382" rx="20" ry="10" fill="#F2B6A0" filter="url(#s1)"/>
  <ellipse cx="357" cy="382" rx="20" ry="10" fill="#F2B6A0" filter="url(#s1)"/>
  <g fill="#B5734C" filter="url(#s1)">{"".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.15"/>' for x, y, r, o in face_dots)}</g>
  {stroke_cut(P['brow_l'], 7, '#6E4A33', 1)}{stroke_cut(P['brow_r'], 7, '#6E4A33', 1)}
  {cut(P['eye_l'], '#FAF4EC', 1)}{cut(P['eye_r'], '#FAF4EC', 1)}
  <clipPath id="el"><path d="{P['eye_l']}"/></clipPath><clipPath id="er"><path d="{P['eye_r']}"/></clipPath>
  <g clip-path="url(#el)"><circle cx="{EYE_L[0]}" cy="{EYE_L[1]}" r="10" fill="#7C7140"/><circle cx="{EYE_L[0]}" cy="{EYE_L[1]}" r="4.4" fill="#22190F"/></g>
  <g clip-path="url(#er)"><circle cx="{EYE_R[0]}" cy="{EYE_R[1]}" r="10" fill="#7C7140"/><circle cx="{EYE_R[0]}" cy="{EYE_R[1]}" r="4.4" fill="#22190F"/></g>
  {stroke_cut(P['lid_l'], 4, '#2E2219', 1)}{stroke_cut(P['lid_r'], 4, '#2E2219', 1)}
  {stroke_cut(P['nose'], 3, '#D79C7C', 1)}{stroke_cut(P['nose_base'], 3, '#D79C7C', 1)}
  {cut(P['lip_upper'], '#D48C80', 1)}{cut(P['lip_lower'], '#E3A498', 1)}
  {cut(P['lock_l'], '#6B4330', 3)}{cut(P['lock_r'], '#6B4330', 3)}
  {cut(P['hairline'], '#6B4330', 2)}
  <g fill="none" stroke="#8E5B3C" stroke-width="5" stroke-linecap="round" filter="url(#s1)">
    <path d="M178,280 C172,330 184,360 176,410 C168,460 146,486 154,536"/>
    <path d="M422,280 C428,330 416,360 424,410 C432,460 454,486 446,536"/>
    <path d="M140,560 C132,610 146,650 138,700"/>
    <path d="M462,560 C470,610 456,650 464,700"/>
  </g>
  <rect width="{W}" height="{H}" filter="url(#fibre)"/>
</svg>
'''


if __name__ == "__main__":
    svg = papercut()
    open(f"{OUT}/09-cut-paper.svg", "w").write(svg)
    print(len(svg))
