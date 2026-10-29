from simplibs.validate import validate_call
# Outers
from ...annotations import LineNumber
from .._common.helpers import join_lines, split_lines
# Inners
from ._validations import raise_invalid_line_range_error


@validate_call
def keep_line_range(
    text: str,
    start: LineNumber = 1,
    end: LineNumber | None = None,
) -> str:
    """Keep only the lines from `start` to `end`.

    Args:
        text: The text.
        start: The first line to keep, counted from 1.
        end: The last line to keep (included); `None` means up to the last line.

    Returns:
        The lines of the range. A range past the end of the text gives an empty text.

    Raises:
        ParamError: If `end` is lower than `start`.
    """

    # 1. A backwards range is a mistake, not an empty selection
    if end is not None and end < start:
        raise_invalid_line_range_error(start, end)

    # 2. Cut the range out; both ends are included, lines are counted from 1
    lines, has_end = split_lines(text)
    return join_lines(lines[start - 1:end], has_end)


_DESIGN_NOTES = """
# keep_line_range — Lines 10 to 20

## Purpose
Show a part of a file the way an editor numbers it: first line is 1, both ends
are included.

## Final Newline
The result ends with a newline if the text did, also when the range stops in
the middle of the text: each kept line is a closed line.

## Out of Range
A start past the last line gives an empty text, an end past the last line is
the same as `end=None`. Neither is an error — a file simply may be shorter than
the caller hoped, and the caller usually cannot know in advance.
"""
