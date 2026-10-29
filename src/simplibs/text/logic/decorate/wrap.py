import textwrap
from simplibs.types import int_positive
from simplibs.validate import validate_call
# Outers
from .._common.helpers import is_blank, join_lines, split_lines


@validate_call
def wrap(
    text: str,
    width: int_positive = 80,
    *,
    break_long_words: bool = False,
) -> str:
    """Wrap lines that are longer than `width`, keeping each line's indentation.

    Args:
        text: The text.
        width: The longest allowed line.
        break_long_words: Split a single word that is longer than the line.
            By default such a word stays whole on its own line.

    Returns:
        The text with long lines wrapped; lines that fit are untouched.
    """

    # 1. Wrap line by line; a line that fits (or is blank) is not touched at all
    lines, has_end = split_lines(text)
    wrapped: list[str] = []
    for line in lines:
        if len(line) <= width or is_blank(line):
            wrapped.append(line)
            continue

        # 1.1 The continuation lines get the same indentation as the first
        lead = line[:len(line) - len(line.lstrip())]
        wrapped.append(
            textwrap.fill(
                line.strip(),
                width=width,
                initial_indent=lead,
                subsequent_indent=lead,
                break_long_words=break_long_words,
                break_on_hyphens=False,
                expand_tabs=False,
                replace_whitespace=False,
            )
        )

    # 2. Nothing wrapped — the very same text back
    if wrapped == lines:
        return text

    return join_lines(wrapped, has_end)


_DESIGN_NOTES = """
# wrap — Long Lines, Short Lines

## Purpose
Make prose and comments fit a width without ruining indentation.

## What It Does Not Touch
A line that already fits keeps every character, tabs and inner spaces included.
Only an overlong line is rebuilt, and then without changing tabs and whitespace
inside it (`expand_tabs` and `replace_whitespace` are off).

## No Breaking at Hyphens
`textwrap` splits `kebab-case-name` at its hyphens by default. In code and
identifiers that changes meaning, so words break only at whitespace.

## Long Words
A word longer than `width` (a URL) stays whole by default; `break_long_words=True`
splits it. Better a long line than a broken link.

## Width and Tabs
A tab counts as one character, so a line indented with tabs is measured shorter
than it looks.
"""
