from .keep_between import keep_between
from .keep_line_range import keep_line_range
from .keep_lines_matching import keep_lines_matching
from .keep_matches import keep_matches


_DESIGN_NOTES = """
# Keep Logic Sub-Package

## Purpose
Functions that keep only a chosen part of a text and drop the rest: matches,
lines, a range of lines, the part between two markers.

## Internal Components Registry

| Component              | Type     | Description                                                      |
| :--------------------- | :------- | :--------------------------------------------------------------- |
| `keep_between`         | Function | Keeps the parts between a start marker and an end marker.        |
| `keep_line_range`      | Function | Keeps lines `start` to `end` (counted from 1, both included).    |
| `keep_lines_matching`  | Function | Keeps whole lines that contain a match.                          |
| `keep_matches`         | Function | Keeps only the matches themselves, joined with a separator.      |

## Layering & Design
- The mirror of `remove`: `keep_lines_matching` and `remove_lines_matching` split a text exactly in two.
"""
