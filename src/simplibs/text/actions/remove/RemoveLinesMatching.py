from simplibs.actions import create_action
# Outers
from ...logic.remove import remove_lines_matching


RemoveLinesMatching = create_action(
    remove_lines_matching,
    main_param="text",
    class_name="RemoveLinesMatching",
)
"""Action wrapping `remove_lines_matching` — removes the lines that contain a match."""


_DESIGN_NOTES = """
# RemoveLinesMatching — Action Over `remove_lines_matching`

## Purpose
`RemoveLinesMatching(pattern="print(")` — drop debugging lines.

## Shape
Main input: `text`. Options: `pattern` (required), `flags`. Text in, text out.
"""
