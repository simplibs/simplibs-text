import pytest
from simplibs.text.logic.clean._helpers import has_category


@pytest.mark.parametrize(
    "character, prefix",
    [
        ("a", "L"), ("a", "Ll"), ("A", "Lu"), ("č", "L"),
        (",", "P"), ("-", "Pd"), ("_", "Pc"), ("(", "Ps"), ("\u00ab", "Pi"),
        ("+", "S"), ("+", "Sm"), ("$", "Sc"), ("\U0001f600", "So"),
        ("5", "N"), ("5", "Nd"),
        (" ", "Z"), (" ", "Zs"),
        ("\u0301", "M"),
    ],
)
def test_has_category_true_when_the_category_starts_with_the_prefix(character, prefix) -> None:
    """A one-letter prefix is the whole family, two letters one category."""
    assert has_category(character, prefix) is True


@pytest.mark.parametrize(
    "character, prefix",
    [("a", "P"), ("a", "Lu"), ("A", "Ll"), ("-", "Pc"), ("+", "P"), ("$", "Sm"), ("5", "L"), (" ", "P")],
)
def test_has_category_false_for_another_category(character, prefix) -> None:
    """Different family, or the same family but another category."""
    assert has_category(character, prefix) is False
