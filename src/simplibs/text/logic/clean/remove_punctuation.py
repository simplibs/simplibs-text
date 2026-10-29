from simplibs.validate import validate_call
# Inners
from ._helpers import has_category


@validate_call
def remove_punctuation(text: str) -> str:
    """Remove punctuation characters (`. , ! ? - _ ( ) " « »` and the like).

    Args:
        text: The text.

    Returns:
        The text without punctuation; the same text if there was none.
    """

    # 1. Unicode category P — the whole family, in every script
    result = "".join(char for char in text if not has_category(char, "P"))

    # 2. Nothing removed — the very same text back
    return text if result == text else result


_DESIGN_NOTES = """
# remove_punctuation — Words Without Marks

## Purpose
Prepare text for counting words or comparing it.

## What Is Punctuation
Everything Unicode puts into category `P`: dashes, brackets, quotes, `_`, `-`,
`.`, `,`, `!`, `?`, `/`, `#`, `%`, `@`... Characters such as `$ + < = > ^ | ~`
are SYMBOLS (category `S`); `remove_symbols` handles those.

## Words Run Together
`well-known` becomes `wellknown`. To keep words apart use `replace_punctuation`.
"""
