# agent-md-query

A tiny CLI that helps AI agents query structured Markdown before reading files.

Stop wasting tokens reading every Markdown file. Query the metadata first.

## Why?

AI agents often waste tokens by reading too many Markdown files.

`agent-md-query` lets agents filter Markdown files by YAML Front Matter first, then read only the files they actually need.

This helps agent workflows become:

- Cheaper
- Faster
- More deterministic
- Less noisy
- Easier to review

## Background

`agent-md-query` was originally created for [`ai-hisho-os`](https://github.com/tomhat/ai-hisho-os), a Markdown-first AI secretary OS experiment.

In that project, AI agents manage workboards, tasks, state, memory, and history as Markdown files.

However, letting agents read all Markdown files every time can waste tokens and introduce unnecessary context noise.

The same problem appears in many agent-based workflows:

- Obsidian vaults
- Git-managed knowledge bases
- Markdown task boards
- Codex projects
- Claude Code projects
- Cursor workspaces
- Local AI agent environments

`agent-md-query` is designed as a small, reusable tool for these workflows.

## Concept

Before:

```text
AI agent reads many Markdown files
↓
High token usage
↓
Slow and noisy context
```

After:

```text
agent-md-query filters files by Front Matter
↓
AI agent reads only relevant files
↓
Lower token usage and cleaner context
```

## Features

- Query Markdown files by YAML Front Matter
- Output results as Markdown, JSON, or file paths
- Designed for AI agents such as Codex, Claude Code, Cursor, and local agents
- Works well with Obsidian-style Markdown
- No database required for the first version
- Optional SQLite index planned for future versions

## Example

Given Markdown files like this:

```markdown
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
```

You can query them before asking an AI agent to read the full file:

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format markdown
```

Example output:

```markdown
# Query Result

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `examples/workboard/tasks/task-20260607-001.md`
  - assignee: codex
  - updated_at: 2026-06-07
```

Then the AI agent can read only the matching file instead of scanning the whole `workboard/` directory.

## Installation

PyPI release is not available yet.

Local development:

```bash
git clone https://github.com/tomhat/agent-md-query.git
cd agent-md-query
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m agent_md_query --help
```

Planned installation method:

```bash
pip install agent-md-query
```

## Usage

Available commands (v0.1):

```bash
agent-md-query list examples/workboard/tasks --where status=doing
agent-md-query list examples/workboard/tasks --where project=ai-hisho-os --where status!=done
```

Output formats:

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format markdown
agent-md-query list examples/workboard/tasks --where status=doing --format json
agent-md-query list examples/workboard/tasks --where status=doing --format paths
```

Filter by tag:

```bash
agent-md-query list examples/workboard/tasks --tag token-budget
agent-md-query list examples/workboard/tasks --where status=doing --tag dispatch
```

Planned commands (post-MVP):

```bash
agent-md-query summary examples/workboard/tasks --group-by project
agent-md-query validate examples/workboard/tasks
```

## Commands

### `list`

List Markdown files that match Front Matter conditions.

```bash
agent-md-query list examples/workboard/tasks --where status=doing
```

Multiple conditions:

```bash
agent-md-query list examples/workboard/tasks --where project=ai-hisho-os --where status!=done
```

Filter by tag:

```bash
agent-md-query list examples/workboard/tasks --tag token-budget
agent-md-query list examples/workboard/tasks --where status=doing --tag dispatch
```

### `summary`

Summarize matching Markdown files.

```bash
agent-md-query summary examples/workboard/tasks --group-by project
```

### `validate`

Validate Front Matter fields (planned).

```bash
agent-md-query validate examples/workboard/tasks
```

## Front Matter Schema

`agent-md-query` does not require a fixed schema, but it works best when Markdown files use consistent YAML Front Matter.

Recommended fields for task-like Markdown files:

```yaml
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
```

Common fields:

| Field | Description |
|---|---|
| `type` | Document type, such as `task`, `project`, `note`, or `decision` |
| `id` | Stable identifier |
| `project` | Project name or project id |
| `status` | Workflow status, such as `todo`, `doing`, `blocked`, or `done` |
| `priority` | Priority value, such as `high`, `medium`, or `low` |
| `assignee` | Human or agent responsible for the item |
| `updated_at` | Last updated date |
| `tags` | List of tags |

## Output Formats

### Markdown

Best for AI agents and human-readable summaries.

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format markdown
```

Example:

```markdown
# Query Result

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `examples/workboard/tasks/task-20260607-001.md`
  - assignee: codex
  - updated_at: 2026-06-07
```

### JSON

Best for scripts and integrations.

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format json
```

Example:

```json
[
  {
    "title": "Codex Token Budget Review",
    "project": "ai-hisho-os",
    "status": "doing",
    "priority": "high",
    "assignee": "codex",
    "updated_at": "2026-06-07",
    "file_path": "examples/workboard/tasks/task-20260607-001.md"
  }
]
```

### Paths

Best when the next step is reading only matching files.

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format paths
```

Example:

```text
examples/workboard/tasks/task-20260607-001.md
```

## AI Agent Usage Pattern

Recommended pattern for AI agents:

```text
1. Query metadata first.
2. Read only matching Markdown files.
3. Use the full file content only when needed.
```

For example:

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format paths
```

Then read only the returned files.

This avoids scanning large Markdown directories and reduces unnecessary context.

## Relationship with ai-hisho-os

`ai-hisho-os` is the original use case for this tool.

In `ai-hisho-os`, Markdown files are used to manage:

- Workboards
- Tasks
- State
- Memory
- History
- Agent handoff information

`agent-md-query` is intended to help AI agents work with those Markdown files more efficiently.

However, this tool is not specific to `ai-hisho-os`. It can be used with any Markdown-based knowledge base or task system that uses YAML Front Matter.

## Roadmap

### v0.1

- Recursively scan `.md` and `.markdown` files
- Parse YAML Front Matter
- Support `--where key=value`
- Support `--where key!=value`
- Support `--tag`
- Support `--format markdown|json|paths`

### v0.2

- Add `summary`
- Add `--group-by`
- Add sorting
- Add `--limit`

### v0.3

- Add schema validation
- Add required field checks
- Add status and priority validation

### v0.4

- Optional SQLite index cache
- Faster repeated queries
- Index refresh command

### v0.5

- AI agent instruction templates
- AGENTS.md usage examples
- Integration examples for Codex, Claude Code, Cursor, and local agents

## Design Principles

### Markdown-first

Markdown remains the source of truth.

`agent-md-query` only helps agents find relevant files before reading them.

### Metadata-first

Structured metadata should be queried before full text is read.

### Agent-friendly

Outputs should be easy for AI agents to consume.

### No database required

The first version should work directly on Markdown files.

A SQLite index may be added later as an optional cache.

## License

MIT