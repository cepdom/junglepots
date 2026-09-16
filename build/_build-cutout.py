#!/usr/bin/env python3
"""Turn white-background catalogue product JPEGs into clean alpha cutouts,
then lay each one out on a shared plate with a common baseline and
consistent optical weight.

No pixel of the product itself is altered: only the white studio sweep is
removed and the result is repositioned. Colours and silhouettes are untouched.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = "index-assets"
OUT = "index-assets-cut"

# products that are genuine project photography, not studio cutouts
PHOTOS = {"bar-planter.jpg", "custom-project.jpg"}


def cutout(path, white_lo=234, ramp=16, despeckle_frac=0.00040):
    """Return RGBA array with the white sweep removed."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    lo = a.min(axis=2)           # 255 on pure white
    hi = a.max(axis=2)
    sat = hi - lo                # 0 on any neutral

    # distance from "paper white", in levels
    d = np.maximum(255.0 - lo, sat * 1.8)
    alpha = np.clip((d - (255 - white_lo - ramp)) / ramp, 0.0, 1.0)

    solid = alpha > 0.55
    h, w = solid.shape
    area = h * w

    # 1. fill pinholes: small opaque-less islands fully inside the product
    #    (specular highlights read as white and would punch holes)
    holes, n = ndimage.label(~solid)
    if n:
        border_ids = set(np.unique(np.concatenate([
            holes[0], holes[-1], holes[:, 0], holes[:, -1]])))
        border_ids.discard(0)
        sizes = ndimage.sum(np.ones_like(holes), holes, range(1, n + 1))
        for i in range(1, n + 1):
            if i in border_ids:
                continue
            # an enclosed white region large enough to be real background
            # (an open frame, the gap under an arch) stays transparent
            if sizes[i - 1] < area * 0.0016:
                solid |= holes == i

    # 2. despeckle: drop JPEG ringing specks floating in the sweep
    blobs, n = ndimage.label(solid)
    if n:
        sizes = ndimage.sum(np.ones_like(blobs), blobs, range(1, n + 1))
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes >= area * despeckle_frac
        solid = keep[blobs]

    alpha = np.where(solid, np.maximum(alpha, 0.0), np.minimum(alpha, 0.0))
    # soften the cut by one pixel so edges do not stair-step on the paper
    alpha = np.asarray(
        Image.fromarray((alpha * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(0.6))
    ).astype(np.float32) / 255.0

    # 3. edge decontamination: unpremultiply the white the sweep left behind
    #    on semi-transparent pixels, so the fringe does not glow on paper
    e = np.clip(alpha, 0.04, 1.0)[..., None]
    rgb = np.clip((a - 255.0 * (1.0 - e)) / e, 0, 255)
    blend = np.clip((alpha[..., None] - 0.15) / 0.5, 0, 1)
    rgb = rgb * blend + a * (1 - blend)

    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return out


def trim(rgba, thresh=8):
    al = rgba[..., 3]
    ys, xs = np.where(al > thresh)
    if len(ys) == 0:
        return rgba
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


# ---------------------------------------------------------------- plates
PLATE_W, PLATE_H = 1320, 990          # 4:3, matches the card frame
BASELINE = 0.885                       # products stand on one shared line
MAX_H = 0.700                          # tall objects never exceed this
MAX_W = 0.780                          # wide objects never exceed this

# Optical weight per item. Objects are NOT at a common physical scale --
# the catalogue does not supply one -- so this is a drawing convention that
# keeps the grid even: a lone tall tower and a four-piece family of cubes
# should occupy a similar amount of ink.
WEIGHT = {
    "big-ben-tower.jpg":  1.00,
    "tower-bridge.jpg":   1.00,
    "siena.jpg":          0.94,
    "dawn.jpg":           0.92,
    "riverside-flow.jpg": 1.00,
    "riverside-rise.jpg": 1.00,
    "riverside-base.jpg": 0.96,
    "grand-wall.jpg":     1.00,
    "siena-kubo.jpg":     0.88,
    "pixie.jpg":          1.00,
    "cube-shelf.jpg":     0.98,
    "garden.jpg":         0.94,
}


TARGET_INK = 0.215   # how much of the plate a collection should occupy


def plate(rgba, weight=1.0):
    im = Image.fromarray(rgba, "RGBA")
    w, h = im.size
    s = min(PLATE_H * MAX_H / h, PLATE_W * MAX_W / w) * weight

    # damped ink normalisation: a lone slender tower and a four-piece family
    # of cubes should carry similar visual weight without either being
    # distorted, so correct only part of the way towards the target
    ink = (rgba[..., 3] > 8).mean() * (w * s) * (h * s) / (PLATE_W * PLATE_H)
    if ink > 0:
        s *= float(np.clip((TARGET_INK / ink) ** 0.34, 0.86, 1.16))
    s = min(s, PLATE_H * MAX_H / h, PLATE_W * MAX_W / w)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    im = im.resize((nw, nh), Image.LANCZOS)

    canvas = Image.new("RGBA", (PLATE_W, PLATE_H), (0, 0, 0, 0))
    x = (PLATE_W - nw) // 2
    y = round(PLATE_H * BASELINE) - nh
    canvas.alpha_composite(im, (x, max(0, y)))
    return canvas


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    report = {}
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".jpg") or f in PHOTOS:
            continue
        src = os.path.join(SRC, f)
        r = trim(cutout(src))
        p = plate(r, WEIGHT.get(f, 1.0))
        name = f.replace(".jpg", ".png")
        p.save(os.path.join(OUT, name), optimize=True)
        cover = (np.asarray(p)[..., 3] > 8).mean()
        report[name] = {"source": f, "trimmed": list(r.shape[:2][::-1]),
                        "ink_coverage": round(float(cover), 4)}
        print(f"{name:24s} trimmed={r.shape[1]}x{r.shape[0]:<5d} ink={cover:.3f}")
    json.dump(report, open(os.path.join(OUT, "_report.json"), "w"), indent=1)
