#!/usr/bin/env python3
"""Build the Siena Kubo collection page.

Derived from the Tower Bridge page, which was derived from Big Ben Tower, so
the chrome, type, grid, motion and interactions are the same code throughout.

What this collection forces the template to learn:

  * **Three sizes, one schedule.** Not three cards. The flexible-collection
    template is explicit about this, and it is right: a specifier comparing
    35, 44 and 54 wants them in one table with the letters running down the
    columns, not the same paragraph three times. The schedule becomes a
    comparison table and the page grows a `<thead>` it has never had.
  * **Its own A/B/C.** Siena Kubo uses **B for height** where Big Ben Tower
    and Tower Bridge use C. The drawing takes its letters as arguments for
    exactly this reason, so the letters on the drawing and the letters in the
    table agree without anyone having to remember a global convention.
  * **One drawing for three models.** They are cubes; they differ only in
    scale, so a second drawing would carry no second fact. The caption says
    so rather than leaving a reader to wonder which size is drawn.
  * **No capacity at all.** The catalogue supplies none for this collection.
    That is a row reading "not supplied", not a row quietly missing.

Photography: the catalogue's own, all three views from pages 16 and 27. The
context frame carries all three sizes together, so it doubles as the scale
comparison the schedule cannot give.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-siena-kubo.html"
DRAWING = Path("/home/claude/tb/siena-kubo-drawing.svg")
ASSETS = Path("/home/claude/tb/sk-assets")

MODELS = [("1", 350), ("2", 440), ("3", 540)]

VIEWS = [
    ("context", "collection-assets/siena-kubo-project.jpg",
     "Three sizes of Siena Kubo planters standing together in front of a "
     "moss-covered green wall",
     "IN CONTEXT / ALL THREE SIZES", "CATALOGUE 16", "3/2"),
    ("product", "collection-assets/siena-kubo-isolated.png",
     "Isolated Siena Kubo planter, a square volume with a folded rim",
     "ISOLATED PRODUCT", "CATALOGUE 27", "1/1"),
    ("rim", "collection-assets/siena-kubo-rim.jpg",
     "Close view of the folded rim and corner of a Siena Kubo planter, "
     "showing the sand-textured powder-coated finish",
     "FOLDED RIM / CORNER", "CATALOGUE 16", "5/4"),
]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def schedule_rows():
    rows = []
    for name, mm in MODELS:
        cells = "".join(
            '<td><span data-mm="%d">%d</span></td>' % (mm, mm) for _ in range(3))
        rows.append('<tr><th scope="row">%s</th>%s</tr>' % (name, cells))
    return "".join(rows)


def main():
    s = (SRC / "junglepots-tower-bridge.html").read_text(encoding="utf-8")

    s = s.replace("<title>Tower Bridge | JunglePots</title>",
                  "<title>Siena Kubo | JunglePots</title>")
    s = s.replace("<span>Tower Bridge</span>", "<span>Siena Kubo</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(
            [("context", "In context"), ("product", "Product"), ("rim", "Rim")]))
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="1800" height="1262"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">09 / RECTANGULAR PLANTERS</p><h1 id="collection-title">Siena<br>Kubo</h1><p class="description">A cube, and nothing else. No base, no taper, no visible fixing — three scales of the same square volume, to be placed singly or in a run.</p><div class="hero-facts"><span>Galvanized steel</span><span>Indoor / outdoor</span><span>Three catalogued sizes</span><span>Hidden wheels option</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the three sizes ↓</a><p class="small hero-note">The catalogue supplies no capacity for this collection. Confirm planting volume before specifying.</p></div>
</section>""" % (VIEWS[0][1], VIEWS[0][2], VIEWS[0][3], VIEWS[0][4], controls)
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
        'drawing serves all three models</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">SIENA KUBO / THREE MODELS</p>'
        '<table class="compare"><caption class="sr-only">Siena Kubo '
        'catalogue specifications, three models</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Width '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Height '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">C</span> Depth '
        '<span class="unit">mm</span></th></tr></thead>'
        '<tbody>' + schedule_rows() +
        '<tr><th scope="row">Capacity</th>'
        '<td colspan="3" class="absent">Not supplied*</td></tr>'
        '</tbody></table>'
        '<p class="small">Source: supplied catalogue, page 16. All three '
        'models are cubes, so A, B and C carry the same value in each row; '
        'the columns are kept because the letters differ on the drawing.</p>'
        '<details open class="verification"><summary>* No capacity is '
        'published</summary><p>The catalogue gives planting volume for most '
        'collections and none for this one. Nothing has been derived from the '
        'external dimensions: a cube’s bounding box is not its planting '
        'volume, and the liner and drainage details that would settle it are '
        'not supplied either. Request the usable volume before specifying.'
        '</p></details>'
        '<details class="verification"><summary>A, B and C on this drawing'
        '</summary><p>Siena Kubo’s catalogue convention is <strong>A '
        'width, B height, C depth</strong> — B is the vertical here, '
        'where Big Ben Tower and Tower Bridge use C. The drawing follows this '
        'collection’s own letters so that they read directly against the '
        'columns beside it.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material: the wheels option belongs here, not in the schedule ----
    s = s.replace(
        "<div><dt>Base</dt><dd>Integrated adjustable feet</dd></div>",
        "<div><dt>Base</dt><dd>Integrated adjustable feet</dd></div>"
        "<div><dt>Wheels</dt><dd>Hidden castors, optional</dd></div>")
    s = s.replace(
        "<p class=\"small\">Digital colours are indicative. The photographed "
        "red-brown finish has no identified catalogue code, and the two "
        "sources do not agree: the project photography reads as a deep brick "
        "red, the studio photography as a warmer terracotta. That may be "
        "white balance rather than two finishes, but it cannot be settled "
        "from photographs. Confirm a physical sample for your project.</p>",
        "<p class=\"small\">Digital colours are indicative. Siena Kubo is "
        "photographed throughout in a dark grey close to Anthracite 7016, but "
        "the catalogue does not name the code used. Confirm a physical sample "
        "for your project.</p>")

    # ---- related: the other two rectangular collections -------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(r'<div class="related-grid">.*?</div></section>', """<div class="related-grid"><article><img src="related-assets/siena.png" alt="Isolated Siena planter, a rectangular trough" width="880" height="660" loading="lazy"><details><summary><span>Siena<small>The same language, drawn long.</small></span><span>+</span></summary><p>Three models: 65 and 95 at 50 cm high, and 95H at 70 cm. A length, B depth, C height — a different convention again. Capacities are published but the usable volume is not defined.</p><a href="#inquiry" class="text-link" data-related="Siena">Enquire about Siena <span>↗</span></a></details></article><article><img src="related-assets/grand-wall.png" alt="Isolated Grand Wall planter, a long low trough on feet" width="880" height="660" loading="lazy"><details><summary><span>Grand Wall<small>A room divider that plants.</small></span><span>+</span></summary><p>Three lengths at one section: 90, 140 and 190 cm, all 42 × 74 cm. Capacity is not supplied for this collection either.</p><a href="#inquiry" class="text-link" data-related="Grand Wall">Enquire about Grand Wall <span>↗</span></a></details></article></div></section>""", rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Tower Bridge</option><option>Big Ben Tower</option>",
                  "<option>Siena Kubo</option><option>Big Ben Tower</option>"
                  "<option>Tower Bridge</option>")
    s = re.sub(r"<option>Siena Kubo</option>\s*</select>", "</select>", s, count=1)

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['rim','base'].includes(b.dataset.view)",
                  "['rim'].includes(b.dataset.view)")

    # ---- the hero frame, sized to this collection ------------------------
    # the context frame holds three cubes side by side, so it is landscape
    # where the two towers wanted a deep portrait
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:1/1\.4;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:3/2;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:3/2}}\n</style>", s)

    # ---- the comparison table needs a header row ------------------------
    s = s.replace("</body></html>", """<style>
/* ---- Comparison schedule: the first table on the site with columns ---- */
#jp-detail-review .compare thead th{
  font:10.5px/1.6 'IBM Plex Mono',monospace;letter-spacing:.055em;
  color:var(--muted);text-align:right;padding-block:10px;font-weight:400;
}
#jp-detail-review .compare thead th:first-child{text-align:left}
#jp-detail-review .compare thead .letter{width:auto;margin-right:4px}
#jp-detail-review .compare tbody th{font-variant-numeric:tabular-nums}
#jp-detail-review .compare .absent{color:var(--muted)}
@container detail (max-width:520px){
  #jp-detail-review .compare thead th{font-size:9.5px}
  #jp-detail-review .compare th,#jp-detail-review .compare td{font-size:14px}
}
</style>
</body></html>""")

    OUT.write_text(s, encoding="utf-8")
    dst = SRC / "collection-assets"
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, dst / f.name)
    for f in Path("/home/claude/tb/related-assets").glob("*.png"):
        shutil.copy(f, SRC / "related-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
