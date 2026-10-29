from simplibs.actions import create_action
# Outers
from ...logic.remove import squeeze_blank_lines


SqueezeBlankLines = create_action(
    squeeze_blank_lines,
    main_param="text",
    class_name="SqueezeBlankLines",
)
"""Action wrapping `squeeze_blank_lines` — shortens runs of blank lines."""


_DESIGN_NOTES = """
# SqueezeBlankLines — Action Over `squeeze_blank_lines`

## Purpose
`SqueezeBlankLines(max_consecutive=1)` — one blank line between blocks, never more.

## Shape
Main input: `text`. Options: `max_consecutive` (default `1`). Text in, text out.
"""
