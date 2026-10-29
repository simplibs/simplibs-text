import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic._common.validations import raise_invalid_callback_result_error


def _shout(line: str) -> str:
    return line.upper()


class _Callable:
    """A callable object that has no `__name__`."""

    def __call__(self, line: str) -> str:
        return line

    def __repr__(self) -> str:
        return "<my callable>"


@pytest.mark.parametrize(
    "func, expected_name",
    [
        (_shout, "_shout"),
        (lambda line: line, "<lambda>"),
        (_Callable(), "<my callable>"),
    ],
    ids=["function", "lambda", "object-without-name"],
)
@pytest.mark.parametrize(
    "result, context",
    [
        (None, "line 3"),
        (5, "the match at 12"),
        (["a"], "line 1"),
        (b"x", "the match at 0"),
    ],
    ids=["None", "int", "list", "bytes"],
)
def test_raise_invalid_callback_result_error_contract(
    subtests, func, expected_name, result, context,
) -> None:
    """Verify raise_invalid_callback_result_error produces a well-formed ParamError card."""

    def raising_wrapper(rejected_func, rejected_result, where):
        raise_invalid_callback_result_error(rejected_func, rejected_result, where)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(func, result, context),
        exception_type=ParamError,
        error_name="TEXT_CALLBACK_RESULT_INVALID",
        label=f"result of '{expected_name}'",
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
        verbose=False,
    )

    # The wrapped standard type is TypeError: the function gave the wrong type
    assert isinstance(exc, TypeError)
