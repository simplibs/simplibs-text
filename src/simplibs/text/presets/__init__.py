from .CLEANUP_WHITESPACE import CLEANUP_WHITESPACE
from .COMPACT import COMPACT

__all__ = [
    "CLEANUP_WHITESPACE",
    "COMPACT",
]


_DESIGN_NOTES = """
# simplibs.text.presets — Ready-Made Pipeline Steps

## Purpose
Chains of actions that people build again and again, built once.

    from simplibs.text.presets import CLEANUP_WHITESPACE, COMPACT

## Domain Folder
`presets/` has its own `__all__` and is not re-exported from the package root,
like `actions/`. It stands to the right of `actions` (it uses them), so it is the
top layer of the library.

## Internal Components Registry

| Component            | Type   | Description                                                            |
| :------------------- | :----- | :--------------------------------------------------------------------- |
| `CLEANUP_WHITESPACE` | Action | Strips line ends, shrinks blank runs to one line, trims the edges.     |
| `COMPACT`            | Action | Strips line ends and removes every blank line.                         |

## Functions Instead of Chains
`cleanup_whitespace` and `compact` (root exports) do the same for code that is
not a pipeline.
"""
