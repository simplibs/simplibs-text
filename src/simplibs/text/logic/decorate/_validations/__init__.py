from .raise_invalid_template_error import raise_invalid_template_error
from .raise_missing_limit_error import raise_missing_limit_error


_DESIGN_NOTES = """
# Decorate Diagnostic Helpers Sub-Package

## Purpose
Internal diagnostic helpers raising structured exceptions for the decorate functions.

## Internal Components Registry

| Component                      | Type     | Description                                                  |
| :----------------------------- | :------- | :----------------------------------------------------------- |
| `raise_invalid_template_error` | Function | Raises `ParamError` when a line template cannot be filled in. |
| `raise_missing_limit_error`    | Function | Raises `ParamError` when `truncate` gets no limit.            |
"""
