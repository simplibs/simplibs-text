from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import SqueezeBlankLines
from simplibs.text.logic.remove import squeeze_blank_lines

SAMPLES = ['a\n\n\n\nb', 'a\nb', '']


def test_squeeze_blank_lines_contract(subtests) -> None:
    """Verify the execution and construction contract of the SqueezeBlankLines action."""
    assert_action(
        subtests,
        SqueezeBlankLines(max_consecutive=2),
        valid_values=SAMPLES,
        expected_outputs=['a\n\n\nb', 'a\nb', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=SqueezeBlankLines,
        invalid_init_params=[((), {"max_consecutive": -1}), ((), {"max_consecutive": "x"}), ((), {"max_consecutive": None})],
        verbose=False,
    )


def test_squeeze_blank_lines_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = SqueezeBlankLines(max_consecutive=2)

    for text in SAMPLES:
        assert action(text) == squeeze_blank_lines(text, max_consecutive=2)
