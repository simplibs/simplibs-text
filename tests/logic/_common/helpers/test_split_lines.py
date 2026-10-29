from itertools import product
import pytest
from simplibs.text.logic._common.helpers import join_lines, split_lines


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", ([], False)),
        ("a", (["a"], False)),
        ("a\n", (["a"], True)),
        ("a\nb", (["a", "b"], False)),
        ("a\nb\n", (["a", "b"], True)),
        ("a\n\nb", (["a", "", "b"], False)),
    ],
)
def test_split_lines_splits_and_remembers_the_final_newline(text, expected) -> None:
    """The lines come without their newline; the flag says whether the text was closed."""
    assert split_lines(text) == expected


def test_split_lines_an_empty_text_has_no_lines() -> None:
    """Nothing at all is no lines, not one empty line."""
    lines, has_end = split_lines("")
    assert lines == []
    assert has_end is False


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\n", ([""], True)),
        ("\n\n", (["", ""], True)),
        ("\n\n\n", (["", "", ""], True)),
        ("a\n\n", (["a", ""], True)),
        ("\na", (["", "a"], False)),
    ],
)
def test_split_lines_only_the_last_newline_closes_the_text(text, expected) -> None:
    """Every other newline separates lines, so blank lines are kept and counted."""
    assert split_lines(text) == expected


@pytest.mark.parametrize(
    "text",
    ["a\rb", "a\x0bb", "a\x0cb", "a\x1cb", "a\x85b", "a\u2028b", "a\u2029b"],
    ids=["CR", "VT", "FF", "FS", "NEL", "LS", "PS"],
)
def test_split_lines_splits_on_the_line_feed_only(text) -> None:
    """The separators that `str.splitlines` also knows are ordinary characters here."""
    assert split_lines(text) == ([text], False)


def test_split_lines_keeps_a_carriage_return_at_the_end_of_a_line() -> None:
    """A text with `\\r\\n` is not normalized here (readers already did that): `\\r` stays on the line."""
    assert split_lines("a\r\nb\r\n") == (["a\r", "b\r"], True)


def test_split_lines_returns_a_real_bool() -> None:
    """The flag is a bool, not a truthy value."""
    assert split_lines("a\n")[1] is True
    assert split_lines("a")[1] is False


@pytest.mark.parametrize("length", range(0, 7))
def test_split_lines_and_join_lines_give_back_every_text(length) -> None:
    """Splitting and joining again is lossless, for every text made of `a` and newlines."""
    for characters in product("a\n", repeat=length):
        text = "".join(characters)
        assert join_lines(*split_lines(text)) == text
