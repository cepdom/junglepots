#!/usr/bin/env python3
"""Put the traced line drawing into the Big Ben Tower specification panel,
replacing the flat catalogue photograph.

The dimension letters keep the catalogue's own roles and the values stay in
the schedule table beside the drawing. The caption changes from "Catalogue
drawing" to "Traced from catalogue photography" because that is now what it is.
"""
import os

BUILD = "build"
PAGE = "junglepots-big-ben-tower.html"

OLD_FIG = ('<figure class="drawing"><img src="collection-assets/big-ben-abc.png"'
           ' alt="Original Big Ben Tower dimension illustration: A across the'
           ' front, B depth, C overall height" width="435" height="643">'
           '<figcaption>Catalogue drawing / not to scale</figcaption></figure>')

CSS = """
/* ---- Specification drawing ------------------------------------------- */
#jp-detail-review .spec-drawing{display:block;height:430px;width:auto;max-width:300px;overflow:visible}
#jp-detail-review .drawing{background:transparent;padding:8px 0 0}
#jp-detail-review .spec-drawing .dwg-out{stroke:var(--ink);stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;fill:none}
#jp-detail-review .spec-drawing .dim-letter{font:400 27px Manrope,Arial,sans-serif;fill:var(--ink)}
#jp-detail-review .spec-drawing .dims line{stroke:var(--ink)}
@container detail (max-width:1000px){#jp-detail-review .spec-drawing{height:360px;max-width:255px}}
@container detail (max-width:760px){#jp-detail-review .spec-drawing{height:345px}}
@container detail (max-width:520px){#jp-detail-review .spec-drawing{height:280px}}
#jp-detail-review .drawing figcaption{padding-top:18px}
"""

MOTION = """
<script>
/* The specification drawing draws itself once, when it is first scrolled to --
   the same gesture as the homepage hero. Progressive enhancement only. */
(()=>{
  const root=document.getElementById('jp-detail-review');
  if(!root)return;
  const svg=root.querySelector('.spec-drawing');
  if(!svg)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  if(!('animate' in Element.prototype)||!('IntersectionObserver' in window))return;
  const shapes=[...svg.querySelectorAll('.dwg-out')];
  const dims=[...svg.querySelectorAll('.dims line,.dim-letter')];
  if(!shapes.length||typeof shapes[0].getTotalLength!=='function')return;

  const reset=()=>{
    shapes.forEach(p=>{p.style.strokeDasharray='';p.style.strokeDashoffset='';});
    dims.forEach(d=>{d.style.opacity='';});
  };
  const io=new IntersectionObserver(es=>{
    es.forEach(e=>{
      if(!e.isIntersecting)return;
      io.disconnect();
      const failsafe=setTimeout(reset,3400);
      try{
        shapes.forEach((p,i)=>{
          const len=Math.ceil(p.getTotalLength());
          p.style.strokeDasharray=len;
          p.animate([{strokeDashoffset:len},{strokeDashoffset:0}],
            {duration:1400,delay:i*140,easing:'cubic-bezier(.62,.02,.34,1)',fill:'both'});
        });
        dims.forEach(d=>d.animate([{opacity:0},{opacity:1}],
          {duration:620,delay:1150,easing:'ease-out',fill:'both'}));
        clearTimeout(failsafe);
      }catch(err){clearTimeout(failsafe);reset()}
    });
  },{threshold:.3});
  io.observe(svg);
})();
</script>
"""


def main():
    path = os.path.join(BUILD, PAGE)
    h = open(path, encoding="utf-8").read()
    svg = open("big-ben-drawing.svg", encoding="utf-8").read()

    new_fig = ('<figure class="drawing">' + svg +
               "<figcaption>Traced from catalogue photography / not to scale"
               "</figcaption></figure>")

    if OLD_FIG in h:
        h = h.replace(OLD_FIG, new_fig)
        print("ok  drawing figure replaced")
    else:
        import re
        m = re.search(r'<figure class="drawing">.*?</figure>', h, re.S)
        if not m:
            raise SystemExit("!! drawing figure not found")
        h = h[:m.start()] + new_fig + h[m.end():]
        print("ok  drawing figure replaced (regex)")

    # the old rules targeted <img>; let them cover the inline drawing too
    n = h.count(".drawing img{")
    h = h.replace(".drawing img{", ".drawing :is(img,svg):not(.spec-drawing){")
    print(f"ok  neutralised {n} legacy .drawing img rules")

    j = h.rfind("<style>")
    h = h[:j] + "<style>" + CSS + "</style>\n" + h[j:]
    h = h.replace("</body></html>", MOTION + "</body></html>")

    open(path, "w", encoding="utf-8").write(h)
    print("wrote", path)


if __name__ == "__main__":
    main()
