from .SplitWords import SplitWords
from .ToCamelCase import ToCamelCase
from .ToKebabCase import ToKebabCase
from .ToPascalCase import ToPascalCase
from .ToSnakeCase import ToSnakeCase


_DESIGN_NOTES = """
# Text Actions Case Sub-Package

## Purpose
Pipeline actions wrapping the case functions: splitting words and converting between naming styles.

## Internal Components Registry

| Component      | Type   | Description |
| :------------- | :----- | :---------- |
| `SplitWords`   | Action | Wraps `split_words`: splits the text into its words (a `list[str]`). |
| `ToCamelCase`  | Action | Wraps `to_camel_case`: writes every line in `camelCase`. |
| `ToKebabCase`  | Action | Wraps `to_kebab_case`: writes every line in `kebab-case`. |
| `ToPascalCase` | Action | Wraps `to_pascal_case`: writes every line in `PascalCase`. |
| `ToSnakeCase`  | Action | Wraps `to_snake_case`: writes every line in `snake_case`. |
"""
