from simplibs.types import int_non_negative
from simplibs.validate import validate_call
# Outers
from .._common.helpers import is_blank, join_lines, split_lines


@validate_call
def squeeze_blank_lines(
    text: str,
    max_consecutive: int_non_negative = 1,
) -> str:
    """Shorten every run of blank lines to at most `max_consecutive` lines.

    Args:
        text: The text.
        max_consecutive: How many blank lines in a row may stay. `0` removes them all.

    Returns:
        The text with shorter runs of blank lines. Running it twice gives the same result.
    """

    # 1. Count the blank lines in a row and keep only as many as allowed
    lines, has_end = split_lines(text)
    kept: list[str] = []
    run = 0
    for line in lines:
        run = run + 1 if is_blank(line) else 0
        if run <= max_consecutive:
            kept.append(line)

    # 2. Nothing removed — the very same text back
    if len(kept) == len(lines):
        return text

    return join_lines(kept, has_end)


_DESIGN_NOTES = """
# squeeze_blank_lines — Breathing Room, Not Gaps

## Purpose
Code with three blank lines between functions becomes code with one.

## Which Line of a Run Stays
The first ones; the rest of the run is dropped. Their content does not matter
(they are blank), but a whitespace-only line may stay and an empty one go,
so combine with `strip_trailing_spaces` when the exact result matters.

## `max_consecutive=0`
Same as `remove_empty_lines`, so the two never disagree.
"""
