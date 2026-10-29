from .split_words import split_words
from .to_camel_case import to_camel_case
from .to_kebab_case import to_kebab_case
from .to_pascal_case import to_pascal_case
from .to_snake_case import to_snake_case


_DESIGN_NOTES = """
# Case Logic Sub-Package

## Purpose
Functions that rewrite names between naming styles: words are split out of
whatever style the text uses and put together in the wanted one.

## Internal Components Registry

| Component        | Type     | Description                                                     |
| :--------------- | :------- | :-------------------------------------------------------------- |
| `split_words`    | Function | Splits a text or identifier into words (returns a list).        |
| `to_camel_case`  | Function | Writes each line in `camelCase`.                                |
| `to_kebab_case`  | Function | Writes each line in `kebab-case`.                               |
| `to_pascal_case` | Function | Writes each line in `PascalCase`.                               |
| `to_snake_case`  | Function | Writes each line in `snake_case`.                               |

## Layering & Design
- Layers go left to right: `_helpers` -> `split_words` -> `_conversion` -> `to_*`.
- All four conversions share `convert_lines` and differ only in how words are joined.
"""
