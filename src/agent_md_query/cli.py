"""CLI entry point for agent-md-query."""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="agent-md-query",
        description="Query Markdown files by YAML Front Matter metadata.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List Markdown files matching Front Matter filters")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to subcommands."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "list":
        parser.error("list command is not implemented yet")

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
