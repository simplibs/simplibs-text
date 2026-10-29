import pytest
from simplibs.text.annotations._helpers import is_line_number


@pytest.mark.parametrize("value", [1, 2, 42, 10**9])
def test_is_line_number_accepts_positive_integers(value) -> None:
    """Lines are counted from 1."""
    assert is_line_number(value) is True


@pytest.mark.parametrize("value", [0, -1, -42])
def test_is_line_number_rejects_zero_and_negatives(value) -> None:
    """There is no line 0 and no line before the first."""
    assert is_line_number(value) is False


@pytest.mark.parametrize("value", [True, False])
def test_is_line_number_rejects_bool(value) -> None:
    """A bool is an int in Python, but never what the caller meant."""
    assert is_line_number(value) is False


@pytest.mark.parametrize("value", [1.0, 1.5, "1", b"1", None, [1], (1,), {"a": 1}])
def test_is_line_number_rejects_other_types(value) -> None:
    """Anything that is not an int is rejected without raising."""
    assert is_line_number(value) is False
