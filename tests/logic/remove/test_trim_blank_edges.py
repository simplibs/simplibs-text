import pytest
from simplibs.text.logic.remove import trim_blank_edges


@pytest.mark.parametrize(
    "text, expected",
    [
        ("\n\na\nb\n\n", "a\nb\n"),
        ("\na", "a"),
        ("a\n\n", "a\n"),
        ("a\n\n\n", "a\n"),
        ("  \n\t\na\n \n", "a\n"),
        ("  a\n\n", "  a\n"),
    ],
    ids=["both-edges", "start-only", "end-only", "several-at-end", "whitespace-lines", "indent-kept"],
)
def test_trim_blank_edges_removes_blank_lines_at_both_ends(text, expected) -> None:
    """Blank means empty or whitespace-only."""
    assert trim_blank_edges(text) == expected


def test_trim_blank_edges_leaves_the_inside_alone() -> None:
    """Blank lines between content stay."""
    assert trim_blank_edges("\na\n\n\nb\n\n") == "a\n\n\nb\n"


@pytest.mark.parametrize("text", ["", "\n", "\n\n\n", "  \n \t\n", "   "])
def test_trim_blank_edges_a_text_of_blank_lines_becomes_empty(text) -> None:
    """Nothing is left."""
    assert trim_blank_edges(text) == ""


@pytest.mark.parametrize("text", ["a", "a\n", "a\n\nb", "\ta\n b\n"])
def test_trim_blank_edges_nothing_to_trim_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert trim_blank_edges(probe) is probe


@pytest.mark.parametrize("text", ["\n\na\n\n", "  \na\n  ", "\n"])
def test_trim_blank_edges_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = trim_blank_edges(text)
    assert trim_blank_edges(once) == once
