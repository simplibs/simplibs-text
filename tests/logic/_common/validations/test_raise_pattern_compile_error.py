import re
import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic._common.validations import raise_pattern_compile_error


@pytest.mark.parametrize(
    "source, caught_exc",
    [
        ("(", re.error("missing ), unterminated subpattern")),
        ("a{2,1}", re.error("min repeat greater than max repeat")),
        ("a", ValueError("cannot use LOCALE flag with a str pattern")),
    ],
    ids=["re.error-paren", "re.error-repeat", "ValueError-flags"],
)
def test_raise_pattern_compile_error_contract(subtests, source, caught_exc) -> None:
    """Verify raise_pattern_compile_error produces a well-formed ParamError card."""

    def raising_wrapper(rejected):
        raise_pattern_compile_error(rejected, caught_exc)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(source,),
        exception_type=ParamError,
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
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
