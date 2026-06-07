# CLAUDE.md

Project instructions for Claude Code working on `tomhat/agent-md-query`.

## Purpose

`agent-md-query` is a small Python CLI that helps AI agents query Markdown YAML Front Matter before reading full files.

Core value:

> Filter candidate Markdown files by metadata before asking an AI to read them.

## Rule organization

Keep this file short and project-wide. Detailed rules are organized under `.claude/rules/`.

The split rule files should be treated as role-specific guidance and read when relevant to the files or task being edited.

Rule files:

- `.claude/rules/00-project-overview.md`: product concept and MVP non-goals
- `.claude/rules/10-python-package.md`: Python package structure and implementation style
- `.claude/rules/20-cli-behavior.md`: CLI commands, filters, and output formats
- `.claude/rules/30-markdown-scanner.md`: Markdown scanning and Front Matter parsing
- `.claude/rules/40-testing-docs.md`: tests, fixtures, documentation, and PR reporting

## Current priority

Implement the MVP in issue order:

1. Issue #1: Python package scaffold
2. Issue #2: Markdown scanner and Front Matter parser
3. Issue #3: `list` command with `--where`
4. Issue #4: output formats: `markdown`, `json`, `paths`

Do not implement later roadmap features unless explicitly requested.

## Working rules

- Keep changes small and issue-scoped.
- Read the relevant issue and README before editing.
- Prefer simple, testable Python.
- Update tests with behavior changes.
- Keep README examples aligned with actual CLI behavior.

If instructions conflict, prefer the most specific rule for the files being edited.
