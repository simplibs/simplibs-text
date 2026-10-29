from simplibs.validate import validate_call
# Inners
from ._helpers import has_category


@validate_call
def replace_punctuation(
    text: str,
    replacement: str = " ",
) -> str:
    """Replace every punctuation character with a text.

    Args:
        text: The text.
        replacement: What to put in place of each punctuation character. Used literally.

    Returns:
        The changed text; the same text if there was no punctuation.
    """

    # 1. Unicode category P — the same family as remove_punctuation
    result = "".join(replacement if has_category(char, "P") else char for char in text)

    # 2. Nothing replaced — the very same text back
    return text if result == text else result


_DESIGN_NOTES = """
# replace_punctuation — Marks Become Gaps

## Purpose
`well-known, indeed!` -> `well known  indeed ` keeps the words apart, where
`remove_punctuation` would glue them together.

## One for One
Every punctuation character is replaced, so two marks in a row give two
replacements. Combine with `replace_matches` or `squeeze` steps if needed.
"""
