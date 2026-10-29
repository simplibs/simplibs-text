from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern
from .._common.helpers import compile_pattern, join_lines, split_lines


@validate_call
def keep_lines_matching(
    text: str,
    pattern: Pattern,
    *,
    flags: int = 0,
) -> str:
    """Keep only the lines that contain a match of a pattern.

    Args:
        text: The text.
        pattern: A literal `str`, a compiled `re.Pattern` or a `Regex` tree.
        flags: `re` flags; not allowed with a compiled `re.Pattern`.

    Returns:
        The matching lines, whole; an empty text if none matches.

    Raises:
        ParamError: If the pattern cannot be compiled, or flags come with a compiled pattern.
    """

    # 1. One compiled pattern whatever form came in
    compiled = compile_pattern(pattern, flags)

    # 2. Keep the lines with a match
    lines, has_end = split_lines(text)
    kept = [line for line in lines if compiled.search(line)]

    # 3. Every line kept — the very same text back
    if len(kept) == len(lines):
        return text

    return join_lines(kept, has_end)


_DESIGN_NOTES = """
# keep_lines_matching — Whole Lines With a Match

## Purpose
`keep_lines_matching(source, "def ")` — an outline of a file. The mirror of
`remove_lines_matching`: the two split any text between them with no line lost
and none counted twice.

## Line by Line
The pattern is searched in each line separately (see `remove_lines_matching`).
"""
