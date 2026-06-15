#!/usr/bin/env python3
"""Generate Rockbox RGB565 BMP assets for h2yorushika (Amy diary theme)."""

from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".rockbox" / "wps" / "h2yorushika"

# Amy diary palette
BG = (0x1C, 0x18, 0x14)
BG_LIGHT = (0x28, 0x22, 0x1C)
PAPER = (0xF0, 0xE8, 0xDC)
AMBER = (0x8B, 0x6F, 0x47)
AMBER_LIGHT = (0xA8, 0x90, 0x70)
TRACK = (0x2A, 0x24, 0x1E)
TRACK_EDGE = (0x3D, 0x35, 0x2C)


def rgb565(r: int, g: int, b: int) -> int:
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


def save_bmp565(path: Path, width: int, height: int, pixels: list[list[tuple[int, int, int]]]) -> None:
    """Save bottom-up RGB565 BMP with BI_BITFIELDS (Rockbox-compatible)."""
    row_bytes = width * 2
    row_padded = (row_bytes + 3) & ~3
    pixel_data = bytearray()
    for row in reversed(pixels):
        line = bytearray()
        for r, g, b in row:
            line.extend(struct.pack("<H", rgb565(r, g, b)))
        line.extend(b"\x00" * (row_padded - row_bytes))
        pixel_data.extend(line)

    header_size = 14 + 40 + 12
    file_size = header_size + len(pixel_data)
    buf = bytearray()
    # BITMAPFILEHEADER
    buf.extend(b"BM")
    buf.extend(struct.pack("<I", file_size))
    buf.extend(struct.pack("<HH", 0, 0))
    buf.extend(struct.pack("<I", header_size))
    # BITMAPINFOHEADER
    buf.extend(struct.pack("<I", 40))
    buf.extend(struct.pack("<ii", width, height))
    buf.extend(struct.pack("<HH", 1, 16))
    buf.extend(struct.pack("<I", 3))  # BI_BITFIELDS
    buf.extend(struct.pack("<I", len(pixel_data)))
    buf.extend(struct.pack("<iiii", 2835, 2835, 0, 0))
    # RGB565 masks
    buf.extend(struct.pack("<III", 0xF800, 0x07E0, 0x001F))
    buf.extend(pixel_data)
    path.write_bytes(buf)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def lerp_rgb(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))


def make_backdrop(width: int = 320, height: int = 240) -> list[list[tuple[int, int, int]]]:
    pixels: list[list[tuple[int, int, int]]] = []
    cx, cy = width * 0.55, height * 0.35
    max_dist = (width**2 + height**2) ** 0.5
    for y in range(height):
        row: list[tuple[int, int, int]] = []
        for x in range(width):
            # Warm vertical gradient
            t = y / max(height - 1, 1)
            base = lerp_rgb(BG, BG_LIGHT, t * 0.35)
            # Soft vignette toward corners
            dx = x - cx
            dy = y - cy
            dist = (dx * dx + dy * dy) ** 0.5
            vignette = min(dist / (max_dist * 0.65), 1.0) * 0.22
            r = max(0, int(base[0] * (1.0 - vignette)))
            g = max(0, int(base[1] * (1.0 - vignette)))
            b = max(0, int(base[2] * (1.0 - vignette)))
            # Subtle paper grain
            grain = ((x * 17 + y * 31) & 7) - 3
            row.append((min(255, r + grain), min(255, g + grain), min(255, b + grain)))
        pixels.append(row)
    return pixels


def solid(width: int, height: int, color: tuple[int, int, int]) -> list[list[tuple[int, int, int]]]:
    return [[color for _ in range(width)] for _ in range(height)]


def make_pb_back(width: int = 304, height: int = 6) -> list[list[tuple[int, int, int]]]:
    pixels = solid(width, height, TRACK)
    for y in range(height):
        pixels[y][0] = TRACK_EDGE
        pixels[y][width - 1] = TRACK_EDGE
    pixels[0] = [TRACK_EDGE] * width
    pixels[height - 1] = [TRACK_EDGE] * width
    return pixels


def make_pb_fill(width: int = 304, height: int = 6) -> list[list[tuple[int, int, int]]]:
    pixels: list[list[tuple[int, int, int]]] = []
    for _ in range(height):
        row: list[tuple[int, int, int]] = []
        for x in range(width):
            t = x / max(width - 1, 1)
            row.append(lerp_rgb(AMBER, AMBER_LIGHT, t * 0.6))
        pixels.append(row)
    return pixels


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    save_bmp565(OUT / "backdrop.bmp", 320, 240, make_backdrop())
    save_bmp565(OUT / "pb_back.bmp", 304, 6, make_pb_back())
    save_bmp565(OUT / "pb.bmp", 304, 6, make_pb_fill())
    print(f"Wrote assets to {OUT}")


if __name__ == "__main__":
    main()
