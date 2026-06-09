# Plan: Issue #3 — `list` command with `--where` filters

- Issue: Implement list command with --where filters
- Depends on: #2
- Status: planned

## Goal

Implement the `list` command with basic Front Matter filtering so users and AI agents can
query Markdown files by metadata before reading them.

## Scope

- Add `agent-md-query list <path>`.
- Support `--where key=value` and `--where key!=value`.
- Allow multiple `--where` options, combined with AND.
- Match values from parsed YAML Front Matter.
- Return only matching files.
- Use a simple default output for now; dedicated formats come in #4.

## Design

- `src/agent_md_query/matcher.py` — pure filtering logic:
  - `parse_where(expr) -> (key, op, value)`: split on the first `!=` then `=`. `op` is one
    of `"=="`/`"!="`. Reject malformed expressions with a clear CLI error.
  - `matches(metadata, conditions) -> bool`: evaluate all conditions with AND.
  - Value comparison is string-based: compare `str(metadata.get(key))` to the given value
    so `priority: 1` and `--where priority=1` behave intuitively. Document this.
- `cli.py` — wire the `list` subcommand:
  - positional `path`; repeatable `--where` (`action="append"`).
  - call `scanner.scan(path)`, filter with `matcher`, print results.
  - default output: one matching file path per line (kept minimal; #4 generalizes this
    behind `--format`).

### Missing-key semantics (per `.claude/rules/20-cli-behavior.md`)

- `key=value` does **not** match when the key is missing.
- `key!=value` **does** match when the key is missing.
- Never crash on missing keys.

These rules make the `--where ... --format paths` workflow safe and predictable. If they
change, document and test the new behavior.

## Tasks

1. Add `matcher.py` with `parse_where` and `matches`.
2. Add the `list` subcommand in `cli.py`, wiring scanner + matcher.
3. Decide the comparison rule (string-based) and document it in a docstring.
4. Add `tests/test_matcher.py` and extend `tests/test_cli.py`.

## Example commands

```bash
agent-md-query list <path> --where status=doing
agent-md-query list <path> --where project=example-project --where status!=done
```

## Test plan

- `test_matcher.py`:
  - `key=value` matches when equal, excludes when different.
  - `key!=value` excludes when equal, includes when different.
  - `key=value` does not match a missing key.
  - `key!=value` matches a missing key.
  - multiple `--where` filters combine with AND.
  - malformed `--where` (no operator) raises a clear error.
- `test_cli.py`: `list` over a fixtures directory returns exactly the expected files.

## Risks

- **`=` vs `!=` parsing order**: check `!=` before `=` so `a!=b` is not misread as
  `a` `=` `!=b`.
- **Type coercion**: YAML may yield ints/bools/dates. String comparison is the documented
  MVP rule; note the limitation rather than building a type system.
- **List-valued fields** (e.g. `tags`): equality against a list is out of scope here — tag
  matching is issue #5. Keep `--where` for scalar fields; document this.

## Out of scope

- `--tag` filtering (#5), `--format` options (#4), `summary` (#6), `validate` (#8).

## Acceptance criteria (from issue)

- `list` command exists.
- `--where key=value` works.
- `--where key!=value` works.
- Multiple filters work together.
- Tests cover matching and non-matching files.
