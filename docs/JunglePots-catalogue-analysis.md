# JunglePots catalogue → product structure

All 28 pages of the supplied catalogue were reviewed visually. The catalogue is the primary product source; its graphic design is not adopted. Prices are excluded from this structure and the website. The approved homepage remains unchanged.

## Collections and variants

All dimensions below are transcribed in **cm**. Capacity is in **L**, where supplied. Letters retain each drawing's own convention.

| Collection | Variants and catalogue dimensions | Other technical fields | Photography |
|---|---|---|---|
| Big Ben Tower | One unnamed model: A40 B40 C99 | 30 L; A width, B depth, C overall height | Strong entrance and lounge projects, isolated product, rim and adjustable feet; pp. 2–3, 27 |
| Tower Bridge | One unnamed model: A40 B40 C99 | 30 L; A width, B depth, C height | Strong lounge / glazed interior images, isolated product, rim and feet; pp. 4–5, 27 |
| Siena | 65: 65/27/50; 95: 95/27/50; 95H: 95/27/70 (A/B/C) | 7 / 17 / 43 L; A length, B depth, C height | Group, rim and feet; pp. 6, 24 |
| Dawn | 295: A29.5 B30; 395: A39.5 B35; 440: A44 B40 | 21 / 43 / 60 L; A across rim, B height | Group and isolated colour groups; faceting / rim; shown on Cube Shelf; pp. 7–8, 24 |
| Riverside Flow | 200: A20 B40; 300: A30 B40; 400: A40 B50; 600: A60 B60 | 7 / 17 / 43 / 127 L; A diameter; B height convention requires clarification | Product groups and leg joint detail; pp. 9, 24 |
| Riverside Rise | 600: A30 B60; 800: A30 B80; 1000: A30 B100 | 31 L printed for all three; A diameter, B shown as overall height | Group and isolated colour groups; pp. 10, 25 |
| Riverside Base | 300: A30 B35; 400: A40 B35; 600: A60 B60 | 17 / 43 / 169 L; optional hidden wheels; A diameter, B height | Particularly strong CYBERCITY office / lobby projects plus groups; pp. 11–13, 25 |
| Grand Wall | 900: 90/42/74; 1400: 140/42/74; 1900: 190/42/74 (A/B/C) | A length, B depth, C height; capacity absent | Strong mall seating and CYBERCITY lobby projects; pp. 14–15, 26 |
| Siena Kubo | 1: 35/35/35; 2: 44/44/44; 3: 54/54/54 | A width, **B height, C depth**; hidden wheels option; capacity absent | Group, rim and feet; pp. 16, 27 |
| Cube Shelf | 30: 30/30/30; 40: 40/40/40; 50: 50/50/50 | 20 × 20 mm thick-walled square profile, powder coating, metal sheet shelf, plastic plugs; A/B plan sides, C height | Isolated frames and assembled shelf with Dawn; pp. 17, 25 |
| Garden | X1: A57 B22; X2: A111 B22; X3: A165 B22; X4: A220 B22 | 4 / 4 / 4 / 6 hooks; A length, B depth; chain or steel cable, rings/carabiners, concrete-ceiling anchors described | Strong café / glazed-office project, isolated trays and hook details; pp. 18–19, 26 |
| Bar Planter | No variant schedule supplied | Dimensions, capacity and detailed construction absent | Real office installation only; p. 20 |
| Pixie | 150: 15/15/15; 170: 17/17/17; 200: 20/20/20; 230: 23/23/23 | Printed capacities 15 / 17 / 20 / 23 L are inconsistent; hold from publication | Small isolated technical illustrations only; p. 26 |

Non-standard projects (pp. 21–22) belong in a project/custom-work entity, not a fourteenth standard range. Riverside may be a navigation family, but Flow, Rise and Base retain distinct product records.

## Shared material information

Page 23 describes galvanized steel planters with primer and powder coating, integrated height-adjustable feet, indoor/outdoor use and a sand-textured finish in matte or gloss. It lists Anthracite 7016, Pale Green 6021, Cappuccino 1014 and Pure white 9010, plus custom colours. Preserve the catalogue names; digital swatches are indicative. The red-brown finish in Big Ben Tower photography is not assigned a colour code.

The catalogue uses frost / UV resistance and handmade icons without test ratings or certifications. Do not invent ratings. Stainless steel, Corten and lacquered metal are described for custom products, not automatically as options for every standard collection. Accessory construction must remain separate from planter defaults.

## CMS issues to retain explicitly

- **Height conflict:** supplied p. 27 gives Big Ben Tower and Tower Bridge 99 cm; older online material gives 90 cm. Big Ben Tower's [existing listing](https://emedelynas.lt/vazonai-/12774-metalinis-vazonas-big-ben-tower-40x40x90cm.html) explicitly uses 90 cm. Display 99 cm provisionally with a confirmation note; never silently merge the values.
- **Per-collection A/B/C:** Siena Kubo uses B for height, whereas Big Ben Tower and Siena use C. Store measurement labels per drawing, not global A/B/C definitions.
- **Flow leg convention:** B appears to stop at the body; the separate “150” leg annotation has no printed unit. Rise depicts B as overall height. Store the unresolved annotation without inferring total height.
- **Pixie capacity:** printed litres exceed the external bounding-box volumes. Retain raw values for audit, suppress public capacity pending confirmation.
- **Other capacities:** Rise repeats 31 L across three heights; Siena volumes are small relative to external dimensions. Preserve source values, but request usable-volume / insert definitions. Do not derive replacement volumes.
- **Riverside Base:** online BASE300 dimensions differ from the supplied schedule. PDF values retain priority pending confirmation.
- **Missing fields:** product weight, steel thickness, drainage / liner system, tolerances, load ratings, fixing schedules, CAD/BIM, maintenance and performance certificates are absent. Blank is not zero or “not applicable.”
- **Variant evidence:** Flow has four scheduled models but only three photographed together. Do not infer a photo for every variant. Big Ben Tower has no supplied SKU or variant name.
- **Imagery metadata:** retain page, collection match, image role, original resolution, crop and finish-identification status. Do not guess project names, architects or locations from photographs.
- **Downloads:** the source contains prices; no public source-PDF link. The prototype supplies a newly composed price-free specification sheet with its evidence and unresolved height visible.
- **Edition:** the back cover contains a 2023 copyright, but no explicit edition date. Review date and source edition must be separate fields.

## Recommended content model

Collection → variants → measurements `{symbol, meaning, source_value, source_unit, normalized_mm, source_page, verification_status}`. Capacity has its own value, unit, definition and status. Materials, finishes and use claims carry scope (global / collection / variant) and provenance. Store images separately with role and confirmed collection match. Store documents with version, price-free status and approval status. Keep unresolved facts in a verification queue; hold critical unverified dimensions before production specification.

Big Ben Tower is the strongest first example: distinctive geometry, two complementary architectural images, an isolated product, two construction details and an A/B/C schedule. It demonstrates the editorial and professional specification system without inventing multiple sizes.
