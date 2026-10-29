from simplibs.actions import create_action
# Outers
from ...logic.case import split_words


SplitWords = create_action(
    split_words,
    main_param="text",
    class_name="SplitWords",
)
"""Action wrapping `split_words` — splits the text into its words (a `list[str]`)."""


_DESIGN_NOTES = """
# SplitWords — Action Over `split_words`

## Purpose
`SplitWords() >> ForEach(...)` — the words of an identifier, for a style of your own.

## Shape
Main input: `text`. No options. Text in, list of words out.
"""
