import random
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.logic.recipes import compact
from simplibs.text.presets import COMPACT

SAMPLES = ["\n\n  a  \n\n\n\nb\t\n\n", "tidy\ntext\n", "", "   \n"]


def test_compact_preset_contract(subtests) -> None:
    """Verify the execution contract of the COMPACT chain."""
    assert_action(
        subtests,
        COMPACT,
        valid_values=SAMPLES,
        expected_outputs=["  a\nb\n", "tidy\ntext\n", "", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_compact_preset_gives_what_the_function_gives() -> None:
    """The chain and `compact` are two spellings of one thing."""
    rng = random.Random(31)
    for _ in range(300):
        text = "".join(rng.choice("ab \t\n") for _ in range(rng.randint(0, 16)))
        assert COMPACT(text) == compact(text), repr(text)


def test_compact_preset_can_be_used_again_and_again() -> None:
    """One shared chain holds no state between calls."""
    first = COMPACT("a  \n\n\n\nb")
    assert COMPACT("x \n\n\n\ny") == "x\ny"
    assert COMPACT("a  \n\n\n\nb") == first == "a\nb"
