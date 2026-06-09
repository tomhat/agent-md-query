# Plan: Issue #5 — Tag filtering

- Issue: Add tag filtering
- Roadmap: v0.2
- Depends on: MVP (#2 scanner, #3 list/matcher, #4 formats) — all merged
- Status: planned

## Goal

Add `--tag <name>` to the `list` command so files can be filtered by list-style `tags`
Front Matter, on its own or combined with `--where`.

## Current code to build on

- `src/agent_md_query/matcher.py`: `parse_where`, `matches(metadata, conditions)`.
- `src/agent_md_query/cli.py`: `run_list(path, where_exprs, fmt)` filters with
  `matches(item["metadata"], conditions)`.
- `tags` already parses as a Python list (see `scanner` fixture `task-doing.md`).

## Design

Add tag matching to `matcher.py` (keep it a pure function, no CLI coupling):

```python
def matches_tags(metadata: dict, required_tags: list[str]) -> bool:
    """Return True if metadata's tags include every required tag (AND)."""
```

Behavior:

- No `--tag` given (`required_tags == []`) → passes (no constraint).
- `tags` is a list → match when every required tag is a member.
- `tags` missing → no match when any tag is required (safe, no crash).
- `tags` is a scalar string → coerce to a one-element list before matching
  (lenient, documented). Any other type → no match.
- Multiple `--tag` combine with **AND** (consistent with `--where` AND semantics).

Wire into `cli.py`:

- Add `--tag` to the `list` subparser: `action="append"`, `default=[]`, `metavar="TAG"`,
  repeatable.
- Extend `run_list` signature to accept `tags` and filter with
  `matches(...) and matches_tags(item["metadata"], tags)`.

`--where` and `--tag` are combined with AND across both kinds of condition.

## Tasks

1. Add `matches_tags` to `matcher.py` with the behavior above (document the scalar-coercion
   and missing-`tags` rules in the docstring).
2. Add `--tag` to the `list` subparser and thread it through `run_list`.
3. Add a fixture with multiple tags and one without `tags`.
4. Extend `tests/test_matcher.py` and `tests/test_cli.py`.

## Example commands

```bash
agent-md-query list <path> --tag token-budget
agent-md-query list <path> --where status=doing --tag dispatch
agent-md-query list <path> --tag token-budget --tag dispatch   # AND
```

## Test plan

- `matches_tags`: matches when tag present; excludes when absent; missing `tags` → no match;
  scalar `tags` string coerced and matched; multiple required tags use AND.
- `list` integration: `--tag` alone; `--tag` + `--where` together; file without `tags`
  handled safely; output unchanged across `--format` values.

## Risks

- **AND vs OR for multiple `--tag`**: this plan fixes AND for consistency. If OR is wanted
  later, add it explicitly (e.g. a separate flag) — do not silently change semantics.
- **Scalar `tags`**: coercion is lenient; document it so behavior is predictable.
- Keep tag handling simple — no tag expression language (per issue Notes).

## Out of scope

- Tag expressions / negation / OR groups, `summary` (#6), `validate` (#8).

## Acceptance criteria (from issue)

- `--tag` option exists.
- Tag filtering works with list-style YAML tags.
- Tag filtering works together with `--where`.
- Tests cover matching, non-matching, and missing tags.
