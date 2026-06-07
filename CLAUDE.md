# CLAUDE.md

## Purpose

This file is the working guide for Claude Code in this repository.

`agent-md-query` is a small CLI for querying structured Markdown metadata before asking AI agents to read full Markdown files.

Core concept:

```text
Query metadata first.
Read full Markdown only when needed.
Reduce token waste and context noise.
```

## Project identity

`agent-md-query` is a generic OSS tool.

It was originally motivated by `