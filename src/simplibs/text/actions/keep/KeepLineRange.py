from simplibs.actions import create_action
# Outers
from ...logic.keep import keep_line_range


KeepLineRange = create_action(
    keep_line_range,
    main_param="text",
    class_name="KeepLineRange",
)
"""Action wrapping `keep_line_range` — keeps the lines from `start` to `end`."""


_DESIGN_NOTES = """
# KeepLineRange — Action Over `keep_line_range`

## Purpose
`KeepLineRange(start=10, end=20)` — lines 10 to 20, as an editor numbers them.

## Shape
Main input: `text`. Options: `start` (default `1`), `end` (default: the last line). Text in, text out.
"""
