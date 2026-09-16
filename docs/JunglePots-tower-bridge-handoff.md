# Tower Bridge — collection page

The second collection detail page. Same chrome, same type, same grid, same
motion layer as Big Ben Tower — literally the same code, transformed. What
follows is only what is Tower Bridge's own.

---

## 1. The drawing

Big Ben Tower's specification drawing is an outline. Tower Bridge's carries
two interior edges: the arch, and the corner where the front face meets the
side.

That is not a change of mind. The arch in the catalogue photograph is a
high-contrast aperture — you see straight through to a brighter inner wall —
and it sits in full light. Big Ben's recessed slot sits in shadow at the
resolution the catalogue supplies, which is why it was drawn and then removed.
Both pages follow the same rule: **draw what the photograph resolves.**

Drawing Tower Bridge as an outline alone would have been worse than plain.
The white background is only visible through the narrow gap *between* the two
legs, so a pure silhouette renders the collection as a slot, not an arch — the
one feature the whole collection is named for would have been missing from its
own specification panel.

**Why not trace the sharper photograph.** The listing's isolated view
is six times the resolution and shows the arch as a true opening against the
sweep — on the face of it the better source. It was tried and rejected: that
shot lights the inner face of the right leg against white through a soft
gradient, so the traced edge comes out visibly wavy where the catalogue crop
gives a clean one. Better to look at, worse to measure. The drawing stays with
the catalogue; the gallery takes the listing photograph.

### How it is made

`spec_drawing.py` replaces the one-off `drawing.py` / `make_svg.py` pair and
takes any collection with a single-object isolated view.

**Silhouette.** Traced from the alpha cutout, as before. The Douglas-Peucker
pass now runs fine (1 px) and is followed by a straightening pass: any run of
points that stays within 6 px of its own chord *and* spans at least 30 px is
replaced by that chord. A single coarse tolerance cannot serve both a
prismatic box and an arch — coarse enough to recover true straight edges, it
turns the arch into a pair of chamfers. Two passes give straight edges that
are straight and curves that stay curved.

Every tolerance is quoted against a 552 px reference — the catalogue's own
crops — and scaled to whatever the source actually is. That matters as soon as
a second source appears: the listing photographs run past 4000 px, where a
tolerance fixed in pixels leaves edges visibly ragged that came out clean at
catalogue size. If an alpha cutout is ever seen through a hole (rather than a
concavity), that hole is traced as part of the silhouette too.

**Interior edges.** Luminance inside the cutout is clustered into four levels;
levels holding real area are kept and the widest gap between adjacent ones is
taken as the boundary between two planes. Shading across one face falls either
side of a narrow gap and stays together; two genuinely different planes do
not. The brighter region's boundary is traced, everything lying on the
silhouette is dropped, and each surviving run is cut back at the first turn
sharper than 60° — which keeps the arch whole and removes the pixel staircases
where an edge meets the outline. On a form whose interior is in shadow,
nothing survives, which is the correct outcome.

Interior edges are drawn at 1.5 px against the silhouette's 2.2 px, and they
draw themselves with it when the panel is first scrolled to.

**Dimension arrows.** Each line is now offset perpendicular to the edge it
measures, with its letter beyond it. On Big Ben the two rim edges are close to
equal and a straight-up offset worked; Tower Bridge is photographed nearly
front-on, so B is heavily foreshortened and the old placement collided with A.

`spec_drawing.py` takes the A/B/C letters and their roles as arguments rather
than assuming them, because the conventions differ by collection — Siena Kubo
uses B for height where Big Ben uses C.

---

## 2. Evidence, and what the page does not claim

| | |
|---|---|
| Schedule | Catalogue page 27. A 400 / B 400 / C 990 mm, 30 L |
| Height | **Unresolved, and the catalogue is now outvoted.** The catalogue says 99 cm; the existing product listing says 90 cm; Jungle Flora's own marketplace listing says 40 × 40 × 90 cm and 30 L, down to its page title. The page still shows 99 and says why |
| Arch opening | **Not dimensioned anywhere in the catalogue.** It is drawn, and the page says it is not specified |
| Capacity | Stated by the catalogue; usable volume undefined |
| Steel thickness, weight | 2 mm and 6 kg, marked † — **not from the catalogue**, which gives neither. Shown because specifiers need them, under a disclosure naming the source |
| Finish | No catalogue colour code, and the two photographic sources disagree — project photography reads as a deep brick red, studio photography as a warmer terracotta. Possibly white balance; not settleable from photographs |

There is **no Tower Bridge specification PDF**, so where Big Ben offers a
download this page offers "Request specification sheet", pointing at the
enquiry. Nothing was generated to fill the gap.

---

## 3. Photography

The page began with one photograph. It now has five views, because Jungle
Flora's own marketplace listing at `emedelynas.lt/.../12775-...-tower-bridge-40x40x90cm.html` carries
four images at 3000–4600 px on the long edge:

| View | Source | Note |
|---|---|---|
| 01 In context | Jungle Flora | lounge, fluted panel wall |
| 02 In use | Jungle Flora listing | café interior, glazed partition — a genuinely different installation |
| 03 Product | Jungle Flora listing | replaces the 512 × 770 catalogue crop; six times the pixels |
| 04 Rim | Jungle Flora listing | folded rim and the welded inner liner |
| 05 Base | Jungle Flora listing | leg undersides, two adjustable feet each |

**Every frame names its source** on the right of the caption, the way the
homepage hero already labels its photography. Four of the five come from a
sales listing rather than the specification catalogue, and a specifier should
see that without opening a provenance file.

Each view also carries its own frame proportion — 1 : 1.4 for the tall
installation shots, 4 : 5 for the product plate, landscape for the rim and
square for the base. One ratio cannot serve a 99 cm planter and a close-up of
a rim without stranding either the feet or half the frame.

**Rights — resolved.** The listing names **Jungle Flora as the seller**.
emedelynas.lt is a marketplace, and these are the client's own listings
carrying their own photography, not a third party's. Worth one line of
confirmation before publication, but it is no longer an open risk, and the
frames are labelled "Jungle Flora / listing" rather than "retail listing".

The same marketplace carries listings for Big Ben Tower, Siena, Siena Kubo,
Grand Wall and Pixie — each with its own studio set. Several of the thinner
pages ahead are no longer thin.

---

## 4. Wiring

The client-side router each page carries is now a slug → page map rather than
a single hard-coded `if`. Adding the next collection page is one entry, not an
edit to eight files. `wire_site.py` rewrites it across every page, adds the
"View collection" link to the index card, and sets `detail` in
`JunglePots-collections-data.json`.

The index card's "Enquire" mailto is kept alongside the new link.

---

## 5. Housekeeping

The Big Ben page carried **nine identical copies** of the specification-drawing
style block and nine of its animation script — `build_drawing.py` had been run
nine times against an already-built page. The Tower Bridge build keeps one of
each; the page is 57 KB against Big Ben's 76 KB, with a longer drawing in it.
Big Ben itself is untouched and still carries the duplicates — worth clearing
when its own drawing is next revisited.

---

## 6. Verified

Tower Bridge, the collection index and the homepage, at 1920 / 1440 / 1024 /
768 / 390, with motion and with reduced motion forced: no page or console
errors beyond the offline font request, no horizontal overflow, no broken
images, no element left below full opacity, and every stroke dash offset
resolved to 0.

Every touch-target and `aria-current` observation the checker reports is
present identically on Big Ben Tower — they are site-wide chrome behaviours,
not new here. Two are worth a pass of their own:

* the breadcrumb link is 17.6 px tall and the footer links 38 px, both under
  the 44 px minimum above 700 px;
* `aria-current="page"` appears twice per inner page — once in the header nav
  and once in the mobile menu. The chrome handoff claims one per page; it is
  one per navigation. Correct as markup, wrong in that document.

---

## 7. What this establishes for the remaining collections

The pipeline is now: cut → plate → `spec_drawing.py` → transform the Big Ben
page → `wire_site.py` → `verify.py`. What changes per collection is evidence,
not code.

Of the eleven remaining, **Siena, Siena Kubo, Grand Wall and Garden** have
single-object isolated views and can be drawn this way. **Dawn, Pixie, Cube
Shelf and the three Riversides** are photographed as groups of three or four,
which trace to a group silhouette that cannot carry dimension arrows; those
pages get a full-width schedule and no drawing. **Bar Planter** has no
isolated view and no schedule at all, and becomes an enquiry-led page.
