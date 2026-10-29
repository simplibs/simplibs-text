def join_lines(lines: list[str], has_end: bool) -> str:
    """Join lines back into a text.

    Args:
        lines: The lines, without their `"\\n"`.
        has_end: Whether the text should end with a newline.

    Returns:
        The text. No lines give an empty text, even with `has_end=True`.
    """

    # 1. No lines, no text — a lone newline would be one empty line, not nothing
    if not lines:
        return ""

    # 2. Join, and close the last line if the text was closed
    return "\n".join(lines) + ("\n" if has_end else "")


_DESIGN_NOTES = """
# join_lines — the Inverse of `split_lines`

## Empty Collection
`split_lines("")` returns no lines, so `join_lines([], ...)` returns `""`.
An operation that removes every line therefore leaves an empty text, not a
single newline.
"""
