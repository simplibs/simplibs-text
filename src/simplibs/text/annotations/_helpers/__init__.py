from .is_line_number import is_line_number
from .is_pattern import is_pattern


_DESIGN_NOTES = """
# Text Annotations Internal Helpers Sub-Package

## Purpose
The predicates behind the annotated types of `simplibs-text`.

## Internal Components Registry

| Component        | Type     | Description                                                              |
| :--------------- | :------- | :----------------------------------------------------------------------- |
| `is_line_number` | Function | Checks that a value is an `int` of at least 1 (and not a `bool`).        |
| `is_pattern`     | Function | Checks that a value is a non-empty `str`, a `re.Pattern`, a `Regex` or a `RegexPattern`.   |"""
