from simplibs.actions import create_action
# Outers
from ...logic.case import to_kebab_case


ToKebabCase = create_action(
    to_kebab_case,
    main_param="text",
    class_name="ToKebabCase",
)
"""Action wrapping `to_kebab_case` — writes every line in `kebab-case`."""


_DESIGN_NOTES = """
# ToKebabCase — Action Over `to_kebab_case`

## Purpose
`ToKebabCase()` — a title to a URL part.

## Shape
Main input: `text`. No options. Text in, text out.
"""
