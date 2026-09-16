#!/usr/bin/env python3
"""Related-collections cards: the catalogue's own isolated plates, larger.

They were showing project photography cropped to a 4:5 portrait sliver 150 px
wide -- a fragment of an interior, at a size where the interior is unreadable
and the planter is a silhouette in it. The collection index already solves
this: each collection has an isolated plate, the product cut out and laid on
the plate tint. Those are what a reader recognises a collection by, so the
related cards now use the same asset, in the same frame, at the same 4:3.

Wider, too. The column grows from 150 to 250 px, which is as far as it can go
before the card's own text has to wrap awkwardly against it.
The plates are not the index's own files. Those are laid out for a 380 px
card and the product reads as a speck at 230; these are rebuilt from the same
cutouts on a 4:3 plate with the product filling it, and the index's
optical-weight pass retuned so a cube and a tower still carry the same weight
beside each other.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/claude/s8")
PLATE_DIR = Path("/home/claude/tb/related-assets")

# page -> {old image src fragment: (new src, alt, w, h)}
# Each entry: every src this card has previously carried -> the plate it
# should carry now, so the patch can be re-run without hunting for which
# version of the page it is looking at.
PLATES = [
    (["hero-assets/big-ben-project-hero.jpg",
      "collection-assets/big-ben-project-entry.jpg",
      "index-assets/big-ben-tower.png"],
     "related-assets/big-ben-tower.png",
     "Isolated Big Ben Tower planter showing its complete architectural form"),
    (["collection-assets/tower-bridge-project.jpg",
      "index-assets/tower-bridge.png"],
     "related-assets/tower-bridge.png",
     "Isolated Tower Bridge planter showing its complete architectural form"),
    (["collection-assets/siena-kubo-project.jpg",
      "index-assets/siena-kubo.png"],
     "related-assets/siena-kubo.png",
     "Isolated Siena Kubo planter showing its cubic form"),
]

CSS = """
/* ---- Related collections: isolated plates, as on the collection index ---- */
__R__ .related-grid article{grid-template-columns:250px 1fr;gap:28px}
__R__ .related-grid img{
  aspect-ratio:4/3;object-fit:contain;background:var(--plate);padding:8px;
}
@container detail (max-width:900px){
  /* two cards side by side leave ~140px for a title once the plate has its
     250px, so the pair stacks here rather than at 600 */
  __R__ .related-grid{grid-template-columns:1fr;gap:30px}
  __R__ .related-grid article{grid-template-columns:200px 1fr;gap:24px}
}
@container detail (max-width:600px){
  __R__ .related-grid article{grid-template-columns:150px 1fr;gap:18px}
  __R__ .related-grid article+article img{aspect-ratio:4/3}
}
"""


def main():
    dst = SRC / "related-assets"
    dst.mkdir(exist_ok=True)
    for f in PLATE_DIR.glob("*.png"):
        shutil.copy(f, dst / f.name)

    for name, root in (("junglepots-tower-bridge.html", "#jp-detail-review"),
                       ("junglepots-big-ben-tower.html", "#jp-detail-review")):
        f = SRC / name
        s = f.read_text(encoding="utf-8")
        before = s

        rel = re.search(r'<section id="related".*?</section>', s, re.S)
        block = rel.group(0)
        for olds, new, alt in PLATES:
            for old in olds:
                block = re.sub(
                    r'<img src="%s"[^>]*>' % re.escape(old),
                    '<img src="%s" alt="%s" width="880" height="660" '
                    'loading="lazy">' % (new, alt), block)
        s = s[:rel.start()] + block + s[rel.end():]

        if "Related collections: isolated plates" not in s:
            s = s.replace("</body></html>",
                          "<style>" + CSS.replace("__R__", root) +
                          "</style>\n</body></html>")

        if s != before:
            f.write_text(s, encoding="utf-8")
            print("patched", name)


if __name__ == "__main__":
    main()
