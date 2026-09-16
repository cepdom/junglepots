#!/usr/bin/env python3
"""Build the Riverside Rise collection page.

Derived from the Riverside Flow page.

**One capacity, three heights.** Page 25 prints 31 L against Riverside Rise
600, 800 and 1000 alike -- three cylinders of the same diameter and three
different heights. The catalogue analysis flagged this as "inconsistent; hold
from publication". This page publishes the figure as printed and sets out both
readings without choosing:

  * A repeated row. Under the reading that fits every Riverside Flow figure --
    a cylinder A across and B minus the 150 mm legs tall -- the 600 holds
    31.8 L. The 800 and 1000 would hold 45.9 and 60.0 L. So 31 L is the 600's
    number, apparently copied down the column.
  * A fixed planting liner of the same size in all three, which would make
    31 L correct throughout. No source mentions a liner for this collection.

Together with Riverside Flow this is now five published figures out of five
that the B-minus-150 reading explains -- and that reading contradicts the
page 24 diagram, which measures B down the bowl only. Both facts go on the
page; neither is resolved.

**Both isolated groups ship with their own clipping mask.** p10-1 is the alpha
for p10-0 and p10-5 for p10-4, so the anthracite and cappuccino groups are both
pixel-exact cutouts rather than threshold guesses. That is now the second page
where the catalogue's masks have been found; they are worth looking for on
every remaining collection.

**Four legs, not three.** Riverside Flow stands on three tubular legs and
Riverside Rise on four. The two collections are otherwise the same idea and the
catalogue never mentions the difference.

**The third collection photographed in more than one finish**, and the first
shown in something other than a grey: a beige close to Cappuccino 1014 from the
four swatches. Neither source names it.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-riverside-rise.html"
DRAWING = Path("/home/claude/tb/rr-drawing.svg")
ASSETS = Path("/home/claude/tb/rr-assets")

# model, A diameter mm, B cylinder height mm, printed capacity L,
# what a cylinder A across and B-150 tall would hold
MODELS = [("Riverside Rise 600", 300, 600, 31, "31.8"),
          ("Riverside Rise 800", 300, 800, 31, "45.9"),
          ("Riverside Rise 1000", 300, 1000, 31, "60.0")]

VIEWS = [
    ("context", "collection-assets/riverside-rise-moss-wall.jpg",
     "Three Riverside Rise planters of different heights, planted, standing "
     "on grey carpet against a preserved moss wall",
     "IN CONTEXT / MOSS WALL", "CATALOGUE 10", "1/1"),
    ("sizes", "collection-assets/riverside-rise-three-sizes.png",
     "The three Riverside Rise heights isolated in a dark finish, each on a "
     "four-legged stand",
     "THREE HEIGHTS / ANTHRACITE", "CATALOGUE 10", "16/9"),
    ("cappuccino", "collection-assets/riverside-rise-cappuccino.png",
     "The three Riverside Rise heights isolated in a beige finish",
     "THREE HEIGHTS / BEIGE", "CATALOGUE 10", "16/9"),
    ("legs", "collection-assets/riverside-rise-legs.jpg",
     "Close view of the four-legged stands of two Riverside Rise planters "
     "standing on grey carpet",
     "FOUR-LEGGED STAND", "CATALOGUE 10 / SAME FRAME", "2/1"),
]

LABELS = [("context", "In context"), ("sizes", "Three heights"),
          ("cappuccino", "In beige"), ("legs", "Stand")]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    out = "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td>%d L*</td></tr>' % (m, a, a, b, b, cap)
        for m, a, b, cap, _ in MODELS)
    out += ('<tr><th scope="row">Leg height</th>'
            '<td colspan="3"><span data-mm="150">150</span> '
            '<span class="unit">mm</span>, all three models</td></tr>')
    return out


def main():
    s = (SRC / "junglepots-riverside-flow.html").read_text(encoding="utf-8")

    s = s.replace("<title>Riverside Flow | JunglePots</title>",
                  "<title>Riverside Rise | JunglePots</title>")
    s = s.replace("<span>Riverside Flow</span>", "<span>Riverside Rise</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1100" height="1100"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">11 / ROUND PLANTERS</p><h1 id="collection-title">Riverside<br>Rise</h1><p class="description">One diameter at three heights, each lifted 150 mm on a four-legged stand. Where Riverside Flow spreads, this one climbs: a 300 mm column that reaches a metre and holds a plant at eye level without a shelf under it.</p><div class="hero-facts"><span>Galvanized steel</span><span>Four-legged stand</span><span>Three heights, 600–1000</span><span>One diameter, 300 mm</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three heights ↓</a><p class="small hero-note">One capacity — 31 L — is printed against all three heights. Both readings of that are set out below.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    check = "".join(
        '<tr><th scope="row">%s</th><td>%d</td><td>%s</td></tr>'
        % (m.replace("Riverside Rise ", ""), cap, geo)
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
        '<figcaption>Traced from the catalogue’s isolated group / not to scale '
        '/ one drawing serves all three heights. B runs down the cylinder and '
        'the leg height sits below it, as on the catalogue’s own diagram.'
        '</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">RIVERSIDE RISE / THREE HEIGHTS</p>'
        '<table class="compare"><caption class="sr-only">Riverside Rise '
        'catalogue specifications, three heights</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Diameter '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Height '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Capacity</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, pages 10 and 25. One '
        'diameter, three heights, and a 150 mm stand under each — the same '
        'leg height as Riverside Flow, though on four legs here rather than '
        'three. As on that page, no combined overall height is published, so '
        'none is shown.</p>'
        '<details open class="verification"><summary>* One capacity is printed '
        'against all three heights</summary>'
        '<p>31 L appears against the 600, the 800 and the 1000 alike. There '
        'are two readings and the catalogue does not say which is right:</p>'
        '<table class="compare"><thead><tr><th scope="col">Model</th>'
        '<th scope="col">Printed</th>'
        '<th scope="col">A × (B − 150) as a cylinder</th></tr></thead>'
        '<tbody>' + check + '</tbody></table>'
        '<p><strong>A repeated row.</strong> The reading in the right-hand '
        'column is the one that matches every published Riverside Flow figure '
        'to within a litre. Under it the 600 holds 31.8 L — so 31 L is the '
        '600’s number and the two taller models carry it by mistake.</p>'
        '<p><strong>Or a fixed liner.</strong> If all three take the same '
        'planting insert, 31 L is correct throughout and the extra height is '
        'plinth rather than volume. No source mentions a liner for this '
        'collection.</p>'
        '<p>Nothing has been corrected or chosen. Note also that the '
        'right-hand column relies on a reading that contradicts the '
        'catalogue’s own diagram, which measures B down the cylinder and the '
        'legs separately — the same contradiction set out on the Riverside '
        'Flow page. Request the usable volumes before specifying.</p>'
        '</details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace("<dt>Base</dt><dd>Three tubular legs</dd>",
                  "<dt>Base</dt><dd>Four-legged stand</dd>")
    s = s.replace(
        "Riverside Flow is one of only two collections photographed in two "
        "finishes: the moss-wall view shows the usual dark grey and the "
        "isolated group a pale green, which may be Pale Green 6021 above. "
        "Neither source names either one.",
        "Riverside Rise is photographed in two finishes and is the only "
        "collection shown in something other than a grey or a green: the "
        "isolated groups appear in the usual dark and in a beige close to "
        "Cappuccino 1014 above. Neither source names either one.")

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/riverside-flow.png" alt="Isolated Riverside Flow '
        'planter, a wide cylinder on three legs" width="880" height="660" '
        'loading="lazy"><details><summary><span>Riverside Flow<small>The same '
        'stand, wider and lower.</small></span><span>+</span></summary><p>Four '
        'diameters from 200 to 600 mm on the same 150 mm legs — three of them '
        'rather than four. Its capacity column has the same problem, set out '
        'in full on that page.</p><a href="junglepots-riverside-flow.html" '
        'class="text-link">View collection <span>↗</span></a></details>'
        '</article><article><img src="related-assets/riverside-base.png" '
        'alt="Isolated Riverside Base planter, a plain cylinder" width="880" '
        'height="660" loading="lazy"><details><summary><span>Riverside Base'
        '<small>The same cylinder, on the floor.</small></span><span>+</span>'
        '</summary><p>Three sizes with no stand at all, and an optional set of '
        'hidden wheels.</p><a href="#inquiry" class="text-link" '
        'data-related="Riverside Base">Enquire about Riverside Base '
        '<span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Riverside Flow</option><option>Cube Shelf</option>",
                  "<option>Riverside Rise</option>"
                  "<option>Riverside Flow</option><option>Cube Shelf</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['sizes'].includes(b.dataset.view)",
                  "['sizes','cappuccino'].includes(b.dataset.view)")
    s = s.replace("['joint','detail'].includes(b.dataset.view)",
                  "['legs'].includes(b.dataset.view)")

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
