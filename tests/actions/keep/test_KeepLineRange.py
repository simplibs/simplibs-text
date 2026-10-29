from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import KeepLineRange
from simplibs.text.logic.keep import keep_line_range

SAMPLES = ['a\nb\nc\nd', 'one', '']


def test_keep_line_range_contract(subtests) -> None:
    """Verify the execution and construction contract of the KeepLineRange action."""
    assert_action(
        subtests,
        KeepLineRange(start=2, end=3),
        valid_values=SAMPLES,
        expected_outputs=['b\nc', '', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=KeepLineRange,
        invalid_init_params=[((), {"start": 0}), ((), {"start": "x"}), ((), {"end": 0}), ((), {"end": "x"})],
        verbose=False,
    )


def test_keep_line_range_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = KeepLineRange(start=2, end=3)

    for text in SAMPLES:
        assert action(text) == keep_line_range(text, start=2, end=3)
