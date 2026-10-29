import unicodedata
import pytest
from simplibs.text.logic.clean import remove_diacritics


@pytest.mark.parametrize(
    "text, expected",
    [
        ("P\u0159\u00edli\u0161 \u017elu\u0165ou\u010dk\u00fd k\u016f\u0148", "Prilis zlutoucky kun"),
        ("caf\u00e9", "cafe"),
        ("\u00c5ngstr\u00f6m", "Angstrom"),
        ("\u01d6", "u"),
        ("\u1ec7", "e"),
        ("\u03ac", "\u03b1"),
        ("\u1fb3", "\u03b1"),
        ("\u00f1", "n"),
    ],
    ids=["czech", "cafe", "angstrom", "u-diaeresis-macron", "vietnamese", "greek-tonos", "greek-iota-subscript", "tilde"],
)
def test_remove_diacritics_removes_the_accents_and_keeps_the_letter(text, expected) -> None:
    """An accented letter becomes its plain letter."""
    assert remove_diacritics(text) == expected


def test_remove_diacritics_the_angstrom_sign_is_an_accented_a() -> None:
    """The sign U+212B decomposes to A and a ring."""
    assert remove_diacritics("\u212b") == "A"


@pytest.mark.parametrize("text", ["P\u0159\u00edli\u0161 caf\u00e9", "\u1ec7\u01d6", "\u00c5ngstr\u00f6m"])
def test_remove_diacritics_composed_and_decomposed_input_give_the_same_result(text) -> None:
    """`\u00e9` and `e` + a combining accent are one letter written two ways."""
    assert remove_diacritics(unicodedata.normalize("NFC", text)) == remove_diacritics(unicodedata.normalize("NFD", text))


def test_remove_diacritics_a_lone_combining_mark_is_removed() -> None:
    """Also when it has nothing to attach to."""
    assert remove_diacritics("\u0301") == ""
    assert remove_diacritics("e\u0301\u0323") == "e"


@pytest.mark.parametrize("text", ["\u0142\u00f8\u0111\u00df\u00e6", "\u0141\u00d8\u0110", "\u0131"], ids=["lower", "upper", "dotless-i"])
def test_remove_diacritics_letters_without_a_decomposition_stay(text) -> None:
    """Turning `\u0142` into `l` is transliteration, a different job."""
    assert remove_diacritics(text) == text


@pytest.mark.parametrize(
    "text",
    ["\u0939\u093f\u0902\u0926\u0940", "\u0e17\u0e35\u0e48", "\ud55c\uae00", "\u4e2d\u6587", "\u0958"],
    ids=["devanagari", "thai", "hangul", "chinese", "nukta-letter"],
)
def test_remove_diacritics_other_scripts_are_not_touched(text) -> None:
    """Vowel signs and tone marks are not accents; a character that is not accented is never rewritten."""
    assert remove_diacritics(text) == text


@pytest.mark.parametrize("text", ["abc", "", "a\nb", "\u0142\u00f8", "\u0939\u093f\u0902"])
def test_remove_diacritics_nothing_to_remove_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert remove_diacritics(probe) is probe


def test_remove_diacritics_works_line_by_line_without_touching_newlines() -> None:
    """Whitespace is kept."""
    assert remove_diacritics("\u010d\n\u0161\t\u017e") == "c\ns\tz"


@pytest.mark.parametrize("text", ["P\u0159\u00edli\u0161", "\u212b", "e\u0301\u0323", "\u0958x"])
def test_remove_diacritics_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = remove_diacritics(text)
    assert remove_diacritics(once) == once
