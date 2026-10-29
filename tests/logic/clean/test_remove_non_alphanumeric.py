import unicodedata
import pytest
from simplibs.text.logic.clean import remove_non_alphanumeric


@pytest.mark.parametrize(
    "text, expected",
    [
        ("AB-12 / x", "AB12  x"),
        ("a_b", "ab"),
        ("Hello, world!", "Hello world"),
        ("a\n-b\n", "a\nb\n"),
        ("\u0663\u0664", "\u0663\u0664"),
        ("\u4e2d\u6587!", "\u4e2d\u6587"),
        ("a\U0001f600b", "ab"),
    ],
    ids=["codes", "underscore", "sentence", "newlines", "arabic-digits", "chinese", "emoji"],
)
def test_remove_non_alphanumeric_keeps_letters_digits_and_whitespace(text, expected) -> None:
    """Letters and digits of any script stay; so does whitespace by default."""
    assert remove_non_alphanumeric(text) == expected


def test_remove_non_alphanumeric_without_whitespace_the_result_is_one_run() -> None:
    """For codes and identifiers."""
    assert remove_non_alphanumeric("AB-12 / x\n", keep_whitespace=False) == "AB12x"


def test_remove_non_alphanumeric_the_vowel_signs_of_other_scripts_stay() -> None:
    """The signs are marks, not letters, and still part of the word."""
    assert remove_non_alphanumeric("\u0939\u093f\u0902\u0926\u0940, ok!") == "\u0939\u093f\u0902\u0926\u0940 ok"


def test_remove_non_alphanumeric_an_accent_written_separately_stays_with_its_letter() -> None:
    """Text from systems that write accents as combining characters is not damaged."""
    assert remove_non_alphanumeric("cafe\u0301!") == "cafe\u0301"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\u0301a", "a"),
        ("a \u0301b", "a b"),
        ("a-\u0301b", "ab"),
        ("\n\u0301a", "\na"),
    ],
    ids=["at-start", "after-space", "after-removed-punctuation", "after-newline"],
)
def test_remove_non_alphanumeric_a_mark_goes_when_the_character_before_it_did_not_stay(text, expected) -> None:
    """A mark belongs to a kept letter or digit; otherwise it is removed with what it stood on."""
    assert remove_non_alphanumeric(text) == expected


def test_remove_non_alphanumeric_composed_and_decomposed_input_agree() -> None:
    """The result differs only in how the accents are written."""
    text = "P\u0159\u00edli\u0161, \u017elu\u0165ou\u010dk\u00fd!"
    composed = remove_non_alphanumeric(unicodedata.normalize("NFC", text))
    decomposed = remove_non_alphanumeric(unicodedata.normalize("NFD", text))
    assert unicodedata.normalize("NFC", decomposed) == composed


def test_remove_non_alphanumeric_a_keycap_stays_together() -> None:
    """A digit with its emoji marks is not torn apart."""
    keycap = "1\ufe0f\u20e3"
    assert remove_non_alphanumeric(keycap) == keycap


@pytest.mark.parametrize("text", ["abc 123", "", "a\nb", "\u0939\u093f"])
def test_remove_non_alphanumeric_nothing_to_remove_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert remove_non_alphanumeric(probe) is probe


@pytest.mark.parametrize("keep_whitespace", [True, False])
def test_remove_non_alphanumeric_is_idempotent(keep_whitespace) -> None:
    """Running it twice gives the same result."""
    text = "a-b c\u0301!\u0301 \u0939\u093f, 1\ufe0f\u20e3"
    once = remove_non_alphanumeric(text, keep_whitespace=keep_whitespace)
    assert remove_non_alphanumeric(once, keep_whitespace=keep_whitespace) == once
