from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import ToSnakeCase
from simplibs.text.logic.case import to_snake_case

SAMPLES = ['myVarName', 'my var', '']


def test_to_snake_case_contract(subtests) -> None:
    """Verify the execution and construction contract of the ToSnakeCase action."""
    assert_action(
        subtests,
        ToSnakeCase(),
        valid_values=SAMPLES,
        expected_outputs=['my_var_name', 'my_var', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_to_snake_case_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = ToSnakeCase()

    for text in SAMPLES:
        assert action(text) == to_snake_case(text)
