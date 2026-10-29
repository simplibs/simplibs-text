# Inners
from .is_mark import is_mark


def starts_new_word(text: str, index: int) -> bool:
    """Check whether a new word begins at an index inside a run of letters and digits.

    Args:
        text: The text.
        index: Position of a letter or digit that has a letter or digit before it
            (marks standing between do not count).

    Returns:
        True at a lower-to-upper step (`fooBar`), after a digit before a capital
        (`v2Beta`), and at the end of an acronym (`HTMLParser`: before `P`).
    """

    # 1. Only a capital can begin a word inside a run
    current = text[index]
    if not current.isupper():
        return False

    # 2. The letter before, looking past combining marks (`e` + accent is still `e`)
    previous_index = index - 1
    while previous_index > 0 and is_mark(text[previous_index]):
        previous_index -= 1
    previous = text[previous_index]

    # 3. After a lowercase letter or a digit: fooBar, v2Beta
    if previous.islower() or previous.isdigit():
        return True

    # 4. The last capital of an acronym that is followed by lowercase: HTMLParser
    following_index = index + 1
    while following_index < len(text) and is_mark(text[following_index]):
        following_index += 1
    following = text[following_index] if following_index < len(text) else ""
    return previous.isupper() and following.islower()


_DESIGN_NOTES = """
# starts_new_word — Where `camelCase` Falls Apart

## The Rules
`fooBar` -> `foo|Bar`; `HTMLParser` -> `HTML|Parser`; `v2Beta` -> `v2|Beta`;
`HTTP2Server` -> `HTTP2|Server`.

## Not a Boundary
Between a letter and a digit (`utf8`, `base64`, `2fa` stay whole) — the digits
belong to the word they stand next to. Names such as `utf8` would otherwise
become `utf_8` and be unrecognisable.

## Combining Marks
The neighbours are judged past any combining marks, so a word written with
separate accents (`cafe` + `´` + `Bar`) splits where `café` + `Bar` does.
"""
