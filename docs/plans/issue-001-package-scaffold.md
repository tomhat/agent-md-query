# Plan: Issue #1 — Set up Python package scaffold

- Issue: Set up Python package scaffold
- Depends on: none
- Status: planned

## Goal

Prepare the repository so later issues can focus on scanning, parsing, filtering, and
formatting. This issue is **only** the scaffold. No Markdown logic.

## Scope

- Add `pyproject.toml` (build metadata + console script).
- Add `src/agent_md_query/` package with `__init__.py`, `__main__.py`, `cli.py`.
- Add a minimal CLI entry point with a working `--help`.
- Add `tests/` with a basic test setup.

## Tasks

1. Create `pyproject.toml`:
   - `[project]` with name `agent-md-query`, version `0.1.0`, Python requirement, and
     `PyYAML` as the only runtime dependency (used from #2 onward; declaring it now keeps
     the scaffold stable).
   - `[project.scripts]` entry: `agent-md-query = "agent_md_query.cli:main"`.
   - `src/` layout configuration (setuptools or hatchling; pick one and record it).
2. Create `src/agent_md_query/__init__.py` exposing `__version__`.
3. Create `src/agent_md_query/cli.py`:
   - `build_parser()` returning an `argparse.ArgumentParser` with program name
     `agent-md-query` and a help description.
   - `main(argv=None)` that parses args and prints help when no command is given.
   - Keep a placeholder for the `list` subcommand wiring (added in #3) but do not implement
     filtering here.
4. Create `src/agent_md_query/__main__.py` calling `main()` so `python -m agent_md_query`
   works.
5. Create `tests/test_cli.py` covering the help path.

## Expected commands

```bash
python -m agent_md_query --help
agent-md-query --help   # if console script is installed
```

## Test plan

- `test_cli.py`: invoking the CLI with `--help` exits cleanly (exit code 0) and prints
  usage; invoking with no args prints help without raising.
- `pytest` runs locally with no network access.

## Risks

- Build-backend choice (setuptools vs hatchling) affects `src/` discovery — pick one,
  verify an editable install (`pip install -e .`) exposes `agent_md_query`, and record the
  choice.
- Console-script test may depend on install; prefer testing `main()` directly to avoid
  requiring installation in CI.

## Out of scope

- Markdown scanning, Front Matter parsing, `--where`, output formats. These belong to
  #2–#4. Per `.claude/rules/40-testing-docs.md`, do not implement scanning here.

## Acceptance criteria (from issue)

- The package can be imported as `agent_md_query`.
- The CLI help command runs without error.
- Tests can be executed locally.
- No Markdown scanning logic is required.
