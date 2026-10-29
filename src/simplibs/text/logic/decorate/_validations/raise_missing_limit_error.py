from typing import NoReturn
from simplibs.exception import ParamError


def raise_missing_limit_error() -> NoReturn:
    """Raise ParamError when truncate gets no limit at all."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_TRUNCATE_LIMIT_MISSING",
        label="max_lines / max_chars",
        value=None,
        problem=(
            "Neither max_lines nor max_chars was given.",
            "Without a limit there is nothing to truncate to.",
        ),
        expected="max_lines, max_chars, or both.",
        how_to_fix=(
            "Pass max_lines=... to limit the number of lines.",
            "Pass max_chars=... to limit the number of characters.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_missing_limit_error — Truncate to What?

## Purpose
The one check that relates two optional parameters: each may be missing, not
both. Silently returning the text would hide a forgotten argument.
"""
