#!/usr/bin/env python3
"""Build the Garden collection page.

Derived from the Grand Wall page.

**One photograph, three views.** Garden is the first collection with no
listing anywhere -- I enumerated all 21 Jungle Flora metal-planter listings on
emedelynas and Garden, Cube Shelf and Bar Planter are absent, and a search of
jungleflora.lt returns nothing either. So the page rests on a single catalogue
photograph from page 18. Rather than run the single-image path, the page
carries three views cut from that one frame: the isolated tray, the corner
ring, and the cap nut over the rolled edge. The source line says CATALOGUE 18
on all three and the detail captions say DETAIL OF THE SAME FRAME, so nobody
reads it as three shoots.

That crop is worth the trouble. At full resolution the black shapes resolve
into the actual suspension mechanism -- a dome cap nut on the tray face, a
bolt through the corner, a closed ring beneath -- which is the one thing a
specifier needs to see on a hanging product and the one thing the isolated
view is too small to show.

**The absence here is a safety absence.** Siena's capacity was published and
wrong; Dawn's was published and right; Grand Wall's was published nowhere.
Garden's missing number is the safe working load of a tray hung from a
concrete ceiling, and alongside it the tray height and the capacity are
missing too. Three empty rows and a disclosure that derives nothing: the dead
load of 2.2 m of wet substrate is not a figure to estimate from a photograph.

**Plan mode in the tracer.** Garden is shown in plan-ish perspective with no
vertical dimension published, so `spec_drawing.build` is called with
`mode='plan'`: two letters, and the extreme vertices of the whole silhouette
rather than the top band, because the top band of a flat tray is a single
edge and both arrows collapsed onto one corner.

The two suspension rings hang below the tray and the tracer turned them into
ragged notches on the near-left corner. They are masked out of the source
before tracing -- a plan outline has no business carrying a drooping ring --
and the caption says so, with view 02 showing what was left out.

**A real bug, inherited.** Every derived page since Tower Bridge reads
`hero.style.aspectRatio=v[5]` from a five-element array, so the per-view
aspect ratios have never applied. Fixed here and patched across the family.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-garden.html"
DRAWING = Path("/home/claude/tb/ga-drawing.svg")

# model, A length mm, B depth mm, suspension points
MODELS = [("X1", 570, 220, 4),
          ("X2", 1110, 220, 4),
          ("X3", 1650, 220, 4),
          ("X4", 2200, 220, 6)]

VIEWS = [
    ("product", "collection-assets/garden-isolated.png",
     "Isolated Garden tray, a long shallow steel tray with a cap nut at each "
     "corner and a suspension ring beneath",
     "ISOLATED PRODUCT", "CATALOGUE 18", "2/1"),
    ("suspension", "collection-assets/garden-suspension.png",
     "Close view of a Garden corner showing the black suspension ring beneath "
     "the tray and the dome cap nut on the tray face above it",
     "SUSPENSION RING / CORNER", "CATALOGUE 18 / SAME FRAME", "2/1"),
    ("edge", "collection-assets/garden-edge.png",
     "Close view of the rolled edge of a Garden tray with two dome cap nuts "
     "on its face",
     "ROLLED EDGE / CAP NUTS", "CATALOGUE 18 / SAME FRAME", "2/1"),
]

LABELS = [("product", "Product"), ("suspension", "Suspension"),
          ("edge", "Edge")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    out = "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td>%d</td></tr>' % (m, a, a, b, b, n)
        for m, a, b, n in MODELS)
    for label in ("Tray height", "Capacity", "Safe working load"):
        star = "*" if label == "Safe working load" else ""
        out += ('<tr><th scope="row">%s</th>'
                '<td colspan="3" class="absent">Not published%s</td></tr>'
                % (label, star))
    return out


def main():
    s = (SRC / "junglepots-grand-wall.html").read_text(encoding="utf-8")

    s = s.replace("<title>Grand Wall | JunglePots</title>",
                  "<title>Garden | JunglePots</title>")
    s = s.replace("<span>Grand Wall</span>", "<span>Garden</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img isolated" src="%s" alt="%s" width="1600" height="800"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">08 / SUSPENDED SYSTEMS</p><h1 id="collection-title">Garden</h1><p class="description">A planting tray that hangs. Four lengths at one depth, carried on a ring at each corner — six on the longest — from chain or steel cable anchored into a concrete ceiling.</p><div class="hero-facts"><span>Galvanized steel</span><span>Ceiling-suspended</span><span>Four lengths, one depth</span><span>Up to 2200 mm</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the four lengths ↓</a><p class="small hero-note">No safe working load is published for this collection. It hangs from a ceiling; ask for one before specifying.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    pre, _, post = cut(s, '<section id="dimensions"', "</section>")
    spec = (
        '<section id="dimensions" class="wrap space"><div class="section-top">'
        '<p class="eyebrow">01 / SPECIFICATION</p>'
        '<span class="eyebrow">FORM / PROPORTION / SUSPENSION</span></div>'
        '<div class="section-heading"><h2>Dimensions &amp; variants.</h2>'
        '<div class="units" aria-label="Dimension units">'
        '<button data-unit="mm" aria-pressed="true">mm</button>'
        '<button data-unit="cm" aria-pressed="false">cm</button></div></div>'
        '<div class="spec-grid"><figure class="drawing">' + svg +
        '<figcaption>Traced from catalogue photography / not to scale / one '
        'drawing serves all four lengths. The rings hang below the tray and '
        'are left out of the plan outline; view 02 shows one.</figcaption>'
        '</figure>'
        '<div class="schedule">'
        '<p class="eyebrow">GARDEN / FOUR LENGTHS</p>'
        '<table class="compare"><caption class="sr-only">Garden catalogue '
        'specifications, four lengths</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Length '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Depth '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Rings</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, pages 18–19 and 26. A '
        'length, B depth — the catalogue publishes two dimensions and no '
        'third, so how deep the tray is remains unknown. Chain or steel cable '
        'suspension with rings and carabiners, anchored into a concrete '
        'ceiling, is described but not specified.</p>'
        '<details open class="verification"><summary>* No load rating is '
        'published for a product that hangs from a ceiling</summary>'
        '<p>The catalogue describes the suspension — chain or steel cable, '
        'rings and carabiners, concrete-ceiling anchors — and gives no safe '
        'working load, no fixing specification, no steel thickness and no '
        'filled weight. Garden has no retail listing anywhere, on Jungle '
        'Flora’s own storefront or elsewhere, so there is no second source to '
        'close the gap.</p>'
        '<p>Nothing has been derived. The dead load of 2.2 m of wet substrate '
        'is not a figure to estimate from a photograph. Request the safe '
        'working load, the fixing specification and the filled weight from '
        'the manufacturer, and have the ceiling fixing checked by a '
        'structural engineer, before this is specified.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace("<dt>Base</dt><dd>Integrated adjustable feet</dd>",
                  "<dt>Suspension</dt><dd>Chain or steel cable</dd>")
    s = s.replace(
        "Grand Wall is the only collection photographed in two finishes: the "
        "studio and moss-wall views show the usual dark grey, and the roof "
        "terrace shows a pale sage green. That may be Pale Green 6021 from "
        "the swatches above, but neither source names it.",
        "Garden is photographed once, in a mid grey the catalogue does not "
        "name. The rings and cap nuts are black in that frame; whether they "
        "follow the tray’s finish or are supplied black is not stated.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/cube-shelf.png" alt="Isolated Cube Shelf frame, '
        'a square-profile steel cube" width="880" height="660" '
        'loading="lazy"><details><summary><span>Cube Shelf<small>The same '
        'idea, standing.</small></span><span>+</span></summary><p>Three '
        'frames — 30, 40 and 50 cm — in 20 × 20 mm square profile with a '
        'sheet shelf. Where Garden hangs from the slab, this one carries a '
        'planter at height without touching it.</p><a href="#inquiry" '
        'class="text-link" data-related="Cube Shelf">Enquire about Cube Shelf '
        '<span>↗</span></a></details></article><article><img '
        'src="related-assets/grand-wall.png" alt="Isolated Grand Wall '
        'planter, a long low trough" width="880" height="660" '
        'loading="lazy"><details><summary><span>Grand Wall<small>The same '
        'line, on the floor.</small></span><span>+</span></summary><p>Three '
        'lengths to 1900 mm at one section. No capacity is published for that '
        'collection either.</p><a href="junglepots-grand-wall.html" '
        'class="text-link">View collection <span>↗</span></a></details>'
        '</article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Grand Wall</option><option>Dawn</option>",
                  "<option>Garden</option><option>Grand Wall</option>"
                  "<option>Dawn</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    # the ratio is element 4 of a five-element array; every page since Tower
    # Bridge has read element 5 and quietly applied nothing
    s = s.replace("hero.style.aspectRatio=v[5]", "hero.style.aspectRatio=v[4]")
    s = s.replace("['detail'].includes(b.dataset.view)",
                  "['suspension','edge'].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    # the template sets .hero-img at three container breakpoints -- base, 800
    # and 600 -- and the trailing override block has only ever covered base
    # and 600, so every page in this family has shown its hero in the
    # template's portrait ratio between 600 and 800. All three are set here.
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:3/2;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:2/1;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:800px)"
               "{#jp-detail-review .hero-img{aspect-ratio:2/1}}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:2/1}}\n</style>", s)

    OUT.write_text(s, encoding="utf-8")
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
