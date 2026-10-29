from simplibs.actions import create_action
# Outers
from ...logic.clean import normalize_unicode


NormalizeUnicode = create_action(
    normalize_unicode,
    main_param="text",
    class_name="NormalizeUnicode",
)
"""Action wrapping `normalize_unicode` — writes the text in one Unicode normalization form."""


_DESIGN_NOTES = """
# NormalizeUnicode — Action Over `normalize_unicode`

## Purpose
`NormalizeUnicode() >> RemoveDiacritics()` — a search key that ignores accents.

## Shape
Main input: `text`. Options: `form` (default `"NFC"`). Text in, text out.
"""
