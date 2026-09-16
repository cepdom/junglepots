# Dawn — collection page

The fifth collection page, and the first round one. Three things in the
drawing system had to change for it, and the data came out clean for once.

---

## 1. A round form takes two letters, not three

The catalogue gives Dawn a diameter and a height and nothing else, because a
cylinder has no receding top edge to measure. `spec_drawing.py` now accepts a
two-letter call and draws one horizontal arrow across the widest point of the
rim and one vertical down the side. Drawing a third arrow would have invented
a dimension nobody published.

That mode is now there for the three Riverside collections, which are
dimensioned the same way.

## 2. A faceted form is traced but not straightened

The straightening pass exists to recover the true straight edges of a
prismatic box: trace finely, then replace any long flat run with its chord.
Dawn has no long straight edges. Every break in its outline is a real facet,
and straightening rounded all of them away into a blob.

`curved=True` keeps the fine trace as it stands. The facet breaks along the
rim and the base survive, and the drawing reads as a folded vessel rather than
a bucket.

## 3. The annotation layer now scales with the object

The letters, arrowheads, padding and stand-off were sized in the same
coordinate space as the object, so on a large source they came out
proportionally tiny once the SVG was scaled into its panel — Dawn's letters
rendered at 12 px where Big Ben's rendered at 17. They are now sized against
the object, so a letter reads the same on every collection.

The panel had a second version of the same fault: `max-width: 300px` with
`height: 430px` meant a tall drawing was height-limited and a squat one was
width-limited to half the column. Dawn caps the height instead and lets the
width take the column.

Both fixes are on this page only. Applying them to the four pages already
approved is a five-minute pass whenever you want it.

**Interior edges are not drawn.** The rim's inner ellipse is plainly visible
to a reader, but the face-clustering pass recovers only fragments of it. By
the rule this system has followed since Big Ben Tower, nothing is drawn rather
than something half-right.

---

## 4. The data checks out

| Model | A ⌀ | B height | Capacity | Listing |
|---|---|---|---|---|
| 295 | 295 | 300 | 21 L | 29.5 × 30 cm, 21 L ✓ |
| 395 | 395 | 350 | 43 L | 39.5 × 35 cm, 43 L ✓ |
| 440 | 440 | 400 | 60 L | 44 × 40 cm, 60 L ✓ |

Every figure is corroborated by Jungle Flora's own listing for that model. The
listing set also carries **the manufacturer's own dimension diagram** — the
planter marked 295 across and 300 high — which confirms the A / B convention
exactly as transcribed. It is not used as the page's drawing (734 px, and a
different drawing language), but it is a clean second source.

This is the first collection where the two sources agree on everything. Siena's
capacities differ by a factor of ten; Tower Bridge's height by 9 cm. The page
says so, because after Siena a silence would read as an omission.

---

## 5. Photography

Four views, all from Jungle Flora's own listing:

| View | Note |
|---|---|
| 01 In context | all three sizes, planted, against a moss wall |
| 02 On a shelf | Dawn standing on a Cube Shelf frame |
| 03 Product | isolated, on the paper colour |
| 04 Facets | close on the folded facets and the rim |

View 02 earns its place: the catalogue photographs Cube Shelf holding a Dawn
planter and notes that they are separate collections. Showing the pairing here
and linking Cube Shelf as a related collection makes that relationship visible
instead of a footnote.

---

## 6. Three facts the catalogue does not carry

The listing publishes, and the material panel now shows under a † with a
disclosure naming the source:

* powder coating in **any RAL shade** — the catalogue offers four
* **logo and initial engraving**
* **manufacture to custom dimensions**
* Lithuanian origin

These are sales copy rather than a specification, so the disclosure says to
treat them as an opening position rather than a guarantee. They are also, for
a B2B audience, three of the most useful things on the page.

---

## 7. Verified

Dawn and the collection index at 1920 / 1440 / 1024 / 768 / 390, motion and
reduced motion: no page or console errors, no horizontal overflow, no broken
images, nothing below full opacity, every stroke dash offset at 0.

Remaining reports are the site-wide chrome ones, identical on every page.

---

## 8. Note on image transfers

Two of the four photographs came back truncated the first time and decoded as
a grey field below the first few hundred rows. They were re-fetched and
checked visually before use. Worth knowing for the remaining collections: a
silently truncated JPEG looks like a successful download.
