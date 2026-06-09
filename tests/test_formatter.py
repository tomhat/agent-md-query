"""Tests for output formatters."""

from __future__ import annotations

import json

from agent_md_query.formatter import (
    NO_PROJECT,
    format_json,
    format_markdown,
    format_paths,
    render,
)


def _sample_results() -> list[dict]:
    return [
        {
            "file_path": "examples/workboard/tasks/task-001.md",
            "title": "Codex Token Budget Review",
            "metadata": {
                "project": "ai-hisho-os",
                "status": "doing",
                "priority": "high",
                "assignee": "codex",
                "updated_at": "2026-06-07",
            },
        },
        {
            "file_path": "examples/workboard/tasks/task-002.md",
            "title": "Other Task",
            "metadata": {
                "project": "ai-hisho-os",
                "status": "doing",
                "priority": "low",
            },
        },
        {
            "file_path": "examples/notes/note.md",
            "title": "Untagged Note",
            "metadata": {
                "status": "todo",
                "priority": "medium",
            },
        },
    ]


def test_format_paths_one_per_line() -> None:
    output = format_paths(_sample_results())
    lines = output.splitlines()
    assert lines == [
        "examples/workboard/tasks/task-001.md",
        "examples/workboard/tasks/task-002.md",
        "examples/notes/note.md",
    ]
    assert not any(line.startswith("-") for line in lines)


def test_format_paths_empty() -> None:
    assert format_paths([]) == ""


def test_format_json_stable_fields_and_nulls() -> None:
    output = format_json(_sample_results())
    data = json.loads(output)
    assert len(data) == 3
    first = data[0]
    assert set(first.keys()) == {
        "title",
        "project",
        "status",
        "priority",
        "assignee",
        "updated_at",
        "file_path",
    }
    assert first["title"] == "Codex Token Budget Review"
    assert first["file_path"] == "examples/workboard/tasks/task-001.md"
    assert data[1]["assignee"] is None
    assert data[2]["project"] is None


def test_format_markdown_groups_by_project() -> None:
    output = format_markdown(_sample_results())
    assert output.startswith("# Query Result\n")
    assert "## ai-hisho-os\n" in output
    assert f"## {NO_PROJECT}\n" in output
    assert "- doing / high: Codex Token Budget Review" in output
    assert "  - file: `examples/workboard/tasks/task-001.md`" in output
    assert "  - assignee: codex" in output
    assert "  - updated_at: 2026-06-07" in output


def test_format_markdown_omits_optional_sub_lines() -> None:
    output = format_markdown(_sample_results())
    task_two_section = output.split("- doing / low: Other Task")[1].split("- ")[0]
    assert "assignee" not in task_two_section
    assert "updated_at" not in task_two_section


def test_format_markdown_folds_empty_status_priority() -> None:
    results = [
        {
            "file_path": "examples/notes/note.md",
            "title": "Bare Note",
            "metadata": {"project": "p"},
        }
    ]
    output = format_markdown(results)
    assert "- Bare Note" in output
    assert " / :" not in output
    assert "-  / : Bare Note" not in output


def test_format_markdown_empty_results() -> None:
    assert format_markdown([]) == "# Query Result\n"


def test_render_dispatch() -> None:
    results = _sample_results()[:1]
    assert "Codex Token Budget Review" in render(results, "markdown")
    assert json.loads(render(results, "json"))
    assert render(results, "paths").endswith("task-001.md")
