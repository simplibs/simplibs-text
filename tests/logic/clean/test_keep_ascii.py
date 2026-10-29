import pytest
from simplibs.text.logic.clean import keep_ascii


@pytest.mark.parametrize(
    "text, expected",
    [
        ("P\u0159\u00edli\u0161", "Pli"),
        ("caf\u00e9", "caf"),
        ("a\U0001f600b", "ab"),
        ("a\u00a0b", "ab"),
        ("\u4e2d\u6587", ""),
    ],
    ids=["czech", "cafe", "emoji", "nbsp", "chinese"],
)
def test_keep_ascii_removes_every_other_character(text, expected) -> None:
    """Letters with accents go whole, not only their accent."""
    assert keep_ascii(text) == expected


def test_keep_ascii_newlines_and_tabs_stay_so_lines_stay_lines() -> None:
    """They are ASCII."""
    assert keep_ascii("a\u010d\n\tb\r\n") == "a\n\tb\r\n"


@pytest.mark.parametrize("text", ["", "abc", "a\nb\t!", "\x00\x7f"])
def test_keep_ascii_an_ascii_text_is_returned_as_it_is(text) -> None:
    """The same object comes back; `\\x7f` is the last ASCII character."""
    probe = "".join(list(text))
    assert keep_ascii(probe) is probe


def test_keep_ascii_the_first_non_ascii_code_point_goes() -> None:
    """`\\x80` is the first one past ASCII."""
    assert keep_ascii("a\x80b") == "ab"


@pytest.mark.parametrize("text", ["P\u0159\u00edli\u0161", "a\u010d", "\u4e2d"])
def test_keep_ascii_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = keep_ascii(text)
    assert keep_ascii(once) == once
