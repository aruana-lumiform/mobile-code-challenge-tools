#!/usr/bin/env python3
"""Generate the placeholder JPEGs referenced by code-challenge/challenge.json.

The images are committed to the repo; this script exists so they can be
regenerated or restyled deterministically instead of being opaque binaries.

Usage: python3 scripts/generate_images.py
Requires: pillow
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "code-challenge"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SIZE = (1600, 1000)

IMAGES = [
    {
        "name": "welcome.jpg",
        "title": "Welcome Image",
        "subtitle": "Mobile Code Challenge",
        "colors": ((28, 58, 122), (64, 132, 211)),
    },
    {
        "name": "chapter1.jpg",
        "title": "Chapter 1 Image",
        "subtitle": "Subsection 1.1",
        "colors": ((17, 92, 84), (58, 179, 143)),
    },
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


def gradient(size, start, end) -> Image.Image:
    """Vertical two-colour gradient, drawn one row at a time."""
    width, height = size
    base = Image.new("RGB", (1, height))
    pixels = base.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        pixels[0, y] = tuple(round(s + (e - s) * t) for s, e in zip(start, end))
    return base.resize(size, Image.BILINEAR)


def centered(draw: ImageDraw.ImageDraw, text: str, font, y: int, fill) -> None:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    draw.text(
        ((SIZE[0] - (right - left)) / 2 - left, y - top),
        text,
        font=font,
        fill=fill,
    )


def build(spec: dict) -> Path:
    image = gradient(SIZE, *spec["colors"])
    draw = ImageDraw.Draw(image, "RGBA")

    # Soft diagonal band so a scaled-down thumbnail still reads as a picture.
    draw.polygon(
        [(0, 760), (SIZE[0], 470), (SIZE[0], SIZE[1]), (0, SIZE[1])],
        fill=(255, 255, 255, 26),
    )
    draw.rounded_rectangle((60, 60, SIZE[0] - 60, SIZE[1] - 60), radius=28,
                           outline=(255, 255, 255, 90), width=3)

    centered(draw, spec["title"], load_font(FONT_BOLD, 108), 380, (255, 255, 255))
    centered(draw, spec["subtitle"], load_font(FONT_REGULAR, 52), 530, (255, 255, 255, 215))
    centered(draw, f"{SIZE[0]} x {SIZE[1]}", load_font(FONT_REGULAR, 34), 640, (255, 255, 255, 170))

    out = OUT_DIR / spec["name"]
    image.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in IMAGES:
        path = build(spec)
        print(f"wrote {path.relative_to(Path.cwd())} ({path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
