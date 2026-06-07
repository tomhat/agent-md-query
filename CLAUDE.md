# CLAUDE.md

Project instructions for Claude Code working on `tomhat/agent-md-query`.

## Purpose

`agent-md-query` is a small Python CLI that helps AI agents query Markdown YAML Front Matter before reading full files.

Core value:

> Filter candidate Markdown files by metadata before asking an AI to read them.

## Rule organization

Keep this file short and project-wide. Detailed rules are split into `.claude/rules/`.

@.claude/rules/00-project-overview.md
@.claude/rules/10-python-package.md
@.claude/rules/20-cli-behavior.md
@.claude/rules/30-markdown-scanner.md
@.claude/rules/40-testing-docs.md

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
