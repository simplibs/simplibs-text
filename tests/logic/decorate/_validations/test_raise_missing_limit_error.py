from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic.decorate._validations import raise_missing_limit_error


def test_raise_missing_limit_error_contract(subtests) -> None:
    """Verify raise_missing_limit_error produces a well-formed ParamError card."""

    exc = assert_exception_function(
        subtests,
        raise_missing_limit_error,
        invalid_params=(),
        exception_type=ParamError,
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
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
