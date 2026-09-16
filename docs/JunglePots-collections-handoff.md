# All Collections — design handoff

The collection index contains all 13 catalogue ranges, using confirmed catalogue imagery and no prices. It preserves the approved paper / ink / olive palette, Manrope typography, monospaced labels, thin dividers and square-edged imagery.

## Browsing structure

- Sculptural (2): Big Ben Tower, Tower Bridge.
- Round (4): Dawn, Riverside Flow, Riverside Rise, Riverside Base.
- Rectangular (4): Siena, Grand Wall, Siena Kubo, Pixie.
- Systems & accessories (3): Cube Shelf, Garden, Bar Planter.

These are website editorial categories based on observed form and construction, not claimed manufacturer taxonomy. Grand Wall belongs to Rectangular for its elongated plan despite its rounded ends. No indoor/outdoor filter is offered because application evidence is not equally specific across accessories and custom systems.

Each card shows the actual name, form and scheduled size count. Expandable specification previews include available catalogue dimensions and critical caveats. Big Ben Tower links to the completed compact detail page. Other ranges currently offer factual previews and email enquiries; their full detail pages are not yet implemented. The inline conversation version opens the local Big Ben Tower preview; the standalone version provides the cross-page link.

Custom projects have a separate architectural image and expandable enquiry entry, outside the 13 standard ranges. Nothing is sent automatically by the prototype.

## Imagery and evidence

All images are extracted from the supplied PDF. The two sculptural planters and Pixie use isolated views to retain their complete silhouettes. Other collections use verified catalogue photographs. No generated products, invented project credits or unsupported finish codes are introduced. Source pages are recorded in `JunglePots-index-asset-provenance.json`. The index data lives in `JunglePots-collections-data.json`; the detailed verification queue remains in the catalogue analysis.

The Flow photo shows three pots while the schedule supplies four models; its card correctly says four sizes. Bar Planter has no schedule, so its card says “Enquire for dimensions.” Pixie's inconsistent capacities are withheld. Height and volume ambiguities are retained in the previews.

## Implementation and validation

Use one reusable card and a CMS collection array; filtering changes visibility and announces the count. The 3-column grid becomes 2 columns on tablet/mobile and 1 column below 360 px. Native details disclosures are keyboard accessible. No pagination or sorting is needed for this range size.

Desktop composition was visually inspected. The Round filter returned Dawn, Flow, Rise and Base. The Rectangular filter returned Siena, Grand Wall, Siena Kubo and Pixie. At 390 px, the page scroll width equals its content width; the Siena Kubo preview opens correctly and preserves its A width / B height / C depth convention. Big Ben Tower navigation is verified in the standalone review.

Open `junglepots-collections.html` in the extracted review package with its sibling files and asset directories. This is a design prototype, not a hosted production website. The homepage's approved design is preserved; replacing its earlier illustrative imagery is a separate next step.
