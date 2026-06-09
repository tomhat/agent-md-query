"""Tests for the CLI entry point."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_md_query.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_help_exits_zero(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "agent-md-query" in captured.out
    assert "usage:" in captured.out.lower()


def test_no_args_prints_help(capsys) -> None:
    assert main([]) == 0
    captured = capsys.readouterr()
    assert "agent-md-query" in captured.out


def test_list_filters_by_where_markdown_default(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert main(["list", str(fixture_dir), "--where", "status=doing"]) == 0
    captured = capsys.readouterr()
    assert "# Query Result" in captured.out
    assert "Codex Token Budget Review" in captured.out


def test_list_format_paths(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert (
        main(
            [
                "list",
                str(fixture_dir),
                "--where",
                "status=doing",
                "--format",
                "paths",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    lines = [line for line in captured.out.strip().splitlines() if line]
    assert lines == [str(fixture_dir / "task-doing.md")]


def test_list_multiple_where_filters(capsys) -> None:
    assert (
        main(
            [
                "list",
                str(FIXTURES),
                "--where",
                "status=doing",
                "--where",
                "project=example-project",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "Codex Token Budget Review" in captured.out
    assert "task-doing.md" in captured.out
    assert "task-done.md" not in captured.out


def test_list_invalid_where_returns_error(capsys) -> None:
    assert main(["list", str(FIXTURES), "--where", "statusdoing"]) == 2
    captured = capsys.readouterr()
    assert "error:" in captured.err


def test_list_missing_path_returns_error(capsys) -> None:
    assert main(["list", str(FIXTURES / "missing"), "--where", "status=doing"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err


def test_list_format_json(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert (
        main(
            [
                "list",
                str(fixture_dir),
                "--where",
                "status=doing",
                "--format",
                "json",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert '"title": "Codex Token Budget Review"' in captured.out
    assert '"file_path"' in captured.out
