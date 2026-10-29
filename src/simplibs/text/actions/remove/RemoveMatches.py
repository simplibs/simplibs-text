from simplibs.actions import create_action
# Outers
from ...logic.remove import remove_matches


RemoveMatches = create_action(
    remove_matches,
    main_param="text",
    class_name="RemoveMatches",
)
"""Action wrapping `remove_matches` — removes every match of a pattern from the text flowing in."""


_DESIGN_NOTES = """
# RemoveMatches — Action Over `remove_matches`

## Purpose
`RemoveMatches(pattern="# TODO") >> RemoveEmptyLines()` — strip a marker, then close the gaps.

## Shape
Main input: `text`. Options: `pattern` (required), `flags`, `drop_emptied_lines`. Text in, text out.
"""
