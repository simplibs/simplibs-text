import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic.remove._validations import raise_invalid_span_error


@pytest.mark.parametrize(
    "span, index, text_length",
    [
        ((-1, 2), 0, 10),
        ((3, 2), 2, 10),
        ((0, 11), 1, 10),
        ((11, 12), 0, 10),
        ((0, 1), 0, 0),
    ],
)
def test_raise_invalid_span_error_contract(subtests, span, index, text_length) -> None:
    """Verify raise_invalid_span_error produces a well-formed ParamError card."""

    def raising_wrapper(rejected):
        raise_invalid_span_error(rejected, index, text_length)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(span,),
        exception_type=ParamError,
        error_name="TEXT_SPAN_INVALID",
        label=f"spans[{index}]",
        value=span,
        problem=(
            f"The span {span!r} does not fit into a text of {text_length} characters.",
            "A span is a half-open range: start is included, end is not.",
        ),
        expected=f"0 <= start <= end <= {text_length}",
        how_to_fix=(
            "Make sure the spans were measured on exactly this text.",
            "If the text was changed after measuring (e.g. stripped), measure again.",
        ),
        exception=ValueError,
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
