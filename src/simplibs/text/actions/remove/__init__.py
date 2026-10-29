from .Dedent import Dedent
from .RemoveEmptyLines import RemoveEmptyLines
from .RemoveLinesMatching import RemoveLinesMatching
from .RemoveMatches import RemoveMatches
from .RemoveSpans import RemoveSpans
from .SqueezeBlankLines import SqueezeBlankLines
from .StripTrailingSpaces import StripTrailingSpaces
from .TrimBlankEdges import TrimBlankEdges


_DESIGN_NOTES = """
# Text Actions Remove Sub-Package

## Purpose
Pipeline actions wrapping the remove functions: matches, lines, blank lines, trailing spaces, common indentation.

## Internal Components Registry

| Component             | Type   | Description |
| :-------------------- | :----- | :---------- |
| `Dedent`              | Action | Wraps `dedent`: removes the indentation common to all non-blank lines. |
| `RemoveEmptyLines`    | Action | Wraps `remove_empty_lines`: removes blank lines. |
| `RemoveLinesMatching` | Action | Wraps `remove_lines_matching`: removes the lines that contain a match. |
| `RemoveMatches`       | Action | Wraps `remove_matches`: removes every match of a pattern from the text flowing in. |
| `RemoveSpans`         | Action | Wraps `remove_spans`: cuts the given character ranges out of the text flowing in. |
| `SqueezeBlankLines`   | Action | Wraps `squeeze_blank_lines`: shortens runs of blank lines. |
| `StripTrailingSpaces` | Action | Wraps `strip_trailing_spaces`: removes spaces and tabs from the ends of lines. |
| `TrimBlankEdges`      | Action | Wraps `trim_blank_edges`: removes blank lines at the start and at the end. |
"""
