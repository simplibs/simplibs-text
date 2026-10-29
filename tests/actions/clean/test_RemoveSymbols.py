from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveSymbols
from simplibs.text.logic.clean import remove_symbols

SAMPLES = ['P\u0159\xedli\u0161, caf\xe9!', 'plain', '']


def test_remove_symbols_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveSymbols action."""
    assert_action(
        subtests,
        RemoveSymbols(),
        valid_values=SAMPLES,
        expected_outputs=['P\u0159\xedli\u0161, caf\xe9!', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_remove_symbols_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveSymbols()

    for text in SAMPLES:
        assert action(text) == remove_symbols(text)
