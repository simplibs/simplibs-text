from simplibs.validate import validate_call
# Outers
from ..remove import remove_empty_lines, strip_trailing_spaces


@validate_call
def compact(text: str) -> str:
    """Make a text as short as whitespace allows: no trailing spaces, no blank lines.

    Args:
        text: The text.

    Returns:
        The compacted text; the same text if it was compact. Running it twice gives the same result.
    """

    # 1. Line ends
    compacted = strip_trailing_spaces(text)

    # 2. No blank lines at all — this also covers the start and the end of the text
    return remove_empty_lines(compacted)


_DESIGN_NOTES = """
# compact — Everything Blank Goes

## Purpose
The form of a text for a prompt or a report where every line counts. Use
`cleanup_whitespace` when paragraphs must stay visible.

## Same Chain as the Preset
`COMPACT` in `presets` is this function as a chain of actions.

## No Third Step
The draft ended with `trim_blank_edges`. After `remove_empty_lines` there are no
blank lines left, so there is nothing at the edges to trim; the step was dropped.
"""
