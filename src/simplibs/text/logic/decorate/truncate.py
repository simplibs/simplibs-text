from simplibs.types import int_positive
from simplibs.validate import validate_call
# Outers
from .._common.helpers import split_lines
# Inners
from ._validations import raise_missing_limit_error


@validate_call
def truncate(
    text: str,
    *,
    max_lines: int_positive | None = None,
    max_chars: int_positive | None = None,
    marker: str = "… (truncated)",
) -> str:
    """Shorten a text to a number of lines and / or characters and say so.

    Args:
        text: The text.
        max_lines: The most lines to keep.
        max_chars: The most characters to keep. Counted after `max_lines` was applied.
        marker: A line added after a shortened text; `""` adds nothing.

    Returns:
        The shortened text followed by the marker on its own line; the same
        text if it already fits.

    Raises:
        ParamError: If neither limit is given.
    """

    # 1. A limit is required
    if max_lines is None and max_chars is None:
        raise_missing_limit_error()

    # 2. Lines first
    shortened = text
    was_cut = False
    if max_lines is not None:
        lines, _ = split_lines(text)
        if len(lines) > max_lines:
            shortened = "\n".join(lines[:max_lines])
            was_cut = True

    # 3. Then characters
    if max_chars is not None and len(shortened) > max_chars:
        shortened = shortened[:max_chars]
        was_cut = True

    # 4. Fits as it is — the very same text back
    if not was_cut:
        return text

    return shortened + ("\n" + marker if marker else "")


_DESIGN_NOTES = """
# truncate — Short, and Honest About It

## Purpose
Keep a long file or a log from flooding a prompt or a report. The marker tells
the reader that something is missing instead of letting the text just stop.

## Order
Lines are cut first, characters second, so `max_chars` is a hard ceiling
on what remains. It may cut in the middle of a word or a line; for a clean cut
use `max_lines` alone.

## The Marker
Not counted into `max_chars`. It stands on its own line, so a text that was cut
in the middle of a line still ends with a clean line. `marker=""` cuts silently.

## A Final Newline Counts
`max_chars` counts the whole text, final newline included. A text whose content
is exactly `max_chars` long and ends with a newline is cut by that newline and
gets the marker, although nothing visible is missing.

## Final Newline
A shortened text does not end with the original's newline: the marker (or the cut)
is the end.
"""
