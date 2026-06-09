"""Guard the bundled examples against drift.

These tests ensure every file under ``examples/`` parses cleanly (no malformed
YAML warnings) so the documented commands in ``examples/README.md`` keep working.
"""

from __future__ import annotations

from pathlib import Path

from agent_md_query.scanner import scan

EXAMPLES = Path(__file__).parent.parent / "examples" / "workboard" / "tasks"


def test_examples_parse_without_warnings(capsys) -> None:
    results = scan(EXAMPLES)
    captured = capsys.readouterr()
    assert captured.err == ""  # no malformed-YAML warnings
    assert len(results) == 3
    assert all(item["metadata"] for item in results)


def test_examples_have_expected_projects() -> None:
    results = scan(EXAMPLES)
    projects = {item["metadata"].get("project") for item in results}
    assert projects == {"ai-hisho-os", "dev-access-manager"}


def test_examples_demonstrate_validate_case() -> None:
    """At least one example is intentionally missing a recommended field."""
    from agent_md_query.validator import validate

    results = scan(EXAMPLES)
    missing_by_file = dict(validate(results))
    assert any(missing for missing in missing_by_file.values())
