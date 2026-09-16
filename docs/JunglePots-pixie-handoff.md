# Pixie — collection page

The twelfth collection page. Every standard collection now has one; Bar Planter
remains, as an enquiry-led page rather than a specification one.

---

## 1. The capacity column is the A dimension with the unit changed

Pixie is a cube, so its volume is fixed by one number and there is no
convention to argue about:

| Model | Printed | Volume of the box |
|---|---|---|
| 150 | 15 L | 3.4 L |
| 170 | 17 L | 4.9 L |
| 200 | 20 L | 8.0 L |
| 230 | 23 L | 12.2 L |

A 150 mm cube encloses 3.4 L. The catalogue prints 15 L beside it. On all four
rows the printed figure is exactly the A dimension in centimetres with *cm*
swapped for *L* — 15, 17, 20, 23.

**This is the one place in the catalogue where a capacity is unambiguously
wrong rather than ambiguously derived.** Everywhere else — Riverside Flow,
Rise, Base, Siena — the argument is about which convention was used. Here there
is no convention that produces 15 L from a 150 mm cube. It suggests the
capacity column was assembled by hand rather than computed, which is worth
saying in the same breath as the Riverside figures rather than separately.

The page prints the catalogue table unchanged and shows the enclosed volume of
the box beside it, labelled as geometry and explicitly **not** a planting
capacity — it takes no account of wall thickness, drainage or freeboard.

---

## 2. Pixie has no photograph

Every other collection has at least one project, interior or context image.
Pixie appears **only on the specification page**, as two small isolated renders:
one cube and a group of four. No project, no interior, no detail, no scale
reference, no hand or plant beside it.

It is the least expensive item in the range and the one most likely to be
ordered in quantity, and there is nothing to show it with. Two views, and the
page says so in the schedule note rather than hiding it.

---

## 3. Two notes on the tooling

**The catalogue's own mask carries its dimension arrows.** `p26-5` is the alpha
for `p26-4`, but the drawn A/B/C arrows are in it as thin strokes. The cube
component is 91007 px and the next largest is 856, so taking the largest
connected component alone drops every arrow and leaves a clean isolated cube.
That trick is worth remembering for any other annotated illustration.

**`interior=True` is essential here.** Without it the open top reads as a solid
hexagon and the object stops being a planter. With it the rim comes back and it
reads as a box.

---

## 4. A finding for the Garden page, not this one

Page 26 carries two footnotes under the Garden table. The first repeats the
suspension description already on that page. The second is new:

> *Recommended pots: - Nicoli bed pot Clypso Matt 50; Nicoli bed pot Minos
> Cassetta 45

So the catalogue **does** name liner pots for Garden, by third-party brand and
model. The Garden page currently says the tray depth and capacity are not
published and does not mention liners at all, which is now incomplete.

Two reasons this has not been added unilaterally:

1. It names a third-party manufacturer on what would be a JunglePots page. That
   is a commercial decision, not a design one.
2. It is not certain from the layout that the footnote belongs to Garden rather
   than to the page as a whole, though its position directly under the Garden
   table and the fit of a bed pot to a 22 cm tray both point that way.

**Recommended: confirm with the client, then add a liner row to the Garden
schedule.** It answers the "how deep, how much does it hold" question that page
currently has to leave open.

---

## 5. Evidence

| Model | A | B | C | Capacity |
|---|---|---|---|---|
| 150 | 150 | 150 | 150 | 15 L |
| 170 | 170 | 170 | 170 | 17 L |
| 200 | 200 | 200 | 200 | 20 L |
| 230 | 230 | 230 | 230 | 23 L |

Catalogue page 26. A true cube at every size, open at the top.

Two views, both from page 26: the isolated product and the four sizes together.
Illustrated only in the dark grey, unnamed.

Related collections: Siena Kubo and Riverside Base, both built, both linked.

**Page 26 carries prices and they are deliberately not shown**, per the brief.

---

## 6. Verified

Pixie and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion and
reduced motion: no page or console errors, no horizontal overflow, no broken
images, nothing below full opacity, every stroke dash offset at 0. Remaining
reports are the site-wide chrome ones, identical on every page.
