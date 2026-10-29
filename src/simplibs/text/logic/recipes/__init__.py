from .compact import compact
from .cleanup_whitespace import cleanup_whitespace


_DESIGN_NOTES = """
# Recipes Logic Sub-Package

## Purpose
Ready-made combinations of the basic functions — the two cleanups people reach
for most often.

## Internal Components Registry

| Component            | Type     | Description                                                           |
| :------------------- | :------- | :-------------------------------------------------------------------- |
| `cleanup_whitespace` | Function | Strips line ends, shrinks blank runs to one line, trims the edges.    |
| `compact`            | Function | Strips line ends and removes every blank line.                        |

## The One Domain That Looks Sideways
Every other domain imports only `_common`. A recipe is a COMBINATION of
functions, so it imports from `remove`; that is why it stands apart as the top
layer of `logic` and nothing in `logic` imports it.
"""
