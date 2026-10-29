import random
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.logic.recipes import cleanup_whitespace
from simplibs.text.presets import CLEANUP_WHITESPACE

SAMPLES = ["\n\n  a  \n\n\n\nb\t\n\n", "tidy\n\ntext\n", "", "   \n"]


def test_cleanup_whitespace_preset_contract(subtests) -> None:
    """Verify the execution contract of the CLEANUP_WHITESPACE chain."""
    assert_action(
        subtests,
        CLEANUP_WHITESPACE,
        valid_values=SAMPLES,
        expected_outputs=["  a\n\nb\n", "tidy\n\ntext\n", "", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_cleanup_whitespace_preset_gives_what_the_function_gives() -> None:
    """The chain and `cleanup_whitespace` are two spellings of one thing."""
    rng = random.Random(30)
    for _ in range(300):
        text = "".join(rng.choice("ab \t\n") for _ in range(rng.randint(0, 16)))
        assert CLEANUP_WHITESPACE(text) == cleanup_whitespace(text), repr(text)


def test_cleanup_whitespace_preset_can_be_used_again_and_again() -> None:
    """One shared chain holds no state between calls."""
    first = CLEANUP_WHITESPACE("a  \n\n\n\nb")
    assert CLEANUP_WHITESPACE("x \n\n\n\ny") == "x\n\ny"
    assert CLEANUP_WHITESPACE("a  \n\n\n\nb") == first == "a\n\nb"
