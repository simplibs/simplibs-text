_DESIGN_NOTES = """
# Text Common Logic Sub-Package

## Purpose
Groups shared internal helper functions and diagnostic routines used across the
text logic sub-packages.

## Internal Components Registry

| Sub-package   | Kind                    | What it holds                                                                  |
| :------------ | :---------------------- | :----------------------------------------------------------------------------- |
| `helpers`     | Shared internal helpers | `split_lines`, `join_lines`, `is_blank`, `compile_pattern`.                    |
| `validations` | Diagnostic helpers      | Structured exception raisers for patterns (`raise_pattern_compile_error`, ...). |
"""
