#!/usr/bin/env python3
"""One shared header and footer across all eight pages.

The pages were built at different times and had drifted into two different
header implementations (.site-header / .header), two menu buttons, two mobile
menus, inconsistent aria-current, and -- on six of eight pages -- a "Request a
quote" action that was display:none at mobile and missing from the mobile menu
entirely, leaving the site's primary action unreachable on a phone.

This replaces both with one component:

  * sticky header that condenses on scroll, so navigation stays reachable on
    pages that run to 6000px;
  * the quote action always reachable, including inside the mobile menu;
  * exactly one aria-current="page" per page;
  * a real skip link and a main landmark on every page;
  * 44px minimum on every control;
  * mobile menu with Escape, focus move and return, and scroll lock;
  * footer with column labels, a restored "back to top", and a wordmark that
    scales with its own container rather than the viewport.

Styling hangs off new jpc- classes so none of the old rules apply. The legacy
class names are kept on the toggle and menu only so that older page scripts
still resolve their selectors; their listeners are then detached by cloning
the button, and this component binds its own.
"""
import re, os, glob

NAV = [
    ("About",                "junglepots-about.html"),
    ("Products",             "junglepots-collections.html"),
    ("Production / Quality", "junglepots-production-quality.html"),
    ("B2B Business",         "junglepots-b2b.html"),
    ("Contact",              "junglepots-contact.html"),
]
HOME = "junglepots-homepage-hero.html"
QUOTE = "junglepots-contact.html"

# which nav item is current for each page
ACTIVE = {
    "junglepots-about.html": "About",
    "junglepots-collections.html": "Products",
    "junglepots-big-ben-tower.html": "Products",
    "junglepots-production-quality.html": "Production / Quality",
    "junglepots-b2b.html": "B2B Business",
    "junglepots-contact.html": "Contact",
    "junglepots-homepage.html": None,        # home is the wordmark
    "junglepots-homepage-hero.html": None,
}

EMAIL = "info@jungleflora.lt"
PHONE_TEXT = "+370 600 20608"
PHONE_HREF = "+37060020608"


def header_html(page, menu_id):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if ACTIVE.get(page) == label else ""
        items.append(f'<a href="{href}"{cur}>{label}</a>')
    menu_items = []
    for i, (label, href) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if ACTIVE.get(page) == label else ""
        menu_items.append(
            f'<a href="{href}"{cur}><small>0{i}</small><span>{label}</span></a>')
    home_cur = ' aria-current="page"' if ACTIVE.get(page) is None else ""
    return f'''<a class="jpc-skip" href="#jp-main">Skip to content</a>
<header class="jpc-header">
<div class="jpc-rail"><span>ARCHITECTURAL PLANTERS \u2014 LITHUANIA</span><a href="tel:{PHONE_HREF}">{PHONE_TEXT}</a></div>
<div class="jpc-bar">
<a class="jpc-mark" href="{HOME}"{home_cur} aria-label="JunglePots — home">JunglePots<span aria-hidden="true">.</span></a>
<nav class="jpc-nav" aria-label="Main navigation">{''.join(items)}</nav>
<a class="jpc-quote" href="{QUOTE}">Request a quote <span aria-hidden="true">↗</span></a>
<button class="jpc-toggle menu menu-button" type="button" aria-expanded="false" aria-controls="{menu_id}"><span>Menu</span><span class="jpc-burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
</div>
</header>
<nav class="jpc-menu mobile-nav" id="{menu_id}" aria-label="Site menu" hidden>
<div class="jpc-menu-inner">
{''.join(menu_items)}
<a class="jpc-menu-quote" href="{QUOTE}"><span>Request a quote</span><span aria-hidden="true">↗</span></a>
<div class="jpc-menu-contact">
<a href="mailto:{EMAIL}">{EMAIL}</a>
<a href="tel:{PHONE_HREF}">{PHONE_TEXT}</a>
</div>
</div>
</nav>'''


def footer_html():
    nav = "".join(f'<a href="{href}">{label}</a>' for label, href in NAV)
    return f"""<footer class="jpc-footer">
<div class="jpc-f-grid">
<div class="jpc-f-brand">
<p class="jpc-label">JUNGLEPOTS / LITHUANIA</p>
<p class="jpc-f-line">Architectural planters.<br>Professional projects.</p>
</div>
<nav class="jpc-f-col jpc-f-index" aria-label="Footer navigation">
<p class="jpc-label">INDEX</p>
{nav}
</nav>
<div class="jpc-f-col jpc-f-contact">
<p class="jpc-label">HEADQUARTERS &amp; PRODUCTION</p>
<a href="mailto:{EMAIL}">{EMAIL}</a>
<a href="tel:{PHONE_HREF}">{PHONE_TEXT}</a>
<a class="jpc-f-quote" href="{QUOTE}">Request a quote <span aria-hidden="true">&#8599;</span></a>
</div>
</div>
<p class="jpc-f-wordmark" aria-hidden="true">JunglePots.</p>
<div class="jpc-f-bottom">
<span>Form. Material. Living spaces.</span>
<span>&copy; JunglePots 2026</span>
<a class="jpc-f-top" href="#jp-main">Back to top <span aria-hidden="true">&#8593;</span></a>
</div>
</footer>"""


CSS = """
<style>
/* ===== Shared site chrome ==============================================
   Self-contained tokens: the eight pages name their custom properties
   differently (--paper vs --jp-paper), so the chrome carries its own.
   Every rule is prefixed with the page root id so it outranks the older
   per-page header and footer rules still present in the document. */
__R__ .jpc-header,__R__ .jpc-menu,__R__ .jpc-footer{
  --jpc-paper:#F3F1EB; --jpc-ink:#232822; --jpc-muted:#676B61;
  --jpc-line:#CCCFC4; --jpc-hair:#DEDFD6; --jpc-olive:#3E4739;
  font-family:Manrope,Arial,sans-serif;
  color:var(--jpc-ink);
}
__R__ .jpc-header a,__R__ .jpc-menu a,__R__ .jpc-footer a{
  color:inherit;text-decoration:none;
}
__R__ .jpc-label{
  font:11px/1.6 'IBM Plex Mono',monospace;letter-spacing:.06em;
  color:var(--jpc-muted);margin:0 0 16px;
}

/* ---- skip link ---- */
__R__ .jpc-skip{
  position:absolute;left:-9999px;top:0;z-index:60;
  background:var(--jpc-olive);color:var(--jpc-paper);
  padding:14px 20px;font-size:13px;
}
__R__ .jpc-skip:focus{left:0}

/* ---- header ---------------------------------------------------------
   Premium here is space and type contrast: a large, quiet wordmark against
   very small wide-tracked navigation, with almost nothing else in the bar. */
__R__ .jpc-header{
  position:sticky;top:0;z-index:40;
  background:var(--jpc-paper);
  border-bottom:1px solid var(--jpc-line);
}
__R__ .jpc-rail{
  display:flex;justify-content:space-between;align-items:center;gap:24px;
  padding:0 56px;height:38px;
  border-bottom:1px solid var(--jpc-hair);
  font:9.5px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;
  color:var(--jpc-muted);
  overflow:hidden;
  transition:height 420ms cubic-bezier(.16,.84,.44,1),opacity 300ms ease;
}
__R__ .jpc-rail a:hover{color:var(--jpc-ink)}
__R__ .jpc-header[data-scrolled] .jpc-rail{height:0;opacity:0;border-bottom-color:transparent}
__R__ .jpc-bar{
  display:flex;align-items:center;gap:48px;
  height:104px;padding-inline:56px;
  transition:height 420ms cubic-bezier(.16,.84,.44,1);
}
__R__ .jpc-header[data-scrolled] .jpc-bar{height:70px}
__R__ .jpc-mark{
  font-size:33px;font-weight:500;letter-spacing:-.062em;line-height:1;
  white-space:nowrap;display:flex;align-items:center;min-height:44px;
  transition:font-size 420ms cubic-bezier(.16,.84,.44,1);
}
__R__ .jpc-header[data-scrolled] .jpc-mark{font-size:26px}

/* navigation reads as a discreet index, not a row of links */
__R__ .jpc-nav{display:flex;gap:34px;margin-left:auto;align-items:center}
__R__ .jpc-nav a{
  position:relative;
  font-size:10.5px;font-weight:500;letter-spacing:.155em;text-transform:uppercase;
  color:var(--jpc-muted);
  min-height:44px;display:flex;align-items:center;white-space:nowrap;
  transition:color 380ms cubic-bezier(.16,.84,.44,1);
}
__R__ .jpc-nav a:hover{color:var(--jpc-ink)}
__R__ .jpc-nav a[aria-current="page"]{color:var(--jpc-ink)}
/* the marker is a short rule under the word, drawn from the left */
__R__ .jpc-nav a::after{
  content:"";position:absolute;left:0;right:.155em;bottom:12px;height:1px;
  background:currentColor;transform:scaleX(0);transform-origin:left;
  transition:transform 480ms cubic-bezier(.16,.84,.44,1);
}
__R__ .jpc-nav a:hover::after,__R__ .jpc-nav a[aria-current="page"]::after{transform:scaleX(1)}

/* the action speaks the site's label language rather than importing a button */
__R__ .jpc-quote{
  font:10.5px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;
  text-transform:uppercase;white-space:nowrap;
  display:flex;align-items:center;gap:13px;
  min-height:44px;margin-left:44px;
  transition:color 380ms ease;
}
__R__ .jpc-quote:hover{color:var(--jpc-olive)}
__R__ .jpc-quote span{transition:transform 420ms cubic-bezier(.16,.84,.44,1)}
__R__ .jpc-quote:hover span{transform:translate(4px,-4px)}

__R__ .jpc-toggle{
  display:none;align-items:center;gap:13px;margin-left:auto;
  min-height:44px;padding:0;border:0;background:none;cursor:pointer;
  font:10.5px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;
  text-transform:uppercase;color:inherit;
}
__R__ .jpc-burger{display:flex;flex-direction:column;gap:5px;width:20px}
__R__ .jpc-burger i{display:block;height:1px;background:currentColor;
  transition:transform 320ms cubic-bezier(.16,.84,.44,1),opacity 260ms ease}
__R__ .jpc-toggle[aria-expanded="true"] .jpc-burger i:nth-child(1){transform:translateY(6px) rotate(45deg)}
__R__ .jpc-toggle[aria-expanded="true"] .jpc-burger i:nth-child(2){opacity:0}
__R__ .jpc-toggle[aria-expanded="true"] .jpc-burger i:nth-child(3){transform:translateY(-6px) rotate(-45deg)}

/* ---- mobile menu ---- */
__R__ .jpc-menu{
  position:sticky;top:70px;z-index:39;
  background:var(--jpc-paper);border-bottom:1px solid var(--jpc-line);
}
__R__ .jpc-menu-inner{padding:18px 22px 40px}
__R__ .jpc-menu a{display:flex;align-items:center;gap:22px;
  padding-block:17px;font-size:27px;font-weight:400;letter-spacing:-.035em;line-height:1.2;
  border-bottom:1px solid var(--jpc-hair);min-height:44px}
__R__ .jpc-menu small{font:9.5px 'IBM Plex Mono',monospace;letter-spacing:.12em;color:var(--jpc-muted);width:24px}
__R__ .jpc-menu a[aria-current="page"] span{text-decoration:underline;text-underline-offset:7px}
__R__ .jpc-menu-quote{justify-content:space-between;font-size:19px!important;
  font-family:'IBM Plex Mono',monospace!important;letter-spacing:.1em!important;text-transform:uppercase}
__R__ .jpc-menu-contact{display:flex;flex-direction:column;padding-top:24px}
__R__ .jpc-menu-contact a{font-size:13px;border:0;padding-block:12px;min-height:44px;
  font-family:'IBM Plex Mono',monospace;letter-spacing:.08em;color:var(--jpc-muted)}

/* ---- footer -------------------------------------------------------- */
__R__ .jpc-footer{
  container-type:inline-size;
  background:var(--jpc-paper);
  padding:0 56px 30px;
  font:14px/1.75 Manrope,Arial,sans-serif;
}
__R__ .jpc-f-grid{
  display:grid;grid-template-columns:1.5fr 1fr 1.1fr;gap:6%;
  border-top:1px solid var(--jpc-line);padding-top:52px;
}
__R__ .jpc-f-line{margin:0;font-size:15px;line-height:1.7}
__R__ .jpc-f-col{display:flex;flex-direction:column;align-items:flex-start}
__R__ .jpc-f-col a{
  min-height:34px;display:flex;align-items:center;gap:10px;
  color:var(--jpc-muted);
  transition:color 380ms cubic-bezier(.16,.84,.44,1);
}
__R__ .jpc-f-col a:hover{color:var(--jpc-ink)}
__R__ .jpc-f-index a{
  font-size:10.5px;font-weight:500;letter-spacing:.155em;text-transform:uppercase;
  min-height:38px;
}
__R__ .jpc-f-quote{
  margin-top:26px;
  font:10.5px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;
  text-transform:uppercase;color:var(--jpc-ink)!important;
  padding-top:22px;border-top:1px solid var(--jpc-hair);width:100%;
  justify-content:space-between;
}
__R__ .jpc-f-quote:hover{color:var(--jpc-olive)!important}
__R__ .jpc-f-quote span{transition:transform 420ms cubic-bezier(.16,.84,.44,1)}
__R__ .jpc-f-quote:hover span{transform:translate(4px,-4px)}
__R__ .jpc-f-wordmark{
  font-size:clamp(54px,21.4cqi,320px);
  letter-spacing:-.075em;line-height:1.05;font-weight:500;
  margin:clamp(56px,7cqi,120px) 0 clamp(40px,4cqi,64px);
}
__R__ .jpc-f-bottom{
  display:flex;justify-content:space-between;align-items:center;gap:20px;
  flex-wrap:wrap;border-top:1px solid var(--jpc-line);padding-top:24px;
  font:9.5px/1.6 'IBM Plex Mono',monospace;letter-spacing:.14em;
  color:var(--jpc-muted);
}
__R__ .jpc-f-top{min-height:44px;display:flex;align-items:center;gap:11px;
  transition:color 380ms ease}
__R__ .jpc-f-top:hover{color:var(--jpc-ink)}

/* ---- focus ---- */
__R__ .jpc-header :focus-visible,__R__ .jpc-menu :focus-visible,
__R__ .jpc-footer :focus-visible,__R__ .jpc-skip:focus-visible{
  outline:2px solid var(--jpc-olive);outline-offset:4px;
}

@media (max-width:1250px){
  __R__ .jpc-bar{padding-inline:40px;gap:30px}
  __R__ .jpc-rail{padding-inline:40px}
  __R__ .jpc-nav{gap:24px}
  __R__ .jpc-nav a{font-size:10px;letter-spacing:.12em}
  __R__ .jpc-quote{font-size:10px;letter-spacing:.11em}
  __R__ .jpc-footer{padding-inline:40px}
  __R__ .jpc-f-grid{grid-template-columns:1fr 1fr;gap:40px;align-items:start}
  __R__ .jpc-f-brand{grid-column:1/-1}
}
@media (max-width:900px){
  /* the rail is 34-38px, so a tap target in it cannot reach 44px; the number
     stays reachable at full size in the menu and the footer */
  __R__ .jpc-rail a{display:none}
  __R__ .jpc-nav{display:none}
  __R__ .jpc-toggle{display:flex}
  __R__ .jpc-quote{margin-left:auto;order:2}
  __R__ .jpc-toggle{margin-left:0;order:3}
  __R__ .jpc-bar{height:84px;gap:20px}
  __R__ .jpc-header[data-scrolled] .jpc-bar{height:64px}
  __R__ .jpc-menu{top:64px}
}
@media (max-width:600px){
  __R__ .jpc-rail{padding-inline:22px;font-size:8.5px;letter-spacing:.1em;height:34px}
  __R__ .jpc-bar{padding-inline:22px;gap:14px;height:72px}
  __R__ .jpc-header[data-scrolled] .jpc-bar{height:58px}
  __R__ .jpc-menu{top:58px}
  __R__ .jpc-mark{font-size:27px}
  __R__ .jpc-header[data-scrolled] .jpc-mark{font-size:24px}
  __R__ .jpc-quote{font-size:9px;letter-spacing:.08em;gap:8px}
  __R__ .jpc-toggle{font-size:9px;letter-spacing:.08em;gap:9px}
  __R__ .jpc-footer{padding:0 22px 24px}
  __R__ .jpc-f-grid{grid-template-columns:1fr;gap:30px;padding-top:36px}
  __R__ .jpc-f-bottom{gap:10px;font-size:9px}
}
@media (pointer:coarse){__R__ .jpc-f-col a{min-height:44px}}
@media (prefers-reduced-motion:reduce){
  __R__ .jpc-bar,__R__ .jpc-mark,__R__ .jpc-nav a::after,
  __R__ .jpc-quote span,__R__ .jpc-burger i,__R__ .jpc-header{transition:none}
}
</style>
"""


JS = """
<script>
/* Shared chrome behaviour. Older page scripts bound their own handlers to the
   legacy .menu/.menu-button selectors; cloning the button detaches those so
   the two do not fight over the same toggle. */
(()=>{
  const header=document.querySelector('.jpc-header');
  const menu=document.querySelector('.jpc-menu');
  let toggle=document.querySelector('.jpc-toggle');
  if(!header||!menu||!toggle)return;

  const fresh=toggle.cloneNode(true);
  toggle.replaceWith(fresh);
  toggle=fresh;

  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  let open=false;

  const setOpen=(next)=>{
    open=next;
    toggle.setAttribute('aria-expanded',String(open));
    menu.hidden=!open;
    document.documentElement.style.overflow=open?'hidden':'';
    if(open){
      const first=menu.querySelector('a');
      if(first)first.focus({preventScroll:true});
    }
  };

  toggle.addEventListener('click',()=>setOpen(!open));

  menu.addEventListener('keydown',(e)=>{
    if(e.key!=='Escape')return;
    setOpen(false);
    toggle.focus({preventScroll:true});
  });
  toggle.addEventListener('keydown',(e)=>{
    if(e.key==='Escape'&&open){setOpen(false);toggle.focus({preventScroll:true});}
  });
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));

  // close the menu if the viewport grows past the mobile breakpoint
  const wide=matchMedia('(min-width:901px)');
  wide.addEventListener('change',e=>{if(e.matches&&open)setOpen(false);});

  // condense on scroll
  let ticking=false;
  const onScroll=()=>{
    if(ticking)return;
    ticking=true;
    requestAnimationFrame(()=>{
      header.toggleAttribute('data-scrolled',window.scrollY>24);
      ticking=false;
    });
  };
  addEventListener('scroll',onScroll,{passive:true});
  onScroll();

  // back to top
  const top=document.querySelector('.jpc-f-top');
  if(top)top.addEventListener('click',(e)=>{
    e.preventDefault();
    scrollTo({top:0,behavior:reduce.matches?'auto':'smooth'});
  });
})();
</script>
"""


def main():
    pages = sorted(glob.glob("*.html"))
    for p in pages:
        h = open(p, encoding="utf-8").read()
        root = re.search(r'id="(jp-[a-z-]+review|jp-review)"', h)
        if not root:
            print("!! no root id:", p); continue
        root_sel = "#" + root.group(1)

        # menu id: reuse the page's existing one so any stale aria-controls
        # elsewhere in the document still resolves
        old_menu = re.search(r'<nav[^>]*id="([^"]*menu)"', h)
        menu_id = old_menu.group(1) if old_menu else "jp-menu"

        # 1. strip the review toolbar
        h, n_tb = re.subn(r'<div class="review-tools".*?</div>\s*</div>', '', h, flags=re.S)
        if not n_tb:
            h, n_tb = re.subn(r'<div class="review-tools".*?</div>', '', h, flags=re.S)

        # 1b. strip leftover review annotations and the duplicate skip link
        h = re.sub(r'<p class="review-note">.*?</p>\s*', '', h, flags=re.S)
        h = re.sub(r'<a class="skip-link"[^>]*>.*?</a>\s*', '', h, flags=re.S)

        # 2. drop the old mobile nav (the new header carries its own)
        h = re.sub(r'<nav[^>]*class="[^"]*mobile-nav[^"]*"[^>]*>.*?</nav>', '', h, flags=re.S)

        # 3. replace header and footer
        h, n_h = re.subn(r'<header[^>]*>.*?</header>', lambda m: header_html(p, menu_id), h, count=1, flags=re.S)
        h, n_f = re.subn(r'<footer[^>]*>.*?</footer>', lambda m: footer_html(), h, count=1, flags=re.S)

        # 4. main landmark for the skip link
        if not re.search(r'<main[^>]*id=', h):
            h = re.sub(r'<main', '<main id="jp-main"', h, count=1)

        # 5. inject chrome CSS + JS last
        h = h.replace("</body></html>",
                      CSS.replace("__R__", root_sel) + JS + "</body></html>")
        if "jpc-header" not in h:
            print("!! header not injected:", p)

        open(p, "w", encoding="utf-8").write(h)
        print(f"{p:36s} root={root_sel:22s} menu={menu_id:16s} toolbar={n_tb} header={n_h} footer={n_f}")


if __name__ == "__main__":
    main()
