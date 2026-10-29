import pytest
from simplibs.actions.testing import assert_action
from simplibs.exception import ParamError, ValidationError
from simplibs.text.actions import Truncate
from simplibs.text.logic.decorate import truncate

SAMPLES = ['a\nb\nc', 'short', '']


def test_truncate_contract(subtests) -> None:
    """Verify the execution and construction contract of the Truncate action."""
    assert_action(
        subtests,
        Truncate(max_lines=1),
        valid_values=SAMPLES,
        expected_outputs=['a\n\u2026 (truncated)', 'short', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=Truncate,
        invalid_init_params=[((), {"max_lines": 0}), ((), {"max_chars": "x"}), ((), {"max_chars": 0}), ((), {"marker": 5})],
        verbose=False,
    )


def test_truncate_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = Truncate(max_lines=1)

    for text in SAMPLES:
        assert action(text) == truncate(text, max_lines=1)


def test_truncate_without_a_limit_fails_when_it_is_called_not_when_it_is_built() -> None:
    """The limit is checked by the function, so `Truncate()` can be built and only its use is refused."""
    step = Truncate()
    with pytest.raises(ParamError):
        step("abc")
