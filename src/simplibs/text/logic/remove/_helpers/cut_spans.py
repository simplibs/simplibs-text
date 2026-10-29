# Outers
from ..._common.helpers import is_blank


def cut_spans(
    text: str,
    spans: list[tuple[int, int]],
    drop_emptied_lines: bool,
) -> str:
    """Remove normalized spans from a text.

    Args:
        text: The text.
        spans: Sorted, separate, non-empty `(start, end)` ranges (see `normalize_spans`).
        drop_emptied_lines: If True, a line that is blank only BECAUSE of the removal disappears whole.

    Returns:
        The text without the spans.
    """

    # 1. What stays between the spans; consecutive pieces were separated by one removal
    pieces: list[str] = []
    position = 0
    for start, end in spans:
        pieces.append(text[position:start])
        position = end
    pieces.append(text[position:])

    # 2. A plain cut — lines are not looked at
    if not drop_emptied_lines:
        return "".join(pieces)

    # 3. Rebuild line by line; `emptied` says that the current line lost something
    lines: list[str] = []
    buffer = ""
    emptied = False
    for index, piece in enumerate(pieces):
        if index > 0:
            emptied = True
        first, *rest = piece.split("\n")
        buffer += first
        for part in rest:
            if not (emptied and is_blank(buffer)):
                lines.append(buffer)
            buffer, emptied = part, False

    # 4. The last, not yet closed line
    if not (emptied and is_blank(buffer)):
        lines.append(buffer)

    return "\n".join(lines)


_DESIGN_NOTES = """
# cut_spans — Removal That Knows About Lines

## Purpose
The one place where text is actually cut. `remove_matches` and `remove_spans`
both end here, so a comment cut out by a regex and a docstring cut out by a
parser behave identically.

## Why Not a Marker Character
The first draft replaced each match with `\\x00`, then dropped lines that held
only the marker. That fails on a text that contains `\\x00` itself. Working
with positions needs no reserved character and no restriction on the input.

## Which Lines Disappear
Only a line that became blank BECAUSE of a removal. A blank line that was in
the text from the start stays. A removed span may contain newlines (a docstring
over five lines): what is left before and after it joins into one line, and that
one line is judged as a whole.

## The End of the Text
A text that ended with `"\\n"` still ends with it, and one that did not still
does not. If the last line itself is emptied, it goes and the text then ends
after the previous line. The result is joined with `"\\n"` directly: the part
after the last newline is always there as the final, possibly empty, element.
"""
