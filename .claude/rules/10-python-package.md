---
paths:
  - "pyproject.toml"
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python Package Rules

## Defaults

Use these defaults unless the repository already establishes a different choice.

| Item | Default |
|---|---|
| Language | Python |
| Package layout | `src/agent_md_query/` |
| CLI library | `argparse` |
| Test framework | `pytest` |
| YAML parser | `PyYAML` is acceptable |
| Storage | Direct Markdown file scanning |

Avoid unnecessary dependencies.

## Expected Structure

The MVP structure should be close to:

~~~text
agent-md-query/
  pyproject.toml
  src/
    agent_md_query/
      __init__.py
      __main__.py
      cli.py
      scanner.py
      matcher.py
      formatter.py
  tests/
    fixtures/
    test_cli.py
    test_scanner.py
    test_matcher.py
    test_formatter.py
~~~

This is a guide, not a strict requirement. Keep the structure simple and consistent.

## CLI Entry Points

After Issue #1, this should work:

~~~bash
python -m agent_md_query --help
~~~

If console scripts are configured, this should also work:

~~~bash
agent-md-query --help
~~~

## Implementation Style

- Prefer pure functions for scanner, matcher, and formatter logic.
- Keep CLI parsing separate from business logic.
- Avoid hidden global state.
- Return structured data internally.
- Format output only at the edge.
- Keep error messages readable for CLI users.
