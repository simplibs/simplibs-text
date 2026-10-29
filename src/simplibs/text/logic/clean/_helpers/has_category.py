import unicodedata


def has_category(character: str, prefix: str) -> bool:
    """Check whether a character belongs to a Unicode general category.

    Args:
        character: One character.
        prefix: A category or its first letter: `"P"` for all punctuation, `"Pd"` for dashes only.

    Returns:
        True if the character's category starts with the prefix.
    """

    # 1. Unicode names every character's category with 1-2 letters (Lu, Nd, Po, Sc, ...)
    return unicodedata.category(character).startswith(prefix)


_DESIGN_NOTES = """
# has_category — Letting Unicode Decide

## Purpose
"Is this punctuation?" is answered by the Unicode database, not by a hand-made
list of characters that always forgets `„`, `—` or `¿`.

## Categories Used Here
`P*` punctuation (`. , ! ? - _ ( ) " « »` ...), `S*` symbols (`$ + < = > ^ | ~`
and emoji). Letters are `L*`, digits `Nd`, marks `M*`.
"""
