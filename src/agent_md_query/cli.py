"""CLI entry point for agent-md-query."""

from __future__ import annotations

import argparse
import sys

from agent_md_query.formatter import format_summary, render
from agent_md_query.matcher import WhereParseError, matches, matches_tags, parse_where
from agent_md_query.scanner import scan
from agent_md_query.validator import validate as validate_results


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
    list_parser.add_argument(
        "--tag",
        action="append",
        default=[],
        metavar="TAG",
        help="Filter by Front Matter tag; repeatable (AND)",
    )

    summary_parser = subparsers.add_parser(
        "summary",
        help="Summarize Markdown files grouped by a metadata field",
    )
    summary_parser.add_argument(
        "path",
        help="Directory or Markdown file to scan",
    )
    summary_parser.add_argument(
        "--group-by",
        required=True,
        metavar="FIELD",
        help="Front Matter field to group by",
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate Markdown Front Matter recommended fields",
    )
    validate_parser.add_argument(
        "path",
        help="Directory or Markdown file to scan",
    )
    return parser


def run_list(
    path: str,
    where_exprs: list[str],
    fmt: str,
    tag_filters: list[str] | None = None,
) -> int:
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

    tags = tag_filters if tag_filters is not None else []
    filtered = [
        item
        for item in results
        if matches(item["metadata"], conditions)
        and matches_tags(item["metadata"], tags)
    ]
    output = render(filtered, fmt)
    if output:
        print(output, end="" if output.endswith("\n") else "\n")

    return 0


def run_summary(path: str, group_by: str) -> int:
    """Execute the summary subcommand."""
    try:
        results = scan(path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output = format_summary(results, group_by)
    if output:
        print(output, end="" if output.endswith("\n") else "\n")

    return 0


def run_validate(path: str) -> int:
    """Execute the validate subcommand."""
    try:
        results = scan(path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    failures = 0
    for file_path, missing in validate_results(results):
        if missing:
            failures += 1
            fields = ", ".join(missing)
            print(f"MISSING: {file_path} -> {fields}")
        else:
            print(f"OK: {file_path}")

    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to subcommands."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "list":
        return run_list(args.path, args.where, args.format, args.tag)

    if args.command == "summary":
        return run_summary(args.path, args.group_by)

    if args.command == "validate":
        return run_validate(args.path)

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
