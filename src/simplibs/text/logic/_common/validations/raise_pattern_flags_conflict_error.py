import re
from typing import NoReturn
from simplibs.exception import ParamError


def raise_pattern_flags_conflict_error(
    pattern: re.Pattern,
    flags: int,
) -> NoReturn:
    """Raise ParamError when flags are given together with an already compiled pattern.

    Args:
        pattern: The compiled pattern that was passed (a `RegexPattern` arrives as its `re.Pattern`).
        flags: The rejected flags.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_PATTERN_FLAGS_CONFLICT",
        label="flags",
        value=flags,
        problem=(
            f"Flags were given together with the compiled pattern {pattern.pattern!r}.",
            "A compiled pattern already carries its flags, so these would be ignored.",
        ),
        expected="flags=0 with a compiled pattern, or flags with a str / Regex pattern.",
        how_to_fix=(
            "Put the flags into the pattern: re.compile(source, flags) or RegexPattern(tree, flags=...).",
            "Or pass the pattern as a str or a Regex tree and keep flags=...",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_pattern_flags_conflict_error — Flags Nobody Would Read

## Purpose
`re.compile(pattern_object, flags)` fails in the standard library. Here the
combination is refused for the same reason but with a card that names both ways out.

## `RegexPattern`
`compile_pattern` hands over the `re.Pattern` held inside it, so the card shows
the rendered source and the first way out names `RegexPattern(tree, flags=...)`
next to `re.compile`.
"""
