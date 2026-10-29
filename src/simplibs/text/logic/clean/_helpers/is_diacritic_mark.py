# Ranges of the Unicode blocks that hold combining diacritical marks
_DIACRITIC_RANGES = (
    (0x0300, 0x036F),  # Combining Diacritical Marks
    (0x1AB0, 0x1AFF),  # Combining Diacritical Marks Extended
    (0x1DC0, 0x1DFF),  # Combining Diacritical Marks Supplement
    (0x20D0, 0x20FF),  # Combining Diacritical Marks for Symbols
    (0xFE20, 0xFE2F),  # Combining Half Marks
)


def is_diacritic_mark(character: str) -> bool:
    """Check whether a character is a combining diacritical mark (an accent, a caron, ...).

    Args:
        character: One character.

    Returns:
        True for the marks in the Combining Diacritical Marks blocks.
    """

    # 1. A mark is recognized by the block it sits in
    code = ord(character)
    return any(low <= code <= high for low, high in _DIACRITIC_RANGES)


_DESIGN_NOTES = """
# is_diacritic_mark — Only the Accents

## Why Not "Every Combining Mark"
Unicode category `Mn` also holds the vowel signs of Devanagari, Thai, Arabic
points and more. They are not accents on Latin letters: they carry the vowels
of their scripts. Removing them would destroy those texts. Only the dedicated
Combining Diacritical Marks blocks are taken.
"""
