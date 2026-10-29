from .dedent import dedent
from .remove_empty_lines import remove_empty_lines
from .remove_lines_matching import remove_lines_matching
from .remove_matches import remove_matches
from .remove_spans import remove_spans
from .squeeze_blank_lines import squeeze_blank_lines
from .strip_trailing_spaces import strip_trailing_spaces
from .trim_blank_edges import trim_blank_edges


_DESIGN_NOTES = """
# Remove Logic Sub-Package

## Purpose
Functions that take something away from a text: matches, lines, blank lines,
trailing spaces, common indentation.

## Internal Components Registry

| Component               | Type     | Description                                                          |
| :---------------------- | :------- | :------------------------------------------------------------------- |
| `dedent`                | Function | Removes the indentation common to all non-blank lines.               |
| `remove_empty_lines`    | Function | Removes blank lines.                                                 |
| `remove_lines_matching` | Function | Removes whole lines that contain a match.                            |
| `remove_matches`        | Function | Removes the matches of a pattern; emptied lines disappear.           |
| `remove_spans`          | Function | Removes given character ranges (for parsers and tokenizers).         |
| `squeeze_blank_lines`   | Function | Shortens runs of blank lines.                                        |
| `strip_trailing_spaces` | Function | Removes spaces and tabs at the ends of lines.                        |
| `trim_blank_edges`      | Function | Removes blank lines at the start and at the end.                     |

## Layering & Design
- Every function returns the very same text (equal and unchanged) if there is nothing to do.
- `remove_matches` and `remove_spans` share `cut_spans` (in `_helpers`).
"""
