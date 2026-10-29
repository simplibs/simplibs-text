from typing import Final
# Outers
from ..actions.remove import RemoveEmptyLines, StripTrailingSpaces


COMPACT: Final = (
    StripTrailingSpaces()
    >> RemoveEmptyLines()
)
"""Compact a text as a ready pipeline step: no trailing spaces and no blank lines at all."""


_DESIGN_NOTES = """
# COMPACT — Every Line Counts

## Purpose
The shortest honest form of a text, for prompts and reports.

## The Function Form
`compact`. See there for why the draft's third step (`TrimBlankEdges`) is not here.
"""
