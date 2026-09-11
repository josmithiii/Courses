#!/usr/bin/env python3
"""Condition the raw single-coil E2 recording into the through-line ``note.wav``.

Source: SingleCoil3-E2-f0-E2-bp06-plectrum-mf.wav (JOS, mono 44.1 kHz, ~35 s).
Output: note.wav - mono, 44.1 kHz, 16-bit PCM, TOTAL_S seconds, starting PRE_ONSET_S
before the detected pluck onset, untouched for KEEP_S seconds, then multiplied by an
exponential decay window (time constant TAU_S) so the tail dies to silence instead of
being cut. Peak-normalized to PEAK_DBFS. Deterministic; re-run to regenerate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SRC = Path(__file__).with_name("SingleCoil3-E2-f0-E2-bp06-plectrum-mf.wav")
OUT = Path(__file__).with_name("note.wav")
PRE_ONSET_S: float = 0.030   # keep this much pre-attack silence
KEEP_S: float = 5.0          # untouched length after the start
TOTAL_S: float = 6.0         # total output length
TAU_S: float = 0.15          # exponential fade time constant (1 s of fade ~ -58 dB)
ONSET_FRAC: float = 0.01     # onset = first |x| above this fraction of peak
PEAK_DBFS: float = -1.0


def main() -> None:
    if not SRC.exists():
        sys.exit(f"*** source recording missing: {SRC}")
    x, fs = sf.read(SRC, always_2d=True)
    x = x.mean(axis=1)
    onset = int(np.argmax(np.abs(x) > ONSET_FRAC * np.abs(x).max()))
    start = max(0, onset - int(PRE_ONSET_S * fs))
    n_total = int(TOTAL_S * fs)
    y = x[start:start + n_total].copy()
    if len(y) < n_total:
        sys.exit(f"*** source too short: need {n_total} samples from {start}, got {len(y)}")
    n_keep = int(KEEP_S * fs)
    t = np.arange(n_total - n_keep) / fs
    y[n_keep:] *= np.exp(-t / TAU_S)
    peak = float(np.abs(y).max())
    if not np.isfinite(peak) or peak == 0.0:
        sys.exit("*** conditioned note is silent or non-finite")
    y *= 10 ** (PEAK_DBFS / 20) / peak
    sf.write(OUT, (np.clip(y, -1, 1) * 32767).astype(np.int16), fs, subtype="PCM_16")
    print(f"wrote {OUT}: {n_total} samples @ {fs} Hz ({TOTAL_S} s), onset at source sample "
          f"{onset} ({onset/fs:.3f} s), start {start/fs:.3f} s, fade from {KEEP_S} s, tau {TAU_S} s")


if __name__ == "__main__":
    main()
