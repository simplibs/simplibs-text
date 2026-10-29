from typing import Literal


UnicodeForm = Literal["NFC", "NFD", "NFKC", "NFKD"]
"""The four Unicode normalization forms."""


_DESIGN_NOTES = """
# UnicodeForm — the Four Ways to Write the Same Letter

## Purpose
The type of `form` in `normalize_unicode`.

## The Forms
* `NFC` — composed: `é` is one character. The usual form for storing and comparing.
* `NFD` — decomposed: `é` is `e` plus a combining accent.
* `NFKC` / `NFKD` — the same, and also "compatibility" characters become their
  plain equivalents (`ﬁ` -> `fi`, `²` -> `2`, a full-width `Ａ` -> `A`).

## Why a Literal
A typo (`"NFC "`, `"nfc"`) fails at the signature, not deep inside `unicodedata`.
"""
