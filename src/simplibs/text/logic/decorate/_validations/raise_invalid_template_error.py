from typing import NoReturn
from simplibs.exception import ParamError


def raise_invalid_template_error(
    template: str,
    caught_exc: Exception,
) -> NoReturn:
    """Raise ParamError when a line template cannot be filled in.

    Args:
        template: The template that was passed.
        caught_exc: The `KeyError`, `IndexError`, `ValueError` or `AttributeError` raised by `str.format`.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_TEMPLATE_INVALID",
        label="template",
        value=template,
        problem=(
            f"The template {template!r} cannot be filled in.",
            f"{type(caught_exc).__name__}: {caught_exc}.",
        ),
        expected="A str.format template using only {number}, {line} and {width}.",
        how_to_fix=(
            "Use only the fields {number}, {line} and {width}, e.g. '{number:>{width}}: {line}'.",
            "Write a literal brace as '{{' or '}}'.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_template_error — a Template That Does Not Fit

## Purpose
`str.format` reports a wrong field as a bare `KeyError: 'nubmer'`. The card
names the template and the three fields that exist.
"""
