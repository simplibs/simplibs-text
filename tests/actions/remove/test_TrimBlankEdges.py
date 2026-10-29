from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.text.actions import TrimBlankEdges
from simplibs.text.logic.remove import trim_blank_edges

SAMPLES = ['  a  \n\n  b  \n\n', 'plain', '']


def test_trim_blank_edges_contract(subtests) -> None:
    """Verify the execution and construction contract of the TrimBlankEdges action."""
    assert_action(
        subtests,
        TrimBlankEdges(),
        valid_values=SAMPLES,
        expected_outputs=['  a  \n\n  b  \n', 'plain', ''],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_trim_blank_edges_gives_what_the_function_gives() -> None:
    """The action is the function in a pipeline step: same text in, same result out."""
    action = TrimBlankEdges()

    for text in SAMPLES:
        assert action(text) == trim_blank_edges(text)
