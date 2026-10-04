"""Build the LIA brand package from the client's traced artwork.

Logos, the navicon mark and the circular icon family come from the client's own
artwork (tools/brand-source/*.png), traced to vector by tools/trace_brand.py.
This script colours, pads and exports them, renders PNGs and favicons, writes the
utility icons, injects the icon sprite into index.html, and writes the manifest.

Run:  python3 tools/trace_brand.py   (only when the source artwork changes)
      python3 tools/build_brand.py
Needs: cairosvg, pillow
"""
import json
import random
import re
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
TOOLS = Path(__file__).resolve().parent
TRACED = TOOLS / "brand-traced"

CHARCOAL = "#1F2A23"
OLIVE = "#3E4A3F"
TAUPE = "#A89F8F"
CREAM = "#DCCFC1"
OFFWHITE = "#F8F6F2"

LABEL = 'role="img" aria-label="LIA — Pilates, Mobility, Neuromovement"'


def traced(name):
    j = json.loads((TRACED / f"{name}.json").read_text())
    return j["viewBox"][2], j["viewBox"][3], j["d"]


def compact(d, places=1):
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.{places}f}".rstrip("0").rstrip("."), d)


def artwork_svg(name, color, pad=0.0):
    w, h, d = traced(name)
    p = round(max(w, h) * pad)
    vb = f"{-p} {-p} {w + 2 * p} {h + 2 * p}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w + 2 * p}" height="{h + 2 * p}" {LABEL}>'
            f'<path fill="{color}" fill-rule="evenodd" d="{compact(d)}"/></svg>')


def favicon_svg(small=False):
    """Navicon mark in off-white on a charcoal tile. Small sizes get a slightly larger mark."""
    w, h, d = traced("lia-navicon-mark")
    inner = 50 if small else 44
    s = inner / max(w, h)
    tx, ty = (64 - w * s) / 2, (64 - h * s) / 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<rect width="64" height="64" rx="14" fill="{CHARCOAL}"/>'
            f'<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})" fill="{OFFWHITE}" fill-rule="evenodd" d="{compact(d)}"/>'
            "</svg>")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def png(svg, path, width=None, height=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path), output_width=width, output_height=height)


# ---------------------------------------------------------------- icons
# The client's circular icon family (traced). Square viewBox, fill = currentColor.
BRAND_ICONS = ["personalised", "mobility", "control", "connection", "longevity", "home-studio"]


def brand_icon(name):
    w, h, d = traced(f"icon-{name}")
    side = max(w, h)
    vb = f"{-(side - w) / 2:.1f} {-(side - h) / 2:.1f} {side} {side}"
    return vb, compact(d)


# Utility icons drawn to sit with the family: 24px grid, light line, round ends.
# Discipline icons are enclosed in a circle like the client's set.
CIRCLE = '<circle cx="12" cy="12" r="11"/>'
UTIL_ICONS = {
    "pilates": CIRCLE + '<path d="M5 15.5h14M6.5 15.5v2M17.5 15.5v2"/><path d="M7.5 13h6l2.75-4.5"/><circle cx="9" cy="10.6" r="1.4"/>',
    "neuromovement": CIRCLE + '<circle cx="8" cy="8" r="1.6"/><circle cx="16" cy="16" r="1.6"/><path d="M9.2 9.2l5.6 5.6"/><path d="M16 6.5c-3 .3-5 2-5.3 4.7M8 17.5c3-.3 5-2 5.3-4.7"/>',
    "experience": CIRCLE + '<circle cx="12" cy="12" r="6.5"/><circle cx="12" cy="12" r="2.25"/>',
    "calendar": '<rect x="3.75" y="5.25" width="16.5" height="15" rx="1.5"/><path d="M3.75 9.75h16.5M8 3.5v3.5M16 3.5v3.5"/><path d="M8 13.5h.01M12 13.5h.01M16 13.5h.01M8 16.75h.01M12 16.75h.01"/>',
    "location": '<path d="M12 21s-6.75-6.2-6.75-11.25a6.75 6.75 0 0 1 13.5 0C18.75 14.8 12 21 12 21z"/><circle cx="12" cy="9.75" r="2.25"/>',
    "instagram": '<rect x="3.75" y="3.75" width="16.5" height="16.5" rx="4.5"/><circle cx="12" cy="12" r="3.75"/><path d="M17 7h.01"/>',
    "email": '<rect x="3.25" y="5.5" width="17.5" height="13" rx="1.5"/><path d="M3.75 6.5L12 13l8.25-6.5"/>',
    "phone": '<path d="M5.4 3.75h3.1l1.6 4.1-2 1.3a11 11 0 0 0 4.75 4.75l1.3-2 4.1 1.6v3.1a1.6 1.6 0 0 1-1.7 1.6A15.3 15.3 0 0 1 3.75 5.45a1.6 1.6 0 0 1 1.65-1.7z"/>',
    "arrow-right": '<path d="M4 12h15.5M14 6.5l5.5 5.5-5.5 5.5"/>',
}


def util_icon_svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" '
            f'stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def sprite():
    out = []
    for name in BRAND_ICONS:
        vb, d = brand_icon(name)
        out.append(f'    <symbol id="b-{name}" viewBox="{vb}"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></symbol>')
    return "\n".join(out)


def inject_sprite():
    page = ROOT / "index.html"
    html = page.read_text()
    start, end = "<!-- brand-icons:start -->", "<!-- brand-icons:end -->"
    if start in html:
        a, b = html.index(start) + len(start), html.index(end)
        page.write_text(html[:a] + "\n" + sprite() + "\n    " + html[b:])


# ---------------------------------------------------------------- placeholders and textures
PLACEHOLDERS = {
    "hero.webp": (1920, 1280, "Hero — Lia, controlled reformer work"),
    "pilates.webp": (1600, 900, "Pilates — one-to-one reformer"),
    "mobility-90-90.webp": (1448, 1086, "Mobility — guided hip work"),
    "neuromovement-coordination.webp": (1448, 1086, "Neuromovement — balance / coordination"),
    "lia-portrait.webp": (1200, 1500, "Portrait — Lia"),
    "studio-wide.webp": (1920, 1080, "Studio \u2014 the whole room, daylight"),
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def placeholder(w, h, label, seed):
    rnd = random.Random(seed)
    base = Image.new("RGB", (w, h), hex_rgb(CREAM))
    grad = Image.linear_gradient("L").rotate(90).resize((w, h))
    base = Image.composite(Image.new("RGB", (w, h), hex_rgb(OFFWHITE)), base, grad)
    shapes = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(shapes)
    for _ in range(5):
        r = rnd.randint(int(min(w, h) * .2), int(min(w, h) * .55))
        cx, cy = rnd.randint(0, w), rnd.randint(int(h * .3), h)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hex_rgb(TAUPE) + (46,))
    base = Image.alpha_composite(base.convert("RGBA"), shapes.filter(ImageFilter.GaussianBlur(min(w, h) // 10)))
    d = ImageDraw.Draw(base)
    font = ImageFont.truetype(str(TOOLS / "fonts" / "hanken.ttf"), max(18, w // 60))
    for text, dy, a in (("PLACEHOLDER", -2, 90), (label.upper(), 0, 150)):
        d.text(((w - d.textlength(text, font=font)) / 2, h / 2 + dy * font.size), text, fill=hex_rgb(OLIVE) + (a,), font=font)
    return base.convert("RGB")


def noise_texture(w, h, tint):
    img = Image.effect_noise((w // 4, h // 4), 40).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    dark = Image.new("RGB", (w, h), tuple(max(0, c - 22) for c in hex_rgb(tint)))
    return Image.composite(Image.new("RGB", (w, h), hex_rgb(tint)), dark, img.point(lambda v: 150 + v // 3))


def botanical_shadow(w, h, seed):
    rnd = random.Random(seed)
    mask = Image.new("L", (w, h), 0)
    for _ in range(26):
        lw, lh = rnd.randint(60, 160), rnd.randint(18, 40)
        leaf = Image.new("L", (lw, lh), 0)
        ImageDraw.Draw(leaf).ellipse((0, 0, lw, lh), fill=rnd.randint(60, 110))
        leaf = leaf.rotate(rnd.randint(0, 180), expand=True)
        mask.paste(leaf, (rnd.randint(-100, w), rnd.randint(-100, h)), leaf)
    ImageDraw.Draw(mask).line((0, h, w, 0), fill=40, width=6)
    return Image.composite(Image.new("RGB", (w, h), hex_rgb(TAUPE)), Image.new("RGB", (w, h), hex_rgb(OFFWHITE)),
                           mask.filter(ImageFilter.GaussianBlur(18)))


def timber(w, h, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for x in range(0, w, 46):
        t = rnd.randint(-14, 14)
        c = (126 + t, 90 + t, 60 + t)
        d.rectangle((x, 0, x + 38, h), fill=c)
        d.rectangle((x + 38, 0, x + 46, h), fill=(58, 40, 28))
        for _ in range(10):
            gx = x + rnd.randint(2, 34)
            d.line((gx, 0, gx + rnd.randint(-3, 3), h), fill=(c[0] - 10, c[1] - 9, c[2] - 7), width=1)
    return img.filter(ImageFilter.GaussianBlur(0.6))


# ---------------------------------------------------------------- build
def main():
    manifest = {"brand": "LIA — Pilates • Mobility • Neuromovement", "files": []}

    def add(path, kind, note=""):
        manifest["files"].append({"path": str(path.relative_to(ROOT)), "type": kind, "note": note})

    b = ASSETS / "branding"
    for old in b.glob("*"):
        old.unlink()
    logos = [
        ("lia-logo-horizontal", "lia-logo-primary", CHARCOAL, "Primary logo: leaf over LIA, subtitle beneath"),
        ("lia-logo-horizontal-light", "lia-logo-primary", OFFWHITE, "Primary logo, reversed"),
        ("lia-logo-dark", "lia-logo-alternative", CHARCOAL, "Stacked logo (leaf-figure over LIA), charcoal"),
        ("lia-logo-light", "lia-logo-alternative", OFFWHITE, "Stacked logo, off-white — for dark/photo backgrounds"),
        ("lia-wordmark", "lia-wordmark", CHARCOAL, "Leaf + LIA without subtitle — site header"),
        ("lia-wordmark-light", "lia-wordmark", OFFWHITE, "Leaf + LIA without subtitle, reversed"),
        ("lia-mark", "lia-navicon-mark", CHARCOAL, "Standalone brand mark (navicon)"),
        ("lia-mark-light", "lia-navicon-mark", OFFWHITE, "Standalone brand mark, off-white"),
    ]
    for out, src, color, note in logos:
        write(b / f"{out}.svg", artwork_svg(src, color, pad=0.04))
        add(b / f"{out}.svg", "svg", note)
    for out, width in (("lia-logo-horizontal", 2000), ("lia-logo-dark", 1400), ("lia-logo-light", 1400), ("lia-mark", 1024)):
        png((b / f"{out}.svg").read_text(), b / f"{out}.png", width=width)
        add(b / f"{out}.png", "png", f"{width}px wide, transparent")
    png(favicon_svg(), b / "lia-mark-tile.png", width=1024)
    add(b / "lia-mark-tile.png", "png", "Mark on charcoal tile — social avatar")

    f = ASSETS / "favicon"
    write(f / "favicon.svg", favicon_svg())
    add(f / "favicon.svg", "svg", "Browser favicon / navicon")
    for size in (16, 32, 180, 192, 512):
        png(favicon_svg(small=size <= 32), f / f"favicon-{size}.png", width=size, height=size)
        add(f / f"favicon-{size}.png", "png", f"{size}×{size}")
    (f / "apple-touch-icon.png").write_bytes((f / "favicon-180.png").read_bytes())
    add(f / "apple-touch-icon.png", "png", "180×180")
    Image.open(f / "favicon-32.png").save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)])
    add(ROOT / "favicon.ico", "ico", "16 + 32 legacy favicon at site root")

    i = ASSETS / "icons"
    for old in i.glob("*.svg"):
        old.unlink()
    for name in BRAND_ICONS:
        vb, d = brand_icon(name)
        write(i / f"{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="64" height="64" aria-hidden="true">'
                                 f'<path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>')
        add(i / f"{name}.svg", "svg", "Client icon family (traced), fill currentColor")
    for name, body in UTIL_ICONS.items():
        write(i / f"{name}.svg", util_icon_svg(body))
        add(i / f"{name}.svg", "svg", "24px line icon, currentColor")
    inject_sprite()

    im = ASSETS / "images"
    im.mkdir(parents=True, exist_ok=True)
    for n, (name, (w, h, label)) in enumerate(PLACEHOLDERS.items()):
        out = im / name
        if not out.exists():  # never overwrite a real photograph
            placeholder(w, h, label, n).save(out, "WEBP", quality=78, method=6)
        add(out, "webp", label)

    t = ASSETS / "textures"
    t.mkdir(parents=True, exist_ok=True)
    noise_texture(1200, 1200, CREAM).save(t / "warm-plaster.webp", "WEBP", quality=72)
    botanical_shadow(1600, 1000, 2).save(t / "botanical-shadow.webp", "WEBP", quality=72)
    timber(1200, 800, 3).save(t / "timber.webp", "WEBP", quality=74)
    for n in ("warm-plaster", "botanical-shadow", "timber"):
        add(t / f"{n}.webp", "webp", "Procedural texture (replace with photographed texture if wanted)")

    for fnt in sorted((ASSETS / "fonts").glob("*.woff2")):
        add(fnt, "woff2", "Self-hosted web font, Latin subset (OFL)")
    for doc in ("brand-guide.md", "colour-palette.txt"):
        add(ASSETS / doc, doc.rsplit(".", 1)[1], "")
    manifest["colours"] = {"charcoal": CHARCOAL, "olive": OLIVE, "taupe": TAUPE, "cream": CREAM, "offwhite": OFFWHITE}
    (ASSETS / "asset-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"built {len(manifest['files'])} assets")


if __name__ == "__main__":
    main()
