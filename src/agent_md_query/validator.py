"""Validate Markdown Front Matter against a built-in recommended schema."""

from __future__ import annotations

RECOMMENDED_FIELDS = ("type", "id", "project", "status", "priority", "updated_at")


def _is_empty(value: object) -> bool:
    """Return True when a field value should be treated as missing."""
    return value is None or (isinstance(value, str) and value == "")


def missing_fields(
    metadata: dict,
    required: tuple[str, ...] = RECOMMENDED_FIELDS,
) -> list[str]:
    """Return required fields absent or empty in metadata, in schema order."""
    missing: list[str] = []
    for field in required:
        if field not in metadata or _is_empty(metadata[field]):
            missing.append(field)
    return missing


def validate(results: list[dict]) -> list[tuple[str, list[str]]]:
    """Return (file_path, missing_fields) for every scanned file."""
    return [
        (item["file_path"], missing_fields(item["metadata"]))
        for item in results
    ]
