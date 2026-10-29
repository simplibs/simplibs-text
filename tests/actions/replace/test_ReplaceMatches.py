from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import ReplaceMatches
from simplibs.text.logic.replace import replace_matches

SAMPLES = ['aaa', 'xyz', 'a.a']


def test_replace_matches_contract(subtests) -> None:
    """Verify the execution and construction contract of the ReplaceMatches action."""
    assert_action(
        subtests,
        ReplaceMatches(pattern="a", replacement="b"),
        valid_values=SAMPLES,
        expected_outputs=['bbb', 'xyz', 'b.b'],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=ReplaceMatches,
        invalid_init_params=[((), {}), ((), {"pattern": "a"}), ((), {"pattern": "", "replacement": "x"}), ((), {"pattern": "a", "replacement": 5}), ((), {"pattern": "a", "replacement": "b", "count": -1}), ((), {"pattern": "a", "replacement": "b", "flags": "x"})],
        construction_exception_type=[TypeError, TypeError, ValidationError, ValidationError, ValidationError, ValidationError],
        verbose=False,    )


def test_replace_matches_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = ReplaceMatches(pattern="a", replacement="b")

    for text in SAMPLES:
        assert action(text) == replace_matches(text, pattern="a", replacement="b")
