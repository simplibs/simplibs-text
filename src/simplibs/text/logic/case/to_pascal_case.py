from simplibs.validate import validate_call
# Inners
from ._conversion import convert_lines


@validate_call
def to_pascal_case(text: str) -> str:
    """Write every line of a text in `PascalCase`.

    Args:
        text: The text; each line is converted separately.

    Returns:
        The converted text; the same text if it already was in this style.
    """

    # 1. Every word with a capital first letter, joined without a separator
    return convert_lines(text, lambda words: "".join(word[:1].upper() + word[1:].lower() for word in words))


_DESIGN_NOTES = """
# to_pascal_case — `PascalCase`

`my_var_name` and `my var name` become `MyVarName`.

## Acronyms
`HTTPServer` becomes `HttpServer`: the style capitalizes only the first letter of
each word. Converting back with `to_snake_case` gives `http_server`.

## Single-Letter Words
`PascalCase` and `camelCase` cannot tell a one-letter word followed by a capital
from an acronym: `AB` may be `A` + `B` or `AB`. A text with such words (`x Ray`)
may change once more when converted a second time. `snake_case` and `kebab-case`
carry their separators and do not have this problem.

## Per Line, Indentation Kept
See `convert_lines`.
"""
