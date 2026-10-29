import re
from typing import Annotated, get_args, get_origin
import pytest
from simplibs.regex import DIGIT, Literal, Regex, RegexPattern
from simplibs.rules import IsTyping
from simplibs.validate.testing import assert_type_contract
from simplibs.text.annotations import Pattern
from simplibs.text.annotations._helpers import is_pattern


@pytest.mark.parametrize(
    "value",
    [
        "a",
        "a.b",
        re.compile("a+"),
        Literal("a") + DIGIT,
        RegexPattern(Literal("a")),
    ],
    ids=["str", "str-with-symbol", "re.Pattern", "Regex", "RegexPattern"],
)
def test_pattern_accepts_the_four_forms(value) -> None:
    """A literal str, a compiled pattern, a Regex tree and a RegexPattern are usable patterns."""
    assert IsTyping(Pattern).is_valid(value)


@pytest.mark.parametrize("value", ["", None, 1, 1.5, b"a", ["a"], ("a",), {"a"}])
def test_pattern_rejects_everything_else(value) -> None:
    """The empty text and every other type are rejected."""
    assert not IsTyping(Pattern).is_valid(value)


def test_pattern_contract(subtests) -> None:
    """Verify Pattern satisfies both the Rule contract and @validate_call integration."""
    assert_type_contract(
        subtests,
        type_=Pattern,
        valid_values=["a", re.compile("a"), Literal("a"), RegexPattern(Literal("a"))],
        invalid_values=["", None, 1, b"a", ["a"]],
        verbose=False,
    )


def test_pattern_is_an_annotated_union_of_the_four_forms() -> None:
    """Spelled as `Annotated`, so editors see the plain union and validation reads the predicate."""
    assert get_origin(Pattern) is Annotated
    assert get_args(Pattern) == (str | re.Pattern | Regex | RegexPattern, is_pattern)
