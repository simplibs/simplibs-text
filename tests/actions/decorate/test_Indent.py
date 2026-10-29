from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import Indent
from simplibs.text.logic.decorate import indent

SAMPLES = ['a\nb', '  x', '']


def test_indent_contract(subtests) -> None:
    """Verify the execution and construction contract of the Indent action."""
    assert_action(
        subtests,
        Indent(prefix=2),
        valid_values=SAMPLES,
        expected_outputs=['  a\n  b', '    x', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=Indent,
        invalid_init_params=[((), {"prefix": -1}), ((), {"prefix": None}), ((), {"prefix": 1.5})],
        verbose=False,
    )


def test_indent_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = Indent(prefix=2)

    for text in SAMPLES:
        assert action(text) == indent(text, prefix=2)
