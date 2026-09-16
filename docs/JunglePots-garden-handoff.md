# Garden — collection page

The seventh collection page, and the first built from a single photograph.
Also the first where the missing number is a safety number.

---

## 1. One frame, three views

Garden has no retail listing anywhere. I enumerated all 21 Jungle Flora
metal-planter listings on emedelynas: Garden, Cube Shelf and Bar Planter are
absent from all of them, and a search of jungleflora.lt returns nothing
either. So the page rests on one catalogue photograph, page 18.

Rather than run the template's single-image path, the page carries three views
cut from that one frame:

| View | What it shows |
|---|---|
| 01 Product | the isolated tray, white sweep removed |
| 02 Suspension | a corner: cap nut above, bolt through, ring beneath |
| 03 Edge | the rolled edge and two cap nuts |

All three carry `CATALOGUE 18` in the source line and the two details say
`SAME FRAME`, so nobody reads this as three shoots.

That second crop earned its place. At catalogue scale the black shapes are
unreadable specks; at full resolution they resolve into the actual suspension
mechanism — a dome cap nut on the tray face, a bolt through the corner, a
closed ring underneath. On a product that hangs over people's heads, that is
the one thing a specifier needs to see, and the isolated view is far too small
to show it.

The two details are alpha cutouts, not JPEGs, so they sit on the paper the way
the isolated plates do rather than punching a white rectangle into the page.

---

## 2. The absence here is a safety absence

Three pages, three shapes of the same problem, and this is the fourth and the
sharpest:

* **Siena** — capacity published, and wrong.
* **Dawn** — published, and right.
* **Grand Wall** — published nowhere.
* **Garden** — the missing number is the **safe working load of a tray hung
  from a concrete ceiling**, and the tray height and capacity are missing
  alongside it.

The catalogue describes the suspension — chain or steel cable, rings and
carabiners, concrete-ceiling anchors — and gives no safe working load, no
fixing specification, no steel thickness and no filled weight. With no listing
anywhere, there is no second source to close the gap.

The schedule shows three explicit "Not published" rows and the disclosure
derives nothing. The dead load of 2.2 m of wet substrate is not a figure to
estimate from a photograph, and the page says so, and says to have the ceiling
fixing checked by a structural engineer.

**This is the strongest single argument for the content request** that Siena,
Grand Wall and Garden have been building towards. The other three are
commercial. This one is liability.

---

## 3. The drawing: plan mode

Garden is photographed nearly in plan and the catalogue publishes no vertical
dimension, so `spec_drawing.build` gained `mode="plan"`: two letters, and the
**extreme vertices of the whole silhouette** rather than the top band. The
top band of a flat tray is one single edge, so both arrows had collapsed onto
the same corner.

The two suspension rings hang below the tray, and the tracer turned them into
ragged notches on the near-left corner. They are masked out of the source
before tracing — a plan outline has no business carrying a drooping ring — and
the caption says so and points at view 02.

Letters are sized by `ui=0.78`. The rule that keeps emerging: the letter size
should hold `font-size / viewBox-width` roughly constant across the family,
because every squat drawing is width-limited in the spec column. A tall
drawing is the opposite case.

---

## 4. Two inherited bugs, fixed across the family

Both were invisible until a page needed them.

**`hero.style.aspectRatio=v[5]` on a five-element array.** The gallery entry is
`[src, alt, caption, source, ratio]`; index 5 is `undefined`, so the assignment
sets nothing. Every page since Tower Bridge has been ignoring its per-view
aspect ratios and rendering every view in whatever the CSS said. Now `v[4]`,
patched on all five derived pages.

**A hole at one breakpoint.** The template styles `.hero-img` at three
container breakpoints — base, 800 and 600 — and each page's trailing override
block only ever set base and 600. Between 600 and 800 the hero fell back to the
template's portrait ratio, so a landscape product view was cropped to a
portrait slot at that one width. The 800 rule now carries each page's own
ratio.

`patch_gallery.py` applies both. Big Ben Tower has neither a gallery nor a
trailing block and is untouched.

---

## 5. Evidence

| Model | A length | B depth | Rings |
|---|---|---|---|
| X1 | 570 | 220 | 4 |
| X2 | 1110 | 220 | 4 |
| X3 | 1650 | 220 | 4 |
| X4 | 2200 | 220 | 6 |

Catalogue pages 18–19 and 26. Two dimensions only — how deep the tray is, and
therefore how much it holds, is not published.

Material panel: the "Base / Integrated adjustable feet" row from the template
is wrong for a suspended product and now reads "Suspension / Chain or steel
cable". Garden is photographed once, in a mid grey the catalogue does not name;
the rings and cap nuts are black in that frame and whether that is the finish
or a supplied component is not stated.

Related collections: Cube Shelf (the same idea, standing) and Grand Wall (the
same line, on the floor).

---

## 6. Verified

Garden and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion and
reduced motion: no page or console errors, no horizontal overflow, no broken
images, nothing below full opacity, every stroke dash offset at 0. Grand Wall
and Dawn re-verified after the two patches, with the gallery switching checked
by hand on Tower Bridge and Siena — the per-view ratios now apply and nothing
overflows.

Remaining reports are the site-wide chrome ones, identical on every page.
