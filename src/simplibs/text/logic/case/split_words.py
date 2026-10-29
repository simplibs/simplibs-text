from simplibs.validate import validate_call
# Inners
from ._helpers import is_mark, starts_new_word


@validate_call
def split_words(text: str) -> list[str]:
    """Split a text or an identifier into its words.

    Understands spaces, `snake_case`, `kebab-case`, `camelCase`, `PascalCase`
    and acronyms (`HTMLParser` -> `HTML`, `Parser`).

    Args:
        text: The text.

    Returns:
        The words in their original letter case; no empty words.
    """

    # 1. Walk through the characters; anything that is not a letter or a digit separates words
    words: list[str] = []
    current: list[str] = []
    for index, char in enumerate(text):

        # 1.1 A combining mark belongs to the letter before it; with no word open, it is dropped
        if is_mark(char):
            if current:
                current.append(char)
            continue

        if not char.isalnum():
            if current:
                words.append("".join(current))
                current = []
            continue

        # 1.2 Inside a run a capital may start a new word (fooBar, HTMLParser)
        if current and starts_new_word(text, index):
            words.append("".join(current))
            current = []
        current.append(char)

    # 2. The last word
    if current:
        words.append("".join(current))

    return words


_DESIGN_NOTES = """
# split_words — the Common Ground of All Naming Styles

## Purpose
Every case conversion starts here: take the words out, then put them together
the way the target style wants.

## Examples
`"my_var-name"`, `"myVarName"`, `"MyVarName"`, `"my var name"` -> `["my", "var", "name"]`.
`"HTTPServer2Go"` -> `["HTTP", "Server2", "Go"]`. `"don't"` -> `["don", "t"]`.

## Any Script
`isalnum`, `isupper` and `islower` are Unicode-aware, so `"příliš žlutý"` and
`"PříšerněŽlutý"` split as expected. A script without letter case (Chinese) forms
one word per run.

## Combining Marks
A mark is part of the word it follows, so `"हिंदी"` is one word, and a text with
accents written as separate characters (`e` + `´`, as file names from some
systems are) gives the same words as the same text with composed letters.

## Returns a List
It is the one function of this package that does not return a text. It is still a
fine pipeline step, and it is what a caller with their own style (Title Case,
`CONSTANT_CASE`) builds on.
"""
