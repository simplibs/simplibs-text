from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import KeepBetween
from simplibs.text.logic.keep import keep_between

SAMPLES = ['[a] x [b]', 'no markers', '']


def test_keep_between_contract(subtests) -> None:
    """Verify the execution and construction contract of the KeepBetween action."""
    assert_action(
        subtests,
        KeepBetween(start="[", end="]"),
        valid_values=SAMPLES,
        expected_outputs=['[a]\n[b]', '', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=KeepBetween,
        invalid_init_params=[((), {}), ((), {"start": "", "end": "]"}), ((), {"start": "[", "end": 5}), ((), {"start": "[", "end": "]", "include_markers": "x"}), ((), {"start": "[", "end": "]", "flags": "x"}), ((), {"start": "[", "end": "]", "separator": 5})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError, ValidationError, ValidationError],
        verbose=False,
    )


def test_keep_between_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = KeepBetween(start="[", end="]")

    for text in SAMPLES:
        assert action(text) == keep_between(text, start="[", end="]")
