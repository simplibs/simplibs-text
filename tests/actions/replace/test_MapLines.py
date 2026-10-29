import pytest
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import MapLines
from simplibs.text.logic.replace import map_lines

SAMPLES = ['a\nb', 'X', '']


def test_map_lines_contract(subtests) -> None:
    """Verify the execution and construction contract of the MapLines action."""
    assert_action(
        subtests,
        MapLines(func=str.upper),
        valid_values=SAMPLES,
        expected_outputs=['A\nB', 'X', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=MapLines,
        invalid_init_params=[((), {}), ((), {"func": 5}), ((), {"func": "upper"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError],
        verbose=False,    )


def test_map_lines_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = MapLines(func=str.upper)

    for text in SAMPLES:
        assert action(text) == map_lines(text, func=str.upper)


def test_map_lines_the_function_is_called_for_every_line() -> None:
    """The configured function is the one the action uses."""
    seen: list[str] = []

    def remember(line: str) -> str:
        seen.append(line)
        return line

    MapLines(func=remember)("a\n\nb\n")

    assert seen == ["a", "", "b"]
