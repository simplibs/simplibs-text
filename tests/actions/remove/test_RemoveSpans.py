from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveSpans
from simplibs.text.logic.remove import remove_spans

SAMPLES = ['abc', 'xy', '\nabc']


def test_remove_spans_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveSpans action."""
    assert_action(
        subtests,
        RemoveSpans(spans=[(0, 1)]),
        valid_values=SAMPLES,
        expected_outputs=['bc', 'y', 'abc'],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=RemoveSpans,
        invalid_init_params=[((), {}), ((), {"spans": 5}), ((), {"spans": [(1, 2, 3)]}), ((), {"spans": ["ab"]}), ((), {"spans": [(0, 1)], "drop_emptied_lines": "x"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError, ValidationError],
        verbose=False,    )


def test_remove_spans_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveSpans(spans=[(0, 1)])

    for text in SAMPLES:
        assert action(text) == remove_spans(text, spans=[(0, 1)])
