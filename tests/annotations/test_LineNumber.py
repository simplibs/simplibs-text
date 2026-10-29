from typing import Annotated, get_args, get_origin
import pytest
from simplibs.rules import IsTyping
from simplibs.validate.testing import assert_type_contract
from simplibs.text.annotations import LineNumber
from simplibs.text.annotations._helpers import is_line_number


@pytest.mark.parametrize("value", [1, 2, 42, 10**9])
def test_line_number_accepts_positive_integers(value) -> None:
    """A positive int is a line number."""
    assert IsTyping(LineNumber).is_valid(value)


@pytest.mark.parametrize("value", [0, -1, True, False, 1.5, "1", None, [1]])
def test_line_number_rejects_everything_else(value) -> None:
    """Zero, negatives, bool and non-int types are rejected."""
    assert not IsTyping(LineNumber).is_valid(value)


def test_line_number_contract(subtests) -> None:
    """Verify LineNumber satisfies both the Rule contract and @validate_call integration."""
    assert_type_contract(
        subtests,
        type_=LineNumber,
        valid_values=[1, 42, 10**9],
        invalid_values=[0, -1, True, 1.5, "1", None],
        verbose=False,
    )


def test_line_number_is_an_annotated_int() -> None:
    """Spelled as `Annotated`, so editors see a plain `int` with a predicate attached."""
    assert get_origin(LineNumber) is Annotated
    assert get_args(LineNumber) == (int, is_line_number)
