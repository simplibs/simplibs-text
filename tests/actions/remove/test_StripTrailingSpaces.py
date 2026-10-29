from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import StripTrailingSpaces
from simplibs.text.logic.remove import strip_trailing_spaces

SAMPLES = ['  a  \n\n  b  \n\n', 'plain', '']


def test_strip_trailing_spaces_contract(subtests) -> None:
    """Verify the execution and construction contract of the StripTrailingSpaces action."""
    assert_action(
        subtests,
        StripTrailingSpaces(),
        valid_values=SAMPLES,
        expected_outputs=['  a\n\n  b\n\n', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_strip_trailing_spaces_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = StripTrailingSpaces()

    for text in SAMPLES:
        assert action(text) == strip_trailing_spaces(text)
