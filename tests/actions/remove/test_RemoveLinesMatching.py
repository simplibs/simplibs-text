from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import RemoveLinesMatching
from simplibs.text.logic.remove import remove_lines_matching

SAMPLES = ['a\nTODO\nb', 'none', 'TODO']


def test_remove_lines_matching_contract(subtests) -> None:
    """Verify the execution and construction contract of the RemoveLinesMatching action."""
    assert_action(
        subtests,
        RemoveLinesMatching(pattern="TODO"),
        valid_values=SAMPLES,
        expected_outputs=['a\nb', 'none', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=RemoveLinesMatching,
        invalid_init_params=[((), {}), ((), {"pattern": ""}), ((), {"pattern": 5}), ((), {"pattern": "a", "flags": "x"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError],
        verbose=False,    )


def test_remove_lines_matching_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = RemoveLinesMatching(pattern="TODO")

    for text in SAMPLES:
        assert action(text) == remove_lines_matching(text, pattern="TODO")
