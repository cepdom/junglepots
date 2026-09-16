# Header and footer — one shared component

All eight pages now use a single header and footer. Previously they had drifted
into two separate implementations, built at different times.

## What was wrong

| | Before |
|---|---|
| Header markup | Two versions: `.site-header` on the two homepages, `.header` on the other six — different heights, gaps, menu buttons (`Menu ☰` vs `Menu +`) and mobile menus |
| **Quote action on mobile** | **`display:none` on six of eight pages, and absent from their mobile menus — the site's single primary action was unreachable on a phone** |
| `aria-current` | 0 on three pages, 2 on four, 3 on Contact (where the quote link was also marked current) |
| Touch targets | Nav links had no minimum height on six pages |
| Landmarks | Only the two homepages had a `<main>` id or a skip link |
| Wordmark link | Homepages pointed it at an in-page anchor rather than home |
| Footer | Already unified by the previous pass, but styled with `!important` throughout, hard-coded hex instead of tokens, and a wordmark sized in `vw` — so inside the 1600px shell it no longer related to its container |
| Chrome | Review toolbar on five of eight pages, absent on three; a stray review note above the homepage headers |

## What it is now

**Header** — sticky, condensing once you scroll past 96px and expanding again
below 28px, with the hairline appearing only when condensed. The two
thresholds matter: a single one at 24px let any movement hovering around it
cross repeatedly, and each crossing animated 34px of layout, so the rail
flapped open and shut inside one gesture. The state is held in JS rather than
read back off the DOM, so the comparison never depends on an attribute the
transition is part-way through. On pages that run to 6000px
the navigation stays reachable without a trip back to the top. The active page
is marked once, with a rule that wipes in from the left; hovering any other
item previews the same marker.

**The quote action is always present**, including inside the mobile menu, which
also carries the email and phone.

**Mobile menu** — numbered 01–05 in the site's monospace, Escape closes it,
focus moves to the first item on open and returns to the button on close, the
page scroll locks while it is open, and the burger becomes a close mark. It
closes itself if the viewport grows past the breakpoint.

**Footer** — labelled columns (identity, pages, headquarters), the quote
action as a bordered link rather than a plain line, and **"Back to top"
restored** — it had been dropped along with the unapproved social and legal
links. Smooth scroll, or instant under reduced motion.

Social and legal links stay out, as the design guide directs, until real
destinations exist.

## Premium pass

The first version was correct but anonymous — a wordmark, five small links and
a bordered button, which could sit on any manufacturer's site. It spoke none of
the language the rest of the pages speak. This pass rebuilt it around three
ideas: more space, stronger type contrast, and fewer elements.

**A service rail.** Every section on this site opens with a mono label left, a
mono label right and a rule between. The header was the only surface not doing
it. It now carries `ARCHITECTURAL PLANTERS — LITHUANIA` and the telephone
number at 9.5px with 0.14em tracking, and collapses to nothing on scroll.

**Navigation as an index.** Uppercase Manrope at 10.5px with 0.155em tracking,
set in muted grey, resolving to ink on hover and for the current page. Against
a 33px wordmark that gives the bar a real hierarchy instead of two similar
sizes competing. The current page also carries a short rule that draws in from
the left.

**No button.** The bordered control was the most generic element on the page.
The action is now `REQUEST A QUOTE ↗` in IBM Plex Mono — unmistakably not a
nav item, so the underline still means current page, but said in the site's own
voice. It moves to olive on hover, the one place olive appears outside the
specification desk, and sits 44px clear of the navigation.

**Space.** The bar is 104px at rest, condensing to 70px. The footer opens at
52px above its top rule and gives the closing wordmark its own clamp of
vertical space.

**Footer in three columns** rather than four: identity, index, and headquarters
with the action beneath a hairline. The index is set in the same tracked
uppercase as the header nav, so the two navigations are visibly the same
system. Four columns of unequal length had left ragged air; three have
substance.

One accessibility consequence, handled: a tap target inside a 34px rail cannot
reach 44px, so the telephone link is hidden from the rail below 900px. The
number stays reachable at full size in the mobile menu and the footer.

## Implementation notes

Styling hangs off new `jpc-` class names, so none of the older header or footer
rules apply to it; those rules are now dead but harmless. Each rule is prefixed
with the page's own root id (`#jp-review`, `#jp-index-review`, and so on) so it
outranks whatever remains in the document.

The component carries **its own tokens** (`--jpc-paper`, `--jpc-ink`,
`--jpc-line`, `--jpc-muted`, `--jpc-olive`) because the eight pages name their
custom properties differently — `--paper` on five, `--jp-paper` on the
homepages. That makes the chrome portable into the React build as a single
component with no dependency on page-level naming.

The legacy `.menu` / `.menu-button` / `.mobile-nav` class names are kept on the
toggle and the menu only, so older page scripts still resolve their selectors
instead of throwing on a null. Their listeners are then detached by cloning the
button, and this component binds its own — the two never fight over the toggle.

The oversized closing wordmark has been removed. Its vertical rhythm is kept:
the bottom rule carries the margin the wordmark used to, so the footer still
breathes rather than collapsing onto the rule. On the homepage the closing
"Let's look at the plans." now ends the page, which it should have all along.

Review toolbars and the homepage review note are removed from every page.

## Verified

Eight pages, motion and reduced-motion, at 1920 / 1440 / 1024 / 768 / 390:
no console or page errors, no horizontal overflow, and one `aria-current="page"`
per navigation -- which is two per inner page, the header nav and the mobile
menu. An earlier version of this document said one per page; that was wrong.
Chrome controls: the rail's phone link is 9.5px tall above 900px and the footer
links 38px, both under the 44px minimum and both still open. Mobile menu
checked for open state, focus move, scroll lock, Escape, focus return and
release.

Build: `build_chrome.py`, applied to the extracted review package.
