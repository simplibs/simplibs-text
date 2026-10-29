import pytest
from simplibs.text.logic._common.helpers import is_blank


@pytest.mark.parametrize(
    "line",
    ["", " ", "   ", "\t", " \t ", "\r", "\x0b", "\x0c", "\u00a0", "\u2003", "\u3000"],
    ids=["empty", "space", "spaces", "tab", "space-tab", "CR", "VT", "FF", "NBSP", "EM-SPACE", "IDEOGRAPHIC"],
)
def test_is_blank_true_for_an_empty_or_whitespace_only_line(line) -> None:
    """Empty and whitespace-only lines are blank."""
    assert is_blank(line) is True


@pytest.mark.parametrize(
    "line",
    ["a", " a", "a ", " a ", ".", "0", "\u200b", "\x00", "-"],
    ids=["letter", "lead", "trail", "both", "dot", "zero", "ZWSP", "NUL", "dash"],
)
def test_is_blank_false_when_there_is_something_on_the_line(line) -> None:
    """Anything visible, and also invisible non-whitespace characters, makes a line non-blank."""
    assert is_blank(line) is False
