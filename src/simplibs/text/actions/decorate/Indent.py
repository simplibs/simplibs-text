from simplibs.actions import create_action
# Outers
from ...logic.decorate import indent


Indent = create_action(
    indent,
    main_param="text",
    class_name="Indent",
)
"""Action wrapping `indent` — puts a prefix in front of every non-blank line."""


_DESIGN_NOTES = """
# Indent — Action Over `indent`

## Purpose
`Indent(prefix="> ")` — a quoted text.

## Shape
Main input: `text`. Options: `prefix` (default four spaces). Text in, text out.
"""
