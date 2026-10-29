from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import Wrap
from simplibs.text.logic.decorate import wrap

SAMPLES = ['aaa bbb ccc', 'short', '']


def test_wrap_contract(subtests) -> None:
    """Verify the execution and construction contract of the Wrap action."""
    assert_action(
        subtests,
        Wrap(width=5),
        valid_values=SAMPLES,
        expected_outputs=['aaa\nbbb\nccc', 'short', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=Wrap,
        invalid_init_params=[((), {"width": 0}), ((), {"width": "x"}), ((), {"break_long_words": "x"})],
        verbose=False,
    )


def test_wrap_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = Wrap(width=5)

    for text in SAMPLES:
        assert action(text) == wrap(text, width=5)
