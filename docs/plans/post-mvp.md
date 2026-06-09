# Post-MVP outline (issues #5, #6, #8, #9)

> **Status update**: the MVP (#1–#4) is implemented and merged into `main`. Each issue below
> now has a **detailed plan** grounded in the merged interfaces:
> [issue-005](issue-005-tag-filtering.md), [issue-006](issue-006-summary-group-by.md),
> [issue-008](issue-008-validate.md), [issue-009](issue-009-fixtures-docs.md).
> This file remains the lighter outline + sequencing rationale. Still implement only on
> explicit request, one issue per PR.

These issues were **out of scope for the MVP**. This file captures intent at a lighter level
than the per-issue plans, so the order and shape stay clear.

The MVP package structure now exists, so every item below builds on real
`scanner` / `matcher` / `formatter` / `cli` interfaces.

## Sequencing

```text
MVP (#1–#4)
  ├── #5 tag filtering            (v0.2) — extends matcher + list
  ├── #6 summary --group-by       (v0.2) — new command, reuses scanner
  └── #8 validate                 (v0.3) — new command, reuses scanner
#9 fixtures & docs examples       — cross-cutting; grow alongside #2–#4, finalize after #4
```

#5, #6, and #8 are independent of each other (all depend only on the scanner). #9 is
cross-cutting and is best advanced incrementally as #2–#4 land.

## #5 — Tag filtering (v0.2)

- Add `--tag <name>` to `list`; match against list-style `tags` Front Matter.
- Combine with `--where` (AND); support multiple `--tag` filters if practical.
- Files without `tags` are handled safely (no match, no crash).
- Lives in `matcher.py`; keep tag handling simple (no tag expression language yet).
- Tests: matching, non-matching, missing `tags`, `--tag` + `--where` together.

## #6 — `summary` with `--group-by` (v0.2)

- Add `agent-md-query summary <path> --group-by <field>`.
- Group scanner results by a Front Matter field; render a concise Markdown summary that
  includes file paths. Handle missing group values safely.
- Reuses `scanner` and the Markdown rendering approach from `formatter.py`.
- Tests: grouping behavior, missing group values.

## #8 — `validate` command (v0.3)

- Add `agent-md-query validate <path>` checking recommended Front Matter fields:
  `type`, `id`, `project`, `status`, `priority`, `updated_at`.
- Report missing fields; report invalid values where practical.
- Return a non-zero exit code when validation fails.
- Start with a simple built-in recommended schema; configurable schema is a later issue.
- Tests: valid fixtures pass; invalid fixtures report clearly; non-zero exit on failure.

## #9 — Fixtures and documentation examples (cross-cutting)

- Add an `examples/` directory and sample task/project Markdown files.
- Align `tests/fixtures/` with the examples where practical.
- Keep README examples consistent with actual command behavior.
- Reinforce the metadata-first workflow: query first, read only matching files.
- Practically: fixtures are created during #2–#4 already; this issue consolidates them into
  a coherent `examples/` set and verifies README parity once formats (#4) are stable.

## Not planned at all (hard non-goals)

From `.claude/rules/00-project-overview.md` — do not introduce these even as scaffolding:
SQLite index cache, vector search, embeddings, semantic ranking, long-running daemon, web
server, complex query language, AI API integration, Obsidian plugin behavior, and any
ai-hisho-os-specific behavior.
