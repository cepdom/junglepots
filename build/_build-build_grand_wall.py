#!/usr/bin/env python3
"""Build the Grand Wall collection page.

Derived from the Dawn page.

**The missing capacity is genuinely missing.** The catalogue publishes none
for this collection, and neither does any of the six Jungle Flora listings --
where Dawn's and Siena's both carry "naudingas turis", every Grand Wall
listing stops at the dimensions. So this is not a transcription gap that a
second source can close: nobody has published it. That is worth stating
plainly rather than leaving as an empty cell, and it is a different finding
from Siena (published, and wrong) or Dawn (published, and right).

**The letters run the other way.** The catalogue photographs Grand Wall almost
front-on with its long face to camera, so the near corner of the rim falls at
the right-hand end and the long span is the *left* edge. `spec_drawing.py`
takes its letters in draw order, so A -- the length -- is passed second here.
Nothing about the drawing code changed; the call did.

**The first real exterior photograph in the whole set.** View 01 is a roof
terrace: decking, sky, ornamental grasses, and a Grand Wall in a pale green
that is not the dark grey everything else is photographed in. The homepage
claims "interior, exterior and landscape projects" and until now every
collection page has shown interiors.

Six listings exist for three models -- two each, same dimensions and same
price. Worth telling the client; it is their storefront, not a page problem.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-grand-wall.html"
DRAWING = Path("/home/claude/tb/gw-drawing.svg")
ASSETS = Path("/home/claude/tb/gw-assets")

# model, A length, B depth, C height
MODELS = [("900", 900, 420, 740),
          ("1400", 1400, 420, 740),
          ("1900", 1900, 420, 740)]

VIEWS = [
    ("terrace", "collection-assets/grand-wall-terrace.jpg",
     "A Grand Wall planter in a pale green finish on a roof terrace, planted "
     "with ornamental grasses, decking and sky behind it",
     "IN CONTEXT / ROOF TERRACE", "JUNGLE FLORA / LISTING", "3/2"),
    ("planted", "collection-assets/grand-wall-planted.jpg",
     "A Grand Wall planter planted with broad-leaved foliage against a moss "
     "wall",
     "IN USE / PLANTED", "JUNGLE FLORA / LISTING", "3/2"),
    ("product", "collection-assets/grand-wall-isolated.png",
     "Isolated Grand Wall planter, a long low trough with rounded ends on feet",
     "ISOLATED PRODUCT", "CATALOGUE 26", "16/9"),
    ("length", "collection-assets/grand-wall-full-length.jpg",
     "An empty Grand Wall planter seen along its full length, showing the "
     "folded panel seams and the feet beneath",
     "FULL LENGTH / FEET", "JUNGLE FLORA / LISTING", "3/2"),
    ("detail", "collection-assets/grand-wall-detail.jpg",
     "Close view of a planted Grand Wall, showing the rounded end and the "
     "folded seam between panels",
     "ROUNDED END / SEAM", "JUNGLE FLORA / LISTING", "1/1"),
]

LABELS = [("terrace", "In context"), ("planted", "In use"),
          ("product", "Product"), ("length", "Full length"),
          ("detail", "Detail")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    return "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td></tr>' % (m, a, a, b, b, c, c)
        for m, a, b, c in MODELS)


def main():
    s = (SRC / "junglepots-dawn.html").read_text(encoding="utf-8")

    s = s.replace("<title>Dawn | JunglePots</title>",
                  "<title>Grand Wall | JunglePots</title>")
    s = s.replace("<span>Dawn</span>", "<span>Grand Wall</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1500" height="998"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">07 / RECTANGULAR PLANTERS</p><h1 id="collection-title">Grand<br>Wall</h1><p class="description">A trough long enough to divide a room, at one section and three lengths. Rounded ends and a continuous folded face, so it reads as a wall rather than a box.</p><div class="hero-facts"><span>Galvanized steel</span><span>Indoor / outdoor</span><span>Three lengths, one section</span><span>Up to 1900 mm</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three lengths ↓</a><p class="small hero-note">No capacity is published for this collection, by the catalogue or by any listing.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    pre, _, post = cut(s, '<section id="dimensions"', "</section>")
    spec = (
        '<section id="dimensions" class="wrap space"><div class="section-top">'
        '<p class="eyebrow">01 / SPECIFICATION</p>'
        '<span class="eyebrow">FORM / PROPORTION / VOLUME</span></div>'
        '<div class="section-heading"><h2>Dimensions &amp; variants.</h2>'
        '<div class="units" aria-label="Dimension units">'
        '<button data-unit="mm" aria-pressed="true">mm</button>'
        '<button data-unit="cm" aria-pressed="false">cm</button></div></div>'
        '<div class="spec-grid"><figure class="drawing">' + svg +
        '<figcaption>Traced from catalogue photography / not to scale / one '
        'drawing serves all three lengths</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">GRAND WALL / THREE LENGTHS</p>'
        '<table class="compare"><caption class="sr-only">Grand Wall catalogue '
        'specifications, three lengths</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Length '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Depth '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">C</span> Height '
        '<span class="unit">mm</span></th></tr></thead>'
        '<tbody>' + rows() +
        '<tr><th scope="row">Capacity</th>'
        '<td colspan="3" class="absent">Not published anywhere*</td></tr>'
        '</tbody></table>'
        '<p class="small">Source: supplied catalogue, page 26, confirmed '
        'dimension for dimension by Jungle Flora’s listings. A length, B '
        'depth, C height. The rounded ends are clear in the photography but '
        'fall below what the catalogue crop can resolve, so the drawing '
        'squares them.</p>'
        '<details open class="verification"><summary>* Nobody has published a '
        'capacity for Grand Wall</summary><p>The catalogue gives none. '
        'Neither does any of the six Jungle Flora listings — where Dawn '
        'and Siena both carry a usable volume, every Grand Wall listing stops '
        'at the dimensions. So this is not a transcription gap a second source '
        'can close.</p><p>Nothing has been derived. The external box of the '
        '1900 is 590 L, which is not its planting volume by any margin worth '
        'guessing at. Request the usable volume before specifying.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace(
        "Dawn is photographed throughout in a dark grey close to Anthracite "
        "7016. The listing offers any RAL shade, but does not say which one "
        "the photography shows.",
        "Grand Wall is the only collection photographed in two finishes: the "
        "studio and moss-wall views show the usual dark grey, and the roof "
        "terrace shows a pale sage green. That may be Pale Green 6021 from "
        "the swatches above, but neither source names it.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        """<div class="related-grid"><article><img src="related-assets/siena.png" alt="Isolated Siena planter, a rectangular trough" width="880" height="660" loading="lazy"><details><summary><span>Siena<small>The same idea, at desk scale.</small></span><span>+</span></summary><p>Three models from 65 to 95 cm long. The catalogue and the listing disagree about its capacity by a factor of ten — both figures are shown on that page.</p><a href="#inquiry" class="text-link" data-related="Siena">Enquire about Siena <span>↗</span></a></details></article><article><img src="related-assets/siena-kubo.png" alt="Isolated Siena Kubo planter, a square volume" width="880" height="660" loading="lazy"><details><summary><span>Siena Kubo<small>The point, rather than the line.</small></span><span>+</span></summary><p>Three cubes: 35, 44 and 54 cm. Hidden wheels option. No capacity published for that collection either.</p><a href="#inquiry" class="text-link" data-related="Siena Kubo">Enquire about Siena Kubo <span>↗</span></a></details></article></div></section>""",
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Dawn</option><option>Siena</option>",
                  "<option>Grand Wall</option><option>Dawn</option>"
                  "<option>Siena</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['facets'].includes(b.dataset.view)",
                  "['detail'].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:1/1;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:3/2;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:3/2}}\n</style>", s)

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
