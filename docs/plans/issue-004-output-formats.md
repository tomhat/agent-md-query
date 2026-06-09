# Plan: Issue #4 — Output formats: markdown, json, paths

- Issue: Add output formats: markdown, json, and paths
- Depends on: #3
- Status: planned

## Goal

Add `--format markdown|json|paths` to `list`, defaulting to `markdown`, so the tool serves
humans, scripts, and AI-agent read workflows.

## Scope

- Add `--format markdown`, `--format json`, `--format paths`.
- Default to `markdown`.
- Include file paths in all formats.
- Add tests for each output format.

## Design

`src/agent_md_query/formatter.py` — pure rendering, one function per format, selected by a
small dispatch. Format only at the edge; the matcher returns plain data.

### markdown (default)

Human- and agent-readable. Group by `project` (the example shape), then list items.

```markdown
# Query Result

## <project>

- <status> / <priority>: <title>
  - file: `<file_path>`
  - assignee: <assignee>
  - updated_at: <updated_at>
```

- Missing `project` → a stable fallback group (e.g. `(no project)`).
- Omit optional sub-lines (`assignee`, `updated_at`) when the field is absent.

### json

Script-friendly. A JSON array of objects with stable field names (per
`.claude/rules/20-cli-behavior.md`): `title`, `project`, `status`, `priority`, `assignee`,
`updated_at`, `file_path`. Use `json.dumps(..., ensure_ascii=False, indent=2)`. Decide and
document how non-listed metadata is handled (recommended: include the listed stable fields;
keep it predictable).

### paths

The most important format for AI-agent workflows. One `file_path` per line, nothing else —
no bullets, headings, or explanations.

```text
<path>/task-001.md
<path>/task-002.md
```

## Tasks

1. Add `formatter.py` with `format_markdown`, `format_json`, `format_paths`, and a
   `render(results, fmt)` dispatch.
2. Add `--format` to the `list` subcommand (`choices=["markdown","json","paths"]`,
   `default="markdown"`); replace the placeholder output from #3.
3. Add `tests/test_formatter.py`; extend `test_cli.py` for each `--format` value.
4. Verify README output examples match actual output; reconcile per
   `.claude/rules/40-testing-docs.md` (fix code or fix README).

## Test plan

- `test_formatter.py`:
  - `markdown`: grouping by project, fallback group for missing project, optional sub-lines
    omitted when absent.
  - `json`: valid JSON, stable field names, `file_path` present, expected ordering.
  - `paths`: only paths, one per line, no extra characters.
- `test_cli.py`: `--format` default is `markdown`; each explicit value produces the
  corresponding shape.

## Risks

- **README drift**: examples in README must run as written. Adjust whichever side is wrong.
- **JSON field selection**: if a file lacks a stable field, decide null vs omit and keep it
  consistent across files. Document the choice.
- **Output stability**: keep ordering deterministic (rely on the scanner's sorted results)
  so agents and scripts get stable output.

## Out of scope

- `--tag` (#5), `summary` (#6), `validate` (#8). MVP ends here (v0.1).

## Acceptance criteria (from issue)

- `--format markdown`, `--format json`, `--format paths` all work.
- Default output is Markdown.
- Output is stable enough for AI agents and scripts.
- Tests cover all output formats.
