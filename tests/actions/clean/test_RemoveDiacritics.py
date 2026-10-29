from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveDiacritics
from simplibs.text.logic.clean import remove_diacritics

SAMPLES = ['P\u0159\xedli\u0161, caf\xe9!', 'plain', '']


def test_remove_diacritics_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveDiacritics action."""
    assert_action(
        subtests,
        RemoveDiacritics(),
        valid_values=SAMPLES,
        expected_outputs=['Prilis, cafe!', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_remove_diacritics_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveDiacritics()

    for text in SAMPLES:
        assert action(text) == remove_diacritics(text)
