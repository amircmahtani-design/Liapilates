"""Generate the LIA brand package (logos, mark, favicons, icons, placeholder imagery).

Text in logos is converted to outlines so the SVGs render identically everywhere.
Run:  python3 tools/build_brand.py
Needs: fonttools, cairosvg, pillow
"""
import io
import json
import random
from pathlib import Path

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"

CHARCOAL = "#1F2A23"
OLIVE = "#3E4A3F"
TAUPE = "#A89F8F"
CREAM = "#DCCFC1"
OFFWHITE = "#F8F6F2"

# ---------------------------------------------------------------- the mark
# Two leaves opening from a single stem: growth, movement, the body opening.
# Drawn on a 64x64 grid with a single line weight.
# Geometry from the client's LIA kit (branding/lia-mark.svg), re-centred on the grid.
MARK_PATHS = [
    "M23 41C11 30 11 15 25 9c9 13 7 24-2 32Z",     # upright leaf
    "M23 41C34 28 39 16 53 16c0 14-10 24-30 25Z",  # opening leaf
    "M23 41v14",                                   # stem
]


def mark_group(color, width=1.5, tx=0, ty=0, scale=1.0):
    paths = "".join(f'<path d="{d}"/>' for d in MARK_PATHS)
    return (
        f'<g transform="translate({tx} {ty}) scale({scale})" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{paths}</g>'
    )


# Bolder, filled version for tiny sizes (favicon). Fewer details, same silhouette.
FAV_LEAVES = MARK_PATHS[:2]
FAV_STEM = "M23 40.5v15"


def favicon_svg(size_hint="large"):
    sw = 4.2 if size_hint == "large" else 5.5
    sc = 0.86 if size_hint == "large" else 1.0
    leaves = "".join(f'<path d="{d}" fill="{OFFWHITE}" stroke="{OFFWHITE}" stroke-width="1.2" stroke-linejoin="round"/>' for d in FAV_LEAVES)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="14" fill="{CHARCOAL}"/>'
        f'<g transform="translate(32 32) scale({sc}) translate(-32 -32)">'
        f'{leaves}<path d="{FAV_STEM}" fill="none" stroke="{OFFWHITE}" stroke-width="{sw}" stroke-linecap="round"/>'
        "</g></svg>"
    )


# ---------------------------------------------------------------- text → outlines
_font_cache = {}


def load_font(name, wght):
    key = (name, wght)
    if key not in _font_cache:
        f = TTFont(FONTS / f"{name}.ttf")
        _font_cache[key] = instantiateVariableFont(f, {"wght": wght})
    return _font_cache[key]


def text_path(text, font, size, tracking_em=0.0):
    """Return (svg path d, width) for text set at `size` px, baseline at y=0."""
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    s = size / upm
    x = 0.0
    pen = SVGPathPen(gs)
    extra = []
    centres = []
    for i, ch in enumerate(text):
        if ch == "\u2022":  # draw a true round dot; the font's bullet is square
            r = size * 0.11
            adv = size * 0.5
            cx, cy = x + adv / 2, -cap_height(font, size) / 2
            extra.append(f"M{cx - r:.2f} {cy:.2f}a{r:.2f} {r:.2f} 0 1 0 {2 * r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2 * r:.2f} 0Z")
            x += adv + tracking_em * size
            continue
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        centres.append(x + hmtx[gname][0] * s / 2)
        tp = TransformPen(pen, (s, 0, 0, -s, x, 0))
        gs[gname].draw(tp)
        x += hmtx[gname][0] * s
        if i < len(text) - 1:
            x += tracking_em * size
    text_path.centres = centres
    return pen.getCommands() + "".join(extra), x


def cap_height(font, size):
    os2 = font["OS/2"]
    ch = getattr(os2, "sCapHeight", 0) or font["head"].unitsPerEm * 0.66
    return ch * size / font["head"].unitsPerEm


SUBTITLE = "PILATES • MOBILITY • NEUROMOVEMENT"


def wordmark_parts(color, lia_size=120, sub_size=13):
    serif = load_font("cormorant", 400)
    sans = load_font("hanken", 400)
    lia_d, lia_w = text_path("LIA", serif, lia_size, tracking_em=0.22)
    i_centre = text_path.centres[1]
    sub_d, sub_w = text_path(SUBTITLE, sans, sub_size, tracking_em=0.34)
    return dict(
        lia_d=lia_d, lia_w=lia_w, i_centre=i_centre, lia_cap=cap_height(serif, lia_size),
        sub_d=sub_d, sub_w=sub_w, sub_cap=cap_height(sans, sub_size), color=color,
    )


def stacked_logo(color, with_rule=True):
    p = wordmark_parts(color)
    W = max(p["lia_w"], p["sub_w"]) + 40
    mark_s = 1.05
    lia_x = (W - p["lia_w"]) / 2
    ix = lia_x + p["i_centre"]
    y = 6
    # stem (x=23 on the mark grid) lines up with the centre of the I; stem foot (y=55) stops just above it
    mark = mark_group(color, width=1.6, tx=ix - 23 * mark_s, ty=y, scale=mark_s)
    y += 55 * mark_s + 10
    lia_base = y + p["lia_cap"]
    sub_base = lia_base + 34 + p["sub_cap"]
    body = (
        mark
        + f'<path d="{p["lia_d"]}" fill="{color}" transform="translate({(W - p["lia_w"]) / 2:.2f} {lia_base:.2f})"/>'
        + f'<path d="{p["sub_d"]}" fill="{color}" transform="translate({(W - p["sub_w"]) / 2:.2f} {sub_base:.2f})"/>'
    )
    H = sub_base + 12
    if with_rule:
        ry = sub_base + 26
        body += f'<path d="M{W / 2 - 22:.1f} {ry:.1f}H{W / 2 + 22:.1f}" stroke="{color}" stroke-width="1"/>'
        H = ry + 10
    return svg_doc(W, H, body)


def horizontal_logo(color):
    p = wordmark_parts(color, lia_size=96, sub_size=11)
    mark_s = 1.5
    mark_w = 64 * mark_s
    gap = 34
    text_w = max(p["lia_w"], p["sub_w"])
    W = mark_w + gap + text_w + 8
    H = 64 * mark_s + 8
    lia_base = H / 2 + p["lia_cap"] / 2 - 10
    sub_base = lia_base + 24 + p["sub_cap"]
    tx = mark_w + gap
    body = (
        mark_group(color, width=1.2, tx=0, ty=4, scale=mark_s)
        + f'<path d="M{mark_w + gap / 2:.1f} 18V{H - 18:.1f}" stroke="{color}" stroke-opacity=".35" stroke-width="1"/>'
        + f'<path d="{p["lia_d"]}" fill="{color}" transform="translate({tx + 4:.2f} {lia_base:.2f})"/>'
        + f'<path d="{p["sub_d"]}" fill="{color}" transform="translate({tx + 4:.2f} {sub_base:.2f})"/>'
    )
    return svg_doc(W + 4, H, body)


def svg_doc(w, h, body, bg=None):
    rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
        f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="LIA — Pilates, Mobility, Neuromovement">'
        f"{rect}{body}</svg>"
    )


def write_svg(path, svg):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def svg_to_png(svg, path, width=None, height=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path), output_width=width, output_height=height)


# ---------------------------------------------------------------- icons
# 24px grid, 1.25 stroke, round caps. Quiet line drawings, no clip-art.
ICONS = {
    "pilates": '<path d="M3 17.5h18"/><path d="M5 17.5v2M19 17.5v2"/><path d="M6.5 14.5h7.5"/><path d="M14 14.5l3.5-6"/><circle cx="8" cy="11.6" r="1.6"/><path d="M17.5 8.5V5.5"/>',
    "mobility": '<circle cx="12" cy="12" r="8.25"/><path d="M12 12l4.5-4.5"/><path d="M12 3.75v2M20.25 12h-2M12 20.25v-2M3.75 12h2"/><path d="M8.2 6.6a6.4 6.4 0 0 1 7.6-.1" stroke-dasharray="1.2 1.6"/>',
    "neuromovement": '<circle cx="6" cy="6.5" r="2"/><circle cx="18" cy="17.5" r="2"/><path d="M7.6 7.7c3 2.4 5.8 5.4 8.8 8.6"/><path d="M18 4.5c-3.5.4-6 2.6-6.4 5.7M6 19.5c3.5-.4 6-2.6 6.4-5.7"/>',
    "personalised": '<path d="M12 20.5c-.3-5 .2-9 -.7-12.4"/><path d="M11.3 8.1C9.5 5.5 9.9 3.3 12.6 1.9c1.4 2.7.8 5-1.3 6.2z"/><path d="M12.1 13c1.9-2.3 4.4-2.9 7-1.6-1.4 2.6-4 3.3-7 1.6z"/>',
    "experience": '<circle cx="12" cy="12" r="8.25"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.75"/>',
    "home-studio": '<path d="M3.75 10.5L12 4l8.25 6.5"/><path d="M5.75 9v10.25h12.5V9"/><path d="M12 17.5c-.1-2.3.1-3.8-.3-5.3"/><path d="M11.7 12.2c-.9-1.3-.7-2.4.6-3.1.7 1.3.4 2.5-.6 3.1z"/>',
    "calendar": '<rect x="3.75" y="5.25" width="16.5" height="15" rx="1.5"/><path d="M3.75 9.75h16.5M8 3.5v3.5M16 3.5v3.5"/><path d="M8 13.5h.01M12 13.5h.01M16 13.5h.01M8 16.75h.01M12 16.75h.01"/>',
    "location": '<path d="M12 21s-6.75-6.2-6.75-11.25a6.75 6.75 0 0 1 13.5 0C18.75 14.8 12 21 12 21z"/><circle cx="12" cy="9.75" r="2.25"/>',
    "instagram": '<rect x="3.75" y="3.75" width="16.5" height="16.5" rx="4.5"/><circle cx="12" cy="12" r="3.75"/><path d="M17 7h.01"/>',
    "email": '<rect x="3.25" y="5.5" width="17.5" height="13" rx="1.5"/><path d="M3.75 6.5L12 13l8.25-6.5"/>',
    "phone": '<path d="M5.4 3.75h3.1l1.6 4.1-2 1.3a11 11 0 0 0 4.75 4.75l1.3-2 4.1 1.6v3.1a1.6 1.6 0 0 1-1.7 1.6A15.3 15.3 0 0 1 3.75 5.45a1.6 1.6 0 0 1 1.65-1.7z"/>',
    # extra icons used by the site
    "control": '<path d="M4 12h16"/><circle cx="9" cy="12" r="2.25"/><path d="M4 6.5h16M4 17.5h16" stroke-opacity=".45"/>',
    "connection": '<circle cx="8.5" cy="12" r="4.75"/><circle cx="15.5" cy="12" r="4.75"/>',
    "longevity": '<path d="M3.5 15.5c3-6 5.5-6 8.5 0s5.5 6 8.5 0"/><path d="M3.5 9.5c3-3 5.5-3 8.5 0s5.5 3 8.5 0" stroke-opacity=".45"/>',
    "arrow-right": '<path d="M4 12h15.5M14 6.5l5.5 5.5-5.5 5.5"/>',
}


def icon_svg(body, color="currentColor"):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" '
        f'stroke="{color}" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


# ---------------------------------------------------------------- placeholders
# Neutral stand-ins at the final sizes. Replace each file with the real photograph
# (same name, same aspect ratio) and the site picks it up with no code change.
PLACEHOLDERS = {
    "hero.webp": (1920, 1280, "Hero — Lia, controlled reformer work, home studio"),
    "pilates.webp": (1200, 1500, "Pilates — reformer footwork / bridge"),
    "mobility-90-90.webp": (1200, 1500, "Mobility — client in 90/90, Lia cueing"),
    "neuromovement-coordination.webp": (1200, 1500, "Neuromovement — contralateral coordination"),
    "lia-portrait.webp": (1200, 1500, "Portrait — Lia"),
    "studio-wide.webp": (1920, 1200, "Studio — wide, daylight, reformer"),
    "studio-detail.webp": (1000, 1250, "Studio — detail, mats, small equipment"),
    "private-session.webp": (1920, 1100, "Private session — warm, final CTA"),
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def placeholder(w, h, label, seed):
    rnd = random.Random(seed)
    base = Image.new("RGB", (w, h), hex_rgb(CREAM))
    # soft daylight wash from the left
    grad = Image.linear_gradient("L").rotate(90).resize((w, h))
    light = Image.new("RGB", (w, h), hex_rgb(OFFWHITE))
    base = Image.composite(light, base, grad)
    # a few large soft shapes so it reads as "photo goes here", not as a blank box
    shapes = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(shapes)
    for _ in range(5):
        r = rnd.randint(int(min(w, h) * .2), int(min(w, h) * .55))
        cx, cy = rnd.randint(0, w), rnd.randint(int(h * .3), h)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hex_rgb(TAUPE) + (46,))
    shapes = shapes.filter(ImageFilter.GaussianBlur(min(w, h) // 10))
    base = Image.alpha_composite(base.convert("RGBA"), shapes)
    d = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype(str(FONTS / "hanken.ttf"), max(18, w // 60))
    except OSError:
        font = ImageFont.load_default()
    tw = d.textlength(label.upper(), font=font)
    d.text(((w - tw) / 2, h / 2), label.upper(), fill=hex_rgb(OLIVE) + (150,), font=font)
    d.text(((w - d.textlength("PLACEHOLDER", font=font)) / 2, h / 2 - font.size * 2),
           "PLACEHOLDER", fill=hex_rgb(OLIVE) + (90,), font=font)
    return base.convert("RGB")


def noise_texture(w, h, seed, tint, amount):
    rnd = random.Random(seed)
    img = Image.effect_noise((w // 4, h // 4), amount).resize((w, h), Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(2))
    col = Image.new("RGB", (w, h), hex_rgb(tint))
    dark = Image.new("RGB", (w, h), tuple(max(0, c - 22) for c in hex_rgb(tint)))
    _ = rnd
    return Image.composite(col, dark, img.point(lambda v: 150 + v // 3))


def botanical_shadow(w, h, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), hex_rgb(OFFWHITE))
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for _ in range(26):
        x, y = rnd.randint(-100, w), rnd.randint(-100, h)
        lw, lh = rnd.randint(60, 160), rnd.randint(18, 40)
        leaf = Image.new("L", (lw, lh), 0)
        ImageDraw.Draw(leaf).ellipse((0, 0, lw, lh), fill=rnd.randint(60, 110))
        leaf = leaf.rotate(rnd.randint(0, 180), expand=True)
        mask.paste(leaf, (x, y), leaf)
    d.line((0, h, w, 0), fill=40, width=6)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    shade = Image.new("RGB", (w, h), hex_rgb(TAUPE))
    return Image.composite(shade, img, mask)


def timber(w, h, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h), (120, 86, 58))
    d = ImageDraw.Draw(img)
    slat = 46
    for x in range(0, w, slat):
        tone = rnd.randint(-14, 14)
        c = (126 + tone, 90 + tone, 60 + tone)
        d.rectangle((x, 0, x + slat - 8, h), fill=c)
        d.rectangle((x + slat - 8, 0, x + slat, h), fill=(58, 40, 28))
        for _ in range(10):
            gx = x + rnd.randint(2, slat - 12)
            d.line((gx, 0, gx + rnd.randint(-3, 3), h), fill=(c[0] - 10, c[1] - 9, c[2] - 7), width=1)
    return img.filter(ImageFilter.GaussianBlur(0.6))


# ---------------------------------------------------------------- build
def main():
    b = ASSETS / "branding"
    manifest = {"brand": "LIA — Pilates • Mobility • Neuromovement", "files": []}

    def add(path, kind, note=""):
        manifest["files"].append({"path": str(path.relative_to(ROOT)), "type": kind, "note": note})

    variants = {
        "lia-logo-dark.svg": (stacked_logo(CHARCOAL), "Stacked logo, charcoal — primary on light backgrounds"),
        "lia-logo-light.svg": (stacked_logo(OFFWHITE), "Stacked logo, off-white — reversed, for dark/photo backgrounds"),
        "lia-logo-horizontal.svg": (horizontal_logo(CHARCOAL), "Primary horizontal logo, charcoal"),
        "lia-logo-horizontal-light.svg": (horizontal_logo(OFFWHITE), "Horizontal logo, off-white"),
    }
    for name, (svg, note) in variants.items():
        write_svg(b / name, svg)
        add(b / name, "svg", note)

    for name in ("lia-logo-dark", "lia-logo-light"):
        svg = (b / f"{name}.svg").read_text()
        svg_to_png(svg, b / f"{name}.png", width=1200)
        add(b / f"{name}.png", "png", "1200px wide, transparent")

    mark = svg_doc(64, 64, mark_group(CHARCOAL, width=1.5))
    write_svg(b / "lia-mark.svg", mark)
    add(b / "lia-mark.svg", "svg", "Standalone brand mark")
    write_svg(b / "lia-mark-light.svg", svg_doc(64, 64, mark_group(OFFWHITE, width=1.5)))
    add(b / "lia-mark-light.svg", "svg", "Standalone brand mark, off-white")
    svg_to_png(mark, b / "lia-mark.png", width=1024)
    add(b / "lia-mark.png", "png", "1024px, transparent")
    # mark on a solid tile (avatars, social)
    tile = svg_doc(64, 64, mark_group(OFFWHITE, width=1.4, tx=4, ty=4, scale=56 / 64), bg=CHARCOAL)
    svg_to_png(tile, b / "lia-mark-tile.png", width=1024)
    add(b / "lia-mark-tile.png", "png", "Mark on charcoal tile — social avatar")

    f = ASSETS / "favicon"
    write_svg(f / "favicon.svg", favicon_svg())
    add(f / "favicon.svg", "svg", "Browser favicon / navicon")
    for size in (16, 32, 180, 192, 512):
        svg = favicon_svg("small" if size <= 32 else "large")
        svg_to_png(svg, f / f"favicon-{size}.png", width=size, height=size)
        add(f / f"favicon-{size}.png", "png", f"{size}×{size}")
    (f / "apple-touch-icon.png").write_bytes((f / "favicon-180.png").read_bytes())
    add(f / "apple-touch-icon.png", "png", "180×180")
    ico_imgs = [Image.open(f / f"favicon-{s}.png") for s in (16, 32)]
    ico_imgs[1].save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32)])
    add(ROOT / "favicon.ico", "ico", "16 + 32 legacy favicon at site root")

    i = ASSETS / "icons"
    for name, body in ICONS.items():
        write_svg(i / f"{name}.svg", icon_svg(body))
        add(i / f"{name}.svg", "svg", "24px line icon, 1.25 stroke, currentColor")

    im = ASSETS / "images"
    im.mkdir(parents=True, exist_ok=True)
    for n, (name, (w, h, label)) in enumerate(PLACEHOLDERS.items()):
        out = im / name
        if not out.exists():  # never overwrite a real photograph
            placeholder(w, h, label, n).save(out, "WEBP", quality=78, method=6)
        add(out, "webp", f"{w}×{h} — {label}")

    t = ASSETS / "textures"
    t.mkdir(parents=True, exist_ok=True)
    noise_texture(1200, 1200, 1, CREAM, 40).save(t / "warm-plaster.webp", "WEBP", quality=72)
    botanical_shadow(1600, 1000, 2).save(t / "botanical-shadow.webp", "WEBP", quality=72)
    timber(1200, 800, 3).save(t / "timber.webp", "WEBP", quality=74)
    for n in ("warm-plaster", "botanical-shadow", "timber"):
        add(t / f"{n}.webp", "webp", "Procedural texture (replace with photographed texture if wanted)")

    for fnt in sorted((ASSETS / "fonts").glob("*.woff2")):
        add(fnt, "woff2", "Self-hosted web font, Latin subset (OFL)")
    for doc in ("brand-guide.md", "colour-palette.txt"):
        add(ASSETS / doc, doc.rsplit(".", 1)[1], "")
    manifest["colours"] = {"charcoal": CHARCOAL, "olive": OLIVE, "taupe": TAUPE, "cream": CREAM, "offwhite": OFFWHITE}
    manifest["placeholders"] = [f["path"] for f in manifest["files"] if f["path"].startswith("assets/images/")]
    (ASSETS / "asset-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"built {len(manifest['files'])} assets")


if __name__ == "__main__":
    main()
