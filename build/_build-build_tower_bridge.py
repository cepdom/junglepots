#!/usr/bin/env python3
"""Build the Tower Bridge collection page.

Derived from the approved Big Ben Tower page, so the chrome, the type, the
grid, the motion layer and every interaction are literally the same code --
this is the catalogue's second entry, not a second design.

What is Tower Bridge's own:

  * the specification drawing, traced from Tower Bridge's own isolated
    catalogue photograph. It carries two interior edges, the arch and the
    front/side corner, because that photograph resolves them: the arch is a
    high-contrast aperture, not a shadowed recess. Big Ben Tower's drawing
    stays an outline for the same reason in reverse;
  * the schedule, from catalogue page 27, with the unresolved 99 / 90 cm
    height carried visibly rather than silently resolved, and steel thickness
    and weight shown under their own marker because they are not the
    catalogue's;
  * five views. Four of them -- a second interior, a far better isolated
    product, the folded rim and the leg base -- come from a retail listing
    rather than from JunglePots, so each frame names its source and the
    provenance file carries an outstanding rights check.

The drawing is still traced from the catalogue photograph and not from the
sharper retail one: the retail shot lights the inner leg against white through
a soft gradient, and the traced edge comes out visibly wavy where the
catalogue crop gives a clean one. Better to look at, worse to measure.

There is no Tower Bridge specification PDF, so the download link becomes a
request rather than a dead file.
"""
import re
import shutil
import sys
from pathlib import Path

SRC = Path("/home/claude/s8")
OUT = SRC / "junglepots-tower-bridge.html"

DRAWING = Path("/home/claude/tb/tower-bridge-drawing.svg")
ASSETS = Path("/home/claude/tb/out-assets")

HERO_IMG = "hero-assets/tower-bridge-project-hero.jpg"
HERO_ALT = ("A Tower Bridge planter with its arched base, planted and "
            "installed against a fluted panel wall in a lounge interior")


def cut(s, start, end, what):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a], s[a:b], s[b:]


def main():
    s = (SRC / "junglepots-big-ben-tower.html").read_text(encoding="utf-8")

    # ---- the build ran build_drawing.py and the motion pass repeatedly, so
    #      nine identical style blocks and nine identical motion scripts are
    #      in the file. Keep one of each.
    for marker, head in (("/* ---- Specification drawing", "<style>"),
                         ("/* Motion layer.", "<style>")):
        blocks = [m for m in re.finditer(
            re.escape(head) + r"\s*\n" + re.escape(marker) + r".*?</style>",
            s, re.S)]
        for m in reversed(blocks[1:]):
            s = s[:m.start()] + s[m.end():]
    draw = list(re.finditer(
        r"<script>\n/\* The specification drawing draws itself once.*?</script>",
        s, re.S))
    for m in reversed(draw[1:]):
        s = s[:m.start()] + s[m.end():]

    # the interior edges are part of the drawing, so they draw with it
    s = s.replace("svg.querySelectorAll('.dwg-out')",
                  "svg.querySelectorAll('.dwg-out,.dwg-in')")

    # ---- identity -----------------------------------------------------
    s = s.replace("<title>Big Ben Tower | JunglePots</title>",
                  "<title>Tower Bridge | JunglePots</title>")
    s = s.replace('<span>Big Ben Tower</span>', '<span>Tower Bridge</span>')

    # ---- hero ---------------------------------------------------------
    pre, hero, post = cut(s, '<section class="wrap hero"', "</section>", "hero")
    hero = f"""<section class="wrap hero" aria-labelledby="collection-title">
<div class="hero-visual"><figure><img class="hero-img" src="{HERO_IMG}" alt="{HERO_ALT}" width="1100" height="1650"><figcaption><span class="hero-caption" aria-live="polite">IN CONTEXT</span><span class="hero-source">JUNGLE FLORA</span></figcaption></figure><div class="image-controls" aria-label="Collection gallery">
<button data-view="context" aria-pressed="true">01 / In context</button>
<button data-view="cafe" aria-pressed="false">02 / In use</button>
<button data-view="product" aria-pressed="false">03 / Product</button>
<button data-view="rim" aria-pressed="false">04 / Rim</button>
<button data-view="base" aria-pressed="false">05 / Base</button>
</div>
</div>
<div class="hero-copy"><p class="eyebrow">02 / SCULPTURAL PLANTERS</p><h1 id="collection-title">Tower<br>Bridge</h1><p class="description">The same square planting volume as Big Ben Tower, carried on an arch. One opening cut through the base turns a tall planter into a threshold.</p><div class="hero-facts"><span>Galvanized steel</span><span>Indoor / outdoor</span><span>One catalogued size</span><span>30 L capacity</span></div><a href="#inquiry" class="text-link">Request a quote <span>↗</span></a><a href="#dimensions" class="quiet-link">Explore dimensions ↓</a><p class="small hero-note">Catalogue height: 99 cm. Confirmation required before project specification.</p></div>
</section>"""
    s = pre + hero + post

    # ---- specification -------------------------------------------------
    svg = DRAWING.read_text()
    pre, spec, post = cut(s, '<section id="dimensions"', "</section>", "spec")
    spec = ('<section id="dimensions" class="wrap space"><div class="section-top">'
            '<p class="eyebrow">01 / SPECIFICATION</p>'
            '<span class="eyebrow">FORM / PROPORTION / VOLUME</span></div>'
            '<div class="section-heading"><h2>Dimensions &amp; variants.</h2>'
            '<div class="units" aria-label="Dimension units">'
            '<button data-unit="mm" aria-pressed="true">mm</button>'
            '<button data-unit="cm" aria-pressed="false">cm</button></div></div>'
            '<div class="spec-grid"><figure class="drawing">' + svg +
            '<figcaption>Traced from catalogue photography / not to scale'
            '</figcaption></figure><div class="schedule">'
            '<p class="eyebrow">TOWER BRIDGE / SINGLE MODEL</p>'
            '<table><caption class="sr-only">Tower Bridge catalogue '
            'specifications</caption><tbody>'
            '<tr><th scope="row"><span class="letter">A</span> Width</th>'
            '<td><span data-mm="400">400</span> <span class="unit">mm</span></td></tr>'
            '<tr><th scope="row"><span class="letter">B</span> Depth</th>'
            '<td><span data-mm="400">400</span> <span class="unit">mm</span></td></tr>'
            '<tr><th scope="row"><span class="letter">C</span> Overall height*</th>'
            '<td><span data-mm="990">990</span> <span class="unit">mm</span></td></tr>'
            '<tr><th scope="row">Capacity</th><td>30 L</td></tr>'
            # left out of the mm / cm toggle on purpose: sheet steel is
            # specified in millimetres whatever unit the schedule is showing
            '<tr><th scope="row">Steel thickness†</th><td>2 mm</td></tr>'
            '<tr><th scope="row">Weight†</th><td>6 kg</td></tr>'
            '</tbody></table>'
            '<p class="small">Source: supplied catalogue, page 27. The arch '
            'opening is not dimensioned anywhere in the catalogue, so its '
            'width, height and radius are shown but not specified.</p>'
            '<details open class="verification"><summary>* Height confirmation '
            'required</summary><p>The catalogue states 99 cm. The existing '
            'product listing states 90 cm, and so does the retail listing '
            'that supplies the product photography on this page — down to '
            'its page title. Two independent listings against the catalogue '
            'makes 90 cm the more likely figure, but we retain the catalogue '
            'value here rather than overrule the manufacturer. Please confirm '
            'with JunglePots before specifying.</p></details>'
            '<details class="verification"><summary>† Not from the '
            'catalogue</summary><p>Steel thickness and weight come from a '
            'retail listing, not from the supplied catalogue, which gives '
            'neither. They are shown because specifiers need them and '
            'withholding them helps nobody — but they carry a retailer’s '
            'authority, not the manufacturer’s. Confirm before '
            'specifying.</p></details>'
            '<a class="text-link" href="#inquiry">Request specification sheet '
            '<span>↗</span></a></div></div></section>')
    s = pre + spec + post

    # ---- related: Big Ben Tower takes the place Tower Bridge held --------
    pre, rel, post = cut(s, '<section id="related"', "</section>", "related")
    rel = rel.replace(
        '<img src="collection-assets/tower-bridge-project.jpg" '
        'alt="Tower Bridge planter with arched base in a glazed lounge '
        'interior" width="1467" height="2200" loading="lazy">',
        '<img src="hero-assets/big-ben-project-hero.jpg" '
        'alt="Big Ben Tower planters lining a glazed office corridor" '
        'width="1000" height="1500" loading="lazy">')
    rel = rel.replace(
        '<span>Tower Bridge<small>The arch as a defining gesture.</small></span>',
        '<span>Big Ben Tower<small>The same volume, on a stepped base.</small>'
        '</span>')
    rel = rel.replace(
        '<p>One catalogued model. A40 × B40 × C99 cm; 30 L. Height '
        'requires confirmation against existing 90 cm listings.</p>',
        '<p>One catalogued model. A40 × B40 × C99 cm; 30 L. The same '
        'schedule as Tower Bridge, and the same unresolved height.</p>')
    rel = rel.replace('data-related="Tower Bridge">Enquire about Tower Bridge',
                      'data-related="Big Ben Tower">Enquire about Big Ben Tower')
    s = pre + rel + post

    # ---- enquiry form defaults to this collection ------------------------
    s = s.replace(
        '<option>Big Ben Tower</option><option>Tower Bridge</option>',
        '<option>Tower Bridge</option><option>Big Ben Tower</option>')

    # ---- gallery -------------------------------------------------------
    # Five views, as on Big Ben Tower. Each carries its own frame proportion:
    # the planter is a tall object and the construction close-ups are
    # landscape, and one ratio cannot serve both without stranding either the
    # feet or half the frame.
    # Each view names its own source on the right of the frame. Four of the
    # five come from a retail listing rather than from JunglePots, and a
    # specifier should be able to see that without reading a provenance file.
    views = [
        ("context", HERO_IMG, HERO_ALT,
         "IN CONTEXT", "JUNGLE FLORA", "1/1.4"),
        ("cafe", "collection-assets/tower-bridge-context-cafe.jpg",
         "A Tower Bridge planter standing beside a glazed partition in a "
         "café interior, planted with a broad-leaved plant",
         "IN USE / CAFÉ INTERIOR", "RETAIL LISTING", "1/1.4"),
        ("product", "collection-assets/tower-bridge-isolated.png",
         "Isolated Tower Bridge planter, showing the arch cut through its base",
         "ISOLATED PRODUCT", "RETAIL LISTING", "4/5"),
        ("rim", "collection-assets/tower-bridge-rim.png",
         "Close view of the folded upper rim of Tower Bridge and the welded "
         "inner liner below it",
         "FOLDED RIM / INNER LINER", "RETAIL LISTING", "1/0.78"),
        ("base", "collection-assets/tower-bridge-base.png",
         "Close view of the underside of the two legs of Tower Bridge, each "
         "with two adjustable levelling feet",
         "LEG BASE / ADJUSTABLE FEET", "RETAIL LISTING", "1/1"),
    ]
    old = re.search(r"const gallery=\{.*?\};", s, re.S)
    entries = ",".join(
        "%s:['%s','%s','%s','%s','%s']" % (k, src, alt, cap, who, ar)
        for k, src, alt, cap, who, ar in views)
    s = s[:old.start()] + "const gallery={" + entries + "};" + s[old.end():]

    old = re.search(r"root\.querySelectorAll\('\[data-view\]'\)\.forEach"
                    r"\(b=>b\.addEventListener\('click',\(\)=>\{.*?\}\)\);",
                    s, re.S)
    s = (s[:old.start()] +
         "root.querySelectorAll('[data-view]').forEach(b=>b.addEventListener("
         "'click',()=>{const v=gallery[b.dataset.view];hero.src=v[0];"
         "hero.alt=v[1];hero.classList.toggle('isolated',"
         "b.dataset.view==='product');hero.classList.toggle('detail-view',"
         "['rim','base'].includes(b.dataset.view));hero.style.aspectRatio=v[5];"
         "root.querySelector('.hero-caption').textContent=v[2];"
         "root.querySelector('.hero-source').textContent=v[3];"
         "root.querySelectorAll('[data-view]').forEach(x=>x.setAttribute("
         "'aria-pressed',String(x===b)))}));" +
         s[old.end():])

    # ---- collection router: a map, so the next page is one line ---------
    s = re.sub(
        r"if\(el\.dataset\.collection\)\{url=[^}]*\}",
        "if(el.dataset.collection){const pages={'Big Ben Tower':"
        "'junglepots-big-ben-tower.html','Tower Bridge':"
        "'junglepots-tower-bridge.html'};url=pages[el.dataset.collection]||"
        "'junglepots-collections.html#'+el.dataset.collection.toLowerCase()"
        ".replaceAll(' ','-')}", s)

    # ---- the interior edges need a weight of their own -------------------
    s = s.replace(
        "#jp-detail-review .spec-drawing .dwg-out{stroke:var(--ink);"
        "stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;fill:none}",
        "#jp-detail-review .spec-drawing .dwg-out{stroke:var(--ink);"
        "stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;fill:none}\n"
        "/* Interior edges sit lighter than the silhouette, the way a hand "
        "drawing separates the form from what happens inside it. */\n"
        "#jp-detail-review .spec-drawing .dwg-in{stroke:var(--ink);"
        "stroke-width:1.5;stroke-linejoin:round;stroke-linecap:round;fill:none}")

    # ---- the hero frame, sized to this photograph ------------------------
    # Big Ben's context photograph is a corridor with planters along it and
    # crops happily to a near-square. There is one Tower Bridge photograph and
    # the arch is the whole point of the collection, so the frame is deeper
    # here: the planter stands complete in it, feet to rim. Appended last so
    # it also outranks the 600 px container rule.
    s = s.replace("</body></html>", """<style>
#jp-detail-review .hero-img{aspect-ratio:1/1.4;object-position:45% 44%}
@container detail (max-width:600px){#jp-detail-review .hero-img{aspect-ratio:1/1.4}}
</style>
</body></html>""")

    # ---- the finish, photographed twice and not matching -----------------
    s = s.replace(
        "<p class=\"small\">Digital colours are indicative. The photographed "
        "red-brown finish has no identified catalogue code. Confirm a "
        "physical sample for your project.</p>",
        "<p class=\"small\">Digital colours are indicative. The photographed "
        "red-brown finish has no identified catalogue code, and the two "
        "sources do not agree: the project photography reads as a deep brick "
        "red, the studio photography as a warmer terracotta. That may be "
        "white balance rather than two finishes, but it cannot be settled "
        "from photographs. Confirm a physical sample for your project.</p>")

    OUT.write_text(s, encoding="utf-8")
    for f in ASSETS.iterdir():
        if f.suffix in (".png", ".jpg"):
            shutil.copy(f, SRC / "collection-assets" / f.name)
    print("wrote", OUT.name, len(s), "bytes")


if __name__ == "__main__":
    main()
