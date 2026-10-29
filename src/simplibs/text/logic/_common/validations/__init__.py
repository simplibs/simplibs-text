from .raise_invalid_callback_result_error import raise_invalid_callback_result_error
from .raise_pattern_compile_error import raise_pattern_compile_error
from .raise_pattern_flags_conflict_error import raise_pattern_flags_conflict_error


_DESIGN_NOTES = """
# Text Common Diagnostic Helpers Sub-Package

## Purpose
Internal diagnostic helpers raising structured exceptions shared across the text logic.

## Internal Components Registry

| Component                              | Type     | Description                                                              |
| :------------------------------------- | :------- | :----------------------------------------------------------------------- |
| `raise_invalid_callback_result_error`  | Function | Raises `ParamError` when a caller's function returns something but a `str`. |
| `raise_pattern_compile_error`          | Function | Raises `ParamError` when a pattern cannot be compiled.                   |
| `raise_pattern_flags_conflict_error`   | Function | Raises `ParamError` when flags come with a compiled pattern.             |
"""
