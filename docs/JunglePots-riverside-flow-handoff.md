# Riverside Flow — collection page

The ninth collection page. It closes one open question from the catalogue
analysis and opens a much bigger one about the capacity column.

---

## 1. The B convention is settled — by the catalogue's own diagram

The analysis flagged Riverside Flow's B as *"height convention requires
clarification"*. Page 24's diagram answers it, and the answer is not the
obvious one:

* **A** spans the rim.
* **B** runs from the rim to the **underside of the bowl**.
* A separate figure, printed as a bare `150`, spans from the bowl's underside
  to the floor.

So **B is the bowl alone**, and the overall height is B + 150 mm. The schedule
carries A, B and a leg-height row, and deliberately prints **no combined
overall height**, because the catalogue prints none.

The same `150` appears on the Riverside Rise diagram on page 25, so the
convention should carry to that page too.

---

## 2. The capacities do not reconcile, and this page can show it

A plain cylinder A across and B tall would hold roughly double the printed
figure at the small end:

| Model | Printed | A × B as a cylinder |
|---|---|---|
| 200 | 7 L | 12.6 L |
| 300 | 17 L | 28.3 L |
| 400 | 43 L | 62.8 L |
| 600 | 127 L | 169.6 L |

Three further facts, all from the catalogue itself:

1. **Riverside Base 600 is published at the same A and B as Riverside Flow
   600** — 60 cm and 60 cm — and at a different capacity: **169 L against 127
   L**. And 169 L is *exactly* the plain cylinder volume of those dimensions.
2. The figures **7, 17 and 43 L** are also printed against Siena, and 17 and 43
   against Riverside Base. These three numbers move around the catalogue.
3. Every Flow figure matches a cylinder A across and **B minus 150** tall, to
   within a litre — 7.9 / 17.7 / 44.0 / 127.2 against 7 / 17 / 43 / 127.

Fact 3 is the tempting one and the page does **not** act on it. It would imply
that Flow's capacities were computed as though B included the legs, which
contradicts the diagram that settles §1. Both readings are consistent with part
of the evidence and neither with all of it, so the page prints the published
figures, shows the arithmetic beside them, and asks for the usable volumes.

That is now the fourth distinct shape of the capacity problem, and the first
where two collections contradict each other directly.

---

## 3. Two changes to the tooling

**`spec_drawing` gained a `stand` mode.** `round` mode runs its vertical arrow
from the rim to the bottom of the silhouette, which on a bowl standing on legs
would contradict the source. `stand` finds the bowl's base — the row where the
filled width of the silhouette collapses from a solid cylinder to three thin
bars — runs B to there, and puts a third short dimension below it for the legs.
The drawing now reads exactly like the catalogue's own.

**The cutout needed a different test for one image.** The isolated green group
was shot with a soft drop shadow that picks up the planter's own colour, so the
usual whiteness test keeps the shadow — shadow and pale legs sit at almost the
same lightness. Saturation separates them cleanly: shadow 17, legs 44, bowl
102. That one image is cut on saturation, with a darkness term to keep the
black plug caps.

The two leg close-ups are **not** cut out. They are crops on a soft studio
gradient rather than a white sweep, so thresholding leaves a rectangle of
retained grey. They stay photographs.

---

## 4. Evidence

| Model | A diameter | B bowl height | Capacity |
|---|---|---|---|
| 200 | 200 | 400 | 7 L |
| 300 | 300 | 400 | 17 L |
| 400 | 400 | 500 | 43 L |
| 600 | 600 | 600 | 127 L |

Legs 150 mm on all four. Catalogue pages 9 and 24.

Four views, all from page 9: the moss wall in context, the isolated group in
pale green, the leg meeting the bowl underside, and the tube end at the bowl's
lower edge.

**The group photograph shows three planters; the schedule lists four models.**
Which three is not stated.

Riverside Flow is the second collection photographed in two finishes — dark
grey on the moss wall, pale green isolated — after Grand Wall. Neither source
names either colour.

Related collections: Riverside Base and Riverside Rise, neither built yet, so
both cards are enquiry-only.

**Page 24 carries prices and they are deliberately not shown**, per the brief.

---

## 5. Carried forward to the rest of the family

* **Riverside Rise** prints 31 L against all three heights. Under the §1
  convention a 30 cm bowl at B = 60 holds 31.8 L — so the 600's figure is
  right and the 800 and 1000 appear to be the first row repeated. The
  alternative is a fixed-size planting liner. Both go on that page.
* **Riverside Base 300** is 30 × 35 cm in the catalogue and 30 × 25 cm on the
  Jungle Flora listing — a conflict pinned earlier. Its published 17 L is
  consistent with 25 cm and not with 35 cm. Worth stating on that page; still
  the client's to confirm.

---

## 6. Verified

Riverside Flow and the collection index at 1920 / 1440 / 1024 / 768 / 390,
motion and reduced motion: no page or console errors, no horizontal overflow,
no broken images, nothing below full opacity, every stroke dash offset at 0.
Remaining reports are the site-wide chrome ones, identical on every page.
