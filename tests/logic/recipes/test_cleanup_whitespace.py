import random
import pytest
from simplibs.text.logic.recipes import cleanup_whitespace
from simplibs.text.logic.remove import squeeze_blank_lines, strip_trailing_spaces, trim_blank_edges


def _random_texts(count: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    return ["".join(rng.choice("ab \t\n") for _ in range(rng.randint(0, 16))) for _ in range(count)]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a  \nb\t\n", "a\nb\n"),
        ("\n\na\n\n\n\nb\n\n", "a\n\nb\n"),
        ("a\n  \n\t\nb", "a\n\nb"),
        ("  a  \n\n\n\nb\t\n", "  a\n\nb\n"),
        ("   ", ""),
        ("\n\n\n", ""),
        ("", ""),
    ],
)
def test_cleanup_whitespace_tidies_line_ends_blank_runs_and_edges(text, expected) -> None:
    """No trailing spaces, one blank line at most between blocks, none at the start or the end."""
    assert cleanup_whitespace(text) == expected


@pytest.mark.parametrize("text", ["a\n\nb\n", "a", "a\nb", "  a\n\n  b\n"])
def test_cleanup_whitespace_a_tidy_text_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert cleanup_whitespace(probe) is probe


def test_cleanup_whitespace_is_the_three_steps_in_order() -> None:
    """Line ends first, so a line of spaces counts as blank in the next step."""
    for text in _random_texts(400, 10):
        expected = trim_blank_edges(squeeze_blank_lines(strip_trailing_spaces(text), 1))
        assert cleanup_whitespace(text) == expected, repr(text)


def test_cleanup_whitespace_running_it_twice_gives_the_same_result() -> None:
    """Idempotent, for any text."""
    for text in _random_texts(500, 11):
        once = cleanup_whitespace(text)
        assert cleanup_whitespace(once) == once, repr(text)


def test_cleanup_whitespace_the_result_has_the_promised_shape() -> None:
    """No two blank lines in a row, no blank line at the edges, no trailing space or tab."""
    for text in _random_texts(500, 12):
        result = cleanup_whitespace(text)
        assert "\n\n\n" not in result, repr(text)
        if result:
            lines = result.rstrip("\n").split("\n")
            assert lines[0].strip() != "" and lines[-1].strip() != "", repr(text)
        assert all(line == line.rstrip(" \t") for line in result.split("\n")), repr(text)
