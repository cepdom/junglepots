#!/usr/bin/env python3
"""Build the Siena collection page.

Derived from the Siena Kubo page, so the comparison schedule, the per-view
frame proportions and the letter-convention disclosure all come for free.

The reason this page matters more than its place in the running order:

**The catalogue's capacity column for Siena is wrong, and it can be shown.**

  catalogue page 24     7 L      17 L     43 L
  bounding box         87.8 L   128.3 L  179.6 L
  Jungle Flora listing 80 L     120 L    170 L   ("naudingas turis", usable)

The listing figures sit at 91 / 94 / 95 % of the external box, which is what a
thin-walled steel trough should give. The catalogue's do not sit anywhere
sensible -- and 7 / 17 / 43 are *exactly* Riverside Flow's 200 / 300 / 400
capacities from page 9. The column looks copied from another collection.

So the page publishes both, in a capacity table of their own, and says what it
thinks. It does not pick one silently, and it does not derive a third number.

Photography is Jungle Flora's own marketplace listing (the seller field on
emedelynas.lt reads "Jungle flora"), which also supplied Tower Bridge's.
There is no installed photograph of Siena anywhere: the moss-wall frame those
listings carry shows Siena Kubo cubes, not Siena troughs, so it is not used
here. The gallery leads with the isolated product instead, as the flexible
template directs when no project photograph exists.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-siena.html"
DRAWING = Path("/home/claude/tb/siena-drawing-listing.svg")
ASSETS = Path("/home/claude/tb/si-assets")

# model, A length, B depth, C height, catalogue L, listing usable L
MODELS = [("65", 650, 270, 500, "7 L", "80 L"),
          ("95", 950, 270, 500, "17 L", "120 L"),
          ("95H", 950, 270, 700, "43 L", "170 L")]

VIEWS = [
    ("product", "collection-assets/siena-isolated.png",
     "Isolated Siena planter, a rectangular trough with a folded rim",
     "ISOLATED PRODUCT", "JUNGLE FLORA / LISTING", "4/3"),
    ("sizes", "collection-assets/siena-three-sizes.png",
     "The three Siena models together, showing 65 and 95 at the same height "
     "and 95H taller",
     "ALL THREE MODELS", "JUNGLE FLORA / LISTING", "4/3"),
    ("rim", "collection-assets/siena-rim.jpg",
     "Close view of the folded rim and corner of a Siena trough, showing the "
     "sand-textured powder-coated finish",
     "FOLDED RIM / CORNER", "JUNGLE FLORA / LISTING", "3/2"),
    ("feet", "collection-assets/siena-feet.jpg",
     "Close view of an adjustable levelling foot under the corner of a Siena "
     "trough",
     "ADJUSTABLE FOOT", "JUNGLE FLORA / LISTING", "2/1"),
]

LABELS = [("product", "Product"), ("sizes", "Three models"),
          ("rim", "Rim"), ("feet", "Foot")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def dim_rows():
    return "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td></tr>' % (m, a, a, b, b, c, c)
        for m, a, b, c, _, _ in MODELS)


def cap_rows():
    return "".join(
        '<tr><th scope="row">%s</th><td class="absent">%s</td><td>%s</td></tr>'
        % (m, cat, lst) for m, _, _, _, cat, lst in MODELS)


def main():
    s = (SRC / "junglepots-siena-kubo.html").read_text(encoding="utf-8")

    s = s.replace("<title>Siena Kubo | JunglePots</title>",
                  "<title>Siena | JunglePots</title>")
    s = s.replace("<span>Siena Kubo</span>", "<span>Siena</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1200" height="900"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">08 / RECTANGULAR PLANTERS</p><h1 id="collection-title">Siena</h1><p class="description">A long, low trough on adjustable feet. Two lengths at one height and a third drawn taller — the collection for dividing a space rather than marking a point in it.</p><div class="hero-facts"><span>Galvanized steel</span><span>Indoor / outdoor</span><span>Three catalogued sizes</span><span>Adjustable feet</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three models ↓</a><p class="small hero-note">The catalogue and the manufacturer’s own listing disagree about capacity by a factor of ten. Both are shown below.</p></div>
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
        '<p class="eyebrow">SIENA / THREE MODELS</p>'
        '<table class="compare"><caption class="sr-only">Siena catalogue '
        'dimensions, three models</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Length '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Depth '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">C</span> Height '
        '<span class="unit">mm</span></th></tr></thead>'
        '<tbody>' + dim_rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, page 24. '
        'A length, B depth, C height — C is the vertical here, as on Big '
        'Ben Tower and Tower Bridge, but not as on Siena Kubo.</p>'
        '<p class="eyebrow cap-head">CAPACITY / TWO SOURCES, TEN TIMES APART</p>'
        '<table class="compare capacity"><caption class="sr-only">Siena '
        'capacity as published by the catalogue and by the manufacturer’s '
        'listing</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col">Catalogue*</th>'
        '<th scope="col">Usable volume*</th></tr></thead>'
        '<tbody>' + cap_rows() + '</tbody></table>'
        '<details open class="verification"><summary>* Which number to '
        'specify against</summary><p>The catalogue (page 24) publishes 7, 17 '
        'and 43 L. Jungle Flora’s own marketplace listing — they are the '
        'named seller on it — publishes 80, 120 and '
        '170 L as usable volume. The external boxes are 87.8, 128.3 and '
        '179.6 L, so the listing figures sit at 91–95 % of the box — '
        'what a thin-walled steel trough should give. The catalogue figures '
        'sit nowhere sensible.</p><p>They are also, exactly, Riverside '
        'Flow’s 200 / 300 / 400 capacities from page 9. The column looks '
        'copied from another collection. We publish both rather than choose, '
        'and nothing has been derived: please confirm which figure governs, '
        'and whether it is soil volume or liner volume.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace("<div><dt>Wheels</dt><dd>Hidden castors, optional</dd></div>",
                  "")
    s = s.replace(
        "Siena Kubo is photographed throughout in a dark grey close to "
        "Anthracite 7016, but the catalogue does not name the code used.",
        "Siena is photographed throughout in a dark grey close to Anthracite "
        "7016, but neither the catalogue nor the listing names the code used.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        """<div class="related-grid"><article><img src="related-assets/siena-kubo.png" alt="Isolated Siena Kubo planter, a square volume" width="880" height="660" loading="lazy"><details><summary><span>Siena Kubo<small>The same language, squared.</small></span><span>+</span></summary><p>Three cubes: 35, 44 and 54 cm. Hidden wheels option. No capacity is published for that collection at all — a different gap from this one.</p><a href="#inquiry" class="text-link" data-related="Siena Kubo">Enquire about Siena Kubo <span>↗</span></a></details></article><article><img src="related-assets/grand-wall.png" alt="Isolated Grand Wall planter, a long low trough on feet" width="880" height="660" loading="lazy"><details><summary><span>Grand Wall<small>The same idea, at room scale.</small></span><span>+</span></summary><p>Three lengths at one section: 90, 140 and 190 cm, all 42 × 74 cm. Capacity is not supplied for that collection either.</p><a href="#inquiry" class="text-link" data-related="Grand Wall">Enquire about Grand Wall <span>↗</span></a></details></article></div></section>""",
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Siena Kubo</option><option>Big Ben Tower</option>"
                  "<option>Tower Bridge</option>",
                  "<option>Siena</option><option>Siena Kubo</option>"
                  "<option>Big Ben Tower</option><option>Tower Bridge</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['rim'].includes(b.dataset.view)",
                  "['rim','feet'].includes(b.dataset.view)")
    s = s.replace("b.dataset.view==='product'",
                  "['product','sizes'].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:3/2;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:4/3;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:4/3}}\n</style>", s)

    # ---- the second table needs a little air above it --------------------
    s = s.replace("</body></html>", """<style>
#jp-detail-review .cap-head{margin-top:38px;padding-top:20px;
  border-top:1px solid var(--line)}
#jp-detail-review .capacity td{font-variant-numeric:tabular-nums}
</style>
</body></html>""")

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
