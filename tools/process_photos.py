"""Crop and export the client's photography to the site's WebP files.

Usage:  python3 tools/process_photos.py /path/to/LIA-Website-Assets/images
Crops are fractions of the source image (left, top, right, bottom). Sources are never upscaled.
"""
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "images"

# target file: (source file, crop box as fractions, max width, note)
JOBS = {
    "hero.webp": ("pilates-reformer-movement.png", (0, 0, 1, 1), 1920, "Lia, controlled bridge on the reformer"),
    "pilates.webp": ("pilates-private-session.png", (0, 0, 1, 1), 1600, "One-to-one reformer instruction"),
    "mobility-90-90.webp": ("mobility-guided-session.png", (0, 0, 1, 1), 1448, "Guided seated hip mobility"),
    "neuromovement-coordination.webp": ("neuromovement-balance-session.png", (0, 0, 1, 1), 1448, "Single-leg balance and reach on a balance cushion"),
    # portrait: trimmed on the right to keep the frame on Lia, 4:5
    "lia-portrait.webp": ("lia-portrait-concept.png", (0, 0, 0.838, 0.838), 1200, "Lia, portrait"),
    # studio section: the reformer side of the room
    "studio-wide.webp": ("studio-wide.png", (0, 0.04, 0.66, 1), 1600, "Studio: reformer, arched window, daylight"),
    # final call to action: the whole room
    "private-session.webp": ("studio-wide.png", (0, 0, 1, 1), 1920, "The full home studio, warm daylight"),
}


def main(src_dir):
    src_dir = Path(src_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, (l, t, r, b), max_w, note) in JOBS.items():
        im = Image.open(src_dir / src).convert("RGB")
        w, h = im.size
        im = im.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(OUT / name, "WEBP", quality=80, method=6)
        print(f"{name}: {im.width}x{im.height} {(OUT / name).stat().st_size // 1024} KB  ({note})")


if __name__ == "__main__":
    main(sys.argv[1])
