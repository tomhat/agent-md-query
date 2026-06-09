# Plan: Issue #9 — Fixtures and documentation examples

- Issue: Add fixtures and documentation examples
- Roadmap: cross-cutting (finalize after feature issues)
- Depends on: MVP (#1–#4); ideally land after #5/#6/#8 so examples cover every command
- Status: planned

## Goal

Provide example Markdown files, an `examples/` directory, and example command outputs that
demonstrate the metadata-first workflow, and ensure README examples match actual behavior.

## Current state to build on

- `tests/fixtures/` already exists from the MVP (with/without front matter, nested,
  extensions, malformed). This issue **consolidates** a clean, human-facing `examples/`
  set and aligns fixtures/README — it does not start from zero.
- README currently shows commands against illustrative paths (e.g. `workboard/tasks`) that
  do not exist in the repo. After this issue, at least one documented command should be
  runnable as written against `examples/`.

## Design

Add a small, generic `examples/` tree (allowed to use illustrative names per
`.claude/rules/00-project-overview.md`; do **not** hard-code such names in `src/`):

```text
examples/
  workboard/
    tasks/
      task-001.md   # type: task, status: doing, priority: high, tags: [...]
      task-002.md   # status: todo, different project
      task-003.md   # missing some recommended fields (useful for `validate`)
  README.md         # the metadata-first workflow + copy-pasteable commands & outputs
```

- Each example file uses consistent, recommended Front Matter (`type`, `id`, `project`,
  `status`, `priority`, `updated_at`, `tags`) so the same fixtures exercise `list`,
  `--where`, `--tag`, `summary`, and `validate`.
- Keep files small and self-explanatory (per `.claude/rules/40-testing-docs.md`).

Documentation alignment:

- Verify every README example command runs and its shown output matches real output for
  `list` (markdown/json/paths), and — if #5/#6/#8 are merged — `--tag`, `summary`,
  `validate`. Where README and behavior diverge, fix one side (prefer fixing the docs to
  point at `examples/`), per the testing-docs rule "do not leave examples that cannot run".
- Optionally point tests at the shared examples where it keeps fixtures DRY, but keep
  test-only edge cases (malformed YAML, no front matter) under `tests/fixtures/`.

## Tasks

1. Create `examples/` with 3+ task files (include one intentionally missing recommended
   fields for `validate` demos) and an `examples/README.md` with commands + expected output.
2. Reconcile the top-level `README.md` examples with actual output; make at least the core
   `list ... --format paths` workflow runnable against `examples/`.
3. Align/與 `tests/fixtures/` where practical; add a light test that every `examples/*.md`
   parses via `scanner.scan` without warnings (guards against drift).
4. Re-run all documented commands and confirm outputs.

## Test plan

- A test scans `examples/` and asserts all files parse (no `None` results, no warnings) and
  that expected fields are present.
- Manual/automated check that README example outputs match real CLI output for each command
  that the README shows.

## Risks

- **Doc drift**: examples and README must track real output as features land. Doing #9 last
  (after #5/#6/#8) minimizes rework; if done earlier, revisit when later commands merge.
- **Generality**: illustrative project/task names belong only in `examples/`, fixtures, and
  docs — never in `src/`.
- **Fixture duplication**: avoid two sources of truth; share where clean, but keep
  adversarial cases in `tests/fixtures/`.

## Out of scope

- New CLI behavior. This issue is examples + documentation only.

## Acceptance criteria (from issue)

- Example Markdown files are added.
- Test fixtures are added or aligned with examples.
- README examples remain consistent with actual command behavior.
- Examples are simple enough for AI agents to understand.
- Examples demonstrate the metadata-first workflow.
