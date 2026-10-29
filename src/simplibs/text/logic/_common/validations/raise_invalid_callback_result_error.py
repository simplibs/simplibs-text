from collections.abc import Callable
from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_invalid_callback_result_error(
    func: Callable[..., Any],
    result: Any,
    context: str,
) -> NoReturn:
    """Raise ParamError when a function given by the caller returns something other than text.

    Args:
        func: The caller's function.
        result: What it returned.
        context: Where it happened, in a few words ("line 3", "the match at 12").
    """

    # 1. Name of the function as the caller knows it
    name = getattr(func, "__name__", repr(func))

    # 2. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="TEXT_CALLBACK_RESULT_INVALID",
        label=f"result of '{name}'",
        value=result,
        problem=(
            f"The function returned {type(result).__name__} for {context}.",
            "Text steps work with text, so the function must return a str.",
        ),
        expected="A str (it may be empty).",
        how_to_fix=(
            "Return a str on every path of the function, including the 'nothing to change' one.",
            "A function without a return statement returns None.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_invalid_callback_result_error — a Function That Forgot to Return

## Purpose
`map_lines` and `replace_matches` call a function supplied by the caller. If it
returns `None` (a forgotten `return`) the standard library fails deep inside
`re.sub` or `str.join` with a message about internals. Here the card names the
function and the place where it went wrong.
"""
