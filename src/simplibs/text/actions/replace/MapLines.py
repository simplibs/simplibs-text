from simplibs.actions import create_action
# Outers
from ...logic.replace import map_lines


MapLines = create_action(
    map_lines,
    main_param="text",
    class_name="MapLines",
)
"""Action wrapping `map_lines` — applies a function to every line."""


_DESIGN_NOTES = """
# MapLines — Action Over `map_lines`

## Purpose
`MapLines(func=str.upper)` — when no ready step fits, a function does.

## Shape
Main input: `text`. Options: `func` (required). Text in, text out.
"""
