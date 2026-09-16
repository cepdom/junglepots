# Grand Wall — collection page

The sixth collection page. Three lengths at one section, and three findings
worth more than the page itself.

---

## 1. The missing capacity is genuinely missing

Siena's capacity was published and wrong. Dawn's was published and right.
Grand Wall's is **not published by anyone**.

The catalogue gives none. Neither does any of the **six** Jungle Flora
listings — where Dawn's and Siena's both carry *naudingas tūris*, every Grand
Wall listing stops at the dimensions. So this is not a transcription gap that
a second source can close.

The page shows it as a row reading "Not published anywhere", with a disclosure
that says so and says nothing has been derived. The external box of the 1900
is 590 L, which is not its planting volume by any margin worth guessing at.

That is now three different shapes of the same problem, and together they make
a better content request than any one of them would alone.

## 2. The letters run the other way

The catalogue photographs Grand Wall almost front-on with its long face to
camera, so the near corner of the rim falls at the right-hand end and the long
span is the **left** edge. The first trace came out with A on the short end
and B down the length — backwards.

Nothing in the drawing code changed. `spec_drawing.py` takes its letters in
draw order, so A — the length — is simply passed second here. That the call
site can fix this without touching the tracer is the point of passing letters
as arguments.

**The rounded ends do not survive the trace.** They are clear in all four
photographs and they are what distinguishes this collection, but the catalogue
crop puts the whole object in 450 × 215 px, where the end radius is a handful
of pixels. Tracing it as a curved form recovered JPEG noise, not the radius.
The drawing squares the ends and the note under the schedule says so.

## 3. The first real exterior photograph in the set

View 01 is a roof terrace: decking, sky, ornamental grasses, café chairs — and
a Grand Wall in a **pale sage green**, not the dark grey everything else in
this catalogue is photographed in.

Two things follow. The homepage claims "interior, exterior and landscape
projects" and until now every collection page has shown an interior; this is
the first page that evidences the claim. And Grand Wall is the only collection
photographed in two finishes, which is worth a line in the material panel: the
green may be Pale Green 6021 from the four swatches, but neither source names
it.

---

## 4. Evidence

| Model | A length | B depth | C height |
|---|---|---|---|
| 900 | 900 | 420 | 740 |
| 1400 | 1400 | 420 | 740 |
| 1900 | 1900 | 420 | 740 |

Catalogue page 26, confirmed dimension for dimension by the listings. A
length, B depth, C height — C vertical, as on the towers and Siena, not as on
Siena Kubo.

Five views: the roof terrace, a planted view against the moss wall, the
isolated catalogue product, the full length empty (showing the folded panel
seams and the feet), and a close view of a rounded end.

---

## 5. A housekeeping note for the client

**Six listings exist for three models** — two each, same dimensions, same
price:

* 4551 and 7174 — the 900
* 4554 and 7175 — the 1400
* 4555 and 7176 — the 1900

The older pair carries a single image each; the newer pair carries the good
photography. That is their storefront, not a problem with this page, but
duplicate listings split reviews and confuse search, so it is worth passing on.

---

## 6. Verified

Grand Wall and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion
and reduced motion: no page or console errors, no horizontal overflow, no
broken images, nothing below full opacity, every stroke dash offset at 0.

Remaining reports are the site-wide chrome ones, identical on every page.

---

## 7. Package note

The build had grown past the 20 MB transfer limit. Eight genuinely unused
images were moved to `_unused/` (the old homepage hero, two orphaned Riverside
project shots, the superseded Tower Bridge crop and its 512 × 770 isolated
view, among others), and the five largest context photographs were re-encoded
at the size the pages actually display them. Nothing the pages reference
changed resolution in a way that shows.
