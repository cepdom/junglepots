#!/usr/bin/env python3
"""Build a specification line drawing for one collection.

Generalised from the Big Ben Tower build so every collection with a
single-object isolated view can be drawn the same way.

Everything drawn comes from an isolated photograph of the product: the outer
silhouette is traced from the alpha cutout, and interior edges are drawn only
where the photograph resolves them unambiguously -- Tower Bridge's arch and
front/side corner survive, Big Ben Tower's shadowed recess does not. Nothing
is modelled or idealised, and a form whose interior is in shadow simply gets
an outline.

The A / B / C letters keep each collection's own catalogue convention, which
differs between collections, so the roles are passed in rather than assumed.
No dimension value is drawn: the numbers stay in the schedule table beside the
drawing with their source and verification status.
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure

# The silhouette is the outer prismatic form, so it is simplified firmly.
# Interior edges can include curvature, so they are traced finely and
# straightened only where a run is genuinely flat over a long span.
#
# Every tolerance below is quoted against a reference object 552 px tall --
# the catalogue's own isolated crops -- and scaled by SCALE to whatever the
# source actually is. Retailer photography runs to 4000 px and more; a
# tolerance fixed in pixels would leave its edges visibly ragged where the
# same object at catalogue size came out clean.
REF_H = 552.0
SCALE = 1.0

OUT_FINE, OUT_STRAIGHT, OUT_RUN = 1.0, 6.0, 30
IN_FINE, IN_STRAIGHT, IN_RUN = 0.45, 2.2, 40
ON_OUTLINE = 9.0    # native px: closer than this counts as the silhouette
MIN_EDGE = 0.085    # an interior edge must span this share of the height
PAD_L, PAD_T, PAD_R, PAD_B = 104, 88, 60, 30
OFF = 34            # how far the A / B dimension lines sit off the rim
# The annotation layer -- letters, arrowheads, padding, stand-off -- is drawn
# in the same coordinate space as the object, so on a big source it comes out
# proportionally tiny once the SVG is scaled to fit its panel. UI_SCALE sizes
# it against the object instead, so the letters read the same on every
# collection. 1.0 keeps the original sizing for drawings already approved.
UI_SCALE = 1.0
INK = "#232822"


# Trace from the NATIVE cutout, not from a collection-index plate. The plates
# resize each product onto a shared baseline, and a small source scaled up --
# Siena Kubo's cube is 332 px native on a 469 px plate -- comes back with soft
# edges that survive the straightening pass as a bowed bottom and a bulge at
# the near corner. At native resolution the same cube traces dead straight.


def trim_rgba(path):
    a = np.asarray(Image.open(path).convert("RGBA"))
    ys, xs = np.where(a[..., 3] > 8)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def straighten(poly, flat, run_px):
    """Collapse long, flat runs into single edges while leaving curvature
    alone.

    A uniform Douglas-Peucker tolerance cannot serve both a prismatic box and
    an arch: coarse enough to recover true straight edges, it turns the arch
    into a pair of chamfers. So a contour is traced finely, then any run of
    points that stays within `flat` px of its own chord *and* spans at least
    `run_px` is replaced by that chord. Straight edges come out straight; the
    arch, whose points leave the chord immediately, is untouched.
    """
    out = [poly[0]]
    i = 0
    n = len(poly)
    while i < n - 1:
        j = i + 1
        best = i + 1
        while j < n:
            a, b = poly[i], poly[j]
            ab = b - a
            L = float(np.hypot(*ab))
            if L < 1e-9:
                j += 1
                continue
            seg = poly[i:j + 1]
            dev = np.abs(np.cross(ab, seg - a)) / L
            if dev.max() > flat:
                break
            if L >= run_px:
                best = j
            j += 1
        out.append(poly[best])
        i = best
    return np.array(out)


def scaled():
    return (OUT_FINE * SCALE, OUT_STRAIGHT * SCALE, OUT_RUN * SCALE)


CURVED = False      # set for a form with no long straight edges to recover


def silhouette(rgba):
    """The outer boundary, and any hole the object is genuinely seen through.

    Tower Bridge's arch is a real opening: photographed against the studio
    sweep it cuts a hole in the alpha, so it belongs to the silhouette rather
    than to the interior edges. A form photographed against its own inner wall
    has no such hole and gets nothing here.
    """
    fine, flat, run = scaled()
    alpha = np.pad(rgba[..., 3].astype(np.float32) / 255.0, 2)
    cs = sorted(measure.find_contours(alpha, 0.5), key=len, reverse=True)
    out = []
    for c in cs:
        if out and len(c) < 0.06 * len(cs[0]):
            break
        p = measure.approximate_polygon(c, tolerance=fine)[:, ::-1] - 2
        # The straightening pass exists to recover the true straight edges of
        # a prismatic box. A faceted cylinder has none: every break in its
        # outline is a real facet, and straightening rounds them all away into
        # a blob. So a curved form keeps the fine trace as it stands.
        out.append(p if CURVED else straighten(p, flat, run))
    return out


def face_threshold(lum, mask):
    """Split the product into its lit faces.

    Luminance inside the mask is clustered into four levels; the levels that
    hold real area are kept, and the widest gap between adjacent ones is the
    face boundary. Shading gradients across a single face fall either side of
    a narrow gap and stay together; two genuinely different planes do not.
    """
    v = lum[mask]
    ks = [v.min() + (v.max() - v.min()) * f for f in (.12, .38, .62, .88)]
    for _ in range(80):
        lab = np.abs(v[:, None] - np.array(ks)[None, :]).argmin(1)
        ks = [v[lab == i].mean() if (lab == i).any() else ks[i]
              for i in range(4)]
    keep = sorted(k for i, k in enumerate(ks)
                  if (np.abs(v[:, None] - np.array(ks)[None, :]).argmin(1)
                      == i).mean() >= 0.08)
    if len(keep) < 2:
        return None
    i = int(np.argmax(np.diff(keep)))
    return (keep[i] + keep[i + 1]) / 2


def interior_edges(rgba, outline):
    """Interior edges, drawn only where the photograph resolves them.

    A face brighter than the threshold is found as a region, its boundary is
    traced and simplified exactly like the silhouette, and every part of that
    boundary lying on the silhouette is dropped -- so what survives is the
    edge where one plane meets another, drawn once. On Tower Bridge that is
    the arch and the front/side corner; on a form whose interior is in shadow
    nothing survives, which is the correct outcome.
    """
    r = rgba.astype(np.float32)
    mask = r[..., 3] > 200
    k = max(3, int(round(5 * SCALE)) | 1)
    lum = ndimage.median_filter(
        .299 * r[..., 0] + .587 * r[..., 1] + .114 * r[..., 2], k)
    t = face_threshold(lum, mask)
    if t is None:
        return []
    # Opened and closed generously: the boundary between two flat faces is a
    # straight or smoothly curved line, so a few pixels of sensor noise along
    # it are removed rather than drawn.
    o = max(3, int(round(9 * SCALE)) | 1)
    cl = max(3, int(round(13 * SCALE)) | 1)
    bright = ndimage.binary_closing(
        ndimage.binary_opening((lum > t) & mask, np.ones((o, o))),
        np.ones((cl, cl)))
    lab, n = ndimage.label(bright)
    h = rgba.shape[0]
    out_segs = [(outline[i], outline[i + 1]) for i in range(len(outline) - 1)]

    runs = []
    for i in range(1, n + 1):
        region = lab == i
        if region.sum() < 0.03 * mask.sum():
            continue
        for c in measure.find_contours(np.pad(region.astype(float), 2), 0.5):
            if len(c) < 80 * SCALE:
                continue
            poly = straighten(
                measure.approximate_polygon(
                    c, tolerance=IN_FINE * SCALE)[:, ::-1] - 2,
                IN_STRAIGHT * SCALE, IN_RUN * SCALE)
            # A segment is judged by its own body, not its endpoints: an edge
            # that runs the height of the object still counts as interior
            # where it happens to begin at the silhouette.
            run = []
            for j in range(len(poly) - 1):
                s0 = (poly[j], poly[j + 1])
                if on_outline(s0, out_segs, ON_OUTLINE * SCALE):
                    if len(run) > 1 and path_len(run) > MIN_EDGE * h:
                        runs.append(trim_nubs(np.array(run)))
                    run = []
                else:
                    if not run:
                        run = [s0[0]]
                    run.append(s0[1])
            if len(run) > 1 and path_len(run) > MIN_EDGE * h:
                runs.append(trim_nubs(np.array(run)))
    return runs


MAX_TURN = 60.0     # degrees: a sharper turn than this ends the edge


def trim_nubs(run, _unused=None):
    """Cut a run back to the edge it is actually describing.

    Where an interior edge reaches the silhouette, the two regions can
    disagree by a few pixels and the traced boundary steps sideways along the
    outline before it stops. That staircase turns through a right angle; a
    curve like the arch turns gradually. So the run is grown outward from its
    longest segment and cut at the first turn sharper than MAX_TURN -- which
    keeps the arch whole and drops the steps.
    """
    if len(run) < 3:
        return run
    d = np.diff(run, axis=0)
    L = np.hypot(d[:, 0], d[:, 1])
    ang = np.degrees(np.arctan2(d[:, 1], d[:, 0]))
    turn = lambda i, j: abs((ang[i] - ang[j] + 180) % 360 - 180)
    k = int(L.argmax())
    lo = k
    while lo > 0 and turn(lo - 1, lo) <= MAX_TURN:
        lo -= 1
    hi = k
    while hi < len(d) - 1 and turn(hi + 1, hi) <= MAX_TURN:
        hi += 1
    return run[lo:hi + 2]


def on_outline(s, out_segs, near):
    mids = [s[0] * f + s[1] * (1 - f) for f in (0.2, 0.5, 0.8)]
    return all(min(point_to_seg(m, o) for o in out_segs) < near
               for m in mids)


def point_to_seg(p, s):
    a, b = s
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-9), 0, 1)
    return float(np.hypot(*(p - (a + t * ab))))


def path_len(pts):
    return float(sum(np.hypot(*(pts[i + 1] - pts[i]))
                     for i in range(len(pts) - 1)))


def corners(poly):
    """Rim corners: the nearest top corner, and the left and right extremes of
    the top band -- measured from the drawing, not assumed."""
    y0, y1 = poly[:, 1].min(), poly[:, 1].max()
    band = poly[poly[:, 1] <= y0 + (y1 - y0) * 0.18]
    return (band[band[:, 1].argmin()],
            band[band[:, 0].argmin()],
            band[band[:, 0].argmax()])


def line(x1, y1, x2, y2):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{INK}" stroke-width="1.3" '
            f'vector-effect="non-scaling-stroke" '
            f'marker-start="url(#jp-ah)" marker-end="url(#jp-ah)"/>')


def label(x, y, t):
    fs = 27.0 * UI_SCALE
    return (f'<text x="{x:.0f}" y="{y:.0f}" class="dim-letter" '
            f'font-size="{fs:.0f}" '
            f'text-anchor="middle" dominant-baseline="middle">{t}</text>')


def outward(p, q, centre):
    """Unit normal to pq, pointing away from the object."""
    d = np.array(q, float) - np.array(p, float)
    n = np.array([-d[1], d[0]])
    n /= max(np.hypot(*n), 1e-9)
    mid = (np.array(p, float) + np.array(q, float)) / 2
    return -n if np.dot(n, mid - np.array(centre, float)) < 0 else n


def offset_dim(p, q, centre, gap, lab, ui=1.0):
    """A dimension line parallel to pq, set off the edge it measures, with its
    letter beyond it -- so a foreshortened edge still reads."""
    n = outward(p, q, centre)
    a = np.array(p, float) + n * gap
    b = np.array(q, float) + n * gap
    mid = (a + b) / 2 + n * 22 * ui
    return line(a[0], a[1], b[0], b[1]) + "\n" + label(mid[0], mid[1], lab)


def build(src, name, letters, roles, interior=False, curved=False,
          ui=1.0, mode="round"):
    """letters / roles: three labels in draw order (across, receding,
    vertical), or two (across, vertical) for a round form.

    A cylinder has no receding top edge to measure -- the catalogue gives
    Dawn and the Riversides a diameter and a height and nothing else -- so a
    two-letter call draws one horizontal arrow across the widest point of the
    rim and one vertical. Drawing a third arrow there would invent a
    dimension the catalogue does not publish.
    """
    global SCALE, CURVED, UI_SCALE
    CURVED = curved
    UI_SCALE = ui
    rgba = trim_rgba(src)
    SCALE = rgba.shape[0] / REF_H
    rings = silhouette(rgba)
    poly = rings[0]
    inner = interior_edges(rgba, poly) if interior else []
    d = " ".join("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in r) + " Z"
                 for r in rings)
    W = float(poly[:, 0].max())
    H = float(poly[:, 1].max())
    pl, pt, pr, pb = (PAD_L * ui, PAD_T * ui, PAD_R * ui, PAD_B * ui)
    off = OFF * ui
    vw, vh = W + pl + pr, H + pt + pb

    if len(letters) == 2 and mode == "plan":
        # A tray is seen from above, so its whole outline is the plan and the
        # "top band" holds only one corner. Take the extreme points instead:
        # the topmost vertex and the leftmost and rightmost ones are the three
        # corners of the two plan edges.
        top = poly[poly[:, 1].argmin()]
        left = poly[poly[:, 0].argmin()]
        right = poly[poly[:, 0].argmax()]
    else:
        top, left, right = corners(poly)
    T = lambda p: (p[0] + pl, p[1] + pt)
    centre = T((poly[:, 0].mean(), poly[:, 1].mean()))
    top, left, right = T(top), T(left), T(right)
    bottom = pt + H
    cx = pl + float(poly[:, 0].min()) - 60 * ui
    y0 = pt + float(poly[:, 1].min())

    # three letters: across, receding, vertical (a box)
    # two letters, mode "round": across the rim, and height (a cylinder)
    # two letters, mode "plan":  across, and receding (a tray -- no height
    #     letter, because the catalogue publishes none for a suspended tray)
    round_form = len(letters) == 2 and mode == "round"
    plan_form = len(letters) == 2 and mode == "plan"
    stand_form = mode == "stand"
    p = [f'<svg class="spec-drawing" viewBox="0 0 {vw:.0f} {vh:.0f}" '
         f'fill="none" role="img" aria-label="Line drawing of {name} traced '
         f'from the catalogue photograph, with '
         + ", ".join("%s %s" % (l, r) for l, r in zip(letters, roles))
         + '">',
         '<defs><marker id="jp-ah" viewBox="0 0 10 10" refX="9" refY="5" '
         f'markerUnits="userSpaceOnUse" markerWidth="{15 * UI_SCALE:.0f}" '
         f'markerHeight="{15 * UI_SCALE:.0f}" '
         'orient="auto-start-reverse">'
         f'<path d="M0,1 L10,5 L0,9 z" fill="{INK}"/></marker></defs>',
         f'<g transform="translate({pl:.0f},{pt:.0f})">',
         f'<path class="dwg-out" d="{d}" vector-effect="non-scaling-stroke"/>']
    p += [f'<path class="dwg-in" d="M' + " L".join(f"{x:.1f},{y:.1f}"
          for x, y in run) + '" vector-effect="non-scaling-stroke"/>'
          for run in inner]
    p += ["</g>",
         '<g class="dims">']
    if round_form or stand_form:
        # widest point of the rim, measured on the drawing
        band = poly[poly[:, 1] <= poly[:, 1].min() + H * 0.30]
        xl = pl + float(band[:, 0].min())
        xr = pl + float(band[:, 0].max())
        yr = pt + float(band[:, 1].min()) - off
        p += [line(xl, yr, xr, yr),
              label((xl + xr) / 2, yr - 24 * ui, letters[0])]
        if stand_form:
            # A bowl on legs. The catalogue measures B down the bowl only and
            # prints the leg height as a separate figure below it, so running
            # one arrow to the feet would contradict the source. The bowl's
            # base is where the filled width of the silhouette collapses from
            # a solid cylinder to three thin bars.
            solid = rgba[..., 3] > 8
            cover = solid.sum(axis=1)
            full = cover.max()
            body = np.flatnonzero(cover >= full * 0.92)
            base = pt + float(body[-1])
            p += [line(cx, y0, cx, base),
                  label(cx - 24 * ui, (y0 + base) / 2, letters[1])]
            if len(letters) > 2:
                p += [line(cx, base + 6 * ui, cx, bottom),
                      label(cx - 24 * ui, (base + bottom) / 2, letters[2])]
        else:
            p += [line(cx, y0, cx, bottom),
                  label(cx - 24 * ui, (y0 + bottom) / 2, letters[1])]
    elif plan_form:
        # a tray: two edges of the plan and no height letter, because the
        # catalogue publishes none for a suspended tray
        p += [offset_dim(top, right, centre, off, letters[0], ui),
              offset_dim(top, left, centre, off, letters[1], ui)]
    else:
        a, b, c = letters
        p += [offset_dim(top, right, centre, off, a, ui),
              offset_dim(top, left, centre, off, b, ui),
              line(cx, y0, cx, bottom),
              label(cx - 24 * ui, (y0 + bottom) / 2, c)]
    p += ["</g>", "</svg>"]
    return "\n".join(p), dict(w=round(W, 1), h=round(H, 1),
                              points=len(poly), rings=len(rings), interior=len(inner))


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "tower-bridge"
    name = sys.argv[2] if len(sys.argv) > 2 else "Tower Bridge"
    svg, info = build(f"index-assets-cut/{slug}.png", name, "ABC",
                      ("across the top rear edge",
                       "along the receding top edge",
                       "as overall height"), interior=True)
    open(f"{slug}-drawing.svg", "w").write(svg)
    json.dump(info, open(f"{slug}-drawing.json", "w"), indent=1)
    print(slug, info)
