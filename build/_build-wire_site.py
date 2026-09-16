#!/usr/bin/env python3
"""Link the Tower Bridge page into the rest of the site.

Three things have to know a collection page exists: the collection index card,
the client-side router that every page carries, and the collections data file
the React build will be fed from. The router becomes a slug map here, so the
next collection page is one line rather than another edit to eight files.
"""
import json
import re
from pathlib import Path

SRC = Path("/home/claude/s8")

PAGES = {"Big Ben Tower": "junglepots-big-ben-tower.html",
         "Tower Bridge": "junglepots-tower-bridge.html",
         "Siena Kubo": "junglepots-siena-kubo.html",
         "Siena": "junglepots-siena.html",
         "Dawn": "junglepots-dawn.html",
         "Grand Wall": "junglepots-grand-wall.html",
         "Garden": "junglepots-garden.html",
         "Cube Shelf": "junglepots-cube-shelf.html",
         "Riverside Flow": "junglepots-riverside-flow.html",
         "Riverside Rise": "junglepots-riverside-rise.html",
         "Riverside Base": "junglepots-riverside-base.html",
         "Pixie": "junglepots-pixie.html",
         "Bar Planter": "junglepots-bar-planter.html"}

ROUTER = ("if(el.dataset.collection){const pages=" +
          json.dumps(PAGES, separators=(",", ":")).replace('"', "'") +
          ";url=pages[el.dataset.collection]||'junglepots-collections.html#'"
          "+el.dataset.collection.toLowerCase().replaceAll(' ','-')}")


def main():
    # ---- the router, on every page that carries one
    for f in sorted(SRC.glob("junglepots-*.html")):
        s = f.read_text(encoding="utf-8")
        new = re.sub(r"if\(el\.dataset\.collection\)\{(?:const pages=\{[^}]*\};)?"
                     r"url=[^}]*\}", ROUTER, s)
        if new != s:
            f.write_text(new, encoding="utf-8")
            print("router  ", f.name)

    # ---- the collection index card gains the link the Big Ben card has
    f = SRC / "junglepots-collections.html"
    s = f.read_text(encoding="utf-8")
    before = s
    for label, page in (("Tower%20Bridge", "junglepots-tower-bridge.html"),
                        ("Siena%20Kubo", "junglepots-siena-kubo.html"),
                        ("Siena", "junglepots-siena.html"),
                        ("Dawn", "junglepots-dawn.html"),
                        ("Grand%20Wall", "junglepots-grand-wall.html"),
                        ("Garden", "junglepots-garden.html"),
                        ("Cube%20Shelf", "junglepots-cube-shelf.html"),
                        ("Riverside%20Flow", "junglepots-riverside-flow.html"),
                        ("Riverside%20Rise", "junglepots-riverside-rise.html"),
                        ("Riverside%20Base", "junglepots-riverside-base.html"),
                        ("Pixie", "junglepots-pixie.html"),
                        ("Bar%20Planter", "junglepots-bar-planter.html")):
        # guard on the anchor itself, not on the page name: the router map
        # further down the file mentions every page, so a name test always
        # passes and the link silently never gets added
        anchor = ('href="mailto:info@jungleflora.lt?subject=JunglePots%20enquiry'
                  '%20%E2%80%94%20' + label + '">Enquire <span>\u2197</span></a>'
                  "</div></details>")
        link = ('<a class="text-link" href="' + page +
                '">View collection <span>\u2197</span></a>')
        if anchor in s and link not in s:
            s = s.replace(anchor, anchor + link)
            print("index    card linked ->", page)
    if s != before:
        f.write_text(s, encoding="utf-8")

    # ---- the data file the production build reads
    f = SRC / "JunglePots-collections-data.json"
    data = json.loads(f.read_text(encoding="utf-8"))
    for c in data:
        for slug, page in (("tower-bridge", "junglepots-tower-bridge.html"),
                           ("siena-kubo", "junglepots-siena-kubo.html"),
                           ("siena", "junglepots-siena.html"),
                           ("dawn", "junglepots-dawn.html"),
                           ("grand-wall", "junglepots-grand-wall.html"),
                           ("garden", "junglepots-garden.html"),
                           ("cube-shelf", "junglepots-cube-shelf.html"),
                           ("riverside-flow", "junglepots-riverside-flow.html"),
                           ("riverside-rise", "junglepots-riverside-rise.html"),
                           ("riverside-base", "junglepots-riverside-base.html"),
                           ("pixie", "junglepots-pixie.html"),
                           ("bar-planter", "junglepots-bar-planter.html")):
            if c["slug"] == slug:
                c["detail"] = page
    f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                 encoding="utf-8")
    print("data     detail pages set")


if __name__ == "__main__":
    main()
