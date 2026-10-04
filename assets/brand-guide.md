# LIA — Brand guide

**LIA · Pilates • Mobility • Neuromovement**
Private home studio, Jumeirah Park, Dubai.

## Essence

Private · sophisticated · warm · highly experienced · personal · calm · intelligent · movement-focused.
Premium without being pretentious. A private movement practice, never a gym, clinic or influencer brand.

Lia doesn’t teach a set of exercises — she looks at how each person moves and builds the session around them.

## Logo

All logo artwork is the client’s own (`LIA-Website-Assets` pack), traced to clean vector paths by `tools/trace_brand.py` — no live fonts, so it renders identically everywhere.

| File | Use |
|---|---|
| `branding/lia-logo-horizontal.svg / .png` | **Primary.** Leaf sweeping over LIA, subtitle beneath. Documents, signage, social headers |
| `branding/lia-logo-horizontal-light.svg` | Primary, reversed |
| `branding/lia-logo-dark.svg / .png` | Stacked alternative (leaf-figure rising above LIA), charcoal |
| `branding/lia-logo-light.svg / .png` | Stacked alternative, off-white — footer, dark or photographic backgrounds |
| `branding/lia-wordmark.svg` / `-light.svg` | Leaf + LIA without subtitle — website header and small spaces |
| `branding/lia-mark.svg / .png`, `lia-mark-light.svg` | Standalone navicon mark: the two calligraphic leaves |
| `branding/lia-mark-tile.png` | Mark on a charcoal tile — social avatars |
| `favicon/*` | Favicon / navicon: the mark in off-white on a charcoal tile, recognisable at 16 × 16 and 32 × 32 px |

Do: give the logo clear space at least equal to the height of the “L”. Use charcoal on light, off-white on dark.
Don’t: recolour, stretch, add effects, separate the leaf from the wordmark in the primary logo, or place it on busy parts of photos.

Minimum sizes: primary 160 px wide on screen; wordmark 60 px wide; mark alone 20 px (below that use the favicon).

## Colour

See `colour-palette.txt`.
Lots of off-white and cream space, charcoal typography, olive used sparingly for action (buttons, links, icons).

## Typography

Two typefaces only.

| Role | Typeface | Use |
|---|---|---|
| Headings | **Cormorant Garamond** Medium (+ Italic) | Sentence case. Italic for a deliberate second line (“Your session.”) |
| Body & UI | **Manrope** Regular / Medium / SemiBold | Body 16–17px, line-height 1.65. Labels 12px SemiBold, uppercase, +0.16em, used sparingly |

Scale (fluid): H1 44→76px · H2 34→54px · H3 26→32px · lead 17→19px · body 16→17px.
No script or handwritten type on the website. Web fonts are self-hosted in `/assets/fonts/` (Latin subset, WOFF2, SIL Open Font License).

## Layout system

- Container 1280px, gutters 20 / 28 / 40px (phone / tablet / desktop).
- Spacing scale 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 80 · 96 · 120px.
- Section padding 56 / 80 / 112px.
- Buttons: 48px high, 26px side padding, 3px radius. Primary olive, secondary 1px outline. Nothing else.
- Separation with 1px hairlines, never shadows or cards.

## Icons

The core icons are the client’s circular line family (`icons/lia-icon-set-reference.png`), traced to SVG and opened up slightly so the hairlines hold at 40–64 px:
`personalised`, `mobility`, `control`, `connection`, `longevity`, `home-studio` — fill `currentColor`.

Supporting icons (`pilates`, `neuromovement`, `experience`, `calendar`, `location`, `instagram`, `email`, `phone`, `arrow-right`) are 24 px line icons drawn to sit with that family; the discipline ones are enclosed in a circle to match.

## Photography direction

Full brief: `docs/client-kit/IMAGE-DIRECTION.md`. The mobility pose in the reference board is **not** approved.

All images share one treatment: natural Dubai daylight, warm neutral residential interiors, subtle greenery, realistic Pilates equipment, soft shadows, natural skin. Editorial, not staged; no glossy gym look.

Non-negotiables:
- Every pose anatomically plausible: five fingers, limbs that connect, no contortion, no extreme flexibility.
- Pilates = strength, control, precision (reformer footwork, bridge, side-lying work).
- Mobility = controlled joint movement (90/90 hips, thoracic rotation, ankle drills) — never splits or backbends. A normal adult client with Lia beside them cueing.
- Neuromovement = coordination, balance, proprioception (contralateral reach, balance pad, small ball). No brain graphics, no tech, no clinic.
- Show a range of ages and body types, not only young athletic women.

| Site file | Source (client pack) | Notes |
|---|---|---|
| `images/hero.webp` | pilates-reformer-movement | Lia, controlled bridge on the reformer |
| `images/pilates.webp` | pilates-private-session | One-to-one reformer instruction |
| `images/mobility-90-90.webp` | mobility-guided-session | Guided seated hip mobility |
| `images/neuromovement-coordination.webp` | neuromovement-balance-session | Single-leg balance and reach |
| `images/lia-portrait.webp` | lia-portrait-concept | Cropped to 4:5, trimmed on the right |
| `images/studio-wide.webp` | studio-wide | The whole room, shown wide in the studio section |

Re-export with `python3 tools/process_photos.py <folder of source PNGs>`; crops are defined at the top of that script.

Export as WebP, quality ~78. Hero/wide images 1600–2000 px wide, card images 800–1200 px.

## Voice

Calm, precise, warm. Short sentences. Concrete words about bodies and movement.
Avoid: “elevate”, “transform your life”, “unleash”, fitness hype, medical claims (“cure”, “treat”, “fix pain”).
