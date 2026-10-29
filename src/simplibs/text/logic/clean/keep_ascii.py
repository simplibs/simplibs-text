from simplibs.validate import validate_call


@validate_call
def keep_ascii(text: str) -> str:
    """Keep only the ASCII characters (code points 0 to 127).

    Args:
        text: The text.

    Returns:
        The text without any other character; the same text if it was ASCII only.
    """

    # 1. A plain ASCII text needs no work
    if text.isascii():
        return text

    # 2. Keep what is ASCII — including newlines and tabs, so lines stay lines
    return "".join(char for char in text if char.isascii())


_DESIGN_NOTES = """
# keep_ascii — What an Old System Can Read

## Purpose
Prepare text for places that accept only ASCII.

## Dropping, Not Converting
Non-ASCII characters are removed, not approximated. `Příliš` becomes `Pli`.
Use `remove_diacritics` first to keep `Prilis`.
"""
