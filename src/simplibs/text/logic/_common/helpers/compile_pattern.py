import re
from simplibs.regex.compiler import RegexPattern
# Outers
from ....annotations import Pattern
from ..validations import raise_pattern_compile_error, raise_pattern_flags_conflict_error


def compile_pattern(pattern: Pattern, flags: int = 0) -> re.Pattern:
    """Turn any accepted pattern into a compiled `re.Pattern`.

    Args:
        pattern: A literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.
        flags: `re` flags (e.g. `re.IGNORECASE`). Not allowed together with a
            compiled pattern (`re.Pattern`, `RegexPattern`), which already carries its own.

    Returns:
        The compiled pattern.

    Raises:
        ParamError: If flags come with a compiled pattern, or the pattern cannot be compiled.
    """

    # 1. A `RegexPattern` holds a compiled `re.Pattern` — take that one
    if isinstance(pattern, RegexPattern):
        pattern = pattern.compiled

    # 2. A compiled pattern is used as it is; flags would be silently ignored, so they are refused
    if isinstance(pattern, re.Pattern):
        if flags:
            raise_pattern_flags_conflict_error(pattern, flags)
        return pattern

    # 3. A text is a literal — escaped, so "(" and "." mean themselves
    if isinstance(pattern, str):
        source = re.escape(pattern)

    # 4. A `Regex` tree renders itself
    else:
        source = pattern.to_pattern()

    # 5. Compile; a tree can still render something `re` refuses
    try:
        return re.compile(source, flags)
    except (re.error, ValueError) as caught_exc:
        raise_pattern_compile_error(source, caught_exc)


_DESIGN_NOTES = """
# compile_pattern — One Door for Every Kind of Pattern

## Purpose
Every function that searches calls this first, so the four accepted forms
(see `Pattern`) behave the same everywhere.

## `RegexPattern`
It is only a wrapper around a `re.Pattern`, so its `.compiled` is taken and the
rest is the same as for any compiled pattern. A `lazy=True` pattern is compiled
at this moment.

## `flags` With a Compiled Pattern
`re.compile` itself refuses `flags` for an already compiled pattern; here it is
refused with a card that says what to do. Silently ignoring them would hide a
mistake such as `remove_matches(text, re.compile("a"), flags=re.I)`. The same
holds for a `RegexPattern`, whose flags are set when it is built.

## Flags and Literals
Flags work on a `str` literal too: `flags=re.IGNORECASE` finds `Abc` for `"abc"`.

## Compile Errors
`re.error` is raised for a bad pattern and `ValueError` for a bad combination
of flags (`re.LOCALE` with a `str` pattern). Both become one card.
"""
