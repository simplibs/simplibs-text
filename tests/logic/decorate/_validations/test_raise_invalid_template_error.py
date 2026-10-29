import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic.decorate._validations import raise_invalid_template_error


@pytest.mark.parametrize(
    "template, caught_exc",
    [
        ("{foo}", KeyError("foo")),
        ("{0}", IndexError("Replacement index 0 out of range for positional args tuple")),
        ("{", ValueError("Single '{' encountered in format string")),
        ("{number.x}", AttributeError("'int' object has no attribute 'x'")),
    ],
    ids=["KeyError", "IndexError", "ValueError", "AttributeError"],
)
def test_raise_invalid_template_error_contract(subtests, template, caught_exc) -> None:
    """Verify raise_invalid_template_error produces a well-formed ParamError card."""

    def raising_wrapper(rejected):
        raise_invalid_template_error(rejected, caught_exc)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(template,),
        exception_type=ParamError,
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
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
