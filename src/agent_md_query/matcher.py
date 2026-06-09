"""Evaluate --where filter conditions against Front Matter metadata."""

from __future__ import annotations


class WhereParseError(ValueError):
    """Raised when a --where expression is malformed."""


def parse_where(expr: str) -> tuple[str, str, str]:
    """Parse ``key=value`` or ``key!=value`` into ``(key, op, value)``.

    ``!=`` is checked before ``=`` so values containing ``=`` are handled
    predictably.
    """
    if "!=" in expr:
        key, value = expr.split("!=", 1)
        op = "!="
    elif "=" in expr:
        key, value = expr.split("=", 1)
        op = "=="
    else:
        raise WhereParseError(
            f"invalid --where expression {expr!r}: expected key=value or key!=value"
        )

    key = key.strip()
    value = value.strip()
    if not key:
        raise WhereParseError(
            f"invalid --where expression {expr!r}: key must not be empty"
        )

    return key, op, value


def matches(metadata: dict, conditions: list[tuple[str, str, str]]) -> bool:
    """Return whether metadata satisfies all conditions (AND).

    Values are compared as strings so YAML scalars such as ``priority: 1``
    match ``--where priority=1``. A missing key never satisfies ``==`` and
    always satisfies ``!=``.
    """
    for key, op, expected in conditions:
        present = key in metadata
        if op == "==":
            if not present or str(metadata[key]) != expected:
                return False
        elif op == "!=":
            if present and str(metadata[key]) == expected:
                return False
        else:
            raise ValueError(f"unsupported operator: {op}")

    return True
