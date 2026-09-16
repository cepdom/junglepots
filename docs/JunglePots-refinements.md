# Refinement pass

The previous connected review is preserved as `JunglePots-before-refinements.zip`.

## Imagery

Twelve collection cards now use genuine catalogue-native isolated product views. Green-wall backgrounds have been removed from the browsing experience by selecting existing isolated assets, not by generating or reconstructing planters. Bar Planter retains its actual project photograph because no isolated view is supplied. Custom projects retain architectural photography.

The product cards share a quiet background, contained image treatment and consistent spacing. CSS blending integrates the original white backgrounds with the page surface; it is not a colour-accurate finish simulation. Product photographs are not displayed at a common physical scale. Some images show one representative model and others a group; scheduled variant counts remain independent of photo counts. Updated image provenance is in the index provenance file.

## Motion

All four standalone pages now have one-time, 550 ms section entrances, small link-arrow movement and 320 ms collection/construction image fades where those selectors exist. The effects use browser-native animation and IntersectionObserver, with no animation library. Reduced-motion preference disables these additions. Content remains visible if JavaScript or animation is unavailable; scrolling is never intercepted.

## Scope and checks

Existing page structures and technical disclosures are retained. The index footer copy is shortened and clarifies that images are not to scale. The homepage's earlier contextual concept images have not been replaced in this pass. No new claims, measurements or finish codes are introduced.

The refined desktop index was visually inspected. At 390 px the content and scroll widths both measure 390 px. The Round filter still reports four collections. Product view switching, enquiry actions and previous specification data remain in the existing components. Motion is progressive enhancement, not required for navigation.

Build order: run the three page builders, then apply the shared `work/premium-motion.html` enhancement to final outputs. `work/apply_refinements.py` records this pass and should not be blindly rerun as an idempotent build: it appends styles. The standalone HTML files in the review archive are the final design deliverables for later React/Tailwind implementation.
