"""Tests for the public landing pages in landing-pages/ (run: uvx pytest tests/)."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "landing-pages"
PAGES = sorted([SITE / "index.html", *SITE.glob("*/index.html")])
BOOK_SERIES = SITE / "book-series/index.html"
GITHUB_REPO = "https://github.com/josmithiii/Courses"

# External hosts: loads are only Google Fonts; links may go further. Relative URLs
# must resolve to files in landing-pages/ (they are published together).
LOAD_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}
LINK_HOSTS = LOAD_HOSTS | {
    "ccrma.stanford.edu", "github.com", "claude.com", "josmithiii.github.io", "cm-gitlab.stanford.edu",
}
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


def resolve(page: Path, url: str) -> tuple[Path, str]:
    """A relative URL on `page` -> (file it names, fragment)."""
    path, _, frag = url.partition("#")
    target = (page.parent / path).resolve() if path else page
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, frag


def parse(page: Path) -> TagChecker:
    checker = TagChecker()
    checker.feed(page.read_text())
    return checker


def test_expected_pages_exist() -> None:
    names = {p.relative_to(SITE).as_posix() for p in PAGES}
    assert {"index.html", "book-series/index.html", "ai-foundations/index.html",
            "ai-miracle-decade-plus/index.html"} <= names


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(SITE).as_posix())
def test_page_is_standalone_and_well_formed(page: Path) -> None:
    text = page.read_text()
    assert text.lstrip().lower().startswith("<!doctype html>")
    assert re.search(r'<html lang="[a-z-]+">', text)
    assert re.search(r"<title>[^<]{3,}</title>", text)
    assert 'name="viewport"' in text and 'name="description"' in text
    assert "claude:" not in text, "artifact-only meta tag left in a standalone page"
    checker = parse(page)
    assert checker.errors == [] and checker.stack == []
    for url in checker.loads:
        if host(url):
            assert host(url) in LOAD_HOSTS, f"loads from a disallowed host: {url}"
        else:
            assert resolve(page, url)[0].is_file(), f"missing local file: {url}"


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(SITE).as_posix())
def test_page_links_resolve(page: Path) -> None:
    for url in parse(page).links:
        if host(url):
            assert host(url) in LINK_HOSTS, f"links to an unexpected host: {url}"
            if url.startswith(GITHUB_REPO + "/"):
                m = re.match(rf"{re.escape(GITHUB_REPO)}/(?:tree|blob)/main/([^#]+)", url)
                if m:
                    assert (REPO / m.group(1)).exists(), f"GitHub link to a missing repo path: {url}"
            continue
        target, frag = resolve(page, url)
        assert target.is_file(), f"broken relative link {url}"
        if frag:
            assert f'id="{frag}"' in target.read_text(), f"broken anchor {url}"


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(SITE).as_posix())
def test_named_courses_exist(page: Path) -> None:
    text = page.read_text()
    named = set(re.findall(r"today's ([a-z0-9-]+) lesson", text))
    named |= set(re.findall(r'<span class="mono">([a-z0-9-]+)</span>', text)) - {"./take"}
    for course in named:
        assert (REPO / course / ".claude/commands/lesson.md").is_file(), f"no course named {course}"


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(SITE).as_posix())
def test_install_command_matches_readme(page: Path) -> None:
    readme = (REPO / "README.md").read_text()
    m = re.search(r"^(claude plugin marketplace add \S+ && claude plugin install \S+)$", readme, re.M)
    assert m, "README.md no longer has the one-line install command"
    text = page.read_text().replace("&amp;", "&")
    if "claude plugin" in text:
        assert m.group(1) in text


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
    shown = re.search(r"<span>(\d+) exercises</span>", card)
    assert shown and int(shown.group(1)) == bank_total(course), f"{course} card's exercise count is stale"
    assert f"https://ccrma.stanford.edu/~jos/{course}/" in card
    assert f"{GITHUB_REPO}/tree/main/{course}" in card


@pytest.mark.parametrize(("course", "heading"), [("ai-foundations", r"^## Phase \d+"),
                                                 ("ai-miracle-decade-plus", r"^### Phase \d+")])
def test_ai_page_phases_match_syllabus(course: str, heading: str) -> None:
    syllabus = (REPO / course / "syllabus.md").read_text()
    page = (SITE / course / "index.html").read_text()
    phases = re.search(r'<ol class="phases">(.*?)</ol>', page, re.S)
    assert phases
    assert len(re.findall(r"<li>", phases.group(1))) == len(re.findall(heading, syllabus, re.M))


def test_ai_miracle_paper_count_matches_syllabus() -> None:
    syllabus = (REPO / "ai-miracle-decade-plus/syllabus.md").read_text()
    n = len(re.findall(r"^- \*\*\d+\.\d+\*\* \[", syllabus, re.M))
    page = (SITE / "ai-miracle-decade-plus/index.html").read_text()
    assert page.count("<circle") == n, "timeline dots don't match the syllabus's paper stops"
    words = {40: "Forty", 41: "Forty-one", 39: "Thirty-nine"}
    assert f"{n} papers" in page or words.get(n, "?") in page
