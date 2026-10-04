# LIA — Pilates • Mobility • Neuromovement

Static website for Lia’s private home studio in Jumeirah Park, Dubai. No build step: Netlify publishes the repository root.

## Structure

```
index.html          the whole site (inline CSS + JS)
thank-you.html      form fallback page
netlify.toml        headers / publish settings
site.webmanifest
assets/
  branding/  favicon/  icons/  images/  textures/  fonts/
  brand-guide.md  colour-palette.txt  asset-manifest.json
docs/client-kit/      the client's brief, image direction and reference boards
tools/build_brand.py   regenerates logos, favicons, icons (and placeholders for missing photos)
```

## Photographs and brand artwork

Photos come from the client pack and are cropped/exported by `tools/process_photos.py`.
Logos, the navicon and the circular icons are the client’s artwork traced to SVG:

```
python3 tools/trace_brand.py    # PNG artwork in tools/brand-source → vector paths
python3 tools/build_brand.py    # logos, favicons, icons, sprite in index.html, manifest
```

To swap a photo, replace the file in `assets/images/` with the same name (or update the crop table and re-run the script).

## Contact details

At the bottom of `index.html`, fill in the `CONTACT` object (WhatsApp, phone, email, Instagram). Each line appears on the site only once it has a value.

## Booking form

Uses **Netlify Forms** (form name `booking`). Submissions appear in Netlify → Site → Forms. Add an email notification there so requests go straight to Lia.

## Testimonials

The two quotes are taken from the design brief. Replace them with real client words before launch.
