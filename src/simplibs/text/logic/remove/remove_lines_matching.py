from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern
from .._common.helpers import compile_pattern, join_lines, split_lines


@validate_call
def remove_lines_matching(
    text: str,
    pattern: Pattern,
    *,
    flags: int = 0,
) -> str:
    """Remove every line that contains a match of a pattern.

    Args:
        text: The text.
        pattern: A literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.
        flags: `re` flags; not allowed with a compiled pattern.

    Returns:
        The text without the matching lines.

    Raises:
        ParamError: If the pattern cannot be compiled, or flags come with a compiled pattern.
    """

    # 1. One compiled pattern whatever form came in
    compiled = compile_pattern(pattern, flags)

    # 2. Keep the lines without a match
    lines, has_end = split_lines(text)
    kept = [line for line in lines if not compiled.search(line)]

    # 3. Nothing matched — the very same text back
    if len(kept) == len(lines):
        return text

    return join_lines(kept, has_end)


_DESIGN_NOTES = """
# remove_lines_matching — the Whole Line Goes

## Purpose
Remove lines like `import x`, `# TODO ...` or `print(...)` entirely.

## Difference From `remove_matches`
`remove_matches` cuts out the match and leaves the rest of the line;
this function removes the line even if the match is only part of it.

## Line by Line
The pattern is searched in each line separately, so `^` and `$` mean the start
and the end of a line without any `re.MULTILINE`, and a match can never span
lines.
"""
