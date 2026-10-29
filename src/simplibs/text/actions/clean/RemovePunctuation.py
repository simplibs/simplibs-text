from simplibs.actions import create_action
# Outers
from ...logic.clean import remove_punctuation


RemovePunctuation = create_action(
    remove_punctuation,
    main_param="text",
    class_name="RemovePunctuation",
)
"""Action wrapping `remove_punctuation` — removes punctuation characters."""


_DESIGN_NOTES = """
# RemovePunctuation — Action Over `remove_punctuation`

## Purpose
`RemovePunctuation()` before counting words.

## Shape
Main input: `text`. No options. Text in, text out.
"""
