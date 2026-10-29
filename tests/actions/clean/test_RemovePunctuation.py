from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemovePunctuation
from simplibs.text.logic.clean import remove_punctuation

SAMPLES = ['P\u0159\xedli\u0161, caf\xe9!', 'plain', '']


def test_remove_punctuation_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemovePunctuation action."""
    assert_action(
        subtests,
        RemovePunctuation(),
        valid_values=SAMPLES,
        expected_outputs=['P\u0159\xedli\u0161 caf\xe9', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_remove_punctuation_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemovePunctuation()

    for text in SAMPLES:
        assert action(text) == remove_punctuation(text)
