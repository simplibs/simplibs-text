from simplibs.validate import validate_call
# Inners
from ._helpers import has_category


@validate_call
def remove_symbols(text: str) -> str:
    """Remove symbol characters (`$ + < = > ^ | ~`, currency signs, emoji and the like).

    Args:
        text: The text.

    Returns:
        The text without symbols; the same text if there were none.
    """

    # 1. Unicode category S — math, currency, modifier and other symbols
    result = "".join(char for char in text if not has_category(char, "S"))

    # 2. Nothing removed — the very same text back
    return text if result == text else result


_DESIGN_NOTES = """
# remove_symbols — Emoji, Currency, Math

## Purpose
The other half of "special characters": what is not punctuation, not a letter,
not a digit and not whitespace.

## Joined Emoji
An emoji made of several parts (a family, a skin tone) is joined by invisible
characters (U+200D, U+FE0F) that are not symbols themselves. They stay behind.

## Mind the Code
`<`, `>`, `=`, `+`, `|` and `~` are symbols, so removing them from source code
breaks it. This is a function for prose.
"""
