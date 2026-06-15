#!/usr/bin/env python3
"""Generate Rockbox BMP assets for h2yorushika (24-bit, PIL — matches official theme packs)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".rockbox" / "wps" / "h2yorushika"

BG = (0x1C, 0x18, 0x14)
BG_LIGHT = (0x28, 0x22, 0x1C)
AMBER = (0x8B, 0x6F, 0x47)
AMBER_LIGHT = (0xA8, 0x90, 0x70)
TRACK = (0x2A, 0x24, 0x1E)
TRACK_EDGE = (0x3D, 0x35, 0x2C)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def lerp_rgb(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))


def make_backdrop(width: int = 320, height: int = 240) -> Image.Image:
    img = Image.new("RGB", (width, height))
    px = img.load()
    cx, cy = width * 0.55, height * 0.35
    max_dist = (width**2 + height**2) ** 0.5
    for y in range(height):
        for x in range(width):
            t = y / max(height - 1, 1)
            base = lerp_rgb(BG, BG_LIGHT, t * 0.35)
            dx, dy = x - cx, y - cy
            dist = (dx * dx + dy * dy) ** 0.5
            vignette = min(dist / (max_dist * 0.65), 1.0) * 0.22
            grain = ((x * 17 + y * 31) & 7) - 3
            r = max(0, min(255, int(base[0] * (1.0 - vignette)) + grain))
            g = max(0, min(255, int(base[1] * (1.0 - vignette)) + grain))
            b = max(0, min(255, int(base[2] * (1.0 - vignette)) + grain))
            px[x, y] = (r, g, b)
    return img


def make_pb(width: int = 304, height: int = 15) -> Image.Image:
    img = Image.new("RGB", (width, height), TRACK)
    px = img.load()
    for x in range(width):
        t = x / max(width - 1, 1)
        color = lerp_rgb(AMBER, AMBER_LIGHT, t * 0.6)
        for y in range(1, height - 1):
            px[x, y] = color
    for x in range(width):
        px[x, 0] = TRACK_EDGE
        px[x, height - 1] = TRACK_EDGE
    for y in range(height):
        px[0, y] = TRACK_EDGE
        px[width - 1, y] = TRACK_EDGE
    return img


def save_bmp(path: Path, img: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "BMP")


def main() -> None:
    save_bmp(OUT / "backdrop.bmp", make_backdrop())
    save_bmp(OUT / "pb.bmp", make_pb())
    # pb_back unused in WPS; keep for optional future use
    save_bmp(OUT / "pb_back.bmp", make_pb())
    print(f"Wrote 24-bit BMP assets to {OUT}")


if __name__ == "__main__":
    main()
