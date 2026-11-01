from typing import get_args, get_origin
import pytest
from simplibs.rules import IsTyping
from simplibs.text.annotations import Span


@pytest.mark.parametrize("value", [(0, 0), (0, 5), (3, 3), (10, 20)])
def test_span_accepts_a_pair_of_integers(value) -> None:
    """Two integers are a span, empty ones (`start == end`) included."""
    assert IsTyping(Span).is_valid(value)


@pytest.mark.parametrize("value", [(-1, 5), (5, 2), (0, 10**9)])
def test_span_does_not_judge_whether_it_fits_a_text(value) -> None:
    """The type checks the shape only; the fit to a text is decided by `remove_spans`."""
    assert IsTyping(Span).is_valid(value)


@pytest.mark.parametrize("value", [(1,), (1, 2, 3), (), ("a", 2), (1, "b"), (1.5, 2), 5, "ab", None])
def test_span_rejects_everything_else(value) -> None:
    """A tuple of another length, a pair of non-integers and every other type are rejected."""
    assert not IsTyping(Span).is_valid(value)


def test_span_is_a_plain_pair_of_integers() -> None:
    """A plain alias, not `Annotated`: there is no predicate to read."""
    assert get_origin(Span) is tuple
    assert get_args(Span) == (int, int)
