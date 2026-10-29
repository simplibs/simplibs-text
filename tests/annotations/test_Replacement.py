import re
from typing import Annotated, get_args, get_origin
import pytest
from simplibs.rules import IsTyping
from simplibs.text.annotations import Replacement


def _upper(match: re.Match) -> str:
    return match.group(0).upper()


@pytest.mark.parametrize("value", ["", "x", " ", "\\1", "\n"])
def test_replacement_accepts_any_text_even_the_empty_one(value) -> None:
    """Any str is a literal replacement; the empty one simply removes the match."""
    assert IsTyping(Replacement).is_valid(value)


@pytest.mark.parametrize("value", [_upper, lambda match: "x", str.upper])
def test_replacement_accepts_a_function(value) -> None:
    """A function from the match to a str is a replacement."""
    assert IsTyping(Replacement).is_valid(value)


@pytest.mark.parametrize("value", [None, 1, 1.5, b"x", ["x"], ("x",), {"x"}])
def test_replacement_rejects_everything_else(value) -> None:
    """Neither a text nor a function: rejected."""
    assert not IsTyping(Replacement).is_valid(value)


def test_replacement_is_a_plain_union_without_a_predicate() -> None:
    """Unlike `Pattern`, nothing is excluded, so there is no `Annotated` predicate."""
    assert get_origin(Replacement) is not Annotated
    assert str in get_args(Replacement)
    assert len(get_args(Replacement)) == 2
