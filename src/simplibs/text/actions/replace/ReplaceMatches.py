from simplibs.actions import create_action
# Outers
from ...logic.replace import replace_matches


ReplaceMatches = create_action(
    replace_matches,
    main_param="text",
    class_name="ReplaceMatches",
)
"""Action wrapping `replace_matches` — replaces the matches of a pattern by a text or by a function's result."""


_DESIGN_NOTES = """
# ReplaceMatches — Action Over `replace_matches`

## Purpose
`ReplaceMatches(pattern="\\t", replacement="    ")` — tabs to spaces.

## Shape
Main input: `text`. Options: `pattern` (required), `replacement` (required), `flags`, `count`. Text in, text out.
"""
