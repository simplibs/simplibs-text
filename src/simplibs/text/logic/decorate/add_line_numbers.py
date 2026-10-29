from simplibs.types import int_non_negative, int_positive
from simplibs.validate import validate_call
# Outers
from .._common.helpers import join_lines, split_lines
# Inners
from ._validations import raise_invalid_template_error


@validate_call
def add_line_numbers(
    text: str,
    *,
    start: int_non_negative = 1,
    template: str = "{number:>{width}}: {line}",
    width: int_positive | None = None,
) -> str:
    """Put a number in front of every line.

    Args:
        text: The text.
        start: The number of the first line.
        template: A `str.format` template with the fields `{number}`, `{line}` and `{width}`.
        width: Width of the number field; `None` means as many digits as the last number has.

    Returns:
        The numbered lines. An empty text stays empty.

    Raises:
        ParamError: If the template cannot be filled in.
    """

    # 1. Try the template once, so a mistake is reported even for a short text
    try:
        template.format(number=start, line="", width=1)
    except (KeyError, IndexError, ValueError, AttributeError) as caught_exc:
        raise_invalid_template_error(template, caught_exc)

    # 2. The width that fits the last number, unless the caller chose one
    lines, has_end = split_lines(text)
    field_width = width or len(str(start + max(len(lines) - 1, 0)))

    # 3. Number every line, blank ones too
    numbered = [
        template.format(number=start + index, line=line, width=field_width)
        for index, line in enumerate(lines)
    ]

    return join_lines(numbered, has_end)


_DESIGN_NOTES = """
# add_line_numbers — Numbers in the Margin

## Purpose
Show code or text with line numbers, so a reader (or a model) can say
"line 42" and mean the same line.

## Template
Three fields: `{number}`, `{line}`, `{width}`. The default `"{number:>{width}}: {line}"`
right-aligns the numbers so the text stays in one column. The line is a VALUE
given to `format`, not part of the template, so braces inside the text are safe.

## Blank Lines
They are numbered too; numbers must match the lines of the original.

## `start`
`1` as editors count, `0` allowed for the programmer's count.
"""
