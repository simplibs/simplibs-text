from simplibs.actions import create_action
# Outers
from ...logic.remove import dedent


Dedent = create_action(
    dedent,
    main_param="text",
    class_name="Dedent",
)
"""Action wrapping `dedent` — removes the indentation common to all non-blank lines."""


_DESIGN_NOTES = """
# Dedent — Action Over `dedent`

## Purpose
`KeepLineRange(start=10, end=20) >> Dedent()` — a block lifted out of a class.

## Shape
Main input: `text`. No options. Text in, text out.
"""
