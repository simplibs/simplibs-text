from simplibs.validate import validate_call
# Outers
from .._common.helpers import is_blank, join_lines, split_lines


@validate_call
def trim_blank_edges(text: str) -> str:
    """Remove blank lines from the start and from the end of a text.

    Args:
        text: The text.

    Returns:
        The text without leading and trailing blank lines. Running it twice gives the same result.
    """

    # 1. Find the first and the last line with something on it
    lines, has_end = split_lines(text)
    first = 0
    while first < len(lines) and is_blank(lines[first]):
        first += 1
    last = len(lines)
    while last > first and is_blank(lines[last - 1]):
        last -= 1

    # 2. Nothing trimmed — the very same text back
    if first == 0 and last == len(lines):
        return text

    return join_lines(lines[first:last], has_end)


_DESIGN_NOTES = """
# trim_blank_edges — a Clean Start and a Clean End

## Purpose
After other steps removed content, a text may begin or end with an empty
stretch. This leaves the inside of the text alone.

## Final Newline
Kept if the text had one, as in every line operation (see `split_lines`).
A text made only of blank lines becomes the empty text.
"""
