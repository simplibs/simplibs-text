from typing import Annotated
# Inners
from ._helpers import is_line_number


LineNumber = Annotated[int, is_line_number]
"""A line number counted from 1. Zero, negatives and `bool` are rejected."""


_DESIGN_NOTES = """
# LineNumber — a Line Counted the Way People Count

## Purpose
The type of `start` and `end` in `keep_line_range` and of `start` in
`add_line_numbers`.

## Why `Annotated`
`Annotated[int, is_line_number]` is a plain `int` to an editor and a checked
value to `@validate_call` — the same construction as `ByteCount` in `simplibs-file`.
"""
