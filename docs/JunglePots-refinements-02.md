# Refinement pass 02 — imagery, frames, motion

The approved "architectural catalogue system" direction is unchanged. No
section was added, removed or reordered, and no copy, measurement, finish
code, capacity or product claim was altered. This pass is about how the
existing material is presented.

The previous state is preserved in `_source-assets/` alongside the original
`JunglePots-before-refinements.zip`.

## 1. Product imagery is genuinely cut out

Twelve catalogue product views were being shown as white JPEGs inside a white
card, faked onto the page with `mix-blend-mode: multiply`. That approach
darkens rather than removes, so every product carried a grey halo and each
card read as a shop tile rather than a catalogue plate.

Those twelve are now real alpha cutouts (PNG). The studio sweep is removed by
thresholding on whiteness and saturation, enclosed regions that are actually
background — the gap under the Tower Bridge arch, the voids in the Cube Shelf
frame — are kept transparent, and semi-transparent edge pixels are
un-premultiplied so no white fringe glows against the paper ground.

Nothing was generated, painted, retouched or reconstructed. Product colour,
silhouette, proportion and photographic lighting are the supplied catalogue
pixels, unmodified.

The detail page's isolated Big Ben Tower view received the same treatment, so
it no longer sits in a white box.

## 2. One plate, one baseline

Each cutout is placed on a 4:3 plate against `--plate` (`#EDEBE4`, between the
paper and surface tokens) with:

- a shared standing line at 88.5% of the plate height, so the grid reads as
  one catalogue sheet instead of thirteen unrelated crops;
- a damped optical-weight correction toward a common ink coverage, capped so
  nothing is distorted and no object is enlarged past 70% of the plate height
  or 78% of its width.

**This is a drawing convention, not a scale.** Objects are still not shown at
a common physical scale — the catalogue does not supply one — and the existing
"images are not to scale" disclosure is retained and still required. A plate
showing a family of sizes still shows the photographed group; scheduled
variant counts remain independent of how many objects appear.

## 3. Material close-ups contain no studio background

The homepage rim spread previously ended in a hard white wedge where the
studio sweep entered the frame. The rim, feet and leg-connection close-ups are
now cropped to the largest rectangle at the required aspect ratio that
contains no background, found by search over the original photograph. Each
crop is a strict subset of the supplied image — nothing is cloned, extended or
in-painted. Crop rectangles are recorded in
`JunglePots-refinement-02-provenance.json`.

The production page's construction frame changed from `object-fit: contain`
on white to `cover` on the plate token, so a view switch no longer flashes a
white box.

## 4. Motion as a deliberate layer

The previous pass applied one 550 ms fade to everything. This pass replaces it:

- the hero title reveals a line at a time from behind its own baseline
  (1150 ms, 110 ms apart);
- supporting hero copy and actions follow at 820 ms on a short stagger;
- the hero photograph settles from 1.055 to 1.0 over 1700 ms rather than
  appearing;
- sections and catalogue plates enter on approach, batched and sorted by
  position so a grid resolves top-left to bottom-right at 70 ms intervals
  instead of flashing in as a block;
- filtering re-deals the visible cards;
- product and construction view switches dissolve (520 ms) instead of cutting;
- hover: plate image 1.028 over 900 ms, plate ground deepens over 700 ms, link
  arrows 380 ms, disclosure markers rotate 340 ms.

All easing is `cubic-bezier(.16,.84,.44,1)`. Browser-native Web Animations and
IntersectionObserver only; no animation library.

**Safety.** Hidden initial states are applied only after the script confirms
it can finish, are wrapped in try/catch, and are released by a 2.6 s failsafe
timer. With JavaScript off, animation unsupported, or
`prefers-reduced-motion: reduce`, every element renders visible and static.
Scrolling is never intercepted and no entrance gates reading.

## 5. Verification

Checked at 1920, 1440, 1024, 768 and 390 px: no horizontal overflow on any
page. No console or page errors. With motion on and with reduced motion
forced, no element is left below full opacity. The Round filter returns Dawn,
Riverside Flow, Riverside Rise and Riverside Base and reports four
collections. Specification disclosures open. The detail page's product view
loads the new plate and keeps its isolated treatment; the production page's
leg-connection view loads its cleaned crop and updates its caption. No email
was sent.

## 6. Open items for the client

- **Riverside Flow** is photographed in a bright green finish. The cutout is
  faithful to the supplied catalogue, and it is the one collection that sits
  outside the restrained palette in the grid. A neutral-finish photograph of
  the same range would resolve it; recolouring the existing photograph would
  misrepresent the product and has not been done.
- **Bar Planter** still has no isolated view in the catalogue and keeps its
  project photograph, so it is the one card in the grid that is not a plate.
- Real workshop photography, an approved manufacturing description and finish
  sample documentation remain the highest-value content inputs.

## 7. Build order

`build_refined.py` rebuilds `build/` from scratch, then `build_hero.py`, then
`drawing.py` → `make_svg.py` → `build_drawing.py`. Supporting scripts:
`cutout.py` (plates), `materialcrop.py` (background-free close-ups),
`trace.py` (hero silhouettes). All are included as `_build-*.py`.
