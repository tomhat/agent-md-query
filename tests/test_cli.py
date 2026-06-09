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


def test_summary_groups_by_project(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert main(["summary", str(fixture_dir), "--group-by", "project"]) == 0
    captured = capsys.readouterr()
    assert "# Summary" in captured.out
    assert "## example-project" in captured.out
    assert "Codex Token Budget Review" in captured.out
    assert "Completed Task" in captured.out
    assert "task-doing.md" in captured.out
    assert "task-done.md" in captured.out


def test_summary_missing_path_returns_error(capsys) -> None:
    assert main(["summary", str(FIXTURES / "missing"), "--group-by", "project"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err


def test_list_filters_by_tag(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert main(["list", str(fixture_dir), "--tag", "token-budget"]) == 0
    captured = capsys.readouterr()
    assert "Codex Token Budget Review" in captured.out
    assert "Completed Task" not in captured.out


def test_list_tag_excludes_non_matching(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert (
        main(
            [
                "list",
                str(fixture_dir),
                "--tag",
                "nonexistent",
                "--format",
                "paths",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == ""


def test_list_tag_and_where_combined(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert (
        main(
            [
                "list",
                str(fixture_dir),
                "--where",
                "status=doing",
                "--tag",
                "dispatch",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "Codex Token Budget Review" in captured.out


def test_list_multiple_tags_use_and(capsys) -> None:
    fixture_dir = FIXTURES / "with_frontmatter"
    assert (
        main(
            [
                "list",
                str(fixture_dir),
                "--tag",
                "token-budget",
                "--tag",
                "dispatch",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "Codex Token Budget Review" in captured.out


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

VALIDATE_FIXTURES = FIXTURES / "validate"


def test_validate_all_valid_returns_zero(capsys) -> None:
    valid_file = VALIDATE_FIXTURES / "valid-task.md"
    assert main(["validate", str(valid_file)]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == f"OK: {valid_file}"


def test_validate_missing_fields_returns_one(capsys) -> None:
    assert main(["validate", str(VALIDATE_FIXTURES)]) == 1
    captured = capsys.readouterr()
    assert f"OK: {VALIDATE_FIXTURES / 'valid-task.md'}" in captured.out
    assert (
        f"MISSING: {VALIDATE_FIXTURES / 'missing-updated-at.md'} -> updated_at"
        in captured.out
    )
    assert (
        f"MISSING: {VALIDATE_FIXTURES / 'missing-multiple.md'} -> project, priority"
        in captured.out
    )
    assert (
        f"MISSING: {VALIDATE_FIXTURES / 'empty-status.md'} -> status"
        in captured.out
    )


def test_validate_without_frontmatter_reports_all_fields_missing(capsys) -> None:
    plain_file = FIXTURES / "without_frontmatter" / "plain.md"
    assert main(["validate", str(plain_file)]) == 1
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "MISSING: "
        f"{plain_file} -> type, id, project, status, priority, updated_at"
    )


def test_validate_missing_path_returns_error(capsys) -> None:
    assert main(["validate", str(FIXTURES / "missing")]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err
