from .has_category import has_category
from .is_diacritic_mark import is_diacritic_mark


_DESIGN_NOTES = """
# Clean Internal Helpers Sub-Package

## Purpose
Shared helper functions used internally by the clean functions.

## Internal Components Registry

| Component          | Type     | Description                                                        |
| :----------------- | :------- | :----------------------------------------------------------------- |
| `has_category`     | Function | Checks a character's Unicode general category.                     |
| `is_diacritic_mark`| Function | Checks that a character is a combining diacritical mark.           |
"""
