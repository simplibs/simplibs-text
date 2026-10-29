from simplibs.validate import validate_call
# Inners
from ._conversion import convert_lines


@validate_call
def to_snake_case(text: str) -> str:
    """Write every line of a text in `snake_case`.

    Args:
        text: The text; each line is converted separately.

    Returns:
        The converted text; the same text if it already was in this style.
    """

    # 1. Words in lowercase, joined into one name per line
    return convert_lines(text, lambda words: "_".join(word.lower() for word in words))


_DESIGN_NOTES = """
# to_snake_case — `snake_case`

`MyVarName`, `my-var-name` and `my var name` all become `my_var_name`.

## Per Line, Indentation Kept
See `convert_lines`. A line without any word (blank, only punctuation) is kept as it is.

## Idempotent
A text that is already in this style comes back unchanged.
"""
