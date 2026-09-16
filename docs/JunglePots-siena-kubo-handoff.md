# Siena Kubo — collection page

The third collection page, and the first with more than one size. Same chrome,
type, grid and motion as Big Ben Tower and Tower Bridge. What follows is what
this collection forced the template to learn, and what it has behind it.

---

## 1. Three sizes, one schedule

Not three cards. The flexible-collection template says so and it is right: a
specifier comparing 35, 44 and 54 wants them in one table with the letters
running down the columns, not the same paragraph three times.

So the schedule becomes a comparison table — the first table on the site with
a `<thead>` — and the mm / cm switch drives the column headers rather than
repeating a unit in nine cells.

| Model | A width | B height | C depth |
|---|---|---|---|
| 1 | 350 | 350 | 350 |
| 2 | 440 | 440 | 440 |
| 3 | 540 | 540 | 540 |

They are cubes, so each row repeats. The columns stay anyway, because the
letters differ on the drawing and the table is what a reader checks them
against. The page says this rather than leaving it looking like a mistake.

---

## 2. Its own A / B / C

**Siena Kubo uses B for height.** Big Ben Tower and Tower Bridge use C.

This is exactly why `spec_drawing.py` takes the three letters as arguments
instead of assuming them — the drawing is built with the vertical arrow
lettered B, so the letters on the drawing and the letters in the table agree
without anyone having to hold a global convention in their head. A disclosure
beside the schedule states the convention explicitly, because a specifier who
has just read the Tower Bridge page will be carrying the other one.

**One drawing serves all three models.** They differ only in scale, so a
second drawing would carry no second fact. The caption says so.

---

## 3. A change to how drawings are traced

Trace from the **native cutout**, not from a collection-index plate.

The index plates resize each product onto a shared baseline. Siena Kubo's cube
is 332 px in the catalogue and 469 px on its plate — a 1.4× upscale — and the
softened edges survived the straightening pass as a bowed bottom edge and a
bulge at the near corner. At native resolution the same cube traces dead
straight with no parameter changes at all.

Tower Bridge was unaffected (its plate is a 1.04× upscale, which is why it
looked fine), but the rule now holds for every collection ahead.

---

## 4. Evidence

| | |
|---|---|
| Schedule | Catalogue page 16. Three cubes: 350, 440, 540 mm |
| Capacity | **None published for this collection at all.** Shown as a row reading "not supplied", with a disclosure |
| Wheels | Hidden castors, optional — in the material list, not the schedule, because it is not a dimension |
| Finish | Photographed throughout in a dark grey close to Anthracite 7016; the catalogue does not name the code |

**Nothing was derived for the capacity.** A cube's bounding box is not its
planting volume, and the liner and drainage details that would settle it are
not supplied either. 35³ cm is 42.9 L of air, which would have been an easy
and wrong number to print.

---

## 5. Photography

Three views, all the catalogue's own:

| View | Source | Note |
|---|---|---|
| 01 In context | page 16 | all three sizes in one frame |
| 02 Product | page 27 | isolated, on the paper colour |
| 03 Rim | page 16 | folded rim, corner, and the sand-textured coating |

The context frame carries all three sizes together, so it doubles as the scale
comparison the schedule cannot give — a table of three cubes tells you the
numbers but not what the difference feels like.

Frame proportions are per view again: 3:2 for the landscape context shot, 1:1
for the product (a squat object on a 4:5 plate strands half the frame), 5:4
for the rim.

The rim close-up came from the Production / Quality page, where it was doing
duty as an abstract hero. It belongs to this collection and is now on its
page; the production page keeps its copy.

---

## 6. Related collections

Siena and Grand Wall — the other two rectangular collections, rather than the
two towers. Neither has a page yet, so both cards offer an enquiry, which is
what Big Ben's Siena Kubo card did before this page existed.

---

## 7. Fixed on the way past

The collection index had lost the "View collection" link on the Tower Bridge
card. `wire_site.py` guarded on whether the page name appeared anywhere in the
file — and once the router became a slug map, every page name appears in every
file, so the guard always passed and the link was never re-added. It now
guards on the anchor itself.

`verify.py` also gained two fixes, both false positives it had been reporting:
a lazy image that never entered the viewport reads as broken, and an element
caught part-way through a 700 ms reveal reads as stuck invisible. It now loads
lazy images and waits for animations to settle before judging.

---

## 8. Verified

Siena Kubo and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion
and reduced motion: no page or console errors, no horizontal overflow, no
broken images, nothing left below full opacity, every stroke dash offset at 0.
The mm / cm switch was checked against all three rows and the column headers.

Remaining reports are the site-wide chrome ones, identical on every page: the
breadcrumb at 17.6 px, footer links at 38 px, the rail phone link at 9.5 px
above 900 px, and `aria-current` appearing once per navigation rather than
once per page.
