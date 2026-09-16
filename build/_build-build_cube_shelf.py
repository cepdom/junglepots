#!/usr/bin/env python3
"""Build the Cube Shelf collection page.

Derived from the Garden page.

**The catalogue page renders were on the client's own machine all along.**
`work/catalogue/page-NN.png` and `work/catalogue/index-assets/pNN-N.jpg` sit in
the connected folder -- full page renders and every extracted image. Until now
each collection page has been built from a single low-resolution crop in
`_source-assets/`. Page 17 alone yields four images at up to 1400 px, and page
25 is the authoritative specification sheet. Every remaining collection should
be built from these, and the four earlier pages are worth revisiting.

**The catalogue ships its own clipping mask.** `p17-2.jpg` is a black-and-white
alpha for `p17-1.jpg`. Using it gives a pixel-exact cutout of the three-cube
group, rather than a threshold guess. Worth looking for on every later page.

**An open frame traces beautifully.** `silhouette()` walks holes as well as the
outer ring, so the bare frame on page 17 comes back as eight rings -- the
outline plus seven openings -- which reconstructs the whole wireframe with
every member at its true width. No interior-edge pass needed. The one fix was
the cutout threshold: the sweep behind that frame carries a faint blue cast
that the default `white_lo=234` reads as product, filling the openings that
make it a frame. `white_lo=205, ramp=22` leaves them open.

**Cube Shelf is not a planter**, and the template's material panel was written
for planters. Galvanizing, primer, a sand-textured finish, adjustable feet,
indoor/outdoor use and the four listing claims marked dagger are all about
planters and none of them is stated for this collection. The panel is rewritten
from the only sentence the catalogue gives it: page 25's footnote -- thick-
walled 20 x 20 mm square profile, powder-coated, complete with metal sheet
shelf, with plastic plugs.

**The absence: no shelf load.** The catalogue photographs a planted Dawn on a
Cube 50 and never says what the shelf carries. Same shape as Garden, one storey
down.

**Prices are on page 25 and are deliberately not shown**, per the brief.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-cube-shelf.html"
DRAWING = Path("/home/claude/tb/cs-drawing.svg")
ASSETS = Path("/home/claude/tb/cs-assets")

# model, A mm, B mm, C mm  -- page 25, all three equal per model
MODELS = [("Cube 30", 300, 300, 300),
          ("Cube 40", 400, 400, 400),
          ("Cube 50", 500, 500, 500)]

VIEWS = [
    ("context", "collection-assets/cube-shelf-moss-wall.jpg",
     "Three Cube Shelf frames of different sizes standing on grey carpet "
     "against a preserved moss wall, with a planted Dawn planter on the "
     "largest",
     "IN CONTEXT / MOSS WALL", "CATALOGUE 17", "1/1"),
    ("sizes", "collection-assets/cube-shelf-three-sizes.png",
     "The three Cube Shelf sizes together, isolated: 30, 40 and 50 cm cubes "
     "with sheet shelves",
     "THREE SIZES", "CATALOGUE 17", "16/9"),
    ("frame", "collection-assets/cube-shelf-frame.png",
     "A single Cube Shelf frame photographed without its shelf, showing all "
     "twelve square-profile members",
     "FRAME / WITHOUT SHELF", "CATALOGUE 17", "1/1"),
    ("shelf", "collection-assets/cube-shelf-shelf.jpg",
     "Close view of the sheet shelf seated in the top of a Cube Shelf frame, "
     "with a planter base resting on it",
     "SHELF / SEATED IN FRAME", "CATALOGUE 17 / SAME FRAME", "3/2"),
]

LABELS = [("context", "In context"), ("sizes", "Three sizes"),
          ("frame", "Frame"), ("shelf", "Shelf")]

MATERIAL = (
    '<section id="material" class="material"><div class="wrap space">'
    '<div class="material-grid"><div><h2>Material &amp; finish.</h2>'
    '<p class="material-intro">Thick-walled square steel profile, 20 × 20 mm.'
    '<br>Powder-coated, with a metal sheet shelf and plastic plugs.</p>'
    '<dl>'
    '<div><dt>Profile</dt><dd>20 × 20 mm square</dd></div>'
    '<div><dt>Shelf</dt><dd>Metal sheet, supplied</dd></div>'
    '<div><dt>Ends</dt><dd>Plastic plugs</dd></div>'
    '<div><dt>Finish</dt><dd>Powder coating</dd></div>'
    '<div><dt>Application</dt><dd class="absent">Not stated</dd></div>'
    '<div><dt>Shelf load</dt><dd class="absent">Not published</dd></div>'
    '</dl></div><div class="finish"><div class="swatches">'
    '<button data-colour="Anthracite 7016" aria-pressed="true">'
    '<span style="background:#383e42"></span>Anthracite<small>7016</small>'
    '</button><button data-colour="Pale Green 6021" aria-pressed="false">'
    '<span style="background:#8a9977"></span>Pale Green<small>6021</small>'
    '</button><button data-colour="Cappuccino 1014" aria-pressed="false">'
    '<span style="background:#ddc69b"></span>Cappuccino<small>1014</small>'
    '</button><button data-colour="Pure white 9010" aria-pressed="false">'
    '<span style="background:#f1efe4"></span>Pure white<small>9010</small>'
    '</button></div>'
    '<p class="small">Digital colours are indicative. These four come from the '
    'planter specification on page 23; Cube Shelf is photographed only in the '
    'dark grey shown here and no colour range is published for it. Confirm a '
    'physical sample, and that the finish is available at all, before '
    'specifying one.</p>'
    '<p class="selected-colour" aria-live="polite">Enquiry colour: '
    'Anthracite 7016</p>'
    '<details><summary>Why this panel is shorter than the others</summary>'
    '<p>Every other collection here is a planter, and the material panel on '
    'those pages draws on the general planter specification on page 23 — '
    'galvanized steel under the powder coating, a sand-textured finish, '
    'integrated adjustable feet, indoor and outdoor use — together with four '
    'claims from Jungle Flora’s own listings.</p>'
    '<p>None of that is stated for Cube Shelf. It is not a planter, it has no '
    'listing, and the catalogue gives it exactly one sentence: a footnote on '
    'page 25 reading “thick-walled square profile 20 × 20 mm; powder-coated. '
    'Complete with metal sheet shelf, with plastic plugs.” This panel is that '
    'sentence and nothing else. Whether the frame is galvanized beneath the '
    'coating, and whether it is rated for outdoor use, are open questions '
    'rather than omissions from this page.</p></details>'
    '</div></div></div></section>')


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def rows():
    out = "".join(
        '<tr><th scope="row">%s</th>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td>'
        '<td><span data-mm="%d">%d</span></td></tr>' % (m, a, a, b, b, c, c)
        for m, a, b, c in MODELS)
    out += ('<tr><th scope="row">Shelf load</th>'
            '<td colspan="3" class="absent">Not published*</td></tr>')
    return out


def main():
    s = (SRC / "junglepots-garden.html").read_text(encoding="utf-8")

    s = s.replace("<title>Garden | JunglePots</title>",
                  "<title>Cube Shelf | JunglePots</title>")
    s = s.replace("<span>Garden</span>", "<span>Cube Shelf</span>")

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
<div class="hero-copy"><p class="eyebrow">09 / PLANT STANDS</p><h1 id="collection-title">Cube<br>Shelf</h1><p class="description">The one thing here that is not a planter. A welded frame in 20 × 20 mm square steel with a sheet shelf across its top, in three cubes, built to put a planter at eye level rather than on the floor.</p><div class="hero-facts"><span>20 × 20 mm square profile</span><span>Shelf supplied</span><span>Three cubes: 30, 40, 50</span><span>Powder-coated</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three sizes ↓</a><p class="small hero-note">What the shelf is rated to carry is not published, and the catalogue photographs a planted planter on it.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    pre, _, post = cut(s, '<section id="dimensions"', "</section>")
    spec = (
        '<section id="dimensions" class="wrap space"><div class="section-top">'
        '<p class="eyebrow">01 / SPECIFICATION</p>'
        '<span class="eyebrow">FORM / PROPORTION / STRUCTURE</span></div>'
        '<div class="section-heading"><h2>Dimensions &amp; variants.</h2>'
        '<div class="units" aria-label="Dimension units">'
        '<button data-unit="mm" aria-pressed="true">mm</button>'
        '<button data-unit="cm" aria-pressed="false">cm</button></div></div>'
        '<div class="spec-grid"><figure class="drawing">' + svg +
        '<figcaption>Traced from the catalogue’s isolated frame / not to scale '
        '/ one drawing serves all three sizes. That frame is photographed '
        'without its shelf, so the drawing has none; the shelf is supplied '
        'with the frame.</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">CUBE SHELF / THREE SIZES</p>'
        '<table class="compare"><caption class="sr-only">Cube Shelf catalogue '
        'specifications, three sizes</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Width '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Depth '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">C</span> Height '
        '<span class="unit">mm</span></th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, pages 17 and 25. A true '
        'cube at every size — A, B and C are equal, which is why one drawing '
        'covers all three. Thick-walled square profile 20 × 20 mm, '
        'powder-coated, complete with metal sheet shelf and plastic plugs.</p>'
        '<details open class="verification"><summary>* Nothing is published '
        'about what the shelf carries</summary>'
        '<p>The catalogue gives dimensions and one construction footnote. '
        'There is no shelf load, no sheet thickness, no frame weight and no '
        'statement of indoor or outdoor use — and Cube Shelf has no retail '
        'listing anywhere, so there is no second source. Nothing has been '
        'derived here.</p>'
        '<p>It matters because of how the collection is sold: page 17 '
        'photographs a planted Dawn standing on a Cube 50. A planted planter '
        'is the intended load and its weight is not a figure to guess at. '
        'Request the shelf load before specifying.</p></details>'
        '<details class="verification"><summary>Which planter fits which '
        'cube — an observation, not a recommendation</summary>'
        '<p>Two published tables happen to line up. Dawn measures 29.5, 39.5 '
        'and 44 cm across the rim; the cube tops are 30, 40 and 50 cm square. '
        'So each Dawn sits inside the corresponding cube top with between 5 mm '
        'and 60 mm to spare, and page 17 shows a Dawn on the largest.</p>'
        '<p>Neither source states a pairing, gives a clearance, or says that '
        'any planter is approved for any frame. This is two sets of published '
        'dimensions set beside each other so you can check the arithmetic '
        'yourself — not manufacturer guidance.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material: rewritten, not patched -------------------------------
    pre, _, post = cut(s, '<section id="material"', "</section>")
    s = pre + MATERIAL + post

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/dawn.png" alt="Isolated Dawn planter, a faceted '
        'round planter" width="880" height="660" loading="lazy"><details>'
        '<summary><span>Dawn<small>The planter photographed on it.</small>'
        '</span><span>+</span></summary><p>Three sizes, 29.5 to 44 cm across '
        'the rim, with published capacities. It is a separate collection: the '
        'cube carries it, nothing is sold as a set.</p><a '
        'href="junglepots-dawn.html" class="text-link">View collection '
        '<span>↗</span></a></details></article><article><img '
        'src="related-assets/garden.png" alt="Isolated Garden tray, a long '
        'shallow suspended tray" width="880" height="660" loading="lazy">'
        '<details><summary><span>Garden<small>The same idea, hanging.</small>'
        '</span><span>+</span></summary><p>A planting tray suspended from the '
        'ceiling in four lengths. Where the cube lifts a planter off the '
        'floor, Garden takes it off the ground entirely.</p><a '
        'href="junglepots-garden.html" class="text-link">View collection '
        '<span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Garden</option><option>Grand Wall</option>",
                  "<option>Cube Shelf</option><option>Garden</option>"
                  "<option>Grand Wall</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("hero.classList.toggle('isolated',b.dataset.view==='product')",
                  "hero.classList.toggle('isolated',"
                  "['sizes','frame'].includes(b.dataset.view))")
    s = s.replace("['suspension','edge'].includes(b.dataset.view)",
                  "['shelf'].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:2/1;"
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
