# Examples

Sample Markdown files for trying `agent-md-query`. They live under
`examples/workboard/tasks/` and use consistent YAML Front Matter so the same set
demonstrates every command.

The point of the tool is the **metadata-first workflow**:

1. Query metadata first.
2. Read only the matching Markdown files.
3. Avoid spending tokens on files you do not need.

All commands below are runnable from the repository root, and the output shown is
the actual output.

## Sample files

| File | project | status | priority | tags |
|---|---|---|---|---|
| `task-20260607-001.md` | ai-hisho-os | doing | high | token-budget, dispatch |
| `task-20260607-002.md` | ai-hisho-os | todo | medium | dispatch |
| `task-20260607-003.md` | dev-access-manager | doing | medium | docs |

(`task-20260607-003.md` intentionally omits `updated_at` to demonstrate `validate`.)

## `list` — filter by metadata

```bash
agent-md-query list examples/workboard/tasks --where status=doing --format markdown
```

```markdown
# Query Result

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `examples/workboard/tasks/task-20260607-001.md`
  - assignee: codex
  - updated_at: 2026-06-07

## dev-access-manager

- doing / medium: Add Docker Test Environment
  - file: `examples/workboard/tasks/task-20260607-003.md`
```

### `--format paths` — the agent workflow

The most useful format for agents: feed the matching paths straight into the next
read step.

```bash
agent-md-query list examples/workboard/tasks --where project=ai-hisho-os --where status!=done --format paths
```

```text
examples/workboard/tasks/task-20260607-001.md
examples/workboard/tasks/task-20260607-002.md
```

### `--tag` — filter by tag

```bash
agent-md-query list examples/workboard/tasks --tag token-budget --format paths
```

```text
examples/workboard/tasks/task-20260607-001.md
```

`--tag` and `--where` combine with AND, and multiple `--tag` flags also combine
with AND.

## `summary` — group an overview by a field

```bash
agent-md-query summary examples/workboard/tasks --group-by project
```

```markdown
# Summary

## ai-hisho-os

- doing / high: Codex Token Budget Review
  - file: `examples/workboard/tasks/task-20260607-001.md`
- todo / medium: Improve Dispatch Template
  - file: `examples/workboard/tasks/task-20260607-002.md`

## dev-access-manager

- doing / medium: Add Docker Test Environment
  - file: `examples/workboard/tasks/task-20260607-003.md`
```

## `validate` — check recommended fields

Checks for `type`, `id`, `project`, `status`, `priority`, `updated_at`. Exits with a
non-zero status when any file is missing a recommended field.

```bash
agent-md-query validate examples/workboard/tasks
```

```text
OK: examples/workboard/tasks/task-20260607-001.md
OK: examples/workboard/tasks/task-20260607-002.md
MISSING: examples/workboard/tasks/task-20260607-003.md -> updated_at
```
