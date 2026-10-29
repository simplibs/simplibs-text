from simplibs.actions import create_action
# Outers
from ...logic.clean import remove_non_alphanumeric


RemoveNonAlphanumeric = create_action(
    remove_non_alphanumeric,
    main_param="text",
    class_name="RemoveNonAlphanumeric",
)
"""Action wrapping `remove_non_alphanumeric` — keeps only letters and digits."""


_DESIGN_NOTES = """
# RemoveNonAlphanumeric — Action Over `remove_non_alphanumeric`

## Purpose
`RemoveNonAlphanumeric(keep_whitespace=False)` — a code without any separators.

## Shape
Main input: `text`. Options: `keep_whitespace`. Text in, text out.
"""
