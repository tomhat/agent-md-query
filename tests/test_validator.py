"""Tests for Front Matter validation."""

from __future__ import annotations

from pathlib import Path

from agent_md_query.validator import RECOMMENDED_FIELDS, missing_fields, validate

FIXTURES = Path(__file__).parent / "fixtures" / "validate"


def test_missing_fields_complete_metadata() -> None:
    metadata = {
        "type": "task",
        "id": "task-001",
        "project": "example-project",
        "status": "doing",
        "priority": "high",
        "updated_at": "2026-06-07",
    }
    assert missing_fields(metadata) == []


def test_missing_fields_partial_metadata() -> None:
    metadata = {
        "type": "task",
        "id": "task-002",
        "status": "doing",
    }
    assert missing_fields(metadata) == ["project", "priority", "updated_at"]


def test_missing_fields_empty_string_counts_as_missing() -> None:
    metadata = dict.fromkeys(RECOMMENDED_FIELDS, "value")
    metadata["status"] = ""
    assert missing_fields(metadata) == ["status"]


def test_missing_fields_none_counts_as_missing() -> None:
    metadata = dict.fromkeys(RECOMMENDED_FIELDS, "value")
    metadata["priority"] = None
    assert missing_fields(metadata) == ["priority"]


def test_validate_returns_missing_fields_per_file() -> None:
    results = [
        {
            "file_path": str(FIXTURES / "valid-task.md"),
            "title": "Valid Task",
            "metadata": {
                "type": "task",
                "id": "task-001",
                "project": "example-project",
                "status": "doing",
                "priority": "high",
                "updated_at": "2026-06-07",
            },
        },
        {
            "file_path": str(FIXTURES / "missing-updated-at.md"),
            "title": "Missing Updated At",
            "metadata": {
                "type": "task",
                "id": "task-002",
                "project": "example-project",
                "status": "doing",
                "priority": "high",
            },
        },
    ]
    assert validate(results) == [
        (str(FIXTURES / "valid-task.md"), []),
        (str(FIXTURES / "missing-updated-at.md"), ["updated_at"]),
    ]
