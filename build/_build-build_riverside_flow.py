#!/usr/bin/env python3
"""Build the Riverside Flow collection page.

Derived from the Cube Shelf page.

**The B convention is settled, from the catalogue's own diagram.** The
catalogue analysis flagged Riverside Flow's B as "requires clarification".
Page 24's diagram answers it: A spans the rim, B runs from the rim down to the
*base of the bowl*, and a separate figure, printed simply as `150`, spans from
the bowl's underside to the floor. So B is the bowl, not the overall height,
and the overall height is B plus 150 mm. The page states that and does not
print a combined figure, because the catalogue does not.

**The drawing needed a new mode.** `round` mode runs its vertical arrow from
the rim to the bottom of the silhouette, which on a bowl standing on legs would
contradict the source. `mode="stand"` finds the bowl's base -- the row where
the filled width of the silhouette collapses from a solid cylinder to three
thin bars -- runs B to there, and puts a third short dimension below it for the
legs. The drawing now reads exactly like the catalogue's own.

**The cutout needed a different test.** The isolated green group was shot with
a soft drop shadow that picks up the planter's own colour, so the usual
whiteness test keeps the shadow: shadow and pale legs sit at almost the same
lightness. Saturation separates them cleanly -- shadow 17, legs 44, bowl 102 --
so this one image is cut on saturation, with a darkness term to keep the black
plug caps. Everything else about the pipeline is unchanged.

The two leg close-ups are NOT cut out. They are crops on a soft studio
gradient rather than a white sweep, so thresholding leaves a rectangle of
retained grey; they stay photographs.

**The capacities do not reconcile, and this page can prove it.** See the
disclosure text below. The strongest single fact: Riverside Base 600 is
published at the same A and B as Riverside Flow 600 -- 60 cm and 60 cm -- and
at a different capacity, 169 L against 127 L. 169 L is exactly the plain
cylinder volume of those dimensions. Nothing is derived on the page; both
published figures are shown and the arithmetic is offered as a check, not a
correction.

Prices are on page 24 and are deliberately not shown, per the brief.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-riverside-flow.html"
DRAWING = Path("/home/claude/tb/rf-drawing.svg")
ASSETS = Path("/home/claude/tb/rf-assets")

# model, A diameter mm, B bowl height mm, published capacity L,
# plain-cylinder volume of A x B in L (shown only inside the disclosure)
MODELS = [("Riverside Flow 200", 200, 400, 7, "12.6"),
          ("Riverside Flow 300", 300, 400, 17, "28.3"),
          ("Riverside Flow 400", 400, 500, 43, "62.8"),
          ("Riverside Flow 600", 600, 600, 127, "169.6")]

VIEWS = [
    ("context", "collection-assets/riverside-flow-moss-wall.jpg",
     "Three Riverside Flow planters of different sizes, planted, standing on "
     "grey carpet against a preserved moss wall",
     "IN CONTEXT / MOSS WALL", "CATALOGUE 9", "1/1"),
    ("sizes", "collection-assets/riverside-flow-three-sizes.png",
     "Three Riverside Flow planters isolated, in a pale green finish, showing "
     "the three tubular legs under each bowl",
     "THREE SIZES / PALE GREEN", "CATALOGUE 9", "16/9"),
    ("joint", "collection-assets/riverside-flow-leg-joint.jpg",
     "Close view from below of a leg meeting the underside of a Riverside "
     "Flow bowl",
     "LEG / UNDERSIDE JOINT", "CATALOGUE 9", "1/1"),
    ("detail", "collection-assets/riverside-flow-leg-detail.jpg",
     "Close view of two legs where they meet the lower edge of a dark "
     "Riverside Flow bowl, showing the tube ends",
     "LEG / TUBE END", "CATALOGUE 9", "1/1"),
]

LABELS = [("context", "In context"), ("sizes", "Three sizes"),
          ("joint", "Leg joint"), ("detail", "Tube end")]


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
            '<span class="unit">mm</span>, all four models</td></tr>')
    return out


def main():
    s = (SRC / "junglepots-cube-shelf.html").read_text(encoding="utf-8")

    s = s.replace("<title>Cube Shelf | JunglePots</title>",
                  "<title>Riverside Flow | JunglePots</title>")
    s = s.replace("<span>Cube Shelf</span>", "<span>Riverside Flow</span>")

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
<div class="hero-copy"><p class="eyebrow">10 / ROUND PLANTERS</p><h1 id="collection-title">Riverside<br>Flow</h1><p class="description">A plain steel cylinder lifted 150 mm off the floor on three tubular legs, in four diameters. The gap under the bowl is the whole idea: the planter reads as an object standing in the room rather than a container set down in it.</p><div class="hero-facts"><span>Galvanized steel</span><span>Three tubular legs</span><span>Four diameters, 200–600</span><span>150 mm clear underneath</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Compare the four sizes ↓</a><p class="small hero-note">The published capacities do not reconcile with the published dimensions. Both are shown, with the arithmetic.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- specification --------------------------------------------------
    svg = DRAWING.read_text()
    check = "".join(
        "<tr><th scope=\"row\">%s</th><td>%d</td><td>%s</td></tr>"
        % (m.replace("Riverside Flow ", ""), cap, geo)
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
        '/ one drawing serves all four sizes. The letters sit where the '
        'catalogue’s own diagram puts them: B down the bowl, and the leg '
        'height printed below it as a bare figure.</figcaption></figure>'
        '<div class="schedule">'
        '<p class="eyebrow">RIVERSIDE FLOW / FOUR SIZES</p>'
        '<table class="compare"><caption class="sr-only">Riverside Flow '
        'catalogue specifications, four sizes</caption>'
        '<thead><tr><th scope="col">Model</th>'
        '<th scope="col"><span class="letter">A</span> Diameter '
        '<span class="unit">mm</span></th>'
        '<th scope="col"><span class="letter">B</span> Bowl height '
        '<span class="unit">mm</span></th>'
        '<th scope="col">Capacity</th></tr></thead>'
        '<tbody>' + rows() + '</tbody></table>'
        '<p class="small">Source: supplied catalogue, pages 9 and 24. The '
        'diagram on page 24 settles a convention the rest of the catalogue '
        'leaves open: <strong>B is the bowl alone</strong>, measured from the '
        'rim to its underside, and the legs add a further 150 mm. No combined '
        'overall height is published, so none is shown here.</p>'
        '<details open class="verification"><summary>* The capacities do not '
        'reconcile with the dimensions</summary>'
        '<p>A plain cylinder A across and B tall would hold roughly double the '
        'printed figure at the small end:</p>'
        '<table class="compare"><thead><tr><th scope="col">Model</th>'
        '<th scope="col">Printed</th><th scope="col">A × B as a cylinder</th>'
        '</tr></thead><tbody>' + check + '</tbody></table>'
        '<p>Three further facts, all from the catalogue itself. '
        '<strong>Riverside Base 600 is published at the same A and B as '
        'Riverside Flow 600</strong> — 60 cm and 60 cm — and at a different '
        'capacity, 169 L against 127 L; 169 L is exactly the plain cylinder '
        'volume of those dimensions. The three figures 7, 17 and 43 L are also '
        'printed against Siena, and 17 and 43 L against Riverside Base. And '
        'every Flow figure matches a cylinder A across and <em>B minus '
        '150</em> tall, to within a litre.</p>'
        '<p>Nothing has been corrected. The arithmetic is shown so you can see '
        'the size of the discrepancy, not to propose a replacement. Request '
        'the usable volumes before specifying.</p></details>'
        '<a class="text-link" href="#inquiry">Request specification sheet '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material -------------------------------------------------------
    s = s.replace("<dt>Suspension</dt><dd>Chain or steel cable</dd>",
                  "<dt>Base</dt><dd>Three tubular legs</dd>")
    pre, mat, post = cut(s, '<section id="material"', "</section>")
    mat = re.sub(r'<p class="material-intro">.*?</p>',
                 '<p class="material-intro">Galvanized steel. Primer. Powder '
                 'coating.<br>A sand-textured finish in matte or gloss.</p>',
                 mat, flags=re.S)
    mat = re.sub(r'<dl>.*?</dl>',
                 '<dl><div><dt>Application</dt><dd>Indoor / outdoor</dd></div>'
                 '<div><dt>Base</dt><dd>Three tubular legs</dd></div>'
                 '<div><dt>Clearance</dt><dd>150 mm</dd></div>'
                 '<div><dt>Custom colour</dt><dd>Any RAL shade†</dd></div>'
                 '<div><dt>Custom sizes</dt><dd>Made to dimension†</dd></div>'
                 '<div><dt>Origin</dt><dd>Lithuania†</dd></div></dl>',
                 mat, flags=re.S)
    mat = re.sub(r'<p class="small">Digital colours are indicative\..*?</p>',
                 '<p class="small">Digital colours are indicative. Riverside '
                 'Flow is one of only two collections photographed in two '
                 'finishes: the moss-wall view shows the usual dark grey and '
                 'the isolated group a pale green, which may be Pale Green '
                 '6021 above. Neither source names either one. Confirm a '
                 'physical sample for your project.</p>', mat, flags=re.S)
    mat = re.sub(r'<details><summary>Why this panel is shorter than the '
                 r'others</summary>.*?</details>',
                 '<details><summary>Material information &amp; specification '
                 'limits</summary><p>The three items marked † come from Jungle '
                 'Flora’s own listings rather than the supplied catalogue: '
                 'powder coating in any RAL shade, manufacture to custom '
                 'dimensions, and Lithuanian origin. They are sales copy '
                 'rather than a specification, so treat them as an opening '
                 'position.</p><p>The catalogue describes frost and UV '
                 'resistance but supplies no test ratings. Steel thickness, '
                 'weight, drainage and how the legs attach to the bowl all '
                 'require confirmation — the two close views on this page show '
                 'the joint but no source describes it. Material and finish '
                 'information comes from the general planter specification on '
                 'page 23.</p></details>', mat, flags=re.S)
    s = pre + mat + post

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/riverside-base.png" alt="Isolated Riverside Base '
        'planter, a plain cylinder" width="880" height="660" loading="lazy">'
        '<details><summary><span>Riverside Base<small>The same cylinder, on '
        'the floor.</small></span><span>+</span></summary><p>Three sizes with '
        'no legs. Its 600 is published at the same diameter and height as the '
        'Flow 600 and at a different capacity — the discrepancy set out '
        'above.</p><a href="#inquiry" class="text-link" '
        'data-related="Riverside Base">Enquire about Riverside Base '
        '<span>↗</span></a></details></article><article><img '
        'src="related-assets/riverside-rise.png" alt="Isolated Riverside Rise '
        'planter, a tall cylinder on legs" width="880" height="660" '
        'loading="lazy"><details><summary><span>Riverside Rise<small>The same '
        'cylinder, taller.</small></span><span>+</span></summary><p>One '
        'diameter at three heights, on the same 150 mm legs. The catalogue '
        'prints a single capacity against all three.</p><a href="#inquiry" '
        'class="text-link" data-related="Riverside Rise">Enquire about '
        'Riverside Rise <span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace("<option>Cube Shelf</option><option>Garden</option>",
                  "<option>Riverside Flow</option><option>Cube Shelf</option>"
                  "<option>Garden</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("['sizes','frame'].includes(b.dataset.view)",
                  "['sizes'].includes(b.dataset.view)")
    s = s.replace("['shelf'].includes(b.dataset.view)",
                  "['joint','detail'].includes(b.dataset.view)")

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
