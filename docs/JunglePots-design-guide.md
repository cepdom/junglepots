# JunglePots — Homepage / Direction 01

Status: complete homepage design concept for review. The visual system is proposed, not yet locked. Collection Detail and the remaining pages are reserved for the next approved stage. This is a front-end design blueprint, not a deployed production website.

## Art direction

An architectural product catalogue with the rhythm of an editorial publication. The identity comes from tightly set Manrope typography, small monospaced index labels, rules that organise the page, offset collection photographs, and a mineral-olive specification section. A simple JunglePots wordmark ends in a full stop; a large version closes the page.

Photography supplies warmth and context. Text stays on opaque surfaces, except for small photographic captions. The opening identifies the product directly: **Architectural planters.** There are no prices, baskets, ratings, statistics, or decorative feature-card grids.

The relationship with Jungle Flora is the shared Jungle name, plant-led project context, and a restrained green family. Jungle Flora's bright green controls, botanical illustration, and service-marketing layouts are not carried over. See the existing [Jungle Flora website](https://jungleflora.lt/). [Jessicannes / Our Places](https://www.jessicannes.com/our-places) informed the editorial reference brief; no text, photographs or layouts were copied. The supplied Undomus product URL could not be retrieved, so its role here is limited to the product-presentation principles described in the brief.

## Exact homepage order

| Order | Component | Content and purpose | Desktop layout | Mobile behaviour |
|---|---|---|---|---|
| 1 | Header | Wordmark, five navigation items, quote link | 88px high, fine lower rule | 72px, wordmark and Menu; expanded navigation in normal document flow |
| 2 | Hero | Architectural planters; concise project context; Explore collections | Two-column title band, then full-width photograph | 42–60px title, supporting text and action, 450px image with deliberate right-focused crop |
| 3 | BrandIntroduction | Short professional positioning | Index label left; statement and paragraph on right | Label, statement, paragraph, link |
| 4 | SelectedCollections | Big Ben Tower and Riverside | Two columns in a 1.12:1 ratio; second image begins 164px lower | One collection per row; remove the desktop preface and offset |
| 5 | ProductionMaterialSpread | Surface detail and production information | Image reaches the left page edge; text occupies right column | Full-width image followed by text with standard gutters |
| 6 | SpecificationDesk | Catalogue and project support | Dark olive field; catalogue cover and copy left; project enquiry information right | Catalogue cover and text remain paired; project support follows below |
| 7 | RepresentativeIndex | Lithuania HQ and planned European representative slots | Statement left; expandable country rows right | Statement followed by full-width country rows |
| 8 | ProjectInquiryCTA | Request a quote | Large heading left; restrained arrow action right | Heading then action; no sticky obstruction |
| 9 | Footer | Navigation, catalogue, contact, social/legal slots | Four columns; large wordmark; legal row | Two columns, social row, proportional wordmark, stacked legal information |

Production and material detail are combined into one coherent spread. Catalogue and B2B support are paired as a specification desk. A country index replaces a homepage map because contacting the right person is the immediate task. A geographic map can still be developed for Contact after the direction is approved.

## Colour tokens

| Token | Value | Use |
|---|---|---|
| paper | `#F3F1EB` | Main page background |
| surface | `#E8E6DF` | Secondary neutral surface |
| ink | `#232822` | Headings, body and controls |
| muted | `#676B61` | Supporting copy and small labels |
| line | `#CCCFC4` | Neutral dividers |
| olive | `#3E4739` | Specification desk and small brand accents |
| on-olive | `#F3F1EB` | Primary text on dark olive |
| muted-on-olive | `#C7CEC1` | Index labels on dark olive |
| line-on-olive | `#697361` | Dark-section dividers |

Keep olive concentrated in the specification desk. Do not add separate accent colours for every section. Warm white is a fixed brand theme, not an operating-system light/dark choice.

## Typography

Primary: **Manrope**, weights 400, 500 and 600. Labels: **IBM Plex Mono**, weight 400. Fallbacks: Arial/sans-serif and monospace. Self-host approved font files in the production build; the concept loads Google Fonts.

| Role | Desktop size / line-height | Mobile size / line-height | Weight | Tracking |
|---|---|---|---|---|
| Display / hero | 86px / 1.02 maximum | 42–60px / 1.08 | 400 | -0.06em |
| Large closing title | 92px / 1.13 maximum | 54px / 1.13 | 400 | -0.06em |
| H1, future internal pages | Proposed 64px / 1.08 | Proposed 42px / 1.12 | 400 | -0.05em |
| H2 | 36–62px / 1.13 | 34–42px / 1.13 | 400 | -0.05em |
| H3 | 24–34px / 1.25 | 23–32px / 1.25 | 400 | -0.035em |
| Body large | 16px / 1.8 | 15–16px / 1.8 | 400 | normal |
| Body | 15px / 1.8 | 14–15px / 1.8 | 400 | normal |
| Links | 12–14px / 1.5 | 12–14px / 1.5 | 400 | normal |
| Index label | 11px / 1.5 | 10px / 1.5 | 400 | 0.06em |
| Wordmark | 30px / 1 | 28px / 1 | 600 | approx. -0.06em |

Tiny catalogue-cover lettering is decorative print-cover artwork, not essential interface copy. Product names, navigation and contact actions remain live, accessible text. Keep paragraphs under approximately 55 characters per line. Use tabular numbers in future technical tables.

## Grid, spacing and images

- Page shell: maximum 1600px; text/content container maximum 1440px.
- Gutters: 56px desktop; 40px below 1150px; 22px below 600px.
- Spacing scale: 4 / 8 / 12 / 16 / 20 / 24 / 28 / 32 / 40 / 48 / 56 / 64 / 72 / 88 / 112 / 164.
- Major section spacing: 112px desktop; 88px tablet; 72px mobile.
- Thin rules: 1px. Corners: 0px. No panel shadows.
- Intro: 1:2 grid, 48px gap. Collection spread: 1.12:1 grid, 7.8% gap. Contact area: 1:1 grid, 8% gap.
- Collection photos: 4:5 viewports on desktop and mobile. Offset the second desktop collection with a real preface block, not absolute positioning.
- Hero: full shell width; height `clamp(400px,43vw,650px)` in a viewport-based React implementation; 480px at tablet and 450px at mobile.
- Hero crop: desktop focal point at 50% / 85%; mobile at 90% / 50%. Store focal points per asset in the CMS. Preserve the actual product base and silhouette when replacing assets.
- Surface photo: approximately 1.18:1 desktop, 6:5 mobile.
- Preview uses container queries so the 390px review switch behaves correctly even inside a large browser. Ordinary media queries can reproduce the same rules in a full-width React site.

## Reusable component contracts

| Component | Data / props | Behaviour |
|---|---|---|
| Header | logo, navItems, quoteHref | Collapse navigation below 900px; reveal menu in document flow; Escape closes it |
| SectionLabel | index, label, secondaryLabel | Divider and aligned small typography; hide nonessential secondary label on mobile |
| TextLink | label, href, arrow | Thin underline, 44px action area, restrained arrow motion |
| CollectionCard | name, href, image, alt, focalPoint, index | Image and named link go to the same collection; no ecommerce badges |
| EditorialImageText | image, caption, label, title, body, link | Image/text grid that stacks in reading order |
| CatalogueCTA | title, language, fileUrl, verifiedFileSize, cover | Real download only when a file exists; never invent file size or edition |
| RepresentativeIndex | countryCode, countryName, role, name, email, telephone, status | Click/tap/keyboard expandable rows; details remain adjacent to selected country |
| ProjectInquiryCTA | title, href, selectedCollection | Carry the collection slug into the future inquiry page |
| Footer | navigation, contact, catalogue, socialUrls, legalUrls | No invented profile links; hide unapproved destinations in production |

## Interaction and accessibility

- Image hover: 1.00 to 1.02 over 450ms. Link arrow: 220ms, 2–3px movement.
- No parallax, entrance delay, scroll hijacking, or fixed WhatsApp bubble.
- Honour `prefers-reduced-motion` and preserve keyboard focus indicators.
- Menu state and country selection expose `aria-expanded`. Mobile menu supports Escape.
- Navigation, country rows and primary actions need usable touch targets. Maintain at least 44px for normal touch controls.
- Social/contact links must have meaningful accessible names. Use proper `tel:` and WhatsApp URLs; +370 600 20608 is the supplied contact.
- There are no form submissions, analytics or backend connections in this design concept.

## Prototype behaviour versus the production site

The homepage is complete as a visual concept. Navigation currently scrolls to the corresponding homepage section. Collection buttons open a clearly labelled stage-preview panel; they do not pretend Collection Detail has been designed. Catalogue, social and legal controls explain which client content is missing. Quote actions expose a local contact handoff. These panels are review conveniences and must be replaced with real destinations in production.

For the production site, use these routes:

| Page | Route | Intended structure / next-stage scope |
|---|---|---|
| Home | `/` | Homepage designed here |
| Collections | `/collections` | Intro, approximately 13 confirmed collection entries, catalogue |
| Collection Detail | `/collections/:slug` | Photo/info split, verified model schedule, drawings, gallery, downloads, related collections, quote |
| About | `/about` | Editorial company story, Lithuania context, product photography |
| Production / Quality | `/production-quality` | Verified materials, manufacturing process and quality documentation |
| B2B Business | `/professionals` | Project inquiries, technical documents, catalogue and representative routing |
| Contact | `/contact` | HQ, confirmed representatives, map and contact form |
| Project Inquiry | `/project-inquiry?collection=:slug` | Short professional form with collection preselection |
| Privacy / Legal | `/privacy`, `/legal` | Approved legal content |

Future localisation should use a locale-aware route helper and translated data objects. Do not rely on the English string length. Introduce the language selector only when additional languages exist. JungleMetals is not a current category or navigation item.

## Asset status and content needed

All four photographs are AI-generated art-direction placeholders, created with the built-in image-generation tool. They are not evidence of actual JunglePots product shapes, materials, installations or performance. Neither Big Ben Tower nor Riverside has a verified visual reference in the attached brief. The prototype explicitly labels this at the top and in image alternative text.

Files in this folder:

- `courtyard-concept.jpg` and `.png`: architectural hero.
- `planter-concept.jpg` and `.png`: tall product study.
- `terrace-concept.jpg` and `.png`: contextual terrace study.
- `surface-concept.jpg` and `.png`: surface/rim study.
- `junglepots-homepage.html`: responsive review prototype; keep its JPG files beside it.
- `image-prompts.json`: exact generation prompts for provenance and repeatability.

Before production, obtain the actual English catalogue, approved product images, confirmed collection list, model data, material/finish information, production photographs, representative names/contact details, JunglePots social URLs, legal content and final company copy. Hide absent technical fields rather than fill them with guesses. The catalogue-cover graphic is a concept, not a supplied catalogue cover.

## Lovable handoff instruction

Recreate the approved JunglePots homepage from the attached responsive prototype. Use React and Tailwind with the tokens, ratios, section order, crop positions and responsive rules in this guide. Preserve the offset collection composition, indexed rules, Manrope/IBM Plex Mono hierarchy, dark olive specification desk, simple country index and oversized footer wordmark. Keep components reusable and content data-driven. Replace the prototype-only disclosures with real routes when their pages are built. Do not add stock marketing sections, gradients, pills, shadows, invented technical claims or ecommerce interactions. Keep all generated images explicitly provisional until replaced with client-approved photography. Do not extend or redesign the system until the user approves this direction.

## Review checks completed

Checked page widths at 390, 768, 1024, 1440 and 1920px with no horizontal page overflow. Inspected desktop hero, collection spread and specification desk; mobile hero, navigation, catalogue and contacts. All four images loaded. Verified menu open/close and navigation, representative selection, catalogue pending-file disclosure, and collection context carried into the inquiry preview. Corrected the mobile hero crop and hidden skip-link treatment. Production functionality, legal content, real PDFs and verified product specifications remain outside this visual-design deliverable.
