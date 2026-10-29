from simplibs.actions import create_action
# Outers
from ...logic.decorate import add_line_numbers


AddLineNumbers = create_action(
    add_line_numbers,
    main_param="text",
    class_name="AddLineNumbers",
)
"""Action wrapping `add_line_numbers` — puts a number in front of every line."""


_DESIGN_NOTES = """
# AddLineNumbers — Action Over `add_line_numbers`

## Purpose
`KeepLineRange(start=10, end=20) >> AddLineNumbers(start=10)` — numbers that match the original file.

## Shape
Main input: `text`. Options: `start`, `template`, `width`. Text in, text out.
"""
