"""Scan Markdown files and parse YAML Front Matter."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

MARKDOWN_EXTENSIONS = {".md", ".markdown"}


def split_front_matter(text: str) -> tuple[dict, str]:
    """Split YAML Front Matter from the Markdown body.

    A file is treated as having Front Matter only when it starts with ``---``
    on its own line. The closing ``---`` on its own line ends the block.
    If no leading fence is found, returns empty metadata and the full text.
    """
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text

    yaml_text = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])
    metadata = yaml.safe_load(yaml_text)
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise yaml.YAMLError("Front Matter must be a YAML mapping")
    return metadata, body


def extract_title(metadata: dict, body: str, file_path: str | Path) -> str:
    """Return the first H1 heading in the body, or the file stem as fallback."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("##"):
            return stripped[2:].strip()

    return Path(file_path).stem


def parse_file(file_path: str | Path) -> dict | None:
    """Read a Markdown file and return structured metadata, title, and path.

    Returns ``None`` when YAML Front Matter is present but malformed; a warning
    is printed to stderr and the file is skipped during scans.
    """
    path = Path(file_path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Failed to read {path}: {exc}") from exc

    try:
        metadata, body = split_front_matter(text)
    except yaml.YAMLError as exc:
        print(f"warning: skipping {path}: invalid YAML Front Matter: {exc}", file=sys.stderr)
        return None

    return {
        "file_path": str(path),
        "title": extract_title(metadata, body, path),
        "metadata": metadata,
    }


def scan(path: str | Path) -> list[dict]:
    """Recursively scan for Markdown files and parse Front Matter."""
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {root}")

    results: list[dict] = []
    if root.is_file():
        if root.suffix.lower() in MARKDOWN_EXTENSIONS:
            parsed = parse_file(root)
            if parsed is not None:
                results.append(parsed)
    else:
        for file_path in sorted(root.rglob("*")):
            if file_path.is_file() and file_path.suffix.lower() in MARKDOWN_EXTENSIONS:
                parsed = parse_file(file_path)
                if parsed is not None:
                    results.append(parsed)

    results.sort(key=lambda item: item["file_path"])
    return results
