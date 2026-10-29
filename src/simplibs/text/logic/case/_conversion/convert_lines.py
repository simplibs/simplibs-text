from collections.abc import Callable
# Outers
from ..._common.helpers import join_lines, split_lines
# Inners
from ..split_words import split_words


def convert_lines(
    text: str,
    join_words: Callable[[list[str]], str],
) -> str:
    """Rewrite every line as one identifier built from its words.

    Args:
        text: The text.
        join_words: Gets the words of a line and returns the line's new content.

    Returns:
        The converted text; lines without any word (blank, punctuation only) are kept as they are.
    """

    # 1. Line by line, so a text with many lines stays a text with many lines
    lines, has_end = split_lines(text)
    converted: list[str] = []
    for line in lines:
        words = split_words(line)
        if not words:
            converted.append(line)
            continue

        # 1.1 The indentation is not part of the name and stays
        lead = line[:len(line) - len(line.lstrip())]
        converted.append(lead + join_words(words))

    # 2. Nothing changed — the very same text back
    if converted == lines:
        return text

    return join_lines(converted, has_end)


_DESIGN_NOTES = """
# convert_lines — One Name per Line

## Purpose
The shared body of `to_snake_case`, `to_kebab_case`, `to_camel_case` and
`to_pascal_case`. They differ only in how the words are put together.

## Why per Line
A newline is a separator for `split_words`, so converting the whole text at once
would join all lines into one name. Converting line by line keeps the structure:
a list of names stays a list of names.

## Indentation
Kept, so an indented line of code or a nested list stays where it is.
"""
