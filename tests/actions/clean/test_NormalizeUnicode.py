from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import NormalizeUnicode
from simplibs.text.logic.clean import normalize_unicode

SAMPLES = ['\xe9', 'abc', '']


def test_normalize_unicode_contract(subtests) -> None:
    """Verify the execution and construction contract of the NormalizeUnicode action."""
    assert_action(
        subtests,
        NormalizeUnicode(form="NFD"),
        valid_values=SAMPLES,
        expected_outputs=['e\u0301', 'abc', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=NormalizeUnicode,
        invalid_init_params=[((), {"form": "nfc"}), ((), {"form": 5}), ((), {"form": None})],
        verbose=False,
    )


def test_normalize_unicode_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = NormalizeUnicode(form="NFD")

    for text in SAMPLES:
        assert action(text) == normalize_unicode(text, form="NFD")
