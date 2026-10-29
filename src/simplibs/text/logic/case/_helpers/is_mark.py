import unicodedata


def is_mark(character: str) -> bool:
    """Check whether a character is a combining mark (an accent, a vowel sign, ...).

    Args:
        character: One character.

    Returns:
        True for the Unicode categories Mn, Mc and Me.
    """

    # 1. Marks have no letter case and no meaning alone; they belong to the character before
    return unicodedata.category(character).startswith("M")


_DESIGN_NOTES = """
# is_mark — Part of the Letter Before It

## Purpose
`split_words` must not treat `e` + a combining accent, or a Devanagari consonant
+ its vowel sign, as two things. Both are one letter written in two pieces.

## Why Not `is_diacritic_mark`
That one (in `clean`) knows only the accent blocks, because `remove_diacritics`
must leave other scripts alone. Here every mark counts, in any script.
"""
