from simplibs.actions import create_action
# Outers
from ...logic.clean import remove_diacritics


RemoveDiacritics = create_action(
    remove_diacritics,
    main_param="text",
    class_name="RemoveDiacritics",
)
"""Action wrapping `remove_diacritics` — removes accents and other combining marks from letters."""


_DESIGN_NOTES = """
# RemoveDiacritics — Action Over `remove_diacritics`

## Purpose
`RemoveDiacritics() >> ToKebabCase()` — a title to a file name.

## Shape
Main input: `text`. No options. Text in, text out.
"""
