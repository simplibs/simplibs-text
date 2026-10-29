import pytest
from simplibs.text.logic.case._helpers import is_mark


@pytest.mark.parametrize(
    "character",
    ["\u0301", "\u0902", "\u093f", "\u20e3", "\ufe0f", "\u0e48"],
    ids=["acute-Mn", "anusvara-Mn", "vowel-sign-Mc", "keycap-Me", "variation-selector", "thai-tone"],
)
def test_is_mark_true_for_combining_marks_of_any_script(character) -> None:
    """Mn, Mc and Me."""
    assert is_mark(character) is True


@pytest.mark.parametrize("character", ["a", "A", "5", " ", "-", "\u00e9", "\u0939", "\u200d", "\n"])
def test_is_mark_false_for_everything_else(character) -> None:
    """Letters (also accented and Devanagari ones), digits, spaces, punctuation and the joiner."""
    assert is_mark(character) is False
