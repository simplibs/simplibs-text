from .logic.case import (
    split_words,
    to_camel_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case,
)
from .logic.clean import (
    keep_ascii,
    normalize_unicode,
    remove_diacritics,
    remove_non_alphanumeric,
    remove_punctuation,
    remove_symbols,
    replace_punctuation,
)
from .logic.decorate import (
    add_line_numbers,
    indent,
    truncate,
    wrap,
)
from .logic.keep import (
    keep_between,
    keep_line_range,
    keep_lines_matching,
    keep_matches,
)
from .logic.recipes import (
    cleanup_whitespace,
    compact,
)
from .logic.remove import (
    dedent,
    remove_empty_lines,
    remove_lines_matching,
    remove_matches,
    remove_spans,
    squeeze_blank_lines,
    strip_trailing_spaces,
    trim_blank_edges,
)
from .logic.replace import (
    map_lines,
    replace_matches,
)
from .annotations import (
    LineNumber,
    Pattern,
    Replacement,
    Span,
    UnicodeForm,
)

__all__ = [
    # remove — take something away
    "remove_spans",
    "remove_matches",
    "remove_lines_matching",
    "remove_empty_lines",
    "strip_trailing_spaces",
    "squeeze_blank_lines",
    "trim_blank_edges",
    "dedent",
    # keep — keep only a chosen part
    "keep_matches",
    "keep_lines_matching",
    "keep_line_range",
    "keep_between",
    # replace — change parts of the text
    "replace_matches",
    "map_lines",
    # decorate — add to or reshape the text
    "add_line_numbers",
    "indent",
    "truncate",
    "wrap",
    # clean — the characters of the text
    "normalize_unicode",
    "remove_diacritics",
    "keep_ascii",
    "remove_punctuation",
    "replace_punctuation",
    "remove_symbols",
    "remove_non_alphanumeric",
    # case — naming styles
    "split_words",
    "to_snake_case",
    "to_kebab_case",
    "to_camel_case",
    "to_pascal_case",
    # recipes — ready-made combinations
    "cleanup_whitespace",
    "compact",
    # annotations — types for your own signatures
    "LineNumber",
    "Pattern",
    "Replacement",
    "Span",
    "UnicodeForm",
]


_DESIGN_NOTES = """
# simplibs-text — Package Root

## Purpose
Small, safe steps that turn one text into another: remove, keep, replace,
decorate, clean and convert between naming styles — as plain functions
(`str -> str`) and as pipeline `Action`s.

## What the Root Exports
Every function of the `logic/` sub-packages and the public annotations:

    from simplibs.text import remove_matches, keep_line_range, to_snake_case, Pattern

## What the Root Deliberately Does NOT Export
* **`actions/` and `presets/`** — domain folders with their own `__all__`,
  imported through their domain:

      from simplibs.text.actions import RemoveMatches, KeepLineRange
      from simplibs.text.presets import CLEANUP_WHITESPACE, COMPACT

  A function and an action are different kinds of thing and should stay visibly
  different at the import line.
* **Internals** — `_common/`, `_helpers/`, `_validations/` and `_conversion/`.

## Why the Annotations ARE Exported
`Pattern`, `Replacement`, `LineNumber`, `Span` and `UnicodeForm` are meant for
the caller's own signatures, always used with the functions.

## Text Is Literal by Default
A `str` pattern and a `str` replacement mean exactly themselves. Regex enters
through `re.compile(...)`, a `Regex` tree or a `RegexPattern` from `simplibs-regex`.

## `__all__`
Defined here and in the domain folders (`actions`, `presets`) only; the
sub-packages below export by plain imports.

## Internal Components Registry (Root Exports)

| Component                 | Type           | Description |
| :------------------------ | :------------- | :---------- |
| `remove_spans`            | Function       | Cuts the given character ranges out of the text flowing in. |
| `remove_matches`          | Function       | Removes every match of a pattern from the text flowing in. |
| `remove_lines_matching`   | Function       | Removes the lines that contain a match. |
| `remove_empty_lines`      | Function       | Removes blank lines. |
| `strip_trailing_spaces`   | Function       | Removes spaces and tabs from the ends of lines. |
| `squeeze_blank_lines`     | Function       | Shortens runs of blank lines. |
| `trim_blank_edges`        | Function       | Removes blank lines at the start and at the end. |
| `dedent`                  | Function       | Removes the indentation common to all non-blank lines. |
| `keep_matches`            | Function       | Keeps only the matches of a pattern, joined with a separator. |
| `keep_lines_matching`     | Function       | Keeps only the lines that contain a match. |
| `keep_line_range`         | Function       | Keeps the lines from `start` to `end`. |
| `keep_between`            | Function       | Keeps the parts between a start marker and an end marker. |
| `replace_matches`         | Function       | Replaces the matches of a pattern by a text or by a function's result. |
| `map_lines`               | Function       | Applies a function to every line. |
| `add_line_numbers`        | Function       | Puts a number in front of every line. |
| `indent`                  | Function       | Puts a prefix in front of every non-blank line. |
| `truncate`                | Function       | Shortens the text to a number of lines and / or characters and says so. |
| `wrap`                    | Function       | Wraps lines that are longer than a width, keeping indentation. |
| `normalize_unicode`       | Function       | Writes the text in one Unicode normalization form. |
| `remove_diacritics`       | Function       | Removes accents and other combining marks from letters. |
| `keep_ascii`              | Function       | Keeps only the ASCII characters. |
| `remove_punctuation`      | Function       | Removes punctuation characters. |
| `replace_punctuation`     | Function       | Replaces every punctuation character with a text. |
| `remove_symbols`          | Function       | Removes symbol characters (currency, math signs, emoji). |
| `remove_non_alphanumeric` | Function       | Keeps only letters and digits. |
| `split_words`             | Function       | Splits the text into its words (a `list[str]`). |
| `to_snake_case`           | Function       | Writes every line in `snake_case`. |
| `to_kebab_case`           | Function       | Writes every line in `kebab-case`. |
| `to_camel_case`           | Function       | Writes every line in `camelCase`. |
| `to_pascal_case`          | Function       | Writes every line in `PascalCase`. |
| `cleanup_whitespace`      | Function       | Strips line ends, shrinks blank runs to one line, trims the edges. |
| `compact`                 | Function       | Strips line ends and removes every blank line. |
| `LineNumber`              | Annotated Type | A line number counted from 1. |
| `Pattern`                 | Annotated Type | A literal `str`, a `re.Pattern`, a `Regex` tree or a `RegexPattern` to search for. |
| `Replacement`             | Type Alias     | A literal `str`, or a function from a `re.Match` to a `str`. |
| `Span`                    | Type Alias     | A range of characters `(start, end)`, half-open. |
| `UnicodeForm`             | Literal        | One of the four Unicode normalization forms. |
"""
