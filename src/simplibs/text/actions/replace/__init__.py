from .MapLines import MapLines
from .ReplaceMatches import ReplaceMatches


_DESIGN_NOTES = """
# Text Actions Replace Sub-Package

## Purpose
Pipeline actions wrapping the replace functions: pattern replacement and line mapping.

## Internal Components Registry

| Component        | Type   | Description |
| :--------------- | :----- | :---------- |
| `MapLines`       | Action | Wraps `map_lines`: applies a function to every line. |
| `ReplaceMatches` | Action | Wraps `replace_matches`: replaces the matches of a pattern by a text or by a function's result. |
"""
