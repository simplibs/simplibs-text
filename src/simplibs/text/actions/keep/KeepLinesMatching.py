from simplibs.actions import create_action
# Outers
from ...logic.keep import keep_lines_matching


KeepLinesMatching = create_action(
    keep_lines_matching,
    main_param="text",
    class_name="KeepLinesMatching",
)
"""Action wrapping `keep_lines_matching` — keeps only the lines that contain a match."""


_DESIGN_NOTES = """
# KeepLinesMatching — Action Over `keep_lines_matching`

## Purpose
`KeepLinesMatching(pattern="def ")` — an outline of a file.

## Shape
Main input: `text`. Options: `pattern` (required), `flags`. Text in, text out.
"""
