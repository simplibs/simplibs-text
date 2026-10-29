from typing import Final
# Outers
from ..actions.remove import SqueezeBlankLines, StripTrailingSpaces, TrimBlankEdges


CLEANUP_WHITESPACE: Final = (
    StripTrailingSpaces()
    >> SqueezeBlankLines(max_consecutive=1)
    >> TrimBlankEdges()
)
"""Tidy whitespace as a ready pipeline step: no trailing spaces, one blank line at most, clean edges."""


_DESIGN_NOTES = """
# CLEANUP_WHITESPACE — the Tidy Pass as One Step

## Purpose
`ReadText() >> RemoveMatches(pattern="# ") >> CLEANUP_WHITESPACE` — the usual
last pass after other steps left holes.

## One Object, Many Uses
It is a built chain, so it is created once and used wherever it is needed
(it holds no state). The function form is `cleanup_whitespace`; both give the same text.
"""
