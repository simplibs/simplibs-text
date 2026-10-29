from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import SplitWords
from simplibs.text.logic.case import split_words

SAMPLES = ['myVarName', 'my var', '']


def test_split_words_contract(subtests) -> None:
    """Verify the execution and construction contract of the SplitWords action."""
    assert_action(
        subtests,
        SplitWords(),
        valid_values=SAMPLES,
        expected_outputs=[['my', 'Var', 'Name'], ['my', 'var'], []],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=list[str],
        verbose=False,
    )


def test_split_words_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = SplitWords()

    for text in SAMPLES:
        assert action(text) == split_words(text)
