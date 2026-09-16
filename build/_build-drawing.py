#!/usr/bin/env python3
"""Build a line drawing of Big Ben Tower for the specification panel.

Everything drawn is derived from the catalogue's own isolated photograph:

  * the outer silhouette comes from the alpha cutout, simplified at the same
    tolerance as the hero silhouettes so the two read as one drawing system;
  * the internal edges are the boundaries between the product's flat-shaded
    faces, found by clustering luminance inside the product, tracing each face
    region and then discarding every segment that lies on the outer silhouette
    (so only true interior edges survive, each drawn once);
  * the A / B / C dimension arrows keep the catalogue's own convention --
    A across the top rear edge, B along the receding top edge, C overall
    height -- anchored to rim corners measured from the drawing itself.

Nothing is modelled or idealised, and no dimension value is drawn: the numbers
stay in the schedule table beside the drawing, with their source and
verification status. The panel keeps a "not to scale" note because the source
is a perspective photograph.
"""
import json
import numpy as np
from PIL import Image
from skimage import measure
from scipy import ndimage

SRC = "index-assets-cut/big-ben-tower.png"   # the alpha plate
S = 2                       # supersample for stable face segmentation
FACES = 4
MIN_REGION = 0.015
SIMPLIFY = 4.0              # native px; matches the hero silhouettes
MIN_EDGE = 0.085            # interior edge must span this share of the height
ON_OUTLINE = 4.5            # native px: closer than this counts as the outline


def trim_rgba(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)
    ys, xs = np.where(a[..., 3] > 8)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def polyline(contour, tol):
    return measure.approximate_polygon(contour, tolerance=tol)[:, ::-1]


def segs(poly):
    return [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]


def seg_len(s):
    return float(np.hypot(*(s[1] - s[0])))


def point_to_seg(p, s):
    a, b = s
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-9), 0, 1)
    return float(np.hypot(*(p - (a + t * ab))))


def near_outline(s, outline_segs):
    mids = [s[0] * f + s[1] * (1 - f) for f in (0.25, 0.5, 0.75)]
    return all(min(point_to_seg(m, o) for o in outline_segs) < ON_OUTLINE
               for m in mids)


def same_edge(s, t):
    d1 = max(point_to_seg(s[0], t), point_to_seg(s[1], t))
    d2 = max(point_to_seg(t[0], s), point_to_seg(t[1], s))
    return min(d1, d2) < 10.0


def faces(rgb, mask):
    lum = ndimage.median_filter(
        0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2], 5)
    v = lum[mask]
    ks = [v.min() + (v.max() - v.min()) * f for f in (.12, .38, .62, .88)]
    for _ in range(60):
        lab = np.abs(v[:, None] - np.array(ks)[None, :]).argmin(1)
        ks = [v[lab == i].mean() if (lab == i).any() else ks[i]
              for i in range(FACES)]
    ks = sorted(ks)
    bounds = [(ks[i] + ks[i + 1]) / 2 for i in range(FACES - 1)]
    seg = np.where(mask, np.digitize(lum, bounds), -1)
    out = []
    for i in range(FACES):
        r = ndimage.binary_closing(
            ndimage.binary_opening(seg == i, np.ones((7, 7))), np.ones((9, 9)))
        if r.sum() >= MIN_REGION * mask.sum():
            out.append(r)
    return out


def corners(poly):
    y0, y1 = poly[:, 1].min(), poly[:, 1].max()
    band = poly[poly[:, 1] <= y0 + (y1 - y0) * 0.18]
    return (band[band[:, 1].argmin()],
            band[band[:, 0].argmin()],
            band[band[:, 0].argmax()])


def main():
    rgba = trim_rgba(SRC)
    h, w, _ = rgba.shape

    # ---- outer silhouette, at native resolution
    alpha = np.pad(rgba[..., 3].astype(np.float32) / 255.0, 2)
    cs = sorted(measure.find_contours(alpha, 0.5), key=len, reverse=True)
    silhouette = polyline(cs[0], SIMPLIFY) - 2
    out_segs = segs(silhouette)

    # ---- interior edges, from the supersampled face segmentation
    big = np.asarray(Image.fromarray(rgba, "RGBA")
                     .resize((w * S, h * S), Image.LANCZOS)).astype(np.float32)
    mask = big[..., 3] > 200
    kept = []
    for r in faces(big[..., :3], mask):
        for c in measure.find_contours(np.pad(r.astype(float), 2), 0.5):
            if len(c) < 120:
                continue
            poly = (polyline(c, SIMPLIFY * S) - 2) / S
            for s in segs(poly):
                if seg_len(s) < MIN_EDGE * h:
                    continue
                if near_outline(s, out_segs):
                    continue
                if any(same_edge(s, k) for k in kept):
                    continue
                # Only edges the photograph resolves unambiguously are drawn:
                # the rim quad at the top, and the long corner where the front
                # face meets the side. The recessed slot between the legs is
                # in shadow and its edges cannot be recovered reliably at this
                # resolution, so it is left out rather than guessed at.
                # every kept edge must reach the rim: the rim quad itself and
                # the corner where the front face meets the side both start up
                # there, while the shadowed recess edges begin much lower
                if min(s[0][1], s[1][1]) > 0.32 * h or seg_len(s) < 0.13 * h:
                    continue
                kept.append(s)

    top, left, right = corners(silhouette)
    data = {
        "w": round(float(silhouette[:, 0].max()), 2),
        "h": round(float(silhouette[:, 1].max()), 2),
        "silhouette": "M" + " L".join(f"{x:.1f},{y:.1f}"
                                      for x, y in silhouette) + " Z",
        "edges": [f"M{s[0][0]:.1f},{s[0][1]:.1f} L{s[1][0]:.1f},{s[1][1]:.1f}"
                  for s in kept],
        "anchors": {"top": [round(float(top[0]), 1), round(float(top[1]), 1)],
                    "left": [round(float(left[0]), 1), round(float(left[1]), 1)],
                    "right": [round(float(right[0]), 1), round(float(right[1]), 1)],
                    "bottom": round(float(silhouette[:, 1].max()), 1),
                    "leftmost": round(float(silhouette[:, 0].min()), 1)},
    }
    json.dump(data, open("big-ben-drawing.json", "w"), indent=1)
    print(f"outline pts={len(silhouette)}  interior edges={len(kept)}")
    print("anchors", data["anchors"])


if __name__ == "__main__":
    main()
