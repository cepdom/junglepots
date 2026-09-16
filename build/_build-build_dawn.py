#!/usr/bin/env python3
"""Build the Dawn collection page.

Derived from the Siena page. Three things are new here.

**A round form takes two letters, not three.** The catalogue gives Dawn a
diameter and a height and nothing else, because a cylinder has no receding top
edge to measure. `spec_drawing.py` now accepts a two-letter call and draws one
horizontal arrow across the widest point of the rim and one vertical. Drawing
a third would invent a dimension nobody published.

**A faceted form is traced but not straightened.** The straightening pass
exists to recover the true straight edges of a prismatic box. Dawn has none:
every break in its outline is a real facet, and straightening rounds them all
away into a blob. So `curved=True` keeps the fine trace as it stands, and the
facet breaks along the rim and base survive.

Interior edges are not drawn. The rim's inner ellipse is plainly visible to a
reader but the face-clustering pass recovers only fragments of it, so by the
rule the page has followed since Big Ben Tower, nothing is drawn rather than
something half-right.

**The data checks out, for once.** Every capacity in the catalogue (21 / 43 /
60 L) is confirmed by Jungle Flora's own listing for that model, and the
catalogue's own dimension diagram in the listing set reads 295 across and 300
high, which is the A / B convention exactly as transcribed. After Siena, that
is worth saying on the page rather than leaving as a silence.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-dawn.html"
DRAWING = Path("/home/claude/tb/dawn-drawing.svg")
ASSETS = Path("/home/claude/tb/dw-assets")

# model, A diameter, B height, capacity
MODELS = [("295", 295, 300, "21 L"),
          ("395", 395, 350, "43 L"),
          ("440", 440, 400, "60 L")]

VIEWS = [
    ("context", "collection-assets/dawn-three-sizes.jpg",
     "The three Dawn planters together against a moss wall, each planted",
     "IN CONTEXT / ALL THREE SIZES", "JUNGLE FLORA / LISTING", "1/1"),
    ("shelf", "collection-assets/dawn-on-shelf.jpg",
     "A Dawn planter standing on a Cube Shelf frame against a moss wall",
     "ON A CUBE SHELF FRAME", "JUNGLE FLORA / LISTING", "1/1"),
    ("product", "collection-assets/dawn-isolated.png",
     "Isolated Dawn planter, a faceted round vessel",
     "ISOLATED PRODUCT", "JUNGLE FLORA / LISTING", "1/1"),
    ("facets", "collection-assets/dawn-facets.jpg",
     "Close view of the folded facets of a Dawn planter and the rim above them",
     "FOLDED FACETS / RIM", "JUNGLE FLORA / LISTING", "3/2"),
]

LABELS = [("context", "In context"), ("shelf", "On a shelf"),
          ("product", "Product"), ("facets", "Facets")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    return "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td>%s</td></tr>' % (m, a, a, b, b, cap)
        for m, a, b, cap in MODELS)


def main():
    s = (SRC / "junglepots-siena.html").read_text(encoding="utf-8")

    s = s.replace("<title>Siena | JunglePots</title>",
                  "<title>Dawn | JunglePots</title>")
    s = s.replace("<span>Siena</span>", "<span>Dawn</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1400" height="1400"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">04 / ROUND PLANTERS</p><h1 id="collection-title">Dawn</h1><p class="description">A cylinder folded out of flat sheet, so that it is faceted rather than rolled. The facets catch light down one side and lose it on the next, which is the whole of the design.</p><div class="hero-facts"><span>Galvanized steel</span><span>Indoor / outdoor</span><span>Three catalogued sizes</span><span>21 / 43 / 60 L</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three models ↓</a><p class="small hero-note">Catalogue and listing agree on every figure for this collection.</p></div>
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
        '<figcaption>Traced from product photography / not to scale / one '
        'drawing serves all three models</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">DAWN / THREE MODELS</p>'
        '<table class="compare"><caption class="sr-only">Dawn catalogue '
        'specifications, three models</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Diameter '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Height '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Capacity</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, page 7. '
        'A across the rim, B height — two letters, because a cylinder has '
        'no third dimension to give.</p>'
        '<details open class="verification"><summary>Confirmed against a '
        'second source</summary><p>Every figure here is corroborated by '
        'Jungle Flora’s own listing for that model: 29.5 × 30 cm at '
        '21 L, 39.5 × 35 cm at 43 L, 44 × 40 cm at 60 L. The listing '
        'set also carries the manufacturer’s own dimension diagram, '
        'marked 295 across and 300 high, which is the A / B convention as '
        'transcribed.</p><p>This is the first collection where the two '
        'sources agree on everything. Siena’s capacities differ by a '
        'factor of ten, and Tower Bridge’s height by 9 cm.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material: the listing publishes three things the catalogue does not
    s = s.replace(
        "<div><dt>Custom colour</dt><dd>Available on enquiry</dd></div>",
        "<div><dt>Custom colour</dt><dd>Any RAL shade†</dd></div>"
        "<div><dt>Engraving</dt><dd>Logos and initials†</dd></div>"
        "<div><dt>Custom sizes</dt><dd>Made to dimension†</dd></div>"
        "<div><dt>Origin</dt><dd>Lithuania†</dd></div>")
    s = s.replace(
        "<summary>Material information &amp; specification limits</summary>",
        "<summary>† Material information &amp; specification limits"
        "</summary>")
    s = s.replace(
        "<p>The catalogue describes frost and UV resistance but supplies no "
        "test ratings.",
        "<p>The four items marked † come from Jungle Flora’s own "
        "listing, not from the supplied catalogue: powder coating in any RAL "
        "shade, logo and initial engraving, manufacture to custom dimensions, "
        "and Lithuanian origin. They are sales copy rather than a "
        "specification, so treat them as an opening position, not a "
        "guarantee.</p><p>The catalogue describes frost and UV resistance but "
        "supplies no test ratings.")
    s = s.replace(
        "Siena is photographed throughout in a dark grey close to Anthracite "
        "7016, but neither the catalogue nor the listing names the code used.",
        "Dawn is photographed throughout in a dark grey close to Anthracite "
        "7016. The listing offers any RAL shade, but does not say which one "
        "the photography shows.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        """<div class="related-grid"><article><img src="related-assets/cube-shelf.png" alt="Isolated Cube Shelf frames, three open square frames with shelves" width="880" height="660" loading="lazy"><details><summary><span>Cube Shelf<small>The frame Dawn stands on.</small></span><span>+</span></summary><p>Three frames: 30, 40 and 50 cm cubes in 20 × 20 mm square profile. The catalogue photographs it holding a Dawn planter — they are separate collections, and the second gallery view here shows the pairing.</p><a href="#inquiry" class="text-link" data-related="Cube Shelf">Enquire about Cube Shelf <span>↗</span></a></details></article><article><img src="related-assets/riverside-base.png" alt="Isolated Riverside Base planters, three cylinders" width="880" height="660" loading="lazy"><details><summary><span>Riverside Base<small>The cylinder, rolled rather than folded.</small></span><span>+</span></summary><p>Three diameters: 30, 40 and 60 cm. Hidden wheels optional. The BASE300 dimensions differ between the catalogue and the online listing — unresolved.</p><a href="#inquiry" class="text-link" data-related="Riverside Base">Enquire about Riverside Base <span>↗</span></a></details></article></div></section>""",
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Siena</option><option>Siena Kubo</option>",
                  "<option>Dawn</option><option>Siena</option>"
                  "<option>Siena Kubo</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['rim','feet'].includes(b.dataset.view)",
                  "['facets'].includes(b.dataset.view)")
    s = s.replace("['product','sizes'].includes(b.dataset.view)",
                  "b.dataset.view==='product'")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:4/3;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:1/1;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:1/1}}\n</style>", s)

    # the capacity table's own heading belongs to Siena only
    s = re.sub(r'<p class="eyebrow cap-head">.*?</table>', "", s, flags=re.S)

    # A squat drawing was being width-limited to 300 px while the tall towers
    # were height-limited to 430: the same object drawn wide came out half the
    # size. Cap the height and let the width take the column.
    s = s.replace("</body></html>", """<style>
#jp-detail-review .spec-drawing{height:auto;max-height:430px;max-width:100%}
@container detail (max-width:1000px)
  {#jp-detail-review .spec-drawing{max-height:360px}}
@container detail (max-width:520px)
  {#jp-detail-review .spec-drawing{max-height:280px}}
</style>
</body></html>""")

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
