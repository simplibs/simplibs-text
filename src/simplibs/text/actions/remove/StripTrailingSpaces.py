from simplibs.actions import create_action
# Outers
from ...logic.remove import strip_trailing_spaces


StripTrailingSpaces = create_action(
    strip_trailing_spaces,
    main_param="text",
    class_name="StripTrailingSpaces",
)
"""Action wrapping `strip_trailing_spaces` — removes spaces and tabs from the ends of lines."""


_DESIGN_NOTES = """
# StripTrailingSpaces — Action Over `strip_trailing_spaces`

## Purpose
`StripTrailingSpaces()` as the last step before a text is written.

## Shape
Main input: `text`. No options. Text in, text out.
"""
