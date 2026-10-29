def is_blank(line: str) -> bool:
    """Check whether a line holds nothing but whitespace.

    Args:
        line: One line, without its newline.

    Returns:
        True for an empty line and for a line of spaces, tabs and other whitespace.
    """

    # 1. Whitespace only
    return line.strip() == ""


_DESIGN_NOTES = """
# is_blank — "Looks Empty"

One definition of an empty line for the whole library, so `remove_empty_lines`,
`squeeze_blank_lines` and `trim_blank_edges` never disagree about a line that
holds a single space.
"""
