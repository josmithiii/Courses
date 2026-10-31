#!/usr/bin/env python3
"""Generate the course's own diagrams as SVG files in ai-foundations/figures/.

All figures share one visual language, so a color or shape means the same thing
everywhere. Figures are computed where they can be: the heatmap and the noise tiles
come from the published formulas, not from drawing. Text never goes below TEXT, and
text that would leave the canvas or its box fails the build. gallery.html shows every
figure with a size slider, since a Markdown image can't offer one. Standard library only.

    tools/build_figures.py           # rewrite the figures
    tools/build_figures.py --check   # exit 1 if anything is stale
"""

from __future__ import annotations

import argparse
import base64
import math
import random
import re
import struct
import sys
import zlib
from collections.abc import Callable
from pathlib import Path
from typing import NoReturn
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / "ai-foundations/figures"
GALLERY = "gallery.html"

FONT = "Helvetica, Arial, sans-serif"
TEXT = 21  # the minimum text size; no figure goes below this
TITLE = 26
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


def text_width(s: str, size: int, bold: bool = False) -> float:
    """Estimated rendered width: Helvetica averages about half an em per character."""
    return len(s) * size * (0.55 if bold else 0.5)


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

    def text(self, x: float, y: float, s: str, color: str = INK, anchor: str = "middle",
             weight: str = "normal", sub: str = "", size: int = TEXT) -> None:
        if size < TEXT:
            die(f"'{s}' is {size}, below the minimum of {TEXT}")
        width = text_width(s + sub, size, weight == "bold")
        left = {"start": x, "middle": x - width / 2, "end": x - width}[anchor]
        if left < 0 or left + width > self.width:
            die(f"{self.title}: '{s}' leaves the canvas ({left:g} to {left + width:g} of {self.width})")
        tail = (f'<tspan dy="4" font-size="{max(TEXT, size - 3)}">{escape(sub)}</tspan>' if sub else "")
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
        angle, head = math.atan2(y1 - y0, x1 - x0), 10.0
        base = (x1 - head * math.cos(angle), y1 - head * math.sin(angle))
        self.line((x0, y0), base, color, width, dash)
        wings = [(x1 - head * math.cos(angle + s * 0.42), y1 - head * math.sin(angle + s * 0.42)) for s in (1, -1)]
        corners = " ".join(f"{x:g},{y:g}" for x, y in [(x1, y1), *wings])
        self.add(f'<polygon points="{corners}" fill="{color}"/>')

    def box(self, cx: float, cy: float, label: str, kind: tuple[str, str], w: float = 250, h: float = 42) -> None:
        stroke, fill = kind
        if text_width(label, TEXT) > w - 12:
            die(f"'{label}' doesn't fit a box {w:g} wide")
        self.add(f'<rect x="{cx - w / 2:g}" y="{cy - h / 2:g}" width="{w:g}" height="{h:g}" rx="5"'
                 f' fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.text(cx, cy + 7, label)

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
        pill = text_width(self.grammar, TEXT) + 30
        if 24 + text_width(self.title, TITLE, True) > self.width - pill - 32:
            die(f"title '{self.title}' runs into the grammar label")
        head = [
            f'<rect width="{self.width}" height="{self.height}" rx="10" fill="#ffffff"/>',
            f'<text x="24" y="42" font-size="{TITLE}" font-weight="bold" fill="{INK}">{escape(self.title)}</text>',
            f'<rect x="{self.width - pill - 20:g}" y="16" width="{pill:g}" height="36" rx="18" fill="#f1f3f6" stroke="{EDGE}"/>',
            f'<text x="{self.width - 20 - pill / 2:g}" y="41" font-size="{TEXT}" fill="{MUTED}" text-anchor="middle">{escape(self.grammar)}</text>',
        ]
        y0 = self.height - 16 - 27 * (len(self.legend) - 1)
        for line in self.legend:
            if 24 + text_width(line, TEXT) > self.width - 24:
                die(f"{self.title}: legend line too wide: '{line}'")
        foot = [f'<text x="24" y="{y0 + 27 * i}" font-size="{TEXT}" fill="{MUTED}">{escape(line)}</text>'
                for i, line in enumerate(self.legend)]
        body = "\n".join(head + self.parts + foot)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}"'
                f' width="{self.width}" height="{self.height}" font-family="{FONT}">\n{body}\n</svg>\n')


def mlp() -> str:
    fig = Fig(960, 480, "Multi-layer perceptron", "Graph", [
        "In this grammar a circle is one number and a line is one weight.",
    ])
    columns = [(220.0, [165.0, 235.0, 305.0], DATA, "input"),
               (420.0, [130.0, 200.0, 270.0, 340.0], LEARNED, "hidden"),
               (620.0, [200.0, 270.0], OUTPUT, "output")]
    for (x0, ys0, _, _), (x1, ys1, _, _) in zip(columns, columns[1:]):
        for y0 in ys0:
            for y1 in ys1:
                fig.line((x0, y0), (x1, y1))
    start, end = (220.0, 305.0), (420.0, 340.0)
    fig.line(start, end, LEARNED[0], 3.5)
    for x, ys, kind, label in columns:
        fig.text(x, 92, label, MUTED)
        for y in ys:
            fig.circle(x, y, 20, kind)
    mid = (320.0, 322.5)
    fig.line(mid, (320.0, 382.0), LEARNED[0], 1.2, "3 3")
    fig.text(320, 406, "one line = one weight", LEARNED[0], weight="bold")
    fig.line((640.0, 200.0), (668.0, 176.0), OUTPUT[0], 1.2, "3 3")
    fig.text(672, 172, "one circle = one number", OUTPUT[0], "start", "bold")
    return fig.svg()


def lenet() -> str:
    fig = Fig(1000, 500, "LeNet-5", "Slab", [
        "In this grammar a block is a tensor and the gap between blocks is an operation.",
        "6@28x28 means 6 feature maps, each 28 by 28. Plane sizes are drawn to scale.",
    ])
    cell, cy, gap = 3.3, 205.0, 62.0
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
        fig.text(x + (side + depth) / 2, top - depth - 12, label)
        x += side + depth
        right_edges.append(x)
        x += gap
    for label, n in (("120", 120), ("84", 84), ("10", 10)):
        height = 40 + 1.6 * n
        lefts.append(x)
        fig.plane(x, cy - height / 2, 16, height, LEARNED if n != 10 else OUTPUT)
        fig.text(x + 8, cy - height / 2 - 12, label)
        x += 16
        right_edges.append(x)
        x += gap
    for i, op in enumerate(ops):
        a, b = right_edges[i], lefts[i + 1]
        mid, row = (a + b) / 2, 362.0 + 30 * (i % 2)  # staggered, so wide labels can't collide
        fig.arrow([(a + 5, cy), (b - 5, cy)])
        fig.line((mid, cy + 8), (mid, row - 20), EDGE, 1.0, "2 3")
        fig.text(mid, row, op, (FIXED if op == "subsample" else LEARNED)[0])
    return fig.svg()


def transformer() -> str:
    fig = Fig(930, 975, "The Transformer", "Block", [
        "In this grammar a box is an operation and an arrow carries a whole tensor.",
        "Read bottom to top. Orange has trained weights; gray does not.",
    ])
    enc, dec, half, side = 300.0, 690.0, 21.0, 125.0

    def frame(left: float, top: float, right: float, bottom: float) -> None:
        fig.add(f'<rect x="{left:g}" y="{top:g}" width="{right - left:g}" height="{bottom - top:g}" rx="10"'
                f' fill="none" stroke="{EDGE}" stroke-width="1.5" stroke-dasharray="6 5"/>')

    def up(cx: float, lower: float, upper: float) -> None:
        """Arrow from the top of the box at y=lower to the bottom of the box at y=upper."""
        fig.arrow([(cx, lower - half), (cx, upper + half)])

    def skip(cx: float, out: float, y_from: float, y_to: float) -> None:
        """Residual arrow around a sublayer, entering the Add & Norm box at y_to."""
        edge = cx + (side if out > cx else -side)
        fig.arrow([(cx, y_from), (out, y_from), (out, y_to), (edge, y_to)], MUTED, 1.4)

    def embed(cx: float, name: str, label: str) -> None:
        fig.text(cx, 898, label, DATA[0], weight="bold")
        fig.arrow([(cx, 876), (cx, 853)])
        fig.box(cx, 830, name, LEARNED)
        fig.arrow([(cx, 809), (cx, 776)])
        fig.circle(cx, 760, 15, FIXED)
        fig.text(cx, 767, "+")

    frame(138, 405, 445, 722)
    frame(542, 275, 855, 742)
    embed(enc, "Input Embedding", "Inputs")
    embed(dec, "Output Embedding", "Outputs (shifted right)")
    fig.text(enc - 24, 767, "positional encoding", FIXED[0], "end")
    fig.text(dec + 24, 767, "positional encoding", FIXED[0], "start")

    # Encoder, bottom to top.
    fig.arrow([(enc, 745), (enc, 660 + half)])
    fig.box(enc, 660, "Multi-Head Attention", LEARNED)
    skip(enc, 155, 702, 590)
    up(enc, 660, 590)
    fig.box(enc, 590, "Add & Norm", FIXED)
    up(enc, 590, 510)
    fig.box(enc, 510, "Feed Forward", LEARNED)
    skip(enc, 155, 550, 440)
    up(enc, 510, 440)
    fig.box(enc, 440, "Add & Norm", FIXED)

    # Decoder, bottom to top.
    fig.arrow([(dec, 745), (dec, 685 + half)])
    fig.box(dec, 685, "Masked Multi-Head Attn", LEARNED)
    skip(dec, 837, 726, 615)
    up(dec, 685, 615)
    fig.box(dec, 615, "Add & Norm", FIXED)
    up(dec, 615, 535)
    fig.text(dec - 10, 585, "Q", MUTED, "end")
    fig.box(dec, 535, "Multi-Head Attention", LEARNED)
    skip(dec, 837, 575, 465)
    up(dec, 535, 465)
    fig.box(dec, 465, "Add & Norm", FIXED)
    up(dec, 465, 385)
    fig.box(dec, 385, "Feed Forward", LEARNED)
    skip(dec, 837, 425, 315)
    up(dec, 385, 315)
    fig.box(dec, 315, "Add & Norm", FIXED)

    # Cross-attention: encoder output into the decoder.
    fig.arrow([(enc, 440 - half), (enc, 370), (470, 370), (470, 535), (dec - side, 535)], DATA[0], 2.2)
    fig.text(478, 526, "K, V", DATA[0], "start")
    fig.text(enc, 356, "Encoder", weight="bold")
    fig.text(125, 570, "N x", MUTED, "end")
    fig.text(826, 263, "Decoder", anchor="start", weight="bold")
    fig.text(868, 515, "N x", MUTED, "start")

    up(dec, 315, 235)
    fig.box(dec, 235, "Linear", LEARNED)
    up(dec, 235, 165)
    fig.box(dec, 165, "Softmax", FIXED)
    up(dec, 165, 95)
    fig.box(dec, 95, "Output Probabilities", OUTPUT)
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
    fig = Fig(960, 450, "The diffusion chain", "Probabilistic", [
        "A circle is a random variable; an arrow is a conditional distribution.",
        "Tiles: DDPM noising formula at t = 1000, 300, 200, 0, spaced so change shows.",
    ])
    rng, x0 = random.Random(0), smiley(32)
    left, right = 300.0, 660.0
    nodes = [(100.0, "T", 1000), (left, "t", 300), (right, "t-1", 200), (860.0, "0", 0)]
    y, tile, r = 140.0, 110.0, 32.0
    for x, name, t in nodes:
        fig.circle(x, y, r, DATA)
        fig.text(x - 2, y + 6, "x", sub=name, size=24)
        fig.image(x - tile / 2, 202, tile, tile, noised(x0, t, rng))
    for a, b in ((100.0, left), (right, 860.0)):
        fig.arrow([(a + r + 5, y), (a + r + 42, y)], LEARNED[0], 2.0)
        fig.text((a + b) / 2, y + 7, ". . .", MUTED)
        fig.arrow([(b - r - 42, y), (b - r - 5, y)], LEARNED[0], 2.0)
    mid = (left + right) / 2
    fig.arrow([(left + r + 4, y - 11), (right - r - 4, y - 11)], LEARNED[0], 2.2)
    fig.text(mid, y - 22, "p: learned, removes noise", LEARNED[0], weight="bold")
    fig.arrow([(right - r - 4, y + 11), (left + r + 4, y + 11)], FIXED[0], 2.2, "6 4")
    fig.text(mid, y + 38, "q: fixed, adds noise", FIXED[0], weight="bold")
    fig.text(100, 340, "pure noise", MUTED)
    fig.text(860, 340, "image", MUTED)
    return fig.svg()


def diverging(v: float) -> tuple[int, int, int]:
    """Blue (-1) through white (0) to orange (+1)."""
    far = (208, 112, 26) if v >= 0 else (31, 95, 139)
    return tuple(round(255 + (c - 255) * abs(v)) for c in far)  # type: ignore[return-value]


def positional_encoding() -> str:
    fig = Fig(880, 530, "Positional encoding", "Plot", [
        "The axes carry the data. Each row is the fingerprint of one position.",
        "PE(pos, 2i) = sin(pos / 10000^(2i/d)); PE(pos, 2i+1) = cos(same); d = 128.",
    ])
    d, positions = 128, 64
    rows = []
    for pos in range(positions):
        row = []
        for k in range(d):
            angle = pos / 10000 ** ((k - k % 2) / d)
            row.append(diverging(math.sin(angle) if k % 2 == 0 else math.cos(angle)))
        rows.append(row)
    x, y, w, h = 110.0, 74.0, 576.0, 288.0
    fig.image(x, y, w, h, rows)
    for pos in (0, 32, 63):
        fig.text(x - 10, y + (pos + 0.5) / positions * h + 7, str(pos), MUTED, "end")
    for k in (0, 32, 64, 96, 127):
        fig.text(x + (k + 0.5) / d * w, y + h + 26, str(k), MUTED)
    fig.text(x + w / 2, y + h + 56, "embedding dimension")
    fig.add(f'<text transform="translate(44 {y + h / 2:g}) rotate(-90)" font-size="{TEXT}" fill="{INK}"'
            ' text-anchor="middle">position in the sequence</text>')
    bar = [[diverging(1 - 2 * j / 99)] for j in range(100)]
    fig.image(x + w + 30, y, 20, h, bar)
    fig.text(x + w + 58, y + 16, "+1", MUTED, "start")
    fig.text(x + w + 58, y + h / 2 + 7, "0", MUTED, "start")
    fig.text(x + w + 58, y + h, "-1", MUTED, "start")
    return fig.svg()


FIGURES: dict[str, Callable[[], str]] = {
    "mlp": mlp,
    "lenet-5": lenet,
    "positional-encoding": positional_encoding,
    "transformer": transformer,
    "diffusion-chain": diffusion,
}


def gallery(svgs: dict[str, str]) -> str:
    """A local page showing every figure, with a size slider remembered per browser."""
    cards = []
    for name, text in svgs.items():
        width = re.search(r'viewBox="0 0 (\d+) ', text).group(1)
        cards.append(f'<figure><a href="{name}"><img src="{name}" alt="{name}" style="--w:{width}"></a>'
                     f"<figcaption>{name}</figcaption></figure>")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Foundations Figures</title>
<style>
:root {{ --scale:1; color-scheme:light dark; }}
body {{ margin:0; padding:16px 24px; background:#e9e7e1; color:#23262b; font:17px -apple-system, Helvetica, sans-serif; }}
header {{ position:sticky; top:0; background:#e9e7e1; padding:10px 0; display:flex; gap:14px; align-items:center; flex-wrap:wrap; }}
header strong {{ margin-right:auto; }}
input {{ width:min(280px, 60vw); }}
figure {{ margin:22px 0; overflow-x:auto; }}
img {{ display:block; width:calc(var(--w) * var(--scale) * 1px); }}
figcaption {{ margin-top:6px; color:#667080; font-size:15px; }}
</style></head><body>
<header><strong>AI Foundations figures</strong>
<label for="size">Size</label><input id="size" type="range" min="50" max="300" step="10" value="100">
<output id="value" for="size">100%</output></header>
{"".join(cards)}
<script>
const size = document.getElementById("size"), value = document.getElementById("value");
function apply(percent) {{
  size.value = percent;
  value.textContent = percent + "%";
  document.documentElement.style.setProperty("--scale", percent / 100);
}}
try {{ const saved = localStorage.getItem("figure-scale"); if (saved) apply(saved); }} catch (e) {{}}
size.addEventListener("input", () => {{
  apply(size.value);
  try {{ localStorage.setItem("figure-scale", size.value); }} catch (e) {{}}
}});
</script>
</body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail if anything is stale")
    args = parser.parse_args()
    wanted = {f"{name}.svg": make() for name, make in FIGURES.items()}
    page = gallery(wanted)
    if args.check:
        on_disk = {p.name for p in FIG_DIR.glob("*.svg")}
        if on_disk != set(wanted):
            die(f"{FIG_DIR} differs from FIGURES: {sorted(on_disk ^ set(wanted))}")
        stale = [name for name, text in {**wanted, GALLERY: page}.items() if (FIG_DIR / name).read_text() != text]
        if stale:
            die(f"stale - rerun tools/build_figures.py: {', '.join(stale)}")
        print(f"{FIG_DIR}: up to date")
        return
    FIG_DIR.mkdir(exist_ok=True)
    for path in FIG_DIR.glob("*.svg"):
        path.unlink()
    for name, text in {**wanted, GALLERY: page}.items():
        (FIG_DIR / name).write_text(text)
    print(f"Wrote {len(wanted)} figures and {GALLERY} to {FIG_DIR}")


if __name__ == "__main__":
    main()
