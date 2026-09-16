#!/usr/bin/env python3
"""Give every page the metadata it needs to be shared.

All twenty pages carried exactly two meta tags -- charset and viewport. No
description, no Open Graph, no card image, no favicon. Paste any URL from this
site into Slack, LinkedIn, an email client or a CMS preview and you get a bare
link: no title card, no picture, no sentence. For a site whose whole job is to
be sent to an architect, that is the most consequential thing missing from it,
and it is fixable from what the pages already contain.

Each page already has a <title>, a hero image and, on fifteen of twenty, a
description paragraph. This reuses those rather than writing new copy; the five
pages with no description paragraph get one written here.

**The card image.** A transparent PNG makes a poor share card -- it renders on
whatever background the platform happens to use, which for the cutouts on this
site means the product vanishes into white. So the picker prefers a JPEG from
the page and only falls back to the hero when the hero is one.

**og:image needs an absolute URL at deploy.** Scrapers vary on relative paths
and several ignore them. BASE below is empty because no production domain has
been set; set it to "https://junglepots.eu" (no trailing slash) and re-run, and
every card image becomes absolute. That is the one line to change.

**The favicon** is derived from the existing wordmark -- the paper "J" of
"JunglePots." on the olive of the review chrome -- not invented. It is inlined
as an SVG data URI so there is no extra file to deploy. Swap it for a supplied
mark when there is one.
"""
import glob
import html
import re
from pathlib import Path

SRC = Path("/home/claude/s8")

# set to e.g. "https://junglepots.eu" at deploy; see the module docstring
BASE = ""

SITE = "JunglePots"
DEFAULT_IMAGE = "refinement-assets/terrace-lounge.jpg"

# Garden, Pixie and Siena have no photograph at all -- every image on those
# pages is a transparent cutout -- so each gets a card built by compositing the
# cutout onto the paper ground at the 1.91:1 platforms crop to. The index and
# the two homepages get a representative photograph rather than whichever
# JPEG happens to appear first in the markup.
CARD = {
    "junglepots-garden.html": "card-assets/garden.jpg",
    "junglepots-pixie.html": "card-assets/pixie.jpg",
    "junglepots-siena.html": "card-assets/siena.jpg",
    "junglepots-collections.html": "refinement-assets/terrace-lounge.jpg",
    "junglepots-homepage.html": "refinement-assets/terrace-lounge.jpg",
    "junglepots-homepage-hero.html": "refinement-assets/terrace-lounge.jpg",
}

# the five pages with no description paragraph to reuse
WRITTEN = {
    "junglepots-about.html":
        "The people and the workshop behind JunglePots: galvanized steel "
        "planters made in Lithuania for architectural and commercial "
        "projects.",
    "junglepots-b2b.html":
        "Specification support, volume pricing and project delivery for "
        "architects, interior designers, contractors and distributors "
        "working with JunglePots.",
    "junglepots-collections.html":
        "Every JunglePots collection in one index: thirteen ranges of "
        "galvanized steel planters, from a 150 mm cube to a 2.2 m suspended "
        "tray, with dimensions and drawings for each.",
    "junglepots-contact.html":
        "Start a project enquiry with JunglePots. Send drawings, quantities "
        "and a brief, and get a specification and a quote back.",
    "junglepots-production-quality.html":
        "How JunglePots planters are made: folded and welded galvanized "
        "steel, primed and powder-coated, with the joints, rims and feet "
        "shown close up.",
}

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='6' fill='%233E4739'/%3E"
    "%3Ctext x='16' y='23' font-family='Helvetica,Arial,sans-serif' "
    "font-size='20' font-weight='600' fill='%23F3F1EB' "
    "text-anchor='middle'%3EJ%3C/text%3E%3C/svg%3E")


def strip(t):
    """Markup and entities out, one clean sentence in."""
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def describe(name, s):
    if name in WRITTEN:
        return WRITTEN[name]
    m = re.search(r'<p class="description">(.*?)</p>', s, re.S)
    if not m:
        return ("Architectural planters in galvanized steel, made in "
                "Lithuania for commercial and landscape projects.")
    d = strip(m.group(1))
    if len(d) <= 158:
        return d
    # take whole sentences up to the limit, not just the first one: these
    # descriptions open with a short declarative and the useful detail is in
    # the sentence after it
    out = ""
    for part in re.split(r"(?<=[.!?]) ", d):
        if len(out) + len(part) + 1 > 158:
            break
        out = (out + " " + part).strip()
    # these descriptions open with a short declarative and carry the useful
    # detail in a long sentence after it, so whole-sentence packing often
    # yields a 30-character stub. Below ~110 characters, cut the full text on
    # a word boundary instead -- a trailing ellipsis reads better than a
    # description that says nothing.
    if len(out) >= 110:
        return out
    return d[:155].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"


def card_image(name, s):
    if name in CARD:
        return CARD[name]
    """A JPEG if the page has one: a transparent PNG renders on whatever
    background the platform picks, and these cutouts disappear on white."""
    jpegs = re.findall(r'<img[^>]+src="((?!data:)[^"]+\.jpe?g)"', s)
    if jpegs:
        return jpegs[0]
    hero = re.search(r'class="hero-img[^"]*" src="([^"]+)"', s)
    return hero.group(1) if hero and hero.group(1).endswith(
        (".jpg", ".jpeg")) else DEFAULT_IMAGE


def main():
    for f in sorted(SRC.glob("junglepots-*.html")):
        s = f.read_text(encoding="utf-8")
        # idempotent: drop any block this script wrote before re-adding
        s = re.sub(r'<meta name="description".*?<link rel="icon" href="[^"]*">',
                   "", s, flags=re.S)

        title = strip(re.search(r"<title>(.*?)</title>", s).group(1))
        desc = describe(f.name, s)
        img = card_image(f.name, s)
        url_img = (BASE + "/" + img) if BASE else img

        meta = (
            '<meta name="description" content="%s">'
            '<meta name="theme-color" content="#F3F1EB">'
            '<meta property="og:type" content="website">'
            '<meta property="og:site_name" content="%s">'
            '<meta property="og:locale" content="en_GB">'
            '<meta property="og:title" content="%s">'
            '<meta property="og:description" content="%s">'
            '<meta property="og:image" content="%s">'
            '<meta name="twitter:card" content="summary_large_image">'
            '<meta name="twitter:title" content="%s">'
            '<meta name="twitter:description" content="%s">'
            '<meta name="twitter:image" content="%s">'
            '<link rel="icon" href="%s">'
            % (html.escape(desc, quote=True), SITE,
               html.escape(title, quote=True), html.escape(desc, quote=True),
               html.escape(url_img, quote=True),
               html.escape(title, quote=True), html.escape(desc, quote=True),
               html.escape(url_img, quote=True), FAVICON))

        s = s.replace("</title>", "</title>" + meta, 1)
        f.write_text(s, encoding="utf-8")
        print("meta    %-36s %-30s %s" % (f.name, img.split("/")[-1],
                                          desc[:58] + "…"))


if __name__ == "__main__":
    main()
