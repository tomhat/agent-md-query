# agent-md-query

A tiny CLI that helps AI agents query structured Markdown before reading files.

> Stop wasting tokens reading every Markdown file. Query the metadata first.

## Why?

AI agents often waste tokens by reading too many Markdown files.
`agent-md-query` lets agents filter files by YAML Front Matter first,
then read only the files they actually need.

This is useful for agent workflows that manage tasks, notes, decisions,
project state, or knowledge as Markdown files.

## Background

`agent-md-query` was originally created for `ai-hisho-os`,
a Markdown-first AI secretary OS experiment.

In that project, AI agents manage workboards, tasks, state, memory,
and history as Markdown files. However, letting agents read all Markdown
files every time can waste tokens and create noisy context.

The same problem appears in many agent-based workflows:
Obsidian vaults, Git-managed knowledge bases, task boards,
Codex projects, Claude Code projects, Cursor workspaces, and local agents.

`agent-md-query` solves this