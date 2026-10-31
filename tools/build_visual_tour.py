#!/usr/bin/env python3
"""Build ai-foundations/visual-tour.md from syllabus.md and the-diagram-atlas.md.

The tour walks every syllabus topic in order and annotates each atlas entry with
where to see its figure: a deep link to the PDF page, or the image itself for web
sources. Figures are linked, never copied, so the course stays Markdown-only.

    tools/build_visual_tour.py           # rewrite the tour
    tools/build_visual_tour.py --check   # exit 1 if the tour is stale
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path
from typing import NoReturn

REPO = Path(__file__).resolve().parent.parent
COURSE = REPO / "ai-foundations"
TOUR = COURSE / "visual-tour.md"

ARXIV = "https://arxiv.org/pdf/"
LENET = "http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf"
ALEXNET = "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"
DROPOUT = "https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf"
LI = (ARXIV + "1712.09913", 1, "Li et al., Fig. 1")
TRANSFORMER = ARXIV + "1706.03762"

# Atlas title prefix -> (PDF url, 1-based PDF page, label). Pages were found from each caption.
PAPER_FIGURES: dict[str, list[tuple[str, int, str]]] = {
    "Loss landscape": [LI],
    "Dropout": [(DROPOUT, 2, "Srivastava et al., Fig. 1")],
    "Convolution": [(ARXIV + "1603.07285", 7, "Dumoulin & Visin, Fig. 1.1")],
    "Stride": [(ARXIV + "1603.07285", 11, "Dumoulin & Visin, Figs. 1.5 and 1.6")],
    "LeNet-5": [(LENET, 7, "LeCun et al., Fig. 2")],
    "Receptive field": [(ARXIV + "1311.2901", 4, "Zeiler & Fergus, Fig. 2")],
    "AlexNet": [(ALEXNET, 5, "Krizhevsky et al., Fig. 2"),
                (ARXIV + "1409.1556", 3, "Simonyan & Zisserman, Table 1")],
    "Inception": [(ARXIV + "1409.4842", 5, "Szegedy et al., Fig. 2")],
    "ResNet": [(ARXIV + "1512.03385", 2, "He et al., Fig. 2"),
               (ARXIV + "1512.03385", 4, "He et al., Fig. 3"), LI],
    "Word embedding": [(ARXIV + "1301.3781", 5, "Mikolov et al., Fig. 1")],
    "Seq2seq": [(ARXIV + "1406.1078", 2, "Cho et al., Fig. 1")],
    "Attention as": [(ARXIV + "1409.0473", 6, "Bahdanau et al., Fig. 3"),
                     (ARXIV + "1409.0473", 3, "Bahdanau et al., Fig. 1")],
    "Scaled dot-product": [(TRANSFORMER, 4, "Vaswani et al., Fig. 2 (left)")],
    "Multi-head": [(TRANSFORMER, 4, "Vaswani et al., Fig. 2 (right)")],
    "Normalization": [(ARXIV + "1803.08494", 3, "Wu & He, Fig. 2")],
    "The Transformer": [(TRANSFORMER, 3, "Vaswani et al., Fig. 1")],
    "Decoder-only": [(TRANSFORMER, 3, "Vaswani et al., Fig. 1, right tower")],
    "The RLHF": [(ARXIV + "2203.02155", 3, "Ouyang et al., Fig. 2")],
    "Variational": [(ARXIV + "1312.6114", 2, "Kingma & Welling, Fig. 1")],
    "Generative adversarial": [(ARXIV + "1406.2661", 3, "Goodfellow et al., Fig. 1")],
    "The diffusion chain": [(ARXIV + "2006.11239", 2, "Ho et al., Fig. 2")],
    "U-Net": [(ARXIV + "1505.04597", 2, "Ronneberger et al., Fig. 1")],
    "Latent diffusion": [(ARXIV + "2112.10752", 4, "Rombach et al., Fig. 3")],
    "Vision Transformer": [(ARXIV + "2010.11929", 3, "Dosovitskiy et al., Fig. 1")],
    "CLIP": [(ARXIV + "2103.00020", 2, "Radford et al., Fig. 1")],
}

CONV = "https://raw.githubusercontent.com/vdumoulin/conv_arithmetic/master/gif/"
COLAH = "https://colah.github.io/posts/"
ALAMMAR = "https://jalammar.github.io/images/"

# Atlas title prefix -> (image url, label), shown inline from the cited web source.
WEB_FIGURES: dict[str, list[tuple[str, str]]] = {
    "Computational graph": [(COLAH + "2015-08-Backprop/img/chain-backward-greek.png", "Olah: reverse-mode chain rule")],
    "Convolution": [(CONV + "no_padding_no_strides.gif", "conv_arithmetic: a kernel sliding")],
    "Stride": [(CONV + "padding_strides.gif", "conv_arithmetic: padding with stride 2")],
    "RNN, folded": [(COLAH + "2015-08-Understanding-LSTMs/img/RNN-unrolled.png", "Olah: an RNN unrolled")],
    "LSTM cell": [(COLAH + "2015-08-Understanding-LSTMs/img/LSTM3-chain.png", "Olah: the LSTM chain")],
    "Positional encoding": [(ALAMMAR + "t/transformer_positional_encoding_large_example.png", "Alammar: positional encoding")],
    "Decoder-only": [(ALAMMAR + "gpt2/transformer-attention-mask.png", "Alammar: the attention mask")],
}


# Atlas title prefix -> our own generated figure (tools/build_figures.py), shown first.
COURSE_FIGURES: dict[str, list[str]] = {
    "Artificial neuron": ["neuron"],
    "Activation function": ["activation-functions"],
    "Loss landscape": ["loss-landscape"],
    "Computational graph": ["computational-graph"],
    "Learning curves": ["learning-curves"],
    "Dropout": ["dropout"],
    "An image as": ["rgb-channels"],
    "Convolution": ["convolution"],
    "Stride": ["stride-padding-pooling"],
    "Receptive field": ["receptive-field"],
    "AlexNet": ["alexnet-vgg"],
    "Inception": ["inception"],
    "ResNet": ["resnet-block"],
    "Multi-layer perceptron": ["mlp"],
    "LeNet-5": ["lenet-5"],
    "Positional encoding": ["positional-encoding"],
    "The Transformer": ["transformer"],
    "The diffusion chain": ["diffusion-chain"],
}


def die(msg: str) -> NoReturn:
    print(f"*** build_visual_tour: {msg}", file=sys.stderr)
    sys.exit(1)


def matching(table: dict[str, list], title: str) -> list:
    return [v for key, values in table.items() if title.startswith(key) for v in values]


def parse_atlas(text: str) -> dict[str, list[tuple[str, str]]]:
    """Topic number -> [(title, body)] for each `### <topic> <title>` entry."""
    start, end = text.index("## Phase 1"), text.index("## Final review")
    entries: dict[str, list[tuple[str, str]]] = {}
    pattern = r"^### (\d+\.\d+) (.+?)\n(.*?)(?=^##|\Z)"
    for topic, title, body in re.findall(pattern, text[start:end], re.M | re.S):
        entries.setdefault(topic, []).append((title, body.strip()))
    return entries


def parse_syllabus(text: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """[(phase heading, [(topic number, description)])], in syllabus order."""
    phases = []
    for head, body in re.findall(r"^## (Phase .+?)\n(.*?)(?=^## |^---|\Z)", text, re.M | re.S):
        topics = re.findall(r"^- \*\*(\d+\.\d+)\*\* (.+?)(?=^- \*\*|\Z)", body, re.M | re.S)
        phases.append((head, [(t, " ".join(d.split())) for t, d in topics]))
    return phases


def search_url(phrase: str) -> str:
    return "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(phrase)


def see_lines(title: str, body: str) -> list[str]:
    phrases = re.search(r"^- \*\*Search:\*\* (.+)$", body, re.M)
    if not phrases:
        die(f"atlas entry '{title}' has no Search field")
    lines = [f"- Image search: [{p.strip()}]({search_url(p.strip())})" for p in phrases.group(1).split(",")]
    lines += [f"- [{label}, PDF page {page}]({url}#page={page})"
              for url, page, label in matching(PAPER_FIGURES, title)]
    return lines


def entry_md(topic: str, title: str, body: str) -> str:
    annotation = re.sub(r"^- \*\*Search:\*\* .+\n", "", body, flags=re.M)
    ours = [f"![{title}](figures/{name}.svg)" for name in matching(COURSE_FIGURES, title)]
    images = [f"![{label}]({url})" for url, label in matching(WEB_FIGURES, title)]
    parts = [f"### {topic} {title}", *ours, "\n".join(see_lines(title, body)), *images, annotation]
    return "\n\n".join(parts)


def render() -> str:
    entries = parse_atlas((COURSE / "the-diagram-atlas.md").read_text())
    phases = parse_syllabus((COURSE / "syllabus.md").read_text())
    known = {topic for _, topics in phases for topic, _ in topics}
    if set(entries) - known:
        die(f"atlas topics not in the syllabus: {sorted(set(entries) - known)}")
    for names in COURSE_FIGURES.values():
        for name in names:
            if not (COURSE / f"figures/{name}.svg").is_file():
                die(f"missing figures/{name}.svg - run tools/build_figures.py")
    for table in (PAPER_FIGURES, WEB_FIGURES, COURSE_FIGURES):
        titles = [title for items in entries.values() for title, _ in items]
        for key in table:
            if not any(t.startswith(key) for t in titles):
                die(f"figure key '{key}' matches no atlas entry")

    out = [
        "# Visual Tour of AI Foundations",
        "<!-- Generated by tools/build_visual_tour.py from syllabus.md and the-diagram-atlas.md"
        " - do not edit here; edit those and rebuild. -->",
        "Every topic in the course, in order, with the famous diagrams beside the topics"
        " that teach them. Each diagram is annotated with its image search, the exact PDF"
        " page of its primary figure where there is one, and notes on how to read it. For"
        " the reading method and the five grammars, see"
        " [`the-diagram-atlas.md`](the-diagram-atlas.md).",
    ]
    for head, topics in phases:
        out.append(f"## {head}")
        for topic, description in topics:
            out.append(f"**{topic}** {description}")
            out += [entry_md(topic, title, body) for title, body in entries.get(topic, [])]
    return "\n\n".join(out) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="fail if the tour is stale")
    args = parser.parse_args()
    text = render()
    if args.check:
        if not TOUR.is_file() or TOUR.read_text() != text:
            die(f"{TOUR} is stale - rerun tools/build_visual_tour.py")
        print(f"{TOUR}: up to date")
        return
    TOUR.write_text(text)
    print(f"Wrote {TOUR}")


if __name__ == "__main__":
    main()
