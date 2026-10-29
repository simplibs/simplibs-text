from simplibs.validate import validate_call
# Outers
from .._common.helpers import is_blank, join_lines, split_lines


@validate_call
def remove_empty_lines(text: str) -> str:
    """Remove every line that is empty or holds only whitespace.

    Args:
        text: The text.

    Returns:
        The text without blank lines. Running it twice gives the same result.
    """

    # 1. Keep the lines that have something on them
    lines, has_end = split_lines(text)
    kept = [line for line in lines if not is_blank(line)]

    # 2. Nothing removed — the very same text back
    if len(kept) == len(lines):
        return text

    return join_lines(kept, has_end)


_DESIGN_NOTES = """
# remove_empty_lines — No Blank Lines at All

## Purpose
The compact form of a text. For a gentler cleanup (one blank line between
blocks) use `squeeze_blank_lines`.

## Whitespace-Only Lines
A line with spaces or tabs counts as blank (see `is_blank`).
"""
