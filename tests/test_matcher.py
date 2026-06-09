"""Tests for --where filter matching."""

from __future__ import annotations

import pytest

from agent_md_query.matcher import WhereParseError, matches, matches_tags, parse_where


def test_parse_where_equality() -> None:
    assert parse_where("status=doing") == ("status", "==", "doing")


def test_parse_where_inequality() -> None:
    assert parse_where("status!=done") == ("status", "!=", "done")


def test_parse_where_checks_not_equal_before_equal() -> None:
    assert parse_where("a!=b=c") == ("a", "!=", "b=c")


def test_parse_where_malformed_raises() -> None:
    with pytest.raises(WhereParseError, match="key=value or key!=value"):
        parse_where("statusdoing")


def test_parse_where_empty_key_raises() -> None:
    with pytest.raises(WhereParseError, match="key must not be empty"):
        parse_where("=doing")


def test_equality_matches() -> None:
    metadata = {"status": "doing"}
    assert matches(metadata, [("status", "==", "doing")])


def test_equality_excludes_different_value() -> None:
    metadata = {"status": "done"}
    assert not matches(metadata, [("status", "==", "doing")])


def test_equality_does_not_match_missing_key() -> None:
    assert not matches({}, [("status", "==", "doing")])


def test_inequality_excludes_equal_value() -> None:
    metadata = {"status": "done"}
    assert not matches(metadata, [("status", "!=", "done")])


def test_inequality_includes_different_value() -> None:
    metadata = {"status": "doing"}
    assert matches(metadata, [("status", "!=", "done")])


def test_inequality_matches_missing_key() -> None:
    assert matches({}, [("status", "!=", "done")])


def test_multiple_conditions_use_and() -> None:
    metadata = {"status": "doing", "project": "example-project"}
    conditions = [
        ("status", "==", "doing"),
        ("project", "==", "example-project"),
    ]
    assert matches(metadata, conditions)


def test_multiple_conditions_fail_when_one_fails() -> None:
    metadata = {"status": "doing", "project": "other"}
    conditions = [
        ("status", "==", "doing"),
        ("project", "==", "example-project"),
    ]
    assert not matches(metadata, conditions)


def test_string_comparison_for_numeric_yaml_values() -> None:
    metadata = {"priority": 1}
    assert matches(metadata, [("priority", "==", "1")])


def test_matches_tags_single_tag() -> None:
    metadata = {"tags": ["token-budget", "dispatch"]}
    assert matches_tags(metadata, ["token-budget"])


def test_matches_tags_excludes_non_matching_tag() -> None:
    metadata = {"tags": ["token-budget", "dispatch"]}
    assert not matches_tags(metadata, ["other"])


def test_matches_tags_requires_all_tags() -> None:
    metadata = {"tags": ["token-budget", "dispatch"]}
    assert matches_tags(metadata, ["token-budget", "dispatch"])
    assert not matches_tags(metadata, ["token-budget", "missing"])


def test_matches_tags_missing_tags_field() -> None:
    assert not matches_tags({}, ["token-budget"])


def test_matches_tags_scalar_string_coerced() -> None:
    assert matches_tags({"tags": "token-budget"}, ["token-budget"])


def test_matches_tags_non_list_non_string_tags_field() -> None:
    assert not matches_tags({"tags": 42}, ["42"])


def test_matches_tags_empty_required_list() -> None:
    assert matches_tags({}, [])
