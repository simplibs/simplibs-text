from .is_mark import is_mark
from .starts_new_word import starts_new_word


_DESIGN_NOTES = """
# Case Internal Helpers Sub-Package

## Purpose
Low-level helper functions used by `split_words`.

## Internal Components Registry

| Component         | Type     | Description                                                       |
| :---------------- | :------- | :---------------------------------------------------------------- |
| `is_mark`         | Function | Tells a combining mark (accent, vowel sign) from a letter.        |
| `starts_new_word` | Function | Decides whether a word begins inside a run of letters and digits. |

## Layering
`_helpers` knows nothing of `split_words`; `_conversion` builds on it.
`starts_new_word` builds on `is_mark`.
"""
