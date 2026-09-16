#!/usr/bin/env python3
"""Homepage variant.

Two changes to the approved homepage:

  * the hero photograph is a real exterior terrace project, keeping the
    approved full-width hero band. The hero promises interior, exterior and
    landscape projects, and every other photograph on the page is an interior;
  * the two Sculptural collections appear as traced silhouettes inside
    section 01, under the statement "Considered as part of the architecture" --
    the drawing is the argument that statement is making.

The silhouettes are traced from the alpha channel of the catalogue's own
isolated product photographs, so each outline is the real object's, not a
modelled approximation.

Project photography comes from the client's own Jungle Flora site, where the
source filenames identify the products. No client project is named on the page.
"""
import json, os, re, shutil

BUILD = "build"
OUT = "junglepots-homepage-hero.html"

S = json.load(open("silhouettes.json"))

# Catalogue heights in cm, used only to size the two forms relative to each
# other. Both are catalogued at 99 cm, so they draw at the same height --
# which is the point. No dimension is printed, so the unresolved 99/90 cm
# question for Big Ben Tower is not surfaced as a claim.
# Catalogue order: Big Ben Tower is 01 and Tower Bridge 02 on the collection
# index, and the selected-collection cards below run the same way.
STRIP = [
    ("big-ben-tower", "Big Ben Tower", "Stepped square tower",       99.0),
    ("tower-bridge",  "Tower Bridge",  "Square tower / arched base", 99.0),
]
TALLEST = max(cm for *_, cm in STRIP)


def svg(slug, cm):
    v = S[slug]
    w, h = v["w"], v["h"]
    return (
        f'<svg class="elev" viewBox="0 0 {w:.0f} {h:.0f}" '
        f'style="--rel:{cm / TALLEST:.4f};--ratio:{w / h:.4f}" '
        f'fill="none" aria-hidden="true" focusable="false">'
        f'<path d="{v["paths"][0]["d"]}" vector-effect="non-scaling-stroke"/>'
        f'</svg>')


FIG = """              <figure class="elev-item">
                {svg}
                <figcaption><span class="elev-name">{name}</span><span class="elev-form">{form}</span></figcaption>
              </figure>"""


HERO = """        <section class="hero" aria-labelledby="hero-title">
          <div class="hero-intro wrap">
            <div><p class="index-label">JUNGLEPOTS / EUROPE</p><h1 id="hero-title">Architectural<br>planters.</h1></div>
            <div class="hero-aside"><p>Planters for interior,<br>exterior and landscape projects.</p><a class="text-link" href="#jp-collections">Explore collections <span aria-hidden="true">&#8600;</span></a></div>
          </div>
          <figure class="hero-image">
            <img src="hero-assets/terrace-project.jpg" alt="Dark cylindrical and rectangular planters holding grasses and shrubs on a roof terrace, behind a glass balustrade with a city skyline beyond" width="1920" height="1280" fetchpriority="high">
            <figcaption><span>JUNGLEPOTS / IN CONTEXT</span><span>EXTERIOR / TERRACE PROJECT</span></figcaption>
          </figure>
          <div class="hero-foot wrap"><span>FORM / MATERIAL / SPECIFICATION</span><span>Explore below &#8595;</span></div>
        </section>"""


ABOUT = """        <section id="jp-about" class="intro wrap section-space" aria-labelledby="intro-title">
          <div class="intro-top">
            <p class="index-label"><span>01 /</span> THE APPROACH</p>
            <span class="index-label intro-note">SILHOUETTES / TRACED FROM CATALOGUE PHOTOGRAPHY</span>
          </div>
          <div class="intro-grid">
            <div class="intro-text">
              <h2 id="intro-title">Considered as part<br>of the architecture.</h2>
              <p class="intro-copy">JunglePots brings architectural planters to professional projects. Explore collections through their form, proportions and technical information.</p>
              <a href="#jp-production" class="text-link">About JunglePots <span aria-hidden="true">&#8599;</span></a>
            </div>
            <div class="approach-forms">
              <div class="elev-row">
__FIGURES__
              </div>
            </div>
          </div>
        </section>"""


CSS = """
/* ---- Hero: the approved full-width band, holding an exterior project ---- */
#jp-site .hero-image img{object-position:50% 64%}

/* ---- Section 01: the forms drawn on the left, the statement on the right.
   A departure from the guide's "index label left, statement right" intro:
   the drawing is the argument the statement is making, so the two belong
   side by side in one section rather than stacked as two. */
#jp-site .intro{display:block}
#jp-site .intro-top{
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap:24px;
  border-bottom:1px solid var(--jp-line);
  padding-bottom:15px;
}
#jp-site .intro .index-label{padding-top:0}
#jp-site .intro-note{color:var(--jp-muted)}
#jp-site .intro-grid{
  display:grid;
  grid-template-columns:1fr 1.1fr;
  gap:7%;
  align-items:center;
  padding-top:clamp(44px,5.5cqw,84px);
}
#jp-site .approach-forms{grid-column:1;grid-row:1;min-width:0}
#jp-site .intro-text{grid-column:2;grid-row:1;min-width:0}
#jp-site .intro-text h2{margin-top:0}
#jp-site .elev-row{
  --elev-h:clamp(220px,24cqw,360px);
  display:flex;
  align-items:flex-end;
  justify-content:center;
  gap:clamp(36px,5cqw,72px);
  min-width:0;
}
#jp-site .elev-item{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:18px;
  min-width:0;
}
#jp-site .elev{
  display:block;
  height:calc(var(--elev-h) * var(--rel));
  width:calc(var(--elev-h) * var(--rel) * var(--ratio));
  max-width:100%;
  overflow:visible;
}
#jp-site .elev path{
  stroke:var(--jp-ink);
  stroke-width:1.4;
  stroke-linejoin:round;
  fill:none;
}
#jp-site .elev-item figcaption{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:5px;
  text-align:center;
}
#jp-site .elev-name{font-size:15px;letter-spacing:-.02em;white-space:nowrap}
#jp-site .elev-form{
  font:10px/1.5 'IBM Plex Mono',monospace;
  letter-spacing:.05em;
  color:var(--jp-muted);
  white-space:nowrap;
}

@container jp (max-width:900px){
  /* stack: the statement reads first, the drawing follows as its evidence */
  #jp-site .intro-grid{grid-template-columns:1fr;gap:0;padding-top:36px}
  #jp-site .intro-text{grid-column:1;grid-row:1}
  #jp-site .approach-forms{grid-column:1;grid-row:2;padding-top:48px}
  #jp-site .elev-row{--elev-h:clamp(180px,32cqw,260px);justify-content:flex-start}
  #jp-site .intro-note{display:none}
}
@container jp (max-width:600px){
  #jp-site .elev-row{--elev-h:clamp(155px,42cqw,210px);gap:34px}
  #jp-site .elev-form{display:none}
}
"""


MOTION = """
<style>
#jp-review[data-forms="on"] .elev path{stroke-dashoffset:var(--len)}
#jp-review[data-forms="on"] .elev-item figcaption{opacity:0}
</style>
<script>
/* The two forms draw themselves once, when section 01 is first scrolled to.
   Progressive enhancement only -- with no JS, reduced motion, or no SVG
   geometry API, they render complete and static. */
(()=>{
  const root=document.getElementById('jp-review');
  if(!root)return;
  const row=root.querySelector('.approach-forms');
  if(!row)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  if(!('animate' in Element.prototype)||!('IntersectionObserver' in window))return;
  const paths=[...row.querySelectorAll('.elev path')];
  if(!paths.length||typeof paths[0].getTotalLength!=='function')return;

  const off=()=>root.removeAttribute('data-forms');
  const failsafe=setTimeout(off,4200);
  try{
    root.dataset.forms='on';
    const io=new IntersectionObserver(es=>{
      es.forEach(e=>{
        if(!e.isIntersecting)return;
        io.disconnect();
        try{
          paths.forEach((p,i)=>{
            const len=Math.ceil(p.getTotalLength());
            p.style.setProperty('--len',len);
            p.style.strokeDasharray=len;
            p.animate([{strokeDashoffset:len},{strokeDashoffset:0}],
              {duration:1500,delay:i*260,easing:'cubic-bezier(.62,.02,.34,1)',fill:'both'});
          });
          row.querySelectorAll('.elev-item figcaption').forEach((c,i)=>
            c.animate([{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'none'}],
              {duration:700,delay:1400+i*260,easing:'cubic-bezier(.16,.84,.44,1)',fill:'both'}));
        }catch(err){off()}
        clearTimeout(failsafe);
      });
    },{threshold:.25});
    io.observe(row);
  }catch(e){clearTimeout(failsafe);off()}
})();
</script>
"""


def main():
    src = open(os.path.join(BUILD, "junglepots-homepage.html"),
               encoding="utf-8").read()

    # ---- hero: approved full-width band, exterior project photograph
    a = src.index('<section class="hero"')
    b = src.index("</section>", a) + len("</section>")
    out = src[:a] + HERO + src[b:]

    # ---- section 01: drawings left, statement right, one section
    figures = "\n".join(
        FIG.format(svg=svg(slug, cm), name=name, form=form)
        for slug, name, form, cm in STRIP)
    about = ABOUT.replace("__FIGURES__", figures)

    m = re.search(r'<section id="jp-about".*?</section>', out, re.S)
    if not m:
        raise SystemExit("!! intro section not found")
    out = out[:m.start()] + about + out[m.end():]

    # ---- selected collections: the two Sculptural forms, matching the
    #      drawings in section 01, both with better project photography
    out = out.replace(
        '<img src="collection-assets/big-ben-project-entry.jpg" '
        'alt="Big Ben Tower planters with stepped bases in a glazed interior '
        'entrance" width="1024" height="1536" loading="lazy">',
        '<img src="hero-assets/big-ben-project-hero.jpg" '
        'alt="Big Ben Tower planters lining a glazed office corridor" '
        'width="1000" height="1500" loading="lazy">')

    out = out.replace(
        'data-collection="Riverside Base" aria-label="Preview Riverside Base '
        'collection"><img src="homepage-assets/riverside-project-1.jpg" '
        'alt="Riverside Base planter in the CYBERCITY lounge" width="1024" '
        'height="1280" loading="lazy">',
        'data-collection="Tower Bridge" aria-label="Preview Tower Bridge '
        'collection"><img src="hero-assets/tower-bridge-project-hero.jpg" '
        'alt="A Tower Bridge planter with its arched base, planted and '
        'installed against a fluted panel wall in a lounge interior" '
        'width="1100" height="1650" loading="lazy">')

    out = out.replace(
        '<h3>Riverside Base</h3><p>Cylindrical form / Three catalogued sizes</p>',
        '<h3>Tower Bridge</h3><p>Arched square form / One catalogued size</p>')

    # every remaining reference on this page is to the same card
    out = out.replace("Riverside Base", "Tower Bridge")
    out = out.replace('data-collection="Tower Bridge">Riverside \u2197<',
                      'data-collection="Tower Bridge">Tower Bridge \u2197<')

    j = out.rfind("<style>\n/* Motion layer")
    if j < 0:
        j = out.rfind("<style>")
    out = out[:j] + "<style>" + CSS + "</style>\n" + out[j:]
    out = out.replace("</body></html>", MOTION + "</body></html>")

    open(os.path.join(BUILD, OUT), "w", encoding="utf-8").write(out)

    dst = os.path.join(BUILD, "hero-assets")
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir("hero-assets"):
        shutil.copy(os.path.join("hero-assets", f), dst)
    print("wrote", OUT, "+", sorted(os.listdir(dst)))


if __name__ == "__main__":
    main()
