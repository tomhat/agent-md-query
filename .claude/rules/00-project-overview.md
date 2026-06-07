# Project Overview Rules

## Concept

`agent-md-query` is not a semantic search tool.

It is a structured metadata query tool for Markdown files with YAML Front Matter.

Use this distinction:

| Tool | Role |
|---|---|
| Cursor | Semantic search and vague context discovery |
| agent-md-query | Exact filtering by Front Matter |
| Local LLM | Low-cost reading and summarization |
| Codex / Claude Code | Implementation, tests, and PRs |
| Higher-end models | Design decisions and final review |

## Core Principle

Follow this principle:

> Programs extract. AI interprets. Stronger AI decides.

The CLI should do deterministic filtering and formatting. It should not try to infer meaning.

## Main Workflow

The central workflow is:

~~~bash
agent-md-query list workboard/tasks --where status=doing --format paths
~~~

An AI agent can then read only the returned files.

Protect this workflow when changing behavior.

## Generality

`ai-hisho-os` is an important origin and example use case, but this tool must not be hard-coded to it.

Do not hard-code:

- `ai-hisho-os`
- `workboard`
- `history`
- `memory`
- `dispatch`
- specific project names
- specific task IDs

Use them only in examples, fixtures, or documentation.

## MVP Non-Goals

Do not add these in the MVP:

- SQLite index cache
- vector search
- embedding generation
- semantic ranking
- long-running daemon
- web server
- complex query language
- AI API integration
- Obsidian plugin behavior
- ai-hisho-os-specific behavior
