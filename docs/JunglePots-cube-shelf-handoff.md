# Cube Shelf — collection page

The eighth collection page, and the one that changes how the remaining four
should be built.

---

## 1. The catalogue was on your machine the whole time

`work/catalogue/` in the connected folder holds a full-page render of every
catalogue page and every image extracted from it — `page-17.png`,
`index-assets/p17-0.jpg` through `p17-3.jpg`, and the same for all 28 pages.

Every collection page so far has been built from one low-resolution crop in
`_source-assets/`. Page 17 alone yields **four** images at up to 1400 px: the
moss-wall project photograph, the three-size group, an isolated bare frame, and
the group's clipping mask. Page 25 is the authoritative specification sheet.

Two consequences:

* The four remaining collections — Pixie, Riverside Flow, Rise and Base — should
  be built from these, not from `_source-assets/`.
* **The earlier pages are worth revisiting.** Tower Bridge, Siena, Siena Kubo,
  Dawn and Grand Wall were each built from a single crop where several images
  and a spec sheet existed. That is a short, high-value pass.

### The catalogue ships its own clipping masks

`p17-2.jpg` is a black-and-white alpha channel for `p17-1.jpg`. Using it gives a
pixel-exact cutout of the three-cube group instead of a threshold guess. Worth
looking for on every page from here on.

---

## 2. An open frame traces beautifully

`silhouette()` walks holes as well as the outer ring, so the bare frame comes
back as **eight rings** — the outline plus seven openings — which reconstructs
the whole wireframe with every member at its true width. No interior-edge pass,
no straightening special case. It is the best drawing in the set.

One fix was needed. The sweep behind that frame carries a faint blue cast that
the default `white_lo=234` reads as product, filling in exactly the openings
that make it a frame. `white_lo=205, ramp=22` leaves them open.

The letters are passed `('B','A','C')` so that A lands on the left-going top
edge and B on the right-going one, matching the catalogue's own diagram on page
25. All three are equal at every size, so nothing numerical turns on it — but
the drawing and the source now agree.

---

## 3. Cube Shelf is not a planter, and the material panel was

Every other page's material panel draws on the general planter specification on
page 23: galvanized steel under the coating, a sand-textured finish, integrated
adjustable feet, indoor and outdoor use, plus four claims from Jungle Flora's
listings. **None of that is stated for Cube Shelf.** It is not a planter, it has
no listing, and the catalogue gives it one sentence — the footnote on page 25:

> thick-walled square profile 20 × 20 mm; powder-coated. Complete with metal
> sheet shelf, with plastic plugs.

The panel is now that sentence and nothing else, with Application and Shelf load
shown as explicitly absent, and a disclosure saying why it is shorter than the
others. Whether the frame is galvanized beneath the coating, and whether it is
rated for outdoor use, are open questions rather than omissions.

This also means the four RAL swatches carry a warning: they come from the
planter spec, Cube Shelf is photographed only in dark grey, and no colour range
is published for it.

---

## 4. The absence: no shelf load

Same shape as Garden, one storey down. Page 17 photographs a **planted Dawn
standing on a Cube 50**, so a planted planter is the intended load — and no
shelf load, sheet thickness or frame weight is published, by the catalogue or
by anyone else.

### And a second panel: which planter fits which cube

Two published tables happen to line up. Dawn is 29.5, 39.5 and 44 cm across the
rim; the cube tops are 30, 40 and 50 cm square. Each Dawn sits inside the
corresponding cube top with 5 to 60 mm to spare.

The page shows this as **an observation, not a recommendation**, and says so in
the summary line: neither source states a pairing, gives a clearance, or
approves any planter for any frame. It is two published tables set side by side
so a specifier can check the arithmetic — which is useful, and is not the same
as manufacturer guidance.

---

## 5. Evidence

| Model | A | B | C |
|---|---|---|---|
| Cube 30 | 300 | 300 | 300 |
| Cube 40 | 400 | 400 | 400 |
| Cube 50 | 500 | 500 | 500 |

Catalogue pages 17 and 25. A true cube at every size, which is why one drawing
covers all three.

Four views, all from page 17: the moss wall in context, the three sizes
isolated, the bare frame, and the shelf seated in the frame.

Related collections: Dawn (the planter photographed on it) and Garden.

**Page 25 carries prices — 136, 148 and 157 € — and they are deliberately not
shown**, per the brief. The same page also confirms Riverside Base at 30/35,
40/35 and 60/60 cm and Riverside Rise at 31 L for all three heights, both of
which will matter when those pages are built.

---

## 6. Verified

Cube Shelf and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion
and reduced motion: no page or console errors, no horizontal overflow, no broken
images, nothing below full opacity, every stroke dash offset at 0. Remaining
reports are the site-wide chrome ones, identical on every page.

## 7. Package note

The build had crossed the 20 MB transfer limit again. The sixteen photographs
over 300 KB were re-encoded at quality 82, progressive, at unchanged pixel
dimensions — 2.8 MB saved with no visible loss. Nothing was resized.
