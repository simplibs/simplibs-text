from simplibs.actions import create_action
# Outers
from ...logic.remove import remove_empty_lines


RemoveEmptyLines = create_action(
    remove_empty_lines,
    main_param="text",
    class_name="RemoveEmptyLines",
)
"""Action wrapping `remove_empty_lines` — removes blank lines."""


_DESIGN_NOTES = """
# RemoveEmptyLines — Action Over `remove_empty_lines`

## Purpose
`RemoveMatches(pattern="#") >> RemoveEmptyLines()` — the compact form of a text.

## Shape
Main input: `text`. No options. Text in, text out.
"""
