from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import AddLineNumbers
from simplibs.text.logic.decorate import add_line_numbers

SAMPLES = ['a\nb', 'x', '']


def test_add_line_numbers_contract(subtests) -> None:
    """Verify the execution and construction contract of the AddLineNumbers action."""
    assert_action(
        subtests,
        AddLineNumbers(start=5),
        valid_values=SAMPLES,
        expected_outputs=['5: a\n6: b', '5: x', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=AddLineNumbers,
        invalid_init_params=[((), {"start": -1}), ((), {"start": "x"}), ((), {"template": 5}), ((), {"width": 0}), ((), {"width": "x"})],
        verbose=False,
    )


def test_add_line_numbers_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = AddLineNumbers(start=5)

    for text in SAMPLES:
        assert action(text) == add_line_numbers(text, start=5)
