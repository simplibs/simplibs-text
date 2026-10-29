from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveMatches
from simplibs.text.logic.remove import remove_matches

SAMPLES = ['axb', 'abc', 'x\nx\n']


def test_remove_matches_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveMatches action."""
    assert_action(
        subtests,
        RemoveMatches(pattern="x"),
        valid_values=SAMPLES,
        expected_outputs=['ab', 'abc', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=RemoveMatches,
        invalid_init_params=[((), {}), ((), {"pattern": ""}), ((), {"pattern": 5}), ((), {"pattern": "a", "flags": "x"}), ((), {"pattern": "a", "drop_emptied_lines": "x"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError, ValidationError],
        verbose=False,    )


def test_remove_matches_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveMatches(pattern="x")

    for text in SAMPLES:
        assert action(text) == remove_matches(text, pattern="x")
