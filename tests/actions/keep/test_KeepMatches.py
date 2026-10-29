import re
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import KeepMatches
from simplibs.text.logic.keep import keep_matches

SAMPLES = ['a1b22', 'none', '']


def test_keep_matches_contract(subtests) -> None:
    """Verify the execution and construction contract of the KeepMatches action."""
    assert_action(
        subtests,
        KeepMatches(pattern=re.compile(r"\d+")),
        valid_values=SAMPLES,
        expected_outputs=['1\n22', '', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=KeepMatches,
        invalid_init_params=[((), {}), ((), {"pattern": ""}), ((), {"pattern": 5}), ((), {"pattern": "a", "separator": 5}), ((), {"pattern": "a", "flags": "x"})],
        construction_exception_type=[TypeError, ValidationError, ValidationError, ValidationError, ValidationError],
        verbose=False,    )


def test_keep_matches_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = KeepMatches(pattern=re.compile(r"\d+"))

    for text in SAMPLES:
        assert action(text) == keep_matches(text, pattern=re.compile(r"\d+"))
