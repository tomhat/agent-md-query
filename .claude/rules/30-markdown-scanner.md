---
paths:
  - "src/agent_md_query/scanner.py"
  - "src/agent_md_query/matcher.py"
  - "tests/test_scanner.py"
  - "tests/fixtures/**/*.md"
  - "tests/fixtures/**/*.markdown"
  - "examples/**/*.md"
  - "examples/**/*.markdown"
---

# Markdown Scanner Rules

## Supported Files

The scanner should recursively scan:

- `.md`
- `.markdown`

Do not scan unrelated file types.

## Front Matter

The tool targets Markdown files with YAML Front Matter.

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

## Common Metadata Fields

Common fields include:

| Field | Meaning |
|---|---|
| `type` | `task`, `project`, `note`, `decision`, etc. |
| `id` | stable identifier |
| `project` | project name or ID |
| `status` | `todo`, `doing`, `blocked`, `done`, etc. |
| `priority` | `high`, `medium`, `low`, etc. |
| `assignee` | human or AI executor |
| `updated_at` | last updated date |
| `tags` | list of tags |

Do not assume every field exists.

## Safe Degradation

For normal query commands:

- Files without Front Matter should not crash the tool.
- Missing metadata should not crash the tool.
- Malformed YAML should produce a clear error or warning.
- File read errors should produce a clear error.

Prefer predictable behavior over clever recovery.

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

## Internal Result Shape

Internally, scanner results should contain at least:

- metadata
- title
- file path

Keep the internal structure simple and easy to test.
