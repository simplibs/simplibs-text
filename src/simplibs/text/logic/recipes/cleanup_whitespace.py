from simplibs.validate import validate_call
# Outers
from ..remove import squeeze_blank_lines, strip_trailing_spaces, trim_blank_edges


@validate_call
def cleanup_whitespace(text: str) -> str:
    """Tidy the whitespace of a text without removing its structure.

    Trailing spaces and tabs go, runs of blank lines shrink to one, and blank
    lines at the start and at the end go.

    Args:
        text: The text.

    Returns:
        The tidied text; the same text if it was tidy. Running it twice gives the same result.
    """

    # 1. Line ends first, so a line of spaces counts as a blank line in the next step
    cleaned = strip_trailing_spaces(text)

    # 2. One blank line between blocks, never more
    cleaned = squeeze_blank_lines(cleaned, 1)

    # 3. A clean start and a clean end
    return trim_blank_edges(cleaned)


_DESIGN_NOTES = """
# cleanup_whitespace — Tidy, Not Compact

## Purpose
What an editor's "clean up" does: invisible noise goes, the paragraphs stay.
`compact` is the stronger sibling that leaves no blank line at all.

## Same Chain as the Preset
`CLEANUP_WHITESPACE` in `presets` is this function as a chain of actions; both
give the same result.

## Order
`strip_trailing_spaces` is first so that a line of spaces becomes an empty line
before `squeeze_blank_lines` counts blank lines.
"""
