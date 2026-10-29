from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveEmptyLines
from simplibs.text.logic.remove import remove_empty_lines

SAMPLES = ['  a  \n\n  b  \n\n', 'plain', '']


def test_remove_empty_lines_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveEmptyLines action."""
    assert_action(
        subtests,
        RemoveEmptyLines(),
        valid_values=SAMPLES,
        expected_outputs=['  a  \n  b  \n', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_remove_empty_lines_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveEmptyLines()

    for text in SAMPLES:
        assert action(text) == remove_empty_lines(text)
