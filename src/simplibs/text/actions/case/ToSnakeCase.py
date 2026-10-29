from simplibs.actions import create_action
# Outers
from ...logic.case import to_snake_case


ToSnakeCase = create_action(
    to_snake_case,
    main_param="text",
    class_name="ToSnakeCase",
)
"""Action wrapping `to_snake_case` — writes every line in `snake_case`."""


_DESIGN_NOTES = """
# ToSnakeCase — Action Over `to_snake_case`

## Purpose
`ToSnakeCase()` — `MyVarName` to `my_var_name`.

## Shape
Main input: `text`. No options. Text in, text out.
"""
