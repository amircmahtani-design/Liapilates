"""Trace the client's raster brand artwork (logos, navicon, icon sheet) into clean SVG paths.

Source PNGs live in tools/brand-source/ (transparent background, artwork in any colour).
Output goes to tools/brand-traced/*.json as {"viewBox": [...], "d": "..."} for build_brand.py.
Run:  python3 tools/trace_brand.py
Needs: potracer, numpy, pillow
"""
import json
from pathlib import Path

import numpy as np
import potrace
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
SRC = HERE / "brand-source"
OUT = HERE / "brand-traced"

# Icon sheet: 3 x 2 grid. Names map the client's reference to the site's uses.
ICON_GRID = [
    ["personalised", "mobility", "control"],
    ["connection", "longevity", "home-studio"],
]


def trace(alpha, scale=2, turd=12):
    """alpha: 2D uint8 array. Returns (d, w, h) in the source pixel space."""
    img = Image.fromarray(alpha)
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.LANCZOS)
    img = img.filter(ImageFilter.GaussianBlur(scale * 0.6))
    # potracer fills the dark (False) pixels, so hand it the artwork as False
    bm = potrace.Bitmap(~(np.array(img) > 127))
    plist = bm.trace(turdsize=turd * scale * scale, alphamax=1.0, opticurve=True, opttolerance=0.25)
    s = 1 / scale
    parts = []
    f = lambda p: f"{p.x * s:.2f} {p.y * s:.2f}"
    for curve in plist:
        parts.append(f"M{f(curve.start_point)}")
        for seg in curve.segments:
            if seg.is_corner:
                parts.append(f"L{f(seg.c)}L{f(seg.end_point)}")
            else:
                parts.append(f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
        parts.append("Z")
    return "".join(parts)


def bbox(alpha, pad=0):
    ys, xs = np.where(alpha > 127)
    return max(xs.min() - pad, 0), max(ys.min() - pad, 0), xs.max() + 1 + pad, ys.max() + 1 + pad


def save(name, alpha, thicken=0):
    if thicken:  # icons: open the hairlines up a little so they hold at 40-64px
        alpha = np.array(Image.fromarray(alpha).filter(ImageFilter.MaxFilter(thicken)))
    x0, y0, x1, y1 = bbox(alpha)
    crop = alpha[y0:y1, x0:x1]
    d = trace(crop)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps({"viewBox": [0, 0, int(x1 - x0), int(y1 - y0)], "d": d}))
    print(f"{name}: {x1 - x0}x{y1 - y0}, {len(d)} chars")
    return crop


def main():
    for name in ("lia-logo-primary", "lia-logo-alternative", "lia-navicon-mark"):
        a = np.array(Image.open(SRC / f"{name}.png").convert("RGBA"))[..., 3]
        save(name, a)
        if name == "lia-logo-primary":
            # split the primary logo into its parts: leaf+LIA (top) and the subtitle line (bottom)
            rows = np.where((a > 127).any(axis=1))[0]
            gaps = np.where(np.diff(rows) > 8)[0]
            cut = rows[gaps[-1]] + 4
            top = a.copy(); top[cut:] = 0
            bottom = a.copy(); bottom[:cut] = 0
            save("lia-wordmark", top)
            save("lia-subtitle", bottom)

    sheet = np.array(Image.open(SRC / "lia-icon-set-reference.png").convert("RGBA"))[..., 3]
    h, w = sheet.shape
    for r, row in enumerate(ICON_GRID):
        for c, name in enumerate(row):
            cell = sheet[r * h // 2:(r + 1) * h // 2, c * w // 3:(c + 1) * w // 3]
            save(f"icon-{name}", cell, thicken=5)


if __name__ == "__main__":
    main()
