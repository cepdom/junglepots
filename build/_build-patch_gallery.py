#!/usr/bin/env python3
"""Two defects the Garden build turned up, fixed across the whole family.

1. `hero.style.aspectRatio=v[5]` on a five-element array. The gallery entry is
   [src, alt, caption, source, ratio]; index 5 is undefined, so assigning it
   sets nothing and the per-view aspect ratio has never applied on any page
   since Tower Bridge. Views that should have switched between portrait and
   landscape have all been rendering in whatever the CSS said.

2. The template styles `.hero-img` at three container breakpoints -- base, 800
   and 600 -- and each page's trailing override block has only ever set base
   and 600. Between 600 and 800 the hero fell back to the template's portrait
   ratio, so a landscape product view was cropped to a portrait slot at that
   one width. The 800 rule is inserted carrying the page's own base ratio.

Big Ben Tower has neither a gallery nor a trailing override block and is left
alone.
"""
import re
from pathlib import Path

SRC = Path("/home/claude/s8")
PAGES = ["junglepots-tower-bridge.html", "junglepots-siena.html",
         "junglepots-siena-kubo.html", "junglepots-dawn.html",
         "junglepots-grand-wall.html"]

BLOCK = re.compile(
    r"<style>\n#jp-detail-review \.hero-img\{aspect-ratio:([^;}]+)[^}]*\}\n"
    r"(?!@container detail \(max-width:800px\))")


def main():
    for name in PAGES:
        f = SRC / name
        s = f.read_text(encoding="utf-8")
        before = s

        s = s.replace("hero.style.aspectRatio=v[5]",
                      "hero.style.aspectRatio=v[4]")

        m = BLOCK.search(s)
        if m:
            rule = ("@container detail (max-width:800px)"
                    "{#jp-detail-review .hero-img{aspect-ratio:%s}}\n"
                    % m.group(1))
            s = s[:m.end()] + rule + s[m.end():]

        if s != before:
            f.write_text(s, encoding="utf-8")
            print("patched", name, "->", m.group(1) if m else "ratio only")


if __name__ == "__main__":
    main()
