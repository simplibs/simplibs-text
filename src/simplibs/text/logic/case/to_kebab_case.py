from simplibs.validate import validate_call
# Inners
from ._conversion import convert_lines


@validate_call
def to_kebab_case(text: str) -> str:
    """Write every line of a text in `kebab-case`.

    Args:
        text: The text; each line is converted separately.

    Returns:
        The converted text; the same text if it already was in this style.
    """

    # 1. Words in lowercase, joined into one name per line
    return convert_lines(text, lambda words: "-".join(word.lower() for word in words))


_DESIGN_NOTES = """
# to_kebab_case — `kebab-case`

`MyVarName`, `my_var_name` and `my var name` all become `my-var-name`.

## Per Line, Indentation Kept
See `convert_lines`. A line without any word (blank, only punctuation) is kept as it is.

## Idempotent
A text that is already in this style comes back unchanged.
"""
