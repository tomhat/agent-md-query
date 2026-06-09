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


def test_list_filters_by_where(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert main(["list", str(fixture_dir), "--where", "status=doing"]) == 0
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
    lines = captured.out.strip().splitlines()
    assert len(lines) == 1
    assert lines[0].endswith("task-doing.md")


def test_list_invalid_where_returns_error(capsys) -> None:
    assert main(["list", str(FIXTURES), "--where", "statusdoing"]) == 2
    captured = capsys.readouterr()
    assert "error:" in captured.err


def test_list_missing_path_returns_error(capsys) -> None:
    assert main(["list", str(FIXTURES / "missing"), "--where", "status=doing"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err
