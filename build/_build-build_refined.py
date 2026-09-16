#!/usr/bin/env python3
"""Refinement pass 2 — imagery, frames and motion.

Takes the approved JunglePots review package and produces a refined build:
  * catalogue product shots become real alpha cutouts on the paper surface
    (the previous mix-blend-mode: multiply hack is removed)
  * material close-ups are re-cropped so no studio white enters the frame
  * the dimension drawing sits in ink on paper instead of a white box
  * motion becomes a deliberate layer: hero line reveal, staggered plates,
    slow image response -- all progressive enhancement

No copy, measurement, finish code or product claim is changed.
"""
import os, re, shutil, json, sys

SRC = "."
BUILD = "build"

ISOLATED = ["big-ben-tower", "tower-bridge", "siena", "dawn", "riverside-flow",
            "riverside-rise", "riverside-base", "grand-wall", "siena-kubo",
            "pixie", "cube-shelf", "garden"]

PAGES = ["junglepots-homepage.html", "junglepots-collections.html",
         "junglepots-production-quality.html", "junglepots-big-ben-tower.html"]

ROOT_ID = {"junglepots-homepage.html": "jp-review",
           "junglepots-collections.html": "jp-index-review",
           "junglepots-production-quality.html": "jp-production-review",
           "junglepots-big-ben-tower.html": "jp-detail-review"}

PLATE = "#edebe4"
PLATE_HOVER = "#e5e3da"


def sub(text, old, new, label, required=True):
    if old not in text:
        if required:
            print("  !! MISSING:", label)
        return text
    n = text.count(old)
    print(f"  ok  {label}  x{n}")
    return text.replace(old, new)


# ----------------------------------------------------------------- assets
def assets():
    if os.path.exists(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)
    for d in ["index-assets", "collection-assets", "production-assets",
              "homepage-assets"]:
        shutil.copytree(d, os.path.join(BUILD, d))
    for f in os.listdir(SRC):
        if f.endswith((".html", ".json", ".md", ".pdf")) and not f.startswith("_"):
            shutil.copy(f, BUILD)

    keep = os.path.join(BUILD, "_source-assets")
    os.makedirs(keep, exist_ok=True)

    # 1. isolated product plates
    for name in ISOLATED:
        src_jpg = os.path.join(BUILD, "index-assets", name + ".jpg")
        shutil.move(src_jpg, os.path.join(keep, name + ".jpg"))
        shutil.copy(os.path.join("index-assets-cut", name + ".png"),
                    os.path.join(BUILD, "index-assets", name + ".png"))

    # 2. construction close-ups: the studio sweep is cut away rather than
    #    cropped out, so the whole photograph can be shown on the page colour
    for cut, dst in [("big-ben-rim.png", "collection-assets/big-ben-rim"),
                     ("big-ben-feet.png", "collection-assets/big-ben-feet"),
                     ("rim.png", "production-assets/rim"),
                     ("feet.png", "production-assets/feet"),
                     ("joint.png", "production-assets/joint")]:
        old = os.path.join(BUILD, dst + ".jpg")
        if os.path.exists(old):
            shutil.move(old, os.path.join(keep, "orig-" + os.path.basename(dst)
                                          + ".jpg"))
        shutil.copy(os.path.join("detail-cut", cut),
                    os.path.join(BUILD, dst + ".png"))

    # 2b. detail-page hero product view, as a 4:5 plate
    shutil.move(os.path.join(BUILD, "collection-assets", "big-ben-isolated.jpg"),
                os.path.join(keep, "big-ben-isolated.jpg"))
    shutil.copy("hero-cut/big-ben-isolated.png",
                os.path.join(BUILD, "collection-assets", "big-ben-isolated.png"))

    # 3. dimension drawing: line art freed from its white box
    shutil.copy("collection-assets/big-ben-abc.png",
                os.path.join(keep, "big-ben-abc.png"))
    shutil.copy("drawing-cut/big-ben-abc.png",
                os.path.join(BUILD, "collection-assets", "big-ben-abc.png"))
    print("assets staged")


# ------------------------------------------------------------------ motion
MOTION = """<style>
/* Motion layer. Every initial state is applied only after JS confirms it can
   finish the job, so content is fully visible without scripting. */
#__ROOT__[data-motion="on"] .m-hold{opacity:0}
#__ROOT__[data-motion="on"] .m-rise{opacity:0;transform:translateY(26px)}
#__ROOT__[data-motion="on"] .m-word{display:block;overflow:hidden}
#__ROOT__[data-motion="on"] .m-word>span{display:block;transform:translateY(104%)}
@media(prefers-reduced-motion:no-preference){
  #__ROOT__ .text-link span{transition:transform 380ms cubic-bezier(.16,.84,.44,1)}
  #__ROOT__ .text-link{transition:opacity 380ms ease}
  #__ROOT__ .text-link:hover{opacity:.62}
  #__ROOT__ .text-link:hover span{transform:translate(4px,-3px)}
  #__ROOT__ .collection-image,#__ROOT__ .collection-media,#__ROOT__ figure{
    transition:background-color 700ms cubic-bezier(.16,.84,.44,1)}
  #__ROOT__ .collection-image img,#__ROOT__ .collection-media img,
  #__ROOT__ .hero-image img,#__ROOT__ .production figure img{
    transition:transform 900ms cubic-bezier(.16,.84,.44,1),
               filter 900ms cubic-bezier(.16,.84,.44,1);will-change:transform}
  #__ROOT__ a:hover .collection-image img,
  #__ROOT__ .collection-card:hover .collection-image img,
  #__ROOT__ .collection-card:hover .collection-media img,
  #__ROOT__ a:hover>img,#__ROOT__ figure:hover>img{transform:scale(1.028)}
  #__ROOT__ .collection-card:hover .collection-image{background:__HOVER__}
  #__ROOT__ .item-number{transition:transform 520ms cubic-bezier(.16,.84,.44,1),
               opacity 520ms ease}
  #__ROOT__ .collection-card:hover .item-number{transform:translateY(-2px);opacity:.55}
  #__ROOT__ summary::after{transition:transform 340ms cubic-bezier(.16,.84,.44,1)}
  #__ROOT__ details[open] summary::after{transform:rotate(180deg)}
}
</style>
<script>
(()=>{
const root=document.getElementById('__ROOT__');
if(!root)return;
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
if(!('animate' in Element.prototype)||!('IntersectionObserver' in window))return;

const EASE='cubic-bezier(.16,.84,.44,1)';
const clear=()=>root.removeAttribute('data-motion');
// hard safety net: whatever happens, nothing stays hidden
const failsafe=setTimeout(clear,2600);

try{
  root.dataset.motion='on';

  /* 1. Hero title, revealed a line at a time from behind its own baseline. */
  const title=root.querySelector('.hero h1,.hero-title,h1');
  if(title&&title.innerHTML.includes('<br')){
    const lines=title.innerHTML.split(/<br\\s*\\/?>/i);
    title.innerHTML=lines.map(l=>'<span class="m-word"><span>'+l+'</span></span>').join('');
  }else if(title){
    title.innerHTML='<span class="m-word"><span>'+title.innerHTML+'</span></span>';
  }
  const words=root.querySelectorAll('.m-word>span');
  words.forEach((w,i)=>w.animate(
    [{transform:'translateY(104%)'},{transform:'translateY(0)'}],
    {duration:1150,delay:90+i*110,easing:EASE,fill:'both'}));

  /* 2. Everything above the fold that sits beside the title. */
  const intro=root.querySelectorAll(
    '.hero .index-label,.hero-aside>*,.hero-foot,.intro-aside>*,.header');
  intro.forEach((el,i)=>{
    el.classList.add('m-hold');
    el.animate([{opacity:0,transform:'translateY(14px)'},
                {opacity:1,transform:'none'}],
      {duration:820,delay:260+i*90,easing:EASE,fill:'both'});
  });

  /* 3. Hero photograph settles rather than appears. */
  const heroImg=root.querySelector('.hero-image img,.hero-visual img,.hero-img');
  if(heroImg)heroImg.animate(
    [{transform:'scale(1.055)',opacity:.55},{transform:'scale(1)',opacity:1}],
    {duration:1700,easing:'cubic-bezier(.22,.68,.28,1)',fill:'both'});

  /* 4. Sections and catalogue plates enter on approach, staggered by row
        so a grid resolves left to right instead of flashing in as a block. */
  const seen=new WeakSet();
  let batch=[],timer=null;
  const flush=()=>{
   try{
    batch.sort((a,b)=>{
      const ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();
      return (ra.top-rb.top)||(ra.left-rb.left);
    });
    batch.forEach((el,i)=>el.animate(
      [{opacity:0,transform:'translateY(26px)'},{opacity:1,transform:'none'}],
      {duration:selDur(el),delay:Math.min(i,8)*70,easing:EASE,fill:'both'}));
   }catch(e){batch.forEach(el=>el.classList.remove('m-rise'))}
   batch=[];
  };
  const selDur=el=>el.matches('.collection-card')?760:880;
  const io=new IntersectionObserver(es=>{
    es.forEach(e=>{
      if(!e.isIntersecting||seen.has(e.target))return;
      seen.add(e.target);
      e.target.classList.add('m-rise');
      batch.push(e.target);
      io.unobserve(e.target);
    });
    clearTimeout(timer);timer=setTimeout(flush,40);
  },{threshold:.06,rootMargin:'0px 0px -6% 0px'});

  root.querySelectorAll(
    'main>section:not(.hero),.collection-card,.custom-grid>*,.production-grid>*'
  ).forEach(el=>io.observe(el));

  /* 5. Swapping a product or construction view is a dissolve, not a cut. */
  root.querySelectorAll('[data-view],[data-detail]').forEach(b=>
    b.addEventListener('click',()=>{
      const p=root.querySelector('.hero-img,.construction-photo');
      if(p)p.animate([{opacity:.25,transform:'scale(1.012)'},
                      {opacity:1,transform:'none'}],
        {duration:520,easing:EASE});
    }));

  /* 6. Filtering re-deals the grid instead of snapping it. */
  root.querySelectorAll('[data-filter]').forEach(b=>
    b.addEventListener('click',()=>{
      const vis=[...root.querySelectorAll('.collection-card')]
        .filter(c=>!c.hidden);
      vis.forEach((c,i)=>c.animate(
        [{opacity:0,transform:'translateY(14px)'},{opacity:1,transform:'none'}],
        {duration:560,delay:Math.min(i,9)*45,easing:EASE}));
    }));

  clearTimeout(failsafe);
}catch(e){clearTimeout(failsafe);clear()}
})();
</script>
</body></html>"""


def motion_for(page):
    return (MOTION.replace("__ROOT__", ROOT_ID[page])
                  .replace("__HOVER__", PLATE_HOVER))


# ------------------------------------------------------------------- pages
def collections(h):
    print(" collections page")
    h = sub(h, "#jp-index-review{--paper:#f3f1eb;",
            f"#jp-index-review{{--plate:{PLATE};--plate-hover:{PLATE_HOVER};"
            "--paper:#f3f1eb;", "tokens")
    # frames: drop the white box and the blend hack
    h = sub(h,
            "#jp-index-review .collection-image{position:relative;"
            "background:#e8e6df;overflow:hidden}",
            "#jp-index-review .collection-image{position:relative;"
            "background:var(--plate);overflow:hidden}", "frame background")
    h = sub(h, "#jp-index-review .collection-image.isolated{background:#fff}",
            "#jp-index-review .collection-image.isolated{background:var(--plate)}",
            "isolated background")
    h = sub(h,
            "#jp-index-review .collection-image.isolated img{object-fit:contain;"
            "padding:28px}",
            "#jp-index-review .collection-image.isolated img{object-fit:contain;"
            "padding:0}", "isolated padding")
    h = sub(h,
            "#jp-index-review .collection-image.isolated img{mix-blend-mode:"
            "multiply;padding:32px;object-fit:contain}",
            "#jp-index-review .collection-image.isolated img{padding:0;"
            "object-fit:contain}", "blend hack removed")
    # cutouts
    for name in ISOLATED:
        h = sub(h, f'src="index-assets/{name}.jpg"',
                f'src="index-assets/{name}.png"', f"src {name}")
    h = h.replace('width="900" height="936"', 'width="1320" height="990"')
    # the plate already carries its own breathing room, so the grid can tighten
    h = sub(h, ".collection-grid{display:grid;grid-template-columns:repeat(3,"
               "minmax(0,1fr));gap:42px 28px;align-items:start}",
            ".collection-grid{display:grid;grid-template-columns:repeat(3,"
            "minmax(0,1fr));gap:52px 30px;align-items:start}", "grid gap")
    return h


def production(h):
    print(" production page")
    h = sub(h, "#jp-production-review{--paper:#f3f1eb;",
            f"#jp-production-review{{--plate:{PLATE};--paper:#f3f1eb;", "tokens")
    h = sub(h, ".construction-photo{aspect-ratio:3/2;object-fit:contain;"
               "background:#fff}",
            ".construction-photo{aspect-ratio:3/2;object-fit:contain;"
            "background:var(--paper);padding:2%}", "construction frame")
    h = sub(h, ".hero-detail img{aspect-ratio:1/1;object-fit:cover}",
            ".hero-detail img{aspect-ratio:1/1;object-fit:contain;"
            "background:var(--paper)}", "production hero frame")
    for n in ("rim", "feet", "joint"):
        h = sub(h, f"production-assets/{n}.jpg", f"production-assets/{n}.png",
                f"src {n}")
    # dead rules carried over from the index; cleaned so the white box and the
    # multiply hack do not reach the React implementation
    h = sub(h, "#jp-production-review .collection-image.isolated{background:#fff}",
            "#jp-production-review .collection-image.isolated{"
            "background:var(--plate)}", "dead isolated white", required=False)
    h = sub(h, "#jp-production-review .collection-image.isolated img{"
               "mix-blend-mode:multiply;padding:32px;object-fit:contain}",
            "#jp-production-review .collection-image.isolated img{padding:0;"
            "object-fit:contain}", "dead blend hack", required=False)
    return h


def detail(h):
    print(" detail page")
    h = sub(h, "#jp-detail-review{--paper:#f3f1eb;",
            f"#jp-detail-review{{--plate:{PLATE};--paper:#f3f1eb;", "tokens")
    h = sub(h, ".drawing{background:#fff;padding:40px;display:flex;"
               "align-items:center;flex-direction:column;justify-content:center}",
            ".drawing{background:var(--plate);padding:40px;display:flex;"
            "align-items:center;flex-direction:column;justify-content:center}",
            "drawing plate")
    # rim and feet are full-bleed material crops with no studio background,
    # so they fill the frame instead of sitting letterboxed on white
    h = sub(h, ".hero-img.detail-view{object-fit:contain;background:#fff;"
               "padding:20px}",
            ".hero-img.detail-view{object-fit:contain;"
            "background:var(--paper);padding:4%}", "detail view frame")
    for n in ("big-ben-rim", "big-ben-feet"):
        h = sub(h, f"'collection-assets/{n}.jpg'", f"'collection-assets/{n}.png'",
                f"src {n}")
    h = sub(h, ".hero-img.isolated{object-fit:contain;background:#fff;padding:36px}",
            ".hero-img.isolated{object-fit:contain;background:var(--paper);"
            "padding:0}", "hero plate")
    h = sub(h, ".hero-visual:has(.isolated) figcaption{color:var(--ink);"
               "background:#f3f1eb;text-shadow:none}",
            ".hero-visual:has(.isolated) figcaption{color:var(--ink);"
            "background:var(--paper);text-shadow:none}", "isolated caption")
    h = sub(h, "'collection-assets/big-ben-isolated.jpg'",
            "'collection-assets/big-ben-isolated.png'", "hero product src")
    return h


def homepage(h):
    print(" homepage")
    h = sub(h, "#jp-site{", f"#jp-site{{--jp-plate:{PLATE};", "tokens",
            required=False)
    h = sub(h, "collection-assets/big-ben-rim.jpg",
            "collection-assets/big-ben-rim.png", "rim src")
    h = sub(h, "#jp-site .production figure img{aspect-ratio:1.18;height:auto}",
            "#jp-site .production figure img{aspect-ratio:1.18;height:auto;"
            "object-fit:contain;background:var(--jp-paper)}", "detail spread frame")
    return h


TRANSFORM = {"junglepots-collections.html": collections,
             "junglepots-production-quality.html": production,
             "junglepots-big-ben-tower.html": detail,
             "junglepots-homepage.html": homepage}


def pages():
    for p in PAGES:
        path = os.path.join(BUILD, p)
        h = open(path, encoding="utf-8").read()
        h = TRANSFORM[p](h)
        # replace the previous motion tail wholesale
        j = h.rfind("<style>\n@media(prefers-reduced-motion:no-preference){")
        if j < 0:
            print("  !! motion tail not found in", p)
        else:
            h = h[:j] + motion_for(p)
            print("  ok  motion layer replaced")
        open(path, "w", encoding="utf-8").write(h)


if __name__ == "__main__":
    assets()
    pages()
    print("\nbuild complete ->", BUILD)
