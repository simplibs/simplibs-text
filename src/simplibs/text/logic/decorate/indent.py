from simplibs.types import int_non_negative
from simplibs.validate import validate_call
# Outers
from .._common.helpers import is_blank, join_lines, split_lines


@validate_call
def indent(
    text: str,
    prefix: str | int_non_negative = "    ",
) -> str:
    """Put a prefix in front of every non-blank line.

    Args:
        text: The text.
        prefix: The text to put in front, or a number of spaces.

    Returns:
        The indented text; blank lines are left as they are. The same text
        if there is nothing to add.
    """

    # 1. A number means that many spaces
    if isinstance(prefix, int):
        prefix = " " * prefix

    # 2. Nothing to add — the very same text back
    if prefix == "":
        return text

    # 3. Prefix the lines that have something on them
    lines, has_end = split_lines(text)
    indented = [line if is_blank(line) else prefix + line for line in lines]

    return join_lines(indented, has_end)


_DESIGN_NOTES = """
# indent — Move a Block to the Right

## Purpose
The opposite of `dedent`. Put a function body into a class, a snippet into a
Markdown list, a quoted text behind `"> "`.

## Blank Lines
Left alone, so no line is made of spaces only. That also keeps the step
reversible: `dedent(indent(text))` gives back the text for ordinary content.

## Number or Text
`indent(text, 2)` is two spaces, `indent(text, "> ")` is a quote mark.
"""
