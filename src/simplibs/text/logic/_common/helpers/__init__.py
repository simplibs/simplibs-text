from .compile_pattern import compile_pattern
from .is_blank import is_blank
from .join_lines import join_lines
from .split_lines import split_lines


_DESIGN_NOTES = """
# Text Common Internal Helpers Sub-Package

## Purpose
Shared helper functions used internally across the text logic.

## Internal Components Registry

| Component         | Type     | Description                                                          |
| :---------------- | :------- | :------------------------------------------------------------------- |
| `compile_pattern` | Function | Turns a literal, a `re.Pattern`, a `Regex` tree or a `RegexPattern` into `re.Pattern`. || `is_blank`        | Function | Checks that a line holds only whitespace.                            |
| `join_lines`      | Function | Joins lines back into a text (inverse of `split_lines`).             |
| `split_lines`     | Function | Splits a text into lines and remembers its final newline.            |
"""
