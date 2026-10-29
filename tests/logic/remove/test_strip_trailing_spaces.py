import pytest
from simplibs.text.logic.remove import strip_trailing_spaces


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a  \nb\t\n", "a\nb\n"),
        ("a \t \n", "a\n"),
        ("  a  \n", "  a\n"),
        ("a\n   \nb", "a\n\nb"),
        ("a  ", "a"),
        ("   ", ""),
    ],
    ids=["spaces-and-tab", "mixed", "leading-stays", "blank-line-emptied", "no-final-newline", "only-spaces"],
)
def test_strip_trailing_spaces_removes_spaces_and_tabs_at_line_ends(text, expected) -> None:
    """Only the end of each line; the start and the inside stay."""
    assert strip_trailing_spaces(text) == expected


@pytest.mark.parametrize("character", ["\x0b", "\x0c", "\u00a0", "\u2003", "\u200b"])
def test_strip_trailing_spaces_other_whitespace_is_content(character) -> None:
    """Only a space and a tab count; `str.rstrip` would remove these too."""
    text = f"a{character}\n"
    assert strip_trailing_spaces(text) == text


def test_strip_trailing_spaces_stops_at_another_whitespace_character() -> None:
    """Spaces after a non-breaking space go, the non-breaking space stays."""
    assert strip_trailing_spaces("a \u00a0 \n") == "a \u00a0\n"


def test_strip_trailing_spaces_a_carriage_return_protects_the_spaces_before_it() -> None:
    """A text with `\\r\\n` is expected to be normalized earlier (readers do that); `\\r` ends the line here."""
    text = "a  \r\n"
    assert strip_trailing_spaces(text) == text


@pytest.mark.parametrize("text", ["a\n", "a\nb", "  a\n  b\n", "", "\n\n"])
def test_strip_trailing_spaces_nothing_to_strip_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert strip_trailing_spaces(probe) is probe


@pytest.mark.parametrize("text", ["a  \nb \t\n", "  \n  ", "x"])
def test_strip_trailing_spaces_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = strip_trailing_spaces(text)
    assert strip_trailing_spaces(once) == once
