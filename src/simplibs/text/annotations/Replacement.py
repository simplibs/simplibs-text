import re
from collections.abc import Callable


Replacement = str | Callable[[re.Match], str]
"""What to put in place of a match: a literal `str`, or a function from the match to a `str`."""


_DESIGN_NOTES = """
# Replacement — a Text, or a Rule for Making It

## Purpose
The type of the `replacement` parameter of `replace_matches`.

## A `str` Is Literal
Like `Pattern`, a `str` means itself. `"\\1"` or `"\\g<name>"` are NOT group
references here — they are two ordinary characters. A surprise from a stray
backslash (`re.error: bad escape`) is therefore impossible.

## Using Groups
Pass a function: `lambda match: match.group(1).upper()`. It gets the whole
`re.Match`, so named groups, positions and everything else are available.

## Why Not `Annotated`
There is nothing to check beyond the type: any `str` is fine, including `""`
(that is a removal) — unlike `Pattern`, where the empty string is a mistake.
"""
