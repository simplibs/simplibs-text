from .AddLineNumbers import AddLineNumbers
from .Indent import Indent
from .Truncate import Truncate
from .Wrap import Wrap


_DESIGN_NOTES = """
# Text Actions Decorate Sub-Package

## Purpose
Pipeline actions wrapping the decorate functions: line numbers, indentation, truncation, wrapping.

## Internal Components Registry

| Component        | Type   | Description |
| :--------------- | :----- | :---------- |
| `AddLineNumbers` | Action | Wraps `add_line_numbers`: puts a number in front of every line. |
| `Indent`         | Action | Wraps `indent`: puts a prefix in front of every non-blank line. |
| `Truncate`       | Action | Wraps `truncate`: shortens the text to a number of lines and / or characters and says so. |
| `Wrap`           | Action | Wraps `wrap`: wraps lines that are longer than a width, keeping indentation. |
"""
