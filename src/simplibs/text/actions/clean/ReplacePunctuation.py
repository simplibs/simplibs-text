from simplibs.actions import create_action
# Outers
from ...logic.clean import replace_punctuation


ReplacePunctuation = create_action(
    replace_punctuation,
    main_param="text",
    class_name="ReplacePunctuation",
)
"""Action wrapping `replace_punctuation` — replaces every punctuation character with a text."""


_DESIGN_NOTES = """
# ReplacePunctuation — Action Over `replace_punctuation`

## Purpose
`ReplacePunctuation(replacement=" ")` — marks become gaps, words stay apart.

## Shape
Main input: `text`. Options: `replacement` (default one space). Text in, text out.
"""
