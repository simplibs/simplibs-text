from typing import get_args
import pytest
from simplibs.rules import IsTyping
from simplibs.text.annotations import UnicodeForm


@pytest.mark.parametrize("value", ["NFC", "NFD", "NFKC", "NFKD"])
def test_unicode_form_accepts_the_four_forms(value) -> None:
    """The four normalization forms of the standard."""
    assert IsTyping(UnicodeForm).is_valid(value)


@pytest.mark.parametrize("value", ["nfc", "NFC ", "", "NF", "utf-8", "NFKCD", None, 1, b"NFC"])
def test_unicode_form_rejects_everything_else(value) -> None:
    """Lowercase, padded, invented names and non-strings are rejected."""
    assert not IsTyping(UnicodeForm).is_valid(value)


def test_unicode_form_lists_exactly_the_four_forms_in_order() -> None:
    """The Literal carries the four names, nothing else."""
    assert get_args(UnicodeForm) == ("NFC", "NFD", "NFKC", "NFKD")
