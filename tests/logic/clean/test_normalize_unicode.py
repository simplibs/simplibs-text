import unicodedata
import pytest
from simplibs.text.logic.clean import normalize_unicode

E_ACUTE = "\u00e9"
E_PLUS_ACUTE = "e\u0301"
LIGATURE_FI = "\ufb01"


def test_normalize_unicode_default_is_nfc() -> None:
    """Composed letters."""
    assert normalize_unicode(E_PLUS_ACUTE) == E_ACUTE


@pytest.mark.parametrize(
    "text, form, expected",
    [
        (E_PLUS_ACUTE, "NFC", E_ACUTE),
        (E_ACUTE, "NFD", E_PLUS_ACUTE),
        (LIGATURE_FI, "NFC", LIGATURE_FI),
        (LIGATURE_FI, "NFD", LIGATURE_FI),
        (LIGATURE_FI, "NFKC", "fi"),
        (LIGATURE_FI, "NFKD", "fi"),
        (E_ACUTE, "NFKD", E_PLUS_ACUTE),
        (E_PLUS_ACUTE, "NFKC", E_ACUTE),
    ],
)
def test_normalize_unicode_each_form(text, form, expected) -> None:
    """The canonical forms keep a ligature, the compatibility forms (K) spell it out."""
    assert normalize_unicode(text, form) == expected


@pytest.mark.parametrize("form", ["NFC", "NFD", "NFKC", "NFKD"])
@pytest.mark.parametrize("text", ["abc", "", "P\u0159\u00edli\u0161", "e\u0301\u0323", "\ufb01", "\u0958"])
def test_normalize_unicode_matches_the_standard_library_and_is_idempotent(text, form) -> None:
    """It is `unicodedata.normalize`; a second round changes nothing."""
    once = normalize_unicode(text, form)
    assert once == unicodedata.normalize(form, text)
    assert normalize_unicode(once, form) == once


@pytest.mark.parametrize("form", ["NFC", "NFD", "NFKC", "NFKD"])
def test_normalize_unicode_a_text_already_in_the_form_is_returned_as_it_is(form) -> None:
    """The same object comes back."""
    text = unicodedata.normalize(form, "".join(["caf", "\u00e9"]))
    assert normalize_unicode(text, form) is text


def test_normalize_unicode_the_two_spellings_of_a_letter_become_equal() -> None:
    """The point of the function: comparing texts that look the same."""
    assert normalize_unicode(E_ACUTE) == normalize_unicode(E_PLUS_ACUTE)
