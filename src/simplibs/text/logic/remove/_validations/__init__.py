from .raise_invalid_span_error import raise_invalid_span_error


_DESIGN_NOTES = """
# Remove Diagnostic Helpers Sub-Package

## Purpose
Internal diagnostic helpers raising structured exceptions for the remove functions.

## Internal Components Registry

| Component                 | Type     | Description                                          |
| :------------------------ | :------- | :--------------------------------------------------- |
| `raise_invalid_span_error`| Function | Raises `ParamError` when a span does not fit the text. |
"""
