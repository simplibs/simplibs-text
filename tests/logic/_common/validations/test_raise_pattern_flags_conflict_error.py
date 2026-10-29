import re
import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.text.logic._common.validations import raise_pattern_flags_conflict_error


@pytest.mark.parametrize("source", ["a", "a+b", "(?i)x"])
@pytest.mark.parametrize("flags", [re.IGNORECASE, re.IGNORECASE | re.MULTILINE])
def test_raise_pattern_flags_conflict_error_contract(subtests, source, flags) -> None:
    """Verify raise_pattern_flags_conflict_error produces a well-formed ParamError card."""

    pattern = re.compile(source)

    def raising_wrapper(rejected_pattern, rejected_flags):
        raise_pattern_flags_conflict_error(rejected_pattern, rejected_flags)

    exc = assert_exception_function(
        subtests,
        raising_wrapper,
        invalid_params=(pattern, flags),
        exception_type=ParamError,
        error_name="TEXT_PATTERN_FLAGS_CONFLICT",
        label="flags",
        value=flags,
        problem=(
            f"Flags were given together with the compiled pattern {source!r}.",
            "A compiled pattern already carries its flags, so these would be ignored.",
        ),
        expected="flags=0 with a compiled pattern, or flags with a str / Regex pattern.",
        how_to_fix=(
            "Put the flags into the pattern: re.compile(source, flags) or RegexPattern(tree, flags=...).",
            "Or pass the pattern as a str or a Regex tree and keep flags=...",
        ),
        exception=ValueError,
        verbose=False,
    )

    # A caller can catch the wrapped standard type
    assert isinstance(exc, ValueError)
