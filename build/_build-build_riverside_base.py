#!/usr/bin/env python3
"""Build the Riverside Base collection page.

Derived from the Riverside Rise page.

**The 30 x 35 / 30 x 25 conflict resolves itself arithmetically.** An earlier
session pinned a disagreement: the catalogue gives Riverside Base 300 as
30 x 35 cm, Jungle Flora's listing as 30 x 25 cm. Page 25 settles which is
consistent, without anyone having to measure anything:

  * the 400 is published at 40 x 35 cm and 43 L; a plain cylinder of those
    dimensions holds 44.0 L
  * the 600 is published at 60 x 60 cm and 169 L; a plain cylinder holds
    169.6 L
  * the 300 is published at 30 x 35 cm and 17 L; a plain cylinder holds 24.7 L

So two of the three rows are the plain cylinder volume of their own dimensions
to within a litre, and the third is not. The height that would give 17 L at
30 cm across is 24 cm -- and the listing says 25. The page states all of this
and changes nothing; which figure is right is the client's to confirm.

**And it sharpens the Riverside Flow contradiction.** This page demonstrates
that the catalogue's capacity method IS plain cylinder volume, at least here.
Riverside Flow 600 carries the same published A and B as Riverside Base 600 --
60 cm and 60 cm -- and a different capacity, 127 L against 169 L. The two pages
now point at each other.

**The best photography in the catalogue.** Pages 12 and 13 carry a full-page
studio shot and two real CYBERCITY installation photographs: a lobby with a
neon sign and tan armchairs, and a corridor. No extracted originals exist for
those two pages -- only the page renders -- so these three are cropped from the
render itself, which is stated in the provenance.

**Both isolated images ship with their own clipping mask** (p11-1 for p11-0,
p11-3 for p11-2), as on Cube Shelf and Riverside Rise. Three pages now.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-riverside-base.html"
DRAWING = Path("/home/claude/tb/rb-drawing.svg")
ASSETS = Path("/home/claude/tb/rb-assets")

# model, A diameter mm, B height mm, published capacity L,
# what a plain cylinder A across and B tall would hold
MODELS = [("Riverside Base 300", 300, 350, 17, "24.7"),
          ("Riverside Base 400", 400, 350, 43, "44.0"),
          ("Riverside Base 600", 600, 600, 169, "169.6")]

VIEWS = [
    ("cybercity", "collection-assets/riverside-base-cybercity.jpg",
     "A Riverside Base planter holding a tall plant in the CYBERCITY office "
     "lobby, beside tan and cream armchairs under a neon sign",
     "IN USE / CYBERCITY LOBBY", "CATALOGUE 13", "3/2"),
    ("corridor", "collection-assets/riverside-base-corridor.jpg",
     "A Riverside Base planter holding a large monstera at the end of a "
     "gallery corridor in the same building",
     "IN USE / CYBERCITY GALLERY", "CATALOGUE 13", "3/2"),
    ("moss", "collection-assets/riverside-base-moss-wall.jpg",
     "Three planted Riverside Base planters of different sizes against a "
     "preserved moss wall",
     "IN CONTEXT / MOSS WALL", "CATALOGUE 11", "1/1"),
    ("sizes", "collection-assets/riverside-base-three-sizes.png",
     "The three Riverside Base sizes isolated: plain cylinders with no legs "
     "and no visible base",
     "THREE SIZES", "CATALOGUE 11", "16/9"),
    ("planted", "collection-assets/riverside-base-planted.jpg",
     "A single large Riverside Base planted with a mature Strelitzia against "
     "a moss wall",
     "PLANTED / LARGEST SIZE", "CATALOGUE 12", "3/4"),
]

LABELS = [("cybercity", "In use"), ("corridor", "Gallery"),
          ("moss", "In context"), ("sizes", "Three sizes"),
          ("planted", "Planted")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    return "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span>%s</td>'
        '<td><span data-mm="%d">%d</span>%s</td>'
        '<td>%d L</td></tr>'
        % (m, a, a, "", b, b, "*" if m.endswith("300") else "", cap)
        for m, a, b, cap, _ in MODELS)


def main():
    s = (SRC / "junglepots-riverside-rise.html").read_text(encoding="utf-8")

    s = s.replace("<title>Riverside Rise | JunglePots</title>",
                  "<title>Riverside Base | JunglePots</title>")
    s = s.replace("<span>Riverside Rise</span>", "<span>Riverside Base</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1300" height="867"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">12 / ROUND PLANTERS</p><h1 id="collection-title">Riverside<br>Base</h1><p class="description">The cylinder with nothing under it. Three sizes, from a 300 mm pot beside a chair to a 600 mm floor planter that carries a mature Strelitzia, with an optional set of hidden wheels. It is the collection the catalogue photographs in real buildings rather than in the studio.</p><div class="hero-facts"><span>Galvanized steel</span><span>Sits on the floor</span><span>Three sizes, 300–600</span><span>Hidden wheels option</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three sizes ↓</a><p class="small hero-note">The 300’s published height is the one figure in this collection that does not reconcile with its own published capacity.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    check = "".join(
        '<tr><th scope="row">%s</th><td>%d</td><td>%s</td></tr>'
        % (m.replace("Riverside Base ", ""), cap, geo)
        for m, a, b, cap, geo in MODELS)
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
        'scale / one drawing serves all three sizes. No legs, no plinth and no '
        'visible base — A across the rim and B to the floor, as on the '
        'catalogue’s own diagram.</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">RIVERSIDE BASE / THREE SIZES</p>'
        '<table class="compare"><caption class="sr-only">Riverside Base '
        'catalogue specifications, three sizes</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Diameter '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Height '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Capacity</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, pages 11–13 and 25. A '
        'plain cylinder: the only collection in this range with no legs, no '
        'plinth and no stand. Hidden wheels are offered as an option and are '
        'not shown in any photograph.</p>'
        '<details open class="verification"><summary>* Two of these three '
        'rows check out exactly. The 300 does not</summary>'
        '<table class="compare"><thead><tr><th scope="col">Model</th>'
        '<th scope="col">Printed</th>'
        '<th scope="col">A × B as a cylinder</th></tr></thead>'
        '<tbody>' + check + '</tbody></table>'
        '<p>The 400 and the 600 are each the plain cylinder volume of their own '
        'published dimensions, to within a litre. The 300 is not: 30 × 35 cm '
        'would hold 24.7 L, half again as much as the 17 L printed beside '
        'it.</p>'
        '<p>The height that gives 17 L at 300 mm across is <strong>240 mm'
        '</strong>. <strong>Jungle Flora’s own listing gives the Riverside '
        'Base 300 as 30 × 25 cm</strong>, not 30 × 35. So the catalogue’s 350 '
        'is the single figure in this collection that does not reconcile, and '
        'the listing’s is the one that does.</p>'
        '<p>Nothing has been changed. The table above is the catalogue as '
        'printed. Confirm which height is correct before specifying.</p>'
        '</details>'
        '<details class="verification"><summary>And the same dimensions appear '
        'on another collection with a different capacity</summary>'
        '<p>Riverside Base 600 and <a class="text-link" '
        'href="junglepots-riverside-flow.html">Riverside Flow</a> 600 are '
        'published at the same A and B — 60 cm and 60 cm — and at different '
        'capacities: 169 L here, 127 L there.</p>'
        '<p>This page shows that the catalogue’s method is plain cylinder '
        'volume, at least for two of these three rows. On the Riverside Flow '
        'page no row follows that method, and all four follow a different one. '
        'The two pages point at each other; the answer is one question, not '
        'two.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace('<div><dt>Base</dt><dd>Four-legged stand</dd></div>'
                  '<div><dt>Clearance</dt><dd>150 mm</dd></div>',
                  '<div><dt>Base</dt><dd>Sits on the floor</dd></div>'
                  '<div><dt>Wheels</dt><dd>Hidden, optional</dd></div>')
    s = s.replace("<dt>Base</dt><dd>Four-legged stand</dd>",
                  "<dt>Base</dt><dd>Sits on the floor</dd>")
    s = s.replace(
        "Riverside Rise is photographed in two finishes and is the only "
        "collection shown in something other than a grey or a green: the "
        "isolated groups appear in the usual dark and in a beige close to "
        "Cappuccino 1014 above. Neither source names either one.",
        "Riverside Base is photographed only in the dark grey shown here — in "
        "the studio, and in two real installations at CYBERCITY. No source "
        "names the colour, and no other finish is illustrated for this "
        "collection.")
    s = s.replace(
        "weight, drainage and how the legs attach to the bowl all require "
        "confirmation — the two close views on this page show the joint but "
        "no source describes it.",
        "weight, drainage and the hidden wheel option all require "
        "confirmation — the wheels are offered in the catalogue text and "
        "appear in none of its photographs.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/riverside-flow.png" alt="Isolated Riverside Flow '
        'planter, a wide cylinder on three legs" width="880" height="660" '
        'loading="lazy"><details><summary><span>Riverside Flow<small>The same '
        'cylinder, lifted.</small></span><span>+</span></summary><p>Four '
        'diameters on 150 mm legs. Its 600 shares this one’s published '
        'diameter and height and carries a different capacity — the '
        'contradiction set out above.</p><a '
        'href="junglepots-riverside-flow.html" class="text-link">View '
        'collection <span>↗</span></a></details></article><article><img '
        'src="related-assets/riverside-rise.png" alt="Isolated Riverside Rise '
        'planter, a tall cylinder on a stand" width="880" height="660" '
        'loading="lazy"><details><summary><span>Riverside Rise<small>The same '
        'cylinder, taller and lifted.</small></span><span>+</span></summary>'
        '<p>One diameter at three heights on a four-legged stand. One capacity '
        'is printed against all three.</p><a '
        'href="junglepots-riverside-rise.html" class="text-link">View '
        'collection <span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Riverside Rise</option>",
                  "<option>Riverside Base</option><option>Riverside Rise</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['sizes','cappuccino'].includes(b.dataset.view)",
                  "['sizes'].includes(b.dataset.view)")
    s = s.replace("['legs'].includes(b.dataset.view)",
                  "[].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:[^;]*;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:3/2;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:800px)"
               "{#jp-detail-review .hero-img{aspect-ratio:3/2}}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:3/2}}\n</style>", s)

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
