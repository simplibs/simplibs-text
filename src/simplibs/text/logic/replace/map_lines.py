from collections.abc import Callable
from simplibs.validate import validate_call
# Outers
from .._common.helpers import join_lines, split_lines
from .._common.validations import raise_invalid_callback_result_error


@validate_call
def map_lines(
    text: str,
    func: Callable[[str], str],
) -> str:
    """Apply a function to every line.

    Args:
        text: The text.
        func: Gets a line without its newline and returns the new line (a `str`).

    Returns:
        The text made of the new lines; the same text if no line changed.

    Raises:
        ParamError: If the function returns something but a `str`.
    """

    # 1. Call the function on every line and check what comes back
    lines, has_end = split_lines(text)
    mapped: list[str] = []
    for number, line in enumerate(lines, start=1):
        result = func(line)
        if not isinstance(result, str):
            raise_invalid_callback_result_error(func, result, f"line {number}")
        mapped.append(result)

    # 2. Nothing changed — the very same text back
    if mapped == lines:
        return text

    return join_lines(mapped, has_end)


_DESIGN_NOTES = """
# map_lines — One Function, Every Line

## Purpose
The open door of the library: when no ready step fits, `map_lines(text, str.upper)`
or `map_lines(text, my_rule)` does the job and still takes part in pipelines.

## What the Function Sees
A line without its newline. The newline is put back by the library, so a
function never has to care whether a line was the last one.

## Returned Newlines
A returned `str` may contain `"\\n"`; it is used as it is, so one line can
become several. The function decides — it is not checked.

## Not for Dropping Lines
Return an empty string and the line stays as an empty line. To drop lines use
`remove_lines_matching` or `remove_empty_lines`.
"""
