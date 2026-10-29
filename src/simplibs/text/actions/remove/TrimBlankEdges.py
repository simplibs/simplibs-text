from simplibs.actions import create_action
# Outers
from ...logic.remove import trim_blank_edges


TrimBlankEdges = create_action(
    trim_blank_edges,
    main_param="text",
    class_name="TrimBlankEdges",
)
"""Action wrapping `trim_blank_edges` — removes blank lines at the start and at the end."""


_DESIGN_NOTES = """
# TrimBlankEdges — Action Over `trim_blank_edges`

## Purpose
`TrimBlankEdges()` after steps that left empty stretches at the edges.

## Shape
Main input: `text`. No options. Text in, text out.
"""
