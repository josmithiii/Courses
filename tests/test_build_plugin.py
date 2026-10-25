"""Tests for tools/build_plugin.py (run: uvx pytest tests/)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "tools/build_plugin.py"


def load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_plugin", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bp = load_builder()


def frontmatter(text: str) -> dict[str, str]:
    lines = text.split("\n")
    assert lines[0] == "---"
    end = lines.index("---", 1)
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        key, value = line.split(":", 1)
        meta[key] = json.loads(value) if value.strip().startswith('"') else value.strip()
    return meta


def test_room_acoustics_skill(tmp_path: Path) -> None:
    out = tmp_path / "plugin"
    bp.build(["room-acoustics"], out)
    skill = out / "skills/room-acoustics"
    for name in ["SKILL.md", "CLAUDE.md", "syllabus.md", "progress.template.md", "motivating-question.md"]:
        assert (skill / name).is_file(), name

    text = (skill / "SKILL.md").read_text()
    meta = frontmatter(text)
    assert meta["name"] == "room-acoustics"
    assert "room-acoustics lesson" in meta["description"]
    assert len(meta["description"]) <= 1024

    # The repo-layout data-root default is replaced by the plugin resolution rules,
    # in both the skill and the course's tutor context.
    assert "${COURSES_DATA_DIR:-" not in text
    assert "Courses-data/` inside the folder they" in text
    assert "<data root>/room-acoustics/progress.md" in text
    assert "${COURSES_DATA_DIR:-" not in (skill / "CLAUDE.md").read_text()
    # The rest of lesson.md survives intact.
    assert "## Start of session" in text and "## End of session" in text

    manifest = json.loads((out / ".claude-plugin/plugin.json").read_text())
    assert manifest["name"] == "courses"
    assert manifest["displayName"] == bp.PLUGIN_DISPLAY_NAME


def test_marketplace_matches_plugin() -> None:
    market = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    (entry,) = market["plugins"]
    assert entry["name"] == bp.PLUGIN_NAME
    assert entry["displayName"] == bp.PLUGIN_DISPLAY_NAME
    assert entry["source"] == f"./{bp.PLUGIN_DIR_NAME}"


def test_every_course_builds(tmp_path: Path) -> None:
    out = tmp_path / "plugin"
    bp.build(bp.all_courses(), out)
    built = sorted(d.name for d in (out / "skills").iterdir())
    assert built == bp.all_courses()
    assert "course-template" not in built


def test_missing_section_fails_loudly() -> None:
    with pytest.raises(SystemExit):
        bp.replace_section("# Title\n\n## Other\ntext\n", bp.LESSON_STATE_HEADING, "x", Path("x.md"))


def test_unknown_course_fails_loudly(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        bp.build(["no-such-course"], tmp_path / "plugin")


def test_refuses_to_replace_foreign_dir(tmp_path: Path) -> None:
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "keep.txt").write_text("mine")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "room-acoustics", "--out", str(foreign)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert (foreign / "keep.txt").read_text() == "mine"


def test_committed_plugin_is_up_to_date() -> None:
    result = subprocess.run([sys.executable, str(SCRIPT), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
