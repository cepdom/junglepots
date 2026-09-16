#!/usr/bin/env python3
"""Trace product silhouettes out of the alpha cutouts into SVG paths.

The outline is derived from the actual catalogue photograph's alpha channel,
so it is a traced silhouette of the real object -- not a redrawn or modelled
approximation. Perspective from the original photograph is retained; these are
form studies, not orthographic elevations, and they are labelled as such.
"""
import json
import numpy as np
from PIL import Image
from skimage import measure

# Catalogue heights in cm, used only for RELATIVE sizing within the strip.
# Big Ben Tower's height is disputed in the source (99 vs 90); the strip
# carries no dimension labels and claims no scale, so the ambiguity is not
# surfaced as a number anywhere.
ITEMS = [
    ("big-ben-tower",  "Big Ben Tower",  "Stepped square tower", 99.0),
    ("tower-bridge",   "Tower Bridge",   "Square tower / arched base", 99.0),
    ("grand-wall",     "Grand Wall",     "Long planter / rounded ends", 74.0),
]

SIMPLIFY = 4.0     # Douglas-Peucker tolerance; these are prismatic objects,
                   # so a coarse tolerance recovers their true straight edges
MIN_LEN = 60       # drop contour fragments shorter than this


def trace(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[..., 3].astype(np.float32) / 255.0
    # pad so contours never run off the array edge
    a = np.pad(a, 2)
    ys, xs = np.where(a > 0.5)
    if len(ys) == 0:
        raise SystemExit("empty alpha in " + path)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()

    paths = []
    for c in measure.find_contours(a, 0.5):
        if len(c) < MIN_LEN:
            continue
        c = measure.approximate_polygon(c, tolerance=SIMPLIFY)
        if len(c) < 4:
            continue
        pts = [(round(float(p[1] - x0), 2), round(float(p[0] - y0), 2))
               for p in c]
        d = "M" + " L".join(f"{x},{y}" for x, y in pts) + " Z"
        paths.append({"d": d, "points": len(pts)})

    paths.sort(key=lambda p: -p["points"])
    return {"w": float(x1 - x0), "h": float(y1 - y0), "paths": paths}


if __name__ == "__main__":
    out = {}
    for slug, name, form, cm in ITEMS:
        t = trace(f"index-assets-cut/{slug}.png")
        t.update(name=name, form=form, cm=cm)
        out[slug] = t
        print(f"{slug:16s} box={t['w']:.0f}x{t['h']:.0f}  "
              f"contours={len(t['paths'])}  pts={[p['points'] for p in t['paths']]}")
    json.dump(out, open("silhouettes.json", "w"), indent=1)
