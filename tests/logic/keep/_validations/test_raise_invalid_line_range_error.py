import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic.keep._validations import raise_invalid_line_range_error


@pytest.mark.parametrize("start, end", [(5, 3), (2, 1), (10, 9), (1000, 1)])
def test_raise_invalid_line_range_error_contract(subtests, start, end) -> None:
    """Verify raise_invalid_line_range_error produces a well-formed ParamError card."""

    def raising_wrapper(rejected_end):
        raise_invalid_line_range_error(start, rejected_end)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(end,),
        exception_type=ParamError,
        error_name="TEXT_LINE_RANGE_INVALID",
        label="end",
        value=end,
        problem=(
            f"The range ends at line {end} but starts at line {start}.",
            "Both ends are counted from 1 and both are included.",
        ),
        expected=f"end >= start ({start}), or None for 'to the last line'.",
        how_to_fix=(
            "Swap the values if they were passed the other way round.",
            "Use end=None to keep everything from the start line on.",
        ),
        exception=ValueError,
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
