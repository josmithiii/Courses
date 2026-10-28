"""Tests for tools/build_book_exercises.py and the book courses it feeds (run: uvx pytest tests/)."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "tools/build_book_exercises.py"


def load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_book_exercises", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # @dataclass resolves annotations through sys.modules
    spec.loader.exec_module(module)
    return module


bx = load_builder()
BOOK_IDS = sorted(bx.BOOKS)


def has_source(book_id: str) -> bool:
    book = bx.BOOKS[book_id]
    return (book.default_src / f"exercises/{book_id}-exercises.json").is_file()


def skip_without_source(book_id: str) -> None:
    # The book repos are JOS's local checkouts; other clones only have the committed banks.
    if not has_source(book_id):
        pytest.skip(f"{book_id} book course data not found under {bx.BOOKS_DIR} (set $JOS_BOOKS_DIR)")


@pytest.mark.parametrize(
    ("html_in", "text_out"),
    [
        ("<i>z</i> = 3 + 4<i>j</i>", "z = 3 + 4j"),
        ("<i>z</i><sub>1</sub><sup><i>N</i></sup>", "z_1^N"),
        ("<i>z</i><sub>1</sub><i>S</i><sub><i>N</i></sub>", "z_1 S_N"),
        ("<i>e</i><sup>&minus;<i>j</i>2&pi;<i>k&tau;</i>/<i>N</i></sup>", "e^(−j2πkτ/N)"),
        ('<span style="text-decoration: overline"><i>X</i>(<i>k</i>)</span>', "X̅(k)"),
        ('<span style="text-decoration:overline">&alpha;</span>', "α̅"),
        ("2&gamma;&thinsp;cos(&theta;)", "2γ cos(θ)"),
        ("<b>bold</b> and <code>fft(x)</code>", "**bold** and `fft(x)`"),
        ("<strong>never</strong> cancel", "**never** cancel"),
        ("<u,v> = 0", "<u,v> = 0"),  # plain-text angle brackets survive
    ],
)
def test_html_to_text(html_in: str, text_out: str) -> None:
    assert bx.html_to_text(html_in) == text_out


def test_unknown_tag_fails_loudly() -> None:
    with pytest.raises(SystemExit):
        bx.html_to_text('<span class="mystery">x</span>')
    with pytest.raises(SystemExit):
        bx.html_to_text("a <br> b")


def test_missing_source_fails_loudly(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        bx.build(bx.BOOKS["mdft"], tmp_path / "nowhere", tmp_path / "out")


def test_unknown_book_fails_loudly() -> None:
    result = subprocess.run([sys.executable, str(SCRIPT), "no-such-book"], capture_output=True, text=True)
    assert result.returncode != 0


def test_unnumbered_chapter_gets_bare_slug() -> None:
    outline = [
        {"file": "Intro.html", "title": "Intro", "num": "1", "depth": 1},
        {"file": "Summary.html", "title": "Summary and Conclusions", "num": "", "depth": 1},
        {"file": "Notation.html", "title": "Notation", "num": "A", "depth": 1},
    ]
    assert bx.chapter_files(outline) == {
        "Intro": ("1", "ch01-intro"),
        "Summary and Conclusions": ("", "summary-and-conclusions"),
        "Notation": ("A", "appA-notation"),
    }


@pytest.mark.parametrize("book_id", BOOK_IDS)
def test_committed_bank_is_well_formed(book_id: str) -> None:
    bank = bx.BOOKS[book_id].out_dir
    index = (bank / "index.md").read_text()
    total = int(re.search(r"^(\d+) multiple-choice exercises", index, re.M).group(1))
    listed = re.findall(r"\| \[`([\w-]+\.md)`\]\([\w-]+\.md\) \| (\d+) \|", index)
    assert listed, "index.md lists no chapter files"
    assert sorted(f for f, _ in listed) == sorted(p.name for p in bank.glob("*.md") if p.name != "index.md")
    count = 0
    for name, n in listed:
        text = (bank / name).read_text()
        heads = re.findall(r"^#### `", text, re.M)
        answers = re.findall(r"^\*\*Answer: \([a-z]\)\.\*\*", text, re.M)
        assert len(heads) == len(answers) == int(n), name
        assert not re.search(r"&[A-Za-z#0-9]+;", text), f"{name}: unescaped HTML entity"
        assert not re.search(r"</?(?:span|sup|sub|i|b|strong|em|code)>", text), f"{name}: leftover HTML tag"
        assert f"Book page: {bx.BOOKS[book_id].url}" in text
        count += len(heads)
    assert count == total


@pytest.mark.parametrize("book_id", BOOK_IDS)
def test_committed_bank_is_up_to_date(book_id: str) -> None:
    skip_without_source(book_id)
    result = subprocess.run([sys.executable, str(SCRIPT), book_id, "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("book_id", BOOK_IDS)
def test_course_cites_real_book_pages(book_id: str) -> None:
    skip_without_source(book_id)
    meta = json.loads((bx.BOOKS[book_id].default_src / "page-metadata.json").read_text())
    text = "".join((REPO / book_id / f).read_text() for f in ["syllabus.md", "CLAUDE.md"])
    cited = set(re.findall(r"`([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]+|[A-Z][a-z]+)`", text))
    cited -= {"COURSES_DATA_DIR", "Page_Name", "JOS_BOOKS_DIR"}
    assert cited
    assert sorted(c for c in cited if f"{c}.html" not in meta) == []
