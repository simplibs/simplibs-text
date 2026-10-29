from typing import NoReturn
from simplibs.exception import ParamError


def raise_invalid_line_range_error(
    start: int,
    end: int,
) -> NoReturn:
    """Raise ParamError when the end of a line range lies before its start.

    Args:
        start: The first line of the range.
        end: The last line of the range.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_LINE_RANGE_INVALID",
        label="end",
        value=end,
        problem=(
            f"The range ends at line {end} but starts at line {start}.",
            "Both ends are counted from 1 and both are included.",
        ),
        expected=f"end >= start ({start}), or None for 'to the last line'.",
        how_to_fix=(
            "Swap the values if they were passed the other way round.",
            "Use end=None to keep everything from the start line on.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_line_range_error — a Range That Runs Backwards

## Purpose
The only check an annotation cannot make alone: it relates two parameters.
Each of them is already known to be a valid `LineNumber`.
"""
