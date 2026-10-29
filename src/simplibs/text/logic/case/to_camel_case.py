from simplibs.validate import validate_call
# Inners
from ._conversion import convert_lines


def _join_camel(words: list[str]) -> str:
    """The first word in lowercase, every other with a capital first letter."""

    # 1. First word small, the rest as in PascalCase
    first, *rest = words
    return first.lower() + "".join(word[:1].upper() + word[1:].lower() for word in rest)


@validate_call
def to_camel_case(text: str) -> str:
    """Write every line of a text in `camelCase`.

    Args:
        text: The text; each line is converted separately.

    Returns:
        The converted text; the same text if it already was in this style.
    """

    # 1. One name per line
    return convert_lines(text, _join_camel)


_DESIGN_NOTES = """
# to_camel_case — `camelCase`

`my_var_name` and `MyVarName` become `myVarName`.

## Acronyms
`HTTPServer` becomes `httpServer` (see `to_pascal_case`).

## Digits
A word that is only digits stays as it is: `item_2_name` becomes `item2Name`.

## Single-Letter Words
`PascalCase` and `camelCase` cannot tell a one-letter word followed by a capital
from an acronym: `AB` may be `A` + `B` or `AB`. A text with such words (`x Ray`)
may change once more when converted a second time. `snake_case` and `kebab-case`
carry their separators and do not have this problem.

## Per Line, Indentation Kept
See `convert_lines`.
"""
