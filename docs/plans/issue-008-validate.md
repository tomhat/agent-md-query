# Plan: Issue #8 — `validate` command for Front Matter fields

- Issue: Add validate command for Front Matter fields
- Roadmap: v0.3
- Depends on: MVP (#2 scanner) — merged
- Status: planned

## Goal

Add `agent-md-query validate <path>` that checks Markdown Front Matter for a set of
recommended fields, reports missing fields per file, and exits non-zero when any file fails.

## Current code to build on

- `scanner.scan(path)` returns `list[dict]` (`file_path`, `title`, `metadata`).
- The scanner **skips** files with malformed YAML, printing a `warning:` to stderr and
  returning `None` for them (see `parse_file`). See the open design decision below.

## Recommended fields (built-in schema)

Per the issue, the first version checks these task-like fields:

```text
type, id, project, status, priority, updated_at
```

(Note: `assignee` and `tags` are intentionally **not** required.)

## Design

Add a small `src/agent_md_query/validator.py`:

```python
RECOMMENDED_FIELDS = ("type", "id", "project", "status", "priority", "updated_at")

def missing_fields(metadata: dict, required=RECOMMENDED_FIELDS) -> list[str]:
    """Return required fields absent (or empty) in metadata, in schema order."""

def validate(results: list[dict]) -> list[tuple[str, list[str]]]:
    """Return (file_path, missing_fields) for every scanned file."""
```

- A field counts as missing when the key is absent or its value is `None`/empty string.
- Keep the first version to **missing-field checks only**. The issue's "invalid or
  unexpected values where practical" and a configurable schema are explicitly deferred
  (issue Notes: "simple built-in recommended schema ... configurable schema later").

Add a `validate` subcommand to `cli.py`:

- `validate <path>`; `run_validate(path)`:
  - `scan(path)`, run `validate`, print one line per file:
    - `OK: <path>` when nothing is missing,
    - `MISSING: <path> -> field1, field2` otherwise.
  - Return `0` when all files pass, `1` when any file has missing fields.
  - Reuse `FileNotFoundError` → exit-code-1 handling like `run_list`.
- Output goes to stdout; keep the format exactly as the issue example.

## Open design decision (surface in the PR)

Malformed-YAML files are dropped by the scanner before `validate` sees them (warned on
stderr). Options:

- **(A) Accept scanner behavior (recommended for first version)**: malformed files are
  warned but do not by themselves fail `validate`. Simplest; consistent with existing
  scanner semantics.
- **(B) Treat unparseable files as validation failures**: requires surfacing skipped files
  from the scanner (e.g. a variant that reports parse errors). Larger change.

Default to (A) and note it in the PR. Do not implement (B) unless the user asks — it expands
scope and touches the scanner's public behavior.

## Tasks

1. Add `validator.py` with `RECOMMENDED_FIELDS`, `missing_fields`, `validate`.
2. Add the `validate` subcommand + `run_validate` to `cli.py`; dispatch in `main` with the
   non-zero exit code.
3. Add valid/invalid fixtures and `tests/test_validator.py` + a `validate` CLI test
   (assert exit code via `main([...])`).

## Example command / output

```bash
agent-md-query validate <path>
```

```text
OK: <path>/task-001.md
MISSING: <path>/task-002.md -> updated_at
MISSING: <path>/task-003.md -> project, priority
```

## Test plan

- `missing_fields`: complete metadata → `[]`; partial → the absent fields in schema order;
  empty/`None` values count as missing.
- A fully-valid fixture set → exit code 0.
- A set containing an invalid file → reported `MISSING:` line and exit code 1.
- File without Front Matter → all recommended fields reported missing (does not crash).

## Risks

- **Exit code wiring**: `main` must propagate the non-zero code from `run_validate`. Test
  through `main([...])`, not just the helper.
- **Empty vs missing**: decide and document that empty-string/`None` values count as missing
  so `status:` with no value is caught.
- **Scope creep**: value validation (allowed `status`/`priority` sets) and configurable
  schema are out of scope for this issue.

## Out of scope

- Configurable / external schema, value/enum validation, auto-fixing, JSON output for
  validate. Later issues.

## Acceptance criteria (from issue)

- `validate` command exists.
- Missing recommended fields are reported.
- Valid files pass validation.
- Invalid files are reported clearly.
- Non-zero exit code is returned when validation fails.
- Tests cover valid and invalid examples.
