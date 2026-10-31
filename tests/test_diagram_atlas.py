"""Tests for ai-foundations/the-diagram-atlas.md (run: uvx pytest tests/)."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType
from xml.etree import ElementTree

import pytest

REPO = Path(__file__).resolve().parent.parent
COURSE = REPO / "ai-foundations"
ATLAS = (COURSE / "the-diagram-atlas.md").read_text()
SYLLABUS = (COURSE / "syllabus.md").read_text()

FIELDS = ("Grammar", "Figure", "Search", "Source", "Read it", "Trap", "Check")
GRAMMARS = {"Graph", "Block", "Slab", "Probabilistic", "Plot"}

REQUIRED_BUZZWORDS = (
    "perceptron", "MLP", "LeNet-5", "AlexNet", "VGG", "Inception", "ResNet", "U-Net",
    "RNN", "LSTM", "Seq2seq", "Attention", "Multi-head", "Transformer", "GPT",
    "Autoencoder", "VAE", "GAN", "diffusion", "Stable Diffusion", "ViT", "CLIP", "Agent",
)


def entries() -> list[tuple[str, str, str]]:
    """(topic, title, body) for each `### <topic> <title>` entry."""
    found = re.findall(r"^### (\d+\.\d+) (.+?)\n(.*?)(?=^##|\Z)", ATLAS, re.M | re.S)
    assert found, "no atlas entries parsed"
    return found


def field(body: str, name: str) -> str:
    match = re.search(rf"^- \*\*{name}:\*\* (.+)$", body, re.M)
    assert match, f"missing {name}"
    return match.group(1)


def test_atlas_is_ascii() -> None:
    bad = sorted({c for c in ATLAS if not c.isascii()})
    assert not bad, f"non-ASCII characters: {bad}"


@pytest.mark.parametrize(("topic", "title", "body"), entries(), ids=lambda v: v[:30])
def test_entry_is_complete(topic: str, title: str, body: str) -> None:
    for name in FIELDS:
        assert field(body, name), f"{topic} {title}: empty {name}"
    assert field(body, "Grammar") in GRAMMARS


@pytest.mark.parametrize(("topic", "title", "body"), entries(), ids=lambda v: v[:30])
def test_entry_topic_is_in_syllabus(topic: str, title: str, body: str) -> None:
    assert f"- **{topic}** " in SYLLABUS, f"{title}: no syllabus topic {topic}"


def test_entries_follow_syllabus_order() -> None:
    topics = [tuple(map(int, topic.split("."))) for topic, _, _ in entries()]
    assert topics == sorted(topics)


@pytest.mark.parametrize("buzzword", REQUIRED_BUZZWORDS)
def test_buzzword_is_covered(buzzword: str) -> None:
    titles = " ".join(title for _, title, _ in entries()).lower()
    assert buzzword.lower() in titles


def test_every_grammar_is_used() -> None:
    assert {field(body, "Grammar") for _, _, body in entries()} == GRAMMARS


def test_course_files_require_the_atlas() -> None:
    assert "the-diagram-atlas.md" in SYLLABUS
    assert "the-diagram-atlas.md" in (COURSE / ".claude/commands/lesson.md").read_text()
    assert "the-diagram-atlas.md" in (COURSE / "CLAUDE.md").read_text()


def test_atlas_ships_in_the_plugin() -> None:
    assert (REPO / "courses-plugin/skills/ai-foundations/the-diagram-atlas.md").is_file()


def load_tour_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_visual_tour", REPO / "tools/build_visual_tour.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vt = load_tour_builder()


def test_visual_tour_is_fresh() -> None:
    assert (COURSE / "visual-tour.md").read_text() == vt.render(), "rerun tools/build_visual_tour.py"


def test_visual_tour_has_every_topic_and_entry() -> None:
    tour = (COURSE / "visual-tour.md").read_text()
    for topic in re.findall(r"^- \*\*(\d+\.\d+)\*\* ", SYLLABUS, re.M):
        assert f"**{topic}** " in tour
    for topic, title, _ in entries():
        assert f"### {topic} {title}\n" in tour


def test_visual_tour_deep_links_each_paper_figure() -> None:
    tour = (COURSE / "visual-tour.md").read_text()
    for figures in vt.PAPER_FIGURES.values():
        for url, page, label in figures:
            assert f"[{label}, PDF page {page}]({url}#page={page})" in tour


def test_visual_tour_ships_in_the_plugin() -> None:
    assert (REPO / "courses-plugin/skills/ai-foundations/visual-tour.md").is_file()


def load_figure_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_figures", REPO / "tools/build_figures.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bf = load_figure_builder()
FIGURE_NAMES = sorted(bf.FIGURES)


@pytest.mark.parametrize("name", FIGURE_NAMES)
def test_figure_is_fresh_and_well_formed(name: str) -> None:
    path = COURSE / f"figures/{name}.svg"
    assert path.read_text() == bf.FIGURES[name](), "rerun tools/build_figures.py"
    root = ElementTree.fromstring(path.read_text())
    assert root.tag.endswith("svg")


@pytest.mark.parametrize("name", FIGURE_NAMES)
def test_figure_appears_in_the_tour_and_plugin(name: str) -> None:
    assert f"(figures/{name}.svg)" in (COURSE / "visual-tour.md").read_text()
    assert (REPO / f"courses-plugin/skills/ai-foundations/figures/{name}.svg").is_file()


@pytest.mark.parametrize("name", FIGURE_NAMES)
def test_figure_text_meets_the_minimum_size(name: str) -> None:
    sizes = [int(s) for s in re.findall(r'font-size="(\d+)"', (COURSE / f"figures/{name}.svg").read_text())]
    assert sizes and min(sizes) >= bf.TEXT == 21
    assert max(sizes) == bf.TITLE


@pytest.mark.parametrize("name", FIGURE_NAMES)
def test_figure_font_survives_a_viewer_stylesheet(name: str) -> None:
    """Emacs's SVG stylesheet beats a font-family attribute, and monospace text then overflows."""
    root = ElementTree.fromstring((COURSE / f"figures/{name}.svg").read_text())
    assert root.get("style") == f"font-family:{bf.FONT}"


def test_text_below_the_minimum_fails_the_build() -> None:
    fig = bf.Fig(400, 200, "t", "Plot", [])
    with pytest.raises(SystemExit):
        fig.text(200, 100, "too small", size=bf.TEXT - 1)


def test_text_off_the_canvas_fails_the_build() -> None:
    fig = bf.Fig(400, 200, "t", "Plot", [])
    with pytest.raises(SystemExit):
        fig.text(390, 100, "much too long for this spot", anchor="start")


def test_gallery_is_fresh_and_lists_every_figure() -> None:
    page = (COURSE / "figures/gallery.html").read_text()
    assert page == bf.gallery({f"{n}.svg": bf.FIGURES[n]() for n in bf.FIGURES})
    assert all(f'src="{name}.svg"' in page for name in FIGURE_NAMES)
    assert 'type="range"' in page


def test_gallery_ships_in_the_plugin() -> None:
    assert (REPO / "courses-plugin/skills/ai-foundations/figures/gallery.html").is_file()


def test_no_orphan_figures() -> None:
    assert sorted(p.stem for p in (COURSE / "figures").glob("*.svg")) == FIGURE_NAMES


def figure_name(body: str) -> str:
    match = re.search(r"\(figures/([\w-]+)\.svg\)", field(body, "Figure"))
    assert match, "Figure field names no file"
    return match.group(1)


def test_every_figure_belongs_to_exactly_one_entry() -> None:
    assert sorted(figure_name(body) for _, _, body in entries()) == FIGURE_NAMES


@pytest.mark.parametrize(("topic", "title", "body"), entries(), ids=lambda v: v[:30])
def test_figure_grammar_matches_its_entry(topic: str, title: str, body: str) -> None:
    svg = (COURSE / f"figures/{figure_name(body)}.svg").read_text()
    assert f">{field(body, 'Grammar')}</text>" in svg


def test_tutor_is_told_to_show_the_figure() -> None:
    assert "Show the course figure" in ATLAS
    assert "course figure" in (COURSE / ".claude/commands/lesson.md").read_text()


def test_figures_preference_is_asked_once_and_recorded() -> None:
    assert "**Figures** preference" in ATLAS
    assert "**Figures** preference" in (COURSE / ".claude/commands/lesson.md").read_text()
    assert "**Figures** preference" in (COURSE / "CLAUDE.md").read_text()
    assert "- Figures: _(unset" in (COURSE / "progress.template.md").read_text()


def test_convolution_output_matches_the_atlas_check() -> None:
    assert ">-2</text>" in bf.convolution()


def test_backprop_figure_matches_the_atlas_check() -> None:
    assert "dL/dw = 6" in bf.computational_graph()


def test_diverging_colormap_endpoints() -> None:
    assert bf.diverging(0.0) == (255, 255, 255)
    assert bf.diverging(1.0) == (208, 112, 26)
    assert bf.diverging(-1.0) == (31, 95, 139)


def test_noising_at_t_zero_leaves_the_image_unchanged() -> None:
    image = [[-1.0, 1.0], [1.0, -1.0]]
    rows = bf.noised(image, 0, bf.random.Random(0))
    assert rows == [[(0, 0, 0), (255, 255, 255)], [(255, 255, 255), (0, 0, 0)]]
