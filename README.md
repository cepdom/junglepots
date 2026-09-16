# JunglePots.eu — static site

Twenty pages, thirteen collections. **Plain HTML with no build step** — no
npm, no bundler, no framework, no dependencies. Every page is self-contained:
CSS and JS are inline, images are local files, and the only external request is
the Google Fonts stylesheet.

That means it can be hosted by anything that serves files.

```
index.html                  the home page (a copy of junglepots-homepage-hero.html)
junglepots-*.html           the 20 pages
collection-assets/          per-collection photography and cutouts
card-assets/                social share cards for the 3 pages with no photograph
hero-assets/ homepage-assets/ index-assets/
production-assets/ refinement-assets/ related-assets/
.nojekyll                   stops GitHub Pages' Jekyll from dropping files
docs/                       handoffs, provenance, catalogue analysis
build/                      the Python that generated the pages and drawings
```

---

## Deploy: GitHub Pages

The whole thing in one go, from inside this folder:

```bash
git init
git add .
git commit -m "JunglePots site"
git branch -M main
git remote add origin https://github.com/YOUR-USER/junglepots-site.git
git push -u origin main
```

Then on GitHub: **Settings → Pages → Source: Deploy from a branch →
`main` / `(root)` → Save.** It is live at
`https://YOUR-USER.github.io/junglepots-site/` in a minute or two.

For a custom domain, add `junglepots.eu` under Settings → Pages → Custom
domain, and point a CNAME at `YOUR-USER.github.io` with your registrar.

`.nojekyll` matters: without it GitHub Pages runs Jekyll, which silently
ignores any file or folder whose name starts with an underscore.

## Deploy: Netlify or Vercel (no git needed)

Drag this folder onto <https://app.netlify.com/drop>. It is live in seconds on
a random subdomain, and you can attach a custom domain after. Vercel's
equivalent is `vercel deploy` from inside the folder, or the same drag-and-drop
in their dashboard.

Either is a reasonable way to show the client something today without touching
git at all.

---

## One thing to change before a real launch

`og:image` on every page is a **relative** path. Several link-preview scrapers
(Slack, LinkedIn, iMessage) ignore relative image URLs, so share cards will
show text without a picture until they are absolute.

The fix is one line. In `build/_build-patch_meta.py`:

```python
BASE = "https://junglepots.eu"     # currently ""
```

Re-run it against the pages and every card image becomes absolute. Do it once
the real domain is known.

## Other things left open

Listed in full in `docs/JunglePots-bar-planter-handoff.md`, section 6. The
short version:

* **The specification disclosures ship as written.** Nine pages carry panels
  setting out where the catalogue's own figures do not reconcile. That was a
  deliberate choice and the evidence is in `docs/`. When the corrected figures
  arrive, those panels should be rewritten as ordinary specification notes
  rather than left as errata.
* **Six pages were built from low-resolution crops** before the full catalogue
  page renders were found — Big Ben Tower, Tower Bridge, Siena, Siena Kubo,
  Dawn and Grand Wall. Rebuilding them from the renders is the largest
  remaining quality gain.
* **Touch targets** in the footer and breadcrumb fall below the 44 px minimum.
* **`junglepots-big-ben-tower.html` carries ~17 KB of duplicated style blocks
  and scripts** — it is the oldest page and was never cleaned.

## The enquiry form

`junglepots-contact.html` posts to `/api/enquiries`, which does not exist on a
static host. With no server attached it says so plainly rather than failing
silently. `build/serve_enquiries.py` is a small local server that implements
that endpoint for testing the full flow; in production the form needs a real
backend, a form service (Netlify Forms, Formspree) or a `mailto:` fallback.

## Provenance

Every image is the client's own catalogue or Jungle Flora's own listings.
Nothing is AI-generated. `docs/JunglePots-collection-asset-provenance.json`
records the source page and the exact treatment for each file, and
`docs/JunglePots-*-handoff.md` records why each page is built the way it is.
