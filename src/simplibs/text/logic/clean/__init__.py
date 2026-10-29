from .keep_ascii import keep_ascii
from .normalize_unicode import normalize_unicode
from .remove_diacritics import remove_diacritics
from .remove_non_alphanumeric import remove_non_alphanumeric
from .remove_punctuation import remove_punctuation
from .remove_symbols import remove_symbols
from .replace_punctuation import replace_punctuation


_DESIGN_NOTES = """
# Clean Logic Sub-Package

## Purpose
Functions that clean the CHARACTERS of a text (accents, punctuation, symbols,
non-ASCII), as opposed to `remove`, which works with matches, lines and whitespace.

## Internal Components Registry

| Component                 | Type     | Description                                                   |
| :------------------------ | :------- | :------------------------------------------------------------ |
| `keep_ascii`              | Function | Keeps only ASCII characters.                                  |
| `normalize_unicode`       | Function | Writes the text in one Unicode normalization form.            |
| `remove_diacritics`       | Function | Removes accents and other combining marks.                    |
| `remove_non_alphanumeric` | Function | Keeps only letters and digits (and optionally whitespace).    |
| `remove_punctuation`      | Function | Removes punctuation characters.                               |
| `remove_symbols`          | Function | Removes symbol characters.                                    |
| `replace_punctuation`     | Function | Replaces every punctuation character with a text.             |

## Layering & Design
- Decisions about characters are taken from the Unicode database, not from hand-made lists.
"""
