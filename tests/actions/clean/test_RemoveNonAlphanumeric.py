from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveNonAlphanumeric
from simplibs.text.logic.clean import remove_non_alphanumeric

SAMPLES = ['a-b c', 'abc', '\n!']


def test_remove_non_alphanumeric_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveNonAlphanumeric action."""
    assert_action(
        subtests,
        RemoveNonAlphanumeric(keep_whitespace=False),
        valid_values=SAMPLES,
        expected_outputs=['abc', 'abc', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=RemoveNonAlphanumeric,
        invalid_init_params=[((), {"keep_whitespace": "x"}), ((), {"keep_whitespace": None})],
        verbose=False,
    )


def test_remove_non_alphanumeric_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveNonAlphanumeric(keep_whitespace=False)

    for text in SAMPLES:
        assert action(text) == remove_non_alphanumeric(text, keep_whitespace=False)
