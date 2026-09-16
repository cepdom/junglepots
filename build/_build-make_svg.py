#!/usr/bin/env python3
"""Compose the Big Ben Tower specification drawing as inline SVG.

Dimension letters keep the catalogue's roles: A across the top rear edge,
B along the receding edge, C overall height. No numbers are drawn -- those
stay in the schedule table beside the drawing, with their source and
verification status.
"""
import json

d = json.load(open("big-ben-drawing.json"))
W, H, a = d["w"], d["h"], d["anchors"]

PAD_L, PAD_T, PAD_R, PAD_B = 104, 76, 44, 30
vw, vh = W + PAD_L + PAD_R, H + PAD_T + PAD_B

def T(p):
    return (p[0] + PAD_L, p[1] + PAD_T)

top, left, right = T(a["top"]), T(a["left"]), T(a["right"])
bottom = PAD_T + a["bottom"]
cx = PAD_L + a["leftmost"] - 58
OFF = 30                      # how far the A/B dimension lines sit off the rim

INK = "#232822"


def line(x1, y1, x2, y2):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{INK}" stroke-width="1.3" '
            f'vector-effect="non-scaling-stroke" '
            f'marker-start="url(#jp-ah)" marker-end="url(#jp-ah)"/>')


def label(x, y, t):
    return (f'<text x="{x:.0f}" y="{y:.0f}" class="dim-letter" '
            f'text-anchor="middle">{t}</text>')


p = [f'<svg class="spec-drawing" viewBox="0 0 {vw:.0f} {vh:.0f}" fill="none" '
     f'role="img" aria-label="Line drawing of Big Ben Tower traced from the '
     f'catalogue photograph, with A across the top rear edge, B along the '
     f'receding top edge and C as overall height">',
     '<defs><marker id="jp-ah" viewBox="0 0 10 10" refX="9" refY="5" '
     'markerUnits="userSpaceOnUse" markerWidth="15" markerHeight="15" '
     'orient="auto-start-reverse">'
     f'<path d="M0,1 L10,5 L0,9 z" fill="{INK}"/></marker></defs>',
     f'<g transform="translate({PAD_L},{PAD_T})">',
     f'<path class="dwg-out" d="{d["silhouette"]}" '
     f'vector-effect="non-scaling-stroke"/>',
     "</g>"]

p += [
    '<g class="dims">',
    line(top[0], top[1] - OFF, right[0], right[1] - OFF),
    line(top[0], top[1] - OFF, left[0], left[1] - OFF),
    line(cx, left[1], cx, bottom),
    label((top[0] + right[0]) / 2, (top[1] + right[1]) / 2 - OFF - 16, "A"),
    label((top[0] + left[0]) / 2, (top[1] + left[1]) / 2 - OFF - 16, "B"),
    label(cx - 20, (left[1] + bottom) / 2 + 9, "C"),
    "</g>",
    "</svg>",
]

svg = "\n".join(p)
open("big-ben-drawing.svg", "w").write(svg)

CSS = """
.spec-drawing{width:100%;height:auto;max-width:340px;overflow:visible}
.spec-drawing .dwg-out{stroke:#232822;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;fill:none}
.spec-drawing .dim-letter{font:400 27px Manrope,Arial,sans-serif;fill:#232822}
"""
open("big-ben-drawing.css", "w").write(CSS)

html = ('<body style="margin:0;background:#edebe4;display:grid;'
        'place-items:center;height:100vh">'
        '<style>' + CSS.replace("max-width:340px", "max-width:none")
        + '.spec-drawing{height:86vh;width:auto}</style>' + svg + "</body>")
open("/tmp/prev.html", "w").write(html)
print("viewBox", round(vw), round(vh), "edges", len(d["edges"]))
