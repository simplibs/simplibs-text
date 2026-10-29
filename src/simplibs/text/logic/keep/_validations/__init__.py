from .raise_invalid_line_range_error import raise_invalid_line_range_error


_DESIGN_NOTES = """
# Keep Diagnostic Helpers Sub-Package

## Purpose
Internal diagnostic helpers raising structured exceptions for the keep functions.

## Internal Components Registry

| Component                       | Type     | Description                                                   |
| :------------------------------ | :------- | :------------------------------------------------------------ |
| `raise_invalid_line_range_error`| Function | Raises `ParamError` when a line range ends before it starts.  |
"""
