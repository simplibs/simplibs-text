from .KeepAscii import KeepAscii
from .NormalizeUnicode import NormalizeUnicode
from .RemoveDiacritics import RemoveDiacritics
from .RemoveNonAlphanumeric import RemoveNonAlphanumeric
from .RemovePunctuation import RemovePunctuation
from .RemoveSymbols import RemoveSymbols
from .ReplacePunctuation import ReplacePunctuation


_DESIGN_NOTES = """
# Text Actions Clean Sub-Package

## Purpose
Pipeline actions wrapping the clean functions: Unicode normalizing and removing accents, punctuation, symbols and non-ASCII.

## Internal Components Registry

| Component               | Type   | Description |
| :---------------------- | :----- | :---------- |
| `KeepAscii`             | Action | Wraps `keep_ascii`: keeps only the ASCII characters. |
| `NormalizeUnicode`      | Action | Wraps `normalize_unicode`: writes the text in one Unicode normalization form. |
| `RemoveDiacritics`      | Action | Wraps `remove_diacritics`: removes accents and other combining marks from letters. |
| `RemoveNonAlphanumeric` | Action | Wraps `remove_non_alphanumeric`: keeps only letters and digits. |
| `RemovePunctuation`     | Action | Wraps `remove_punctuation`: removes punctuation characters. |
| `RemoveSymbols`         | Action | Wraps `remove_symbols`: removes symbol characters (currency, math signs, emoji). |
| `ReplacePunctuation`    | Action | Wraps `replace_punctuation`: replaces every punctuation character with a text. |
"""
