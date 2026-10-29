from simplibs.actions import create_action
# Outers
from ...logic.decorate import wrap


Wrap = create_action(
    wrap,
    main_param="text",
    class_name="Wrap",
)
"""Action wrapping `wrap` — wraps lines that are longer than a width, keeping indentation."""


_DESIGN_NOTES = """
# Wrap — Action Over `wrap`

## Purpose
`Wrap(width=80)` — long comments to a readable width.

## Shape
Main input: `text`. Options: `width` (default `80`), `break_long_words`. Text in, text out.
"""
