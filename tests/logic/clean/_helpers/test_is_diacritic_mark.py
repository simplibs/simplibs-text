import pytest
from simplibs.text.logic.clean._helpers import is_diacritic_mark


@pytest.mark.parametrize(
    "character",
    ["\u0300", "\u0301", "\u0308", "\u030c", "\u0323", "\u036f", "\u1ab0", "\u1aff", "\u1dc0", "\u1dff", "\u20d0", "\u20ff", "\ufe20", "\ufe2f"],
    ids=["grave", "acute", "diaeresis", "caron", "dot-below", "block-1-end", "ext-start", "ext-end",
         "supp-start", "supp-end", "symbols-start", "symbols-end", "half-start", "half-end"],
)
def test_is_diacritic_mark_true_inside_the_combining_blocks(character) -> None:
    """The five blocks of combining diacritical marks, ends included."""
    assert is_diacritic_mark(character) is True


@pytest.mark.parametrize(
    "character",
    ["a", "\u00e9", "\u02c7", "\u02ff", "\u0370", "\u1aaf", "\u1b00", "\u0902", "\u093f", "\u093c", "\u0e48", "\u0e34", "\u200d", "\u20cf", "\ufe1f", "\ufe30"],
    ids=["letter", "precomposed", "modifier-caron", "before-block", "after-block-1", "before-ext", "after-ext",
         "devanagari-anusvara", "devanagari-vowel", "nukta", "thai-tone", "thai-vowel", "ZWJ", "before-symbols", "before-half", "after-half"],
)
def test_is_diacritic_mark_false_outside_those_blocks(character) -> None:
    """Letters, precomposed accents and the marks of other scripts are not diacritics here."""
    assert is_diacritic_mark(character) is False
