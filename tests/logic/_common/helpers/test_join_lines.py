import pytest
from simplibs.text.logic._common.helpers import join_lines


@pytest.mark.parametrize(
    "lines, has_end, expected",
    [
        (["a"], False, "a"),
        (["a"], True, "a\n"),
        (["a", "b"], False, "a\nb"),
        (["a", "b"], True, "a\nb\n"),
        (["a", "", "b"], False, "a\n\nb"),
    ],
)
def test_join_lines_joins_with_newlines_and_closes_on_request(lines, has_end, expected) -> None:
    """Lines are separated by a newline; the last one is closed only when asked."""
    assert join_lines(lines, has_end) == expected


@pytest.mark.parametrize("has_end", [True, False])
def test_join_lines_no_lines_give_an_empty_text(has_end) -> None:
    """No lines, no text; a lone newline would be one empty line, not nothing."""
    assert join_lines([], has_end) == ""


@pytest.mark.parametrize(
    "lines, has_end, expected",
    [
        ([""], False, ""),
        ([""], True, "\n"),
        (["", ""], False, "\n"),
        (["", ""], True, "\n\n"),
    ],
)
def test_join_lines_empty_lines_are_lines(lines, has_end, expected) -> None:
    """A list of empty lines is still a list of lines."""
    assert join_lines(lines, has_end) == expected


def test_join_lines_does_not_look_inside_the_lines() -> None:
    """A line that holds a newline is used as it is; the caller decides."""
    assert join_lines(["a\nb", "c"], True) == "a\nb\nc\n"
