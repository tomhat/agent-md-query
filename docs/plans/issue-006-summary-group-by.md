# Plan: Issue #6 — `summary` command with `--group-by`

- Issue: Add summary command with --group-by support
- Roadmap: v0.2
- Depends on: MVP (#2 scanner, #4 formatter) — merged
- Status: planned

## Goal

Add `agent-md-query summary <path> --group-by <field>` that groups Markdown metadata by a
field and prints a concise Markdown overview (with file paths) so an agent can survey a set
before reading any full file.

## Current code to build on

- `scanner.scan(path)` returns `list[dict]` with `file_path`, `title`, `metadata`.
- `formatter.format_markdown` already groups results by the hard-coded `project` field and
  renders `## <group>` then `- <status> / <priority>: <title>` with a `  - file:` line.
  Reuse this grouping shape, generalized to an arbitrary field.

## Design

Add a grouped Markdown renderer to `formatter.py` rather than overloading `format_markdown`:

```python
def format_summary(results: list[dict], group_by: str) -> str:
    """Group results by metadata[group_by] and render a Markdown summary."""
```

- Heading: `# Summary` (the `list` markdown uses `# Query Result`; keep them distinct).
- Group key: `str(metadata.get(group_by))`; missing/empty value → a stable fallback bucket,
  e.g. `(no <group_by>)`, sorted last (mirror the existing `NO_PROJECT` ordering trick).
- Per item: reuse the folded `status / priority: title` header from #4 plus the
  `  - file:` line. Keep the optional sub-lines minimal (file path is required by the issue;
  assignee/updated_at optional).
- Consider extracting a small private helper `_group(results, field, fallback)` shared by
  `format_markdown` and `format_summary`. Only extract if it stays simple — do not refactor
  `format_markdown`'s public behavior (no unnecessary churn per `.claude/rules`).

Add a `summary` subcommand to `cli.py`:

- `summary <path> --group-by <field>` (`--group-by` required).
- `run_summary(path, group_by)`: `scan` → `format_summary` → print. Reuse the same
  `FileNotFoundError` → exit 1 handling as `run_list`.
- Output is Markdown only for now (the issue specifies a Markdown summary; no `--format`).

## Tasks

1. Add `format_summary` (and optional shared `_group` helper) to `formatter.py`.
2. Add the `summary` subcommand + `run_summary` to `cli.py`; dispatch in `main`.
3. Add `tests/test_formatter.py` cases and a `summary` integration test in `test_cli.py`.

## Example command / output

```bash
agent-md-query summary <path> --group-by project
```

```markdown
# Summary

## <project-a>

- doing / high: Token Budget Review
  - file: `<path>/task-001.md`

## (no project)

- todo / medium: Loose note
  - file: `<path>/note.md`
```

## Test plan

- Grouping by a present field produces one section per distinct value.
- Missing group values fall into the fallback bucket and do not crash.
- File paths appear under each item.
- Heading is `# Summary`; empty results produce a stable minimal output (`# Summary\n`).

## Risks

- **Grouping reuse**: tempting to refactor `format_markdown` to share code. Keep changes
  additive; only extract a helper if it does not change `list` output.
- **Group key types**: `group_by` may target non-string values (ints/dates) — stringify the
  key for the heading, consistent with the matcher's string comparison rule.

## Out of scope

- Sorting options, `--limit`, multiple group-by fields, non-Markdown summary formats. These
  are later v0.2+ items, not this issue.

## Acceptance criteria (from issue)

- `summary` command exists.
- `--group-by` option works.
- Markdown summary output is generated.
- Tests cover grouping behavior.
