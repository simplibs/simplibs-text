from simplibs.actions import create_action
# Outers
from ...logic.decorate import truncate


Truncate = create_action(
    truncate,
    main_param="text",
    class_name="Truncate",
)
"""Action wrapping `truncate` — shortens the text to a number of lines and / or characters and says so."""


_DESIGN_NOTES = """
# Truncate — Action Over `truncate`

## Purpose
`Truncate(max_lines=200)` — a long log that must fit into a report.

## Shape
Main input: `text`. Options: `max_lines`, `max_chars` (at least one), `marker`. Text in, text out.
"""
