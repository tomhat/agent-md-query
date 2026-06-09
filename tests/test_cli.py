"""Tests for the CLI entry point."""

from __future__ import annotations

import pytest

from agent_md_query.cli import main


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
