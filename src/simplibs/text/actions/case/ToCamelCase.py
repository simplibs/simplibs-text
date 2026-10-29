from simplibs.actions import create_action
# Outers
from ...logic.case import to_camel_case


ToCamelCase = create_action(
    to_camel_case,
    main_param="text",
    class_name="ToCamelCase",
)
"""Action wrapping `to_camel_case` — writes every line in `camelCase`."""


_DESIGN_NOTES = """
# ToCamelCase — Action Over `to_camel_case`

## Purpose
`ToCamelCase()` — `my_var_name` to `myVarName`.

## Shape
Main input: `text`. No options. Text in, text out.
"""
