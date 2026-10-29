import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.keep import keep_line_range

TEXT = "a\nb\nc\nd\n"


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (2, 3, "b\nc\n"),
        (1, 1, "a\n"),
        (4, 4, "d\n"),
        (3, None, "c\nd\n"),
        (1, None, "a\nb\nc\nd\n"),
        (1, 4, "a\nb\nc\nd\n"),
    ],
)
def test_keep_line_range_keeps_both_ends(start, end, expected) -> None:
    """Lines are counted from 1 and both ends are included."""
    assert keep_line_range(TEXT, start, end) == expected


def test_keep_line_range_default_keeps_everything() -> None:
    """From line 1 to the last one."""
    assert keep_line_range(TEXT) == TEXT


@pytest.mark.parametrize("start, end", [(5, None), (9, 12), (5, 5)])
def test_keep_line_range_a_range_past_the_end_gives_an_empty_text(start, end) -> None:
    """Not an error: there is simply nothing there."""
    assert keep_line_range(TEXT, start, end) == ""


def test_keep_line_range_an_end_past_the_text_is_cut_at_the_text() -> None:
    """The text just ends sooner."""
    assert keep_line_range(TEXT, 3, 99) == "c\nd\n"


@pytest.mark.parametrize(
    "text, start, end, expected",
    [
        ("a\nb\nc", 2, 3, "b\nc"),
        ("a\nb\nc", 1, 2, "a\nb"),
        ("a\nb\nc\n", 3, 3, "c\n"),
        ("a\nb", 1, 1, "a"),
    ],
)
def test_keep_line_range_keeps_the_final_newline_status(text, start, end, expected) -> None:
    """The final newline stays with the last line, and only when the last line is kept."""
    assert keep_line_range(text, start, end) == expected


def test_keep_line_range_blank_lines_are_lines() -> None:
    """They count and they are kept."""
    assert keep_line_range("a\n\nb", 2, 3) == "\nb"
    assert keep_line_range("a\n\nb", 2, 2) == ""


@pytest.mark.parametrize("start, end", [(3, 2), (2, 1), (10, 9)])
def test_keep_line_range_a_backwards_range_is_refused(start, end) -> None:
    """A mistake, not an empty selection."""
    with pytest.raises(ParamError):
        keep_line_range(TEXT, start, end)


def test_keep_line_range_a_range_of_one_line_is_not_backwards() -> None:
    """`end == start` is the shortest valid range."""
    assert keep_line_range(TEXT, 2, 2) == "b\n"


def test_keep_line_range_empty_text() -> None:
    """Nothing to keep."""
    assert keep_line_range("", 1, 5) == ""
