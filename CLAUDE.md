# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

`agent-md-query` is a tiny CLI that helps AI agents query structured Markdown before reading full files.

The core idea is:

> Stop wasting tokens reading every Markdown file. Query the metadata first.

This project was originally inspired by `tomhat/ai-hisho-os`, but it should be developed as a general-purpose OSS tool for AI agents, Obsidian vaults, Git-managed knowledge bases, Markdown task boards, Codex, Claude Code, Cursor, and local agent environments.

## Core Concept

`agent-md-query` is not a semantic search tool.

It is a structured metadata query tool for Markdown files that use YAML Front Matter.

Use this distinction consistently:

| Tool | Role |
|---|---|
| Cursor | Semantic search and vague context discovery |
| agent-md-query | Exact structured filtering by Front Matter |
| Local LLM | Low-cost reading and summarization |
| Codex / Claude Code | Implementation, tests, and PRs |
| Higher-end models | Design decisions and final review |

The project should follow this principle:

> Programs extract. AI interprets. Stronger AI decides.

## Primary Goal

The MVP goal is to make it possible for an AI agent to do this:

1. Query Markdown metadata first.
2. Get only the relevant file paths.
3. Read only those files.
4. Reduce token usage and avoid unnecessary context loading.

The most important value is:

> Filter candidate Markdown files before asking an AI to read them.

## MVP Scope

The initial MVP is GitHub Issues #1 to #4.

| Issue | Scope |
|---|---|
| #1 | Set up Python package scaffold |
| #2 | Implement Markdown scanner and Front Matter parser |
| #3 | Implement list command with `--where` filters |
| #4 | Add output formats: `markdown`, `json`, and `paths` |

Do not implement later features before the MVP is stable unless explicitly instructed.

Later issues include:

| Issue | Scope |
|---|---|
| #5 | Add tag filtering |
| #6 | Add summary command with `--group-by` support |
| #8 | Add validate command for Front Matter fields |
| #9 | Add fixtures and documentation examples |

Issue #7 was a duplicate of #6 and should not be implemented separately.

## Development Policy

Prefer small, reviewable changes.

Do not do a large implementation sweep unless explicitly requested.

When working on an issue:

1. Read the issue.
2. Check the README.
3. Identify the minimum required change.
4. Implement only that scope.
5. Add or update tests.
6. Run tests if possible.
7. Report what changed and what was not changed.

If requirements are ambiguous, choose the smallest behavior that supports the README and MVP.

## Implementation Defaults

Use these defaults unless the repository already contains a different established choice.

| Item | Default |
|---|---|
| Language | Python |
| Package layout | `src/agent_md_query/` |
| CLI library | `argparse` |
| Test framework | `pytest` |
| YAML parser | `PyYAML` is acceptable |
| Initial storage | Direct Markdown file scanning |
| SQLite | Do not add in MVP |
| Default output format | `markdown` |
| Important output format | `paths` |

Avoid unnecessary dependencies.

Do not add SQLite, indexing, semantic search, vector search, or background daemon behavior in the MVP.

## Expected Repository Structure

The target structure for the MVP is approximately:

~~~text
agent-md-query/
  README.md
  LICENSE
  pyproject.toml
  CLAUDE.md
  src/
    agent_md_query/
      __init__.py
      __main__.py
      cli.py
      scanner.py
      matcher.py
      formatter.py
  tests/
    fixtures/
      tasks/
        task-001.md
        task-002.md
    test_cli.py
    test_scanner.py
    test_matcher.py
    test_formatter.py
~~~

This structure is a guide, not a strict requirement. Keep changes consistent with the actual repository.

## Markdown Format Assumption

The tool should target Markdown files with YAML Front Matter.

Example:

~~~markdown
---
type: task
id: task-20260607-001
project: ai-hisho-os
status: doing
priority: high
assignee: codex
updated_at: 2026-06-07
tags:
  - token-budget
  - dispatch
---

# Codex Token Budget Review

Review and reduce token usage when delegating work from one Codex session to another.
~~~

Common fields:

| Field | Meaning |
|---|---|
| `type` | `task`, `project`, `note`, `decision`, etc. |
| `id` | Stable identifier |
| `project` | Project name or ID |
| `status` | `todo`, `doing`, `blocked`, `done`, etc. |
| `priority` | `high`, `medium`, `low`, etc. |
| `assignee` | Human or AI executor |
| `updated_at` | Last updated date |
| `tags` | List of tags |

The parser should not assume every field exists.

## Scanner Behavior

The scanner should eventually support:

- Recursively scanning `.md` and `.markdown` files.
- Reading YAML Front Matter when present.
- Returning metadata, title, and file path.
- Handling files without Front Matter without crashing.
- Handling malformed YAML gracefully.

For MVP behavior, prefer safe degradation over hard failure unless a command specifically validates metadata.

## Title Extraction

Preferred title extraction order:

1. First Markdown H1 after Front Matter.
2. File stem as fallback.

Example:

~~~markdown
# Codex Token Budget Review
~~~

should produce:

~~~text
Codex Token Budget Review
~~~

If no H1 exists, use the filename without extension.

## List Command

The `list` command should support:

~~~bash
agent-md-query list workboard/tasks --where status=doing
agent-md-query list workboard/tasks --where project=ai-hisho-os --where status!=done
~~~

Multiple `--where` conditions should be treated as AND.

Supported operators for MVP:

| Pattern | Meaning |
|---|---|
| `key=value` | metadata field equals value |
| `key!=value` | metadata field does not equal value |

Keep parsing simple and predictable.

Do not implement complex expression parsing in MVP.

## Output Formats

The command should support:

~~~bash
--format markdown
--format json
--format paths
~~~

Default format:

~~~text
markdown
~~~

### Markdown Output

Human and AI-readable summary.

Example:

~~~markdown
# Query Result

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `workboard/tasks/task-20260607-001.md`
  - assignee: codex
  - updated_at: 2026-06-07
~~~

### JSON Output

Script-friendly output.

Example:

~~~json
[
  {
    "title": "Codex Token Budget Review",
    "project": "ai-hisho-os",
    "status": "doing",
    "priority": "high",
    "assignee": "codex",
    "updated_at": "2026-06-07",
    "file_path": "workboard/tasks/task-20260607-001.md"
  }
]
~~~

### Paths Output

The most important format for AI-agent workflows.

Example:

~~~text
workboard/tasks/task-20260607-001.md
workboard/tasks/task-20260607-002.md
~~~

This lets an AI agent read only the files returned by the query.

## Tag Filtering

Tag filtering belongs to Issue #5, not the initial MVP unless explicitly requested.

Expected future usage:

~~~bash
agent-md-query list workboard/tasks --tag token-budget
agent-md-query list workboard/tasks --where status=doing --tag dispatch
~~~

Tags are expected to be stored as a YAML list.

## Summary Command

The `summary` command belongs to Issue #6.

Expected future usage:

~~~bash
agent-md-query summary workboard/tasks --group-by project
~~~

Do not implement summary before the MVP unless explicitly instructed.

## Validate Command

The `validate` command belongs to Issue #8.

Expected future behavior:

- Check recommended Front Matter fields.
- Report missing fields.
- Return a non-zero exit code when validation fails.

Recommended fields:

~~~text
type
id
project
status
priority
updated_at
~~~

Do not make these fields mandatory for normal `list` queries.

## Error Handling Philosophy

For normal query commands:

- Missing Front Matter should not crash the tool.
- Missing metadata keys should simply not match positive filters.
- Malformed YAML should be reported clearly.
- File read errors should be reported clearly.
- Avoid noisy stack traces for normal user errors.

For validation commands:

- It is acceptable to return non-zero exit codes.
- Report actionable messages.

## Testing Policy

Add tests for new behavior.

Prefer small fixture files under:

~~~text
tests/fixtures/
~~~

Useful test cases:

- Markdown with valid Front Matter.
- Markdown without Front Matter.
- Markdown with H1 title.
- Markdown without H1 title.
- `--where key=value`
- `--where key!=value`
- Multiple `--where` filters.
- `markdown` output.
- `json` output.
- `paths` output.

Do not rely on network access in tests.

## CLI Expectations

The following should work after Issue #1:

~~~bash
python -m agent_md_query --help
~~~

If console scripts are configured, this should also work:

~~~bash
agent-md-query --help
~~~

The following should work by the end of Issue #4:

~~~bash
agent-md-query list tests/fixtures/tasks --where status=doing
agent-md-query list tests/fixtures/tasks --where status=doing --format json
agent-md-query list tests/fixtures/tasks --where status=doing --format paths
~~~

## Documentation Policy

Keep README examples aligned with actual CLI behavior.

If implementation behavior differs from README examples, either:

1. Update the implementation to match the README, or
2. Update the README if the implementation choice is intentionally better.

Do not leave examples that cannot run.

## AI Agent Usage Pattern

This project should support workflows like:

~~~bash
agent-md-query list workboard/tasks --where status=doing --format paths
~~~

Then the AI agent reads only the returned files.

This is the central workflow. Preserve it.

## Relationship with ai-hisho-os

`ai-hisho-os` is the origin and an important use case, but `agent-md-query` should not become tightly coupled to it.

Avoid hard-coding:

- `ai-hisho-os`
- `workboard`
- `history`
- `memory`
- `dispatch`
- specific project names
- specific task IDs

Use them only as examples.

The tool should work for any Markdown repository that uses YAML Front Matter.

## Design Principles

Follow these principles:

1. Metadata first.
2. Plain Markdown.
3. Git-friendly.
4. Small CLI.
5. No database in MVP.
6. No semantic search in MVP.
7. Useful for humans and AI agents.
8. Stable, predictable output.
9. Minimal dependencies.
10. Easy to test.

## What Not To Do

Do not add these in MVP:

- SQLite index cache.
- Vector search.
- Embedding generation.
- Semantic ranking.
- Long-running daemon.
- Web server.
- Complex query language.
- AI API integration.
- Obsidian plugin behavior.
- ai-hisho-os-specific hard coding.

These may be future ideas, but they are not MVP requirements.

## Commit and PR Guidance

Use focused commits.

Good commit examples:

~~~text
Add Python package scaffold
Implement Markdown front matter scanner
Add list command filters
Add output formatters
~~~

Avoid broad commits like:

~~~text
Implement everything
Update project
Misc changes
~~~

When opening a PR, include:

- Summary
- Related issue
- Tests run
- Notes or limitations

Example PR body:

~~~markdown
## Summary

- Added initial Python package scaffold
- Added CLI entry point
- Added minimal help command test

## Related Issue

Closes #1

## Tests

- `pytest`

## Notes

Markdown scanning is intentionally not implemented in this PR.
~~~

## Work Reporting

When reporting back, include:

1. What changed.
2. What tests were run.
3. What was intentionally not changed.
4. Any follow-up issue.

Example:

~~~markdown
## Done

- Added `pyproject.toml`
- Added `src/agent_md_query/`
- Added CLI help entry point
- Added minimal CLI test

## Tests

- `pytest`

## Not included

- Markdown scanning
- Front Matter parsing
- `list` command

These belong to later issues.
~~~

## Current Priority

Start with Issue #1 unless instructed otherwise.

Issue #1 scope:

- `pyproject.toml`
- `src/agent_md_query/`
- `__init__.py`
- `__main__.py`
- `cli.py`
- `tests/`
- `python -m agent_md_query --help`
- Optional console script: `agent-md-query --help`
- Minimal test

Do not implement Markdown search logic in Issue #1.
