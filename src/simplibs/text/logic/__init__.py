_DESIGN_NOTES = """
# Text Logic Package

## Purpose
The functional core of `simplibs-text`: plain functions `str -> str`, grouped by
what they do to the text. No `Rule` and no `Action` is known here; those are
thin layers built on top.

This package groups; it does not export. It has no imports of its own, so
importing it costs nothing and creates no import cycles.

## Internal Components Registry

| Sub-package | Kind                  | What it holds                                                                |
| :---------- | :-------------------- | :--------------------------------------------------------------------------- |
| `_common`   | Shared internal logic | Line splitting and joining, pattern compiling and their error cards.         |
| `case`      | Public functions      | `split_words`, `to_snake_case`, `to_kebab_case`, `to_camel_case`, `to_pascal_case`. |
| `clean`     | Public functions      | Unicode normalizing and removing accents, punctuation, symbols, non-ASCII.   |
| `decorate`  | Public functions      | `add_line_numbers`, `indent`, `truncate`, `wrap`.                            |
| `keep`      | Public functions      | `keep_matches`, `keep_lines_matching`, `keep_line_range`, `keep_between`.    |
| `recipes`   | Public functions      | `cleanup_whitespace`, `compact` — combinations of functions from `remove`.   |
| `remove`    | Public functions      | `remove_matches`, `remove_spans`, whitespace and blank-line cleanups, `dedent`. |
| `replace`   | Public functions      | `replace_matches`, `map_lines`.                                              |

## Layering & Design
- Domain sub-packages never import each other, only `_common`. The one exception is
  `recipes`, which combines functions and is the top layer; nothing imports it.
- Every function is pure: the same text in, the same text out, nothing on disk.
- Every function returns the very same text (equal and unchanged) if there is nothing to do.
"""
