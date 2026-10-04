# LIA — Pilates • Mobility • Neuromovement

Static website for Lia’s private home studio in Jumeirah Park, Dubai. No build step: Netlify publishes the repository root.

## Structure

```
index.html                 Home
about/  method/  studio/  contact/
pilates/  mobility/  neuromovement/
404.html  thank-you.html
assets/site.css            the one stylesheet (design tokens at the top)
assets/site.js             menu, header, contact details, booking form
assets/images/             photos as .webp with a .jpg twin
tools/build_pages.py       generates every page from shared templates
```

Pages are plain static HTML. To change copy or layout, edit `tools/build_pages.py`, run `python3 tools/build_pages.py`, and commit the output. When photos, CSS or JS change, bump `V` in that script so browsers fetch the new files.

## Photographs and brand artwork

Photos come from the client pack and are cropped/exported by `tools/process_photos.py`.
Logos, the navicon and the circular icons are the client’s artwork traced to SVG:

```
python3 tools/trace_brand.py    # PNG artwork in tools/brand-source → vector paths
python3 tools/build_brand.py    # logos, favicons, icons, sprite in index.html, manifest
```

To swap a photo, replace the file in `assets/images/` with the same name (or update the crop table and re-run the script).

## Contact details

At the top of `assets/site.js`, fill in the `CONTACT` object (WhatsApp, phone, email, Instagram). Each line appears on the site only once it has a value.

## Booking form

Uses **Netlify Forms** (form name `booking`). Submissions appear in Netlify → Site → Forms. Add an email notification there so requests go straight to Lia.

## Testimonials

The two quotes are taken from the design brief. Replace them with real client words before launch.
