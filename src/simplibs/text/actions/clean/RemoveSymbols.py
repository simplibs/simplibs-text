from simplibs.actions import create_action
# Outers
from ...logic.clean import remove_symbols


RemoveSymbols = create_action(
    remove_symbols,
    main_param="text",
    class_name="RemoveSymbols",
)
"""Action wrapping `remove_symbols` — removes symbol characters (currency, math signs, emoji)."""


_DESIGN_NOTES = """
# RemoveSymbols — Action Over `remove_symbols`

## Purpose
`RemoveSymbols()` on prose; not on source code.

## Shape
Main input: `text`. No options. Text in, text out.
"""
