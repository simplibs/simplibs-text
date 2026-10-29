from .remove.RemoveSpans import RemoveSpans
from .remove.RemoveMatches import RemoveMatches
from .remove.RemoveLinesMatching import RemoveLinesMatching
from .remove.RemoveEmptyLines import RemoveEmptyLines
from .remove.StripTrailingSpaces import StripTrailingSpaces
from .remove.SqueezeBlankLines import SqueezeBlankLines
from .remove.TrimBlankEdges import TrimBlankEdges
from .remove.Dedent import Dedent
from .keep.KeepMatches import KeepMatches
from .keep.KeepLinesMatching import KeepLinesMatching
from .keep.KeepLineRange import KeepLineRange
from .keep.KeepBetween import KeepBetween
from .replace.ReplaceMatches import ReplaceMatches
from .replace.MapLines import MapLines
from .decorate.AddLineNumbers import AddLineNumbers
from .decorate.Indent import Indent
from .decorate.Truncate import Truncate
from .decorate.Wrap import Wrap
from .clean.NormalizeUnicode import NormalizeUnicode
from .clean.RemoveDiacritics import RemoveDiacritics
from .clean.KeepAscii import KeepAscii
from .clean.RemovePunctuation import RemovePunctuation
from .clean.ReplacePunctuation import ReplacePunctuation
from .clean.RemoveSymbols import RemoveSymbols
from .clean.RemoveNonAlphanumeric import RemoveNonAlphanumeric
from .case.SplitWords import SplitWords
from .case.ToSnakeCase import ToSnakeCase
from .case.ToKebabCase import ToKebabCase
from .case.ToCamelCase import ToCamelCase
from .case.ToPascalCase import ToPascalCase


__all__ = [
    # remove — take something away
    "RemoveSpans",
    "RemoveMatches",
    "RemoveLinesMatching",
    "RemoveEmptyLines",
    "StripTrailingSpaces",
    "SqueezeBlankLines",
    "TrimBlankEdges",
    "Dedent",
    # keep — keep only a chosen part
    "KeepMatches",
    "KeepLinesMatching",
    "KeepLineRange",
    "KeepBetween",
    # replace — change parts of the text
    "ReplaceMatches",
    "MapLines",
    # decorate — add to or reshape the text
    "AddLineNumbers",
    "Indent",
    "Truncate",
    "Wrap",
    # clean — characters of the text
    "NormalizeUnicode",
    "RemoveDiacritics",
    "KeepAscii",
    "RemovePunctuation",
    "ReplacePunctuation",
    "RemoveSymbols",
    "RemoveNonAlphanumeric",
    # case — naming styles
    "SplitWords",
    "ToSnakeCase",
    "ToKebabCase",
    "ToCamelCase",
    "ToPascalCase",
]


_DESIGN_NOTES = """
# Text Actions Sub-Package

## Purpose
The functions of the library as `Action`s: constructed once with their options,
then called with the text and chainable with `>>`, `&` and `|`.

```python
pipeline = (
    RemoveMatches(pattern="# TODO")
    >> KeepLineRange(start=10, end=60)
    >> AddLineNumbers(start=10)
    >> Truncate(max_lines=40)
)
```

## One Direction Only
Every action takes the TEXT as its main input; the pattern, the limit or the
prefix is configuration. `file` offers a second direction for writers because it
has two things to carry (a path and a content). Here there is one thing to carry,
so a mirrored variant (`RemoveMatchesFrom(text=...)(pattern)`) would have no use.

## What Is Not Here
* **`cleanup_whitespace`, `compact`:** the ready-made chains are `CLEANUP_WHITESPACE`
  and `COMPACT` in `simplibs.text.presets`.
* **Helpers** such as `split_lines` or `compile_pattern`: internal, not steps.

## `SplitWords` Returns a List
The only action whose result is not a text. It ends a text pipeline; whatever
follows must accept a `list[str]`.

## Logging
All actions use the default logging of `create_action`.

## Async
All are synchronous actions; in an async pipeline they run through the usual
`acall` path of `simplibs-actions`.

## Domain Folder: `__all__`
This package defines `__all__` (the public actions), like `rules/` in the sibling
libraries; the sub-packages below export by plain imports.

## Internal Components Registry

| Sub-package | Kind    | Actions                                                                   |
| :---------- | :------ | :------------------------------------------------------------------------ |
| `remove` | Actions | `RemoveSpans`, `RemoveMatches`, `RemoveLinesMatching`, `RemoveEmptyLines`, `StripTrailingSpaces`, `SqueezeBlankLines`, `TrimBlankEdges`, `Dedent` |
| `keep` | Actions | `KeepMatches`, `KeepLinesMatching`, `KeepLineRange`, `KeepBetween` |
| `replace` | Actions | `ReplaceMatches`, `MapLines` |
| `decorate` | Actions | `AddLineNumbers`, `Indent`, `Truncate`, `Wrap` |
| `clean` | Actions | `NormalizeUnicode`, `RemoveDiacritics`, `KeepAscii`, `RemovePunctuation`, `ReplacePunctuation`, `RemoveSymbols`, `RemoveNonAlphanumeric` |
| `case` | Actions | `SplitWords`, `ToSnakeCase`, `ToKebabCase`, `ToCamelCase`, `ToPascalCase` |
"""
