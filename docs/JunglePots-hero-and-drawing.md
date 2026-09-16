# Homepage and linework — design handoff

Covers the new-hero homepage (`junglepots-homepage-hero.html`) and the drawn
linework that now runs through the site. The earlier homepage is untouched at
`junglepots-homepage.html` so the two can be compared directly.

---

# 1. Homepage

## Hero

The approved full-width hero band is kept. What changed is the photograph: a
roof-terrace project, replacing an office corridor in which the planter was a
small element in a busy frame.

The hero states "Planters for interior, exterior and landscape projects", and
every other photograph on the page is an interior. This is the only evidence
on the homepage for two thirds of that claim.

Cropped at `50% 64%` so the balustrade and planters hold the band rather than
the sky.

## Section 01 — the forms, drawn

One section, two columns: the two Sculptural collections drawn as line
silhouettes on the left, "Considered as part of the architecture" and its copy
on the right. Above both, the section label row carries `01 / THE APPROACH`
left and `SILHOUETTES / TRACED FROM CATALOGUE PHOTOGRAPHY` right — the same
label-left / label-right rhythm every other section uses, with the mono note
promoted to the section's secondary label rather than floating beside the
drawings.

The drawing is the argument that statement is making, which is why the two sit
side by side rather than stacked, and why this is in section 01 rather than in
the hero.

This is a deliberate departure from the design guide's intro spec ("index label
left; statement and paragraph on right", 1:2 grid). The grid is now 1 : 1.1 with
a 7% gap, and the index label has moved up into its own rule-bounded row.

Below 900px the two columns stack with the statement first and the drawings
following as its evidence — set with explicit grid placement, so the DOM order
already reads statement-first for screen readers. The secondary label hides
below 900px, following the guide's existing rule.

**Where the outlines come from.** Traced from the alpha channel of the
catalogue's own isolated product photographs — the same cutouts used on the
collection index — then reduced with a Douglas-Peucker simplification at a 4 px
tolerance. These are prismatic objects, so a coarse tolerance recovers their
real straight edges rather than smoothing them away. Nothing is modelled,
redrawn or idealised.

They retain the perspective of the source photograph, so they are silhouettes
rather than orthographic elevations, and the note says so.

Both forms are catalogued at 99 cm and draw at the same height. No dimension is
printed, so Big Ben Tower's unresolved 99 / 90 cm question is not surfaced as a
claim.

**Motion.** The two forms draw themselves once when section 01 is first
scrolled to, 260 ms apart, then their names fade in. Progressive enhancement
behind a 4.2 s failsafe: with reduced motion, no JavaScript or no SVG geometry
API, they render complete and static.

## Photography

From the client's own Jungle Flora site, where the source filenames identify
the products:

| File | Source | Used for |
|---|---|---|
| `hero-assets/terrace-project.jpg` | `tesonet-terasa-6` | Hero band |
| `hero-assets/big-ben-project-hero.jpg` | `metal-bigben` | Selected collection 01 — Big Ben Tower |
| `hero-assets/tower-bridge-project-hero.jpg` | `metal-towerbridge` | Selected collection 02 — Tower Bridge |
| `hero-assets/riverside-project-hero.jpg` | `metal-riverside` | **Currently unused** — held for a Riverside collection page |

Downscaled (1000–1920 px) for the prototype; the production build should use
the originals.

**Two things the page does not claim.** The client project behind the hero
photograph is not named, and its planters are not attributed to a collection —
the photograph does not identify one. Both need client confirmation before
publication; the real sources are in the provenance file.

**Selected collections.** The second card was Riverside Base; it is now Tower
Bridge. The homepage therefore features exactly the two Sculptural collections
that section 01 draws, in the catalogue's own order (Big Ben Tower 01, Tower
Bridge 02), photographed in the same red-brown finish. The drawings and the
photographs are now the same two objects.

The original card also carried stale `data-collection="Riverside Base"`
attributes behind a "Riverside Flow" heading; those are gone with the swap.
Everything on the page — headings, preview panel, index shortcuts and ARIA
labels — now names Tower Bridge consistently.

The red-brown finish in this photography still has no catalogue colour code,
as the catalogue analysis records.

---

# 2. Specification drawing (Big Ben Tower detail page)

The `Dimensions & variants` panel shows a line drawing rather than a flat
catalogue photograph with arrows over it, so the A / B / C letters read
directly against the A / B / C rows in the schedule table beside it.

## What is drawn

The outer silhouette only, traced the same way and at the same tolerance as the
homepage forms — so the homepage and the specification panel speak one drawing
language.

Interior edges were built and then removed on review. An intermediate version
drew the rim quad and the front/side corner, recovered by clustering luminance
into flat-shaded faces; the recessed slot between the legs could never be
resolved cleanly, because it sits in shadow at the resolution the catalogue
supplies. A pure outline is both more confident and more honest. If
higher-resolution product photography or a CAD outline is supplied later, a
fuller drawing becomes possible.

## Placement and weight

The drawing sits directly on the page — no plate, no frame. Stroke weight uses
`vector-effect: non-scaling-stroke`, so the 2.2 px line stays crisp at every
breakpoint instead of thinning as the drawing scales down. Arrowheads use
`userSpaceOnUse` so they scale with the drawing, as they should.

## Dimension letters

A across the top rear edge, B along the receding top edge, C overall height —
the catalogue's own convention, preserved, anchored to rim corners measured
from the drawing itself. **No dimension value is drawn.** The numbers stay in
the schedule table with their source page and verification status, including
the unresolved height note.

The caption reads "Traced from catalogue photography / not to scale" rather
than "Catalogue drawing", because that is now what it is.

---

# 3. Why not 3D

Raised and set aside deliberately. The catalogue analysis lists CAD/BIM among
the missing fields, and the schedule gives only overall A/B/C: the step
proportions on Big Ben Tower and the arch radius on Tower Bridge are not
dimensioned anywhere. Modelling either would mean inventing geometry a
specifier could measure off. The forms that *could* be modelled truthfully
(Siena Kubo, Pixie, the Riverside cylinders) are boxes and tubes.

3D belongs on the collection detail pages as a specification tool, with
downloadable Revit / IFC / DWG, once JunglePots supplies real geometry. That is
a content request to make of the client, and a genuinely valuable one for this
audience.

---

# 4. Frame treatment

Three treatments, chosen by what each image is:

| Context | Frame | Why |
|---|---|---|
| Collection index cards | plate tint, product sized to fill | a browsing grid needs each card to register as a discrete unit |
| Detail page product view | paper colour, product smaller with room around it | a single focused view reads as an object on the page, not a picture in a box |
| Rim / feet / leg joint | paper colour, full alpha cutout shown whole | the studio sweep is cut away rather than cropped out, so nothing is lost and the boundary is invisible |
| Project photography | full bleed | context images have no background of their own |

No white background remains anywhere in the build.

---

# 5. Verification

No console or page errors on any of the five pages, with motion on and with
reduced motion forced. Nothing is left below full opacity; no broken images;
all stroke dash offsets resolve to 0. No horizontal overflow at 1920, 1440,
1024, 768 or 390 px. The collection index still filters to four under Round,
specification disclosures open, and every view switcher loads its new source.

Build order: `build_refined.py`, then `build_hero.py`, then `drawing.py` →
`make_svg.py` → `build_drawing.py`. Supporting scripts: `cutout.py` (index
plates), `hero_plate.py` (detail product plate), `detail_cut.py` (construction
cutouts), `trace.py` (silhouettes). All included as `_build-*.py`.
