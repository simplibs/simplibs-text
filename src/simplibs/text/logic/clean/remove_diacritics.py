import unicodedata
from simplibs.validate import validate_call
# Inners
from ._helpers import is_diacritic_mark


@validate_call
def remove_diacritics(text: str) -> str:
    """Remove accents and other diacritical marks from letters (`č` -> `c`, `é` -> `e`).

    Args:
        text: The text.

    Returns:
        The text without diacritics; the same text if there were none.
    """

    # 1. Plain ASCII has no accents
    if text.isascii():
        return text

    # 2. Go character by character, so a character without a diacritic is never touched
    pieces: list[str] = []
    for char in text:

        # 2.1 A mark that already stands alone (text in decomposed form)
        if is_diacritic_mark(char):
            continue

        # 2.2 An accented letter: split it into the letter and its marks, keep the letter
        decomposed = unicodedata.normalize("NFD", char)
        if decomposed != char and any(is_diacritic_mark(part) for part in decomposed):
            char = unicodedata.normalize(
                "NFC", "".join(part for part in decomposed if not is_diacritic_mark(part))
            )
        pieces.append(char)

    # 3. Nothing removed — the very same text back
    result = "".join(pieces)
    return text if result == text else result


_DESIGN_NOTES = """
# remove_diacritics — `Příliš žluťoučký` -> `Prilis zlutoucky`

## Purpose
Search keys, slugs, file names, comparisons that should not depend on accents.

## Letters Without a Decomposition
`ł`, `ø`, `đ`, `ß` and `æ` are not "a letter plus an accent" in Unicode, so they
stay as they are. Turning them into `l`, `o`, `d`, `ss`, `ae` is transliteration,
a different and language-dependent job.

## Other Scripts
Only the dedicated combining-accent blocks are removed (see `is_diacritic_mark`),
so the vowel signs of Devanagari or Thai are not damaged.

## Only Accented Letters Are Touched
Each character is looked at on its own. A character that has no diacritic in its
decomposition is left exactly as it is, even when Unicode would write it in
another form (the Devanagari `क़` is `क` + a nukta, which is not an accent and
is not recomposed by NFC). Normalizing the whole text first would change such
characters and break the promise "the same text if there were none".

## Both Forms of the Input
`é` written as one character and `e` + a combining accent both give `e`.
"""
