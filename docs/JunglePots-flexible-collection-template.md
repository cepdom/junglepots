# One collection template

The Big Ben Tower prototype now demonstrates the default compact layout. All collections use the same typography, gallery frame, specification hierarchy, finish band, enquiry action and related links. Content changes the amount of information, not the visual quality or page architecture.

| Area | Required core | Flexible behaviour |
|---|---|---|
| Introduction | Name, short description, verified facts, quote action | Natural title wrapping. No marketing paragraphs added to fill a column. |
| Gallery | At least one confirmed product image | Project, isolated and detail photographs share one gallery. Hide gallery controls when there is only one image. If no project photo exists, lead with the isolated product on a quiet background. Do not generate a substitute product. |
| Specification | Available measurements, their meanings and source | One model uses the simple key/value schedule shown on Big Ben Tower. Multiple sizes use a single comparison table: model, A/B/C or applicable dimensions, capacity where known. No separate section per size. |
| Drawing | Source drawing when supplied | Pair it with the schedule; a selected variant changes the drawing only when a matching drawing exists. Without a drawing, let the schedule use the full width. Never invent one. |
| Material and finish | Applicable construction and finish facts | One compact band. Swatches only for documented colour choices. Accessories use their own construction fields rather than inherited planter claims. Additional notes sit in a disclosure. |
| Resources | Available approved, price-free files | Links sit beside specifications. Hide unavailable downloads; no empty resource section. |
| Enquiry | Persistent action near the title | Expand the shared enquiry form on demand, with collection / selected variant / colour carried through. No always-open form adding length to every collection. |
| Related collections | Two or three useful links where appropriate | Compact image-and-title entries. Omit if relationships have not been selected. |

## Multiple-size behaviour

Desktop: retain one drawing and a comparison schedule, not repeated product cards. For example, Siena Kubo has rows 1 / 2 / 3 with 35 / 44 / 54 cm values. Preserve its actual A = width, B = height, C = depth convention. Capacity is omitted because none is supplied. At narrow widths, each row becomes a labelled specification block with the same ordering; keep every model available without requiring a dropdown to discover it. A model may be selected for enquiry without hiding the comparison.

Garden uses length, depth and hook count instead of planter capacity. Bar Planter, with no supplied schedule, shows a concise custom-specification enquiry and confirmed product photography. Pixie's unverified capacity stays unpublished. These are conditional data slots in the same template, not separate page designs.

## Constraints for implementation

- One shared React collection-page component fed by CMS records. Optional fields govern rendering; do not maintain copied page markup for each collection.
- No section-per-photo, duplicate download chapter, standalone construction chapter or second lifestyle spread by default.
- Keep dimensions, applicability and material facts visible. Use disclosures for secondary notes and the enquiry form, not to conceal essential specifications.
- One image stage with contained framing for isolated/detail views and an editorial crop for project views. Maintain stable frame height when switching.
- Gallery labels and captions come from image records; gallery length must be data-driven. Add useful alt text and announce the changed caption.
- Keep unresolved critical facts visible beside the affected values. Do not hide the Big Ben Tower height conflict just to shorten the page.
- No prices, basket, checkout or stock-driven purchase controls.

## Current example

Big Ben Tower now contains five real photographs in one gallery, its original diagram and schedule, the price-free PDF link, a compact finish band, an expandable enquiry and two compact related entries. The earlier standalone construction, second project spread and download section have been removed. The supplied specification PDF remains unchanged.

Browser checks: 390 px layout has no horizontal overflow; mm → cm yields 40 / 40 / 99; gallery selection loads the adjustable-feet source. The desktop page measures approximately 2,959 px in the review browser with enquiry closed. Production CMS rendering and the multiple-size table are implementation rules, not a claim that all collection pages have already been built.
