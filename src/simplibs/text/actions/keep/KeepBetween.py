from simplibs.actions import create_action
# Outers
from ...logic.keep import keep_between


KeepBetween = create_action(
    keep_between,
    main_param="text",
    class_name="KeepBetween",
)
"""Action wrapping `keep_between` — keeps the parts between a start marker and an end marker."""


_DESIGN_NOTES = """
# KeepBetween — Action Over `keep_between`

## Purpose
`KeepBetween(start="# region", end="# endregion")` — one marked region of a file.

## Shape
Main input: `text`. Options: `start` (required), `end` (required), `include_markers`, `flags`, `separator`. Text in, text out.
"""
