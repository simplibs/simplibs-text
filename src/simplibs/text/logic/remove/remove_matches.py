from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern
from .._common.helpers import compile_pattern
# Inners
from ._helpers import cut_spans, normalize_spans


@validate_call
def remove_matches(
    text: str,
    pattern: Pattern,
    *,
    flags: int = 0,
    drop_emptied_lines: bool = True,
) -> str:
    """Remove every match of a pattern from a text.

    Args:
        text: The text.
        pattern: A literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.
        flags: `re` flags; not allowed with a compiled pattern.
        drop_emptied_lines: A line that is blank only because of the removal
            disappears whole (a full-line comment leaves no hole). Blank lines
            that were there before stay.

    Returns:
        The text without the matches; the same text if nothing matched.

    Raises:
        ParamError: If the pattern cannot be compiled, or flags come with a compiled pattern.
    """

    # 1. One compiled pattern whatever form came in
    compiled = compile_pattern(pattern, flags)

    # 2. Where the matches are; empty matches are dropped by normalize_spans
    spans = normalize_spans([match.span() for match in compiled.finditer(text)], len(text))

    # 3. Nothing matched — the very same text back
    if not spans:
        return text

    # 4. Cut
    return cut_spans(text, spans, drop_emptied_lines)


_DESIGN_NOTES = """
# remove_matches — Delete What Matches

## Purpose
The basic "remove" step: strip comments, markers, noise.

## Literal by Default
A `str` pattern is a literal (see `Pattern`). `remove_matches(text, "# TODO")`
does what it says; a regex needs `re.compile(...)` or a `Regex` tree.

## Known Limit
A pattern knows nothing about the language. A regex for `#` comments removes
the `#` inside the string `"a # b"` as well. Correct removal in source code is
the job of the code extractor, which finds the spans with a real parser and
hands them to `remove_spans`.

## Empty Matches
A pattern that can match nothing (`a*`) produces zero-length matches. They are
ignored: they remove nothing and must not flag a line as emptied.
"""
