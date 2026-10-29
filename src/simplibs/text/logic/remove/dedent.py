import textwrap
from simplibs.validate import validate_call


@validate_call
def dedent(text: str) -> str:
    """Remove the indentation that every non-blank line has in common.

    Args:
        text: The text.

    Returns:
        The text moved to the left. Whitespace-only lines become empty lines.
    """

    # 1. The standard library already does exactly this
    return textwrap.dedent(text)


_DESIGN_NOTES = """
# dedent — Move a Block to the Left

## Purpose
A function body cut out of a class is indented by four spaces; after this it
starts in the first column.

## Whitespace-Only Lines
`textwrap.dedent` turns them into empty lines and ignores them when looking for
the common indentation. That is wanted here and it is not hidden: the result
of `dedent` on an already flush-left text with such lines is not byte-identical.

## Tabs and Spaces
They are different characters: a line with a tab and a line with spaces have
no common indentation, and nothing is removed.
"""
