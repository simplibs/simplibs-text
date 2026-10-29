def split_lines(text: str) -> tuple[list[str], bool]:
    """Split a text into lines and remember whether it ended with a newline.

    Args:
        text: The text. Line endings are expected to be `"\\n"` (as `read_text` returns them).

    Returns:
        The lines without their `"\\n"` and `True` if the text ended with one.
        An empty text has no lines.
    """

    # 1. Nothing at all is no lines — not one empty line
    if text == "":
        return [], False

    # 2. Remember the final newline, then cut it off so it is not read as one more line
    has_end = text.endswith("\n")
    body = text[:-1] if has_end else text

    # 3. Split on "\n" only
    return body.split("\n"), has_end


_DESIGN_NOTES = """
# split_lines — Lines Without Losing the Last Newline

## Why Not `str.splitlines()`
It drops the information whether the text ended with a newline, and it also
splits on `\\x0b`, `\\x0c`, `\\x1c`, `\\u2028` and more — separators that are
ordinary characters in a source file. Here only `"\\n"` separates lines.

## The Pair
`join_lines(*split_lines(text))` gives back the exact input, for `""`, `"a"`,
`"a\\n"` and `"\\n"` too. Every line operation relies on that.
"""
