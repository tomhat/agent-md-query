# Development Plan: agent-md-query

This directory holds the implementation plans for `agent-md-query`, derived from the
GitHub issues. Plans describe **how** each issue will be implemented before any code is
written. Issues describe **what** to do; plans describe **how**.

Read this overview first, then the per-issue plan together with the issue itself and the
relevant file under `.claude/rules/`.

## Product goal

> Filter candidate Markdown files by metadata (YAML Front Matter) before asking an AI to
> read them.

`agent-md-query` is a deterministic metadata query tool, not a semantic search tool. The
CLI extracts and filters; it does not interpret meaning. Protect this central workflow:

```bash
agent-md-query list <path> --where status=doing --format paths
```

## MVP boundary

The MVP is **issues #1–#4** only. Everything else is post-MVP and must not be built unless
explicitly requested.

### MVP (v0.1) — implemented and merged

| Issue | Title | Plan | Status |
|---|---|---|---|
| #1 | Set up Python package scaffold | [issue-001-package-scaffold.md](issue-001-package-scaffold.md) | done |
| #2 | Implement Markdown scanner and Front Matter parser | [issue-002-scanner.md](issue-002-scanner.md) | done |
| #3 | Implement `list` command with `--where` filters | [issue-003-list-where.md](issue-003-list-where.md) | done |
| #4 | Add output formats: markdown, json, paths | [issue-004-output-formats.md](issue-004-output-formats.md) | done |

### Post-MVP — planned

Each has a detailed plan grounded in the merged MVP interfaces. A lighter outline and the
sequencing rationale live in [post-mvp.md](post-mvp.md).

| Issue | Title | Plan | Roadmap |
|---|---|---|---|
| #5 | Add tag filtering (`--tag`) | [issue-005-tag-filtering.md](issue-005-tag-filtering.md) | v0.2 |
| #6 | Add `summary` with `--group-by` | [issue-006-summary-group-by.md](issue-006-summary-group-by.md) | v0.2 |
| #8 | Add `validate` command | [issue-008-validate.md](issue-008-validate.md) | v0.3 |
| #9 | Fixtures and documentation examples | [issue-009-fixtures-docs.md](issue-009-fixtures-docs.md) | cross-cutting |

Explicitly **not** in the project at all (see `.claude/rules/00-project-overview.md`):
SQLite index, vector/semantic search, embeddings, daemon, web server, complex query
language, AI API integration, Obsidian plugin behavior, ai-hisho-os-specific behavior.

## Sequencing and dependencies

```text
#1 scaffold
  └── #2 scanner ──┐
                   ├── #3 list --where ── #4 output formats
                   └──────────────────────┘
```

- #1 has no dependencies. It only sets up the package, CLI entry point, and test harness.
- #2 depends on #1. It is the core (scan files, parse Front Matter, extract title) and is
  pure library code with no CLI flags.
- #3 depends on #2. It wires the scanner into a `list` command and adds `--where`.
- #4 depends on #3. It adds `--format markdown|json|paths` (default `markdown`).

Implement strictly in this order. Each issue should land as a small, reviewable change with
its own tests.

## Target package structure (end of MVP)

```text
agent-md-query/
  pyproject.toml
  src/
    agent_md_query/
      __init__.py
      __main__.py
      cli.py          # argparse, dispatch only
      scanner.py      # find files, parse Front Matter, extract title
      matcher.py      # --where evaluation
      formatter.py    # markdown / json / paths rendering
  tests/
    fixtures/
    test_cli.py
    test_scanner.py
    test_matcher.py
    test_formatter.py
  docs/
    plans/
```

This is a guide, not a hard requirement. Keep the structure simple and consistent with
`.claude/rules/10-python-package.md`.

## Cross-cutting conventions

These apply to every issue (see `.claude/rules/`):

- **Stack**: Python, `src/agent_md_query/` layout, `argparse`, `pytest`, `PyYAML` for YAML.
  Avoid unnecessary dependencies.
- **Architecture**: pure functions in scanner / matcher / formatter; keep CLI parsing
  separate from business logic; format output only at the edge; no hidden global state.
- **Generality**: never hard-code `ai-hisho-os`, `workboard`, project names, or task IDs in
  source. They may appear only in examples, fixtures, and docs.
- **Safe degradation**: files without Front Matter, missing keys, and malformed YAML must
  not crash the tool. Prefer predictable behavior over clever recovery.
- **Tests**: add/update `pytest` tests with every behavior change. No network in tests.
- **Docs**: keep README examples runnable and aligned with actual CLI behavior.

## Design decision log (MVP-level)

| Decision | Choice | Rationale | Revisit when |
|---|---|---|---|
| CLI library | `argparse` (stdlib) | No extra dependency; MVP needs only simple subcommands and flags | Sub-command set grows large or needs rich help/validation |
| YAML parser | `PyYAML` (`yaml.safe_load`) | De-facto standard; `safe_load` avoids arbitrary object construction | A lighter front-matter-only parser becomes preferable |
| Layout | `src/` layout | Avoids import-shadowing; standard for testable packages | — |
| Internal shape | dict per file: `metadata`, `title`, `file_path` | Simple, easy to test, maps cleanly to JSON output | A typed dataclass is needed for clarity |
| Missing-key semantics | `key=value` does not match; `key!=value` matches | Matches `.claude/rules/20-cli-behavior.md`; makes `paths` workflow safe | A clearer rule is documented and tested |

## Definition of done (per issue)

- Acceptance criteria in the issue are met.
- Tests cover matching and non-matching / edge cases and pass locally (`pytest`).
- No out-of-scope features were added.
- README examples that the issue touches still run as written.
- Scope discipline from `.claude/rules/40-testing-docs.md` was respected.
