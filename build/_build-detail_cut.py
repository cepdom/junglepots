#!/usr/bin/env python3
"""Alpha-cut the construction close-ups (rim, feet, leg joint).

Earlier these were cropped tight into the product so no studio white entered
the frame. Now that every frame sits on the page colour, the white can simply
be removed instead: the whole photograph is shown, zoomed out, and the frame
boundary is invisible.

Only the studio sweep is removed. No pixel of the product is altered.
"""
import os
import numpy as np
from PIL import Image

import cutout

SRC = "build/_source-assets"
OUT = "detail-cut"

JOBS = [
    ("orig-big-ben-rim.jpg",  "big-ben-rim.png"),
    ("orig-big-ben-feet.jpg", "big-ben-feet.png"),
    ("orig-rim.jpg",          "rim.png"),
    ("orig-feet.jpg",         "feet.png"),
    ("orig-joint.jpg",        "joint.png"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, dst in JOBS:
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            print("missing", p)
            continue
        # these close-ups have large mid-tone product areas and only a corner
        # of sweep, so a slightly higher threshold avoids eating pale faces
        r = cutout.trim(cutout.cutout(p, white_lo=240, ramp=12,
                                      despeckle_frac=0.002))
        im = Image.fromarray(r, "RGBA")
        im.save(os.path.join(OUT, dst), optimize=True)
        cov = (r[..., 3] > 8).mean()
        print(f"{dst:20s} {im.size}  opaque={cov:.3f}")


if __name__ == "__main__":
    main()
