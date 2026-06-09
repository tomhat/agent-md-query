"""CLI entry point for agent-md-query."""

from __future__ import annotations

import argparse
import sys

from agent_md_query.formatter import render
from agent_md_query.matcher import WhereParseError, matches, parse_where
from agent_md_query.scanner import scan


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="agent-md-query",
        description="Query Markdown files by YAML Front Matter metadata.",
    )
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser(
        "list",
        help="List Markdown files matching Front Matter filters",
    )
    list_parser.add_argument(
        "path",
        help="Directory or Markdown file to scan",
    )
    list_parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="EXPR",
        help="Filter by metadata (key=value or key!=value); repeatable (AND)",
    )
    list_parser.add_argument(
        "--format",
        choices=["markdown", "json", "paths"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    return parser


def run_list(path: str, where_exprs: list[str], fmt: str) -> int:
    """Execute the list subcommand."""
    try:
        conditions = [parse_where(expr) for expr in where_exprs]
    except WhereParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        results = scan(path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    filtered = [
        item for item in results if matches(item["metadata"], conditions)
    ]
    output = render(filtered, fmt)
    if output:
        print(output, end="" if output.endswith("\n") else "\n")

    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to subcommands."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "list":
        return run_list(args.path, args.where, args.format)

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
