from simplibs.validate import validate_call
# Outers
from .._common.helpers import join_lines, split_lines


@validate_call
def strip_trailing_spaces(text: str) -> str:
    """Remove spaces and tabs from the end of every line.

    Args:
        text: The text.

    Returns:
        The text with clean line ends. Running it twice gives the same result.
    """

    # 1. Strip each line; only spaces and tabs, so other characters stay as they are
    lines, has_end = split_lines(text)
    stripped = [line.rstrip(" \t") for line in lines]

    # 2. Nothing changed — the very same text back
    if stripped == lines:
        return text

    return join_lines(stripped, has_end)


_DESIGN_NOTES = """
# strip_trailing_spaces — Invisible Noise at Line Ends

## Why Only Spaces and Tabs
`str.rstrip()` also removes `\\x0b`, `\\x0c`, `\\u00a0` and other characters
that are real content in some files. Trailing whitespace in the editor sense is
a space or a tab.
"""
