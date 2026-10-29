def is_line_number(value: int) -> bool:
    """Check whether a value is a usable line number (counted from 1).

    Args:
        value: The candidate.

    Returns:
        True for an `int` greater than zero; False for zero, negatives and `bool`.
    """

    # 1. A real integer (a bool is an int in Python, but never what the caller meant)
    if not isinstance(value, int) or isinstance(value, bool):
        return False

    # 2. Lines are counted from 1
    return value > 0


_DESIGN_NOTES = """
# is_line_number — "The First Line Is Line 1"

The rule behind `LineNumber`. Editors, error messages and `sed` all count from 1,
so the library does too. `0` is refused instead of being quietly read as "the
first line" or "before the first line", which is how an off-by-one slips in.
"""
