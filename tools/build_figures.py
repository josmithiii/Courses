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

    def polyline(self, points: list[Point], color: str, width: float = 2.4, dash: str = "") -> None:
        dashed = f' stroke-dasharray="{dash}"' if dash else ""
        corners = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.add(f'<polyline points="{corners}" fill="none" stroke="{color}" stroke-width="{width:g}"'
                 f' stroke-linejoin="round"{dashed}/>')

    def polygon(self, points: list[Point], fill: str, stroke: str = EDGE, width: float = 1.0) -> None:
        corners = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.add(f'<polygon points="{corners}" fill="{fill}" stroke="{stroke}" stroke-width="{width:g}"/>')

    def outline(self, x: float, y: float, w: float, h: float, color: str = EDGE, width: float = 1.5,
                dash: str = "6 5", rx: float = 10) -> None:
        dashed = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="none"'
                 f' stroke="{color}" stroke-width="{width:g}"{dashed}/>')

    def rotated(self, x: float, y: float, s: str, color: str = INK) -> None:
        """Text reading upward, centered on (x, y)."""
        self.add(f'<text transform="translate({x:g} {y:g}) rotate(-90)" font-size="{TEXT}" fill="{color}"'
                 f' text-anchor="middle">{escape(s)}</text>')

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
        # An inline style, not a font-family attribute: Emacs gives every SVG a stylesheet
        # naming its default font, which outranks an attribute but not an inline style.
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}"'
                f' width="{self.width}" height="{self.height}" style="font-family:{FONT}">\n{body}\n</svg>\n')


def neuron() -> str:
    fig = Fig(960, 420, "Artificial neuron", "Graph", [
        "The usual single circle hides two steps: a weighted sum, then a bend.",
    ])
    cy, sum_x, r = 215.0, 440.0, 62.0
    for i, y in enumerate((125.0, 215.0, 305.0), 1):
        fig.line((136, y), (sum_x - r * 0.92, cy + (y - cy) * 0.25), LEARNED[0], 2.0)
        fig.circle(110, y, 26, DATA)
        fig.text(108, y + 7, "x", sub=str(i), size=24)
        fig.text(262, cy + (y - cy) * 0.62 - 12, "w", LEARNED[0], sub=str(i), size=24)
    fig.outline(358, 120, 382, 190)
    fig.text(549, 106, "one neuron: two steps", MUTED)
    fig.circle(sum_x, cy, r, LEARNED)
    fig.text(sum_x, cy + 7, "sum + b")
    fig.arrow([(sum_x + r + 2, cy), (574, cy)])
    fig.box(650, cy, "activation", FIXED, w=150, h=56)
    fig.arrow([(727, cy), (802, cy)])
    fig.circle(830, cy, 26, OUTPUT)
    fig.text(830, cy + 8, "y", size=24)
    return fig.svg()


def activation_functions() -> str:
    fig = Fig(980, 450, "Activation functions", "Plot", [
        "Across: the neuron's weighted sum. Up: its output. The bend is the point.",
    ])
    panels: list[tuple[float, str, Callable[[float], float], float, float]] = [
        (60.0, "sigmoid", lambda s: 1 / (1 + math.exp(-s)), -0.25, 1.25),
        (375.0, "tanh", math.tanh, -1.25, 1.25),
        (690.0, "ReLU", lambda s: max(0.0, s), -1.0, 5.0),
    ]
    top, w, h = 104.0, 250.0, 240.0
    for x0, name, f, low, high in panels:
        def px(s: float) -> float:
            return x0 + (s + 5) / 10 * w

        def py(v: float) -> float:
            return top + (high - v) / (high - low) * h

        fig.outline(x0, top, w, h, EDGE, 1.2, "", 0)
        fig.line((x0, py(0)), (x0 + w, py(0)), EDGE, 1.2)
        fig.line((px(0), top), (px(0), top + h), EDGE, 1.2)
        fig.polyline([(px(s / 10), py(f(s / 10))) for s in range(-50, 51)], LEARNED[0], 3.0)
        fig.text(x0 + w / 2, top - 14, name, weight="bold")
        for s in (-5, 0, 5):
            fig.text(px(s), top + h + 28, str(s), MUTED)
        fig.text(x0 - 8, py(1) + 7, "1", MUTED, "end")
    return fig.svg()


def loss_landscape() -> str:
    fig = Fig(900, 550, "Loss landscape and gradient descent", "Plot", [
        "Axes are weights, not inputs. Contours mark equal loss; darkest is lowest.",
        "Both paths are computed gradient descent on a real quadratic loss.",
    ])
    a, b = 1.0, 12.0
    x, y, w, h = 80.0, 76.0, 540.0, 360.0

    def loss(w1: float, w2: float) -> float:
        return 0.5 * (a * w1 * w1 + b * w2 * w2)

    def px(w1: float) -> float:
        return x + (w1 + 3) / 6 * w

    def py(w2: float) -> float:
        return y + (2 - w2) / 4 * h

    def color(value: float) -> tuple[int, int, int]:
        band = min(1.0, int(math.sqrt(value) * 3) / 12)
        return tuple(round(c + (255 - c) * band) for c in (112, 165, 200))  # type: ignore[return-value]

    columns, lines = 270, 180
    fig.image(x, y, w, h, [[color(loss(-3 + 6 * (i + 0.5) / columns, 2 - 4 * (j + 0.5) / lines))
                            for i in range(columns)] for j in range(lines)])

    def descend(rate: float) -> list[Point]:
        w1, w2 = -2.7, 1.1
        path = [(px(w1), py(w2))]
        for _ in range(60):
            w1, w2 = w1 - rate * a * w1, w2 - rate * b * w2
            path.append((px(w1), py(w2)))
        return path

    fig.polyline(descend(0.155), LEARNED[0], 2.6)
    fig.polyline(descend(0.03), INK, 3.0)
    fig.circle(px(-2.7), py(1.1), 7, (INK, "#ffffff"))
    fig.text(x + w / 2, y + h + 30, "weight 1")
    fig.rotated(44, y + h / 2, "weight 2")
    fig.text(636, 200, "rate 0.03:", INK, "start", "bold")
    fig.text(636, 228, "smooth descent", INK, "start")
    fig.text(636, 290, "rate 0.155:", LEARNED[0], "start", "bold")
    fig.text(636, 318, "zig-zags across", LEARNED[0], "start")
    fig.text(636, 346, "the valley", LEARNED[0], "start")
    return fig.svg()


def computational_graph() -> str:
    w, x, t = 2.0, 3.0, 5.0
    y, e = w * x, w * x - t
    loss, dl_de = e * e, 2 * e
    dl_dy, dl_dw = dl_de, dl_de * x
    fig = Fig(1000, 430, "Computational graph and backpropagation", "Block", [
        "Black arrows carry values forward; orange arrows carry gradients back.",
        "Computed for L = (w*x - t)^2. The backward pass is the same graph in reverse.",
    ])
    row, fwd, back = 190.0, 176.0, 204.0
    fig.circle(100, 122, 32, DATA)
    fig.text(100, 130, f"w={w:g}")
    fig.circle(100, 262, 32, DATA)
    fig.text(100, 270, f"x={x:g}")
    centers = (300.0, 530.0, 760.0)
    for cx, label in zip(centers, ("multiply", f"subtract {t:g}", "square")):
        fig.box(cx, row, label, FIXED, w=130, h=64)
    fig.arrow([(132, 122), (232, fwd - 8)], INK)
    fig.arrow([(132, 262), (232, row + 20)], INK)
    fig.arrow([(235, fwd + 6), (132, 134)], LEARNED[0], 2.2, "6 4")
    forward = [(365.0, 465.0, f"y = {y:g}"), (595.0, 695.0, f"e = {e:g}"), (825.0, 892.0, f"L = {loss:g}")]
    for a, b, label in forward:
        fig.arrow([(a, fwd), (b, fwd)], INK)
        fig.text((a + b) / 2, fwd - 14, label)
    backward = [(892.0, 825.0, "start: 1"), (695.0, 595.0, f"dL/de = {dl_de:g}"), (465.0, 365.0, f"dL/dy = {dl_dy:g}")]
    for a, b, label in backward:
        fig.arrow([(a, back), (b, back)], LEARNED[0], 2.2, "6 4")
        fig.text((a + b) / 2, back + 56, label, LEARNED[0], weight="bold")
    fig.circle(922, row, 28, OUTPUT)
    fig.text(922, row + 8, "L")
    fig.text(186, 118, f"dL/dw = {dl_dw:g}", LEARNED[0], "start", "bold")
    return fig.svg()


def learning_curves() -> str:
    fig = Fig(860, 450, "Learning curves and overfitting", "Plot", [
        "Illustrative curves, not a real run. The widening gap is the symptom.",
    ])
    x0, y0, w, h = 90.0, 70.0, 700.0, 280.0

    def train(s: float) -> float:
        return 0.06 + 0.85 * math.exp(-4 * s)

    def val(s: float) -> float:
        return 0.2 + 0.75 * math.exp(-5 * s) + 0.5 * s * s

    def point(s: float, v: float) -> Point:
        return (x0 + s * w, y0 + (1 - v) * h)

    times = [i / 100 for i in range(101)]
    best = min(times, key=val)
    fig.line((x0, y0), (x0, y0 + h), MUTED, 1.5)
    fig.line((x0, y0 + h), (x0 + w, y0 + h), MUTED, 1.5)
    fig.line(point(best, 1.0), point(best, 0.0), FIXED[0], 1.5, "4 4")
    fig.polyline([point(s, train(s)) for s in times], DATA[0], 3.2)
    fig.polyline([point(s, val(s)) for s in times], LEARNED[0], 3.2)
    fig.text(point(best, 0)[0] + 8, y0 + 22, "early stopping here", FIXED[0], "start")
    fig.text(x0 + w, point(1, val(1))[1] - 12, "validation", LEARNED[0], "end", "bold")
    fig.text(x0 + w, point(1, train(1))[1] - 12, "training", DATA[0], "end", "bold")
    fig.text(x0 + w / 2, y0 + h + 30, "epochs")
    fig.rotated(52, y0 + h / 2, "loss")
    return fig.svg()


def dropout() -> str:
    fig = Fig(980, 460, "Dropout", "Graph", [
        "Crossed-out units are off for this batch only. At test time all are on.",
    ])
    sizes = (3, 4, 4, 2)

    def network(x0: float, title: str, off: set[tuple[int, int]]) -> None:
        nodes = [[(x0 + c * 130, 245 + (r - (n - 1) / 2) * 72) for r in range(n)] for c, n in enumerate(sizes)]
        for c in range(len(sizes) - 1):
            for r0, a in enumerate(nodes[c]):
                for r1, b in enumerate(nodes[c + 1]):
                    if (c, r0) not in off and (c + 1, r1) not in off:
                        fig.line(a, b)
        kinds = (DATA, LEARNED, LEARNED, OUTPUT)
        for c, column in enumerate(nodes):
            for r, (x, y) in enumerate(column):
                dead = (c, r) in off
                fig.circle(x, y, 19, (EDGE, "#f4f5f7") if dead else kinds[c])
                if dead:
                    fig.line((x - 13, y - 13), (x + 13, y + 13), FIXED[0], 2.2)
                    fig.line((x - 13, y + 13), (x + 13, y - 13), FIXED[0], 2.2)
        fig.text(x0 + 195, 92, title, weight="bold")

    network(84, "full network", set())
    network(536, "thinned for one batch", {(0, 1), (1, 1), (1, 3), (2, 0), (2, 2)})
    return fig.svg()


def number_grid(fig: Fig, x: float, y: float, cell: float, values: list[list[int]],
                fill: Callable[[int, int], str] = lambda r, c: DATA[1]) -> None:
    """A table of numbers, one square cell per entry."""
    for r, row in enumerate(values):
        for c, value in enumerate(row):
            fig.plane(x + c * cell, y + r * cell, cell, cell, (DATA[0], fill(r, c)))
            fig.text(x + (c + 0.5) * cell, y + (r + 0.5) * cell + 7, str(value))


def blank_grid(fig: Fig, x: float, y: float, cell: float, rows: int, columns: int,
               kind: tuple[str, str] = DATA) -> None:
    for r in range(rows):
        for c in range(columns):
            fig.plane(x + c * cell, y + r * cell, cell, cell, kind)


def rgb_channels() -> str:
    fig = Fig(800, 390, "An image as a tensor", "Slab", [
        "Pictures usually show height x width x channels.",
        "PyTorch stores channels x height x width.",
    ])
    size = 16

    def pixel(r: int, c: int) -> tuple[int, int, int]:
        if math.hypot(r - 5, c - 10) < 3.4:
            return (250, 205, 70)
        if r > 10:
            return (60 + 6 * c, 150, 80)
        return (120, 170 + 3 * r, 235)

    rows = [[pixel(r, c) for c in range(size)] for r in range(size)]
    y, tile = 130.0, 150.0
    fig.image(40, y, tile, tile, rows)
    fig.text(40 + tile / 2, y - 14, "image", weight="bold")
    fig.arrow([(200, y + tile / 2), (236, y + tile / 2)])
    names = ("red", "green", "blue")
    for k, name in enumerate(names):
        x = 246 + k * 180 - k * 8
        mono = [[tuple(px[k] if i == k else 0 for i in range(3)) for px in row] for row in rows]
        fig.image(x, y, tile, tile, mono)
        fig.text(x + tile / 2, y - 14, name, weight="bold")
    return fig.svg()


def convolution() -> str:
    image = [[3, 1, 0, 2], [2, 5, 1, 1], [0, 4, 2, 3], [1, 0, 3, 1]]
    kernel = [[1, 0], [0, -1]]
    output = [[sum(image[r + i][c + j] * kernel[i][j] for i in range(2) for j in range(2))
               for c in range(3)] for r in range(3)]
    fig = Fig(900, 410, "Convolution", "Slab", [
        "Slide the kernel: at each stop, multiply overlapping numbers and add.",
        "3*1 + 1*0 + 2*0 + 5*(-1) = -2 at the top left. The kernel is not flipped.",
    ])
    cell, top = 58.0, 88.0
    middle = top + 2 * cell
    number_grid(fig, 50, top, cell, image, lambda r, c: LEARNED[1] if r < 2 and c < 2 else DATA[1])
    fig.outline(50, top, 2 * cell, 2 * cell, LEARNED[0], 3.5, "", 0)
    fig.text(50 + 2 * cell, top - 12, "input", weight="bold")
    fig.text(316, middle + 8, "*", size=30)
    number_grid(fig, 350, middle - cell, cell, kernel, lambda r, c: LEARNED[1])
    fig.text(350 + cell, middle - cell - 12, "kernel", weight="bold")
    fig.text(504, middle + 8, "=", size=30)
    number_grid(fig, 546, middle - 1.5 * cell, cell, output, lambda r, c: LEARNED[1] if r == c == 0 else OUTPUT[1])
    fig.outline(546, middle - 1.5 * cell, cell, cell, LEARNED[0], 3.5, "", 0)
    fig.text(546 + 1.5 * cell, middle - 1.5 * cell - 12, "output", weight="bold")
    return fig.svg()


def stride_padding_pooling() -> str:
    fig = Fig(1000, 430, "Stride, padding and pooling", "Slab", [
        "Stride and padding set the output size. Pooling has no weights at all.",
    ])
    top, cell = 132.0, 34.0
    blank_grid(fig, 60, top, cell, 5, 5)
    fig.outline(60, top, 3 * cell, 3 * cell, LEARNED[0], 3.5, "", 0)
    fig.outline(60 + 2 * cell, top, 3 * cell, 3 * cell, FIXED[0], 3.5, "7 4", 0)
    fig.text(60 + 2.5 * cell, top - 16, "stride 2", weight="bold")
    fig.text(60 + 2.5 * cell, top + 5 * cell + 34, "window hops 2 cells", MUTED)
    small = 28.0
    x2 = 340.0
    blank_grid(fig, x2, top - small, small, 7, 7, ("#c6cdd6", "#f4f5f7"))
    blank_grid(fig, x2 + small, top, small, 5, 5)
    fig.outline(x2, top - small, 3 * small, 3 * small, LEARNED[0], 3.5, "", 0)
    fig.text(x2 + 3.5 * small, top - small - 14, "padding 1", weight="bold")
    fig.text(x2 + 3.5 * small, top + 6 * small + 34, "a border is added", MUTED)
    values = [[1, 3, 2, 1], [4, 6, 1, 0], [0, 2, 5, 7], [1, 1, 3, 2]]
    pooled = [[max(values[r + i][c + j] for i in range(2) for j in range(2)) for c in (0, 2)] for r in (0, 2)]

    def shade(r: int, c: int) -> str:
        return LEARNED[1] if r == c else FIXED[1]

    size = 42.0
    x3 = 640.0
    number_grid(fig, x3, top, size, values, lambda r, c: shade(r // 2, c // 2))
    fig.arrow([(x3 + 4 * size + 8, top + 2 * size), (x3 + 4 * size + 46, top + 2 * size)])
    number_grid(fig, x3 + 4 * size + 54, top + size, size, pooled, shade)
    fig.text(x3 + 150, top - 16, "max pool 2x2", weight="bold")
    fig.text(x3 + 150, top + 5 * 34 + 34, "keeps each maximum", MUTED)
    return fig.svg()


def receptive_field() -> str:
    fig = Fig(860, 430, "Receptive field", "Slab", [
        "Each 3x3 layer widens the view by 2, so three stacked layers see 7.",
        "One row of each layer is shown.",
    ])
    cell, height, x0 = 52.0, 34.0, 200.0
    rows = [(92.0, "layer 3", 1), (162.0, "layer 2", 3), (232.0, "layer 1", 5), (302.0, "input", 7)]
    for (y, _, seen), (y1, _, below) in zip(rows, rows[1:]):
        for side in (-1, 1):
            fig.line((x0 + (4.5 + side * seen / 2) * cell, y + height),
                     (x0 + (4.5 + side * below / 2) * cell, y1), LEARNED[0], 1.6, "5 4")
    for y, label, seen in rows:
        for c in range(9):
            on = abs(c - 4) <= seen // 2
            fig.plane(x0 + c * cell, y, cell, height, LEARNED if on else DATA)
        fig.text(x0 - 14, y + 24, label, anchor="end")
        fig.text(x0 + 9 * cell + 14, y + 24, f"{seen} cell{'s' if seen > 1 else ''}", LEARNED[0], "start")
    return fig.svg()


def alexnet_vgg() -> str:
    fig = Fig(1000, 640, "AlexNet and VGG-16", "Slab", [
        "Top numbers are image size; bottom numbers are channels or units.",
        "AlexNet's two lanes are its two GPUs. VGG just repeats plain 3x3 conv layers.",
    ])
    cy, x0, step, width = 190.0, 110.0, 96.0, 52.0
    alex: list[tuple[str, str, float, tuple[str, str]]] = [
        ("224", "3", 130, DATA), ("55", "96", 106, DATA), ("27", "256", 86, DATA), ("13", "384", 66, DATA),
        ("13", "384", 66, DATA), ("13", "256", 66, DATA), ("", "4096", 130, LEARNED), ("", "4096", 130, LEARNED),
        ("", "1000", 52, OUTPUT),
    ]
    fig.text(24, 84, "AlexNet (2012)", anchor="start", weight="bold")
    for i, (top, bottom, height, kind) in enumerate(alex):
        x = x0 + i * step
        if i in (0, len(alex) - 1):
            fig.plane(x, cy - height / 2, width, height, kind)
        else:
            fig.plane(x, cy - height / 2, width, height / 2 - 3, kind)
            fig.plane(x, cy + 3, width, height / 2 - 3, kind)
        if top:
            fig.text(x + width / 2, cy - height / 2 - 10, top)
        fig.text(x + width / 2, cy + 90, bottom, MUTED)
        if i < len(alex) - 1:
            fig.arrow([(x + width + 4, cy), (x + step - 4, cy)], MUTED, 1.4)
    fig.text(24, cy - 16, "GPU 1", MUTED, "start")
    fig.text(24, cy + 30, "GPU 2", MUTED, "start")

    cy, x = 440.0, 60.0
    fig.text(24, 330, "VGG-16 (2015)", anchor="start", weight="bold")
    groups: list[tuple[str, str, int, float]] = [
        ("224", "64 x2", 2, 130), ("112", "128 x2", 2, 110), ("56", "256 x3", 3, 90),
        ("28", "512 x3", 3, 70), ("14", "512 x3", 3, 52),
    ]
    for size, label, layers, height in groups:
        span = layers * 14 + (layers - 1) * 5
        for k in range(layers):
            fig.plane(x + k * 19, cy - height / 2, 14, height, DATA)
        fig.text(x + span / 2, cy - height / 2 - 10, size)
        fig.text(x + span / 2, cy + 92, label, MUTED)
        x += span
        fig.arrow([(x + 6, cy), (x + 66, cy)], MUTED, 1.4)
        x += 74
    for label, height, kind in (("4096", 130.0, LEARNED), ("4096", 130.0, LEARNED), ("1000", 52.0, OUTPUT)):
        fig.plane(x, cy - height / 2, 18, height, kind)
        fig.text(x + 9, cy + 92, label, MUTED)
        x += 18
        if label != "1000" or height != 52.0:
            fig.arrow([(x + 6, cy), (x + 50, cy)], MUTED, 1.4)
        x += 58
    return fig.svg()


def inception() -> str:
    fig = Fig(980, 540, "Inception module", "Block", [
        "Several filter sizes run side by side, then concatenate. Read bottom to top.",
    ])
    columns = (140.0, 370.0, 600.0, 830.0)
    w, h = 190.0, 46.0
    prev, low, high, top, source, sink = 440.0, 335.0, 230.0, 110.0, 400.0, 170.0
    fig.box(485, prev, "Previous layer", DATA, w=250, h=h)
    fig.box(485, top, "Filter concatenation", DATA, w=250, h=h)
    fig.line((485, prev - h / 2), (485, source), MUTED, 1.8)
    fig.line((columns[0], source), (columns[-1], source), MUTED, 1.8)
    fig.line((columns[0], sink), (columns[-1], sink), MUTED, 1.8)
    fig.arrow([(485, sink), (485, top + h / 2)])
    fig.arrow([(columns[0], source), (columns[0], high + h / 2)])
    fig.box(columns[0], high, "1x1 conv", LEARNED, w, h)
    for x, lower, upper, kind in ((columns[1], "1x1 conv", "3x3 conv", LEARNED),
                                  (columns[2], "1x1 conv", "5x5 conv", LEARNED),
                                  (columns[3], "3x3 max pool", "1x1 conv", FIXED)):
        fig.arrow([(x, source), (x, low + h / 2)])
        fig.box(x, low, lower, kind, w, h)
        fig.arrow([(x, low - h / 2), (x, high + h / 2)])
        fig.box(x, high, upper, LEARNED, w, h)
    for x in columns:
        fig.line((x, high - h / 2), (x, sink), MUTED, 1.8)
    return fig.svg()


def resnet_block() -> str:
    fig = Fig(760, 660, "ResNet residual block", "Block", [
        "The layers learn a correction F(x); the input is added back.",
        "Read top to bottom.",
    ])
    cx, right = 300.0, 540.0
    fig.text(cx, 76, "x", DATA[0], weight="bold", size=24)
    fig.circle(cx, 112, 6, FIXED)
    fig.arrow([(cx, 118), (cx, 150)])
    fig.box(cx, 172, "weight layer", LEARNED)
    fig.arrow([(cx, 193), (cx, 224)])
    fig.box(cx, 246, "relu", FIXED)
    fig.arrow([(cx, 267), (cx, 298)])
    fig.box(cx, 320, "weight layer", LEARNED)
    fig.arrow([(cx, 341), (cx, 396)])
    fig.circle(cx, 414, 18, FIXED)
    fig.text(cx, 421, "+")
    fig.arrow([(cx, 432), (cx, 466)])
    fig.box(cx, 488, "relu", FIXED)
    fig.arrow([(cx, 509), (cx, 544)])
    fig.text(cx, 570, "F(x) + x", OUTPUT[0], weight="bold")
    fig.text(cx - 140, 250, "F(x)", LEARNED[0], "end", "bold")
    fig.arrow([(cx + 6, 112), (right, 112), (right, 414), (cx + 18, 414)], DATA[0], 2.4)
    fig.text(right + 12, 256, "x", DATA[0], "start", "bold")
    fig.text(right + 12, 284, "(identity)", DATA[0], "start")
    return fig.svg()


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
    "neuron": neuron,
    "activation-functions": activation_functions,
    "mlp": mlp,
    "loss-landscape": loss_landscape,
    "computational-graph": computational_graph,
    "learning-curves": learning_curves,
    "dropout": dropout,
    "rgb-channels": rgb_channels,
    "convolution": convolution,
    "stride-padding-pooling": stride_padding_pooling,
    "lenet-5": lenet,
    "receptive-field": receptive_field,
    "alexnet-vgg": alexnet_vgg,
    "inception": inception,
    "resnet-block": resnet_block,
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
