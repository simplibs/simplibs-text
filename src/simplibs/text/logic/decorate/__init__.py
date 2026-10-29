from .add_line_numbers import add_line_numbers
from .indent import indent
from .truncate import truncate
from .wrap import wrap


_DESIGN_NOTES = """
# Decorate Logic Sub-Package

## Purpose
Functions that add something to a text or reshape it without removing content:
line numbers, indentation, a cut with a marker, wrapped lines.

## Internal Components Registry

| Component          | Type     | Description                                                       |
| :----------------- | :------- | :---------------------------------------------------------------- |
| `add_line_numbers` | Function | Puts a number in front of every line.                             |
| `indent`           | Function | Puts a prefix in front of every non-blank line.                   |
| `truncate`         | Function | Shortens a text to a number of lines and / or characters.         |
| `wrap`             | Function | Wraps lines longer than a width, keeping indentation.             |
"""
