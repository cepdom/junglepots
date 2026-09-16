#!/usr/bin/env python3
"""Generate the 4:5 isolated-product plate used by the Big Ben Tower detail
page's "02 / Product" view.

Sized smaller than the collection-index plates: the detail view sits on a
frame the same colour as the page, so the product needs room around it to read
as an object on the page rather than a picture in a box.
"""
import os
from PIL import Image

import cutout

SRC = "collection-assets/big-ben-isolated.jpg"
OUT = "hero-cut/big-ben-isolated.png"

PLATE_W, PLATE_H = 1000, 1250   # 4:5, matches the detail hero frame
BASELINE = 0.865                # generous bottom margin, not a tight crop
MAX_H = 0.640
MAX_W = 0.620


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cutout.PLATE_W, cutout.PLATE_H = PLATE_W, PLATE_H
    cutout.BASELINE, cutout.MAX_H, cutout.MAX_W = BASELINE, MAX_H, MAX_W
    cutout.TARGET_INK = 1e9      # disable ink normalisation for a single object

    r = cutout.trim(cutout.cutout(SRC))
    p = cutout.plate(r, 1.0)
    p.save(OUT, optimize=True)
    import numpy as np
    print(f"{OUT}  {p.size}  product={r.shape[1]}x{r.shape[0]}  "
          f"ink={(np.asarray(p)[..., 3] > 8).mean():.3f}")


if __name__ == "__main__":
    main()
