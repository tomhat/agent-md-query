# CLAUDE.md

Project instructions for Claude Code working on `tomhat/agent-md-query`.

## Project Purpose

`agent-md-query` is a small Python CLI that helps AI agents query Markdown YAML Front Matter before reading full files.

Core value:

> Filter candidate Markdown files by metadata before asking an AI to read them.

This project originated from `ai-hisho-os`, but must remain a general-purpose OSS tool for Markdown repositories, Obsidian vaults, Git-managed knowledge bases, Codex, Claude Code, Cursor, and local agent workflows.

## Current Priority

Implement the MVP in issue order:

1. Issue #1: Python package scaffold
2. Issue #2: Markdown scanner and Front Matter parser
3. Issue #3: `list` command with `--where`
4. Issue #4: output formats: `markdown`, `json`, `paths`

Do not implement later roadmap features unless explicitly requested.

## Working Rules

- Keep changes small and issue-scoped.
- Read the relevant issue and README before editing.
- Prefer simple, testable Python.
- Do not add SQLite, vector search, semantic search, daemon behavior, or AI API integration in the MVP.
- Update tests with behavior changes.
- Keep README examples aligned with actual CLI behavior.

## Role-Specific Rules

Additional project rules live in `.claude/rules/`.

Use them as follows:

- `00-project-overview.md`: product concept and non-goals
- `10-python-package.md`: Python package and project structure
- `20-cli-behavior.md`: CLI command behavior
- `30-markdown-scanner.md`: Markdown and Front Matter parsing
- `40-testing-docs.md`: tests, fixtures, and documentation

If instructions conflict, prefer the most specific rule for the files being edited.
