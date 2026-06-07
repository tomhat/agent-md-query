---
paths:
  - "tests/**/*"
  - "examples/**/*"
  - "README.md"
  - "docs/**/*"
  - "src/**/*.py"
---

# Testing and Documentation Rules

## Testing Policy

Add or update tests for behavior changes.

Use `pytest` unless the repository establishes a different test framework.

Do not rely on network access in tests.

## Useful Test Cases

Cover these cases as the MVP is implemented:

- Markdown with valid Front Matter
- Markdown without Front Matter
- Markdown with H1 title
- Markdown without H1 title
- `--where key=value`
- `--where key!=value`
- multiple `--where` filters
- `markdown` output
- `json` output
- `paths` output

## Fixtures

Prefer small fixture files under:

~~~text
tests/fixtures/
~~~

Fixture files should be easy to understand and should not contain unnecessary content.

## Documentation

Keep README examples aligned with actual CLI behavior.

If implementation behavior differs from README examples, either:

1. update the implementation to match the README, or
2. update the README if the implementation choice is intentionally better.

Do not leave examples that cannot run.

## PR Reporting

When reporting work, include:

~~~markdown
## Summary

- What changed

## Related Issue

Closes #N

## Tests

- Commands run

## Notes

- What was intentionally not included
- Follow-up issues if needed
~~~

## Issue Scope Discipline

For Issue #1, do not implement Markdown scanning.

For Issue #2, do not implement full query filtering unless required.

For Issue #3, focus on `list` and `--where`.

For Issue #4, focus on output formats.
