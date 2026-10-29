from simplibs.actions import create_action
# Outers
from ...logic.case import to_pascal_case


ToPascalCase = create_action(
    to_pascal_case,
    main_param="text",
    class_name="ToPascalCase",
)
"""Action wrapping `to_pascal_case` — writes every line in `PascalCase`."""


_DESIGN_NOTES = """
# ToPascalCase — Action Over `to_pascal_case`

## Purpose
`ToPascalCase()` — `my_var_name` to `MyVarName`.

## Shape
Main input: `text`. No options. Text in, text out.
"""
