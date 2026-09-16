#!/usr/bin/env python3
"""Build the Pixie collection page.

Derived from the Riverside Base page.

**The capacity column is the A dimension with the unit changed.** Pixie is a
cube, so its volume is fixed by one number and there is no convention to argue
about. A 150 mm cube encloses 3.4 L; the catalogue prints 15 L. A 170 prints
17 L against 4.9. A 200 prints 20 against 8.0. A 230 prints 23 against 12.2.
Every printed figure is exactly the A dimension in centimetres with "cm"
swapped for "L".

That makes Pixie the one place in this catalogue where the capacity error is
unambiguous rather than a matter of which convention was used. Worth carrying
into the same conversation as the Riverside family, because it suggests the
capacity column was assembled by hand rather than computed.

The page prints the catalogue table unchanged and shows the enclosed volume of
the box beside it, labelled as geometry rather than as a planting capacity.

**Pixie has no photograph.** Every other collection has at least one project or
context image. Pixie appears only on the specification page, as two small
isolated renders: one cube and a group of four. No project, no interior, no
detail, no scale reference. It is the least expensive item in the range and the
one most likely to be ordered in quantity, and there is nothing to show it
with. Two views, and the page says why.

**The catalogue's own mask carries its dimension arrows.** `p26-5` is the alpha
for `p26-4`, but the drawn A/B/C arrows are in it as thin strokes. The cube
component is 91007 px and the next largest is 856, so taking the largest
connected component alone drops every arrow and leaves a clean isolated cube.

`interior=True` is essential here: without it the open top reads as a solid
hexagon. With it the rim comes back and the cube reads as a box.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-pixie.html"
DRAWING = Path("/home/claude/tb/px-drawing.svg")
ASSETS = Path("/home/claude/tb/px-assets")

# model, A mm, printed capacity L, enclosed volume of the box in L
MODELS = [("Pixie 150", 150, 15, "3.4"),
          ("Pixie 170", 170, 17, "4.9"),
          ("Pixie 200", 200, 20, "8.0"),
          ("Pixie 230", 230, 23, "12.2")]

VIEWS = [
    ("product", "collection-assets/pixie-product.png",
     "An isolated Pixie planter: a small steel cube, open at the top, with a "
     "thin folded wall",
     "ISOLATED PRODUCT", "CATALOGUE 26", "1/1"),
    ("sizes", "collection-assets/pixie-four-sizes.png",
     "The four Pixie sizes together, isolated: cubes of 150, 170, 200 and "
     "230 mm",
     "FOUR SIZES", "CATALOGUE 26", "16/9"),
]

LABELS = [("product", "Product"), ("sizes", "Four sizes")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    return "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td>%d L*</td></tr>' % (m, a, a, a, a, a, a, cap)
        for m, a, cap, _ in MODELS)


def main():
    s = (SRC / "junglepots-riverside-base.html").read_text(encoding="utf-8")

    s = s.replace("<title>Riverside Base | JunglePots</title>",
                  "<title>Pixie | JunglePots</title>")
    s = s.replace("<span>Riverside Base</span>", "<span>Pixie</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img isolated" src="%s" alt="%s" width="1000" height="1000"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">13 / SMALL PLANTERS</p><h1 id="collection-title">Pixie</h1><p class="description">The smallest thing in the range. Four open steel cubes from 150 to 230 mm, folded from the same sheet as everything else here and finished the same way — for a desk, a windowsill, or a run of them along a counter.</p><div class="hero-facts"><span>Galvanized steel</span><span>Open cube</span><span>Four sizes, 150–230</span><span>Smallest in the range</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the four sizes ↓</a><p class="small hero-note">The printed capacity column is the A dimension with the unit changed. Both are shown below.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    check = "".join(
        '<tr><th scope="row">%s</th><td>%d L</td><td>%s L</td></tr>'
        % (m.replace("Pixie ", ""), cap, geo) for m, a, cap, geo in MODELS)
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
        '<figcaption>Traced from the catalogue’s isolated product / not to '
        'scale / one drawing serves all four sizes. A true cube, open at the '
        'top — A, B and C are equal at every size.</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">PIXIE / FOUR SIZES</p>'
        '<table class="compare"><caption class="sr-only">Pixie catalogue '
        'specifications, four sizes</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">C</span> '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Capacity</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, page 26. A cube at every '
        'size, open at the top. Pixie is the only collection in the range with '
        'no photograph beyond these two isolated views — no project, no '
        'interior, no detail and nothing to give it scale.</p>'
        '<details open class="verification"><summary>* The capacity column is '
        'the A dimension with the unit changed</summary>'
        '<table class="compare"><thead><tr><th scope="col">Model</th>'
        '<th scope="col">Printed</th>'
        '<th scope="col">Volume of the box</th></tr></thead>'
        '<tbody>' + check + '</tbody></table>'
        '<p>A cube’s volume is fixed by a single number, so there is no '
        'convention to argue about here. A 150 mm cube encloses 3.4 L; the '
        'catalogue prints 15 L beside it. The printed figure is the A '
        'dimension in centimetres with <em>cm</em> swapped for <em>L</em>, on '
        'all four rows — 15, 17, 20, 23.</p>'
        '<p>Nothing has been substituted. The right-hand column is the '
        'enclosed volume of the box, which is geometry rather than a planting '
        'capacity: it takes no account of wall thickness, drainage or the '
        'freeboard a planted pot needs. Request the usable volumes.</p>'
        '<p>This is the one place in the catalogue where a capacity is '
        'unambiguously wrong rather than ambiguously derived, which is worth '
        'raising alongside the <a class="text-link" '
        'href="junglepots-riverside-flow.html">Riverside</a> figures rather '
        'than separately.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace('<div><dt>Base</dt><dd>Sits on the floor</dd></div>'
                  '<div><dt>Wheels</dt><dd>Hidden, optional</dd></div>',
                  '<div><dt>Form</dt><dd>Open cube, no lid</dd></div>'
                  '<div><dt>Base</dt><dd class="absent">Not stated</dd></div>')
    s = s.replace(
        "Riverside Base is photographed only in the dark grey shown here — in "
        "the studio, and in two real installations at CYBERCITY. No source "
        "names the colour, and no other finish is illustrated for this "
        "collection.",
        "Pixie is illustrated only in the dark grey of these two small "
        "renders. No source names the colour, and there is no photograph of "
        "this collection in any finish, in any setting.")
    s = s.replace(
        "weight, drainage and the hidden wheel option all require "
        "confirmation — the wheels are offered in the catalogue text and "
        "appear in none of its photographs.",
        "weight, drainage and whether these have any base detail at all "
        "require confirmation — at this size the catalogue shows no feet, no "
        "drainage and no underside.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/siena-kubo.png" alt="Isolated Siena Kubo '
        'planter, a square volume" width="880" height="660" loading="lazy">'
        '<details><summary><span>Siena Kubo<small>The same cube, floor '
        'scale.</small></span><span>+</span></summary><p>Three cubes at 35, 44 '
        'and 54 cm, with a hidden wheels option. No capacity is published for '
        'that collection at all.</p><a href="junglepots-siena-kubo.html" '
        'class="text-link">View collection <span>↗</span></a></details>'
        '</article><article><img src="related-assets/riverside-base.png" '
        'alt="Isolated Riverside Base planter, a plain cylinder" width="880" '
        'height="660" loading="lazy"><details><summary><span>Riverside Base'
        '<small>The same idea, round.</small></span><span>+</span></summary>'
        '<p>Three plain cylinders from 300 mm up. Its capacity column mostly '
        'checks out, which is what makes this one stand out.</p><a '
        'href="junglepots-riverside-base.html" class="text-link">View '
        'collection <span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Riverside Base</option>",
                  "<option>Pixie</option><option>Riverside Base</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("hero.classList.toggle('isolated',"
                  "['sizes'].includes(b.dataset.view))",
                  "hero.classList.toggle('isolated',true)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:[^;]*;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:1/1;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:800px)"
               "{#jp-detail-review .hero-img{aspect-ratio:1/1}}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:1/1}}\n</style>", s)

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
