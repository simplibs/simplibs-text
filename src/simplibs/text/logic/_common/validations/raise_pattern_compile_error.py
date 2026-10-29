import re
from typing import NoReturn
from simplibs.exception import ParamError


def raise_pattern_compile_error(
    source: str,
    caught_exc: re.error | ValueError,
) -> NoReturn:
    """Raise ParamError when a pattern cannot be compiled.

    Args:
        source: The regex source that was handed to `re.compile`.
        caught_exc: The `re.error` or `ValueError` that was caught.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_PATTERN_COMPILE_FAILED",
        label="pattern",
        value=source,
        problem=(
            f"The pattern {source!r} cannot be compiled.",
            f"{type(caught_exc).__name__}: {caught_exc}.",
        ),
        expected="A pattern and flags that `re.compile` accepts.",
        how_to_fix=(
            "Check the pattern and the flags (e.g. re.LOCALE cannot be used with a str pattern).",
            "Pass plain text as a str: it is searched for literally, so nothing needs escaping.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_pattern_compile_error — a Pattern `re` Refuses

## Purpose
A literal `str` is escaped and a `re.Pattern` is already compiled, so only a
`Regex` tree or an odd flag combination can end here. The card shows the
rendered source, which is what the caller usually cannot see.
"""
