from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import ReplacePunctuation
from simplibs.text.logic.clean import replace_punctuation

SAMPLES = ['a,b', 'a b', '!']


def test_replace_punctuation_contract(subtests) -> None:
    """Verify the execution and construction contract of the ReplacePunctuation action."""
    assert_action(
        subtests,
        ReplacePunctuation(replacement="_"),
        valid_values=SAMPLES,
        expected_outputs=['a_b', 'a b', '_'],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=ReplacePunctuation,
        invalid_init_params=[((), {"replacement": 5}), ((), {"replacement": None})],
        verbose=False,
    )


def test_replace_punctuation_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = ReplacePunctuation(replacement="_")

    for text in SAMPLES:
        assert action(text) == replace_punctuation(text, replacement="_")
