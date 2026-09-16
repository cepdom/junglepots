#!/usr/bin/env python3
"""Two chrome corrections, applied to every page.

1. The header flapped open and shut around one scroll position. It condensed
   on a single threshold -- scrollY > 24 -- so any movement that hovered
   around 24 px crossed it repeatedly, and each crossing animated the service
   rail's height and the bar's, 34 px of layout, at whatever rate the wheel or
   trackpad was oscillating. A single threshold is the bug; the fix is two.
   It now condenses only past 96 px, which is clear of the rail, and expands
   only back under 28 px, so the two states never trade inside the same
   gesture. The flag is held in JS rather than read back off the DOM, so the
   comparison never depends on the attribute the transition is mid-way
   through.

2. The oversized closing wordmark is removed. Its vertical rhythm is kept --
   the bottom rule inherits the margin the wordmark used to carry -- so the
   footer still breathes at the bottom instead of collapsing onto the rule.
"""
import re
from pathlib import Path

SRC = Path("/home/claude/s8")

OLD_SCROLL = """  // condense on scroll
  let ticking=false;
  const onScroll=()=>{
    if(ticking)return;
    ticking=true;
    requestAnimationFrame(()=>{
      header.toggleAttribute('data-scrolled',window.scrollY>24);
      ticking=false;
    });
  };"""

NEW_SCROLL = """  // condense on scroll, with hysteresis: one threshold would let a small
  // movement around it flap the rail open and shut inside a single gesture
  const CONDENSE=96, RELEASE=28;
  let ticking=false, condensed=false;
  const onScroll=()=>{
    if(ticking)return;
    ticking=true;
    requestAnimationFrame(()=>{
      const y=window.scrollY;
      if(!condensed&&y>CONDENSE)condensed=true;
      else if(condensed&&y<RELEASE)condensed=false;
      header.toggleAttribute('data-scrolled',condensed);
      ticking=false;
    });
  };"""


def main():
    for f in sorted(SRC.glob("junglepots-*.html")):
        s = f.read_text(encoding="utf-8")
        before = s

        s = s.replace(OLD_SCROLL, NEW_SCROLL)

        # the wordmark itself
        s = re.sub(r'\n?<p class="jpc-f-wordmark"[^>]*>.*?</p>', "", s)

        # its rule, and the bottom rule takes over its spacing
        s = re.sub(r'\n[^{}]*\.jpc-f-wordmark[^{]*\{[^}]*\}', "", s)
        s = re.sub(r'(\.jpc-f-bottom\{\n?\s*display:flex;)',
                   r'\1margin-top:clamp(56px,7cqi,120px);', s)

        if s != before:
            f.write_text(s, encoding="utf-8")
            print("patched", f.name)


if __name__ == "__main__":
    main()
