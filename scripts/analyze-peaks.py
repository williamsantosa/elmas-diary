#!/usr/bin/env python3
"""Analyze peak levels across sim music files for peak meter tuning."""

from __future__ import annotations

import os
import subprocess
import sys

import numpy as np

MUSIC = r"C:\RockboxSim\simdisk\Music"
TRACKS = [
    "01_01_晴る_ヨルシカ.flac",
    "Value - Ado.opus",
    "八月、某、月明かり–ヨルシカ｜Guitar cover By雨音 空 - Kuu Amane (128k).opus",
]
WIN_SEC = 0.05
SR = 48000


def analyze(path: str) -> dict | None:
    win = int(WIN_SEC * SR)
    cmd = ["ffmpeg", "-hide_banner", "-i", path, "-ac", "1", "-f", "f32le", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()
    if proc.returncode != 0 or not raw:
        return None
    samples = np.frombuffer(raw, dtype=np.float32)
    n = len(samples) // win
    blocks = samples[: n * win].reshape(n, win)
    peak_db = 20 * np.log10(np.maximum(np.max(np.abs(blocks), axis=1), 1e-9))
    rms = max(float(np.sqrt(np.mean(samples**2))), 1e-9)
    return {
        "name": os.path.basename(path),
        "dur": len(samples) / SR,
        "mean": 20 * np.log10(rms),
        "max": float(peak_db.max()),
        "p1": float(np.percentile(peak_db, 1)),
        "p5": float(np.percentile(peak_db, 5)),
        "p10": float(np.percentile(peak_db, 10)),
        "p25": float(np.percentile(peak_db, 25)),
        "p50": float(np.percentile(peak_db, 50)),
        "p75": float(np.percentile(peak_db, 75)),
        "p90": float(np.percentile(peak_db, 90)),
        "p99": float(np.percentile(peak_db, 99)),
        "peak_db": peak_db,
    }


def display_pct(peak_db: np.ndarray, min_db: float, max_db: float = 0.0) -> np.ndarray:
    span = max_db - min_db
    return np.clip(100 * (peak_db - min_db) / span, 0, 100)


def main() -> int:
    paths = [os.path.join(MUSIC, name) for name in TRACKS]
    paths = [p for p in paths if os.path.isfile(p)]
    if not paths:
        print("No tracks found", file=sys.stderr)
        return 1

    tracks: list[dict] = []
    for path in paths:
        row = analyze(path)
        if not row:
            print(f"FAILED: {path}", file=sys.stderr)
            continue
        tracks.append(row)
        short = row["name"].encode("ascii", "backslashreplace").decode("ascii")
        print(f"=== {short} ({row['dur']:.0f}s) ===")
        print(f"mean~{row['mean']:.1f} max={row['max']:.1f} dBFS")
        for k in ("p1", "p5", "p10", "p25", "p50", "p75", "p90", "p99"):
            print(f"  {k}: {row[k]:6.1f} dB")
        print()

    if not tracks:
        return 1

    print("=== Simulated bar fill (linear dB map, max=0) ===")
    candidates = [60, 48, 40, 36, 30, 27, 24, 21, 20, 18, 15]
    best: tuple[int, float] | None = None
    for min_cfg in candidates:
        min_db = -min_cfg
        print(f"--- min={min_cfg} (-{min_cfg} dB) ---")
        score = 0.0
        for row in tracks:
            pcts = display_pct(row["peak_db"], min_db)
            p10, p50, p90 = np.percentile(pcts, [10, 50, 90])
            peg = 100 * np.mean(pcts >= 99)
            short = row["name"].encode("ascii", "backslashreplace").decode("ascii")
            print(
                f"  {short[:44]:44s} "
                f"p10={p10:5.0f}% p50={p50:5.0f}% p90={p90:5.0f}% peg={peg:4.1f}%"
            )
            # want p10>5, p50 35-75, p90<100, peg<40 per track; penalize extremes
            if p10 < 3:
                score += (3 - p10) * 2
            if p50 < 20:
                score += (20 - p50)
            if p50 > 85:
                score += (p50 - 85) * 1.5
            if peg > 45:
                score += (peg - 45) * 2
        print(f"  score={score:.1f} (lower is better)")
        if best is None or score < best[1]:
            best = (min_cfg, score)
        print()

    if best:
        print(f"Recommended min: {best[0]} (score={best[1]:.1f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
