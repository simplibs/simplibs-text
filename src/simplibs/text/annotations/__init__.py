from .LineNumber import LineNumber
from .Pattern import Pattern
from .Replacement import Replacement
from .UnicodeForm import UnicodeForm


_DESIGN_NOTES = """
# annotations — Shared Types of simplibs-text

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component     | Type           | Description                                                           |
| :------------ | :------------- | :-------------------------------------------------------------------- |
| `LineNumber`  | Annotated Type | A line number counted from 1.                                         |
| `Pattern`     | Annotated Type | A literal `str`, a `re.Pattern`, a `Regex` tree or a `RegexPattern` to search for.      || `Replacement` | Type Alias     | A literal `str`, or a function from a `re.Match` to a `str`.          |
| `UnicodeForm` | Literal        | One of the four Unicode normalization forms.                          |
"""
