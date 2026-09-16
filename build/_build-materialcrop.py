#!/usr/bin/env python3
"""Find the largest crop at a target aspect ratio that contains no studio
background, so a material close-up fills its frame with nothing but product.

Nothing is painted, cloned or generated: the crop is a subset of the
original photograph.
"""
import numpy as np
from PIL import Image


def white_mask(a, lo=232):
    mn = a.min(axis=2).astype(np.int16)
    mx = a.max(axis=2).astype(np.int16)
    return (mn >= lo) & ((mx - mn) <= 14)


def best_crop(path, aspect, tolerance=0.00002, steps=70):
    """aspect = width / height"""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    H, W, _ = a.shape
    bad = white_mask(a).astype(np.float64)
    ii = bad.cumsum(0).cumsum(1)
    ii = np.pad(ii, ((1, 0), (1, 0)))

    def frac(x0, y0, w, h):
        s = (ii[y0 + h, x0 + w] - ii[y0, x0 + w]
             - ii[y0 + h, x0] + ii[y0, x0])
        return s / (w * h)

    best = None
    # widest possible box at this aspect, then shrink
    w_max = min(W, int(round(H * aspect)))
    for k in range(steps):
        w = int(round(w_max * (1 - k / steps * 0.72)))
        h = int(round(w / aspect))
        if w < 40 or h < 40 or h > H:
            continue
        stride = max(2, min(W - w, H - h) // 42 or 2)
        for y0 in range(0, H - h + 1, stride):
            for x0 in range(0, W - w + 1, stride):
                if frac(x0, y0, w, h) <= tolerance:
                    best = (x0, y0, w, h)
                    break
            if best:
                break
        if best:
            break
    if best is None:
        return None
    x0, y0, w, h = best
    return im.crop((x0, y0, x0 + w, y0 + h)), (x0, y0, w, h), (W, H)


if __name__ == "__main__":
    import sys, os, json
    jobs = [
        ("collection-assets/big-ben-rim.jpg", 1.18, "rim-detail.jpg", 0.0006),
        ("production-assets/rim.jpg",         1.30, "rim.jpg",        0.0006),
        ("production-assets/feet.jpg",        1.30, "feet.jpg",       0.00002),
        ("production-assets/joint.jpg",       1.30, "joint.jpg",      0.0006),
        ("collection-assets/big-ben-feet.jpg", 1.30, "bbt-feet.jpg",  0.00002),
    ]
    os.makedirs("detail-assets", exist_ok=True)
    rec = {}
    for src, asp, out, tol in jobs:
        if not os.path.exists(src):
            print("missing", src)
            continue
        r = best_crop(src, asp, tolerance=tol)
        if r is None:
            print("no clean crop", src)
            continue
        im, box, orig = r
        im = im.resize((1600, int(1600 / asp)), Image.LANCZOS) if im.width < 1600 \
            else im.resize((1600, int(1600 / asp)), Image.LANCZOS)
        im.save("detail-assets/" + out, quality=90, optimize=True)
        rec[out] = {"source": src, "crop_xywh": list(box),
                    "source_size": list(orig), "aspect": asp}
        print(f"{out:16s} from {src} crop={box} of {orig}")
    json.dump(rec, open("detail-assets/_crops.json", "w"), indent=1)
