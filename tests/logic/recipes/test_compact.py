import random
import pytest
from simplibs.text.logic.recipes import compact
from simplibs.text.logic.remove import remove_empty_lines, strip_trailing_spaces, trim_blank_edges


def _random_texts(count: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    return ["".join(rng.choice("ab \t\n") for _ in range(rng.randint(0, 16))) for _ in range(count)]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a  \n\n b \n\n", "a\n b\n"),
        ("a\n\n\n\nb", "a\nb"),
        ("\n\na\n\n", "a\n"),
        ("a\n  \n\t\nb", "a\nb"),
        ("   ", ""),
        ("\n\n", ""),
        ("", ""),
        ("a", "a"),
    ],
)
def test_compact_strips_line_ends_and_removes_every_blank_line(text, expected) -> None:
    """The shortest form a text can have without touching its content."""
    assert compact(text) == expected


@pytest.mark.parametrize("text", ["a\nb\n", "a", "  a\n  b"])
def test_compact_a_compact_text_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert compact(probe) is probe


def test_compact_is_the_two_steps_in_order() -> None:
    """Line ends first, so a line of spaces counts as blank in the next step."""
    for text in _random_texts(400, 20):
        assert compact(text) == remove_empty_lines(strip_trailing_spaces(text)), repr(text)


def test_compact_running_it_twice_gives_the_same_result() -> None:
    """Idempotent, for any text."""
    for text in _random_texts(500, 21):
        once = compact(text)
        assert compact(once) == once, repr(text)


def test_compact_the_result_has_no_blank_line_and_no_trailing_space() -> None:
    """The promised shape."""
    for text in _random_texts(500, 22):
        result = compact(text)
        body = result[:-1] if result.endswith("\n") else result
        if result:
            assert all(line.strip() != "" for line in body.split("\n")), repr(text)
        assert all(line == line.rstrip(" \t") for line in result.split("\n")), repr(text)


def test_compact_there_is_nothing_left_for_trim_blank_edges_to_trim() -> None:
    """The reason `COMPACT` has no `TrimBlankEdges` step."""
    for text in _random_texts(1000, 23):
        once = remove_empty_lines(text)
        assert trim_blank_edges(once) == once, repr(text)
