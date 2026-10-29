import re
from simplibs.types import int_non_negative
from simplibs.validate import validate_call
# Outers
from ...annotations import Pattern, Replacement
from .._common.helpers import compile_pattern
from .._common.validations import raise_invalid_callback_result_error


@validate_call
def replace_matches(
    text: str,
    pattern: Pattern,
    replacement: Replacement,
    *,
    flags: int = 0,
    count: int_non_negative = 0,
) -> str:
    """Replace the matches of a pattern.

    Args:
        text: The text.
        pattern: A literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.
        replacement: A literal `str`, or a function that gets the `re.Match` and returns a `str`.
        flags: `re` flags; not allowed with a compiled pattern.
        count: How many matches to replace, from the start; `0` means all of them.

    Returns:
        The text with the replacements; the same text if nothing matched.

    Raises:
        ParamError: If the pattern cannot be compiled, flags come with a compiled
            pattern, or the function returns something but a `str`.
    """

    # 1. One compiled pattern whatever form came in
    compiled = compile_pattern(pattern, flags)

    # 2. A text is put in as it is; a function is called for every match and checked
    if isinstance(replacement, str):
        def substitute(match: re.Match) -> str:
            return replacement
    else:
        def substitute(match: re.Match) -> str:
            result = replacement(match)
            if not isinstance(result, str):
                raise_invalid_callback_result_error(
                    replacement, result, f"the match at {match.start()}"
                )
            return result

    # 3. Replace; nothing matched means the very same text back
    replaced = compiled.sub(substitute, text, count=count)
    return text if replaced == text else replaced


_DESIGN_NOTES = """
# replace_matches — Change What Matched

## Literal Replacement
A `str` replacement is inserted as it is (see `Replacement`): no `\\1`, no
`\\g<name>`, no escape errors. The text goes through a function so that
`re.sub` never interprets it.

## Groups and Computed Values
Pass a function: `lambda m: m.group("year")`, `lambda m: m.group(0).upper()`.

## `count`
`0` replaces everything, as in `re.sub`. A positive number replaces that many
matches from the start of the text.

## Empty Matches
A pattern that can match nothing (`a*`, or `^` with `re.MULTILINE`) matches at
positions, and each of those matches is replaced. That is what makes
`replace_matches(text, re.compile("^", re.M), "> ")` a way to prefix every line.
Note that `^` with `re.MULTILINE` also matches after a final newline, so a text
ending with `"\\n"` gets one more prefix at its very end. `remove_matches` and
`keep_matches` skip empty matches because they have nothing to cut or keep;
replacing is the place where an empty match still means something (insertion).

## Removing
`replacement=""` removes the matches but leaves their lines (a line that became
blank stays). Use `remove_matches` when emptied lines should disappear.
"""
