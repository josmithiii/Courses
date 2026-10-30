#!/usr/bin/env python3
"""Generate the course's own diagrams as SVG files in ai-foundations/figures/.

All figures share one visual language, so a color or shape means the same thing
everywhere. Figures are computed where they can be: the heatmap and the noise tiles
come from the published formulas, not from drawing. Standard library only.

    tools/build_figures.py           # rewrite the figures
    tools/build_figures.py --check   # exit 1 if any figure is stale
"""

from __future__ import annotations

import argparse
import base64
import math
import random
import struct
import sys
import zlib
from collections.abc import Callable
from pathlib import Path
from typing import NoReturn
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / "ai-foundations/figures"

FONT = "Helvetica, Arial, sans-serif"
INK = "#23262b"
MUTED = "#667080"
EDGE = "#aab2bd"

# Meaning of each color across every figure: (stroke, fill).
DATA = ("#1f8a7d", "#d6f0ec")  # data and tensors
LEARNED = ("#d0701a", "#fbe7d3")  # has trainable weights
FIXED = ("#5b6b80", "#e8edf2")  # fixed operation, no weights
OUTPUT = ("#7a4ca3", "#ecdff4")  # model output

Point = tuple[float, float]


def die(msg: str) -> NoReturn:
    print(f"*** build_figures: {msg}", file=sys.stderr)
    sys.exit(1)


def png_data_uri(rows: list[list[tuple[int, int, int]]]) -> str:
    """Encode RGB pixel rows as a PNG data URI (keeps pixel images compact and deterministic)."""
    height, width = len(rows), len(rows[0])
    raw = b"".join(b"\0" + bytes(c for px in row for c in px) for row in rows)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    return "data:image/png;base64," + base64.b64encode(png).decode()


class Fig:
    def __init__(self, width: int, height: int, title: str, grammar: str, legend: list[str]) -> None:
        self.width, self.height = width, height
        self.title, self.grammar, self.legend = title, grammar, legend
        self.parts: list[str] = []

    def add(self, element: str) -> None:
        self.parts.append(element)

    def text(self, x: float, y: float, s: str, size: int = 14, color: str = INK, anchor: str = "middle",
             weight: str = "normal", sub: str = "") -> None:
        tail = (f'<tspan dy="4" font-size="{size - 3}">{escape(sub)}</tspan>' if sub else "")
        self.add(f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
                 f' font-weight="{weight}">{escape(s)}{tail}</text>')

    def line(self, a: Point, b: Point, color: str = EDGE, width: float = 1.5, dash: str = "") -> None:
        dashed = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{a[0]:g}" y1="{a[1]:g}" x2="{b[0]:g}" y2="{b[1]:g}" stroke="{color}"'
                 f' stroke-width="{width:g}"{dashed}/>')

    def arrow(self, points: list[Point], color: str = MUTED, width: float = 1.8, dash: str = "") -> None:
        """A polyline ending in an arrowhead."""
        for a, b in zip(points[:-2], points[1:-1]):
            self.line(a, b, color, width, dash)
        (x0, y0), (x1, y1) = points[-2], points[-1]
        angle, head = math.atan2(y1 - y0, x1 - x0), 9.0
        base = (x1 - head * math.cos(angle), y1 - head * math.sin(angle))
        self.line((x0, y0), base, color, width, dash)
        wings = [(x1 - head * math.cos(angle + s * 0.42), y1 - head * math.sin(angle + s * 0.42)) for s in (1, -1)]
        corners = " ".join(f"{x:g},{y:g}" for x, y in [(x1, y1), *wings])
        self.add(f'<polygon points="{corners}" fill="{color}"/>')

    def box(self, cx: float, cy: float, label: str, kind: tuple[str, str], w: float = 170, h: float = 34) -> None:
        stroke, fill = kind
        self.add(f'<rect x="{cx - w / 2:g}" y="{cy - h / 2:g}" width="{w:g}" height="{h:g}" rx="5"'
                 f' fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.text(cx, cy + 5, label)

    def circle(self, cx: float, cy: float, r: float, kind: tuple[str, str], width: float = 1.8) -> None:
        stroke, fill = kind
        self.add(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{width:g}"/>')

    def plane(self, x: float, y: float, w: float, h: float, kind: tuple[str, str]) -> None:
        stroke, fill = kind
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')

    def image(self, x: float, y: float, w: float, h: float, rows: list[list[tuple[int, int, int]]]) -> None:
        self.add(f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" style="image-rendering:pixelated"'
                 f' preserveAspectRatio="none" href="{png_data_uri(rows)}"/>')
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="none" stroke="{EDGE}"/>')

    def svg(self) -> str:
        pill = 9 * len(self.grammar) + 22
        head = [
            f'<rect width="{self.width}" height="{self.height}" rx="10" fill="#ffffff"/>',
            f'<text x="24" y="36" font-size="21" font-weight="bold" fill="{INK}">{escape(self.title)}</text>',
            f'<rect x="{self.width - pill - 20}" y="18" width="{pill}" height="26" rx="13" fill="#f1f3f6" stroke="{EDGE}"/>',
            f'<text x="{self.width - 20 - pill / 2:g}" y="36" font-size="14" fill="{MUTED}" text-anchor="middle">{escape(self.grammar)}</text>',
        ]
        y0 = self.height - 14 - 19 * (len(self.legend) - 1)
        foot = [f'<text x="24" y="{y0 + 19 * i}" font-size="14" fill="{MUTED}">{escape(line)}</text>'
                for i, line in enumerate(self.legend)]
        body = "\n".join(head + self.parts + foot)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}"'
                f' width="{self.width}" height="{self.height}" font-family="{FONT}">\n{body}\n</svg>\n')


def mlp() -> str:
    fig = Fig(860, 450, "Multi-layer perceptron", "Graph", [
        "In this grammar a circle is one number and a line is one weight.",
    ])
    columns = [(200.0, [155.0, 225.0, 295.0], DATA, "input"),
               (380.0, [120.0, 190.0, 260.0, 330.0], LEARNED, "hidden"),
               (560.0, [190.0, 260.0], OUTPUT, "output")]
    for (x0, ys0, _, _), (x1, ys1, _, _) in zip(columns, columns[1:]):
        for y0 in ys0:
            for y1 in ys1:
                fig.line((x0, y0), (x1, y1))
    start, end = (200.0, 295.0), (380.0, 330.0)
    fig.line(start, end, LEARNED[0], 3.5)
    for x, ys, kind, label in columns:
        fig.text(x, 84, label, 15, MUTED)
        for y in ys:
            fig.circle(x, y, 20, kind)
    mid = (290.0, 312.5)
    fig.line(mid, (290.0, 372.0), LEARNED[0], 1.2, "3 3")
    fig.text(290, 390, "one line = one weight", 15, LEARNED[0], weight="bold")
    fig.line((580.0, 190.0), (612.0, 165.0), OUTPUT[0], 1.2, "3 3")
    fig.text(616, 160, "one circle = one number", 15, OUTPUT[0], "start", "bold")
    return fig.svg()


def lenet() -> str:
    fig = Fig(980, 400, "LeNet-5", "Slab", [
        "In this grammar a block is a tensor and the gap between blocks is an operation.",
        "6@28x28 means 6 feature maps, each 28 by 28. Plane sizes are drawn to scale.",
    ])
    cell, cy, gap = 3.3, 190.0, 50.0
    stages: list[tuple[str, int, int, tuple[str, str]]] = [
        ("input 32x32", 1, 32, DATA), ("6@28x28", 6, 28, DATA), ("6@14x14", 6, 14, DATA),
        ("16@10x10", 16, 10, DATA), ("16@5x5", 16, 5, DATA),
    ]
    ops = ["conv 5x5", "subsample", "conv 5x5", "subsample", "full", "full", "Gaussian"]
    x = 34.0
    right_edges: list[float] = []
    lefts: list[float] = []
    for label, maps, size, kind in stages:
        side, step = size * cell, (4.0 if maps <= 6 else 2.6)
        lefts.append(x)
        depth = (maps - 1) * step
        top = cy - (side - depth) / 2
        for i in range(maps - 1, -1, -1):
            fig.plane(x + i * step, top - i * step, side, side, kind)
        fig.text(x + (side + depth) / 2, top - depth - 12, label, 14)
        x += side + depth
        right_edges.append(x)
        x += gap
    for label, n in (("120", 120), ("84", 84), ("10", 10)):
        height = 40 + 1.6 * n
        lefts.append(x)
        fig.plane(x, cy - height / 2, 16, height, LEARNED if n != 10 else OUTPUT)
        fig.text(x + 8, cy - height / 2 - 12, label, 14)
        x += 16
        right_edges.append(x)
        x += gap
    for i, op in enumerate(ops):
        a, b = right_edges[i], lefts[i + 1]
        fig.arrow([(a + 5, cy), (b - 5, cy)])
        kind = FIXED if op == "subsample" else LEARNED
        fig.text((a + b) / 2, 318, op, 13, kind[0])
    if x - gap > fig.width - 20:
        die(f"lenet: layout overflows at x={x - gap:g}")
    return fig.svg()


def transformer() -> str:
    fig = Fig(760, 800, "The Transformer", "Block", [
        "In this grammar a box is an operation and an arrow carries a whole tensor.",
        "Read bottom to top. Orange has trained weights; gray does not.",
    ])
    enc, dec = 235.0, 520.0

    def frame(left: float, top: float, right: float, bottom: float) -> None:
        fig.add(f'<rect x="{left:g}" y="{top:g}" width="{right - left:g}" height="{bottom - top:g}" rx="10"'
                f' fill="none" stroke="{EDGE}" stroke-width="1.5" stroke-dasharray="6 5"/>')

    def skip(cx: float, side: float, y_from: float, y_to: float) -> None:
        """Residual arrow around a sublayer, entering the Add & Norm box at y_to."""
        edge = cx + (85 if side > cx else -85)
        fig.arrow([(cx, y_from), (side, y_from), (side, y_to), (edge, y_to)], MUTED, 1.4)

    def embed(cx: float, name: str, label: str) -> None:
        fig.text(cx, 738, label, 14, DATA[0], weight="bold")
        fig.arrow([(cx, 725), (cx, 699)])
        fig.box(cx, 682, name, LEARNED)
        fig.arrow([(cx, 665), (cx, 652)])
        fig.circle(cx, 638, 13, FIXED)
        fig.text(cx, 643, "+", 17)

    frame(112, 378, 335, 588)
    frame(420, 278, 648, 608)
    embed(enc, "Input Embedding", "Inputs")
    embed(dec, "Output Embedding", "Outputs (shifted right)")
    fig.text(enc - 22, 642, "positional encoding", 13, FIXED[0], "end")
    fig.text(dec + 22, 642, "positional encoding", 13, FIXED[0], "start")

    # Encoder, bottom to top.
    fig.arrow([(enc, 625), (enc, 577)])
    fig.box(enc, 560, "Multi-Head Attention", LEARNED)
    skip(enc, 128, 601, 515)
    fig.arrow([(enc, 543), (enc, 532)])
    fig.box(enc, 515, "Add & Norm", FIXED)
    fig.arrow([(enc, 498), (enc, 467)])
    fig.box(enc, 450, "Feed Forward", LEARNED)
    skip(enc, 128, 482, 405)
    fig.arrow([(enc, 433), (enc, 422)])
    fig.box(enc, 405, "Add & Norm", FIXED)

    # Decoder, bottom to top.
    fig.arrow([(dec, 625), (dec, 592)])
    fig.box(dec, 575, "Masked Multi-Head Attn", LEARNED)
    skip(dec, 630, 600, 530)
    fig.arrow([(dec, 558), (dec, 547)])
    fig.box(dec, 530, "Add & Norm", FIXED)
    fig.arrow([(dec, 513), (dec, 477)])
    fig.text(dec - 10, 499, "Q", 13, MUTED, "end")
    fig.box(dec, 460, "Multi-Head Attention", LEARNED)
    skip(dec, 630, 492, 415)
    fig.arrow([(dec, 443), (dec, 432)])
    fig.box(dec, 415, "Add & Norm", FIXED)
    fig.arrow([(dec, 398), (dec, 367)])
    fig.box(dec, 350, "Feed Forward", LEARNED)
    skip(dec, 630, 382, 305)
    fig.arrow([(dec, 333), (dec, 322)])
    fig.box(dec, 305, "Add & Norm", FIXED)

    # Cross-attention: encoder output into the decoder.
    fig.arrow([(enc, 388), (enc, 350), (385, 350), (385, 460), (dec - 85, 460)], DATA[0], 2.2)
    fig.text(392, 452, "K, V", 13, DATA[0], "start")
    fig.text(enc, 338, "Encoder", 16, weight="bold")
    fig.text(100, 490, "N x", 15, MUTED, "end")
    fig.text(660, 300, "Decoder", 16, anchor="start", weight="bold")
    fig.text(660, 450, "N x", 15, MUTED, "start")

    fig.arrow([(dec, 288), (dec, 252)])
    fig.box(dec, 235, "Linear", LEARNED)
    fig.arrow([(dec, 218), (dec, 202)])
    fig.box(dec, 185, "Softmax", FIXED)
    fig.arrow([(dec, 168), (dec, 148)])
    fig.box(dec, 130, "Output Probabilities", OUTPUT)
    return fig.svg()


def smiley(size: int) -> list[list[float]]:
    """A small test image with values in [-1, 1]."""
    rows = []
    for j in range(size):
        y = (j + 0.5) / size * 2 - 1
        row = []
        for i in range(size):
            x = (i + 0.5) / size * 2 - 1
            r = math.hypot(x, y)
            on = abs(r - 0.82) < 0.09
            on = on or math.hypot(abs(x) - 0.32, y + 0.28) < 0.13
            on = on or (abs(math.hypot(x, y - 0.02) - 0.5) < 0.08 and y > 0.2)
            row.append(-1.0 if on else 1.0)
        rows.append(row)
    return rows


def noised(x0: list[list[float]], t: int, rng: random.Random, steps: int = 1000) -> list[list[tuple[int, int, int]]]:
    """DDPM forward process: x_t = sqrt(abar_t) x_0 + sqrt(1 - abar_t) eps, linear beta schedule."""
    abar = 1.0
    for s in range(1, t + 1):
        abar *= 1 - (1e-4 + (0.02 - 1e-4) * (s - 1) / (steps - 1))
    rows = []
    for row in x0:
        px = []
        for v in row:
            value = math.sqrt(abar) * v + math.sqrt(1 - abar) * rng.gauss(0, 1)
            level = round(255 * min(1.0, max(0.0, (value + 1) / 2)))
            px.append((level, level, level))
        rows.append(px)
    return rows


def diffusion() -> str:
    fig = Fig(920, 390, "The diffusion chain", "Probabilistic", [
        "In this grammar a circle is a random variable and an arrow is a conditional distribution.",
        "Tiles use the DDPM noising formula at t = 1000, 300, 200, 0: far apart, so the change is visible.",
    ])
    rng, x0 = random.Random(0), smiley(32)
    left, right = 340.0, 580.0
    nodes = [(120.0, "T", 1000), (left, "t", 300), (right, "t-1", 200), (800.0, "0", 0)]
    y, tile = 130.0, 96.0
    for x, name, t in nodes:
        fig.circle(x, y, 28, DATA)
        fig.text(x - 2, y + 5, "x", 18, sub=name)
        fig.image(x - tile / 2, 182, tile, tile, noised(x0, t, rng))
    for a, b in ((120.0, left), (right, 800.0)):
        fig.arrow([(a + 34, y), (a + 76, y)], LEARNED[0], 2.0)
        fig.text((a + b) / 2, y + 6, ". . .", 20, MUTED)
        fig.arrow([(b - 76, y), (b - 34, y)], LEARNED[0], 2.0)
    mid = (left + right) / 2
    fig.arrow([(left + 30, y - 10), (right - 30, y - 10)], LEARNED[0], 2.2)
    fig.text(mid, y - 20, "p: learned, removes noise", 13, LEARNED[0], weight="bold")
    fig.arrow([(right - 30, y + 10), (left + 30, y + 10)], FIXED[0], 2.2, "6 4")
    fig.text(mid, y + 30, "q: fixed, adds noise", 13, FIXED[0], weight="bold")
    fig.text(120, 304, "pure noise", 14, MUTED)
    fig.text(800, 304, "image", 14, MUTED)
    return fig.svg()


def diverging(v: float) -> tuple[int, int, int]:
    """Blue (-1) through white (0) to orange (+1)."""
    far = (208, 112, 26) if v >= 0 else (31, 95, 139)
    return tuple(round(255 + (c - 255) * abs(v)) for c in far)  # type: ignore[return-value]


def positional_encoding() -> str:
    fig = Fig(820, 480, "Positional encoding", "Plot", [
        "In this grammar the axes carry the data. Computed from PE(pos, 2i) = sin(pos / 10000^(2i/d)),",
        "PE(pos, 2i+1) = cos(same), with d = 128. Each row is the fingerprint of one position.",
    ])
    d, positions = 128, 64
    rows = []
    for pos in range(positions):
        row = []
        for k in range(d):
            angle = pos / 10000 ** ((k - k % 2) / d)
            row.append(diverging(math.sin(angle) if k % 2 == 0 else math.cos(angle)))
        rows.append(row)
    x, y, w, h = 84.0, 74.0, 576.0, 288.0
    fig.image(x, y, w, h, rows)
    for pos in (0, 16, 32, 48, 63):
        fig.text(x - 8, y + (pos + 0.5) / positions * h + 4, str(pos), 12, MUTED, "end")
    for k in (0, 32, 64, 96, 127):
        fig.text(x + (k + 0.5) / d * w, y + h + 18, str(k), 12, MUTED)
    fig.text(x + w / 2, y + h + 38, "embedding dimension", 14)
    fig.add(f'<text transform="translate(34 {y + h / 2:g}) rotate(-90)" font-size="14" fill="{INK}"'
            ' text-anchor="middle">position in the sequence</text>')
    bar = [[diverging(1 - 2 * j / 99)] for j in range(100)]
    fig.image(x + w + 34, y, 18, h, bar)
    fig.text(x + w + 60, y + 10, "+1", 12, MUTED, "start")
    fig.text(x + w + 60, y + h / 2 + 4, "0", 12, MUTED, "start")
    fig.text(x + w + 60, y + h, "-1", 12, MUTED, "start")
    return fig.svg()


FIGURES: dict[str, Callable[[], str]] = {
    "mlp": mlp,
    "lenet-5": lenet,
    "positional-encoding": positional_encoding,
    "transformer": transformer,
    "diffusion-chain": diffusion,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail if any figure is stale")
    args = parser.parse_args()
    wanted = {f"{name}.svg": make() for name, make in FIGURES.items()}
    if args.check:
        on_disk = {p.name for p in FIG_DIR.glob("*.svg")}
        if on_disk != set(wanted):
            die(f"{FIG_DIR} differs from FIGURES: {sorted(on_disk ^ set(wanted))}")
        stale = [name for name, text in wanted.items() if (FIG_DIR / name).read_text() != text]
        if stale:
            die(f"stale - rerun tools/build_figures.py: {', '.join(stale)}")
        print(f"{FIG_DIR}: up to date")
        return
    FIG_DIR.mkdir(exist_ok=True)
    for path in FIG_DIR.glob("*.svg"):
        path.unlink()
    for name, text in wanted.items():
        (FIG_DIR / name).write_text(text)
    print(f"Wrote {len(wanted)} figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
