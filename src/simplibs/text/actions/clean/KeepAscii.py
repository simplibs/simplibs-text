from simplibs.actions import create_action
# Outers
from ...logic.clean import keep_ascii


KeepAscii = create_action(
    keep_ascii,
    main_param="text",
    class_name="KeepAscii",
)
"""Action wrapping `keep_ascii` — keeps only the ASCII characters."""


_DESIGN_NOTES = """
# KeepAscii — Action Over `keep_ascii`

## Purpose
`RemoveDiacritics() >> KeepAscii()` — text for a system that reads only ASCII.

## Shape
Main input: `text`. No options. Text in, text out.
"""
