import pytest
from simplibs.text.logic.remove import dedent


@pytest.mark.parametrize(
    "text, expected",
    [
        ("    a\n    b", "a\nb"),
        ("    a\n      b", "a\n  b"),
        ("  a\n  b\n", "a\nb\n"),
        ("\ta\n\tb", "a\nb"),
        ("  a\n\n  b", "a\n\nb"),
    ],
    ids=["same", "deeper-line", "final-newline", "tabs", "blank-line-ignored"],
)
def test_dedent_removes_the_common_indentation(text, expected) -> None:
    """The least indented line decides how much goes."""
    assert dedent(text) == expected


def test_dedent_whitespace_only_lines_become_empty() -> None:
    """They do not count towards the common indentation and are emptied."""
    assert dedent("  a\n   \n  b") == "a\n\nb"


def test_dedent_empties_whitespace_only_lines_even_when_there_is_nothing_to_remove() -> None:
    """The one case where `dedent` is not byte-identical on a flush-left text (see its design notes)."""
    assert dedent("a\n  \nb") == "a\n\nb"


def test_dedent_a_tab_and_spaces_have_no_common_indentation() -> None:
    """They are different characters, so nothing is removed."""
    assert dedent("\ta\n    b") == "\ta\n    b"


@pytest.mark.parametrize("text", ["", "a", "a\nb\n", "\n"])
def test_dedent_a_flush_left_text_is_unchanged(text) -> None:
    """Nothing to remove."""
    assert dedent(text) == text
