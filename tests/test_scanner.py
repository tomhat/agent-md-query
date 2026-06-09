"""Tests for the Markdown scanner."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_md_query.scanner import extract_title, parse_file, scan, split_front_matter

FIXTURES = Path(__file__).parent / "fixtures"


def test_split_front_matter_parses_valid_yaml() -> None:
    text = "---\nstatus: doing\n---\n\n# Title\n"
    metadata, body = split_front_matter(text)
    assert metadata == {"status": "doing"}
    assert "# Title" in body


def test_split_front_matter_without_fence() -> None:
    text = "# Title only\n"
    metadata, body = split_front_matter(text)
    assert metadata == {}
    assert body == text


def test_extract_title_from_h1() -> None:
    title = extract_title({}, "# My Title\n\nBody", "task.md")
    assert title == "My Title"


def test_extract_title_ignores_h2() -> None:
    title = extract_title({}, "## Not H1\n\n# Real Title\n", "task.md")
    assert title == "Real Title"


def test_extract_title_falls_back_to_stem() -> None:
    title = extract_title({}, "No heading", "path/to/task-no-h1.md")
    assert title == "task-no-h1"


def test_parse_file_with_front_matter() -> None:
    path = FIXTURES / "with_frontmatter" / "task-doing.md"
    result = parse_file(path)
    assert result is not None
    assert result["title"] == "Codex Token Budget Review"
    assert result["metadata"]["status"] == "doing"
    assert result["metadata"]["tags"] == ["token-budget", "dispatch"]
    assert result["file_path"] == str(path)


def test_parse_file_without_front_matter() -> None:
    path = FIXTURES / "without_frontmatter" / "plain.md"
    result = parse_file(path)
    assert result is not None
    assert result["metadata"] == {}
    assert result["title"] == "Plain Document"


def test_parse_file_without_h1_uses_stem() -> None:
    path = FIXTURES / "with_frontmatter" / "task-no-h1.md"
    result = parse_file(path)
    assert result is not None
    assert result["title"] == "task-no-h1"


def test_parse_file_malformed_yaml_returns_none(capsys) -> None:
    path = FIXTURES / "malformed" / "bad-yaml.md"
    result = parse_file(path)
    assert result is None
    captured = capsys.readouterr()
    assert "warning:" in captured.err
    assert "bad-yaml.md" in captured.err


def test_scan_discovers_md_and_markdown_recursively() -> None:
    results = scan(FIXTURES)
    paths = {item["file_path"] for item in results}
    assert str(FIXTURES / "with_frontmatter" / "task-doing.md") in paths
    assert str(FIXTURES / "nested" / "subdir" / "nested.md") in paths
    assert str(FIXTURES / "extensions" / "file.markdown") in paths
    assert str(FIXTURES / "malformed" / "bad-yaml.md") not in paths


def test_scan_sorts_by_file_path() -> None:
    results = scan(FIXTURES)
    paths = [item["file_path"] for item in results]
    assert paths == sorted(paths)


def test_scan_missing_path_raises() -> None:
    with pytest.raises(FileNotFoundError, match="Path not found"):
        scan(FIXTURES / "does-not-exist")


def test_parse_file_read_error_raises(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"
    with pytest.raises(OSError, match="Failed to read"):
        parse_file(missing)
