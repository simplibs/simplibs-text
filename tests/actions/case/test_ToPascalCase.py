from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import ToPascalCase
from simplibs.text.logic.case import to_pascal_case

SAMPLES = ['myVarName', 'my var', '']


def test_to_pascal_case_contract(subtests) -> None:
    """Verify the execution and construction contract of the ToPascalCase action."""
    assert_action(
        subtests,
        ToPascalCase(),
        valid_values=SAMPLES,
        expected_outputs=['MyVarName', 'MyVar', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_to_pascal_case_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = ToPascalCase()

    for text in SAMPLES:
        assert action(text) == to_pascal_case(text)
