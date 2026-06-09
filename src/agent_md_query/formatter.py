"""Render scan results as markdown, JSON, or file paths."""

from __future__ import annotations

import json
from collections import defaultdict

NO_PROJECT = "(no project)"

def _json_field(value: object) -> str | int | float | bool | None:
    """Convert metadata values to JSON-serializable scalars."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def format_paths(results: list[dict]) -> str:
    """Return one file path per line with no extra decoration."""
    if not results:
        return ""
    return "\n".join(item["file_path"] for item in results)


def format_json(results: list[dict]) -> str:
    """Return a JSON array with stable field names.

    Listed fields are always present; missing metadata values are emitted as
    JSON ``null`` so consumers get a predictable schema.
    """
    payload = []
    for item in results:
        metadata = item["metadata"]
        record = {
            "title": item["title"],
            "project": _json_field(metadata.get("project")),
            "status": _json_field(metadata.get("status")),
            "priority": _json_field(metadata.get("priority")),
            "assignee": _json_field(metadata.get("assignee")),
            "updated_at": _json_field(metadata.get("updated_at")),
            "file_path": item["file_path"],
        }
        payload.append(record)

    return json.dumps(payload, ensure_ascii=False, indent=2)


def format_markdown(results: list[dict]) -> str:
    """Return human-readable Markdown grouped by project."""
    if not results:
        return "# Query Result\n"

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in results:
        project = item["metadata"].get("project") or NO_PROJECT
        grouped[project].append(item)

    lines = ["# Query Result", ""]
    project_names = sorted(grouped.keys(), key=lambda name: (name == NO_PROJECT, name))

    for project in project_names:
        lines.append(f"## {project}")
        lines.append("")
        for item in grouped[project]:
            metadata = item["metadata"]
            status = metadata.get("status", "")
            priority = metadata.get("priority", "")
            header_parts = [
                str(part) for part in (status, priority) if part not in (None, "")
            ]
            header = " / ".join(header_parts)
            if header:
                lines.append(f"- {header}: {item['title']}")
            else:
                lines.append(f"- {item['title']}")
            lines.append(f"  - file: `{item['file_path']}`")
            if "assignee" in metadata:
                lines.append(f"  - assignee: {metadata['assignee']}")
            if "updated_at" in metadata:
                lines.append(f"  - updated_at: {metadata['updated_at']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render(results: list[dict], fmt: str) -> str:
    """Dispatch to the formatter for the requested output format."""
    if fmt == "paths":
        return format_paths(results)
    if fmt == "json":
        return format_json(results)
    if fmt == "markdown":
        return format_markdown(results)
    raise ValueError(f"unsupported format: {fmt}")
