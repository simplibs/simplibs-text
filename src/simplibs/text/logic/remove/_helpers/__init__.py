from .cut_spans import cut_spans
from .normalize_spans import normalize_spans


_DESIGN_NOTES = """
# Remove Internal Helpers Sub-Package

## Purpose
Shared helper functions used internally by the remove functions.

## Internal Components Registry

| Component         | Type     | Description                                                           |
| :---------------- | :------- | :-------------------------------------------------------------------- |
| `cut_spans`       | Function | Removes normalized spans, optionally dropping lines emptied by it.    |
| `normalize_spans` | Function | Validates spans and turns them into sorted, separate, non-empty ranges. |
"""
