from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern
from .._common.helpers import compile_pattern


@validate_call
def keep_matches(
    text: str,
    pattern: Pattern,
    *,
    flags: int = 0,
    separator: str = "\n",
) -> str:
    """Keep only the matches of a pattern.

    Args:
        text: The text.
        pattern: A literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.
        flags: `re` flags; not allowed with a compiled pattern.
        separator: What goes between the matches.

    Returns:
        The matches joined with the separator; an empty text if nothing matched.

    Raises:
        ParamError: If the pattern cannot be compiled, or flags come with a compiled pattern.
    """

    # 1. One compiled pattern whatever form came in
    compiled = compile_pattern(pattern, flags)

    # 2. Every match with some content — empty matches carry nothing to keep
    found = [match.group(0) for match in compiled.finditer(text) if match.end() > match.start()]

    # 3. Only the matches, one after another
    return separator.join(found)


_DESIGN_NOTES = """
# keep_matches — Only What Matched

## Purpose
Pull the pieces out of a text: all the function names, all the numbers.
The opposite of `remove_matches`.

## Not Position-Preserving
The result is a list of pieces joined with `separator`, not the original text
with everything else blanked out. The text around the matches is gone.

## Empty Matches
A pattern that can match nothing (`a*`) would otherwise add an empty piece
(and a separator) at every position. They are skipped.
"""
