from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import KeepLinesMatching
from simplibs.text.logic.keep import keep_lines_matching

SAMPLES = ['a\nb\nab', 'b', 'a\n']


def test_keep_lines_matching_contract(subtests) -> None:
    """Verify the execution and construction contract of the KeepLinesMatching action."""
    assert_action(
        subtests,
        KeepLinesMatching(pattern="a"),
        valid_values=SAMPLES,
        expected_outputs=['a\nab', '', 'a\n'],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=KeepLinesMatching,
        invalid_init_params=[((), {}), ((), {"pattern": ""}), ((), {"pattern": 5}), ((), {"pattern": "a", "flags": "x"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError],
        verbose=False,
    )


def test_keep_lines_matching_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = KeepLinesMatching(pattern="a")

    for text in SAMPLES:
        assert action(text) == keep_lines_matching(text, pattern="a")
