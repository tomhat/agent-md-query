# Plan: Issue #2 — Markdown scanner and Front Matter parser

- Issue: Implement Markdown scanner and Front Matter parser
- Depends on: #1
- Status: planned

## Goal

Implement the core that finds Markdown files and parses YAML Front Matter into structured
metadata. This is the foundation everything else builds on. Pure library code — no CLI
flags, no filtering, no output formats.

## Scope

- Recursively scan `.md` and `.markdown` files under a path.
- Parse YAML Front Matter (the leading `---` … `---` block).
- Return structured metadata, the source file path, and an extracted title.
- Ignore files without Front Matter safely.
- Add fixture Markdown files for tests.

## Design

Implement in `src/agent_md_query/scanner.py` as pure functions.

- `scan(path) -> list[dict]`: walk the directory recursively, collect `.md`/`.markdown`
  files, parse each, and return results. Sort results by `file_path` for deterministic
  output.
- `parse_file(file_path) -> dict | None`: read text, split Front Matter from body, parse
  YAML, extract title.
- `split_front_matter(text) -> tuple[dict, str]`: detect a leading `---` fence, parse the
  YAML between fences with `yaml.safe_load`, return `(metadata, body)`. No leading fence →
  `({}, text)`.
- `extract_title(metadata, body, file_path) -> str`: first Markdown H1 (`# ...`) in the
  body; fall back to the file stem when no H1 exists.

### Internal result shape

```python
{
    "file_path": "examples/workboard/tasks/task-001.md",
    "title": "Token Budget Review",
    "metadata": {"type": "task", "status": "doing", "tags": ["token-budget"], ...},
}
```

Keep `metadata` as the raw parsed mapping (`{}` when absent). Keep the shape minimal and
easy to test, per `.claude/rules/30-markdown-scanner.md`.

## Tasks

1. Add `scanner.py` with the functions above.
2. Decide Front Matter detection precisely: file must start with `---` on its own line;
   the closing `---` ends the block. Document the rule in a docstring.
3. Title extraction: first `# ` heading after the Front Matter; otherwise filename without
   extension.
4. Add fixtures under `tests/fixtures/` covering the cases below.
5. Add `tests/test_scanner.py`.

## Test plan

Fixtures + `test_scanner.py` covering:

- Markdown with valid Front Matter → metadata parsed, title from H1.
- Markdown without Front Matter → `metadata == {}`, does not crash, title from filename.
- Markdown with H1 title → title from H1.
- Markdown without H1 title → title from file stem.
- `.markdown` extension is discovered as well as `.md`.
- Recursive discovery across nested directories.
- List-style YAML (`tags`) parses into a Python list.
- Malformed YAML produces a clear error/warning rather than an opaque crash.

## Risks

- **Title from H1 vs filename**: define the H1 rule (first `#` heading only, ignore `##`).
  Test both branches.
- **Malformed YAML**: decide and document behavior (warn-and-skip vs raise with a clear
  message). `.claude/rules/30` says "clear error or warning"; prefer a clear message and a
  result that does not abort the whole scan unless required.
- **Encoding / read errors**: produce a clear error; do not silently swallow.
- **Determinism**: sort results so tests and `paths` output are stable.

## Out of scope

- Filtering (`--where`), tag filtering, output formats, CLI wiring. Those are #3/#4/#5.
  Do not implement query filtering here.

## Acceptance criteria (from issue)

- `.md` and `.markdown` files are discovered recursively.
- YAML Front Matter is parsed correctly.
- Files without Front Matter do not crash the scanner.
- File paths are included in scanner results.
- Tests cover basic parsing behavior.
