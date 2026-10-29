from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import Dedent
from simplibs.text.logic.remove import dedent

SAMPLES = ['  a  \n\n  b  \n\n', 'plain', '']


def test_dedent_contract(subtests) -> None:
    """Verify the execution and construction contract of the Dedent action."""
    assert_action(
        subtests,
        Dedent(),
        valid_values=SAMPLES,
        expected_outputs=['a  \n\nb  \n\n', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_dedent_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = Dedent()

    for text in SAMPLES:
        assert action(text) == dedent(text)
