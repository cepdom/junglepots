#!/usr/bin/env python3
"""Build the Bar Planter page.

Derived from the Pixie page, then taken apart: this is the only collection the
catalogue gives **no schedule at all**. No dimensions, no capacity, no
material, no finish, no variants -- one photograph on page 20 and nothing else.

So the page is enquiry-led rather than specification-led, and three parts of
the template are deliberately removed rather than left empty:

**No drawing.** Every other page traces the catalogue's own photograph. Here
the object is half-hidden behind its own planting and a blurred foreground
leaf, and no dimension is published to check a trace against. Tracing it would
invent a form. The drawing plate carries a sentence saying so, which is a truer
thing to put in that space than a guess.

**No schedule.** A table of six "not published" rows would look like a
specification with gaps. Instead the section is titled *What is published*, and
what is published is nothing -- stated once, plainly.

**Observations are separated from specification.** What the photograph shows --
a circular worktop, a planting aperture cut through it, a flared pedestal, a
red-brown finish, a pole carrying a pendant lamp -- goes in its own disclosure,
labelled as observation and explicitly not a specification. Whether the lamp is
part of the product or the building's is not stated by anyone.

**A finding for the finish panel.** Bar Planter is photographed in a red-brown
that is none of the four named swatches. The catalogue analysis already noted
that "the red-brown finish in Big Ben Tower photography is not assigned a
colour code". So the same unnamed colour appears on at least two collections,
and the four-swatch range does not describe what the catalogue actually shows.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-bar-planter.html"
ASSETS = Path("/home/claude/tb/bp-assets")

VIEWS = [
    ("office", "collection-assets/bar-planter-office.jpg",
     "A Bar Planter in an office tea point: a circular red-brown table with "
     "planting growing up through its centre, chairs and a banquette around "
     "it and a pendant lamp above",
     "IN USE / OFFICE TEA POINT", "CATALOGUE 20", "2/3"),
    ("top", "collection-assets/bar-planter-top.jpg",
     "Close view of the Bar Planter worktop, showing the planting aperture "
     "cut through the circular top and the flared pedestal beneath it",
     "WORKTOP / PLANTING APERTURE", "CATALOGUE 20 / SAME FRAME", "2/1"),
]

LABELS = [("office", "In use"), ("top", "Worktop")]

NOTHING = (
    '<figure class="drawing"><p class="small" style="max-width:34ch">'
    'There is no drawing on this page.</p><p class="small" '
    'style="max-width:34ch">Every other collection here is traced from the '
    'catalogue’s own photograph and checked against a published dimension. '
    'Bar Planter has no published dimension, and the single photograph shows '
    'the object half-hidden behind its own planting. A drawing made from it '
    'would be an invention, so there isn’t one.</p></figure>')

OBSERVED = [
    ("Form", "A circular worktop at about bar height, on a flared pedestal"),
    ("Planting", "An aperture cut through the centre of the top, planted "
                 "through"),
    ("Finish", "A red-brown, which is none of the four named swatches"),
    ("Above it", "A pole through the planting carrying a pendant lamp"),
    ("Setting", "An office tea point, with chairs and a banquette around it"),
]


def cut(s, start, end):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def main():
    s = (SRC / "junglepots-pixie.html").read_text(encoding="utf-8")

    s = s.replace("<title>Pixie | JunglePots</title>",
                  "<title>Bar Planter | JunglePots</title>")
    s = s.replace("<span>Pixie</span>", "<span>Bar Planter</span>")

    # ---- hero ----------------------------------------------------------
    pre, _, post = cut(s, '<section class="wrap hero"', "</section>")
    controls = "\n".join(
        '<button data-view="%s" aria-pressed="%s">%02d / %s</button>'
        % (k, "true" if i == 0 else "false", i + 1, lbl)
        for i, (k, lbl) in enumerate(LABELS))
    v = VIEWS[0]
    hero = """<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="%s" alt="%s" width="900" height="1350"><figcaption><span class="hero-caption" aria-live="polite">%s</span><span class="hero-source">%s</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
%s
</div>
</div>
<div class="hero-copy"><p class="eyebrow">14 / PROJECT WORK</p><h1 id="collection-title">Bar<br>Planter</h1><p class="description">A table with a garden growing through it. One circular top at standing height, cut open at the centre and planted, on a flared pedestal — photographed once, in an office tea point, and never specified.</p><div class="hero-facts"><span>Circular worktop</span><span>Central planting aperture</span><span>One photograph</span><span>No schedule published</span></div><a href="#inquiry" class="text-link">Start a project enquiry <span>↗</span></a><a href="#dimensions" class="quiet-link">What is published ↓</a><p class="small hero-note">Nothing is published for this collection — no dimensions, no capacity, no material. This page says so rather than filling the gaps.</p></div>
</section>""" % (v[1], v[2], v[3], v[4], controls)
    s = pre + hero + post

    # ---- "what is published", in place of the specification -------------
    observed = "".join(
        '<tr><th scope="row">%s</th><td>%s</td></tr>' % (k, t)
        for k, t in OBSERVED)
    pre, _, post = cut(s, '<section id="dimensions"', "</section>")
    spec = (
        '<section id="dimensions" class="wrap space"><div class="section-top">'
        '<p class="eyebrow">01 / WHAT IS PUBLISHED</p>'
        '<span class="eyebrow">ONE PHOTOGRAPH / NO SCHEDULE</span></div>'
        '<div class="section-heading"><h2>Nothing, and that is the point.'
        '</h2></div>'
        '<div class="spec-grid">' + NOTHING +
        '<div class="schedule">'
        '<p class="eyebrow">BAR PLANTER / PAGE 20</p>'
        '<p>The supplied catalogue gives Bar Planter <strong>one photograph '
        'and no specification</strong>. There are no dimensions, no capacity, '
        'no material description, no finish code and no variants — not '
        'incomplete ones, none at all. It is the only collection in the range '
        'treated this way, and Jungle Flora has no listing for it either.</p>'
        '<p class="small">Every other page on this site compares models in a '
        'table. There is no table here, because a row of empty cells would '
        'read as a specification with gaps rather than as an absence of '
        'one.</p>'
        '<details open class="verification"><summary>What the photograph '
        'shows — observation, not specification</summary>'
        '<table class="compare"><caption class="sr-only">Observations from the '
        'single Bar Planter photograph</caption><tbody>' + observed +
        '</tbody></table>'
        '<p>None of the above is published by anyone. It is what can be seen '
        'in one frame, written down so there is something concrete to ask '
        'about — not a specification, and not a basis for ordering.</p>'
        '<p>Two things in that photograph are worth asking about directly. '
        'The <strong>pole and pendant lamp</strong> rising through the '
        'planting may be part of the product or may belong to the building; '
        'no source says. And the <strong>red-brown finish</strong> is none of '
        'the four named colours — the same unnamed red-brown appears in the '
        'Big Ben Tower photography, so it is a real finish that the published '
        'range does not describe.</p></details>'
        '<a class="text-link" href="#inquiry">Start a project enquiry '
        '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- material: rewritten, as on Cube Shelf --------------------------
    pre, mat, post = cut(s, '<section id="material"', "</section>")
    mat = re.sub(r'<p class="material-intro">.*?</p>',
                 '<p class="material-intro">Not stated.<br>No material, '
                 'thickness or finish is published for this collection.</p>',
                 mat, flags=re.S)
    mat = re.sub(r'<dl>.*?</dl>',
                 '<dl><div><dt>Material</dt><dd class="absent">Not stated</dd>'
                 '</div><div><dt>Finish</dt><dd class="absent">Not stated'
                 '</dd></div><div><dt>Dimensions</dt>'
                 '<dd class="absent">Not published</dd></div>'
                 '<div><dt>Capacity</dt><dd class="absent">Not published</dd>'
                 '</div><div><dt>Variants</dt><dd class="absent">None listed'
                 '</dd></div><div><dt>Shown in</dt><dd>One office '
                 'installation</dd></div></dl>', mat, flags=re.S)
    mat = re.sub(r'<p class="small">Digital colours are indicative\..*?</p>',
                 '<p class="small">Digital colours are indicative — and for '
                 'this collection they are also beside the point. Bar Planter '
                 'is photographed in a <strong>red-brown that is none of '
                 'these four</strong>. The same unnamed red-brown appears in '
                 'the Big Ben Tower photography, so the published four-colour '
                 'range does not describe what the catalogue itself shows. '
                 'Ask for the actual finish rather than picking from '
                 'above.</p>', mat, flags=re.S)
    mat = re.sub(r'<details><summary>Material information &amp; '
                 r'specification limits</summary>.*?</details>',
                 '<details><summary>Why this panel is empty</summary>'
                 '<p>The material information on the other collection pages '
                 'comes from the general planter specification on page 23 — '
                 'galvanized steel under a powder coating, a sand-textured '
                 'finish, integrated adjustable feet — together with four '
                 'claims from Jungle Flora’s listings.</p>'
                 '<p>None of it is stated for Bar Planter, and Bar Planter is '
                 'not obviously a planter: it is a table with planting cut '
                 'into it. Applying the planter specification to it would be '
                 'a guess dressed as a fact, so this panel records what is '
                 'known, which is the photograph.</p></details>',
                 mat, flags=re.S)

    # the four swatches are a planter range that this collection is not part
    # of; leaving a colour picker on a page that says "ask for the actual
    # finish" would contradict the page
    mat = re.sub(r'<div class="swatches">.*?</div>', '', mat, flags=re.S)
    mat = re.sub(r'<p class="selected-colour"[^>]*>.*?</p>', '', mat, flags=re.S)

    s = pre + mat + post

    # ---- related --------------------------------------------------------
    pre, rel, post = cut(s, '<section id="related"', "</section>")
    rel = re.sub(
        r'<div class="related-grid">.*?</div></section>',
        '<div class="related-grid"><article><img '
        'src="related-assets/garden.png" alt="Isolated Garden tray, a long '
        'shallow suspended tray" width="880" height="660" loading="lazy">'
        '<details><summary><span>Garden<small>The other one that builds into '
        'the room.</small></span><span>+</span></summary><p>A planting tray '
        'suspended from the ceiling in four lengths. Like this one it is '
        'fitted rather than placed — and like this one its load is not '
        'published.</p><a href="junglepots-garden.html" class="text-link">'
        'View collection <span>↗</span></a></details></article>'
        '<article><img src="related-assets/grand-wall.png" alt="Isolated '
        'Grand Wall planter, a long low trough" width="880" height="660" '
        'loading="lazy"><details><summary><span>Grand Wall<small>The other '
        'one that divides a room.</small></span><span>+</span></summary>'
        '<p>Three lengths to 1900 mm at one section, on the floor, with a '
        'full dimensional schedule — the opposite case to this page.</p>'
        '<a href="junglepots-grand-wall.html" class="text-link">View '
        'collection <span>↗</span></a></details></article></div></section>',
        rel, flags=re.S)
    s = pre + rel + post

    s = s.replace('<p class="small inquiry-colour">Colour reference: '
                  'Anthracite 7016</p>',
                  '<p class="small inquiry-colour">Colour reference: to be '
                  'agreed — no colour range is published for this '
                  'collection.</p>')

    s = s.replace("<option>Pixie</option>",
                  "<option>Bar Planter</option><option>Pixie</option>")

    # ---- gallery --------------------------------------------------------
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join("%s:['%s','%s','%s','%s','%s']" % v for v in VIEWS)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]
    s = s.replace("hero.classList.toggle('isolated',true)",
                  "hero.classList.toggle('isolated',false)")
    s = s.replace("[].includes(b.dataset.view)",
                  "['top'].includes(b.dataset.view)")

    # ---- hero frame ------------------------------------------------------
    s = re.sub(r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:[^;]*;"
               r"[^<]*</style>",
               "<style>\n#jp-detail-review .hero-img{aspect-ratio:2/3;"
               "object-position:50% 50%}\n"
               "@container detail (max-width:800px)"
               "{#jp-detail-review .hero-img{aspect-ratio:2/3}}\n"
               "@container detail (max-width:600px)"
               "{#jp-detail-review .hero-img{aspect-ratio:2/3}}\n"
               "/* no drawing on this page: the plate holds a sentence */\n"
               "#jp-detail-review .drawing{align-items:flex-start;"
               "justify-content:flex-start;gap:14px;min-height:240px}\n</style>", s)

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
