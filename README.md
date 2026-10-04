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
tools/build_brand.py   regenerates logos, favicons, icons (and placeholders for missing photos)
```

## Adding the photographs

The files in `assets/images/` are **placeholders**. Replace each with the real photo using the **same file name** (WebP, sizes in `assets/brand-guide.md`). No code changes needed.

## Contact details

At the bottom of `index.html`, fill in the `CONTACT` object (WhatsApp, phone, email, Instagram). Each line appears on the site only once it has a value.

## Booking form

Uses **Netlify Forms** (form name `booking`). Submissions appear in Netlify → Site → Forms. Add an email notification there so requests go straight to Lia.

## Testimonials

The two quotes are taken from the design brief. Replace them with real client words before launch.
