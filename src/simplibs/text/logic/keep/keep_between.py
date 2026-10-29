from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern
from .._common.helpers import compile_pattern


@validate_call
def keep_between(
    text: str,
    start: Pattern,
    end: Pattern,
    *,
    include_markers: bool = True,
    flags: int = 0,
    separator: str = "\n",
) -> str:
    """Keep only the parts of a text between a start marker and an end marker.

    Args:
        text: The text.
        start: Marker where a kept part begins.
        end: Marker where it ends; looked for after the start marker.
        include_markers: Keep the markers themselves too.
        flags: `re` flags; not allowed with a compiled pattern.
        separator: What goes between the parts.

    Returns:
        The parts joined with the separator; an empty text if there is none.

    Raises:
        ParamError: If a marker cannot be compiled, or flags come with a compiled pattern.
    """

    # 1. Both markers compiled the same way as any other pattern
    start_pattern = compile_pattern(start, flags)
    end_pattern = compile_pattern(end, flags)

    # 2. Walk through the text: a start marker, then the first end marker after it
    parts: list[str] = []
    position = 0
    while position <= len(text):
        opening = start_pattern.search(text, position)
        if opening is None:
            break
        closing = end_pattern.search(text, opening.end())
        if closing is None:
            break

        # 2.1 What is kept of this part
        if include_markers:
            parts.append(text[opening.start():closing.end()])
        else:
            parts.append(text[opening.end():closing.start()])

        # 2.2 Continue after the part; always at least one step forward
        position = max(closing.end(), opening.start() + 1)

    return separator.join(parts)


_DESIGN_NOTES = """
# keep_between — From Marker to Marker

## Purpose
Cut a region out of a text: everything between `# region` and `# endregion`,
or between `<body>` and `</body>`.

## Two Searches Instead of One Combined Regex
Gluing the markers into `(start)(.*?)(end)` would use only the SOURCE of a
compiled marker and silently lose its flags. Searching for the start and then
for the end keeps each marker exactly as given, and a lookbehind in the end
marker still sees the text before it.

## Parts Do Not Overlap
The search for the next start continues after the end marker. A start marker
without an end marker after it ends the search; what follows is not a part.
The marker may span lines — nothing here works line by line.

## Empty Markers
A marker that matches nothing (`a*`) is allowed, but the loop always moves at
least one character forward, so it cannot run forever.
"""
