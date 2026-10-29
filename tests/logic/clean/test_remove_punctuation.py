import unicodedata
import pytest
from simplibs.text.logic.clean import remove_punctuation


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, world! (a_b) \u00abx\u00bb", "Hello world ab x"),
        ("a-b", "ab"),
        ("\u201cquoted\u201d \u2014 dash", "quoted  dash"),
        ("\u3053\u3093\u306b\u3061\u306f\u3002", "\u3053\u3093\u306b\u3061\u306f"),
        ("a.b,c;d:e?f", "abcdef"),
    ],
    ids=["mixed", "hyphen", "typographic", "japanese-stop", "ascii-set"],
)
def test_remove_punctuation_removes_the_punctuation_family(text, expected) -> None:
    """Dots, commas, dashes, brackets, quotes of any script."""
    assert remove_punctuation(text) == expected


@pytest.mark.parametrize("text", ["a+b", "$5", "x=y", "a|b", "a<b", "\u00a9", "\U0001f600"])
def test_remove_punctuation_symbols_survive(text) -> None:
    """Symbols are another family (`remove_symbols`)."""
    assert remove_punctuation(text) == text


def test_remove_punctuation_marks_and_whitespace_survive() -> None:
    """Accents and layout are not punctuation."""
    assert remove_punctuation("cafe\u0301, a\n\tb") == "cafe\u0301 a\n\tb"


@pytest.mark.parametrize("text", ["abc 123", "", "a+b", "\u00e9"])
def test_remove_punctuation_nothing_to_remove_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert remove_punctuation(probe) is probe


def test_remove_punctuation_composed_and_decomposed_input_agree() -> None:
    """Only the spelling of the letters differs."""
    text = "P\u0159\u00edli\u0161, \u017elu\u0165ou\u010dk\u00fd!"
    assert unicodedata.normalize("NFC", remove_punctuation(unicodedata.normalize("NFD", text))) == remove_punctuation(unicodedata.normalize("NFC", text))
