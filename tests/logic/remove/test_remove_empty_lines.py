import pytest
from simplibs.text.logic.remove import remove_empty_lines


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a\n\nb\n", "a\nb\n"),
        ("a\n\n\n\nb", "a\nb"),
        ("\n\na\n\n", "a\n"),
        ("  a\n\n  b", "  a\n  b"),
        ("a\r\n\r\nb\r\n", "a\r\nb\r\n"),
    ],
    ids=["one", "many", "edges", "indent-kept", "crlf"],
)
def test_remove_empty_lines_removes_every_empty_line(text, expected) -> None:
    """Whatever stands between, at the start or at the end."""
    assert remove_empty_lines(text) == expected


@pytest.mark.parametrize("blank", [" ", "   ", "\t", " \t ", "\u00a0", "\x0b"])
def test_remove_empty_lines_a_whitespace_only_line_is_blank(blank) -> None:
    """Lines of spaces and tabs go too."""
    assert remove_empty_lines(f"a\n{blank}\nb\n") == "a\nb\n"


@pytest.mark.parametrize("text", ["", "\n", "\n\n", "  \n\t\n", "   "])
def test_remove_empty_lines_a_text_of_blank_lines_becomes_empty(text) -> None:
    """Nothing is left."""
    assert remove_empty_lines(text) == ""


@pytest.mark.parametrize("text", ["a", "a\n", "a\nb", "a\nb\n", "  a\n  b\n"])
def test_remove_empty_lines_without_blank_lines_gives_the_very_same_text(text) -> None:
    """The same object comes back, final newline and indentation untouched."""
    probe = "".join(list(text))
    assert remove_empty_lines(probe) is probe


@pytest.mark.parametrize("text", ["a\n\nb", "\n\n", "a \n \n b\n", "x\n\n\n"])
def test_remove_empty_lines_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = remove_empty_lines(text)
    assert remove_empty_lines(once) == once
