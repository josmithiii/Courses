#!/usr/bin/env python3
"""Generate the deterministic synthetic PLACEHOLDER through-line note.

Writes ``note-placeholder.wav``: a Karplus-Strong plucked string (extended with a
one-pole loop filter for frequency-dependent decay), A2 (110 Hz), mono, 44.1 kHz,
16-bit PCM, 1.5 s.  A fixed random seed makes every learner's file identical.

This is NOT ``note.wav``.  The real through-line note is a recording (see README.md).
Tutors must never treat the placeholder as the real note without saying so.

Usage:
    python3 make_note.py            # writes note-placeholder.wav next to this file
    python3 make_note.py out.wav    # writes to the given path
"""

from __future__ import annotations

import math
import struct
import sys
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE: int = 44_100
F1_HZ: float = 110.0          # open A string, A2
DURATION_S: float = 1.5
LOOP_GAIN: float = 0.996      # overall decay per period
LOOP_FILTER_ALPHA: float = 0.5  # one-pole lowpass: y[n] = a*x[n] + (1-a)*x[n-1]
SEED: int = 423
PEAK_DBFS: float = -1.0


def karplus_strong(f1_hz: float, duration_s: float, fs: int, seed: int) -> np.ndarray:
    """Extended Karplus-Strong: noise burst into a delay line with a one-pole loop filter."""
    period: float = fs / f1_hz
    delay_len: int = int(round(period))          # integer delay (fine for a placeholder)
    n_samples: int = int(duration_s * fs)
    rng = np.random.default_rng(seed)
    buf: np.ndarray = rng.uniform(-1.0, 1.0, delay_len)   # the pluck: a burst of noise
    out = np.empty(n_samples, dtype=np.float64)
    prev: float = 0.0
    for n in range(n_samples):
        x = buf[n % delay_len]
        y = LOOP_GAIN * (LOOP_FILTER_ALPHA * x + (1.0 - LOOP_FILTER_ALPHA) * prev)
        prev = x
        buf[n % delay_len] = y
        out[n] = x
    return out


def normalize(x: np.ndarray, peak_dbfs: float) -> np.ndarray:
    peak = float(np.max(np.abs(x)))
    if not math.isfinite(peak) or peak == 0.0:
        raise RuntimeError("*** synthesized note is silent or non-finite; refusing to write")
    return x * (10.0 ** (peak_dbfs / 20.0)) / peak


def write_wav16(path: Path, x: np.ndarray, fs: int) -> None:
    pcm = np.clip(np.round(x * 32767.0), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(pcm.tobytes())


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("note-placeholder.wav")
    note = normalize(karplus_strong(F1_HZ, DURATION_S, SAMPLE_RATE, SEED), PEAK_DBFS)
    write_wav16(out, note, SAMPLE_RATE)
    print(f"wrote {out} ({len(note)} samples, {SAMPLE_RATE} Hz, f1 = {F1_HZ} Hz)  [PLACEHOLDER, not note.wav]")


if __name__ == "__main__":
    main()
