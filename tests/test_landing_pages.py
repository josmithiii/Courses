"""Tests for the public landing pages in landing-pages/ (run: uvx pytest tests/)."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
PAGES = sorted((REPO / "landing-pages").glob("*/index.html"))
BOOK_SERIES = REPO / "landing-pages/book-series/index.html"

# Hosts a page may load from or link to. Loads are only Google Fonts; links may go further.
LOAD_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}
LINK_HOSTS = LOAD_HOSTS | {"ccrma.stanford.edu", "github.com", "claude.com"}
VOID = {"meta", "link", "br", "img", "input", "hr", "source", "circle", "line", "path", "rect"}


class TagChecker(HTMLParser):
    """Collects unbalanced tags, loaded URLs and linked URLs."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.loads: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "script" and a.get("src"):
            self.loads.append(a["src"] or "")
        if tag == "link" and a.get("rel") == "stylesheet":
            self.loads.append(a.get("href") or "")
        if tag == "img" and a.get("src"):
            self.loads.append(a["src"] or "")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"] or "")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"</{tag}> closes {self.stack[-1:] or 'nothing'}")


def host(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1) if m else ""


def test_there_is_a_page() -> None:
    assert BOOK_SERIES in PAGES


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.parent.name)
def test_page_is_standalone_and_well_formed(page: Path) -> None:
    text = page.read_text()
    assert text.lstrip().lower().startswith("<!doctype html>")
    assert re.search(r'<html lang="[a-z-]+">', text)
    assert re.search(r"<title>[^<]{3,}</title>", text)
    assert 'name="viewport"' in text and 'name="description"' in text
    assert "claude:" not in text, "artifact-only meta tag left in a standalone page"
    checker = TagChecker()
    checker.feed(text)
    assert checker.errors == [] and checker.stack == []
    for url in checker.loads:
        assert host(url) in LOAD_HOSTS, f"loads from a disallowed host: {url}"
    for url in checker.links:
        if url.startswith("#"):
            assert re.search(rf'id="{re.escape(url[1:])}"', text), f"broken anchor {url}"
        else:
            assert host(url) in LINK_HOSTS, f"links to an unexpected host: {url}"


def bank_total(course: str) -> int:
    index = (REPO / course / "exercises/index.md").read_text()
    m = re.search(r"^(\d+) multiple-choice exercises", index, re.M)
    assert m, f"{course}/exercises/index.md has no total"
    return int(m.group(1))


@pytest.mark.parametrize("course", ["mdft", "filters", "sasp", "pasp"])
def test_book_series_card_matches_course(course: str) -> None:
    text = BOOK_SERIES.read_text()
    m = re.search(rf'<article class="course" id="{course}">(.*?)</article>', text, re.S)
    assert m, f"no card for {course}"
    card = m.group(1)
    assert (REPO / course / ".claude/commands/lesson.md").is_file()
    shown = re.search(r"<span>(\d+) exercises</span>", card)
    assert shown and int(shown.group(1)) == bank_total(course), f"{course} card's exercise count is stale"
    assert f"https://ccrma.stanford.edu/~jos/{course}/" in card
    assert f"https://github.com/josmithiii/Courses/tree/main/{course}" in card


def test_book_series_install_command_matches_readme() -> None:
    readme = (REPO / "README.md").read_text()
    m = re.search(r"^(claude plugin marketplace add \S+ && claude plugin install \S+)$", readme, re.M)
    assert m, "README.md no longer has the one-line install command"
    page = BOOK_SERIES.read_text().replace("&amp;", "&")
    assert m.group(1) in page
