from simplibs.validate import validate_call
# Inners
from ._helpers import has_category


@validate_call
def remove_non_alphanumeric(
    text: str,
    *,
    keep_whitespace: bool = True,
) -> str:
    """Keep only letters and digits (of any script), with the marks that belong to them.

    Args:
        text: The text.
        keep_whitespace: Keep spaces, tabs and newlines. With False the result is one unbroken run.

    Returns:
        The text with everything else removed; the same text if there was nothing else.
    """

    # 1. Walk through the text; `anchored` says that the previous character was kept
    #    as a letter, a digit or a mark, so a mark right after it still belongs to it
    kept: list[str] = []
    anchored = False
    for char in text:
        if char.isalnum():
            kept.append(char)
            anchored = True
        elif anchored and has_category(char, "M"):
            kept.append(char)
        elif keep_whitespace and char.isspace():
            kept.append(char)
            anchored = False
        else:
            anchored = False

    # 2. Nothing removed — the very same text back
    result = "".join(kept)
    return text if result == text else result


_DESIGN_NOTES = """
# remove_non_alphanumeric — Letters and Digits Only

## Purpose
The strictest cleanup: no punctuation, no symbols, no leftovers.

## Whitespace Default
Kept by default so words and lines survive; `keep_whitespace=False` is for
codes and identifiers (`"AB-12 / x"` -> `"AB12x"`).

## Any Script
`str.isalnum` knows Czech, Greek and CJK letters and digits of other scripts.

## Marks Stay With Their Letter
Vowel signs of Devanagari or Thai and accents written as separate combining
characters (`e` + `´`) are not "alphanumeric" for `isalnum`, yet removing them
would destroy the word. A mark is therefore kept when the character before it
was kept, and removed together with a letter that is removed. A mark with
nothing before it goes.
"""
