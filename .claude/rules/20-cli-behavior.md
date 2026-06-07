---
paths:
  - "src/agent_md_query/cli.py"
  - "src/agent_md_query/matcher.py"
  - "src/agent_md_query/formatter.py"
  - "tests/test_cli.py"
  - "tests/test_matcher.py"
  - "tests/test_formatter.py"
---

# CLI Behavior Rules

## MVP Commands

The MVP focuses on:

~~~bash
agent-md-query list <path>
~~~

Do not implement `summary`, `validate`, or tag filtering before the MVP unless explicitly requested.

## List Command

The `list` command should support:

~~~bash
agent-md-query list workboard/tasks --where status=doing
agent-md-query list workboard/tasks --where project=ai-hisho-os --where status!=done
~~~

Multiple `--where` conditions are AND conditions.

## Where Syntax

Support these patterns in the MVP:

| Pattern | Meaning |
|---|---|
| `key=value` | metadata field equals value |
| `key!=value` | metadata field does not equal value |

Keep parsing simple. Do not add a complex expression language.

## Missing Keys

For normal query behavior:

- `key=value` should not match when the key is missing.
- `key!=value` may match when the key is missing, unless a clearer rule is already documented.
- Do not crash on missing keys.

If this behavior is changed, document and test it.

## Output Formats

Support:

~~~bash
--format markdown
--format json
--format paths
~~~

Default format:

~~~text
markdown
~~~

## Markdown Output

Markdown output should be readable by humans and AI agents.

Example shape:

~~~markdown
# Query Result

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `workboard/tasks/task-20260607-001.md`
  - assignee: codex
  - updated_at: 2026-06-07
~~~

## JSON Output

JSON output should be script-friendly.

Use stable field names such as:

- `title`
- `project`
- `status`
- `priority`
- `assignee`
- `updated_at`
- `file_path`

## Paths Output

`paths` is the most important format for AI-agent workflows.

Example:

~~~text
workboard/tasks/task-20260607-001.md
workboard/tasks/task-20260607-002.md
~~~

Keep paths output minimal. Do not add bullets, headings, or explanations.
