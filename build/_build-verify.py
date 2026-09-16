#!/usr/bin/env python3
"""Headless check of the built pages.

Per page and width, with motion and with reduced motion forced: console and
page errors, horizontal overflow, chrome controls under the 44 px touch
minimum, exactly one aria-current, images that failed to load, and anything
left invisible after the motion layer has had time to finish.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/home/claude/s8")
WIDTHS = [1920, 1440, 1024, 768, 390]
PAGES = sys.argv[1:] or ["junglepots-tower-bridge.html"]

CHECK = """() => {
  const out = {small: [], hidden: [], broken: [], current: 0};
  document.querySelectorAll('[aria-current="page"]').forEach(() => out.current++);
  document.querySelectorAll(
    '.jpc-header a,.jpc-header button,.jpc-footer a,.jpc-menu a,' +
    '.image-controls button,.units button,.swatches button,main a,main button'
  ).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.height < 43.5) out.small.push(el.className + '|' +
      (el.textContent || '').trim().slice(0, 28) + '|' + r.height.toFixed(1));
  });
  document.querySelectorAll('img').forEach(i => {
    if (!i.complete || i.naturalWidth === 0) out.broken.push(i.getAttribute('src'));
  });
  document.querySelectorAll('main *').forEach(el => {
    const cs = getComputedStyle(el);
    if (parseFloat(cs.opacity) < 0.99 && el.getBoundingClientRect().height > 0
        && !el.closest('details:not([open])'))
      out.hidden.push(el.tagName + '.' + el.className);
  });
  document.querySelectorAll('.spec-drawing path').forEach(p => {
    const o = parseFloat(getComputedStyle(p).strokeDashoffset) || 0;
    if (Math.abs(o) > 0.5) out.hidden.push('dashoffset ' + o.toFixed(1));
  });
  out.overflow = document.documentElement.scrollWidth -
                 document.documentElement.clientWidth;
  return out;
}"""


def run(pw, page_name, width, reduced):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": width, "height": 900},
                        reduced_motion="reduce" if reduced else "no-preference")
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / page_name).as_uri(), wait_until="load")
    # a lazy image that never entered the viewport reports incomplete, which
    # reads as a broken source. Load them all before judging.
    pg.evaluate("() => document.querySelectorAll('img[loading=lazy]')"
                ".forEach(i => i.loading = 'eager')")
    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(5000)
    pg.evaluate("() => window.scrollTo(0, 0)")
    pg.wait_for_timeout(600)
    # let every running animation settle: an element caught mid-fade reads as
    # stuck invisible when it is only part-way through a 700 ms reveal
    pg.evaluate("""() => Promise.all(
        document.getAnimations().map(a => a.finished.catch(() => {})))""")
    pg.wait_for_timeout(200)
    r = pg.evaluate(CHECK)
    r["errors"] = errs
    b.close()
    return r


def main():
    bad = 0
    with sync_playwright() as pw:
        for name in PAGES:
            for w in WIDTHS:
                for reduced in (False, True):
                    r = run(pw, name, w, reduced)
                    tag = f"{name:34s} {w:5d} {'reduced' if reduced else 'motion ':>7s}"
                    issues = []
                    if r["errors"]:
                        issues.append(f"errors={r['errors'][:2]}")
                    if r["overflow"] > 0:
                        issues.append(f"overflow={r['overflow']}")
                    if r["small"]:
                        issues.append(f"small={r['small'][:3]}")
                    if r["broken"]:
                        issues.append(f"broken={r['broken'][:3]}")
                    if r["hidden"]:
                        issues.append(f"hidden={r['hidden'][:3]}")
                    if r["current"] != 1:
                        issues.append(f"aria-current={r['current']}")
                    print(tag, "OK" if not issues else " | ".join(issues))
                    bad += bool(issues)
    print("\n" + ("ALL CLEAN" if not bad else f"{bad} configuration(s) with issues"))


if __name__ == "__main__":
    main()
