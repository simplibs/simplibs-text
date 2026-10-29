from .map_lines import map_lines
from .replace_matches import replace_matches


_DESIGN_NOTES = """
# Replace Logic Sub-Package

## Purpose
Functions that change parts of a text instead of removing or keeping them.

## Internal Components Registry

| Component         | Type     | Description                                                          |
| :---------------- | :------- | :------------------------------------------------------------------- |
| `map_lines`       | Function | Applies a function to every line.                                    |
| `replace_matches` | Function | Replaces the matches of a pattern by a text or by a function's result. |

## Layering & Design
- Both take a function from the caller and check what it returns; the shared card
  lives in `logic/_common/validations`.
"""
